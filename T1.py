import math
import random
import re
import time

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

# Variáveis de controle da câmera (pan e viewport)
left = -1
right = 1
top = 1
bottom = -1
panX = 0
panY = 0

class Entity():
    def __init__(self, x, y, c, frames = None):
        self.x = x
        self.y = y
        self.c = c
        self.frames = [] if frames is None else list(frames)

        #usado para bounding box
        self.minX  = 0
        self.minY  = 0 
        self.maxX  = 0 
        self.maxY  = 0 


def calculaXCurvado (x,legLength,side): #1 para perna direta, 0 para perna esquerda
    if frameSignal == 0: #metade da animacao
        if side==1:
            ang = math.radians(277)
            return (legLength*math.cos(ang))/1000 
        elif side ==0:
            ang = math.radians(263)
            return (legLength*math.cos(ang))/1000 
        else:
            raise ValueError("Wrong side value")
    elif frameSignal == 1:
        if side==1:
            ang = math.radians(285)
            return (legLength*math.cos(ang))/1000 
        elif side ==0:
            ang = math.radians(255)
            return (legLength*math.cos(ang))/1000 
        else:
            raise ValueError("Wrong side value")
    else : raise ValueError("Wrong frameSignal value")

    
def calculaYCurvado (y,legLength,side): #1 para perna direta, 0 para perna esquerda
    if frameSignal == 0: #metade da animacao    
        if side==1:
            ang = math.radians(307)
            return (legLength*math.sin(ang))/1000 
        elif side ==0:
            ang = math.radians(233)
            return (legLength*math.sin(ang))/1000 
        else:
            raise ValueError("Wrong side value")
    elif frameSignal == 1: 
        if side==1:
            ang = math.radians(315)
            return (legLength*math.sin(ang))/1000 
        elif side ==0:
            ang = math.radians(225)
            return (legLength*math.sin(ang))/1000 
        else:
            raise ValueError("Wrong side value")
    else: raise ValueError("Wrong frameSignal value")

def CollisionSystem (xAux,yAux,ent):
    if (ent.x+xAux) > ent.maxX: ent.maxX = ent.x+xAux
    if (ent.x+xAux) < ent.minX: ent.minX = ent.x+xAux
    if (ent.y+yAux) > ent.maxY: ent.maxY = ent.y+yAux
    if (ent.y+yAux) < ent.minY: ent.minY = ent.y+yAux

    for entAux in entityList:
        #if ent.maxX > entAux.minX and ent.maxY > ent.minY: ColorSwitcher(ent,entAux)
        #if ent.maxX > entAux.minX and ent.minY < ent.maxY: ColorSwitcher(ent,entAux)
        #if ent.minX < entAux.maxX and ent.minY < ent.maxY: ColorSwitcher(ent,entAux)
        #if ent.minX < entAux.maxX and ent.maxY > ent.minY: ColorSwitcher(ent,entAux)
        if ent.minX <= entAux.maxX and ent.maxX >= entAux.minX: ColorSwitcher(ent,entAux)
        if ent.minY <= entAux.maxY and ent.maxY >= entAux.minY: ColorSwitcher(ent,entAux)

def ColorSwitcher (ent1,ent2): ##arrumar ainda
    colors = [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1)]
    ent1.c = colors [random.randint(0,5)]
    while ent1.c == ent2.c: ent1.c = colors [random.randint(0,5)]

#mudar algoritmo para calcular antes de desenhar

def desenhaPerna(x,y,xAux,yAux,ent):
    glPushMatrix()
    glLoadIdentity()

    glTranslatef(x / 1000.0, y / 1000.0, 0.0)
    glLineWidth (5)
    #CollisionSystem (xAux,yAux,ent)

    r, g, b = ent.c
    glColor3f(r,g,b)

    glBegin(GL_LINES)
    glVertex2f(0,0)
    glVertex2f(0+xAux,0+yAux)
    glEnd()
    glPopMatrix()

def desenhaTorso (x,y,headY,ent):
    glPushMatrix()
    glLoadIdentity()

    glTranslatef(x / 1000.0, y / 1000.0, 0.0)
    r, g, b = ent.c
    glColor3f(r,g,b) 
    glLineWidth (5)
    
    glBegin(GL_LINES)
    glVertex2f(0,0)
    glVertex2f(0,headY)
    glEnd()
    glPopMatrix()

def desenhaBracos (x,y,headY,signal,ent):
    glPushMatrix()
    glLoadIdentity()

    glTranslatef(x / 1000.0, y / 1000.0, 0.0)
    r, g, b = ent.c
    glColor3f(r,g,b) 
    glLineWidth (5)

    armLength = 50
    
    glBegin(GL_LINES)
    glVertex2f(0,headY)
    xAux = calculaXCurvado(x,armLength,signal)
    yAux = calculaYCurvado(y,armLength,signal)
    varA = 20/1000
    glVertex2f(0+xAux,(headY-varA)+yAux)
    glEnd()
    glPopMatrix()

def desenhaCabeca (x,y,headY,ent):
    glPushMatrix()
    glLoadIdentity()

    glTranslatef(x / 1000.0, y / 1000.0, 0.0)
    r, g, b = ent.c
    glColor3f(r,g,b) 
    glPointSize(20)

    glBegin(GL_POINTS)
    glVertex2f(0,headY)
    glEnd()
    glPopMatrix()


def desenhaEntity(ent):
    if (ent.x is None or ent.y is None): return
    
    x = ent.x
    y = ent.y

    CollisionSystem(ent)

    #perna esquerda
    desenhaPerna(x,y,0,ent)
    #perna esquerda
    desenhaPerna(x,y,1,ent)
    
    bodyLength = 50

    headY = (bodyLength/1000)

    #torso
    desenhaTorso(x,y,headY,ent)
    #braco esquerda
    desenhaBracos(x,y,headY,0,ent)
    #braco direita
    desenhaBracos(x,y,headY,1,ent)

    desenhaCabeca(x,y,headY,ent)

def desenhaEntity2(ent):
    if (ent.x is None or ent.y is None): return
    x = ent.x
    y = ent.y

    #CollisionSystem(ent)

    #perna esquerda
    legLength = 50

    xAux = calculaXCurvado(x,legLength,0) #ultimo é signal, mudar pra 1
    yAux = calculaYCurvado(y,legLength,0)
    desenhaPerna(x,y,0,ent)
    #perna esquerda
    desenhaPerna(x,y,xAux,yAux,ent)
    
    bodyLength = 50

    headY = (bodyLength/1000)

    #torso
    desenhaTorso(x,y,headY,ent)
    #braco esquerda
    desenhaBracos(x,y,headY,0,ent)
    #braco direita
    desenhaBracos(x,y,headY,1,ent)

    desenhaCabeca(x,y,headY,ent)

def Reader():
    with open ("Paths_D_Modified.txt") as f:
        while True:
            entityData = f.readline()
            if entityData == "":
                break
            parse_line(entityData)
    f.close()

triple_re = re.compile(r"\((\d+),(\d+),(\d+)\)")

entityList = [] #.append para adicionar

def parse_line(line: str): #feito em ia
    line = line.strip()
    size_str, rest = line.split(None, 1)  # split at first whitespace
    size = int(size_str)
    localFrames = []
    localFrames.append((0,None,None))
    frame = 1

    for a, b, c in triple_re.findall(rest):
        while (int(c)!=frame):
            localFrames.append((frame,None,None))
            frame +=1
            continue
        localFrames.append((int(c), int(a), int(b))) #frame, x, y 
        frame +=1
    
    
    while (frame<=MAXFRAME): 
        localFrames.append((frame,None,None))
        frame+=1
    
    ent = Entity(localFrames[0][1],localFrames[0][2],(1,1,1),localFrames)
    entityList.append(ent)

#frames globais
currentFrame = 1
MAXFRAME = 375
frameSignal = 0 #0 ou 1
TIME_MS = 100 #1 fps, 1000 ms;10 fps, 100ms;100 fps, 10ms; 20fps, 50ms

def Display():
    glClear(GL_COLOR_BUFFER_BIT) #ia
    glMatrixMode(GL_MODELVIEW) #garantir modelview indentity por frame e evita acumular transformacoes antigas
    glLoadIdentity() 
    for ent in entityList: 
            if currentFrame < len(ent.frames) and len(ent.frames[currentFrame]) > 2: #garante que tem todos os frame e confirma se tem oq mostrar ou nao
                ent.x = ent.frames[currentFrame][1]
                ent.y = ent.frames[currentFrame][2]
                desenhaEntity(ent)
    # usando double-buffer, troque buffers
    glutSwapBuffers() #ao inves de glFlush(), usando quando so um buffer

def Timer(value):
    global currentFrame, frameSignal
    print ("frame: "+str(currentFrame)) ##
    if frameSignal == 0:
        frameSignal = 1
    else:
        frameSignal = 0
        if (currentFrame <= MAXFRAME):
            currentFrame+=1
        elif (currentFrame == 376): currentFrame = 1
    glutTimerFunc(TIME_MS,Timer, 0) #50ms, func Timer, 0 = nada
    glutPostRedisplay() #redesenho


# Inicializa variáveis e configurações de viewport
def Inicializa():
    global left, right, top, bottom, panX, panY

    Reader()
    # cor de fundo
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glMatrixMode(GL_PROJECTION)
    left = -1
    right = 0.1
    top = 0.1
    bottom = -1
    panX = 1 
    panY = 1 
    gluOrtho2D(left + panX, right + panX, bottom + panY, top + panY)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    glutInit(sys.argv) #inicia biblioteca glut
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB) #double pois troca entre back buffer (desenho) e front buffer (oq realmente é mostrado)
    glutInitWindowSize(800, 800)
    glutInitWindowPosition(500,100)
    glutCreateWindow(b"T1") #b = string -> bytes
    Inicializa()
    glutDisplayFunc(Display) #display callback OBRIGATORIO // como parametro, mandar funcao que desenha
    glutTimerFunc(TIME_MS,Timer,0)

    try:
        glutMainLoop()
    except SystemExit:
        pass

if __name__ == '__main__':
    main()


#O QUE FALTA:
#Algum processamento (com visualização) dos dados. Por exemplo: mudar as
#cores dos personagens se eles chegarem muito perto um do outro, desenvolver
#método para que eles evitem colisão, etc...

#Deve haver alguma interação com mouse ou teclado para mover pelo menos
#uma entidade na aplicação (simulando um avatar);

#Video

#Apresentar pipeline do trabalho quando for mostrar

#Artigo