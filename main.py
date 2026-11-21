"""news-image-20261120 entry: draws /output/entry.png, a front page summing up
the world's news of 20 November 2026, using the Python standard library only.
"""
import os

from font5x7 import GLYPH_H, GLYPH_W, glyph_rows
from pngwrite import write_png

WIDTH = 1024
HEIGHT = 1024

PAPER = (247, 244, 235)
INK = (20, 18, 16)
RULE = (60, 56, 50)
RED = (150, 24, 20)
MUTED = (96, 90, 82)
TAG_BG = (20, 18, 16)
TAG_FG = (247, 244, 235)

TAG_COLORS = {
    "UKRAINE": (120, 20, 20),
    "WORLD COURT": (70, 40, 110),
    "MARKETS": (26, 90, 60),
    "COP31": (160, 100, 20),
    "AFRICA": (150, 90, 20),
    "INDIA": (20, 90, 110),
}


def new_canvas(width, height, color):
    row = bytearray(color * width)
    return [bytearray(row) for _ in range(height)]


def fill_rect(rows, x, y, w, h, color):
    width = len(rows[0]) // 3
    height = len(rows)
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(width, x + w), min(height, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    seg = bytes(color) * (x1 - x0)
    for yy in range(y0, y1):
        rows[yy][x0 * 3:x1 * 3] = seg


def hline(rows, x, y, w, color, thickness=1):
    fill_rect(rows, x, y, w, thickness, color)


def vline(rows, x, y, h, color, thickness=1):
    fill_rect(rows, x, y, thickness, h, color)


def text_width(s, scale, spacing=1):
    return len(s) * (GLYPH_W * scale + spacing) - spacing if s else 0


def draw_text(rows, x, y, s, color, scale=2, spacing=1):
    cx = x
    for ch in s:
        for gy in range(GLYPH_H):
            bits = glyph_rows(ch)[gy]
            for gx in range(GLYPH_W):
                if bits[gx] == "1":
                    fill_rect(rows, cx + gx * scale, y + gy * scale, scale, scale, color)
        cx += GLYPH_W * scale + spacing
    return cx - spacing


def draw_text_centered(rows, cx, y, s, color, scale=2, spacing=1):
    w = text_width(s, scale, spacing)
    draw_text(rows, cx - w // 2, y, s, color, scale, spacing)
    return w


def wrap_text(s, scale, max_width, spacing=1):
    words = s.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale, spacing) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_tag(rows, x, y, label, scale=2):
    pad = 7
    bg = TAG_COLORS.get(label, TAG_BG)
    w = text_width(label, scale) + pad * 2
    h = GLYPH_H * scale + pad
    fill_rect(rows, x, y, w, h, bg)
    draw_text(rows, x + pad, y + pad // 2, label, TAG_FG, scale)
    return w, h


def story_block(rows, x, y, w, tag, headline, detail, tag_scale=2, head_scale=3, detail_scale=2, gap=12):
    _, th = draw_tag(rows, x, y, tag, tag_scale)
    y += th + gap
    for line in wrap_text(headline, head_scale, w):
        draw_text(rows, x, y, line, INK, head_scale)
        y += GLYPH_H * head_scale + 8
    y += 6
    for line in wrap_text(detail, detail_scale, w):
        draw_text(rows, x, y, line, MUTED, detail_scale)
        y += GLYPH_H * detail_scale + 6
    return y


def build():
    rows = new_canvas(WIDTH, HEIGHT, PAPER)

    # outer border
    fill_rect(rows, 0, 0, WIDTH, 10, INK)
    fill_rect(rows, 0, HEIGHT - 10, WIDTH, 10, INK)
    fill_rect(rows, 0, 0, 10, HEIGHT, INK)
    fill_rect(rows, WIDTH - 10, 0, 10, HEIGHT, INK)

    margin = 40

    # masthead
    draw_text_centered(rows, WIDTH // 2, 40, "WORLD DAILY", INK, scale=6, spacing=3)
    hline(rows, margin, 112, WIDTH - margin * 2, INK, 4)
    draw_text_centered(rows, WIDTH // 2, 126, "FRIDAY, NOVEMBER 20, 2026", RED, scale=4, spacing=3)
    hline(rows, margin, 184, WIDTH - margin * 2, INK, 4)

    y = 212

    # main headline
    draw_tag(rows, margin, y, "SHENZHEN SUMMIT", 3)
    y += 56
    for line in wrap_text("TRUMP, XI AND PUTIN MEET, PLEDGE NUCLEAR WAR CANNOT BE WON",
                           4, WIDTH - margin * 2):
        draw_text(rows, margin, y, line, INK, 4)
        y += GLYPH_H * 4 + 10
    y += 8
    for line in wrap_text(
            "LEADERS ISSUE JOINT DECLARATION AT FIRST TRILATERAL TALKS; TRUMP SAYS HE MAY MEET KIM NEXT",
            3, WIDTH - margin * 2):
        draw_text(rows, margin, y, line, MUTED, 3)
        y += GLYPH_H * 3 + 8

    y += 22
    hline(rows, margin, y, WIDTH - margin * 2, RULE, 2)
    y += 32

    col_gap = 28
    col_w = (WIDTH - margin * 2 - col_gap * 2) // 3
    cols_x = [margin, margin + col_w + col_gap, margin + (col_w + col_gap) * 2]

    stories = [
        ("UKRAINE", "RUSSIAN STRIKES HIT KYIV BRIDGES",
         "OVERNIGHT DRONE AND MISSILE ATTACK KILLS 8, DAMAGES THREE DNIPRO RIVER CROSSINGS"),
        ("WORLD COURT", "MYANMAR RULED RESPONSIBLE FOR ROHINGYA GENOCIDE",
         "ICJ ISSUES ITS FIRST GENOCIDE VERDICT IN LANDMARK CASE"),
        ("MARKETS", "ANTHROPIC SHARES TRADE NEAR $100 AFTER RECORD IPO",
         "$81 BILLION OFFERING IS LARGEST ON RECORD, TOPPING SPACEX'S JUNE DEBUT"),
        ("COP31", "CLIMATE DRAFT DROPS FOSSIL FUEL LANGUAGE",
         "SLIMMED-DOWN TEXT LEANS ON CARBON CAPTURE INSTEAD"),
        ("AFRICA", "ETHIOPIA, ERITREA TRADE STRIKES NEAR BADME",
         "DRONE AND ARTILLERY FIRE ESCALATES ALONG DISPUTED BORDER"),
        ("INDIA", "CYCLONE AKVAN MAKES LANDFALL IN ODISHA",
         "MORE THAN 300,000 PEOPLE EVACUATED FROM COASTAL DISTRICTS"),
    ]

    grid_top = y
    row_bottom = grid_top
    for i, (tag, headline, detail) in enumerate(stories):
        col = i % 3
        if col == 0 and i > 0:
            grid_top = row_bottom + 30
            hline(rows, margin, grid_top - 15, WIDTH - margin * 2, RULE, 1)
        yb = story_block(rows, cols_x[col], grid_top, col_w, tag, headline, detail,
                          tag_scale=2, head_scale=2, detail_scale=2, gap=10)
        row_bottom = max(row_bottom, yb)

    y = row_bottom + 28
    hline(rows, margin, y, WIDTH - margin * 2, INK, 4)
    y += 24

    draw_tag(rows, margin, y, "ALSO TODAY", 3)
    y += 56
    ticker_lines = [
        "AMERICAS: HAITI POLICE SAY 34 GANG MEMBERS KILLED IN PORT-AU-PRINCE OPERATION",
        "SPORT: KENYA'S JEPCHIRCHIR BANNED 3 YEARS FOR DOPING",
        "SCIENCE: MOON DUST 3D-PRINTED INTO LUNAR BUILDING BRICKS",
    ]
    for line in ticker_lines:
        draw_text(rows, margin, y, line, INK, 2)
        y += GLYPH_H * 2 + 12

    return rows, y


def main():
    rows, used_y = build()
    assert used_y < HEIGHT - 20, f"content overflowed canvas: {used_y}"
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    write_png(out_path, WIDTH, HEIGHT, rows)


if __name__ == "__main__":
    main()
