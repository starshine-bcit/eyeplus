import math

def calculate_horizon_line(accelerometer, gyroscope):
    """Receives accelerometer and gyroscope data and returns the angle and position of the horizon line."""
    # Calculates the roll angle using the gyroscope data
    roll = gyroscope[0]

    # Calculates the pitch angle using the accelerometer and gyroscope data
    pitch = math.atan2(-accelerometer[0], math.sqrt(accelerometer[1]**2 + accelerometer[2]**2))
    pitch_gyro = gyroscope[1]

    # Integrates the pitch angle over time to estimate the current angle of the device
    pitch = pitch * 0.98 + pitch_gyro * 0.02

    return roll, pitch

def compare_gaze_coordinates(gaze_coordinates):
    """Uses horizon line angle and position and gaze coordinates to determine if the user is looking above or below the horizon at the timestamp."""
    # Rotates the gaze coordinates to match the horizon line angle and position
    x = gaze_coordinates[0] * math.cos(pitch) + gaze_coordinates[2] * math.sin(pitch)
    y = gaze_coordinates[1] * math.cos(roll) -  gaze_coordinates[2] * math.sin(roll)

    #Determines if the gaze is above or below the horizon line
    if y > 0:
        return "above"
    else:
        return "below
