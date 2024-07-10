from PIL import Image, ImageDraw, ImageFont
import random
import os


class MemeEngine:
    """Class for meme generation from quote and image"""

    """Init method
    
    ":param[in]: output_dir: output path to save the generated meme
    """
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def draw_text(self, draw, text, position, font, max_width):
        lines = []
        words = text.split()
        while words:
            line = ''
            while words and draw.textbbox((0, 0), line + words[0], font=font)[2] <= max_width:
                line = line + (words.pop(0) + ' ')
            lines.append(line)
        y = position[1]
        for line in lines:
            draw.text((position[0], y), line, font=font, fill="white")
            y += font.getbbox(line)[3] - font.getbbox(line)[1]

    """Create meme form picture and quote

    :param[in]: img_path: path to imnage
    :param[in]: body: body of the qoute
    :param[in]: author: author of the quote
    :param[in]: witdth: width of generated meme, defaut 500
    :return   : path to generated meme
    """
    def make_meme(self, img_path, body, author, width = 500):
        # Open image to process
        try:
            img = Image.open(img_path)
        except ValueError as err:
            print(f"Error generating meme: {err}")
        font_size = 20
        font_path = "../font/dejavu/DejaVuSans-Bold.ttf"
        # resize image
        aspect_ratio = img.height / img.width
        new_height = int(aspect_ratio * width)
        resized_image = img.resize((width, new_height))

        # Prepare the text
        draw = ImageDraw.Draw(resized_image)

        # Specify the font style and size
        font = ImageFont.truetype(font_path, font_size)

        message = f'"{body}" - {author}'

        # Add text to image
        self.draw_text(draw, message, (10, 10), font, width)

        # Ensure the output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Save the image
        output_path = f"{self.output_dir}/meme_{random.randint(0, 1000000)}.jpg"
        resized_image.save(output_path)

        return output_path

