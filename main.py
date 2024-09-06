from constants import *
from sprites import *
from screens import *
from helper_functions import *
from sys import exit
from time import sleep
from typing import Any
import pygame
# pygame initialized in screens.py for easier workflow


def play():
    """Main game loop"""
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
    # prevent the score from incrementing when jumping on the starting platform
    lowest_platform.was_touched = True
    touched_platforms.add(lowest_platform)

    while not game_over:
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
        add_score_display(score)

        pygame.display.flip()
        clock.tick(Constants._fps())

    # if Game Over is reached, execute this function to display
    # results and give the player the option to restart
    game_over_screen(score)


def game_over_screen(score):
    """Display the 'Game Over' screen and handle restart."""
    # save player score to a CSV
    highscore = save_score(score)
    button_rect = pygame.Rect(Constants._screen_w() // 2 - 100, Constants._screen_h() // 2 + 50, 200, 50)

    while True:
        screen.fill((0, 0, 0)) # overwrite the screen with a black background

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

        # impliment restart button tie-in
        pygame.draw.rect(screen, (0, 255, 0), button_rect)
        display_text("Restart", (255, 255, 255), button_rect.x + 40, button_rect.y + 5)
        pygame.display.flip()

        # since we are out of the game loop, we need to account for
        # whenever we quit the game (exiting the window)

        # events are a method in pygame to check for certain conditions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:    # red x on top right of window
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    restart()    # play the game loop from the beginning


def restart():
    """Restart the game by re-entering the game loop"""
    play()


if __name__ == "__main__":
    start_screen()    # only shown once on boot-up
    play()