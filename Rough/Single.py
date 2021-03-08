import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../..')
import Model as m
import numpy as np
import matplotlib.pyplot as plt
import glob

sdirec = '_temp'
deltas = 10

"""
Run

"""

# M = PAR(Da=0.1, Dp=0.1, konA=0.1, koffA=0.01, kposA=0, konP=0.1, koffP=0.0101, kposP=0, kAP=0.00, kPA=0.00,
#             ePneg=2, eAneg=2, xsteps=100, Tmax=1000, deltat=0.01, L=50, psi=0.1, pA=1, pP=0, v=0.04)


model = m.Model(Dm=0.02, Dc=10, Vm=0.04, Vc=0, kon=1 / 200, koff=1 / 200, xsteps=100, Tmax=1000, deltat=0.01,
                deltax=0.5, c_0=1, m_0=1, flowtype=3)

for t in range(int(model.Tmax / model.deltat)):
    model.react()
    model.time = (t + 1) * model.deltat

    if model.time % deltas == 0 or model.time == model.deltat:
        if not os.path.exists('%s/%s' % (sdirec, '{:05d}'.format(int(model.time)))):
            os.mkdir('%s/%s' % (sdirec, '{:05d}'.format(int(model.time))))
        model.save('%s/%s/' % (sdirec, '{:05d}'.format(int(model.time))))

"""
Slider plot

"""

from matplotlib.widgets import Slider

direcs = sorted(glob.glob(sdirec + '/*/'))

ax = plt.subplot2grid((1, 2), (0, 0))
ax2 = plt.subplot2grid((1, 2), (0, 1))
plt.subplots_adjust(bottom=0.25, wspace=0.5)
axframe = plt.axes([0.25, 0.1, 0.65, 0.03])
sframe = Slider(axframe, 'Iteration', 0, len(direcs), valinit=0, valfmt='%d')


def update(i):
    ax.clear()
    ax2.clear()
    direc = direcs[int(i)]
    print(direc)

    # Cortical
    m = np.loadtxt(direc + '/m.txt')
    ax.plot(m, c='k')
    ax.set_ylim(bottom=0)
    ax.set_ylabel('Cortical concentration')

    # Cytoplasmic
    c = np.loadtxt(direc + '/c.txt')
    ax2.plot(c, c='k')
    ax2.set_ylim(bottom=0)
    ax2.set_ylabel('Cytoplasmic concentration')


sframe.on_changed(update)
plt.show()
