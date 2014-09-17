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
	roll = d.roll(5, 3)
	rollsum = d.sum(roll)
	assert rollsum > 4 and rollsum < 91


def test_dice_lowest():
	roll = d.lowest(d.roll(qty=5))

	assert roll > 1 and roll < 13


def test_random_stats_novice():
	age = 18
	rank = 'Novice'
	stats = d.random_stats(age, rank)

	assert len(stats) is 5

	for die in stats:
		assert die > 1

	age = 16
	stats = d.random_stats(age, rank)

	assert stats is False


def test_random_stats_advanced():
	age = 16
	rank = 'Advanced'
	stats = d.random_stats(age, rank)

	assert stats is False

	age = 22
	stats = d.random_stats(age, rank)
	assert len(stats) is 5


def assert_dice(qty, sets):
	roll = d.roll(qty=qty, sets=sets)

	assert len(roll) is sets

	for dset in roll:
		assert len(dset) is qty

		for die in dset:
			assert die in range(1, 7)
