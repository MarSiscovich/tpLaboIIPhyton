import pygame
import sys
import random

from libreria import Boton, obtener_fuente

# variables globales
ANCHO = 1280
ALTO = 720
ROJO = pygame.Color(255, 0, 0)
AZUL = pygame.Color(0, 154, 255)
BLANCO = pygame.Color(255, 255, 255)
VERDE = pygame.Color(10, 130, 0)
messiX = 50
messiY = 350
suelo = pygame.Rect(0, 450, ANCHO, 0)
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
# Definición global de cargoImagen
def cargoImagen(ruta, dimensiones):
    imagen = pygame.image.load(ruta)
    return pygame.transform.scale(imagen, dimensiones)
 
def jugar(pantalla):
    # Cargar imágenes de oponentes
    ruta_imagenes_oponentes = ["pics/mbappe.png", "pics/brasil.png", "pics/francia.png"]
    imagenes_oponentes = [cargoImagen(ruta, (50, 50)) for ruta in ruta_imagenes_oponentes]

    while True:
        # Resto de tu código
        def inicializoJuego(): #funcion inicializar juego
            pygame.init()
            surface = pygame.display.set_mode((ANCHO, ALTO))
            clock = pygame.time.Clock()
            font = pygame.font.Font(None, 36)
            return surface, clock, font
        
        def creoOponente(oponentes):
            indice_imagen = random.randint(0, len(imagenes_oponentes) - 1)
            oponente = {
                "rect": pygame.Rect(ANCHO, 430, 15, 20),
                "imagen": indice_imagen
            }
            oponentes.append(oponente)  # Esta línea debe estar dentro de la función creoOponente

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

        def moverOponentes():  # Función que mueve los oponentes
            global finDelJuego, puntos, velocidadOponentes, tiempoJuego, ultimoOponenteX
            rectMessi = pygame.Rect(messiX, messiY, 90, 100)

            for oponente in oponentes[:]:
                oponente['rect'].x -= velocidadOponentes  # Acceder al rectángulo del oponente
                if oponente['rect'].x < 10:
                    ultimoOponenteX = oponente['rect'].x
                if rectMessi.colliderect(oponente['rect']):  # Acceder al rectángulo para la colisión
                    finDelJuego = True
                if oponente['rect'].right < 0:  # Acceder al rectángulo para verificar la posición
                    oponentes.remove(oponente)
                    puntos += 1

            if tiempoJuego > 6000:
                velocidadOponentes += 1
                tiempoJuego = 0

            if random.randint(1, 95) == 1:
                creoOponente(oponentes)

        def mostrarPantalla(surface, fondo, messi, suelo, font):
            surface.blit(fondo, (0, 0))
            surface.blit(messi, (messiX, messiY))
            pygame.draw.rect(surface, BLANCO, suelo)
            for oponente in oponentes:
                imagen_oponente = imagenes_oponentes[oponente["imagen"]]
                surface.blit(imagen_oponente, oponente["rect"].topleft)

            puntuacion = font.render(f"Puntos: {puntos}", True, BLANCO)
            surface.blit(puntuacion, (10, 675))

        def reiniciarJuego():  #funcion reinicio el juego
            global messiX, messiY, suelo, oponentes, gravedad, salta, saltando, puntos, velocidadOponentes, tiempoJuego, corriendo, enElAire, finDelJuego,ultimoOponenteX

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
            pygame.display.set_caption("JUEGO Scaloneta")  # título a ventana

            fondo = cargoImagen("pics/back.png", (ANCHO, ALTO))
            messi = cargoImagen("pics/messiRun.png", (90, 100))

            while corriendo:
                tiempoJuego += clock.get_time()

                if manejoEvento():
                    corriendo = False

                manejoSalto()
                moverOponentes()

                if finDelJuego:
                    posiciones_raton = pygame.mouse.get_pos()
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

        
        pygame.display.update()

def opciones(pantalla):
    while True:
        posiciones_raton = pygame.mouse.get_pos()

        pantalla.fill("white")

        texto_opciones = obtener_fuente(45).render("This is the OPTIONS screen.", True, "Black")
        rectangulo_opciones = texto_opciones.get_rect(center=(640, 260))
        pantalla.blit(texto_opciones, rectangulo_opciones)

        boton_volver_opciones = Boton(imagen=None, posicion=(640, 460), 
                                      entrada_texto="BACK", fuente=obtener_fuente(75), color_base="Black", color_hover="Green")

        boton_volver_opciones.cambiar_color(posiciones_raton)
        boton_volver_opciones.actualizar(pantalla)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver_opciones.verificar_entrada(posiciones_raton):
                    return 

        pygame.display.update()

def menu_principal():
    pygame.init()
    pantalla = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Menú SCALONETA")

    fondo = pygame.image.load("assets/Background.png")

    while True:
        pantalla.blit(fondo, (0, 0))

        posiciones_raton = pygame.mouse.get_pos()

        texto_menu_principal = obtener_fuente(75).render("MESSI Y LA COPA", True, "#b68f40")
        rectangulo_menu_principal = texto_menu_principal.get_rect(center=(640, 100))

        boton_jugar = Boton(imagen=pygame.image.load("assets/Play Rect.png"), posicion=(640, 250), 
                            entrada_texto="PLAY", fuente=obtener_fuente(75), color_base="#d7fcd4", color_hover="White")
        boton_opciones = Boton(imagen=pygame.image.load("assets/Options Rect.png"), posicion=(640, 400), 
                               entrada_texto="OPTIONS", fuente=obtener_fuente(75), color_base="#d7fcd4", color_hover="White")
        boton_salir = Boton(imagen=pygame.image.load("assets/Quit Rect.png"), posicion=(640, 550), 
                            entrada_texto="QUIT", fuente=obtener_fuente(75), color_base="#d7fcd4", color_hover="White")

        pantalla.blit(texto_menu_principal, rectangulo_menu_principal)

        for boton in [boton_jugar, boton_opciones, boton_salir]:
            boton.cambiar_color(posiciones_raton)
            boton.actualizar(pantalla)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.verificar_entrada(posiciones_raton):
                    jugar(pantalla)
                if boton_opciones.verificar_entrada(posiciones_raton):
                    opciones(pantalla)
                if boton_salir.verificar_entrada(posiciones_raton):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

menu_principal()

