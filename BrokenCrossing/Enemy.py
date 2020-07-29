import pygame
import random
from .Utils import *
from .Fighter import *
from .Constants import *
from .Collision import *
from .Animation import *
from .Renderable import *

# Enemy class
# used to handle all enemy objects
class Enemy(Fighter, Animation):
	# initialize enemy at a random spot
	# that is not in a collision coordinate
	def __init__(self, enemy, health, damage):
		Fighter.__init__(self, health, damage)
		Animation.__init__(self, enemy)
		(row, col, x, y) = Collision.get_spawn_loc()
		self.set_position(x, y)
		Collision.add_enemy_tile(row, col, self)
	
	def render(self, screen):
		if self.action == Actions.HURT and Actions.NUM_FRAMES[Actions.HURT] - 1 == self.active_frame:
			self.removed = True
			self.drop_item()
		else:
			Animation.render(self, screen)
	
	# enemy will have ability to drop an item
	def drop_item(self):
		from .Item import MapItem, HealthItem, SwordItem
		
		play_sound('OGG\\dropLeather.ogg')
		num = rand_range(0, 100)
		# get enemy current position
		(row, col) = self.get_coordinates()
		x = self.x_position
		y = self.y_position
		
		# randomly drop a health or sword item
		if len(Collision.enemy_tiles) == 0:
			item = MapItem(row, col, x, y)
		elif num <= 50:
			item = HealthItem(row, col, x, y)
		else:
			item = SwordItem(row, col, x, y)
		
		Renderable.add_renderable(49, item)

class Skeleton(Enemy):
	def __init__(self):
		Enemy.__init__(self, "Skeleton.png", 75, 10)

class Orc(Enemy):
	def __init__(self):
		Enemy.__init__(self, "Orc.png", 85, 15)
		
	# drops something more special by chance
	def drop_item(self):
		from .Item import MapItem, PoisonItem, SwordItem
		
		play_sound('OGG\\dropLeather.ogg')
		num = rand_range(0, 100)
		# get enemy current position
		(row, col) = self.get_coordinates()
		x = self.x_position
		y = self.y_position
		
		# randomly drop a health or sword item
		if len(Collision.enemy_tiles) == 0:
			item = MapItem(row, col, x, y)
		elif num <= 75:
			item = PoisonItem(row, col, x, y)
			Renderable.add_renderable(51, item)
		else:
			item = SwordItem(row, col, x, y)
		
		Renderable.add_renderable(49, item)
