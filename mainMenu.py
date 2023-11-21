import pygame
import sys
import random
import pygame.mixer

from libreria import Boton, obtener_fuente, reproducir_video

# variables globales
ANCHO = 1280
ALTO = 720
ROJO = pygame.Color(255, 0, 0)
AZUL = pygame.Color(0, 154, 255)
BLANCO = pygame.Color(255, 255, 255)
VERDE = pygame.Color(10, 130, 0)
messiX = 50
messiY = 310
suelo = pygame.Rect(0, 450, ANCHO, 0)
oponentes = []
gravedad = 0.80
salta = -15
saltando = False
puntos = 0
velocidadOponentes = 10
tiempoJuego = 0
corriendo = True
enElAire = False
finDelJuego = False
ultimoOponenteX = 0

pygame.mixer.init()
cancion_menu = pygame.mixer.Sound("assets/campeones.wav")  
cancion_juego = pygame.mixer.Sound("assets/entreno.wav")  

# Definición global de cargoImagen
def cargoImagen(ruta, dimensiones):
    imagen = pygame.image.load(ruta)
    return pygame.transform.scale(imagen, dimensiones)
 
def jugar(pantalla):
    # Cargar imágenes de oponentes
    ruta_imagenes_oponentes = ["pics/mbappe.png", "pics/brasil.png", "pics/francia.png", "pics/arabia.png", "pics/australia.png", "pics/croacia.png", "pics/holanda.png", "pics/mexico.png", "pics/polonia.png"]
    imagenes_oponentes = [cargoImagen(ruta, (50, 50)) for ruta in ruta_imagenes_oponentes]

    cancion_menu.stop()
    cancion_juego.play(loops=-1)

    while True:

        def inicializoJuego(): #funcion inicializar juego
            pygame.init()
            surface = pygame.display.set_mode((ANCHO, ALTO))
            clock = pygame.time.Clock()
            font = pygame.font.Font(None, 36)
            return surface, clock, font
        
        def creoOponente(oponentes, ultimoOponenteX):
            indice_imagen = random.randint(0, len(imagenes_oponentes) - 1)
            nueva_posicion_x = max(ultimoOponenteX + 200, ANCHO - 15)
            oponente = {
                "rect": pygame.Rect(ANCHO, 400, 15, 20),
                "imagen": indice_imagen
            }
            oponentes.append(oponente)  # Esta línea debe estar dentro de la función creoOponente
            ultimoOponenteX = nueva_posicion_x

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
                if messiY >= 310:
                    messiY = 310
                    salta = -15
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

            if random.randint(1, 90) == 1:
                creoOponente(oponentes, ultimoOponenteX)

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
            messiY = 310
            suelo = pygame.Rect(0, 450, ANCHO, 15)
            oponentes = []
            gravedad = 0.80
            salta = -15
            saltando = False
            puntos = 0
            velocidadOponentes = 10
            tiempoJuego = 0
            corriendo = True
            enElAire = False
            finDelJuego = False
            ultimoOponenteX = 0  # Agregar esta línea para inicializar la variable      

        
        def victoria_y_reinicio():
            global finDelJuego, corriendo, puntos

            posiciones_raton = pygame.mouse.get_pos()
            finDelJuego = True

            textoWIN = obtener_fuente(40).render("MESSI CONSIGUIÓ LA COPA", True, "#b68f40")
            rectWIN = textoWIN.get_rect(center=(640, 100))
            pantalla.blit(textoWIN, rectWIN)

            reinicio = obtener_fuente(25).render("PULSE R PARA REINICIAR", True, "#b68f40")
            rectReinicio = reinicio.get_rect(center=(640, 200))
            pantalla.blit(reinicio, rectReinicio)

            pygame.display.flip()

            boton_volver = Boton(imagen=None, posicion=(640, 650), 
                                        entrada_texto="BACK TO MENU", fuente=obtener_fuente(50), color_base="WHITE", color_hover="BLACK")

            boton_volver.cambiar_color(posiciones_raton)
            boton_volver.actualizar(pantalla)

            pygame.display.update()

            reproducir_video()

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

        def perder_y_reiniciar(surface):
            global finDelJuego, corriendo, puntos

            finDelJuego = True

            posiciones_raton = pygame.mouse.get_pos()

            textoGameOver = obtener_fuente(90).render("GAME OVER", True, "#b68f40")
            rectGameOver = textoGameOver.get_rect(center=(640, 100))
            pantalla.blit(textoGameOver, rectGameOver)

            reinicio = obtener_fuente(25).render("PULSE R PARA REINICIAR", True, "#b68f40")
            rectReinicio = reinicio.get_rect(center=(640, 200))
            pantalla.blit(reinicio, rectReinicio)

            mensajePuntuacion = obtener_fuente(15).render(f"Puntuación Final: {puntos}", True, "#b68f40")
            x_pos = ANCHO // 2 - mensajePuntuacion.get_width() // 2
            y_pos = 250
            surface.blit(mensajePuntuacion, (x_pos, y_pos))

            pygame.display.flip()

            boton_volver = Boton(imagen=None, posicion=(640, 650),
                                entrada_texto="BACK TO MENU", fuente=obtener_fuente(50), color_base="WHITE", color_hover="BLACK")

            boton_volver.cambiar_color(posiciones_raton)
            boton_volver.actualizar(pantalla)

            pygame.display.update()

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

        def mostrar_instrucciones():
            instrucciones = ["AYUDA A MESSI A GANAR LA COPA","Salta a los rivales","Objetivo: saltar 5"]
            tiempo_inicio = pygame.time.get_ticks()

            fondoCopa = cargoImagen("pics/fondoCopa.jpg",(ANCHO, ALTO))
            pantalla.blit(fondoCopa, (0, 0))

            while pygame.time.get_ticks() - tiempo_inicio < 3000: 
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                y_pos = 100 
                for instr in instrucciones:
                    texto_instr = obtener_fuente(25).render(instr, True, "WHITE")
                    rect_instr = texto_instr.get_rect(center=(900, y_pos))
                    pantalla.blit(texto_instr, rect_instr)
                    y_pos += 75

                pygame.display.flip()

            pygame.time.delay(1000)
            

        def main():
            global messiX, messiY, suelo, oponentes, gravedad, salta, saltando, puntos, velocidadOponentes, tiempoJuego, corriendo, enElAire, finDelJuego, ultimoOponenteX

            surface, clock, font = inicializoJuego()
            pygame.display.set_caption("JUEGO Scaloneta")  

            fondo = cargoImagen("pics/back.png", (ANCHO, ALTO))
            messi = cargoImagen("pics/messiRun.png", (150, 160))
            suelo = pygame.Rect(0, 450, ANCHO, 15)

            mostrar_instrucciones()

            while corriendo:
                tiempoJuego += clock.get_time()

                if manejoEvento():
                    corriendo = False

                manejoSalto()
                moverOponentes()

                if puntos == 5:
                    victoria_y_reinicio()

                if finDelJuego and not puntos == 6:
                    perder_y_reiniciar(surface)


                mostrarPantalla(surface, fondo, messi, suelo, font)

                pygame.display.flip()
                clock.tick(30)

            pygame.quit()
            sys.exit()

        # Iniciar el juego
        if __name__ == "__main__":
            main()

        
        pygame.display.update()

def creditos(pantalla):

    pygame.display.set_caption("OPCIONES Scaloneta")  # título a ventana

    nombres_participantes = ["Martina Siscovich", "Damian Cabral", "Santiago Rodriguez Spina", "Quimey Polimeni","Aliz Tovar", "MESSI TE AMAMOS"] 

    while True:
        posiciones_raton = pygame.mouse.get_pos()

        fondoCreditos = cargoImagen("pics/fondoCreditos.jpg", (ANCHO, ALTO))
        pantalla.blit(fondoCreditos, (0, 0))

        texto_creditos = obtener_fuente(60).render("CREDITS", True, "WHITE")
        rectangulo_creditos = texto_creditos.get_rect(center=(640, 100))
        pantalla.blit(texto_creditos, rectangulo_creditos)

        y_pos = 200 
        for nombre in nombres_participantes:
            texto_nombre = obtener_fuente(30).render(nombre, True, "WHITE")
            rectangulo_nombre = texto_nombre.get_rect(center=(640, y_pos))
            pantalla.blit(texto_nombre, rectangulo_nombre)
            y_pos += 75
       
        boton_volver_creditos = Boton(imagen=None, posicion=(640, 650), 
                                      entrada_texto="BACK TO MENU", fuente=obtener_fuente(50), color_base="WHITE", color_hover="BLACK")

        boton_volver_creditos.cambiar_color(posiciones_raton)
        boton_volver_creditos.actualizar(pantalla)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver_creditos.verificar_entrada(posiciones_raton):
                    return

        pygame.display.update()

def menu_principal():
    pygame.init()
    pantalla = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Menú SCALONETA")

    fondo = pygame.image.load("assets/Background.png")

    while True:
        pantalla.blit(fondo, (0, 0))

        cancion_menu.play(loops=-1)

        posiciones_raton = pygame.mouse.get_pos()

        texto_menu_principal = obtener_fuente(75).render("MESSI Y LA COPA", True, "#b68f40")
        rectangulo_menu_principal = texto_menu_principal.get_rect(center=(640, 100))

        boton_jugar = Boton(imagen=pygame.image.load("assets/Play Rect.png"), posicion=(640, 250), 
                            entrada_texto="PLAY", fuente=obtener_fuente(75), color_base="#d7fcd4", color_hover="White")
        boton_creditos = Boton(imagen=pygame.image.load("assets/Options Rect.png"), posicion=(640, 400), 
                               entrada_texto="CREDITS", fuente=obtener_fuente(75), color_base="#d7fcd4", color_hover="White")
        boton_salir = Boton(imagen=pygame.image.load("assets/Quit Rect.png"), posicion=(640, 550), 
                            entrada_texto="QUIT", fuente=obtener_fuente(75), color_base="#d7fcd4", color_hover="White")

        pantalla.blit(texto_menu_principal, rectangulo_menu_principal)

        for boton in [boton_jugar, boton_creditos, boton_salir]:
            boton.cambiar_color(posiciones_raton)
            boton.actualizar(pantalla)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.verificar_entrada(posiciones_raton):
                    jugar(pantalla)
                if boton_creditos.verificar_entrada(posiciones_raton):
                    creditos(pantalla)
                if boton_salir.verificar_entrada(posiciones_raton):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

menu_principal()
