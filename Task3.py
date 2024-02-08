import os
import sys
import pygame
import requests
import json

MAP_FILE = "map.png"
MAP_REQUEST = "http://static-maps.yandex.ru/1.x/?"
CORDS, SCALE = sys.argv[1:]
# 30.401486,59.963203 0.002,0.002
SCALE = [float(el) for el in SCALE.split(',')]
CORDS = [float(el) for el in CORDS.split(',')]
SPN = [0.001, 0.002, 0.003, 0.006, 0.01, 0.02, 0.04, 0.08, 0.1, 0.16, 0.2]
RESPONSE = ''
JSON_RESPONSE = ''
LOWER_CORNER = ''
UPPER_CORNER = ''


def image_show():  # вывод картинки на экран
    global SCALE, CORDS, RESPONSE
    params = {"ll": ','.join([str(el) for el in CORDS]),
              "spn": ','.join([str(el) for el in SCALE]),
              "l": "map",
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


image_show()  # создали файл с нужным изображением
geocode_inf()
pygame.init()
screen = pygame.display.set_mode((700, 700))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
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
            if event.key == pygame.K_RIGHT:
                CORDS[0] += (float(UPPER_CORNER[0]) - float(LOWER_CORNER[0])) * 2
            if event.key == pygame.K_UP:
                CORDS[1] += (float(UPPER_CORNER[1]) - float(LOWER_CORNER[1])) * 2
            if event.key == pygame.K_DOWN:
                CORDS[1] -= (float(UPPER_CORNER[1]) - float(LOWER_CORNER[1])) * 2
            image_show()
            geocode_inf()
    screen.fill((255, 255, 255))
    screen.blit(pygame.image.load(MAP_FILE), (50, 250))
    pygame.display.flip()


# Удаляем за собой файл с изображением.
os.remove(MAP_FILE)