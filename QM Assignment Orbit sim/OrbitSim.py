import pygame
import math
from pygame.locals import *

pygame.init()

class Body:
    def __init__(self, name, mass, colour = [255, 0, 60], initial_velocity = [0,0], position = [0,0]) -> None:
        
        self.name = name
        self.mass = mass
        self.velocity = initial_velocity
        self.pos = position
        self.display_log_base = 1.3
        self.min_display_size = 10
        self.display_size = max(math.log(self.mass, self.display_log_base), self.min_display_size)
        self.colour = colour
        self.obj_rect = pygame.FRect(((self.pos[0] - self.display_size/2), (self.pos[1] - self.display_size/2)), (self.display_size, self.display_size))

    def move(self):
        self.pos[0] += self.velocity[0] 
        self.pos[1] += self.velocity[1]

    def draw(self):      
        self.obj_rect = pygame.FRect(((self.pos[0] - self.display_size/2), (self.pos[1] - self.display_size/2)),
                                      (self.display_size, self.display_size))

        pygame.draw.rect(win, self.colour, self.obj_rect)

class SolarSystem:
    def __init__(self) -> None:
        self.bodies = []

    def add_body(self, body):

        if type(body) == list:
            for i in body:
                self.bodies.append(i)
        else:
            self.bodies.append(body)

    def remove_body(self, list, body):
            list.remove(body)
 
    def update_all(self):
        for body in self.bodies:
            body.move()
            body.draw()

    @staticmethod
    def accelerate_due_to_gravity(first, second, distance, angle):
        G_const = 0.006673
        force = first.mass * second.mass / (distance ** 2) * G_const
        reverse = -1
        for body in first, second:
            acceleration = force / body.mass

            acc_x = acceleration * math.cos(math.radians(angle))
            acc_y = acceleration * math.sin(math.radians(angle))

            body.velocity = (body.velocity[0] + (reverse * acc_x), body.velocity[1] + (reverse * acc_y),)
            reverse = 1

    def check_collision(self, first, second, distance):

        if distance < first.display_size/2 + second.display_size/2:
            if first.mass <= second.mass:
                self.remove_body(self.bodies, first)
                second.velocity = self.momentum_transfer(first, second)
                second.mass += first.mass
            if first.mass >= second.mass: 
                self.remove_body(self.bodies, second)
                first.velocity = self.momentum_transfer(first, second)
                first.mass += second.mass
                
    def momentum_transfer(self, first, second):
        final_velocity = (((first.velocity[0] * first.mass) + (second.velocity[0] * second.mass))/(first.mass + second.mass), 
                          ((first.velocity[1] * first.mass) + (second.velocity[1] * second.mass))/(first.mass + second.mass)) 
        return final_velocity

    def calculate_all_body_interactions(self):
        bodies_copy = self.bodies.copy()
        for idx, first in enumerate(bodies_copy):
            for second in bodies_copy[idx + 1:]:

                distancex = second.pos[0] - first.pos[0] 
                distancey = second.pos[1] - first.pos[1]
                distance = math.sqrt(distancex**2 + distancey **2)

                if distancex == 0 and distancey > 0:
                    angle = 270
                elif distancex == 0 and distancey < 0:
                    angle = 90            
                else:
                    angle = math.degrees((math.atan(distancey/distancex)))
                                
                if distancex < 0 and distancey > 0:
                    angle += 360 
                if distancex > 0 and distancey > 0:
                    angle += 180
                if distancex > 0 and distancey < 0:
                    angle += 180
               
                self.accelerate_due_to_gravity(first, second, distance=distance, angle=angle)
                self.check_collision(first, second, distance=distance)

def main():

    global win, win_size, clock_speed, red, black

    black = (0, 0, 0)
    red = (205, 92, 92)
    win_size = [900, 700]
    win = pygame.display.set_mode(win_size)
    clock_speed = 30

    pygame.display.set_caption("OrbitSim")

    clock = pygame.time.Clock()

    ss = SolarSystem()
    
    # regular initial conditions
    Sun = Body("sun", 2000000, colour=(255, 255, 0), initial_velocity=[0,0], position=[450,350])
    p1 = Body("earth", 1, colour = (0,100,255), initial_velocity=(-4, 5), position=[644,350])
    p2 = Body("mars", 0.6, colour = (255, 0, 0), initial_velocity=(4, 2), position=[500,50])
    p3 = Body("venus", 4, initial_velocity=(5, 4), position=[400,550])
    p4 = Body("jupiter", 40, initial_velocity=(4,-4), position=[150, 150])
    m5 = Body("jupiter_moon", 0.1, initial_velocity=(-1,-6), position=[700, 400])
    
    ss.add_body(Sun)
    ss.add_body([p1, p2, p3, p4, m5])
    

    # two suns 
    # Sun1 = Body("sun", 2000000, colour=(255, 255, 0), initial_velocity=[6,-4], position=[300,300])
    # Sun2 = Body("sun", 2000000, colour=(255, 255, 0), initial_velocity=[-6,3], position=[400,400])

    # ss.add_body([Sun1, Sun2])
    
    #collision initial conditions

    # Sun = Body("sun", 200000, colour=[255, 255, 0], initial_velocity=[0,0], position=[450,350])
    # p1 = Body("earth", 60, colour = [0,100,255], initial_velocity=(2, -2), position=[110,150])
    # p2 = Body("mars", 6, colour = [255, 0, 0], initial_velocity=(-2, -2), position=[790,150])
    # p3 = Body("venus", 4, initial_velocity=(5, 4), position=[400,550])
    # p4 = Body("jupiter", 40, initial_velocity=(4,-4), position=[620, 620])
    # m5 = Body("jupiter_moon", 0.001, initial_velocity=(4,-1), position=[600, 600])
    
    # ss.add_body(Sun)
    # ss.add_body([p1, p2, p3, p4, m5])

    # Sun1 = Body("sun1", 2000, initial_velocity=[2,1], position=[400,300])
    # Sun2 = Body("sun2", 2000, initial_velocity=[1,2], position=[300,400])
    # Sun3 = Body("sun2", 2000, initial_velocity=[-0.5, -0.5], position=[500,500])
    # ss.add_body([Sun1, Sun2, Sun3])
    
    run = True

    while run:
        win.fill(black)
        
        ss.calculate_all_body_interactions()
        ss.update_all()

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
        
        clock.tick(clock_speed)
        pygame.display.update()
        if not run:
            pygame.quit()

    if not run:
        print("close")

if __name__ == "__main__":
    main()