# gesture_VCNL4035
Vishay Gesture sensor VCNL4035X01 test

This programm uses linux system calls to access I2C bus from linux user space. System calls are how a programm enters the kernel to perform some task
x86-64 CPUs have concept called privilege levels. The kernel runs at the most privileged level, called “Ring 0”. User programs run at a lesser level, typically “Ring 3”.
To run this code on raspberry:
1.enable I2C (sudo raspi-config);
2.sudo apt-get install i2c-tools
3.sudo apt-get update
4.sudo apt-get install libi2c-dev

You can test I2C bus:
>ls /dev/*i2c* 
sudo i2cdetect -y x //search for all I2C devices on bus and returns addresses. x= 0 or 1. 
sudo i2cget -y x [device addr] [register addr] 




Useful links:
https://www.kernel.org/doc/Documentation/i2c/dev-interface
https://elinux.org/Interfacing_with_I2C_Devices
https://raspberry-projects.com/pi/programming-in-c/i2c/using-the-i2c-interface
