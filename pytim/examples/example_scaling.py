# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
import MDAnalysis as mda
import numpy as np
import pytim  
from pytim.datafiles import *
import matplotlib.pyplot as plt

def plot():
    data = np.loadtxt('timings.dat')
    size=np.array(data[:,0]) 
    time=np.array(data[:,1])
#    popt, pcov = curve_fit(func, size, time,method='lm')
#    interval = np.linspace(np.min(size),np.max(size),100)
    plt.loglog(size,time)
#    plt.loglog(interval,func(interval,popt[0]))
    plt.ylabel('time (s)')
    plt.xlabel('atoms')
    plt.savefig("scaling.png")

try:
    plot()

except:

    u       = mda.Universe(WATERSMALL_GRO)
    radii=pytim_data.vdwradii(G43A1_TOP)
    u.atoms.write("test.pdb")
    
    times=[]
    
    for n in range(9):
        box = u.atoms.dimensions[:]
        interface =pytim.ITIM(u,max_layers=1,molecular=True)#,cluster_cut=3.5)
        g = u.select_atoms('all')
        nres = g.resids[-1]
        natm = g.ids[-1]
        print nres," molecules"
    
        pytim.lap()
        interface.assign_layers()
        times.append((natm,pytim.lap()))
    
        u2 = mda.Merge(g,g)
        u2.atoms.dimensions=box[:]
        u2.atoms.dimensions[0]=box[0]*2
        u2.atoms[natm:].resids += nres
        u2.atoms[natm:].translate([box[0],0,0])
        u2.atoms.write("test.pdb")
    
        del interface
        del u2
        del u
        u = mda.Universe("test.pdb")
    
    np.savetxt('timings.dat',times)
    plot()
