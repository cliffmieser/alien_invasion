#alien invasion project

#importing sys and pygame. pygame module contains import functionality for the game
#sys module holds tools to exit the game when a player quits
import sys 
import pygame

class AlianInvasion:

    """Overall class to manage game assets and behaviors"""

    def __init__(self):
        """Initialize game, and create game resources."""
        pygame.init() #initializes background settings for pygame to work properly

        #The object assigned to self.screen can be refered as a surface, which is a part of the screen where a game element 
        #will be displayed in pygame
        self.screen = pygame.display.set_mode((1200, 800)) #creates a display window in which all graphic elements are drawn                                                
        pygame.display.set_caption("Alien Invasion")


    def run_game(self):
        """Start the main loop for the game."""

        while True:
            # watch for keyboard and mouse events.
            #An event is an action that the use performs while playing the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT():
                    sys.exit()

            # Make the most recently drawn screen visible
            pygame.display.flip()

if __name__ == '__main__':
    #make a game instance, and run the game/.

    ai = AlienInvasion()
    ai.run_game()