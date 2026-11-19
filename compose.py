#!/usr/bin/env python3
"""Compose the entry image for make.fun news-image-20261119:
"The World in One Day" for Thursday 19 November 2026, a one-page
newspaper holding 34 stories.

Page plan, on a 1024x1024 cream sheet, top to bottom:
  masthead   the paper's name, the date as headline, a deck line
  stat band  six of the day's headline numbers with captions
  lead       story 1 - the first Trump-Xi-Putin three-way summit in
             Shenzhen, with the APEC cover illustration drawn for the
             18 November edition (assets/hero-apec.png)
  grid       stories 2-13 in three rows of four boxes; each box is a
             flat editorial illustration, a kicker, a headline and a
             three-line summary
  also       stories 14-34 as numbered one-liners in two columns
  strip      the DATE CHECK line and the sources line in one box

All wording is set here in PIL from the story data below. The
illustrations are text-free artwork, so no lettering can come out
garbled. SOURCES.md is the verification record behind every line.

Output is entry.png beside this file. If the PNG ever exceeded the
1,048,576-byte gate the script falls back to JPEG bytes (the grader
reads the format from the magic bytes), but the flat artwork and
cream page normally keep PNG well under it.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT_PATH = os.path.join(HERE, "entry.png")

PAGE = 1024
MARGIN = 24
CONTENT_W = PAGE - 2 * MARGIN  # 976

PAPER = (246, 241, 228)
INK = (27, 26, 23)
FADED = (92, 87, 76)
STAT_LABEL = (70, 65, 56)  # darker than FADED: stat captions sit at
# 9pt, where FADED's contrast on cream gets thin; this keeps them
# clearly readable without shouting over the numbers above them.
HAIRLINE = (168, 160, 144)
RED = (158, 27, 27)
NAVY = (22, 50, 74)
GOLD = (168, 127, 20)
TEAL = (15, 118, 110)
PLUM = (91, 74, 138)
GREEN = (63, 98, 18)

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
NUMBERS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# ------------------------------------------------------------- the day

STATS = [
    ("$81.3bn", "RAISED IN ANTHROPIC'S IPO, THE LARGEST EVER", GREEN),
    ("15.9m", "GTA VI PRE-ORDERS BANKED BEFORE RELEASE DAY", PLUM),
    ("730,000", "ROHINGYA WHO FLED IN 2017, IN THE ICJ CASE", NAVY),
    ("$120bn", "ADAPTATION FINANCE UNRESOLVED AT COP31", TEAL),
    ("589m", "CHILDREN LIVING IN CONFLICT ZONES, A RECORD", RED),
    ("15.3 in", "OF RAIN ON BROWARD COUNTY IN 24 HOURS", NAVY),
]

LEAD = {
    "kicker": "1 · SHENZHEN · SUMMIT",
    "headline": "Trump, Xi and Putin hold first three-way summit",
    "summary": (
        "The leaders of the United States, China and Russia sat down "
        "together in Shenzhen on Thursday for an hour of talks spanning "
        "Ukraine, Iran, nuclear arms, trade and AI. Trump also met each "
        "man separately beforehand. No breakthrough was expected, and "
        "none was announced."
    ),
    "credit": "Cover: the three leaders in Shenzhen. Original illustration.",
    "image": "hero-apec.png",
    "hero_crop": (60, 400, 1540, 1185),
}

BOXES = [
    {
        "kicker": "2 · NEW YORK · GAMES",
        "headline": "GTA VI arrives after a 13-year wait",
        "summary": (
            "Unlocked at midnight in each country, New Zealand first, "
            "on PS5 and Xbox; no PC yet. First reviews: 99 of 100; "
            "2.3m watched the streams."
        ),
        "image": "illo-gta.png",
    },
    {
        "kicker": "3 · NASDAQ · MARKETS",
        "headline": "Anthropic debuts in the biggest IPO ever",
        "summary": (
            "Priced at $83, above its range, the Claude maker raised "
            "$81.3bn, valuing it near $1.5tn. Shares trade from "
            "Thursday as ANT."
        ),
        "image": "illo-anthropic.png",
    },
    {
        "kicker": "4 · THE HAGUE · LAW",
        "headline": "World Court reads judgment on Myanmar",
        "summary": (
            "The ICJ delivers judgment in The Gambia's genocide case "
            "over the 2017 crackdown on the Rohingya. Myanmar "
            "denies it."
        ),
        "image": "illo-icj.png",
    },
    {
        "kicker": "5 · ANTALYA · CLIMATE",
        "headline": "COP31 enters its final 48 hours",
        "summary": (
            "Ministers take over the text in Antalya, but the $120bn "
            "adaptation finance package is still open as the talks "
            "near their end."
        ),
        "image": "illo-cop31.png",
    },
    {
        "kicker": "6 · CRIMEA · WAR",
        "headline": "Ukraine hits Crimean Bridge a third time",
        "summary": (
            "Traffic is suspended after a third strike in a week on "
            "the bridge between Russia and Crimea."
        ),
        "image": "illo-kerch.png",
    },
    {
        "kicker": "7 · GULF · WAR",
        "headline": "Kuwait repels first Iranian attack in two months",
        "summary": (
            "Kuwait fought off its first Iranian attack in two months. "
            "The IEA calls the Hormuz crisis the greatest "
            "energy-security threat it has seen."
        ),
        "image": "illo-gulf.png",
    },
    {
        "kicker": "8 · DHAKA · UNREST",
        "headline": "Bangladesh sinks into turmoil",
        "summary": (
            "Muhammad Yunus's ancestral home was set ablaze and "
            "violence hit 28 districts, as backers of the "
            "death-sentenced Sheikh Hasina protest."
        ),
        "image": "illo-bangladesh.png",
    },
    {
        "kicker": "9 · NEW YORK · ART",
        "headline": "Van Gogh sells for a record $190.4m",
        "summary": (
            "Châtaigniers en Fleurs (1890), unseen for 50 years, "
            "smashed the artist's record at Sotheby's in New York, "
            "at $190.4m with fees."
        ),
        "image": "illo-vangogh.png",
    },
    {
        "kicker": "10 · FLORIDA · WEATHER",
        "headline": "Flooded Florida braces for more rain",
        "summary": (
            "15.3 inches of rain fell near Plantation and Hollywood "
            "took 300-plus calls in a night. Schools stay shut "
            "Thursday; more rain is due."
        ),
        "image": "illo-florida.png",
    },
    {
        "kicker": "11 · BERLIN · DEFENCE",
        "headline": "Europe gathers to arm Ukraine's future",
        "summary": (
            "Leaders gather in Berlin to define Ukraine's defence "
            "future, as the Commission proposes a new €45bn loan "
            "for Kyiv."
        ),
        "image": "illo-europe.png",
    },
    {
        "kicker": "12 · YONGBYON · NUCLEAR",
        "headline": "North Korea expands uranium work",
        "summary": (
            "The UN watchdog reports expanded uranium enrichment at "
            "Yongbyon, North Korea's main nuclear complex."
        ),
        "image": "illo-northkorea.png",
    },
    {
        "kicker": "13 · GAZA · WAR",
        "headline": "Israel pushes beyond the Yellow Line",
        "summary": (
            "Israeli forces launch a ground operation beyond the "
            "Yellow Line in central Gaza, the line the ceasefire "
            "drew across the territory."
        ),
        "image": "illo-gaza.png",
    },
]

ALSO = [
    "APEC leaders wind up in Shenzhen; Putin backs the draft declaration",
    "Xi pledges $20m for APEC cooperation and a new studies centre",
    "Ukraine is off the summit agenda, the White House says; Kyiv watches",
    "The US and Venezuela sign a military cooperation agreement",
    "Netanyahu presses Trump to strike Iran's nuclear and energy sites",
    "A Riyadh tower is damaged by debris from an intercepted Houthi rocket",
    "Trump says Iran is exploring chemical and biological weapons",
    "Ethiopia and Eritrea mass their forces along the border",
    "Israel delays E1 settlement; a settler kills a woman near Jericho",
    "Datacentres face a 70% rise in emissions by 2030, says the IEA",
    "A record 589 million children now live in conflict zones",
    "IMF chief Georgieva warns world inflation has hit 4.7%",
    "Vanuatu urges reform of the climate talks themselves",
    "NASA sets coverage for Northrop Grumman's CRS-25 launch",
    "Some companies give staff the day off to play GTA VI",
    "OpenAI is expected to hold its own IPO next year",
    "Art records also fall for Cassatt ($13.3m) and Douglas ($14.5m)",
    "Trump tells APEC the US opposes global regulation of AI",
    "South Korea's Lee calls for renewed dialogue with Pyongyang",
    "Rockstar promotes GTA VI in China, where it cannot yet sell it",
    "Putin: all three powers share an interest in ending the Ukraine war",
]

DATE_CHECK = (
    "DATE CHECK - Every story here happened, or was first reported, "
    "on Thursday 19 November 2026. Disputed claims are attributed, "
    "not stated as fact."
)

SOURCES_LINE = (
    "Sources: Reuters · AP · AFP · BBC · CBS News · USA Today · "
    "Le Monde · CNN · Al Jazeera · IAEA · IEA · NASA · Sensor Tower "
    "· The Art Newspaper"
)

# ------------------------------------------------------------- helpers


def F(path, size):
    return ImageFont.truetype(path, size)


def shrink_to_fit(draw, text, path, max_w, start, floor=9):
    """Largest font size, from start down, at which text fits max_w."""
    size = start
    while size > floor:
        f = F(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return F(path, floor)


def wrap_lines(draw, text, f, max_w):
    """Greedy wrap on measured widths; returns the line list."""
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
    """Crop an artwork file to exactly w x h (explicit crop first,
    then a centred crop to the target ratio)."""
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


def centered(draw, y, text, f, fill):
    w = draw.textlength(text, font=f)
    draw.text(((PAGE - w) / 2, y), text, font=f, fill=fill)


# ------------------------------------------------------------- layout


def build_page():
    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(page)

    # ---- masthead ----------------------------------------------
    draw.rectangle([MARGIN, 12, PAGE - MARGIN, 15], fill=INK)
    draw.line([MARGIN, 19, PAGE - MARGIN, 19], fill=INK, width=1)
    f_brand = F(SANS_BOLD, 12)
    draw_tracked(draw, MARGIN, 25, "THE WORLD IN ONE DAY", f_brand, INK, 3)
    tag = "ONE PAGE · 34 STORIES"
    tw = tracked_w(draw, tag, f_brand, 3)
    draw_tracked(draw, PAGE - MARGIN - tw, 25, tag, f_brand, INK, 3)

    title = "Thursday 19 November 2026"
    f_title = shrink_to_fit(draw, title, SERIF_BLACK, CONTENT_W, 47)
    centered(draw, 42, title, f_title, INK)
    deck = ("Three powers sit down in Shenzhen · GTA VI arrives after "
            "13 years · Anthropic's record debut")
    f_deck = shrink_to_fit(draw, deck, SERIF_IT, CONTENT_W, 16)
    centered(draw, 96, deck, f_deck, FADED)
    draw.line([MARGIN, 118, PAGE - MARGIN, 118], fill=INK, width=1)
    draw.rectangle([MARGIN, 121, PAGE - MARGIN, 124], fill=INK)

    # ---- stat band ----------------------------------------------
    band_y = 130
    col_w = CONTENT_W // 6
    for i, (num, label, colour) in enumerate(STATS):
        x = MARGIN + i * col_w
        draw.rectangle([x + 4, band_y, x + col_w - 4, band_y + 4],
                       fill=colour)
        f_num = shrink_to_fit(draw, num, NUMBERS, col_w - 12, 29, 17)
        nw = draw.textlength(num, font=f_num)
        draw.text((x + (col_w - nw) / 2, band_y + 9), num,
                  font=f_num, fill=INK)
        f_lab = F(SANS_BOLD, 9)
        lab = wrap_lines(draw, label, f_lab, col_w - 10)
        assert len(lab) <= 3, f"stat caption too long: {label}"
        ly = band_y + 44
        for ln in lab:
            lw = draw.textlength(ln, font=f_lab)
            draw.text((x + (col_w - lw) / 2, ly), ln,
                      font=f_lab, fill=STAT_LABEL)
            ly += 11
        if i:
            draw.line([x, band_y + 9, x, band_y + 70],
                      fill=HAIRLINE, width=1)
    draw.line([MARGIN, band_y + 76, PAGE - MARGIN, band_y + 76],
              fill=INK, width=1)

    # ---- lead ----------------------------------------------------
    lead_y = band_y + 84
    img_w, img_h = 380, 134
    hero = make_thumb(os.path.join(ASSETS, LEAD["image"]), img_w, img_h,
                      crop=LEAD["hero_crop"])
    page.paste(hero, (MARGIN, lead_y))
    draw.rectangle([MARGIN, lead_y, MARGIN + img_w, lead_y + img_h],
                   outline=INK, width=1)
    draw.text((MARGIN, lead_y + img_h + 4), LEAD["credit"],
              font=F(SERIF_IT, 10), fill=FADED)
    tx = MARGIN + img_w + 16
    tw2 = PAGE - MARGIN - tx
    draw_tracked(draw, tx, lead_y + 2, LEAD["kicker"],
                 F(SANS_BOLD, 13), RED, 2)
    f_head = F(SERIF_BOLD, 31)
    head = wrap_lines(draw, LEAD["headline"], f_head, tw2)
    assert len(head) <= 2, "lead headline overflow"
    hy = lead_y + 24
    for ln in head:
        draw.text((tx, hy), ln, font=f_head, fill=INK)
        hy += 36
    draw.line([tx, hy + 2, PAGE - MARGIN, hy + 2], fill=HAIRLINE, width=1)
    f_sum = F(SANS, 13.5)
    body = wrap_lines(draw, LEAD["summary"], f_sum, tw2)
    assert len(body) <= 5, "lead summary overflow"
    sy = hy + 10
    for ln in body:
        draw.text((tx, sy), ln, font=f_sum, fill=INK)
        sy += 17
    lead_bottom = max(lead_y + img_h + 20, sy)

    # ---- grid of boxes --------------------------------------------
    grid_y = lead_bottom + 12
    gap = 12
    box_w = (CONTENT_W - 3 * gap) // 4
    thumb_h = 48
    box_h = 140
    row_gap = 8
    for idx, box in enumerate(BOXES):
        bx = MARGIN + (idx % 4) * (box_w + gap)
        by = grid_y + (idx // 4) * (box_h + row_gap)
        draw.line([bx, by - 5, bx + box_w, by - 5], fill=HAIRLINE, width=1)
        art = make_thumb(os.path.join(ASSETS, box["image"]),
                         box_w, thumb_h)
        page.paste(art, (bx, by))
        draw.rectangle([bx, by, bx + box_w, by + thumb_h],
                       outline=HAIRLINE, width=1)
        draw_tracked(draw, bx, by + thumb_h + 4, box["kicker"],
                     F(SANS_BOLD, 10), NAVY, 1)
        f_bh = F(SERIF_BOLD, 14.5)
        blines = wrap_lines(draw, box["headline"], f_bh, box_w)
        assert len(blines) <= 2, f"box headline overflow: {box['headline']}"
        hy2 = by + thumb_h + 17
        for ln in blines:
            draw.text((bx, hy2), ln, font=f_bh, fill=INK)
            hy2 += 16.5
        f_bs = F(SANS, 10.5)
        slines = wrap_lines(draw, box["summary"], f_bs, box_w)
        assert len(slines) <= 3, f"box summary overflow: {box['headline']}"
        sy2 = hy2 + 2
        for ln in slines:
            draw.text((bx, sy2), ln, font=f_bs, fill=INK)
            sy2 += 12.3
        assert sy2 <= by + box_h, f"box overflow: {box['headline']} -> {sy2}"
    # Thin vertical rules between the box columns: with only a 12px
    # gutter the four columns run together at a glance, and rules
    # are the classic newspaper fix for that.
    for c in range(1, 4):
        vx = MARGIN + c * (box_w + gap) - gap // 2
        draw.line([vx, grid_y - 5, vx,
                   grid_y + 3 * box_h + 2 * row_gap],
                  fill=HAIRLINE, width=1)
    grid_bottom = grid_y + 3 * box_h + 2 * row_gap

    # ---- also on thursday ------------------------------------------
    also_y = grid_bottom + 8
    draw.line([MARGIN, also_y, PAGE - MARGIN, also_y], fill=INK, width=1)
    draw_tracked(draw, MARGIN, also_y + 5, "ALSO ON THURSDAY",
                 F(SANS_BOLD, 13), INK, 2)
    items_y = also_y + 27
    col2_w = (CONTENT_W - 24) // 2
    per_col = (len(ALSO) + 1) // 2
    f_item = F(SANS, 11.5)
    f_no = F(SANS_BOLD, 11.5)
    row_h = 11.8
    for j, item in enumerate(ALSO):
        col = j // per_col
        row = j % per_col
        x = MARGIN + col * (col2_w + 24)
        y = items_y + row * row_h
        num = f"{j + 14}."
        draw.text((x, y), num, font=f_no, fill=RED)
        nw2 = draw.textlength(num + " ", font=f_no)
        one = wrap_lines(draw, item, f_item, col2_w - nw2)
        assert len(one) == 1, f"also item wraps: {item}"
        draw.text((x + nw2, y), one[0], font=f_item, fill=INK)
    items_bottom = items_y + per_col * row_h
    # A hairline down the middle of the ALSO columns keeps the two
    # numbered runs from bleeding into each other at reading speed.
    mid_x = MARGIN + col2_w + 12
    draw.line([mid_x, items_y, mid_x, items_bottom - 4],
              fill=HAIRLINE, width=1)

    # ---- date check + sources strip ---------------------------------
    strip_y = items_bottom + 4
    draw.rectangle([MARGIN, strip_y, PAGE - MARGIN, strip_y + 30],
                   outline=RED, width=2)
    f_dc = shrink_to_fit(draw, DATE_CHECK, SANS_BOLD, CONTENT_W - 20, 11)
    centered(draw, strip_y + 4, DATE_CHECK, f_dc, RED)
    f_src = shrink_to_fit(draw, SOURCES_LINE, SANS, CONTENT_W - 20, 10)
    centered(draw, strip_y + 17, SOURCES_LINE, f_src, FADED)
    assert strip_y + 30 <= PAGE - 2, f"page overflow: {strip_y + 30}"

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
