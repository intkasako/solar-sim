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

## How it works

Each frame follows three steps:

1. Calculate gravitational force between every pair of bodies (`F = G * m1 * m2 / r^2`)
2. Update each body's velocity and position based on the resulting force
3. Draw everything on screen

Gravitational interaction is calculated pairwise: with N bodies, that's N*(N-1)/2 pairs per frame. Each pair produces a force applied to both bodies in opposite directions (Newton's third law).

## Structure

```
main.py        # main loop, events, rendering
body.py        # Body class (position, velocity, mass, color)
physics.py     # gravity calculation and position updates
constants.py   # gravitational constant
```

## Design decisions

**Physics separated from Body** — force calculation and position updates live in `physics.py`, not as methods on the `Body` class. The class only holds data and position history. This keeps Body as a simple data structure and concentrates all physics logic in one place.

**Fixed Sun** — the Sun has a `fixed=True` attribute that prevents its position from being updated. This simplifies the simulation without significant loss of accuracy, since in the real solar system the Sun's movement relative to the planets is negligible.

**Euler integration** — the simulation uses Euler's method to update positions: `vel += force/mass`, then `pos += vel`. It's the simplest integrator there is. It works fine for visualization, but has two visible side effects:

- Orbits precess over time (the ellipse slowly rotates around the Sun)
- Orbits can gradually expand in long-running simulations

These effects are numerical error, not real physics. An integrator like Velocity Verlet would fix this by conserving energy better.

**Made-up values** — masses, distances, and velocities don't correspond to the real solar system. They were tuned through trial and error until the orbits looked visually stable and fit on screen.

## Dependencies

- [pygame-ce](https://pypi.org/project/pygame-ce/) — rendering and input
- [numpy](https://pypi.org/project/numpy/) — vector math
