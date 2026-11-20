#!/usr/bin/env python3
"""Compose the entry image for make.fun news-image-20261119:
"The World in One Day" for Thursday 19 November 2026, holding
the same 34 verified stories as the first edition of the page.

This revision rebuilds the page on the structure of the
edition's winning pages, as the reader directed: mirror that
structure faithfully, adapted to our own Thursday content and
our own artwork. Nothing here is copied from another entry -
the stories are the 34 verified for this page (SOURCES.md),
the illustrations are the pool drawn for our two editions,
re-cropped to the card shapes on per-picture focal windows,
and the words are set here in PIL.

Page plan, on a 1024x1024 sheet, top to bottom:
  masthead   a navy band: a red-and-white date badge at the
             left (NOV / 19 / THU - 2026), the paper's name in
             small caps, the date itself in huge white serif,
             an italic standfirst, and the page's counts at
             the top right (34 STORIES - 7 REGIONS - 11
             DRAWN - ONE PAGE)
  rainbow    one band of seven coloured segments, one per
             region, each carrying its story count
  timeline   THE DAY IN UTC: a label box and four moment
             boxes with the day's grounded times
  lead row   three cards with their artwork on top at about
             2:1 - the Shenzhen summit under the APEC
             presidents cover (the reader's non-negotiable
             hero, large at last), GTA VI's launch, and
             Anthropic's record IPO debut
  card rows  two rows of four cards, artwork on top at 2:1,
             numbered, headline and short brief: the World
             Court judgment, the Crimean Bridge strike,
             Europe in Berlin, the Van Gogh record, flooded
             Florida, COP31's final hours, Kuwait's repelled
             attack and Gaza's Yellow Line - eleven drawn
             stories in all
  bottom     WHERE IT HAPPENED at the left: the dot-matrix
             world map, the eleven drawn stories pinned by
             number, dots for the briefs, and the region
             legend; at the right, ALSO ON THURSDAY 19
             NOVEMBER - the remaining 23 stories as numbered
             one-liners in three columns, each with a bold
             lead word, wire-style and terse so the type can
             stay large
  footer     the red DATE CHECK strip and the sources line

The page is built to be read at thumbnail, half and full
size, which is how the judge compares entries: headlines
are big, briefs and one-liners keep their type floors, and
no picture is a sliced banner - every card shows its scene
whole on its focal window.

Stories are numbered in reading order, 1 to 34. All wording
is set here in PIL from the story data below; the
illustrations are text-free artwork, so no lettering can
come out garbled. SOURCES.md is the verification record
behind every line.

Output is entry.png beside this file. If the PNG ever
exceeded the 1,048,576-byte gate the script falls back to
JPEG bytes (the grader reads the format from the magic
bytes), but the flat artwork and cream page keep PNG well
under it.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT_PATH = os.path.join(HERE, "entry.png")

PAGE = 1024
MARGIN = 24
CONTENT_W = PAGE - 2 * MARGIN  # 976

# ------------------------------------------------------------ knobs
# The geometry of the mirrored structure: a full-bleed navy
# masthead and rainbow band, then the body in three card rows
# at about 2:1 art, a map-and-briefs bottom zone and the
# footer strip.
MASTHEAD_H = 96
RAINBOW_H = 17
TIMELINE_H = 38
LEAD_ART_H = 150
CARD_ART_H = 112
MAP_W, MAP_H = 300, 94

PAPER = (247, 242, 231)
INK = (27, 26, 23)
FADED = (92, 87, 76)
HAIRLINE = (176, 168, 150)
MAPDOT = (158, 149, 128)
WHITE = (252, 250, 244)
NAVY_TXT = (206, 200, 182)

RED = (176, 32, 40)
NAVY = (22, 50, 74)
PLUM = (91, 74, 138)
TEAL = (15, 118, 110)
GOLD = (168, 127, 20)
GREEN = (63, 98, 18)
GRAY = (70, 65, 56)

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

# ------------------------------------------------------------- the day

STANDFAST = ("Everything on this page happened, or was first "
             "reported, on Thursday 19 November 2026.")

COUNTS_LINE = "34 STORIES · 7 REGIONS · 11 DRAWN · ONE PAGE"

# The rainbow band, in reading order, with the story counts
# recounted from the final numbering: Asia holds the summit
# and nine briefs; Europe its three cards; the Americas two
# lead cards, two cards and four briefs; the Middle East
# three cards and four briefs; Africa, Oceania and Global
# their briefs.
REGION_BAND = [
    ("ASIA", 10, RED),
    ("EUROPE", 3, NAVY),
    ("AMERICAS", 8, PLUM),
    ("MIDDLE EAST", 7, TEAL),
    ("AFRICA", 1, GOLD),
    ("OCEANIA", 1, GREEN),
    ("GLOBAL", 4, GRAY),
]

# The day in UTC. Times and labels are from SOURCES.md: the
# Xi-Trump meeting at 12:45 Shenzhen time (04:45 UTC), the
# three-way at 15:30 Shenzhen (07:30 UTC), 2.3m Twitch viewers
# by 12:15 Paris time (11:15 UTC), and Nasdaq's 14:30 UTC open
# for Anthropic's first trades as ANT.
TIMELINE = [
    ("04:45", "Trump meets Xi in Shenzhen"),
    ("07:30", "Three-way summit opens"),
    ("11:15", "2.3m watch GTA VI streams"),
    ("14:30", "Anthropic trades as ANT"),
]

# Focal centres for the story artwork, as a fraction of each
# panorama's width. The illustrations were drawn as wide
# panoramas (mostly 2640x864, ratio about 3.06:1). A card
# shows a 2:1 window centred on the picture's subject - the
# crowd and the mosque in Dhaka, the towers at Yongbyon, the
# painting at the Van Gogh sale - so the picture reads
# complete, never as a slice cut out of a taller scene.
FOCAL = {
    "illo-bangladesh.png": 0.466,
    "illo-northkorea.png": 0.591,
    "illo-icj.png": 0.500,
    "illo-kerch.png": 0.500,
    "illo-europe.png": 0.470,
    "illo-gta.png": 0.447,
    "illo-anthropic.png": 0.492,
    "illo-vangogh.png": 0.644,
    "illo-florida.png": 0.360,
    "illo-cop31.png": 0.568,
    "illo-gulf.png": 0.457,
    "illo-gaza.png": 0.548,
}

# The hero window for the lead card: the APEC cover is a
# square scene (the APEC banner above, the three leaders
# below). The card's 2:1 window takes the scene's full width
# less a small trim, centred on the leaders (source y about
# 840), so the presidents and their flags read whole and
# large - the picture scaled, never stretched.
HERO_CROP = (40, 450, 1560, 1164)

# A card is a dict: n (its number in reading order), img,
# color (its region's), kicker (region - place), tag (its
# sources), head, brief. The lead row runs three of them
# wide; the card rows run four.
LEAD_CARDS = [
    {"n": 1, "img": "hero-apec.png", "color": RED,
     "kicker": "ASIA · THE SUMMIT", "tag": "USA TODAY · CBS NEWS",
     "head": "Trump, Xi and Putin hold first three-way summit",
     "brief": "The leaders of the United States, China and "
              "Russia sat down in Shenzhen for an hour of "
              "talks spanning Ukraine, Iran, nuclear arms, "
              "trade and AI. No breakthrough was announced."},
    {"n": 2, "img": "illo-gta.png", "color": PLUM,
     "kicker": "AMERICAS · GAMES", "tag": "REUTERS · LE MONDE",
     "head": "GTA VI arrives after a 13-year wait",
     "brief": "Midnight launch, New Zealand first; PS5 and "
              "Xbox only. Reviews: 99/100, tying the all-time "
              "record; 15.9m pre-orders."},
    {"n": 3, "img": "illo-anthropic.png", "color": PLUM,
     "kicker": "AMERICAS · MARKETS", "tag": "REUTERS",
     "head": "Anthropic debuts in the biggest IPO ever",
     "brief": "Priced at $83, it raised $81.3bn — the largest "
              "IPO ever — and a near-$1.5tn valuation. First "
              "trades open on Nasdaq as ANT."},
]

ROW_CARDS = [
    {"n": 4, "img": "illo-icj.png", "color": NAVY,
     "kicker": "EUROPE · THE HAGUE", "tag": "HORIZON",
     "head": "World Court reads judgment on Myanmar",
     "brief": "The ICJ delivers judgment in The Gambia's "
              "genocide case over the 2017 crackdown that "
              "drove out 730,000 Rohingya. Myanmar denies it."},
    {"n": 5, "img": "illo-kerch.png", "color": NAVY,
     "kicker": "EUROPE · CRIMEA", "tag": "ONE TURN",
     "head": "Ukraine hits Crimean Bridge a third time",
     "brief": "Traffic is suspended after a third strike in "
              "a week on the bridge between Russia and Crimea."},
    {"n": 6, "img": "illo-europe.png", "color": NAVY,
     "kicker": "EUROPE · BERLIN", "tag": "NEWS MEDIA HOUSE",
     "head": "Europe gathers to arm Ukraine's future",
     "brief": "Leaders gather in Berlin to define Ukraine's "
              "defence future, as the Commission proposes "
              "a €45bn loan for Kyiv."},
    {"n": 7, "img": "illo-vangogh.png", "color": PLUM,
     "kicker": "AMERICAS · NEW YORK", "tag": "REUTERS",
     "head": "Van Gogh sells for a record $190.4m",
     "brief": "Châtaigniers en Fleurs (1890), unseen for "
              "50 years, broke the artist's record."},
    {"n": 8, "img": "illo-florida.png", "color": PLUM,
     "kicker": "AMERICAS · FLORIDA", "tag": "CNN · AP",
     "head": "Flooded Florida braces for more rain",
     "brief": "15.3in of rain near Plantation; 300-plus "
              "calls in one Hollywood night. Schools shut."},
    {"n": 9, "img": "illo-cop31.png", "color": TEAL,
     "kicker": "MIDDLE EAST · ANTALYA", "tag": "HORIZON",
     "head": "COP31 enters its final 48 hours",
     "brief": "Ministers take over the text in Antalya, "
              "but the $120bn adaptation package is still "
              "open as talks near their end."},
    {"n": 10, "img": "illo-gulf.png", "color": TEAL,
     "kicker": "MIDDLE EAST · KUWAIT", "tag": "HORIZON",
     "head": "Kuwait repels first Iranian attack in two months",
     "brief": "Kuwait fought off its first Iranian attack "
              "in two months; the IEA calls Hormuz its "
              "greatest energy threat ever."},
    {"n": 11, "img": "illo-gaza.png", "color": TEAL,
     "kicker": "MIDDLE EAST · GAZA", "tag": "ONE TURN",
     "head": "Israel pushes beyond the Yellow Line",
     "brief": "Israeli forces launch a ground operation "
              "beyond the Yellow Line in central Gaza, the "
              "line the ceasefire drew."},
]

# The ALSO one-liners: (number, bold lead, rest, region
# colour). Wire-style and terse, as the winning pages write
# them, so each fits one line at full one-liner size; every
# fact is the verified story's own (SOURCES.md).
BRIEFS = [
    (12, "Shenzhen:", "APEC summit week ends", RED),
    (13, "Bangladesh:", "turmoil hits 28 districts", RED),
    (14, "N. Korea:", "uranium enrichment rises", RED),
    (15, "Xi:", "$20m for APEC cooperation", RED),
    (16, "Ukraine:", "kept off the summit agenda", RED),
    (17, "Trump:", "US opposes global AI rules", RED),
    (18, "Seoul:", "Lee seeks Pyongyang dialogue", RED),
    (19, "Rockstar:", "markets GTA VI in China", RED),
    (20, "Putin:", "powers share aim to end war", RED),
    (21, "Caracas:", "US–Venezuela military deal", PLUM),
    (22, "NASA:", "sets CRS-25 launch coverage", PLUM),
    (23, "OpenAI:", "IPO expected next year", PLUM),
    (24, "New York:", "Cassatt, Douglas records", PLUM),
    (25, "Netanyahu:", "urges strikes on Iran", TEAL),
    (26, "Riyadh:", "tower hit by rocket debris", TEAL),
    (27, "Iran:", "chemical arms alleged by Trump", TEAL),
    (28, "Jericho:", "E1 delayed, settler killing", TEAL),
    (29, "Ethiopia:", "both sides mass forces", GOLD),
    (30, "Vanuatu:", "reform the climate talks", GREEN),
    (31, "Datacentres:", "face 70% emissions rise", GRAY),
    (32, "Record:", "589m children in war zones", GRAY),
    (33, "Georgieva:", "inflation has hit 4.7%", GRAY),
    (34, "GTA VI:", "firms give staff the day off", GRAY),
]

DATE_CHECK = (
    "DATE CHECK — Every story here happened, or was first "
    "reported, on Thursday 19 November 2026. Disputed claims are "
    "attributed, not stated as fact."
)

SOURCES_LINE = (
    "Sources: Reuters · AP · AFP · BBC · CBS News · USA Today · "
    "Le Monde · CNN · Al Jazeera · IAEA · IEA · NASA · "
    "Sensor Tower · The Art Newspaper"
)

# ------------------------------------------------------------- helpers


def F(path, size):
    return ImageFont.truetype(path, size)


def shrink_to_fit(draw, text, path, max_w, start, floor=8):
    """Largest font size, from start down, at which text fits."""
    size = start
    while size > floor:
        f = F(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return F(path, floor)


def wrap_lines(draw, text, f, max_w):
    """Greedy word wrap on measured widths; returns the lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def tracked_w(draw, text, f, tracking):
    return sum(draw.textlength(ch, font=f) for ch in text) \
        + tracking * max(0, len(text) - 1)


def draw_tracked(draw, x, y, text, f, fill, tracking=2):
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=f, fill=fill)
        cx += draw.textlength(ch, font=f) + tracking
    return cx


def make_thumb(path, w, h, crop=None):
    """Crop an artwork file to exactly w x h (explicit crop box
    first, then a centred crop to the target ratio)."""
    im = Image.open(path).convert("RGB")
    if crop is not None:
        im = im.crop(crop)
    ratio = w / h
    cw, ch = im.size
    if cw / ch > ratio:
        nw = int(ch * ratio)
        x0 = (cw - nw) // 2
        im = im.crop((x0, 0, x0 + nw, ch))
    else:
        nh = int(cw / ratio)
        y0 = (ch - nh) // 2
        im = im.crop((0, y0, cw, y0 + nh))
    return im.resize((w, h), Image.LANCZOS)


def make_wide(path, w, h, cx_frac):
    """Crop a panorama to exactly w x h on a window centred on
    the picture's subject (cx_frac of its width). The window
    keeps the panorama's full height whenever the box is wider
    than the source ratio allows, so the scene reads whole."""
    im = Image.open(path).convert("RGB")
    cw, ch = im.size
    ratio = w / h
    if cw / ch > ratio:
        nw = int(ch * ratio)
        x0 = int(cx_frac * cw - nw / 2)
        x0 = max(0, min(x0, cw - nw))
        im = im.crop((x0, 0, x0 + nw, ch))
    else:
        nh = int(cw / ratio)
        y0 = (ch - nh) // 2
        im = im.crop((0, y0, cw, y0 + nh))
    return im.resize((w, h), Image.LANCZOS)


def centered(draw, y, text, f, fill, cx=PAGE / 2):
    w = draw.textlength(text, font=f)
    draw.text((cx - w / 2, y), text, font=f, fill=fill)


# ------------------------------------------------------------- the map

# A dot-matrix world: 100 columns (longitude -180 to 180) by 25
# rows (latitude 85 to -40), '#' for land. Coarse by design - it
# only has to read as the world at a glance, with the pins doing
# the precise work.
MAP_ROWS = [
    "......####" ".........." ".........." "........##" "##........"
    "....#....." "....##.###" "......###." "....#....." "#.........",
    "....#####." ".##.##.##." ".........." "......####" "#####....."
    ".........." ".........." "...######." "..#######." ".....##...",
    "...#######" "##########" "#######..." ".......###" "####......"
    "..########" "##########" "##########" "##########" "########..",
    "...#######" "##########" "##########" "#.......##" "###......."
    ".#########" "##########" "##########" "##########" "#########.",
    "....######" "##########" "####....##" "####.....#" "##...#...."
    ".#########" "##########" "##########" "##########" "#########.",
    ".....#####" "##.#######" "####.....#" "#####....." "#.......##"
    "..########" "##########" "##########" "##########" "#######...",
    ".........." "......####" "##########" "###......." "........##"
    "##########" "##########" "##########" "##########" "#####.....",
    ".........." ".......###" "##########" "##........" ".......###"
    "##########" "##########" "##########" "##########" "#####.....",
    ".........." "......####" "##########" "#........." ".......###"
    "..########" "##########" "##########" "##########" "..........",
    ".........." "......####" "##########" ".........." ".........."
    ".#.#######" "##########" "##########" "#########." "..........",
    ".........." ".......###" "#########." ".........." ".....#####"
    "##########" "##########" "##########" "######...." "..........",
    ".........." ".........." "######.##." ".........." "....######"
    "##########" "##########" "##########" "####......" "..........",
    ".........." ".........." ".#####...." ".........." "....######"
    "##########" "##########" "##########" "....#....." "..........",
    ".........." ".........." "....###.##" "#####....." "....######"
    "##########" "#####....." "##########" "..###....." "..........",
    ".........." ".........." "........##" "#########." ".....#####"
    "##########" "####......" ".##...##.." ".........." "..........",
    ".........." ".........." "........##" "##########" "......####"
    "##########" "###......." ".....#####" "####..###." "..........",
    ".........." ".........." "........##" "##########" ".......###"
    "##########" ".#........" ".....#####" "##########" "#.........",
    ".........." ".........." ".........#" "#########." "........##"
    "##########" "#........." ".........." "###....###" "##........",
    ".........." ".........." ".........#" "#########." "........##"
    "##########" ".........." ".........#" "###......." "..........",
    ".........." ".........." ".........#" "########.." ".........#"
    "#########." ".##......." ".........." "..########" "##........",
    ".........." ".........." ".........#" "#######..." ".........#"
    "########.." ".###......" ".........." ".#########" "###.......",
    ".........." ".........." ".........#" "######...." ".........."
    "#######..." ".##......." ".........." ".#########" "###.......",
    ".........." ".........." ".........#" "#####....." ".........."
    "######...." ".........." ".........." "..########" "##........",
    ".........." ".........." ".........#" "####......" ".........."
    ".####....." ".........." ".........." "...#######" "#.....##..",
    ".........." ".........." ".........#" "###......." ".........."
    ".........." ".........." ".........." "......####" "#.....###.",
]
for _row in MAP_ROWS:
    assert len(_row) == 100, f"map row is {len(_row)} cells wide"

# (label, longitude, latitude, colour, dx, dy) - the eleven
# drawn stories pinned by number; the nudges keep the dense
# European and Gulf clusters from sitting on each other. The
# New York pill carries the three drawn stories that belong
# to the city: the GTA VI launch's publisher, the Anthropic
# listing on Nasdaq and the Van Gogh sale at Sotheby's.
PINS = [
    ("1", 114.1, 22.5, RED, 0, 0),          # Shenzhen - the summit
    ("4", 4.3, 52.1, NAVY, -5, 2),          # The Hague
    ("6", 13.4, 52.5, NAVY, 10, -3),        # Berlin
    ("5", 34.1, 44.9, NAVY, 3, -3),         # Crimea
    ("9", 30.7, 36.9, TEAL, -4, 0),         # Antalya
    ("11", 34.3, 31.4, TEAL, 6, 7),         # Gaza
    ("10", 48.0, 29.4, TEAL, 3, 1),         # Kuwait
    ("2·3·7", -74.0, 40.7, PLUM, 0, 0),     # New York x3
    ("8", -81.7, 27.8, PLUM, -2, 2),        # Florida
]

# Small unnumbered dots for briefs with a clear place:
# (longitude, latitude, colour).
BRIEF_DOTS = [
    (90.4, 23.8, RED),      # 13 Dhaka
    (125.8, 39.7, RED),     # 14 Yongbyon
    (-66.9, 10.5, PLUM),    # 21 Caracas
    (40.0, 9.0, GOLD),      # 29 Ethiopia-Eritrea border
    (167.0, -16.0, GREEN),  # 30 Vanuatu
]


def draw_map(page, draw, x, y, w, h):
    """The dot world with the drawn stories pinned by number
    and small dots for the briefs that have a clear place."""
    cols, rows = 100, 25
    cw, chh = w / cols, h / rows
    for r, row in enumerate(MAP_ROWS):
        for c, cell in enumerate(row):
            if cell == "#":
                cx = x + (c + 0.5) * cw
                cy = y + (r + 0.5) * chh
                draw.ellipse([cx - 1.3, cy - 1.3, cx + 1.3, cy + 1.3],
                             fill=MAPDOT)
    for lon, lat, colour in BRIEF_DOTS:
        px = x + (lon + 180) / 360 * w
        py = y + (85 - lat) / 125 * h
        draw.ellipse([px - 2.6, py - 2.6, px + 2.6, py + 2.6],
                     fill=colour)
    f_pin = F(SANS_BOLD, 8)
    for label, lon, lat, colour, dx, dy in PINS:
        px = x + (lon + 180) / 360 * w + dx
        py = y + (85 - lat) / 125 * h + dy
        if "·" in label:
            tw = draw.textlength(label, font=f_pin)
            draw.rounded_rectangle(
                [px - tw / 2 - 4, py - 6.5, px + tw / 2 + 4, py + 6.5],
                radius=6, fill=colour)
            draw.text((px - tw / 2, py - 4.5), label,
                      font=f_pin, fill=WHITE)
        else:
            draw.ellipse([px - 7.5, py - 7.5, px + 7.5, py + 7.5],
                         fill=colour, outline=WHITE, width=1)
            tw = draw.textlength(label, font=f_pin)
            draw.text((px - tw / 2, py - 4.5), label,
                      font=f_pin, fill=WHITE)

# ------------------------------------------------------------- sections


def draw_masthead(draw):
    """The navy band: date badge at the left, the paper's name
    and the huge date centred, the counts at the top right."""
    draw.rectangle([0, 0, PAGE, MASTHEAD_H], fill=NAVY)
    bx, by, bw, bh = MARGIN, 10, 74, 76
    draw.rectangle([bx, by, bx + bw, by + bh], fill=WHITE)
    draw.rectangle([bx, by, bx + bw, by + 19], fill=RED)
    centered(draw, by + 3, "NOV", F(SANS_BOLD, 12), WHITE,
             cx=bx + bw / 2)
    centered(draw, by + 21, "19", F(SERIF_BLACK, 34), NAVY,
             cx=bx + bw / 2)
    centered(draw, by + 61, "THU · 2026", F(SANS_BOLD, 9), RED,
             cx=bx + bw / 2)
    f_counts = F(SANS_BOLD, 9.5)
    cw_ = tracked_w(draw, COUNTS_LINE, f_counts, 1)
    draw_tracked(draw, PAGE - MARGIN - cw_, 12, COUNTS_LINE,
                 f_counts, WHITE, 1)
    name = "THE WORLD IN ONE DAY"
    f_name = F(SANS_BOLD, 11)
    nw = tracked_w(draw, name, f_name, 3)
    draw_tracked(draw, (PAGE - nw) / 2, 11, name, f_name, WHITE, 3)
    date = "Thursday 19 November 2026"
    f_date = shrink_to_fit(draw, date, SERIF_BLACK, 720, 41)
    centered(draw, 20, date, f_date, WHITE)
    centered(draw, 74, STANDFAST, F(SERIF_IT, 12), NAVY_TXT)
    return MASTHEAD_H


def draw_rainbow(draw, y):
    """One band of seven coloured segments, one per region,
    each carrying its story count; segment widths grow with
    the counts, over a minimum that fits the label."""
    f_seg = F(SANS_BOLD, 10)
    labels = [f"{name} {count}" for name, count, _ in REGION_BAND]
    mins = [draw.textlength(t, font=f_seg) + 18 for t in labels]
    extra = PAGE - sum(mins)
    total = sum(c for _, c, _ in REGION_BAND)
    x = 0.0
    for (name, count, color), lab, mn in zip(REGION_BAND, labels,
                                             mins):
        w = mn + extra * count / total
        draw.rectangle([x, y, x + w, y + RAINBOW_H], fill=color)
        tw = draw.textlength(lab, font=f_seg)
        draw.text((x + (w - tw) / 2, y + 3), lab, font=f_seg,
                  fill=WHITE)
        x += w
    return y + RAINBOW_H


def draw_timeline(draw, y):
    """THE DAY IN UTC: a red label box and four moment boxes,
    each with its time in red over its label."""
    draw.rectangle([MARGIN, y, MARGIN + 92, y + TIMELINE_H],
                   fill=RED)
    centered(draw, y + 5, "THE DAY", F(SANS_BOLD, 10.5), WHITE,
             cx=MARGIN + 46)
    centered(draw, y + 19, "IN UTC", F(SANS_BOLD, 10.5), WHITE,
             cx=MARGIN + 46)
    bx = MARGIN + 92 + 6
    bw = (PAGE - MARGIN - bx - 3 * 6) / 4
    f_time = F(SANS_BOLD, 11.5)
    f_lab = F(SANS, 9.5)
    for i, (time, text) in enumerate(TIMELINE):
        x = bx + i * (bw + 6)
        draw.rectangle([x, y, x + bw, y + TIMELINE_H], fill=WHITE,
                       outline=HAIRLINE, width=1)
        draw.text((x + 8, y + 4), time, font=f_time, fill=RED)
        draw.text((x + 8, y + 21), text, font=f_lab, fill=INK)
    return y + TIMELINE_H


def draw_card(page, draw, x, y, w, card, art_h, head_size,
              head_lh, brief_size, brief_lh):
    """One numbered story card with its artwork on top at
    about 2:1; returns its height. The artwork is shown whole
    on its focal window (the hero on its HERO_CROP); the
    story's number and region kicker, its headline and its
    brief run under the art, with the source tag at the
    right of the kicker line."""
    if card["img"] == "hero-apec.png":
        art = make_thumb(os.path.join(ASSETS, card["img"]), w,
                         art_h, crop=HERO_CROP)
    else:
        art = make_wide(os.path.join(ASSETS, card["img"]), w,
                        art_h, FOCAL[card["img"]])
    page.paste(art, (x, y))
    draw.rectangle([x, y, x + w, y + art_h], outline=HAIRLINE,
                   width=1)
    ty = y + art_h + 5
    f_num = F(SANS_BOLD, 13)
    draw.text((x, ty), str(card["n"]), font=f_num,
              fill=card["color"])
    nw = draw.textlength(str(card["n"]) + " ", font=f_num)
    draw_tracked(draw, x + nw + 2, ty + 3, card["kicker"],
                 F(SANS_BOLD, 8.5), card["color"], 1)
    f_tag = F(SANS_BOLD, 7.5)
    tagw = tracked_w(draw, card["tag"], f_tag, 1)
    draw_tracked(draw, x + w - tagw, ty + 3, card["tag"], f_tag,
                 FADED, 1)
    f_head = F(SERIF_BOLD, head_size)
    head = wrap_lines(draw, card["head"], f_head, w)
    assert len(head) <= 2, f"card headline overflow: {card['head']}"
    hy = ty + 16
    for ln in head:
        draw.text((x, hy), ln, font=f_head, fill=INK)
        hy += head_lh
    f_brief = F(SANS, brief_size)
    brief = wrap_lines(draw, card["brief"], f_brief, w)
    assert len(brief) <= 3, f"card brief overflow: {card['head']}"
    by = hy + 2
    for ln in brief:
        draw.text((x, by), ln, font=f_brief, fill=INK)
        by += brief_lh
    return int(round(by - y))


def draw_card_row(page, draw, y, cards, art_h, head_size, head_lh,
                  brief_size, brief_lh):
    """A row of cards across the content width; returns the
    row's bottom."""
    n = len(cards)
    gap = 11 if n == 3 else 10
    bw = (CONTENT_W - (n - 1) * gap) // n
    h = 0
    for i, card in enumerate(cards):
        h = max(h, draw_card(page, draw, MARGIN + i * (bw + gap),
                             y, bw, card, art_h, head_size,
                             head_lh, brief_size, brief_lh))
    return y + h


def draw_bottom(page, draw, y):
    """WHERE IT HAPPENED at the left - the dot-matrix map,
    its pins and the region legend - and ALSO ON THURSDAY 19
    NOVEMBER at the right: the 23 briefs as numbered
    one-liners in three columns, each opening with a bold
    lead word. Returns the zone's bottom."""
    f_head = F(SANS_BOLD, 10.5)
    draw_tracked(draw, MARGIN, y, "WHERE IT HAPPENED", f_head,
                 INK, 2)
    ax = MARGIN + MAP_W + 16
    draw_tracked(draw, ax, y, "ALSO ON THURSDAY 19 NOVEMBER",
                 f_head, INK, 2)
    top = y + 15
    draw_map(page, draw, MARGIN, top, MAP_W, MAP_H)
    legend = ("ASIA 10 · EUROPE 3 · AMERICAS 8 · MID EAST 7 · "
              "AFRICA 1 · OCEANIA 1 · GLOBAL 4")
    draw.text((MARGIN, top + MAP_H + 4), legend, font=F(SANS, 7.5),
              fill=FADED)
    left_bottom = top + MAP_H + 14
    aw = PAGE - MARGIN - ax
    cols, gap = 3, 12
    col_w = (aw - (cols - 1) * gap) // cols
    per_col = (len(BRIEFS) + cols - 1) // cols
    f_no = F(SANS_BOLD, 11)
    f_lead = F(SANS_BOLD, 11)
    f_rest = F(SANS, 11)
    bottom = top
    for j, (num, lead, rest, color) in enumerate(BRIEFS):
        cx = ax + (j // per_col) * (col_w + gap)
        cy = top + (j % per_col) * 14
        label = f"{num}."
        draw.text((cx, cy), label, font=f_no, fill=color)
        nw = draw.textlength(label + " ", font=f_no)
        draw.text((cx + nw, cy), lead, font=f_lead, fill=INK)
        lw = draw.textlength(lead + " ", font=f_lead)
        one = wrap_lines(draw, rest, f_rest, col_w - nw - lw)
        assert len(one) == 1, f"ALSO line wraps: {lead} {rest}"
        draw.text((cx + nw + lw, cy), one[0], font=f_rest, fill=INK)
        bottom = max(bottom, cy + 14)
    return int(round(max(left_bottom, bottom)))


def draw_footer(draw, y):
    draw.rectangle([MARGIN, y, PAGE - MARGIN, y + 24], outline=RED,
                   width=2)
    f_dc = shrink_to_fit(draw, DATE_CHECK, SANS_BOLD,
                         CONTENT_W - 20, 10)
    centered(draw, y + 3, DATE_CHECK, f_dc, RED)
    f_src = shrink_to_fit(draw, SOURCES_LINE, SANS, CONTENT_W - 20,
                          8.5)
    centered(draw, y + 13, SOURCES_LINE, f_src, FADED)
    return y + 24


def build_page():
    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(page)
    y = draw_masthead(draw)
    y = draw_rainbow(draw, y)
    y = draw_timeline(draw, y + 6) + 6
    y = draw_card_row(page, draw, y, LEAD_CARDS, LEAD_ART_H, 24,
                      26, 10, 12.5)
    y = draw_card_row(page, draw, y + 8, ROW_CARDS[:4], CARD_ART_H,
                      15, 17, 9.5, 11.5)
    y = draw_card_row(page, draw, y + 8, ROW_CARDS[4:],
                      CARD_ART_H, 15, 17, 9.5, 11.5)
    y = draw_bottom(page, draw, y + 8)
    y = draw_footer(draw, y + 6)
    assert y <= PAGE - 2, f"page overflow: content ends at {y}"
    return page


def main():
    page = build_page()
    page.save(OUT_PATH, optimize=True)
    size = os.path.getsize(OUT_PATH)
    fmt = "PNG"
    if size > 1_048_576:
        page.save(OUT_PATH, format="JPEG", quality=88)
        size = os.path.getsize(OUT_PATH)
        fmt = "JPEG q88"
    if size > 1_048_576:
        page.save(OUT_PATH, format="JPEG", quality=80)
        size = os.path.getsize(OUT_PATH)
        fmt = "JPEG q80"
    print(f"wrote {OUT_PATH}: {page.size}, {fmt}, {size} bytes")
    assert size <= 1_048_576, "entry image exceeds the 1 MiB gate"


if __name__ == "__main__":
    main()
