#!/usr/bin/env python
# -*- coding: utf-8 -*-

# base (2+dice_mod)d6
# level: mod
dice_mod = {
	1: 0,
	6: 1,
	12: 2,
	18: 3
}
inv_dice_mod = {
	1: 3,
	6: 2,
	12: 1,
	18: 0
}


def get(level):
	if level < 0:
		return 0
	if 1 <= level <= 2:
		return 1
	if 3 <= level <= 5:
		return 2
	if 6 <= level <= 9:
		return 3
	if 10 <= level <= 14:
		return 4
	if 15 <= level <= 20:
		return 5
	if 21 <= level <= 27:
		return 6
	if 28 <= level <= 35:
		return 7
	if level is 36:
		return 8
	return 0


def dice(mod, invert=0):
	if not isinstance(mod, int) or mod > 8 or mod is 0:
		return 0

	dmod = dice_mod
	
	if invert is 1:
		dmod = inv_dice_mod
	for mod in dmod:
		if mod <= dmod[mod]:
			return mod


def next(level):
	if get(level) < 8 and get(level) is not 0:
		return get(level) + 1
	return 0
