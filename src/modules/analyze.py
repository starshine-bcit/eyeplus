class Analyze:
    def __init__(self):
        """Class for checking whether a gaze is looking up or down and storing the totals during runtime.
        Checks to see if a user is looking down are made by calculating whether the user's gaze is both
        below the horizon and within four meters."""

        self.readings_looking_up = 0
        self.readings_looking_down = 0
        self.total_readings = 0

    def check(self, y_intercept, slope, gaze2d_x, gaze2d_y, gaze3d_distance_from_user):
        """Performs the check to see if a user is looking up or down and increments the number of checks that have been made."""
        
        #gaze3d_distance_from_user is the third element in the gaze3d dictionary
        self.total_readings += 1
        if gaze2d_y > slope * gaze2d_x + y_intercept:
            self.readings_looking_up += 1
        elif gaze3d_distance_from_user > 400:
            self.readings_looking_up += 1
        else:
            self.readings_looking_down += 1

    def calculate(self):
        """Returns a tuple containing the percentages of time spent looking up and looking down."""
        
        percent_looking_up = self.readings_looking_up / self.total_readings
        percent_looking_down = self.readings_looking_down / self.total_readings

        return percent_looking_up, percent_looking_down
