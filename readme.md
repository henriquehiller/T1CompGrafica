# Projeto: Animação 2D baseada em dados com detecção de colisão AABB em OpenGL

Este projeto implementa um pipeline de animação 2D “data-driven” (baseado em dados) para múltiplas entidades, lendo coordenadas por frame de um arquivo, atualizando posições, calculando caixas delimitadoras (AABB) e detectando colisões. Em caso de colisão, as entidades mudam de cor. Uma das entidades pode ser controlada pelo usuário via teclado. A renderização é feita com OpenGL (pipeline fixo), usando projeção ortográfica e dupla bufferização.

## Descrição
- Leitura de trajetórias por frame a partir de arquivo (dataset “Cultural Dataset”).
- Atualização de estado por frame, incluindo controle interativo de uma entidade.
- Cálculo de AABB (minX, minY, maxX, maxY) por entidade com base nas poses das partes (pernas, braços, torso, cabeça).
- Detecção de colisão por AABB e resposta visual (alteração de cor) estável por frame.
- Renderização em OpenGL com gluOrtho2D, glBegin/glEnd (linhas), glColor3f, glLineWidth e duplo buffer (GLUT_DOUBLE).

## Pipeline
1) Atualização de estado
- Para cada frame: ler posição da entidade (x, y) do arquivo pré-carregado e aplicar entradas do usuário (se houver).

2) Atualização das AABBs
- Reinicializar min/max (+inf/-inf) por entidade.
- Calcular posições relevantes de cada parte (em coordenadas de mundo) e expandir AABB.

3) Colisão
- Verificar sobreposição de AABBs entre entidades ativas (overlap em X e Y).
- Marcar entidades que colidem (flag collided).

4) Resposta visual e desenho
- Decidir cor por entidade (uma vez por frame).
- Desenhar entidades com OpenGL e trocar buffers.

## Requisitos
- Python 3.x
- Dependências Python:
  - PyOpenGL
  - PyOpenGL_accelerate (opcional)
- GLUT (FreeGLUT) instalado no sistema:
  - Windows: incluir DLLs/instalador compatível, se necessário.
  - Linux (Debian/Ubuntu): sudo apt install freeglut3-dev
  - macOS (Homebrew): brew install freeglut

## Instalação
- Instale as dependências Python:
```bash
pip install PyOpenGL PyOpenGL_accelerate
```
- Garanta que o FreeGLUT esteja instalado no sistema (ver Requisitos).

## Execução
- Abra um terminal na pasta do projeto.
- Execute:
  - Windows: py T1.py
  - Linux/macOS: python T1.py (ou python3 T1.py)
- A janela do projeto será aberta com a animação. Pressione Esc para sair.

## Controles
- W/A/S/D: move a entidade controlável (player).
- Esc: encerra a aplicação.

## Estrutura dos dados
- O dataset fornece, por entidade, uma sequência de tuplas (x, y, frame) por linha, precedida pelo número total de frames presentes.
- Exemplo conceitual de linha:
  - 97 (950,421,1)(950,421,2)(950,421,3) ...
- O parser organiza os dados em um vetor indexado por frame (convenção 1-based no projeto), permitindo acessar rapidamente a posição por frame.

## Arquitetura (visão geral)
- Reader: carrega as coordenadas do dataset em memória antes da animação.
- Estrutura Entity:
  - Atributos principais: x, y, c (cor), frames, active, positions, headY, minX, minY, maxX, maxY, collided.
- Display loop (GLUT):
  - Timer controla avanço de frames/subestados; Display desenha o frame atual.
  - Dupla bufferização com glutSwapBuffers.
- AABB:
  - Calculado por frame em coordenadas “brutas” (as mesmas do dataset).
  - Offsets locais das partes são convertidos para essa mesma escala antes de expandir min/max.
- Colisão:
  - Teste AABB-AABB padrão (overlap em X e Y).
  - Colisão marca collided; cor é decidida uma vez por frame para evitar flicker.

## Resultados
- Animação estável em tempo real, sem flicker, com troca de buffers dupla.
- Colisão por AABB adequada ao contexto: sobreposições corretas e resposta visual consistente.
- Integração de input do usuário sem quebrar a cadência de atualização e sem instabilidades visuais.

## Limitações e melhorias futuras
- Complexidade da colisão O(n²) para n entidades (comparação ingênua). Para muitas entidades, recomenda-se:
  - Evitar pares duplicados (i < j).
  - Broad-phase com grid uniforme ou quadtree.
  - Sweep and prune em um eixo para reduzir candidatos.
- Renderização:
  - Atualmente usa pipeline fixo. Pode ser migrado para shaders (OpenGL moderno) se necessário.

## Créditos e observações
- Ferramentas de IA foram utilizadas para auxiliar a geração de alguns métodos auxiliares (por exemplo, parsing de dados) e para consulta/sugestões de comandos específicos de OpenGL.
- O desenho do pipeline (animação, colisão, renderização), a integração e as decisões de arquitetura foram conduzidos manualmente.
- Dataset: “Cultural Dataset” (organize o caminho/uso conforme sua estrutura local).