import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def check_events(ai_settings, screen, stats, sb, play_button, 
			ship, aliens, bullets):
	"""Respond to keypresses and mouse events"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen,
			ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)	
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, 
			play_button, ship, aliens, bullets, mouse_x, mouse_y)
			

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""Responde to keypresses"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_q:
		sys.exit()
	elif event.key == pygame.K_SPACE:
		#create a new bullet and add it to the bullets group
		if len(bullets) < ai_settings.bullets_allowed:
			new_bullet = Bullet(ai_settings, screen, ship)
			bullets.add(new_bullet)						
			
def check_keyup_events(event, ship):
	"""Responde to keypresses"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False	
		
def check_play_button(ai_settings, screen, stats, sb, play_button, 
			ship, aliens, bullets, mouse_x, mouse_y):
	"""start a new game when play click the play button"""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		#hide the mouse
		pygame.mouse.set_visible(False)
		
		stats.reset_stats()
		stats.game_active = True
		
		#Reset scoreboard image
		sb.prep_score()
		sb.prep_ships()
		
		aliens.empty()
		bullets.empty()
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
def update_bullets(ai_settings, screen, stats, sb, ship, bullets, aliens):
	"""update position of bullet and get rid of old bullets"""
	bullets.update()
	
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
			
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
									bullets, aliens)		
			
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
									bullets, aliens):				
	#When bullet hit alien, destroy both
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
	# When entire fleet gets destroyed, make a new fleet
	if len(aliens) == 0:
		#Destroy existing bullets and create a new fleet
		bullets.empty()
		create_fleet(ai_settings, screen, ship, aliens)
		
					
def get_number_aliens_x(ai_settings, alien_width):
	"""Determin the number of aliens that fit in a row"""	
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
def get_number_rows(ai_settings, ship_height, alien_height):
	"""Determine the number of rows of aliens"""
	available_space_y = (ai_settings.screen_height - ship_height -
	 (3 * alien_height))
	number_rows = int(available_space_y /(2 * alien_height))
	return number_rows
	
	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""Create an alien and place it in a row"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width	
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
	aliens.add(alien)
	
		
def create_fleet(ai_settings, screen, ship, aliens):
	"""Create a fleet of aliens with proper space among them"""
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height,
	 alien.rect.height)
	#Create the first row of aliens
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number,
			 row_number)
				
def check_fleet_edges(ai_settings, aliens):
	"""Change direction if any alien reaches an edge"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break
			
def change_fleet_direction(ai_settings, aliens):
	"""Drop the entire fleet and change the fleet's direction."""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	#Look for alien-ship collisions.
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
	#Look for alien hit the bottom.	
	check_aliens_bottom(ai_settings, stats, sb, screen, 
						ship, aliens, bullets)
						
def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
	"""responde to ship being hit by alien"""
	if stats.ships_left > 0:
		stats.ships_left -= 1
		#update scoreboard to show the remaining ships only
		sb.prep_ships()
	
		#empty aliens and bullets to start 2nd game
		aliens.empty()
		bullets.empty()
	
		#create a new fleet and re-center the ship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
	
		#Pause
		sleep(0.5)
		
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)	

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, 
						aliens, bullets):
	"""check if any aliens hit the bottom"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#same treatment as alien hit ship
			ship_hit(ai_settings, stats, sb, screen, ship, aliens,
					bullets)
			break
							
	
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
					play_button):
	"""Update images on the screen and flip to the new screen"""
	#Redraw the screen druing each pass through the loop.
	screen.fill(ai_settings.bg_color)
	
	#Redraw all bullets behind ship and aliens
	for bullet in bullets.sprites():
		bullet.draw_bullet()
		
	ship.blitme()
	aliens.draw(screen)
	
	# Draw the score information
	sb.show_score()
	
	#Draw the play button if the game is not active
	if not stats.game_active:
		play_button.draw_button()
	
	#Make the most recently drawn objects visible.	
	pygame.display.flip()
