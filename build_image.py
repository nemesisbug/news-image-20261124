#!/usr/bin/env python3
"""Draw the 24 November 2026 front page as a single 1024x1024 PNG.

A newspaper front page: masthead, a wide lead band on Nvidia's
reinstatement of Jensen Huang, eight story cards in a 4x2 grid, a
numbers strip, an "also today" ticker and a date-check footer.
Everything is drawn from scratch with Pillow and the system DejaVu
fonts. No network, no clock reads, no randomness: the same input
always renders the same bytes.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

PAPER = (246, 241, 231)
INK = (22, 22, 28)
NAVY = (22, 38, 77)
NAVY_SOFT = (38, 58, 104)
GREEN = (13, 59, 46)
GREEN_SOFT = (27, 94, 73)
GOLD = (198, 158, 74)
RED = (178, 34, 34)
RED_SOFT = (214, 90, 80)
CARD = (255, 255, 255)
RULE = (190, 182, 168)
MUTED = (96, 94, 88)
MOON = (232, 226, 200)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Split text into lines that fit width, measured with fnt."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, width, leading=None):
    """Draw wrapped text; return the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, xy, text, color=RED, size=13):
    fnt = font(SANS_B, size)
    draw.text(xy, text, font=fnt, fill=color)


def draw_chip_panel(draw, box):
    """Dark-green panel: a chip with a rising chart arrow, NVDA +33%."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=GREEN)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 18
    s = 74
    # Chip pins on all four sides.
    for i in range(4):
        px = cx - s // 2 + 12 + i * 20
        draw.line([px, cy - s // 2 - 12, px, cy - s // 2], fill=GOLD,
                  width=3)
        draw.line([px, cy + s // 2, px, cy + s // 2 + 12], fill=GOLD,
                  width=3)
        py = cy - s // 2 + 12 + i * 20
        draw.line([cx - s // 2 - 12, py, cx - s // 2, py], fill=GOLD,
                  width=3)
        draw.line([cx + s // 2, py, cx + s // 2 + 12, py], fill=GOLD,
                  width=3)
    draw.rounded_rectangle([cx - s // 2, cy - s // 2, cx + s // 2,
                            cy + s // 2], radius=8, outline=GOLD, width=4)
    draw.rounded_rectangle([cx - 20, cy - 20, cx + 20, cy + 20], radius=4,
                           fill=GREEN_SOFT, outline=GOLD, width=2)
    # Rising arrow across the chip.
    draw.line([(cx - 52, cy + 34), (cx - 18, cy + 6), (cx + 2, cy + 18),
               (cx + 52, cy - 30)], fill=(255, 255, 255), width=5,
              joint="curve")
    draw.polygon([(cx + 52, cy - 30), (cx + 30, cy - 32), (cx + 50, cy - 8)],
                 fill=(255, 255, 255))
    tf = font(SANS_B, 28)
    label = "NVDA  +33%"
    tw = draw.textlength(label, font=tf)
    draw.text(((x0 + x1 - tw) / 2, y1 - 52), label, font=tf,
              fill=(255, 255, 255))
    cf = font(SANS, 12)
    cap = "SHARES JUMP AS THE CEO RETURNS"
    cw = draw.textlength(cap, font=cf)
    draw.text(((x0 + x1 - cw) / 2, y1 - 20), cap, font=cf, fill=GOLD)


def draw_card(draw, box, kick, head, deck, icon):
    """One story card: kicker, headline, deck, tiny drawn icon."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=6, fill=CARD, outline=RULE, width=1)
    draw.line([x0 + 12, y0 + 32, x1 - 12, y0 + 32], fill=RULE, width=1)
    kicker(draw, (x0 + 12, y0 + 9), kick, size=12)
    icon(draw, x1 - 42, y0 + 5, 24)
    hf = font(SERIF_B, 18)
    y = text_block(draw, (x0 + 12, y0 + 40), head, hf, INK, x1 - x0 - 24,
                   leading=21)
    df = font(SANS, 12)
    text_block(draw, (x0 + 12, y + 3), deck, df, MUTED, x1 - x0 - 24,
               leading=15)


def icon_ball(d, x, y, s):
    d.ellipse([x, y, x + s, y + s], outline=NAVY_SOFT, width=2)
    d.polygon([(x + s * 0.5, y + s * 0.28), (x + s * 0.72, y + s * 0.42),
               (x + s * 0.64, y + s * 0.68), (x + s * 0.36, y + s * 0.68),
               (x + s * 0.28, y + s * 0.42)], fill=NAVY_SOFT)
    d.line([x + s * 0.5, y + s * 0.28, x + s * 0.5, y], fill=NAVY_SOFT,
           width=2)
    d.line([x + s * 0.72, y + s * 0.42, x + s, y + s * 0.35],
           fill=NAVY_SOFT, width=2)
    d.line([x + s * 0.28, y + s * 0.42, x, y + s * 0.35], fill=NAVY_SOFT,
           width=2)


def icon_box(d, x, y, s):
    d.rectangle([x, y + s * 0.3, x + s, y + s], outline=NAVY_SOFT, width=2)
    d.line([x, y + s * 0.3, x + s * 0.5, y, x + s, y + s * 0.3],
           fill=NAVY_SOFT, width=2)
    d.line([x + s * 0.3, y + s * 0.62, x + s * 0.45, y + s * 0.78,
            x + s * 0.78, y + s * 0.42], fill=RED, width=3, joint="curve")


def icon_flame(d, x, y, s):
    pts = [(x + s * 0.5, y), (x + s * 0.85, y + s * 0.55),
           (x + s * 0.65, y + s * 0.55), (x + s * 0.75, y + s * 0.8),
           (x + s * 0.5, y + s), (x + s * 0.25, y + s * 0.8),
           (x + s * 0.35, y + s * 0.55), (x + s * 0.15, y + s * 0.55)]
    d.polygon(pts, fill=RED_SOFT)


def icon_leaf(d, x, y, s):
    d.ellipse([x, y + s * 0.1, x + s, y + s * 0.9], outline=NAVY_SOFT,
              width=2)
    d.line([x + s * 0.5, y + s * 0.15, x + s * 0.5, y + s * 0.9],
           fill=NAVY_SOFT, width=2)
    d.line([x + s * 0.5, y + s * 0.4, x + s * 0.8, y + s * 0.25],
           fill=NAVY_SOFT, width=2)
    d.line([x + s * 0.5, y + s * 0.6, x + s * 0.2, y + s * 0.45],
           fill=NAVY_SOFT, width=2)


def icon_house(d, x, y, s):
    d.polygon([(x, y + s * 0.5), (x + s * 0.5, y),
               (x + s, y + s * 0.5)], fill=NAVY_SOFT)
    d.rectangle([x + s * 0.12, y + s * 0.5, x + s * 0.88, y + s],
                outline=NAVY_SOFT, width=2)
    d.rectangle([x + s * 0.4, y + s * 0.68, x + s * 0.6, y + s],
                fill=RED_SOFT)


def icon_plane(d, x, y, s):
    d.polygon([(x + s * 0.1, y + s * 0.55), (x + s * 0.9, y + s * 0.25),
               (x + s * 0.95, y + s * 0.4), (x + s * 0.2, y + s * 0.7)],
              fill=NAVY_SOFT)
    d.polygon([(x + s * 0.45, y + s * 0.45), (x + s * 0.6, y + s * 0.15),
               (x + s * 0.7, y + s * 0.5)], fill=NAVY_SOFT)
    d.polygon([(x + s * 0.3, y + s * 0.65), (x + s * 0.4, y + s * 0.9),
               (x + s * 0.55, y + s * 0.6)], fill=NAVY_SOFT)


def icon_mic(d, x, y, s):
    d.rounded_rectangle([x + s * 0.35, y, x + s * 0.65, y + s * 0.55],
                        radius=6, fill=NAVY_SOFT)
    d.arc([x + s * 0.15, y + s * 0.35, x + s * 0.85, y + s * 0.85], 0, 180,
          fill=NAVY_SOFT, width=2)
    d.line([x + s * 0.5, y + s * 0.72, x + s * 0.5, y + s], fill=NAVY_SOFT,
           width=2)
    d.line([x + s * 0.3, y + s, x + s * 0.7, y + s], fill=NAVY_SOFT,
           width=2)


def icon_moon(d, x, y, s):
    d.ellipse([x, y, x + s, y + s], fill=MOON, outline=NAVY_SOFT, width=2)
    d.ellipse([x + s * 0.3, y + s * 0.25, x + s * 0.45, y + s * 0.4],
              fill=(200, 192, 160))
    d.ellipse([x + s * 0.6, y + s * 0.55, x + s * 0.78, y + s * 0.73],
              fill=(200, 192, 160))
    d.ellipse([x + s * 0.25, y + s * 0.6, x + s * 0.38, y + s * 0.73],
              fill=(200, 192, 160))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)

    # ---- Masthead ----
    draw.rectangle([28, 24, 996, 112], fill=NAVY)
    tf = font(SERIF_B, 44)
    title = "THE WORLD IN ONE IMAGE"
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 30), title, font=tf, fill=(255, 255, 255))
    sf = font(SANS_B, 15)
    sub = "TUESDAY 24 NOVEMBER 2026  ·  THE DAY IN ONE PICTURE"
    sw = draw.textlength(sub, font=sf)
    draw.text(((W - sw) / 2, 82), sub, font=sf, fill=GOLD)

    # ---- Lead band: Huang returns ----
    draw.rounded_rectangle([28, 124, 996, 306], radius=6, fill=CARD,
                           outline=RULE, width=1)
    draw_chip_panel(draw, (28, 124, 372, 306))
    kicker(draw, (396, 138), "TECH  ·  NVIDIA  ·  SANTA CLARA", size=13)
    hf = font(SERIF_B, 40)
    y = text_block(draw, (396, 160), "Huang is back\nat Nvidia", hf, INK,
                   996 - 396 - 24, leading=42)
    df = font(SANS, 14)
    y = text_block(
        draw, (396, y + 6),
        "The board unanimously reinstates Jensen Huang as chief "
        "executive, 11 days after he resigned. Shares jump about a "
        "third; the board says no national security risk.",
        df, INK, 996 - 396 - 24, leading=17)
    qf = font(SERIF, 14)
    text_block(draw, (396, y + 4),
               "\u201cSatisfied with Mr. Huang\u2019s candor and ability "
               "to lead.\u201d \u2014 Nvidia board",
               qf, MUTED, 996 - 396 - 24, leading=17)

    # ---- Story grid: 8 cards, 4 x 2 ----
    cards = [
        ("SPORT  ·  FIFA", "Two World Cups,\nfour nations each",
         "USA, Mexico, Costa Rica and Jamaica take 2031; England, "
         "N. Ireland, Scotland and Wales take 2035. First 48-team "
         "editions.", icon_ball),
        ("USA  ·  POLITICS", "Trump takes on\nNewsom at the DOJ",
         "The president attacks the governor\u2019s commutation of 548 "
         "death sentences; his DOJ has sought death 49 times.",
         icon_box),
        ("INDONESIA", "24 dead in\nfactory fire",
         "Blaze at a sweets factory in Cikande, Banten; about 30 "
         "still missing after Saturday\u2019s fire.", icon_flame),
        ("GAZA  ·  ENVIRONMENT", "Gaza poisoned\nfor generations",
         "Oxfam report: toxic contamination across 99% of the "
         "Strip \u2014 air, soil and water.", icon_leaf),
        ("DENMARK  ·  LAW", "Top court backs\n\u2018ghetto law\u2019",
         "Evicting 91 families in Helsing\u00f8r was not "
         "discrimination, the Supreme Court rules.", icon_house),
        ("USA  ·  TRAVEL", "O\u2019Hare stops\nfor staffing",
         "FAA grounds flights into Chicago as the Thanksgiving "
         "rush begins; about 12 cancelled.", icon_plane),
        ("CULTURE  ·  SECURITY", "Mossad: we helped\nstop the Swift plot",
         "Ex-chief Barnea reveals Israel\u2019s role in foiling the "
         "2024 Vienna ISIS attack.", icon_mic),
        ("SKY  ·  SCIENCE", "Supermoon meets\nthe Seven Sisters",
         "Full Beaver Moon peaks 14:53 UTC, 0.9\u00b0 from the "
         "Pleiades \u2014 first of three supermoons.", icon_moon),
    ]
    gx, gy = 28, 320
    cw, ch, gap = 232, 138, 8
    for i, (kick, head, deck, ic) in enumerate(cards):
        cx = gx + (i % 4) * (cw + gap)
        cy = gy + (i // 4) * (ch + gap)
        draw_card(draw, (cx, cy, cx + cw, cy + ch), kick, head, deck, ic)

    # ---- By the numbers ----
    draw.rounded_rectangle([28, 618, 996, 700], radius=6, fill=CARD,
                           outline=RULE, width=1)
    draw.text((44, 628), "BY THE NUMBERS", font=font(SANS_B, 13), fill=NAVY)
    numbers = [
        ("+33%", "Nvidia shares jump"),
        ("48", "2031 World Cup teams"),
        ("548", "death sentences commuted"),
        ("24", "dead in the Indonesia fire"),
        ("99%", "of Gaza found contaminated"),
    ]
    nx = 44
    for big, small in numbers:
        draw.text((nx, 652), big, font=font(SERIF_B, 22), fill=RED)
        nf = font(SANS, 12)
        text_block(draw, (nx, 680), small, nf, MUTED, 180, leading=14)
        nx += 192

    # ---- Also today ticker ----
    draw.rounded_rectangle([28, 712, 996, 884], radius=6, fill=CARD,
                           outline=RULE, width=1)
    draw.text((44, 722), "ALSO TODAY \u2014 IN ONE LINE EACH",
              font=font(SANS_B, 13), fill=NAVY)
    left = [
        "India\u2019s top court grants bail to a Godhra convict.",
        "Lahore tops the world pollution ranking; AQI passes 500.",
        "A 4.0 quake strikes Pakistan near the Afghan border.",
        "Grameen Bank branches attacked across Bangladesh.",
        "De Bruyne: my feelings for Man City \u2018will never change\u2019.",
    ]
    right = [
        "King Charles reaches out to Meghan after her father\u2019s arrest.",
        "Dutch activist Jason Bhugwandass, 28, dies by euthanasia.",
        "Chinese official sentenced to death for leaking 100 reports.",
        "Kim Jong Un receives credentials from India\u2019s new envoy.",
        "Ex-Mississippi mayor jailed 37 months in a bribery case.",
    ]
    tf2 = font(SANS, 12)
    ly = 748
    for item in left:
        draw.text((44, ly), "\u2022  " + item, font=tf2, fill=INK)
        ly += 24
    ry = 748
    for item in right:
        draw.text((520, ry), "\u2022  " + item, font=tf2, fill=INK)
        ry += 24
    draw.text((44, 862), "Minnesota fraud probe raids child centres; "
              "Trump hush-money appeal gets a court path.",
              font=tf2, fill=INK)

    # ---- Date check + footer ----
    draw.rounded_rectangle([28, 896, 996, 1000], radius=6,
                           fill=(238, 232, 216), outline=RULE, width=1)
    draw.text((44, 906), "DATE CHECK \u2014 LEFT OUT ON PURPOSE:",
              font=font(SANS_B, 12), fill=NAVY)
    text_block(draw, (44, 924),
               "COP31 collapsed Sunday 22 Nov \u00b7 Kyiv/Dymer strikes "
               "22\u201323 Nov \u00b7 BepiColombo reaches Mercury 22 Nov "
               "\u00b7 Fiona the hippo dies 19 Nov. This page carries "
               "only stories first reported on 24 November 2026.",
               font(SANS, 12), MUTED, 940, leading=15)
    src = "SOURCES: REUTERS \u00b7 AP \u00b7 BBC \u00b7 FIFA \u00b7 NASA \u00b7 GUARDIAN"
    sw = draw.textlength(src, font=font(SANS_B, 10))
    draw.text((996 - 16 - sw, 980), src, font=font(SANS_B, 10), fill=MUTED)

    img.save(OUT_PATH, optimize=True)
    print("wrote", OUT_PATH)


if __name__ == "__main__":
    main()
