import time
import pygame
import random
import math

width, height = 500, 500
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Evolution sim")
deadcells = []
population = 0
masterpass = False
nextpass = False
alphabet = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", 'P', "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
]
no_food = False
class Cell:
    def __init__(self, x, y, genetics={"health": 0, "speed": 0, "generation": -1, "name": ""}, type="predator"):
        global population
        if type != "food":
            population += 1
        self.x = x
        self.y = y
        self.health = genetics["health"]
        self.speed = genetics["speed"]
        self.type = type
        self.genetics = genetics
        self.surname = self.genetics['name'][int(len(self.genetics['name']) // 2):]
        self.color = genetics['color'] if type == "predator" else (0, 255, 0) if type == "food" else (255, 255, 255)
        self.family = genetics.get('family', None)
    def update(self):
        prevlocation = (self.x, self.y)
        global deadcells
        self.health -= 10
        if self.health <= 0:
            deadcells.append(self)
        highest_generation = 0
        for family in families.values():
            for c in family:
                if c.genetics['generation'] > highest_generation:
                    highest_generation = c.genetics['generation']
        if self.genetics['generation'] < highest_generation - 5:
            deadcells.append(self)
        food = []
        for family in families.values():
            for c in family:
                if c.type == "food":
                    food.append(c)
        closest_food = Cell(40000, 50000, type="food")
        for c in food:
            closeness_1 = math.sqrt((self.x - c.x) ** 2 + (self.y - c.y) ** 2)
            closeness_2 = math.sqrt((self.x - closest_food.x) ** 2 + (self.y - closest_food.y) ** 2)
            if closeness_1 < closeness_2:
                closest_food = c
        if math.sqrt((self.x - closest_food.x) ** 2 + (self.y - closest_food.y) ** 2) < self.speed:
            self.speed -= 1
        if closest_food.x > self.x:
            self.x += self.speed
        elif closest_food.x < self.x:
            self.x -= self.speed
        if closest_food.y > self.y:
            self.y += self.speed
        elif closest_food.y < self.y:
            self.y -= self.speed
        scheduled_for_removal = []
        for family in families.values():
            for c in family:
                if c == self:
                    pass
                elif c.type == "food":
                    if c.x == self.x - 1 and c.y == self.y:
                        self.health = self.genetics['health']
                        scheduled_for_removal.append(c)
                    elif c.x == self.x and c.y == self.y:
                        self.health = self.genetics['health']
                        scheduled_for_removal.append(c)
                    elif c.x == self.x + 1 and c.y == self.y:
                        self.health = self.genetics['health']
                        scheduled_for_removal.append(c)
                    elif c.x == self.x and c.y == self.y - 1:
                        self.health = self.genetics['health']
                        scheduled_for_removal.append(c)
                    elif c.x == self.x and c.y == self.y + 1:
                        self.health = self.genetics['health']
                        scheduled_for_removal.append(c)
                if (c.x, c.y) == prevlocation:
                    self.x = prevlocation[0]
                    self.y = prevlocation[1]
        had_food = False
        if scheduled_for_removal:
            had_food = True
            for c in scheduled_for_removal:
                for family in families.values():
                    if c in family:
                        family.remove(c)
                else:
                    print(f"failed to remove {c.x},{c.y} : {c.genetics['name']}")
        scheduled_for_removal = []
        def hadfood():pass
        if had_food:
            self.speed = self.genetics['speed']
            color_to_edit = random.randint(0, 2)
            color = [self.color[0], self.color[1], self.color[2]]
            color[color_to_edit] += random.randint(-10, 10)
            if color[color_to_edit] > 255:
                while color[color_to_edit] > 255:
                    color[color_to_edit] += random.randint(-10, 0)
            if color[color_to_edit] < 0:
                while color[color_to_edit] < 0:
                    color[color_to_edit] += random.randint(0, 10)
            color = tuple(color)
            name = ""
            for i in range(int(len(self.genetics['name']) // 2)):
                name += random.choice(alphabet)
            name += self.surname
            family = self.family
            if random.random() < 0.1:
                name = ""
                for i in range(int(len(self.genetics['name']) // 2)):
                    name += random.choice(alphabet)
                name += self.surname
            families[family].append(
                Cell(
                    random.randint(0, 49),
                    random.randint(0, 49),
                    genetics={
                        "health": self.genetics["health"] + random.randint(-10, 10),
                        "speed": self.genetics["speed"] + random.randint(-1, 3),
                        "generation": self.genetics['generation'] + 1,
                        "color": color,
                        "name": name,
                        "family": family
                    },
                    type="predator"
                )
            )

families = {"food": []}
for i in range(10):
    x, y = random.randint(0, 49), random.randint(0, 49)
    if i != 0:
        for b in families.values():
            for c in b:
                while c.x == x and c.y == y:
                    x, y = random.randint(0, 49), random.randint(0, 49)
    name = ""
    for __ in range(6):
        name += random.choice(alphabet)
    c = Cell(x, y, genetics={"health": 100, "speed": 1, "generation": 0, "color": (255, 255, 255), "name": name, "family": name[len(name)//2]})
    if c.family not in families:
        families[c.family] = []
    families[c.family].append(c)
for i in range(5):
    x, y = random.randint(0, 49), random.randint(0, 49)
    c = Cell(x, y, type="food")
    families['food'].append(c)

def draw():
    global flags, threads, deadcells, population
    screen.fill((0, 0, 0))
    for family in families.values():
        for c in family:
            if c.type == "predator":
                c.update()
    for c in reversed(deadcells):
        for family in families.values():
            if c in family:
                if not family == families['food'] and not c.genetics['name'] == "":
                    family.remove(c)
        else:
            print(f"failed to remove {c.x},{c.y} : {c.genetics['name']}")

    food = 0
    for family in families.values():
        for c in family:
            if c.type == "food":
                food += 1
    if food < 20 and not no_food:
        family = families['food']
        family.append(Cell(random.randint(0, 49), random.randint(0, 49), type="food"))
    deadcells = []
    for family in families.values():
        for c in family:
            surf = pygame.Surface((10, 10))
            surf.fill(tuple(c.color))
            screen.blit(surf, (c.x * 10, c.y * 10))
    pygame.display.update()

clickcounter = 0
preveiousclicked = Cell(99, 99, genetics={"health": 0, "speed": 0, "generation": 0, "color": (0, 0, 0), "name": ""})

while True:
    oldfamilies = families.copy()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                masterpass = not masterpass
            elif event.key == pygame.K_f:
                nextpass = True
                masterpass = False
            elif event.key == pygame.K_g:
                no_food=not no_food
            elif event.key == pygame.K_p:
                        best_health = Cell(99, 99, {"health": 0, "speed": 0, "generation": 0, "color": (0, 0, 0), "name": ""})
                        best_speed = Cell(99, 99, {"health": 0, "speed": 0, "generation": 0, "color": (0, 0, 0), "name": ""})
                        best_generation = Cell(99, 99, {"health": 0, "speed": 0, "generation": 0, "color": (0, 0, 0), "name": ""})
                        for family in families.values():
                            for c in family:
                                if c.type == "predator":
                                    if c.genetics['health'] > best_health.genetics['health']:
                                        best_health = c
                                    if c.genetics['speed'] > best_speed.genetics['speed']:
                                        best_speed = c
                                    if c.genetics['generation'] > best_generation.genetics['generation']:
                                        best_generation = c
                        print(f"""{best_health.genetics}
{best_speed.genetics}
{best_generation.genetics}""")

        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            x, y = int(x // 10), int(y // 10)
            dontspawn = False
            for family in families.values():
                for c in family:
                    if c.x == x and c.y == y and c.type == "predator" and masterpass:
                        dontspawn = True
                        if c == preveiousclicked or clickcounter == 0:
                            clickcounter += 1
                            preveiousclicked = c
                        if c != preveiousclicked:
                            clickcounter = 0
                        if clickcounter >= 2:
                            deadcells.append(c)
                        print(clickcounter)
                        print(f"cell at {x},{y} : {c.genetics['name']} {c.color} {c.genetics}")
            if not dontspawn:
                name = ""
                for __ in range(6):
                    name += random.choice(alphabet)
                c = Cell(x, y, genetics={"health": 100, "speed": 1, "generation": 0, "color": (255, 255, 255), "name": name, "family": name[len(name)//2]})
                if c.family not in families:
                    families[c.family] = []
                families[c.family].append(c)
    if masterpass:
        continue
    draw()
    if nextpass:
        nextpass = False
        masterpass = True