import numpy as np
from body import Body

#F = G * m1 * m2 / r²

def _calc_delta(first_body_pos : list[float], second_body_pos : list[float]) -> tuple[float]:
    first_body_pos = np.array(first_body_pos)
    second_body_pos = np.array(second_body_pos)
    return second_body_pos - first_body_pos

def _calc_dist(delta : np.array):
    return np.sqrt(delta[0]**2 + delta[1]**2)

def _calc_magnitude(gravity, first_mass, second_mass, dist):
    F = (gravity * first_mass * second_mass) / (dist**2)
    return F

def calc_orbital_velocity(gravity, central_mass, distance):
    return np.sqrt(gravity * central_mass / distance)

def calc_body_forces(gravity, body1, body2):
    delta = _calc_delta(body1.pos, body2.pos)
    dist = _calc_dist(delta)
    if dist == 0:
        return 0, 0
    force = _calc_magnitude(gravity, body1.mass, body2.mass, dist)
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

def _calc_accelerations(gravity, bodies):
    accels = [[0.0, 0.0] for _ in bodies]
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            fx, fy = calc_body_forces(gravity, bodies[i], bodies[j])
            if not bodies[i].fixed:
                accels[i][0] += fx / bodies[i].mass
                accels[i][1] += fy / bodies[i].mass
            if not bodies[j].fixed:
                accels[j][0] -= fx / bodies[j].mass
                accels[j][1] -= fy / bodies[j].mass
    return accels

def step_euler(gravity, bodies):
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            fx, fy = calc_body_forces(gravity, bodies[i], bodies[j])
            update_body(bodies[i], fx, fy)
            update_body(bodies[j], -fx, -fy)

def step_verlet(gravity, bodies):
    accels = _calc_accelerations(gravity, bodies)

    for i, body in enumerate(bodies):
        if body.fixed:
            continue
        body.pos[0] += body.velocity[0] + 0.5 * accels[i][0]
        body.pos[1] += body.velocity[1] + 0.5 * accels[i][1]

    new_accels = _calc_accelerations(gravity, bodies)

    for i, body in enumerate(bodies):
        if body.fixed:
            continue
        body.velocity[0] += 0.5 * (accels[i][0] + new_accels[i][0])
        body.velocity[1] += 0.5 * (accels[i][1] + new_accels[i][1])