import pygame.font
from ship import Ship
from pygame.sprite import Group

class Scoreboard():
	
	def __init__(self, ai_settings, screen, stats):
		"""Initialize scorekeeping attributes"""
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats
		
		#Set the dimensions and properties of the button.
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)
		
		self.prep_score()
		self.prep_ships()
		
	def prep_score(self):
		"""Turn score into a rendered image and display at the top right"""
		score_str = str(self.stats.score)
		self.score_image = self.font.render(score_str, True, 
						self.text_color, self.ai_settings.bg_color)
			
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20
		
	def prep_ships(self):
		"""Show how many ships being left"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_settings, self.screen)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)	
		
	def show_score(self):
		#Draw score to the screen
		self.screen.blit(self.score_image, self.score_rect)
		#Draw ships_left on the screen
		self.ships.draw(self.screen)
		
				
							
