import os
import sys
import pygame
import requests

MAP_FILE = "map.png"
MAP_REQUEST = "http://static-maps.yandex.ru/1.x/?"
CORDS, SCALE = sys.argv[1:]
# 30.401486,59.963203 0.002,0.002
SCALE = [float(el) for el in SCALE.split(',')]


SPN = [0.002, 0.003, 0.006, 0.01, 0.02, 0.04, 0.08, 0.1, 0.16, 0.2]


def image_show(c):
    global SCALE

    params = {"ll": c,
              "spn": ','.join([str(el) for el in SCALE]),
              "l": "map"}
    response = requests.get(MAP_REQUEST, params=params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(MAP_REQUEST)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    # Запишем полученное изображение в файл.
    with open(MAP_FILE, "wb") as file:
        file.write(response.content)


image_show(CORDS)  # создали файл с нужным изображением


pygame.init()
screen = pygame.display.set_mode((600, 450))
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
            image_show(CORDS)
    screen.blit(pygame.image.load(MAP_FILE), (0, 0))
    pygame.display.flip()


# Удаляем за собой файл с изображением.
os.remove(MAP_FILE)