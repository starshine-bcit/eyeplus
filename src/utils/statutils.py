from math import tan, radians

import numpy as np


def get_gaze_stats(gaze2d: dict) -> dict:
    gaze_stats = {}
    vals = np.array(list(gaze2d.values())).transpose()
    gaze_stats['x'] = {
        'mean': np.mean(vals[0]),
        'median': np.median(vals[0]),
        'stdev': np.std(vals[0])
    }
    gaze_stats['y'] = {
        'mean': np.mean(vals[1]),
        'median': np.median(vals[1]),
        'stdev': np.std(vals[1])
    }
    gaze_stats['num_samples'] = len(gaze2d)
    return gaze_stats


def get_fusion_stats(fusion: dict) -> dict:
    fusion_stats = {}
    pitch = np.array([v['pitch'] for v in fusion.values()])
    roll = np.array([v['roll'] + 90 for v in fusion.values()])
    fusion_stats['pitch'] = {
        'mean': np.mean(pitch),
        'median': np.median(pitch),
        'stdev': np.std(pitch)
    }
    fusion_stats['roll'] = {
        'mean': np.mean(roll),
        'median': np.median(roll),
        'stdev': np.std(roll)
    }
    fusion_stats['num_samples'] = len(fusion)
    return fusion_stats


def get_roll_offset(fusion: dict) -> float:
    roll_vals = [v['roll'] for v in fusion.values()]
    avg_roll = int((sum(roll_vals) / len(roll_vals)))
    roll_offset = -90 - avg_roll
    return roll_offset


def calc_horizon_line(fusion: dict, roll_offset: int, pitch_multi: float) -> dict:
    for k, v in fusion.items():
        roll = v['roll'] + roll_offset
        pitch = v['pitch'] * pitch_multi
        # calculate slope based off head tilt
        theta = roll + 90
        if theta != 90 or theta != -90:
            slope = tan(radians(theta))
        else:
            slope = float('inf')

        # calculate intercepts as percentage of screen based off head pitch and slope
        theta = pitch

        fov_constant = 0.40  # determined so that looking up 45 degrees would move the slope down 25 percent of the screen, and vice versa

        if theta >= 0:
            y_intercept = 0.5 - tan(radians(theta))*fov_constant
        elif theta < 0:
            theta = -theta
            y_intercept = 0.5 + tan(radians(theta))*fov_constant

        x_intercept = -y_intercept / slope

        fusion[k]['y_intercept'] = y_intercept
        fusion[k]['x_intercept'] = x_intercept
        fusion[k]['slope'] = slope

    return fusion
