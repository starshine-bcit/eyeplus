from pathlib import Path
from zipfile import ZipFile
import sqlite3
from datetime import date, datetime
import shutil
import gzip
import json
from hashlib import file_digest
from typing import Tuple


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
        (importdate, tags, video, hash, pitchoffset, pitchmulti, horizonoffset, start, end)
        VALUES(:importdate, :tags, :video, :hash, :pitchoffset, :pitchmulti, :horizonoffset, :start, :end);'''

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
                    # removed at request from sponsor
                    pass
                    # if type == 'zip':
                    #     shutil.rmtree(innertemp)
                    # raise FileExistsError(
                    #     'The data you are attempting to import already exists')

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
                'pitchoffset': 0,
                'pitchmulti': 1.0,
                'horizonoffset': 0.0,
                'start': -1,
                'end': -1
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
                pitchoffset INTEGER NOT NULL,
                pitchmulti REAL NOT NULL,
                horizonoffset REAL NOT NULL,
                start INT NOT NULL,
                end INT NOT NULL);''')

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

        self._cur.execute('''CREATE TABLE IF NOT EXISTS processed(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                runid INTEGER NOT NULL,
                timestamp REAL NOT NULL,
                totalcount INTEGER NOT NULL,
                upcount INTEGER NOT NULL,
                downcount INTEGER NOT NULL,
                percentup REAL NOT NULL,
                percentdown REAL NOT NULL,
                currentup INTEGER NOT NULL,
                FOREIGN KEY(runid) REFERENCES run(id));''')

        self._cur.execute('''CREATE TABLE IF NOT EXISTS summary(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                runid INTEGER NOT NULL,
                pitchmean REAL NOT NULL,
                pitchmedian REAL NOT NULL,
                pitchstdev REAL NOT NULL,
                rollmean REAL NOT NULL,
                rollmedian REAL NOT NULL,
                rollstdev REAL NOT NULL,
                fusioncount INTEGER NOT NULL,
                gaze2dxmean REAL NOT NULL,
                gaze2dxmedian REAL NOT NULL,
                gaze2dxstdev REAL NOT NULL,
                gaze2dymean REAL NOT NULL,
                gaze2dymedian REAL NOT NULL,
                gaze2dystdev REAL NOT NULL,
                gaze2dcount INTEGER NOT NULL,
                FOREIGN KEY(runid) REFERENCES run(id));''')

        self._cur.execute('''CREATE INDEX idx_imu_id
                ON imu (id, runid);''')

        self._cur.execute('''CREATE INDEX idx_gaze_id
                ON gaze (id, runid);''')

        self._cur.execute('''CREATE INDEX idx_mag_id
                ON mag (id, runid);''')

        self._cur.execute('''CREATE INDEX idx_processed_id 
                ON processed (timestamp, runid, id);''')

        self._cur.execute('''CREATE INDEX idx_pgaze2d_id 
                ON pgaze2d (timestamp, runid, id);''')

        self._cur.execute('''CREATE INDEX idx_fusion_id 
                ON fusion (timestamp, runid, id)''')

        self._cur.execute('''CREATE INDEX idx_fusion_pitch 
                ON fusion (pitch, runid, id);''')

        self._cur.execute('''CREATE INDEX idx_summary_id
                ON summary (id, runid);''')

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
        self._cur.execute('''SELECT id, importdate, processdate, video, tags, pitchoffset, pitchmulti, horizonoffset, start, end
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
                'pitch_offset': run[5],
                'pitch_multi': run[6],
                'horizon_offset': run[7],
                'start': run[8],
                'end': run[9]
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
        self._cur.execute(
            '''SELECT * FROM gaze WHERE runid=(?) ORDER BY id ASC;''', (runid,))
        gaze_data = self._cur.fetchall()
        if gaze_data:
            for line in gaze_data:
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
        self._cur.execute(
            '''SELECT * FROM imu WHERE runid=(?) ORDER BY id ASC;''', (runid,))
        imu_data = self._cur.fetchall()
        if imu_data:
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
        self._cur.execute(
            '''SELECT * FROM imu where runid=(?) ORDER BY id ASC;''', (runid,))
        mag_data = self._cur.fetchall()
        if mag_data:
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

    def get_pgazed2d_data(self, runid: int, start: float = -1.0, end: float = -1.0) -> dict:
        """Gets all pgaze2d data for a given run, or just the times between a specific timestamp.

        Args:
            runid (int): The runid of which we want to grab data from.
            start (float, optional): The start time to grab data from. Defaults to -1.0.
            end (float, optional): The end time to grab data from. Defaults to -1.0.

        Raises:
            RuntimeError: When trying to select a non-existant runid.

        Returns:
            dict: Contains the processed 2d gaze data for a given runid.
        """
        pgaze2d_dict = {}
        if start == -1.0 and end == -1.0:
            self._cur.execute(
                '''SELECT * FROM pgaze2d WHERE runid=(?) ORDER BY id ASC;''', (runid,))
        else:
            self._cur.execute('''SELECT * FROM pgaze2d
                                WHERE runid=(?)
                                    AND timestamp BETWEEN (?) AND (?)
                                ORDER BY id ASC;''', (runid, start, end,))
        pgaze_data = self._cur.fetchall()
        if pgaze_data:
            for line in pgaze_data:
                pgaze2d_dict[line[2]] = [line[3], line[4]]
            return pgaze2d_dict
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
            (runid, timestamp, heading, pitch, roll,
             q0, q1, q2, q3, yinter, xinter, slope)
            VALUES(:runid, :timestamp, :heading, :pitch, :roll, :q0, :q1, :q2, :q3, :yinter, :xinter, :slope);'''
        self._cur.executemany(fusion_insert_query, fusion_data)
        self._con.commit()

    def get_fusion_data(self, runid: int, start: float = -1.0, end: float = -1.0) -> dict:
        """Gets all relevant fusion data for the runid, optionally including
            only the data between the start and end timestamps.

        Args:
            runid (int): The runid of which we want to grab data from.
            start (float, optional): The start time to grab data from. Defaults to -1.0.
            end (float, optional): The end time to grab data from. Defaults to -1.0.

        Raises:
            RuntimeError: If the runid does not exist

        Returns:
            dict: fusion data ready for other components
        """
        fusion_dict = {}
        if start == -1.0 and end == -1.0:
            self._cur.execute(
                '''SELECT * FROM fusion WHERE runid=(?) ORDER BY id ASC;''', (runid,))
        else:
            self._cur.execute('''SELECT * FROM fusion
                                WHERE runid=(?)
                                    AND timestamp BETWEEN (?) AND (?)
                                ORDER BY id ASC;''', (runid, start, end,))
        fusion_data = self._cur.fetchall()
        if fusion_data:
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
            if not self.check_existing_runid(runid):
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

    def get_gaze3d_z(self, runid: int) -> dict:
        """Gets all gaze_distance data for a specific run.

        Args:
            runid (int): runid we wish to grab gaze data for.

        Raises:
            RuntimeError: If there was an attempt to select a non-existant runid.

        Returns:
            dict: Contains all gaze3d distance data for the given run.
        """
        if self.check_existing_runid(runid):
            gaze_distance_dict = {}
            self._cur.execute('''SELECT timestamp, gaze3d2
                            FROM gaze WHERE runid=(?)''', (runid,))
            res = self._cur.fetchall()
            for row in res:
                gaze_distance_dict[row[0]] = row[1]
            return gaze_distance_dict
        else:
            raise RuntimeError(f'Trying to select a non-existant ID: {runid}')

    def update_parameters(self, runid: int, pitch_offset: int, pitch_multi: float, horizon_offset: float) -> None:
        """Updates the tweakable parameters in the database (run table).

        Args:
            runid (int): The runid that is being updated.
            pitch_offset (int): New roll offset value.
            pitch_multi (float): New pitch multiplier value.
            horizon_offset (float): New horizon offset value.

        Raises:
            RuntimeError: If there was an attempt to select a non-existant runid.
        """
        if self.check_existing_runid(runid):
            self._cur.execute('''UPDATE run
                            SET(pitchoffset, pitchmulti, horizonoffset) = (?, ?, ?)
                            WHERE id=(?);''', (pitch_offset, pitch_multi, horizon_offset, runid))
        else:
            raise RuntimeError(f'Trying to select a non-existant ID: {runid}')

    def get_parameters(self, runid: int) -> tuple:
        """Gets the tweakable parameters that were previously stored (run table).

        Args:
            runid (int): The runid to get parameters for.

        Raises:
            RuntimeError: If there was an attempt to select a non-existant runid.

        Returns:
            tuple: Contains the pitch_offset, pitch_multi, and horizon_offset values.
        """
        if self.check_existing_runid(runid):
            self._cur.execute('''SELECT pitchoffset, pitchmulti, horizonoffset
                            FROM run where id=(?);''', (runid,))
            parameters = self._cur.fetchone()
            return parameters
        else:
            raise RuntimeError(f'Trying to select a non-existant ID: {runid}')

    def write_process_date(self, runid: int) -> None:
        """Writes out the date the data was processed/reprocessed.

        Args:
            runid (int): runid which we are updating the processed date of.
        """
        self._cur.execute('''UPDATE run SET(processdate)=(?)
                        WHERE id=(?);''', (str(datetime.now().date()), runid))
        self._con.commit()

    def check_existing_runid(self, runid: int) -> bool:
        """Quickly check if the given runid exists in the database.

        Args:
            runid (int): runid to search for.

        Returns:
            bool: True if runid exists in run table.
        """
        self._cur.execute('''SELECT id FROM run WHERE id=(?);''', (runid,))
        res = self._cur.fetchall()
        if res:
            return True
        else:
            return False

    def write_processed_data(self, runid: int, processed: dict) -> None:
        """Writes out all data processed by HorizonGaze.

        Args:
            runid (int): The runid of the data to be written out.
            processed (dict): Processed HorizonGaze data.

        Raises:
            RuntimeError: If there was an attempt to select a non-existant runid.
        """
        processed_data = [{'runid': runid, 'timestamp': k, 'totalcount': v['total'], 'upcount': v['up_count'], 'downcount': v['down_count'],
                           'percentup': v['percent_up'], 'percentdown': v['percent_down'], 'currentup': 1 if v['currently_up'] else 0} for k, v in processed.items()]
        processed_query = '''INSERT INTO processed (runid, timestamp, totalcount, upcount, downcount, percentup, percentdown, currentup) VALUES(:runid, :timestamp, :totalcount, :upcount, :downcount, :percentup, :percentdown, :currentup);'''
        if self.check_existing_runid(runid):
            self._cur.executemany(processed_query, processed_data)
            self._con.commit()
        else:
            raise RuntimeError(f'Trying to select a non-existant ID: {runid}')

        self.update_processed_view()

    def get_processed_data(self, runid: int, start: float = -1, end: float = -1) -> dict:
        """Gets all data previously stored from HorizonGaze class, optionally
            only including data between start and end timestamps.

        Args:
            runid (int): The runid of which we want to grab data from.
            start (float, optional): The start time to grab data from. Defaults to -1.0.
            end (float, optional): The end time to grab data from. Defaults to -1.0.

        Raises:
            RuntimeError: If there was an attempt to select a non-existant runid.

        Returns:
            dict: All processed up/down data.
        """
        processed_dict = {}
        if start == -1 and end == -1:
            self._cur.execute(
                '''SELECT * FROM processed WHERE runid=(?) ORDER BY id ASC;''', (runid,))
        else:
            self._cur.execute('''SELECT * FROM processed
                                WHERE runid=(?)
                                    AND timestamp BETWEEN (?) AND (?)
                                ORDER BY id ASC;''', (runid, start, end,))
        processed_data = self._cur.fetchall()
        if processed_data:
            for line in processed_data:
                processed_dict[line[2]] = {
                    'total': line[3],
                    'up_count': line[4],
                    'down_count': line[5],
                    'percent_up': line[6],
                    'percent_down': line[7],
                    'currently_up': True if line[8] else False
                }
            return processed_dict
        else:
            raise RuntimeError(f'Trying to select a non-existant ID: {runid}')

    def update_processed_data(self, runid: int, processed: dict) -> None:
        """Updates existing up/down data, recalculated with HorizonGaze instance.

        Args:
            runid (int): runid of data we wish to update.
            processed (dict): All processed data from HorizonGaze.

        Raises:
            RuntimeError: If there was an attempt to select a non-existant runid.
        """
        update_query = '''UPDATE processed
                        SET (totalcount, upcount, downcount, percentup, percentdown, currentup) = (:totalcount, :upcount, :downcount, :percentup, :percentdown, :currentup)
                        WHERE runid = (:runid) AND timestamp = (:timestamp);'''
        update_list = []
        if not self.check_existing_runid(runid):
            raise RuntimeError(
                f'Trying to select a non-existant ID: {runid}')

        for k, v in processed.items():
            update_list.append({
                'timestamp': k,
                'runid': runid,
                'totalcount': v['total'],
                'upcount': v['up_count'],
                'downcount': v['down_count'],
                'percentup': v['percent_up'],
                'percentdown': v['percent_down'],
                'currentup': 1 if v['currently_up'] else 0
            })

        self._cur.executemany(update_query, update_list)
        self._con.commit()

    def update_processed_view(self) -> None:
        """Creates a view representing processed data grouped by runid.
        """
        drop_view_query = '''DROP VIEW IF EXISTS overall_percentage_view;'''
        view_query = '''
                CREATE VIEW overall_percentage_view
                AS SELECT a.runid, a.percentup, a.percentdown, a.upcount, a.downcount, a.totalcount
                FROM processed a
                INNER JOIN (
                    SELECT runid, MAX(totalcount) totalcount
                    FROM processed
                    GROUP BY runid)
                b ON a.runid = b.runid AND a.totalcount = b.totalcount;'''

        self._cur.execute(drop_view_query)
        self._cur.execute(view_query)
        self._con.commit()

    def get_processed_view(self) -> dict:
        """Creates and returns a dictionary containing the contents of the overall_percentage_view view."""

        select_view_query = '''SELECT * FROM overall_percentage_view;'''

        self._cur.execute(select_view_query)
        data = self._cur.fetchall()
        view_dict = {}

        for line in data:
            view_dict[line[0]] = [line[1], line[2], line[3], line[4], line[5]]

        return view_dict

    def get_overall_up_down(self, runids: list[int], start_times: list[float] = [-1], end_times: list[float] = [-1]) -> dict:
        """Gets the final cumulative calculated up/down for any number of runs.

        Args:
            runids (list[int]): List of runids to get data for.

        Returns:
            dict: Contains averaged up/down values for all input runids.
        """
        p_up = []
        p_down = []
        for runid, start, end in zip(runids, start_times, end_times):
            if start == -1 and end == -1:
                self._cur.execute('''SELECT id, runid, percentup, percentdown
                                FROM processed
                                WHERE runid=(?)
                                ORDER BY id DESC
                                LIMIT 1;''', str(runid))
            else:
                self._cur.execute('''SELECT id, runid, percentup, percentdown
                                FROM processed
                                WHERE runid=(?)
                                    AND timestamp BETWEEN (?) AND (?)
                                ORDER BY id DESC
                                LIMIT 1;''', (runid, start, end))
            line = self._cur.fetchone()
            p_up.append(line[2])
            p_down.append(line[3])
        return {
            'run_count': len(runids),
            'total_up': sum(p_up) / len(p_up),
            'total_down': sum(p_down) / len(p_down)
        }

    def get_all_gaze_2dy(self, runids: list[int]) -> dict:
        """Gets all processed gaze2d y data for any number of runids.

        Args:
            runids (list[int]): List of runids we wish to get data for.

        Returns:
            dict: Contains all gaze2d eye y data for each input run.
        """
        runids = [str(x) for x in runids]
        gaze_data = {}
        for runid in runids:
            self._cur.execute('''SELECT timestamp, pgaze2dy
                            FROM pgaze2d
                            WHERE runid=(?)
                            ORDER BY id ASC;''', runid)
            gaze_list = self._cur.fetchall()
            gaze_data[runid] = {
                'ts': [],
                'y': []
            }
            for line in gaze_list:
                gaze_data[runid]['ts'].append(line[0])
                gaze_data[runid]['y'].append(line[1])
        return gaze_data

    def get_binned_pitch_data(self, runids: list[int], start_times: list[float], end_times: list[float]) -> dict:
        """Gets agregate binned pitch data from any number of input runs.

        Args:
            runids (list[int]): List of runids to get data for.

        Returns:
            dict: Contains binned data alongside total count of samples
                for the provided list of runids.
        """
        binned_data = {}
        ranges = [-45 + (5 * x) for x in range(18)]
        count_query_default_time = '''SELECT COUNT (id) 
                        FROM fusion 
                        WHERE runid = (?);'''
        bin_query_default_time = '''SELECT COUNT (pitch)
                        FROM fusion
                        WHERE runid = (?)
                            AND pitch >= (?) AND pitch < (?);'''
        count_query = '''SELECT COUNT (id) 
                        FROM fusion 
                        WHERE runid = (?)
                            AND timestamp BETWEEN (?) AND (?);'''
        bin_query = '''SELECT COUNT (pitch)
                        FROM fusion
                        WHERE runid = (?)
                            AND pitch >= (?) AND pitch < (?)
                            AND timestamp BETWEEN (?) AND (?);'''
        for runid, start, end in zip(runids, start_times, end_times):
            if start == -1 or end == -1:
                binned_data[runid] = {}
                self._cur.execute(count_query_default_time, (runid,))
                binned_data[runid]['count'] = self._cur.fetchone()[0]
                for x in ranges:
                    self._cur.execute(bin_query_default_time, (runid, x, x + 5))
                    binned_data[runid][x] = self._cur.fetchone()[0] / \
                        binned_data[runid]['count']
            else:
                binned_data[runid] = {}
                self._cur.execute(count_query, (runid,start,end))
                binned_data[runid]['count'] = self._cur.fetchone()[0]
                for x in ranges:
                    self._cur.execute(bin_query, (runid, x, x + 5,start,end))
                    binned_data[runid][x] = self._cur.fetchone()[0] / \
                        binned_data[runid]['count']
        return binned_data

    def get_raw_fusion_data(self, runid: int) -> dict:
        """Gets the heading, pitch, roll, and quaternion values for the given runid.

        Args:
            runid (int): runid of item to get data for.

        Raises:
            RuntimeError: If there was an attempt to select a non-existant runid.

        Returns:
            dict: Contains heading, roll, pitch, and quaternion at each timestamp.
        """
        if self.check_existing_runid(runid):
            fusion_dict = {}
            self._cur.execute('''SELECT timestamp, heading, pitch,
                                roll, q0, q1, q2, q3
                            FROM fusion where runid=(?)
                            ORDER BY id ASC;''', (runid,))
            res = self._cur.fetchall()
            for line in res:
                fusion_dict[line[0]] = {
                    'heading': line[1],
                    'pitch': line[2],
                    'roll': line[3],
                    'q': (line[4], line[5], line[6], line[7])
                }
            return fusion_dict
        else:
            raise RuntimeError(f'Trying to select a non-existant ID: {runid}')

    def get_summary_data(self, runid: int) -> Tuple[dict, dict]:
        """Retrieves the summary data for a single runid.

        Args:
            runid (int): The runid for which we want to grab data for.

        Returns:
            Tuple[dict, dict]: Contains fusion_stats and gaze2d_stats.
        """
        get_summary_query = '''SELECT * FROM summary WHERE runid=(?);'''
        self._cur.execute(get_summary_query, (runid,))
        res = self._cur.fetchone()
        fusion_stats = {
            'pitch': {
                'mean': res[2],
                'median': res[3],
                'stdev': res[4]
            },
            'roll': {
                'mean': res[5],
                'median': res[6],
                'stdev': res[7]
            },
            'num_samples': res[8]
        }
        gaze2d_stats = {
            'x': {
                'mean': res[9],
                'median': res[10],
                'stdev': res[11]
            },
            'y': {
                'mean': res[12],
                'median': res[13],
                'stdev': res[14]
            },
            'num_samples': res[15]
        }
        return fusion_stats, gaze2d_stats

    def write_summary_data(self, runid: int, fusion_stats: dict, gaze2d_stats: dict) -> None:
        """Writes out both the fusion and gaze2d statistics to summary table.

        Args:
            runid (int): The runid to which the stats belong.
            fusion_stats (dict): Previously calculated fusion statistics.
            gaze2d_stats (dict): Previously calculated gaze2d statistics.
        """
        self._cur.execute('''SELECT * FROM summary
                        WHERE runid = (?);''', (runid,))
        res = self._cur.fetchone()
        if res:
            self._cur.execute('''DELETE FROM summary
                        WHERE runid = (?);''', (runid,))
            self._con.commit()

        write_summary_query = '''INSERT INTO summary
            (runid, pitchmean, pitchmedian, pitchstdev, rollmean, rollmedian,
                rollstdev, fusioncount, gaze2dxmean, gaze2dxmedian, gaze2dxstdev,
                gaze2dymean, gaze2dymedian, gaze2dystdev, gaze2dcount)
            VALUES(:runid, :pitchmean, :pitchmedian, :pitchstdev, :rollmean, :rollmedian,
                :rollstdev, :fusioncount, :gaze2dxmean, :gaze2dxmedian, :gaze2dxstdev,
                :gaze2dymean, :gaze2dymedian, :gaze2dystdev, :gaze2dcount);'''
        summary_dict = {
            'runid': runid,
            'pitchmean': fusion_stats['pitch']['mean'],
            'pitchmedian': fusion_stats['pitch']['median'],
            'pitchstdev': fusion_stats['pitch']['stdev'],
            'rollmean': fusion_stats['roll']['mean'],
            'rollmedian': fusion_stats['roll']['median'],
            'rollstdev': fusion_stats['roll']['stdev'],
            'fusioncount': fusion_stats['num_samples'],
            'gaze2dxmean': gaze2d_stats['x']['mean'],
            'gaze2dxmedian': gaze2d_stats['x']['median'],
            'gaze2dxstdev': gaze2d_stats['x']['stdev'],
            'gaze2dymean': gaze2d_stats['y']['mean'],
            'gaze2dymedian': gaze2d_stats['y']['median'],
            'gaze2dystdev': gaze2d_stats['y']['stdev'],
            'gaze2dcount': gaze2d_stats['num_samples']
        }
        self._cur.execute(write_summary_query, summary_dict)
        self._con.commit()

    def update_start_end(self, runid: int, start: int, end: int) -> None:
        update_query = '''UPDATE run 
                        SET start = (?), end = (?)
                        WHERE id = (?);'''
        self._cur.execute(update_query, (start, end, runid))
        self._con.commit()

    def get_total_duration(self, runid: int) -> float:
        self._cur.execute('''SELECT MAX(timestamp) FROM pgaze2d
                            WHERE runid = (?);''', (runid,))
        res = self._cur.fetchone()[0]
        return int(res) - 1


if __name__ == '__main__':
    pass
