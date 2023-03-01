# from visualpresentation import Visual

# V1 = Visual(runid=1)
# # plot = V1.twodgaze_scatterplot()
# # plot.show()


# # 3d gaze
# # plot = V1.threedgaze()
# # plot.show()

# #fusion basic
# # V1.fusion_basic()


# # #fusion basic
# # V1.fusion_basic()
# # # plot.show()


from eyedb import EyeDB
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# from barclass import BarChartUpDown

path = 'data\eye.db'
db = EyeDB(db_path=Path(path))

imu_data = db.get_imu_data(runid=1)

imu_keys = imu_data.keys()

# print(list(imu_keys)[0])
# print(imu_data[0.001038])

# x_list = []
# y_list = []

# for key in imu_keys:
#     gaze = imu_data[key]
#     gyroscope = gaze['gyroscope']

#     if gyroscope[0] and gyroscope[1]:
#         x_list.append(gyroscope[0])
#         y_list.append(gyroscope[1])

# # ## for the scatter plot view where (0,0) is the bottom left of the screen
# x = np.array(x_list)
# y = np.array(y_list)

# barchart = BarChartUpDown(width=500, height=500)
# barchart.plotify(x_list=x,y_list=y)
# # barchart.plt.show()

# from twodgazeclass import twodgazescatter

# gaze_data = db.get_gaze_data(runid=1)
# gaze_keys = gaze_data.keys()

# x_list = []
# y_list = []

# for key in gaze_keys:
#     gaze = gaze_data[key]
#     gaze2d = gaze['gaze2d']

#     if gaze2d[0] and gaze2d[1]:
#         if gaze2d[0] < 200 and gaze2d[1] < 200:
#             x_list.append(gaze2d[0])
#             y_list.append(gaze2d[1])
# for i in range(len(y_list)):
#     y_list[i] = y_list[i] * -1

# scatter = twodgazescatter(height=500,width=500)
# scatter.plotify(x_list=x_list, y_list=y_list)
# scatter.plt.show()



# from pitchliveclass import pitchlive

path = 'data\eye.db'
db = EyeDB(db_path=Path(path))


fusion_data = db.get_fusion_data(runid=1)
fusion_keys = fusion_data.keys()

# # print(list(fusion_keys)[0])
# # print(list(fusion_data[0.009372]))
# print(fusion_data[0.009372])

# y_list = []
# for key in fusion_data:
#     y_list.append(fusion_data[key]['pitch'])
# print(len(y_list))
# xs = [i for i in range(0, len(y_list), 100)]

# plot = pitchlive(width=1000,height=1000)
# plot.plotify(y_list=y_list,x_list=xs)
# plot.plt.show()

# from pitchliveclass import pitchlive
# plot = pitchlive(width=1000,height=1000)
# plot.plot({'y':y_list})
# plot.show()



path = 'data\eye.db'
db = EyeDB(db_path=Path(path))
gaze_data = db.get_gaze_data(runid=1)

gaze_keys = gaze_data.keys()

x_list = []
y_list = []
z_list = []

for key in gaze_keys:
    gaze = gaze_data[key]

    gaze3d = gaze['gaze3d']
    if gaze3d[0] and gaze3d[1] and gaze3d[2]:
        x = gaze3d[0]
        y = gaze3d[1]
        z = gaze3d[2]
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)
data = {}
data['x_list'] = x_list
data['y_list'] = y_list
data['z_list'] = z_list

from threedgazeclass import threedgazeclass
plot = threedgazeclass(width=500, height=500)
plot.plotify(data)
plot.show()