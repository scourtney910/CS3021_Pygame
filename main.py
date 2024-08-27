from constants import Constants
import csv
import math
import pygame
from random import randint
from sprite import Player, Platform
from sys import exit
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


def generate_platforms(num_platforms: int) -> tuple[Any, Any, Any]:
    """
    randomly generate rectangle platforms and return:
    pygame.sprite.Group: Any, lowest_platform.sprite: Any, highest_platform.sprite: Any
    """

    platform_sprites = pygame.sprite.Group()
    lowest_y = 0
    highest_y = Constants._screen_h()
    lowest_platform = None
    highest_platform = None

    for _ in range(num_platforms):

        x = randint(0, Constants._screen_w() - Constants._platform_w())
        y = randint(0, Constants._screen_h() - Constants._platform_h())
        platform = Platform(x, y)  # object / isntantiation of platform class

        # adding the instanced platform to group Platform
        platform_sprites.add(platform)

        if y > lowest_y:
            lowest_y = y  # update the if-condition for every for-loop iteration
            lowest_platform = platform  # update the future return value

        if y < highest_y:
            highest_y = y
            highest_platform = platform

    return platform_sprites, lowest_platform, highest_platform


def refresh_screen(all_sprites, player, platforms, touched_platforms, highest_platform):
    """
    Once the player reaches the top platform on screen, translate player position and platform position to the bottom of the screen.
    Then, generate new platforms above it. New platform attributes get reset manually before function return.
    """
    new_player_bottom = Constants._screen_h() - Constants._platform_h()
    player.rect.bottom = new_player_bottom  # preserves player x-location, changing y

    restart_platform = Platform(highest_platform.rect.x, Constants._screen_h())

    touched_platforms.clear()
    for platform in platforms:
        platform.kill()
        all_sprites.remove(platform)

    new_platforms, lowest_platform, highest_platform = generate_platforms(9)
    lowest_platform = restart_platform
    lowest_platform.was_touched = True
    touched_platforms.add(lowest_platform)
    all_sprites.add(lowest_platform)
    all_sprites.add(new_platforms)

    return all_sprites, lowest_platform, highest_platform


def calculate_vector(start_left_click: tuple, end_left_click: tuple) -> tuple:
    """
    return a tuple where each vector element carries a magnitude and radian position (as a float)
    """

    dx = end_left_click[0] - start_left_click[0]
    dy = end_left_click[1] - start_left_click[1]
    distance = math.sqrt(dx**2 + dy**2)

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
    platforms, lowest_platform, highest_platform = generate_platforms(10)
    player.rect.center = (
        lowest_platform.rect.centerx,
        lowest_platform.rect.top - Constants._player_h() // 2,
    )

    # these lines work when creating one player, but will be moved when creating multiplayer
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(platforms)

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
            score = player.check_collision(platforms, touched_platforms, score)

        if highest_platform in touched_platforms:
            all_sprites, lowest_platform, highest_platform = refresh_screen(
                all_sprites, player, platforms, touched_platforms, highest_platform
            )

        # background image setter
        # randomize background_image later
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
