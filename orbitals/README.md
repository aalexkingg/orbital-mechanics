# Simulating Planetary Orbits

This program contains animations of planets orbiting the sun. By calculating their velocities and position using numerical methods, their trajectory can be mapped.

Where the current position is **r**(t), the position at the next step would therefore be **r**(t + $\delta$t), with $\delta$t being the time step. 

$$**r**(t + \delta t) = **r**(t) + \delta**r** = **r**(t) + **v**\delta t$$
                     
The velocity at the next step, **v**(t + $\delta$t), uses a form of Newtons equation of gravitation to calculate the velocity of the planet at the next time step.
                     
$$**v** (t + \delta t) = **v**(t) + \delta**v** = **v**(t) - \frac{GMr}{|r|^{3}}\delta t$$
                  
This program is designed to investigate the behaviour of planets orbiting a star, and how varying parameters such as initial position, velocity, mass of the planets and mass of the star can effect the orbital path. 

#### Effects of changing mass of star

By changing the mass of star, the magnitude of the force exerted onto the planet becomes greater. So evidently, the greater the mass of the star, the stronger the force and the closer the eccentricity tends to zero (850 < m < 1000). Similarly, when the mass of the star decreases, and the magnitude of the gravitational force decreases, the orbit becomes more eliiptical (550 < m < 850, until it reaches a critical point where the force is too weak, and the planet escapes the stars pull (m < 550).

#### Effects of changing time step

By changing the time step of the simulation, this effects the number of frames of the animation that the computer processes, theoretically this produces a more accurate model, but does require a lot more processing power. A smaller value time step causes the program to process more frames of the simulation, however this comes at the cost of performance, and the simulation may begin to move slower and even lag. Similarly, a higher time step, causes performance to increase signnificantly, but sacrifices the accuracy of the simulation, causing orbits to becomes jagged and unrealistic.<br>(Time step changed back to original value as it cause program to take a substantial amount of time to run)

#### Effects of changing initial position

If the initial position is moved further from the star, than the gravitational force on the planet becomes weaker, and similar efects to decreasing the mass of the star happens. Similarly, if the planet is moved closer to the star, this corresponds to a stronger force acting on the planet, and the same effects from increasing the mass of the star begin to happen.

#### Effects of changing initial velocity

Changing the magnitude and direction of the initial velocity of the planet can have a signnificant effect on the shape fo the planets' orbital path. The velocity of the planet is also dependent on it's distance from the star, as the planet needs to have a velocity less than the escape velocity (to prevent the planet from escaping the gravitational pull of the star), and a velocity great enough to prevent it being pulled directly towards the star. Any velocity within this range will result in the planet following an elliptical path around the star.

#### Calculating required velocity to maintain stable circular orbit

By using the equation:

**v**$^{2}$ = $\frac{GM}{|r|^{2}}$**r**

The required velocity to maintain a stable circular orbit at a given radius can be determined. However, this equation is only able to calculate the magnitude velocity in the same direction at the position vector, in order to fidn the direction of the velocity vector, we simply need to rotate it 90 degrees - As the direction of velocity always acts at a perpendicular angle to the position vector (from the origin). 

