import pygame


from fase_espacial.nave import Nave
# from coletaveis.cristal import Cristal

class Jogo:

    def __init__(self):

        pygame.init()

   
        self.largura = 800
        self.altura = 600

        self.tela = pygame.display.set_mode((self.largura, self.altura))

        pygame.display.set_caption("THE LAST HOPE")

        self.relogio = pygame.time.Clock()
        self.fps = 60

      
        self.rodando = True

    
        self.nave = Nave(375, 500)
        # self.cristal = Cristal(200, 200)

    def processar_eventos(self):

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.rodando = False 
                

    def atualizar(self):

        teclas = pygame.key.get_pressed()

        self.nave.mover(teclas,self.largura,self.altura)

        #if not self.cristal.coletado:
            #if self.nave.retangulo.colliderect(self.cristal.retangulo):
                #print("Cristal coletado!")
                #self.cristal.coletado = True 

    def desenhar(self):

        self.tela.fill((10, 10, 30))
        self.nave.desenhar(self.tela)
        #self.cristal.desenhar(self.tela)


        pygame.display.flip()


    def executar(self):

        while self.rodando:

            self.processar_eventos()

            self.atualizar()

            self.desenhar()

            self.relogio.tick(self.fps)

        pygame.quit()