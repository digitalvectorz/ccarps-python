#! /usr/bin/env python
# -*- coding: utf-8 -*-
from ccarps import dice


d = dice.Dice()


def test_dice_roll():
	assert_dice(qty=1, sets=1)


def test_dice_roll_one_set_two():
	assert_dice(qty=2, sets=1)


def test_dice_roll_five():
	assert_dice(qty=5, sets=5)


def test_dice_roll_sum():
	roll = d.roll(qty=5, sets=3)
	rollsum = d.sum(roll)

	assert rollsum in range(15, 91)


def test_dice_lowest():
	roll = d.lowest(d.roll(qty=5))

	assert roll > 1 and roll < 13


def assert_dice(qty, sets):
	roll = d.roll(qty=qty, sets=sets)

	assert len(roll) is sets

	for dset in roll:
		assert len(dset) is qty

		for die in dset:
			assert die in range(1, 7)
