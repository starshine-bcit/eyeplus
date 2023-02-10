from eyedb import EyeDB
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

path = 'data\eye.db'
db = EyeDB(db_path=Path(path))
gaze_data = db.get_gaze_data(runid=1)

gaze_keys = gaze_data.keys()


x_list = []
y_list = []

for key in gaze_keys:
    gaze = gaze_data[key]
    gaze2d = gaze['gaze2d']

    if gaze2d[0] and gaze2d[1]:
        if gaze2d[0] < 200 and gaze2d[1] < 200:
            x_list.append(gaze2d[0])
            y_list.append(gaze2d[1])

# for the scatter plot view where (0,0) is the bottom left of the screen
# x = np.array(x_list)
# y = np.array(y_list)
# plt.scatter(x, y, s=.1)
# plot red heatmap using matplotlib

# plt.hist2d(x, y, bins=100, cmap='Reds')
# plt.hist2d(x, y, bins=100, cmap='Reds')
# plt.colorbar()
# plt.show()


# if you want the flipped view where (0,0) is the top left of the screen
# flip the view
for i in range(len(y_list)):
    y_list[i] = y_list[i] * -1

x = np.array(x_list)
y = np.array(y_list)

# show heatmap
# plt.hist2d(x, y, bins=100, cmap='Reds')
# plt.colorbar()
# plt.show()

plt.scatter(x, y, s=.1)

# create a title in the scatterplot
plt.title('2D Gaze Plot')

# create a label for the x axis
plt.xlabel('X')

# create a label for the y axis
plt.ylabel('Y')
# show the plot
plt.show()
