import math

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
    def __init__(self, x, y, legLength, armLength, bodyLength, c=(1,0,0)):
        self.x = x
        self.y = y
        self.legLength = legLength
        self.armLength = armLength
        self.bodyLength = bodyLength
        self.c = c


def calculaXCurvado (x,legLength,side): #1 para perna direta, 0 para perna esquerda
    if side==1:
        ang = math.radians(315)
        return (legLength*math.cos(ang))/500 #dividid por 1000???
    elif side ==0:
        ang = math.radians(225)
        return (legLength*math.cos(ang))/500 #dividid por 1000???
    else:
        raise ValueError("Wrong side value")
    
def calculaYCurvado (y,legLength,side): #1 para perna direta, 0 para perna esquerda
    if side==1:
        ang = math.radians(315)
        return (legLength*math.sin(ang))/500 #dividid por 1000???
    elif side ==0:
        ang = math.radians(225)
        return (legLength*math.sin(ang))/500 #dividid por 1000???
    else:
        raise ValueError("Wrong side value")
    

def desenhaPerna(x,y,legLength,signal,color):
    glPushMatrix()
    glLoadIdentity()

    glTranslatef(x / 500.0, y / 500.0, 0.0)
    glColor3f(1,1,1) #MUDAR PARA COLOR
    glLineWidth (5)
    
    glBegin(GL_LINES)
    #perna esquerda
    glVertex2f(0,0)
    xAux = calculaXCurvado(x,legLength,signal)
    yAux = calculaYCurvado(y,legLength,signal)
    glVertex2f(xAux,yAux)
    glEnd()
    glPopMatrix()

def desenhaTorso (x,y,headY,color):
    glPushMatrix()
    glLoadIdentity()

    glTranslatef(x / 500.0, y / 500.0, 0.0)
    glColor3f(1,1,1) #MUDAR PARA COLOR
    glLineWidth (5)
    
    glBegin(GL_LINES)
    glVertex2f(0,0)
    glVertex2f(0,headY)
    glEnd()
    glPopMatrix()

def desenhaBracos (x,y,headY,armLength,signal,color):
    glPushMatrix()
    glLoadIdentity()

    glTranslatef(x / 500.0, y / 500.0, 0.0)
    glColor3f(1,1,1) #MUDAR PARA COLOR
    glLineWidth (5)
    
    glBegin(GL_LINES)
    glVertex2f(0,headY)
    xAux = calculaXCurvado(x,armLength,signal)
    yAux = calculaYCurvado(headY,armLength,signal)
    glVertex2f(xAux,yAux)
    glEnd()
    glPopMatrix()

def desenhaCabeca (x,y,headY,headSize,color):
    glPushMatrix()
    glLoadIdentity()

    glTranslatef(x / 500.0, y / 500.0, 0.0)
    glColor3f(1,1,1) #MUDAR PARA COLOR
    glPointSize(headSize)

    glBegin(GL_POINTS)
    glVertex2f(0,headY)
    glEnd()
    glPopMatrix()


def desenhaEntity(ent):
    x = ent.x
    y = ent.y
    legLength = ent.legLength
    armLength = ent.armLength
    bodyLength = ent.bodyLength
    color = ent.c
    #perna esquerda
    desenhaPerna(x,y,legLength,0,color)
    #perna esquerda
    desenhaPerna(x,y,legLength,1,color)
    
    headY = (bodyLength/500)

    #torso
    desenhaTorso(x,y,headY,color)
    #braco esquerda
    desenhaBracos(x,y,headY,armLength,0,color)
    #braco direita
    desenhaBracos(x,y,headY,armLength,1,color)

    headSize = 20
    desenhaCabeca(x,y,headY,headSize,color)


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

def Display():
    desenhaEixos()
    desenhaEntity(Entity(40,80,50,25,80,(1,1,1)))
    glFlush() #envia comandos para gpu


# Inicializa variáveis e configurações de viewport
def Inicializa():
    global left, right, top, bottom, panX, panY

    glMatrixMode(GL_PROJECTION)
    left = -1
    right = 1
    top = 1
    bottom = -1
    gluOrtho2D(left + panX, right + panX, bottom + panY, top + panY)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit(sys.argv) #inicia biblioteca glut
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(800, 800)
    glutCreateWindow(b"T1") #b = string -> bytes
    glutDisplayFunc(Display) #display callback OBRIGATORIO // como parametro, mandar funcao que desenha
    Inicializa()

    try:
        glutMainLoop()
    except SystemExit:
        pass

if __name__ == '__main__':
    main()