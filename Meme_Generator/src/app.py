import random
import os
import requests
from flask import Flask, render_template, abort, request

#  Import your Ingestor and MemeEngine classes
from MemeGenerator import MemeEngine
from QuoteEngine import *



app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    # TODO: Use the Ingestor class to parse all files in the
    # quote_files variable
    quotes = load_quotes(quote_files)

    images_path = "./_data/photos/dog/"

    # Create an empty list to store the image filenames
    imgs = []

    # Iterate over the files in the directory
    for filename in os.listdir(images_path):
        # Check if the file is an image (you can customize this condition based on your requirements)
        if filename.endswith(".jpg"):
            # Add the image filename to the list
            imgs.append(os.path.join(images_path, filename))

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    # :
    # Use the random python standard library class to:
    # 1. select a random image from imgs array
    # 2. select a random quote from the quotes array

    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    # :
    # 1. Use requests to save the image from the image_url
    #    form param to a temp local file.
    # 2. Use the meme object to generate a meme using this temp
    #    file and the body and author form paramaters.
    # 3. Remove the temporary saved image.

    image_url = request.form['image_url']
    body = request.form['body']
    author = request.form['author']

    # Step 1: Download the image
    response = requests.get(image_url)
    temp_image_path = './static/temp_image.jpg'
    with open(temp_image_path, 'wb') as file:
        file.write(response.content)

    # Step 2: Generate the meme
    meme_path = meme.make_meme(temp_image_path, body, author)

    # Step 3: Remove the temporary image
    os.remove(temp_image_path)

    return render_template('meme.html', path=meme_path)


if __name__ == "__main__":
    app.run()
