import math
import random
import re

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
        self.positions = []
        self.headY = 0

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
    if (ent.active == False): 
        return
    x = ent.x
    y = ent.y

    positions = ent.positions
    headY = ent.headY

    #desenhos
    desenhaPerna(x,y,positions[0][0],positions[0][1],ent) #perna esquerda
    desenhaPerna(x,y,positions[1][0],positions[1][1],ent) #perna direita
    desenhaTorso(x,y,headY,ent) #torso
    desenhaBracos(x,y,headY,ent.positions[2][0],ent.positions[2][1],ent) #braco esquerdo
    desenhaBracos(x,y,headY,ent.positions[3][0],ent.positions[3][1],ent) #braco esquerdo
    desenhaCabeca(x,y,headY,ent) #cabeca


def UpdateEntity(ent,xAux,yAux):
    if xAux > ent.maxX: ent.maxX = xAux
    if xAux < ent.minX: ent.minX = xAux
    if yAux > ent.maxY: ent.maxY = yAux
    if yAux < ent.minY: ent.minY = yAux

def CollisionSystem (ent):
    if (ent.active == False): 
        return
    overlapX = False
    overlapY = False
    for entAux in entityList:
        if entAux == ent: 
            continue
        if entAux.active == False: 
            continue
        if ent.minX <= entAux.maxX and ent.maxX >= entAux.minX: overlapX = True
        if ent.minY <= entAux.maxY and ent.maxY >= entAux.minY: overlapY = True
        if overlapX == True and overlapY == True:
            if(ent.collided == False or entAux.collided == False):
                ColorSwitcher(ent,entAux)
        overlapX = False
        overlapY = False

def InicializeBox(ent):
    if (ent.x is None or ent.y is None): 
        ent.active = False
        return
    else: ent.active = True

    ent.minX  = float('inf')
    ent.minY  = float('inf') 
    ent.maxX  = float('-inf')
    ent.maxY  = float('-inf')
    ent.positions = []
    ent.headY = 0
    ent.collided = False
    ent.c = (1,1,1)

    x = ent.x
    y = ent.y

    positions = []

    legLength = 50

    #calculos posicoes novas
    #perna esquerda
    xAux = calculaXCurvado(legLength,0)
    yAux = calculaYCurvado(legLength,0)
    ent.positions.append((xAux,yAux))
    UpdateEntity(ent,x+(xAux*1000),y+(yAux*1000))

    #perna direita
    xAux = calculaXCurvado(legLength,1)
    yAux = calculaYCurvado(legLength,1)
    ent.positions.append((xAux,yAux))
    UpdateEntity(ent,x+(xAux*1000),y+(yAux*1000))
    
    bodyLength = 50
    headY = (bodyLength/1000)
    ent.headY= headY

    #torso
    UpdateEntity(ent,x,y+(headY*1000))

    armLength = 50

    #braco esquerda
    xAux = calculaXCurvado(armLength,0) 
    yAux = calculaYCurvado(armLength,0)
    ent.positions.append((xAux,yAux))
    UpdateEntity(ent,x+(xAux*1000),y+(headY*1000)+(yAux*1000))
    
    #braco direita
    xAux = calculaXCurvado(armLength,1)
    yAux = calculaYCurvado(armLength,1)
    ent.positions.append((xAux,yAux))
    UpdateEntity(ent,x+(xAux*1000),y+(headY*1000)+(yAux*1000))

    #cabeca 
    UpdateEntity(ent,x+10,y+(headY*1000)+10) #devido a tamanho 20 do ponto da cabeca
    UpdateEntity(ent,x-10,y+(headY*1000)+10) #devido a tamanho 20 do ponto da cabeca

def ColorSwitcher (ent1,ent2):
    colors = [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1)]
    ent1.c = colors [random.randint(0,5)]
    ent2.c = colors [random.randint(0,5)]
    while ent1.c == ent2.c: ent1.c = colors [random.randint(0,5)]
    ent1.collided = True
    ent2.collided = True

def Reader():
    with open ("Paths_D.txt") as f:
        f.readline()
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

#variaveis globais
currentFrame = 1
MAXFRAME = 375
frameSignal = 0 #0 ou 1
TIME_MS = 75 #1 fps, 1000 ms;10 fps, 100ms;100 fps, 10ms; 20fps, 50ms
PlayerEntity = Entity(500,500,(1,1,1),None)

def Display():
    glClear(GL_COLOR_BUFFER_BIT) #ia
    glMatrixMode(GL_MODELVIEW) #garantir modelview indentity por frame e evita acumular transformacoes antigas
    glLoadIdentity() 
    for ent in entityList: 
            if currentFrame < len(ent.frames) and len(ent.frames[currentFrame]) > 2:
                ent.x = ent.frames[currentFrame][1]
                ent.y = ent.frames[currentFrame][2]
                InicializeBox(ent)
            elif ent == PlayerEntity:
                ent.x = ent.x
                ent.y = ent.y
                InicializeBox(ent)
    for ent in entityList: 
            CollisionSystem(ent)
    for ent in entityList: 
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

# Função para teclas do teclado comum (ASCII)
def Teclado(key: chr, x: int, y: int):
    global PlayerEntity

    if key == 27:  # Tecla ESC
        exit(0)

    # Teclas WASD para mover a câmera (pan)
    if key == b'a':
        PlayerEntity.x -=3
    if key == b'd':
        PlayerEntity.x +=3
    if key == b'w':
        PlayerEntity.y +=3
    if key == b's':
        PlayerEntity.y -=3

    # Solicita redesenho
    glutPostRedisplay()

# Inicializa variáveis e configurações de viewport
def Inicializa():
    global left, right, top, bottom, panX, panY, PlayerEntity

    Reader()
    PlayerEntity.active = True #liga o PlayerEntity
    entityList.append(PlayerEntity) #adiciona o PlayerEntity na lista

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
    glutKeyboardFunc(Teclado)
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
#-Processamento de dados aparentemente funcionando, mudar pra gradiente q quando mais se aproxima
#de alguem mais vermelho fica??? Veremos

#Deve haver alguma interação com mouse ou teclado para mover pelo menos
#uma entidade na aplicação (simulando um avatar);

#Aprimoracoes
#So animar se houver movimentacao
#Diminuir mudanca de cor PlayerEntity 

#Video

#Apresentar pipeline do trabalho quando for mostrar

#Artigo