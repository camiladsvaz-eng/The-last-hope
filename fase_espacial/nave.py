
import pygame

class Nave:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 70, 70)
        self.velocidade = 5
        self.imagem = pygame.image.load("fase_espacial/imagens/nave_teste.png").convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (100, 100))

    def mover(self, teclas, largura, altura):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade

        if teclas[pygame.K_RIGHT] and self.rect.right < largura:
            self.rect.x += self.velocidade

        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidade

        if teclas[pygame.K_DOWN] and self.rect.bottom < altura:
            self.rect.y += self.velocidade

        self.rect.clamp_ip(pygame.Rect(0, 0, largura, altura))

    def desenhar(self, tela):
        posicao = self.imagem.get_rect(center=self.rect.center)
        tela.blit(self.imagem, posicao)
