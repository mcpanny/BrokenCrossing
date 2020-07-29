from .Renderable import *
from .Timer import *


# FloatingAnimation class
# used to deal with animations that will float and disappear in the game
class FloatingAnimation(Renderable):
	# initializer
	def __init__(self, target):
		Renderable.__init__(self, target)
		self.animation_time = 1
		self.timer = Timer()
		self.timer.start(self.animation_time)
	
	# rendering on screen
	# reveals hidden image
	def render(self, screen):
		# if time is not expired
		if not self.timer.is_expired():
			temp = self.image.copy()
			# this works on images with per pixel alpha too
			# animate the object to float above the character
			# and make transparency increase over time
			ratio_animation_done = self.timer.get_time_elapsed() / self.animation_time
			transparency = 255 - (ratio_animation_done * 255)
			transparency = int(transparency)
			temp.fill((255, 255, 255, transparency), None, pygame.BLEND_RGBA_MULT)
			y = self.y_position
			y -= TILE_SIZE * ratio_animation_done
			screen.blit(temp, (self.x_position, y))
		else:
			# remove item
			self.removed = True