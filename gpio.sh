#!/usr/bin/env bash
# -*- coding: utf-8 -*-
"""
@author: jantinus
"""
# GPIO Valve 1
echo 4 > /sys/class/gpio/export
# GPIO Valve 2
echo 5 > /sys/class/gpio/export
# GPIO Valve 3
echo 6 > /sys/class/gpio/export
# GPIO Valve 4
echo 12 > /sys/class/gpio/export
# GPIO Valve 5
echo 13 > /sys/class/gpio/export
# GPIO Valve 6
echo 16 > /sys/class/gpio/export
# GPIO Valve 7
echo 17 > /sys/class/gpio/export
# GPIO Valve 8
echo 18 > /sys/class/gpio/export
# GPIO Valve 9
echo 19 > /sys/class/gpio/export
# GPIO Valve 10
echo 20 > /sys/class/gpio/export
# GPIO Valve 11
echo 21 > /sys/class/gpio/export
# GPIO Valve 12
echo 22 > /sys/class/gpio/export
# GPIO Valve 13
echo 23 > /sys/class/gpio/export
# GPIO Valve 14
echo 24 > /sys/class/gpio/export
# GPIO Valve 15
echo 26 > /sys/class/gpio/export
# GPIO Valve 16
echo 27 > /sys/class/gpio/export

echo out > /sys/class/gpio/gpio4/direction
echo out > /sys/class/gpio/gpio5/direction
echo out > /sys/class/gpio/gpio6/direction
echo out > /sys/class/gpio/gpio12/direction
echo out > /sys/class/gpio/gpio13/direction
echo out > /sys/class/gpio/gpio16/direction
echo out > /sys/class/gpio/gpio17/direction
echo out > /sys/class/gpio/gpio18/direction
echo out > /sys/class/gpio/gpio19/direction
echo out > /sys/class/gpio/gpio20/direction
echo out > /sys/class/gpio/gpio21/direction
echo out > /sys/class/gpio/gpio22/direction
echo out > /sys/class/gpio/gpio23/direction
echo out > /sys/class/gpio/gpio24/direction
echo out > /sys/class/gpio/gpio26/direction
echo out > /sys/class/gpio/gpio27/direction

exit