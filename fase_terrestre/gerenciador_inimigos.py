from fase_terrestre.inimigos_terrestres import InimigoTerrestre

class GerenciadorInimigos:

    def __init__(self):
        self.inimigos = []
        self.desbloqueio_realizado = False

    def adicionar_inimigo(self, inimigo):
        self.inimigos.append(inimigo)

    def atualizar(self, largura_tela, gerenciador_coletas):
        for inimigo in self.inimigos:
            inimigo.mover(largura_tela)

        if (
            self.inimigos
            and self.todos_derrotados()
            and not self.desbloqueio_realizado
        ):
            gerenciador_coletas.desbloquear_sobreviventes()
            self.desbloqueio_realizado = True

    def desenhar(self, tela):
        for inimigo in self.inimigos:
            inimigo.desenhar(tela)

    def todos_derrotados(self):
        return not any(inimigo.esta_vivo() for inimigo in self.inimigos)
