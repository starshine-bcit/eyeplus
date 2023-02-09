import math

def calculate_horizon_line(accelerometer, gyroscope):
    """Receives accelerometer and gyroscope data and returns the angle and position of the horizon line."""

    #Calculates the pitch angle using the accelerometer data
    pitch = math.atan2(-accelerometer[0], math.sqrt(accelerometer[1]**2+ accelerometer[2]**2))

    #Integrates the angular velocity from the gyroscope data to get the roll angle
    roll = 0
    for i in range(1, len(gyroscope)):
        roll += gyroscope[i-1] * (gyroscope[i][0]-gyroscope[i-1][0]) 


    #Returns the pitch and rolls angles
    return pitch, roll    
    

def compare_gaze_coordinates(gaze_coordinates):
    """Uses horizon line angle and position and gaze coordinates to determine if the user is looking above or below the horizon at the timestamp."""
    pass
