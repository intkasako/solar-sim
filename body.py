
class Body():
    def __init__(self, name: str, color: tuple[int, int, int], radius: float, mass: float, pos: list[float], velocity: list[float]):
        self.name = name
        self.color = color
        self.radius = radius
        self.mass = mass
        self.pos = pos
        self.velocity = velocity
        self.pos_history = []

    def update_history(self):
        self.pos_history.append(list(self.pos))
        if len(self.pos_history) > 500:
            self.pos_history.pop(0)