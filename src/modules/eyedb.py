from pathlib import Path
from zipfile import ZipFile
import sqlite3
from datetime import date, datetime
import os
import shutil
import gzip
import json


class EyeDB():
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._data_dir = db_path.parent
        self._temp_dir = self._data_dir / '~temp'
        if not self._data_dir.exists():
            self._data_dir.mkdir()
        if not self._temp_dir.exists():
            self._temp_dir.mkdir()
        if not self._db_path.is_file():
            self._init_db()
        else:
            self._con = sqlite3.connect(self._db_path)

    def ingest_data(self, zip_files: list[Path]) -> None:
        # Create backup here

        cur = self._con.cursor()

        run_query = '''INSERT INTO run
        VALUES(:importdate, :tags);'''

        imu_query = '''INSERT INTO imu
        VALUES(:runid, :timestamp, :accelerometer0, :accelerometer1, :accelerometer2 :gyroscope0, :gyroscope1, :gyroscope2);'''

        gaze_query = ''''INTERT INTO gaze
        VALUES(:runid, :timestamp, :gaze2d0, :gaze2d1, :gaze3d0, :gaze3d1, :gaze3d2, :leftorigin0, :leftorigin1, :leftorigin2, :leftdiameter, :rightorigin0, :rightorigin1, :rightorigin2, :rightdirection0, :rightdirection1, :rightdirection2, :rightdiameter);'''

        for zip_file in zip_files:
            innertemp = self._temp_dir / str(datetime.now())
            innertemp.mkdir()
            participant_path = innertemp / 'meta' / 'participant'
            gaze_path = innertemp / 'gazedata.gz'
            imu_path = innertemp / 'imudata.gz'
            mod_time = date.fromtimestamp(gaze_path.stat().st_mtime)
            with ZipFile(zip_file, 'r') as zip:
                zip.extractall(innertemp)
            with gzip.open(gaze_path, 'r', encoding='utf8') as gz:
                gaze_data = gz.read()
            with gzip.open(imu_path, 'r', encoding='utf8') as gz:
                imu_data = gz.read()
            with participant_path.open('r', encoding='utf8') as fo:
                participant_data = json.load(fo)
            shutil.rmtree(innertemp)

            run_data_to_import = {
                'importdate': mod_time,
                'tags': participant_data['name'],
            }

            cur.execute(run_query, run_data_to_import)
            self._con.commit()
            cur.execute('''SELECT seq FROM sqlite_sequence WHERE name="run"''')
            res = cur.fetchone()
            runid = res[0]

            for line in imu_data.splitlines():
                decoded = json.loads(line)
                imu_data_to_insert = {
                    'runid': runid,
                    'timestamp': decoded['timestamp'],
                    'accelerometer0': decoded['data']['accelerometer'][0],
                    'accelerometer1': decoded['data']['accelerometer'][1],
                    'accelerometer2': decoded['data']['accelerometer'][2],
                    'gyroscope0': decoded['data']['gyroscope'][0],
                    'gyroscope1': decoded['data']['gyroscope'][1],
                    'gyroscope2': decoded['data']['gyroscope'][2],
                }

            for line in gaze_data.splitlines():
                decoded = json.loads(line)
                if len(decoded['data']) == 0:
                    decoded['data'] = {
                        'gaze2d': [None, None],
                        'gaze3d': [None, None, None],
                        'eyeleft': {},
                        'eyeright': {},
                    }
                if len(decoded['data']['eyeleft']) == 0:
                    decoded['data']['eyeleft'] = {
                        'gazeorigin': [None, None, None],
                        'gazedirection': [None, None, None],
                        'pupildiameter': None
                    }
                if len(decoded['data']['eyeright']) == 0:
                    decoded['data']['eyeright'] = {
                        'gazeorigin': [None, None, None],
                        'gazedirection': [None, None, None],
                        'pupildiameter': None
                    }

                gaze_data_to_insert = {
                    'runid': runid,
                    'timestamp': decoded['timestamp'],
                    'gaze2d0': decoded['data']['gaze2d'][0],
                    'gaze2d1': decoded['data']['gaze2d'][1],
                    'gaze3d0': decoded['data']['gaze3d'][0],
                    'gaze3d1': decoded['data']['gaze3d'][1],
                    'gaze3d2': decoded['data']['gaze3d'][2],
                    'leftorigin0': decoded['data']['eyeleft']['gazeorigin'][0],
                    'leftorigin1': decoded['data']['eyeleft']['gazeorigin'][1],
                    'leftorigin2': decoded['data']['eyeleft']['gazeorigin'][2],
                    'leftdirection0': decoded['data']['eyeleft']['gazedirection'][0],
                    'leftdirection1': decoded['data']['eyeleft']['gazedirection'][1],
                    'leftdirection2': decoded['data']['eyeleft']['gazedirection'][2],
                    'leftdiameter': decoded['data']['eyeleft']['pupildiameter'],
                    'rightorigin0': decoded['data']['eyeright']['gazeorigin'][0],
                    'rightorigin1': decoded['data']['eyeright']['gazeorigin'][1],
                    'rightorigin2': decoded['data']['eyeright']['gazeorigin'][2],
                    'rightdirection0': decoded['data']['eyeright']['gazeorigin'][0],
                    'rightdirection1': decoded['data']['eyeright']['gazeorigin'][1],
                    'rightdirection2': decoded['data']['eyeright']['gazeorigin'][2],
                    'rightdiameter': decoded['data']['eyeright']['pupildiameter']
                }

                cur.execute(imu_query, imu_data_to_insert)
                cur.execute(gaze_query, gaze_data_to_insert)

        self._con.commit()

    def _init_db(self) -> None:
        self._con = sqlite3.connect(self._db_path)
        cur = self._con.cursor()
        cur.execute('''CREATE TABLE run(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                importdate TEXT NOT NULL,
                processdate TEXT,
                tags TEXT;)''')

        cur.execute('''CREATE TABLE gaze(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                runid INTEGER NOT NULL,
                timestamp REAL NOT NULL,
                gaze2d0 REAL,
                gaze2d1 REAL,
                gaze3d0 REAL,
                gaze3d1 REAL,
                gaze3d2 REAL,
                leftorigin0 REAL,
                leftorigin1 REAL,
                leftorigin2 REAL,
                leftdirection0 REAL,
                leftdirection1 REAL,
                leftdirection2 REAL,
                leftdiameter REAL,
                rightorigin0 REAL,
                rightorigin1 REAL,
                rightorigin2 REAL,
                rightdirection0 REAL,
                rightdirection1 REAL,
                rightdirection2 REAL,
                rightdiameter REAL,
                FOREIGN KEY(runid) REFERENCES run(id));''')

        cur.execute('''CREATE TABLE imu
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                runid INTEGER NOT NULL,
                timestamp REAL NOT NULL,
                accelerometer0 REAL NOT NULL,
                accelerometer1 REAL NOT NULL,
                accelerometer2 REAL NOT NULL,
                gyroscope0 REAL NOT NULL,
                gyroscope1 REAL NOT NULL,
                gyroscope2 REAL NOT NULL,
                FOREIGN KEY(runid) REFERENCES run(id));''')

        cur.execute('''CREATE TABLE processed
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                runid INTEGER NOT NULL,
                FOREIGN KEY(runid) REFERENCES run(id));''')

        self._con.commit()

    def disconnect_db(self) -> None:
        self._con.close()


if __name__ == '__main__':
    eyedb = EyeDB(Path(__file__).parent.parent.parent / 'data' / 'eye.db')
    eyedb.ingest_data(
        [Path('C:\\Courses\\3900\\sample_data\\OneDrive_1_1-23-2023.zip')])
