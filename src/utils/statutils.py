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
    roll = np.array([v['roll'] for v in fusion.values()])
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


def get_pitch_offset(fusion: dict) -> float:
    """Find average average roll throughout a run, in an attempt to provide a sane default value. Not used at this time, simply returns 0.

    Args:
        fusion (dict): All fusion data from the currently processing run.

    Returns:
        float: The calculated roll offset to store and use.
    """
    # roll_vals = [v['pitch'] for v in fusion.values()]
    # mean_pitch = np.mean(roll_vals)
    # return int(mean_pitch)
    return 0


def calc_horizon_line(fusion: dict, pitch_offset: int, pitch_multi: float) -> dict:
    """Determines the horizon line for each timestamp in the given fusion data.

    Args:
        fusion (dict): Processed sensor fusion data, including roll and pitch.
        roll_offset (int): Static roll offset to apply.
        pitch_multi (float): Static pitch multiplier to apply.

    Returns:
        dict: Returns original fusion data with the horizon line now included per timestamp.
    """
    for k, v in fusion.items():
        roll = v['roll']
        pitch = v['pitch'] - pitch_offset
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

        fov_constant = 0.40  # determined so that looking up 45 degrees would move the slope down 40 percent of the screen, and vice versa

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


def next_greatest_element(target: float, timestamps: list[float]) -> float:
    """Finds the next greatest timestamp in a sorted list, based on the target.

    Args:
        target (float): Timestamp of which we want to find the next greatest in list.
        timestamps (list[float]): Sorted list of timestamps to search through.

    Returns:
        float: The found timestamp, or the last one if input list if none was found.
    """
    idx = bisect.bisect_left(timestamps, target)
    if idx >= len(timestamps):
        return timestamps[-1]
    return timestamps[idx]
