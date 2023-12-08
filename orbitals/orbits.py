import pygame
from orbital_mechanics.helpers import *
from vpython import *

pygame.init()

WIDTH = 1600
HEIGHT = 900

AU = 1.495979e+11
G = 1.



class Pos(tuple):
    def __init__(self, points):
        self.x, self.y = points


def force(pos1, pos2, m1, m2):
    """
    Returns the gravitational force exerted by object 2 on object 1.
    Input:
      - pos1 = position vector of first object
      - pos2 = position vector of second object
      - m1   = mass of first object
      - m2   = mass of second object
    Depends on:
      - G    = gravitational constant (global variable)
    """
    # Calculates and returns value of the force
    return -G * m1 * m2 * (pos1 - pos2) / ((mag(pos1 - pos2)) ** 3)


def move_planet(position, velocity, m_star, dt):
    """
    Calculate motion of planet in the gravitational field of a star with given mass
    at the origin, using Euler's method.

    Input:
      - position: position vector of planet at start of time step
      - velocity: velocity vector of planet at start of time step
      - m_star:   mass of star
      - dt:       time step

    Output: (position_new, velocity_new)
      - position_new: position vector of planet at end of time step
      - velocity_new: velocity vector of planet at end of time step

    Depends on:
      - force = function to calculate the gravitational force between two objects
    """
    # Calculates new position using revious position and velocity multiplied with the time step
    position_new = position + velocity * dt

    # First calculates the change in velocity, which can then be used with the time step and previous velocity
    # To find the value of the new velocity
    delta_v = -G * m_star * position * dt / ((mag(position)) ** 3)
    velocity_new = velocity + delta_v

    return position_new, velocity_new


def animate_planet(position, velocity, m_star, dt):
    """
    Animate planetary orbit from given starting position, with given time step.

    Input:
      - position: position vector of planet at start of simulation
      - velocity: velocity vector of planet at start of simulation
      - m_star:   mass of star
      - dt:       time step
    """
    fps = 2000
    time = 0
    max_time = 5  # The amount of time for which the animation runs

    # Defines planet
    planet = sphere(pos=position, color=color.green, radius=0.1, make_trail=True)

    # Loops through every frame of animation, till time has exceeded animations run time
    while time < max_time:
        rate(fps)  # sets the framerate of the animation
        # Calculates new position and velocity
        new_position, new_velocity = move_planet(planet.pos, velocity, m_star, dt)
        velocity = new_velocity  # Sets planets' new velocity
        planet.pos = new_position  # Sets planets' new position
        time += dt  # Increments time


def animate_planets(pos1, pos2, vel1, vel2, m_star, dt):
    """
    Animate planetary orbits from the given starting position of two planets, with given time step.

    Input:
      - pos1: position vector of planet 1 at start of simulation
      - pos2: position vector of planet 2 at start of simulation
      - vel1: velocity vector of planet 1 at start of simulation
      - vel2: velocity vector of planet 2 at start of simulation
      - m_star:   mass of star
      - dt:       time step
    """
    fps = 2000  # 1/dt
    time = 0
    max_time = 5  # Set runtime of animation

    # for planets:

    # Defines the two planet shapes
    planet1 = sphere(pos=pos1, color=color.green, radius=0.1, make_trail=True)
    planet2 = sphere(pos=pos2, color=color.red, radius=0.1, make_trail=True)

    # Loop through every frame of animation till animation time exceeds runtime
    while time < max_time:
        rate(fps)  # Set framerate of animation

        # Calculate new position and velocity of planet 1
        new_pos1, new_vel1 = move_planet(planet1.pos, vel1, m_star, dt)
        vel1 = new_vel1  # Set velocity of planet 1
        planet1.pos = new_pos1  # Set position of planet 1

        # Calculate new position and velocity of planet 2
        new_pos2, new_vel2 = move_planet(planet2.pos, vel2, m_star, dt)
        vel2 = new_vel2  # Set velocity of planet 2
        planet2.pos = new_pos2  # Set position of planet 2

        time += dt  # Increment time


def move_planet_real(position, velocity, mass, position_planet, m_planet, m_star, dt):
    """
    Calculate motion of planet in the gravitational field of a star with given mass
    at the origin, using Euler's method.

    Input:
      - position: position vector of planet at start of time step
      - velocity: velocity vector of planet at start of time step
      - mass: mass of planet
      - position_planet: position of other planet
      - m_planet: mass of other planet
      - m_star:   mass of star
      - dt:       time step

    Output: (position_new, velocity_new)
      - position_new: position vector of planet at end of time step
      - velocity_new: velocity vector of planet at end of time step

    Depends on:
      - force = function to calculate the gravitational force between two objects
    """
    # Calculates new position of planet
    position_new = position + velocity * dt

    Fsun = force(position, vector(0, 0, 0), mass, m_star)  # Calculates force from sun on planet
    Fplanet = force(position, position_planet, mass, m_planet)  # Calculates force from other planet on planet

    Fnet = Fsun + Fplanet  # Calculates total force on planet

    # Calculates new velocity on planet
    delta_v = Fnet * dt / mass
    velocity_new = velocity + delta_v

    return position_new, velocity_new


def animate_planets_real(pos1, pos2, vel1, vel2, mass1, mass2, m_star, dt):
    """
    Animate planetary orbits from the given starting position of two planets, with given time step.

    Input:
      - pos1: position vector of planet 1 at start of simulation
      - pos2: position vector of planet 2 at start of simulation
      - vel1: velocity vector of planet 1 at start of simulation
      - vel2: velocity vector of planet 2 at start of simulation
      - mass1: mass of first planet
      - mass2: mass of second planet
      - m_star:   mass of star
      - dt:       time step
    """
    fps = 2000.  # Sets frame rate of animation
    time = 0  # Sets start time to 0
    max_time = 5  # Sets animation runtime to 5 seconds

    # Defines planets1 and 2
    planet1 = sphere(pos=pos1, color=color.green, radius=0.1, make_trail=True)
    planet2 = sphere(pos=pos2, color=color.red, radius=0.1, make_trail=True)

    # Loops until animation time exceeds runtime
    while time < max_time:
        rate(fps)  # sets framerate of animation

        # Calculates new position and velocity of planet1
        new_pos1, new_vel1 = move_planet_real(planet1.pos, vel1, mass1, planet2.pos, mass2, m_star, dt)
        vel1 = new_vel1
        planet1.pos = new_pos1

        # Calculates new position and velocity of planet2
        new_pos2, new_vel2 = move_planet_real(planet2.pos, vel2, mass2, planet1.pos, mass1, m_star, dt)
        vel2 = new_vel2
        planet2.pos = new_pos2

        time += dt  # Increments time


def calculate_velocity(position, m_star):
    """
    Calculates and returns the required velocity, of planet orbiting star, required to maintain a stable circular orbit

    Input:

     - position: position of planet
     - mass: mass of planet

     Output:

     - velocity: required velocity of planet around star to remain in circular orbit

    """

    # calculate magnitude of velocity
    velocity = ((G * m_star) / ((mag(position)) ** 2)) * position

    # calculate direction of velocity - 90 deg rot = (y, -x)
    return vector(-(abs(velocity.y)) ** 0.5, abs(velocity.x) ** 0.5, abs(velocity.z) ** 0.5)


def moon():
    # Initialize canvas, and set parameters of star and planet.
    canvas()

    m_star = 900.  # mass of star (units where G=1)
    sphere(pos=vector(0, 0, 0), color=color.yellow, radius=0.5)  # draw star

    pos_planet = vector(0, 8, 0)  # initial position of planet
    v_planet = calculate_velocity(pos_planet, m_star)  # initial velocity of planet
    m_planet = 2

    pos_moon = vector(-0.1, 8, 0)  # initial position of moon
    v_moon = vector(-12, -5, 0)  # initial velocity of moon
    m_moon = 1e-6

    # Animate orbit of planet
    animate_planets_real(pos_planet, pos_moon, v_planet, v_moon, m_planet, m_moon, m_star, 1e-5)


def main():

    # Circular orbit

    # Initialize canvas, and set parameters of star and planet.
    canvas()
    pos_planet = vector(0, 2, 0)  # initial position of planet
    v_planet = vector(-22, 0, 0)  # initial velocity of planet
    m_star = 900.  # mass of star (units where G=1)
    sphere(pos=vector(0, 0, 0), color=color.yellow, radius=0.1)  # draw star

    # Animate orbit of planet
    animate_planet(pos_planet, v_planet, m_star, 1e-4)

    # Elliptical Orbit

    # Initialize canvas, and set parameters of star and planet.
    canvas()
    pos_planet = vector(0, 2, 0)  # initial position of planet
    v_planet = vector(-22, 0, 0)  # initial velocity of planet
    m_star = 700  # mass of star (units where G=1)
    sphere(pos=vector(0, 0, 0), color=color.yellow, radius=0.1)  # draw star

    # Animate orbit of planet
    animate_planet(pos_planet, v_planet, m_star, 1e-4)




    """
    # setup
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True

    input_boxes = [
        #InputTextBox(75, 20, 140, 32, "V(x)")
    ]

    sun_pos = Pos((WIDTH/2, HEIGHT/2))
    sun_mass = 2e30

    earth_orbit = 1*AU
    earth_pos = Pos((sun_pos.x, sun_pos.y+300))
    earth_mass = 6e24



    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            for box in input_boxes:
                box.handle_event(event)
                # handle held key in case of backspace etc

            # animte circle here

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        sun = pygame.draw.circle(screen, "yellow", sun_pos, 25)
        earth = pygame.draw.circle(screen, "blue", earth_pos, 15)

        pygame.display.flip()
        # fps limit
        clock.tick(60)
"""


if __name__ == "__main__":
    main()
    pygame.quit()