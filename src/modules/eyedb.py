from pathlib import Path
from zipfile import ZipFile
import sqlite3
from datetime import date, datetime
import shutil
import gzip
import json
from hashlib import file_digest


class EyeDB():
    def __init__(self, db_path: Path) -> None:
        self._data_dir = db_path.parent
        self._temp_dir = self._data_dir / '~temp'
        self._video_dir = self._data_dir / 'videos'
        self._db_path = db_path
        if not self._data_dir.exists():
            self._data_dir.mkdir()
        if not self._temp_dir.exists():
            self._temp_dir.mkdir()
        if not self._video_dir.is_dir():
            self._video_dir.mkdir()
        if self._db_path.is_file():
            self._con = sqlite3.connect(self._db_path)
        else:
            self._init_db()

    def ingest_data(self, files: list[Path], type: str = 'zip') -> None:
        # Create backup here

        cur = self._con.cursor()

        run_query = '''INSERT INTO run
        (importdate, tags, video, hash)
        VALUES(:importdate, :tags, :video, :hash);'''

        imu_query = '''INSERT INTO imu
        (runid, timestamp, accelerometer0, accelerometer1, accelerometer2, gyroscope0, gyroscope1, gyroscope2) 
        VALUES(:runid, :timestamp, :accelerometer0, :accelerometer1, :accelerometer2,:gyroscope0, :gyroscope1, :gyroscope2);'''

        gaze_query = '''INSERT INTO gaze
        (runid, timestamp, gaze2d0, gaze2d1, gaze3d0, gaze3d1, gaze3d2, leftorigin0, leftorigin1, leftorigin2, leftdirection0, leftdirection1, leftdirection2,  leftdiameter, rightorigin0, rightorigin1, rightorigin2, rightdirection0, rightdirection1, rightdirection2, rightdiameter) 
        VALUES(:runid, :timestamp, :gaze2d0, :gaze2d1, :gaze3d0, :gaze3d1, :gaze3d2, :leftorigin0, :leftorigin1, :leftorigin2, :leftdirection0, :leftdirection1, :leftdirection2, :leftdiameter, :rightorigin0, :rightorigin1, :rightorigin2, :rightdirection0, :rightdirection1, :rightdirection2, :rightdiameter);'''

        for item in files:
            now = datetime.now().timestamp()
            mod_time = date.fromtimestamp(item.stat().st_mtime)

            if type == 'zip':
                innertemp = self._temp_dir / str(now)
                innertemp.mkdir()
                participant_path = innertemp / 'meta' / 'participant'
                gaze_path = innertemp / 'gazedata.gz'
                imu_path = innertemp / 'imudata.gz'
                video_path = innertemp / 'scenevideo.mp4'
                with ZipFile(item, 'r') as zip:
                    zip.extractall(innertemp)
            elif type == 'dir':
                participant_path = item / 'meta' / 'participant'
                gaze_path = item / 'gazedata.gz'
                imu_path = item / 'imudata.gz'
                video_path = item / 'scenevideo.mp4'

            with imu_path.open('rb') as fo:
                hash = file_digest(fo, 'sha256').hexdigest()
            cur.execute('''SELECT hash FROM run''')
            hashes = cur.fetchall()
            for db_hash in hashes:
                if db_hash[0] == hash:
                    if type == 'zip':
                        shutil.rmtree(innertemp)
                    raise FileExistsError(
                        'The data you are attempting to import already exists')

            with gzip.open(gaze_path, 'r') as gz:
                gaze_data = gz.read()
                gaze_data = gaze_data.decode('utf8')
            with gzip.open(imu_path, 'r') as gz:
                imu_data = gz.read()
                imu_data = imu_data.decode('utf8')
            with participant_path.open('r') as fo:
                participant_data = json.load(fo)

            new_video_name = f'{now}.mp4'
            new_video_path = self._video_dir / f'{now}.mp4'
            shutil.copyfile(video_path, new_video_path)

            if type == 'zip':
                shutil.rmtree(innertemp)

            run_data_to_import = {
                'importdate': mod_time,
                'tags': participant_data['name'],
                'video': new_video_name,
                'hash': hash
            }

            cur.execute(run_query, run_data_to_import)
            self._con.commit()
            cur.execute('''SELECT seq FROM sqlite_sequence WHERE name="run"''')
            res = cur.fetchone()
            runid = res[0]

            imu_data_list = []
            gaze_data_list = []

            for line in imu_data.splitlines():
                decoded = json.loads(line)
                if 'accelerometer' in decoded['data']:
                    imu_data_list.append({
                        'runid': runid,
                        'timestamp': decoded['timestamp'],
                        'accelerometer0': decoded['data']['accelerometer'][0],
                        'accelerometer1': decoded['data']['accelerometer'][1],
                        'accelerometer2': decoded['data']['accelerometer'][2],
                        'gyroscope0': decoded['data']['gyroscope'][0],
                        'gyroscope1': decoded['data']['gyroscope'][1],
                        'gyroscope2': decoded['data']['gyroscope'][2],
                    })

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

                gaze_data_list.append({
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
                    'rightdirection0': decoded['data']['eyeright']['gazedirection'][0],
                    'rightdirection1': decoded['data']['eyeright']['gazedirection'][1],
                    'rightdirection2': decoded['data']['eyeright']['gazedirection'][2],
                    'rightdiameter': decoded['data']['eyeright']['pupildiameter']
                })

            cur.executemany(imu_query, imu_data_list)
            cur.executemany(gaze_query, gaze_data_list)

        self._con.commit()

    def _init_db(self) -> None:
        self._con = sqlite3.connect(self._db_path)
        cur = self._con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS run(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                importdate TEXT NOT NULL,
                processdate TEXT,
                video TEXT NOT NULL,
                hash TEXT NOT NULL,
                tags TEXT);''')

        cur.execute('''CREATE TABLE IF NOT EXISTS gaze(
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

        cur.execute('''CREATE TABLE IF NOT EXISTS imu(
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

        cur.execute('''CREATE TABLE IF NOT EXISTS processed(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                runid INTEGER NOT NULL,
                FOREIGN KEY(runid) REFERENCES run(id));''')

        self._con.commit()

    def disconnect_db(self) -> None:
        self._con.close()

    def get_all_runs(self) -> list[dict]:
        cur = self._con.cursor()
        cur.execute('''SELECT id, importdate, processdate, video, tags
        FROM run;''')
        all_runs = cur.fetchall()
        ret_runs = []
        for run in all_runs:
            ret_runs.append({
                'id': run[0],
                'importdate': run[1],
                'processdate': run[2],
                'video': self._video_dir / run[3],
                'tags': run[4]
            })
        return ret_runs


if __name__ == '__main__':
    pass
