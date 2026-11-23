
import pygame


class Personagem:
    def __init__(self, x, y, largura, altura, velocidade, vida):
        # Posicao e dimensoes
        self.rect = pygame.Rect(x, y, largura, altura)

        # Caracteristicas gerais
        self.velocidade = velocidade
        self.vida = vida
        self.vida_maxima = vida

        # Movimentacao
        self.velocidade_y = 0
        self.gravidade = 0.8
        self.forca_pulo = -16
        self.no_chao = False
        self.pulo_solicitado = False
        self.direcao = 1

        # Imagens e animacoes
        self.animacoes = {}
        self.animacao_atual = "idle"
        self.quadro_atual = 0
        self.imagem = None
        self.velocidade_animacao = 100
        self.ultimo_quadro = 0
        self.animacao_finalizada = False
        self.loop_animacao = True

    # Sistema de vida
    def receber_dano(self, dano):
        self.vida -= dano

        if self.vida < 0:
            self.vida = 0

    def esta_vivo(self):
        return self.vida > 0

    # Movimentacao horizontal
    def mover_horizontal(self, direcao, plataformas=[]):
        self.rect.x += direcao * self.velocidade

        if direcao != 0:
            self.direcao = direcao

        for plataforma in plataformas:
            if self.rect.colliderect(plataforma):
                if direcao > 0:
                    self.rect.right = plataforma.left
                elif direcao < 0:
                    self.rect.left = plataforma.right

    # Pulo
    def pular(self):
        if self.no_chao:
            self.velocidade_y = self.forca_pulo
            self.no_chao = False

    # Gravidade e colisoes verticais
    def aplicar_gravidade(self, plataformas=None):
        if plataformas is None:
            plataformas = []

        # Executa o pulo solicitado
        if self.pulo_solicitado and self.no_chao:
            self.velocidade_y = self.forca_pulo
            self.no_chao = False
            self.pulo_solicitado = False

        # Guarda a posição anterior
        posicao_anterior = self.rect.copy()

        # Aplica gravidade
        self.velocidade_y += self.gravidade
        self.rect.y += round(self.velocidade_y)

        self.no_chao = False

        # Verifica colisões
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma):

                # Colisão ao cair
                if self.velocidade_y >= 0 and posicao_anterior.bottom <= plataforma.top:
                    self.rect.bottom = plataforma.top
                    self.velocidade_y = 0
                    self.no_chao = True

                # Colisão ao subir
                elif self.velocidade_y < 0 and posicao_anterior.top >= plataforma.bottom:
                    self.rect.top = plataforma.bottom
                    self.velocidade_y = 0

    # Carregamento de spritesheets
    def carregar_animacao(self, nome, imagem, largura_quadro, altura_quadro, linha=0):
        spritesheet = pygame.image.load(imagem).convert_alpha()

        quadros = []

        quantidade_colunas = spritesheet.get_width() // largura_quadro

        for coluna in range(quantidade_colunas):
            quadro = pygame.Rect(
                coluna * largura_quadro,
                linha * altura_quadro,
                largura_quadro,
                altura_quadro
            )

            imagem_quadro = spritesheet.subsurface(quadro)
            imagem_quadro = pygame.transform.scale(
                imagem_quadro,
                (self.rect.width, self.rect.height)
            )

            quadros.append(imagem_quadro)

        self.animacoes[nome] = quadros


    # Escolha da animacao
    def definir_animacao(self, nome, loop=True):
        if nome not in self.animacoes:
            return

        if self.animacao_atual != nome:
            self.animacao_atual = nome
            self.quadro_atual = 0
            self.ultimo_quadro = pygame.time.get_ticks()
            self.animacao_finalizada = False
            self.loop_animacao = loop

    # Atualizacao da animacao
    def atualizar_animacao(self):
        if self.animacao_atual not in self.animacoes:
            return

        quadros = self.animacoes[self.animacao_atual]

        if not quadros:
            return

        agora = pygame.time.get_ticks()

        if agora - self.ultimo_quadro >= self.velocidade_animacao:
            self.ultimo_quadro = agora

            if self.quadro_atual < len(quadros) - 1:
                self.quadro_atual += 1

            elif self.loop_animacao:
                self.quadro_atual = 0

            else:
                self.animacao_finalizada = True

        self.imagem = quadros[self.quadro_atual]

    # Desenho na tela
    def desenhar(self, tela):
        if self.imagem is not None:
            imagem = pygame.transform.flip(
                self.imagem,
                self.direcao == -1,
                False
            )

            tela.blit(imagem, self.rect)

        else:
            pygame.draw.rect(tela, (40, 150, 220), self.rect)
