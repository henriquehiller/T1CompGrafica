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
    #perna esquerda
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


def desenhaEixos():
    glPushMatrix() #Salva a matriz MODELVIEW atual no topo da pilha.
    glLoadIdentity() #Zera a MODELVIEW corrente para a identidade.

    glColor3f(1, 1, 1) #rgb de 1 a 0 // 1,1,1 = branco
    glLineWidth(1)

    #- GL_POINTS: cada glVertex2f cria um ponto.
    #GL_LINES: a cada par de vértices, forma-se um segmento.
    #GL_TRIANGLES: a cada 3 vértices, forma-se um triângulo.
    
    glBegin(GL_LINES)
    #0,0 é o ponto do meio
    glVertex2f(left, 0) #canto esquerdo (-1), 0
    glVertex2f(right, 0) # + canto direito (1), 0
    #par de vertices formando uma linha
    glVertex2f(0, bottom)
    glVertex2f(0, top)
    glEnd()

    glPopMatrix()

def desenhaPonto():
    glPushMatrix() 
    glLoadIdentity() 
    glColor3f(1, 1, 1) 
    glPointSize(15)
    glBegin(GL_POINTS)
    glVertex2f(0, 0) 
    glEnd()

    glPopMatrix()

def Reader():
    with open ("Paths_D_Modified_2.txt") as f: ####
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
    frame = 1

    for a, b, c in triple_re.findall(rest):
        if int(c) == frame:
            localFrames.append((int(c), int(a), int(b))) #frame, x, y 
            frame +=1
        else: 
            localFrames.append((frame,None,None))
            frame +=1
        
    while (frame!=maxFrame): 
        localFrames.append((frame,None,None))
        frame+=1

    ent = Entity(localFrames[0][1],localFrames[0][2],(1,1,1),localFrames)
    entityList.append(ent)

#frames globais
currentFrame = 1
maxFrame = 375

def Display():
    glClear(GL_COLOR_BUFFER_BIT) #ia
    glMatrixMode(GL_MODELVIEW) #garantir modelview indentity por frame e evita acumular transformacoes antigas
    glLoadIdentity()
    desenhaEixos()
    entityNum = 1
    for ent in entityList:
            if currentFrame < len(ent.frames) and len(ent.frames[currentFrame]) > 2: #garante que tem todos os frame e confirma se tem oq mostrar ou nao
                ent.x = ent.frames[currentFrame][1]
                ent.y = ent.frames[currentFrame][2]
                print ("frame"+str(currentFrame)+" entity: "+str(entityNum)+" y: "+str(ent.y)+" x: "+str(ent.x))
                desenhaEntity(ent) #otimizar pra so mudar posicao de entity especifica
            entityNum+=1

    # usando double-buffer, troque buffers: IA
    glutSwapBuffers() #ao inves de glFlush(), usando quando so um buffer

def Timer(value):
    global currentFrame
    if (currentFrame < maxFrame):
        currentFrame+=1
    glutTimerFunc(1000,Timer, 0) #1000ms, func Timer, 0 = nada
    glutPostRedisplay() #redesenho


# Inicializa variáveis e configurações de viewport
def Inicializa():
    global left, right, top, bottom, panX, panY

    Reader()

    # cor de fundo
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glMatrixMode(GL_PROJECTION)
    left = -1
    right = 1
    top = 1
    bottom = -1
    panX = 0
    panY = 0
    gluOrtho2D(left + panX, right + panX, bottom + panY, top + panY)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    glutInit(sys.argv) #inicia biblioteca glut
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB) #double pois troca entre back buffer (desenho) e front buffer (oq realmente é mostrado)
    glutInitWindowSize(800, 800)
    glutInitWindowPosition(100,100)
    glutCreateWindow(b"T1") #b = string -> bytes
    Inicializa()
    glutDisplayFunc(Display) #display callback OBRIGATORIO // como parametro, mandar funcao que desenha

    glutTimerFunc(1000,Timer,0)

    try:
        glutMainLoop()
    except SystemExit:
        pass

if __name__ == '__main__':
    main()