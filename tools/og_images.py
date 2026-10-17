"""Link preview images (og:image, 1200x630) for guides and Learn articles.

build.py calls make() for every page when Pillow is installed (locally). The PNGs go to
static/og/ and are committed, so the GitHub Actions build, which has no Pillow, just copies them.
static/og/manifest.json remembers what each image was drawn from; a changed title redraws it.
"""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (251, 250, 247)
TEXT = (29, 31, 35)
MUTED = (95, 101, 112)
ACCENT = (15, 123, 95)
SOFT = (227, 243, 237)
VERSION = "2"  # bump to redraw every image after a design change

FONTS = {
    "bold": ["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"],
    "semi": ["seguisb.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"],
    "regular": ["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"],
}


def font(kind, size):
    for name in FONTS[kind]:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def compass(draw, cx, cy, r):
    """static/favicon.svg, scaled: 32-unit box, outer r15, ring r11, needle 9 up/down, 3.5 wide."""
    s = r / 15
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ACCENT)
    draw.ellipse((cx - 11 * s, cy - 11 * s, cx + 11 * s, cy + 11 * s), outline=(255, 255, 255), width=max(2, round(2 * s)))
    draw.polygon([(cx, cy - 9 * s), (cx + 3.5 * s, cy), (cx, cy + 9 * s), (cx - 3.5 * s, cy)], fill=(255, 255, 255))
    draw.ellipse((cx - 2 * s, cy - 2 * s, cx + 2 * s, cy + 2 * s), fill=ACCENT)


def render(title, label, out, sub=""):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 18, H), fill=ACCENT)
    pad = 84

    compass(d, pad + 26, 92, 26)
    d.text((pad + 62, 92), "GigCompass", font=font("bold", 38), fill=TEXT, anchor="lm")

    lf = font("semi", 26)
    lw = d.textlength(label, font=lf)
    d.rounded_rectangle((pad, 166, pad + lw + 40, 214), radius=24, fill=SOFT)
    d.text((pad + 20, 190), label, font=lf, fill=ACCENT, anchor="lm")

    # Largest size at which the title fits the space above the footer line (about 250px).
    for size in (72, 66, 60, 56, 52, 48, 44):
        tf = font("bold", size)
        lines = wrap(d, title, tf, W - pad * 2)
        if len(lines) * size * 1.2 <= 250:
            break
    y = 252
    for ln in lines[:4]:
        d.text((pad, y), ln, font=tf, fill=TEXT)
        y += int(size * 1.2)
    if sub and len(lines) == 1:
        d.text((pad, y + 18), sub, font=font("regular", 34), fill=MUTED)

    d.line((pad, H - 96, W - pad, H - 96), fill=(228, 225, 218), width=2)
    d.text((pad, H - 56), "Practical hiring guides for freelance services", font=font("regular", 26),
           fill=MUTED, anchor="lm")
    d.text((W - pad, H - 56), "thegigcompass.com", font=font("semi", 26), fill=ACCENT, anchor="rm")

    out.parent.mkdir(parents=True, exist_ok=True)
    img.quantize(colors=64, method=Image.Quantize.MEDIANCUT).save(out, optimize=True)


def make(og_dir, items):
    """items: {key: (title, label, sub)}. Draws new or changed images, deletes ones no page uses."""
    og_dir = Path(og_dir)
    mf = og_dir / "manifest.json"
    old = json.loads(mf.read_text(encoding="utf-8")) if mf.exists() else {}
    new, drawn = {}, 0
    for key, (title, label, sub) in items.items():
        h = hashlib.sha1(f"{VERSION}|{title}|{label}|{sub}".encode()).hexdigest()[:12]
        new[key] = h
        out = og_dir / f"{key}.png"
        if old.get(key) != h or not out.exists():
            render(title, label, out, sub)
            drawn += 1
    for key in set(old) - set(new):
        (og_dir / f"{key}.png").unlink(missing_ok=True)
    mf.write_text(json.dumps(new, indent=0, sort_keys=True), encoding="utf-8")
    return drawn


if __name__ == "__main__":
    import sys
    render(sys.argv[1], sys.argv[2], Path(sys.argv[3]))
