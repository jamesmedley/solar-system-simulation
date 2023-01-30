import math
import time
import pygame
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
PLANET_IMAGES = ["resources/mercury.png", "resources/venus.png", "resources/earth.png", "resources/mars.png",
                 "resources/jupiter.png", "resources/saturn.png", "resources/uranus.png", "resources/neptune.png",
                 "resources/pluto.png"]
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

G = 6.67 * (10 ** -11)
simulating = True
timestep = 50000  # seconds


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def getVector(self):
        return Vector(x, y)

    def setVector(self, x, y):
        self.x = x
        self.y = y

    def minusVector(self, vector):
        return Vector(self.x - vector.x, self.y - vector.y)

    def addVector(self, vector):
        return Vector(self.x + vector.x, self.y + vector.y)

    def multiplyByScalar(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalise(self):
        magnitude = self.magnitude()
        return Vector(self.x / magnitude, self.y / magnitude)


class Planet:
    def __init__(self, mass, diameter, orbital_radius, orbital_velocity):
        self.position = Vector(orbital_radius, 0)
        self.velocity = Vector(0, orbital_velocity)
        self.acceleration = Vector(None, None)
        self.force = Vector(None, None)
        self.mass = mass
        self.diameter = diameter
        self.orbital_radius = orbital_radius

    def __str__(self):
        return f"mass: {self.mass}, diameter: {self.diameter}"

    def setPosition(self, x, y):
        self.position.setVector(x, y)

    def getPosition(self):
        return self.position

    def setVelocity(self, velocity):
        self.velocity = velocity

    def setAcceleration(self, acceleration):
        self.acceleration = acceleration

    def setResultantForce(self, force):
        self.force = force

    def forceToOtherBody(self, body):
        distance = self.distanceToOtherBody(body)
        normalised_direction = self.directionToOtherBody(body).normalise()
        force = (G * self.mass * body.mass) / (distance ** 2)
        return Vector(normalised_direction.x * force, normalised_direction.y * force)

    def distanceToOtherBody(self, body):
        direction = self.directionToOtherBody(body)
        distance = direction.magnitude()
        return distance

    def directionToOtherBody(self, body):
        direction = body.position.minusVector(self.position)
        return direction


class Star:
    def __init__(self, mass, diameter):
        self.mass = mass
        self.diameter = diameter
        self.position = Vector(0, 0)


planets = []
mercury = Planet(0.330 * (10 ** 24), 4879 * (10 ** 3), 57.9 * (10 ** 9), 47400)
venus = Planet(4.87 * (10 ** 24), 12104 * (10 ** 3), 108.2 * (10 ** 9), 35000)
earth = Planet(5.97 * (10 ** 24), 12756 * (10 ** 3), 149.6 * (10 ** 9), 29800)
mars = Planet(0.642 * (10 ** 24), 6792 * (10 ** 3), 228 * (10 ** 9), 24100)
jupiter = Planet(1898 * (10 ** 24), 142984 * (10 ** 3), 778.5 * (10 ** 9), 13100)
saturn = Planet(568 * (10 ** 24), 120536 * (10 ** 3), 1432 * (10 ** 9), 9700)
uranus = Planet(86.8 * (10 ** 24), 51118 * (10 ** 3), 2867 * (10 ** 9), 6800)
neptune = Planet(102 * (10 ** 24), 49628 * (10 ** 3), 4515 * (10 ** 9), 5400)
pluto = Planet(0.0130 * (10 ** 24), 2376 * (10 ** 3), 5906 * (10 ** 9), 4700)

sun = Star(1988500 * (10 ** 24), 1392700 * (10 ** 3))

planets.append(mercury)
planets.append(venus)
planets.append(earth)
planets.append(mars)
planets.append(jupiter)
planets.append(saturn)
planets.append(uranus)
planets.append(neptune)
planets.append(pluto)


def calculateForces():
    for planet in planets:
        resultant_force = Vector(0, 0)
        resultant_force = resultant_force.addVector(planet.forceToOtherBody(sun))
        for other_planet in planets:
            if planet != other_planet:
                resultant_force = resultant_force.addVector(planet.forceToOtherBody(other_planet))
        planet.setResultantForce(resultant_force)


def calculateAccelerations():
    for planet in planets:
        acceleration = Vector(planet.force.x / planet.mass, planet.force.y / planet.mass)
        planet.setAcceleration(acceleration)


def calculateVelocities():
    for planet in planets:
        planet.velocity = planet.velocity.addVector(planet.acceleration.multiplyByScalar(timestep))


def calculatePositions():
    for planet in planets:
        planet.position = planet.position.addVector(planet.velocity.multiplyByScalar(timestep))


def render():
    # 400px = 6*10^12 m
    # 1px = 1.5 * 10^10 m
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global simulating
            simulating = False
    pygame.draw.circle(screen, (255, 0, 0), cartesianToPixelCoordinates(0, 0), 10)
    for i in range(len(planets)):
        # print(planet)
        x = planets[i].position.x / ((6 * (10 ** 12)) / (SCREEN_WIDTH / 2))
        y = planets[i].position.y / ((6 * (10 ** 12)) / (SCREEN_HEIGHT / 2))
        diameter = 15 * planets[i].diameter / (142984 * (10 ** 3))
        if diameter < 5:
            diameter = 5
        planet_image = pygame.image.load(PLANET_IMAGES[i])
        planet_image.convert()
        planet_image = pygame.transform.scale(planet_image, (diameter, diameter))
        rect = planet_image.get_rect()
        rect = rect.move(cartesianToPixelCoordinates(x, y))
        screen.blit(planet_image, rect)
        #pygame.draw.circle(screen, (0, 0, 255), cartesianToPixelCoordinates(x, y), diameter)

    pygame.display.update()


def cartesianToPixelCoordinates(x, y):
    screen_x = x + SCREEN_WIDTH / 2
    screen_y = SCREEN_HEIGHT / 2 - y
    return screen_x, screen_y


while simulating:
    start_time = time.time_ns()
    # -----------------------------------
    calculateForces()
    calculateAccelerations()
    calculateVelocities()
    calculatePositions()
    render()
    # -----------------------------------
    end_time = time.time_ns()
    time_difference = end_time - start_time
    if time_difference > 0:
        timestep = 10000000 * time_difference / (10 ** 9)
        if timestep > 100000:
            timestep = 50000
    print("fps", 10000000 * 1/timestep)

pygame.quit()
