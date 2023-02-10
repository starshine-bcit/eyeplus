from eyedb import EyeDB
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

path = 'data\eye.db'
db = EyeDB(db_path=Path(path))
mag_data = db.get_mag_data(runid=1)

mag_keys = mag_data.keys()

x_list = []
y_list = []

# create a 2d scatter plot
fig = plt.figure()
ax = fig.add_subplot(111)

# scatterplot for magnetometer
for key in mag_keys:
    mag = mag_data[key]

    mag = mag['magnetometer']
    if mag[0] and mag[1]:
        x = mag[0]
        y = mag[1]
        x_list.append(x)
        y_list.append(y)

x = np.array(x_list)
y = np.array(y_list)

ax.scatter(x, y, s=.1)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_title('2D Magnetometer Scatterplot')

plt.show()
