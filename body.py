
class Body():
    def __init__(self, name: str, color: tuple[int, int, int], radius: float, mass: float, pos: list[float], velocity: list[float]):
        self.name = name
        self.color = color
        self.radius = radius
        self.mass = mass
        self.pos = pos
        self.velocity = velocity

