import smbus2
from PIL import Image, ImageDraw
from .config import I2C_BUS, OLED_ADDR, OLED_WIDTH, OLED_HEIGHT


class _OLEDDevice:
    """Direct SH1106 driver using write_i2c_block_data.
    Luma's i2c_rdwr path fails on this display; raw 32-byte chunk writes work."""

    mode = '1'
    COL_OFFSET = 2  # SH1106 has 132-col driver, visible window starts at col 2

    def __init__(self, port, address, width, height):
        self.size = (width, height)
        self._addr = address
        self._bus = smbus2.SMBus(port)
        self._pages = height // 8
        self._width = width
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

    def display(self, image):
        self._cmd(0xAE)  # display off during write (matches working raw sequence)
        buf = list(image.convert('1').tobytes())
        lo = 0x00 + (self.COL_OFFSET & 0x0F)
        hi = 0x10 + (self.COL_OFFSET >> 4)
        for page in range(self._pages):
            self._cmd(0xB0 | page, lo, hi)
            self._data(buf[page * self._width:(page + 1) * self._width])
        self._cmd(0xAF)  # display on

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
            self._device.display(self._image)


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

    def draw_sparkline(self, draw, title, data, y_min, y_max):
        draw.text((0, 0), f"Graph: {title}", fill="white")
        if len(data) < 2:
            draw.text((0, 20), "Gathering data...", fill="white")
            return
        h = 50
        y_off = 14
        span = (y_max - y_min) if y_max != y_min else 1
        n = len(data)
        for i in range(1, n):
            x1 = int((i - 1) * OLED_WIDTH / (n - 1))
            y1 = h + y_off - int(((data[i - 1] - y_min) / span) * h)
            x2 = int(i * OLED_WIDTH / (n - 1))
            y2 = h + y_off - int(((data[i] - y_min) / span) * h)
            draw.line((x1, y1, x2, y2), fill="white")
