import pygame
from constants import BRANCO, CIANO, AMARELO, VERDE, CINZA_HUD, SCREEN_HEIGHT


class GerenciadorColetas:
    """Gerencia os coletáveis da fase atual e preserva a contagem global entre fases."""

    def __init__(self, fase_inicial="espaco"):
        self.fase_atual = fase_inicial
        self.coletaveis = []
        self.contadores = {
            "cristal": 0,
            "peca_tecnologica": 0,
            "sobrevivente": 0,
        }
        self.fonte = pygame.font.SysFont("arial", 20, bold=True)

    def definir_fase(self, nova_fase):
        """Troca a fase atual e limpa os itens da fase anterior, preservando os contadores."""
        self.fase_atual = nova_fase
        self.coletaveis.clear()

    def adicionar_coletavel(self, coletavel):
        """Adiciona o coletável apenas se ele pertencer à fase atual."""
        if coletavel.fase != self.fase_atual:
            return False
        self.coletaveis.append(coletavel)
        return True

    def desbloquear_sobreviventes(self):
        """Libera o resgate dos sobreviventes quando os inimigos do planeta forem eliminados."""
        for item in self.coletaveis:
            if item.tipo == "sobrevivente":
                item.desbloquear()

    def resetar_tudo(self):
        """Zera coletáveis e contadores (útil ao reiniciar o jogo)."""
        self.coletaveis.clear()
        for chave in self.contadores:
            self.contadores[chave] = 0

    def atualizar(self, jogador):
        """Atualiza coletáveis, remove os que saíram da tela e contabiliza colisões."""
        for item in self.coletaveis[:]:
            item.atualizar()

            # Remove itens espaciais que saírem por baixo da tela
            if item.rect.top > SCREEN_HEIGHT:
                self.coletaveis.remove(item)
                continue

            if item.verificar_colisao(jogador):
                tipo, valor = item.coletar()
                if tipo in self.contadores:
                    self.contadores[tipo] += valor
                self.coletaveis.remove(item)

    def desenhar(self, tela):
        """Desenha todos os coletáveis ativos e o painel de contadores."""
        for item in self.coletaveis:
            item.desenhar(tela)
        self.desenhar_interface(tela)

    def desenhar_interface(self, tela):
        """Exibe os contadores individuais e a fase atual no canto superior esquerdo."""
        painel = pygame.Rect(10, 10, 240, 120)
        pygame.draw.rect(tela, CINZA_HUD, painel, border_radius=8)
        pygame.draw.rect(tela, BRANCO, painel, 2, border_radius=8)

        titulo_fase = "Fase: Espaço" if self.fase_atual == "espaco" else "Fase: Planeta"
        itens_hud = [
            (titulo_fase, BRANCO, 18),
            (f"Cristais: {self.contadores['cristal']}", CIANO, 44),
            (f"Peças Tech: {self.contadores['peca_tecnologica']}", AMARELO, 70),
            (f"Sobreviventes: {self.contadores['sobrevivente']}", VERDE, 96),
        ]

        for texto, cor, y in itens_hud:
            superficie_texto = self.fonte.render(texto, True, cor)
            tela.blit(superficie_texto, (22, y))

    def obter_contagem(self, tipo):
        """Retorna a quantidade atual coletada de um tipo específico."""
        return self.contadores.get(tipo, 0)