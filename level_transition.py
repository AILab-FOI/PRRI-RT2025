import pygame as pg
import sys
from settings import *

class LevelTransition:
    def __init__(self, game):
        self.game = game
    
    def transition_to_next_level(self):
        """Handle the transition to the next level with loading screen"""
        next_level_num = self.game.level_manager.current_level + 1
        
        if next_level_num > self.game.level_manager.max_level:
            print("Congratulations! You have completed all levels!")
            return False
            
        # Start the loading screen
        self.game.loading_screen.start(next_level_num)
        start_time = pg.time.get_ticks()
        duration = 2000
        
        # Run the loading screen loop
        while pg.time.get_ticks() - start_time < duration:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                # Allow skipping the loading screen with spacebar (for testing)
                elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    break
                    
            self.game.loading_screen.update()
            self.game.loading_screen.draw()
            pg.display.flip()
            self.game.clock.tick(60)
            
        # Show a message that we're loading the level
        self.game.loading_screen.draw()
        self.game.loading_screen.set_custom_message("LOADING LEVEL...")
        pg.display.flip()
        
        # Load the next level
        self.game.level_manager.current_level = next_level_num
        self.game.map.load_level(next_level_num)
        self.game.new_game()
        
        return True
