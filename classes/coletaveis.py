import pygame
import math
from constants import CIANO, AMARELO, VERDE
from utils.collision import verificar_colisao


class Coletavel:
    """Classe-base para todos os objetos coletáveis do jogo."""

    def __init__(
        self,
        x,
        y,
        largura,
        altura,
        tipo,
        fase,
        cor,
        valor=1,
        velocidade_y=0,
        desbloqueado=True,
        caminho_imagem=None,
    ):
        self.tipo = tipo
        self.fase = fase  # "espaco" ou "terrestre"
        self.valor = valor
        self.cor = cor
        self.velocidade_y = velocidade_y
        self.desbloqueado = desbloqueado
        self.coletado = False

        self.y_inicial = y
        self.tempo = 0

        self.rect = pygame.Rect(x, y, largura, altura)
        self.imagem = None

        if caminho_imagem:
            img = pygame.image.load(caminho_imagem).convert_alpha()
            self.imagem = pygame.transform.scale(img, (largura, altura))

    def atualizar(self):
        """Atualiza posição/animação do coletável."""
        if self.coletado:
            return

        if self.velocidade_y != 0:
            self.rect.y += self.velocidade_y
        else:
            self.tempo += 0.08
            self.rect.y = int(self.y_inicial + math.sin(self.tempo) * 4)

    def desenhar(self, tela):
        """Desenha o coletável na tela se ainda não tiver sido coletado."""
        if self.coletado:
            return

        if self.imagem:
            tela.blit(self.imagem, self.rect)
        else:
            pygame.draw.rect(tela, self.cor, self.rect, border_radius=6)

    def verificar_colisao(self, jogador):
        """Verifica colisão apenas se o item não foi coletado e está desbloqueado."""
        if self.coletado or not self.desbloqueado:
            return False
        return verificar_colisao(self, jogador)

    def coletar(self):
        """Marca o objeto como coletado e retorna seu tipo e valor."""
        if not self.coletado and self.desbloqueado:
            self.coletado = True
            return self.tipo, self.valor
        return None, 0


class Cristal(Coletavel):
    """Cristal de energia — coletável exclusivo da fase espacial."""

    def __init__(self, x, y, velocidade_y=0, caminho_imagem=None):
        super().__init__(
            x=x,
            y=y,
            largura=24,
            altura=24,
            tipo="cristal",
            fase="espaco",
            cor=CIANO,
            valor=1,
            velocidade_y=velocidade_y,
            desbloqueado=True,
            caminho_imagem=caminho_imagem,
        )

    def desenhar(self, tela):
        if self.coletado:
            return
        if self.imagem:
            tela.blit(self.imagem, self.rect)
        else:
            cx, cy = self.rect.center
            meio_l = self.rect.width // 2
            meio_a = self.rect.height // 2
            pontos = [
                (cx, cy - meio_a),
                (cx + meio_l, cy),
                (cx, cy + meio_a),
                (cx - meio_l, cy),
            ]
            pygame.draw.polygon(tela, self.cor, pontos)


class PecaTecnologica(Coletavel):
    """Peça tecnológica — coletável exclusivo da fase espacial."""

    def __init__(self, x, y, velocidade_y=0, caminho_imagem=None):
        super().__init__(
            x=x,
            y=y,
            largura=26,
            altura=26,
            tipo="peca_tecnologica",
            fase="espaco",
            cor=AMARELO,
            valor=1,
            velocidade_y=velocidade_y,
            desbloqueado=True,
            caminho_imagem=caminho_imagem,
        )


class Sobrevivente(Coletavel):
    """Sobrevivente — único coletável da fase terrestre, liberado após eliminar os inimigos."""

    def __init__(self, x, y, desbloqueado=False, caminho_imagem=None):
        super().__init__(
            x=x,
            y=y,
            largura=24,
            altura=36,
            tipo="sobrevivente",
            fase="terrestre",
            cor=VERDE,
            valor=1,
            velocidade_y=0,
            desbloqueado=desbloqueado,
            caminho_imagem=caminho_imagem,
        )

    def desbloquear(self):
        """Libera o sobrevivente para ser resgatado após os inimigos serem derrotados."""
        self.desbloqueado = True

    def desenhar(self, tela):
        if self.coletado:
            return

        # Cor mais apagada enquanto ainda há inimigos no planeta
        cor_atual = self.cor if self.desbloqueado else (120, 120, 120)

        if self.imagem:
            tela.blit(self.imagem, self.rect)
        else:
            cabeca_centro = (self.rect.centerx, self.rect.top + 8)
            pygame.draw.circle(tela, cor_atual, cabeca_centro, 7)
            corpo = pygame.Rect(self.rect.left + 4, self.rect.top + 16, self.rect.width - 8, 20)
            pygame.draw.rect(tela, cor_atual, corpo, border_radius=4)