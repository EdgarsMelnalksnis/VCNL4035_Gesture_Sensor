/*
 * Simple I2C example
 *
 * Copyright 2017 Joel Stanley <joel@jms.id.au>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 */

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <err.h>
#include <errno.h>

#include <linux/types.h>
#include <linux/i2c.h>
#include <linux/i2c-dev.h>

#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include "time.h"

#define BIT(n) 1u<<n
#define BITL(b)	BIT(b)
#define BITH(b)	BIT(8 + b)

#define DEV_ADDR 0x60


static void i2c_dump_reg(int);
static void i2c_regset(int,uint8_t,uint16_t,uint16_t);
void ms_delay(uint32_t);
static inline __s32 i2c_smbus_access(int file, char read_write, __u8 command,
                                     int size, union i2c_smbus_data *data)
{
	struct i2c_smbus_ioctl_data args;

	args.read_write = read_write;
	args.command = command;
	args.size = size;
	args.data = data;
	return ioctl(file,I2C_SMBUS,&args);
}


static inline __s32 i2c_smbus_read_word_data(int file, __u8 command)
{
	union i2c_smbus_data data;
	uint16_t i2c_data;
	if (i2c_smbus_access(file,I2C_SMBUS_READ,command,
	                     I2C_SMBUS_WORD_DATA,&data))
		return -1;
	else
	{

	return data.word;
}
}


static inline int i2c_smbus_write_word_data(int file, __u8 command,uint16_t value)
{
	union i2c_smbus_data data;
	uint16_t i2c_data;
	data.word=value;
	if (i2c_smbus_access(file,I2C_SMBUS_WRITE,command,
	                     I2C_SMBUS_WORD_DATA,&data))
		{
			return -1;
		}
		else 
		return 0;
}


enum vcnl4035_regs {
	ALS_CONF = 0,	// 0x0
	ALS_THDH,	// 0x1
	ALS_THDL,	// 0x2
	PS_CONF,	// 0x3
	PS_CONF_MS,	// 0x4
	PS_CANC,	// 0x5
	PS_THDL,	// 0x6
	PS_THDH,	// 0x7
	PS1_DATA,	// 0x8
	PS2_DATA,	// 0x9
	PS3_DATA,	// 0xa
	ALS_DATA,	// 0xb
	WHITE_DATA,	// 0xc
	INT_FLAG,	// 0xd
	ID,		// 0xe
};




int main()
{
	uint8_t  addr = DEV_ADDR, reg[0xf] ={0};// 0xe;
	uint16_t data=0;
	const char *path = "/dev/i2c-1";
	int file, rc;

	

	file = open(path, O_RDWR);
	if (file < 0)
		err(errno, "Tried to open '%s'", path); 

	rc = ioctl(file, I2C_SLAVE, addr);
	if (rc < 0)
		err(errno, "Tried to set device address '0x%02x'", addr);

	i2c_smbus_write_word_data(file,PS_CONF_MS,BIT(0) | BIT(3));
	i2c_smbus_write_word_data(file,PS_CONF,BIT(0));
	i2c_smbus_write_word_data(file,ALS_CONF,(2 << 5));
	i2c_smbus_write_word_data(file,PS_THDL,0x1ff);
	i2c_regset(file,PS_CONF,BIT(1),BIT(0));
	i2c_regset(file,PS_CONF, BITH(6)|BITH(7), 0);//enable gesture mode
	i2c_dump_reg(file);
	

while(1)
{
	printf("%d:%d:%d:%d\n",clock(),i2c_smbus_read_word_data(file,PS1_DATA),i2c_smbus_read_word_data(file,PS2_DATA),i2c_smbus_read_word_data(file,PS3_DATA));
	i2c_regset(file,PS_CONF_MS,BIT(2) ,0);//PS_TRIG
	ms_delay(100);
	
}



}

static void i2c_dump_reg(int i2c_file)
{
	for(int i =0; i<0xf;i++)
{
	
	printf("%02x:0x%04x\n",i,i2c_smbus_read_word_data(i2c_file,i));
}
}

static void i2c_regset(int file,uint8_t addr, uint16_t set, uint16_t clear) {
	uint16_t reg_val, new_val;
	reg_val = i2c_smbus_read_word_data(file,addr);//i2c.read(&i2c, addr);
	new_val = reg_val;
	new_val &= ~clear;
	new_val |= set;
	if (reg_val != new_val) 
		i2c_smbus_write_word_data(file,addr,new_val);
		
}

void ms_delay(uint32_t msec)
{
	
	clock_t start_time= clock();
	while( clock() < start_time + msec)
	{
		
	}
	  
}
