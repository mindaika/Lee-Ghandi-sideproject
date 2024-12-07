from PIL import Image

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

def pixellate(image_path, output_path, pixel_size, num_colors):
    # Load the image
    image = load_image(image_path)

    # Calculate the new size
    new_size = (image.width // pixel_size, image.height // pixel_size)

    # Pixellate the image
    pixelated_image = resize_image(image, new_size)

    # Reduce the number of colors
    low_color_image = reduce_colors(pixelated_image, num_colors)

    # Save the image
    low_color_image.save(output_path)
    print(f"Saved {output_path}")

pixellate('/Users/mindaika/Downloads/img.webp', '/Users/mindaika/Downloads/output.png', 16, 256)
# Change for Commit