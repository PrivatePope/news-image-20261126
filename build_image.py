#!/usr/bin/env python3
"""Draw the 26 November 2026 front page: 'The World in One Day'.

Fresh script written in this session. Uses PIL + DejaVu fonts only.
Output: entry.png, 1024x1024.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

PAPER = (247, 243, 232)
INK = (24, 24, 24)
RED = (178, 34, 34)
DARK = (30, 30, 34)
GREY = (90, 86, 78)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def text_block(x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.32)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

def center(y, text, fnt, fill=INK, x0=0, x1=W):
    tw = fnt.getlength(text)
    d.text(((x0 + x1 - tw) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size

MX = 36            # margin
CW = W - 2 * MX    # content width

# ---- top rules + masthead ----
d.line([(MX, 18), (W - MX, 18)], fill=INK, width=4)
d.line([(MX, 24), (W - MX, 24)], fill=INK, width=1)
center(34, "THE WORLD IN ONE DAY", SERIF_B(58), INK)
d.line([(MX, 104), (W - MX, 104)], fill=INK, width=1)

# ---- dateline band ----
d.rectangle([MX, 112, W - MX, 148], fill=DARK)
center(119, "THURSDAY 26 NOVEMBER 2026", SANS_B(22), (255, 255, 255))

# ---- lead kicker + headline ----
center(160, "OIL SHOCK IN THE GULF", SANS_B(20), RED)
hl = wrap("Houthis claim strike on Saudi Arabia's biggest refinery", SERIF_B(38), CW)
y = 186
for ln in hl:
    tw = SERIF_B(38).getlength(ln)
    d.text(((W - tw) / 2, y), ln, font=SERIF_B(38), fill=INK)
    y += 46

# ---- lead illustration: refinery at dusk ----
ix0, iy0, ix1, iy1 = MX, 288, W - MX, 528
# sky gradient (dusk orange to pale)
for i in range(iy1 - iy0):
    t = i / max(1, (iy1 - iy0 - 1))
    r = int(255 - 40 * t)
    g = int(196 - 60 * t)
    b = int(120 + 40 * t)
    d.line([(ix0, iy0 + i), (ix1, iy0 + i)], fill=(r, g, b))
# sun
d.ellipse([ix1 - 150, iy0 + 26, ix1 - 78, iy0 + 98], fill=(255, 214, 90))
# sea
d.rectangle([ix0, iy1 - 46, ix1, iy1], fill=(38, 84, 124))
for sx in range(ix0 + 14, ix1 - 10, 46):
    d.line([(sx, iy1 - 30), (sx + 22, iy1 - 30)], fill=(120, 170, 205), width=3)
# refinery silhouette: towers, tanks, chimneys
base = iy1 - 46
d.rectangle([ix0 + 30, base - 118, ix0 + 120, base], fill=(52, 52, 58))
d.rectangle([ix0 + 140, base - 88, ix0 + 250, base], fill=(64, 64, 70))
d.ellipse([ix0 + 150, base - 108, ix0 + 240, base - 88], fill=(64, 64, 70))
for cx in (ix0 + 300, ix0 + 340, ix0 + 380):
    d.rectangle([cx, base - 150, cx + 18, base], fill=(44, 44, 50))
d.rectangle([ix0 + 440, base - 96, ix0 + 560, base], fill=(52, 52, 58))
d.polygon([(ix0 + 440, base - 96), (ix0 + 500, base - 138), (ix0 + 560, base - 96)], fill=(52, 52, 58))
for cx in (ix0 + 620, ix0 + 660):
    d.rectangle([cx, base - 132, cx + 16, base], fill=(44, 44, 50))
# windows (lit)
for wx in range(ix0 + 44, ix0 + 112, 22):
    d.rectangle([wx, base - 96, wx + 10, base - 80], fill=(255, 214, 90))
# flames on the tallest chimney
fx, fy = ix0 + 309, base - 150
d.polygon([(fx - 16, fy), (fx, fy - 42), (fx + 16, fy)], fill=(255, 120, 20))
d.polygon([(fx - 9, fy), (fx, fy - 26), (fx + 9, fy)], fill=(255, 210, 60))
# smoke puffs
for sx, sy, sr in ((ix0 + 348, base - 168, 16), (ix0 + 366, base - 158, 20),
                   (ix0 + 392, base - 168, 22), (ix0 + 668, base - 150, 14),
                   (ix0 + 684, base - 166, 18)):
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 116, 110))
# frame + price ticker
d.rectangle([ix0, iy0, ix1, iy1], outline=INK, width=2)
d.rectangle([ix0, iy1 - 46, ix1, iy1], fill=(20, 20, 24))
center(iy1 - 40, "BRENT $94.61  ▲ 3.5%      WTI $83.68  ▲ 2%", SANS_B(21), (255, 214, 90))

# ---- lead body ----
y = 544
y = text_block(MX, y, wrap(
    "Yemen's Houthis said on Wednesday they attacked the Ras Tanura refinery and "
    "Riyadh's financial district. Saudi Arabia said its air defences shot down four "
    "drones over the site, with no injuries reported.", SANS(17), CW), SANS(17))
d.line([(MX, y + 6), (W - MX, y + 6)], fill=INK, width=1)

# ---- two columns ----
col_y = y + 20
col_w = (CW - 28) // 2
lx, rx = MX, MX + col_w + 28

# left: Cairo
d.text((lx, col_y), "CAIRO", font=SANS_B(15), fill=RED)
y1 = text_block(lx, col_y + 24, wrap(
    "31 killed as fuel tanker explodes on ring road", SERIF_B(25), col_w), SERIF_B(25))
y1 = text_block(lx, y1 + 6, wrap(
    "A tanker carrying petroleum products crashed and burst into flames on Cairo's "
    "Ring Road in the Waraq district on Wednesday, engulfing more than two dozen "
    "cars. Egypt's health ministry put the toll at 31 dead and 21 injured.",
    SANS(15), col_w), SANS(15))
# small flame drawing
fy0 = y1 + 12
d.rectangle([lx, fy0, lx + col_w, fy0 + 64], fill=(40, 38, 36))
for k, (fx2, fh) in enumerate(((lx + 60, 46), (lx + 150, 58), (lx + 240, 40), (lx + 330, 50))):
    d.polygon([(fx2 - 18, fy0 + 64), (fx2, fy0 + 64 - fh), (fx2 + 18, fy0 + 64)],
              fill=(255, 120, 20) if k % 2 == 0 else (255, 190, 40))
d.text((lx + 8, fy0 + 68), "Ring Road, Giza — Wednesday", font=SANS(12), fill=GREY)

# right: tariffs
d.text((rx, col_y), "TRADE", font=SANS_B(15), fill=RED)
y2 = text_block(rx, col_y + 24, wrap(
    "US proposes new tariffs on 14 economies", SERIF_B(25), col_w), SERIF_B(25))
y2 = text_block(rx, y2 + 6, wrap(
    "Washington proposed Section 301 tariffs on Wednesday — up to 20% on Chinese "
    "goods and 15% on the EU, Japan, South Korea, Taiwan and Switzerland — over "
    "manufacturing overcapacity. Nothing takes effect yet.",
    SANS(15), col_w), SANS(15))
# small globe / ship drawing
gy0 = y2 + 12
d.rectangle([rx, gy0, rx + col_w, gy0 + 64], fill=(32, 64, 96))
d.ellipse([rx + 30, gy0 + 6, rx + 94, gy0 + 58], fill=(70, 130, 180))
d.arc([rx + 30, gy0 + 6, rx + 94, gy0 + 58], 0, 360, fill=(255, 255, 255), width=2)
d.line([(rx + 30, gy0 + 32), (rx + 94, gy0 + 32)], fill=(255, 255, 255), width=2)
d.line([(rx + 62, gy0 + 6), (rx + 62, gy0 + 58)], fill=(255, 255, 255), width=2)
d.text((rx + 116, gy0 + 12), "14 economies", font=SANS_B(17), fill=(255, 255, 255))
d.text((rx + 116, gy0 + 36), "China • EU • Japan", font=SANS(14), fill=(220, 230, 240))
d.text((rx + 8, gy0 + 68), "USTR announcement — Wednesday", font=SANS(12), fill=GREY)

# ---- lighter strip ----
sy0 = 892
d.rectangle([MX, sy0, W - MX, 972], fill=(232, 240, 220), outline=(90, 130, 70), width=2)
d.text((MX + 14, sy0 + 10), "THE LIGHTER SIDE", font=SANS_B(15), fill=(60, 110, 50))
# mosquito drawing: body, wings, legs
mx, my = MX + 70, sy0 + 62
d.ellipse([mx - 26, my - 8, mx + 26, my + 8], fill=(70, 70, 70))          # body
d.ellipse([mx + 22, my - 5, mx + 34, my + 5], fill=(50, 50, 50))          # head
d.ellipse([mx - 34, my - 22, mx + 2, my - 2], fill=(200, 220, 235))       # wing
d.ellipse([mx - 30, my + 2, mx + 6, my + 22], fill=(215, 230, 240))       # wing
for lx2, ly2 in ((mx - 14, my + 18), (mx + 2, my + 20), (mx + 16, my + 16)):
    d.line([(lx2, my + 6), (lx2 - 8, ly2 + 14)], fill=(70, 70, 70), width=2)
text_block(MX + 140, sy0 + 30, wrap(
    "Brazil's bug army beats dengue: mosquitoes carrying the Wolbachia bacterium "
    "cut infections by 68.5% in children in a four-year trial in Belo Horizonte.",
    SANS_B(17), CW - 154), SANS_B(17))

# ---- footer ----
d.line([(MX, 986), (W - MX, 986)], fill=INK, width=1)
center(992, "Sources: Reuters, AP, CNN, USTR, Emory University  •  Events reported 25–26 Nov 2026",
       SANS(12), GREY)

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")
