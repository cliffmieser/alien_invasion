#alien invasion project

#importing sys and pygame. pygame module contains import functionality for the game
#sys module holds tools to exit the game when a player quits
import sys
import pygame 
from time import sleep

from ship import Ship
from game_stats import GameStats
from settings import Settings
from bullet import Bullet
from alien import Alien
from button import Button



class AlienInvasion:

    """Overall class to manage game assets and behaviors"""

    def __init__(self):
        """Initialize game, and create game resources."""
        pygame.init() #initializes background settings for pygame to work properly


        self.settings = Settings() #isntance of Settings 

        #The object assigned to self.screen can be refered as a surface, which is a part of the screen where a game element
        #will be displayed in pygame
        #self.screen = pygame.display.set_mode((0,0 ), pygame.FULLSCREEN) #creates a display window in which all graphic elements are drawn

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #Create an instance to store game statistics.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() #stores bullets in a group
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #mMake the play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""

        while True:
            self._check_events() #calls the _check_events method

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play """
        if self.play_button.rect.collidepoint(mouse_pos):
            self.stats.game_active = True

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
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        #update bullet postions.
        self.bullets.update()
        #get rid of bullets that have dissappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        print(len(self.bullets))
        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            #Destroy eixisting bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()


    def _update_aliens(self):
        """Check if fleet is at an edge, then update position of all aliens """
        self._check_fleet_edges()
        self.aliens.update()

        #Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()



    def _create_fleet(self):
        """Create the fleet of aliens"""
        #create an alien and find the number of aliens in a row
        #spacing between each alein is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (1 * alien_width) #og: (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)                                

        #create full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        #create an alien and place it in a row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number 
        self.aliens.add(alien)
    
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens reach an edge """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    

    def _change_fleet_direction(self):
        """Drop entire fleet and change fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        #Redraw the screen during each pass through the loop. 
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            #Decrement ships left
            self.stats.ships_left -= 1

            #get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.ship.center_ship()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(0.5)
        else:
            self.stats.game_active  = False

    def _check_aliens_bottom(self):
        """Check if any aliens reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if ship got hit
                self._ship_hit()
                break

if __name__ == '__main__':
    #make a game instance, and run the game/.

    ai = AlienInvasion()
    ai.run_game()


