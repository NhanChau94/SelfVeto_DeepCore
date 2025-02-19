#!/bin/sh /cvmfs/icecube.opensciencegrid.org/py3-v4.2.1/icetray-start
#METAPROJECT /cvmfs/icecube.opensciencegrid.org/py3-v4.2.1/RHEL_7_x86_64/metaprojects/icetray/v1.9.2/
import os
from optparse import OptionParser
import glob

def get_file_paths():
    """
    Get the file paths for CORSIKA files
    Note: for every 1000 file only one file contains "I3MCTree" with store muon loss energy information along its path
    Now only take these files (end as *000.i3.zst)
    """
    file_paths = []
    for i in range(0, 80000, 1000):
        file_pattern = f"/data/sim/IceCube/2023/generated/CORSIKA-in-ice/22803/*/*.{i:06d}.i3.zst"
        # print(file_pattern)
        file_paths.extend(glob.glob(file_pattern))
    return file_paths

filelist = get_file_paths()

output_dir = "/data/user/tchau/Sandbox/SelfVeto_DeepCore/scripts/corsika_readers/corsika_file_list"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

parser = OptionParser()
parser.add_option("-n", "--num-per-file", dest="num_per_file", type="int", default=1000,
                    help="number of file paths per output file")

(options, args) = parser.parse_args()

num_per_file = options.num_per_file

if num_per_file > len(filelist):
    num_per_file = len(filelist)

for i in range(0, len(filelist), num_per_file):
    output_file = os.path.join(output_dir, f"filelist_{i // num_per_file:03d}.txt")
    with open(output_file, 'w') as f:
        for path in filelist[i:i + num_per_file]:
            f.write(path + '\n')