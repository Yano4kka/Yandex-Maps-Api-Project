import os
import sys
import pygame
import requests
import json
from func import print_on_screen, Options, Options2

MAP_FILE = "map.png"
MAP_REQUEST = "http://static-maps.yandex.ru/1.x/?"
CORDS = ''
SCALE = [0.002, 0.002]
SPN = [0.001, 0.002, 0.003, 0.006, 0.01, 0.02, 0.04, 0.08, 0.1, 0.16, 0.2]
RESPONSE = ''
JSON_RESPONSE = ''
LOWER_CORNER = ''
UPPER_CORNER = ''
L = "map"
options_group = pygame.sprite.Group()
options_group2 = pygame.sprite.Group()
SEARCH_RESULT = False
movement_is_done = False
CENTER = ''


def search(input_search):
    global CORDS, CENTER
    req = 'https://geocode-maps.yandex.ru/1.x/?'
    params = {"geocode": input_search,
              "spn": ','.join([str(el) for el in SCALE]),
              "format": "json",
              "apikey": "40d1649f-0493-4b70-98ba-98533de7710b"}
    response = requests.get(req, params=params)
    json_response = response.json()
    coods = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
    CORDS = [float(el) for el in coods.split(" ")]
    CENTER = [float(el) for el in coods.split(" ")]
    image_show()
    geocode_inf()


def image_show():  # вывод картинки на экран
    global SCALE, CORDS, RESPONSE, L
    if not movement_is_done and CORDS == CENTER:
        params = {"ll": ','.join([str(el) for el in CORDS]),
                  "spn": ','.join([str(el) for el in SCALE]),
                  "l": L,
                  "size": '600,400',
                  "pt": ','.join([str(el) for el in CORDS]) + ',org'}

    elif movement_is_done and abs(CORDS[0] - CENTER[0]) <= 0.0001 and abs(CORDS[1] - CENTER[1]) <= 0.0001:
        params = {"ll": ','.join([str(el) for el in CORDS]),
                  "spn": ','.join([str(el) for el in SCALE]),
                  "l": L,
                  "size": '600,400',
                  "pt": ','.join([str(el) for el in CENTER]) + ',org'}

    elif movement_is_done and CORDS != CENTER:
        params = {"ll": ','.join([str(el) for el in CORDS]),
                  "spn": ','.join([str(el) for el in SCALE]),
                  "l": L,
                  "size": '600,400'}

    RESPONSE = requests.get(MAP_REQUEST, params=params)
    if not RESPONSE:
        print("Ошибка выполнения запроса:")
        print(MAP_REQUEST)
        print("Http статус:", RESPONSE.status_code, "(", RESPONSE.reason, ")")
        sys.exit(1)
    # Запишем полученное изображение в файл.
    with open(MAP_FILE, "wb") as file:
        file.write(RESPONSE.content)


def geocode_inf():  # получаем нужную информацию с геокодера
    global JSON_RESPONSE, LOWER_CORNER, UPPER_CORNER
    req = 'https://geocode-maps.yandex.ru/1.x/?'
    params = {"geocode": ','.join([str(el) for el in CORDS]),
              "spn": ','.join([str(el) for el in SCALE]),
              "format": "json",
              "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
              "ll": ','.join([str(el) for el in CORDS])}
    response = requests.get(req, params=params)
    JSON_RESPONSE = response.json()

    with open('file.json', 'w') as f:
        json.dump(JSON_RESPONSE, f)

    corners = JSON_RESPONSE['response']["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["boundedBy"]["Envelope"]
    LOWER_CORNER = [float(el) for el in corners["lowerCorner"].split()]
    UPPER_CORNER = [float(el) for el in corners["upperCorner"].split()]

g = Options('гибрид.png', 50, 200, options_group)
m = Options('схема.png', 115, 200, options_group)
s = Options('спутник.png', 170, 200, options_group)
reset = Options2('сброс.jpg', 650, 10, options_group2)

pygame.init()
clock = pygame.time.Clock()
FPS = 60
screen = pygame.display.set_mode((700, 700))
running = True
need_search = False
input_search = ''

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if need_search:
                if event.key == pygame.K_BACKSPACE:  # если нажат backspace стираем по одному элементу
                    input_search = input_search[:-1]
                else:
                    input_search += event.unicode
            if SEARCH_RESULT:  # если топоним найден
                if event.key == pygame.K_PAGEUP:
                    for el in SPN[::-1]:
                        if el < SCALE[0]:
                            SCALE[0] = el
                            SCALE[1] = el
                            break
                if event.key == pygame.K_PAGEDOWN:
                    for el in SPN:
                        if el > SCALE[0]:
                            SCALE[0] = el
                            SCALE[1] = el
                            break
                if event.key == pygame.K_LEFT:
                    CORDS[0] -= (float(UPPER_CORNER[0]) - float(LOWER_CORNER[0])) * 2
                    movement_is_done = True
                if event.key == pygame.K_RIGHT:
                    CORDS[0] += (float(UPPER_CORNER[0]) - float(LOWER_CORNER[0])) * 2
                    movement_is_done = True
                if event.key == pygame.K_UP:
                    CORDS[1] += (float(UPPER_CORNER[1]) - float(LOWER_CORNER[1])) * 2
                    movement_is_done = True
                if event.key == pygame.K_DOWN:
                    CORDS[1] -= (float(UPPER_CORNER[1]) - float(LOWER_CORNER[1])) * 2
                    movement_is_done = True
                if SEARCH_RESULT:
                    image_show()
                    geocode_inf()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if SEARCH_RESULT:  # если найден результат
                for el in options_group.sprites():
                    if el.rect.collidepoint(event.pos) and el.im == 'спутник.png':
                        L = 'sat'
                    if el.rect.collidepoint(event.pos) and el.im == 'схема.png':
                        L = 'map'
                    if el.rect.collidepoint(event.pos) and el.im == 'гибрид.png':
                        L = 'sat,skl'
                    image_show()

            for el in options_group2.sprites():
                if el.rect.collidepoint(event.pos) and el.im == 'сброс.jpg':
                    SEARCH_RESULT = False
                    movement_is_done = False
                    input_search = ''

            '''Поле ввода'''
            if search_field.collidepoint(event.pos):  # коллизия с полем ввода
                need_search = True
            else:
                need_search = False
            if search_button.collidepoint(event.pos) and input_search:
                search(input_search)
                SEARCH_RESULT = True
                movement_is_done = False

    search_field = pygame.draw.rect(screen, pygame.Color('white'), (50, 10, 500, 30))
    search_button = pygame.draw.rect(screen, pygame.Color('white'), (570, 10, 70, 30))
    print_on_screen(screen, ('Искать', 575, 20, 25))
    if not need_search:
        pygame.draw.rect(screen, pygame.Color('black'), (50, 10, 500, 30), 2)
    if need_search:
        pygame.draw.rect(screen, pygame.Color('green'), (50, 10, 500, 30), 2)
    if input_search:
        print_on_screen(screen, (input_search, 65, 15, 20))
    if SEARCH_RESULT:
        screen.blit(pygame.image.load(MAP_FILE), (50, 250))
        options_group.draw(screen)
    else:
        screen.fill(pygame.Color('black'), pygame.Rect(50, 200, 600, 500))
    options_group2.draw(screen)  # рисуем кнопку сброса в любом случае
    pygame.display.update()
    clock.tick(FPS)


# Удаляем за собой файл с изображением.
os.remove(MAP_FILE)

