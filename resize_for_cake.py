#!/usr/bin/env python3
"""
Cake Image Resizer
==================
Resizes images to compact, cake-friendly dimensions suitable for
printing on cake toppers, edible paper, or fondant transfers.

Common cake sizes supported:
  - small_round   :  6" diameter  (compact, single-layer cakes)
  - medium_round  :  8" diameter  (standard round cakes)
  - quarter_sheet :  7" x 10"    (quarter sheet cakes)
  - half_sheet    : 11" x 15"    (half sheet cakes)
  - compact       :  4" x 6"     (small rectangular, ideal for fitting on top)
  - mini          :  3" x 4"     (very small, cupcake-sized)

Usage:
    python3 resize_for_cake.py <input_image> [--size SIZE] [--dpi DPI] [--output OUTPUT]

Examples:
    python3 resize_for_cake.py hotwheels.png --size compact
    python3 resize_for_cake.py hotwheels.png --size small_round --dpi 150
    python3 resize_for_cake.py hotwheels.png --size mini --output cake_ready.png
    python3 resize_for_cake.py hotwheels.png --width 600 --height 450
"""

import argparse
import sys
import math
from pathlib import Path

try:
    from PIL import Image, ImageFilter
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)


CAKE_SIZES = {
    "mini": {
        "description": "Very small / cupcake topper (3\" x 4\")",
        "width_inches": 4,
        "height_inches": 3,
        "shape": "rectangle",
    },
    "compact": {
        "description": "Small rectangular, ideal for cake top (4\" x 6\")",
        "width_inches": 6,
        "height_inches": 4,
        "shape": "rectangle",
    },
    "small_round": {
        "description": "Small round cake topper (6\" diameter)",
        "diameter_inches": 6,
        "shape": "circle",
    },
    "medium_round": {
        "description": "Standard round cake topper (8\" diameter)",
        "diameter_inches": 8,
        "shape": "circle",
    },
    "quarter_sheet": {
        "description": "Quarter sheet cake (7\" x 10\")",
        "width_inches": 10,
        "height_inches": 7,
        "shape": "rectangle",
    },
    "half_sheet": {
        "description": "Half sheet cake (11\" x 15\")",
        "width_inches": 15,
        "height_inches": 11,
        "shape": "rectangle",
    },
}

DEFAULT_DPI = 150


def get_target_pixels(size_name, dpi):
    """Convert a cake size preset to pixel dimensions."""
    preset = CAKE_SIZES[size_name]

    if preset["shape"] == "circle":
        d = preset["diameter_inches"]
        px = int(d * dpi)
        return px, px
    else:
        w = preset["width_inches"]
        h = preset["height_inches"]
        return int(w * dpi), int(h * dpi)


def resize_image(img, target_w, target_h, keep_aspect=True):
    """
    Resize image to fit within target dimensions.
    If keep_aspect is True, the image is scaled to fit inside the
    target box while preserving the aspect ratio (no cropping, no distortion).
    """
    if keep_aspect:
        img.thumbnail((target_w, target_h), Image.LANCZOS)
        return img
    else:
        return img.resize((target_w, target_h), Image.LANCZOS)


def apply_circle_mask(img):
    """Apply a circular mask to make the image round (for round cakes)."""
    size = min(img.size)
    mask = Image.new("L", (size, size), 0)
    from PIL import ImageDraw
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size - 1, size - 1), fill=255)

    if img.size[0] != img.size[1]:
        left = (img.size[0] - size) // 2
        top = (img.size[1] - size) // 2
        img = img.crop((left, top, left + size, top + size))

    output = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    output.paste(img, (0, 0), mask)
    return output


def main():
    parser = argparse.ArgumentParser(
        description="Resize images to cake-friendly dimensions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("input", nargs="?", help="Path to the input image file")
    parser.add_argument(
        "--size",
        choices=list(CAKE_SIZES.keys()),
        default="compact",
        help="Cake size preset (default: compact)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=DEFAULT_DPI,
        help=f"Print DPI (default: {DEFAULT_DPI})",
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: <input>_cake_ready.<ext>)",
    )
    parser.add_argument(
        "--width",
        type=int,
        help="Custom target width in pixels (overrides --size)",
    )
    parser.add_argument(
        "--height",
        type=int,
        help="Custom target height in pixels (overrides --size)",
    )
    parser.add_argument(
        "--round",
        action="store_true",
        help="Apply circular mask (for round cakes)",
    )
    parser.add_argument(
        "--sharpen",
        action="store_true",
        help="Apply slight sharpening after resize (improves print clarity)",
    )
    parser.add_argument(
        "--list-sizes",
        action="store_true",
        help="List all available cake size presets and exit",
    )

    args = parser.parse_args()

    if args.list_sizes:
        print("\nAvailable cake size presets:\n")
        for name, info in CAKE_SIZES.items():
            print(f"  {name:16s}  {info['description']}")
        print(f"\nDefault DPI: {DEFAULT_DPI}")
        print()
        sys.exit(0)

    if not args.input:
        parser.error("the following arguments are required: input")

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    img = Image.open(input_path)
    original_size = img.size
    print(f"Original image: {original_size[0]}x{original_size[1]} pixels")

    if args.width and args.height:
        target_w, target_h = args.width, args.height
        print(f"Custom target: {target_w}x{target_h} pixels")
    else:
        target_w, target_h = get_target_pixels(args.size, args.dpi)
        preset = CAKE_SIZES[args.size]
        print(f"Cake preset: {args.size} - {preset['description']}")
        print(f"DPI: {args.dpi}")
        print(f"Target: {target_w}x{target_h} pixels")

    is_round = args.round or CAKE_SIZES.get(args.size, {}).get("shape") == "circle"

    img = resize_image(img, target_w, target_h, keep_aspect=True)
    print(f"Resized to: {img.size[0]}x{img.size[1]} pixels")

    if is_round:
        img = apply_circle_mask(img)
        print("Applied circular mask for round cake")

    if args.sharpen:
        img = img.filter(ImageFilter.SHARPEN)
        print("Applied sharpening filter")

    if args.output:
        output_path = Path(args.output)
    else:
        suffix = input_path.suffix or ".png"
        output_path = input_path.with_name(f"{input_path.stem}_cake_ready{suffix}")

    if img.mode == "RGBA" and output_path.suffix.lower() in (".jpg", ".jpeg"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg

    img.save(output_path, quality=95, dpi=(args.dpi, args.dpi))

    file_size_kb = output_path.stat().st_size / 1024
    print(f"\nSaved: {output_path}")
    print(f"File size: {file_size_kb:.1f} KB")
    print(f"Dimensions: {img.size[0]}x{img.size[1]} pixels")

    if not (args.width and args.height):
        preset = CAKE_SIZES[args.size]
        if preset["shape"] == "circle":
            d = preset["diameter_inches"]
            print(f"Print size at {args.dpi} DPI: {d}\" diameter")
        else:
            w_in = img.size[0] / args.dpi
            h_in = img.size[1] / args.dpi
            print(f"Print size at {args.dpi} DPI: {w_in:.1f}\" x {h_in:.1f}\"")

    print("\nDone! Your image is ready for cake printing.")


if __name__ == "__main__":
    main()
