#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
files = sorted((ROOT / "pages").glob("R*.png"))
assert len(files) == 32
for group in range(4):
    batch = files[group * 8:(group + 1) * 8]
    first = Image.open(batch[0]).convert("RGB")
    width, height = first.size
    label = 18
    canvas = Image.new("RGB", (4 * width, 2 * (height + label)), (29, 32, 38))
    draw = ImageDraw.Draw(canvas)
    for i, path in enumerate(batch):
        x = (i % 4) * width
        y = (i // 4) * (height + label)
        draw.text((x + 2, y + 2), path.stem, fill="white")
        canvas.paste(Image.open(path).convert("RGB"), (x, y + label))
    canvas.resize((canvas.width * 2, canvas.height * 2), Image.Resampling.NEAREST).save(ROOT / f"blind_sheet_{group + 1}.png")
print("WROTE 4 blind sheets")
