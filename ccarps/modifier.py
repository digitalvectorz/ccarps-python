#!/usr/bin/env python
# -*- coding: utf-8 -*-
mod_table = {
	1: [1, 2],
	2: [3, 4, 5],
	3: [6, 7, 8, 9],
	4: [10, 11, 12, 13, 14],
	5: [15, 16, 17, 18, 19, 20],
	6: [21, 22, 23, 24, 25, 26, 27],
	7: [28, 29, 30, 31, 32, 33, 34, 35],
	8: [36]
}

# base (2+dice_mod)d6
# level: mod
dice_mod = {
	1: 0,
	6: 1,
	12: 2,
	18: 3
}

max_dice_mod = 3

inv_dice_mod = {
	1: 3,
	6: 2,
	12: 1,
	18: 0
}

max_mod = len(mod_table)
top_level_pos = len(mod_table[max_mod])
max_level = mod_table[max_mod][top_level_pos - 1]


def dice(mod, invert=0):
	if not isinstance(mod, int) or mod > 8:
		return 'Invalid mod number.'

	dmod = dice_mod
	
	if invert is 1:
		dmod = inv_dice_mod
	for mod in dmod:
		if mod <= dmod[mod]:
			return mod


def find(level):
	'''
	Find the level in mod_table.
	Coerce level to int, just in case.
	'''
	if level > max_level:
		return 'Invalid level'
	for i in mod_table:
		if int(level) in mod_table[i]:
			return i


def next(level):
	if level <= max_level:
		cur_mod = find(level)
		if cur_mod > max_mod:
			return None

		return cur_mod + 1
