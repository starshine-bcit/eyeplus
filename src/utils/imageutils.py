from typing import Tuple
from PIL import Image, ImageDraw


def create_eye_overlay(dims: tuple, predict_x: float, predict_y: float, prev_x: int, prev_y: int) -> Tuple:
    if dims['w'] >= 960 or dims['h'] >= 540:
        height = 35
        width = 35
        line = 3
    else:
        height = 20
        width = 20
        line = 2
    img = Image.new('RGBA', [30, 30], (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse(((0, 0), (height, width)), fill=None,
                 outline=(255, 155, 0), width=line)
    pos_x = int(
        (dims['w'] - dims['ml'] - dims['mr']) * predict_x + dims['ml'] - (width / 2))
    pos_y = int(
        (dims['h'] - dims['mt'] - dims['mb']) * predict_y + dims['mt'] - (height / 2))
    if ((prev_x - pos_x)**2 + (prev_y - pos_y)**2) <= (height / 2)**2:
        pos_x = prev_x
        pos_y = prev_y
    return img, pos_x, pos_y
