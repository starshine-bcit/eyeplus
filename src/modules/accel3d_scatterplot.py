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
z_list = []

# create a 3d scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# scatterplot for accelerometer
for key in imu_keys:
    imu = imu_data[key]

    accelerometer = imu['accelerometer']
    if accelerometer[0] and accelerometer[1] and accelerometer[2]:
        x = accelerometer[0]
        y = accelerometer[1]
        z = accelerometer[2]
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)

x = np.array(x_list)
y = np.array(y_list)
z = np.array(z_list)

ax.scatter(x, y, z, s=.1)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
ax.set_title('3D Accelerometer Scatterplot')

plt.show()
