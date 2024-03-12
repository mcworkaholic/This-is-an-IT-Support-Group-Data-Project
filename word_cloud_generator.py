
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from os import path
import os
from PIL import Image
from wordcloud import WordCloud

from config import txt_file_path, IT_image_path, image_directory, data_directory

def black_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 0%, 0%)"  # Always return black color

# Load and invert the mask image
original_mask = np.array(Image.open(path.join(image_directory, IT_image_path)))
mask = np.bitwise_not(original_mask)

# Read the text file and count frequencies
with open(path.join(data_directory, txt_file_path)) as f:
    titles = [line.strip() for line in f.readlines()]
frequencies = Counter(titles)

# Initialize the WordCloud object with white background and the inverted mask
wc = WordCloud(
    background_color='white',
    max_words=1000,
    mask=mask,
    margin=10,
    random_state=1
)

# Generate the word cloud from frequencies
wc.generate_from_frequencies(frequencies)

# Display the word cloud
plt.figure(figsize=(10, 6))
plt.imshow(wc.recolor(color_func=black_color_func, random_state=3), interpolation="bilinear")
plt.axis("off")
plt.show()

# Save the word cloud to a file
wc.to_file(path.join(image_directory, "job_title_word_cloud.png"))

