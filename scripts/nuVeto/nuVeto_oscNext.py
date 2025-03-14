#!/usr/bin/env python3

# Run with the virtual environment:/data/user/tchau/Software/.virtualenvs/DC_self_veto/
import numpy as np
import sys, os
import glob
import math
import pickle as pkl
import argparse


from nuVeto.nuveto import passing
from nuVeto.utils import Units
import crflux.models as pm


parser = argparse.ArgumentParser(description="using nuVeto package for computing passing fraction")


parser.add_argument("--cos_theta", type=float, default=1., help="cosine zenith value")
parser.add_argument("--Emin", type=float, default=1., help="minimum energy")
parser.add_argument("--Emax", type=float, default=1000., help="maximum energy")
parser.add_argument("--nE", type=int, default=50, help="number of energy scan logarithmally")
parser.add_argument("--nutype", type=str, default='nu_mu', help="neutrino type: nu_(e|mu)(bar)")
parser.add_argument("--fluxtype", type=str, default='conv', help="flux type: conv|pr|_parent_")
parser.add_argument("--depth", type=float, default=2100, help="depth of the muon")


args = parser.parse_args()
cos_theta = args.cos_theta
Emin = args.Emin
Emax = args.Emax
nE = args.nE
nutype = args.nutype
fluxtype = args.fluxtype
depth = args.depth

energies = np.logspace( np.log10(Emin), np.log10(Emax), nE )
kind = f"{fluxtype} {nutype}"

pf = [passing(enu *Units.GeV, cos_theta, kind=kind, prpl='mudet_oscNextL7',
             pmodel=(pm.HillasGaisser2012, 'H3a'),
             hadr='SIBYLL2.3c', depth=depth*Units.m,
             density=('CORSIKA', ('SouthPole','December'))) for enu in  energies]

output = {"cos_theta":cos_theta, "pf": pf, "energy":energies}
outpath = f"/data/user/tchau/Sandbox/SelfVeto_DeepCore/scripts/nuVeto/output_pf/pf_oscNext_L7_{cos_theta:.3f}_{fluxtype}_{nutype}_{depth}m.pkl"
with open(outpath, "wb") as file:
    pkl.dump(output, file)
file.close()
