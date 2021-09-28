#ifndef __VCNL4035_H__
#define __VCNL4035_h__

//#define DEBUG
#include "types.h"

#define BITL(b)	BIT(b)
#define BITH(b)	BIT(8 + b)

void vcnl4035_init(void);
void vcnl4035_deinit(void);

enum {
	GESTURE_NONE = 0,
	GESTURE_LEFT,
	GESTURE_RIGHT,
	GESTURE_UP,
	GESTURE_DOWN,
};

int vcnl4035_get_gesture_stat(char **name);
int vcnl4035_get_gesture_pat(char **name);

#endif
