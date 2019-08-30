import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	def __init__(self, ai_settings, screen):
		"""Initialize the alien and set its start position"""
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		#Load the alien image and get its rect
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()
		
		"""Start the new alien near the top left corner of the screen.
		Adding a space to the left of it that's equal to the alien's
		width and a space above it equal to its height"""
		
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		#Store a decimal value for the ship's center position
		self.x = float(self.rect.x)
		
	def update(self):
		"""Move the alien right or left"""
		self.x += (self.ai_settings.alien_speed * 
					self.ai_settings.fleet_direction)
		self.rect.x = self.x
		
	def check_edges(self):
		"""Return true if alien is at the edge of the screen"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		if self.rect.left <= 0:
			return True					
		
	def blitme(self):
		"""Draw the ship at its designated location"""
		self.screen.blit(self.image, self.rect)
