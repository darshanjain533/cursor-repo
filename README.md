## Cake image resize (compact / print-ready)

This repo includes a small script to resize an image into common “cake topper” print sizes.

### Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Generate compact cake sizes

Replace `INPUT_IMAGE` with the path to your image.

```bash
python scripts/resize_for_cake.py \
  --input "INPUT_IMAGE" \
  --output-dir out \
  --trim \
  --presets round6 round7 round8 rect8x6 rect10x8
```

### Notes

- **DPI**: Defaults to **300 DPI** (good for edible printing). You can change with `--dpi`.
- **Trim**: `--trim` removes uniform outer margins (often a white border) before resizing, making the result more compact.
- **Round cakes**: Use `round6/round7/round8` presets; optionally add `--circle-mask` (PNG) if you want a circular cutout.
