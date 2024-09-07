from constants import Constants
from sprites import Platform, Items
from random import randint
import math
from typing import Any
import pygame



##############################################################
###################### HELPER FUNCTIONS ######################
##############################################################
def generate_platforms(num_platforms: int) -> tuple[Any, Any, Any, Any]:
    """
    randomly generate rectangle platforms and return:
    platform_sprites.Group: Any, item_sprites.Group: Any, lowest_platform.sprite: Any, highest_platform.sprite: Any
    """

    platform_sprites = pygame.sprite.Group()
    item_sprites = pygame.sprite.Group()
    lowest_y = 0
    highest_y = Constants._screen_h()
    lowest_platform = None
    highest_platform = None
    lowest_item = None

    for i in range(num_platforms):

        x = randint(0, Constants._screen_w() - Constants._platform_w())
        y = randint(30, Constants._screen_h() - Constants._platform_h())
        platform = Platform(x, y)  # object / isntantiation of platform class

        # adding the instanced platform to group Platform
        platform_sprites.add(platform)

        # generate a random number check. If it's even, create an item platform
        if (randint(0, Constants._screen_w()) % Constants._even()) or (i == 0):
            # for the i == 0 case, we need to create at least one item for lowest_item
            item = Items(x + Constants._item_xoffset(), y - Constants._item_yoffset())

        # try to add items. If item was not created during this loop - pass
        try:
            item_sprites.add(item)
        except:
            pass

        if y > lowest_y:
            lowest_y = y  # update the if-condition for every for-loop iteration
            lowest_platform = platform  # update the future return value
            try:
                lowest_item = item  # keep track of lowest item
            except:
                pass

        if y < highest_y:
            highest_y = y
            highest_platform = platform

    lowest_item.kill() # remove the item from the player's starting platform
    return platform_sprites, item_sprites, lowest_platform, highest_platform


def refresh_screen(
        all_sprites: Any, player: Any, platforms: Any, items: Any, touched_platforms: set, highest_platform: Any
) -> tuple[Any, Any, Any]:
    """
    Once the player reaches the top platform on screen, translate player position and platform position to the bottom of the screen.
    Then, generate new platforms above it. New platform attributes get reset manually before function return.
    """
    # Set the player's position to the bottom of the screen
    new_player_bottom = Constants._screen_h() - Constants._platform_h()
    player.rect.bottom = new_player_bottom  # preserves player x-location, changing y

    # Create a new platform at the bottom of the screen with the same x position as the highest platform
    restart_platform = Platform(highest_platform.rect.x, Constants._screen_h() - Constants._platform_h())

    # Remove all old sprites
    for platform in platforms.sprites():
        platform.kill()  # This removes the sprite from all groups and flags it for deletion
    
    for item in items.sprites():
        item.kill()

    # Clear the sprite groups
    touched_platforms.clear()
    platforms.empty()
    items.empty()
    all_sprites.empty()

    # Add the restart platform to the groups before generating new platforms
    platforms.add(restart_platform)
    all_sprites.add(restart_platform)
    all_sprites.add(player)    # the empty() above removed the player

    # Generate new platforms and add them to the groups
    new_platforms, new_item_sprites, lowest_platform, new_highest_platform = generate_platforms(7)

    # Add the new platforms to the sprite groups
    platforms.add(new_platforms)
    all_sprites.add(new_platforms)
    
    # Add the new platforms to the sprite groups
    items.add(new_item_sprites)
    all_sprites.add(new_item_sprites)

    # Update the touched platforms
    restart_platform.was_touched = True
    touched_platforms.add(restart_platform)

    return all_sprites, restart_platform, new_highest_platform


def calculate_vector(start_left_click: tuple, end_left_click: tuple) -> tuple:
    """
    return a tuple where each vector element carries a magnitude and radian position (as a float)
    """

    dx = end_left_click[0] - start_left_click[0]
    dy = end_left_click[1] - start_left_click[1]
    distance = math.sqrt(dx ** 2 + dy ** 2)

    # scale the strength
    strength = min(distance / 10, Constants._max_jump())
    angle = math.atan2(dy, dx)

    # invert x-axis for leftward jump
    vector_x = -strength * math.cos(angle)

    # invert y-axis for upward jump
    vector_y = -strength * math.sin(angle)

    return (vector_x, vector_y)


def save_score(score: int) -> int:
    # Read the existing score from the file
    try:
        with open("highScore.csv", "r") as csvfile:
            content = csvfile.readline()
            if content:
                high_score = int(content)
            else:
                high_score = 0

    except FileNotFoundError:
        # If the file does not exist, set the high_score to 0
        high_score = 0

    # Check if the new score is higher than the existing high score
    if score > high_score:
        with open("highScore.csv", "w") as csvfile:
            csvfile.write(str(score))
        return score
    else:
        return high_score