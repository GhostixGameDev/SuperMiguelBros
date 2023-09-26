#================================================================
#Contexto para los que visiten mi perfil de Github y se encuentren esto:
#Basicamente es un juego que hice sobre un profesor de mi escuela, para una tarea de Pygame.
#Basically its a simple game made based on my highschool master, for a Pygame homework.



#================================================================
#VERSION INCOMPLETA, FALTA TERMINAR CONTROL DE CAMARA, SPRITES Y DEMAS DETALLES
#================================================================





import pygame, time, configparser
from screeninfo import get_monitors

#================================
#CONFIGURATION
config=configparser.ConfigParser()
config.read("../Config/gameConfig.ini")
firstTime=config.getint("GAME_CONFIG","firstTime")
ancho=config.getint("GAME_CONFIG","screenWidth")
largo=config.getint("GAME_CONFIG","screenHeight")
fullscreen=config.getint("GAME_CONFIG","fullscreen")
language=config.get("GAME_CONFIG","language")
maxFPS=config.getint("GAME_CONFIG","maxFPS")
gameVer=config.get("GAME_CONFIG","gameVer")
box_list=[]

#Funcion que uso mas adelante.
def posinega(numero):
    if numero > 0:
        return 1
    elif numero < 0:
        return -1
    else:
        return 0
def escalado(imagen,scalex,scaley):
    return pygame.transform.scale(imagen,(scalex,scaley))
#Clase Sprite para no andar copiando y pegando el codigo para cada sprite de los item que agregue al juego.
class Sprite(pygame.sprite.Sprite):
    #Constructor de la clase :p
    def __init__(self, image, startx, starty):
        super().__init__()

        self.image = pygame.image.load(image)
        #El rectangulo es como la hitbox de Pygame.
        self.rect = self.image.get_rect()

        self.rect.center = [startx, starty]

    def update(self, camerax, cameray):
        pass

    def draw(self, screen,camerax,cameray):
        #Se hace el blitting del sprite (Referencia Hazielistica 1)
        screen.blit(self.image,(self.rect[0]-camerax,self.rect[1]-cameray))

#CONTROLADOR DE CAMARA
class camera():
    def __init__(self):
        self.camerax=0
        self.cameray=0


    def moveCamera(self,movex,movey):
        self.cameray+=movey
        self.camerax+=movex
        print("Camera moved to: "+str(self.posX())+" "+str(self.posY()))
    def posX(self):
        return self.camerax
    def posY(self):
        return self.cameray

#==========================================================
class Miguel(Sprite):
    #Constructor para dejar el sprite ya definido al crear cada objeto de la clase Miguel.
    def __init__(self, startx, starty,camerax,cameray):
        super().__init__("../assets/sprites/miguel/p1_front.png", startx, starty)
        self.image = escalado(self.image,80,80)
        #El rectangulo es como la hitbox de Pygame.
        self.rect = self.image.get_rect()
        self.camerax = camerax
        self.cameray = cameray
        self.dx=0
        self.dy=0

        self.rect.center = [startx, starty]
        #Definimos la velocidad vertical en 0 para cada vuelta.
        self.vspeed=0
        self.gravity=1
        #Animaciones
        self.spriteParado=self.image
        self.caminata=[escalado(pygame.image.load(f"../assets/sprites/miguel/p1_walk{i:0>2}.png"),80,80) for i in range(1,12)]
        self.animationIndex=0
        self.miraIzq=False
        self.spriteSaltando=escalado(pygame.image.load("../assets/sprites/miguel/p1_jump.png"), 80, 80)
        self.teclaAnt=pygame.key.get_pressed()

    #Comprobación de colisiones.
    def checkCollision(self,x,y,boxes):
        self.rect.move_ip([x,y])
        collide = pygame.sprite.spritecollideany(self,boxes)
        self.rect.move_ip([-x,-y])
        return collide


    #Creamos la animacion de caminata
    def animCaminar(self):
        self.image=self.caminata[self.animationIndex]
        if self.miraIzq:
            self.image=pygame.transform.flip(self.image, True, False)
        #Hacer que la animacion vuelva al principio una vez termine de recorrer el vector de Sprites.
        if self.animationIndex<len(self.caminata)-1:
            self.animationIndex+=1
        else:
            self.animationIndex=0

    #Creamos la animacion del salto.
    def animSalto(self):
        self.image=self.spriteSaltando
        if self.miraIzq:
            self.image=pygame.transform.flip(self.image,True,False)


    def update(self, speed, jumpspeed, minJumpspeed, boxes, Camera,pantalla):
        hspeed=0
        #Comprobar si toca cajas.
        onground = self.checkCollision(0,1,boxes)
        #Comprobar las teclas presionadas
        tecla=pygame.key.get_pressed()
        #No lo hago con Match y Case por que por alguna razon que desconozco, no se mueve con esa estructura.
        #Movimientos.
        if tecla[pygame.K_d]:
            self.miraIzq=False
            self.animCaminar()
            hspeed=speed
            print("DEBUG: Moving to right at speed " + str(hspeed))
        elif tecla[pygame.K_a]:
            self.miraIzq=True
            self.animCaminar()
            hspeed=-speed
            #Chirimbolos mios que hice mientras programaba el DeltaTime para comprobar velocidades.
            #Ademas, queda elegante decir DEBUG jeje.
            print("DEBUG: Moving to left at speed "+str(hspeed))
        else:
            self.image=self.spriteParado
        if tecla[pygame.K_SPACE] and onground:
            self.vspeed=-jumpspeed
            print("DEBUG: Moving to up at speed " + str(self.vspeed))

        #Hacemos el salto variable dependiendo de si se suelta el espacio.
        if self.teclaAnt[pygame.K_SPACE] and not tecla[pygame.K_SPACE]:
            if self.vspeed < -minJumpspeed:
                self.vspeed = -minJumpspeed

        self.teclaAnt=tecla
        #caida
        if self.vspeed<10 and not onground:
            #implementamos la animacion de salto
            self.animSalto()
            self.vspeed+=self.gravity
        #dejar de caer.
        if self.vspeed > 0 and onground:
            self.vspeed = 0
        #Movimiento con las velocidades ya definidas:
        self.move(hspeed,self.vspeed, boxes)
        if not onground:
            print("DEBUG: Falling at speed " + str(self.vspeed))


    #Funcion para el movimiento
    def move(self, x, y, boxes):
        #Se checkea colisiones para saber si mover.
        self.dx=x
        self.dy=y
        #Si choca algo verticalmente, se resta dy hasta no chocarlo, en el juego no se ve el proceso, simplemente parece que choca
        while self.checkCollision(0, self.dy, boxes):
            self.dy -= posinega(self.dy)
        #Lo mismo pero horizontalmente.
        while self.checkCollision(self.dx, self.dy, boxes):
            self.dx -= posinega(self.dx)

        self.rect.move_ip([0, self.dy])
    def getPosx(self):
        print("El rect es:" + str(self.rect[0]))
        return self.dx

    def getPosy(self):
        return self.dy


class Caja(Sprite):
    def __init__(self, startx,starty):
        super().__init__("../assets/sprites/objects/box.png", startx,starty)
        self.image = escalado(self.image, 100, 100)
        # El rectangulo es como la hitbox de Pygame.
        self.rect = self.image.get_rect()
        self.rect.center = [startx, starty]
        self.movex=0
        self.movey=0
    def move(self, x, y):
        self.movex+=x
        self.movey+=y
        self.rect.move_ip([self.movex, self.movey])

class mapa(Caja):
    # Ponemos un piso para el Spawn.
    def __init__(self):
        global box_list
    def create(self,camerax):
        for i in range(camerax - 8000, camerax + 3000, 100):
            box_list.append(Caja(i,720))


    def update(self,camerax,pantalla):
        for i in range(0,len(box_list)):
            box_list[i].draw(pantalla,0,0)
            box_list[i].move(camerax,0)
        if camerax<-1080:
            for i in range(0,round(len(box_list)/2)):
                box_list[i].move(round(camerax),0)
        else:
            for i in range(0,round(len(box_list)/2)):
                box_list[i].move(round(camerax),0)


class Texto:
    def __init__(self,text,font,posx,posy,r,g,b,size):
        self.posx=posx
        self.posy=posy
        self.textFont = pygame.font.SysFont(font, size)
        self.textImage = self.textFont.render(text, True, (r, g, b), (0, 0, 0))
        self.textRect = self.textImage.get_rect()
        self.textRect.centerx = posx
        self.textRect.centery = posy
    def update(self,text,r,g,b,posx,posy):
        self.textImage=self.textFont.render(text,True,(r,g,b),(0,0,0))
        self.textRect = self.textImage.get_rect()
        self.textRect.centerx = posx
        self.textRect.centery = posy
def primaryMonitorSize():
    size=[0,0]
    primary=0
    if len(get_monitors())>1:
        for i in range(0,len(get_monitors())):
            if get_monitors()[i].is_primary:
                primary=i
    size[0]=get_monitors()[primary].width
    size[1]=get_monitors()[primary].height
    return size

def main(gameVer):
    icono=pygame.image.load("../icon.ico")
    jugando = True
    deltaTime = 0
    previousTime = time.time()
    now = 0
    if firstTime:
        pantalla=pygame.display.set_mode(primaryMonitorSize())
    else:
        pantalla = pygame.display.set_mode((ancho, largo))
    anchoMapa=8000
    background=escalado(pygame.image.load("../assets/sprites/background/backgrounds.png"),anchoMapa,720)
    FPSLIMITES = 60
    FPSESPERADOS = 60
    pygame.init()
    pygame.display.set_caption("Super Miguel Bros")
    pygame.display.set_icon(icono)
    clock=pygame.time.Clock()
    Camera=camera()
    fpsControl=Texto("FPS: "+str(clock.get_fps()),"Arial",800,100,200,200,200,20)
    #Creamos el objeto jugador.
    miguel=Miguel(100,200,camera.posX(Camera),camera.posY(Camera))
    lvl=mapa()
    lvl.create(round(Camera.posX()))
    while jugando:
        fpsControl.update("FPS: "+str(clock.get_fps()),200,200,200,800,100)
        #CONTROLES DE CAMARA

        pygame.event.pump()
        #Refrescamos al jugador.
        # Definimos la velocidad multiplicada x DeltaTime (Explicado mas abajo en el Bucle infinito señor Miguel o señor West)
        velocidad=9
        velSalto=21
        velSaltoMin=9
        try:
            # Alternativa en Pygame al Time.DeltaTime de Unity, funcion utilizada para que el juego no dependa de
            # Los fps, debido a que si se corre en una pc lenta, las fisicas cambiarian si depende de los fps.
            # Mucho mejor explicado en el video, me da pereza escribir Miguel, disculpa
            # https://www.youtube.com/watch?v=XuyrHE6GIsc
            #=================================================================================================
            #La formula normal por como programe las fisicas no funciona, pero
            #Si multiplicamos la velocidad * los fps/ los fps nos da siempre la misma velocidad
            #Sin importar los fps.
            miguel.update(velocidad*clock.get_fps()/clock.get_fps(),velSalto*clock.get_fps()/clock.get_fps(),velSaltoMin*clock.get_fps()/clock.get_fps(),box_list, Camera,pantalla)
        except ZeroDivisionError:
            print("Fps are 0, cant update")
        #CONTROLES DE CAMARA
        Camera.moveCamera(miguel.getPosx(),0)
        background_posx=Camera.posX()-1080

        #EVENTOS DE PANTALLA
        #================================================================
        #pantalla.fill((0,0,0))
        pantalla.blit(background, (background_posx,0))
        pantalla.blit(fpsControl.textImage,(fpsControl.posx,fpsControl.posy))
        miguel.draw(pantalla, -40,0)
        lvl.update(round(Camera.posX()),pantalla)
        pygame.display.flip()
        #Definimos los fps limite del juego
        clock.tick(FPSLIMITES)

        #Cierre del juego:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugando=False


if __name__ == '__main__':
    main(gameVer)
