from typing import Tuple
from PIL import Image, ImageDraw


def create_video_overlay(dims: tuple, predict_x: float, predict_y: float,  y_intercept: float, x_intercept: float, slope: float) -> Tuple:
    true_width = int(dims['w'] - dims['ml'] - dims['mr'])
    true_height = int(dims['h'] - dims['mt'] - dims['mb'])
    eye_height = 20
    eye_width = 20
    eye_line = 2
    img = Image.new('RGBA', [true_width, true_height], (0, 0, 0, 0))
    eye_pos_x = int(
        true_width * predict_x - (eye_width / 2))
    eye_pos_y = int(
        true_height * predict_y - (eye_height / 2))
    print(
        f'eye_pos_x : {eye_pos_x}, eye_pos_y: {eye_pos_y}, true_width: {true_width}, true_height: {true_height}')
    line_point_one = (0, int((0 * slope + y_intercept)*true_height))
    line_point_two = (
        true_width, (int((true_width * slope + y_intercept))))
    draw = ImageDraw.Draw(img)
    draw.ellipse((eye_pos_x, eye_pos_y, eye_pos_x + eye_width, eye_pos_y + eye_height),
                 fill=None, outline=(255, 155, 0), width=eye_line)
    draw.line((line_point_one, line_point_two),
              fill=(155, 255, 0), width=eye_line)
    return img, dims['ml'], dims['mt']
