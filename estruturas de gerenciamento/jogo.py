import pygame

class Jogo:
    def _init_(self):
        pygame.init()

        self.largura = 800
        self.altura = 600

        self.tela = pygame.display.set_mode ((self.largura, self.altura))

        pygame.display.set_caption("The last hope")