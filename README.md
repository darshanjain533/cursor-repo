# Image Resizer for Cake Printing

This tool resizes images to optimal dimensions for printing on cakes.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start - Three Easy Ways to Resize

### Method 1: Interactive Menu with Presets (BEST FOR BEGINNERS) ⭐

Choose from preset cake sizes with an interactive menu:

1. Place your images in the `input/` folder
2. Run the preset tool:
   ```bash
   python3 resize_presets.py
   ```
3. Select your cake size from the menu
4. Find your resized images in the `output/` folder

**Available presets:**
- Small Round (6-8 inches)
- Standard Sheet (8x10 inches) - Default
- Large Round (10-12 inches)
- Quarter Sheet (9x13 inches)
- Half Sheet (12x18 inches)
- Square Cake (8x8 inches)

### Method 2: Automatic Batch Processing (FASTEST)

Process all images with default settings (8x10 inch cake):

1. Place your images in the `input/` folder
2. Run the batch processor:
   ```bash
   python3 batch_resize.py
   ```
3. Find your resized images in the `output/` folder

### Method 3: Single Image Processing

For processing one specific image:

```bash
python3 resize_for_cake.py <your_image.jpg>
```

## Alternative: Single Image Processing

If you want to resize a specific image:

```bash
python resize_for_cake.py <your_image.jpg>
```

Example:
```bash
python resize_for_cake.py hot_wheels_image.jpg
```

This will create a resized version (e.g., `hot_wheels_image_cake.jpg`) in the same directory.

## Features

- ✨ **Batch processing** - Resize multiple images at once
- 📏 **Optimal dimensions** - Resizes to fit standard cake dimensions (8x10 inches at 300 DPI)
- 🎨 **Maintains aspect ratio** - Your images won't look stretched or squashed
- 🖼️ **High-quality resampling** - Uses LANCZOS algorithm for best print results
- 💾 **Reduces file size** - Optimizes images while maintaining quality
- 🎯 **White backgrounds** - Converts transparent backgrounds to white for printing
- 📊 **Detailed output** - Shows original and new dimensions plus file sizes

## What You Get

For a standard 8x10 inch cake at 300 DPI, your images will be resized to:
- Maximum width: 2400 pixels
- Maximum height: 3000 pixels
- Format: High-quality JPEG
- Optimized file size for easy sharing with cake printers

## Custom Dimensions

Need a different size? You can modify the dimensions in the scripts or use the function directly:

```python
from resize_for_cake import resize_image_for_cake

# Resize for a smaller cake (6x8 inches at 300 DPI)
resize_image_for_cake("input.jpg", "output.jpg", max_width=1800, max_height=2400)
```

## Supported Formats

Input: JPG, JPEG, PNG, GIF, BMP, WEBP
Output: Optimized JPEG
