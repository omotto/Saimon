import pygame

try:
    import android
except ImportError:
    android = None
try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer
    
import os
import sys
import random

import pygame.gfxdraw

# -----------
# Constantes
# -----------

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

IMG_DIR = "images"
SND_DIR = "sounds"
FNT_DIR = ""

MAX_LEVELS      = 10
MAX_SUB_LEVELS  = 20

# http://www.superflashbros.net/as3sfxr/
# http://gucky.uni-muenster.de/cgi-bin/rgbtab-en

RED     = (255  , 0     , 0     , 255)
GREEN   = (0    , 255   , 0     , 255)
BLUE    = (0    , 0     , 255   , 255)
YELLOW  = (255  , 255   , 0     , 255)
CYAN    = (0    , 255   , 255   , 255)
MAGENTA = (255  , 0     , 255   , 255)
BLACK   = (0    , 0     , 0     , 255)
WHITE   = (255  , 255   , 255   , 255) 

DARK_RED      = (100  , 0     , 0     , 255)
DARK_GREEN    = (0    , 100   , 0     , 255)
DARK_BLUE     = (0    , 0     , 100   , 255)
DARK_YELLOW   = (100  , 100   , 0     , 255)
DARK_CYAN     = (0    , 100   , 100   , 255)
DARK_MAGENTA  = (100  , 0     , 100   , 255)

PURPLE  = (85   , 26    , 139   , 255)
GOLDEN  = (255  , 215   , 0     , 255)

# ------------------------------
# Funciones globales al programa
# ------------------------------

def load_image(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print "Error, no se puede cargar la imagen: ", ruta
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha == True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image

def load_sound(nombre, dir_sonido):
    ruta = os.path.join(dir_sonido, nombre)
    # Intentar cargar el sonido
    try:
        sonido = mixer.Sound(ruta)
    except pygame.error, message:
        print "No se pudo cargar el sonido:", ruta
        sonido = None
    return sonido

def load_text_font(nombre, dir_fuente, tamanyo):
    ruta = os.path.join(dir_fuente, nombre)
    # Intentar cargar el sonido
    try:
        fuente = pygame.font.Font(ruta, tamanyo)
    except:
        print "Error, no se puede cargar la fuente: ", ruta
        sys.exit(1)  
    return fuente

# ------------------------------
# Clases globales al programa
# ------------------------------

# Clase Window

class Window():
    def __init__(self, texto1, texto2, text_color, fuente, tamanyo, sonido, x, y, width, heigh, color1, color2, color1_borde, color2_borde):
        self.texto = texto1
        self.intex = texto2
        self.text_color = text_color
        self.fuente = load_text_font(fuente, FNT_DIR, tamanyo)
        self.sonido = load_sound(sonido, SND_DIR)
        self.x = x
        self.y = y
        self.width = width
        self.heigh = heigh
        self.color = color1
        self.incol = color2
        self.borde = color1_borde
        self.inbor = color2_borde
        
    def invert_color(self):
        temp = self.color
        self.color = self.incol
        self.incol = temp
        temp = self.borde
        self.borde = self.inbor
        self.inbor = temp

    def invert_text(self):
        temp = self.texto
        self.texto = self.intex
        self.intex = temp
                
    def is_touched(self, x, y):        
        if x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.heigh:
            retorno = True
        else:
            retorno = False
        return retorno
    
    def set_text(self, texto):
        self.texto = texto
    
    def plot(self, screen):    
        pygame.gfxdraw.box(screen, (self.x, self.y, self.width, self.heigh), self.color)
        pygame.gfxdraw.rectangle(screen, (self.x-5, self.y-5, self.width+10, self.heigh+10), self.borde)
        size = self.fuente.size(self.texto)
        mensaje = self.fuente.render(self.texto, 1, self.text_color)
        screen.blit(mensaje, (self.x + (self.width / 2) - (size[0] / 2), self.y + (self.heigh / 2) - (size[1] / 2)))
    
    def play_sound(self):
        self.sonido.play()

#def print_screen(screen, color, text_color, texto):
#    fondo = Window("", "", WHITE, "DroidSans-Bold.ttf", 1, "sound0.wav", 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, color, WHITE, WHITE, WHITE)
#    fondo.plot(screen)
#    fuente = load_text_font("DroidSans-Bold.ttf", FNT_DIR, 26)
#    size = fuente.size(texto)
#    mensaje = fuente.render(texto, 1, text_color)
#    screen.blit(mensaje, ((SCREEN_WIDTH / 2) - (size[0] / 2), (SCREEN_HEIGHT / 2) - (size[1] / 2)))
#    pygame.display.flip() # Printamos
#    salir = True
#    while salir: 
#        for event in pygame.event.get():
#            # When the touchscreen is pressed, change the color to green.
#            if event.type == pygame.MOUSEBUTTONDOWN:
#                salir = False

def question_screen(screen, color, text_color, texto, max_length):
    # printamos pantalla
    fondo = Window("", "", WHITE, "DroidSans-Bold.ttf", 1, "sound0.wav", 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, color, WHITE, WHITE, WHITE)
    fondo.plot(screen)
    fuente = load_text_font("DroidSans-Bold.ttf", FNT_DIR, 26)
    size = fuente.size(texto)
    mensaje = fuente.render(texto, 1, text_color)
    screen.blit(mensaje, ((SCREEN_WIDTH / 2) - (size[0] / 2), (SCREEN_HEIGHT / 2) - ((size[1] / 2) * 3) ))
    # Inicializamos variables
    y = (SCREEN_HEIGHT / 2) + (size[1])
    x = (SCREEN_WIDTH / 2) - (size[1] * (max_length-1) / 2)
    contador = 0
    text = [0, 0, 0, 0]
    salir = True
    pygame.gfxdraw.rectangle(screen, (x - 5, y - 5, size[1] * (max_length - 1), 10 + size[1]), WHITE)
    pygame.display.flip() # Printamos 
    if android: android.show_keyboard()
    while salir: 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    if contador < max_length:
                        text[contador] = 0
                        contador = contador + 1
                elif event.key == pygame.K_1:
                    if contador < max_length:
                        text[contador] = 1
                        contador = contador + 1                    
                elif event.key == pygame.K_2:
                    if contador < max_length:
                        text[contador] = 2
                        contador = contador + 1                    
                elif event.key == pygame.K_3:
                    if contador < max_length:
                        text[contador] = 3
                        contador = contador + 1                    
                elif event.key == pygame.K_4:
                    if contador < max_length:
                        text[contador] = 4
                        contador = contador + 1                    
                elif event.key == pygame.K_5:
                    if contador < max_length:
                        text[contador] = 5
                        contador = contador + 1                    
                elif event.key == pygame.K_6:
                    if contador < max_length:
                        text[contador] = 6
                        contador = contador + 1                    
                elif event.key == pygame.K_7:                    
                    if contador < max_length:
                        text[contador] = 7
                        contador = contador + 1                    
                elif event.key == pygame.K_8:
                    if contador < max_length:
                        text[contador] = 8
                        contador = contador + 1                    
                elif event.key == pygame.K_9:
                    if contador < max_length:
                        text[contador] = 9
                        contador = contador + 1
                elif event.key == pygame.K_BACKSPACE:
                    if contador > 0:
                        contador = contador - 1
                elif event.key == pygame.K_RETURN:
                    salir = False
                pygame.gfxdraw.box(screen, (x, y, size[0] * 0.6, size[1]), color)
                if (contador == 1): mensaje_text = fuente.render("{0}".format(text[0]), 1, WHITE)
                if (contador == 2): mensaje_text = fuente.render("{0} {1}".format(text[0], text[1]), 1, WHITE)
                if (contador == 3): mensaje_text = fuente.render("{0} {1} {2}".format(text[0], text[1], text[2]), 1, WHITE)
                if (contador == 4): mensaje_text = fuente.render("{0} {1} {2} {3}".format(text[0], text[1], text[2], text[3]), 1, WHITE)
                if (contador > 0): screen.blit(mensaje_text, (x, y))
                pygame.display.flip() # Printamos
                
    if android: android.hide_keyboard()
    return text
                    
def game(screen, sonido, code):
    # Declaramos los objetos
    error = Window("YOU FAIL", "", WHITE, "DroidSans-Bold.ttf", 76, "sound0.wav", SCREEN_WIDTH / 2 - 220, SCREEN_HEIGHT / 2 - 50, 440, 100, RED, DARK_RED, WHITE, WHITE)
    fondo = Window("", "", WHITE, "DroidSans-Bold.ttf", 1, "sound0.wav", 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, WHITE, WHITE)
    windows = [ Window("", "", GREEN, "DroidSans-Bold.ttf", 22, "sound1.wav", 10, 50, 220, 220, RED, DARK_RED, WHITE, WHITE),
                Window("", "", YELLOW, "DroidSans-Bold.ttf", 22, "sound2.wav", 250, 50, 220, 220, GREEN, DARK_GREEN, WHITE, WHITE),
                Window("", "", CYAN, "DroidSans-Bold.ttf", 22, "sound3.wav", 10, 290, 220, 220, YELLOW, DARK_YELLOW, WHITE, WHITE),
                Window("", "", MAGENTA, "DroidSans-Bold.ttf", 22, "sound4.wav", 250, 290, 220, 220, CYAN, DARK_CYAN, WHITE, WHITE),
                Window("", "", CYAN, "DroidSans-Bold.ttf", 22, "sound5.wav", 10, 530, 220, 220, MAGENTA, DARK_MAGENTA, WHITE, WHITE),
                Window("", "", MAGENTA, "DroidSans-Bold.ttf", 22, "sound6.wav", 250, 530, 220, 220, BLUE, DARK_BLUE, WHITE, WHITE) ]
    
    # Printamos
    fondo.plot(screen)
    for contador in range(6):           
        windows[contador].plot(screen)

    pygame.display.flip() # Printamos
    
    fuente = load_text_font("DroidSans-Bold.ttf", FNT_DIR, 26)
    
    # Generamos un array bidimensional de valores alaeatorios del 1 al 6
    valores = [[random.randint(0, 5) for i in range(MAX_SUB_LEVELS)] for i in range(MAX_LEVELS)]
    
    max_sublevels = [10, 12, 12, 14, 14, 16, 16, 18, 18, 20]
    
    # Inicializamos valores globales del juego
    codes = [[4,9,3,0],[3,8,5,6],[4,9,5,1],[1,4,5,6],[0,4,5,6],[6,4,6,2],[7,8,5,6],[3,1,7,4],[9,4,2,2],[3,8,5,7]]
    level = 0
    for i in range(MAX_LEVELS):    
        if (codes[i][0] == code[0]) and (codes[i][1] == code[1]) and (codes[i][2] == code[2]) and (codes[i][3] == code[3]):
            level = i
    exit_game = True
    sublevel = 0
    while exit_game: 
        pygame.gfxdraw.box(screen, (0, 0, SCREEN_WIDTH, 40), BLACK)
        pygame.gfxdraw.box(screen, (0, 755, SCREEN_WIDTH, 40), BLACK)
        mensaje_level = fuente.render("Level {0}".format(level), 1, WHITE)
        screen.blit(mensaje_level, (10, 10))
        mensaje_stage = fuente.render("Stage {0}".format(sublevel), 1, WHITE)
        screen.blit(mensaje_stage, (250, 10))
        mensaje_code = fuente.render("Level Code : {0} {1} {2} {3}".format(codes[level][0], codes[level][1], codes[level][2], codes[level][3]), 1, WHITE)
        screen.blit(mensaje_code, (120, 760))
        pygame.display.flip()
        pygame.time.wait(1000)
        # Mostramos la siguiente combinacion
        for i in range(sublevel+1):
            pygame.time.wait(600 - ((level+2) * 40) - ((sublevel+1) * 5))
            windows[valores[level][i]].invert_color()
            windows[valores[level][i]].plot(screen)
            pygame.display.flip()  
            if sonido == True: windows[valores[level][i]].play_sound()            
            pygame.time.wait(500 - ((level+2) * 20) - ((sublevel+1) * 2))
            windows[valores[level][i]].invert_color()
            windows[valores[level][i]].plot(screen)
            pygame.display.flip()    
        # Ahora nos toca jugar
        salir = True
        indice = 0
        while salir:
            for event in pygame.event.get():
                # When the touchscreen is pressed, change the color to green.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posicion = pygame.mouse.get_pos()
                    touched = 7
                    for i in range(6):
                        if windows[i].is_touched(posicion[0], posicion[1]) == True: 
                            touched = i
                    if touched != 7: # Has dado a un pulsador
                        windows[touched].invert_color()
                        windows[touched].plot(screen)
                        pygame.display.flip()  
                        if sonido == True: windows[touched].play_sound()            
                        pygame.time.wait(200)
                        windows[touched].invert_color()
                        windows[touched].plot(screen)
                        pygame.display.flip()    
                        if touched != valores[level][indice]:# Te has equivocado de boton
                            exit_game = False
                            salir = False
#                            fondo.invert_color()
#                            fondo.plot(screen)
#                            if sonido == True: fondo.play_sound()
#                            pygame.display.flip()
                            touched = 7 #indicamos en la salida que es por error
                        else: 
                            indice = indice + 1
                            if indice == (sublevel + 1):
                                salir = False
                elif event.type == pygame.QUIT:
                    sys.exit()
        # Siguiente nivel
        sublevel = sublevel + 1
        if sublevel == max_sublevels[level]: #MAX_SUB_LEVELS
            level = level + 1
            sublevel = 0
        if level == MAX_LEVELS:
            exit_game = False
    if touched == 7:
        if android: 
            android.vibrate(1)
        error.plot(screen)
        pygame.display.flip()
        salir2 = True
        while salir2:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posicion = pygame.mouse.get_pos()
                    if error.is_touched(posicion[0], posicion[1]) == True:
                        error.invert_color()
                        error.plot(screen)
                        pygame.display.flip()                          
                        if sonido == True: fondo.play_sound()
                        pygame.time.wait(200)
                        error.invert_color()
                        error.plot(screen)
                        pygame.display.flip()                          
                        salir2 = False
                elif event.type == pygame.QUIT:
                    sys.exit()
                
def main():
    pygame.init()
    
    if android: android.init()	
    
    mixer.init()   
 
    # Creamos la ventana y le ponemos un titulo (valido para windows)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("SAIMON GAME")

    # cramos el objeto texto (titulo del juego)
    fuente = load_text_font("DroidSans-Bold.ttf", FNT_DIR, 76)
    size = fuente.size("SAIMON")
    print_text = fuente.render("SAIMON", 1, GOLDEN)

    # creamos los objetos del juego
    
    fondo = Window("", "", WHITE, "DroidSans-Bold.ttf", 1, "sound0.wav", 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, WHITE, WHITE)
    
    start   = Window("START", "", GREEN, "DroidSans-Bold.ttf", 22, "sound0.wav", 10, 150, 220, 220, RED, DARK_RED, WHITE, WHITE)
    sound   = Window("SOUND ON", "SOUND OFF", YELLOW, "DroidSans-Bold.ttf", 22, "sound0.wav", 250, 150, 220, 220, GREEN, DARK_GREEN, WHITE, WHITE)
    exit    = Window("EXIT", "", CYAN, "DroidSans-Bold.ttf", 22, "sound0.wav", 10, 430, 220, 220, YELLOW, DARK_YELLOW, WHITE, WHITE)
    level   = Window("CODE", "", MAGENTA, "DroidSans-Bold.ttf", 22, "sound0.wav", 250, 430, 220, 220, CYAN, DARK_CYAN, WHITE, WHITE)
    
    fondo.plot(screen)
    start.plot(screen)
    sound.plot(screen)
    exit.plot(screen)
    level.plot(screen)
    
    # pintamos texto
    screen.blit(print_text, ((SCREEN_WIDTH / 2) - (size[0] / 2), 20))

    # Creamos el objeto clock de la clase time.Clock
    clock = pygame.time.Clock()	

    salir = True
    sonido = True
    code = [0, 0, 0, 0]
    while salir: 
        pygame.display.flip() # Printamos   
        if android: 
            if android.check_pause(): 
                android.wait_for_resume()
        
        clock.tick(60)    
        
        for event in pygame.event.get():
            # When the touchscreen is pressed, change the color to green.
            if event.type == pygame.MOUSEBUTTONDOWN:
                posicion = pygame.mouse.get_pos()
                if start.is_touched(posicion[0], posicion[1]) == True:
                    start.invert_color()
                    start.plot(screen)
                    if sonido == True: start.play_sound()
                    pygame.display.flip()  
                    pygame.time.wait(200)
                    start.invert_color()
                    start.plot(screen)
                    pygame.display.flip()        
                    game(screen, sonido, code)
                    fondo.plot(screen)
                    start.plot(screen)
                    sound.plot(screen)
                    exit.plot(screen)
                    level.plot(screen)
                    screen.blit(print_text, ((SCREEN_WIDTH / 2) - (size[0] / 2), 20))
                    pygame.display.flip()
                elif sound.is_touched(posicion[0], posicion[1]) == True:
                    sound.invert_color()
                    sound.invert_text()
                    if sonido == True: sound.play_sound()
                    sound.plot(screen)
                    pygame.display.flip()  
                    pygame.time.wait(200)
                    sound.invert_color()
                    sound.plot(screen)
                    sonido = not sonido
                    pygame.display.flip()
                elif level.is_touched(posicion[0], posicion[1]) == True:
                    level.invert_color()
                    level.plot(screen)
                    if sonido == True: level.play_sound()
                    pygame.display.flip()  
                    pygame.time.wait(200)
                    level.invert_color()
                    level.plot(screen) 
                    pygame.display.flip()
                    code = question_screen(screen, PURPLE, GREEN, "LEVEL CODE", 4)
                    fondo.plot(screen)
                    start.plot(screen)
                    sound.plot(screen)
                    exit.plot(screen)
                    level.plot(screen)
                    screen.blit(print_text, ((SCREEN_WIDTH / 2) - (size[0] / 2), 20))
                    pygame.display.flip()                    
                elif exit.is_touched(posicion[0], posicion[1]) == True:                    
                    exit.invert_color()
                    exit.plot(screen)
                    if sonido == True: exit.play_sound()
                    pygame.display.flip()  
                    pygame.time.wait(200)
                    exit.invert_color()
                    exit.plot(screen)                    
                    pygame.display.flip()        
                    salir = False
            elif event.type == pygame.QUIT:
                sys.exit()
        
        
if __name__ == "__main__":
    main()
