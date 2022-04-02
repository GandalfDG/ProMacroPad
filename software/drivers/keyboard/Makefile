obj-m := matrix_keypad.o

all:
	make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -C /home/root/kernel M=`pwd` modules

clean:
	make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- -C /home/root/kernel M=`pwd` clean

