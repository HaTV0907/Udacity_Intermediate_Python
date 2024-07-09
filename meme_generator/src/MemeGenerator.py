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
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        # resize image
        aspect_ratio = img.height / img.width
        new_height = int(aspect_ratio * width)
        resized_image = img.resize((width, new_height))

        # Prepare the text
        draw = ImageDraw.Draw(resized_image)

        # Specify the font style and size
        font = ImageFont.truetype(font_path, font_size)

        message = f'"{body}" - {author}'

        # Calculate text size and position
        text_position = (random.randint(0, width - 100), random.randint(0, new_height - 50))

        # Add text to image
        draw.text(text_position, message, font=font, fill='white')

        # Ensure the output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Save the image
        output_path = f"{self.output_dir}/meme_{random.randint(0, 1000000)}.jpg"
        resized_image.save(output_path)

        return output_path

