from constants import Constants
import csv
import math
import pygame
from random import randint
from sprite import Player, Platform, Items
from sys import exit
from time import sleep
from typing import Any


# Initialize Pygame (required to be at top of main file)
pygame.init()
screen = pygame.display.set_mode((Constants._screen_w(), Constants._screen_h()))
pygame.display.set_caption("Jump King + Doodle Jump")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


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
        y = randint(0, Constants._screen_h() - Constants._platform_h())
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


def refresh_screen(all_sprites, player, platforms, items, touched_platforms, highest_platform):
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
    new_platforms, new_item_sprites, lowest_platform, new_highest_platform = generate_platforms(9)

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


def display_text(text: str, color: tuple, x: int, y: int) -> None:
    """Helper function to set rendering for Game Over Screen"""
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


##############################################################
############################ MAIN ############################
##############################################################


def main() -> None:
    """Run the main game loop here. Program exits when game is killed."""

    # Load background image and sprites
    background_image = pygame.image.load("background.png").convert()  # loading image
    player = Player()  # create sprite
    # manually choose number of platforms here
    platforms, items, lowest_platform, highest_platform = generate_platforms(10)
    player.rect.center = (
        lowest_platform.rect.centerx,
        lowest_platform.rect.top - Constants._player_h() // 2,
    )

    # these lines work when creating one player, but would be moved when creating multiplayer
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(platforms)
    all_sprites.add(items)

    # initialize starting values
    dragging = False
    start_left_click = (0, 0)  # initialize tuple here for mouse position
    score = 0
    game_over = False
    touched_platforms = set()  # to be used in the score mechanic

    # main game-loop
    while True:

        # events are a method in pygame to check for certain conditions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # red x on top right of window
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:  # left click

                # if player isn't jumping, allow click
                if not player.is_jumping:
                    dragging = True
                    start_left_click = pygame.mouse.get_pos()

            elif event.type == pygame.MOUSEBUTTONUP:  # release left click

                if dragging:
                    end_left_click = pygame.mouse.get_pos()
                    vector = calculate_vector(start_left_click, end_left_click)
                    player.jump(vector)
                    dragging = False

        # Increment the score only when the game is not over
        # And the player made a successful jump
        if not game_over:
            game_over = player.update()  # player movement takes place here

            # check for collisions after sprite is updated each frame
            score = player.check_collision(platforms, items, touched_platforms, score)

        if highest_platform in touched_platforms:
            all_sprites, lowest_platform, highest_platform = refresh_screen(
                all_sprites, player, platforms, items, touched_platforms, highest_platform
            )
            sleep(0.5)

        # background image setter
        screen.blit(background_image, (0, 0))

        # drawing updated character position each frame.
        # Would apply to platforms if they were also moving
        all_sprites.draw(screen)

        if game_over:
            # save player score to a CSV
            highscore = save_score(score)

            # display_text(str, color, x_pos, y_pos)
            display_text(
                "Game Over",
                (255, 0, 0),
                (Constants._screen_w() // 2 - 100),
                (Constants._screen_h() // 2 - 100),
            )
            display_text(
                f"Score: {score}",
                (255, 255, 255),
                (Constants._screen_w() // 2 - 100),
                (Constants._screen_h() // 2 - 50),
            )
            display_text(
                f"High Score: {highscore}",
                (0, 255, 255),
                (Constants._screen_w() // 2 - 100),
                (Constants._screen_h() // 2),
            )

        pygame.display.flip()
        clock.tick(Constants._fps())


if __name__ == "__main__":
    main()
