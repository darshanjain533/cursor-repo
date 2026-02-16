# Image Resizer for Cake Printing

This tool resizes images to optimal dimensions for printing on cakes.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start (Batch Processing - RECOMMENDED)

**This is the easiest method!**

1. Place your images in the `input/` folder
2. Run the batch processor:
   ```bash
   python batch_resize.py
   ```
3. Find your resized images in the `output/` folder

That's it! All images will be automatically resized to cake-friendly dimensions.

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
