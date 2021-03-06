

class Settings:
    """A class to store all settings for Alien Invasion. """

    def __init__(self):
        """Initialize the game's settings."""
        #Screen settings
        #orginal width: 1200,  original height: 800
        self.screen_width  = 1300
        self.screen_height = 750
        self.bg_color = (230, 230, 230)


        #ship settings
        self.ship_speed = 2
        self.ship_limit = 4

        #Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60) 
        self.bullets_allowed = 3

        #Alien settings
        self.alien_speed = 0.5
        self.fleet_drop_speed  = 30
        #fleet direction of 1 = right; -1 = left
        self.fleet_direction = 1