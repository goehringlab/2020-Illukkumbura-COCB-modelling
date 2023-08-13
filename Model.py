import numpy as np
from pde_rk import pde_rk


def diffusion(concs, dx=1):
    concs_ = np.r_[concs[0], concs, concs[-1]]
    d = concs_[:-2] - 2 * concs_[1:-1] + concs_[2:]
    return d / (dx**2)


class Model:
    def __init__(
        self, Dm, Dc, Vm, Vc, kon, koff, xsteps, Tmax, deltat, deltax, c_0, m_0
    ):
        # Diffusion
        self.Dm = Dm
        self.Dc = Dc

        # Flow
        self.Vm = Vm
        self.Vc = Vc
        self.flow_profile = np.arange(int(xsteps)) / xsteps

        # Membrane exchange
        self.kon = kon
        self.koff = koff

        # Starting conditions
        self.m_0 = m_0
        self.c_0 = c_0

        # Misc
        self.xsteps = int(xsteps)
        self.Tmax = Tmax
        self.deltat = deltat
        self.deltax = deltax

    def flow(self, concs, dx):
        return -np.diff(np.r_[concs, concs[-1]] * np.r_[self.flow_profile, 0]) / dx

    def dxdt(self, X):
        m = X[0]
        c = X[1]

        dm = (
            (self.kon * c)
            - (self.koff * m)
            + (self.Dm * diffusion(m, self.deltax))
            - (self.Vm * self.flow(m, self.deltax))
        )
        dc = (
            -(self.kon * c)
            + (self.koff * m)
            + (self.Dc * diffusion(c, self.deltax))
            - (self.Vc * self.flow(c, self.deltax))
        )
        return [dm, dc]

    def run(self, save_gap=None):
        if save_gap is None:
            save_gap = self.Tmax

        soln, time, solns, times = pde_rk(
            dxdt=self.dxdt,
            X0=[np.ones([self.xsteps]) * self.m_0, np.ones([self.xsteps]) * self.c_0],
            Tmax=self.Tmax,
            deltat=self.deltat,
            t_eval=np.arange(0, self.Tmax + 0.0001, save_gap),
        )
        return soln, time, solns, times
