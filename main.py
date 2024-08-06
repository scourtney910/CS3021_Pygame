import pygame
import sys
import random
import math
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))


# Constants
SCREEN_WIDTH      = 800
SCREEN_HEIGHT     = 600
FPS               = 60
GRAVITY           = 0.5
PLAYER_WIDTH      = 50 #use to change player size
PLAYER_HEIGHT     = 50
PLATFORM_WIDTH    = 100
PLATFORM_HEIGHT   = 20
# PLATFORM_COLOR    = (0, 255, 0)
PLATFORM_COLOR    = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
MAX_JUMP_STRENGTH = 20


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jump King + Doodle Jump')
clock = pygame.time.Clock()



class Player(pygame.sprite.Sprite):
    """define player functionality"""

    def __init__(self):
        """Initialize all the player attributes"""

        super().__init__() #take attributes form pygame module, inheriting attributes from pygame has is a ?
        self.original_image = pygame.image.load('player.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.original_image,
            (PLAYER_WIDTH, PLAYER_HEIGHT)
            )

        self.rect = self.image.get_rect() #forcing player hot box into  a square
        self.rect.center = ( #starting location for sprite
            SCREEN_WIDTH // 2, 
            SCREEN_HEIGHT - self.rect.height // 2
            )

        self.velocity_y = 0
        self.velocity_x = 0
        self.is_jumping = False


    def jump(self, vector):

        self.velocity_x, self.velocity_y = vector
        self.is_jumping = True


    def update(self):
        """
        update player position on screen based on changing attributes
        """

        if self.is_jumping:

            self.velocity_y += GRAVITY

            self.rect.y += self.velocity_y
            self.rect.x += self.velocity_x

            if self.rect.bottom >= SCREEN_HEIGHT:

                self.rect.bottom = SCREEN_HEIGHT
                self.is_jumping = False

        # Wrap around the screen
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0


    def check_collision(self, platforms):
        """
        Check for collision only when falling.
        To change the platforms structure,
        change the generate_platforms function below.
        Need to add collisin for bottom of platforms
        """
        if self.velocity_y > 0: #sprite is falling, pos vel in y means falling and neg means jumping

            hits = pygame.sprite.spritecollide(self, platforms, False) #hits is a list of something about collisions
            """ sprite collide checks for collision of sprite and platforms and returns lists"""

            if hits: #if list is not empty
                # this code for bottom of char and top of platform
                #shoudl use if statement for bottom and another if statement for top
                self.rect.bottom = hits[0].rect.top 
                """assigning player bottom to top of platform represent by rect top, i.e. only wokrs because the only thign player can hit is a platform"""
                self.velocity_y = 0
                self.is_jumping = False
                #if top of sprite hits bottom of platform:
                #self.velocity = 0
                #self.is_jumping = False
                


class Platform(pygame.sprite.Sprite):
    """define platform size and generation"""

    def __init__(self, x, y):

        super().__init__()
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(PLATFORM_COLOR)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def generate_platforms(num_platforms: int) -> set: 
    #returning a tuple  each tuple represents a platform, inside the tuple are the nuts and bolts of each platform

    platforms = pygame.sprite.Group()

    for _ in range(num_platforms):

        x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT - PLATFORM_HEIGHT)
        platform = Platform(x, y) # object / isntantiation of platform class
        platforms.add(platform) #adding the instanced platform to group Platform

    return platforms


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


##############################################################
############################ MAIN ############################
##############################################################
def main() -> None:
    """Run the main game loop here. Program exits when game is killed."""

    # Load background image
    background_image = pygame.image.load('background.png').convert() # loading image
    player = Player() #create sprite
    all_sprites = pygame.sprite.Group() #might need to make a function to create characters for multiplayer
    all_sprites.add(player)

    platforms = generate_platforms(10) #manually chose number of platforms here
    all_sprites.add(platforms)

    dragging = False
    start_pos = (0, 0) # initializing tuple here for mouse position, change name

    while True:

        for event in pygame.event.get(): #event is class in pygame to check for certain conditions, like quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN: #left click

                if not player.is_jumping: #if player isnt jumping allow click
                    dragging = True
                    start_pos = pygame.mouse.get_pos()

            elif event.type == pygame.MOUSEBUTTONUP: #release left click

                if dragging:
                    end_pos = pygame.mouse.get_pos()
                    vector = calculate_vector(start_pos, end_pos)
                    player.jump(vector)
                    dragging = False
        
        player.update() #player movement function
        player.check_collision(platforms) #only checking for collisions after exiting update, whcih means my y velocity is pos/downwards

        screen.blit(background_image, (0, 0)) #centering background image
        all_sprites.draw(screen) #drawing updated character postion onto screen including platforms
        
        pygame.display.flip()
        clock.tick(FPS) #ticking forward clock


if __name__ == "__main__":
    main()
