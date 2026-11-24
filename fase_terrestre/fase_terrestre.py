
import pygame
from pathlib import Path
from .jogador import Jogador


class FaseTerrestre:
    def __init__(self, largura_tela, altura_tela):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

        # Carregamento do cenário
        pasta_imagens = Path(__file__).resolve().parent / "assets" / "cenario"

        self.fundo = pygame.image.load(
            str(pasta_imagens / "planeta.png")
        ).convert()

        self.fundo = pygame.transform.scale(
            self.fundo,
            (largura_tela, altura_tela)
        )

        # Definição da altura do chão
        altura_chao = int(altura_tela * 0.90)

        # Plataformas do cenário
        self.plataformas = [
            # Chão
            pygame.Rect(
                0,
                altura_chao,
                largura_tela,
                altura_tela - altura_chao
            ),

            # Primeira plataforma
            pygame.Rect(
                int(largura_tela * 0.025),
                int(altura_tela * 0.73),
                int(largura_tela * 0.19),
                16
            ),

            # Segunda plataforma
            pygame.Rect(
                int(largura_tela * 0.24),
                int(altura_tela * 0.57),
                int(largura_tela * 0.18),
                16
            ),

            # Terceira plataforma
            pygame.Rect(
                int(largura_tela * 0.47),
                int(altura_tela * 0.44),
                int(largura_tela * 0.18),
                16
            ),

            # Plataforma final
            pygame.Rect(
                int(largura_tela * 0.74),
                int(altura_tela * 0.35),
                int(largura_tela * 0.24),
                16
            )
        ]

        # Criação do jogador
        self.jogador = Jogador(
            80,
            altura_chao - 96
        )

    # Recebe os comandos do teclado
    def tratar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_SPACE:
                self.jogador.pular()
                
            elif evento.key == pygame.K_RETURN:
                self.jogador.atacar()

    # Atualiza os elementos da fase
    def atualizar(self):
        teclas = pygame.key.get_pressed()

        self.jogador.atualizar(teclas, self.plataformas)

    # Desenha o cenário
    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))

        # Desenho do jogador
        self.jogador.desenhar(tela)

