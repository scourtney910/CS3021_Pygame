from constants import Constants
from sys import exit
import pygame


# Initialize Pygame (required to be at top of file).
pygame.init()
screen = pygame.display.set_mode((Constants._screen_w(), Constants._screen_h()))
pygame.display.set_caption("Jump King + Doodle Jump")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)        # Regular font for all text graphics.
small_font = pygame.font.SysFont(None, 30)  # Starting screen font.


def display_text(text: str, color: tuple, x: int, y: int) -> None:
    """
    Helper function to set rendering for on-screen text.
    Input: text, RGB tuple, x, and y coordinate.
    """
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def display_smaller_text(text: str, color: tuple, x: int, y: int) -> None:
    """
    Helper function to set rendering for start screen text
    Input: text, RGB tuple, x, and y coordinate.
    """
    img = small_font.render(text, True, color)
    screen.blit(img, (x, y))


def start_screen() -> None:
    """
    Display the start screen with a 'Start' button, and some useful information.
    """

    player_image = pygame.image.load("player.png").convert_alpha()
    player_rect = player_image.get_rect(center=(Constants._screen_w() // 2, Constants._screen_h() // 3 + 30))

    start_button_color = (128, 239, 128)
    button_rect = pygame.Rect(Constants._screen_w() // 2 - 100, Constants._screen_h() // 2, 200, 50)

    credited_text = "Welcome to Jump King x Doodle Jump!\n\nby:\nSean Courtney, Jason Sherwood, and James Doocy\n\nCS3021"
    tutorial_text = ("In this game, get as high as your little body can take you! (there's no princess\n\n"
                     "at the top of this tower, unfortunately). Use your mouse anywhere on screen.\n\n"
                     "Hold left click to record your initial position, and pull backwards (like\n\n"
                     "a slingshot!) to make the sprite jump. Strawberries are +5pts extra, while\n\n"
                     "each new platform reached is +1pt. If your character hits the bottom of the\n\n"
                     "screen, it's GAME OVER!")

    while True:
        screen.fill((0, 0, 0))

        # Display credited_text centered above the player sprite.
        credited_lines = credited_text.split('\n') # Turn the wall of text into a list.
        for i, line in enumerate(credited_lines):
            text_width, text_height = small_font.size(line)
            display_smaller_text(line, (128, 0, 32), Constants._screen_w() // 2 - text_width // 2, 30 + i * text_height)

        screen.blit(player_image, player_rect)

        pygame.draw.rect(screen, start_button_color, button_rect)
        display_text("Start", (255, 255, 255), button_rect.x + 60, button_rect.y + 5)

        # Display tutorial_text centered under the start button.
        tutorial_lines = tutorial_text.split('\n')
        for i, line in enumerate(tutorial_lines):
            text_width, text_height = small_font.size(line)
            display_smaller_text(line, (128, 0, 32), Constants._screen_w() // 2 - text_width // 2, button_rect.y + 60 + i * text_height)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Start the game.


def always_display_score(score: int) -> None:
    """
    Display score in the top-left corner of the screen. (in white).
    """
    # The starting pixel here is 10 x 10 away from the top left corner.
    display_text(f"Score: {score}", (255, 255, 255), 10, 10)