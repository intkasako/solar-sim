import pygame
import pygame.gfxdraw
from body import Body
from constants import G
import physics

pygame.init()
screen = pygame.display.set_mode(
    size=(800,600)
)
pygame.display.set_caption("Solar System Simulation")
clock = pygame.time.Clock()

sun = Body("Sun", (255, 255, 0), 30, 5000, [400, 300], [0, 0])
earth = Body("Earth", (0, 0, 255), 7, 1, [550, 300], [0, -3])
mars = Body("Mars", (255, 50, 50), 5, 0.6, [620, 300], [0, -2.5])

bodies = [sun, earth, mars]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            fx, fy = physics.calc_body_forces(G, bodies[i], bodies[j])
            physics.update_body(bodies[i], fx, fy)
            physics.update_body(bodies[j], -fx, -fy)

    screen.fill((0,0,0))
    for body in bodies:
        x, y = round(body.pos[0]), round(body.pos[1])
        pygame.gfxdraw.aacircle(screen, x, y, body.radius, body.color)
        pygame.gfxdraw.filled_circle(screen, x, y, body.radius, body.color)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()