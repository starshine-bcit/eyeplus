from eyedb import EyeDB
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

class Visual():
    def __init__(self, runid):
        """
        Database is initialized based on the path, and self.run id is set to the provided value for access 
        throughout the instance
        Args:
            runid (int): run id must be provided by the user in order to choose the instance visuals will be provided for
        """
        self.path = 'data\eye.db'
        self.db = EyeDB(db_path=Path(self.path))
        self.runid = runid
    
    def twodgaze_scatterplot(self):
        """Thie function creates a scatter plot for x,y coordinates of 2dgaze data and returns the plot

        Returns:
            plt: scatter plot created based on 2d gaze
        """
        gaze_data = self.db.get_gaze_data(runid=self.runid)
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
        for i in range(len(y_list)):
            y_list[i] = y_list[i] * -1

        x = np.array(x_list)
        y = np.array(y_list)
        plt.scatter(x, y, s=.1)
        return plt


