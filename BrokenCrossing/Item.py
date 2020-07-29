import pygame
from .Timer import *
from .Utils import *
from .Collision import *
from .Constants import *
from .Character import *
from .Renderable import *
from .FloatingAnimation import *


# Item class used for usable items in game
# inherits from Renderable
class Item(Renderable):
	# initializer
	def __init__(self, image, hidden_image, row=None, col=None, x=None, y=None):
		Renderable.__init__(self, image)
		
		# get a spawn location if it is not specified when initialized
		if not (row is not None and col is not None and x is not None and y is not None):
			(row, col, x, y) = Collision.get_spawn_loc()
		
		# set spawn location
		self.set_position(x, y)
		# add item into items list
		Collision.add_item_tile(row, col, self)
		# set actual item image
		self.hidden_image = hidden_image
	
	# actions when character collides with item
	def on_collide(self):
		# play open sound
		play_sound('OGG\\cloth2.ogg', 1)
		# reveal the hidden image (hidden item)
		animation = FloatingAnimation(self.hidden_image)
		animation.set_position(self.x_position, self.y_position)
		Renderable.add_renderable(101, animation)
		# use item
		self.activate()
		# set remove trait to true
		self.removed = True
		(row, col) = self.get_coordinates()
		# remove item from items list
		Collision.remove_item(row, col)
	
	# show item on screen
	def render(self, screen):
		Renderable.render(self, screen)
	
	# to be defined based on item type (child classes)
	def activate(self):
		raise NotImplementedError

# HealthItem class
# info for spawning health object
class HealthItem(Item):
	# initializer
	def __init__(self, row=None, col=None, x=None, y=None):
		# this initializer is designed sort of like an overloaded method
		# it will spawn randomly at start of game
		# or the location for item to spawn is specified when enemy is killed
		Item.__init__(self, 'envelope.png', 'heart.png', row, col, x, y)
	
	# use health item (adds health to character)
	def activate(self):
		Character.instance.add_health(25)

# PoisonItem class
# info for spawning poison object
class PoisonItem(Item):
	# initializer
	def __init__(self, row=None, col=None, x=None, y=None):
		# this initializer is designed sort of like an overloaded method
		# it will spawn randomly at start of game
		# or the location for item to spawn is specified when enemy is killed
		Item.__init__(self, 'envelope.png', 'potionGreen.png', row, col, x, y)
	
	# use poison item (deducts health from character)
	def activate(self):
		Character.instance.add_health(-15)

# SwordItem class
# info for spawning sword object
class SwordItem(Item):
	# initializer
	# this initializer is designed sort of like an overloaded method
	# it will spawn randomly at start of game
	# or the location for item to spawn is specified when enemy is killed
	def __init__(self, row=None, col=None, x=None, y=None):
		Item.__init__(self, 'envelope.png', 'sword.png', row, col, x, y)
	
	# use sword item (increases damage attack for character)
	def activate(self):
		Character.instance.add_damage(10)

class MapItem(Item):
	# initializer
	# this initializer is designed sort of like an overloaded method
	# it will spawn randomly at start of game
	# or the location for item to spawn is specified when enemy is killed
	def __init__(self, row=None, col=None, x=None, y=None):
		# to do -- change png image
		Item.__init__(self, 'envelope.png', 'map.png', row, col, x, y)
	
	def activate(self):
		Character.instance.has_key = True