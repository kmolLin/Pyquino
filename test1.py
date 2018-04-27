# code test of pendulum
# T = 2*pi/w = 2*pi*sqrt(L/g)  
# g = (4*pi*L^2)/T^2  
# T = cycle
# g = acceleration of pendulum
# theta = Acos(sqrt(g/L)*t+zeta)

# -*- coding: utf-8 -*-
from math import sin, sqrt
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import fsolve
import pylab as pl
from scipy.special import ellipk

g = 9.8

def pendulum_equations(w, t, l):
    th, v = w
    dth = v
    dv  = - g/l * sin(th)
    return dth, dv

def pendulum_th(t, l, th0):
    track = odeint(pendulum_equations, (th0, 0), [0, t], args=(l,))
    return track[-1, 0]
    
def pendulum_period(l, th0):
    t0 = 2*np.pi*sqrt( l/g ) / 4
    t = fsolve( pendulum_th, t0, args = (l, th0) )
    return t*4
    
ths = np.arange(0, np.pi/2.0, 0.01)
periods = [pendulum_period(1, th) for th in ths]
periods2 = 4*sqrt(1.0/g)*ellipk(np.sin(ths/2)**2) # 计算单摆周期的精确值
pl.plot(ths, periods, label = u"fsolve cycle", linewidth=4.0)
pl.plot(ths, periods2, "r", label = u"real pendulum cycle", linewidth=2.0)
pl.legend(loc='upper left')
pl.title(u"lenth is 1")
pl.xlabel(u"init radins of pendulum")
pl.ylabel(u"cycle (sec)")
pl.show()
