import lvgl as lv
import gc9a01
from machine import Pin, SPI

class DriverGC9A01:
    def __init__(self):
        self._tft = gc9a01.GC9A01(
            SPI(2, baudrate=80000000, polarity=0, sck=Pin(10), mosi=Pin(11)),
            240,
            240,
            reset=Pin(14, Pin.OUT),
            cs=Pin(9, Pin.OUT),
            dc=Pin(8, Pin.OUT),
            backlight=Pin(2, Pin.OUT),
            rotation=0
        )

        # enable display and clear screen
        ORANGE = 0xfa20
        self._tft.init()
        self._tft.fill(ORANGE)

        # enable LVGL
        if not lv.is_initialized():
            lv.init()

        self.width = 240
        self.height = 240
        self.buf_size = self.width * self.height * 2 // 10  # RGB565
        self.buf1 = gc9a01.allocate_framebuffer(self.buf_size, gc9a01.MEMORY_DMA)
        self.buf2 = gc9a01.allocate_framebuffer(self.buf_size, gc9a01.MEMORY_DMA)

        self.disp = lv.display_create(self.width, self.height)
        self.disp.set_color_format(lv.COLOR_FORMAT.RGB565)
        self.disp.set_buffers(self.buf1, self.buf2, self.buf_size, lv.DISPLAY_RENDER_MODE.PARTIAL)
        self.disp.set_flush_cb(self.flush_cb)

    @property
    def display(self):
        return self.disp
    
    @property
    def tft(self):
        return self._tft

    def flush_cb(self, disp, area, color_map):
        w = area.x2 - area.x1 + 1
        h = area.y2 - area.y1 + 1
        data_view = color_map.__dereference__(w * h * 2)
        self._tft.blit_buffer(data_view, area.x1, area.y1, w, h)
        disp.flush_ready()


display = DriverGC9A01()


scrn = lv.screen_active()
scrn.set_style_bg_color(lv.color_hex(0xFF0000), 0)
scrn.set_style_bg_opa(lv.OPA._100, 0)

slider = lv.slider(scrn)
slider.set_size(100, 50)
slider.center()

label = lv.label(scrn)
label.set_text('HELLO WORLD!')
label.align(lv.ALIGN.CENTER, 0, 0)

import time
time_passed = 1
last_print = 0

import random

while True:
    start_time = time.ticks_ms()
    time.sleep_ms(1)
    lv.tick_inc(time_passed)
    time_passed -= time_passed
    lv.task_handler()
    end_time = time.ticks_ms()
    time_passed += time.ticks_diff(end_time, start_time)
    if time.ticks_diff(end_time, last_print) > 1000:
        last_print = end_time
        scrn.set_style_bg_color(lv.color_hex(random.randint(0, 0xFFFFFF)), 0)
        scrn.invalidate()

