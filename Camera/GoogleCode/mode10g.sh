i2cset -f -y 0 0x15 0x40 0xFF i #Set all IREF values
i2cset -f -y 0 0x15 0x00 0x80 i #Set Mode register, to allow auto increment
i2cset -f -y 0 0x15 0x81 0x05 0x08 0x82 0x20 0x08 0x02 0x00 i #values for mode10g
i2cset -f -y 0 0x17 0x40 0xFF i #Set all IREF values
i2cset -f -y 0 0x17 0x00 0x80 i #Set Mode register, to allow auto increment
i2cset -f -y 0 0x17 0x81 0x05 0x08 0x28 0x80 0x20 0x08 0x00 i #values for mode10g