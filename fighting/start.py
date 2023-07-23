import pygame
import sys
import random
import button

from pygame import mixer  # Initialize mixer

pygame.init()

mixer.music.load("fighting/Images/assets/Cipher2.mp3")
mixer.music.set_volume(0.2)

mixer.music.play()

clock = pygame.time.Clock()
fps = 30  # Used later to set the FPS of the game

bottom_panel = 150  # Panel to include stats, health and other information
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle RPG')

# Fonts

font = pygame.font.SysFont('Times New Roman', 26)

# Sword Icon
sword_image = pygame.image.load(
    'fighting/Images/assets/sword.png').convert_alpha()
# Scaling sword image to a reasonable size
sword_image = pygame.transform.scale(sword_image, (40, 40))
# Potion icon
potion_image = pygame.image.load(
    'fighting/Images/assets/potion.png').convert_alpha()
# Load victory image
win_img = pygame.image.load('fighting/Images/assets/win.png').convert_alpha()
win_img = pygame.transform.scale(win_img, (350, 350))
# Load Defeat image
defeat_img = pygame.image.load(
    'fighting/Images/assets/defeat.png').convert_alpha()
defeat_img = pygame.transform.scale(defeat_img, (200, 200))
# Load restart image
restart_img = pygame.image.load(
    'fighting/Images/assets/restart.png').convert_alpha()


# Game Variables
actions = ['Idle', 'Attack', 'Hurt', 'Die']  # Initial Actions in spritesheets
total_fighter = 3
attack = False
potion = False
potion_effect_factor = 10
game_over = 0


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


# Function for drawing text

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Function to the background of the game


def draw_background(image):
    screen.fill(WHITE)
    background_image = pygame.image.load(image)
    background_image = pygame.transform.scale(
        background_image, (screen_width, screen_height - bottom_panel))
    screen.blit(background_image, (0, 0))

# Function to the panel of the game


def draw_panel(image):
    panel_image = pygame.image.load(image)
    screen.blit(panel_image, (0, screen_height - bottom_panel))
    draw_text(f'{Knight.player_name} HP: {Knight.hp}', font,
              RED, 100, screen_height - bottom_panel + 10)

    for count, i in enumerate(Enemy_list):
        draw_text(f'{i.player_name} HP: {i.hp}', font,
                  RED, 550, (screen_height - bottom_panel + 10) + count * 60)


def load_animation_sprites(character_name):
    animation_sprites = {}
    for action in actions:
        sprite_list = []
        for i in range(10):
            img = pygame.image.load(
                f'fighting/Images/{character_name}/{action}/Knight_01__{action.upper()}_00{i}.png')
            img = pygame.transform.scale(
                img, (img.get_width()/4, img.get_height()/4))
            sprite_list.append(img)
        animation_sprites[action] = sprite_list

    return animation_sprites


class Character():
    def __init__(self, x, y, name, player_name, maximum_hp, strenght, heal_potions, flip=False):
        self.name = name  # Name of character
        self.player_name = player_name
        self.maximum_hp = maximum_hp  # Maximum HP
        self.hp = maximum_hp  # Current HP
        self.strenght = strenght  # Strenght
        self.start_potions = heal_potions  # Start Potions
        self.heal_potions = heal_potions  # Current potions
        self.alive = True  # Bool to see if you are alive (health != 0)
        self.animation_sprite_list = []  # Animation master list
        self.frame_index = 0  # Index used to iterate through sprite list
        self.action = 'Idle'  # Idle = 0, Attack = 1, Hurt = 2, Dead = 3
        self.update_time = pygame.time.get_ticks()  # Getting time ticks from pygame
        self.flip = flip

        self.animation_sprite_list = load_animation_sprites(self.name)

        self.image = self.animation_sprite_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        # Handle and update image animation
        self.image = self.animation_sprite_list[self.action][self.frame_index]
        # Check if enough time has passed to update the image
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # If sprite list is done being looped, reset to start of the sprite list
        if self.frame_index >= len(self.animation_sprite_list[self.action]):
            if self.action == "Die":
                self.frame_index = len(
                    self.animation_sprite_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        self.action = 'Idle'
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # Deal damage
        rand = random.randint(-5, 5)
        damage = self.strenght + rand
        target.hp -= damage
        # Target hurt animation
        target.hurt()
        # Check for target death
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(
            target.rect.centerx, target.rect.y, str(damage), RED)
        damage_text_group.add(damage_text)
        # Set attack animation to variable
        self.action = 'Attack'
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        self.action = 'Hurt'
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        self.action = 'Die'
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        self.heal_potions = self.start_potions
        self.hp = self.maximum_hp
        self.frame_index = 0
        self.action = 'Idle'
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        if self.flip == True:
            flip_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flip_image, self.rect)
        else:
            screen.blit(self.image, self.rect)


class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        self.hp = hp
        # Calculate health bar
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.y -= 1
        # Delete text
        self.counter += 1
        if self.counter > 30:
            self.kill()


damage_text_group = pygame.sprite.Group()


Knight = Character(100, 330, 'Knight', 'Eren', 30, 10, 3, False)
Enemy_knight1 = Character(500, 300, 'Knight2', 'Levy', 20, 5, 1, True)
Enemy_knight2 = Character(700, 330, 'Knight3', 'Sukuna', 20, 5, 1, True)

Enemy_list = []
Enemy_list.append(Enemy_knight1)
Enemy_list.append(Enemy_knight2)


Knight_health_bar = HealthBar(
    100, screen_height - bottom_panel + 40, Knight.hp, Knight.maximum_hp)

Enemy_knight1_health_bar = HealthBar(
    550, screen_height - bottom_panel + 40, Enemy_knight1.hp, Enemy_knight1.maximum_hp)
Enemy_knight2_health_bar = HealthBar(
    550, screen_height - bottom_panel + 100, Enemy_knight2.hp, Enemy_knight2.maximum_hp)

pickup_potion_button = button.Button(
    screen, 100, screen_height - bottom_panel + 70, potion_image, 64, 64)
restart_button = button.Button(
    screen, 340, 300, restart_img, 120, 30)


def play_Game():

    current_fighter = 1
    action_cooldown = 0
    action_wait_time = 90
    clicked = False

    while True:

        # Setting FPS of the game to 30 FPS
        clock.tick(fps)
        # Draw Background
        draw_background('fighting/Images/background/game_background.png')

        # Draw Panel
        draw_panel('fighting/Images/assets/panel.png')
        Knight_health_bar.draw(Knight.hp)
        Enemy_knight1_health_bar.draw(Enemy_knight1.hp)
        Enemy_knight2_health_bar.draw(Enemy_knight2.hp)

        # Draw Player Knight
        Knight.update()
        Knight.draw()

        # Draw Enemy Knights
        for enemy in Enemy_list:
            enemy.update()
            enemy.draw()

        # Draw the damage text for combatants
        damage_text_group.update()
        damage_text_group.draw(screen)

        # Reset actions and control player actions
        attack = False
        potion = False
        target = None
        global game_over
        pygame.mouse.set_visible(True)
        if game_over == 0:
            mouse_pos = pygame.mouse.get_pos()
            for count, enemy in enumerate(Enemy_list):
                if enemy.rect.collidepoint(mouse_pos):
                    pygame.mouse.set_visible(False)
                    screen.blit(sword_image, mouse_pos)
                    if clicked == True and enemy.alive == True:
                        attack = True
                        target = Enemy_list[count]
        if pickup_potion_button.draw():
            potion = True
        # Display amount of potion
        draw_text(str(Knight.heal_potions), font, GREEN,
                  150, screen_height - bottom_panel + 70)
        if game_over == 0:
            # Knights actions
            if Knight.alive == True:
                if current_fighter == 1:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        # Action: Attack
                        if attack == True and target != None:
                            Knight.attack(target)
                            current_fighter += 1
                            action_cooldown = 0
                        # Action: potion
                        if potion == True:
                            if Knight.heal_potions > 0:
                                # If potion heal player beyond max health
                                if Knight.maximum_hp - Knight.hp > potion_effect_factor:
                                    healing_amount = potion_effect_factor
                                else:
                                    healing_amount = Knight.maximum_hp - Knight.hp
                                Knight.hp += healing_amount
                                Knight.heal_potions -= 1
                                damage_text = DamageText(
                                    Knight.rect.centerx, Knight.rect.y, str(healing_amount), GREEN)
                                damage_text_group.add(damage_text)
                                current_fighter += 1
                                action_cooldown = 0
            else:
                # -1 = Player has lost
                game_over = -1
                # Enemy attacks
            for count, enemy in enumerate(Enemy_list):
                if current_fighter == 2 + count:
                    if enemy.alive == True:
                        action_cooldown += 1
                        if action_cooldown >= action_wait_time:
                            # enemy healing
                            if (enemy.hp / enemy.maximum_hp) < 0.5 and enemy.heal_potions > 0:
                                if enemy.maximum_hp - enemy.hp > potion_effect_factor:
                                    healing_amount = potion_effect_factor
                                else:
                                    healing_amount = enemy.maximum_hp - enemy.hp
                                enemy.hp += healing_amount
                                enemy.heal_potions -= 1
                                damage_text = DamageText(
                                    enemy.rect.centerx, enemy.rect.y, str(healing_amount), GREEN)
                                damage_text_group.add(damage_text)
                                current_fighter += 1
                                action_cooldown = 0
                            else:
                                enemy.attack(Knight)
                                current_fighter += 1
                                action_cooldown = 0

                    else:
                        current_fighter += 1

            if current_fighter > total_fighter:
                current_fighter = 1

        # Check if all bandits are dead
        alive_enemy_knights = 0
        for enemy in Enemy_list:
            if enemy.alive == True:
                alive_enemy_knights += 1

        if alive_enemy_knights == 0:
            # 1 = All enemies have died
            game_over = 1

        if game_over != 0:
            if game_over == 1:
                mixer.music.stop()
                screen.blit(win_img, (220, 5))
            if game_over == -1:
                mixer.music.stop()
                screen.blit(defeat_img, (290, 95))
            if restart_button.draw():
                Knight.reset()
                for enemy in Enemy_list:
                    enemy.reset()
                current_fighter = 1
                action_cooldown = 0
                game_over = 0
                mixer.music.load("fighting/Images/assets/Cipher2.mp3")
                mixer.music.set_volume(0.2)
                mixer.music.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        pygame.display.update()
