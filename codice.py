from PIL import Image, ImageDraw
import numpy as np
import math

def hexagon_corners(center, size):
    """
    Calculate the corner coordinates of a hexagon given its center and size.

    Parameters:
        center (tuple): The (x, y) coordinates of the hexagon's center.
        size (int): The size (radius) of the hexagon.

    Returns:
        list: A list of (x, y) tuples representing the corners of the hexagon.
    """
    x, y = center
    w = math.sqrt(3) * size  # Width of the hexagon
    h = 2 * size  # Height of the hexagon

    return [
        (x - w / 2, y - h / 4),
        (x, y - h / 2),
        (x + w / 2, y - h / 4),
        (x + w / 2, y + h / 4),
        (x, y + h / 2),
        (x - w / 2, y + h / 4)
    ]

def rectangle_corners(center, w, h):
    """
    Calculate the corner coordinates of a rectangle given its center, width, and height.

    Parameters:
        center (tuple): The (x, y) coordinates of the rectangle's center.
        w (int): The width of the rectangle.
        h (int): The height of the rectangle.

    Returns:
        list: A list of (x, y) tuples representing the corners of the rectangle.
    """
    x, y = center
    return [
        (x - w / 2, y - h / 2),
        (x + w / 2, y - h / 2),
        (x + w / 2, y + h / 2),
        (x - w / 2, y + h / 2)
    ]

def hexagonify(path, hexagon_size):
    """
    Create an image filled with hexagons, sampling colors from the input image.

    Parameters:
        path (str): The path to the input image file.
        hexagon_size (int): The size of each hexagon.

    Returns:
        str: The SVG content representing the hexagonal artwork.
    """
    # Load the input image
    im = Image.open(path)
    I = np.asarray(im)  # Convert the image to a NumPy array for color sampling

    # Calculate the dimensions of the hexagons
    w = math.sqrt(3) * hexagon_size  # Width of the hexagon
    h = 2 * hexagon_size  # Height of the hexagon

    # Calculate how many hexagons fit horizontally and vertically
    num_hor = int(im.size[0] / w) + 2
    num_ver = int(im.size[1] / h * 4 / 3) + 2

    # Start building the SVG content
    svg_content = '<svg xmlns="http://www.w3.org/2000/svg" width="{}" height="{}">'.format(im.size[0], im.size[1])

    # Loop through each position in the grid to draw hexagons
    for i in range(0, num_hor * num_ver):
        column = i % num_hor  # Current column
        row = i // num_hor  # Current row
        even = row % 2  # Offset for even rows

        # Get the corner points of the current hexagon
        p = hexagon_corners((column * w + even * w / 2, row * h * 3 / 4), hexagon_size)

        # Sample the average color using a rectangle approximation
        raw = rectangle_corners((column * w + even * w / 2, row * h * 3 / 4), w, h)
        r = []
        for points in raw:
            np0 = int(np.clip(points[0], 0, im.size[0] - 1))  # Clip to image boundaries
            np1 = int(np.clip(points[1], 0, im.size[1] - 1))  # Clip to image boundaries
            r.append((np0, np1))

        # Ensure we have valid coordinates and avoid empty slices
        if (r[0][0] < r[1][0]) and (r[0][1] < r[3][1]):
            color = np.average(I[r[0][1]:r[3][1], r[0][0]:r[1][0]], axis=(0, 1))
            color = tuple(np.clip(color.astype(int), 0, 255))  # Clip color values to valid range
        else:
            # If no valid pixels were found, default to black
            color = (0, 0, 0)

        # Add hexagon to the SVG content
        svg_content += '<polygon points="{}" fill="rgb({}, {}, {})" />'.format(
            ' '.join(f'{x},{y}' for x, y in p), color[0], color[1], color[2]
        )

    svg_content += '</svg>'  # Close the SVG tag
    return svg_content

if __name__ == "__main__":
    # Path to the input image
    input_path = 'input.png'  # Change this to your input image
    hexagon_size = 20  # Adjust the size of the hexagons here
    svg_output = hexagonify(input_path, hexagon_size)

    # Save the SVG content to a file
    with open('output.svg', 'w') as svg_file:
        svg_file.write(svg_output)
    print("Your hexagonal artwork has been saved as 'output.svg'. Enjoy!")

    # Create an HTML template to display the SVG artwork
    html_content = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>Hexagonal Artwork</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <h1>Hexagonal Artwork from Image</h1>
        <embed src="output.svg" width="100%" height="auto" type="image/svg+xml" />
    </body>
    </html>"""

    # Save the HTML file
    with open('output.html', 'w') as html_file:
        html_file.write(html_content)
    print("An HTML file with your artwork has been created as 'output.html'.")
