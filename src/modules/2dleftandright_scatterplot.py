from eyedb import EyeDB
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

path = 'data\eye.db'
db = EyeDB(db_path=Path(path))
gaze_data = db.get_gaze_data(runid=1)

gaze_keys = gaze_data.keys()

right_x_list = []
right_y_list = []

for key in gaze_keys:
    gaze = gaze_data[key]

    gaze_right = gaze['right']
    if gaze_right['origin'][0] and gaze_right['origin'][1]:
        right_x = gaze_right['origin'][0]
        right_y = gaze_right['origin'][1]
        right_x_list.append(right_x)
        right_y_list.append(right_y)


# for the scatter plot view where (0,0) is the bottom left of the screen
x = np.array(right_x_list)
y = np.array(right_y_list)
plt.scatter(x, y, s=.1)

left_x_list = []
left_y_list = []

for key in gaze_keys:
    gaze = gaze_data[key]

    gaze_left = gaze['left']
    if gaze_left['origin'][0] and gaze_left['origin'][1]:
        left_x = gaze_left['origin'][0]
        left_y = gaze_left['origin'][1]
        left_x_list.append(left_x)
        left_y_list.append(left_y)

left_x = np.array(left_x_list)
left_y = np.array(left_y_list)
plt.scatter(left_x, left_y, s=.1, color='hotpink')

# labels for the scatterplot
plt.title('Left and Right Eye Gaze Plot')
plt.xlabel('X')
plt.ylabel('Y')

plt.show()

# if you want the flipped view where (0,0) is the top left of the screen
# flip the view
# for i in range(len(y_list)):
#     y_list[i] = y_list[i] * -1

# x = np.array(x_list)
# y = np.array(y_list)
# plt.scatter(x, y, s=.1)
# plt.show()
