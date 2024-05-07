import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
pantalla_ancho, pantalla_alto = 1800, 920
pantalla = pygame.display.set_mode((pantalla_ancho, pantalla_alto))

# Cargar imagen de fondo
fondo = pygame.image.load('./assets/scenary/bg.jpeg')  

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Cargar imagen del personaje
personaje_img = pygame.image.load('./assets/characters/yassuobg.png')
nuevo_ancho = 100  
nuevo_alto = 150  
personaje_img = pygame.transform.scale(personaje_img, (nuevo_ancho, nuevo_alto))



# Cargar imagen del enemigo
enemigo_img = pygame.image.load('./assets/characters/enemy.gif')  
nuevo_ancho_enemigo = 100  
nuevo_alto_enemigo = 140  
enemigo_img = pygame.transform.scale(enemigo_img, (nuevo_ancho_enemigo, nuevo_alto_enemigo))

class Enemigo:
    def __init__(self, x, y, velocidad):
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.sprites = []
        self.current_sprite = 0
        self.animation_time = 0.1
        self.time = 0

        for i in range(7):  # Asume que tienes 7 fotogramas 
            sprite = pygame.image.load(f'./assets/characters/enemy/sprite{i}.png')  # Cambia esto a la ruta de tus sprites
            sprite = pygame.transform.flip(sprite, True, False)  # Voltea la imagen horizontalmente
            sprite = pygame.transform.scale(sprite, (nuevo_ancho_enemigo, nuevo_alto_enemigo))  # Escala la imagen

            self.sprites.append(sprite)

        self.image = self.sprites[self.current_sprite]
        self.mask = pygame.mask.from_surface(self.image) 

    def animate(self, dt):
        self.time += dt
        if self.time >= self.animation_time:
            self.time = 0
            self.current_sprite += 1
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]

    def update(self, dt):
        self.animate(dt)
        self.x -= self.velocidad
        


# Configuración del personaje
x = 50
y_original = pantalla_alto - 150
y = y_original
ancho = 40
alto = 60
velocidad = 5

# Variables de salto y gravedad
esta_saltando = False
salto_cuenta = 10

# Vida del jugador
vida_maxima = 100
vida_actual = vida_maxima

# Dibujar la barra de vida
def dibujar_barra_vida(vida_actual, vida_maxima, x, y, ancho, alto):
    vida_porcentaje = vida_actual / vida_maxima
    pygame.draw.rect(pantalla, ROJO, (x, y, ancho, alto))
    pygame.draw.rect(pantalla, VERDE, (x, y, ancho * vida_porcentaje, alto))

# Pausa
en_pausa = False

# Configuración de texto
pygame.font.init()
fuente = pygame.font.SysFont('Arial', 30)

# Enemigos
enemigos = []
tiempo_ultimo_enemigo = 0
frecuencia_enemigos = 1990  # milisegundos

def mostrar_mensaje_pausa():
    texto = fuente.render('Juego Pausado - Presiona Escape para continuar', True, ROJO)
    texto_rect = texto.get_rect(center=(pantalla_ancho/2, pantalla_alto/2))
    pantalla.blit(texto, texto_rect)
    pygame.display.flip()
    
def agregar_enemigo():
    altura_enemigo = nuevo_alto_enemigo
    y_enemigo = pantalla_alto - altura_enemigo - 1
    enemigos.append(Enemigo(pantalla_ancho, y_enemigo, 3))  


def mover_y_dibujar_enemigos(dt):
    for enemigo in enemigos:
        enemigo.update(dt)
        pantalla.blit(enemigo.image, (enemigo.x, enemigo.y))  # Dibujar la imagen del enemigo

    # Eliminar enemigos que salen de la pantalla
    enemigos[:] = [enemigo for enemigo in enemigos if enemigo.x > 0]

# Bucle del juego
corriendo = True
while corriendo:
    tiempo_actual = pygame.time.get_ticks()
    dt = pygame.time.delay(30) / 1000  
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
            
    pantalla.blit(fondo, (0, 0))

    teclas = pygame.key.get_pressed()

    # Pausar / Reanudar con Escape
    if teclas[pygame.K_ESCAPE]:
        en_pausa = not en_pausa
        pygame.time.wait(300)  # esto Evita múltiples pausas/reanudaciones rápidas

    if not en_pausa:
        # Agregar enemigos
        if tiempo_actual - tiempo_ultimo_enemigo > frecuencia_enemigos:
            agregar_enemigo()
            tiempo_ultimo_enemigo = tiempo_actual
            mover_y_dibujar_enemigos(dt)
        # Movimiento izquierda y derecha
        if teclas[pygame.K_LEFT] and x > velocidad:
            x -= velocidad
        #if teclas[pygame.K_RIGHT] and x < pantalla_ancho - ancho - velocidad:
        #    x += velocidad
        if teclas[pygame.K_RIGHT] and x < pantalla_ancho - personaje_img.get_width() - velocidad:
            x += velocidad
        
        # Dibujar el personaje
        pantalla.blit(personaje_img, (x, y))
        
        # Dibujar la barra de vida del jugador
        dibujar_barra_vida(vida_actual, vida_maxima, 20, 20, 200, 20)
    
         # Actualizar la pantalla
        pygame.display.update()

        # Manejo del salto
        if not esta_saltando:
            if teclas[pygame.K_SPACE]:
                esta_saltando = True
        else:
            if salto_cuenta >= -10:
                negativo = 1
                if salto_cuenta < 0:
                    negativo = -1
                y -= (salto_cuenta ** 2) * 0.5 * negativo
                salto_cuenta -= 1
            else:
                esta_saltando = False
                salto_cuenta = 10

        # Verificar si el personaje está en el suelo
        if y > y_original:
            y = y_original
            esta_saltando = False
            salto_cuenta = 10

        # Mover y dibujar enemigos
        mover_y_dibujar_enemigos(dt) 

        jugador_mask = pygame.mask.from_surface(personaje_img)

        # Comprobar colisiones con los enemigos
        for enemigo in enemigos:
            enemigo_mask = enemigo.mask
            offset_x = enemigo.x - x
            offset_y = enemigo.y - y
            if jugador_mask.overlap(enemigo_mask, (offset_x, offset_y)):
                print("¡Colisión!")
                enemigo.x = x + personaje_img.get_width() 
                vida_actual -= 10  # Reducir la vida del jugador
                if vida_actual < 0:  # Asegurarse de que la vida no sea negativa
                    vida_actual = 0

            else:
                enemigo.x -= enemigo.velocidad
    
    else:
        # Mostrar mensaje de pausa
        mostrar_mensaje_pausa()

    pygame.display.update()

# Salir de Pygame
pygame.quit()
sys.exit()
