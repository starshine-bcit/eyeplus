from pathlib import Path

from modules.eyedb import EyeDB
from modules.regressor import Regression2dGazeModel
from modules.fusion import Fusion
from modules.analyze import HorizonGaze
from utils.statutils import calc_horizon_line, get_pitch_offset, get_gaze_stats, get_fusion_stats


def ingest_and_process(cb_progress, eyedb: EyeDB, paths: list[Path], type: str = 'zip', horizon_offset: float = 0.0, pitch_multi: float = 1.0) -> None:
    """Master function which handles the ingesting and processing of input data.

    Args:
        cb_progress (function): Takes a (str, float) argument to display progress to user.
        eyedb (EyeDB): Instance of the database class used to store data.
        paths (list[Path]): List of Path object to attempt and process.
        type (str, optional): Type of input, either zip or dir. Defaults to 'zip'.
        horizon_offset (float, optional): Default horizon_offset to apply. Defaults to 0.13.
        pitch_multi (float, optional): Default pitch multiplier to apply. Defaults to 1.6.
    """
    progress = 0.0
    cb_progress('Beginning to ingest data...', progress)
    runs_to_process = eyedb.ingest_data(paths, type)
    progress += 0.10
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
            f'Run {current_run} of {max_run}: Fusing imu data...', progress)
        fuser = Fusion(imu_data, mag_data)
        fused = fuser.run()
        pitch_offset = get_pitch_offset(fused)
        fused = calc_horizon_line(fused, pitch_offset, pitch_multi)
        progress += 0.20 / len(runs_to_process)
        cb_progress(
            f'Run {current_run} of {max_run}: Calculating predicted up/down...', progress)
        gaze3d = eyedb.get_gaze3d_z(runid)
        horizon = HorizonGaze(predicted_gaze, gaze3d, fused, horizon_offset)
        processed = horizon.calculates_all()
        progress += 0.10 / len(runs_to_process)
        cb_progress(
            f'Run {current_run} of {max_run}: Calculating summary statistics...')
        gaze2d_stats = get_gaze_stats(predicted_gaze)
        fusion_stats = get_fusion_stats(fused)
        progress += 0.20 / len(runs_to_process)
        cb_progress(
            f'Run {current_run} of {max_run}: Writing to database...', progress)
        eyedb.update_parameters(
            runid, pitch_offset, pitch_multi, horizon_offset)
        eyedb.write_fusion_data(runid, fused)
        eyedb.write_process_date(runid)
        eyedb.write_processed_data(runid, processed)
        eyedb.write_summary_data(runid, fusion_stats, gaze2d_stats)


def reprocess(cb_progress, eyedb: EyeDB, runids: list[int], pitch_offset: int, pitch_multi: float, horizon_offset: float) -> None:
    """Master function which handles the reprocessing of data based on tweakable parameters.

    Args:
        cb_progress (function): Takes a (str, float) argument to display progress to user.
        eyedb (EyeDB): Instance of database class used to store data.
        runids (list[int]): List of runids to process.
        pitch_offset (int): User-provided pitch_offset.
        pitch_multi (float): User-provided pitch multiplier.
        horizon_offset (float): User-provided horizon offset.
    """
    progress = 0.0
    cb_progress('Beginning to reprocess data...', progress)
    max_run = len(runids)
    new_data = {}
    for runid in runids:
        new_data[runid] = {}
    for index, runid in enumerate(runids):
        current_run = index + 1
        fused = eyedb.get_raw_fusion_data(runid)
        progress += 0.50 / max_run
        cb_progress(
            f'Run {current_run} of {max_run}: Redoing calculations...', progress)
        fused = calc_horizon_line(fused, pitch_offset, pitch_multi)
        for k, v in fused.items():
            new_data[runid][k] = v
        eyedb.update_parameters(
            runid, pitch_offset=pitch_offset, pitch_multi=pitch_multi, horizon_offset=horizon_offset)
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
