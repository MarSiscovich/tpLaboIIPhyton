import pygame
import sys
import random

# variables globales
ANCHO = 1100
ALTO = 600
ROJO = pygame.Color(255, 0, 0)
AZUL = pygame.Color(0, 154, 255)
BLANCO = pygame.Color(255, 255, 255)
VERDE = pygame.Color(10, 130, 0)
messiX = 50
messiY = 350
suelo = pygame.Rect(0, 450, ANCHO, 15)
oponentes = []
gravedad = 0.75
salta = -10
saltando = False
puntos = 0
velocidadOponentes = 10
tiempoJuego = 0
corriendo = True
enElAire = False
finDelJuego = False
ultimoOponenteX = 0 


def inicializoJuego(): #funcion inicializar juego
    pygame.init()
    surface = pygame.display.set_mode((ANCHO, ALTO))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    return surface, clock, font

def cargoImagen(ruta, dimensiones): #funcion cargar imagen y la dimension
    imagen = pygame.image.load(ruta)
    return pygame.transform.scale(imagen, dimensiones)

def creoOponente(oponentes): #funcion crear oponentes
    oponente = pygame.Rect(ANCHO, 430, 15, 20)
    oponentes.append(oponente)

def manejoEvento(): #funcion manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False

def manejoSalto(): #funcion de salto
    global saltando, enElAire, messiY, salta
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_SPACE] and not saltando:
        saltando = True
        enElAire = True

    if saltando:
        messiY += salta
        salta += gravedad
        if messiY >= 350:
            messiY = 350
            salta = -10
            saltando = False
            enElAire = False

def moverOponentes():  #funcion que mueve los oponentes
    global finDelJuego, puntos, velocidadOponentes, tiempoJuego, ultimoOponenteX
    rectMessi = pygame.Rect(messiX, messiY, 90, 100)

    for oponente in oponentes[:]:
        oponente.x -= velocidadOponentes
        if oponente.x < 10:
            ultimoOponenteX = oponente.x
        if rectMessi.colliderect(oponente):
            finDelJuego = True
        if oponente.right < 0:
            oponentes.remove(oponente)
            puntos += 1

    if tiempoJuego > 6000:
        velocidadOponentes += 1
        tiempoJuego = 0

    if random.randint(1, 95) == 1:
        creoOponente(oponentes)

def mostrarPantalla(surface, fondo, messi, suelo, font): #funcion para mostrar en pantalla
    surface.blit(fondo, (0, 0))
    surface.blit(messi, (messiX, messiY))
    pygame.draw.rect(surface, BLANCO, suelo)
    for oponente in oponentes:
        pygame.draw.rect(surface, ROJO, oponente)

    puntuacion = font.render(f"Puntos: {puntos}", True, BLANCO)
    surface.blit(puntuacion, (10, 560))

def reiniciarJuego():  #funcion reinicio el juego
    global messiX, messiY, suelo, oponentes, gravedad, salta, saltando, puntos, velocidadOponentes, tiempoJuego, corriendo, enElAire, finDelJuego

    messiX = 50
    messiY = 350
    suelo = pygame.Rect(0, 450, ANCHO, 15)
    oponentes = []
    gravedad = 0.75
    salta = -10
    saltando = False
    puntos = 0
    velocidadOponentes = 10
    tiempoJuego = 0
    corriendo = True
    enElAire = False
    finDelJuego = False
    ultimoOponenteX = 0  # Agregar esta línea para inicializar la variable

def main():
    global messiX, messiY, suelo, oponentes, gravedad, salta, saltando, puntos, velocidadOponentes, tiempoJuego, corriendo, enElAire, finDelJuego, ultimoOponenteX

    surface, clock, font = inicializoJuego()
    pygame.display.set_caption("Scaloneta")  # título a ventana

    fondo = cargoImagen("pics/back.png", (ANCHO, ALTO))
    messi = cargoImagen("pics/messiRun.png", (90, 100))

    while corriendo:
        tiempoJuego += clock.get_time()

        if manejoEvento():
            corriendo = False

        manejoSalto()
        moverOponentes()

        if finDelJuego:
            mensajeFin = font.render("Fin del Juego - Presiona R para Reiniciar", True, BLANCO)
            surface.blit(mensajeFin, (ANCHO // 2 - mensajeFin.get_width() // 2, ALTO // 2 - mensajeFin.get_height() // 2))
            pygame.display.flip()

            esperandoAccion = True
            while esperandoAccion:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        corriendo = False
                        esperandoAccion = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            esperandoAccion = False
                            finDelJuego = False
                            reiniciarJuego()

        mostrarPantalla(surface, fondo, messi, suelo, font)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

# Iniciar el juego
if __name__ == "__main__":
    main()

sys.exit()
