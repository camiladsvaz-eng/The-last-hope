import pygame

class InimigoTerrestre:

    def __init__(self, x, y, vida=100, velocidade=2):
        self.x = x
        self.y = y
        self.largura = 40
        self.altura = 40
        self.velocidade = velocidade
        self.vida = vida

        self.retangulo = pygame.Rect(
            self.x, self.y, self.largura, self.altura
        )

    def mover(self, largura_tela):
        if not self.esta_vivo():
            return

        self.x += self.velocidade

        if self.x + self.largura >= largura_tela:
            self.x = largura_tela - self.largura
            self.velocidade = -abs(self.velocidade)

        if self.x <= 0:
            self.x = 0
            self.velocidade = abs(self.velocidade)

        self.retangulo.x = self.x

    def desenhar(self, tela):
        if self.esta_vivo():
            pygame.draw.rect(tela, (255, 0, 0), self.retangulo)

    def receber_dano(self, dano):
        self.vida -= dano

        if self.vida < 0:
            self.vida = 0

    def esta_vivo(self):
        return self.vida > 0