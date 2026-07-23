import pygame
from body import Body

pygame.init()
screen = pygame.display.set_mode(
    size=(800,600)
)
pygame.display.set_caption("Solar System Simulation")
clock = pygame.time.Clock()

sun = Body("Sun", color=(255, 255, 0), radius=30, mass=100, pos=[400,300], velocity=[0,0])
earth = Body("Earth", (0, 0, 255), 7, 5, [200, 150], [0,0])

bodies = [sun, earth]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #####
    

    screen.fill((0,0,0))
    for body in bodies:
        pygame.draw.circle(screen, body.color, body.pos, body.radius)

    pygame.display.flip()
    clock.tick(60)


pygame.quit()