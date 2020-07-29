import pygame

# constants used in game

ANIMATION_DURATION = 0.2

# screen size for game
SCREEN_SIZE = (1280, 768)

# frame timeout for refresh
FRAME_TIMEOUT = 1/30

# size of each tile (grid outlined in game)
TILE_SIZE = 64

# font & sizes
pygame.init()
BIG_FONT = pygame.font.Font('freesansbold.ttf', 72)
REG_FONT = pygame.font.Font('freesansbold.ttf', 24)

# rgb colors
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (255, 0, 0)
BEIGE_COLOR = (239, 228, 176)
BLUE_COLOR = (0, 0, 128)

CENTER_POS = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)

class Directions:
	UP = 0
	LEFT = 1
	DOWN = 2
	RIGHT = 3
	NUM_DIRECTIONS = 4
	
	@classmethod
	def get_opposite(cls, direction):
		opposites = {
			cls.UP: cls.DOWN,
			cls.DOWN: cls.UP,
			cls.LEFT: cls.RIGHT,
			cls.RIGHT: cls.LEFT
		}
		
		return opposites.get(direction, cls.DOWN)

class Actions:
	SPELL_CAST = 0
	THRUST = 1
	WALK = 2
	SLASH = 3
	SHOOT = 4
	HURT = 5
	NUM_ACTIONS = 6
	
	NUM_FRAMES = {
		SPELL_CAST: 7,
		THRUST: 8,
		WALK: 9,
		SLASH: 6,
		SHOOT: 13,
		HURT: 6
	}
	
	