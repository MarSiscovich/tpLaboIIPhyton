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

# Cargar imagen de fondo
fondo = pygame.image.load("pics/back.png")
fondo = pygame.transform.scale(fondo, (ancho, alto))

# Cargar imagen Messi
messi = pygame.image.load("pics/messiRun.png")
messi = pygame.transform.scale(messi, (90, 100))

# Posicion inicial de Messi
messiX = 50
messiY = 350

# Rectángulos con movimientos uso clase rect si no se mueven uso tupla
# Suelo
suelo = pygame.Rect(0, 450, ancho, 15)

# Rectángulos de oponentes
oponentes = []

# Configuración del juego
gravedad = 0.75 
salta = -10  
saltando = False
puntos = 0
font = pygame.font.Font(None, 36)  # fuente de texto

# Función para crear oponentes
def crear_oponente():
    oponente = pygame.Rect(ancho, 430, 15, 20)
    oponentes.append(oponente)

velocidad_oponentes = 10  # Velocidad inicial de los oponentes
tiempo_juego = 0  # Tiempo transcurrido en el juego

# Bucle principal del juego
clock = pygame.time.Clock()
corriendo = True
en_el_aire = False  # Agrego una bandera para controlar el salto
fin_del_juego = False


while corriendo:
    tiempo_juego += clock.get_time()
    
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
        if messiY >= 350:
            messiY = 350
            salta = -10
            saltando = False
            en_el_aire = False

    # Crear un rectángulo para Messi
    rect_messi = pygame.Rect(messiX, messiY, 90, 100)  # Asumiendo que 180x200 es el tamaño de Messi

    # Mover oponentes
    for oponente in oponentes[:]:
        oponente.x -= velocidad_oponentes
        if oponente.x < 10:
            ultimo_oponente_x = oponente.x
        if rect_messi.colliderect(oponente):
            fin_del_juego = True
        if oponente.right < 0:
            oponentes.remove(oponente)
            puntos += 1

    # Aumentar la velocidad de los oponentes con el tiempo
    if tiempo_juego > 6000:  # Por ejemplo, cada 6 segundos
        velocidad_oponentes += 1  # Aumenta la velocidad
        tiempo_juego = 0  # Restablece el contador de tiempo 

       # Crear nuevos oponentes
    if random.randint(1, 95) == 1:
        crear_oponente()

    if fin_del_juego:
        # Mostrar mensaje de fin de juego
        mensaje_fin = font.render("Fin del Juego - Presiona R para Reiniciar", True, blanco)
        surface.blit(mensaje_fin, (ancho // 2 - mensaje_fin.get_width() // 2, alto // 2 - mensaje_fin.get_height() // 2))
        pygame.display.flip()

    # Esperar acción del jugador
        esperando_accion = True
        while esperando_accion:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    corriendo = False
                    esperando_accion = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        esperando_accion = False
                        fin_del_juego = False
                        # Reiniciar el juego (reiniciar variables, etc.)
                        messiX, messiY = 50, 350  # Restablecer posición de Messi
                        oponentes.clear()  # Limpiar lista de oponentes
                        puntos = 0  # Restablecer puntos
                        saltando = False  # Restablecer estado de salto 

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
