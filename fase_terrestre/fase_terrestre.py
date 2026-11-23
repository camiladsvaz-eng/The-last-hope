
import pygame
from pathlib import Path
from .jogador import Jogador
from coletaveis.coletaveis import Sobrevivente
from coletaveis.gerenciador_coletas import GerenciadorColetas
from .gerenciador_inimigos import GerenciadorInimigos
from .inimigos_terrestres import InimigoTerrestre


class FaseTerrestre:
    def __init__(self, largura_tela, altura_tela, gerenciador_coletas):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.gerenciador_coletas = gerenciador_coletas
        self.gerenciador_coletas.definir_fase("terrestre")

        # Carregamento do cenario
        pasta_imagens = Path(__file__).resolve().parent / "assets" / "cenario"

        self.fundo = pygame.image.load(
            str(pasta_imagens / "planeta.png")
        ).convert()

        self.fundo = pygame.transform.scale(
            self.fundo,
            (largura_tela, altura_tela)
        )

        # Criacao das plataformas
        altura_chao = int(altura_tela * 0.90)

        self.plataformas = [
            pygame.Rect(
                0,
                altura_chao,
                largura_tela,
                altura_tela - altura_chao
            ),
            pygame.Rect(
                int(largura_tela * 0.025),
                int(altura_tela * 0.73),
                int(largura_tela * 0.19),
                16
            ),
            pygame.Rect(
                int(largura_tela * 0.24),
                int(altura_tela * 0.57),
                int(largura_tela * 0.18),
                16
            ),
            pygame.Rect(
                int(largura_tela * 0.47),
                int(altura_tela * 0.44),
                int(largura_tela * 0.18),
                16
            ),
            pygame.Rect(
                int(largura_tela * 0.74),
                int(altura_tela * 0.35),
                int(largura_tela * 0.24),
                16
            )
        ]

        # Criacao do jogador
        self.jogador = Jogador(80, altura_chao - 96)

        # Sobrevivente inicialmente bloqueado
        sobrevivente = Sobrevivente(
                x=700,
                y=altura_chao - 36,
                desbloqueado=False
            )

        self.gerenciador_coletas.adicionar_coletavel(sobrevivente)

        # Gerenciador dos inimigos terrestres
        self.gerenciador_inimigos = GerenciadorInimigos()

        # Inimigo temporario para teste de integracao
        inimigo = InimigoTerrestre(
            x=500,
            y=altura_chao - 40
            )

        self.gerenciador_inimigos.adicionar_inimigo(inimigo)
    
    def tratar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_SPACE:
                self.jogador.pular()

            elif evento.key == pygame.K_RETURN:
                self.jogador.atacar()

    def atualizar(self):
        teclas = pygame.key.get_pressed()

        self.jogador.atualizar(teclas, self.plataformas)
        self.gerenciador_coletas.atualizar(self.jogador)
        self.gerenciador_inimigos.atualizar(
        self.largura_tela,
        self.gerenciador_coletas
        )

    def desenhar(self, tela):
        # Cenario
        tela.blit(self.fundo, (0, 0))

        # Plataformas
        for plataforma in self.plataformas:
            pygame.draw.rect(
                tela,
                (100, 75, 55),
                plataforma
            )

        # Jogador
        self.jogador.desenhar(tela)
        self.gerenciador_coletas.desenhar(tela)

        self.gerenciador_inimigos.desenhar(tela)