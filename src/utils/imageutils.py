from typing import Tuple
from PIL import Image, ImageDraw


def create_video_overlay(dims: tuple, predict_x: float, predict_y: float,  y_intercept: float, x_intercept: float, slope: float, roll: float, pitch: float) -> Tuple:
    true_width = int(dims['w'] - dims['ml'] - dims['mr'])
    true_height = int(dims['h'] - dims['mt'] - dims['mb'])
    half_width = int(true_width / 2)
    half_height = int(true_height / 2)
    eye_height = 20
    eye_width = 20
    eye_line = 2
    img = Image.new('RGBA', [true_width, true_height], (0, 0, 0, 0))
    eye_pos_x = int(
        true_width * predict_x - (eye_width / 2))
    eye_pos_y = int(
        true_height * predict_y - (eye_height / 2))
    horizon_line_point_one = (3, int((0 * slope + y_intercept)*true_height))
    horizon_line_point_two = (
        true_width, (int((true_width * slope + y_intercept))))
    roll_line_point_one = (half_width, 3)
    roll_length = int((roll) / 90 * half_width)
    roll_line_point_two = (half_width + roll_length, 3)
    pitch_line_point_one = (3, half_height)
    pitch_length = ((-pitch) / 90 * half_height)
    pitch_line_point_two = (3, half_height + pitch_length)
    draw = ImageDraw.Draw(img)
    draw.ellipse((eye_pos_x, eye_pos_y, eye_pos_x + eye_width, eye_pos_y + eye_height),
                 fill=None, outline=(255, 155, 0), width=eye_line)
    draw.line((horizon_line_point_one, horizon_line_point_two),
              fill=(155, 255, 0), width=eye_line)
    draw.line((roll_line_point_one, roll_line_point_two),
              fill=(255, 255, 0), width=eye_line)
    draw.line((pitch_line_point_one, pitch_line_point_two),
              fill=(255, 255, 0), width=eye_line)
    return img, dims['ml'], dims['mt']
