from PIL import Image
from openai import OpenAI
import uuid
import tkinter as tk
from tkinter import ttk
import os
from dotenv import load_dotenv
import requests
from io import BytesIO

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#OPENAI_SERVICE_ACCOUNT = os.getenv("OPENAI_SERVICE_ACCOUNT")

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
    fields['pixel_size'].insert(0, "32")

    fields['num_colors_label'] = ttk.Label(text='Enter the number of colors:')
    fields['num_colors'] = ttk.Entry(show="*")
    fields['num_colors'].insert(0, "256")

    fields['prompt_label'] = ttk.Label(text='Tell me what you want to draw and pixellate')
    fields['prompt'] = ttk.Entry()
    fields['prompt'].insert(0, "Imagine a tiny hamster with a superhero cape, balancing on top of a giant banana peel, while juggling three flaming donuts under a disco ball.")


    for field in fields.values():
        field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)

     # Create a button
    button = tk.Button(root, text="Pixellate", command=root.quit)
    button.pack()

    # Run the main loop
    # Typically, in a Tkinter program, you place the call to the mainloop() method as the last statement after creating the widgets, or so it says
    root.mainloop()

    # Get the values from the entries
    pixel_size = int(fields['pixel_size'].get())
    num_colors = int(fields['num_colors'].get())
    prompt = str(fields['prompt'].get())

    # Destroy the window
    root.destroy()

    return pixel_size, num_colors, prompt

def generate_image(prompt: str):
    OpenAI.api_key = OPENAI_API_KEY
    #openai.organization = SERVICE_ACCOUNT
    
    client = OpenAI()

    try:
        response = client.images.generate(
            prompt=prompt,
            n=2,
            size="1024x1024"
        )

        # Get the image URL
        image_url = response.data[0].url

        return image_url
    
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def pixellate(output_path):

    # Get the pixel size, number of colors, and prompt text
    pixel_size, num_colors, prompt = get_input()

    # Use the Prompt API to generate an image and convert it to an ImageFile object
    image_URL = generate_image(prompt)     
    image = create_image_file_object(image_URL)

    # Calculate the new size
    new_size = (image.width // pixel_size, image.height // pixel_size)

    # Pixellate the image
    pixelated_image = resize_image(image, new_size)

    # Reduce the number of colors
    low_color_image = reduce_colors(pixelated_image, num_colors)

    # Save the image
    low_color_image.save(output_path)
    print(f"Saved {output_path}")

def create_image_file_object(image_url):
    try:
        # Fetch the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Load the image into a BytesIO stream
        image_stream = BytesIO(response.content)
        
        # Create an Image object using PIL
        image = Image.open(image_stream)
        
        # Optionally, convert the Image to an ImageFile object
        from PIL.ImageFile import ImageFile
        if isinstance(image, ImageFile):
            return image  # It's already an ImageFile
        else:
            # Convert explicitly if necessary
            return image.convert("RGB")  # or appropriate mode
            
    except Exception as e:
        print(f"Error creating image file object: {e}")
        return None

def generate_random_filename():
    random_part = uuid.uuid4().hex[:8]  # Generate a random unique string (8 characters)
    return f"IMAGE-{random_part}.png"

output_path = '/Users/mindaika/Downloads/' + generate_random_filename()
pixellate(output_path)
