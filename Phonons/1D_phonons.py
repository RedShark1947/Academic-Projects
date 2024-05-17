import math, pygame
from pygame.locals import *

class latticept():
    def __init__(self,K,C,a,m,index):
        self.K = K
        self.C = C
        self.a = a
        self.m = m
        self.index = index
        self.pos = self.index * a
        self.rect = pygame.FRect(self.pos + 200, 200, 10, 10)

    def displacement(self, w, t, current_disp):
        x = math.cos((w * t) - (self.K * current_disp))
        print(x)
        return x

class lattice():
    def __init__(self, length, Y, C, a, m) -> None:
        self.length = int(length)
        self.lat = []
        self.C = C
        self.a = a
        self.m = m
        self.K = (2* math.pi) / Y
        for i in range(self.length):
            p = latticept(self.K,C,a,m,i)
            self.lat.append(p)
            
    def update_lattice(self, t):
        for i in self.lat:
            disp = i.displacement(dispersion(self.K, self.C, self.a, self.m), t, i.pos)
            i.rect.move_ip((disp, 0))
    def draw_lattice(self, surface):
        for i in self.lat:
            pygame.draw.rect(surface, (255,0,0),  i.rect)

def dispersion(K,C,a,m):

    w = 2*((C/m)**(0.5))*(abs(math.sin(K*a/2)))
    return w

def main():
    win = pygame.display.set_mode((900,700))
    pygame.display.set_caption("Phonons")
    clock = pygame.time.Clock()

    wavelenght = 0.0001
    lat = lattice(length = 10, Y = wavelenght, C = 1.0, a = 50.0, m = 10.0 )
    t = 0
    run = True    
    while run:
        win.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
        t += 1
        lat.update_lattice(t)
        lat.draw_lattice(win)

        clock.tick(60)
        pygame.display.flip()

if __name__ == "__main__":
    main()
