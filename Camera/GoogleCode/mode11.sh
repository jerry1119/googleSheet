i2cset -f -y 0 0x15 0x00 0x80 i #Set Mode register, to allow auto increment
i2cset -f -y 0 0x15 0x81 0x05 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF i #values for mode 10 for all LEDs
i2cset -f -y 0 0x17 0x00 0x80 i #Set Mode register, to allow auto increment
i2cset -f -y 0 0x17 0x81 0x05 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF i #values for mode 10 for all LEDs