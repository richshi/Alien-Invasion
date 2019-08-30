class Settings():
	"""A class to store all settings for Alien Invasion"""

	def __init__(self):
		#screen settings
		self.screen_width = 1000
		self.screen_height = 600
		self.bg_color = (230, 230, 230)
		#Ship settings
		self.ship_speed = 1.5
		self.ship_limit = 3
		#Bullet settings
		self.bullet_speed = 2
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 3
		#Alien settings
		self.alien_speed = 1
		self.fleet_drop_speed = 8
		self.fleet_direction = 1
		#Score settings
		self.alien_points = 5
