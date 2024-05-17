import math
import pygame
from pygame.locals import *
pygame.init()

def SHM_eqn(frequency_x, frequency_y, phase_diff, amp, frame, time_interval=1):

    y = amp * math.sin((frequency_y * frame/time_interval))
    x = amp * math.cos((frequency_x * frame/time_interval) + math.radians(phase_diff))

    return [x, -y]

def main():

    win_size = [900, 700]
    win = pygame.display.set_mode(win_size)
    pygame.display.set_caption("OrbitSim")
    clock = pygame.time.Clock()
    clock_speed = 120

    global time_interval, red                          
    time_interval = 2975

    #colours
    red = [255, 0, 0] 
    # fonts
    fnt = pygame.font.Font(filename="fonts\Minecraft.ttf", size=40)
    freqx = 30
    freqy = 10
    colour = red
  
    count_txt = fnt.render(str(freqx) + ':' + str(freqy), False, (255, 255, 255))
   
    phaze_diff = 120
    amp = 200
    frame = 0
    original_pos = SHM_eqn(freqx, freqy, phaze_diff, amp, 0, time_interval)
    pressed = False
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pressed = True
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    pressed = False

        if not pressed:   
            pos = SHM_eqn(freqx, freqy, phaze_diff, amp, frame, time_interval)
            rect = pygame.Rect(pos[0]+ (win_size[1] * 0.6), pos[1] + (win_size[1]/2), 2, 2)
            pygame.draw.rect(win, colour, rect)
            frame += 1
            
            if abs(pos[0] - original_pos[0]) < 1 and abs(pos[1] - original_pos[1]) < 1 and frame > ((10 * freqy) + 20):
                print(frame, freqy)
                print(original_pos, pos)
                win.fill((0,0,0))
                freqx += 0 
                freqy += 10
                count_txt = fnt.render(str(freqx) + ':' + str(freqy), False, (255, 255, 255))
                print(frame)
                frame = 0
                time_interval += 225 * (freqy/10)
                
        win.blit(count_txt, (600, 50))

        clock.tick(clock_speed)
        pygame.display.update()

if __name__ == "__main__":
    main()