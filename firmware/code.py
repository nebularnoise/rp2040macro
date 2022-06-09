import microcontroller
import board
import busio
import digitalio
import time
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_sh1106

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP14,)
keyboard.row_pins = (board.GP15,)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.keymap = [
    [KC.A,]
]


displayio.release_displays()

i2c = busio.I2C(board.GP27, board.GP26)

display_bus = displayio.I2CDisplay(i2c_bus=i2c, device_address=0x3C)

#spi = busio.SPI(board.GP18, board.GP19)
#display_bus = displayio.FourWire(
#    spi,
#    command=board.GP21,
#    chip_select=board.GP17,
#    reset=board.GP20,
#    baudrate=1000000,
#)

WIDTH = 128

HEIGHT = 64

BORDER = 10

display = adafruit_displayio_sh1106.SH1106(display_bus, width=WIDTH, height=HEIGHT)


# Make the display context

splash = displayio.Group()

display.show(splash)


color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)

color_palette = displayio.Palette(1)

color_palette[0] = 0xFFFFFF  # White


bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)

splash.append(bg_sprite)


# Draw a smaller inner rectangle

inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)

inner_palette = displayio.Palette(1)

inner_palette[0] = 0x000000  # Black

inner_sprite = displayio.TileGrid(

    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER

)

splash.append(inner_sprite)


# Draw a label
text = "Coucou !"
text_area = label.Label(
    terminalio.FONT, text=text, color=0xFFFFFF, x=24, y=HEIGHT // 2 - 1
)

splash.append(text_area)

if __name__ == '__main__':
    keyboard.go()
