from .Level import *
from .Collision import *
from .Renderable import *


class LevelManager(Renderable):
	instance = None
	
	def __init__(self):
		Renderable.__init__(self, None)
		self.active_level = None
		self.all_levels = [Level1, Level2, Level3]
		
	def render(self, screen):
		from .Character import Character
		if (self.active_level is None or self.active_level.is_complete()) and len(self.all_levels) > 0:
			if self.active_level is not None:
				self.active_level.remove()
				Character.instance.has_key = False
				Character.instance.had_key = False
				Character.instance.continue_level = False
				self.clean_level()
			self.active_level = self.all_levels.pop(0)()
			self.active_level.load()
			Renderable.add_renderable(1, self.active_level)
			Character.instance.set_position(0, 0)
			Character.instance.row = 0
			Character.instance.col = 0
	
	def clean_level(self):
		Collision.empty_all()

	def has_remaining_level(self):
		return len(self.all_levels) > 0
