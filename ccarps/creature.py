#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ccarps import dice, modifier


# Covers:
# * https://github.com/WizardSpire/ccarps/blob/master/CharacterCreation.md
# * https://github.com/WizardSpire/ccarps/blob/master/Combat.md
# * https://github.com/WizardSpire/ccarps/blob/master/TechLevels.md
class Creature(object):
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

		# Override the defaults if any parameters are passed.
		if age is not None:
			self.age = age
		else:
			self.age = 21
		if rank is not None:
			self.rank = rank
		else:
			self.rank = 'Novice'
		if name is not None:
			self.name = name
		else:
			self.name = 'Unnamed Human'

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
		self.CHR = 0
		self.SPD = 0
		self.RFX = 0
		self.LFT = 0
		self.PER = 0

		# Calculates the secondary attributes.
		self.calc_secondary_attr()

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

		# Initial point allocation. Total should equal spent plus unspent.
		# No points should be unspent post-character creation.
		self.points = {
			'spent': 0,
			'unspent': 0,
			'total': 0
		}

		self.points['unspent'] = self.STR + self.DEX + self.CON + self.INT + self.WIL
		self.points['total'] = self.points['spent'] + self.points['unspent']

		# https://github.com/WizardSpire/ccarps/blob/master/TechLevels.md
		self.tech_level = 0

		self.modifiers = {
			'attack': 0,
			'defense': {
				'mental': 0,
				'physical': 0,
				'spiritual': 0
			}
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

		ret = {
			'roll': lowest,
			'success': success
		}

		return ret

	def take_damage(self, damage, type, tracker=None):
		'''
		Take damage. If any damage is greater than 10, move to
		the next health type. If all three are 0, set status to 0.

		Returns nothing on success, as it directly modifies self.health.
		'''
		# Catch any invalid health types and return with list of available.
		if type not in self.health:
			return "Invalid damage type. Available: %s" % ', '.join(self.health)

		# Lets us keep track of total damage of each heal type
		# through the recursive damage system.
		ret = {}

		if tracker is not None:
			ret = tracker

		# Apply initial damage to approriate type
		self.health[type] -= damage

		# Get a copy so we can get the difference later.
		ret[type] = damage

		# If negative number, set value to 0
		# Set damage to equal the negative remainder,
		# and reverse it to positive.
		if self.health[type] <= 0:
			damage = -self.health[type]
			self.health[type] = 0

			# Get the difference so we have number of points healed.
			ret[type] -= damage

			# Apply damage to the next health type.
			if type is 'mental':
				self.take_damage(damage, 'physical', ret)
			if type is 'physical':
				self.take_damage(damage, 'spiritual', ret)
			if type is 'spiritual' or self.health['spiritual'] is 0:
				self.update_status(0)

		return ret

	def health_mod(self):
		health_mod = 0

		# Add up each health
		for health in self.health:
			diff = self.max_health[health] - self.health[health]
			if diff >= 1 and diff < 4:
				health_mod += 1
			if diff >= 4 and diff < 7:
				health_mod += 2
			if diff >= 6:
				health_mod += 3

		# Return it as a negative number, since it's bad.
		return health_mod * -1

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

	def calc_secondary_attr(self):
		self.CHR = (self.CON + self.INT + self.WIL) / 3
		self.SPD = (self.STR + self.DEX) / 2
		self.RFX = (self.STR + self.DEX + self.WIL) / 3
		self.LFT = (self.STR + self.WIL) / 2
		self.PER = (self.INT + self.WIL) / 2
