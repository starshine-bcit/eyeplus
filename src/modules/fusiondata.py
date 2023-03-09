from eyedb import EyeDB
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

path = 'data\eye.db'
db = EyeDB(db_path=Path(path))
fusion_data = db.get_fusion_data(runid=1)

fusion_keys = fusion_data.keys()


# create headings scatter plot
heading_list = []

for key in fusion_keys:
    fusion = fusion_data[key]
    heading = fusion['heading']
    heading_list.append([heading])

heading = np.array(heading_list)

# create a static scatterplot
fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(heading, s=.1)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_title('Fusion Heading Scatterplot')

plt.show()


# create a pitch scatter plot
pitch_list = []

for key in fusion_keys:
    fusion = fusion_data[key]
    pitch = fusion['pitch']
    pitch_list.append([pitch])

pitch = np.array(pitch_list)

# create a static scatterplot
fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(pitch, s=.1)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_title('Fusion Pitch Scatterplot')

plt.show()

# create a roll scatter plot
roll_list = []

for key in fusion_keys:
    fusion = fusion_data[key]
    roll = fusion['roll']
    roll_list.append([roll])

roll = np.array(roll_list)

# create a static scatterplot
fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(roll, s=.1)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_title('Fusion Roll Scatterplot')

plt.show()

# create a scatter plot of heading vs pitch
fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(heading, pitch, s=.1)
ax.set_xlabel('Heading')
ax.set_ylabel('Pitch')
ax.set_title('Fusion Heading vs Pitch Scatterplot')

plt.show()

# create a scatter plot of heading vs roll
fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(heading, roll, s=.1)
ax.set_xlabel('Heading')
ax.set_ylabel('Roll')
ax.set_title('Fusion Heading vs Roll Scatterplot')

plt.show()

# create a scatter plot of pitch vs roll
fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(pitch, roll, s=.1)
ax.set_xlabel('Pitch')
ax.set_ylabel('Roll')
ax.set_title('Fusion Pitch vs Roll Scatterplot')

plt.show()

# create a scatter plot of heading vs pitch vs roll
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(heading, pitch, roll, s=.1)
ax.set_xlabel('Heading')
ax.set_ylabel('Pitch')
ax.set_zlabel('Roll')
ax.set_title('Fusion Heading vs Pitch vs Roll Scatterplot')

plt.show()

# create a scatter plot of y intercept and x intercept
y_intercept_list = []
x_intercept_list = []

for key in fusion_keys:
    fusion = fusion_data[key]
    y_intercept = fusion['y_intercept']
    x_intercept = fusion['x_intercept']
    y_intercept_list.append([y_intercept])
    x_intercept_list.append([x_intercept])

y_intercept = np.array(y_intercept_list)
x_intercept = np.array(x_intercept_list)

# create a static scatterplot
fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(y_intercept, x_intercept, s=.1)
ax.set_xlabel('Y Intercept')
ax.set_ylabel('X Intercept')
ax.set_title('Fusion Y Intercept vs X Intercept Scatterplot')

plt.show()
