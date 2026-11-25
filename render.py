"""Draw the front page of THE WORLD TODAY for Wednesday 25 November 2026.

A single self-contained renderer: Pillow only, no network, no clock, no
randomness, so two runs produce byte-identical PNGs. Every headline, deck
and brief below was checked against wire reporting of 25 November 2026
(Reuters, AP/AFP via Manila Times, SCMP, CNN, Al Jazeera) on the morning
of the day; nothing in it is older than the day it sums up except where
the deck itself says the event broke the day before and the follow-up
(the loyalty pledge, the therapy admission, the market slide) is today's.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 230)
INK = (20, 20, 20)
GREY = (90, 86, 76)
RED = (163, 22, 33)
NAVY = (27, 42, 74)
GOLD = (176, 141, 60)
GREEN = (46, 94, 62)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, text, fnt, x, y, width, leading, fill=INK):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_skyline(draw, x, y, w, h):
    """Shanghai at dusk: navy sky, red sun, tower silhouettes."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    draw.ellipse([x + w - 72, y + 12, x + w - 16, y + 68], fill=RED)
    # Oriental Pearl Tower: spire with two spheres
    cx = x + 46
    draw.line([(cx, y + h - 16), (cx, y + 24)], fill=(240, 235, 220), width=5)
    draw.ellipse([cx - 18, y + 28, cx + 18, y + 64], fill=(240, 235, 220))
    draw.ellipse([cx - 12, y + 84, cx + 12, y + 108], fill=(240, 235, 220))
    # tower blocks
    draw.rectangle([x + 88, y + 58, x + 122, y + h - 16], fill=(58, 74, 110))
    draw.rectangle([x + 130, y + 36, x + 166, y + h - 16], fill=(74, 92, 132))
    draw.rectangle([x + 174, y + 72, x + 202, y + h - 16], fill=(58, 74, 110))
    draw.rectangle([x + 210, y + 48, x + 246, y + h - 16], fill=(74, 92, 132))
    for bx in (96, 138, 182, 218):
        for by in range(y + 66, y + h - 26, 15):
            draw.rectangle([x + bx, by, x + bx + 5, by + 6], fill=(240, 214, 120))
    # river band + label at the top, clear of the spire
    draw.rectangle([x, y + h - 14, x + w, y + h], fill=(96, 122, 158))
    draw.text((x + 84, y + 8), "SHANGHAI", font=font(SANS_B, 14),
              fill=(240, 235, 220))


def draw_chip(draw, x, y, w, h):
    """A chip on a board, with a falling red arrow at the right."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 40, 30))
    # chip, left of centre
    draw.rectangle([x + 14, y + 20, x + 92, y + h - 20], fill=(16, 26, 20),
                   outline=GOLD, width=2)
    for i in range(4):
        px = x + 26 + i * 18
        draw.line([(px, y + 8), (px, y + 20)], fill=GOLD, width=3)
        draw.line([(px, y + h - 20), (px, y + h - 8)], fill=GOLD, width=3)
    draw.rectangle([x + 26, y + 34, x + 80, y + h - 34], fill=GREEN)
    draw.text((x + 33, y + 42), "NVDA", font=font(SANS_B, 17),
              fill=(240, 235, 220))
    # falling arrow, right of the chip
    draw.line([(x + 112, y + 26), (x + 138, y + 58)], fill=RED, width=5)
    draw.polygon([(x + 138, y + 58), (x + 124, y + 54), (x + 134, y + 68)],
                 fill=RED)
    draw.text((x + 104, y + h - 24), "-6%", font=font(SANS_B, 16), fill=RED)


def draw_scales(draw, x, y, w, h):
    """Scales of justice over a dark panel."""
    draw.rectangle([x, y, x + w, y + h], fill=(38, 34, 30))
    cx, top = x + w // 2, y + 12
    draw.line([(cx, top), (cx, y + h - 24)], fill=GOLD, width=4)
    draw.line([(cx - 50, top + 14), (cx + 50, top + 14)], fill=GOLD, width=4)
    for sx in (cx - 50, cx + 50):
        draw.line([(sx, top + 14), (sx, top + 40)], fill=GOLD, width=3)
        draw.polygon([(sx - 24, top + 40), (sx + 24, top + 40), (sx, top + 56)],
                     outline=GOLD, width=3)
    draw.ellipse([cx - 8, top - 8, cx + 8, top + 8], fill=GOLD)
    draw.rectangle([x + 18, y + h - 20, x + w - 18, y + h - 12], fill=GOLD)


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 30  # outer margin

    # frame
    d.rectangle([12, 12, W - 13, H - 13], outline=INK, width=3)
    d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)

    # ---- masthead ----
    d.text((W // 2, 26), "THE WORLD TODAY", font=font(SERIF, 74), fill=INK,
           anchor="ma")
    rule(d, M, W - M, 122)
    dl = font(SANS_B, 20)
    d.text((M, 130), "WEDNESDAY", font=dl, fill=INK)
    d.text((W // 2, 130), "25 NOVEMBER 2026", font=dl, fill=INK, anchor="ma")
    d.text((W - M, 130), "No. 330", font=dl, fill=INK, anchor="ra")
    rule(d, M, W - M, 158, width=3)
    rule(d, M, W - M, 164, width=1)

    # ---- lead story ----
    y = 174
    d.text((M, y), "CHINA  ·  THE PURGE WIDENS", font=font(SANS_B, 18), fill=RED)
    y += 26
    y = para(d, "SHANGHAI FALLS IN LINE AS CHEN PROBE RATTLES BEIJING",
             font(SERIF, 40), M, y, W - 2 * M, 46)
    y += 4
    y = para(d, "City leaders pledge loyalty after Politburo member Chen Jining, 62, "
                "is placed under investigation — the fourth top leader to fall since 2025.",
             font(SERIF_R, 20), M, y, W - 2 * M, 25, fill=(52, 48, 42))
    y += 8
    body_top = y
    lead_text = (
        "Shanghai's Communist Party leadership pledged loyalty to Beijing on "
        "Wednesday after its top official was put under investigation, the "
        "city's official paper said. Chen Jining, the party secretary of "
        "China's financial hub and a member of the elite Politburo, was "
        "placed under investigation on Tuesday for \u201cserious violations of "
        "discipline and law\u201d."
    )
    y = para(d, lead_text, font(SANS, 17), M, y, 596, 22)
    draw_skyline(d, M + 616, body_top, 348, 120)
    d.text((M + 616, body_top + 126), "The Oriental Pearl Tower, Shanghai.",
           font=font(SANS, 13), fill=GREY)
    y = max(y, body_top + 146)
    rule(d, M, W - M, y + 6)

    # ---- second row: two stories ----
    y += 18
    col_w = (W - 2 * M - 28) // 2
    x2 = M + col_w + 28
    d.text((M, y), "TECHNOLOGY  ·  MARKETS", font=font(SANS_B, 16), fill=RED)
    d.text((x2, y), "UNITED STATES  ·  COURTS", font=font(SANS_B, 16), fill=RED)
    y += 24
    h1 = para(d, "HUANG: \u201cI MADE TERRIBLE MISTAKES\u201d",
              font(SERIF, 28), M, y, col_w, 34)
    h2 = para(d, "HUAWEI CONVICTED OF STEALING TRADE SECRETS",
              font(SERIF, 28), x2, y, col_w, 34)
    y = max(h1, h2) + 4
    body_y = y
    y = max(
        para(d, "Nvidia's chief says he is in therapy, a day after the board "
                "restored him. The rally faded fast: Nvidia slid 6% and the "
                "Nasdaq fell 1.5%.",
             font(SANS, 16), M, y, col_w - 168, 21),
        para(d, "A US jury convicted Huawei of stealing trade secrets on "
                "Tuesday, amid high tension between Washington and Beijing.",
             font(SANS, 16), x2, y, col_w - 168, 21),
    )
    draw_chip(d, M + col_w - 156, body_y, 156, 96)
    draw_scales(d, x2 + col_w - 156, body_y, 156, 96)
    y += 8
    rule(d, M, W - M, y)

    # ---- in brief ----
    y += 12
    d.text((M, y), "IN BRIEF", font=font(SERIF, 22), fill=INK)
    y += 30
    briefs = [
        ("CARTAGENA SIEGE", "Gunmen hold 25 hostage in a supermarket; five "
         "elderly women freed."),
        ("700,000 DEAD", "More than 700,000 Russian soldiers killed in "
         "Ukraine, a new analysis finds."),
        ("TURKEYS PARDONED", "President Trump pardons the Thanksgiving "
         "turkeys at the White House."),
        ("MEDAL FOR GIULIANI", "Trump awards Rudy Giuliani the Medal of "
         "Freedom, the top US civilian honour."),
        ("SHEIN PAYS $100M", "Shein to settle FTC claims of deceptive "
         "practices for $100 million."),
        ("RIYADH TOWER HIT", "Saudis condemn a \u201cterrorist attack\u201d after "
         "the PIF skyscraper is hit twice in a week."),
        ("SOLDIER ADMITS SPYING", "US soldier Jian Zhao admits selling "
         "military information to Chinese buyers."),
        ("SPORT", "England beat Australia by eight wickets to level the T20 "
         "series; Real Madrid thrashed PSV 5\u20131."),
    ]
    bx = [M, M + col_w + 28]
    by = [y, y]
    for i, (kick, text) in enumerate(briefs):
        col = i % 2
        x = bx[col]
        yy = by[col]
        d.text((x, yy), kick + " — ", font=font(SANS_B, 14), fill=INK)
        kw = d.textlength(kick + " — ", font=font(SANS_B, 14))
        by[col] = para(d, text, font(SANS, 14), x + kw, yy, col_w - kw, 18) + 5
    y = max(by) + 2
    rule(d, M, W - M, y, width=3)

    # ---- markets strip + footer ----
    y += 10
    d.text((M, y), "MARKETS", font=font(SANS_B, 16), fill=RED)
    d.text((M + 92, y), "Nasdaq \u22121.5%   ·   S&P 500 \u22120.5%   ·   Dow +0.9%   ·   "
                        "Nikkei 58,645   ·   Nvidia \u22126%",
           font=font(SANS, 16), fill=INK)
    y += 26
    d.text((W // 2, y), "THE WORLD TODAY  ·  Wednesday, 25 November 2026",
           font=font(SANS, 14), fill=GREY, anchor="ma")

    img.save(path, "PNG")
    return path


if __name__ == "__main__":
    import sys
    render(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
