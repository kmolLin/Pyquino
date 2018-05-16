#!/usr/bin/env python3

""" Completely specifies the environment including the cart, pendulum, and the
    equations of motion that relate the two. The only input to the system is
    force applied laterally to the cart (the agent is not the cart pendulum
    system but rather the applier of such a force). Basically, the environment
    contains everything but the agent and the constraint imposed on the agent's
    success and reward.
    Most of the physics was written by following Jason Moore's tutorial on
    using sympy to control an inverted pendulum.
    URL: http://www.moorepants.info/blog/npendulum.html
"""

import numpy as np
import scipy
from sympy import symbols, Dummy, lambdify
from sympy.physics.mechanics import *

class Environment(object):
    def __init__(self, links, arm_length, arm_mass, cart_mass, cart_length, rail_length, gravity, t_sim, t_resol):
        """ Initializes the environment.
        """
        # Define system properties.
        self.links = links
        self.arm_length = arm_length
        self.arm_mass = arm_mass
        self.cart_mass = cart_mass
        self.cart_length = cart_length
        self.rail_length = rail_length

        # Define environment properties
        self.gravity = gravity
        self.t_sim = t_sim
        self.t_resol = t_resol

        self.mechanics()
        self.constants()
        self.kinematics()
        self.kinetics()
        self.dynamics()

        # Current state of the pendulum
        self.t0 = 0.0
        self.tf = t_sim
        self.y0 = np.hstack((0, np.pi/2 * np.ones(len(self.q) - 1), 1e-3*np.ones(len(self.u))))

        # Time and state of the environment
        self.t = None
        self.state = None

    def mechanics(self):
        """ Defines the mechanics of the environment.
        
        Mechanics will need the generalized coordinates, generalized speeds,
        and the input force which are all time dependent variables and the bob
        masses, link lengths, and acceleration due to gravity which are all
        constants. Time, t, is also made available because we will need to
        differentiate with respect to time.
        """

        # Generalized coordinates of the cart and each pendulum link
        self.q = dynamicsymbols('q:' + str(self.links + 1))

        # Speeds of the cart and pendulum links
        self.u = dynamicsymbols('u:' + str(self.links + 1))

        # Force
        self.f = dynamicsymbols('f')

        # Constants
        self.m = symbols('m:' + str(self.links + 1))  # mass of each bob
        self.l = symbols('l:' + str(self.links))      # length of each link
        (self.g, self.t) = symbols('g t')             # gravity and time

        # Intertial reference frame
        self.I = ReferenceFrame('I')

        # Origin
        self.O = Point('O')
        self.O.set_vel(self.I, 0)

        # Cart the pendulum is attached to, which has mass and can move
        # laterally
        self.cart = Point('C')
        self.cart.set_pos(self.O, self.q[0]*self.I.x)       # position
        self.cart.set_vel(self.I, self.u[0]*self.I.x)       # velocity
        self.cart_p = Particle('Cp', self.cart, self.m[0])  # define a particle

    def constants(self):
        self.params = [self.g, self.m[0]]
        self.param_vals = [self.gravity, self.cart_mass]
        for i in range(self.links):
            self.params += [self.l[i], self.m[i + 1]]            
            self.param_vals += [self.arm_length, self.arm_mass]

    def kinematics(self):
        """ Defines the kinematics of the system. 
        """
        self.frames = [self.I]
        self.points = [self.cart]
        self.particles = [self.cart_p]
        self.forces = [(self.cart, self.f*self.I.x - self.m[0]* self.g * self.I.y)]
        self.kindiffs = [self.q[0].diff(self.t) - self.u[0]]

        for i in range(self.links):
            # Create a new frame
            Bi = self.I.orientnew('B' + str(i), 'Axis', [self.q[i + 1], self.I.z])
            Bi.set_ang_vel(self.I, self.u[i + 1]*self.I.z)
            self.frames.append(Bi)

            # Create a new point for the link
            Pi = self.points[-1].locatenew('P' + str(i + 1), self.l[i]*Bi.x)
            Pi.v2pt_theory(self.points[-1], self.I, Bi)
            self.points.append(Pi)
            
            # Create a new particle for the link
            Ppi = Particle('Pp' + str(i + 1), Pi, self.m[i + 1])
            self.particles.append(Ppi)

            # Set the force applied to the point
            self.forces.append((Pi, -self.m[i + 1]*self.g*self.I.y))

            # Define the kinematic ODE
            self.kindiffs.append(self.q[i + 1].diff(self.t) - self.u[i + 1])

    def kinetics(self):
        """ Defines the equations of motion for the system.
        """
        self.kane = KanesMethod(self.I, q_ind=self.q, u_ind=self.u, kd_eqs=self.kindiffs)
        (self.fr, self.frstar) = self.kane.kanes_equations(self.forces, self.particles)

    def dynamics(self):
        # Create a list of the states
        dynamic = self.q + self.u

        # Add the input force
        dynamic.append(self.f)

        # Create a dummy symbol for each variable
        dummy_symbols = [Dummy() for i in dynamic]
        dummy_dict = dict(zip(dynamic, dummy_symbols))                 

        # Get the solved kinematical differential equations
        kindiff_dict = self.kane.kindiffdict()

        # Mass and force matrix substitutions 
        M = self.kane.mass_matrix_full.subs(kindiff_dict).subs(dummy_dict)
        F = self.kane.forcing_full.subs(kindiff_dict).subs(dummy_dict)

        # Create callable functions to evaluate mass matrix and forcing vector
        self.M_func = lambdify(dummy_symbols + self.params, M)
        self.F_func = lambdify(dummy_symbols + self.params, F)

    def play_chunk(self, action):
        t = np.linspace(self.t0, self.tf, self.t_resol)
        y = scipy.integrate.odeint(self.differentiate_states, self.y0, t, args=(self, action))

        # Update the initial conditions for the next time chunk
        self.t0 = self.tf
        self.tf = self.t0 + self.t_sim
        self.y0 = y[-1,:]

        # Add the state of this time chunk to the state vector.
        self.t = np.hstack((self.t, t)) if self.t is not None else t
        self.state = np.vstack((self.state, y)) if self.state is not None else y

    @staticmethod
    def differentiate_states(x, t, self, action):
        """ Computes the derivatives of the states.
        To determine the resulting position, we integrate the derivative this
        function returns.
        @param x        Current state vector (np.ndarray with shape 2*(n + 1))
        @param t        Current time
        @return         Derivative of the state (ndarray, shape 2*(n + 1))
        """
        u = action
        arguments = np.hstack((x, u, self.param_vals))

        # Compute the derivative at x
        dx = np.array(np.linalg.solve(self.M_func(*arguments), self.F_func(*arguments))).T[0]
        return dx
