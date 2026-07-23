import pygame
import pygame.gfxdraw
from body import Body
from constants import G
import physics

pygame.init()
screen = pygame.display.set_mode(
    size=(1200,800)
)
pygame.display.set_caption("Solar System Simulation")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 11)
ui_font = pygame.font.SysFont("Arial", 14)

sun = Body("Sun", (255, 255, 0), 30, 5000, [600, 400], [0, 0])
venus = Body("Venus", (255, 165, 0), 6, 0.8, [700, 400], [0, -2.8])
earth = Body("Earth", (0, 0, 255), 7, 1, [770, 400], [0, -2.6])
mars = Body("Mars", (255, 50, 50), 5, 0.6, [850, 400], [0, -2.4])
jupiter = Body("Jupiter", (255, 200, 150), 12, 10, [950, 400], [0, -2.1])

bodies = [sun, venus, earth, mars, jupiter]
pause = False
running = True
speed = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause
            if event.key == pygame.K_UP:
                speed += 1
            if event.key == pygame.K_DOWN:
                speed = max(1, speed - 1)

    if not pause:
        for _ in range(speed):
            for i in range(len(bodies)):
                for j in range(i + 1, len(bodies)):
                    fx, fy = physics.calc_body_forces(G, bodies[i], bodies[j])
                    physics.update_body(bodies[i], fx, fy)
                    physics.update_body(bodies[j], -fx, -fy)
                bodies[i].update_history()
            sun.pos = [600, 400]

    screen.fill((0,0,0))
    for body in bodies:
        text = font.render(body.name, True, (255,255,255))
        x, y = round(body.pos[0]), round(body.pos[1])
        pygame.gfxdraw.aacircle(screen, x, y, body.radius, body.color)
        pygame.gfxdraw.filled_circle(screen, x, y, body.radius, body.color)
        screen.blit(text, ((body.pos[0] + body.radius + 2),( body.pos[1] + body.radius + 2)))
        if len(body.pos_history) > 1:
            pygame.draw.lines(screen, body.color, False, body.pos_history, 1)

    status = "PAUSED" if pause else f"Speed: {speed}x"
    screen.blit(ui_font.render(status, True, (255, 255, 255)), (10, 10))
    screen.blit(ui_font.render("SPACE: pause  |  UP: faster  |  DOWN: slower", True, (150, 150, 150)), (10, 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()