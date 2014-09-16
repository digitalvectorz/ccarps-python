#! /usr/bin/env python
# -*- coding: utf-8 -*-
import heapq
from random import randint


class Dice:
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

	def rank_check(self, age, rank):
		'''
		Simply returns if age is valid for rank.
		'''
		if rank is 'Beginner':
			if age is not None:
				return True

		if rank is 'Novice':
			if age > 17:
				return True

		if age > 20:
			if rank is 'Advanced' or rank is 'Heroic' or rank is 'Epic' or rank is 'Legendary':
				return True

		return False

	def random_stats(self, age, rank=None):
		'''
		Needs to encompass both Options A and B
		https://github.com/WizardSpire/ccarps/blob/master/CharacterCreation.md
		'''

		# Setting default values.
		reroll_on = 0
		dice_sets = 1 

		dice_qty = self.by_age(age)
		rank_check = self.rank_check(age, rank)

		if rank_check is not True:
			return rank_check
			
		if rank is 'Beginner':
			dice_sets = 5
		
		if rank is 'Novice' and age > 17:
			dice_sets = 5
			reroll_on = 1
		
		if age > 20:
			if rank is 'Advanced':
				dice_sets = 6
		
			if rank is 'Heroic':
				dice_sets = 6
				reroll_on = 1
		
			if rank is 'Epic':
				dice_sets = 8
		
			if rank is 'Legendary':
				dice_sets = 10

		if reroll_on is 1:
			roll = self.roll(qty=dice_qty, sets=dice_sets, rerollone=reroll_on)
		else:
			roll = self.roll(qty=dice_qty, sets=dice_sets)

		roll = sorted(roll)
		stat_candidates = [roll[-1], roll[-2], roll[-3], roll[-4], roll[-5]]
		sums = []

		for candidate in stat_candidates:
			sums.append(sum(candidate))

		return sums
