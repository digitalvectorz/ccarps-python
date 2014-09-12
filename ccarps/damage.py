#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Numbers are 2d6
hit_chart = {
	'head': 2,
	'chest': [3, 4],
	'upper back': [3, 4],
	'abdomen': [5, 6, 7],
	'lower back': [5, 6, 7],
	'leg': [8, 9],
	'arm': [10, 11],
	'neck': [12],
	'buttocks': [12],
	'groin': [12]
}


def called_shot():
	stuff = 1
	if stuff:
		stuff = "do"
	return stuff
