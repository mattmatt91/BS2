import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

WIDTH = 128
HEIGHT = 32  # Change to 64 if needed
BORDER = 5


class OledDisplay:
    def __init__(self) -> None:
        pass
        # Define the Reset Pin

        # Configuration for OLED display

        # Initialize I2C and OLED display
        i2c = board.I2C()  # uses board.SCL and board.SDA
        self.oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

        # Clear display
        self.oled.fill(0)
        self.oled.show()

    def draw_number(self, number: str):
        image = Image.new("1", (self.oled.width, self.oled.height))

        draw = ImageDraw.Draw(image)

        draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=255, fill=255)

        draw.rectangle(
            (
                BORDER,
                BORDER,
                self.oled.width - BORDER - 1,
                self.oled.height - BORDER - 1,
            ),
            outline=0,
            fill=0,
        )

        font = ImageFont.load_default()

        text = number

        font_width, font_height = (
            6 * len(text),
            8,
        )  # Approximation for default font size

        draw.text(
            (
                self.oled.width // 2 - font_width // 2,
                self.oled.height // 2 - font_height // 2,
            ),
            text,
            font=font,
            fill=255,
        )

        # Display image
        self.oled.image(image)
        self.oled.show()
