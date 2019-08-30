import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from alien import Alien
import game_functions as gf


def run_game():
	#Initialize game and create a screen object
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width,
	 ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	
	#Make the Play button
	play_button = Button(screen, "Play")
	
	#Make a ship and a list to store bullets and to store aliens
	ship = Ship(ai_settings, screen)
	aliens = Group()
	bullets = Group()
	
	# Create the fleet of aliens.
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	#Create an instance to store game stats and a scoreboard
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	
	#The main loop for the game
	while True:
		gf.check_events(ai_settings, screen, stats, sb, play_button, 
			ship, aliens, bullets)
		
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship,
							bullets, aliens)
			gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, 
							bullets)					
		
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
						bullets, play_button)
		
		
run_game()				
		
