import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen


        #load the alien image and set its rect attribute.
        #picture  = pygame.image.load('images/EnemyShip.bmp')
        #picture = pygame.transform.scale(picture, (800, 800))

        
        self.image = pygame.image.load('images/EnemyShipTwo.bmp')
        self.rect = self.image.get_rect()

        #Start each new alien near the top lef tof the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the alien's exact horizontal position
        self.x = float(self.rect.x)