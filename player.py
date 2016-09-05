
# This module is used to hold the player class.
# The player represents the user-controlled sprite on the screen.


import pygame

import constants

from platforms import MovingPlatform
from spritesheet_functions import SpriteSheet

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player controls."""

    # -- Methods
    def __init__(self):
        """ Contrcutor function """

        # -- Attributes
        # Set speed vector of player
        change_x = 0
        change_y = 0

        # This holds all the images for the animated walk left/right of player
        walking_frames_l = []
        walking_frames_r = []

        # What direction is the player facing?
        direction = "R"

        # List of sprites we can bump against
        level = None


        def __init__(self):
            """ Constructor funciton """

            # Call the parent constructor
            pygame.sprite.Sprite.__init__(self)


            sprite_sheet = SpriteSheet("p1_walk.png")
            # Load all right facing images into a list
            image = sprite_sheet.get_image( 0, 0, 66, 90)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image( 66, 0, 66, 90)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image( 132, 0, 67, 90)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image( 0, 93, 66, 90)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image( 66, 93, 66, 90)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image( 132, 93, 72, 90)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image( 0, 186, 70, 90)
            self.walking_frames_r.append(image)

            # Load all right facing images into a list and flip them to left facing
            image = sprite_sheet.get_image( 0, 0, 66, 90)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image( 66, 0, 66, 90)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image( 132, 0, 67, 90)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image( 0, 93, 66, 90)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image( 66, 93, 66, 90)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image( 132, 93, 72, 90)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image( 0, 186, 70, 90)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_r.append(image)
        
            # Set the image the player starts with
            self.image = self.walking_frames_r[0]

            # Set a reference to images rect.
            self.rect = self.image.get_rect()

        def calc_grav(self):
            """ Calculate the effect of gravity """

            if self.change_y == 0:
                self.change_y = 1
            else:
                self.change_y += .35

            # See if we are on the ground.
            if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
                self.change_y = 0
                self.rect.y = constants.SCREEN_HEIGHT - self.rect.height



        def update(self):
            """ Move the player. """
            # Gravity
            self.calc_grav()

            # Move left/right
            self.rect.x += self.change_x
            pos = self.rect.x + self.level.world_shift
            if self.direction == "R":
                frame = (pos // 30) % len(self.walking_frames_r)
                self.image = self.walking_frames_r[frame]
            else:
                frame = (pos // 30) % len(self.walking_frames_l)
                self.image = self.walking_frames_l[frame]

            # See if we hit anything
            block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            for block in block_hit_list:
                # If we are moving right, set our right side to the left side of the item we hit or vice versa
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    self.rect.left = block.rect.right

            # Move up/down
            self.rect.y += self.change_y

            # Check and see if we hit anything
            block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            for block in block_hit_list:

                # Reset player position based on top/bottom of object.
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom

                # Stop vertical movement
                self.change_y = 0

                if isinstance(block, MovingPlatform):
                    self.rect.x += block.change_x



        def jump(self):
            """ Called when player hits the 'jump' button. """

            # move down a bit and see if there is a platform below us.
            # move down two pixels because it doesn't work well if we only move down 1 when working with a platform moving down
            self.rect.y += 2
            platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            self.rect.y -= 2

            # If it is ok to jump, set our speed upwards
            if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
                self.change_y = -10

        # Player-controlled movement
        def go_left(self):
            """ Called when the user hits left arrow """
            self.change_x = -6
            self.direction = "L"

        def go_right(self):
            """ Called when the user hits the right arrow """
            self.change_x = 6
            self.direction = "R"

        def stop(self):
            """ Called when the user lets off the keyboard """
            self.change_x = 0

            

            
