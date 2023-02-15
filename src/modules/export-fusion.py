import sqlite3
import csv
import os
from pathlib import Path

class DataExporter:
    def __init__(self, db_path: str = 'data/eye.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def export_data_to_csv(self, output_path: str, runid: int = None, prefix: str = ""):
        # If runid is specified, export only data for that runid.
        # Otherwise, export data for all runids in the database.
        if runid is not None:
            runids = [runid]
        else:
            # Get all distinct runids from the "fusion" table.
            query = "SELECT DISTINCT runid FROM fusion;"
            rows = self.cursor.execute(query).fetchall()
            runids = [row[0] for row in rows]

        for runid in runids:
            # Export fusion data
            field_names = ['timestamp', 'heading', 'pitch', 'roll', 'q0', 'q1', 'q2', 'q3']
            rows = []

            query = f"SELECT * FROM fusion WHERE runid={runid};"
            fusion_rows = self.cursor.execute(query).fetchall()
            for row in fusion_rows:
                my_dict = {}
                my_dict['timestamp'] = row[1]
                my_dict['heading'] = row[2]
                my_dict['pitch'] = row[3]
                my_dict['roll'] = row[4]
                my_dict['q0'] = row[5]
                my_dict['q1'] = row[6]
                my_dict['q2'] = row[7]
                my_dict['q3'] = row[8]
                rows.append(my_dict)

            # Write fusion data to CSV file.
            fusion_filename = f'{prefix}fusion_data_runid_{runid}.csv'
            fusion_path = os.path.join(output_path, fusion_filename)
            os.makedirs(os.path.dirname(fusion_path), exist_ok=True)
            with open(fusion_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=field_names)
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)

            # Export pygaze data
            pygaze_field_names = ['timestamps', 'pygaze2dx', 'pygaze2dy']
            pygaze_rows = []

            query = f"SELECT * FROM pgaze2d WHERE runid={runid};"
            pgaze_rows = self.cursor.execute(query).fetchall()
            for row in pgaze_rows:
                my_dict = {}
                my_dict['timestamps'] = row[1]
                my_dict['pygaze2dx'] = row[2]
                my_dict['pygaze2dy'] = row[3]
                pygaze_rows.append(my_dict)

            # Write pygaze data to CSV file.
            pygaze_filename = f'{prefix}pygaze_data_runid_{runid}.csv'
            pygaze_path = os.path.join(output_path, pygaze_filename)
            os.makedirs(os.path.dirname(pygaze_path), exist_ok=True)
            with open(pygaze_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=pygaze_field_names)
                writer.writeheader()
                for row in pygaze_rows:
                    writer.writerow(row)

    def close(self):
        self.cursor.close()
        self.conn.close()
    def __del__(self):
        self.close()

#Test
exporter = DataExporter()

# Export data for a specific runid
exporter.export_data_to_csv('path/to/file', runid=1, prefix="data_")

# Export data for all runids
exporter.export_data_to_csv('path/to/file', prefix="data_")

