import random
import pygame
from .FloatingAnimation import *
from .Renderable import *


# Fighter class
# used for child classes that can fight
class Fighter:
	# initialize fighters (characters and enemies)
	def __init__(self, health, damage):
		self.health = health
		self.damage = damage
	
	# default attack method
	def fight(self, enemy):
		# check if obj is alive
		if self.is_alive():
			# check if obj has an enemy
			if enemy is not None:
				# determine damage to enemy
				damage = self.get_damage()
				enemy.health -= damage
				# show damage on screen
				damage_text = REG_FONT.render('-{}'.format(damage), True, RED_COLOR)
				# make damage text on screen fade
				animation = FloatingAnimation(damage_text)
				animation.set_position(enemy.x_position, enemy.y_position)
				Renderable.add_renderable(101, animation)
	
	# random damage generator for fighting
	def get_damage(self):
		jiggle_amount = self.damage / 10
		half_jiggle = jiggle_amount / 2
		jiggle_amount *= random.random()
		jiggle_amount -= half_jiggle
		damage = self.damage + jiggle_amount
		return int(damage)
	
	# check if fighter is alive
	def is_alive(self):
		return self.health > 0
	
	# determine health of fighter
	def add_health(self, points):
		self.health += points
		self.health = min(self.health, 150)
		return self.health
	
	# determine dmg attack of fighter
	def add_damage(self, points):
		self.damage += points
		self.damage = min(self.damage, 80)
		return self.damage
	