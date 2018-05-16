
""" Simulation.
"""

import numpy as np
from sympy import Dummy, lambdify
from scipy.integrate import odeint

from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Rectangle

from test1 import Environment as environment


class Simulation(object):
    """ Simulates a session.
    """
    def __init__(self, agent, environment):
        """ Initialize the simulation.
        """
        self.a = agent
        self.e = environment

        self.e.play_chunk(0.0)
        self.e.play_chunk(0.0)

        dynamic = self.e.q + self.e.u
        print((self.e.state.shape[1]))
        print(("*"*10))
        lines = plt.plot(self.e.t, self.e.state[:,2])
        lab = plt.xlabel('Time [sec]')
        leg = plt.legend(dynamic[:2])
        animate_pendulum(self.e.t, self.e.state, self.e.arm_length, filename="test.mp4")
        #plt.show()


def animate_pendulum(t, states, length, filename=None):
    """ Animates the inverted pendulum given the time interval and states, 
        optionally saves it to file if the filename is given.
    
    If true a movie file will be saved of the animation, it may take some time.
    @param t        Time array
    @param states   States of the system
    @param length   Length of the pendulum links
    @param filename Name of the filename (optional)
    @return         Figure containing the plot and the animation as a tuple
    Credit: Jason Moore's tutorial on inverted pendulum using sympy.
    URL: http://www.moorepants.info/blog/npendulum.html
    """

    # the number of pendulum bobs
    numpoints = int(states.shape[1] / 2)

    # first set up the figure, the axis, and the plot elements we want to animate
    fig = plt.figure()
    
    # some dimesions
    cart_width = 0.4
    cart_height = 0.2
    
    # set the limits based on the motion
    xmin = np.around(states[:, 0].min() - cart_width / 2.0, 1)
    xmax = np.around(states[:, 0].max() + cart_width / 2.0, 1)
    
    # create the axes
    ax = plt.axes(xlim=(xmin, xmax), ylim=(-1.1, 1.1), aspect='equal')
    
    # display the current time
    time_text = ax.text(0.04, 0.9, '', transform=ax.transAxes)
    
    # create a rectangular cart
    rect = Rectangle([states[0, 0] - cart_width / 2.0, -cart_height / 2],
        cart_width, cart_height, fill=True, color='red', ec='black')
    ax.add_patch(rect)
    
    # blank line for the pendulum
    line, = ax.plot([], [], lw=2, marker='o', markersize=6)

    # initialization function: plot the background of each frame
    def init():
        time_text.set_text('')
        rect.set_xy((0.0, 0.0))
        line.set_data([], [])
        return time_text, rect, line,

    # animation function: update the objects
    def animate(i):
        time_text.set_text('time = {:2.2f}'.format(t[i]))
        rect.set_xy((states[i, 0] - cart_width / 2.0, -cart_height / 2))
        x = np.hstack((states[i, 0], np.zeros((numpoints - 1))))
        y = np.zeros(numpoints)
        for j in np.arange(1, numpoints):
            x[j] = x[j - 1] + length * np.cos(states[i, j])
            y[j] = y[j - 1] + length * np.sin(states[i, j])
        line.set_data(x, y)
        return time_text, rect, line,

    # call the animator function
    anim = animation.FuncAnimation(fig, animate, frames=len(t), init_func=init,
            interval=t[-1] / len(t) * 1000, blit=True, repeat=False)
    plt.show()
    # save the animation if a filename is given
    if filename is not None:
        anim.save(filename, fps=30, codec='libx264')


def main():
    #pdb.set_trace()
    links = 1
    arm_length = 1.0
    arm_mass = 0.01
    cart_mass = 0.1
    cart_length = 1
    rail_length = 10
    gravity = 9.8
    t_sim = 10
    t_resol = 100
    e = environment(links, arm_length, arm_mass, cart_mass, cart_length, rail_length, gravity, t_sim, t_resol)
    s = Simulation(None, e)


if __name__ == '__main__':
    #import pdb
    main()
