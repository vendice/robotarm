#!/usr/bin/python

import time
import unittest
import robotarm

class RobotArmTest(unittest.TestCase):
    
    def test_gyro_minus_drift_range(self):
        # test the range of the gyro data minus drift offset

        d_x, d_y, d_z = robotarm.get_offset_gyros(robotarm.GYRO_ADDR)
        
        for i in range(100):
            g_x, g_y, g_z = robotarm.get_gyros(robotarm.GYRO_ADDR)
            self.assertTrue(-1.0 < g_x - d_x and g_x - d_x < 1.0)
            self.assertTrue(-1.0 < g_y - d_y and g_y - d_y < 1.0)
            self.assertTrue(-1.0 < g_z - d_z and g_z - d_z < 1.0)
            time.sleep(0.1)


    def test_read_gyros(self):
        # test whether you can access the data of both gyros 
        
        for i in range(300):
            print "move gyro 1 and gyro 2: "
            g_1_x, g_1_x, g_1_x = robotarm.get_gyros(robotarm.GYRO_ADDR)
            robotarm.set_tca_channel(1)
            g_2_x, g_2_x, g_2_x = robotarm.get_gyros(robotarm.GYRO_ADDR)
            print "Gyro 1:"
            print "x: " + d_1_x 
            print "y: " + d_1_y
            print "z: " + d_1_z
            print "****************************"
            print "Gyro 2:"
            print "x: " + d_2_x 
            print "y: " + d_2_y
            print "z: " + d_2_z
            sleep(0.01)




if __name__ == '__main__':
    unittest.main()
