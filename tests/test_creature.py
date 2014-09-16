#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ccarps import creature


c = creature.Creature(rank='Beginner', name='Test Creature')


def test_creature_name():
	assert c.name == 'Test Creature'


def test_creature_stats():
	assert type(c.CON) is int
	assert type(c.INT) is int
	assert type(c.STR) is int
	assert type(c.WILL) is int
	assert type(c.DEX) is int


def test_creature_health():
	assert c.health['mental'] is 10
	assert c.health['physical'] is 10
	assert c.health['spiritual'] is 10

def test_creature_take_damage():
	c.take_damage(5, 'mental')
	assert c.health['mental'] is 5

def  test_creature_heal():
	assert c.health['mental'] is 5
	c.heal(5, 'mental')
	for health in c.health:
		assert c.health[health] is 10

def test_creature_complex_damage():
	for health in c.health:
		assert c.health[health] is 10

	c.take_damage(25, 'mental')
	assert c.health['mental'] is 0
	assert c.health['physical'] is 0
	assert c.health['spiritual'] is 5

