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

SQRT2_OVER_2 = math.sqrt(2) / 2 #ia q disse :(

def calculaXPerna (x,legLength,side): #1 para perna direta, 0 para perna esquerda
    if side==1:
        #ang = math.radians(315) ou math.radians(225)
        ang = SQRT2_OVER_2
        return (x+(legLength*math.cos(ang)))/500 #dividid por 1000???
    elif side ==0:
        ang = -SQRT2_OVER_2
        return (x+(legLength*math.cos(ang)))/500 #dividid por 1000???
    else:
        raise ValueError("Wrong side value")
    
def calculaYPerna (y,legLength,side): #1 para perna direta, 0 para perna esquerda
    if side==1:
        ang = -SQRT2_OVER_2
        return (y+(legLength*math.sin(ang)))/500 #dividid por 1000???
    elif side ==0:
        ang = -SQRT2_OVER_2
        return (y+(legLength*math.sin(ang)))/500 #dividid por 1000???
    else:
        raise ValueError("Wrong side value")
    

def desenhaEntity(ent):
    glPushMatrix()
    glLoadIdentity()

    x = ent.x
    y = ent.y
    legLength = ent.legLength
    armLength = ent.legLength
    bodyLength = ent.bodyLength
    glColor3f(1,1,1) #arrumar para receber ent.c
    #antes tava glColor3f(ent.c), nao funcionou pq so tem um argumento (?)
    glLineWidth (5)

    # Normaliza as coordenadas (dividido por 1000)
    glTranslatef(x / 1000.0, y / 1000.0, 0.0)

    glBegin(GL_LINES)
    #perna esquerda
    glVertex2f(0,0)
    xAux = calculaXPerna(x,legLength,0)
    yAux = calculaYPerna(y,legLength,0)
    glVertex2f(xAux,yAux)
    #perna direita
    glVertex2f(0,0)
    xAux = calculaXPerna(x,legLength,1)
    yAux = calculaYPerna(y,legLength,1)
    glVertex2f(xAux,yAux)
    #torso
    headY = (bodyLength/500)
    glVertex2f(0,0)
    glVertex2f(0,headY)
    #bracos
    #esquerda
    glVertex2f(0,headY)
    glVertex2f((armLength/500),headY)
    #direita
    glVertex2f(0,headY)
    glVertex2f(((armLength/500)*-1),headY)
    glEnd()

    #cabeca
    headSize = 20
    glPointSize(headSize)
    glBegin(GL_POINTS)
    glVertex2f(0,headY+(headSize/1000))
    glEnd()


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
    desenhaEntity(Entity(40,80,50,30,80,(1,1,1)))
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