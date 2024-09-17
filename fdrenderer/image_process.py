from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from numpy.random import randint


class ImageProcess:
    __slots__ = (
        "__template_path",
        "__font_name",
        "__box_size",
        "__font_size",
        "__total_height",
    )

    def __init__(self, font_name: str, box_size: tuple, template_path: str):
        self.__template_path = template_path
        self.__font_name = font_name
        self.__box_size = box_size
        self.__font_size = 40
        self.__total_height = 0

    def __create_blank_image(self) -> Image.Image:
        """Создает пустое изображение с заданным размером."""
        return Image.new("RGBA", self.__box_size, (255, 255, 255, 0))

    def __wrap_text(self, subtitles: str) -> list:
        """Разбивает текст на строки, чтобы они помещались в заданный размер."""
        lines = []
        words = subtitles.split()
        current_line = ""

        draw = ImageDraw.Draw(self.__create_blank_image())
        font = ImageFont.truetype(self.__font_name, self.__font_size)

        for word in words:
            test_line = current_line + (word if current_line == "" else " " + word)
            bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]

            if text_width <= self.__box_size[0]:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    def __adjust_font_size(self, draw: ImageDraw.Draw, lines: list) -> int:
        """Корректирует размер шрифта так, чтобы текст помещался в высоту."""
        while self.__font_size > 0:
            font = ImageFont.truetype(self.__font_name, self.__font_size)
            self.__total_height = sum(
                draw.textbbox((0, 0), line, font=font)[3]
                - draw.textbbox((0, 0), line, font=font)[1]
                for line in lines
            )

            if self.__total_height <= self.__box_size[1]:
                return self.__font_size

            self.__font_size -= 5

        return self.__font_size

    def __draw_text(
        self, image: Image.Image, lines: list, font_size: int
    ) -> Image.Image:
        """Рисует субтитры на изображении."""
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.__font_name, font_size)

        y_offset = (self.__box_size[1] - self.__total_height) / 2

        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_x = (self.__box_size[0] - (bbox[2] - bbox[0])) / 2
            draw.text((text_x, y_offset), line, fill="white", font=font)
            y_offset += (bbox[3] - bbox[1]) + 5

        return image

    def process_image(self, subtitles: Optional[str]) -> str:
        """
        Накладывает на изображение субтитры, сохраняет готовое изображение и возвращает название файла.
        """
        subtitles = subtitles or "*БИ-И-ИП*"
        blank_image = self.__create_blank_image()
        lines = self.__wrap_text(subtitles)

        draw = ImageDraw.Draw(blank_image)
        adjusted_font_size = self.__adjust_font_size(draw, lines)

        blank_image_with_text = self.__draw_text(blank_image, lines, adjusted_font_size)

        template = Image.open(self.__template_path).convert("RGBA").resize((1280, 720))
        template.paste(blank_image_with_text, (252, 250), blank_image_with_text)
        template_filename = (
            f"./cache/{len(subtitles)*len(lines) * randint(0, 9999999)}.png"
        )
        template.save(template_filename)
        return template_filename
