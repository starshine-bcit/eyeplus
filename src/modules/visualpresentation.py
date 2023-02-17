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
    def threedgaze(self):
        """A scatter plot of the three d gaze points will be created

        Returns:
            plt: the scatter plot will be returned
        """
        gaze_data = self.db.get_gaze_data(runid=self.runid)

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
            if gaze3d[0] and gaze3d[1] and gaze3d[2]:
                x = gaze3d[0]
                y = gaze3d[1]
                z = gaze3d[2]
                x_list.append(x)
                y_list.append(y)
                z_list.append(z)
        
        x = np.array(x_list)
        y = np.array(y_list)
        z = np.array(z_list)

        ax.scatter(x, y, z, s=.1)

        # ax.set_xlabel('X Label')
        # ax.set_ylabel('Y Label')
        # ax.set_zlabel('Z Label')
        # ax.set_title('Gaze 3d Gaze Plot')

        return plt
    def fusion_basic(self):
        fusion_data = self.db.get_fusion_data(self.runid)
        fusion_keys = fusion_data.keys()

        # print(list(fusion_keys)[0])
        # print(fusion_data[0.001038])

        pitch_list = []

        for key in fusion_keys:
            pitch = fusion_data[key]['pitch']
            if pitch:
                pitch_list.append(pitch)

        x = np.array(pitch_list)


        ## histogram
        plt.hist(x, bins= 100)

        ##bar chart
        positive_values = x[x > 0]
        negative_values = x[x < 0]

        # plt.bar(['positive_values', 'negative_values'], [len(positive_values)/len(pitch_list), len(negative_values)/len(pitch_list)])
        # # plt.xlabel("+")
        # plt.ylabel("-")
        plt.show()

