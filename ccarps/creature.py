#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ccarps import dice, modifier

# Covers:
# * https://github.com/WizardSpire/ccarps/blob/master/CharacterCreation.md
# * https://github.com/WizardSpire/ccarps/blob/master/Combat.md
class Creature:
	'''
	Set up us the Creature! (Monsters, (N)PCs)
	'''
	def __init__(self, age=None, rank=None, name=None):
		# Initialize dice system
		self.dice = dice.Dice()
		self.roll = 0
	
		# Dead: -1 = undead, 0 = dead, 1 = alive(normal), 2 = alive(polymorphed)
		self.status = 1

		# Some defaults so that if creature.Creature() is invoked,
		# a generic 21 year old human Novice will be created.
		self.age = 21
		self.rank = 'Novice'
		self.name = 'Unnamed Human'

		# Override the defaults if any parameters are passed.
		if age is not None:
			self.age = age
		if rank is not None:
			self.rank = rank
		if name is not None:
			self.name = name

		# https://github.com/WizardSpire/ccarps/blob/master/CharacterCreation.md#starting-points
		base = self.dice.random_stats(age=self.age, rank=self.rank)

		# Setting max health allows for modified health bars
		self.max_health = {
			'mental': 10,
			'physical': 10,
			'spiritual': 10
		}

		# Set initial health as full.
		self.health = {
			'mental': 10,
			'physical': 10,
			'spiritual': 10
		}

		# Set the initial stun timer.
		self.stun_timer = 0

		# Primary Attributes
		# https://github.com/WizardSpire/ccarps/blob/master/CharacterCreation.md#primary-attributes
		self.STR = base[0]
		self.DEX = base[1]
		self.CON = base[2]
		self.INT = base[3]
		self.WIL = base[4]

		# Secondary Attributes
		# https://github.com/WizardSpire/ccarps/blob/master/CharacterCreation.md#secondary-attributes
		self.CHR = (self.CON + self.INT + self.WIL) / 3
		self.SPD = (self.STR + self.DEX) / 2
		self.RFX = (self.STR + self.DEX + self.WIL) / 3
		self.LFT = (self.STR + self.WIL) / 2
		self.PER = (self.INT + self.WIL) / 2

		# https://github.com/WizardSpire/ccarps/blob/master/CharacterCreation.md#prestige-prejudice-and-oddities
		self.prestige = {}
		self.prejudice = {}
		self.oddities = {}

		# Denotes which wealth "class" (if any) the creature is from.
		# 0 is average/middle, and this is not always needed in every
		# game or world setting.
		#
		# Influence dictates followers / contacts, but again, is not
		# necessary for all game types.
		# https://github.com/WizardSpire/ccarps/blob/master/CharacterCreation.md#wealth-and-influence
		self.wealth = 0
		self.influence = 0

		# Here's the skill handler dictionary.
		# https://github.com/WizardSpire/ccarps/blob/master/CharacterCreation.md#skills
		self.skills = {}

		# Creature's appearance!
		# https://github.com/WizardSpire/ccarps/blob/master/CharacterCreation.md#character-appearance
		self.appearance = {}
		self.background = {}

		self.points = {
			'spent': 0,
			'unspent': 0,
			'total': 0
		}

		# https://github.com/WizardSpire/ccarps/blob/master/TechLevels.md
		self.tech_level = 0

	def action(self, skill, base_tn):
		'''
		Action handler for combat, using skill, or trying
		to stop from falling out of an airship...
		'''

		# Set the default action modifier and number of dice
		action_mod = 0
		num_dice = 2
		tn = base_tn + action_mod

		if skill in self.skills:
			skill_mod = modifier.find(self.skills[skill])
			num_dice = 2 + modifier.dice(skill_mod)

		roll = self.dice.roll(qty=num_dice)
		lowest = self.dice.low(roll)

		if lowest < tn:
			return lowest

	def take_damage(self, damage, type):
		'''
		Take damage. If any damage is greater than 10, move to
		the next health type. If all three are 0, set status to 0.

		Returns nothing on success, as it directly modifies self.health.
		'''
		# Catch any invalid health types and return with list of available.
		if type not in self.health:
			return "Invalid damage type. Available: %s" % ', '.join(self.health)

		# Apply initial damage to approriate type
		self.health[type] -= damage

		# If negative number, set value to 0
		# Set damage to equal the negative remainder,
		# and reverse it to positive.
		if self.health[type] <= 0:
			damage = -self.health[type]
			self.health[type] = 0

			# Apply damage to the next health type.
			if type is 'mental':
				self.take_damage(damage, 'physical')
			if type is 'physical':
				self.take_damage(damage, 'spiritual')
			if type is 'spiritual' or self.health['spiritual'] is 0:
				self.update_status(0)

	def heal(self, amount, type):
		'''
		Add health to health type.

		Returns nothing as it directly modifies self.health.
		'''
		amt_healed = self.max_health[type] - self.health[type]
		self.health[type] += amount

		if self.health[type] > self.max_health[type]:
			self.health[type] = self.max_health[type]

		
		ret = {
			type: amt_healed
		}

		return ret


	def distance(self, points):
		'''
		Range/Reach in feet.
		0 = 3 ft, 1 = 6 ft, [...]

		Returns the distance in feet.
		'''
		return 3 + (points * 3)

	def stun_recovery(self):
		'''
		For every 100 movement heal one stun.
		This should be overridden by any game
		that uses realtime (since the rules state
		one box per ten minutes)
		'''
		if self.stun_timer > 0:
			self.stun_timer -= 1

		if self.stun_timer % 100 is 1:
			self.heal(1, 'mental')

	def update_status(self, status_id):
		'''
		Creature's life status has changed.
		'''
		was = self.status
		self.status = status_id

		ret = {
			'was': was,
			'now': self.status
		}

		return ret
