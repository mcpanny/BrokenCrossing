import pygame
from .Enemy import *
from .Utils import *
from .Constants import *
from .Renderable import *
	
# Level class is to set the map for the game
class Level(Renderable):
	# initialize map
	def __init__(self, level):
		Renderable.__init__(self, level, False)
		self.image = pygame.transform.scale(self.image, SCREEN_SIZE)
	
	def is_complete(self):
		from .Character import Character
		return Character.instance.continue_level
	
	def get_json_file(self):
		raise NotImplementedError('Level.get_json_file')
	
	def load(self):
		level_json = self.get_json_file()
		
		# read file
		path = get_resource_path(level_json)
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
			Collision.width = collision_layer['width']
			Collision.height = collision_layer['height']
			for i, d in enumerate(collision_layer['data']):
				row = int(i / Collision.width)
				col = i % Collision.width
				if d != 0:
					Collision.colliding_tiles.add((row, col))
		
		# initilize enemies (random number each time)
		for e in range(rand_range(7, 13)):
		#for e in range(rand_range(1, 5)):
			enemies = [Skeleton, Orc]
			enemy_type = random.choice(enemies)
			enemy = enemy_type()
			Renderable.add_renderable(50, enemy)
			
		from .Item import HealthItem, PoisonItem, SwordItem
		# randomly initialize items
		for i in range(rand_range(15, 20)):
			num = rand_range(0, 100)
			if num <= 40:
				health = HealthItem()
				Renderable.add_renderable(51, health)
			elif num <= 80:
				poison = PoisonItem()
				Renderable.add_renderable(51, poison)
			elif num <= 100:
				sword = SwordItem()
				Renderable.add_renderable(51, sword)

# first level of game
class Level1(Level):
	def __init__(self):
		Level.__init__(self, "map\\level_1.png")
	
	def get_json_file(self):
		return 'map\\level_1.json'
	
# second level of game
class Level2(Level):
	def __init__(self):
		Level.__init__(self, "map\\level_2.png")
	
	def get_json_file(self):
		return 'map\\level_2.json'
		
# third level of game
class Level3(Level):
	def __init__(self):
		Level.__init__(self, "map\\level_3.png")
	
	def get_json_file(self):
		return 'map\\level_3.json'