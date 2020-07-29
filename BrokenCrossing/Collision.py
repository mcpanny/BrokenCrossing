import json
from .Utils import *


# static class used to read json file
# json file includes data on background
# collision objects
# item objects
class Collision:
	# set used to store all tiles which cannot be collided on (like a tree or wall)
	colliding_tiles = set()
	# dictionary of where all enemies located
	enemy_tiles = {}
	# dictionary of all items located
	item_tiles = {}
	width = 0
	height = 0
	
	@classmethod
	def empty_all(cls):
		cls.colliding_tiles = set()
		
		for enemy in cls.enemy_tiles.values():
			enemy.remove()
		cls.enemy_tiles = {}
		
		for item in cls.item_tiles.values():
			item.remove()
		cls.item_tiles = {}
	
	# static method
	# set the location of where the object will be located
	@classmethod
	def get_spawn_loc(cls):
		invalid_position = True
		# loop while the position determined is not good
		while invalid_position:
			# randomly determine coordinates based on random and size of screen
			x = random.random() * (SCREEN_SIZE[0])
			y = random.random() * (SCREEN_SIZE[1])
			
			# round the coordinates to whole numbers
			x = round_whole(x, TILE_SIZE)
			y = round_whole(y, TILE_SIZE)
			
			(row, col) = (int(y / TILE_SIZE), int(x / TILE_SIZE))
			# check if there is already an object on the location
			invalid_position = cls.check_collision(row, col) or (row, col) == (0, 0) or Collision.check_item(row, col) or Collision.check_enemy(row, col)
		
		return (row, col, x, y)
	
	# static method
	@classmethod
	def init(cls):	
		# read file
		path = get_resource_path('map\\level_1.json')
		with open(path, 'r') as map_file:
			data = map_file.read()

		# parse file
		# find object layer
		obj = json.loads(data)
		collision_layer = None
		for layer in obj['layers']:
			if layer['name'] == 'Objects':
				collision_layer = layer
				break
		
		# if object layer exists
		# set width and height
		# determine row and col of each collision object
		if collision_layer is not None:
			cls.width = collision_layer['width']
			cls.height = collision_layer['height']
			for i, d in enumerate(collision_layer['data']):
				row = int(i / cls.width)
				col = i % cls.width
				if d != 0:
					cls.colliding_tiles.add((row, col))
	
	# static method
	# check to see if render items are on collision objects
	@classmethod
	def check_collision(cls, row, col):
		collides = ((row, col) in cls.colliding_tiles or
			row < 0 or
			row >= cls.height or
			col < 0 or
			col >= cls.width)
		
		return collides
	
	# static method
	# add the enemy tile into the dictionary
	@classmethod
	def add_enemy_tile(cls, row, col, enemy):
		cls.enemy_tiles[(row, col)] = enemy
	
	# static method
	# check if there is an enemy at the location
	@classmethod
	def check_enemy(cls, row, col):
		return cls.enemy_tiles.get((row, col))
	
	# static method
	# remove the enemy from the dictionary
	@classmethod
	def remove_enemy(cls, row, col):
		cls.enemy_tiles.pop((row, col))
	
	# static method
	# get the total number of enemies in the dictionary
	@classmethod
	def get_num_enemies(cls):
		return len(cls.enemy_tiles)
	
	# static method
	# add an item into the dictionary
	@classmethod
	def add_item_tile(cls, row, col, item):
		cls.item_tiles[(row, col)] = item
	
	# static method
	# check if item exists at location
	@classmethod
	def check_item(cls, row, col):
		return cls.item_tiles.get((row, col))
	
	# static method
	# remove item from dictionary
	@classmethod
	def remove_item(cls, row, col):
		cls.item_tiles.pop((row, col))