from eyedb import EyeDB
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import style
import time
# ask for the run id


path = 'data\eye.db'
db = EyeDB(db_path=Path(path))


fusion_data = db.get_fusion_data(runid=1)
fusion_keys = fusion_data.keys()

# # print(list(fusion_keys)[0])
# # print(list(fusion_data[0.009372]))
# print(fusion_data[0.009372])

y_list = []
for key in fusion_data:
    y_list.append(fusion_data[key]['pitch'])

ax = plt.axes()


xs = [i for i in range(0, len(y_list), 100)]
for i in range(0, len(y_list), 1000):
    y = y_list
    plt.ylim(-15,25)
    plt.scatter(i, y[i])
    plt.plot(i, y[i])
    plt.pause(0.01)

plt.show()

# def write_list_to_file(lst):
#     file_path = Path("example.txt")
#     with file_path.open(mode="w") as file:
#         for i in range(0, len(lst), 1000):
#             file.write("\n".join(lst[i:i+1000]))
#             file.write("\n")
#             time.sleep(3)

# # y_arr = np.array(y_list)

# write_list_to_file(y_list)

# style.use('fivethirtyeight')

# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)

# yx = y_list[:20]
# def animate(i): 
#     xs = [i for i in range(len(yx))]
#     ax1.clear()
#     ax1.plot(xs, yx)

# ani = animation.FuncAnimation(fig, animate, interval=1000)
# plt.show()

# def animate(i): 
#     xs = [i for i in range(len(yx))]
#     graph_data = open('example.txt','r').read()
#     lines = graph_data.split('\n')
#     for line in lines:
#         if len(line) > 1:
#             xs.append(float(line))

#     ax1.clear()
#     ax1.plot(xs, yx)

# ani = animation.FuncAnimation(fig, animate, interval=1000)
# # plt.show()