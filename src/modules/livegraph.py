import numpy as np
import matplotlib.pyplot as plt  # matplotlib >= 3.6.0
import quaternion  # package numpy-quaternion

# See Diebel, James "Representing Attitude: Euler Angles, Unit Quaternions, and Rotation Vectors" (2006)
# https://www.astro.rug.nl/software/kapteyn-beta/_downloads/attitude.pdf
# Sequence (3, 2, 1)
def quat_to_elev_azim_roll(q, angle_offsets=(0, 0, 0)):
    q0, q1, q2, q3 = q.w, q.x, q.y, q.z
    phi = np.arctan2(-2*q1*q2 + 2*q0*q3, q1**2 + q0**2 - q3**2 - q2**2)
    theta = np.arcsin(2*q1*q3 + 2*q0*q2)
    psi = np.arctan2(-2*q2*q3 + 2*q0*q1, q3**2 - q2**2 - q1**2 + q0**2)
    azim = np.rad2deg(phi) + angle_offsets[0]
    elev = np.rad2deg(-theta) + angle_offsets[1]
    roll = np.rad2deg(psi) + angle_offsets[2]
    return elev, azim, roll

def elev_azim_roll_to_quat(elev, azim, roll, angle_offsets=(0, 0, 0)):
    phi = np.deg2rad(azim) - angle_offsets[0]
    theta = np.deg2rad(-elev) - angle_offsets[1]
    psi = np.deg2rad(roll) - angle_offsets[2]
    q0 = np.cos(phi/2)*np.cos(theta/2)*np.cos(psi/2) - np.sin(phi/2)*np.sin(theta/2)*np.sin(psi/2)
    q1 = np.cos(phi/2)*np.cos(theta/2)*np.sin(psi/2) + np.sin(phi/2)*np.sin(theta/2)*np.cos(psi/2)
    q2 = np.cos(phi/2)*np.sin(theta/2)*np.cos(psi/2) - np.sin(phi/2)*np.cos(theta/2)*np.sin(psi/2)
    q3 = np.cos(phi/2)*np.sin(theta/2)*np.sin(psi/2) + np.sin(phi/2)*np.cos(theta/2)*np.cos(psi/2)
    q = np.Quaternion(q0, q1, q2, q3)
    return q

q = np.Quaternion(1, 0, 0, 0)
angles_init = (0, 0, 0)
elev, azim, roll = quat_to_elev_azim_roll(q, angles_init)

ax = plt.figure().add_subplot(projection='3d')
ax.view_init(elev, azim, roll)
