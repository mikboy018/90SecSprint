"""
Sample Python/Pygame Programs
http://programarcadegames.com
http://simpson.edu/computer-science/

Main module for platform scroller example

From:
http://programarcades.com/python_examples/sprite_sheets/

Explanation video: http://youtu.be/czBDKWJq0ao

Game art from Kenny.nl:
http://opengameart.org/content/platformer-art-deluxe
"""

import pygame

import constants
import levels

from player import Player

def main():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("The 90 Second Sprint")

    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append(levels.Level_01(player))
    level_list.append(levels.Level_02(player))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)


    # Loop until the user clicks the close button
    done = False

    # Manage how fast the screen updates
    clock = pygame.time.Clock()

    # ------ Main Program Loop ------------
    while not done:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # User clicks close
                done = True # Flag that we are done allowing us to exit loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # Update the player
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)

        # If the player reaches end level, go to next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list) - 1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level

        # ALL CODE TO DRAW BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)


        # ALL CODE TO DRAW ABOVE THIS COMMENT

        # Limit to 60 fps
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn
        pygame.display.flip()

    # Allow for exit
    pygame.quit()

if __name__ == "__main__":
    main()
    
        
            
