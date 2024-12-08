from PIL import Image
import tkinter as tk

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

    # Create a label
    label = tk.Label(root, text="Enter the pixel size:")
    label.pack(side=tk.TOP)

    # Create an entry
    entry = tk.Entry(root)
    entry.pack()

    # Create another label
    label2 = tk.Label(root, text="Enter the number of colors:")
    label2.pack(side=tk.TOP)

    # Create another entry
    entry2 = tk.Entry(root)
    entry2.pack()

    # Create another label
    label3 = tk.Label(root, text="Tell me what you want to draw and pixellate")
    label3.pack(side=tk.TOP, ipadx=20)

    # Create another entry
    entry3 = tk.Entry(root)
    entry3.pack() 

     # Create a button
    button = tk.Button(root, text="Pixellate", command=root.quit)
    button.pack()

    # Use entry3.get() to get the text from the entry
    # Use this as input to an image generator

    # Run the main loop
    # Typically, in a Tkinter program, you place the call to the mainloop() method as the last statement after creating the widgets.
    root.mainloop()

    # Get the values from the entries
    pixel_size = int(entry.get())
    num_colors = int(entry2.get())

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
