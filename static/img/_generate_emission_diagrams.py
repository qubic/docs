"""Generate the diagrams for docs/learn/emission-mechanism.md.

Outputs BOTH light and dark variants of each diagram so the doc can use
ThemedImage for theme-aware rendering (same pattern as
_generate_upgrading_diagrams.py).

Files:
  emission-multi-epoch-light.png / -dark.png
  emission-sequential-deduction-light.png / -dark.png
  emission-swatch-begin-epoch-light.png / -dark.png
  emission-supply-watch-phase2-light.png / -dark.png

Run: python3 _generate_emission_diagrams.py
"""
from PIL import Image, ImageDraw, ImageFont

# Colored accents used across both themes — same values as
# _generate_upgrading_diagrams for visual consistency.
BLUE   = (0x7B, 0xB3, 0xE0)
GREEN  = (0x3D, 0xBB, 0x6A)
GOLD   = (0xF5, 0xB2, 0x3B)
PURPLE = (0x9C, 0x78, 0xD8)
RED    = (0xE5, 0x68, 0x6A)
WHITE  = (0xFF, 0xFF, 0xFF)


def theme_colors(mode):
    if mode == "light":
        return {
            "bg":        (0xFF, 0xFF, 0xFF),
            "text":      (0x1B, 0x28, 0x39),
            "text_sub":  (0x6C, 0x7A, 0x89),
            "card":      (0xE9, 0xED, 0xF1),
            "border":    (0x1B, 0x28, 0x39),
            "arrow":     (0x1B, 0x28, 0x39),
            "arrow_sub": (0x6C, 0x7A, 0x89),
            "red":       (0xE5, 0x68, 0x6A),
        }
    if mode == "dark":
        return {
            "bg":        (0x1B, 0x1B, 0x1D),
            "text":      (0xFF, 0xFF, 0xFF),
            "text_sub":  (0xBD, 0xBF, 0xC6),
            "card":      (0x2A, 0x2A, 0x2D),
            "border":    (0xBD, 0xBF, 0xC6),
            "arrow":     (0xBD, 0xBF, 0xC6),
            "arrow_sub": (0x8A, 0x8D, 0x96),
            "red":       (0xFF, 0x69, 0x61),
        }
    raise ValueError(f"unknown theme mode: {mode}")


FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_BLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_ITL = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
FONT_MNO = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"


def f(size, weight="reg"):
    return ImageFont.truetype(
        {"reg": FONT_REG, "bld": FONT_BLD, "itl": FONT_ITL, "mno": FONT_MNO}[weight], size)


def text_center(d, cx, cy, text, font, fill):
    bbox = d.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    d.text((cx - w // 2, cy - h // 2 - bbox[1]), text, font=font, fill=fill)


def rounded_box(d, xy, radius=10, fill=BLUE, outline=None, width=0):
    d.rounded_rectangle(xy, radius=radius, fill=fill,
                        outline=outline, width=width)


def arrow(d, x1, y1, x2, y2, color, width=3, head=12):
    d.line([(x1, y1), (x2, y2)], fill=color, width=width)
    if x2 > x1 and y1 == y2:
        d.polygon([(x2, y2),
                   (x2 - head, y2 - head // 2),
                   (x2 - head, y2 + head // 2)], fill=color)
    elif y2 > y1 and x1 == x2:
        d.polygon([(x2, y2),
                   (x2 - head // 2, y2 - head),
                   (x2 + head // 2, y2 - head)], fill=color)


# ─── 1. Multi-epoch flow ─────────────────────────────────────────────────────

def multi_epoch_flow(mode):
    """Multi-epoch view: mining → election → work → payment.

    Restored from an earlier version — it's the compact big-picture story
    of how computor life spans two epochs. Used in the doc as a
    stage-setter, not as an illustration of the per-epoch endEpoch() flow.
    """
    c = theme_colors(mode)
    W, H = 1200, 460
    img = Image.new("RGB", (W, H), c["bg"])
    d = ImageDraw.Draw(img)

    d.text((60, 30), "Mining, election, and revenue span two epochs",
           font=f(28, "bld"), fill=c["text"])
    d.text((60, 68),
           "UPoW scores accumulated in one epoch decide who is seated as a computor in the next.",
           font=f(15, "reg"), fill=c["text_sub"])

    # Epoch boundary dashed line
    def dashed_vline(x, y0, y1, color, dash=8, width=3):
        y = y0
        while y < y1:
            d.line([(x, y), (x, min(y + dash, y1))], fill=color, width=width)
            y += dash * 2

    epoch_x = W // 2
    dashed_vline(epoch_x, 140, 340, GOLD, dash=8)
    d.text((epoch_x - 60, 350), "Epoch boundary",
           font=f(15, "bld"), fill=GOLD)

    # Epoch column headers — offset from the boundary so text doesn't touch it
    d.text((110, 145), "Epoch N", font=f(19, "bld"), fill=c["text"])
    d.text((110, 173), "UPoW mining accumulates scores per pubkey",
           font=f(13, "reg"), fill=c["text_sub"])
    d.text((epoch_x + 70, 145), "Epoch N+1", font=f(19, "bld"), fill=c["text"])
    d.text((epoch_x + 70, 173),
           "top 676 UPoW scorers from epoch N are seated as computors",
           font=f(13, "reg"), fill=c["text_sub"])

    # 4 numbered steps — evenly spaced, text stacked vertically below each badge.
    step_data = [
        (200,  "1", "Mine",       "UPoW scores accumulate per pubkey",    BLUE),
        (450,  "2", "Elect",      "top 676 seated for next epoch",         GREEN),
        (750,  "3", "Validate",   "seated computors mine + validate ticks", BLUE),
        (1000, "4", "Distribute", "revenue paid, cuts applied",             GOLD),
    ]
    badge_y = 240
    for x, num, label, sub, color in step_data:
        d.ellipse([x - 20, badge_y - 20, x + 20, badge_y + 20], fill=color)
        text_center(d, x, badge_y, num, f(18, "bld"), WHITE)
        text_center(d, x, badge_y + 45, label, f(17, "bld"), c["text"])
        text_center(d, x, badge_y + 70, sub, f(13, "reg"), c["text_sub"])

    # Bottom explanatory line
    d.text((60, 400),
           "Steps 3 and 4 happen inside every epoch. The per-epoch details are unpacked in the next section.",
           font=f(13, "itl"), fill=c["text_sub"])

    img.save(f"emission-multi-epoch-{mode}.png", "PNG")
    print(f"wrote emission-multi-epoch-{mode}.png")


# ─── 2. Sequential deduction ─────────────────────────────────────────────────

def sequential_deduction(mode):
    c = theme_colors(mode)
    W, H = 1200, 500
    img = Image.new("RGB", (W, H), c["bg"])
    d = ImageDraw.Draw(img)

    d.text((60, 30), "Sequential deduction — the routing table applied per computor",
           font=f(24, "bld"), fill=c["text"])
    d.text((60, 66),
           "Each entry takes its fraction of what remains after previous entries, not of gross.",
           font=f(14, "reg"), fill=c["text_sub"])

    # Full-width bar showing splits
    bar_x0 = 60
    bar_x1 = W - 60
    bar_y = 130
    bar_h = 90
    bar_w = bar_x1 - bar_x0

    # Illustrative fractions (matching the tweet card):
    # burn ~77.5% of gross, CCF ~1.8% of gross, QEARN ~2.5% of gross, computor ~18.2% of gross
    # after applying compounding.
    segments = [
        (0.775,  RED,    "Burn destination"),
        (0.018,  GOLD,   "CCF"),
        (0.025,  PURPLE, "QEARN"),
        (0.182,  GREEN,  "Computor keeps"),
    ]

    x = bar_x0
    for share, color, label in segments:
        w = int(bar_w * share)
        rounded_box(d, (x, bar_y, x + w, bar_y + bar_h), radius=6, fill=color)
        if w > 90:
            font_size = 15 if w > 200 else 12
            text_center(d, x + w // 2, bar_y + bar_h // 2,
                        label, f(font_size, "bld"), WHITE)
        elif w > 40:
            text_center(d, x + w // 2, bar_y + bar_h // 2,
                        f"{share * 100:.1f}%", f(11, "bld"), WHITE)
        x += w

    # % callouts below
    y = bar_y + bar_h + 26
    d.text((60, y), "Applied in order — each entry cuts a fraction of what remains:",
           font=f(15, "bld"), fill=c["text"])

    # Numbered steps
    steps = [
        "77.5% of revenue → burn destination",
        "8% of the remainder → CCF fee reserve",
        "12.25% of the remainder → QEARN",
        "what's left → the computor",
    ]
    y += 30
    for i, s in enumerate(steps, 1):
        d.text((60, y), f"{i}. {s}", font=f(14, "reg"), fill=c["text"])
        y += 24

    y += 12
    d.text((60, y),
           "Result: computor keeps ~18% of their base revenue for that epoch.",
           font=f(14, "itl"), fill=c["text_sub"])

    img.save(f"emission-sequential-deduction-{mode}.png", "PNG")
    print(f"wrote emission-sequential-deduction-{mode}.png")


# ─── 3. SWATCH BEGIN_EPOCH mechanism ─────────────────────────────────────────

def swatch_begin_epoch(mode):
    c = theme_colors(mode)
    W, H = 1200, 500
    img = Image.new("RGB", (W, H), c["bg"])
    d = ImageDraw.Draw(img)

    d.text((60, 30), "SWATCH — what runs at every BEGIN_EPOCH",
           font=f(24, "bld"), fill=c["text"])
    d.text((60, 66),
           "One hook. Reads balances, tops up fee reserves, burns the remainder — all burns.",
           font=f(14, "reg"), fill=c["text_sub"])

    # Left: incoming balance
    box_h = 70
    box_w = 260
    d.text((70, 130), "Incoming balance", font=f(15, "bld"), fill=c["text_sub"])
    rounded_box(d, (60, 155, 60 + box_w, 155 + box_h),
                radius=10, fill=BLUE)
    text_center(d, 60 + box_w // 2, 155 + box_h // 2,
                "SWATCH balance", f(17, "bld"), WHITE)
    d.text((60, 240),
           "routed to SWATCH via the donation table",
           font=f(12, "itl"), fill=c["text_sub"])

    # Right: 4 outcome boxes (all burns)
    outcomes_x = 500
    outcomes_w = 640
    d.text((outcomes_x, 130), "All four outcomes remove QU from circulating supply:",
           font=f(15, "bld"), fill=c["text"])

    box_data = [
        ("GQMPROP fee reserve", "topped up if under target — QU burned",         GOLD),
        ("SWATCH fee reserve",  "topped up if under target — QU burned",         BLUE),
        ("CCF fee reserve",     "topped up if under target — QU burned",         PURPLE),
        ("qpi.burn(remainder)", "any balance left over is split and burned",     RED),
    ]
    box_h2 = 56
    gap = 8
    y = 155
    for i, (label, sub, color) in enumerate(box_data):
        rounded_box(d, (outcomes_x, y, outcomes_x + outcomes_w, y + box_h2),
                    radius=8, fill=color)
        d.text((outcomes_x + 16, y + 10), label,
               font=f(15, "bld"), fill=WHITE)
        d.text((outcomes_x + 16, y + 32), sub,
               font=f(12, "reg"), fill=WHITE)
        y += box_h2 + gap

    # Arrow from incoming → outcomes
    arrow_y = 155 + box_h // 2
    arrow(d, 60 + box_w + 10, arrow_y, outcomes_x - 10, arrow_y,
          color=c["arrow"], width=3)

    # Bottom note
    d.text((60, 420),
           "Contract fee reserves are burn destinations — QU sent there are destroyed, not held.",
           font=f(14, "bld"), fill=c["red"])
    d.text((60, 444),
           "The reserve is an accounting slot for that contract's execution costs.",
           font=f(13, "reg"), fill=c["text_sub"])

    img.save(f"emission-swatch-begin-epoch-{mode}.png", "PNG")
    print(f"wrote emission-swatch-begin-epoch-{mode}.png")


# ─── 4. Phase 2 stacked bar ──────────────────────────────────────────────────

def supply_watch_phase2(mode):
    c = theme_colors(mode)
    W, H = 1200, 460
    img = Image.new("RGB", (W, H), c["bg"])
    d = ImageDraw.Draw(img)

    d.text((60, 30), "Phase 2 — Supply Watch: adaptive burn contribution",
           font=f(24, "bld"), fill=c["text"])
    d.text((60, 66),
           "Same emission-schedule target. SWATCH burns less as other ecosystem burns pick up.",
           font=f(14, "reg"), fill=c["text_sub"])

    # Target line above the bar
    d.text((60, 130),
           "Target burn per epoch (emission schedule) — same regardless of mix",
           font=f(14, "bld"), fill=c["text"])

    # Stacked bar
    bar_x0 = 60
    bar_x1 = W - 60
    bar_y = 175
    bar_h = 80
    bar_w = bar_x1 - bar_x0

    # Illustrative Phase 2 mix
    segments = [
        (0.68, RED,    "SWATCH",  "adjusts down"),
        (0.18, GOLD,   "SC IPO",  "burns already happening"),
        (0.08, BLUE,   "Dust",    "spectrum-fill triggers"),
        (0.06, PURPLE, "Other",   "programs, misc"),
    ]

    x = bar_x0
    for share, color, label, sub in segments:
        w = int(bar_w * share)
        rounded_box(d, (x, bar_y, x + w, bar_y + bar_h), radius=6, fill=color)
        if w > 120:
            text_center(d, x + w // 2, bar_y + bar_h // 2 - 8,
                        label, f(17, "bld"), WHITE)
            text_center(d, x + w // 2, bar_y + bar_h // 2 + 14,
                        sub, f(12, "reg"), WHITE)
        elif w > 60:
            text_center(d, x + w // 2, bar_y + bar_h // 2,
                        label, f(14, "bld"), WHITE)
        x += w

    # Contrast with Phase 1 (small comparison note)
    y = bar_y + bar_h + 30
    d.text((60, y),
           "Compared to Phase 1 (today): SWATCH burns 100% of what it receives,",
           font=f(14, "reg"), fill=c["text"])
    y += 22
    d.text((60, y),
           "regardless of what other burns are contributing that epoch.",
           font=f(14, "reg"), fill=c["text"])

    y += 40
    d.text((60, y),
           "In Phase 2, SWATCH reads the ecosystem's other burn events and shrinks",
           font=f(14, "bld"), fill=c["red"])
    y += 22
    d.text((60, y),
           "its own contribution so the network's total burn stays on schedule.",
           font=f(14, "bld"), fill=c["red"])

    img.save(f"emission-supply-watch-phase2-{mode}.png", "PNG")
    print(f"wrote emission-supply-watch-phase2-{mode}.png")


# ─── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    for mode in ("light", "dark"):
        multi_epoch_flow(mode)
        sequential_deduction(mode)
        swatch_begin_epoch(mode)
        supply_watch_phase2(mode)
