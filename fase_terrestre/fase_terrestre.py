
import pygame
from pathlib import Path
from .jogador import Jogador
from .gerenciador_inimigos import GerenciadorInimigos
from .inimigos_terrestres import InimigoTerrestre
from sistema_coleta.coletaveis import Sobrevivente


class FaseTerrestre:
    def __init__(self, largura_tela, altura_tela, gerenciador_coletas):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.gerenciador_coletas = gerenciador_coletas

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
        # Criação do gerenciador de inimigos
        self.gerenciador_inimigos = GerenciadorInimigos()
        self.sobreviventes_desbloqueados = False

        # Criação dos inimigos
        inimigo1 = InimigoTerrestre(300, altura_chao - 96)
        inimigo2 = InimigoTerrestre(600, altura_chao - 96)

        self.gerenciador_inimigos.adicionar_inimigo(inimigo1)
        self.gerenciador_inimigos.adicionar_inimigo(inimigo2)

        # Criação dos sobreviventes
        sobrevivente1 = Sobrevivente(
            450,
            altura_chao - 36
        )

        sobrevivente2 = Sobrevivente(
            750,
            altura_chao - 36
        )

        self.gerenciador_coletas.adicionar_coletavel(sobrevivente1)
        self.gerenciador_coletas.adicionar_coletavel(sobrevivente2)

    # Recebe os comandos do teclado
    def tratar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_SPACE:
                self.jogador.pular()
                
            elif evento.key == pygame.K_RETURN:
                self.jogador.atacar()
                self.aplicar_dano_inimigos()

    # Atualiza os elementos da fase
    def atualizar(self):
        teclas = pygame.key.get_pressed()

        self.jogador.atualizar(teclas, self.plataformas)

        self.gerenciador_inimigos.atualizar(
            self.largura_tela,
            self.plataformas
        )
       
        for inimigo in self.gerenciador_inimigos.inimigos:

            if inimigo.esta_vivo():
                inimigo.atacar_jogador(self.jogador)

        if (
            self.gerenciador_inimigos.todos_derrotados()
            and not self.sobreviventes_desbloqueados
        ):
            self.gerenciador_coletas.desbloquear_sobreviventes()
            self.sobreviventes_desbloqueados = True

    # Desenha o cenário
    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))

        # Desenho do jogador
        self.jogador.desenhar(tela)

        self.gerenciador_inimigos.desenhar(tela)

    def aplicar_dano_inimigos(self):
        largura_ataque = 80
        altura_ataque = 60

        if self.jogador.direcao == 1:
            area_ataque = pygame.Rect(
                self.jogador.rect.right - 10,
                self.jogador.rect.top + 18,
                largura_ataque,
                altura_ataque
            )
        else:
            area_ataque = pygame.Rect(
                self.jogador.rect.left - largura_ataque + 10,
                self.jogador.rect.top + 18,
                largura_ataque,
                altura_ataque
            )

        for inimigo in self.gerenciador_inimigos.inimigos:
            if (
                inimigo.esta_vivo()
                and area_ataque.colliderect(inimigo.rect)
            ):
                inimigo.receber_dano(50)
                print("Inimigo recebeu dano! Vida:", inimigo.vida)
