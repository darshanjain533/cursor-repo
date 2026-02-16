#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Literal

from PIL import Image, ImageChops, ImageDraw, ImageOps


FitMode = Literal["cover", "contain"]


@dataclass(frozen=True)
class Preset:
    name: str
    width_in: float
    height_in: float

    def px(self, dpi: int) -> tuple[int, int]:
        return (int(round(self.width_in * dpi)), int(round(self.height_in * dpi)))


PRESETS: dict[str, Preset] = {
    # Round cakes are typically printed as a square then cut as a circle.
    "round6": Preset("round6", 6.0, 6.0),
    "round7": Preset("round7", 7.0, 7.0),
    "round8": Preset("round8", 8.0, 8.0),
    # Common rectangle edible-print sizes.
    "rect8x6": Preset("rect8x6", 8.0, 6.0),
    "rect10x8": Preset("rect10x8", 10.0, 8.0),
}


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Resize an image into compact cake-ready print sizes (inches -> pixels @ DPI)."
    )
    p.add_argument("--input", "-i", required=True, help="Path to input image (png/jpg/webp/etc).")
    p.add_argument("--output-dir", "-o", default="out", help="Output directory. Default: out/")
    p.add_argument(
        "--presets",
        nargs="+",
        default=list(PRESETS.keys()),
        help=f"Presets to generate. Choices: {', '.join(PRESETS.keys())}. Default: all.",
    )
    p.add_argument("--dpi", type=int, default=300, help="DPI for inch->pixel conversion. Default: 300")
    p.add_argument(
        "--fit",
        choices=["cover", "contain"],
        default="cover",
        help="How to fit source into target: cover=crop, contain=letterbox. Default: cover",
    )
    p.add_argument(
        "--trim",
        action="store_true",
        help="Trim uniform outer margins (e.g., white border) before resizing.",
    )
    p.add_argument(
        "--trim-tolerance",
        type=int,
        default=12,
        help="Trim tolerance (0-255). Higher trims more. Default: 12",
    )
    p.add_argument(
        "--pad-pct",
        type=float,
        default=0.015,
        help="After trim, add padding as fraction of max(w,h). Default: 0.015 (1.5%%).",
    )
    p.add_argument(
        "--circle-mask",
        action="store_true",
        help="For square presets, apply a circular mask (useful for round cakes).",
    )
    p.add_argument(
        "--transparent",
        action="store_true",
        help="When using --circle-mask, keep outside area transparent (PNG). Default is white background.",
    )
    p.add_argument(
        "--format",
        choices=["png", "jpg"],
        default="png",
        help="Output format. Default: png",
    )
    return p.parse_args()


def _trim_uniform_border(im: Image.Image, tolerance: int) -> Image.Image:
    """
    Trim a uniform border based on the corner color with a tolerance.
    Works well for removing outer white margins around framed images.
    """
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA")

    # Use RGB for diff; alpha can confuse the bbox if it varies.
    rgb = im.convert("RGB")
    bg_color = rgb.getpixel((0, 0))
    bg = Image.new("RGB", rgb.size, bg_color)
    diff = ImageChops.difference(rgb, bg).convert("L")
    bw = diff.point(lambda p: 255 if p > tolerance else 0)
    bbox = bw.getbbox()
    if not bbox:
        return im
    return im.crop(bbox)


def _add_padding(im: Image.Image, pad_px: int, fill=(255, 255, 255, 0)) -> Image.Image:
    if pad_px <= 0:
        return im
    return ImageOps.expand(im, border=pad_px, fill=fill)


def _resize_to_target(im: Image.Image, target_w: int, target_h: int, fit: FitMode) -> Image.Image:
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA")

    if fit == "contain":
        # Letterbox/pillarbox into *exact* target size.
        contained = ImageOps.contain(im, (target_w, target_h), Image.Resampling.LANCZOS)
        if contained.mode != "RGBA":
            contained = contained.convert("RGBA")
        bg = Image.new("RGBA", (target_w, target_h), (255, 255, 255, 255))
        x = (target_w - contained.size[0]) // 2
        y = (target_h - contained.size[1]) // 2
        bg.paste(contained, (x, y), mask=contained.getchannel("A"))
        return bg

    # cover: crop to fill target
    src_w, src_h = im.size
    src_ratio = src_w / src_h
    tgt_ratio = target_w / target_h

    if src_ratio > tgt_ratio:
        # too wide; crop width
        new_w = int(round(src_h * tgt_ratio))
        left = (src_w - new_w) // 2
        im = im.crop((left, 0, left + new_w, src_h))
    else:
        # too tall; crop height
        new_h = int(round(src_w / tgt_ratio))
        top = (src_h - new_h) // 2
        im = im.crop((0, top, src_w, top + new_h))

    return im.resize((target_w, target_h), Image.Resampling.LANCZOS)


def _apply_circle_mask(im: Image.Image, transparent: bool) -> Image.Image:
    if im.mode != "RGBA":
        im = im.convert("RGBA")

    w, h = im.size
    if w != h:
        raise ValueError("--circle-mask requires a square image (use a round preset like round6).")

    mask = Image.new("L", (w, h), 0)
    # Slight inset to avoid anti-aliased edge clipping.
    inset = max(2, int(round(w * 0.002)))
    d = ImageDraw.Draw(mask)
    d.ellipse((inset, inset, w - inset, h - inset), fill=255)

    if transparent:
        out = Image.new("RGBA", (w, h), (255, 255, 255, 0))
        out.paste(im, (0, 0), mask=mask)
        return out

    # White background outside the circle.
    out = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    out.paste(im, (0, 0), mask=mask)
    return out


def _save(im: Image.Image, out_path: Path, dpi: int, fmt: str) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if fmt == "jpg":
        # JPEG doesn't support alpha; flatten to white.
        if im.mode == "RGBA":
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.getchannel("A"))
            im = bg
        else:
            im = im.convert("RGB")
        im.save(out_path, format="JPEG", quality=92, optimize=True, dpi=(dpi, dpi))
        return

    # PNG: keep RGBA if present. Store DPI metadata where supported.
    im.save(out_path, format="PNG", optimize=True, dpi=(dpi, dpi))


def main() -> int:
    args = _parse_args()
    in_path = Path(args.input)
    out_dir = Path(args.output_dir)
    dpi: int = args.dpi
    fit: FitMode = args.fit

    if not in_path.exists():
        raise FileNotFoundError(f"Input not found: {in_path}")

    unknown = [p for p in args.presets if p not in PRESETS]
    if unknown:
        raise SystemExit(f"Unknown preset(s): {', '.join(unknown)}")

    im = Image.open(in_path)
    im.load()

    if args.trim:
        im = _trim_uniform_border(im, tolerance=max(0, min(255, int(args.trim_tolerance))))
        pad_px = int(round(max(im.size) * max(0.0, float(args.pad_pct))))
        # Use transparent padding if image already has alpha; otherwise white.
        fill = (255, 255, 255, 0) if im.mode == "RGBA" else (255, 255, 255)
        im = _add_padding(im, pad_px=pad_px, fill=fill)

    stem = in_path.stem
    for preset_name in args.presets:
        preset = PRESETS[preset_name]
        target_w, target_h = preset.px(dpi)
        out = _resize_to_target(im, target_w, target_h, fit=fit)

        if args.circle_mask and target_w == target_h:
            out = _apply_circle_mask(out, transparent=bool(args.transparent))

        suffix = "jpg" if args.format == "jpg" else "png"
        out_path = out_dir / f"{stem}__{preset_name}__{target_w}x{target_h}@{dpi}dpi.{suffix}"
        _save(out, out_path, dpi=dpi, fmt=args.format)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
