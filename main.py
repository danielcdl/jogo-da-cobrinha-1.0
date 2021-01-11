import pygame
import time
from random import randint

# ==================== Constantes ===================================
LARGURAJANELA = 500
ALTURAJANELA = 400
TAMANHO = 20

CIMA = pygame.K_UP
BAIXO = pygame.K_DOWN
DIREITA = pygame.K_RIGHT
ESQUERDA = pygame.K_LEFT
                        
# ==================== Cores ===================================
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE_F = (124, 252, 0)

# ============= classes =========================================
class Cobrinha:

    def __init__(self):
        self.pontos = 0
        self.coordenadas = [pygame.Rect(100, 100, TAMANHO, TAMANHO)]
        self.direcao = None
        self.velocidade = 1000
        self.comandos = {CIMA: self.pra_cima,
                        BAIXO: self.pra_baixo,
                        DIREITA: self.pra_direita,
                        ESQUERDA: self.pra_esquerda
                        }

    def andar(self, direcao):
        andou = self.comandos[direcao]()
                
        if andou:
            perdeu = self.verificar_colisao()
            if perdeu:
                return 'perdeu'
            else:
                self.direcao = direcao
                pontuou = self.verificar_pontuou(fruta)
                if pontuou:
                    fruta.nova()
                    self.velocidade = 50 if self.velocidade < 51 else self.velocidade - 10
                else:
                    del self.coordenadas[0]

    def pra_direita(self):
        andou = False
        if self.direcao != ESQUERDA:
            self.coordenadas.append(pygame.Rect(
                cobrinha.coordenadas[-1].x + TAMANHO, 
                cobrinha.coordenadas[-1].y, 
                TAMANHO, 
                TAMANHO
            ))          
            andou = True
        return andou
    
    def pra_esquerda(self):
        andou = False
        if self.direcao != DIREITA:
            self.coordenadas.append(pygame.Rect(
                cobrinha.coordenadas[-1].x - TAMANHO, 
                cobrinha.coordenadas[-1].y, 
                TAMANHO, 
                TAMANHO
            ))
            andou = True
        return andou

    def pra_cima(self):
        andou = False
        if self.direcao != BAIXO:
            self.coordenadas.append(pygame.Rect(
                cobrinha.coordenadas[-1].x, 
                cobrinha.coordenadas[-1].y - TAMANHO, 
                TAMANHO, 
                TAMANHO
            ))
            andou = True
        return andou

    def pra_baixo(self):
        andou = False
        if self.direcao != CIMA:
            self.coordenadas.append(pygame.Rect(
                cobrinha.coordenadas[-1].x, 
                cobrinha.coordenadas[-1].y + TAMANHO,
                TAMANHO, 
                TAMANHO
            ))
            andou = True
        return andou
    
    def verificar_pontuou(self, fruta):
        pontuou = self.coordenadas[-1].colliderect(fruta.coordenada)
        if pontuou:
            self.pontos += 10
        return pontuou
    
    def verificar_colisao(self):
        colidiu = False

        # verifica se a cobrinha comeu seu corpo
        cabeca = cobrinha.coordenadas[-1]
        for coordenada in cobrinha.coordenadas[:-1]:
            colidiu = cabeca.colliderect(coordenada)
            if colidiu:
                break
        
        # Verifica se a cobrinha excedeu o limite da tela
        if not (0 <= cabeca.x < LARGURAJANELA and 0 <= cabeca.y < ALTURAJANELA):
            colidiu = True
        return colidiu

    def perdeu(self):
        self.pontos = 0
        self.coordenadas = [pygame.Rect(100, 100, TAMANHO, TAMANHO)]
        self.direcao = None
        self.velocidade = 1000


class Fruta:

    def __init__(self):
        self.coordenada = pygame.Rect(0, 0, TAMANHO, TAMANHO)
        self.nova()
    
    def nova(self):
        x = randint(0, LARGURAJANELA - TAMANHO)
        x -= x % TAMANHO

        y = randint(0, ALTURAJANELA - TAMANHO)
        y -= y % TAMANHO

        self.coordenada.x = x
        self.coordenada.y = y
        
        if self.coordenada in cobrinha.coordenadas:
            self.nova()

# ================== Funções =============================
def desenhar(cobrinha:object, fruta:object):
    """
    Funcão que desenha a cobrinha, a fruta e o que mais seja necessário
    """

    for coordenada in cobrinha.coordenadas:
        pygame.draw.rect(janela, PRETO, coordenada)
        pygame.draw.rect(janela, VERDE_F, coordenada, 1)
    
    pygame.draw.rect(janela, AZUL, fruta.coordenada)

# ================= Inicialização do jogo =================================
pygame.init()

janela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
pygame.display.set_caption('Jogo da Cobrinha')

cobrinha = Cobrinha()
fruta = Fruta()
continuar = True
andou = False
contador = 0
while continuar:
    contador += 1
    if contador == cobrinha.velocidade:
        if cobrinha.direcao:
            resultado = cobrinha.andar(cobrinha.direcao)
            if resultado == 'perdeu':
                cobrinha.perdeu()
                fruta.nova() 
        contador = 0
    janela.fill(BRANCO)
    pygame.draw.rect(janela, PRETO, (0, 0, LARGURAJANELA, ALTURAJANELA), 1)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            continuar = False

        if evento.type == pygame.KEYDOWN:
            tecla = evento.key
            if tecla in cobrinha.comandos:
                resultado = cobrinha.andar(tecla)
                if resultado == 'perdeu':
                    cobrinha.perdeu()
                    fruta.nova()
                else:
                    contador = 0
    desenhar(cobrinha, fruta)
    pygame.display.update()

pygame.quit() 