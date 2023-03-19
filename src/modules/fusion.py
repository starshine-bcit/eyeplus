from math import sqrt, atan2, asin, degrees, radians

from modules.regressor import RegressionMagnetometerModel


class DeltaT():
    def __init__(self, first_timestamp: float) -> None:
        """Finds time delta from timestamp.

        Args:
            first_timestamp (float): The starting point for the time delta.
        """
        self.first_timestamp = first_timestamp
        self.start_time = None

    def __call__(self, timestamp: float) -> float:
        """Each time DeltaT is called it returns the delta point from the last provided timestamp.

        Args:
            timestamp (float): The current timestamp.

        Returns:
            float: The diff between current time and previous (last call).
        """
        if self.start_time is None:
            self.start_time = self.first_timestamp
            return self.start_time
        delta = timestamp - self.start_time
        self.start_time = timestamp
        return delta


class Fusion():
    # Optional offset for true north. A +ve value adds to heading
    declination = 0

    def __init__(self, imu_data: dict, mag_data: dict) -> None:
        """Fuses gyro, accelerometer, and magnetometer data from Tobii Eye Pro 3 glasses, providing pitch, heading, and roll values.

        Args:
            imu_data (dict): Contains gyro and accelerometer data from Tobii ndjson file.
            mag_data (dict): Contains magnetometer data from Tobii ndjson file.
        """
        # local magnetic bias factors: set from calibration
        self.magbias = (0, 0, 0)
        self.expect_ts = True
        self.q = [1.0, 0.0, 0.0, 0.0]
        GyroMeasError = radians(40)
        # compute beta (see README)
        self.beta = sqrt(3.0 / 4.0) * GyroMeasError
        self.pitch = 0
        self.heading = 0
        self.roll = 0
        self.results = {}
        self.deltat = DeltaT(list(imu_data.keys())[0])
        mag_model = RegressionMagnetometerModel(
            mag_data, list(imu_data.keys()))
        predicted_mag = mag_model.get_predicted_mag()
        self.all_data = {}
        for k, v in imu_data.items():
            self.all_data[k] = {
                'accelerometer': v['accelerometer'],
                'gyroscope': v['gyroscope'],
                'magnetometer': predicted_mag[k]
            }

    def run(self) -> dict:
        """For each timestamp, calculate and store the heading, roll, and pitch, alonside the quaternion represting it's supposed point in space.

        Returns:
            dict: Contains processed data for each timestamp.
        """
        for k, v in self.all_data.items():
            accel = v['accelerometer']
            gyro = v['gyroscope']
            mag = v['magnetometer']
            ts = k
            mx, my, mz = (mag[x] - self.magbias[x]
                          for x in range(3))  # Units irrelevant (normalised)
            ax, ay, az = accel                  # Units irrelevant (normalised)
            gx, gy, gz = (radians(x) for x in gyro)  # Units deg/s
            # short name local variable for readability
            q1, q2, q3, q4 = (self.q[x] for x in range(4))
            # Auxiliary variables to avoid repeated arithmetic
            _2q1 = 2 * q1
            _2q2 = 2 * q2
            _2q3 = 2 * q3
            _2q4 = 2 * q4
            _2q1q3 = 2 * q1 * q3
            _2q3q4 = 2 * q3 * q4
            q1q1 = q1 * q1
            q1q2 = q1 * q2
            q1q3 = q1 * q3
            q1q4 = q1 * q4
            q2q2 = q2 * q2
            q2q3 = q2 * q3
            q2q4 = q2 * q4
            q3q3 = q3 * q3
            q3q4 = q3 * q4
            q4q4 = q4 * q4

            # Normalise accelerometer measurement
            norm = sqrt(ax * ax + ay * ay + az * az)
            if (norm == 0):
                return  # handle NaN
            norm = 1 / norm                     # use reciprocal for division
            ax *= norm
            ay *= norm
            az *= norm

            # Normalise magnetometer measurement
            norm = sqrt(mx * mx + my * my + mz * mz)
            if (norm == 0):
                return                          # handle NaN
            norm = 1 / norm                     # use reciprocal for division
            mx *= norm
            my *= norm
            mz *= norm

            # Reference direction of Earth's magnetic field
            _2q1mx = 2 * q1 * mx
            _2q1my = 2 * q1 * my
            _2q1mz = 2 * q1 * mz
            _2q2mx = 2 * q2 * mx
            hx = mx * q1q1 - _2q1my * q4 + _2q1mz * q3 + mx * q2q2 + \
                _2q2 * my * q3 + _2q2 * mz * q4 - mx * q3q3 - mx * q4q4
            hy = _2q1mx * q4 + my * q1q1 - _2q1mz * q2 + _2q2mx * \
                q3 - my * q2q2 + my * q3q3 + _2q3 * mz * q4 - my * q4q4
            _2bx = sqrt(hx * hx + hy * hy)
            _2bz = -_2q1mx * q3 + _2q1my * q2 + mz * q1q1 + _2q2mx * \
                q4 - mz * q2q2 + _2q3 * my * q4 - mz * q3q3 + mz * q4q4
            _4bx = 2 * _2bx
            _4bz = 2 * _2bz

            # Gradient descent algorithm corrective step
            s1 = (-_2q3 * (2 * q2q4 - _2q1q3 - ax) + _2q2 * (2 * q1q2 + _2q3q4 - ay) - _2bz * q3 * (_2bx * (0.5 - q3q3 - q4q4)
                                                                                                    + _2bz * (q2q4 - q1q3) - mx) + (-_2bx * q4 + _2bz * q2) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my)
                  + _2bx * q3 * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz))

            s2 = (_2q4 * (2 * q2q4 - _2q1q3 - ax) + _2q1 * (2 * q1q2 + _2q3q4 - ay) - 4 * q2 * (1 - 2 * q2q2 - 2 * q3q3 - az)
                  + _2bz * q4 * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (_2bx * q3 + _2bz * q1) * (_2bx * (q2q3 - q1q4)
                                                                                                                      + _2bz * (q1q2 + q3q4) - my) + (_2bx * q4 - _4bz * q2) * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz))

            s3 = (-_2q1 * (2 * q2q4 - _2q1q3 - ax) + _2q4 * (2 * q1q2 + _2q3q4 - ay) - 4 * q3 * (1 - 2 * q2q2 - 2 * q3q3 - az)
                  + (-_4bx * q3 - _2bz * q1) *
                  (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx)
                  + (_2bx * q2 + _2bz * q4) *
                  (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my)
                  + (_2bx * q1 - _4bz * q3) * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz))

            s4 = (_2q2 * (2 * q2q4 - _2q1q3 - ax) + _2q3 * (2 * q1q2 + _2q3q4 - ay) + (-_4bx * q4 + _2bz * q2) * (_2bx * (0.5 - q3q3 - q4q4)
                                                                                                                  + _2bz * (q2q4 - q1q3) - mx) + (-_2bx * q1 + _2bz * q3) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my)
                  + _2bx * q2 * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz))

            # normalise step magnitude
            norm = 1 / sqrt(s1 * s1 + s2 * s2 + s3 * s3 + s4 * s4)
            s1 *= norm
            s2 *= norm
            s3 *= norm
            s4 *= norm

            # Compute rate of change of quaternion
            qDot1 = 0.5 * (-q2 * gx - q3 * gy - q4 * gz) - self.beta * s1
            qDot2 = 0.5 * (q1 * gx + q3 * gz - q4 * gy) - self.beta * s2
            qDot3 = 0.5 * (q1 * gy - q2 * gz + q4 * gx) - self.beta * s3
            qDot4 = 0.5 * (q1 * gz + q2 * gy - q3 * gx) - self.beta * s4

            # Integrate to yield quaternion
            deltat = self.deltat(ts)
            q1 += qDot1 * deltat
            q2 += qDot2 * deltat
            q3 += qDot3 * deltat
            q4 += qDot4 * deltat
            norm = 1 / sqrt(q1 * q1 + q2 * q2 + q3 * q3 +
                            q4 * q4)    # normalise quaternion
            self.q = q1 * norm, q2 * norm, q3 * norm, q4 * norm
            self.heading = self.declination + degrees(atan2(2.0 * (self.q[1] * self.q[2] + self.q[0] * self.q[3]),
                                                            self.q[0] * self.q[0] + self.q[1] * self.q[1] - self.q[2] * self.q[2] - self.q[3] * self.q[3]))
            self.pitch = degrees(-asin(2.0 *
                                 (self.q[1] * self.q[3] - self.q[0] * self.q[2])))
            self.roll = degrees(atan2(2.0 * (self.q[0] * self.q[1] + self.q[2] * self.q[3]),
                                      self.q[0] * self.q[0] - self.q[1] * self.q[1] - self.q[2] * self.q[2] + self.q[3] * self.q[3]))

            self.results[ts] = {
                'heading': self.heading,
                'pitch': self.pitch,
                'roll': self.roll,
                'q': self.q,
            }

        return self.results
