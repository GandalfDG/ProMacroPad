#! /bin/bash

# build the 32-bit config for Pi1, Zero and Zero W
# from https://www.raspberrypi.com/documentation/computers/linux_kernel.html#32-bit-configs
cd kernel
KERNEL=kernel
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcmrpi_defconfig

make -j12 ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- zImage modules dtbs
