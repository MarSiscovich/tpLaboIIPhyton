import pygame
import cv2

from time import sleep

class Boton():
    def __init__(self, imagen, posicion, entrada_texto, fuente, color_base, color_hover):
        self.imagen = imagen
        self.x_pos = posicion[0]
        self.y_pos = posicion[1]
        self.fuente = fuente
        self.color_base, self.color_hover = color_base, color_hover
        self.entrada_texto = entrada_texto
        self.texto = self.fuente.render(self.entrada_texto, True, self.color_base)
        if self.imagen is None:
            self.imagen = self.texto
        self.rectangulo = self.imagen.get_rect(center=(self.x_pos, self.y_pos))
        self.rectangulo_texto = self.texto.get_rect(center=(self.x_pos, self.y_pos))

    def actualizar(self, pantalla):
        if self.imagen is not None:
            pantalla.blit(self.imagen, self.rectangulo)
        pantalla.blit(self.texto, self.rectangulo_texto)

    def verificar_entrada(self, posicion):
        if posicion[0] in range(self.rectangulo.left, self.rectangulo.right) and posicion[1] in range(self.rectangulo.top, self.rectangulo.bottom):
            return True
        return False

    def cambiar_color(self, posicion):
        if posicion[0] in range(self.rectangulo.left, self.rectangulo.right) and posicion[1] in range(self.rectangulo.top, self.rectangulo.bottom):
            self.texto = self.fuente.render(self.entrada_texto, True, self.color_hover)
        else:
            self.texto = self.fuente.render(self.entrada_texto, True, self.color_base)

def obtener_fuente(tamano):
    return pygame.font.Font("assets/font.ttf", tamano)

def reproducir_video():
    cap = cv2.VideoCapture("pics/videoCopa.mp4")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("GANASTE", frame)
        if cv2.waitKey(30) & 0xFF == 27: 
            break

    cap.release()
    cv2.destroyAllWindows()
