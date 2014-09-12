#! /usr/bin/env python
# -*- coding: utf-8 -*-
import heapq
import random


age_table = {
	1: [0, 1, 2, 3, 4, 5],
	2: [6, 7, 8, 9, 10],
	3: [11, 12, 13, 14, 15],
	4: [16, 17, 18, 19, 20],
	5: [21]
}


class Dice:
	def roll(self, type=6, qty=1, sets=1):
		'''
		Rolls qty of type of dice in sets.
		Returns: List of dice set(s).
		'''
		counts = []
		for s in range(sets):
			count = []
			for n in range(qty):
				roll = random.randint(1, type)
				count += [roll]
			counts.append(count)
		return counts

	def low(self, list, qty=2):
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

	def sum(self, type=6, qty=1, sets=1):
		'''
		Same as self.roll but returns the grand total.
		'''
		dicerolls = self.roll(type, qty, sets)
		total = 0
		for dice in dicerolls:
			for d in dice:
				total += d
		return total

	def random_stats(self, age, rank=None):
		'''
		Needs to encompass both Options A and B
		https://github.com/WizardSpire/ccarps/blob/master/CharacterCreation.md
		'''
		for i in age_table:
			if age in age_table[i]:
				if age >= 21:
					dice_qty = 5
				dice_qty = age_table[i]

		if rank is not None:
			reroll_on = 0
			if rank == 'Beginner':
				dice_sets = 5
			if rank == 'Novice' and age >= 18:
				dice_sets = 5
				reroll_on = 1
			if age > 21:
				if rank == 'Advanced':
					dice_sets = 6
				if rank == 'Heroic':
					dice_sets = 6
					reroll_on = 1
				if rank == 'Epic':
					dice_sets = 8
				if rank == 'Legendary':
					dice_sets = 10

		if reroll_on is 1:
			i = dice_sets
			i = 0

		i = 0
		base_stats = []
		while i < 5:
			base_stats.append(self.sum(qty=dice_qty))
			i += 1
		return base_stats
