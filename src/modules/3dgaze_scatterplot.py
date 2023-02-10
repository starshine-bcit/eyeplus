from eyedb import EyeDB
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


path = 'data\eye.db'
db = EyeDB(db_path=Path(path))
gaze_data = db.get_gaze_data(runid=1)

gaze_keys = gaze_data.keys()

x_list = []
y_list = []
z_list = []

# create a 3d scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


# scatterplot for gaze3d
for key in gaze_keys:
    gaze = gaze_data[key]

    gaze3d = gaze['gaze3d']
    if gaze3d['origin'][0] and gaze3d['origin'][1] and gaze3d['origin'][2]:
        x = gaze3d['origin'][0]
        y = gaze3d['origin'][1]
        z = gaze3d['origin'][2]
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)


# scatter plot for right eye
# for key in gaze_keys:
#     gaze = gaze_data[key]

#     gaze_right = gaze['right']
#     if gaze_right['origin'][0] and gaze_right['origin'][1] and gaze_right['origin'][2]:
#         x = gaze_right['origin'][0]
#         y = gaze_right['origin'][1]
#         z = gaze_right['origin'][2]
#         x_list.append(x)
#         y_list.append(y)
#         z_list.append(z)

# # scatter plot for left eye
# for key in gaze_keys:
#     gaze = gaze_data[key]

#     gaze_left = gaze['left']
#     if gaze_left['origin'][0] and gaze_left['origin'][1] and gaze_left['origin'][2]:
#         x = gaze_left['origin'][0]
#         y = gaze_left['origin'][1]
#         z = gaze_left['origin'][2]
#         x_list.append(x)
#         y_list.append(y)
#         z_list.append(z)


x = np.array(x_list)
y = np.array(y_list)
z = np.array(z_list)


print(x)

ax.scatter(x, y, z, s=.1)

# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')
# ax.set_title('Gaze 3d Gaze Plot')

# plt.show()
