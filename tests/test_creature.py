#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ccarps import creature


c = creature.Creature(rank='Beginner', name='Test Creature')


def test_creature_name():
	assert c.name == 'Test Creature'


def test_creature_distance():
	distance = c.distance(0)
	assert distance['feet'] is 3


def test_creature_stats():
	assert type(c.CON) is int
	assert type(c.INT) is int
	assert type(c.STR) is int
	assert type(c.WIL) is int
	assert type(c.DEX) is int


def test_creature_health():
	assert c.health['mental'] is 10
	assert c.health['physical'] is 10
	assert c.health['spiritual'] is 10


def test_creature_take_damage():
	damage = c.take_damage(5, 'mental')
	
	assert damage['mental'] is 5


def test_creature_heal():
	assert c.health['mental'] is 5
	
	heal = c.heal(5, 'mental')

	assert heal['mental'] is 5

	for health in c.health:
		assert c.health[health] is 10


def test_creature_complex_damage():
	for health in c.health:
		assert c.health[health] is 10

	damage = c.take_damage(25, 'mental')

	assert damage['mental'] is 10
	assert damage['physical'] is 10
	assert damage['spiritual'] is 5

	assert c.health['mental'] is 0
	assert c.health['physical'] is 0
	assert c.health['spiritual'] is 5

	heal = c.heal(10, 'mental')
	assert heal['mental'] is 10
	
	heal = c.heal(10, 'physical')
	assert heal['physical'] is 10

	heal = c.heal(10, 'spiritual')
	assert heal['spiritual'] is 5

	assert c.health['mental'] is 10
	assert c.health['physical'] is 10
	assert c.health['spiritual'] is 10

	c.take_damage(9, 'spiritual')
	assert c.health['spiritual'] is 1
	
	c.take_damage(1, 'spiritual')
	assert c.status is 0


def test_update_status():
	assert c.status is 0
	
	status_update = c.update_status(1)

	assert status_update['was'] is 0
	assert status_update['now'] is 1
	assert c.status is 1
