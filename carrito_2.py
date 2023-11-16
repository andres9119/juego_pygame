import pygame
import random

pygame.init()
pygame.mixer.init()

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (50, 255, 100)
fuente = pygame.font.Font(None, 36)

ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Esquivar Carritos")


class Menu:
    def __init__(self, opciones):
        self.opciones = opciones
        self.seleccion = 0

    def dibujar(self, pantalla):
        font = pygame.font.Font(None, 36)

        for i, opcion in enumerate(self.opciones):
            texto = font.render(opcion, True, BLANCO)
            x = ANCHO // 2 - texto.get_width() // 2
            y = ALTO // 2 - len(self.opciones) * 20 + i * 40
            pantalla.blit(texto, (x, y))

            if i == self.seleccion:
                pygame.draw.rect(
                    pantalla, ROJO, (x - 10, y, texto.get_width() + 20, texto.get_height()), 3)

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.seleccion = (self.seleccion - 1) % len(self.opciones)
                elif evento.key == pygame.K_DOWN:
                    self.seleccion = (self.seleccion + 1) % len(self.opciones)
                elif evento.key == pygame.K_RETURN:
                    return self.opciones[self.seleccion]

        return None


class Carrito(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert()
        # Configura el color transparente (en este caso, negro)
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Jugador(Carrito):
    def __init__(self):
        super().__init__('imagenes/Player.png', ANCHO // 2, ALTO - 110)
        self.rect = pygame.Rect(self.rect.x, self.rect.y,
                                self.image.get_width(), self.image.get_height())

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += 5

        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()


class Obstaculo(Carrito):
    def __init__(self, x, y):
        super().__init__('imagenes/rivales.png', x, y)

    def update(self):
        self.rect.y += 5
        if self.rect.y > ALTO + 10:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-300, -50)


todos_los_sprites = pygame.sprite.Group()
jugador = Jugador()
todos_los_sprites.add(jugador)

obstaculos = pygame.sprite.Group()
for i in range(8):
    obstaculo = Obstaculo(random.randrange(ANCHO - 50),
                          random.randrange(-300, -50))
    obstaculos.add(obstaculo)
    todos_los_sprites.add(obstaculo)

reloj = pygame.time.Clock()
opciones_menu = ["Iniciar Partida", "Salir"]
menu = Menu(opciones_menu)
puntuacion = 0
tiempo_transcurrido = 0

jugando = True
en_menu = True
pygame.mixer.music.load('sonidos/pista1.mp3')
pygame.mixer.music.play(-1)

perdiste_font = pygame.font.Font(None, 72)  # Fuente para el letrero "Perdiste"
puntuacion_final_font = pygame.font.Font(None, 36)

while jugando:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

    if en_menu:
        # Bucle cuando estás en el menú
        pantalla.fill(NEGRO)
        menu.dibujar(pantalla)
        pygame.display.flip()

        opcion_seleccionada = menu.manejar_eventos(pygame.event.get())
        if opcion_seleccionada:
            if opcion_seleccionada == "Iniciar Partida":
                en_menu = False  # Cambia a la pantalla de juego
            elif opcion_seleccionada == "Salir":
                jugando = False  # Sale del juego

    else:
        # Bucle cuando estás en el juego
        todos_los_sprites.update()

        if pygame.sprite.spritecollide(jugador, obstaculos, False):
            print("¡Perdiste!")
            jugando = False

         # Mostrar el letrero "Perdiste" y la puntuación final
            pantalla.fill(NEGRO)
            texto_perdiste = perdiste_font.render("¡Perdiste!", True, ROJO)
            texto_puntuacion_final = puntuacion_final_font.render(
                f"Puntuación Final: {puntuacion}", True, BLANCO)

            x_perdiste = ANCHO // 2 - texto_perdiste.get_width() // 2
            y_perdiste = ALTO // 2 - 50
            pantalla.blit(texto_perdiste, (x_perdiste, y_perdiste))

            x_puntuacion_final = ANCHO // 2 - texto_puntuacion_final.get_width() // 2
            y_puntuacion_final = ALTO // 2 + 50
            pantalla.blit(texto_puntuacion_final,
                          (x_puntuacion_final, y_puntuacion_final))

            pygame.display.flip()
            pygame.time.delay(3000)  # Esperar 3000 milisegundos (3 segundos)

            # Salir del bucle del juego
            break

        # Incrementar la puntuación cada segundo
        tiempo_transcurrido += reloj.tick(150)
        if tiempo_transcurrido >= 100:  # 1000 milisegundos = 1 segundo
            puntuacion += 1
            tiempo_transcurrido = 0  # Reiniciar el contador de tiempo

        # Mostrar la puntuación en pantalla
        texto_puntuacion = fuente.render(
            f"Puntuación: {puntuacion}", True, BLANCO)
        pantalla.fill(VERDE)
        pantalla.blit(texto_puntuacion, (10, 10))

        pygame.draw.rect(pantalla, ROJO, jugador.rect, 2)
        todos_los_sprites.draw(pantalla)
        pygame.display.flip()

        reloj.tick(120)

pygame.quit()
