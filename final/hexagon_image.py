from PIL import Image, ImageFilter
import math
import cairosvg

HEXAGON_SIZE = 7.5  # Size of the hexagons

def calculate_average_color(img, start_x, start_y, end_x, end_y):
    """Calculates the average color of a specified region in the image."""
    color_list = []

    # Ensure the specified area is within image bounds
    start_x = max(0, start_x)
    start_y = max(0, start_y)
    end_x = min(img.width, end_x)
    end_y = min(img.height, end_y)

    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            color_list.append(img.getpixel((x, y)))

    if not color_list:
        return (255, 255, 255)  # Return white if there are no pixels

    # Calculate the average RGB values
    avg_color = tuple(sum(color[i] for color in color_list) // len(color_list) for i in range(3))

    return avg_color

def create_hexagon_svg(x_pos, y_pos, size, fill_color):
    """Creates a flat hexagon in SVG format without outlines."""
    vertices = []
    for i in range(6):
        angle_in_degrees = 60 * i
        angle_in_radians = math.radians(angle_in_degrees)
        vertices.append((x_pos + size * math.cos(angle_in_radians), y_pos + size * math.sin(angle_in_radians)))

    # Format points to two decimal places
    vertices_str = ' '.join(f'{v[0]:.2f},{v[1]:.2f}' for v in vertices)
    color_rgb = f'rgb({fill_color[0]},{fill_color[1]},{fill_color[2]})'

    return f'<polygon points="{vertices_str}" fill="{color_rgb}" stroke="none" stroke-width="0"/>\n'

def create_half_hexagon_svg(x_pos, y_pos, size, fill_color):
    """Creates a half hexagon in SVG format."""
    vertices = [
        (x_pos, y_pos),  # Bottom left point
        (x_pos + size, y_pos + (size * math.sqrt(3) / 2)),  # Top right point
        (x_pos + size * 2, y_pos)  # Bottom right point
    ]

    # Format points to two decimal places
    vertices_str = ' '.join(f'{v[0]:.2f},{v[1]:.2f}' for v in vertices)
    color_rgb = f'rgb({fill_color[0]},{fill_color[1]},{fill_color[2]})'

    return f'<polygon points="{vertices_str}" fill="{color_rgb}" stroke="none" stroke-width="0"/>\n'

def create_aligned_svg(img, hex_size, img_width, img_height):
    """Generates SVG with aligned hexagons corresponding to the model in the input image."""
    # Start the SVG structure with specified dimensions
    svg_output = f'<svg width="{img_width * 2}" height="{img_height * 2}" xmlns="http://www.w3.org/2000/svg">\n'

    # Calculate grid steps for precise alignment
    horizontal_step = hex_size * 1.5  # Horizontal step between hexagons
    vertical_step = math.sqrt(3) * hex_size  # Vertical step between hexagons

    # Iterate over the image using the adjusted hexagonal grid
    for row in range(-int(vertical_step), img_height + int(vertical_step), int(vertical_step)):
        for col in range(-int(horizontal_step), img_width + int(horizontal_step), int(horizontal_step)):
            # Adjust the rows to create proper hexagonal alignment
            row_shift = hex_size * 0.75 if (col // int(horizontal_step)) % 2 == 1 else 0

            hexagon_start_x = col  # Starting x position for the hexagon
            hexagon_start_y = row + row_shift  # Starting y position for the hexagon

            # Sample the average color for this hexagon
            avg_fill_color = calculate_average_color(img, int(hexagon_start_x), int(hexagon_start_y),
                                                     int(hexagon_start_x + hex_size * 1.5), int(hexagon_start_y + vertical_step))

            # Create the hexagon in SVG
            svg_output += create_hexagon_svg(hexagon_start_x, hexagon_start_y, hex_size, avg_fill_color)

    # Add half hexagons for the bottom edge
    for col in range(0, img_width, int(horizontal_step)):
        # Calculate the average color of the upper hexagons for continuity
        avg_fill_color_top_left = calculate_average_color(img, int(col), int(img_height / 2 - hex_size),
                                                           int(col + hex_size), int(img_height / 2))
        avg_fill_color_top_right = calculate_average_color(img, int(col + hex_size), int(img_height / 2 - hex_size),
                                                            int(col + hex_size * 2), int(img_height / 2))
        avg_fill_color = (
            (avg_fill_color_top_left[0] + avg_fill_color_top_right[0]) // 2,
            (avg_fill_color_top_left[1] + avg_fill_color_top_right[1]) // 2,
            (avg_fill_color_top_left[2] + avg_fill_color_top_right[2]) // 2
        )

        # Create the half hexagon in SVG
        svg_output += create_half_hexagon_svg(col, img_height, hex_size, avg_fill_color)

    svg_output += '</svg>'  # Close the SVG structure
    return svg_output

# Load the image only when needed
def main(input_image_path):
    # Load the image
    img = Image.open(input_image_path)

    # Get the dimensions of the image
    image_width, image_height = img.width, img.height

    # Generate the SVG content with adjusted hexagonal alignment
    svg_output_aligned = create_aligned_svg(img, HEXAGON_SIZE, image_width, image_height)

    # Define the output SVG file path
    output_svg_path = 'aligned_output.svg'  # Change this to your desired SVG output file name

    # Write the aligned SVG content to the output file
    with open(output_svg_path, 'w') as output_file:
        output_file.write(svg_output_aligned)

    # Convert the SVG to PNG
    output_png_path = 'output_image.png'  # Change this to your desired PNG output file name
    cairosvg.svg2png(url=output_svg_path, write_to=output_png_path)

    cropped_output_path = 'cropped_output.png'  # Change this to your final cropped output file name
    border_crop = 10  # Set how many pixels to crop from the bottom edge

    with Image.open(output_png_path) as final_image:
        # Crop the image, reducing the height from the bottom edge
        final_image_cropped = final_image.crop((0, 0, image_width, image_height - border_crop))

        # Apply a sharpening filter to enhance image clarity
        sharpened_image = final_image_cropped.filter(ImageFilter.SHARPEN)
        sharpened_image.save(cropped_output_path)  # Save the sharpened image

    # Print the output file paths for confirmation
    print(f"SVG saved to {output_svg_path}")
    print(f"PNG image saved to {output_png_path}")
    print(f"Cropped and sharpened image saved to {cropped_output_path}")

# Example call (uncomment to use)
main('C:/Users/danju/OneDrive/Desktop/Lille/RinCS/Project/input.png')
