from pathlib import Path

from modules.eyedb import EyeDB
from modules.regressor import Regression2dGazeModel
from modules.fusion import Fusion


def ingest_and_process(cb_progress, eyedb: EyeDB, paths: list[Path], type: str = 'zip') -> None:
    progress = 0.0
    cb_progress('Beginning to ingest data...', progress)
    runs_to_process = eyedb.ingest_data(paths, type)
    progress += 0.25
    cb_progress('Data ingested!', progress)
    max_run = len(runid)
    for index, runid in enumerate(runs_to_process):
        current_run = index + 1
        gaze_data = eyedb.get_gaze_data(runid)
        gaze_predictor = Regression2dGazeModel(gaze_data)
        progress += 0.25 / len(runs_to_process)
        cb_progress(
            f'Run {current_run} of {max_run}: Using magic to predict 2d gaze...', progress)
        predicted_gaze = gaze_predictor.get_predicted_2d()
        eyedb.write_pgaze2d_data(runid, predicted_gaze)
        imu_data = eyedb.get_imu_data(runid)
        mag_data = eyedb.get_mag_data(runid)
        progress += 0.25 / len(runs_to_process)
        cb_progress(
            f'Run {current_run} of {max_run}: Fusing imu and magnetometer data...', progress)
        fuser = Fusion(imu_data, mag_data)
        fused = fuser.run()
        progress += 0.25 / len(runs_to_process)
        cb_progress(
            f'Run {current_run} of {max_run}: Finishing up...', progress)
        eyedb.write_fusion_data(runid, fused)
