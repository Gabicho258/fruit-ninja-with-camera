
import pygame
import cv2
import mediapipe as mp
import threading
import random
import time


class StartCamera(threading.Thread):
    def __init__(self, x):
        self.__x = x
        threading.Thread.__init__(self)

    def run(self):  # run() se utiliza para definir el comportamiento del hilo
        start_camera()

    def kill(self):
        self.killed = True


class StartCollisions(threading.Thread):
    def __init__(self, x):
        self.__x = x
        threading.Thread.__init__(self)

    def run(self):  # run() se utiliza para definir el comportamiento del hilo
        start_collisions()

    def kill(self):
        self.killed = True


BLANCO = (255, 255, 255)
COLOR_TEXTO = (50, 60, 80)

# Inicialización de Pygame
pygame.init()
# Inicialización de la superficie de dibujo
width = 640
height = 480

ventana = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fruit Ninja")
background = pygame.image.load("images/background_image.jpg")
background = pygame.transform.scale(background, (width, height))
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

x = 0
y = 0


def start_camera():
    mp_hands = mp.solutions.hands
    # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5) as hands:
        while not game_over:
            ret, frame = cap.read()
            if ret == False:
                break
            height, width, _ = frame.shape
            # print("Height", height)
            # print("Width", width)
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)
            # print("Handedness:", results.multi_handedness)
            # print('Hand landmarks:', results.multi_hand_landmarks)
            if results.multi_hand_landmarks is not None:
                index = [12]
                for hand_landmarks in results.multi_hand_landmarks:
                    for (i, points) in enumerate(hand_landmarks.landmark):
                        if i in index:
                            global x
                            global y
                            x = int(points.x * width)
                            y = int(points.y * height)

            # cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    cap.release()
    # cv2.destroyAllWindows()


#################################colisiones############################################
# size of a block
pixel = 64

# load the image
gameIcon = pygame.image.load("rectangleBlock.png")


# load the image
backgroundImg = pygame.image.load("wallBackground.jpg")
backgroundImg = pygame.transform.scale(backgroundImg, (width, height))

# load the image
playerImage = pygame.image.load("player.png")
playerImage = pygame.transform.scale(playerImage, (50, 50))

# set the position
playerXPosition = (width/2) - (pixel/2)

# So that the player will be
# at height of 20 above the base
playerYPosition = height - pixel - 10

# set initially 0
playerXPositionChange = 0

# define a function for setting
# the image at particular
# coordinates


def player(x, y):
    # paste image on screen object
    ventana.blit(playerImage, (x, y))


# load the image
blockImage = pygame.image.load("rectangleBlock.png")
blockImage = pygame.transform.scale(blockImage, (pixel, pixel))

# set the random position
blockXPosition = random.randint(0,
                                (width - pixel))

blockYPosition = 0 - pixel
counter = 0
# set the speed of
# the block
blockXPositionChange = 0
blockYPositionChange = 2

# define a function for setting
# the image at particular
# coordinates


def block(x, y):
    # paste image on screen object
    ventana.blit(blockImage,
                 (x, y))

# define a function for
# collision detection


def crash():
    # take a global variable
    global blockYPosition
    global blockXPosition
    global counter
    global x
    global y
    global pixel
    # check conditions
    if y < (blockYPosition + pixel):

        if ((x > blockXPosition
             and x < (blockXPosition + pixel))
            or ((x + pixel) > blockXPosition
                and (x + pixel) < (blockXPosition + pixel))):
            blockYPosition = height + 10
            counter += 1
            print("Score: ", counter)


def start_collisions():
    global ventana
    global game_over
    global playerXPosition
    global playerYPosition
    global blockXPosition
    global blockYPosition
    global counter
    global blockXPositionChange
    global blockYPositionChange
    global playerXPositionChange
    global playerImage
    global blockImage
    global backgroundImg
    global gameIcon
    global pixel
    global width
    global height
    global x
    global y

    while not game_over:
        # set the image on screen object
        ventana.blit(backgroundImg, (0, 0))

        # loop through all events
        for event in pygame.event.get():

            # check the quit condition
            if event.type == pygame.QUIT:
                # quit the game
                pygame.quit()

            # movement key control of player
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:

                    playerXPositionChange = 1

                if event.key == pygame.K_LEFT:

                    playerXPositionChange = -1

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_RIGHT or pygame.K_LEFT:

                    playerXPositionChange = 0
        # Boundaries to the Player

        # if it comes at right end,
        # stay at right end and
        # does not exceed
        if playerXPosition >= (width - pixel):
            playerXPosition = (width - pixel)

        # if it comes at left end,
        # stay at left end and
        # does not exceed
        if playerXPosition <= 0:
            playerXPosition = 0
        # Multiple Blocks Movement after each other
        # and condition used because of game over function
        if (blockYPosition >= height - 0 and
                blockYPosition <= (height + 200)):

            blockYPosition = 0 - pixel

            # randomly assign value in range
            blockXPosition = random.randint(0, (width - pixel))
        # movement of Player
        playerXPosition += playerXPositionChange

        # movement of Block
        blockYPosition += blockYPositionChange

        # player Function Call
        player(x, y)

        # block Function Call
        block(blockXPosition, blockYPosition)

        # crash function call
        crash()

        time.sleep(0.01)
        # update screen
        pygame.display.update()

########################################################################################


def main():
    global game_over
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

    dibujar_botones_iniciales(botones)
    click = False
    camera = StartCamera(1)
    collisions = StartCollisions(2)
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
            print("Jugar")
            camera.start()
            collisions.start()
            click = False

        # dibujar_botones_iniciales(botones)

        if click and botones[1]['on_click']:
            game_over = True
            camera.kill()
            camera.join()
            collisions.kill()
            collisions.join()
            click = False

        # print("X: ", x)
        # print("Y: ", y)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
