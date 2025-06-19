import math
import pygame
import random

def solarinit(width, height):
    global multiplier, orbitmultiplier, solarscreen, planets, font
    global offset, follow

    multiplier = 0.5
    orbitmultiplier = 1.2
    solarscreen = pygame.Surface((width, height))
    follow = ""
    offset = [0, 0]

    planets = {
    "sun": {
        "x": round(width / 2),
        "y": round(height / 2),
        "radius": 15,
        "orbits": "",
        "orbitdistance": 3,
        "orbitspeed": 3,
        "color": (255, 204, 0)
    },
    "mercury": {
        "radius": 1,
        "orbits": "sun",
        "orbitdistance": 2,
        "orbitspeed": 4.8,
        "color": (169, 169, 169)
    },
    "venus": {
        "radius": 2,
        "orbits": "sun",
        "orbitdistance": 4.5,
        "orbitspeed": 3.5,
        "color": (218, 165, 32)
    },
    "earth": {
        "radius": 2,
        "orbits": "sun",
        "orbitdistance": 7.5,
        "orbitspeed": 3,
        "color": (0, 102, 204)
    },
    "mars": {
        "radius": 1,
        "orbits": "sun",
        "orbitdistance": 11,
        "orbitspeed": 2.4,
        "color": (255, 80, 0)
    },
    "jupiter": {
        "radius": 4,
        "orbits": "sun",
        "orbitdistance": 13,
        "orbitspeed": 1.3,
        "color": (204, 153, 102)
    },
    "saturn": {
        "radius": 3,
        "orbits": "sun",
        "orbitdistance": 20.5,
        "orbitspeed": 1,
        "color": (210, 180, 140)
    },
    "uranus": {
        "radius": 2,
        "orbits": "sun",
        "orbitdistance": 25,
        "orbitspeed": 0.7,
        "color": (173, 216, 230)
    },
    "neptune": {
        "radius": 2,
        "orbits": "sun",
        "orbitdistance": 28.5,
        "orbitspeed": 0.5,
        "color": (0, 0, 128)
    }
}


    for i in planets:
        if "x" not in planets[i]:
            planets[i]["x"] = 0
            planets[i]["y"] = 0
        if "degrees" not in planets[i]:
            planets[i]["degrees"] = 0
        planets[i]["radius"] = planets[i]["radius"] / 100 * width * multiplier
        planets[i]["orbitdistance"] = planets[i][
            "orbitdistance"] / 100 * width * orbitmultiplier

    planets["anchor"] = {"radius": 0, "orbitdistance": 0, "orbits": "", "x": 0, "y": 0}

    font = {
        'a': [2, 123, 13],
        'b': [12, 123, 123],
        'c': [123, 1, 123],
        'd': [12, 13, 12],
        'e': [123, 12, 123],
        'f': [123, 12, 1],
        'g': [12, 13, 123],
        'h': [13, 123, 13],
        'i': [123, 2, 123],
        'j': [23, 3, 123],
        'k': [13, 12, 13],
        'l': [1, 1, 123],
        'm': [123, 123, 13],
        'n': [123, 13, 13],
        'o': [123, 13, 123],
        'p': [123, 123, 1],
        'q': [12, 12, 3],
        'r': [123, 12, 13],
        's': [23, 2, 12],
        't': [123, 2, 2],
        'u': [13, 13, 123],
        'v': [13, 13, 2],
        'w': [13, 123, 123],
        'x': [13, 2, 13],
        'y': [13, 2, 2],
        'z': [12, 2, 23],
        '"': [13, 0, 0],
        "'": [2, 0, 0],
        '.': [0, 0, 2],
        ',': [0, 0, 21],
        '!': [2, 2, 2],
        '?': [123, 23, 2],
        ';': [8, 0, 21],
        ':': [8, 0, 2],
        '(': [23, 12, 23],
        ')': [21, 23, 21],
        '_': [0, 0, 123],
        '-': [0, 123, 0],
        '0': [23, 13, 12],
        '1': [12, 2, 123],
        '2': [12, 23, 23],
        '3': [3, 23, 12],
        '4': [13, 123, 3],
        '5': [23, 12, 12],
        '6': [1, 123, 123],
        '7': [123, 3, 3],
        '8': [23, 123, 12],
        '9': [123, 123, 3],
        ' ': [0, 0, 0]
    }
   
def solarupdate(width, height):
    global solarscreen, follow
    solarscreen.fill((0, 0, 0))
    for i in planets:
        if planets[i]["orbits"] != "":
            planets[i]["degrees"] += planets[i]["orbitspeed"] /5
            planets[i]["x"] = planets[planets[i]["orbits"]]["x"] + (
                planets[i]["orbitdistance"] +
                planets[planets[i]["orbits"]]["radius"] + planets[i]["radius"]
            ) * math.cos(math.radians(planets[i]["degrees"]))
            planets[i]["y"] = planets[planets[i]["orbits"]]["y"] + (
                planets[i]["orbitdistance"] +
                planets[planets[i]["orbits"]]["radius"] + planets[i]["radius"]
            ) * math.sin(math.radians(planets[i]["degrees"]))
        elif i != "anchor":
            planets[i]["x"] += planets["anchor"]["x"]
            planets[i]["y"] += planets["anchor"]["y"]
        if planets[i]["x"] + planets[i]["radius"] >= 0 and planets[i][
                "x"] - planets[i]["radius"] <= width and planets[i][
                    "y"] + planets[i]["radius"] >= 0 and planets[i][
                        "y"] - planets[i]["radius"] <= height and i != "anchor":
            pygame.draw.circle(solarscreen,planets[i]["color"],(math.ceil(planets[i]["x"]), math.ceil(planets[i]["y"])),math.floor(planets[i]["radius"]))

    for i in planets:
        position = 0
        if math.floor(
                planets[i]["radius"] * 2
        ) - 1 > 0 and i[0] != "*" and planets[i]["y"] - planets[i][
                "radius"] - 1 >= 0 and planets[i]["y"] - planets[i][
                    "radius"] - 4 <= height and planets[i]["x"] - len(
                        i) * 2 <= width and planets[i]["x"] + len(i) * 2 >= 0:
            for f in i:
                for y in range(len(font[f.lower()])):
                    for x in str(font[f.lower()][y]):
                        if x != "0":
                            solarscreen.set_at(
                                (math.ceil(planets[i]["x"] - len(i) * 2 +
                                           int(x) + position - 1),
                                 math.ceil(planets[i]["y"] -
                                           math.floor(planets[i]["radius"]) - 4 + y)),
                                (255, 255, 255))
                position += 4
    planets["anchor"]["x"] = 0
    planets["anchor"]["y"] = 0
    return solarscreen
