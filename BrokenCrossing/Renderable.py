import pygame
from .Utils import *
from .Constants import *


# Renderable is a class used to render objects onto the screen
class Renderable:
	# renderables to store different renderable items 
	# and which key to indicate when to render
	renderables = {}

	# initialize renderable
	def __init__(self, image, normalize_size=True):
		# the object image that is passed in could be a string or layer
		# if image is a string
		if type(image) is str:
			self.image = pygame.image.load(get_resource_path(image))
			if normalize_size:
				self.image = pygame.transform.scale(self.image, ((TILE_SIZE, TILE_SIZE)))
			
		else:
			# if image is layer
			self.image = image
		
		# default position
		self.x_position = 0
		self.y_position = 0
		self.removed = False
		
	# show render item on screen
	def render(self, screen):
		screen.blit(self.image, (self.x_position, self.y_position))
	
	# move render item
	def move(self, x, y):
		self.x_position += x
		self.y_position += y
		
	# set position of render item
	def set_position(self, x, y):
		self.x_position = x
		self.y_position = y
		
	# get coordinates of current render item
	def get_coordinates(self):
		return (int(self.y_position / TILE_SIZE), int(self.x_position / TILE_SIZE))
	
	def remove(self):
		self.removed = True
		
	# static method
	# add render items to list based on key
	# key will be a number specified in __init__
	# higher number = outer layer
	@classmethod
	def add_renderable(cls, depth, renderable):
		renderable_layer = cls.renderables.get(depth, [])
		renderable_layer.append(renderable)
		cls.renderables[depth] = renderable_layer
		
	# static method
	# get list of renderables
	@classmethod
	def get_renderables(cls):
		# sort the renderables
		keys = list(cls.renderables.keys())
		keys.sort()
		all_renderables = []
		
		# loop each key
		for key in keys:
			# put into temp variable
			renderable_layer = cls.renderables[key]
			current_renderables = []
			for renderable in renderable_layer:
				# put each renderable into the list
				# if removed trait is set to false
				if not renderable.removed:
					current_renderables.append(renderable)
					all_renderables.append(renderable)
					
			cls.renderables[key] = current_renderables
		
		return all_renderables
	
	@classmethod
	def show_win(cls, screen):
	# render text onto center screen
		win_display = 'YOU WIN.'
		win_text = BIG_FONT.render(win_display, True, RED_COLOR, BEIGE_COLOR)
		win_text_rect = win_text.get_rect()
		win_text_rect.center = CENTER_POS
		
		screen.blit(win_text, win_text_rect)
		
	@classmethod
	def show_lose(cls, screen):
		# render text onto center screen
		lose_display = 'YOU LOSE.'
		lose_text = BIG_FONT.render(lose_display, True, RED_COLOR, BEIGE_COLOR)
		lose_text_rect = lose_text.get_rect()
		lose_text_rect.center = CENTER_POS
		
		screen.blit(lose_text, lose_text_rect)	

	@classmethod
	def show_complete(cls, screen):
	# render text onto center screen
		level_complete_display = 'LEVEL COMPLETE.'
		level_complete_text = BIG_FONT.render(level_complete_display, True, RED_COLOR, BEIGE_COLOR)
		level_complete_text_rect = level_complete_text.get_rect()
		level_complete_text_rect.center = CENTER_POS
		
		continue_display = 'PRESS ENTER TO CONTINUE.'
		continue_text = REG_FONT.render(continue_display, True, RED_COLOR, BEIGE_COLOR)
		continue_text_rect = continue_text.get_rect()
		continue_text_rect.midtop = level_complete_text_rect.midbottom
		
		screen.blit(level_complete_text, level_complete_text_rect)
		screen.blit(continue_text, continue_text_rect)