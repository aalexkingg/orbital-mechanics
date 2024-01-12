import vpython
from vpython import *

AU = 1.495979e+8  # km
G = 1.
SOLAR_MASS = 1.988e30  # kg


class Body:
    def __init__(self, m, r, a, e, inc):
        """

        :param m: Mass (kg)
        :param r: Radius (km)
        :param a: Distance (km)
        :param e: Eccentricity
        :param inc: Inclination (degrees)
        """
        self.m = m
        self.r = r
        self.a = a
        self.e = e
        self.inc = inc

        self.rel_m = m / SOLAR_MASS
        self.rel_a = a / AU
        self.R_p = self.rel_a * (1 - self.e)
        self.R_a = self.rel_a * (1 + self.e)

        self._pos = vector(0, 0, 0)
        self._vel = vector(0, 0, 0)
        self._sphere: vpython.sphere = None
        # Find a way of going up the "super()" chain in order to track forces

    @property
    def pos(self): return self._pos

    @pos.setter
    def pos(self, new: vector):
        self._pos = new
        self._sphere.pos = new

    @property
    def vel(self): return self._vel

    @vel.setter
    def vel(self, new): self._vel = new


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


def net_force(pos, m):
    """
    Gets net force of object in position 0
    :param pos: List of positions as vector
    :param m: List of masses
    :return: Net force
    """
    if len(pos) > 1 and len(pos) == len(m):
        return sum([force(pos[0], pos[i+1], m[0], m[i+1]) for i in range(len(pos))])
    else:
        raise "Incorrect parameters for net force."


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
    max_time = 1000  # Sets animation runtime to 5 seconds

    # Defines planets1 and 2
    planet1 = sphere(pos=pos1, color=color.green, radius=0.1, make_trail=True, trail_radius=0.05)
    planet2 = sphere(pos=pos2, color=color.red, radius=0.1, make_trail=True, trail_radius=0.05)

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

    pos_planet = vector(20, 8, 10)  # initial position of planet
    v_planet = calculate_velocity(pos_planet, m_star)  # initial velocity of planet
    m_planet = 2

    pos_moon = vector(-0.1, 8, 0)  # initial position of moon
    v_moon = vector(-12, -5, 0)  # initial velocity of moon
    m_moon = 1e-6

    # Animate orbit of planet
    animate_planets_real(pos_planet, pos_moon, v_planet, v_moon, m_planet, m_moon, m_star, 1e-5)


MERCURY = Body(0.33e24, 2439.5, 57.9e6, 0.206, 7)
VENUS = Body(4.87e24, 6052, 108.2e6, 0.007, 3.4)
EARTH = Body(5.972e24, 6378, 149.6e6, 0.017, 0)
MARS = Body(0.642e24, 3396, 228e6, 0.094, 1.8)
JUPITER = Body(1898e24, 71492, 778.5, 0.049, 1.3)
SATURN = Body(586e24, 60268, 1432e6, 0.052, 2.5)
URANUS = Body(86.8e24, 25559, 2867e6, 0.047, 0.8)
NEPTUNE = Body(102e24, 24764, 4515e6, 0.01, 1.8)
PLUTO = Body(0.013e24, 1188, 5906.4e6, 0.244, 17.2)
MOON = Body(0.073e24, 1737.5, 0.384e6, 0.055, 5.1)

"""
############### Circular orbit of single planet ###############

# Initialize canvas, and set parameters of star and planet.
canvas()
pos_planet = vector(0, 2, 0)  # initial position of planet
v_planet = vector(-22, 0, 0)  # initial velocity of planet
m_star = 900.  # mass of star (units where G=1)
sphere(pos=vector(0, 0, 0), color=color.yellow, radius=0.1)  # draw star

# Animate orbit of planet
animate_planet(pos_planet, v_planet, m_star, 1e-4)

############### Elliptical Orbit of single planet #####################

# Initialize canvas, and set parameters of star and planet.
canvas()
pos_planet = vector(0, 2, 0)  # initial position of planet
v_planet = vector(-22, 0, 0)  # initial velocity of planet
m_star = 700  # mass of star (units where G=1)
sphere(pos=vector(0, 0, 0), color=color.yellow, radius=0.1)  # draw star

# Animate orbit of planet
animate_planet(pos_planet, v_planet, m_star, 1e-4)

############## Circular orbit of two planets ############################

# Initialize canvas, and set parameters of star and planet.
canvas()

pos_planet1 = vector(1.85, 0, 0)  # initial position of planet1
v_planet1 = vector(0, 23.25, 0)  # initial velocity of planet1

pos_planet2 = vector(1.96, 0.4, 0)  # initial position of planet2
v_planet2 = vector(-4.44, 21.9, 0)  # initial velocity of planet2

m_star = 1000.  # mass of star (units where G=1)
sphere(pos=vector(0, 0, 0), color=color.yellow, radius=0.1)  # draw star

# Animate orbit of planet
animate_planets(pos_planet1, pos_planet2, v_planet1, v_planet2, m_star, 1e-4)


################ Elliptical orbit of two planets ########################

# Initialize canvas, and set parameters of star and planet.
canvas()

pos_planet1 = vector(1.85, 0, 0)  # initial position of planet1
v_planet1 = vector(0, 23.25, 0)  # initial velocity of planet1
mass1 = 2

pos_planet2 = vector(1.96, 0.4, 0)  # initial position of planet2
v_planet2 = vector(-4.44, 21.9, 0)  # initial velocity of planet2
mass2 = 2

m_star = 1000.  # mass of star (units where G=1)
sphere(pos=vector(0, 0, 0), color=color.yellow, radius=0.5)  # draw star

# Animate orbit of planet
animate_planets_real(pos_planet1, pos_planet2, v_planet1, v_planet2, mass1, mass2, m_star, 1e-4)

#################### Real orbit of two planets ########################

# Initialize canvas, and set parameters of star and planet.
canvas()

m_star = 900.  # mass of star (units where G=1)
sphere(pos=vector(0, 0, 0), color=color.yellow, radius=0.5)  # draw star

pos_planet1 = vector(0, 2, 0)  # initial position of planet1
mass1 = 2  # mass of planet 1
v_planet1 = calculate_velocity(pos_planet1, m_star)  # initial velocity of planet1

pos_planet2 = vector(0, 3.5, 0)  # initial position of planet2
mass2 = 2  # mass of planet 2
v_planet2 = calculate_velocity(pos_planet2, m_star)  # initial velocity of planet2

# Animate orbit of planet
animate_planets_real(pos_planet1, pos_planet2, v_planet1, v_planet2, mass1, mass2, m_star, 1e-4)

####################### Orbit of moon around planet ###############################

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
animate_planets_real(pos_planet, pos_moon, v_planet, v_moon, m_planet, m_moon, m_star, 1e-4)
"""


def start_animation(bodies, dt):
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
    max_time = 20  # Sets animation runtime

    orbitals = []
    for body in bodies:
        body.sphere = sphere(
            pos=body.pos,
            color=body.colour,
            radius=body.radius,
            make_trail=True,
            trail_radius=0.1,
            retain=1000
        )
        orbitals.append(body)

    #planet1 = sphere(pos=pos1, color=color.green, radius=0.1, make_trail=True)
    #planet2 = sphere(pos=pos2, color=color.red, radius=0.1, make_trail=True)

    m_star = orbitals[0].m

    # Loops until animation time exceeds runtime
    while time < max_time:
        rate(fps)  # sets framerate of animation


        #for i, body in enumerate(orbitals):
            #orbitals[i].pos, bodies[i].vel = move_planet_real(orbitals[i].pos, orbitals[i].vel, orbitals[i].m, ..., m_star=m_star, dt)

        # Calculates new position and velocity of planet1
        #new_pos1, new_vel1 = move_planet_real(planet1.pos, vel1, mass1, planet2.pos, mass2, m_star, dt)
        #vel1 = new_vel1
        #planet1.pos = new_pos1

        time += dt  # Increments time

def main():
    canvas()
    scene.userpan = True

    m_star = 900.  # Solar mass

    sphere(pos=vector(0, 0, 0), color=color.yellow, radius=1)  # draw star

    pos_planet = vector(0, 8, 0)  # initial position of planet
    v_planet = calculate_velocity(pos_planet, m_star)  # initial velocity of planet
    m_planet = 2

    pos_moon = vector(-0.1, 8, 0)  # initial position of moon
    v_moon = vector(-12, -5, 0)  # initial velocity of moon
    m_moon = 1e-6

    # Animate orbit of planet
    animate_planets_real(pos_planet, pos_moon, v_planet, v_moon, m_planet, m_moon, m_star, 1e-4)





if __name__ == "__main__":
    main()
