from math import tan, radians
import bisect

import numpy as np


def get_gaze_stats(gaze2d: dict) -> dict:
    """Get mean, median, and stdev from gaze2d data.

    Args:
        gaze2d (dict): All 2d gaze data from selected run.

    Returns:
        dict: Compiled statistics, including total number of samples.
    """
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
    """Get mean, median, and stdev of pitch and roll from fusion data.

    Args:
        fusion (dict): All fusion data from selected run.

    Returns:
        dict: Compiled statistics, including number of samples.
    """
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
    """Find average average roll throughout a run, in an attempt to provide a sane default value.

    Args:
        fusion (dict): All fusion data from the currently processing run.

    Returns:
        float: The calculated roll offset to store and use.
    """
    roll_vals = [v['roll'] for v in fusion.values()]
    avg_roll = int((sum(roll_vals) / len(roll_vals)))
    roll_offset = -90 - avg_roll
    return roll_offset


def calc_horizon_line(fusion: dict, roll_offset: int, pitch_multi: float) -> dict:
    """Determines the horizon line for each timestamp in the given fusion data.

    Args:
        fusion (dict): Processed sensor fusion data, including roll and pitch.
        roll_offset (int): Static roll offset to apply.
        pitch_multi (float): Static pitch multiplier to apply.

    Returns:
        dict: Returns original fusion data with the horizon line now included per timestamp.
    """
    for k, v in fusion.items():
        roll = v['roll'] + roll_offset
        pitch = v['pitch'] * pitch_multi
        # calculate slope based off head tilt
        theta = roll
        # theta = roll + 90
        if theta != 90 or theta != -90:
            slope = tan(radians(theta))
        else:
            slope = float('inf')

        # calculate intercepts as percentage of screen based off head pitch and slope
        theta = -pitch

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


def next_greatest_element(target: float, timestamps: list[float]) -> float | None:
    idx = bisect.bisect_left(timestamps, target)
    if idx >= len(timestamps):
        return timestamps[-1]
    return timestamps[idx]
