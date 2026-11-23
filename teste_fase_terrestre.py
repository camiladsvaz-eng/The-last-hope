
import pygame
from fase_terrestre.fase_terrestre import FaseTerrestre
from coletaveis.gerenciador_coletas import GerenciadorColetas

pygame.init()

LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Teste - Fase Terrestre")

relogio = pygame.time.Clock()

gerenciador_coletas = GerenciadorColetas()

fase = FaseTerrestre(
    LARGURA,
    ALTURA,
    gerenciador_coletas
)

rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        fase.tratar_eventos(evento)

    fase.atualizar()
    fase.desenhar(tela)

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
