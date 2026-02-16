# 🎂 Cake Sizes Guide

## Standard Cake Dimensions

This guide helps you choose the right size for your cake image.

### Round Cakes

| Size | Serves | Recommended Pixels | Physical Size |
|------|--------|-------------------|---------------|
| 6" Round | 8-10 | 1800x1800 | Small celebration |
| 8" Round | 15-20 | 2400x2400 | Standard birthday |
| 10" Round | 25-30 | 3000x3000 | Large party |
| 12" Round | 35-40 | 3600x3600 | Big celebration |

### Sheet Cakes

| Size | Serves | Recommended Pixels | Physical Size |
|------|--------|-------------------|---------------|
| Quarter Sheet (9x13") | 20-30 | 2700x3900 | Small party |
| Half Sheet (12x18") | 40-60 | 3600x5400 | Large party |
| Full Sheet (18x26") | 80-100 | 5400x7800 | Very large event |

### Square Cakes

| Size | Serves | Recommended Pixels | Physical Size |
|------|--------|-------------------|---------------|
| 6" Square | 12-15 | 1800x1800 | Small |
| 8" Square | 20-25 | 2400x2400 | Standard |
| 10" Square | 30-35 | 3000x3000 | Large |

## Resolution Guide

**DPI (Dots Per Inch)** determines print quality:

- **300 DPI** - Professional quality (RECOMMENDED for cakes)
- **200 DPI** - Good quality
- **150 DPI** - Acceptable quality
- **Below 150 DPI** - May look pixelated

### How to Calculate Pixels Needed

```
Pixels = Inches × DPI

Example for 8" cake at 300 DPI:
8 × 300 = 2400 pixels
```

## Image Quality Tips

### ✅ Best Practices

1. **Use high-resolution images** - Start with the largest image possible
2. **Avoid stretching** - Let the tool maintain aspect ratio
3. **Check image clarity** - Zoom in to check details before printing
4. **Use RGB color mode** - Most printers prefer RGB over CMYK
5. **Avoid overly dark images** - They may look muddy on cakes
6. **Test with printer** - Ask for a small sample print first

### ❌ Avoid

1. **Low resolution images** - Screenshots and social media images are often too small
2. **Heavy compression** - Repeatedly saved JPEGs lose quality
3. **Extreme cropping** - May reduce detail too much
4. **Very busy patterns** - Simple, clear images work best on cakes

## For Your Hot Wheels Image

The Hot Wheels image you have appears to be a colorful cartoon scene, which is perfect for cake printing!

**Recommended settings:**
- **Small cake (serves 10-15):** Use preset #1 (6-8" round)
- **Standard cake (serves 15-25):** Use preset #2 (8x10" sheet) ⭐ DEFAULT
- **Large cake (serves 25+):** Use preset #3 or #4

### Why these settings work well:

1. **Bright colors** - Will print vibrantly on frosting
2. **Cartoon style** - Clear lines and shapes work great on cakes
3. **Characters** - The Hot Wheels characters will be recognizable even at smaller sizes
4. **Good contrast** - Dark and light areas will show up well

## Talking to Your Cake Printer

When you contact your cake baker/printer, provide:

1. **The resized image file** (from the output/ folder)
2. **Desired cake size** (in inches)
3. **Image dimensions** (shown in the resize output)
4. **Any special instructions** (borders, text to add, etc.)

Most bakers prefer:
- **File format:** JPEG or PNG
- **File size:** Under 5MB (easy to email)
- **Resolution:** 200-300 DPI
- **Delivery method:** Email or USB drive

## Common Questions

**Q: My image is landscape, but the cake is square. What happens?**
A: The tool maintains aspect ratio, so your image will fit within the square with space on sides. This is normal and looks good!

**Q: Can I use multiple images?**
A: Yes! Just place all images in the input/ folder. Each will be resized separately.

**Q: The file size decreased a lot. Is quality lost?**
A: The tool optimizes the JPEG compression while maintaining visual quality. The resized image will still look great on a cake!

**Q: Do I need to crop my image first?**
A: It helps! Crop out unnecessary borders or background before resizing for best results.

**Q: Can the baker add text?**
A: Yes! Most bakers can add "Happy Birthday" or other text on top of the image.

## Quick Reference Commands

```bash
# Interactive menu (recommended)
python3 resize_presets.py

# Quick batch processing
python3 batch_resize.py

# Single image
python3 resize_for_cake.py your_image.jpg
```

---

**Need more help?** Check out QUICK_START.md for step-by-step instructions!
