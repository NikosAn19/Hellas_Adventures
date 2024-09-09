import time

import pygame
from pygame import mixer
import os
import random
import csv
import button

mixer.init()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hellas Adventures')

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 250
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 58
MAX_LEVELS = 3
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
start_intro = False
progress = False

# define player action variables
moving_left = False
moving_right = False
attack = False
# define game logic variables
all_letters_collected = False
letter_counter = 0
locked_item_picked = False
mute = False
start_timer = False
total_letters = []
all_letter_collected_level_1 = False
all_letter_collected_level_2 = False
all_letter_collected_level_3 = False

# player selection
is_male = True

# load music and sounds
jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.15)
shot_fx = pygame.mixer.Sound('audio/shot.wav')
shot_fx.set_volume(0.05)
background_music = pygame.mixer.Sound('audio/main_music.mp3')
background_channel = pygame.mixer.Channel(0)
background_channel.set_volume(0.5)

# play background music
background_channel.play(background_music, loops=-1)

# load images
# button images
start_img = pygame.image.load('img/buttons/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/buttons/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/buttons/restart_btn.png').convert_alpha()
continue_img = pygame.image.load('img/buttons/continue_button_img.png').convert_alpha()
leksiko_img = pygame.image.load('img/buttons/leksiko_button_img.png').convert_alpha()
logo_img = pygame.image.load('img/logo.png').convert_alpha()
athens_end_img = pygame.image.load('img/words_info/Athens_End.png').convert_alpha()
knossos_end_img = pygame.image.load('img/words_info/Knosos_End.png').convert_alpha()
sparta_end_img = pygame.image.load('img/words_info/Sparta_End.png').convert_alpha()
end_credit_img = pygame.image.load('img/words_info/End_Credit.png').convert_alpha()
male_button_img = pygame.image.load('img/buttons/male_button_img.png').convert_alpha()
female_button_img = pygame.image.load('img/buttons/female_button_img.png').convert_alpha()
easy_button_img = pygame.image.load('img/buttons/easy_button.png').convert_alpha()
medium_button_img = pygame.image.load('img/buttons/medium_button.png').convert_alpha()
hard_button_img = pygame.image.load('img/buttons/hard_button.png').convert_alpha()

# load grades images
grade_a_img = pygame.image.load('img/grades/grade_a.png').convert_alpha()
grade_b_img = pygame.image.load('img/grades/grade_b.png').convert_alpha()
grade_c_img = pygame.image.load('img/grades/grade_c.png').convert_alpha()

# load quiz question images
q1_grifos_img = pygame.image.load('img/quiz/q1/q1_grifos.png').convert_alpha()
q2_grifos_img = pygame.image.load('img/quiz/q2/q2_grifos.png').convert_alpha()
q3_grifos_img = pygame.image.load('img/quiz/q3/q3_grifos.png').convert_alpha()
q4_grifos_img = pygame.image.load('img/quiz/q4/q4_grifos.png').convert_alpha()
q5_grifos_img = pygame.image.load('img/quiz/q5/q5_grifos.png').convert_alpha()
q6_grifos_img = pygame.image.load('img/quiz/q6/q6_grifos.png').convert_alpha()
q7_grifos_img = pygame.image.load('img/quiz/q7/q7_grifos.png').convert_alpha()
q8_grifos_img = pygame.image.load('img/quiz/q8/q8_grifos.png').convert_alpha()
q9_grifos_img = pygame.image.load('img/quiz/q9/q9_grifos.png').convert_alpha()
q10_grifos_img = pygame.image.load('img/quiz/q10/q10_grifos.png').convert_alpha()
q11_grifos_img = pygame.image.load('img/quiz/q11/q11_grifos.png').convert_alpha()
q12_grifos_img = pygame.image.load('img/quiz/q12/q12_grifos.png').convert_alpha()
q13_grifos_img = pygame.image.load('img/quiz/q13/q13_grifos.png').convert_alpha()
q14_grifos_img = pygame.image.load('img/quiz/q14/q14_grifos.png').convert_alpha()
q15_grifos_img = pygame.image.load('img/quiz/q15/q15_grifos.png').convert_alpha()
q16_grifos_img = pygame.image.load('img/quiz/q16/q16_grifos.png').convert_alpha()
q17_grifos_img = pygame.image.load('img/quiz/q17/q17_grifos.png').convert_alpha()
q18_grifos_img = pygame.image.load('img/quiz/q18/q18_grifos.png').convert_alpha()
q19_grifos_img = pygame.image.load('img/quiz/q19/q19_grifos.png').convert_alpha()

# load quiz correct answers
q1_correct_img = pygame.image.load('img/quiz/q1/correct_answer_img.png').convert_alpha()
q2_correct_img = pygame.image.load('img/quiz/q2/correct_answer_img.png').convert_alpha()
q3_correct_img = pygame.image.load('img/quiz/q3/correct_answer_img.png').convert_alpha()
q4_correct_img = pygame.image.load('img/quiz/q4/correct_answer_img.png').convert_alpha()
q5_correct_img = pygame.image.load('img/quiz/q5/correct_answer_img.png').convert_alpha()
q6_correct_img = pygame.image.load('img/quiz/q6/correct_answer_img.png').convert_alpha()
q7_correct_img = pygame.image.load('img/quiz/q7/correct_answer_img.png').convert_alpha()
q8_correct_img = pygame.image.load('img/quiz/q8/correct_answer_img.png').convert_alpha()
q9_correct_img = pygame.image.load('img/quiz/q9/correct_answer_img.png').convert_alpha()
q10_correct_img = pygame.image.load('img/quiz/q10/correct_answer_img.png').convert_alpha()
q11_correct_img = pygame.image.load('img/quiz/q11/correct_answer_img.png').convert_alpha()
q12_correct_img = pygame.image.load('img/quiz/q12/correct_answer_img.png').convert_alpha()
q13_correct_img = pygame.image.load('img/quiz/q13/correct_answer_img.png').convert_alpha()
q14_correct_img = pygame.image.load('img/quiz/q14/correct_answer_img.png').convert_alpha()
q15_correct_img = pygame.image.load('img/quiz/q15/correct_answer_img.png').convert_alpha()
q16_correct_img = pygame.image.load('img/quiz/q16/correct_answer_img.png').convert_alpha()
q17_correct_img = pygame.image.load('img/quiz/q17/correct_answer_img.png').convert_alpha()
q18_correct_img = pygame.image.load('img/quiz/q18/correct_answer_img.png').convert_alpha()
q19_correct_img = pygame.image.load('img/quiz/q19/correct_answer_img.png').convert_alpha()

# load quiz wrong answers
q1_wrong_img = pygame.image.load('img/quiz/q1/wrong_answer_img.png').convert_alpha()
q2_wrong_img = pygame.image.load('img/quiz/q2/wrong_answer_img.png').convert_alpha()
q3_wrong_img = pygame.image.load('img/quiz/q3/wrong_answer_img.png').convert_alpha()
q4_wrong_img = pygame.image.load('img/quiz/q4/wrong_answer_img.png').convert_alpha()
q5_wrong_img = pygame.image.load('img/quiz/q5/wrong_answer_img.png').convert_alpha()
q6_wrong_img = pygame.image.load('img/quiz/q6/wrong_answer_img.png').convert_alpha()
q7_wrong_img = pygame.image.load('img/quiz/q7/wrong_answer_img.png').convert_alpha()
q8_wrong_img = pygame.image.load('img/quiz/q8/wrong_answer_img.png').convert_alpha()
q9_wrong_img = pygame.image.load('img/quiz/q9/wrong_answer_img.png').convert_alpha()
q10_wrong_img = pygame.image.load('img/quiz/q10/wrong_answer_img.png').convert_alpha()
q11_wrong_img = pygame.image.load('img/quiz/q11/wrong_answer_img.png').convert_alpha()
q12_wrong_img = pygame.image.load('img/quiz/q12/wrong_answer_img.png').convert_alpha()
q13_wrong_img = pygame.image.load('img/quiz/q13/wrong_answer_img.png').convert_alpha()
q14_wrong_img = pygame.image.load('img/quiz/q14/wrong_answer_img.png').convert_alpha()
q15_wrong_img = pygame.image.load('img/quiz/q15/wrong_answer_img.png').convert_alpha()
q16_wrong_img = pygame.image.load('img/quiz/q16/wrong_answer_img.png').convert_alpha()
q17_wrong_img = pygame.image.load('img/quiz/q17/wrong_answer_img.png').convert_alpha()
q18_wrong_img = pygame.image.load('img/quiz/q18/wrong_answer_img.png').convert_alpha()
q19_wrong_img = pygame.image.load('img/quiz/q19/wrong_answer_img.png').convert_alpha()

quiz_grifoi_imgs = [q1_grifos_img, q2_grifos_img, q3_grifos_img, q4_grifos_img, q5_grifos_img, q6_grifos_img,
                    q7_grifos_img,
                    q8_grifos_img, q9_grifos_img, q10_grifos_img, q11_grifos_img, q12_grifos_img, q13_grifos_img,
                    q14_grifos_img, q15_grifos_img, q16_grifos_img, q17_grifos_img, q18_grifos_img, q19_grifos_img]

# background
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()
background_athens = pygame.image.load('img/Background/background_1.png').convert_alpha()
background_knosos = pygame.image.load('img/Background/background_knosos2.png').convert_alpha()
background_sparta = pygame.image.load('img/Background/background_Sparta.png').convert_alpha()
# background_quiz = pygame.image.load('img/Background/background_quiz.png').convert_alpha()
athens_img = pygame.image.load('img/Background/Athens_Map.png').convert_alpha()
sparta_img = pygame.image.load('img/Background/Sparta_Map.png').convert_alpha()
knosos_img = pygame.image.load('img/Background/Knosos_Map.png').convert_alpha()

# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/Tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
# bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
# pick up boxes
alpha_box_img = pygame.image.load('img/tile/21.png').convert_alpha()
bhta_box_img = pygame.image.load('img/tile/22.png').convert_alpha()
gama_box_img = pygame.image.load('img/tile/23.png').convert_alpha()
delta_box_img = pygame.image.load('img/tile/24.png').convert_alpha()
epsilon_box_img = pygame.image.load('img/tile/25.png').convert_alpha()
zhta_box_img = pygame.image.load('img/tile/26.png').convert_alpha()
hta_box_img = pygame.image.load('img/tile/27.png').convert_alpha()
thita_box_img = pygame.image.load('img/tile/28.png').convert_alpha()
giota_box_img = pygame.image.load('img/tile/29.png').convert_alpha()
kapa_box_img = pygame.image.load('img/tile/30.png').convert_alpha()
lamda_box_img = pygame.image.load('img/tile/31.png').convert_alpha()
mi_box_img = pygame.image.load('img/tile/32.png').convert_alpha()
ni_box_img = pygame.image.load('img/tile/33.png').convert_alpha()
ksi_box_img = pygame.image.load('img/tile/34.png').convert_alpha()
omikron_box_img = pygame.image.load('img/tile/35.png').convert_alpha()
pi_box_img = pygame.image.load('img/tile/36.png').convert_alpha()
ro_box_img = pygame.image.load('img/tile/37.png').convert_alpha()
sigma_box_img = pygame.image.load('img/tile/38.png').convert_alpha()
taf_box_img = pygame.image.load('img/tile/39.png').convert_alpha()
ypsilon_box_img = pygame.image.load('img/tile/40.png').convert_alpha()
fi_box_img = pygame.image.load('img/tile/41.png').convert_alpha()
xi_box_img = pygame.image.load('img/tile/42.png').convert_alpha()
psi_box_img = pygame.image.load('img/tile/43.png').convert_alpha()
omega_box_img = pygame.image.load('img/tile/44.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
alpha_locked_img = pygame.image.load('img/tile/45.png').convert_alpha()
bhta_locked_img = pygame.image.load('img/tile/46.png').convert_alpha()
gama_locked_img = pygame.image.load('img/tile/47.png').convert_alpha()
delta_locked_img = pygame.image.load('img/tile/48.png').convert_alpha()
epsilon_locked_img = pygame.image.load('img/tile/49.png').convert_alpha()
zhta_locked_img = pygame.image.load('img/tile/50.png').convert_alpha()
giota_locked_img = pygame.image.load('img/tile/51.png').convert_alpha()
psi_locked_img = pygame.image.load('img/tile/52.png').convert_alpha()
ypsilon_locked_img = pygame.image.load('img/tile/53.png').convert_alpha()
omikron_locked_img = pygame.image.load('img/tile/54.png').convert_alpha()
hta_locked_img = pygame.image.load('img/tile/55.png').convert_alpha()
ro_locked_img = pygame.image.load('img/tile/56.png').convert_alpha()
sigma_locked_img = pygame.image.load('img/tile/57.png').convert_alpha()
item_boxes = {
    'Health': alpha_box_img,
    'Ammo': ammo_box_img,
    'Grenade': grenade_box_img,
    'Alpha': alpha_box_img,
    'Bhta': bhta_box_img,
    'Gama': gama_box_img,
    'Delta': delta_box_img,
    'Epsilon': epsilon_box_img,
    'Zhta': zhta_box_img,
    'Hta': hta_box_img,
    'Thita': thita_box_img,
    'Giota': giota_box_img,
    'Kapa': kapa_box_img,
    'Lamda': lamda_box_img,
    'Mi': mi_box_img,
    'Ni': ni_box_img,
    'Ksi': ksi_box_img,
    'Omikron': omikron_box_img,
    'Pi': pi_box_img,
    'Ro': ro_box_img,
    'Sigma': sigma_box_img,
    'Taf': taf_box_img,
    'Ypsilon': ypsilon_box_img,
    'Fi': fi_box_img,
    'Xi': xi_box_img,
    'Psi': psi_box_img,
    'Omega': omega_box_img,
    'Alpha_Locked': alpha_locked_img,
    'Bhta_Locked': bhta_locked_img,
    'Gama_Locked': gama_locked_img,
    'Delta_Locked': delta_locked_img,
    'Epsilon_Locked': epsilon_locked_img,
    'Zhta_Locked': zhta_locked_img,
    'Giota_Locked': giota_locked_img,
    'Psi_Locked': psi_locked_img,
    'Ypsilon_Locked': ypsilon_locked_img,
    'Omikron_Locked': omikron_locked_img,
    'Hta_Locked': hta_locked_img,
    'Ro_Locked': ro_locked_img,
    'Sigma_Locked': sigma_locked_img,
}

# define colours
BG = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)

# define font
font = pygame.font.SysFont('Futura', 30)


def draw_bg():
    if level == 1:
        screen.fill(BG)
        width = background_athens.get_width()
        for x in range(5):
            screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
            screen.blit(background_athens,
                        ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - background_athens.get_height()))
    elif level == 2:
        screen.fill(BG)
        width = background_knosos.get_width()
        for x in range(5):
            screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
            screen.blit(background_knosos,
                        ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - background_knosos.get_height()))
    else:
        screen.fill(BG)
        width = background_sparta.get_width()
        for x in range(5):
            screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
            screen.blit(background_sparta
                        , ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - background_sparta.get_height()))


# function to reset level
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    # create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data


class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.attack_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # load all images for the players
        animation_types = ['Idle', 'Run', 'Jump', 'Death', 'Attack']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            if is_male:
                self.char_type = 'player'
                num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
                for i in range(num_of_frames):
                    img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                    img = pygame.transform.scale(img, (
                        int(img.get_width() * (scale / 0.8)), int(img.get_height() * (scale / 0.8))))
                    temp_list.append(img)
                self.animation_list.append(temp_list)
            elif is_male == False:
                self.char_type = 'player_female'
                num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
                for i in range(num_of_frames):
                    img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                    img = pygame.transform.scale(img, (
                        int(img.get_width() * (scale / 0.8)), int(img.get_height() * (scale / 0.8))))
                    temp_list.append(img)
                self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def set_char_type(self, char_type):
        self.char_type = char_type

    def update(self):
        self.update_animation()
        self.check_alive()
        self.check_collisions()
        # update cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def move(self, moving_left, moving_right):
        # reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        # assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -14
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # check for collision
        for tile in world.obstacle_list:
            # check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # check for collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        # check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        # check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        # check if going off the edges of the screen
        if self.char_type == 'player' or self.char_type == 'player_female':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # update scroll based on player position
        if self.char_type == 'player' or self.char_type == 'player_female':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (
                    world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
                    or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def check_collisions(self):
        collided_enemies = pygame.sprite.spritecollide(self, enemy_group, False)
        for enemy in collided_enemies:
            if self.attack_cooldown == 0:
                self.attack_cooldown = 20
            if attack:
                if enemy.alive:
                    enemy.health -= 25
                    print("Attacked Enemy")

                shot_fx.play()

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 4:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            print('Attack on update action', self.action)
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

        # load all images for the players
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img,
                                             (int(img.get_width() * (scale / 0.8)),
                                              int(img.get_height() * (scale / 0.8))))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        # assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -14
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # check for collision
        for tile in world.obstacle_list:
            # check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                # if the ai has hit a wall then make it turn around
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
                # check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # check for collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        # check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        # check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        # check if going off the edges of the screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

            # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # update scroll based on player position
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (
                    world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
                    or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 50
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery,
                            self.direction)
            bullet_group.add(bullet)
            # reduce ammo
            self.ammo -= 1
            shot_fx.play()

    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)  # 0: idle
                self.idling = True
                self.idling_counter = 50
            # check if the ai in near the player
            if self.vision.colliderect(player.rect):
                # stop running and face the player
                self.update_action(0)  # 0: idle
                # shoot
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)  # 1: run
                    self.move_counter += 1
                    # update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

            # scroll
        self.rect.x += screen_scroll

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 200
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class World():
    def __init__(self, male_selected=True):
        self.obstacle_list = []
        self.male_selected = male_selected

    def process_data(self, data):
        self.level_length = len(data[0])
        # iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:  # create player
                        if self.male_selected:
                            player = Player('player', x * TILE_SIZE, y * TILE_SIZE, 1.15, 5)
                        elif self.male_selected == False:
                            player = Player('player_female', x * TILE_SIZE, y * TILE_SIZE, 1.15, 5)
                        # self.player = player
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile == 16:  # create enemies
                        enemy = Soldier('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.15, 2, 20, 0)
                        enemy_group.add(enemy)
                    elif tile == 17:  # create ammo box
                        item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 18:  # create grenade box
                        item_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19:  # create health box
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20:  # create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                    elif tile == 21:  # create exit
                        item_box = ItemBox('Alpha', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 22:  # create exit
                        item_box = ItemBox('Bhta', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 23:  # create exit
                        item_box = ItemBox('Gama', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 24:  # create exit
                        item_box = ItemBox('Delta', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 25:  # create exit
                        item_box = ItemBox('Epsilon', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 26:  # create exit
                        item_box = ItemBox('Zhta', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 27:  # create exit
                        item_box = ItemBox('Hta', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 28:  # create exit
                        item_box = ItemBox('Thita', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 29:  # create exit
                        item_box = ItemBox('Giota', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 30:  # create exit
                        item_box = ItemBox('Kapa', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 31:  # create exit
                        item_box = ItemBox('Lamda', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 32:  # create exit
                        item_box = ItemBox('Mi', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 33:  # create exit
                        item_box = ItemBox('Ni', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 34:  # create exit
                        item_box = ItemBox('Ksi', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 35:  # create exit
                        item_box = ItemBox('Omikron', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 36:  # create exit
                        item_box = ItemBox('Pi', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 37:  # create exit
                        item_box = ItemBox('Ro', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 38:  # create exit
                        item_box = ItemBox('Sigma', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 39:  # create exit
                        item_box = ItemBox('Taf', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 40:  # create exit
                        item_box = ItemBox('Ypsilon', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 41:  # create exit
                        item_box = ItemBox('Fi', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 42:  # create exit
                        item_box = ItemBox('Xi', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 43:  # create exit
                        item_box = ItemBox('Psi', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 44:  # create exit
                        item_box = ItemBox('Omega', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 45:  # create exit
                        item_box = ItemBox('Alpha_Locked', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 46:  # create exit
                        item_box = ItemBox('Bhta_Locked', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 47:  # create exit
                        item_box = ItemBox('Gama_Locked', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 48:  # create exit
                        item_box = ItemBox('Delta_Locked', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 49:  # create exit
                        item_box = ItemBox('Epsilon_Locked', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 50:  # create exit
                        item_box = ItemBox('Zhta_Locked', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 51:  # create exit
                        item_box = ItemBox('Giota_Locked', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 52:  # create exit
                        item_box = ItemBox('Psi_Locked', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 53:  # create exit
                        item_box = ItemBox('Ypsilon_Locked', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 54:  # create exit
                        item_box = ItemBox('Omikron_Locked', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 55:  # create exit
                        item_box = ItemBox('Hta_Locked', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 56:  # create exit
                        item_box = ItemBox('Ro_Locked', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 57:  # create exit
                        item_box = ItemBox('Sigma_Locked', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)

        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.letter_counter = 0

    def update(self):
        global locked_item_picked
        global all_letters_collected
        global letter_counter
        global total_letters
        global all_letter_collected_level_1
        global all_letter_collected_level_2
        global all_letter_collected_level_3
        # scroll
        self.rect.x += screen_scroll
        # check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            if self.item_type in item_boxes:
                letter_counter = letter_counter + 1
                if letter_counter == 9 and level == 1:
                    all_letters_collected = True
                    all_letter_collected_level_1 = True
                if letter_counter == 12 and level == 2:
                    all_letters_collected = True
                    all_letter_collected_level_2 = True
                if letter_counter == 13 and level == 3:
                    all_letters_collected = True
                    all_letter_collected_level_3 = True
                print('Level :', level)
                print('Letters colected:', letter_counter)
                print('Are all letter collected?', all_letters_collected)
            # check what kind of box it was
            if self.item_type == 'Psi_Locked' or self.item_type == 'Alpha_Locked' or self.item_type == 'Giota_Locked' \
                    or self.item_type == 'Epsilon_Locked' or self.item_type == 'Ro_Locked' or self.item_type == 'Delta_Locked' \
                    or self.item_type == 'Ypsilon_Locked' or self.item_type == 'Sigma_Locked':
                locked_item_picked = True

                # player.health += 25
                # if player.health > player.max_health:
                # 	player.health = player.max_health
            total_letters.append(self.item_type)
            # delete the item box
            self.kill()


class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        # update with new health
        self.health = health
        # calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 2
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        # check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        # check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

            # check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()


class ScreenFade():

    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:  # whole screen fade
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour,
                             (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour,
                             (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.direction == 2:  # vertical screen fade down
            pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True

        return fade_complete


# create screen fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)

# create texts
text_font = pygame.font.SysFont(None, 25, bold=True)
text_font2 = pygame.font.SysFont(None, 50, bold=True)



# create quiz
# dict with correct answers
quiz_correct_img_dict = {
    q1_grifos_img: q1_correct_img,
    q2_grifos_img: q2_correct_img,
    q3_grifos_img: q3_correct_img,
    q4_grifos_img: q4_correct_img,
    q5_grifos_img: q5_correct_img,
    q6_grifos_img: q6_correct_img,
    q7_grifos_img: q7_correct_img,
    q8_grifos_img: q8_correct_img,
    q9_grifos_img: q9_correct_img,
    q10_grifos_img: q10_correct_img,
    q11_grifos_img: q11_correct_img,
    q12_grifos_img: q12_correct_img,
    q13_grifos_img: q13_correct_img,
    q14_grifos_img: q14_correct_img,
    q15_grifos_img: q15_correct_img,
    q16_grifos_img: q16_correct_img,
    q17_grifos_img: q17_correct_img,
    q18_grifos_img: q18_correct_img,
    q19_grifos_img: q19_correct_img,

}
# dict with wrong answers
quiz_wrong_img_dict = {
    q1_grifos_img: q1_wrong_img,
    q2_grifos_img: q2_wrong_img,
    q3_grifos_img: q3_wrong_img,
    q4_grifos_img: q4_wrong_img,
    q5_grifos_img: q5_wrong_img,
    q6_grifos_img: q6_wrong_img,
    q7_grifos_img: q7_wrong_img,
    q8_grifos_img: q8_wrong_img,
    q9_grifos_img: q9_wrong_img,
    q10_grifos_img: q10_wrong_img,
    q11_grifos_img: q11_wrong_img,
    q12_grifos_img: q12_wrong_img,
    q13_grifos_img: q13_wrong_img,
    q14_grifos_img: q14_wrong_img,
    q15_grifos_img: q15_wrong_img,
    q16_grifos_img: q16_wrong_img,
    q17_grifos_img: q17_wrong_img,
    q18_grifos_img: q18_wrong_img,
    q19_grifos_img: q19_wrong_img,
}
# list of quiz strings
quiz_list = ['Η ορθή ονομασία του γκρέιπφρουτ στα Ελληνικά είναι βοτρυόκαρπος.',
             'Η ορθή ονομασία της φράουλας στα Ελληνικά είναι βοτρυόκαρπος.',
             'Μαζί με το μήνυμα σας αποστέλλω _____ τα απαραίτητα έγγραφα.',
             'Ο ______ είναι πολύ νόστιμο ψάρι.',
             'Ο Διονύσιος ______ είναι ο Εθνικός μας ποιητής.',
             'Η ορθή ονομασία της ομπρέλας στα Ελληνικά είναι αποβρόχιο.',
             'Η ορθή ονομασία για τα κεφτεδάκια στα ελληνικά είναι κρεατοσφαιρίδια.',
             'Η ορθή ονομασία του ασανσέρ στα ελληνικά είναι ',
             'Πολλοί διάσημοι έδωσαν το ____ στην μεγάλη εκδήλωση του τηλεοπτικού σταθμού.',
             'Η διάσημη φράση του Κλεόβουλου του Λίνδιου είναι ______.',
             'Ο άνθρωπος που κρατάει μυστικά λέγεται και εγγαστρίμυθος.',
             'Ο Δήμος προχώρησε στην αποκομιδή των ______ από τον χώρο του πάρκου.',
             'Μπορείς να διαλέξεις _____ σου αρέσει.',
             'Ο Περικλής πέθανε από τον _____ που ενέσκυψε στην πόλη της Αθήνας από τα άταφα πτώματα.',
             'Λόγω της κακής ______ των υδάτων συγκεντρώθηκαν πολλά λιμνάζοντα ύδατα.',
             'Ο διαγωνισμός θα λάβει χώρα τον ____.',
             'Η υψηλότερη οροσειρά της Πελοποννήσου λέγεται ______.',
             'Κάποιος έσπασε τον _____ καθρέπτη του αυτοκινήτου μου.',
             'Θα συναντηθούμε με τον _____ του τμήματος.']

# dict with quiz testing
quiz_dict = {
    'Η ορθή ονομασία του γκρέιπφρουτ στα Ελληνικά είναι βοτρυόκαρπος.': 'Σωστό',
    'Η ορθή ονομασία της φράουλας στα Ελληνικά είναι βοτρυόκαρπος.': 'Λάθος',
    'Μαζί με το μήνυμα σας αποστέλλω _____ τα απαραίτητα έγγραφα.': 'Συνημμένα',
    'Ο ______ είναι πολύ νόστιμο ψάρι.': 'Σολομός',
    'Ο Διονύσιος ______ είναι ο Εθνικός μας ποιητής.': 'Σωλομός',
    'Η ορθή ονομασία της ομπρέλας στα Ελληνικά είναι αποβρόχιο.': 'Λάθος',
    'Η ορθή ονομασία για τα κεφτεδάκια στα ελληνικά είναι κρεατοσφαιρίδια.': 'Σωστό',
    'Η ορθή ονομασία του ασανσέρ στα ελληνικά είναι :': 'Ανελκυστήρας',
    'Πολλοί διάσημοι έδωσαν το ____ στην μεγάλη εκδήλωση του τηλεοπτικού σταθμού.': 'Παρών',
    'Η διάσημη του Κλεόβουλου του Λίνδιου είναι ______.': 'Μέτρον Άριστον',
    'Ο άνθρωπος που κρατάει μυστικά λέγεται και εγγαστρίμυθος.': 'Λάθος',
    'Ο Δήμος προχώρησε στην αποκομιδή των ______ από τον χώρο του πάρκου.': 'Απορριμάτων',
    'Μπορείς να διαλέξεις _____ σου αρέσει.': 'Ό,τι',
    'Ο Περικλής πέθανε από τον _____ που ενέσκυψε στην πόλη της Αθήνας από τα άταφα πτώματα.': 'Λοιμό',
    'Λόγω της κακής ______ των υδάτων συγκεντρώθηκαν πολλά λιμνάζοντα ύδατα.': 'Ρύσης',
    'Ο διαγωνισμός θα λάβει χώρα τον ____.': 'Μάιο',
    'Η υψηλότερη οροσειρά της Πελοποννήσου λέγεται ______.': 'Ταϋγετος',
    'Κάποιος έσπασε τον _____ καθρέπτη του αυτοκινήτου μου.': 'Πλαϊνό',
    'Θα συναντηθούμε με τον _____ του τμήματος.': 'Επικεφαλής'
}
grifos = random.choice(quiz_grifoi_imgs)

# create buttons

# difficulty buttons
easy_button = button.ButtonText(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 5, easy_button_img, 1)
medium_button = button.ButtonText(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 5, medium_button_img, 1)
hard_button = button.ButtonText(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 5, hard_button_img, 1)
difficulty_active_button = easy_button

# player selection buttons
male_button = button.ButtonText(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 5, male_button_img, 1)
female_button = button.ButtonText(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 5, female_button_img, 1)
other_button = male_button
other_button.set_visible(False)
active_button = female_button
# menu buttons
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 125, start_img, 1)
continue_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 125, continue_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 150, exit_img, 1)
leksiko_ingame_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 150, leksiko_img, 1)
leksiko_button = button.Button(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 + 150, leksiko_img, 1)
back_button = button.Button(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 + 150, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 125, restart_img, 2)
# quiz buttons
first_button = button.ButtonText(SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT // 2 - 25, text='')
first_button.set_image(q1_correct_img)
second_button = button.ButtonText(SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 - 25, text='')
second_button.set_image(q1_wrong_img)
correct_button = first_button
wrong_button = second_button
logo = button.Button(SCREEN_WIDTH // 3 - 120, SCREEN_HEIGHT // 2 - 290, logo_img, 1)

# test buttons
alpha_button = button.ButtonLetter(150, 150, alpha_box_img, 1.5)
bhta_button = button.ButtonLetter(200, 150, bhta_box_img, 1.5)
gama_button = button.ButtonLetter(250, 150, gama_box_img, 1.5)
delta_button = button.ButtonLetter(300, 150, delta_box_img, 1.5)
epsilon_button = button.ButtonLetter(350, 150, epsilon_box_img, 1.5)
zhta_button = button.ButtonLetter(400, 150, zhta_box_img, 1.5)
hta_button = button.ButtonLetter(450, 150, hta_box_img, 1.5)
thita_button = button.ButtonLetter(500, 150, thita_box_img, 1.5)
giota_button = button.ButtonLetter(150, 250, giota_box_img, 1.5)
kapa_button = button.ButtonLetter(200, 250, kapa_box_img, 1.5)
lamda_button = button.ButtonLetter(250, 250, lamda_box_img, 1.5)
mi_button = button.ButtonLetter(300, 250, mi_box_img, 1.5)
ni_button = button.ButtonLetter(350, 250, ni_box_img, 1.5)
ksi_button = button.ButtonLetter(400, 250, ksi_box_img, 1.5)
omikron_button = button.ButtonLetter(450, 250, omikron_box_img, 1.5)
pi_button = button.ButtonLetter(500, 250, ksi_box_img, 1.5)
ro_button = button.ButtonLetter(150, 350, ro_box_img, 1.5)
sigma_button = button.ButtonLetter(200, 350, sigma_box_img, 1.5)
taf_button = button.ButtonLetter(250, 350, taf_box_img, 1.5)
ypsilon_button = button.ButtonLetter(300, 350, ypsilon_box_img, 1.5)
fi_button = button.ButtonLetter(350, 350, fi_box_img, 1.5)
xi_button = button.ButtonLetter(400, 350, xi_box_img, 1.5)
psi_button = button.ButtonLetter(450, 350, psi_box_img, 1.5)
omega_button = button.ButtonLetter(500, 350, omega_box_img, 1.5)

button_container = [button.ButtonLetter(150, 150, psi_box_img, 1.5),
                    button.ButtonLetter(200, 150, giota_box_img, 1.5),
                    button.ButtonLetter(250, 150, mi_box_img, 1.5),
                    button.ButtonLetter(300, 150, ypsilon_box_img, 1.5),
                    button.ButtonLetter(350, 150, thita_box_img, 1.5),
                    button.ButtonLetter(400, 150, giota_box_img, 1.5),
                    button.ButtonLetter(450, 150, omega_box_img, 1.5),
                    button.ButtonLetter(500, 150, sigma_box_img, 1.5),
                    button.ButtonLetter(550, 150, hta_box_img, 1.5)]

button_container2 = [button.ButtonLetter(100, 250, ro_box_img, 1.5),
                     button.ButtonLetter(150, 250, hta_box_img, 1.5),
                     button.ButtonLetter(200, 250, ksi_box_img, 1.5),
                     button.ButtonLetter(250, 250, giota_box_img, 1.5),
                     button.ButtonLetter(300, 250, kapa_box_img, 1.5),
                     button.ButtonLetter(350, 250, epsilon_box_img, 1.5),
                     button.ButtonLetter(400, 250, lamda_box_img, 1.5),
                     button.ButtonLetter(450, 250, epsilon_box_img, 1.5),
                     button.ButtonLetter(500, 250, ypsilon_box_img, 1.5),
                     button.ButtonLetter(550, 250, thita_box_img, 1.5),
                     button.ButtonLetter(600, 250, omikron_box_img, 1.5),
                     button.ButtonLetter(650, 250, sigma_box_img, 1.5),]

button_container3 = [button.ButtonLetter(100, 350, sigma_box_img, 1.5),
                     button.ButtonLetter(150, 350, ypsilon_box_img, 1.5),
                     button.ButtonLetter(200, 350, ni_box_img, 1.5),
                     button.ButtonLetter(250, 350, delta_box_img, 1.5),
                     button.ButtonLetter(300, 350, alpha_box_img, 1.5),
                     button.ButtonLetter(350, 350, giota_box_img, 1.5),
                     button.ButtonLetter(400, 350, taf_box_img, 1.5),
                     button.ButtonLetter(450, 350, ypsilon_box_img, 1.5),
                     button.ButtonLetter(500, 350, mi_box_img, 1.5),
                     button.ButtonLetter(550, 350, omikron_box_img, 1.5),
                     button.ButtonLetter(600, 350, ni_box_img, 1.5),
                     button.ButtonLetter(650, 350, alpha_box_img, 1.5),
                     button.ButtonLetter(700, 350, sigma_box_img, 1.5)]

# letter buttons dict
letter_buttons_dict = {
    'Alpha': alpha_button,
    'Bhta': bhta_button,
    'Gama': gama_button,
    'Delta': delta_button,
    'Epsilon': epsilon_button,
    'Zhta': zhta_button,
    'Hta': hta_button,
    'Thita': thita_button,
    'Giota': giota_button,
    'Kapa': kapa_button,
    'Lamda': lamda_button,
    'Mi': mi_button,
    'Ni': ni_button,
    'Ksi': ksi_button,
    'Omikron': omikron_button,
    'Pi': pi_button,
    'Ro': ro_button,
    'Sigma': sigma_button,
    'Taf': taf_button,
    'Ypsilon': ypsilon_button,
    'Fi': fi_button,
    'Xi': xi_button,
    'Psi': psi_button,
    'Omega': omega_button,
    'Alpha_Locked': alpha_button,
    'Bhta_Locked': bhta_button,
    'Gama_Locked': gama_button,
    'Delta_Locked': delta_button,
    'Epsilon_Locked': epsilon_button,
    'Zhta_Locked': zhta_button,
    'Giota_Locked': giota_button,
    'Psi_Locked': psi_button,
    'Ypsilon_Locked': ypsilon_button,
    'Omikron_Locked': omikron_button,
    'Hta_Locked': hta_button,
    'Ro_Locked': ro_button,
    'Sigma_Locked': sigma_button,
}


def update_buttons():
    global correct_button
    global wrong_button
    correct_answer_img = quiz_correct_img_dict[grifos]
    button_list = [first_button, second_button]
    correct_button = random.choice(button_list)
    correct_button.set_image(correct_answer_img)
    for button in button_list:
        if button != correct_button:
            button.set_image(quiz_wrong_img_dict[grifos])
            wrong_button = button


update_buttons()


def update_quiz():
    global grifos
    grifos = random.choice(quiz_grifoi_imgs)


# create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
# load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World(male_selected=True)
player, health_bar = world.process_data(world_data)


class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False

    def start(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True

    def stop(self):
        if self.running:
            self.elapsed_time += time.time() - self.start_time
            self.running = False

    def reset(self):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False

    def get_elapsed_time(self):
        if self.running:
            return self.elapsed_time + (time.time() - self.start_time)
        return self.elapsed_time

    def get_elapsed_time_formatted(self):
        elapsed_time = self.get_elapsed_time()
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        return f"{minutes:02}:{seconds:02}"


# initialize timer
timer = Timer()
timer.start()
next_text_update_time = pygame.time.get_ticks() + 1000
font = pygame.font.Font(None, 36)
time_text = font.render(f"Time: {timer.get_elapsed_time_formatted()}", True, (255, 0, 0))
time_passed_text = font.render('Time passed!', True, (255, 0, 0))
time_under_one_minute = True

# not all letter collected prompt
not_all_letters_text = font.render('You should collect all letters!', True, (255, 0, 0))
move_prompt_text = font.render('Move back to continue!', True, (255, 0, 0))

# time prompts
medium_time_prompt = font.render('You have 60 seconds to complete the level', True, (255, 0, 0))
hard_time_prompt = font.render('You have 45 seconds to complete the level', True, (255, 0, 0))

# game difficulty
easy_level = True
medium_level = False
hard_level = False

# event flags
proceed_to_credit = False
proceed_to_start = False
grades_shown = False
leksiko_clicked = False
leksiko_in_game_clicked = False
display_menu = False
menu_active = False
game_finished = False
muted_index = 0
show_athens = False
show_knosos = False
proceed_to_first_level = False
proceed_to_next_level = False

end_game = False
run = True

while run:

    # clock.tick(FPS)
    if start_game:
        # mute and unmute music
        if muted_index % 2 is not 0:
            background_channel.set_volume(0.0)
        else:
            background_channel.set_volume(1.0)
        if start_timer == True:
            current_time = pygame.time.get_ticks()
            if current_time >= next_text_update_time:
                time_text = font.render(f"Time: {timer.get_elapsed_time_formatted()}", True,
                                        (255, 0, 0))  # Κόκκινο χρώμα
                next_text_update_time = current_time + 1000
            screen.blit(time_text, (350, 20))
            if medium_level == True:
                screen.blit(medium_time_prompt, (150, 50))
                # pygame.display.flip()
            elif hard_level == True:
                screen.blit(hard_time_prompt, (150, 50))
                # pygame.display.flip()
            pygame.display.update()
    clock.tick(FPS)
    if start_game == False and leksiko_clicked == False:
        # draw menu
        screen.fill(BG)
        # add buttons
        if active_button.draw(screen):
            if active_button is male_button:
                print('male selected')
                is_male = True
                print('Is male:', is_male)
                # create empty tile list
                world_data = reset_level()
                for row in range(ROWS):
                    r = [-1] * COLS
                    world_data.append(r)
                # load in level data and create world
                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World(male_selected=True)
                player, health_bar = world.process_data(world_data)
                active_button.set_visible(False)
                other_button.set_visible(True)
                active_button, other_button = other_button, active_button
            elif active_button is female_button:
                print('female selected')
                is_male = False
                print('Is male:', is_male)
                # create empty tile list
                world_data = reset_level()
                for row in range(ROWS):
                    r = [-1] * COLS
                    world_data.append(r)
                # load in level data and create world
                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world = World(male_selected=False)
                player, health_bar = world.process_data(world_data)
                active_button.set_visible(False)
                other_button.set_visible(True)
                active_button, other_button = other_button, active_button
        active_button.draw(screen)
        if start_button.draw(screen):
            show_athens = True
            start_game = True
            start_intro = True
            proceed_to_start = True
            level_start_time = pygame.time.get_ticks()
            # timer.reset()
        if exit_button.draw(screen):
            run = False

        if leksiko_button.draw(screen):
            leksiko_clicked = True

        if logo.draw(screen):
            pass
        if difficulty_active_button.draw(screen):
            # change to medium
            if difficulty_active_button is easy_button:
                easy_level = False
                medium_level = True
                hard_level = False
                difficulty_active_button = medium_button
                print('Difficulty medium:', 'medium_level =', medium_level)
            # change to hard
            elif difficulty_active_button is medium_button:
                easy_level = False
                medium_level = False
                hard_level = True
                difficulty_active_button = hard_button
                print('Difficulty easy:', 'hard_level =', hard_level)
            # change to easy
            elif difficulty_active_button is hard_button:
                easy_level = True
                medium_level = False
                hard_level = False
                difficulty_active_button = easy_button
                print('Difficulty easy:', 'easy_level =', easy_level)
    elif start_game == False and leksiko_clicked == True:
        screen.fill((0, 0, 0))
        if all_letter_collected_level_1 == True:
            for button in button_container:
                button.draw(screen)
        if all_letter_collected_level_2 == True:
            for button in button_container2:
                button.draw(screen)
        if all_letter_collected_level_3 == True:
            for button in button_container3:
                button.draw(screen)
        if back_button.draw(screen):
            leksiko_clicked = False
            back_button.draw(screen)
    elif start_game == True and menu_active:
        timer.stop()
        print('menu active', menu_active)
        screen.fill((0, 0, 0))
        if continue_button.draw(screen):
            menu_active = False
            timer.start()
        if leksiko_in_game_clicked:
            screen.fill((0, 0, 0))
            if all_letter_collected_level_1 == True:
                for button in button_container:
                    button.draw(screen)
            if all_letter_collected_level_2 == True:
                for button in button_container2:
                    button.draw(screen)
            if all_letter_collected_level_3 == True:
                for button in button_container3:
                    button.draw(screen)
            if leksiko_ingame_button.draw(screen):
                    leksiko_in_game_clicked = False
        if leksiko_ingame_button.draw(screen):
            leksiko_in_game_clicked = True
    else:
        if show_athens:
            screen.blit(athens_img, (0, 0))
            if progress and proceed_to_first_level == False:
                start_intro = True
                proceed_to_first_level = True
                timer.reset()
                timer.start()
        if proceed_to_first_level == True:
            start_timer = True
            # update background
            draw_bg()
            # draw world map
            world.draw()
            # show player health
            health_bar.draw(player.health)

            player.update()
            player.draw()

            for enemy in enemy_group:
                enemy.ai()
                enemy.update()
                enemy.draw()

            # update and draw groups
            bullet_group.update()
            item_box_group.update()
            decoration_group.update()
            water_group.update()
            exit_group.update()
            bullet_group.draw(screen)
            item_box_group.draw(screen)
            decoration_group.draw(screen)
            water_group.draw(screen)
            exit_group.draw(screen)

        # show intro
        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        # update player actions
        if player.alive:
            if locked_item_picked == True:
                screen.fill((0, 0, 0))
                screen.blit(grifos, (5, 50))
                if correct_button.draw(screen):
                    print('correct button clicked')
                    locked_item_picked = False
                    update_quiz()
                    update_buttons()
                elif first_button.draw(screen):
                    if first_button is not correct_button:
                        print('first button clicked and is NOT correct button')
                        letter_counter = 0
                        locked_item_picked = False
                        update_quiz()
                        update_buttons()
                        start_intro = True
                        bg_scroll = 0
                        world_data = reset_level()
                        # load in level data and create world
                        with open(f'level{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        player, health_bar = world.process_data(world_data)
                elif second_button.draw(screen):
                    if second_button is not correct_button:
                        print('Second button clicked and is NOT correct button')
                        letter_counter = 0
                        locked_item_picked = False
                        update_quiz()
                        update_buttons()
                        start_intro = True
                        bg_scroll = 0
                        world_data = reset_level()
                        # load in level data and create world
                        with open(f'level{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        player, health_bar = world.process_data(world_data)

            # player actions
            if attack:
                player.update_action(4)  # attack
                # player.check_collisions()
            elif player.in_air:
                player.update_action(2)  # 2: jump
            elif moving_left or moving_right:
                player.update_action(1)  # 1: run
            else:
                player.update_action(0)  # 0: idle
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            if medium_level == True:
                if timer.get_elapsed_time() > 60 and level_complete == False:
                    screen_scroll = 0
                    if death_fade.fade():
                        if restart_button.draw(screen):
                            letter_counter = 0
                            death_fade.fade_counter = 0
                            start_intro = True
                            bg_scroll = 0
                            world_data = reset_level()
                            # load in level data and create world
                            with open(f'level{level}_data.csv', newline='') as csvfile:
                                reader = csv.reader(csvfile, delimiter=',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] = int(tile)
                            world = World()
                            player, health_bar = world.process_data(world_data)
                            timer.reset()
                            timer.start()
                # pygame.display.flip()
            elif hard_level == True and level_complete == False:
                if timer.get_elapsed_time() > 45:
                    screen_scroll = 0
                    if death_fade.fade():
                        if restart_button.draw(screen):
                            letter_counter = 0
                            death_fade.fade_counter = 0
                            start_intro = True
                            bg_scroll = 0
                            world_data = reset_level()
                            # load in level data and create world
                            with open(f'level{level}_data.csv', newline='') as csvfile:
                                reader = csv.reader(csvfile, delimiter=',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] = int(tile)
                            world = World()
                            player, health_bar = world.process_data(world_data)
                            timer.reset()
                            timer.start()
            # check if player has completed the level
            if level_complete:
                if easy_level:
                    if grades_shown == False:
                        if timer.get_elapsed_time() < 60:
                            print('time <60')
                            time_under_one_minute = False
                            screen.fill((0, 0, 0))
                            print('screen filled black')
                            screen.blit(grade_a_img, (350, 150))
                            print('image blited')
                            # pygame.display.flip()
                        elif 60 < timer.get_elapsed_time() <= 80:
                            print('time 60<>80')
                            time_under_one_minute = False
                            screen.fill((0, 0, 0))
                            print('screen filled black')
                            screen.blit(grade_b_img, (350, 150))
                            print('image blited')
                        elif timer.get_elapsed_time() > 80:
                            print('time >80')
                            time_under_one_minute = False
                            screen.fill((0, 0, 0))
                            print('screen filled black')
                            screen.blit(grade_c_img, (350, 150))
                            print('image blited')
                    while progress and proceed_to_credit == False:
                        print('progress true to proceed to credit')
                        proceed_to_credit = True
                        progress = False
                        grades_shown = True
                    if proceed_to_credit:
                        screen.fill(BG)
                        if level == 1:
                            screen.blit(athens_end_img, (0, 0))
                        elif level == 2:
                            screen.blit(knossos_end_img, (0, 0))
                        elif level == 3:
                            screen.blit(sparta_end_img, (0, 0))
                            while progress and game_finished == False:
                                screen.blit(end_credit_img, (0, 0))
                                if progress:
                                    game_finished = True
                                    start_game = False
                                    show_athens = False
                                    proceed_to_first_level = False
                                    level = 1
                                    progress = False
                                    world_data = []
                                    bg_scroll = 0
                                    for row in range(ROWS):
                                        r = [-1] * COLS
                                        world_data.append(r)
                                    # load in level data and create world
                                    with open(f'level{level}_data.csv', newline='') as csvfile:
                                        reader = csv.reader(csvfile, delimiter=',')
                                        for x, row in enumerate(reader):
                                            for y, tile in enumerate(row):
                                                world_data[x][y] = int(tile)
                                    world = World(male_selected=True)
                                    player, health_bar = world.process_data(world_data)
                                    timer.reset()
                                    # timer.start()
                        while progress and proceed_to_next_level == False:
                            print('progress true to proceed to next level')
                            proceed_to_next_level = True
                            start_intro = True
                            progress = False

                        if proceed_to_next_level and level == 1:
                            # pygame.time.wait(2000)
                            screen.blit(knosos_img, (0, 0))
                            while progress:
                                print('progress true to level 1')
                                start_intro = True
                                level += 1
                                bg_scroll = 0
                                world_data = reset_level()
                                if level <= MAX_LEVELS:
                                    # load in level data and create world
                                    with open(f'level{level}_data.csv', newline='') as csvfile:
                                        reader = csv.reader(csvfile, delimiter=',')
                                        for x, row in enumerate(reader):
                                            for y, tile in enumerate(row):
                                                world_data[x][y] = int(tile)
                                    world = World()
                                    player, health_bar = world.process_data(world_data)
                                    proceed_to_next_level = False
                                    proceed_to_credit = False
                                    letter_counter = 0
                                    all_letters_collected = False
                                    progress = False
                                    grades_shown = False
                                    timer.reset()
                                    timer.start()
                        elif proceed_to_next_level and level == 2:
                            screen.blit(sparta_img, (0, 0))
                            while progress:
                                print('progress true to level 3')
                                start_intro = True
                                level += 1
                                bg_scroll = 0
                                world_data = reset_level()
                                if level <= MAX_LEVELS:
                                    # load in level data and create world
                                    with open(f'level{level}_data.csv', newline='') as csvfile:
                                        reader = csv.reader(csvfile, delimiter=',')
                                        for x, row in enumerate(reader):
                                            for y, tile in enumerate(row):
                                                world_data[x][y] = int(tile)
                                    world = World()
                                    player, health_bar = world.process_data(world_data)
                                    proceed_to_next_level = False
                                    proceed_to_credit = False
                                    letter_counter = 0
                                    all_letters_collected = False
                                    progress = False
                                    grades_shown = False
                                    timer.reset()
                                    timer.start()
                elif medium_level:
                    if grades_shown == False:
                        if timer.get_elapsed_time() < 60:
                            time_under_one_minute = False
                            screen.fill((0, 0, 0))
                            screen.blit(grade_a_img, (350, 150))
                            # pygame.display.update()
                        elif timer.get_elapsed_time() > 60 and timer.get_elapsed_time() <= 80:
                            time_under_one_minute = False
                            screen.fill((0, 0, 0))
                            screen.blit(grade_b_img, (350, 150))
                            # pygame.display.update()
                        elif timer.get_elapsed_time() > 80:
                            time_under_one_minute = False
                            screen.fill((0, 0, 0))
                            screen.blit(grade_c_img, (350, 150))
                            # pygame.display.update()
                    while progress and proceed_to_credit == False:
                        proceed_to_credit = True
                        progress = False
                        grades_shown = True

                    if not all_letters_collected:
                        screen.fill((0, 0, 0))
                        screen.blit(not_all_letters_text, (150, 150))
                        screen.blit(move_prompt_text, (150, 250))
                    elif all_letters_collected and proceed_to_credit:
                        screen.fill(BG)
                        if level == 1:
                            screen.blit(athens_end_img, (0, 0))
                        elif level == 2:
                            screen.blit(knossos_end_img, (0, 0))
                        elif level == 3:
                            screen.blit(sparta_end_img, (0, 0))
                            if end_game:
                                screen.blit(end_credit_img, (0, 0))
                                if progress:
                                    start_game = False
                                    show_athens = False
                                    proceed_to_first_level = False
                                    level = 1
                                    progress = False
                                    world_data = []
                                    bg_scroll = 0

                                    for row in range(ROWS):
                                        r = [-1] * COLS
                                        world_data.append(r)
                                    # load in level data and create world
                                    with open(f'level{level}_data.csv', newline='') as csvfile:
                                        reader = csv.reader(csvfile, delimiter=',')
                                        for x, row in enumerate(reader):
                                            for y, tile in enumerate(row):
                                                world_data[x][y] = int(tile)
                                    world = World(male_selected=True)
                                    player, health_bar = world.process_data(world_data)
                                    timer.reset()
                                    timer.start()

                        # add buttons
                        while progress and proceed_to_next_level == False:
                            proceed_to_next_level = True
                            start_intro = True
                            progress = False

                        if proceed_to_next_level and level == 1:
                            screen.blit(knosos_img, (0, 0))
                            while progress:
                                start_intro = True
                                level += 1
                                bg_scroll = 0
                                world_data = reset_level()
                                if level <= MAX_LEVELS:
                                    # load in level data and create world
                                    with open(f'level{level}_data.csv', newline='') as csvfile:
                                        reader = csv.reader(csvfile, delimiter=',')
                                        for x, row in enumerate(reader):
                                            for y, tile in enumerate(row):
                                                world_data[x][y] = int(tile)
                                    world = World()
                                    player, health_bar = world.process_data(world_data)
                                    proceed_to_next_level = False
                                    proceed_to_credit = False
                                    letter_counter = 0
                                    all_letters_collected = False
                                    progress = False
                                    grades_shown = False
                                    timer.reset()
                                    timer.start()
                        elif proceed_to_next_level and level == 2:
                            screen.blit(sparta_img, (0, 0))
                            while progress:
                                start_intro = True
                                level += 1
                                bg_scroll = 0
                                world_data = reset_level()
                                if level <= MAX_LEVELS:
                                    # load in level data and create world
                                    with open(f'level{level}_data.csv', newline='') as csvfile:
                                        reader = csv.reader(csvfile, delimiter=',')
                                        for x, row in enumerate(reader):
                                            for y, tile in enumerate(row):
                                                world_data[x][y] = int(tile)
                                    world = World()
                                    player, health_bar = world.process_data(world_data)
                                    proceed_to_next_level = False
                                    proceed_to_credit = False
                                    letter_counter = 0
                                    all_letters_collected = False
                                    progress = False
                                    grades_shown = False
                                    timer.reset()
                                    timer.start()
                elif hard_level:
                    if grades_shown == False:
                        if timer.get_elapsed_time() < 60:
                            time_under_one_minute = False
                            screen.fill((0, 0, 0))
                            screen.blit(grade_a_img, (350, 150))
                            # pygame.display.update()
                        elif timer.get_elapsed_time() > 60 and timer.get_elapsed_time() <= 80:
                            time_under_one_minute = False
                            screen.fill((0, 0, 0))
                            screen.blit(grade_b_img, (350, 150))
                            # pygame.display.update()
                        elif timer.get_elapsed_time() > 80:
                            time_under_one_minute = False
                            screen.fill((0, 0, 0))
                            screen.blit(grade_c_img, (350, 150))
                            # pygame.display.update()

                    while progress and proceed_to_credit == False:
                        proceed_to_credit = True
                        progress = False
                        grades_shown = True

                    if not all_letters_collected:
                        screen.fill((0, 0, 0))
                        screen.blit(not_all_letters_text, (150, 150))

                    elif all_letters_collected and proceed_to_credit:
                        screen.fill(BG)
                        if level == 1:
                            screen.blit(athens_end_img, (0, 0))
                        elif level == 2:
                            screen.blit(knossos_end_img, (0, 0))
                        elif level == 3:
                            screen.blit(sparta_end_img, (0, 0))
                            if end_game:
                                screen.blit(end_credit_img, (0, 0))
                                if progress:
                                    start_game = False
                                    show_athens = False
                                    proceed_to_first_level = False
                                    level = 1
                                    progress = False
                                    world_data = []
                                    bg_scroll = 0
                                    for row in range(ROWS):
                                        r = [-1] * COLS
                                        world_data.append(r)
                                    # load in level data and create world
                                    with open(f'level{level}_data.csv', newline='') as csvfile:
                                        reader = csv.reader(csvfile, delimiter=',')
                                        for x, row in enumerate(reader):
                                            for y, tile in enumerate(row):
                                                world_data[x][y] = int(tile)
                                    world = World(male_selected=True)
                                    player, health_bar = world.process_data(world_data)
                                    timer.reset()
                                    timer.start()
                        while progress and proceed_to_next_level == False:
                            proceed_to_next_level = True
                            start_intro = True
                            progress = False
                        if proceed_to_next_level and level == 1:
                            screen.blit(knosos_img, (0, 0))
                            while progress:
                                start_intro = True
                                level += 1
                                bg_scroll = 0
                                world_data = reset_level()
                                if level <= MAX_LEVELS:
                                    # load in level data and create world
                                    with open(f'level{level}_data.csv', newline='') as csvfile:
                                        reader = csv.reader(csvfile, delimiter=',')
                                        for x, row in enumerate(reader):
                                            for y, tile in enumerate(row):
                                                world_data[x][y] = int(tile)
                                    world = World()
                                    player, health_bar = world.process_data(world_data)
                                    proceed_to_next_level = False
                                    proceed_to_credit = False
                                    letter_counter = 0
                                    all_letters_collected = False
                                    progress = False
                                    grades_shown = False
                                    timer.reset()
                                    timer.start()
                        elif proceed_to_next_level and level == 2:
                            screen.blit(sparta_img, (0, 0))
                            while progress:
                                start_intro = True
                                level += 1
                                bg_scroll = 0
                                world_data = reset_level()
                                if level <= MAX_LEVELS:
                                    # load in level data and create world
                                    with open(f'level{level}_data.csv', newline='') as csvfile:
                                        reader = csv.reader(csvfile, delimiter=',')
                                        for x, row in enumerate(reader):
                                            for y, tile in enumerate(row):
                                                world_data[x][y] = int(tile)
                                    world = World()
                                    player, health_bar = world.process_data(world_data)
                                    proceed_to_next_level = False
                                    proceed_to_credit = False
                                    letter_counter = 0
                                    all_letters_collected = False
                                    progress = False
                                    grades_shown = False
                                    timer.reset()
                                    timer.start()
        else:
            screen_scroll = 0
            if death_fade.fade():
                if restart_button.draw(screen):
                    letter_counter = 0
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    world_data = reset_level()
                    # load in level data and create world
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                attack = True
                # print('Attacked')
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_ESCAPE:
                # run = False
                # display_menu = True
                menu_active = True
            if event.key == pygame.K_e:
                progress = True
                handled_e_press = False
            if event.key == pygame.K_q:
                end_game = True
            if event.key == pygame.K_m:
                muted_index += 1

        # keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                attack = False
            if event.key == pygame.K_q:
                end_game = False
            if event.key == pygame.K_e:
                progress = False
            # if event.key == pygame.K_ESCAPE:
            #     display_menu = False

    pygame.display.update()

pygame.quit()
