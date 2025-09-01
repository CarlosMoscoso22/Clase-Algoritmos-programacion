import pygame 

pygame.init()
ventana= pygame.display.pygame.display.set_mode((400, 300))
pygame.display.pygame.display.set_caption("mi primer juego")

AZUL=(0,0,225)
ejecutando=True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type ==pygame.QUIT:
            ejecutando=False
        ventana.fill(AZUL)
        pygame.display.flip()
        pygame.quit()