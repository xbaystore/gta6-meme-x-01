#!/usr/bin/env python3
"""Build the final gta6-meme-x-01 meme image.

Pipeline:
  1. Start from the generated base scene in ``assets/base.png`` — a tired
     gamer, a stuck download bar, and the make.fun ghost with his cash.
     The generated art intentionally contains no text and no logos.
  2. Composite the *official* make.fun mark (``assets/mark-1024.png``, the
     white ghost on its magenta disc, straight from make.fun's press kit)
     onto the blank laptop lid that faces the viewer in the scene, using
     the mark's own alpha channel, so the real brand reads as part of the
     room instead of a sticker pasted in a corner.
  3. Draw the caption in bold white type with a heavy black stroke,
     auto-fitted to 94% of the image width.

Outputs (both are written):
  - ``meme/meme.png`` next to this script's folder (the in-repo copy), and
  - ``/home/hatch/workspace/makefun/gta6-meme-x-01/meme-final.png``.

Run from the repository root:  ``python3 meme/make_meme.py``
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# --- Tunable compositing constants -------------------------------------------
# Centre of the laptop lid in the base scene, as fractions of image size.
# The lid occupies roughly x 0.235-0.635, y 0.625-0.910 of the frame.
MARK_CENTER_X = 0.435
MARK_CENTER_Y = 0.735
# Mark diameter as a fraction of image width. ~21% keeps the whole disc
# inside the lid (which spans roughly y 0.625-0.910) and clear of the
# bottom caption block, while staying big enough to read at a glance.
MARK_WIDTH_FRACTION = 0.21

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CAPTION_MAX_WIDTH_FRACTION = 0.94
TOP_MARGIN_FRACTION = 0.018
BOTTOM_MARGIN_FRACTION = 0.018
LINE_GAP_FRACTION = 0.012

TOP_TEXT = "WAITED 13 YEARS FOR GTA VI"
BOTTOM_TEXTS = ["MY AGENT ALREADY GOT PAID", "ON MAKE.FUN"]

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_PATH = SCRIPT_DIR / "assets" / "base.png"
MARK_PATH = SCRIPT_DIR / "assets" / "mark-1024.png"
REPO_OUTPUT_PATH = SCRIPT_DIR / "meme.png"
EXTERNAL_OUTPUT_PATH = Path(
    "/home/hatch/workspace/makefun/gta6-meme-x-01/meme-final.png"
)


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_width: int) -> ImageFont.FreeTypeFont:
    """Largest DejaVuSans-Bold size whose rendered width fits max_width."""
    size = 10
    while True:
        font = ImageFont.truetype(FONT_PATH, size + 2)
        stroke = max(1, (size + 2) // 12)
        bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
        if bbox[2] - bbox[0] > max_width:
            return ImageFont.truetype(FONT_PATH, size)
        size += 2


def draw_centered(
    draw: ImageDraw.ImageDraw,
    text: str,
    center_x: int,
    top_y: int,
    max_width: int,
    font: ImageFont.FreeTypeFont | None = None,
) -> int:
    """Draw one caption line centred at center_x; return its pixel height."""
    if font is None:
        font = fit_font(draw, text, max_width)
    stroke = max(2, font.size // 12)
    draw.text(
        (center_x, top_y),
        text,
        font=font,
        fill="white",
        stroke_width=stroke,
        stroke_fill="black",
        anchor="ma",  # middle-ascender: x is the centre, y is the top
    )
    ascent, descent = font.getmetrics()
    return ascent + descent


def main() -> None:
    base = Image.open(BASE_PATH).convert("RGBA")
    width, height = base.size

    # --- Paste the official mark onto the laptop lid -------------------------
    mark = Image.open(MARK_PATH).convert("RGBA")
    mark_size = int(width * MARK_WIDTH_FRACTION)
    mark = mark.resize((mark_size, mark_size), Image.LANCZOS)
    mark_x = int(width * MARK_CENTER_X - mark_size / 2)
    mark_y = int(height * MARK_CENTER_Y - mark_size / 2)
    base.alpha_composite(mark, dest=(mark_x, mark_y))

    # --- Captions -------------------------------------------------------------
    draw = ImageDraw.Draw(base)
    max_text_width = int(width * CAPTION_MAX_WIDTH_FRACTION)
    center_x = width // 2
    line_gap = int(height * LINE_GAP_FRACTION)

    top_y = int(height * TOP_MARGIN_FRACTION)
    draw_centered(draw, TOP_TEXT, center_x, top_y, max_text_width)

    # Bottom block: both lines share one font size, fitted to the longest
    # line, so the pair reads as a single caption. Measure first so the
    # block sits flush at the bottom margin.
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    shared_font = fit_font(probe, max(BOTTOM_TEXTS, key=len), max_text_width)
    ascent, descent = shared_font.getmetrics()
    line_height = ascent + descent
    block_height = line_height * len(BOTTOM_TEXTS) + line_gap * (len(BOTTOM_TEXTS) - 1)
    y = height - int(height * BOTTOM_MARGIN_FRACTION) - block_height
    for text in BOTTOM_TEXTS:
        draw_centered(draw, text, center_x, y, max_text_width, font=shared_font)
        y += line_height + line_gap

    # --- Save ------------------------------------------------------------------
    final = base.convert("RGB")
    final.save(REPO_OUTPUT_PATH)
    EXTERNAL_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    final.save(EXTERNAL_OUTPUT_PATH)
    print(f"wrote {REPO_OUTPUT_PATH} and {EXTERNAL_OUTPUT_PATH} ({width}x{height})")


if __name__ == "__main__":
    main()
