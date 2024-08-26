from constants import Constants
import pygame
from typing import Any


class Player(pygame.sprite.Sprite, Constants):
    """define player functionality"""

    def __init__(self):
        """Initialize all the player attributes"""
        # Player uses has-a relationship from pygame
        super().__init__()  # take attributes form pygame module, inheriting attributes from pygame

        self.original_image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.original_image, (self._player_w(), self._player_h())
        )

        self.rect = self.image.get_rect()  # forcing player hot box into  a square

        self.velocity_y = 0
        self.velocity_x = 0
        self.is_jumping = False

    def jump(self, vector: tuple) -> None:
        """change player state to recognize sprite jumping
        vector expected is from the calculate_vector function"""

        self.velocity_x, self.velocity_y = vector
        self.is_jumping = True

    def update(self):
        """update player position on screen based on changing attributes"""

        if self.is_jumping:

            self.velocity_y += self._grav()
            # too high a velocity will cause the player to
            # fall through platforms before the collision can be checked
            self.velocity_y = min(self.velocity_y, self._max_velocity())

            self.rect.y += self.velocity_y
            self.rect.x += self.velocity_x

            if self.rect.bottom >= self._screen_h():
                # Game Over is set
                return True

        # Wrap around the screen
        if self.rect.right > (self._screen_w() + (self._player_w() / 2)):
            # if half the player sprite is off the right side of the screen
            self.rect.left = 0 - (self._player_w() / 2)
            # move the player to the left side of the screen, but half-off

        elif self.rect.left < (0 - self._player_w() / 2):
            # if half the player sprite is off the left side of the screen
            self.rect.right = self._screen_w() + (self._player_w() / 2)
            # move the player to the right side of the screen, but half-off

        # All previous checks did not change the state of play
        return False

    def check_collision(
        self, platforms: Any, touched_platforms: set, score: int
    ) -> int:
        """
        Check for collision only when falling.
        To change the platforms structure,
        change the generate_platforms function in main.
        """
        # collision_detection is a list of platforms the player sprite has touched each game loop
        collision_detection = pygame.sprite.spritecollide(self, platforms, False)

        for platform in collision_detection:
            # "if sprite is falling", (+)velocity_y means falling and neg means jumping
            if self.velocity_y > 0:
                # continue with normal collision routine
                # this code for bottom of char and top of platform
                if self.rect.bottom <= platform.rect.top + 20:
                    self.rect.bottom = platform.rect.top
                    # assigning player bottom to top of platform represented by rect top,
                    # i.e. only works because the only thing the player can hit is a platform
                    self.velocity_y = 0
                    self.is_jumping = False

                if (platform not in touched_platforms) and (self.velocity_y == 0):
                    # fix the score-variable to increment only when
                    # the player touches a new platform on screen
                    touched_platforms.add(platform)
                    score += 1

        return score


class Platform(pygame.sprite.Sprite, Constants):
    """define platform size and color using pygame module
    attributes must be referenced later"""

    def __init__(self, x, y):

        super().__init__()
        self.image = pygame.Surface((self._platform_w(), self._platform_h()))
        self.image.fill(self._platform_rgb())

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.was_touched = False  # new boolean added
