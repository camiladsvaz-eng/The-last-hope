import pygame
def verificar_colisao(objeto_a, objeto_b):
    # Retorna True se os retângulos dos dois objetos colidirem.
    return objeto_a.rect.colliderect(objeto_b.rect)