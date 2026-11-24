
import pygame
from pathlib import Path
from .personagem import Personagem


class Jogador(Personagem):
    def __init__(self, x, y):
        super().__init__(x, y, 96, 96, 5, 100)

        # Velocidade de corrida
        self.velocidade_corrida = 8

        # Estado do ataque
        self.atacando = False

        # Localizacao das imagens
        pasta_imagens = Path(__file__).resolve().parent / "assets" / "jogador"

        # Carregamento das animacoes
        self.carregar_animacao(
            "idle",
            str(pasta_imagens / "Swordsman_lvl3_Idle_with_shadow.png"),
            64, 64, linha=0
        )

        self.carregar_animacao(
            "walk",
            str(pasta_imagens / "Swordsman_lvl3_Walk_with_shadow.png"),
            64, 64, linha=0
        )

        self.carregar_animacao(
            "run",
            str(pasta_imagens / "Swordsman_lvl3_Run_with_shadow.png"),
            64, 64, linha=0
        )

        self.carregar_animacao(
            "attack",
            str(pasta_imagens / "Swordsman_lvl3_attack_with_shadow.png"),
            64, 64, linha=0
        )

        self.definir_animacao("idle")

    # Comando de ataque
    def atacar(self):
        if not self.atacando:
            self.atacando = True
            self.definir_animacao("attack", loop=False)

    # Atualizacao do jogador
    def atualizar(self, teclas, plataformas):
        direcao = 0

        # Movimentacao
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            direcao = -1

        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            direcao = 1

        # Corrida com Shift
        if teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]:
            self.velocidade = self.velocidade_corrida
        else:
            self.velocidade = 5

        # Movimento e gravidade
        self.mover_horizontal(direcao, plataformas)
        self.aplicar_gravidade(plataformas)

        # Escolha da animacao
        if not self.atacando:
            if direcao != 0:
                if self.velocidade == self.velocidade_corrida:
                    self.definir_animacao("run")
                else:
                    self.definir_animacao("walk")
            else:
                self.definir_animacao("idle")

        # Atualizacao da animacao
        self.atualizar_animacao()

        # Finalizacao do ataque
        if self.atacando and self.animacao_finalizada:
            self.atacando = False
            self.definir_animacao("idle")

