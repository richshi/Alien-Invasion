import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""a class to manage bullets fired from the ship"""
	
	def __init__(self, ai_settings, screen, ship):
		super().__init__()
		self.screen = screen
		
		#create a bullet using pygame.Rect class and set correct position
		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
			ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		
		#store the bullet's position as a decimal value.
		self.y = float(self.rect.y)
		
		self.color = ai_settings.bullet_color
		self.speed = ai_settings.bullet_speed
		
	def update(self):
		"""Move the bullet up the screen"""
		self.y -= self.speed
		self.rect.y = self.y
		
	def draw_bullet(self):
		pygame.draw.rect(self.screen, self.color, self.rect)				
		    
		
