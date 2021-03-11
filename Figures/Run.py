import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from Model import Model
import numpy as np
from multiprocessing import Pool

"""
A: no exchange, vary D
(Figure 3a)

"""


def func(d):
    path = 'Data/A_%s' % d
    print(path)

    # Set up model
    model = Model(Dm=d, Dc=0, Vm=0.05, Vc=0, kon=0, koff=0, xsteps=100, Tmax=1000, deltat=0.01, deltax=0.1, c_0=0,
                  m_0=1)

    # Simulate
    soln, _, _, _ = model.run()

    # Save
    if not os.path.exists(path):
        os.mkdir(path)
    np.savetxt(path + '/m.txt', soln[0])
    np.savetxt(path + '/c.txt', soln[1])
    print(path + ' Done!')


Pool(3).map(func, [0.01, 0.05, 1])

"""
B: exchanging, vary kon, koff
(Figure 3B)

"""


def func(k):
    path = 'Data/B_%s' % k
    print(path)

    # Set up model
    model = Model(Dm=0, Dc=1, Vm=0.05, Vc=0, kon=k, koff=k, xsteps=100, Tmax=1000, deltat=0.01, deltax=0.1,
                  c_0=1, m_0=1)

    # Simulate
    soln, _, _, _ = model.run()

    # Save
    if not os.path.exists(path):
        os.mkdir(path)
    np.savetxt(path + '/m.txt', soln[0])
    np.savetxt(path + '/c.txt', soln[1])
    print(path + ' Done!')


Pool(3).map(func, [0.007, 0.01, 0.1])

"""
C: retrograde flow
(Figure 4D)

"""


def func(koff):
    path = 'Data/C_%s' % koff
    print(path)

    # Set up model
    model = Model(Dm=0.01, Dc=1, Vm=0.05, Vc=0, kon=koff * np.r_[np.zeros([80]), 5 * np.ones([20])], koff=koff,
                  xsteps=100, Tmax=1000, deltat=0.01, deltax=0.1, c_0=1, m_0=1)

    # Simulate
    soln, _, _, _ = model.run()

    # Save
    if not os.path.exists(path):
        os.mkdir(path)
    np.savetxt(path + '/m.txt', soln[0])
    np.savetxt(path + '/c.txt', soln[1])
    print(path + ' Done!')


Pool(3).map(func, [0.001, 0.01, 0.1])
