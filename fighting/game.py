import pygame
import sys

from fighting.start import *


def create_button(image_path, width, height, x_pos, y_pos):
    # Load and scale image
    button_image = pygame.image.load(image_path)
    button_image = pygame.transform.scale(button_image, (width, height))
    # Create and center button rectangle
    button_rect = button_image.get_rect()
    button_rect.center = (x_pos, y_pos)
    return button_image, button_rect


def menu_background(image):
    background_image = pygame.image.load(image)
    background_image = pygame.transform.scale(
        background_image, (screen_width, 550))
    screen.blit(background_image, (0, 0))


# Creating Play button
play_image, play_button = create_button(
    'fighting/Images/assets/play.png', 175, 100, screen_width // 2, 300)

# Creating Quit Button
quit_image, quit_button = create_button(
    'fighting/Images/assets/quit.png', 200, 100, screen_width // 2, 425)


class Game():
    pygame.init()

    def run():
        while True:

            MOUSE_POS = pygame.mouse.get_pos()
            menu_background('fighting/Images/background/menu_background.png')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(MOUSE_POS):
                        play_Game()
                    elif quit_button.collidepoint(MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            screen.blit(play_image, play_button)
            screen.blit(quit_image, quit_button)

            pygame.display.flip()
            pygame.display.update()
