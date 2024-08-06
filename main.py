import pygame
import random
import sys
from typing import Any, Union
import math


# Constants
SCREEN_WIDTH      = 800
SCREEN_HEIGHT     = 600
FPS               = 60
GRAVITY           = 0.5
PLAYER_WIDTH      = 50
PLAYER_HEIGHT     = 50
PLATFORM_WIDTH    = 100
PLATFORM_HEIGHT   = 20
PLATFORM_COLOR    = (0, 255, 0)
MAX_JUMP_STRENGTH = 20


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jump King + Doodle Jump')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


class Player(pygame.sprite.Sprite):
    """define player functionality"""

    def __init__(self):
        """Initialize all the player attributes"""

        super().__init__()
        self.original_image = pygame.image.load('player.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.original_image,
            (PLAYER_WIDTH, PLAYER_HEIGHT)
            )

        self.rect = self.image.get_rect()

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

            self.velocity_y += GRAVITY

            self.rect.y += self.velocity_y
            self.rect.x += self.velocity_x

            if self.rect.bottom >= SCREEN_HEIGHT:
                # Game Over is set
                return True

        # Wrap around the screen
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        
        # All previous checks did not change the state of play
        return False


    def check_collision(self, platforms: Any) -> None:
        """
        Check for collision only when falling.
        To change the platforms structure,
        change the generate_platforms function below.
        """
        if self.velocity_y > 0:

            hits = pygame.sprite.spritecollide(self, platforms, False)

            if hits:
                self.rect.bottom = hits[0].rect.top
                self.velocity_y = 0
                self.is_jumping = False


class Platform(pygame.sprite.Sprite):
    """define platform size and generation"""

    def __init__(self, x, y):

        super().__init__()
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(PLATFORM_COLOR)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def generate_platforms(num_platforms: int) -> tuple[Any, Any]:
    """randomly generate rectangle platforms and return:
    pygame.sprite.Group: Any, lowest_platform.sprite: Any"""

    platforms = pygame.sprite.Group()
    lowest_y = 0
    lowest_platform = None

    for _ in range(num_platforms):

        x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT - PLATFORM_HEIGHT)
        platform = Platform(x, y)
        platforms.add(platform)

        if y > lowest_y:
            lowest_y = y    #update the if-condition for every for-loop iteration
            lowest_platform = platform    #update the future return value

    return platforms, lowest_platform


def calculate_vector(start_pos: tuple, end_pos: tuple) -> tuple:
    """
    start_pos is when the mouse's left click is pressed
    end_pos is when the left click is released
    """

    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    distance = math.sqrt(dx ** 2 + dy ** 2)

    #scale the strength
    strength = min(distance / 10, MAX_JUMP_STRENGTH)
    angle = math.atan2(dy, dx)

    #invert x-axis for leftward jump
    vector_x = -strength * math.cos(angle)

    #invert y-axis for upward jump
    vector_y = -strength * math.sin(angle)

    return (vector_x, vector_y)

def display_text(text, color, x, y) -> None:
    """Helper function to set rendering for Game Over Screen"""
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


##############################################################
############################ MAIN ############################
##############################################################


def main() -> None:
    """Run the main game loop here. Program exits when game is killed."""

    # Load background image and sprites
    background_image = pygame.image.load('background.png').convert()
    player = Player()
    platforms, lowest_platform = generate_platforms(10)
    player.rect.center = (lowest_platform.rect.centerx, lowest_platform.rect.top - PLAYER_HEIGHT // 2)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(platforms)

    #initialize starting values
    dragging = False
    start_pos = (0, 0)
    score = 0
    game_over = False

    #main game-loop
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if not player.is_jumping:
                    dragging = True
                    start_pos = pygame.mouse.get_pos()

            elif event.type == pygame.MOUSEBUTTONUP:

                if dragging:
                    end_pos = pygame.mouse.get_pos()
                    vector = calculate_vector(start_pos, end_pos)
                    player.jump(vector)
                    dragging = False

        #Increment the score only when the game is not over
        #And the player made a successful jump
        if not game_over:
            game_over = player.update()
            player.check_collision(platforms)
            if not player.is_jumping:
                score += 1

        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        
        if game_over:
            display_text('Game Over', (255, 0, 0), (SCREEN_WIDTH // 2 - 100), (SCREEN_HEIGHT // 2 - 50))
            display_text(f'Score: {score}', (255, 255, 255), (SCREEN_WIDTH // 2 - 100), (SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
