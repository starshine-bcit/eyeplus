from eyedb import EyeDB
from pathlib import Path
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

path = 'data\eye.db'
db = EyeDB(db_path=Path(path))
imu_data = db.get_imu_data(runid=1)

imu_keys = imu_data.keys()

x_list = []
y_list = []

# create a 2d scatter plot
fig = plt.figure()
ax = fig.add_subplot(111)

# scatterplot for gyroscope
for key in imu_keys:
    imu = imu_data[key]

    gyroscope = imu['gyroscope']
    if gyroscope[0] and gyroscope[1]:
        x = gyroscope[0]
        y = gyroscope[1]
        x_list.append(x)
        y_list.append(y)

x = np.array(x_list)
y = np.array(y_list)

ax.scatter(x, y, s=.1)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_title('2D Gyroscope Scatterplot')

plt.show()
