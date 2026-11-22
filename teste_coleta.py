import random
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PRETO, VERMELHO, BRANCO
from classes.coletaveis import Cristal, PecaTecnologica, Sobrevivente
from classes.gerenciador_coletas import GerenciadorColetas


class JogadorProvisorio:
    """Representa temporariamente a Nave (espaço) ou o Personagem (planeta)."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.velocidade = 5

    def atualizar(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidade
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.rect.y += self.velocidade

        # Mantém o jogador dentro dos limites da tela
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def desenhar(self, tela):
        pygame.draw.rect(tela, VERMELHO, self.rect)


def carregar_fase_espaco(gerenciador):
    gerenciador.definir_fase("espaco")
    # Cristais e peças descendo pela tela (estilo Atari)
    for _ in range(3):
        x = random.randint(60, SCREEN_WIDTH - 60)
        y = random.randint(-120, 120)
        gerenciador.adicionar_coletavel(Cristal(x, y, velocidade_y=2))

    for _ in range(2):
        x = random.randint(60, SCREEN_WIDTH - 60)
        y = random.randint(-120, 120)
        gerenciador.adicionar_coletavel(PecaTecnologica(x, y, velocidade_y=2))


def carregar_fase_planeta(gerenciador):
    gerenciador.definir_fase("terrestre")
    # Sobrevivente começa bloqueado (cinza) até os inimigos serem derrotados
    gerenciador.adicionar_coletavel(Sobrevivente(650, 420, desbloqueado=False))


def main():
    pygame.init()
    tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Teste Semana 1 - Sistema de Coleta")
    relogio = pygame.time.Clock()
    fonte_ajuda = pygame.font.SysFont("arial", 16)

    jogador = JogadorProvisorio(380, 450)
    gerenciador = GerenciadorColetas(fase_inicial="espaco")
    carregar_fase_espaco(gerenciador)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    carregar_fase_espaco(gerenciador)
                elif evento.key == pygame.K_2:
                    carregar_fase_planeta(gerenciador)
                elif evento.key == pygame.K_e:
                    gerenciador.desbloquear_sobreviventes()
                elif evento.key == pygame.K_r:
                    gerenciador.resetar_tudo()
                    carregar_fase_espaco(gerenciador)

        jogador.atualizar()
        gerenciador.atualizar(jogador)

        tela.fill(PRETO)
        jogador.desenhar(tela)
        gerenciador.desenhar(tela)

        # Legenda de comandos no rodapé para facilitar os testes
        legenda = "WASD/Setas: Mover | [1] Espaço | [2] Planeta | [E] Eliminar inimigos (libera sobrevivente) | [R] Resetar"
        texto_ajuda = fonte_ajuda.render(legenda, True, BRANCO)
        tela.blit(texto_ajuda, (12, SCREEN_HEIGHT - 28))

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()