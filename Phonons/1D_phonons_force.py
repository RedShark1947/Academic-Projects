import math, pygame
from pygame.locals import *

class LatticePoint:
    def __init__(self, index,  bond_strenght = 1.0, lattice_parameter = 50.0, point_size = 1, mass = 20) -> None:
        
        self.bond_strenght = bond_strenght #Spring constant (k)
        self.lattice_parameter = lattice_parameter #Bond lenght (a)
        self.point_size = point_size
        self.index = index
        self.mass = mass
        self.velocity = 0
        self.acceleration = 0

        # Setting up positions 
        self.initial_position = ((self.index * self.lattice_parameter) + 200, 150)
        self.current_position = self.initial_position
        self.adjacent_displacement = [0,0]

        # Pygame rect
        self.rect = pygame.FRect(self.initial_position[0], self.initial_position[1], self.point_size, self.point_size)
    
    def displacement(self):
        net_force = self.restorative_force()
        self.acceleration = net_force/self.mass
        self.velocity += self.acceleration
        # trigger each frame
        self.rect.move_ip(self.velocity,0)
        # Changing current position to align with displacement 

        self.current_position = (self.current_position[0] + self.velocity, self.current_position[1])
        # print(self.index, (self.initial_position[0] - self.current_position[0], self.initial_position[1] - self.current_position[1]), self.velocity)
        displacement = self.initial_position[0] - self.current_position[0]
        
        print(self.index, self.current_position[0] - self.initial_position[0], self.velocity, self.acceleration)

        return displacement

    def external_force(self, force = (0,0)):
        if force != (0,0):
            acceleration = self.acceleration + force/self.mass
            self.velocity = self.velocity + acceleration

    def restorative_force(self):

        # For displacement, first adjacent atom considered is directly above the current atom, 
        # second is directly below, third is on the right and fourth is on the left 

        x = self.current_position[0] - self.initial_position[0]

        k = self.bond_strenght
        aad = self.adjacent_displacement
        
        if x == 0 and aad == [0, 0]:
                Fx = 0
        else:   
            Fx = -1 * k * ((2 * x) + aad[0] + aad[1])
            
        return (Fx)

    def draw(self, surface, colour = (255, 0, 0)):
        pygame.draw.rect(surface, colour, self.rect)

class Lattice:
    def __init__(self, dimentions, bond_strenght, lattice_parameter, point_size) -> None:

        self.lattice_matrix = []
        for i in range(dimentions):
            self.lattice_matrix.append(LatticePoint(i, bond_strenght, lattice_parameter, point_size))

    def update_lattice(self):
        for row in range(len(self.lattice_matrix)):
            displacement = self.lattice_matrix[row].displacement()
            
            if row > 0:
                self.lattice_matrix[row - 1].adjacent_displacement[0] = displacement

            if row < len(self.lattice_matrix) - 1:
                self.lattice_matrix[row + 1].adjacent_displacement[1] = displacement


    def draw_lattice(self, surface):
        for row in self.lattice_matrix:
            row.draw(surface)

    def external_force_on_single_atom(self, force, index):
        self.lattice_matrix[index].external_force(force)

def main():
    win = pygame.display.set_mode((900,700))
    pygame.display.set_caption("Phonons")
    clock = pygame.time.Clock()
    frame_rate = 10
    lattice_object = Lattice(dimentions = 5, bond_strenght = 1.0, lattice_parameter = 50.0, point_size = 5)
    count = 0
    run = True    
    while run:

        win.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

        count += 1

        if count == 10:
            lattice_object.external_force_on_single_atom(10, 0)
        
        lattice_object.update_lattice()
        lattice_object.draw_lattice(win)
        print(count)
        clock.tick(frame_rate)
        pygame.display.flip()

if __name__ == "__main__":
    main()
