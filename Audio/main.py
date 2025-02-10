from PIL import Image
import pytesseract
from gtts import gTTS
import os
import re

# Function to extract text from an image
def extract_text_from_image(image_path):
    # Open the image using PIL
    img = Image.open(image_path)
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(img)
    return text

def is_valid_word(word):
    # Check if the word contains at least one alphanumeric character
    return bool(re.search(r'\w', word))

def create_mp3_files(words):
    for word in words:
        if not is_valid_word(word):  # Skip invalid words
            print(f"Skipping invalid word: {word}")
            continue
        print(f"Processing word: {word}")  # Debug print
        tts = gTTS(text=word, lang='en')
        mp3_filename = f"{word}.mp3"
        tts.save(mp3_filename)
        print(f"Created: {mp3_filename}")

# Main function
def main(image_path):
    # Extract text from the image
    text = extract_text_from_image(image_path)
    # Split the text into individual words
    words = text.split()
    # Create MP3 files for each word
    create_mp3_files(words)

# Path to the image file
image_path = "/Users/sushmita.goswami/Desktop/Gyan/Python/mp3/word.png"  # Replace with your image file path

# Run the program
if __name__ == "__main__":
    main(image_path)