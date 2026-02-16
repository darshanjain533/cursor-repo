# 🎂 Quick Start Guide - Resize Image for Cake

## Step-by-Step Instructions

### For Your Hot Wheels Image:

1. **Save your Hot Wheels image** to the `input/` folder
   - You can name it anything (e.g., `hot_wheels.jpg`, `cake_image.png`, etc.)

2. **Run the batch processor**:
   ```bash
   python3 batch_resize.py
   ```

3. **Get your resized image** from the `output/` folder
   - It will be named something like `hot_wheels_cake.jpg`
   - This image is now perfect for cake printing!

## What Happens?

Your image will be automatically:
- ✅ Resized to fit an 8-10 inch cake
- ✅ Optimized to 2400x3000 pixels (300 DPI)
- ✅ Converted to high-quality JPEG format
- ✅ Reduced in file size (easier to email to cake printer)
- ✅ Aspect ratio maintained (no distortion)

## Example Output

```
Processing: hot_wheels_image.jpg
  Original: 4032x3024 pixels (2547.83 KB)
  Resized: 2400x1800 pixels (856.42 KB)
  Cake size: ~8.0" x 6.0" (at 300 DPI)
  Saved to: output/hot_wheels_image_cake.jpg
```

## Common Cake Sizes

If you need different dimensions, here are standard cake sizes:

| Cake Size | Dimensions | Command |
|-----------|------------|---------|
| Quarter Sheet (9x13") | 2700x3900px | Default settings |
| Half Sheet (12x18") | 3600x5400px | See custom sizes below |
| Round 8" | 2400x2400px | Use square dimensions |
| Round 10" | 3000x3000px | Use square dimensions |

## Custom Sizes

To resize for a specific cake size, edit `batch_resize.py` and change these values:

```python
# For a 6x8 inch cake:
resize_image_for_cake(image_file, output_dir, max_width=1800, max_height=2400)

# For a 10x12 inch cake:
resize_image_for_cake(image_file, output_dir, max_width=3000, max_height=3600)
```

## Troubleshooting

**Q: Image is too small/large?**
A: Adjust the `max_width` and `max_height` parameters in the script.

**Q: Image looks stretched?**
A: The tool automatically maintains aspect ratio, so this shouldn't happen. Check your original image.

**Q: Need better quality?**
A: Increase the `quality` parameter (default is 95, max is 100).

**Q: Transparent background?**
A: The tool automatically converts to white background for printing.

## Send to Your Cake Printer

Once you have your resized image:
1. Check with your cake printer for their specific requirements
2. Most accept images via email or USB drive
3. Specify the exact cake size you want
4. Show them the resized image dimensions

## Need Help?

The resized image should work for most cake printers. If they have specific requirements, you can easily adjust the settings in the script!
