#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ccarps import dice, modifier


class Creature:
	'''
	Set up us the Creature! (Monsters, (N)PCs)
	type = 'Novice', 'Beginner', 'Adventurer', 'Master'
	'''
	def __init__(self, rank='empty', name=None):
		# Initialize dice system
		self.dice = dice.Dice()
		self.roll = 0

		# Dead: 0 = Alive, 1 = Dead, 2 = Undead/Other
		self.dead = 0

		# Randomly generate a creature based on rank passed.
		if isinstance(rank, str):
			base = self.dice.random_stats(rank)
		else:
			return 'Invalid attribute argument.'

		# Default name if none is presented.
		self.name = 'Unnamed Creature'
		if name is not None:
			self.name = name

		# Primary Stats
		self.STR = int(base[0])
		self.DEX = int(base[1])
		self.CON = int(base[2])
		self.INT = int(base[3])
		self.WILL = int(base[4])

		# Secondary Stats
		self.CHR = (self.CON + self.INT + self.WILL) / 3
		self.SPD = (self.STR + self.DEX) / 2
		self.RFX = (self.STR + self.DEX + self.WILL) / 3
		self.LFT = (self.STR + self.WILL) / 2
		self.PER = (self.INT + self.WILL) / 2
		
		# Setting max health allows for modified health bars
		self.max_health = {
			'mental': 10,
			'physical': 10,
			'spiritual': 10
		}

		# Set initial health as full.
		self.health = self.max_health

		# Here's the skill handler dictionary.
		self.skills = {
			'some skill': 0
		}

	def action(skill, base_tn):
		'''
		Action handler for combat, using skill, or trying
		to stop from falling out of an airship...
		'''

		# Set the default action modifier and number of dice
		# and set the default success to fail.
		success = 0
		action_mod = 0
		num_dice = 2
		tn = base_tn + action_mod

		if skill in self.skills:
			skill_mod = modifier.find(self.skills[skill])
			num_dice = 2 + modifier.dice(skill_mod)

		roll = self.dice.roll(qty=num_dice)
		lowest = self.dice.low(roll)

		if lowest < tn:
			success = 1

		return success

	def take_damage(self, damage, type):
		'''
		Take damage. If any damage is greater than 10, move to
		the next health type. If all three are 0, set dead = True
		'''
		# Catch any invalid health types and return with list of available.
		if type not in self.health:
			return "Invalid damage type. Available: %s" % ', '.join(self.health)

		# Apply initial damage to approriate type
		self.health[type] -= damage
		# If specified health type is zeror or above, return
		if self.health[type] >= 0:
			return

		# If negative number, set value to 0
		# Set damage to equal the negative remainder,
		# and reverse it to positive.
		if self.health[type] < 0:
			damage = -self.health[type]
			self.health[type] = 0

			# Apply damage to the next health type.
			if type is 'mental':
				self.take_damage(damage, 'physical')
			if type is 'physical':
				self.take_damage(damage, 'spiritual')
			if type is 'spiritual':
				self.dead = 1

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
