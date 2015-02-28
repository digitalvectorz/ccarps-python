#! /usr/bin/env python
# -*- coding: utf-8 -*-
import heapq
from random import randint


class Dice(object):
	def __init__(self):
		self.roll()

	def roll(self, type=6, qty=1, sets=1, rerollone=0):
		'''
		Rolls qty of type of dice in sets.
		Returns: List of dice set(s).
		'''
		counts = []
		for s in range(sets):
			count = []
			for n in range(qty):
				roll = randint(1, type)
				if rerollone is 1 and roll < 2:
					self.roll(qty=1, rerollone=1)
				count += [roll]
			counts.append(count)
		return counts

	def lowest(self, list, qty=2):
		'''
		Returns the lowest qty dice in a roll set.
		Default: Two lowest dice.
		'''
		twolowest = []
		for s in list:
			twolows = heapq.nsmallest(qty, s)
			twolows = sum(twolows)
			twolowest += [twolows]
		return min(twolowest)

	def sum(self, dicesets):
		'''
		Sums up all dice sets.
		'''
		total = 0
		for dice in dicesets:
			for d in dice:
				total += d
		return total

	def by_age(self, age):
		'''
		Returns number of dice to roll.
		'''
		if age > 20:
			return 5
		if age < 21 and age > 15:
			return 4
		if age < 21 and age > 10:
			return 3
		if age < 11 and age > 5:
			return 2
		if age < 6:
			return 1

	def random_stats(self, age):
		'''
		https://github.com/WizardSpire/ccarps/blob/master/Character_Creation.md
		'''

		dice_qty = self.by_age(age)
		dice_sets = 5
		
		roll = self.roll(qty=dice_qty, sets=dice_sets)
		roll = sorted(roll)

		stat_candidates = [roll[-1], roll[-2], roll[-3], roll[-4], roll[-5]]
		sums = []

		for candidate in stat_candidates:
			sums.append(sum(candidate))

		return sums
