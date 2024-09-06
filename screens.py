from constants import Constants
from sys import exit
import pygame


# Initialize Pygame (required to be at top of main file)
pygame.init()
screen = pygame.display.set_mode((Constants._screen_w(), Constants._screen_h()))
pygame.display.set_caption("Jump King + Doodle Jump")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def display_text(text: str, color: tuple, x: int, y: int) -> None:
    """Helper function to set rendering for Game Over Screen"""
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def start_screen():
    """Display the start screen with a 'Start' button."""
    background_image = pygame.image.load("background.png").convert()
    player_image = pygame.image.load("player.png").convert_alpha()
    player_image = pygame.transform.scale(player_image, (Constants._player_w(), Constants._player_h()))
    player_rect = player_image.get_rect(center=(Constants._screen_w() // 2, Constants._screen_h() // 3))

    start_button_color = (0, 255, 0)
    button_rect = pygame.Rect(Constants._screen_w() // 2 - 100, Constants._screen_h() // 2, 200, 50)

    while True:
        screen.blit(background_image, (0, 0))
        screen.blit(player_image, player_rect)
        pygame.draw.rect(screen, start_button_color, button_rect)
        display_text("Start", (255, 255, 255), button_rect.x + 60, button_rect.y + 5)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Start the game

def add_score_display(score):
    """Display score in the top-left corner of the screen."""
    display_text(f"Score: {score}", (255, 255, 255), 10, 10)