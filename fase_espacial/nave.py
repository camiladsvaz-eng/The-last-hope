
import pygame

class Nave:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 70, 70)
        self.velocidade = 5
        self.imagem = pygame.image.load("fase_espacial/imagens/nave_teste.png").convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (100, 100))

    def mover(self, teclas, largura, altura):
        if teclas[pygame.K_LEFT] and self.retangulo.left > 0:
            self.retangulo.x -= self.velocidade

        if teclas[pygame.K_RIGHT] and self.retangulo.right < largura:
            self.retangulo.x += self.velocidade

        if teclas[pygame.K_UP] and self.retangulo.top > 0:
            self.retangulo.y -= self.velocidade

        if teclas[pygame.K_DOWN] and self.retangulo.bottom < altura:
            self.retangulo.y += self.velocidade

        self.retangulo.clamp_ip(pygame.Rect(0, 0, largura, altura))

    def desenhar(self, tela):
        posicao = self.imagem.get_rect(center=self.retangulo.center)
        tela.blit(self.imagem, posicao)
