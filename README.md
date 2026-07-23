# solar-sim

2D solar system simulator with Newtonian gravity, built with Python and Pygame.

![Python](https://img.shields.io/badge/Python-3.12+-blue) ![Pygame](https://img.shields.io/badge/Pygame--CE-2.x-green)

## How to run

```bash
pip install pygame-ce numpy
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| SPACE | Pause / Resume |
| UP | Speed up simulation |
| DOWN | Slow down simulation |
| V | Toggle integrator (Euler / Verlet) |
| SCROLL | Zoom in / out |

## How it works

Each frame follows three steps:

1. Calculate gravitational force between every pair of bodies (`F = G * m1 * m2 / r^2`)
2. Update each body's velocity and position based on the resulting force
3. Draw everything on screen

Gravitational interaction is calculated pairwise: with N bodies, that's N*(N-1)/2 pairs per frame. Each pair produces a force applied to both bodies in opposite directions (Newton's third law).

## Integrators

The simulation supports two numerical integrators, switchable at runtime with the V key:

**Euler**: the simplest integrator. Updates velocity then position in one step. Works fine for visualization but doesn't conserve energy, which causes two visible artifacts:

- Orbits precess over time (the ellipse slowly rotates around the Sun)
- Orbits can gradually expand in long-running simulations

Runs with 4 planets (Venus, Earth, Mars, Jupiter) using hand-tuned velocities.

**Velocity Verlet**: a second-order integrator that calculates forces twice per step: before and after moving each body, then uses the average acceleration to update velocity. This conserves energy much better, producing stable orbits that hold their shape indefinitely.

Runs with all 8 planets (Mercury through Neptune) and an asteroid belt between Mars and Jupiter, using velocities calculated from the circular orbit formula `v = sqrt(G * M / r)`. Euler can't handle this many bodies at these distances without orbits breaking apart, which is a good demonstration of why the choice of integrator matters.

## Structure

```
main.py        # main loop, events, rendering
body.py        # Body class (position, velocity, mass, color)
physics.py     # gravity calculation and position updates
constants.py   # gravitational constant
```

## Design decisions

**Physics separated from Body**: force calculation and position updates live in `physics.py`, not as methods on the `Body` class. The class only holds data and position history. This keeps Body as a simple data structure and concentrates all physics logic in one place.

**Fixed Sun**: the Sun has a `fixed=True` attribute that prevents its position from being updated. This simplifies the simulation without significant loss of accuracy, since in the real solar system the Sun's movement relative to the planets is negligible.

**Made-up values**: masses, distances, and velocities don't correspond to the real solar system. They were tuned through trial and error (Euler) or calculated for circular orbits (Verlet) until the simulation looked visually stable and fit on screen.

**Asteroid belt and Kuiper belt**: two rings of small bodies (Verlet only). The asteroid belt sits between Mars and Jupiter (30 bodies), and the Kuiper belt extends beyond Neptune (20 bodies). Each body is placed at a random angle and distance using trigonometry, with a perpendicular velocity calculated from the orbital formula. They interact gravitationally with all other bodies, which produces emergent behavior: some asteroids get flung out of their orbits by close encounters with larger planets, then get pulled back by the Sun: the same gravitational perturbation that happens in the real solar system.

## Known limitations

**No moons**: satellites like the Moon can't realistically orbit a planet at this scale. The simulation compresses distances so much that the Sun's gravity dominates at every point. In reality the Moon orbits Earth because it's roughly 1/400th of the Earth-Sun distance away; in our simulation that ratio would be around 1/11, which isn't enough for Earth's gravity to hold a satellite against the Sun's pull.

## Dependencies

- [pygame-ce](https://pypi.org/project/pygame-ce/): rendering and input
- [numpy](https://pypi.org/project/numpy/): vector math
