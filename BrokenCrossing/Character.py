import pygame
import random
from .Timer import *
from .Fighter import *
from .Collision import *
from .Constants import *
from .Renderable import *
from .LevelManager import *


# Character class
# used for the user
class Character(Fighter, CharacterAnimation):
	instance = None
	
	# initialize character
	def __init__(self):
		Fighter.__init__(self, 150, 15)
		CharacterAnimation.__init__(self)
		self.inactive_time = 1.0
		# user location will always be top left
		self.row = 0
		self.col = 0
		
		self.y_position = 0
		self.has_key = False
		
		self.input_timer = Timer()
		self.input_timer.start(ANIMATION_DURATION)
		
		self.inactive_timer = Timer()
		self.inactive_timer.start(self.inactive_time)
		
		self.had_key = False
		self.previous_lost = False
		
		self.continue_level = False
		
	# render character info
	def render(self, screen):
		# show character object
		CharacterAnimation.render(self, screen)
		
		# WIN STATUS
		# check if there are any enemies on map			
		#if num_enemies == 0:
		if self.has_key:			
			if not self.had_key:	
				play_sound('win.wav', 1)			
			
			if LevelManager.instance.has_remaining_level():
				Renderable.show_complete(screen)
			else:
				Renderable.show_win(screen)
				
			self.had_key = True
		# if there are enemies
		# check if user still alive
		if self.is_alive():
			# render user's health and damage at bottom left
			health_display = 'Health: {} / 150'.format(self.health)
			damage_display = 'Damage: {} / 80'.format(self.damage)
			
			health_text = REG_FONT.render(health_display, True, BLUE_COLOR, BEIGE_COLOR)
			health_text_rect = health_text.get_rect()
			health_text_rect.topleft = (0, SCREEN_SIZE[1] - (TILE_SIZE))
			
			damage_text = REG_FONT.render(damage_display, True, BLUE_COLOR, BEIGE_COLOR)
			damage_text_rect = damage_text.get_rect()
			damage_text_rect.topleft = (health_text_rect.left, health_text_rect.top + health_text_rect.height)
			
			screen.blit(health_text, health_text_rect)
			screen.blit(damage_text, damage_text_rect)
		else:
			# if there are enemies
			# and user is not alive
			Renderable.show_lose(screen)
			if not self.previous_lost:
				self.set_action(Actions.HURT)
				play_sound('OGG\\creak2.ogg')
				play_sound('OGG\\creak3.ogg')
		
		self.previous_lost = not self.is_alive()
		
	# when button is pressed for up, down, left, right
	def on_button_press(self):
		row = self.row
		col = self.col
		move_x = 0
		move_y = 0
		direction = self.direction
		
		if self.action == Actions.WALK:
			self.set_frozen(self.inactive_timer.is_expired())
		
		if self.action != Actions.WALK:
			return
		
		if self.input_timer.is_expired():
			self.input_timer.start(ANIMATION_DURATION)
		else:
			return
		
		# verify that user is alive
		# if not alive, exit
		if not self.is_alive():
			return
		
		# check to see if character will collide when moved
		# if no collision then move the character
		keys = pygame.key.get_pressed()
		
		if not self.has_key:
			if keys[pygame.K_LEFT]:
				col -= 1
				move_x = -TILE_SIZE
				direction = Directions.LEFT
			elif keys[pygame.K_RIGHT]:
				col += 1
				move_x = TILE_SIZE
				direction = Directions.RIGHT
			elif keys[pygame.K_UP]:
				row -= 1
				move_y = -TILE_SIZE
				direction = Directions.UP
			elif keys[pygame.K_DOWN]:
				row += 1
				move_y = TILE_SIZE
				direction = Directions.DOWN
		else:
			if keys[pygame.K_RETURN]:
				self.continue_level = True

		if direction != self.direction:
			self.set_direction(direction)
		
		# check to see if user is moving into a tile
		# that will collide with an object
		if not Collision.check_collision(row, col):
			item = Collision.check_item(row, col)
			enemy = Collision.check_enemy(row, col)
			is_item_present = item is not None
			is_enemy_present = enemy is not None
			
			# trigger for if there is an item on tile
			if is_item_present:
				item.on_collide()
			# trigger for if there is an enemy on tile
			elif is_enemy_present:
				# initiates fight
				# play sword sound
				play_sound('OGG\\chop.ogg')
				self.fight(enemy)
				enemy.fight(self)
				self.set_action(Actions.THRUST)
				self.set_frozen(False)
				enemy_direction = Directions.get_opposite(self.direction)
				enemy.set_direction(enemy_direction)
				enemy.set_action(Actions.THRUST)
				enemy.set_frozen(False)
				# once enemy dies
				if not enemy.is_alive():
					# enemy drops item
					# enemy removed from screen
					enemy.set_action(Actions.HURT)
					Collision.remove_enemy(row, col)
			
			# if enemy is not on the tile
			# allow user to move to tile
			if not is_enemy_present and (move_x or move_y):
				self.move(move_x, move_y)
				self.row = row
				self.col = col
				self.inactive_timer.start(self.inactive_time)
	
	def add_health(self, health):
		self.health = clamp(self.health + health, 0, 150)

	def add_damage(self, damage):
		self.damage = clamp(self.damage + damage, 0, 80)