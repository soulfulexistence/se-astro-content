"""
Soulful Existence Graphic Generator
Generates branded social media graphics using Pillow.
Brand: Dark academia / cottage witch aesthetic
Colors: Deep Night bg, Gold Mid accent, Parchment text
Font: Cormorant Garamond (falls back to DejaVu Serif)
"""

import os
import textwrap
import base64
from io import BytesIO

try:
    from PIL import Image, ImageDraw, ImageFont
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

# ── Brand colors ──────────────────────────────────────────────────────────────
BG_COLOR       = (14, 13, 11)     # #0e0d0b Deep Night
GOLD_MID       = (184, 154, 92)   # #b89a5c Gold Mid — rules, eyebrow
PARCHMENT      = (232, 223, 200)  # #e8dfc8 Parchment — display text
TEXT_MUTED     = (200, 188, 164)  # #c8bca4 Text Muted — handle, date

# ── Font paths ────────────────────────────────────────────────────────────────
# Railway container: install via apt or download to /data/.hermes/fonts/
FONT_PATHS = {
    "italic": [
        "/data/.hermes/fonts/CormorantGaramond-LightItalic.ttf",
        "/data/.hermes/fonts/CormorantGaramond-Italic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerifCondensed-Italic.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    ],
    "light": [
        "/data/.hermes/fonts/CormorantGaramond-Light.ttf",
        "/data/.hermes/fonts/CormorantGaramond-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerifCondensed.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    ],
}

def get_font(style, size):
    for path in FONT_PATHS.get(style, FONT_PATHS["light"]):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def letter_space(text, spacing=3):
    """Add letter spacing by inserting thin spaces."""
    return (" " * spacing).join(text)

def draw_se_graphic(
    event_name: str,
    pull_quote: str,
    post_date: str,
    handle: str = "@soulfulxistence",
    width: int = 1080,
    height: int = 1080,
) -> str:
    """
    Generate a branded SE social media graphic.
    Returns base64-encoded PNG string.
    """
    if not PILLOW_AVAILABLE:
        return ""

    W, H = width, height
    MARGIN = 88

    img = Image.new("RGB", (W, H), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # ── Top gold rule ────────────────────────────────────────────────────────
    rule_top_y = 108
    draw.line([(MARGIN, rule_top_y), (W - MARGIN, rule_top_y)], fill=GOLD_MID, width=1)

    # ── Eyebrow — event name (uppercase, spaced, gold) ───────────────────────
    font_eyebrow = get_font("light", 26)
    eyebrow = letter_space(event_name.upper(), 3)
    bbox = draw.textbbox((0, 0), eyebrow, font=font_eyebrow)
    ew = bbox[2] - bbox[0]
    draw.text(((W - ew) / 2, rule_top_y + 44), eyebrow, font=font_eyebrow, fill=GOLD_MID)

    # ── Pull quote — italic display, centered ────────────────────────────────
    # Choose font size based on quote length
    if len(pull_quote) < 40:
        display_size = 82
        wrap_width = 20
        line_height = 96
    elif len(pull_quote) < 70:
        display_size = 68
        wrap_width = 24
        line_height = 82
    else:
        display_size = 56
        wrap_width = 28
        line_height = 70

    font_display = get_font("italic", display_size)
    wrapped = textwrap.fill(pull_quote, width=wrap_width)
    lines = wrapped.split("\n")

    total_h = len(lines) * line_height
    quote_start_y = (H / 2) - (total_h / 2) + 20

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_display)
        lw = bbox[2] - bbox[0]
        draw.text(((W - lw) / 2, quote_start_y + i * line_height), line, font=font_display, fill=PARCHMENT)

    # ── Bottom gold rule ─────────────────────────────────────────────────────
    rule_bot_y = H - 148
    draw.line([(MARGIN, rule_bot_y), (W - MARGIN, rule_bot_y)], fill=GOLD_MID, width=1)

    # ── Date (left) and handle (right) ───────────────────────────────────────
    font_small = get_font("light", 22)

    draw.text((MARGIN, rule_bot_y + 28), post_date, font=font_small, fill=TEXT_MUTED)

    handle_bbox = draw.textbbox((0, 0), handle, font=font_small)
    hw = handle_bbox[2] - handle_bbox[0]
    draw.text((W - MARGIN - hw, rule_bot_y + 28), handle, font=font_small, fill=TEXT_MUTED)

    # ── Export as base64 ─────────────────────────────────────────────────────
    buffer = BytesIO()
    img.save(buffer, format="PNG", optimize=True)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


def save_graphic(
    event_name: str,
    pull_quote: str,
    post_date: str,
    handle: str = "@soulfulxistence",
    output_path: str = "/tmp/se_graphic.png",
) -> str:
    """Generate and save graphic to file. Returns file path."""
    if not PILLOW_AVAILABLE:
        return ""

    W, H = 1080, 1080
    MARGIN = 88

    img = Image.new("RGB", (W, H), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    rule_top_y = 108
    draw.line([(MARGIN, rule_top_y), (W - MARGIN, rule_top_y)], fill=GOLD_MID, width=1)

    font_eyebrow = get_font("light", 26)
    eyebrow = letter_space(event_name.upper(), 3)
    bbox = draw.textbbox((0, 0), eyebrow, font=font_eyebrow)
    ew = bbox[2] - bbox[0]
    draw.text(((W - ew) / 2, rule_top_y + 44), eyebrow, font=font_eyebrow, fill=GOLD_MID)

    if len(pull_quote) < 40:
        display_size, wrap_width, line_height = 82, 20, 96
    elif len(pull_quote) < 70:
        display_size, wrap_width, line_height = 68, 24, 82
    else:
        display_size, wrap_width, line_height = 56, 28, 70

    font_display = get_font("italic", display_size)
    wrapped = textwrap.fill(pull_quote, width=wrap_width)
    lines = wrapped.split("\n")
    total_h = len(lines) * line_height
    quote_start_y = (H / 2) - (total_h / 2) + 20

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_display)
        lw = bbox[2] - bbox[0]
        draw.text(((W - lw) / 2, quote_start_y + i * line_height), line, font=font_display, fill=PARCHMENT)

    rule_bot_y = H - 148
    draw.line([(MARGIN, rule_bot_y), (W - MARGIN, rule_bot_y)], fill=GOLD_MID, width=1)

    font_small = get_font("light", 22)
    draw.text((MARGIN, rule_bot_y + 28), post_date, font=font_small, fill=TEXT_MUTED)
    handle_bbox = draw.textbbox((0, 0), handle, font=font_small)
    hw = handle_bbox[2] - handle_bbox[0]
    draw.text((W - MARGIN - hw, rule_bot_y + 28), handle, font=font_small, fill=TEXT_MUTED)

    img.save(output_path, "PNG", optimize=True)
    return output_path


if __name__ == "__main__":
    # Test
    path = save_graphic(
        event_name="Venus enters Leo",
        pull_quote="The sky gives you the weather. Your birth chart tells you what to wear.",
        post_date="June 13, 2026",
        output_path="/tmp/se_test.png"
    )
    print(f"Saved to {path}")
