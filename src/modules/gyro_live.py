from eyedb import EyeDB
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import style

# ask for the run id

path = 'data\eye.db'
db = EyeDB(db_path=Path(path))

# print(list(imu_keys)[0])


imu_data = db.get_imu_data(runid=1)

imu_keys = imu_data.keys()

y_list = []
for key in imu_keys:
    y_list.append(imu_data[key]['accelerometer'][1])

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)



yx = y_list[:10]
def animate(i): 

    xs = [i for i in range(len(yx))]
    ax1.clear()
    ax1.plot(xs, yx)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()