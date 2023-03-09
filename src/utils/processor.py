from pathlib import Path

from modules.eyedb import EyeDB
from modules.regressor import Regression2dGazeModel
from modules.fusion import Fusion
from modules.analyze import HorizonGaze


def ingest_and_process(cb_progress, eyedb: EyeDB, paths: list[Path], type: str = 'zip', horizon_offset: float = 0.15, pitch_multi: float = 1.5) -> None:
    progress = 0.0
    cb_progress('Beginning to ingest data...', progress)
    runs_to_process = eyedb.ingest_data(paths, type)
    progress += 0.20
    cb_progress('Data ingested!', progress)
    max_run = len(runs_to_process)
    for index, runid in enumerate(runs_to_process):
        current_run = index + 1
        gaze_data = eyedb.get_gaze_data(runid)
        gaze_predictor = Regression2dGazeModel(gaze_data)
        progress += 0.20 / len(runs_to_process)
        cb_progress(
            f'Run {current_run} of {max_run}: Using magic to predict 2d gaze...', progress)
        predicted_gaze = gaze_predictor.get_predicted_2d()
        eyedb.write_pgaze2d_data(runid, predicted_gaze)
        imu_data = eyedb.get_imu_data(runid)
        mag_data = eyedb.get_mag_data(runid)
        progress += 0.20 / len(runs_to_process)
        cb_progress(
            f'Run {current_run} of {max_run}: Fusing imu and magnetometer data...', progress)
        fuser = Fusion(imu_data, mag_data)
        fuser.run()
        roll_offset = fuser.get_mean_roll()
        fuser.calc_horizon_line(roll_offset, pitch_multi)
        fused = fuser.get_results()
        progress += 0.20 / len(runs_to_process)
        cb_progress(
            f'Run {current_run} of {max_run}: Calculating predicted up/down...', progress)
        gaze3d = eyedb.get_gaze3d_z(runid)
        horizon = HorizonGaze(predicted_gaze, gaze3d, fused, horizon_offset)
        processed = horizon.calculates_all()
        progress += 0.20 / len(runs_to_process)
        cb_progress(
            f'Run {current_run} of {max_run}: Finishing up...', progress)
        eyedb.update_parameters(
            runid, 90 + roll_offset, pitch_multi, horizon_offset)
        eyedb.write_fusion_data(runid, fused)
        eyedb.write_process_date(runid)
        eyedb.write_processed_data(runid, processed)


def reprocess(cb_progress, eyedb: EyeDB, runids: list[int], roll_offset: int, pitch_multi: float, horizon_offset: float) -> None:
    progress = 0.0
    cb_progress('Beginning to reprocess data...', progress)
    max_run = len(runids)
    new_data = {}
    for runid in runids:
        new_data[runid] = {}
    for index, runid in enumerate(runids):
        current_run = index + 1
        imu_data = eyedb.get_imu_data(runid)
        mag_data = eyedb.get_mag_data(runid)
        progress += 0.50 / max_run
        cb_progress(
            f'Run {current_run} of {max_run}: Redoing calculations...', progress)
        fuser = Fusion(imu_data, mag_data)
        fuser.run()
        fuser.calc_horizon_line(roll_offset, pitch_multi)
        fused = fuser.get_results()
        for k, v in fused.items():
            new_data[runid][k] = v
        eyedb.update_parameters(
            runid, roll_offset=roll_offset, pitch_multi=pitch_multi, horizon_offset=horizon_offset)
        predicted_gaze = eyedb.get_pgazed2d_data(runid)
        gaze3d = eyedb.get_gaze3d_z(runid)
        horizon = HorizonGaze(predicted_gaze, gaze3d, fused, horizon_offset)
        processed = horizon.calculates_all()
        eyedb.update_processed_data(runid, processed)
    progress += 0.25
    cb_progress(
        f'Updating data in database...', progress)
    eyedb.update_fusion_data(new_data)
    eyedb.write_process_date(runid)
