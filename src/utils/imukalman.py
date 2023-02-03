#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# brief        IMU angular estimation with extended Kalman Filter
# author       Tateo YANAGI
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import numpy as np

P1 = []
P2 = []
P3 = []
time_s = 0


class extKalmanFilter(object):
    def __init__(self, period_ms):
        self.dts = period_ms / 1000

        # initialize angular velocity
        angular_vel_x = np.deg2rad(10.0)
        angular_vel_y = np.deg2rad(10.0)
        angular_vel_z = np.deg2rad(0.0)
        self.gyro_angular_vel = np.array(
            [[angular_vel_x], [angular_vel_y], [angular_vel_z]])

        # observation matrix H
        self.H = np.diag([1.0, 1.0])

        # system noise variance
        self.Q = np.diag([1.74E-2*self.dts*self.dts,
                         1.74E-2*self.dts*self.dts])

        # observation noise variance
        self.R = np.diag([1.0*self.dts*self.dts, 1.0*self.dts*self.dts])

        # initialize true status
        self.x_true = np.array([[0.0], [0.0]])

        # initialize prediction
        self.x_bar = self.x_true

        # initialize eastimation
        self.x_hat = self.x_true

        # initialize covariance
        self.P = self.Q

        # initialize jacbian matrix of H
        self.jacobianH = np.diag([1.0, 1.0])

    def get_ekf(self):
        # Ground Truth
        self.x_true = self.get_status(self.x_true)

        # [step1] prediction
        self.x_bar = self.get_status(self.x_hat)

        # jacobian matrix
        jacobianF = self.get_jacobianF(self.x_bar)

        # pre_covariance
        P_bar = (jacobianF @ self.P @ jacobianF.T) + self.Q

        # observation
        w = np.random.multivariate_normal([0.0, 0.0], self.R, 1).T
        y = (self.H @ self.x_true) + w

        # [step2] update the filter
        s = (self.H @ P_bar @ self.H.T) + self.R
        K = (P_bar @ self.H.T) @ np.linalg.inv(s)

        # eastimation
        e = y - (self.jacobianH @ self.x_bar)
        self.x_hat = self.x_bar + (K @ e)

        # post_covariance
        I = np.identity(self.x_hat.shape[0])
        self.P = (I - K @ self.H) @ P_bar

        return self.x_true, y, self.x_hat, self.P

    # get status
    def get_status(self, x):
        tri = self.get_trigonometrxic(x)
        Q = np.array([[1, tri[0, 1]*tri[1, 2], tri[0, 0] *
                     tri[1, 2]], [0, tri[0, 0], -tri[0, 1]]])
        x = x + (Q @ self.gyro_angular_vel) * self.dts
        return x

    # get jacobian matrix of F
    def get_jacobianF(self, x):
        g = self.gyro_angular_vel
        tri = self.get_trigonometrxic(x)
        jacobianF = np.array([[1.0+(tri[0, 0]*tri[1, 2]*g[1][0]-tri[0, 1]*tri[1, 2]*g[2][0])*self.dts, (tri[0, 1]/tri[1, 0]/tri[1, 0]*g[1][0]+tri[0, 0]/tri[1, 0]/tri[1, 0]*g[2][0])*self.dts],
                              [-(tri[0, 1]*g[1][0]+tri[0, 0]*g[2][0])*self.dts, 1.0]])
        return jacobianF

    # get trigonometrxic of roll&pitch
    def get_trigonometrxic(self, x):
        return np.array([[np.cos(x[0][0]), np.sin(x[0][0]), np.tan(x[0][0])], [np.cos(x[1][0]), np.sin(x[1][0]), np.tan(x[1][0])]])
