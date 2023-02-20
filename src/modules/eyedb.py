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
        """EyeDB provides various methods, including the import of data from zip files
        or folders, to work with the sqlite database at that specified path. If the
        database does exist, it is automatically created, along with the requisite
        folders to store it and other data.

        Args:
            db_path (Path): Path to the (non)existant database to work with.
        """
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
        if not self._db_path.is_file():
            self._init_db()
        else:
            self._con = sqlite3.connect(self._db_path)
            self._cur = self._con.cursor()

    def ingest_data(self, paths: list[Path], type: str = 'zip') -> list[int]:
        """Takes a list of paths with with the type of 'zip' or 'dir' and imports them
        into the database

        Args:
            paths (list[Path]): List of path objects to process
            type (str, optional): Either 'zip' or 'dir'. Defaults to 'zip'.

        Raises:
            FileExistsError: If the data that the user is attempting to import already
            exists in the database

        Returns:
            list[int]: List of all the runids imported at once
        """

        # Create backup here

        run_query = '''INSERT INTO run
        (importdate, tags, video, hash, rolloffset, pitchmulti)
        VALUES(:importdate, :tags, :video, :hash, :rolloffset, :pitchmulti);'''

        imu_query = '''INSERT INTO imu
        (runid, timestamp, accelerometer0, accelerometer1,
         accelerometer2, gyroscope0, gyroscope1, gyroscope2)
        VALUES(:runid, :timestamp, :accelerometer0, :accelerometer1, :accelerometer2,:gyroscope0, :gyroscope1, :gyroscope2);'''

        gaze_query = '''INSERT INTO gaze
        (runid, timestamp, gaze2d0, gaze2d1, gaze3d0, gaze3d1, gaze3d2, leftorigin0, leftorigin1, leftorigin2, leftdirection0, leftdirection1,
         leftdirection2,  leftdiameter, rightorigin0, rightorigin1, rightorigin2, rightdirection0, rightdirection1, rightdirection2, rightdiameter)
        VALUES(:runid, :timestamp, :gaze2d0, :gaze2d1, :gaze3d0, :gaze3d1, :gaze3d2, :leftorigin0, :leftorigin1, :leftorigin2, :leftdirection0, :leftdirection1, :leftdirection2, :leftdiameter, :rightorigin0, :rightorigin1, :rightorigin2, :rightdirection0, :rightdirection1, :rightdirection2, :rightdiameter);'''

        mag_query = '''INSERT INTO mag
        (runid, timestamp, mag0, mag1, mag2)
        VALUES(:runid, :timestamp, :mag0, :mag1, :mag2);'''

        runs_ingested = []

        for item in paths:
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
            self._cur.execute('''SELECT hash FROM run''')
            hashes = self._cur.fetchall()
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
                'hash': hash,
                'rolloffset': 90,
                'pitchmulti': 1.0
            }

            self._cur.execute(run_query, run_data_to_import)
            self._con.commit()
            self._cur.execute(
                '''SELECT seq FROM sqlite_sequence WHERE name="run"''')
            res = self._cur.fetchone()
            runid = res[0]
            runs_ingested.append(runid)

            imu_data_list = []
            gaze_data_list = []
            mag_data_list = []

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
                elif 'magnetometer' in decoded['data']:
                    mag_data_list.append({
                        'runid': runid,
                        'timestamp': decoded['timestamp'],
                        'mag0': decoded['data']['magnetometer'][0],
                        'mag1': decoded['data']['magnetometer'][1],
                        'mag2': decoded['data']['magnetometer'][2],
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

            self._cur.executemany(imu_query, imu_data_list)
            self._cur.executemany(gaze_query, gaze_data_list)
            self._cur.executemany(mag_query, mag_data_list)

        self._con.commit()
        return runs_ingested

    def _init_db(self) -> None:
        """Creates the database and tables if it does not exist.
        """

        self._con = sqlite3.connect(self._db_path)
        self._cur = self._con.cursor()

        self._cur.execute('''CREATE TABLE IF NOT EXISTS run(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                importdate TEXT NOT NULL,
                processdate TEXT,
                video TEXT NOT NULL,
                hash TEXT NOT NULL,
                tags TEXT,
                rolloffset INTEGER NOT NULL,
                pitchmulti REAL NOT NULL);''')

        self._cur.execute('''CREATE TABLE IF NOT EXISTS gaze(
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

        self._cur.execute('''CREATE TABLE IF NOT EXISTS imu(
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

        self._cur.execute('''CREATE TABLE IF NOT EXISTS mag(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                runid INTEGER NOT NULL,
                timestamp REAL NOT NULL,
                mag0 REAL NOT NULL,
                mag1 REAL NOT NULL,
                mag2 REAL NOT NULL,
                FOREIGN KEY(runid) REFERENCES run(id));''')

        self._cur.execute('''CREATE TABLE IF NOT EXISTS pgaze2d(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                runid INTEGER NOT NULL,
                timestamp REAL NOT NULL,
                pgaze2dx REAL NOT NULL,
                pgaze2dy REAL NOT NULL,
                FOREIGN KEY(runid) REFERENCES run(id));''')

        self._cur.execute('''CREATE TABLE IF NOT EXISTS pgaze3d(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                runid INTEGER NOT NULL,
                timestamp REAL NOT NULL,
                pgaze3dx REAL NOT NULL,
                pgaze3dy REAL NOT NULL,
                pgaze3dz REAL NOT NULL,
                FOREIGN KEY(runid) REFERENCES run(id));''')

        self._cur.execute('''CREATE TABLE IF NOT EXISTS fusion(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                runid INTEGER NOT NULL,
                timestamp REAL NOT NULL,
                heading REAL NOT NULL,
                pitch REAL NOT NULL,
                roll REAL NOT NULL,
                q0 REAL NOT NULL,
                q1 REAL NOT NULL,
                q2 REAL NOT NULL,
                q3 REAL NOT NULL,
                yinter REAL NOT NULL,
                xinter REAL NOT NULL,
                slope REAL NOT NULL,
                FOREIGN KEY(runid) REFERENCES run(id));''')

        self._cur.execute('''CREATE INDEX idx_imu_id
                ON imu (id, runid);''')

        self._cur.execute('''CREATE INDEX idx_gaze_id
                ON gaze (id, runid);''')

        self._cur.execute('''CREATE INDEX idx_mag_id
                ON mag (id, runid);''')

        self._cur.execute('''CREATE INDEX idx_pgaze2d_id
                ON pgaze2d (id, runid);''')

        self._cur.execute('''CREATE INDEX idx_pgaze3d_id
                ON pgaze3d (id, runid);''')

        self._cur.execute('''CREATE INDEX idx_fusion_id
                ON fusion (id, runid);''')

        self._cur.execute('''CREATE INDEX idx_fusion_timestamp
                ON fusion (runid, timestamp);''')

        self._con.commit()

    def disconnect_db(self) -> None:
        """Closes the connection with database, allowing for a safe program exit.
        """
        self._cur.close()
        self._con.close()

    def get_all_runs(self) -> list[dict]:
        """Queries the database to find base data on all runs, including id.

        Returns:
            list[dict]: Information from the 'run' table that is deemed relevant.
        """
        self._cur.execute('''SELECT id, importdate, processdate, video, tags, rolloffset, pitchmulti
        FROM run;''')
        all_runs = self._cur.fetchall()
        ret_runs = []
        for run in all_runs:
            ret_runs.append({
                'id': run[0],
                'importdate': run[1],
                'processdate': run[2],
                'video': self._video_dir / run[3],
                'tags': run[4],
                'roll_offset': run[5],
                'pitch_multi': run[6]
            })
        return ret_runs

    def get_gaze_data(self, runid: int) -> dict:
        """Gets all relevant gaze data matching the runid

        Args:
            runid (int): id of the run from which we need data

        Raises:
            RuntimeError: If we are trying to select a non-existant id

        Returns:
            dict: Data loaded in a dict and ready for the other components
        """
        gaze_dict = {}
        self._cur.execute('''SELECT id FROM run WHERE id=(?);''', (runid,))
        res = self._cur.fetchall()
        if res:
            self._cur.execute(
                '''SELECT * FROM gaze WHERE runid=(?) ORDER BY id ASC;''', (runid,))
            imu_data = self._cur.fetchall()
            for line in imu_data:
                gaze_dict[line[2]] = {
                    'gaze2d': [line[3], line[4]],
                    'gaze3d': [line[5], line[6], line[7]],
                    'left': {
                        'origin': [line[8], line[9], line[10]],
                        'direction': [line[11], line[12], line[13]],
                        'diameter': line[14]
                    },
                    'right': {
                        'origin': [line[15], line[16], line[17]],
                        'direction': [line[18], line[19], line[20]],
                        'diameter': line[21]
                    }
                }
            return gaze_dict
        else:
            raise RuntimeError(f'Trying to select a non-existant ID: {runid}')

    def get_imu_data(self, runid: int) -> dict:
        """Gets all relevant imu data from the runid

        Args:
            runid (int): The run we wish to grab data from

        Raises:
            RuntimeError: If we are trying to select a nonexistant runid

        Returns:
            dict: imu data ready for the other components
        """
        imu_dict = {}
        self._cur.execute('''SELECT id FROM run WHERE id=(?);''', (runid,))
        res = self._cur.fetchall()
        if res:
            self._cur.execute(
                '''SELECT * FROM imu WHERE runid=(?) ORDER BY id ASC;''', (runid,))
            imu_data = self._cur.fetchall()
            for line in imu_data:
                imu_dict[line[2]] = {
                    'accelerometer': [line[3], line[4], line[5]],
                    'gyroscope': [line[6], line[7], line[8]]
                }
            return imu_dict
        else:
            raise RuntimeError(f'Trying to select a non-existant ID: {runid}')

    def get_mag_data(self, runid: int) -> dict:
        """Gets relevant mag data for the runid

        Args:
            runid (int): The runid of the data we wish to grab

        Raises:
            RuntimeError: If the runid does not exist

        Returns:
            dict: mag data formatted and ready for the other components
        """
        mag_dict = {}
        self._cur.execute('''SELECT id FROM run WHERE id=(?);''', (runid,))
        res = self._cur.fetchall()
        if res:
            self._cur.execute(
                '''SELECT * FROM imu where runid=(?) ORDER BY id ASC;''', (runid,))
            mag_data = self._cur.fetchall()
            for line in mag_data:
                mag_dict[line[2]] = {
                    'magnetometer': [line[3], line[4], line[5]]
                }
            return mag_dict
        else:
            raise RuntimeError(f'Trying to select a non-existant ID: {runid}')

    def write_pgaze2d_data(self, runid: int, pgaze: dict) -> None:
        """Writes out all predicted 2d gaze data to the database

        Args:
            runid (int): The runid of the data
            pgaze (dict): The data to ingest
        """
        pgaze_data = [{'runid': runid, 'timestamp': k,
                       'pgaze2dx': v[0], 'pgaze2dy': v[1]} for k, v in pgaze.items()]
        pgaze_insert_query = '''INSERT INTO pgaze2d
            (runid, timestamp, pgaze2dx, pgaze2dy)
            VALUES(:runid, :timestamp, :pgaze2dx, :pgaze2dy);'''
        self._cur.executemany(pgaze_insert_query, pgaze_data)
        self._con.commit()

    def get_pgazed2d_data(self, runid: int) -> None:
        """Gets all relevant predicted 2d gaze data for the runid

        Args:
            runid (int): The runid of the data we wish to grab

        Raises:
            RuntimeError: If the runid does not exist
        """
        pgaze_dict = {}
        self._cur.execute('''SELECT id FROM run WHERE id=(?);''', (runid,))
        res = self._cur.fetchall()
        if res:
            self._cur.execute(
                '''SELECT * FROM pgaze2d WHERE runid=(?) ORDER BY id ASC;''', (runid,))
            pgaze_data = self._cur.fetchall()
            for line in pgaze_data:
                pgaze_dict[line[2]] = [line[3], line[4]]
            return pgaze_dict
        else:
            raise RuntimeError(f'Trying to select a non-existant ID: {runid}')

    def write_pgaze3d_data(self, runid: int, pgaze: dict) -> None:
        """Writes out all predicted 3d gaze data to the database

        Args:
            runid (int): The runid of the data
            pgaze (dict): The data to ingest
        """
        pgaze_data = [{'runid': runid, 'timestamp': k,
                       'pgaze3dx': v[0], 'pgaze3dy': v[1], 'pgaze3dz': v[2]} for k, v in pgaze.items()]
        pgaze_insert_query = '''INSERT INTO pgaze3d
            (runid, timestamp, pgaze3dx, pgaze3dy, pgaze3dz)
            VALUES(:runid, :timestamp, :pgaze3dx, :pgaze3dy, :pgaze3dz);'''
        self._cur.executemany(pgaze_insert_query, pgaze_data)
        self._con.commit()

    def get_pgazed3d_data(self, runid: int) -> None:
        """Gets all relevant predicted 3d gaze data for the runid

        Args:
            runid (int): The runid of the data we wish to grab

        Raises:
            RuntimeError: If the runid does not exist
        """
        pgaze_dict = {}
        self._cur.execute('''SELECT id FROM run WHERE id=(?);''', (runid,))
        res = self._cur.fetchall()
        if res:
            self._cur.execute(
                '''SELECT * FROM pgaze3d WHERE runid=(?) ORDER BY id ASC;''', (runid,))
            pgaze_data = self._cur.fetchall()
            for line in pgaze_data:
                pgaze_dict[line[2]] = [line[3], line[4], line[5]]
            return pgaze_dict
        else:
            raise RuntimeError(f'Trying to select a non-existant ID: {runid}')

    def write_fusion_data(self, runid: int, fusion: dict) -> None:
        """Writes out all fusion data to the database for the runid

        Args:
            runid (int): runid of the processed data
            fusion (dict): The data to ingest
        """
        fusion_data = [{'runid': runid, 'timestamp': k, 'heading': v['heading'], 'pitch': v['pitch'], 'roll': v['roll'],
                        'q0': v['q'][0], 'q1': v['q'][1], 'q2': v['q'][2], 'q3': v['q'][3], 'yinter': v['y_intercept'], 'xinter': v['x_intercept'], 'slope': v['slope']} for k, v in fusion.items()]
        fusion_insert_query = '''INSERT INTO fusion
            (runid, timestamp, heading, pitch, roll, q0, q1, q2, q3, yinter, xinter, slope)
            VALUES(:runid, :timestamp, :heading, :pitch, :roll, :q0, :q1, :q2, :q3, :yinter, :xinter, :slope);'''
        self._cur.executemany(fusion_insert_query, fusion_data)
        self._con.commit()

    def get_fusion_data(self, runid: int) -> dict:
        """Gets all relevant fusion data for the runid

        Args:
            runid (int): runid of the data we want to grab

        Raises:
            RuntimeError: If the runid does not exist

        Returns:
            dict: fusion data ready for other components
        """
        fusion_dict = {}
        self._cur.execute('''SELECT id FROM run WHERE id=(?);''', (runid,))
        res = self._cur.fetchall()
        if res:
            self._cur.execute(
                '''SELECT * FROM fusion WHERE runid=(?) ORDER BY id ASC;''', (runid,))
            fusion_data = self._cur.fetchall()
            for line in fusion_data:
                fusion_dict[line[2]] = {
                    'heading': line[3],
                    'pitch': line[4],
                    'roll': line[5],
                    'q': (line[6], line[7], line[8], line[9]),
                    'y_intercept': line[10],
                    'x_intercept': line[11],
                    'slope': line[12]
                }
            return fusion_dict
        else:
            raise RuntimeError(f'Trying to select a non-existant ID: {runid}')

    def update_fusion_data(self, new_data: dict) -> None:
        """Updates already existing fusion data

        Args:
            new_data (dict): The data to update

        Raises:
            RuntimeError: If we try to update a non-existing runid
        """
        update_query = ('''UPDATE fusion
                        SET (heading, pitch, roll, q0, q1, q2, q3, yinter, xinter, slope) = (:heading, :pitch, :roll, :q0, :q1, :q2, :q3, :yinter, :xinter, :slope)
                        WHERE runid = (:runid) AND timestamp = (:timestamp);''')
        update_list = []
        for runid in new_data.keys():
            self._cur.execute('''SELECT id FROM run WHERE id=(?);''', (runid,))
            res = self._cur.fetchall()
            if not res:
                raise RuntimeError(
                    f'Trying to select a non-existant ID: {runid}')

        for k, v in new_data.items():
            for k2, v2 in v.items():
                update_list.append({
                    'heading': v2['heading'],
                    'pitch': v2['pitch'],
                    'roll': v2['roll'],
                    'q0': v2['q'][0],
                    'q1': v2['q'][1],
                    'q2': v2['q'][2],
                    'q3': v2['q'][3],
                    'yinter': v2['y_intercept'],
                    'xinter': v2['x_intercept'],
                    'slope': v2['slope'],
                    'runid': k,
                    'timestamp': k2
                })

        self._cur.executemany(update_query, update_list)
        self._con.commit()

    def update_parameters(self, runid: int, roll_offset: int, pitch_multi: float) -> None:
        self._cur.execute('''SELECT id FROM run WHERE id=(?);''', (runid,))
        res = self._cur.fetchall()
        if res:
            self._cur.execute('''UPDATE run
                            SET(rolloffset, pitchmulti) = (?, ?)
                            WHERE id=(?);''', (roll_offset, pitch_multi, runid))
        else:
            raise RuntimeError(f'Trying to select a non-existant ID: {runid}')

    def get_parameters(self, runid: int) -> tuple:
        self._cur.execute('''SELECT id FROM run WHERE id=(?);''', (runid,))
        res = self._cur.fetchall()
        if res:
            self._cur.execute('''SELECT rolloffset, pitchmulti
                            FROM run where id=(?);''', (runid,))
            parameters = self._cur.fetchone()
            return parameters
        else:
            raise RuntimeError(f'Trying to select a non-existant ID: {runid}')

    def write_process_date(self, runid: int) -> None:
        self._cur.execute('''UPDATE run SET(processdate)=(?)
                        WHERE id=(?);''', (str(datetime.now().date()), runid))
        self._con.commit()


if __name__ == '__main__':
    pass
