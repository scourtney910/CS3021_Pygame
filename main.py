from constants import *
from sprites import *
from screens import *
from helper_functions import *
from sys import exit
from time import sleep
import pygame

# Pygame is initialized in screens.py for easier workflow.


def play() -> None:
    """Main game loop"""
    # Load background image and sprites.
    background_image = pygame.image.load("background.png").convert()  # Loading image.
    player = Player()  # Create the player sprite.
    # Manually choose number of platforms here...
    platforms, items, lowest_platform, highest_platform = generate_platforms(8)
    player.rect.center = (
        lowest_platform.rect.centerx,
        lowest_platform.rect.top - Constants._player_h() // 2,
    )

    # Move all sprites into one sprite.group for use in the main game loop.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(platforms)
    all_sprites.add(items)

    # Initialize starting values.
    dragging = False
    start_left_click = (0, 0)  # Tuple for the starting mouse position on screen.
    score = 0
    game_over = False
    touched_platforms = set()  # To be used in updating the score.

    # Prevent the score from incrementing when jumping on the starting platform:
    lowest_platform.was_touched = True
    touched_platforms.add(lowest_platform)

    while not game_over:
        # Events are a method in pygame to check for certain conditions.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit = Red x on the top right of the window
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:  # Left click.

                # If player isn't jumping, allow click.
                if not player.is_jumping:
                    dragging = True
                    start_left_click = pygame.mouse.get_pos()

            elif event.type == pygame.MOUSEBUTTONUP:  # Release left click.

                if dragging:
                    end_left_click = pygame.mouse.get_pos()
                    vector = calculate_vector(start_left_click, end_left_click)
                    player.jump(vector)
                    dragging = False

        # Increment the score only when the game is not over
        # And the player made a successful jump.
        if not game_over:
            game_over = player.update()  # Player movement takes place here.

            # Check for collisions after sprite is updated each frame.
            # Collisions is within the Player class, because the player touches everything.
            score = player.check_collision(platforms, items, touched_platforms, score)

        if highest_platform in touched_platforms:
            all_sprites, lowest_platform, highest_platform = refresh_screen(
                all_sprites,
                player,
                platforms,
                items,
                touched_platforms,
                highest_platform,
            )
            sleep(0.5)

        # Background image setter.
        screen.blit(background_image, (0, 0))

        # Drawing updated character position for each frame.
        # Would apply to platforms if they were also moving.
        all_sprites.draw(screen)
        always_display_score(score)

        pygame.display.flip()
        clock.tick(Constants._fps())
        # End while-loop.

    # If Game Over is reached, execute this function to display
    # results and give the player the option to restart.
    game_over_screen(score)


def game_over_screen(score: int) -> None:
    """Display the 'Game Over' screen and trigger restart or quit."""
    # Save player score to a CSV.
    highscore = save_score(score)
    button_rect = pygame.Rect(
        Constants._screen_w() // 2 - 100, Constants._screen_h() // 2 + 50, 200, 50
    )

    while True:
        screen.fill((0, 0, 0))  # Overwrite the screen with a black background.

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

        # Impliment restart button tie-in.
        pygame.draw.rect(screen, (128, 239, 128), button_rect)
        display_text("Restart", (255, 255, 255), button_rect.x + 40, button_rect.y + 5)
        pygame.display.flip()

        # Since we are out of the game loop, we need to account for
        # whenever we quit the game (exiting the window).
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit = Red x on the top right of the window
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    restart()  # Play the game loop from the beginning.


def restart() -> None:
    """Restart the game by re-entering the game loop"""
    play()


if __name__ == "__main__":
    start_screen()  # Only shown once on boot-up.
    play()
