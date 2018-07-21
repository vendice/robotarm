#!/usr/bin/python

import time
import unittest
import robotarm

class RobotArmTest(unittest.TestCase):
    
    def test_gyro_minus_drift_range(self):
        # test the range of the gyro data minus drift offset

        d_x, d_y, d_z = robotarm.get_offset_gyros(robotarm.GYRO_1)
        
        for i in range(100):
            g_x, g_y, g_z = robotarm.get_gyros(robotarm.GYRO_1)
            self.assertTrue(-1.0 < g_x - d_x and g_x - d_x < 1.0)
            self.assertTrue(-1.0 < g_y - d_y and g_y - d_y < 1.0)
            self.assertTrue(-1.0 < g_z - d_z and g_z - d_z < 1.0)
            time.sleep(0.1)


if __name__ == '__main__':
    unittest.main()
