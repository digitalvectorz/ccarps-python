#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ccarps import dice, modifier


# Covers:
# * https://github.com/WizardSpire/ccarps/blob/master/Character_Creation.md
# * https://github.com/WizardSpire/ccarps/blob/master/Combat.md
# * https://github.com/WizardSpire/ccarps/blob/master/Tech_Levels.md
class Creature(object):
	'''
	Set up us the Creature! (Monsters, (N)PCs)
	'''
	def __init__(self, age=None, name=None):
		# Initialize dice system
		self.dice = dice.Dice()
		self.roll = 0
	
		# Dead: -1 = undead, 0 = dead, 1 = unconscious, 2 = alive, 3 = polymorphed
		self.status = 2

		# Some defaults so that if creature.Creature() is invoked,
		# a generic 21 year old human will be created.

		# Override the defaults if any parameters are passed.
		if age is not None:
			self.age = age
		else:
			self.age = 21
		if name is not None:
			self.name = name
		else:
			self.name = 'Unnamed Human'

		# https://github.com/WizardSpire/ccarps/blob/master/Character_Creation.md#starting-points
		base = self.dice.random_stats(age=self.age)

		# Setting max health allows for modified health bars.
		self.max_health = {
			'mental': 10,
			'physical': 10,
			'spiritual': 10
		}

		# Set initial health as full.
		# https://github.com/WizardSpire/ccarps/blob/master/Combat.md#damage-levels
		self.health = {
			'mental': 10,
			'physical': 10,
			'spiritual': 10
		}

		# Numbers are 2d6
		# https://github.com/WizardSpire/ccarps/blob/master/Combat.md#hit-location-chart
		self.body_parts = {
			'head': 2,
			'chest or upper back': [3, 4],
			'abdomen or lower back': [5, 6, 7],
			'leg': [8, 9],
			'arm': [10, 11],
			'neck, buttocks, or groin': [12]
		}

		# Primary Attributes
		# https://github.com/WizardSpire/ccarps/blob/master/Character_Creation.md#primary-attributes
		self.STR = base[0]
		self.DEX = base[1]
		self.CON = base[2]
		self.INT = base[3]
		self.WIL = base[4]

		# Secondary Attributes
		# https://github.com/WizardSpire/ccarps/blob/master/CharacterCreation.md#secondary-attributes
		self.CHA = 0
		self.SPD = 0
		self.RFX = 0
		self.LFT = 0
		self.PER = 0

		# Set Secondary Attribute Modifiers.
		self.get_attribute_modifiers()

		# Total Points
		# https://github.com/WizardSpire/ccarps/blob/master/Character_Creation.md#starting-points
		self.points = {
			'spent': {
				'STR': 0,
				'DEX': 0,
				'CON': 0,
				'INT': 0,
				'WIL': 0,
				'Skills': 0,
				'Oddities': 0
			},
			'accumulator': {
				'STR': 0,
				'DEX': 0,
				'CON': 0,
				'INT': 0,
				'WIL': 0
			},
			'unspent': self.STR + self.DEX + self.CON + self.INT + self.WIL,
			'total': 0
		}

		# Setting our inital total points.
		self.points['total'] = sum(self.points['spent'].itervalues()) + self.points['unspent']  # NOQA

		# Oddities
		# https://github.com/WizardSpire/ccarps/blob/master/Character_Creation.md#character-creation-specific-oddities
		self.oddities = {
			'Wealth': 0,
			'Social Influence': 0
		}

		self.contacts = {}

		# Skills
		# https://github.com/WizardSpire/ccarps/blob/master/Character_Creation.md#skills
		self.skills = {}

		# Character Apperance
		# https://github.com/WizardSpire/ccarps/blob/master/Character_Creation.md#character-appearance
		self.appearance = {}
		self.background = {}

		# https://github.com/WizardSpire/ccarps/blob/master/Tech_Levels.md
		self.tech_level = 0

		self.modifiers = {
			'mental': 0,
			'physical': 0,
			'spiritual': 0,
			'resistance': {},
		}

	def action(self, skill, base_tn):
		'''
		Action handler for combat, using skill, or trying
		to stop from falling out of an airship...
		'''

		# Set the default action modifier and number of dice
		action_mod = 0
		success = 0
		num_dice = 2
		health_mod = self.health_mod()  # Will always be 0 or negative.

		# To make things easy in ccarps, we always add.
		tn = base_tn + action_mod + health_mod

		if skill in self.skills:
			skill_mod = modifier.get(self.skills[skill])
			num_dice = 2 + modifier.dice(skill_mod)

		roll = self.dice.roll(qty=num_dice)
		lowest = self.dice.lowest(roll)

		if lowest < tn:
			success = 1

		return {
			'roll': lowest,
			'success': success
		}

	def take_damage(self, damage, dtype, tracker=None):
		'''
		Take damage. If any damage is greater than 10, move to
		the next health type. If all three are 0, set status to 0.

		Returns nothing on success, as it directly modifies self.health.
		'''
		# Catch any invalid health types and return with list of available.
		if dtype not in self.health:
			return "Invalid damage type. Available: %s" % ', '.join(self.health)

		# Lets us keep track of total damage of each heal type
		# through the recursive damage system.
		ret = {}

		if tracker is not None:
			ret = tracker

		status = self.health_check()
		if status['now'] is 0:
			return ret

		# Apply initial damage to approriate type
		self.health[dtype] -= damage

		# Get a copy so we can get the difference later.
		ret[dtype] = damage

		# If negative number, set value to 0
		# Set damage to equal the negative remainder,
		# and reverse it to positive.
		if self.health[dtype] <= 0:
			damage = -self.health[dtype]
			self.health[dtype] = 0

			# Get the difference so we have number of points healed.
			ret[dtype] -= damage

			# Apply damage to the next health type.
			if dtype is 'mental':
				self.take_damage(damage, 'physical', ret)

			if dtype is 'physical':
				self.take_damage(damage, 'spiritual', ret)

			if dtype is 'spiritual' or self.health['spiritual'] is 0:
				self.take_damage(damage, 'mental')

		return ret

	def health_mod(self):
		health_mod = 0

		# Add up each health
		for health in self.health:
			diff = self.max_health[health] - self.health[health]
			if diff >= 1 and diff < 5:
				health_mod += 1
			if diff >= 5 and diff < 8:
				health_mod += 2
			if diff >= 8:
				health_mod += 3

		# Return it as a negative number, since it's bad.
		return health_mod * -1

	def unconscious_dying(self):
		'''
		This should be called only once per turn (or x seconds) when
		the character is unconscious.

		Returns damage taken, or None if not unconscious.
		'''
		damaged = None

		if self.status is 1:
			roll = self.dice.roll(qty=2)

			if roll >= self.CHA:
				damaged = 1
				self.take_damage(1, 'mental')
			
		return damaged

	def health_check(self):
		'''
		Checks for health status.

		Returns result of self.update_status()
		'''
		if self.status is 0:
			return self.update_status(0)

		total_health = sum(self.health.values())
		status = self.status

		# If character has no health, they are dead.
		if total_health is 0:
			return self.update_status(0)

		# If any health types are 1, character is unconscious.
		# There's probably a better way to do this.
		for num in self.health.values():
			if num is 0:
				status = 1

		return self.update_status(status)

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

	def hit_location(self, roll):
		'''
		Return location that was struck.
		'''
		location = 'None'
		
		for key in self.body_parts.keys():
			if isinstance(self.body_parts[key], list):
				for n in self.body_parts[key]:
					if roll is n:
						location = key

			if roll is self.body_parts[key]:
				location = key

		ret = {
			'location': location
		}

		return ret

	def distance(self, points):
		'''
		Range/Reach in feet.
		0 = 3 ft, 1 = 6 ft, [...]

		Returns the distance in feet.
		'''
		ret = {
			'feet': 3 + (points * 3)
		}

		return ret

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

	def get_attribute_modifiers(self):
		self.CHA = modifier.get((self.CON + self.INT + self.WIL) / 3)
		self.SPD = modifier.get((self.STR + self.DEX) / 2)
		self.RFX = modifier.get((self.STR + self.DEX + self.WIL) / 3)
		self.LFT = modifier.get((self.STR + self.WIL) / 2)
		self.PER = modifier.get((self.INT + self.WIL) / 2)
