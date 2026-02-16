# Image Dimensions for Cake

Resize images to small, compact dimensions suitable for cake printing (edible icing sheets, toppers, etc.).

## Quick Start

1. **Save your image** to this folder (e.g., `hotwheels.png`)

2. **Install dependency:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Resize for cake:**
   ```bash
   python resize_for_cake.py your_image.png
   ```

   This creates `your_image_cake.jpg` at ~2" (600px) max dimension—compact for small cakes.

## Options

| Option | Description |
|--------|-------------|
| `-s small` | ~2" (default, most compact) |
| `-s medium` | ~3" |
| `-s large` | ~4" |
| `-p 500` | Custom max pixels (e.g., 500 for extra compact) |
| `-b 5` | Remove 5% from each edge (helps trim ornate borders) |
| `-o output.jpg` | Custom output path |

## Examples

```bash
# Extra compact (500px max)
python resize_for_cake.py image.png -p 500

# Trim ornate border, then resize
python resize_for_cake.py image.png -b 5 -s small

# Medium size, custom output
python resize_for_cake.py image.png -o cake_ready.jpg -s medium
```

## Typical Cake Sizes

- **Edible icing sheets:** 2–4 inches
- **300 DPI** (print quality): 600px = 2", 900px = 3", 1200px = 4"
