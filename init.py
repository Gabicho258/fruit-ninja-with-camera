
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
# size of a block
pixel = 64

ventana = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fruit Ninja")
background = pygame.image.load("images/background_image.jpg")
background = pygame.transform.scale(background, (width, height))
# imagen_panel = pygame.image.load("./img/panel.png")
imagen_boton = pygame.image.load("./images/button.png")
imagen_boton_scaled = pygame.transform.scale(imagen_boton, (280, 49))
imagen_boton_pressed = pygame.image.load("./images/buttonPressed.png")
fuente = pygame.font.SysFont('Courier', 20)

#############frutas################

orange = pygame.image.load("./images/orange.png")
orange = pygame.transform.scale(orange, (pixel, pixel))
watermelon = pygame.image.load("./images/watermelon.png")
watermelon = pygame.transform.scale(watermelon, (pixel, pixel))
pineapple = pygame.image.load("./images/pineapple.png")
pineapple = pygame.transform.scale(pineapple, (pixel, pixel))
apple = pygame.image.load("./images/apple.png")
apple = pygame.transform.scale(apple, (pixel, pixel))
banana = pygame.image.load("./images/banana.png")
banana = pygame.transform.scale(banana, (pixel, pixel))

fruits = [orange, watermelon, pineapple, apple, banana]

current_fruit = fruits[random.randint(0, len(fruits) - 1)]

###################################

startTime = 0
endTime = 0


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

camera_open = False


def start_camera():
    global camera_open
    camera_open = True
    mp_hands = mp.solutions.hands
    # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5) as hands:
        while camera_open:
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
# buttons
r_button_timer = imagen_boton.get_rect()
r_button_timer.center = (width/2, 30)
button_timer = {'texto': "Time", 'imagen': imagen_boton,
                'imagen_pressed': imagen_boton_pressed, 'rect': r_button_timer, 'on_click': False}
r_button_score = imagen_boton.get_rect()
r_button_score.topleft = (25, 420)
button_score = {'texto': "Score", 'imagen': imagen_boton,
                'imagen_pressed': imagen_boton_pressed, 'rect': r_button_score, 'on_click': False}

# load the image
gameIcon = pygame.image.load("./images/rectangleBlock.png")


# load the image
backgroundImg = pygame.image.load("./images/wallBackground.jpg")
backgroundImg = pygame.transform.scale(backgroundImg, (width, height))

# load the image
playerImage = pygame.image.load("./images/katana2.png")
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
blockImage = pygame.image.load("./images/rectangleBlock.png")
blockImage = pygame.transform.scale(blockImage, (pixel, pixel))

# set the random position
blockXPosition = random.randint(0,
                                (width - pixel))

blockYPosition = 0 - pixel
score = 0
# set the speed of
# the block
blockXPositionChange = 0
blockYPositionChange = 2

# define a function for setting
# the image at particular
# coordinates


def block(x, y):
    global current_fruit
    # paste image on screen object
    ventana.blit(current_fruit,
                 (x, y))

# define a function for
# collision detection


def crash():
    # take a global variable
    global blockYPosition
    global blockXPosition
    global score
    global x
    global y
    global pixel
    global fruits
    global current_fruit
    # check conditions
    if y < (blockYPosition + pixel):

        if ((x > blockXPosition
             and x < (blockXPosition + pixel))
            or ((x + pixel) > blockXPosition
                and (x + pixel) < (blockXPosition + pixel))):
            blockYPosition = height + 10
            score += 1
            print("Score: ", score)
            current_fruit = fruits[random.randint(0, len(fruits) - 1)]


def start_collisions():
    global ventana
    global game_over
    global playerXPosition
    global playerYPosition
    global blockXPosition
    global blockYPosition
    global score
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
    global startTime
    global endTime
    global camera_open
    global game_started

    while game_started:
        # set the image on screen object
        # if game_over:
        #     break
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

        endTime = int(time.time())
        button_timer['text'] = "Time: " + \
            str(60 - int(endTime - startTime))
        ventana.blit(button_timer['imagen'], button_timer['rect'])
        dibujar_texto(button_timer['text'], button_timer['imagen'].get_rect(),
                      button_timer['rect'], fuente, BLANCO)
        button_score['text'] = "Score: " + \
            str(score)
        ventana.blit(button_score['imagen'], button_score['rect'])
        dibujar_texto(button_score['text'], button_score['imagen'].get_rect(),
                      button_score['rect'], fuente, BLANCO)
        if (endTime - startTime) > 60:
            ventana.blit(backgroundImg, (0, 0))
            button_score['text'] = "Tu score final es: " + \
                str(score)
            button_score['imagen'] = imagen_boton_scaled
            r_button_score.center = (width/2 - 50, height/2 - 10)
            ventana.blit(button_score['imagen'], button_score['rect'])
            dibujar_texto(button_score['text'], button_score['imagen'].get_rect(),
                          button_score['rect'], fuente, BLANCO)
            time.sleep(5)
            camera_open = False
            game_over = True
            game_started = False

        time.sleep(0.01)
        # update screen

        pygame.display.update()


########################################################################################
game_started = False
botones = []


def main():
    global game_over
    global game_started
    global botones
    global camera_open
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
    game_started = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                camera_open = False
                game_started = False
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
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

            global startTime
            game_started = True
            camera.start()
            startTime = int(time.time())

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
