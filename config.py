from manim import *
import manimpango


BG = "#111111"
TEXT = "#ECEFF1"
MUTED = "#9AA3AA"
DIM = "#343A40"
ACCENT = "#00E5FF"
ACCENT_2 = "#F2C94C"
GREEN = "#27E08A"
RED = "#FF4081"
VIOLET = "#A78BFA"

ROW_H = 0.78
EQ_SCALE = 0.72


def _pick_font(*names: str) -> str:
    available = {font.lower(): font for font in manimpango.list_fonts()}
    for name in names:
        if name.lower() in available:
            return available[name.lower()]
    return names[-1]


FONT_TITLE = _pick_font("CMU Serif", "Times New Roman", "Georgia")
FONT_BODY = _pick_font("Segoe UI", "Arial")
FONT_SUBTITLE = _pick_font("Segoe UI", "Arial")
FONT_CODE = _pick_font("JetBrains Mono", "Cascadia Mono", "Consolas")

TITLE_SIZE = 44
SECTION_SIZE = 36
SUBTITLE_SIZE = 26
BODY_SIZE = 22
SMALL_SIZE = 18
EQ_SIZE = 34

FAST = 0.35
MED = 0.75
SLOW = 1.15

LEFT_COL_X = -4.9
TITLE_COL_X = -1.8
EQ_COL_X = 2.35

FRAME_W = 14.2
FRAME_H = 8.0
