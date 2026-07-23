import numpy as np
from body import Body

#F = G * m1 * m2 / r²

def calc_delta(first_body_pos : list[float], second_body_pos : list[float]) -> tuple[float]:
    first_body_pos = np.array(first_body_pos)
    second_body_pos = np.array(second_body_pos)
    return second_body_pos - first_body_pos

def calc_dist(delta : np.array):
    return np.sqrt(delta[0]**2 + delta[1]**2)

def calc_magnitude(gravity, first_mass, second_mass, dist):
    F = (gravity * first_mass * second_mass) / (dist**2)
    return F

def calc_body_forces(gravity, body1, body2):
    delta = calc_delta(body1.pos, body2.pos)
    dist = calc_dist(delta)
    if dist == 0:
        return 0, 0
    force = calc_magnitude(gravity, body1.mass, body2.mass, dist)
    fx = force * delta[0] / dist
    fy = force * delta[1] / dist
    return fx, fy

def update_body(body : Body, fx, fy):
    if body.fixed:
        return
    body.velocity[0] += fx / body.mass
    body.velocity[1] += fy / body.mass
    body.pos[0] += body.velocity[0]
    body.pos[1] += body.velocity[1]