import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	def __init__(self, ai_settings, screen):
		"""Initialize the ship and set its start position"""
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		#Load the ship image and get its rect
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		#Start the new ship at the bottom center of the screen
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		
		#Store a decimal value for the ship's center position
		self.center = float(self.rect.centerx)
		
		#Movement flag
		self.moving_right = False
		self.moving_left = False
	
	def center_ship(self):
		self.center = self.screen_rect.centerx
		
	def update(self):
		"""move the ship's position (center value) based on the flag"""
		if self.moving_right and \
		self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed
			
		#Update the ship's rect position from self.center
		self.rect.centerx = self.center				
		
	def blitme(self):
		"""Draw the ship at its designated location"""
		self.screen.blit(self.image, self.rect)	
		
