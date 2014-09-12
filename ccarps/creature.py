#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ccarps import dice


class Creature:
	'''
	Set up us the Creature! (Monsters, (N)PCs)
	type = 'Novice', 'Beginner', 'Adventurer', 'Master'
	'''
	def __init__(self, type='empty', name=None):
		if isinstance(type, str):
			base = dice.random_stats(type)
		else:
			return 'Invalid attribute argument.'

		self.dice = dice.Dice()

		self.name = 'Creature'  # This should really be generated or input.

		if name is not None:
			self.name = name

		self.STR = int(base[0])
		self.DEX = int(base[1])
		self.CON = int(base[2])
		self.INT = int(base[3])
		self.WILL = int(base[4])
		
		self.health = {
			'mental': 10,
			'physical': 10,
			'spritual': 10
		}
		
		self.max_health = {
			'mental': 10,
			'physical': 10,
			'spritual': 10
		}

		self.roll = 0
		self.CHR = (self.CON + self.INT + self.WILL) / 3
		self.SPD = (self.STR + self.DEX) / 2
		self.RFX = (self.STR + self.DEX + self.WILL) / 3
		self.LFT = (self.STR + self.WILL) / 2
		self.PER = (self.INT + self.WILL) / 2

		self.skills = {}  # Should load from a JSON file or sommat.

	def action(skill, base_tn):
		'''
		Action handler, be it combat, using skill, or trying
		to stop from falling out of an airship...
		'''

		'''
		action_mod = 0
		num_dice = 2
		tn = base_tn + action_mod

		if skill in self.skills:
			skill_mod = modifier.find(self.skills[skill]['level'])
			num_dice = 2 + modifier.dice(skill_mod)

		roll = self.dice.roll(qty=num_dice)
		lowest = self.dice.low(roll)


		if lowest < tn:
			success = 1
		'''

	def take_damage(self, damage, type):
		if damage > 0:
			new_dmg = self.health[type] - damage
			if new_dmg <= 0:
				if self.health[type] == 'mental':
					self.health[type] = 0
					self.health['physical'] += new_dmg
				if self.health[type] == 'physical':
					self.health[type] = 0
					self.health['spiritual'] += new_dmg
				if self.health[type] == 'spiritual':
					self.health[type] = new_dmg

	def heal(self, amount, type):
		self.health[type] += amount
		if self.health[type] > self.max_health[type]:
			self.health[type] = self.max_health[type]

	def distance(points):
		'''
		Range/Reach in feet.
		0 = 3 ft, 1 = 6 ft, [...]
		'''
		return 3 + (points * 3)
