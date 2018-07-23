#!/usr/bin/python

import pygame
import smbus
import time

# name register addresses as constants
POWER_MGMT_1 = 0x6b
POWER_MGMT_2 = 0x6c

GYRO_REGISTER_START = 0x43

GYRO_ADDR = 0x68

TCA_ADDR = 0x70

soundfile = "/home/pi/progs/robotarm/sounds/motor.wav"
bus = smbus.SMBus(1)


def twos_compliment (value):
    # returns the twos compliment of value must have 2 bytes max

    if (value >= 0x8000):
        return - ((65535 - value) + 1)
    else:
        return value


def get_gyros (device):
    # returns the scaled gyro values of all three axis of the address in device

    raw_gyro = bus.read_i2c_block_data(device, GYRO_REGISTER_START, 6)

    x = twos_compliment((raw_gyro[0] << 8) + raw_gyro[1]) / 131.0
    y = twos_compliment((raw_gyro[2] << 8) + raw_gyro[3]) / 131.0
    z = twos_compliment((raw_gyro[4] << 8) + raw_gyro[5]) / 131.0

    return x,y,z


def get_offset_gyros (device):
    # determines the avergae drift of the gyros 

    sum_x = 0.0
    sum_y = 0.0
    sum_z = 0.0

    for i in range(100):
        x, y, z = get_gyros(device)
        sum_x += x
        sum_y += y
        sum_z += z
        time.sleep(0.01)

    return sum_x / 100, sum_y / 100, sum_z / 100


def set_tca_channel (channel):
    ''' selects the channel to communicate to a value between 0 and 7 channel 0 is 0b00000001
        channel 1 0b00000010
    '''
    if channel > 7:
        return
    bus.write_byte(TCA_ADDR, 1 << channel)


# set tca to channel 0 and wake gyrometer
set_tca_channel (0)
bus.write_byte_data(GYRO_ADDR, POWER_MGMT_1, 0)

# will only be executed if program is called from commandline, not imported
if __name__ == "__main__":
    
    pygame.mixer.init()
    pygame.mixer.music.load(soundfile)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.pause()
    d_x, d_y, d_z = get_offset_gyros(GYRO_ADDR)

    while True:
        g_x, g_y, g_z = get_gyros(GYRO_ADDR)
        print g_x, g_y, g_z
        if (g_z - d_z > 5.0 or g_z - d_z < -5.0 ):
            if True: #not pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
        else:
            if True: #pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
        time.sleep(0.01)

