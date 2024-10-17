import pytest
from PIL import Image
from your_module import (
    calculate_average_color,
    create_hexagon_svg,
    create_half_hexagon_svg,
    create_aligned_svg,
)  # Replace 'your_module' with the actual name of the module where your functions are defined

# Sample image data for testing
@pytest.fixture
def sample_image():
    """Create a simple 4x4 test image with known colors."""
    img = Image.new('RGB', (4, 4), 'white')
    img.putpixel((0, 0), (255, 0, 0))  # Red
    img.putpixel((1, 0), (0, 255, 0))  # Green
    img.putpixel((2, 0), (0, 0, 255))  # Blue
    img.putpixel((3, 0), (255, 255, 0))  # Yellow
    img.putpixel((0, 1), (255, 255, 255))  # White
    img.putpixel((1, 1), (0, 0, 0))  # Black
    img.putpixel((2, 1), (128, 128, 128))  # Grey
    img.putpixel((3, 1), (255, 0, 255))  # Magenta
    return img

def test_calculate_average_color(sample_image):
    """Test the calculate_average_color function."""
    avg_color = calculate_average_color(sample_image, 0, 0, 2, 2)  # Average colors from the top-left 2x2 region
    assert avg_color == (127, 127, 127), "Expected average color should be (127, 127, 127)"

def test_create_hexagon_svg():
    """Test the create_hexagon_svg function."""
    svg_output = create_hexagon_svg(0, 0, 7.5, (255, 0, 0))
    expected_output = '<polygon points="0.0,7.5 3.75,0.0 0.0,-7.5 -3.75,0.0" fill="rgb(255,0,0)" stroke="none" stroke-width="0" />\n'
    assert svg_output.strip() == expected_output.strip(), "SVG output does not match expected output."

def test_create_half_hexagon_svg():
    """Test the create_half_hexagon_svg function."""
    svg_output = create_half_hexagon_svg(0, 0, 7.5, (0, 255, 0))
    expected_output = '<polygon points="0.0,0 7.5,6.49519052838329 15.0,0" fill="rgb(0,255,0)" stroke="none" stroke-width="0" />\n'
    assert svg_output.strip() == expected_output.strip(), "Half SVG output does not match expected output."

def test_create_aligned_svg(sample_image):
    """Test the create_aligned_svg function."""
    svg_output = create_aligned_svg(sample_image, 7.5, 4, 4)
    assert '<svg' in svg_output and '</svg>' in svg_output, "SVG output should start and end with SVG tags."

    # Check if the SVG has the expected number of hexagons based on the input image size
    hexagon_count = svg_output.count('<polygon')
    assert hexagon_count > 0, "Expected to find at least one hexagon in the SVG output."

# Run the tests
if __name__ == "__main__":
    pytest.main()
