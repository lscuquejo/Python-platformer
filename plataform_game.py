import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *

# Initialize the Pygame
pygame.init()

# Title
pygame.display.set_caption('My Pygame Window')

# Create the screem
WINDOW_SIZE = (600, 400)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((300, 200))

# Images load
background_image = pygame.image.load("sky.png")
cloud_image = pygame.image.load('cloud.png')
player_image = pygame.image.load('player.png')
ground_image = pygame.image.load('ground.png')
black_image = pygame.image.load('black.png')

TILE_SIZE = black_image.get_width()


# game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
#             ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
#             ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
#             ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
#             ['0','0','0','0','0','0','0','2','2','2','2','2','0','0','0','0','0','0','0'],
#             ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
#             ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],
#             ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1'],
#             ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
#             ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
#             ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
#             ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
#             ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]

game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','2','2','2','2','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','2','2','2','2','2','2','2','2','2','2'],
            ['2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2'],
            ['2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2'],
            ['2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2'],
            ['2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2']]

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

moving_right = False
moving_left = False

player_location = [50,50]
player_y_momentum = 0

player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(50,50,100, 50)

while True: #game loop

    # screen.blit(background_image, [0, 0])
    display.fill((146,244,255))

    # Background Image
    display.blit(background_image, (0,0))

    # Cloud generator
    number_of_clouds = 3
    y_pixels = 20
    x_pixels = 0
    for cloud in range(number_of_clouds):
        display.blit(cloud_image, (x_pixels, y_pixels))
        x_pixels += 100
    
    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(black_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                display.blit(ground_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    player_movement = [0, 0]

    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3 :
        player_y_momentum = 3
    
    # player_rect, collision_types = move(player_rect, player_movement, tile_rects)
    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    display.blit(player_image, (player_rect.x, player_rect.y))

    # if moving_right == True:
    #     player_location[0] += 4
    # if moving_left == True:
    #     player_location[0] -= 4

    # player_rect.x = player_location[0]
    # player_rect.y = player_location[1]

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
    
    # screen.blit(background_image, [0, 0])

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))

    pygame.display.update()
    clock.tick(60)