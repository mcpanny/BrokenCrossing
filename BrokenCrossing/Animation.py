import pygame
from .Timer import *
from .Constants import *
from .Renderable import *


class Animation(Renderable):
	def __init__(self, image):
		Renderable.__init__(self, image, False)
		self.timer = Timer()
		self.timer.start(ANIMATION_DURATION)
		self.active_frame = 0
		self.direction = Directions.DOWN
		self.action = Actions.WALK
		self.frame_size = 64
		self.__is_frozen = True
	
	def render(self, screen):
		if self.__is_frozen:
			self.active_frame = 0
		elif self.timer.is_expired():
			if not (self.action == Actions.HURT and self.active_frame == Actions.NUM_FRAMES[Actions.HURT] - 1):
				self.timer.start(ANIMATION_DURATION)
				self.active_frame += 1				
				self.active_frame %= Actions.NUM_FRAMES[self.action]
			if self.active_frame == 0 and self.action != Actions.WALK:
				self.set_action(Actions.WALK)
				self.set_frozen(True)
		
		crop_x = self.active_frame * self.frame_size
		crop_y = ((Directions.NUM_DIRECTIONS * self.action) + self.direction) * self.frame_size
		cropped = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
		cropped.blit(self.image, (0, 0), (crop_x, crop_y, self.frame_size, self.frame_size))
		cropped = pygame.transform.scale(cropped, (TILE_SIZE, TILE_SIZE))
		screen.blit(cropped, (self.x_position, self.y_position))
	
	def set_action(self, action):
		if self.action != action:
			self.action = action
			self.active_frame = 0
			if self.action == Actions.HURT:
				self.direction = Directions.UP
		
	def set_direction(self, direction):
		if self.direction != direction and self.action != Actions.HURT:
			self.direction = direction
			self.active_frame = 0
	
	def set_frozen(self, frozen):
		if self.__is_frozen != frozen:
			self.__is_frozen = frozen
			if not self.__is_frozen:
				self.timer.start(ANIMATION_DURATION)

	def get_frozen(self):
		return self.__is_frozen

class CharacterAnimation(Animation):
	def __init__(self):
		Animation.__init__(self, "Character.png")