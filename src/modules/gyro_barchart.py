from eyedb import EyeDB
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# ask for the run id

path = 'data\eye.db'
db = EyeDB(db_path=Path(path))
# mag_data = db.get_mag_data(runid=1)

# mag_keys = mag_data.keys()

# print(list(mag_keys)[0])
# print(mag_data[0.001038])

# x_list = []
# y_list = []

# for key in mag_keys:
#     gaze = mag_data[key]
#     magnetometer = gaze['magnetometer']

#     if magnetometer[0] and magnetometer[1]:
#         x_list.append(magnetometer[0])
#         y_list.append(magnetometer[1])

# # ## for the scatter plot view where (0,0) is the bottom left of the screen
# x = np.array(x_list)
# y = np.array(y_list)
# plt.scatter(x, y, s=.1)
# plt.show()


imu_data = db.get_imu_data(runid=1)

imu_keys = imu_data.keys()

# print(list(imu_keys)[0])
# print(imu_data[0.001038])

x_list = []
y_list = []

for key in imu_keys:
    gaze = imu_data[key]
    gyroscope = gaze['gyroscope']

    if gyroscope[0] and gyroscope[1]:
        x_list.append(gyroscope[0])
        y_list.append(gyroscope[1])

# ## for the scatter plot view where (0,0) is the bottom left of the screen
x = np.array(x_list)
y = np.array(y_list)

# plt.scatter(x, y, s=.1)
# plt.show()

ups = y[(y < 0)]
downs = y[(y > 0)]

x = ['Pos', 'Negative']
y = [len(ups), len(downs)]
fig = plt.figure(figsize=(10, 5))
plt.bar(x, y, color='maroon',
        width=0.4)

plt.xlabel("Gyroscope")
plt.ylabel("Count")
plt.title("Gyroscope Bar Chart")
plt.show()
