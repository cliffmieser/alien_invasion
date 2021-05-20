#alien invasion project

#importing sys and pygame. pygame module contains import functionality for the game
#sys module holds tools to exit the game when a player quits
import sys
import pygame 

from ship import Ship
from settings import Settings
from bullet import Bullet

class AlienInvasion:

    """Overall class to manage game assets and behaviors"""

    def __init__(self):
        """Initialize game, and create game resources."""
        pygame.init() #initializes background settings for pygame to work properly


        self.settings = Settings() #isntance of Settings 

        #The object assigned to self.screen can be refered as a surface, which is a part of the screen where a game element
        #will be displayed in pygame
        self.screen = pygame.display.set_mode((0,0 ), pygame.FULLSCREEN) #creates a display window in which all graphic elements are drawn
        self.settings.screen_width = self.screen.get_rect().width 
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() #stores bullets in a group

    def run_game(self):
        """Start the main loop for the game."""

        while True:
            self._check_events() #calls the _check_events method
            self.ship.update()
            self.bullets.update()
            self._update_screen()



    def _check_events(self):
        """Respond to keypresses and mouse events."""
        # watch for keyboard and mouse events.
        #An event is an action that the use performs while playing the game
        for event in pygame.event.get():  # an event loop that listens for events to peform the appropriate tasks
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Response to keypresses"""
        #move ship to the right
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True 
        elif event.key == pygame.K_LEFT:
            #moving ship to the left
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            #moving ship to the left
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bulet and add it to the bullets group"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        #Redraw the screen during each pass through the loop. 
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    #make a game instance, and run the game/.

    ai = AlienInvasion()
    ai.run_game()


