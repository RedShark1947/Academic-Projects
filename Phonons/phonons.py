import math, pygame
from pygame.locals import *

class LatticePoint:
    def __init__(self, index,  bond_strenght = 1.0, lattice_parameter = 50.0, point_size = 1, mass = 10) -> None:
        
        self.bond_strenght = bond_strenght #Spring constant (k)
        self.lattice_parameter = lattice_parameter #Bond lenght (a)
        self.point_size = point_size
        self.index = index
        self.mass = mass
        self.velocity = (0,0)
        self.acceleration = (0,0)
        # Setting up positions 
        self.initial_position = ((self.index[0] * self.lattice_parameter) + 200, (index[1] * self.lattice_parameter) + 150)
        self.current_position = self.initial_position
        self.adjacent_displacement = [[0,0],[0,0],[0,0],[0,0]]
        # Pygame rect
        self.rect = pygame.FRect(self.initial_position[0], self.initial_position[1], self.point_size, self.point_size)
    
    def displacement(self):
        rst_force = self.restorative_force()
        # net_force = (self.ext_force[0] + self.restorative_force()[0], self.ext_force[1] + self.restorative_force()[1])
        acceleration = (self.acceleration[0] + (rst_force[0]/self.mass), self.acceleration[1] + (rst_force[1]/self.mass))
        self.velocity = (self.velocity[0] + acceleration[0], self.velocity[1] + acceleration[1])
        # trigger each frame
        self.rect.move_ip(self.velocity[0], self.velocity[1])
        # Changing current position to align with displacement 

        self.current_position = (self.current_position[0] + self.velocity[0], self.current_position[1] + self.velocity[1])
        # print(self.index, (self.initial_position[0] - self.current_position[0], self.initial_position[1] - self.current_position[1]), self.velocity)
        displacement = (self.initial_position[0] - self.current_position[0], self.initial_position[1] - self.current_position[1])
        return displacement
    
    def external_force(self, force = (0,0)):
        if force != (0,0):
            self.acceleration = (force[0]/self.mass, force[1]/self.mass)
            self.velocity = (self.velocity[0] + self.acceleration[0], self.velocity[1] + self.acceleration[1])

    def restorative_force(self):

        # For displacement, first adjacent atom considered is directly above the current atom, 
        # second is directly below, third is on the right and fourth is on the left 

        x = self.current_position[0] - self.initial_position[0] 
        y = self.current_position[1] - self.initial_position[1]
        k = self.bond_strenght
        a = self.lattice_parameter
        aad = self.adjacent_displacement
        Q3 = math.atan(y/(a+x))
        Q4 = math.atan(y/(a-x))

        if x == 0: 
            Q1 = 0
            Q2 = 0
        else:
            Q1 = math.atan((a+y)/x)
            Q2 = math.atan((a-y)/x)
        if x == 0 and aad == [(0,0), (0,0), (0,0), (0,0)]:
                Fx = 0
        else:   
            Fx = -1 * k * ((math.sqrt((a + y + aad[0][1])**2 + (x + aad[0][0])**2) - a) * math.cos(Q1) - 
                        (math.sqrt((a - y + aad[1][1])**2 + (x + aad[1][0])**2) - a) * math.cos(Q2) +
                        (math.sqrt((a + x + aad[2][0])**2 + (y + aad[2][1])**2) - a) * math.cos(Q3) -
                        (math.sqrt((a - x + aad[3][0])**2 + (y + aad[3][1])**2) - a) * math.cos(Q4))
         
        if y == 0 and aad == [(0,0), (0,0), (0,0), (0,0)]:
            Fy = 0
        else:            
            Fy = -1 * k * ((math.sqrt((a + y - aad[0][1])**2 + (x - aad[0][0])**2) - a) * math.sin(Q1) - 
                        (math.sqrt((a - y + aad[1][1])**2 + (x + aad[1][0])**2) - a) * math.sin(Q2) +
                        (math.sqrt((a + x - aad[2][0])**2 + (y - aad[2][1])**2) - a) * math.sin(Q3) -
                        (math.sqrt((a - x + aad[3][0])**2 + (y + aad[3][1])**2) - a) * math.sin(Q4))
            
        if self.index == (0, 5):
            print(self.index, Fx, Fy, x, y, aad)
        return (Fx, Fy)

    def draw(self, surface, colour = (255, 0, 0)):
        pygame.draw.rect(surface, colour, self.rect)

class Lattice:
    def __init__(self, dimentions, bond_strenght, lattice_parameter, point_size) -> None:

        self.lattice_matrix = []
        for i in range(dimentions[1]):
            self.lattice_matrix.append([])
            for j in range(dimentions[0]):
                self.lattice_matrix[i].append(LatticePoint((i,j), bond_strenght, lattice_parameter, point_size))

    def update_lattice(self):
        for row in range(len(self.lattice_matrix)):
            for element in range(len(self.lattice_matrix[row])):
                displacement = self.lattice_matrix[row][element].displacement()

                #check displacement function for why the displacements are positioned this way

                if row > 0:
                    self.lattice_matrix[row - 1][element].adjacent_displacement[1] = displacement
                if row < len(self.lattice_matrix) - 1:
                    self.lattice_matrix[row + 1][element].adjacent_displacement[0][0] = displacement[0]
                if element > 0:
                    self.lattice_matrix[row][element - 1].adjacent_displacement[2][0] = displacement[0]
                if element < len(self.lattice_matrix[row]) - 1:
                    self.lattice_matrix[row][element + 1].adjacent_displacement[3][0] += displacement[0]
                    
                if self.lattice_matrix[row][element].index == (0, 5):
                    self.lattice_matrix[row][element].adjacent_displacement[1] = (1, 1)
                    print('f', displacement)
                    
    def draw_lattice(self, surface):
        for row in self.lattice_matrix:
            for element in row:
                element.draw(surface)

    def external_force_on_single_atom(self, force, index):
        self.lattice_matrix[index[0]][index[1]].external_force(force)

    def external_force_on_whole_surface(self, force):
        for i in range(len(self.lattice_matrix)):
            self.lattice_matrix[i][0].external_force(force)
