# Image Resizer for Cake Printing

This tool resizes images to optimal dimensions for printing on cakes.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Save your image to this directory (e.g., `hot_wheels_image.jpg`)

2. Run the resize script:
```bash
python resize_for_cake.py <your_image.jpg>
```

Example:
```bash
python resize_for_cake.py hot_wheels_image.jpg
```

This will create a resized version (e.g., `hot_wheels_image_cake.jpg`) that's optimized for cake printing.

## Features

- Resizes images to fit standard cake dimensions (8x10 inches at 300 DPI)
- Maintains aspect ratio
- High-quality resampling for best print results
- Reduces file size while maintaining quality
- Converts transparent backgrounds to white for printing

## Custom Dimensions

You can also import and use the function with custom dimensions:

```python
from resize_for_cake import resize_image_for_cake

# Resize for a smaller cake (6x8 inches at 300 DPI)
resize_image_for_cake("input.jpg", "output.jpg", max_width=1800, max_height=2400)
```
