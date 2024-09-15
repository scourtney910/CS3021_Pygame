from constants import Constants
from typing import Any
import pygame


class Player(pygame.sprite.Sprite, Constants):
    """
    Define player functionality for the player interacting with everything.
    """

    def __init__(self):
        """
        Initialize all the player attributes.
        """
        # Player uses has-a relationship from pygame.
        super().__init__()  # Take attributes from pygame module, inheriting attributes from pygame.

        self.original_image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.original_image, (self._player_w(), self._player_h())
        )

        self.rect = self.image.get_rect()  # Forcing player hit box into a square.

        self.velocity_y = 0
        self.velocity_x = 0
        self.is_jumping = False

    def jump(self, vector: tuple) -> None:
        """
        Change player state to recognize sprite jumping. The
        vector expected is from the calculate_vector() function.
        """
        self.velocity_x, self.velocity_y = vector
        self.is_jumping = True

    def update(self) -> bool:
        """
        Update player position on screen based on changing attributes.
        """

        if self.is_jumping:

            self.velocity_y += self._grav()
            # Too high a velocity will cause the player to fall
            # through platforms before the collision can be checked.
            self.velocity_y = min(self.velocity_y, self._max_velocity())

            self.rect.y += self.velocity_y
            self.rect.x += self.velocity_x

            if self.rect.bottom >= self._screen_h():
                # Game Over is set.
                return True

        # Wrap around the screen:
        if self.rect.right > (self._screen_w() + (self._player_w() / 2)):
            # If half the player sprite is off the right side of the screen...
            self.rect.left = 0 - (self._player_w() / 2)
            # then move the player to the left side of the screen, but half-off.

        elif self.rect.left < (0 - self._player_w() / 2):
            # If half the player sprite is off the left side of the screen...
            self.rect.right = self._screen_w() + (self._player_w() / 2)
            # then move the player to the right side of the screen, but half-off.

        # All previous checks did not change the state of play.
        return False

    def check_collision(
            self,
            platforms: Any, 
            items: Any, 
            touched_platforms: set, 
            score: int
            ) -> int:
        """
        Check for collision only when falling. To change the platforms structure,
        change the generate_platforms function in helper_functions.py
        """

        # platform_collision_detection is a list of platforms the player sprite 
        # has touched each game loop.
        platform_collision_detection = pygame.sprite.spritecollide(self, platforms, False)

        for platform in platform_collision_detection:
            # In short: "falling" = (+)velocity_y, which means "jumping" = (-)velocity_y.
            if self.velocity_y > 0:
                # Continue with normal collision routine.

                # This code is for the bottom of the player and the top of the platform:
                if self.rect.bottom <= platform.rect.top + 20:
                    self.rect.bottom = platform.rect.top

                    # Assigning player bottom to the top of a platform represented by rect.top.
                    # This only works because the only thing the player can land on is a platform.
                    self.velocity_y = 0
                    self.is_jumping = False

                if (platform not in touched_platforms) and (self.velocity_y == 0):
                    # The score-variable will only increment when
                    # the player touches a new platform on screen.
                    touched_platforms.add(platform)
                    score += 1

        # Similarly for items, only remove the item if it's collected.
        item_collision_detection = pygame.sprite.spritecollide(self, items, False)
        
        for item in item_collision_detection:
            item.kill()
            score += Constants._item_score()

            # Make a sound collecting the item.
            item_get = pygame.mixer.Sound("denethor.mp3")
            item_get.set_volume(0.9)
            item_get.play()
            score += Constants._item_score()

        return score


class Platform(pygame.sprite.Sprite, Constants):
    """
    Define platform attributes using pygame module.
    """

    def __init__(self, x: int, y: int):

        super().__init__()
        self.original_image = pygame.image.load("platform.png").convert_alpha()
        self.image = pygame.transform.scale(
          self.original_image, (self._platform_w(), self._platform_h())
        )

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.was_touched = False    # Used for collision


class Items(pygame.sprite.Sprite, Constants):
    """
    Define item attributes using pygame module.
    """

    def __init__(self, x: int, y: int):
        super().__init__()
        self.original_image = pygame.image.load("strawberry.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.original_image, (self._item_size(), self._item_size())
        )

        # Creating rectangular object with width = x and height = y.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.was_touched = False