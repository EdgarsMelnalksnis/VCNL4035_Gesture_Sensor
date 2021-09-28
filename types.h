#ifndef __TYPES_H__
#define __TYPES_H__

typedef unsigned char uint8_t;
typedef unsigned short uint16_t;

#ifdef DEBUG
#define debug(...)	printf(__VA_ARGS__);
#else
#define debug(...)
#endif

#endif
