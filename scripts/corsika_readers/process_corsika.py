#!/bin/sh /cvmfs/icecube.opensciencegrid.org/py3-v4.2.1/icetray-start
#METAPROJECT /cvmfs/icecube.opensciencegrid.org/py3-v4.2.1/RHEL_7_x86_64/metaprojects/icetray/v1.9.2/

from icecube import icetray, dataio, dataclasses, simclasses,  recclasses, astro, MuonGun
import numpy as np
from optparse import OptionParser


parser = OptionParser()
parser.add_option("--filelist", type = "string", action = "store", default = None, metavar  = "<filelist>", 
                  help = "list of file provided in a txt",)
parser.add_option("--outpath", type = "string", action = "store", default = None, metavar  = "<outpath>", 
                  help = "output path")

(options, args) = parser.parse_args()
filelist = options.filelist
outpath = options.outpath

with open(filelist, "r") as file:
    paths = [line.strip() for line in file]

def files(args, include_frames=[], print_file=False):
    """A frame generator that can continue over multiple files"""
    if not isinstance(args, list):
        args = [args]
    
    for a in args:
        try:
            with dataio.I3File(a) as i3file:
                if print_file: print(f"Opening: {a}")
                for frame in i3file:
                    if len(include_frames) and not frame.Stop.id in include_frames:
                        continue
                    yield frame
        except RuntimeError:
            print(f"Error opening file: {a}")
            pass

def process_frame(frame):
    """Extract relevant particles (neutrinos + muons) from an air shower."""
    if "I3MCTree" not in frame:
        return None
    
    # mctree = frame["I3MCTree"]
    # new_mc_tree = dataclasses.I3MCTree()
    # new_mc_tree_coincidence = dataclasses.I3MCTree()
    
    # polyplopia_primary = frame["PolyplopiaPrimary"]
    
    # for particle in mctree:
    #     if abs(particle.pdg_encoding) in [12, 14, 16, 13]:
    #         if mctree.get_primary(particle) == polyplopia_primary:
    #             new_mc_tree.insert(particle)
    #         else:
    #             new_mc_tree_coincidence.insert(particle)
    
    new_frame = icetray.I3Frame(icetray.I3Frame.DAQ)
    new_frame["CorsikaWeightMap"] = frame["CorsikaWeightMap"]
    new_frame["PolyplopiaPrimary"] = frame["PolyplopiaPrimary"]
    new_frame["MMCTrackList"] = frame["MMCTrackList"]
    new_frame["I3MCTree"] = frame["I3MCTree"]
    # new_frame["PrimaryShower"] = new_mc_tree
    # new_frame["Coincidence"] = new_mc_tree_coincidence
    
    return new_frame

def process_files(input_files, output_file):
    """Process CORSIKA MC files and store selected particles in an output I3 file."""
    outfile = dataio.I3File(output_file, "w")
    
    for frame in files(input_files, print_file=True):
        new_frame = process_frame(frame)
        if new_frame:
            outfile.push(new_frame)
    
    outfile.close()
    print(f"Processed frames saved to {output_file}")

process_files(paths, outpath)