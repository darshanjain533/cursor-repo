# Cake Image Resizer

A Python tool to resize images to small, compact dimensions suitable for printing on cakes (edible paper, fondant transfers, cake toppers).

## Requirements

- Python 3.8+
- Pillow (`pip install Pillow`)

## Quick Start

```bash
pip install Pillow
python3 resize_for_cake.py your_image.png --size compact
```

This will create a resized file named `your_image_cake_ready.png` at **4" x 6"** print size — small and compact enough to fit on most cakes.

## Available Cake Size Presets

| Preset          | Dimensions      | Best For                          |
|-----------------|-----------------|-----------------------------------|
| `mini`          | 3" x 4"         | Cupcake toppers, very small cakes |
| `compact`       | 4" x 6"         | Standard cake top (default)       |
| `small_round`   | 6" diameter      | Small round cakes                 |
| `medium_round`  | 8" diameter      | Standard round cakes              |
| `quarter_sheet` | 7" x 10"        | Quarter sheet cakes               |
| `half_sheet`    | 11" x 15"       | Half sheet cakes                  |

## Usage Examples

### Compact size (recommended for fitting on a cake)
```bash
python3 resize_for_cake.py hotwheels.png --size compact
```

### Very small / cupcake size
```bash
python3 resize_for_cake.py hotwheels.png --size mini
```

### Round cake (applies circular mask)
```bash
python3 resize_for_cake.py hotwheels.png --size small_round
```

### Custom pixel dimensions
```bash
python3 resize_for_cake.py hotwheels.png --width 600 --height 400
```

### Higher DPI for sharper print
```bash
python3 resize_for_cake.py hotwheels.png --size compact --dpi 300
```

### With sharpening for better print clarity
```bash
python3 resize_for_cake.py hotwheels.png --size compact --sharpen
```

### Custom output path
```bash
python3 resize_for_cake.py hotwheels.png --size compact -o cake_image_final.png
```

### List all presets
```bash
python3 resize_for_cake.py --list-sizes
```

## How It Works

1. Opens your image (supports PNG, JPG, JPEG, BMP, TIFF, WebP)
2. Resizes to the chosen cake preset while **preserving aspect ratio** (no stretching or distortion)
3. Optionally applies a **circular mask** for round cakes
4. Optionally **sharpens** the image for better print quality
5. Saves with print-quality settings (95% quality, DPI metadata embedded)

## Tips for Best Results

- Use **`compact`** (4"x6") or **`mini`** (3"x4") for a small, compact image that fits nicely on a cake
- Use **`--sharpen`** flag to improve clarity after downsizing
- Use **`--dpi 300`** if your cake printer supports high-resolution printing
- For round cakes, the round presets automatically crop to a circle
- The tool preserves aspect ratio — your image won't be stretched or squished
