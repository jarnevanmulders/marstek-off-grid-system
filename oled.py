from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
import time

# Change address if needed (0x3C is most common)
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

# Create blank image
image = Image.new("1", (device.width, device.height))
draw = ImageDraw.Draw(image)

draw.text((0, 0), "Hello Raspberry Pi!", fill=255)
draw.text((0, 20), "OLED working", fill=255)

device.display(image)

time.sleep(5)

