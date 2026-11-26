import pygame
from pathlib import Path

class InimigoTerrestre:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.largura = 96
        self.altura = 96

        self.velocidade = 2
        self.direcao = 1
        self.vida = 100

        # Configurações de ataque
        self.dano = 10
        self.intervalo_ataque = 1000
        self.ultimo_ataque = 0

        self.atacando = False
        self.dano_aplicado = False

        self.morrendo = False
        self.morto = False

        self.distancia_ataque = 15

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.largura,
            self.altura
        )

        # Carrega a spritesheet
        caminho_imagem = (
            Path(__file__).resolve().parent
            / "assets"
            / "inimigos"
            / "inimigos.png"
        )

        self.spritesheet = pygame.image.load(
            str(caminho_imagem)
        ).convert_alpha()

        # Configuração da spritesheet
        self.colunas = 8
        self.linhas = 4

        self.largura_quadro = (
            self.spritesheet.get_width() // self.colunas
        )

        self.altura_quadro = (
            self.spritesheet.get_height() // self.linhas
        )

        # Carrega todas as animações
        self.animacoes = {}

        nomes_animacoes = {
            "andar": 0,
            "correr": 1,
            "atacar": 2,
            "morrer": 3
        }

        for nome, linha in nomes_animacoes.items():

            quadros = []

            for coluna in range(self.colunas):

                quadro = pygame.Surface(
                    (self.largura_quadro, self.altura_quadro),
                    pygame.SRCALPHA
                )

                quadro.blit(
                    self.spritesheet,
                    (0, 0),
                    (
                        coluna * self.largura_quadro,
                        linha * self.altura_quadro,
                        self.largura_quadro,
                        self.altura_quadro
                    )
                )

                quadro = pygame.transform.scale(
                    quadro,
                    (self.largura, self.altura)
                )

                quadros.append(quadro)

            self.animacoes[nome] = quadros

        # Animação inicial
        self.animacao_atual = "andar"
        self.quadro_atual = 0

        # Velocidade de cada animação (milissegundos)
        self.velocidades_animacao = {
            "andar": 120,
            "correr": 80,
            "atacar": 90,
            "morrer": 150
        }

        self.intervalo_animacao = self.velocidades_animacao["andar"]
        self.ultimo_update_animacao = pygame.time.get_ticks()

    # Movimentação do inimigo
    def mover(self, largura_tela, plataformas):

        if self.atacando or self.morrendo:
            self.atualizar_animacao()
            return
        
        
        distancia = 8
        altura_deteccao = 150

        if self.direcao == 1:
            area_frente = pygame.Rect(
                self.rect.right,
                self.rect.bottom - altura_deteccao,
                distancia,
                altura_deteccao
            )
        else:
            area_frente = pygame.Rect(
                self.rect.left - distancia,
                self.rect.bottom - altura_deteccao,
                distancia,
                altura_deteccao
            )

        # Verifica as plataformas
        for plataforma in plataformas:

            if plataforma.height > 30:
                continue

            if area_frente.colliderect(plataforma):
                self.direcao *= -1
                break

        # Movimento horizontal
        self.rect.x += self.velocidade * self.direcao
        self.x = self.rect.x

        self.limitar_movimento(largura_tela)

        self.atualizar_animacao()

    # Limita o movimento na tela
    def limitar_movimento(self, largura_tela):

        if self.rect.right >= largura_tela:
            self.rect.right = largura_tela
            self.x = self.rect.x
            self.direcao = -1

        if self.rect.left <= 0:
            self.rect.left = 0
            self.x = self.rect.x
            self.direcao = 1

    # Ataque ao jogador
    def atacar_jogador(self, jogador):

        if self.morrendo or self.morto:
            return

        if not jogador.esta_vivo():
            return

        # Área de proximidade
        area_ataque = self.rect.inflate(
            self.distancia_ataque * 2,
            20
        )

        tempo_atual = pygame.time.get_ticks()

        # Inicia o ataque
        if (
            not self.atacando
            and area_ataque.colliderect(jogador.rect)
            and tempo_atual - self.ultimo_ataque >= self.intervalo_ataque
        ):

            # Vira na direção do jogador
            if jogador.rect.centerx > self.rect.centerx:
                self.direcao = 1
            else:
                self.direcao = -1

            self.atacando = True
            self.dano_aplicado = False

            self.animacao_atual = "atacar"
            self.quadro_atual = 0

            self.ultimo_update_animacao = tempo_atual
            self.ultimo_ataque = tempo_atual

        # Aplica dano uma única vez durante o ataque
        if (
            self.atacando
            and self.quadro_atual >= 4
            and not self.dano_aplicado
        ):

            area_dano = self.rect.inflate(60, 20)

            if area_dano.colliderect(jogador.rect):
                jogador.receber_dano(self.dano)

                print(
                    "Jogador recebeu dano! Vida:",
                    jogador.vida
                )

            self.dano_aplicado = True

    # Atualização das animações
    
    def atualizar_animacao(self):

        tempo_atual = pygame.time.get_ticks()

        self.intervalo_animacao = self.velocidades_animacao[
            self.animacao_atual
        ]

        if tempo_atual - self.ultimo_update_animacao >= self.intervalo_animacao:

            self.ultimo_update_animacao = tempo_atual

            quadros = self.animacoes[self.animacao_atual]

            if self.quadro_atual < len(quadros) - 1:
                self.quadro_atual += 1

            else:

                if self.morrendo:
                    self.morrendo = False
                    self.morto = True

                elif self.atacando:
                    self.atacando = False
                    self.animacao_atual = "andar"
                    self.quadro_atual = 0

                else:
                    self.quadro_atual = 0

    # Recebe dano
    def receber_dano(self, dano):

        if self.morrendo or self.morto:
            return

        self.vida -= dano

        if self.vida <= 0:

            self.vida = 0

            self.atacando = False
            self.morrendo = True

            self.animacao_atual = "morrer"
            self.quadro_atual = 0

            self.ultimo_update_animacao = pygame.time.get_ticks()

    def esta_vivo(self):
        return not self.morto

    # Desenha o inimigo
    def desenhar(self, tela):

        if self.esta_vivo():

            imagem = self.animacoes[
                self.animacao_atual
            ][self.quadro_atual]

            if self.direcao == -1:
                imagem = pygame.transform.flip(
                    imagem,
                    True,
                    False
                )

            tela.blit(
                imagem,
                (self.rect.x, self.rect.y - 10)
            )