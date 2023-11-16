import pygame
import sys
import random

# Inicializo pygame
pygame.init()

# Creación de ventana
ancho = 1100
alto = 600
surface = pygame.display.set_mode((ancho, alto))  # ventana
pygame.display.set_caption("Scaloneta")  # titulo a ventana

# RGB agrego los colores que necesite
rojo = pygame.Color(255, 0, 0)
azul = pygame.Color(0, 154, 255)
blanco = pygame.Color(255, 255, 255)
verde = pygame.Color(10, 130, 0)


# Cargar imagen Messi
messi = pygame.image.load("pics/messiRun.png")
messi = pygame.transform.scale(messi, (180, 200))

# Posicion inicial de Messi
messiX = 50
messiY = 270

# Rectángulos con movimientos uso clase rect si no se mueven uso tupla
# Suelo
suelo = pygame.Rect(0, 450, ancho, 15)

# Rectángulos de oponentes
oponentes = []

# Configuración del juego
gravedad = 1.5
salta = -20
saltando = False
puntos = 0
font = pygame.font.Font(None, 36)  # fuente de texto

# Función para crear oponentes
def crear_oponente():
    oponente = pygame.Rect(ancho, 430, 15, 20)
    oponentes.append(oponente)

# Bucle principal del juego
clock = pygame.time.Clock()
corriendo = True
en_el_aire = False  # Agrego una bandera para controlar el salto

while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False

    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_SPACE] and not saltando:
        saltando = True
        en_el_aire = True

    if saltando:
        messiY += salta
        salta += gravedad
        if messiY >= 270:
            messiY = 270
            salta = -20
            saltando = False
            en_el_aire = False

    # Mover oponentes
    for oponente in oponentes[:]:
        oponente.x -= 5
        if oponente.colliderect(messiX, messiY, 25, 40):
            corriendo = False
        if oponente.right < 0:
            oponentes.remove(oponente)
            puntos += 1

    # Crear nuevos oponentes
    if random.randint(1, 95) == 1:
        crear_oponente()

    surface.blit(fondo, (0, 0))
    surface.blit(messi, (messiX, messiY))
    pygame.draw.rect(surface, blanco, suelo)
    for oponente in oponentes:
        pygame.draw.rect(surface, rojo, oponente)

    # Mostrar puntuación
    puntuacion = font.render(f"Puntos: {puntos}", True, blanco)
    surface.blit(puntuacion, (10, 560))

    pygame.display.flip()
    clock.tick(30)  # la ejecución del juego a un máximo de 30 FPS

pygame.quit()
sys.exit()
