"""Generate the three diagrams for docs/computors/upgrading.md.

Outputs BOTH light and dark variants of each diagram so the doc can
use ThemedImage for automatic theme switching. Dark variant matches
the Docusaurus dark default (#1B1B1D bg, #FFF headings, #BDBFC6 body).

Files:
  upgrading-tick-continuity-light.png / -dark.png
  upgrading-decision-flow-light.png   / -dark.png
  upgrading-tick-vote-light.png       / -dark.png

Run: python3 _generate_upgrading_diagrams.py
Outputs to the current directory (should be /home/claude/qubic-docs/static/img/).
"""
from PIL import Image, ImageDraw, ImageFont

# Colored accent boxes stay identical across themes (still readable on both)
BLUE  = (0x7B, 0xB3, 0xE0)
GREEN = (0x3D, 0xBB, 0x6A)
GOLD  = (0xF5, 0xB2, 0x3B)
WHITE = (0xFF, 0xFF, 0xFF)

# Theme-dependent colors — pulled from theme_colors()
def theme_colors(mode):
    if mode == "light":
        return {
            "bg":        (0xFF, 0xFF, 0xFF),
            "text":      (0x1B, 0x28, 0x39),  # DARK — headings + primary text
            "text_sub":  (0x6C, 0x7A, 0x89),  # GRAY — secondary text
            "card":      (0xE9, 0xED, 0xF1),  # LIGHT — question / neutral fills
            "border":    (0x1B, 0x28, 0x39),  # DARK
            "arrow":     (0x1B, 0x28, 0x39),  # DARK
            "arrow_sub": (0x6C, 0x7A, 0x89),  # GRAY
            "red":       (0xE5, 0x68, 0x6A),
            "on_dark_pill": (0x1B, 0x28, 0x39),  # DARK — for the "Tick finalizes" pill
        }
    if mode == "dark":
        return {
            "bg":        (0x1B, 0x1B, 0x1D),  # Docusaurus dark default
            "text":      (0xFF, 0xFF, 0xFF),  # site heading color
            "text_sub":  (0xBD, 0xBF, 0xC6),  # site body color in dark mode
            "card":      (0x2A, 0x2A, 0x2D),  # slightly-lighter dark surface
            "border":    (0xBD, 0xBF, 0xC6),
            "arrow":     (0xBD, 0xBF, 0xC6),
            "arrow_sub": (0x8A, 0x8D, 0x96),
            "red":       (0xFF, 0x69, 0x61),  # site --code-highlighter-red
            "on_dark_pill": (0x0A, 0x0A, 0x0C),  # even darker than bg for pill contrast
        }
    raise ValueError(f"unknown theme mode: {mode}")


FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_BLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_MNO = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"


def f(size, weight="reg"):
    return ImageFont.truetype(
        {"reg": FONT_REG, "bld": FONT_BLD, "mno": FONT_MNO}[weight], size)


def text_center(d, cxpos, cypos, text, font, fill):
    bbox = d.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    d.text((cxpos - w // 2, cypos - h // 2 - bbox[1]), text, font=font, fill=fill)


def rounded_box(d, xy, radius=10, fill=BLUE, outline=None):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline,
                        width=2 if outline else 0)


def arrow(d, x1, y1, x2, y2, color, width=3, head=12):
    d.line([(x1, y1), (x2, y2)], fill=color, width=width)
    if x2 > x1 and y1 == y2:
        d.polygon([(x2, y2), (x2 - head, y2 - head // 2),
                   (x2 - head, y2 + head // 2)], fill=color)
    elif y2 > y1 and x1 == x2:
        d.polygon([(x2, y2), (x2 - head // 2, y2 - head),
                   (x2 + head // 2, y2 - head)], fill=color)


# ─── Diagram 1: tick continuity ──────────────────────────────────────────────

def tick_continuity(mode):
    c = theme_colors(mode)
    W, H = 1200, 640
    img = Image.new("RGB", (W, H), c["bg"])
    d = ImageDraw.Draw(img)

    d.text((60, 30), "Tick continuity across the epoch boundary",
           font=f(30, "bld"), fill=c["text"])

    def dashed_vline(x, y0, y1, color=GOLD, dash=8):
        y = y0
        while y < y1:
            d.line([(x, y), (x, min(y + dash, y1))], fill=color, width=3)
            y += dash * 2

    epoch_x = W // 2
    # Boundary line in two segments so it doesn't cross the GAP label zone
    dashed_vline(epoch_x, 95, 458)
    dashed_vline(epoch_x, 510, H - 60)
    d.text((epoch_x - 65, H - 45), "Epoch boundary",
           font=f(16, "bld"), fill=GOLD)
    d.text((epoch_x - 60, H - 25), "(Wed 12:00 UTC)",
           font=f(13, "reg"), fill=c["text_sub"])

    y_seam = 170
    d.text((60, y_seam - 55), "SEAMLESS", font=f(22, "bld"), fill=GREEN)
    d.text((60, y_seam - 28), "Tick numbers continue sequentially — no gap",
           font=f(15, "reg"), fill=c["text_sub"])

    tick_w, tick_h, gap = 92, 60, 10
    labels_left = ["N-3", "N-2", "N-1", "N"]
    labels_right = ["N+1", "N+2", "N+3", "N+4"]
    for i, label in enumerate(labels_left):
        x0 = epoch_x - (len(labels_left) - i) * (tick_w + gap) + gap // 2
        rounded_box(d, (x0, y_seam, x0 + tick_w, y_seam + tick_h),
                    radius=8, fill=BLUE)
        text_center(d, x0 + tick_w // 2, y_seam + tick_h // 2, label,
                    f(18, "bld"), fill=WHITE)
    for i, label in enumerate(labels_right):
        x0 = epoch_x + i * (tick_w + gap) + gap // 2
        rounded_box(d, (x0, y_seam, x0 + tick_w, y_seam + tick_h),
                    radius=8, fill=GREEN)
        text_center(d, x0 + tick_w // 2, y_seam + tick_h // 2, label,
                    f(18, "bld"), fill=WHITE)

    left_edge = epoch_x - (tick_w + gap) + tick_w + gap // 2
    right_edge = epoch_x + gap // 2
    d.line([(left_edge, y_seam + tick_h // 2), (right_edge, y_seam + tick_h // 2)],
           fill=GREEN, width=4)

    y_non = 400
    d.text((60, y_non - 55), "COORDINATED CUTOVER",
           font=f(22, "bld"), fill=c["red"])
    d.text((60, y_non - 28), "Tick-number gap while all nodes re-sync",
           font=f(15, "reg"), fill=c["text_sub"])

    labels_left2 = ["N-3", "N-2", "N-1", "N"]
    labels_right2 = ["M", "M+1", "M+2", "M+3"]
    for i, label in enumerate(labels_left2):
        x0 = epoch_x - (len(labels_left2) - i) * (tick_w + gap) + gap // 2
        rounded_box(d, (x0, y_non, x0 + tick_w, y_non + tick_h),
                    radius=8, fill=BLUE)
        text_center(d, x0 + tick_w // 2, y_non + tick_h // 2, label,
                    f(18, "bld"), fill=WHITE)
    for i, label in enumerate(labels_right2):
        x0 = epoch_x + i * (tick_w + gap) + gap // 2
        rounded_box(d, (x0, y_non, x0 + tick_w, y_non + tick_h),
                    radius=8, fill=GOLD)
        text_center(d, x0 + tick_w // 2, y_non + tick_h // 2, label,
                    f(18, "bld"), fill=WHITE)

    left_edge = epoch_x - (tick_w + gap) + tick_w + gap // 2
    right_edge = epoch_x + gap // 2
    for i in range(left_edge, right_edge, 12):
        d.line([(i, y_non + tick_h // 2), (min(i + 6, right_edge), y_non + tick_h // 2)],
               fill=c["red"], width=4)
    mid = (left_edge + right_edge) // 2
    d.text((mid - 22, y_non + tick_h + 6), "GAP",
           font=f(14, "bld"), fill=c["red"])
    d.text((mid - 90, y_non + tick_h + 25), "nodes re-sync · M > N+1",
           font=f(12, "reg"), fill=c["text_sub"])

    img.save(f"upgrading-tick-continuity-{mode}.png", "PNG")
    print(f"wrote upgrading-tick-continuity-{mode}.png")


# ─── Diagram 2: decision flow ────────────────────────────────────────────────

def decision_flow(mode):
    c = theme_colors(mode)
    W, H = 1200, 640
    img = Image.new("RGB", (W, H), c["bg"])
    d = ImageDraw.Draw(img)

    d.text((60, 30), "Upgrade decision flow",
           font=f(30, "bld"), fill=c["text"])
    d.text((60, 68), "Which transition mode is required?",
           font=f(16, "reg"), fill=c["text_sub"])

    q_x, q_w, q_h = 100, 480, 80
    out_x, out_w, out_h = 700, 400, 70

    y_q1 = 150
    y_q2 = 330
    y_out3 = 510

    questions = [
        "1. Does the change affect any tick-vote digest?",
        "2. Can the switch point be gate-guarded (epoch or tick)?",
    ]

    # Q1
    rounded_box(d, (q_x, y_q1, q_x + q_w, y_q1 + q_h),
                radius=10, fill=c["card"], outline=c["border"])
    text_center(d, q_x + q_w // 2, y_q1 + q_h // 2, questions[0],
                f(17, "bld"), fill=c["text"])

    # Q1 NO → Seamless A
    out1_y = y_q1 + (q_h - out_h) // 2
    rounded_box(d, (out_x, out1_y, out_x + out_w, out1_y + out_h),
                radius=10, fill=GREEN)
    text_center(d, out_x + out_w // 2, out1_y + 22, "SEAMLESS — Path A",
                f(16, "bld"), fill=WHITE)
    text_center(d, out_x + out_w // 2, out1_y + 48,
                "deploy any time · no coordination needed",
                f(13, "reg"), fill=WHITE)
    arrow(d, q_x + q_w + 5, y_q1 + q_h // 2, out_x - 5, y_q1 + q_h // 2,
          color=c["arrow"], width=3)
    d.text((q_x + q_w + 20, y_q1 + q_h // 2 - 26), "NO",
           font=f(14, "bld"), fill=c["text"])

    # Q1 YES → Q2
    arrow(d, q_x + q_w // 2, y_q1 + q_h + 4,
          q_x + q_w // 2, y_q2 - 4, color=c["arrow"], width=2, head=10)
    d.text((q_x + q_w // 2 + 15, y_q1 + q_h + 30), "YES",
           font=f(14, "bld"), fill=c["text"])

    # Q2
    rounded_box(d, (q_x, y_q2, q_x + q_w, y_q2 + q_h),
                radius=10, fill=c["card"], outline=c["border"])
    text_center(d, q_x + q_w // 2, y_q2 + q_h // 2, questions[1],
                f(17, "bld"), fill=c["text"])

    # Q2 YES → Seamless B
    out2_y = y_q2 + (q_h - out_h) // 2
    rounded_box(d, (out_x, out2_y, out_x + out_w, out2_y + out_h),
                radius=10, fill=GREEN)
    text_center(d, out_x + out_w // 2, out2_y + 22, "SEAMLESS — Path B",
                f(16, "bld"), fill=WHITE)
    text_center(d, out_x + out_w // 2, out2_y + 48,
                "deploy in advance · all nodes flip at gate",
                f(13, "reg"), fill=WHITE)
    arrow(d, q_x + q_w + 5, y_q2 + q_h // 2, out_x - 5, y_q2 + q_h // 2,
          color=c["arrow"], width=3)
    d.text((q_x + q_w + 20, y_q2 + q_h // 2 - 26), "YES",
           font=f(14, "bld"), fill=c["text"])

    # Q2 NO → down to Coord Restart terminal outcome
    arrow(d, q_x + q_w // 2, y_q2 + q_h + 4,
          q_x + q_w // 2, y_out3 - 4, color=c["arrow"], width=2, head=10)
    d.text((q_x + q_w // 2 + 15, y_q2 + q_h + 30), "NO",
           font=f(14, "bld"), fill=c["text"])

    # Coord Restart — spans both cols
    coord_x, coord_w = q_x, q_w + (out_x - q_x - q_w) + out_w
    rounded_box(d, (coord_x, y_out3, coord_x + coord_w, y_out3 + out_h),
                radius=10, fill=c["red"])
    text_center(d, coord_x + coord_w // 2, y_out3 + 22, "COORDINATED RESTART",
                f(16, "bld"), fill=WHITE)
    text_center(d, coord_x + coord_w // 2, y_out3 + 48,
                "X or Y version bump · Wed 12:00 UTC · every node sets START_NETWORK_FROM_SCRATCH=1",
                f(13, "reg"), fill=WHITE)

    d.text((60, H - 55), "Priority: network safety > transition smoothness",
           font=f(15, "bld"), fill=c["text"])
    d.text((60, H - 32), "A coordinated restart is not a failure mode — it is the correct pattern when no gate can cover the change.",
           font=f(12, "reg"), fill=c["text_sub"])

    img.save(f"upgrading-decision-flow-{mode}.png", "PNG")
    print(f"wrote upgrading-decision-flow-{mode}.png")


# ─── Diagram 3: tick vote structure ──────────────────────────────────────────

def tick_vote(mode):
    c = theme_colors(mode)
    W, H = 1200, 600
    img = Image.new("RGB", (W, H), c["bg"])
    d = ImageDraw.Draw(img)

    d.text((60, 30), "Tick vote — what every computor signs",
           font=f(30, "bld"), fill=c["text"])
    d.text((60, 68), "5 digest fields must match byte-for-byte across ≥451 of 676 votes",
           font=f(16, "reg"), fill=c["text_sub"])

    digests = [
        ("spectrum digest",    "balances (Merkle root)"),
        ("universe digest",    "assets (Merkle root)"),
        ("computer digest",    "smart-contract state (Merkle root)"),
        ("transaction digest", "TickData hash"),
        ("timestamp",          "network-agreed tick timestamp"),
    ]

    box_x, box_w, box_h = 60, 400, 60
    box_gap = 14
    y_start = 130
    for i, (name, sub) in enumerate(digests):
        y = y_start + i * (box_h + box_gap)
        rounded_box(d, (box_x, y, box_x + box_w, y + box_h),
                    radius=8, fill=BLUE)
        d.text((box_x + 18, y + 10), name, font=f(17, "bld"), fill=WHITE)
        d.text((box_x + 18, y + 34), sub, font=f(13, "reg"), fill=WHITE)

    center_x, center_y = 720, 300
    cw, ch = 220, 100
    rounded_box(d, (center_x - cw // 2, center_y - ch // 2,
                    center_x + cw // 2, center_y + ch // 2),
                radius=12, fill=GOLD)
    text_center(d, center_x, center_y - 6, "TICK VOTE",
                f(22, "bld"), fill=WHITE)
    text_center(d, center_x, center_y + 20, "signed",
                f(13, "reg"), fill=WHITE)

    for i in range(len(digests)):
        y = y_start + i * (box_h + box_gap) + box_h // 2
        arrow(d, box_x + box_w + 5, y,
              center_x - cw // 2 - 5, center_y,
              color=c["arrow_sub"], width=2, head=10)

    right_x = 980
    rounded_box(d, (right_x, 140, right_x + 170, 200),
                radius=8, fill=c["card"], outline=c["border"])
    text_center(d, right_x + 85, 170, "676 computors",
                f(15, "bld"), fill=c["text"])
    text_center(d, right_x + 85, 189, "sign a vote",
                f(12, "reg"), fill=c["text_sub"])

    arrow(d, right_x + 85, 205, right_x + 85, 245, color=c["arrow"], width=2, head=10)

    rounded_box(d, (right_x, 250, right_x + 170, 320),
                radius=8, fill=GREEN)
    text_center(d, right_x + 85, 275, "≥451 must match",
                f(15, "bld"), fill=WHITE)
    text_center(d, right_x + 85, 296, "byte-for-byte",
                f(12, "reg"), fill=WHITE)

    arrow(d, right_x + 85, 325, right_x + 85, 365, color=c["arrow"], width=2, head=10)

    rounded_box(d, (right_x, 370, right_x + 170, 430),
                radius=8, fill=c["on_dark_pill"])
    text_center(d, right_x + 85, 400, "Tick finalizes",
                f(15, "bld"), fill=WHITE)

    warn_y = 500
    d.text((60, warn_y), "If any node computes ANY digest differently → its vote doesn't align.",
           font=f(15, "bld"), fill=c["red"])
    d.text((60, warn_y + 26), "This is why any consensus-touching code change requires all nodes to activate the new logic together.",
           font=f(13, "reg"), fill=c["text_sub"])

    img.save(f"upgrading-tick-vote-{mode}.png", "PNG")
    print(f"wrote upgrading-tick-vote-{mode}.png")


if __name__ == "__main__":
    for mode in ("light", "dark"):
        tick_continuity(mode)
        decision_flow(mode)
        tick_vote(mode)
