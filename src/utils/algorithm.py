import math
import time


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
    
def detect_motion(accelerometer, gyroscope):
    """Detects if the user is in motion based on the accelerometer and gyroscope data. """

    #Calculate the magnitude of the acceleration vector
    acceleration = math.sqrt(sum(a**2 for a in accelerometer))

    #Calculete the magnitude of the angular velocity vector
    angular_velocity = math.sqrt(sum(a**2 for a in gyroscope))

    #Check if the user is in motion based on the values
    if acceleration > 1.5 and angular_velocity > 0.5:
        return True
    else: 
        return False
    

def detect_blink(gaze1, gaze2):
    """Detects a blink based on changes in gaze coordinates"""
    _, y1, _ = gaze1
    _, y2, _ = gaze2

    if y1 -y2 > 0.05:
        return True
    else:
        return False
    
def calibrate_gaze_tracker(screen_position):
    """Runs a calinration routine to determine the relationship between the user's gaze coord and the position on the screen. """
    #Display a series of targets in different positions on the screen
    targets = [(0.1,0.1), (0.5,0.5), (0.9,0.9), (0.1,0.9), (0.9,0.1)]
    for target in targets:
            (int(screen_position[0] + target[0]*(screen_position[2] - screen_position[0])),
            int(screen_position[1] + target[1]*(screen_position[3] - screen_position[1])))

def detect_saccade(gaze1, gaze2):
    """Detects a saccade(rapid eye movements) based on changes in gaze coordinates"""
    x1, y1, _ = gaze1
    x2, y2, _ = gaze2
    if abs(x2 - x1) > 0.1 or abs(y2 - y1) > 0.1: # threshold for a saccade (adjust as needed)
        return True
    else:
        return False
    #Can change the parameters in this function any time



def calibrate_tracker(tracker):
    """Calibrates the tracker by having the user look at four points on the screen."""
    # Define four points in the screen, for example, the four corners.
    points = [(0, 0), (0, 100), (100, 100), (100, 0)]

    # Display each point and record the gaze coordinates.
    gaze_data = []
    for point in points:
        # Display the target.
        tracker.show_target(point)

        # Wait for the user to fixate on the target.
        while True:
            # Get the latest gaze coordinates.
            gaze_coordinates = tracker.get_gaze_coordinates()

            # Check if the gaze coordinates are within a tolerance of the target point.
            if abs(gaze_coordinates[0] - point[0]) <= 5 and abs(gaze_coordinates[1] - point[1]) <= 5:
                # Record the gaze coordinates and move to the next target.
                gaze_data.append(gaze_coordinates)
                time.sleep(1)  # Wait for a short period to avoid rapid transitions.
                break

    # Calculate the average gaze coordinates for each target.
    avg_gaze_data = [(sum(x) / len(x), sum(y) / len(y)) for x, y in zip(*[iter(gaze_data)] * 2)]

    # Calculate the calibration offset and update the tracker's calibration.
    x_offset = sum([point[0] - gaze[0] for point, gaze in zip(points, avg_gaze_data)]) / len(points)
    y_offset = sum([point[1] - gaze[1] for point, gaze in zip(points, avg_gaze_data)]) / len(points)
    tracker.set_calibration_offset((x_offset, y_offset))


def estimate_distance(object_size, fov_angle):
    """Calculates the estimated distance to an object based on its size and camera's"""
    object_size = object_size / 100  #converts to cm
    fov_angle = math.radians(fov_angle)
    distance = object_size / (2 * math.tan(fov_angle / 2))

    return distance * 100 # convert back to cm


def get_gaze_position(gaze_direction, head_pose, camera_pose):
    """
    Calculates the 3D position of the gaze in world coordinates based on the gaze direction, head pose, and camera pose.
    """
    # Convert the gaze direction from camera coordinates to world coordinates
    gaze_direction_world = np.dot(np.linalg.inv(camera_pose), np.append(gaze_direction, 0))
    gaze_direction_world = gaze_direction_world[:3] / np.linalg.norm(gaze_direction_world[:3])

    # Calculate the position of the gaze in world coordinates
    gaze_position = head_pose[:3, 3] + (gaze_direction_world * 100)  # Assume distance of 100 units from the head

    return gaze_position

    
    
