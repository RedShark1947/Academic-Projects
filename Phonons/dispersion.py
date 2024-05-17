import numpy as np
import pygame

class latticept():
    def __init__(self,K,C,a,m,index):
        self.K = K
        self.C = C
        self.a = a
        self.m = m
        self.index = index
        self.point = pygame.FRect(self.pos)

class lattice():
    def __init__(self, length, K, C, a, m) -> None:
        self.length = int(length)
        self.lat = []
        for i in range(self.length):
            row = []
            for j in range(self.length):
                p = latticept(K,C,a,m,(i,j))
                row.append(p)
            self.lat.append(row)


def dispersion(K,C,a,m):

    w = 2*((C/m)**(0.5))*(abs(np.sin(K*a/2)))

    return w

def main():
    win = pygame.display.set_mode((500,500))
    clock = pygame.time.Clock()
    frame_rate = 60


    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        clock.tick(frame_rate)
        pygame.display.flip()

main()




