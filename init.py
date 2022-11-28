
import pygame

BLANCO = (255, 255, 255)
COLOR_TEXTO = (50, 60, 80)

# Inicialización de Pygame
pygame.init()
# Inicialización de la superficie de dibujo
ventana = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Fruit Ninja")
background = pygame.image.load("images/background_image.jpg")
background = pygame.transform.scale(background, (640, 480))
# imagen_panel = pygame.image.load("./img/panel.png")
imagen_boton = pygame.image.load("./img/button.png")
imagen_boton_pressed = pygame.image.load("./img/buttonPressed.png")
fuente = pygame.font.SysFont('Courier', 20)


def dibujar_texto(texto, contenedor_imagen, contenedor_rec, fuente_render, color):
    text = fuente_render.render(texto, 1, color)
    centro = text.get_rect()
    diferencia_x = contenedor_imagen.center[0] - centro.center[0]
    diferencia_y = contenedor_imagen.center[1] - centro.center[1]
    ventana.blit(text, [contenedor_rec.left + diferencia_x,
                        contenedor_rec.top + diferencia_y])


#

def dibujar_botones_iniciales(lista_botones):
    # panel = pygame.transform.scale(imagen_panel, [560, 420])
    # ventana.blit(panel, [20, 20])
    for boton in lista_botones:
        if boton['on_click']:
            ventana.blit(boton['imagen_pressed'], boton['rect'])
        else:
            ventana.blit(boton['imagen'], boton['rect'])
        dibujar_texto(boton['texto'], boton['imagen'].get_rect(),
                      boton['rect'], fuente, BLANCO)


ventana.blit(background, (0, 0))
# Bucle principal del juego
# jugando = True
# while jugando:
#     # Comprobamos los eventos
#     # Comprobamos si se ha pulsado el botón de cierre de la ventana
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             jugando = False
#     # Se pinta la ventana con un color
#     # Esto borra los posibles elementos que teníamos anteriormente
#     # ventana.fill((255, 255, 255))
#     # Todos los elementos del juego se vuelven a dibujar
#     pygame.display.flip()
#     # Controlamos la frecuencia de refresco (FPS)
#     pygame.time.Clock().tick(60)
# pygame.quit()


def main():
    game_over = False
    clock = pygame.time.Clock()

    r_boton_1_1 = imagen_boton.get_rect()
    r_boton_1_2 = imagen_boton.get_rect()

    botones = []
    r_boton_1_1.topleft = [230, 200]
    botones.append({'texto': "Jugar", 'imagen': imagen_boton,
                   'imagen_pressed': imagen_boton_pressed, 'rect': r_boton_1_1, 'on_click': False})
    r_boton_1_2.topleft = [230, 280]
    botones.append({'texto': "Salir", 'imagen': imagen_boton,
                   'imagen_pressed': imagen_boton_pressed, 'rect': r_boton_1_2, 'on_click': False})

    # dibujar_botones_iniciales(botones)
    click = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = event.pos
                for boton in botones:
                    boton['on_click'] = boton['rect'].colliderect(
                        [mouse[0], mouse[1], 1, 1])
                click = True
            if event.type == pygame.MOUSEBUTTONUP:
                for boton in botones:
                    boton['on_click'] = False

        if botones[0]['on_click'] and click:
            print("boton 1")
            click = False

        dibujar_botones_iniciales(botones)

        if click and botones[1]['on_click']:
            game_over = True
            click = False

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()
