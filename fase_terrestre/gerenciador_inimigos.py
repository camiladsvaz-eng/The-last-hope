class GerenciadorInimigos:

    def __init__(self):
        self.inimigos = []

    def adicionar_inimigo(self, inimigo):
        self.inimigos.append(inimigo)

    def atualizar(self, largura_tela, plataformas):
        for inimigo in self.inimigos:
            if inimigo.esta_vivo():
                inimigo.mover(largura_tela, plataformas)

    def desenhar(self, tela):
        for inimigo in self.inimigos:
            inimigo.desenhar(tela)

    def todos_derrotados(self):
        return not any(
            inimigo.esta_vivo()
            for inimigo in self.inimigos
        )
