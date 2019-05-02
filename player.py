class Player:
    def __init__(self, name='Dawid!', x = 0, y = 0, orient='down'):
        self.name = name
        self.health = 100
        self.x = x
        self.y = y
        self.orient = orient
        self.money = 0
        self.mov_counter = 0
        self.ammo = 0
        self.marked = False
