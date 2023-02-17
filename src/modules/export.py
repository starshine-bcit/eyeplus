import csv
from pathlib import Path
from datetime import datetime

from modules.eyedb import EyeDB


class DataExporter:
    def __init__(self, eyedb: EyeDB) -> None:
        """This object will grab data from the database and write out two csv
        files, one with the predicted 2d gaze data, the other with sensor fusion data,
        either for one run, or all runs.

        Args:
            eyedb (EyeDB): The database object to interact with.
        """
        self._db = eyedb

    def export_single(self, out_path: Path, runid: int) -> None:
        fused = self._db.get_fusion_data(runid)
        fused = [{'runid': runid, 'timestamp': k, 'heading': v['heading'], 'pitch': v['pitch'], 'roll': v['roll'],
                  'q0': v['q'][0], 'q1': v['q'][1], 'q2': v['q'][2], 'q3': v['q'][3], 'yinter': v['y_intercept'], 'xinter': v['x_intercept'], 'slope': v['slope']} for k, v in fused.items()]
        pgaze = self._db.get_pgazed2d_data(runid)
        pgaze = [{'runid': runid, 'timestamp': k,
                  'pgaze2dx': v[0], 'pgaze2dy': v[1]} for k, v in pgaze.items()]
        fused_out = out_path.with_name(f'{out_path.stem}_fusion.csv')
        pgaze_out = out_path.with_name(f'{out_path.stem}_pgaze.csv')
        with fused_out.open('w', encoding='utf8', newline='') as fo:
            csv_writer = csv.DictWriter(fo, fieldnames=list(fused[0].keys()))
            csv_writer.writeheader()
            csv_writer.writerows(fused)
        with pgaze_out.open('w', encoding='utf8', newline='') as fo:
            csv_writer = csv.DictWriter(fo, fieldnames=list(pgaze[0].keys()))
            csv_writer.writeheader()
            csv_writer.writerows(pgaze)

    def export_all(self, out_path: Path) -> None:
        all_runs = self._db.get_all_runs()
        for run in all_runs:
            now = datetime.now()
            base_name = out_path / f'id_{run["id"]}_{now.timestamp()}.csv'
            self.export_single(base_name, run['id'])
