from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
from .config import I2C_BUS, OLED_ADDR, OLED_WIDTH, OLED_HEIGHT

class OLED:
    def __init__(self):
        self.ok = False
        self.error = None
        self.device = None
        try:
            serial = i2c(port=I2C_BUS, address=OLED_ADDR)
            self.device = sh1106(serial, width=OLED_WIDTH, height=OLED_HEIGHT)
            self.ok = True
        except Exception as e:
            self.error = str(e)

    def canvas(self):
        """Context manager — use as: with oled.canvas() as draw: ..."""
        return canvas(self.device)

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
        for i in range(1, len(data)):
            x1 = int((i - 1) * (OLED_WIDTH / OLED_WIDTH))
            y1 = h + y_off - int(((data[i - 1] - y_min) / span) * h)
            x2 = int(i * (OLED_WIDTH / OLED_WIDTH))
            y2 = h + y_off - int(((data[i] - y_min) / span) * h)
            draw.line((x1, y1, x2, y2), fill="white")
