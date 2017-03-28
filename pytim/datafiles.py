# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
"""
Location of data files for Pytim examples and tests
====================================================

Real MD simulation data are stored in the ``data/`` subdirectory.


    Example: load an example trajectory

    >>> import MDAnalysis as mda
    >>> import pytim
    >>> from pytim.datafiles import *
    >>> u         = mda.Universe(WATER_GRO,WATER_XTC)
    >>> print u
    <Universe with 12000 atoms>

    Example: list all configurations

    >>> for config in sorted(pytim_data.config):
    ...     print("{:20s} {:s}".format(config,pytim_data.description[config]))
    MICELLE_PDB          DPC micelle
    WATERSMALL_GRO       small SPC water/vapour interface
    WATER_GRO            SPC water/vapour interface


    Example: list all topologies

    >>> print pytim_data.topol
    ['G43A1_TOP']

    Example: list all trajectories

    >>> print pytim_data.traj
    ['WATER_XTC']


    Example: list all files, file type, file format and description

    >>> for label in  pytim_data.label:
    ...      type        = pytim_data.type[label]
    ...      format      = pytim_data.format[label]
    ...      description = pytim_data.description[label]


"""

__all__ = [
    "WATER_GRO",             # GROMACS single frame, water/vapour interface
    "WATERSMALL_GRO",        # GROMACS single frame, water/vapour interface
    "METHANOL_GRO",          # XYZ, single frame, methanol/vapour interface with molecules in the vapour phase
    "ILBENZENE_GRO",         # Ionic liquid/benzene, partial miscibility
    "MICELLE_PDB",           # PDB of dodecylphosphocholine micelle in water
    "WATER_XTC",             # GROMACS trajectory, 100 frames, water/vapour interface
    "G43A1_TOP",             # GROMOS 43a1 nonbonded parameters, from gromacs distribution
    "pytim_data",            # class to access the data
    "_TEST_ORIENTATION_GRO", # test file
    "_TEST_PROFILE_GRO", # test file
]

from pkg_resources import resource_filename
import re as re


class Data(object):

    @property
    def config(self):
        labels = [label for label,val in self.type.iteritems() if val == 'config']
        return list(  set(labels) & set(self.label)   )

    @property
    def topol(self):
        labels = [label for label,val in self.type.iteritems() if val == 'topol']
        return list(  set(labels) & set(self.label)   )

    @property
    def traj(self):
        labels = [label for label,val in self.type.iteritems() if val == 'traj']
        return list(  set(labels) & set(self.label)   )

    def __init__(self):
        self._label=list()
        self.label=list()
        self.file=dict()
        self.type=dict()
        self.format=dict()
        self.description=dict()

    def add(self,label,type,format,desc):
        self._label.append(label)
        if label[0] is not '_':
            self.label.append(label)
        self.file[label]       = globals()[label]
        file = self.file[label]
        self.type[file]=type
        self.type[label]=type
        self.format[file]=format
        self.format[label]=format
        self.description[file]=desc
        self.description[label]=desc


    nm2angs=10.0

    def vdwradii(self,filename):
        if self.type[filename] == 'topol':
            if self.format[filename] == 'GMX':
                with open(filename) as _f:
                    scan=False
                    _radii=dict()
                    for _line in _f:
                        if (scan and re.match('^ *\[',_line)):
                            return _radii
                        if (scan):
                            try:
                                _data=(_line.split(";")[0]).split()
                                _atom = str(_data[0])
                                _c6  = float(_data[5])
                                _c12 = float(_data[6])
                                if (_c6 == 0.0 or _c12 == 0.0) :
                                    _sigma=0.0
                                else:
                                    _sigma = (_c12/_c6)**(1./6.) * self.nm2angs
                                _radii[_atom]=_sigma/2.
                            except:
                                pass
                        if (re.match('^ *\[ *atomtypes *\]',_line)):
                            scan=True
                return _radii


pytim_data=Data()

## NOTE: to add a new datafile, make sure it is listed in setup.py (in the root directory)
##       in the package_data option (a glob like 'data/*' is usually enough)
WATER_GRO      = resource_filename('pytim', 'data/water.gro')
pytim_data.add('WATER_GRO'  ,  'config', 'GRO', 'SPC water/vapour interface')

MICELLE_PDB    = resource_filename('pytim', 'data/micelle.pdb')
pytim_data.add('MICELLE_PDB',  'config', 'GRO','DPC micelle')

WATERSMALL_GRO = resource_filename('pytim', 'data/water-small.gro')
pytim_data.add('WATERSMALL_GRO'  ,  'config', 'GRO','small SPC water/vapour interface')

METHANOL_GRO   = resource_filename('pytim', 'data/methanol.gro')
pytim_data.add('METHANOL_GRO'  ,  'conf', 'GRO', 'methanol/vapour interface')

ILBENZENE_GRO = resource_filename('pytim', 'data/ilbenzene.gro')
pytim_data.add('ILBENZENE_GRO'  ,  'conf', 'GRO', 'BMIM PF4 / benzene interface')

WATER_XTC      = resource_filename('pytim', 'data/water.xtc')
pytim_data.add('WATER_XTC'  ,  'traj', 'XTC','SPC water/vapour interface trajectory')

_TEST_ORIENTATION_GRO = resource_filename('pytim', 'data/_test_orientation.gro')
pytim_data.add('_TEST_ORIENTATION_GRO',  'config', 'GRO','test file')

_TEST_PROFILE_GRO = resource_filename('pytim', 'data/_test_profile.gro')
pytim_data.add('_TEST_PROFILE_GRO',  'config', 'GRO','test file')

G43A1_TOP = resource_filename('pytim', 'data/ffg43a1.nonbonded.itp') # This should be the last line: clean up namespace
pytim_data.add('G43A1_TOP'  , 'topol' , 'GMX','GROMOS 43A1 topology for GROMACS')


del resource_filename