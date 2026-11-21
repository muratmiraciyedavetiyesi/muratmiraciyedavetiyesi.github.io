#!/usr/bin/env python3
"""Generate the Derya–Ibrahim WhatsApp preview from the approved original floral layout."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
DEST = Path(__file__).resolve().parent / "davetiye-paylasim.jpg"
S = 2

def font_from_woff2(filename):
    source = ROOT / filename
    ttf_path = source.with_suffix(".temporary.ttf")
    font = TTFont(str(source))
    font.flavor = None
    font.save(str(ttf_path))
    return ttf_path

def main():
    source = Image.open(ROOT / "davetiye-paylasim-2026.jpg").convert("RGB")
    canvas = source.resize((1200 * S, 630 * S), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(canvas)
    draw.ellipse((280*S, 39*S, 920*S, 594*S), fill=(248, 240, 226))
    draw.ellipse((276*S, 35*S, 924*S, 597*S), outline=(170, 134, 84), width=2*S)
    draw.ellipse((282*S, 41*S, 918*S, 591*S), outline=(196, 164, 115), width=1*S)

    text_color = (108, 80, 56)
    gold = (158, 126, 84)
    gv = font_from_woff2("great-vibes-400.woff2")
    cg = font_from_woff2("cormorant-garamond-500.woff2")

    def text_center(text, y, font_path, size, fill=text_color, tracking=0, maxwidth=600):
        f = ImageFont.truetype(str(font_path), size * S)
        while True:
            box = draw.textbbox((0, 0), text, font=f)
            width = box[2]-box[0] + max(0, len(text)-1) * tracking * S
            if width <= maxwidth*S or size <= 15:
                break
            size -= 1
            f = ImageFont.truetype(str(font_path), size * S)
        start_x = (1200*S - width) / 2
        ypos = y*S - box[1]
        if tracking:
            x=start_x
            for ch in text:
                draw.text((int(x), int(ypos)), ch, font=f, fill=fill)
                cbox=draw.textbbox((0,0),ch,font=f)
                x+=cbox[2]-cbox[0]+tracking*S
        else:
            draw.text((int(start_x-box[0]),int(ypos)),text,font=f,fill=fill)

    text_center("DÜĞÜNÜMÜZE DAVETLİSİNİZ", 86, cg, 18, fill=gold, tracking=2.4)
    text_center("Derya", 144, gv, 121, maxwidth=520)
    text_center("ve", 260, gv, 56, fill=gold)
    text_center("İbrahim", 324, gv, 126, maxwidth=540)
    draw.line((502*S, 462*S, 568*S, 462*S), fill=gold, width=S)
    draw.line((632*S, 462*S, 698*S, 462*S), fill=gold, width=S)
    draw.polygon([(600*S,454*S),(606*S,462*S),(600*S,470*S),(594*S,462*S)],outline=gold)
    text_center("29 KASIM 2026", 485, cg, 34, fill=text_color, tracking=3)
    text_center("PAZAR · 18:00–22:00", 530, cg, 23, fill=gold, tracking=.5)
    text_center("NİKÂH 19:00", 563, cg, 20, fill=text_color, tracking=.5)

    canvas.resize((1200,630), Image.Resampling.LANCZOS).save(DEST, "JPEG", quality=90, subsampling=0, optimize=True)
    gv.unlink(missing_ok=True)
    cg.unlink(missing_ok=True)
    print(f"Created {DEST}, {DEST.stat().st_size} bytes")

if __name__ == "__main__":
    main()
