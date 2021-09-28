import time
import threading
import random
from functools import partial
import smbus
import time
import csv

I2C_ADDRESS = 0x60 #VCNL4035 I2C address, can be found with: i2cdetect -y 1

def i2c_regset(bus, addr,set_bit, clear): 
    reg_val = bus.read_word_data(I2C_ADDRESS, addr)
    new_val = reg_val
    new_val &= ~clear
    new_val |= set_bit
    if reg_val != new_val: 
        bus.write_word_data(I2C_ADDRESS, addr, new_val);

class Sensor(threading.Thread):
    def __init__(self, callbackFunc, running, sensorTimeoutMs):
        print("Sensor thread created")

        threading.Thread.__init__(self) # Initialize the threading superclass
        self.running = running # Store the current state of the Flag
        self.callbackFunc = callbackFunc # Store the callback function
        self.sensorTimeoutMs = sensorTimeoutMs

        bus = smbus.SMBus(1)
        #setup VCNL4035
        bus.write_word_data(I2C_ADDRESS, 0x4, 1<<3|1<<0)
        bus.write_word_data(I2C_ADDRESS, 0x3, 1<<0)
        i2c_regset(bus, 0x3, 1<<1, 1<<0)
        i2c_regset(bus, 0x3, 1<<14|1<<15, 0)

        self.bus = bus

    def run(self):
        print("Sensor thread started")

        started = time.time()
        filename = time.strftime("%Y%m%d-%H%M%S.csv")
        f = open(f'log/{filename}', 'w')
        with f:
            writer = csv.DictWriter(f, fieldnames=['ts_ms', 'ps1', 'ps2', 'ps3'])
            writer.writeheader()

            while self.running.is_set():
                time.sleep(self.sensorTimeoutMs / 1000)
                ps1 = self.bus.read_word_data(I2C_ADDRESS, 0x8)
                ps2 = self.bus.read_word_data(I2C_ADDRESS, 0x9)
                ps3 = self.bus.read_word_data(I2C_ADDRESS, 0xA)

                writer.writerow(dict(ts_ms=int((time.time() - started) * 1e3), ps1=ps1, ps2=ps2, ps3=ps3))
                f.flush()

                self.i2c_regset(0x4, 1<<2, 0)
                self.callbackFunc.doc.add_next_tick_callback(partial(self.callbackFunc.update, [ps1, ps2, ps3]))

        print("Sensor thread killed")

    def i2c_regset(self, addr, set_bit, clear):
        reg_val = self.bus.read_word_data(I2C_ADDRESS, addr)
        new_val = reg_val
        new_val &= ~clear
        new_val |= set_bit
        if reg_val != new_val:
            self.bus.write_word_data(I2C_ADDRESS, addr, new_val);

