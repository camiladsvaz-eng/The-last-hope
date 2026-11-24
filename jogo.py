
import pygame
import random

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from fase_espacial.nave import Nave
from fase_terrestre.fase_terrestre import FaseTerrestre

from sistema_coleta.coletaveis import Cristal, PecaTecnologica
from sistema_coleta.gerenciador_coletas import GerenciadorColetas


class Jogo:

    def __init__(self):

        pygame.init()

        self.largura = SCREEN_WIDTH
        self.altura = SCREEN_HEIGHT

        self.tela = pygame.display.set_mode(
            (self.largura, self.altura)
        )

        pygame.display.set_caption("THE LAST HOPE")

        self.relogio = pygame.time.Clock()
        self.fps = FPS

        self.rodando = True

        # Controle das fases
        self.fase_atual = "espacial"

        # Fase espacial
        self.nave = Nave(375, 500)

        # Cronômetro da fase espacial
        self.tempo_fase = 10
        self.inicio_fase = pygame.time.get_ticks()

        # Sistema de coleta
        self.gerenciador_coletas = GerenciadorColetas(
            fase_inicial="espaco",
            altura_tela=self.altura
        )

        self.iniciar_coletas_espaciais()

        # Fase terrestre
        self.fase_terrestre = None

    def iniciar_coletas_espaciais(self):

        # Adiciona três cristais
        for _ in range(3):

            x = random.randint(60, self.largura - 60)
            y = random.randint(-120, 120)

            cristal = Cristal(
                x,
                y,
                velocidade_y=2
            )

            self.gerenciador_coletas.adicionar_coletavel(cristal)

        # Adiciona duas peças tecnológicas
        for _ in range(2):

            x = random.randint(60, self.largura - 60)
            y = random.randint(-120, 120)

            peca = PecaTecnologica(
                x,
                y,
                velocidade_y=2
            )

            self.gerenciador_coletas.adicionar_coletavel(peca)

    def processar_eventos(self):

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                self.rodando = False

            elif evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    self.rodando = False

            if self.fase_atual == "terrestre":
                self.fase_terrestre.tratar_eventos(evento)

    def mudar_fase(self):

        if self.fase_atual == "espacial":

            print("Iniciando fase terrestre!")

            self.fase_atual = "terrestre"

            # Limpa os coletáveis espaciais
            self.gerenciador_coletas.definir_fase("terrestre")

            self.fase_terrestre = FaseTerrestre(
                self.largura,
                self.altura
            )

    def atualizar(self):

        if self.fase_atual == "espacial":

            teclas = pygame.key.get_pressed()

            self.nave.mover(
                teclas,
                self.largura,
                self.altura
            )

            # Atualiza os coletáveis e verifica colisões com a nave
            self.gerenciador_coletas.atualizar(self.nave)

            tempo_decorrido = (
                pygame.time.get_ticks() - self.inicio_fase
            ) // 1000

            tempo_restante = self.tempo_fase - tempo_decorrido

            if tempo_restante <= 0:
                self.mudar_fase()

        elif self.fase_atual == "terrestre":

            self.fase_terrestre.atualizar()

    def desenhar(self):

        if self.fase_atual == "espacial":

            self.tela.fill((10, 10, 30))

            # Desenha coletáveis e painel de contagem
            self.gerenciador_coletas.desenhar(self.tela)

            # Desenha a nave
            self.nave.desenhar(self.tela)

            tempo_decorrido = (
                pygame.time.get_ticks() - self.inicio_fase
            ) // 1000

            tempo_restante = max(
                0,
                self.tempo_fase - tempo_decorrido
            )

            fonte = pygame.font.Font(None, 36)

            texto = fonte.render(
                f"Tempo: {tempo_restante}s",
                True,
                (255, 255, 255)
            )

            # Cronômetro no canto superior direito
            posicao_x = self.largura - texto.get_width() - 20

            self.tela.blit(texto, (posicao_x, 20))

        elif self.fase_atual == "terrestre":

            self.fase_terrestre.desenhar(self.tela)

        pygame.display.flip()

    def executar(self):

        while self.rodando:

            self.processar_eventos()

            self.atualizar()

            self.desenhar()

            self.relogio.tick(self.fps)

        pygame.quit()

    def verificar_tempo(self):

        tempo_atual = pygame.time.get_ticks()

        tempo_decorrido = (
            tempo_atual - self.inicio_fase
        ) // 1000

        tempo_restante = self.tempo_fase - tempo_decorrido

        if tempo_restante <= 0:
            print("Tempo esgotado! Próxima fase...")
            self.rodando = False

        return tempo_restante
