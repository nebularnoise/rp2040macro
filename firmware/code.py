import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_sh1106

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation

from conf import screen_type, keymap, ScreenType

keyboard = KMKKeyboard()

keyboard.col_pins = (
    board.GP6,   # COL0
    board.GP12,  # COL1
    board.GP11,  # COL2
    board.GP10,  # COL3
)
keyboard.row_pins = (
    board.GP0,  # ROW0
    board.GP9,  # ROW1
    board.GP8,  # ROW2
    board.GP7,  # ROW3
)

keyboard.diode_orientation = DiodeOrientation.ROW2COL

keyboard.keymap = keymap


displayio.release_displays()
spi = busio.SPI(board.GP18, board.GP19)
i2c = busio.I2C(board.GP15, board.GP14)

if screen_type == ScreenType.SPI:
    display_bus = displayio.FourWire(
        spi,
        command=board.GP21,
        chip_select=board.GP17,
        reset=board.GP20,
        baudrate=1000000,
    )
    rotation_angle = 0
elif screen_type == ScreenType.I2C:
    display_bus = displayio.I2CDisplay(i2c_bus=i2c, device_address=0x3C)
    rotation_angle = 180

WIDTH = 128
HEIGHT = 64
BORDER = 10

display = adafruit_displayio_sh1106.SH1106(
    display_bus, width=WIDTH, height=HEIGHT, rotation=rotation_angle
)

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


if __name__ == "__main__":
    keyboard.go()
