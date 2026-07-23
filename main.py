import pygame
import pygame.gfxdraw
from body import Body
from constants import G
import physics
import random
import math

pygame.init()
screen = pygame.display.set_mode(
    size=(1200,800)
)
pygame.display.set_caption("Solar System Simulation")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 11)
ui_font = pygame.font.SysFont("Arial", 14)

SUN_POS = [600, 400]
SUN_MASS = 5000

def create_belt(n, min_dist, max_dist, color) -> list[Body]:
    bodies = []
    v = physics.calc_orbital_velocity
    for _ in range(n):
        dist = random.uniform(min_dist, max_dist)
        angle = random.uniform(0, 2 * math.pi)
        pos_x = SUN_POS[0] + dist * math.cos(angle)
        pos_y = SUN_POS[1] + dist * math.sin(angle)
        vel = v(G, SUN_MASS, dist)
        vel_x = -vel * math.sin(angle)
        vel_y = vel * math.cos(angle)
        radius = random.randint(1, 2)
        bodies.append(Body("", color, radius, 0.0001, [pos_x, pos_y], [vel_x, vel_y]))
    return bodies

def create_bodies(method="euler"):
    if method == "verlet":
        v = physics.calc_orbital_velocity
        return [
            Body("Sun", (255, 255, 0), 30, SUN_MASS, list(SUN_POS), [0, 0], fixed=True),
            Body("Mercury", (180, 180, 180), 3, 0.3, [660, 400], [0, -v(G, SUN_MASS, 60)]),
            Body("Venus", (255, 165, 0), 6, 0.8, [700, 400], [0, -v(G, SUN_MASS, 100)]),
            Body("Earth", (0, 0, 255), 7, 1, [770, 400], [0, -v(G, SUN_MASS, 170)]),
            Body("Mars", (255, 50, 50), 5, 0.6, [850, 400], [0, -v(G, SUN_MASS, 250)]),
            Body("Jupiter", (255, 200, 150), 12, 10, [950, 400], [0, -v(G, SUN_MASS, 350)]),
            Body("Saturn", (230, 210, 170), 10, 8, [1100, 400], [0, -v(G, SUN_MASS, 500)]),
            Body("Uranus", (170, 220, 230), 8, 5, [1300, 400], [0, -v(G, SUN_MASS, 700)]),
            Body("Neptune", (50, 50, 255), 7, 5, [1550, 400], [0, -v(G, SUN_MASS, 950)]),
        ]
    return [
        Body("Sun", (255, 255, 0), 30, SUN_MASS, list(SUN_POS), [0, 0], fixed=True),
        Body("Venus", (255, 165, 0), 6, 0.8, [700, 400], [0, -2.8]),
        Body("Earth", (0, 0, 255), 7, 1, [770, 400], [0, -2.6]),
        Body("Mars", (255, 50, 50), 5, 0.6, [850, 400], [0, -2.4]),
        Body("Jupiter", (255, 200, 150), 12, 10, [950, 400], [0, -2.1]),
    ]

integrator = "verlet"
bodies = create_bodies(integrator)
asteroids = create_belt(30, 270, 330, (150, 150, 150)) + create_belt(20, 1000, 1200, (100, 130, 160))
pause = False
running = True
speed = 1
zoom = 1.0
center = [600, 400]
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
            if event.key == pygame.K_v:
                integrator = "verlet" if integrator == "euler" else "euler"
                bodies = create_bodies(integrator)
                asteroids = create_belt(30, 270, 330, (150, 150, 150)) + create_belt(20, 1000, 1200, (100, 130, 160)) if integrator == "verlet" else []
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                zoom *= 1.1
            else:
                zoom = max(0.2, zoom / 1.1)

    if not pause:
        all_bodies = bodies + asteroids
        for _ in range(speed):
            if integrator == "euler":
                physics.step_euler(G, all_bodies)
            else:
                physics.step_verlet(G, all_bodies)
            for body in bodies:
                body.update_history()

    def to_screen(pos):
        sx = center[0] + (pos[0] - center[0]) * zoom
        sy = center[1] + (pos[1] - center[1]) * zoom
        return round(sx), round(sy)

    screen.fill((0,0,0))
    for body in bodies:
        text = font.render(body.name, True, (255,255,255))
        x, y = to_screen(body.pos)
        r = max(2, round(body.radius * zoom))
        pygame.gfxdraw.aacircle(screen, x, y, r, body.color)
        pygame.gfxdraw.filled_circle(screen, x, y, r, body.color)
        screen.blit(text, (x + r + 2, y - 5))
        if len(body.pos_history) > 1:
            trail = [to_screen(p) for p in body.pos_history]
            pygame.draw.lines(screen, body.color, False, trail, 1)
    for asteroid in asteroids:
        x, y = to_screen(asteroid.pos)
        pygame.draw.circle(screen, asteroid.color, (x, y), max(1, round(asteroid.radius * zoom)))

    fps = int(clock.get_fps())
    status = "PAUSED" if pause else f"Speed: {speed}x"
    screen.blit(ui_font.render(f"{status}  |  Integrator: {integrator.upper()}  |  FPS: {fps}", True, (255, 255, 255)), (10, 10))
    screen.blit(ui_font.render("SPACE: pause  |  UP: faster  |  DOWN: slower  |  V: integrator  |  SCROLL: zoom", True, (150, 150, 150)), (10, 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()