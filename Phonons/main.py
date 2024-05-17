import pygame, math
from pygame.locals import *
from phonons import *

def main():
    win = pygame.display.set_mode((900,700))
    pygame.display.set_caption("Phonons")
    clock = pygame.time.Clock()
    frame_rate = 10
    lattice_object = Lattice(dimentions = (10,10), bond_strenght = 1.0, lattice_parameter = 50.0, point_size = 5)
    count = 0
    run = True    
    while run:

        win.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

        count += 1

        if count == 10:
            lattice_object.external_force_on_single_atom((10,0), (0,5))
        # if count == 12:
            # run = False
        lattice_object.update_lattice()
        lattice_object.draw_lattice(win)
        print(count)
        clock.tick(frame_rate)
        pygame.display.flip()

if __name__ == "__main__":
    main()
