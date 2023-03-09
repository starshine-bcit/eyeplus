from eyedb import EyeDB
from pathlib import Path
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.animation as animation

path = 'data\eye.db'
db = EyeDB(db_path=Path(path))
gaze_data = db.get_gaze_data(runid=1)

gaze_keys = gaze_data.keys()

x_list = []
y_list = []

for key in gaze_keys:
    gaze = gaze_data[key]
    gaze2d = gaze['gaze2d']

    gaze2d = gaze['gaze2d']
    if gaze2d[0] and gaze2d[1]:
        x = gaze2d[0]
        y = gaze2d[1]
        x_list.append(x)
        y_list.append(y)


for i in range(len(y_list)):
    y_list[i] = y_list[i] * -1

x = np.array(x_list)
y = np.array(y_list)

fig = plt.figure()
ax = fig.add_subplot(111)

# create a dynamic scatterplot


def update(i):
    ax.clear()
    ax.scatter(x[:i], y[:i], s=.1)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_title('2D Gaze Scatterplot')


ani = animation.FuncAnimation(fig, update, interval=1)
plt.show()
