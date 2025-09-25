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
        self.active = False
        self.collided = False

        #usado para bounding box
        self.minX  = float('inf')
        self.minY  = float('inf') 
        self.maxX  = float('-inf')
        self.maxY  = float('-inf')


def calculaXCurvado (legLength,side): #1 para perna direta, 0 para perna esquerda
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

    
def calculaYCurvado (legLength,side): #1 para perna direta, 0 para perna esquerda
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


def desenhaPerna(x,y,xAux,yAux,ent):
    glPushMatrix()
    glLoadIdentity()

    glTranslatef(x / 1000.0, y / 1000.0, 0.0)
    r, g, b = ent.c
    glColor3f(r,g,b)
    glLineWidth (5)

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

def desenhaBracos (x,y,headY,xAux,yAux,ent):
    glPushMatrix()
    glLoadIdentity()

    glTranslatef(x / 1000.0, y / 1000.0, 0.0)
    r, g, b = ent.c
    glColor3f(r,g,b) 
    glLineWidth (5)

    glBegin(GL_LINES)
    glVertex2f(0,headY)
    glVertex2f(0+xAux,(headY)+yAux)
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
    if (ent.x is None or ent.y is None): 
        ent.active = False
        return
    else: ent.active = True
    x = ent.x
    y = ent.y

    positions = []

    legLength = 50

    #calculos posicoes novas
    #perna esquerda
    xAux = calculaXCurvado(legLength,0)
    yAux = calculaYCurvado(legLength,0)
    positions.append((xAux,yAux))
    UpdateEntity(ent,x+xAux,y+yAux)

    print("perna esquerda: ",y+yAux) #

    #perna direita
    xAux = calculaXCurvado(legLength,1)
    yAux = calculaYCurvado(legLength,1)
    positions.append((xAux,yAux))
    UpdateEntity(ent,x+xAux,y+yAux)

    print("perna direita: ",y+yAux)
    
    bodyLength = 50
    headY = (bodyLength/1000)

    #torso
    UpdateEntity(ent,x,y+headY)

    print("torso: ",y+headY)

    armLength = 50

    #braco esquerda
    xAux = calculaXCurvado(armLength,0) 
    yAux = calculaYCurvado(armLength,0)
    positions.append((xAux,yAux))
    UpdateEntity(ent,x+xAux,y+(headY)+yAux)

    print("headY: ",headY)
    print("braco esquerda: ",y+(headY)+yAux)
    
    #braco direita
    xAux = calculaXCurvado(armLength,1)
    yAux = calculaYCurvado(armLength,1)
    positions.append((xAux,yAux))
    UpdateEntity(ent,x+xAux,y+(headY)+yAux)

    print("headY: ",headY)
    print("braco direita: ",y+(headY)+yAux)

    #cabeca ARRUMAR PRA CADA LADO PQ ELE NAO TA PEGANDO AS EXTREMIDADES
    UpdateEntity(ent,x+10,y+(headY)+10) #devido a tamanho 20 do ponto da cabeca

    print("cabeca: ",y+(headY+10))

    CollisionSystem(ent)

    #desenhos
    desenhaPerna(x,y,positions[0][0],positions[0][1],ent) #perna esquerda
    desenhaPerna(x,y,positions[1][0],positions[1][1],ent) #perna direita
    desenhaTorso(x,y,headY,ent) #torso
    desenhaBracos(x,y,headY,positions[2][0],positions[2][1],ent) #braco esquerdo
    desenhaBracos(x,y,headY,positions[3][0],positions[3][1],ent) #braco esquerdo
    desenhaCabeca(x,y,headY,ent) #cabeca


def UpdateEntity(ent,xAux,yAux):
    if xAux > ent.maxX: ent.maxX = xAux
    if xAux < ent.minX: ent.minX = xAux
    if yAux > ent.maxY: ent.maxY = yAux
    if yAux < ent.minY: ent.minY = yAux

def CollisionSystem (ent):
    print(ent.c) #
    nmro = 0 # 
    overlapX = False
    overlapY = False
    print ("Main Ent\n Min X:",ent.minX, " Max X: ",ent.maxX, " Min Y: ",ent.minY, " Max Y: ",ent.maxY) # 
    for entAux in entityList:
        if entAux == ent: 
            nmro +=1
            continue
        print (nmro," Ent\n Min X:",entAux.minX, " Max X: ",entAux.maxX, " Min Y: ",entAux.minY, " Max Y: ",entAux.maxY) # 
        if entAux.active == False: 
            nmro +=1
            continue
        if ent.minX <= entAux.maxX and ent.maxX >= entAux.minX: overlapX = True
        if ent.minY <= entAux.maxY and ent.maxY >= entAux.minY: overlapY = True
        if overlapX == True and overlapY == True: 
            print ("COLISSION!") #
            print ("Collission Ent\n Min X:",entAux.minX, " Max X: ",entAux.maxX, " Min Y: ",entAux.minY, " Max Y: ",entAux.maxY) # 
            ColorSwitcher(ent,entAux)
        overlapX = False
        overlapY = False
        nmro +=1

def ColorSwitcher (ent1,ent2):
    colors = [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1)]
    ent1.c = colors [random.randint(0,5)]
    while ent1.c == ent2.c: ent1.c = colors [random.randint(0,5)]


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
TIME_MS = 75 #1 fps, 1000 ms;10 fps, 100ms;100 fps, 10ms; 20fps, 50ms; O NORMAL E 75!!!!!!!!!!!!!!!!!!!!!!!

def Display():
    glClear(GL_COLOR_BUFFER_BIT) #ia
    glMatrixMode(GL_MODELVIEW) #garantir modelview indentity por frame e evita acumular transformacoes antigas
    glLoadIdentity() 
    for ent in entityList: 
            InicializeBox(ent)
            if currentFrame < len(ent.frames) and len(ent.frames[currentFrame]) > 2: #garante que tem todos os frame e confirma se tem oq mostrar ou nao
                ent.x = ent.frames[currentFrame][1]
                ent.y = ent.frames[currentFrame][2]
                desenhaEntity(ent)
    # usando double-buffer, troque buffers
    glutSwapBuffers() #ao inves de glFlush(), usando quando so um buffer

def InicializeBox(ent):
    ent.minX  = float('inf')
    ent.minY  = float('inf') 
    ent.maxX  = float('-inf')
    ent.maxY  = float('-inf')

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