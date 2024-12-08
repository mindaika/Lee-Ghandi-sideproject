from PIL import Image
import openai
import tkinter as tk
from tkinter import ttk
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
SERVICE_ACCOUNT = os.getenv("OPENAI_SERVICE_ACCOUNT")

# Load an image from a file
def load_image(image_path):
    return Image.open(image_path) # '/Users/mindaika/Downloads/img.webp'

def resize_image(image, new_size):
    smaller_image = image.resize(new_size, Image.Resampling.NEAREST)
    return smaller_image.resize(image.size, Image.Resampling.NEAREST)

def reduce_colors(image, num_colors):
    # Convert to RGB if necessary
    image = image.convert("RGB")
    return image.quantize(num_colors)

def get_input():
    root = tk.Tk()
    root.title("Pixify")

    fields = {}

    fields['pixel_size_label'] = ttk.Label(text='Enter the pixel size:')
    fields['pixel_size'] = ttk.Entry()

    fields['num_colors_label'] = ttk.Label(text='Enter the number of colors:')
    fields['num_colors'] = ttk.Entry(show="*")

    fields['image_label'] = ttk.Label(text='Tell me what you want to draw and pixellate')
    fields['image'] = ttk.Entry()

    for field in fields.values():
        field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)

     # Create a button
    
    button = tk.Button(root, text="Pixellate", command=root.quit)
    button.pack()

    # Use entry3.get() to get the text from the entry
    # Use this as input to an image generator

    # Run the main loop
    # Typically, in a Tkinter program, you place the call to the mainloop() method as the last statement after creating the widgets.
    root.mainloop()

    # Get the values from the entries
    pixel_size = int(fields['pixel_size'].get())
    num_colors = int(fields['num_colors'].get())

    # Destroy the window
    root.destroy()

    return pixel_size, num_colors

def pixellate(image_path, output_path):
    # Load the image
    image = load_image(image_path)

    # Get the pixel size and number of colors
    pixel_size, num_colors = get_input()

    # Calculate the new size
    new_size = (image.width // pixel_size, image.height // pixel_size)

    # Pixellate the image
    pixelated_image = resize_image(image, new_size)

    # Reduce the number of colors
    low_color_image = reduce_colors(pixelated_image, num_colors)

    # Save the image
    low_color_image.save(output_path)
    print(f"Saved {output_path}")

pixellate('/Users/mindaika/Downloads/img.webp', '/Users/mindaika/Downloads/output.png')
