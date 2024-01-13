import pygame
import random
import math
from pygame import mixer
import io

# Inicializar Pygame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e Icono
pygame.display.set_caption("Invasión Espacial by Adderly")
icono = pygame.image.load("Extraterrestre.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load('wallpaper.jpg')

#agregar musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Variables del Jugador
img_jugador = pygame.image.load("cohete.png")
jugador_x = 368
jugador_y = 520
jugador_x_Cambio = 0

# Variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_Cambio = []
enemigo_y_Cambio = []
cantidad_enemigo = 8

for e in range(cantidad_enemigo):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(25,100))
    enemigo_x_Cambio.append(1)
    enemigo_y_Cambio.append(50)

# Variables de la bala
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_x_Cambio = 0
bala_y_Cambio = 1
bala_visible = False

#puntaje
puntaje = 0
fuente = pygame.font.Font("freesansbold.ttf", 16)
texto_x = 10
texto_y = 10

#Final de juego
fuente_final = pygame.font.Font('freesansbold.ttf', 40)

def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (60,200))

#funcion mostrar puntaje
def mostrar_puntaje(x,y):
    texto = fuente.render(f'Puntaje: {puntaje}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


#Funcion del jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


#Funcion del jugador
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

#Funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

#Funcion colision
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        False



# Loop del juego
se_ejecuta = True
while se_ejecuta:

    # imagen de fondo
    pantalla.blit(fondo, (0, 0))

    #Iterar eventos
    for evento in pygame.event.get():

        #evento Cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        #Evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_Cambio = -0.3
            if evento.key == pygame.K_RIGHT:
                jugador_x_Cambio = 0.3
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

        #Evento soltar flechas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_Cambio = 0

    #modificar ubicacion del jugador
    jugador_x += jugador_x_Cambio

    #mantener dentro de bordes al jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736
    jugador(jugador_x, jugador_y)

    #modificar ubicacion del enemigo
    for e in range(cantidad_enemigo):
        enemigo_x[e] += enemigo_x_Cambio[e]

        #fin del juego
        if enemigo_y[e] > 250:
            for k in range(cantidad_enemigo):
                enemigo_y[k] = 1000
                texto_final()
                break

    #mantener dentro de bordes al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_Cambio[e] = 0.1
            enemigo_y[e] += enemigo_y_Cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_Cambio[e] = -0.1
            enemigo_y[e] += enemigo_y_Cambio[e]

        # colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound('golpe.mp3')
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(25, 100)

        enemigo(enemigo_x[e], enemigo_y[e], e)

    #movimiento bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_Cambio





    jugador(jugador_x, jugador_y)

    mostrar_puntaje(texto_x, texto_y)

    #actualizacion
    pygame.display.update()

