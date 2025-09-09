import math
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
    def __init__(self, x, y, c=(1,1,1), frames = None):
        self.x = x
        self.y = y
        self.c = c
        self.frames = [] if frames is None else list(frames)
        #fazer variaveis pra vertices dos bracos cabecas e pernas


def calculaXCurvado (x,legLength,side): #1 para perna direta, 0 para perna esquerda
    if side==1:
        ang = math.radians(285)
        return (legLength*math.cos(ang))/1000 
    elif side ==0:
        ang = math.radians(255)
        return (legLength*math.cos(ang))/1000 
    else:
        raise ValueError("Wrong side value")
    
def calculaYCurvado (y,legLength,side): #1 para perna direta, 0 para perna esquerda
    if side==1:
        ang = math.radians(315)
        return (legLength*math.sin(ang))/1000 
    elif side ==0:
        ang = math.radians(225)
        return (legLength*math.sin(ang))/1000 
    else:
        raise ValueError("Wrong side value")
    

def desenhaPerna(x,y,signal,color):
    glPushMatrix()
    glLoadIdentity()

    glTranslatef(x / 1000.0, y / 1000.0, 0.0)
    glColor3f(1,1,1) 
    glLineWidth (5)
    
    legLength = 50

    glBegin(GL_LINES)
    glVertex2f(0,0)
    xAux = calculaXCurvado(x,legLength,signal)
    yAux = calculaYCurvado(y,legLength,signal)
    glVertex2f(0+xAux,0+yAux)
    glEnd()
    glPopMatrix()

def desenhaTorso (x,y,headY,color):
    glPushMatrix()
    glLoadIdentity()

    glTranslatef(x / 1000.0, y / 1000.0, 0.0)
    glColor3f(1,1,1) 
    glLineWidth (5)
    
    glBegin(GL_LINES)
    glVertex2f(0,0)
    glVertex2f(0,headY)
    glEnd()
    glPopMatrix()

def desenhaBracos (x,y,headY,signal,color):
    glPushMatrix()
    glLoadIdentity()

    glTranslatef(x / 1000.0, y / 1000.0, 0.0)
    glColor3f(1,1,1) 
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

def desenhaCabeca (x,y,headY,color):
    glPushMatrix()
    glLoadIdentity()

    glTranslatef(x / 1000.0, y / 1000.0, 0.0)
    glColor3f(1,1,1) 
    glPointSize(20)

    glBegin(GL_POINTS)
    glVertex2f(0,headY)
    glEnd()
    glPopMatrix()


def desenhaEntity(ent):
    if (ent.x is None or ent.y is None): return
    
    x = ent.x
    y = ent.y
    color = ent.c

    #perna esquerda
    desenhaPerna(x,y,0,color)
    #perna esquerda
    desenhaPerna(x,y,1,color)
    
    bodyLength = 50

    headY = (bodyLength/1000)

    #torso
    desenhaTorso(x,y,headY,color)
    #braco esquerda
    desenhaBracos(x,y,headY,0,color)
    #braco direita
    desenhaBracos(x,y,headY,1,color)

    desenhaCabeca(x,y,headY,color)

def Reader():
    with open ("Paths_D_Modified.txt") as f: ####
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

def Display():
    glClear(GL_COLOR_BUFFER_BIT) #ia
    glMatrixMode(GL_MODELVIEW) #garantir modelview indentity por frame e evita acumular transformacoes antigas
    glLoadIdentity()
    entityNum = 1
    for ent in entityList:
            if currentFrame < len(ent.frames) and len(ent.frames[currentFrame]) > 2: #garante que tem todos os frame e confirma se tem oq mostrar ou nao
                ent.x = ent.frames[currentFrame][1]
                ent.y = ent.frames[currentFrame][2]
                print ("frame"+str(currentFrame)+" entity: "+str(entityNum)+" y: "+str(ent.y)+" x: "+str(ent.x))
                desenhaEntity(ent)
            entityNum+=1

    # usando double-buffer, troque buffers: IA
    glutSwapBuffers() #ao inves de glFlush(), usando quando so um buffer
    

TIME_MS = 50 #1 fps, 1000 ms;10 fps, 100ms;100 fps, 10ms

def Timer(value):
    global currentFrame
    if (currentFrame <= MAXFRAME):
        currentFrame+=1
    elif (currentFrame == 376): currentFrame = 1
    glutTimerFunc(TIME_MS,Timer, 0) #1000ms, func Timer, 0 = nada
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