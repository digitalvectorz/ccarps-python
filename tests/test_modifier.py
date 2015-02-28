#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ccarps import modifier


def test_get_mod():
	ret = modifier.get(15)
	assert ret is 5


def test_find_mod_invalid():
	ret = modifier.get(37)
	assert ret is 0


def test_next_mod():
	ret = modifier.next(15)
	assert ret is 6


def test_next_mod_invalid():
	ret = modifier.next(39)
	assert ret is 0


def test_dice_mod():
	mod = modifier.get(15)
	ret = modifier.dice(mod)
	assert ret is None


def test_dice_mod_invalid():
	mod = modifier.get(37)
	ret = modifier.dice(mod)
	assert ret is 0


def test_inverted_dice_mod():
	mod = modifier.get(22)
	ret = modifier.dice(mod, invert=1)
	assert ret is 1


def test_inverted_dice_mod_invalid():
	ret = modifier.dice(37, invert=1)
	assert ret is 0
