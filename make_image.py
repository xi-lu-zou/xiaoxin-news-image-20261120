#!/usr/bin/env python3
"""Generate entry.png: the world news of Friday 20 November 2026 in one image.
Stories per the day's wire reporting (Reuters, AP, AFP, Al Jazeera, CNN).
Deterministic, no network, no assets — everything is drawn with PIL.
Canvas 1024x1024, editorial front-page collage style.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
PAPER = (247, 243, 234)
INK = (18, 18, 20)
RED = (178, 34, 40)
BLUE = (24, 62, 120)
TEAL = (10, 110, 110)
GOLD = (196, 144, 32)
GREY = (90, 90, 95)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def wrap(s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def panel(x, y, w, h, accent):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=WHITE, outline=(205, 198, 182), width=2)
    d.rounded_rectangle([x, y, x + w, y + 30], radius=10, fill=accent)
    d.rectangle([x, y + 20, x + w, y + 30], fill=accent)

def headline(x, y, s, size, maxw, fill=INK):
    f = F(SANS_B, size)
    lh = int(size * 1.18)
    lines = wrap(s, f, maxw)
    for i, ln in enumerate(lines):
        text(x, y + i * lh, ln, f, fill)
    return y + len(lines) * lh

def caption(x, y, s, maxw, size=17):
    f = F(SANS, size)
    lines = wrap(s, f, maxw)
    for i, ln in enumerate(lines):
        text(x, y + i * int(size * 1.3), ln, f, (52, 52, 58))
    return y + len(lines) * int(size * 1.3)

def tag(x, y, s):
    text(x + 12, y + 5, s, F(SANS_B, 16), WHITE)

# ---------------- masthead ----------------
text(W // 2, 16, "T H E   W O R L D   I N   O N E   D A Y", F(SERIF_B, 25), INK, "ma")
d.line([36, 58, W - 36, 58], fill=INK, width=3)
text(W // 2, 66, "FRIDAY 20 NOVEMBER 2026", F(SERIF_B, 47), RED, "ma")
d.line([36, 128, W - 36, 128], fill=INK, width=3)
text(W // 2, 134, "Kyiv's bridges burn, Russian missiles land in Poland — and the rout turns into a correction", F(SANS, 18), GREY, "ma")

# ---------------- lead panel: Kyiv strike ----------------
LX, LY, LW, LH = 36, 168, W - 72, 218
panel(LX, LY, LW, LH, RED)
tag(LX, LY, "LEAD STORY  •  KYIV UNDER FIRE")
# bridge over the Dnipro with missile trails and bursts
base = LY + LH - 16
deck = LY + 150
d.rectangle([LX + 20, deck + 26, LX + 330, base], fill=(170, 190, 205))
d.line([LX + 24, deck, LX + 326, deck], fill=INK, width=6)
for px in (70, 160, 260):
    d.line([LX + px, deck, LX + px, deck + 26], fill=INK, width=5)
d.arc([LX + 24, deck + 4, LX + 180, deck + 40], start=0, end=180, fill=(90, 140, 190), width=4)
d.arc([LX + 170, deck + 4, LX + 326, deck + 40], start=0, end=180, fill=(90, 140, 190), width=4)
# missile trails
for sx, ex in [(60, 130), (130, 185), (215, 250)]:
    d.line([LX + sx, LY + 52, LX + ex, deck - 16], fill=(150, 150, 155), width=3)
    d.polygon([(LX + ex - 7, deck - 4), (LX + ex, deck - 22), (LX + ex + 7, deck - 4)], fill=(90, 90, 96))
for bx, by, br in [(185, deck - 8, 15), (250, deck - 12, 11)]:
    d.ellipse([LX + bx - br, LY + 0 + by - br - 40, LX + bx + br, LY + by + br - 40], fill=(255, 120, 40))
    d.ellipse([LX + bx - br // 2, LY + by - br // 2 - 40, LX + bx + br // 2, LY + by + br // 2 - 40], fill=(255, 190, 60))
headline(LX + 356, LY + 44, "RUSSIA'S BIGGEST STRIKE OF THE YEAR BATTERS KYIV", 27, 580)
caption(LX + 356, LY + 118, "27 ballistic missiles, 84 cruise missiles, 404 drones: three Dnipro bridges hit, power and water out — at least 8 dead, 28 wounded", 580, 16)

# ---------------- row 2: Poland + Shenzhen fallout ----------------
RY, RH = 402, 196
PW = (W - 72 - 16) // 2
# Poland
panel(36, RY, PW, RH, BLUE); tag(36, RY, "NATO  •  POLAND")
# map dot + impact star
mx, my = 84, RY + 138
d.ellipse([mx - 26, my - 26, mx + 26, my + 26], outline=(90, 140, 90), width=3)
for a in range(0, 360, 45):
    import math
    rad = math.radians(a)
    d.line([mx, my, mx + int(17 * math.cos(rad)), my + int(17 * math.sin(rad))], fill=RED, width=4)
d.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=RED)
text(mx + 36, my - 10, "SE POLAND", F(SANS_B, 13), GREY)
headline(160, RY + 40, "RUSSIAN MISSILES LAND IN POLAND", 20, PW - 176)
caption(160, RY + 92, "Tusk: 'a deliberate provocation' — NATO voices solidarity; no casualties", PW - 176, 15)
# Shenzhen fallout
SX = 36 + PW + 16
panel(SX, RY, PW, RH, (84, 60, 140)); tag(SX, RY, "DIPLOMACY  •  SHENZHEN FALLOUT")
text(SX + 16, RY + 44, "“No Yalta.”", F(SERIF_B, 34), BLUE)
headline(SX + 16, RY + 92, "EUROPE REJECTS A CARVE-UP DECIDED OVER ITS HEAD", 19, PW - 32)
caption(SX + 16, RY + 148, "Merz dismisses the summit as a photo-op; Trump insists Putin 'wants to make a deal'", PW - 32, 15)

# ---------------- row 3: Markets + COP31 ----------------
R3Y, R3H = 614, 176
panel(36, R3Y, PW, R3H, TEAL); tag(36, R3Y, "MARKETS  •  THE AI MELTDOWN")
text(52, R3Y + 44, "−3.7%", F(SERIF_B, 46), RED)
text(52, R3Y + 102, "S&P 500", F(SANS_B, 20), INK)
headline(226, R3Y + 44, "WALL ST CONFIRMS A CORRECTION", 18, PW - 242)
caption(226, R3Y + 98, "Seventh straight loss; Dow −950, Nasdaq −5.3%, Nvidia −14%, Anthropic −9%", PW - 242, 15)
# COP31
CX = 36 + PW + 16
panel(CX, R3Y, PW, R3H, (10, 110, 110)); tag(CX, R3Y, "CLIMATE  •  COP31, ANTALYA")
# hourglass
hx, hy = CX + 58, R3Y + 66
d.polygon([(hx - 20, hy), (hx + 20, hy), (hx, hy + 22)], outline=INK, width=3)
d.polygon([(hx - 20, hy + 48), (hx + 20, hy + 48), (hx, hy + 26)], outline=INK, width=3)
d.line([hx - 26, hy - 6, hx + 26, hy - 6], fill=INK, width=4)
d.line([hx - 26, hy + 54, hx + 26, hy + 54], fill=INK, width=4)
d.polygon([(hx - 7, hy + 40), (hx + 7, hy + 40), (hx, hy + 28)], fill=GOLD)
headline(CX + 104, R3Y + 44, "COP31 BLOWS PAST ITS DEADLINE", 18, PW - 120)
caption(CX + 104, R3Y + 98, "Closing plenary suspended to Saturday as the fossil-fuel wording fight deadlocks", PW - 120, 15)

# ---------------- row 4: UK–EU reset + chips ----------------
R4Y, R4H = 806, 128
panel(36, R4Y, PW, R4H, (30, 90, 160)); tag(36, R4Y, "BRUSSELS  •  BREXIT RESET")
def mini_flag(x0, y0, fw, fh, kind):
    if kind == "UK":
        d.rectangle([x0, y0, x0 + fw, y0 + fh], fill=(30, 60, 140))
        d.line([x0, y0, x0 + fw, y0 + fh], fill=WHITE, width=5)
        d.line([x0 + fw, y0, x0, y0 + fh], fill=WHITE, width=5)
        d.rectangle([x0 + fw // 2 - 5, y0, x0 + fw // 2 + 5, y0 + fh], fill=WHITE)
        d.rectangle([x0, y0 + fh // 2 - 5, x0 + fw, y0 + fh // 2 + 5], fill=WHITE)
        d.rectangle([x0 + fw // 2 - 3, y0, x0 + fw // 2 + 3, y0 + fh], fill=(200, 30, 50))
        d.rectangle([x0, y0 + fh // 2 - 3, x0 + fw, y0 + fh // 2 + 3], fill=(200, 30, 50))
    else:
        d.rectangle([x0, y0, x0 + fw, y0 + fh], fill=(0, 51, 153))
        import math
        for k in range(8):
            rad = math.radians(k * 45)
            sx = x0 + fw // 2 + int(fw * 0.32 * math.cos(rad))
            sy = y0 + fh // 2 + int(fh * 0.32 * math.sin(rad))
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
mini_flag(52, R4Y + 52, 56, 38, "UK")
mini_flag(120, R4Y + 52, 56, 38, "EU")
headline(196, R4Y + 40, "FOOD CHECKS SCRAPPED IN UK–EU 'RESET'", 16, PW - 212)
caption(196, R4Y + 82, "Youth mobility for 100,000 a side; a claimed £17bn boost", PW - 212, 15)
# chips
TX = 36 + PW + 16
panel(TX, R4Y, PW, R4H, (60, 60, 66)); tag(TX, R4Y, "TECH  •  CHIP WAR")
qx, qy = TX + 34, R4Y + 52
d.rectangle([qx, qy, qx + 52, qy + 52], fill=(40, 40, 46), outline=(150, 150, 160), width=2)
d.rectangle([qx + 14, qy + 14, qx + 38, qy + 38], outline=GOLD, width=2)
for k in range(4):
    d.line([qx + 8 + k * 12, qy - 8, qx + 8 + k * 12, qy], fill=(150, 150, 160), width=3)
    d.line([qx + 8 + k * 12, qy + 52, qx + 8 + k * 12, qy + 60], fill=(150, 150, 160), width=3)
    d.line([qx - 8, qy + 8 + k * 12, qx, qy + 8 + k * 12], fill=(150, 150, 160), width=3)
    d.line([qx + 52, qy + 8 + k * 12, qx + 60, qy + 8 + k * 12], fill=(150, 150, 160), width=3)
headline(TX + 116, R4Y + 40, "TSMC HALTS CHINA CHIP SHIPMENTS", 16, PW - 132)
caption(TX + 116, R4Y + 66, "A new US export rule closes the foundry loophole; Samsung caught too", PW - 132, 15)

# ---------------- ticker ----------------
TY = 950
d.rectangle([0, TY, W, H], fill=INK)
ticker = "HOUTHIS FIRE ON SAUDI ARABIA AGAIN  •  US SANCTIONS IRAN'S 'OIL TRUSTEES'  •  HORMUZ TRAFFIC 65% BELOW PRE-WAR  •  BUKELE SEEKS A THIRD TERM"
f = F(SANS_B, 17)
while d.textlength(ticker, font=f) > W - 40 and f.size > 11:
    f = F(SANS_B, f.size - 1)
text(W // 2, TY + 16, ticker, f, WHITE, "ma")
text(W // 2, TY + 44, "One day, one picture — Friday 20 November 2026", F(SANS, 14), (200, 200, 205), "ma")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out)
print(out, os.path.getsize(out), "bytes")
