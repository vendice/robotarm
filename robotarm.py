#!/usr/bin/python

import pygame
import smbus
import time

# name register addresses as constants
POWER_MGMT_1 = 0x6b
POWER_MGMT_2 = 0x6c

GYRO_REGISTER_START = 0x43

GYRO_1 = 0x68

soundfile = "/home/pi/progs/robotarm/sounds/robot.wav"
bus = smbus.SMBus(1)


def twos_compliment (value):
    # returns the twos compliment of value must have 2 bytes max

    if (value >= 0x8000):
        return - ((65535 - value) + 1)
    else:
        return value


def read_gyro (device):
    # returns the scaled gyro values of all three axis of the address in device

    raw_gyro = bus.read_i2c_block_data(device, GYRO_REGISTER_START, 6)

    x = twos_compliment((raw_gyro[0] << 8) + raw_gyro[1]) / 131.0
    y = twos_compliment((raw_gyro[2] << 8) + raw_gyro[3]) / 131.0
    z = twos_compliment((raw_gyro[4] << 8) + raw_gyro[5]) / 131.0

    return x,y,z


# wake gyrometer
bus.write_byte_data(GYRO_1, POWER_MGMT_1, 0)

gyro_1_x, gyro_1_y, gyro_1_z = read_gyro(GYRO_1)

print gyro_1_x, gyro_1_y, gyro_1_z


