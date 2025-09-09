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