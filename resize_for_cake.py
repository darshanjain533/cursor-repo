#!/usr/bin/env python3
"""
Resize images to compact dimensions suitable for cake printing.
Typical cake edible images: 2-4 inches. At 300 DPI: 600-1200px.
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)


# Cake-friendly dimensions (width, height) in pixels at 300 DPI
# 2" = 600px, 3" = 900px, 4" = 1200px
CAKE_SIZES = {
    "small": (600, 600),   # ~2" square - compact for small cakes
    "medium": (900, 900),  # ~3" square
    "large": (1200, 1200), # ~4" square
}


def resize_for_cake(
    input_path: str,
    output_path: str | None = None,
    max_dimension: int = 600,
    quality: int = 95,
    remove_border_percent: float = 0,
) -> str:
    """
    Resize an image to compact dimensions for cake printing.
    
    Args:
        input_path: Path to source image
        output_path: Path for resized image (default: adds _cake suffix)
        max_dimension: Maximum width or height in pixels (default 600 = ~2")
        quality: JPEG quality 1-100 (default 95)
        remove_border_percent: Crop this % from each edge to remove borders (0-20)
    
    Returns:
        Path to the saved image
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Image not found: {input_path}")

    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_cake{input_path.suffix}"
    output_path = Path(output_path)

    img = Image.open(input_path).convert("RGB")

    # Optionally crop border (e.g., ornate frame) to make more compact
    if remove_border_percent > 0:
        w, h = img.size
        crop_pct = min(remove_border_percent / 100, 0.2)  # Cap at 20%
        left = int(w * crop_pct)
        top = int(h * crop_pct)
        right = int(w * (1 - crop_pct))
        bottom = int(h * (1 - crop_pct))
        img = img.crop((left, top, right, bottom))

    # Resize maintaining aspect ratio
    w, h = img.size
    if w > max_dimension or h > max_dimension:
        ratio = min(max_dimension / w, max_dimension / h)
        new_size = (int(w * ratio), int(h * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    # Save
    if output_path.suffix.lower() in (".jpg", ".jpeg"):
        img.save(output_path, "JPEG", quality=quality, optimize=True)
    else:
        output_path = output_path.with_suffix(".jpg")
        img.save(output_path, "JPEG", quality=quality, optimize=True)

    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Resize images to compact dimensions for cake printing"
    )
    parser.add_argument(
        "image",
        help="Path to the image file to resize",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output path (default: input_cake.jpg)",
    )
    parser.add_argument(
        "-s", "--size",
        choices=["small", "medium", "large"],
        default="small",
        help="Target size: small (~2\"), medium (~3\"), large (~4\")",
    )
    parser.add_argument(
        "-p", "--pixels",
        type=int,
        help="Override max dimension in pixels (e.g., 500 for extra compact)",
    )
    parser.add_argument(
        "-b", "--remove-border",
        type=float,
        default=0,
        metavar="PERCENT",
        help="Crop this %% from each edge to remove ornate borders (e.g., 5)",
    )
    parser.add_argument(
        "-q", "--quality",
        type=int,
        default=95,
        help="JPEG quality 1-100 (default: 95)",
    )

    args = parser.parse_args()
    max_dim = args.pixels or CAKE_SIZES[args.size][0]

    try:
        out = resize_for_cake(
            args.image,
            output_path=args.output,
            max_dimension=max_dim,
            quality=args.quality,
            remove_border_percent=args.remove_border,
        )
        print(f"Saved compact image: {out}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
