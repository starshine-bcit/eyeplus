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
