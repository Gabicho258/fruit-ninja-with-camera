import pygame
import random
from pygame.locals import *

FONDO = (32, 30, 32)
BLANCO = (255, 255, 255)
COLOR_TEXTO = (50, 60, 80)

pygame.init()
dimensiones = [600, 460]
pantalla = pygame.display.set_mode(dimensiones)
pygame.display.set_caption("Entrada de texto")
imagen_panel = pygame.image.load("./img/panel.png")
imagen_boton = pygame.image.load("./img/button.png")
imagen_boton_pressed = pygame.image.load("./img/buttonPressed.png")
fuente = pygame.font.SysFont('Courier', 20)
#########


def dibujar_texto(texto, contenedor_imagen, contenedor_rec, fuente_render, color):
    text = fuente_render.render(texto, 1, color)
    centro = text.get_rect()
    diferencia_x = contenedor_imagen.center[0] - centro.center[0]
    diferencia_y = contenedor_imagen.center[1] - centro.center[1]
    pantalla.blit(text, [contenedor_rec.left + diferencia_x,
                  contenedor_rec.top + diferencia_y])


#

def dibujar_botones_iniciales(lista_botones):
    panel = pygame.transform.scale(imagen_panel, [560, 420])
    pantalla.blit(panel, [20, 20])
    for boton in lista_botones:
        if boton['on_click']:
            pantalla.blit(boton['imagen_pressed'], boton['rect'])
        else:
            pantalla.blit(boton['imagen'], boton['rect'])
        dibujar_texto(boton['texto'], boton['imagen'].get_rect(),
                      boton['rect'], fuente, BLANCO)

#########


def main():
    game_over = False
    clock = pygame.time.Clock()

    r_boton_1_1 = imagen_boton.get_rect()
    r_boton_1_2 = imagen_boton.get_rect()

    botones = []
    r_boton_1_1.topleft = [80, 80]
    botones.append({'texto': "Jugar", 'imagen': imagen_boton,
                   'imagen_pressed': imagen_boton_pressed, 'rect': r_boton_1_1, 'on_click': False})
    r_boton_1_2.topleft = [90, 80]
    botones.append({'texto': "Salir", 'imagen': imagen_boton,
                   'imagen_pressed': imagen_boton_pressed, 'rect': r_boton_1_2, 'on_click': False})

    # dibujar_botones_iniciales(botones)
    click = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_over = True
            if event.type == MOUSEBUTTONDOWN:
                mouse = event.pos
                for boton in botones:
                    boton['on_click'] = boton['rect'].colliderect(
                        [mouse[0], mouse[1], 1, 1])
                click = True
            if event.type == MOUSEBUTTONUP:
                for boton in botones:
                    boton['on_click'] = False

        if botones[0]['on_click'] and click:
            print("boton 1")
            click = False

        pantalla.fill(FONDO)
        dibujar_botones_iniciales(botones)
        # pantalla.blit(input_text, campo_texto['rect'].topleft)

        if click and botones[1]['on_click']:
            print("boton 2")
            click = False

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()
