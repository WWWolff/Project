# Hexagonal Image Generator

## Overview
The **Hexagonal Image Generator** is a Python application designed to transform images into hexagonal patterns represented in SVG format. By sampling average colors from specific regions of the image, this program generates visually appealing hexagons that can also be converted to PNG format. The resulting images can be used for various applications, including digital art, wallpapers, and more.

## Features
- **Hexagon Generation**: Creates filled hexagons based on average colors from the input image.
- **Half Hexagon Support**: Allows for the generation of half hexagons for better alignment at the edges.
- **SVG Output**: Outputs the hexagonal pattern in SVG format, maintaining high quality and scalability.
- **PNG Conversion**: Converts the generated SVG into a PNG file for easier sharing and use.
- **Image Enhancement**: Applies sharpening filters to improve image clarity after cropping.
- **Customizable Size**: Adjust the hexagon size to suit your design needs.

## Dependencies
This project requires the following Python libraries:
- **Pillow**: A powerful library for image processing.
- **CairoSVG**: A library for converting SVG files to PNG format.

To install the required libraries, use pip:

```bash
pip install Pillow cairosvg
```

## Author
This project was developed by **Daniel Wolff**. You can find me on GitHub as [WWWolff](https://github.com/WWWolff).

## License
This project is licensed under the **MIT License**. You are free to use, modify, and distribute this software, provided that proper attribution is given to the original author.

For more details, see the [LICENSE](LICENSE) file in the project repository.
