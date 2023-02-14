from eyedb import EyeDB
from pathlib import Path
import csv

path = 'data\eye.db'
db = EyeDB(db_path=Path(path))

field_names = ['timestamp', 'heading', 'pitch', 'roll', 'q0', 'q1', 'q2', 'q3']
rows = []

run_id = 1
fusion_data = db.get_fusion_data(runid=1)
fusion_keys = fusion_data.keys()

# print(fusion_data[0.003754]['heading'])
# print(fusion_data[0.003754]['q'][0])
# print(list(fusion_keys)[0])
for key in fusion_keys:
    my_dict = {}
    # my_dict['runid'] = run_id
    if fusion_data[key]:
        my_dict['timestamp'] = key
        my_dict['heading'] = fusion_data[key]['heading']
        my_dict['pitch'] = fusion_data[key]['pitch']
        my_dict['roll'] = fusion_data[key]['roll']
        my_dict['q0'] = fusion_data[key]['q'][0]
        my_dict['q1'] = fusion_data[key]['q'][1]
        my_dict['q2'] = fusion_data[key]['q'][2]
        my_dict['q3'] = fusion_data[key]['q'][3]
        rows.append(my_dict)

with open('fusion.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = field_names)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

pygaze_field_names = ['timestamps', 'pygaze2dx', 'pygaze2dy']
pygaze_rows = []

run_id = 1
pgaze_data = db.get_gaze_data(runid=1)
pgaze_keys = pgaze_data.keys()
for key in pgaze_keys:
    my_dict = {}
    if pgaze_data[key]:
        my_dict['timestamps'] = key
        my_dict['pygaze2dx'] = pgaze_data[key]['gaze2d'][0]
        my_dict['pygaze2dy'] = pgaze_data[key]['gaze2d'][1]
        pygaze_rows.append(my_dict)

with open('pygaze.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = pygaze_field_names)
    writer.writeheader()
    for row in pygaze_rows:
        writer.writerow(row)



# for key in pgaze_keys:
#     my_dict = {}
#     if pgaze_data[key]:
#         my_dict['timestamp'] = key
#         my_dict['pgaze2dx'] = pgaze_data[key]['pgaze2dx'][0]
#         my_dict['pgaze2dy'] = pgaze_data[key]['pgaze2dy'][0]
#         pgaze_rows.append(my_dict)

# with open('pygaze.csv', 'w', newline='') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames = pgaze_field_names)
#     writer.writeheader()
#     for row in pgaze_rows:
#         writer.writerow(row)



