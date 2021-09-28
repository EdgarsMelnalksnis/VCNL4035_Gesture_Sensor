import time
import datetime
import smbus
I2C_ADDRESS= 0x60 #VCNL4035 I2C address, can be found with: i2cdetect -y 1
bus = smbus.SMBus(1)

def i2c_dump_reg():
    for i in range (0,0xf):
        print "%02x:%04X" % (i,bus.read_word_data(I2C_ADDRESS,i))

def i2c_regset(addr,set_bit, clear): 
    reg_val = bus.read_word_data(I2C_ADDRESS,addr)
    new_val = reg_val
    new_val &= ~clear
    new_val |= set_bit
    if reg_val != new_val: 
        bus.write_word_data(I2C_ADDRESS,addr,new_val);
        
#setup VCNL4035
bus.write_word_data(I2C_ADDRESS,0x4,1<<3|1<<0)
bus.write_word_data(I2C_ADDRESS,0x3,1<<0)

i2c_regset(0x3,1<<1,1<<0)
i2c_regset(0x3,1<<14|1<<15,0)

#for time reference
time_now=datetime.datetime.now()
#dump all registers
i2c_dump_reg()
while True:
    time_us=datetime.datetime.now()-time_now
    print "%04d:%04d:%04d:%04d" % (time_us.microseconds,bus.read_word_data(I2C_ADDRESS,0x8),bus.read_word_data(I2C_ADDRESS,0x9),bus.read_word_data(I2C_ADDRESS,0xA))
    #triggers new PS reading
    i2c_regset(0x4,1<<2,0)
    #adjust for better performance/response
    time.sleep(0.001)
