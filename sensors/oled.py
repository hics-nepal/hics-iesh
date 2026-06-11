import smbus2
from PIL import Image, ImageDraw
from .config import I2C_BUS, OLED_ADDR, OLED_WIDTH, OLED_HEIGHT

try:
    import numpy as _np
except ImportError:
    _np = None


class _OLEDDevice:
    """Direct SH1106 driver using write_i2c_block_data.
    Luma's i2c_rdwr path fails on this display; raw 32-byte chunk writes work.

    Differential rendering: the last framebuffer sent is kept per page, and
    only pages whose bytes changed are rewritten. The SH1106 scans the panel
    continuously while we write, so a full 8-page rewrite shows as a visible
    left-to-right sweep — diffing means steady-state updates (clock, countdown
    bar) touch 1-2 pages and are imperceptible."""

    mode = '1'
    COL_OFFSET = 2  # SH1106 has 132-col driver, visible window starts at col 2

    def __init__(self, port, address, width, height):
        self.size = (width, height)
        self._addr = address
        self._port = port
        self._bus = smbus2.SMBus(port)
        self._pages = height // 8
        self._width = width
        self._last_pages = None  # per-page byte lists from last successful write
        self._init()

    def _cmd(self, *cmds):
        self._bus.write_i2c_block_data(self._addr, 0x00, list(cmds))

    def _data(self, data):
        for i in range(0, len(data), 32):
            self._bus.write_i2c_block_data(self._addr, 0x40, list(data[i:i + 32]))

    def _init(self):
        self._cmd(0xAE)                    # display off
        self._cmd(0xD5, 0x80)              # clock div ratio / osc freq
        self._cmd(0xA8, self.size[1] - 1)  # multiplex ratio
        self._cmd(0xD3, 0x00)              # display offset = 0
        self._cmd(0x40)                    # start line = 0
        self._cmd(0xAD, 0x8B)              # SH1106 DC-DC charge pump ON
        self._cmd(0xA1)                    # seg remap (col 127 = SEG0)
        self._cmd(0xC8)                    # COM scan dec
        self._cmd(0xDA, 0x12)              # COM pins hardware config
        self._cmd(0x81, 0x80)              # contrast
        self._cmd(0xD9, 0x1F)              # precharge period
        self._cmd(0xDB, 0x40)              # VCOM deselect level
        self._cmd(0xA4)                    # all-on resume
        self._cmd(0xA6)                    # normal display
        self._cmd(0xAF)                    # display on

    def _pack(self, image):
        """PIL image → SH1106 page buffers (list of per-page byte lists).
        SH1106 is page-addressed: each byte = 8 vertical pixels in a column,
        LSB at the top. PIL tobytes() is row-major, so we must re-pack."""
        img = image.convert('1')
        w, h = img.size
        if _np is not None:
            a = (_np.asarray(img, dtype=_np.uint8) > 0).astype(_np.uint8)
            a = a.reshape(self._pages, 8, w)
            packed = _np.packbits(a, axis=1, bitorder='little')[:, 0, :]
            return [packed[p].tolist() for p in range(self._pages)]
        pixels = img.load()
        pages = []
        for page in range(self._pages):
            buf = []
            for x in range(w):
                byte = 0
                for bit in range(8):
                    y = page * 8 + bit
                    if y < h and pixels[x, y]:
                        byte |= (1 << bit)
                buf.append(byte)
            pages.append(buf)
        return pages

    def _render(self, image):
        """Write only the pages that differ from the last successful write."""
        pages = self._pack(image)
        lo = 0x00 + (self.COL_OFFSET & 0x0F)
        hi = 0x10 + (self.COL_OFFSET >> 4)
        if self._last_pages is None:
            self._last_pages = [None] * self._pages
        for p, buf in enumerate(pages):
            if self._last_pages[p] == buf:
                continue
            self._cmd(0xB0 | p, lo, hi)
            self._data(buf)
            self._last_pages[p] = buf

    def display(self, image):
        try:
            self._render(image)
        except OSError:
            # Bus stuck: close and reopen. Soft retry avoids display-off/on flash.
            import time as _t
            try:
                self._bus.close()
            except Exception:
                pass
            _t.sleep(0.05)
            self._bus = smbus2.SMBus(self._port)
            self._last_pages = None  # panel RAM state unknown — force full write
            try:
                self._render(image)
            except OSError:
                # Soft retry failed — full reinit needed (display will briefly blank).
                self._init()
                self._last_pages = None
                self._render(image)

    def clear(self):
        self.display(Image.new('1', self.size))

    def cleanup(self):
        self.clear()
        self._bus.close()


class _Canvas:
    """Drop-in replacement for luma.core.render.canvas."""
    def __init__(self, device):
        self._device = device
        self._image = Image.new('1', device.size)
        self._draw = ImageDraw.Draw(self._image)

    def __enter__(self):
        return self._draw

    def __exit__(self, exc_type, *_):
        if exc_type is None:
            try:
                self._device.display(self._image)
            except OSError:
                pass  # transient I2C error — skip frame, next loop will retry


class OLED:
    def __init__(self):
        self.ok = False
        self.error = None
        self.device = None
        try:
            self.device = _OLEDDevice(I2C_BUS, OLED_ADDR, OLED_WIDTH, OLED_HEIGHT)
            self.ok = True
        except Exception as e:
            self.error = str(e)

    def canvas(self):
        """Context manager — use as: with oled.canvas() as draw: ..."""
        return _Canvas(self.device)

    def clear(self):
        if self.ok and self.device:
            self.device.clear()

    def draw_bar(self, draw, x, y, w, h, frac):
        """Filled progress bar. frac in [0.0, 1.0]."""
        frac = max(0.0, min(1.0, frac))
        draw.rectangle((x, y, x + w - 1, y + h - 1), outline="white")
        if frac > 0:
            filled = max(1, int((w - 2) * frac))
            draw.rectangle((x + 1, y + 1, x + filled, y + h - 2), fill="white")

    def draw_sparkline(self, draw, title, data, y_min=None, y_max=None):
        """Line chart with auto-scaling if y_min/y_max are not provided."""
        draw.text((0, 0), title, fill="white")
        if len(data) < 2:
            draw.text((0, 16), "Gathering...", fill="white")
            return
        lo = y_min if y_min is not None else min(data)
        hi = y_max if y_max is not None else max(data)
        span = (hi - lo) if hi != lo else 1
        chart_h = 36
        y_off   = 14
        w       = OLED_WIDTH
        n       = len(data)
        for i in range(1, n):
            x1 = int((i - 1) * w / (n - 1))
            y1 = chart_h + y_off - int(((data[i - 1] - lo) / span) * chart_h)
            x2 = int(i * w / (n - 1))
            y2 = chart_h + y_off - int(((data[i] - lo) / span) * chart_h)
            draw.line((x1, y1, x2, y2), fill="white")
        lo_s = f"{lo:.0f}"
        hi_s = f"{hi:.0f}"
        draw.text((0, 52), lo_s, fill="white")
        draw.text((w - len(hi_s) * 6, 52), hi_s, fill="white")
