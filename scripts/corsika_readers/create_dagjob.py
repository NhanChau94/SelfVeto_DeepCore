#!/usr/bin/env /cvmfs/icecube.opensciencegrid.org/py3-v4.2.1/RHEL_7_x86_64/bin/python

import glob
import pickle as pkl
import sys, os
import numpy as np
import json
from optparse import OptionParser

#############################################################################################################
#   Create .config, .submit files
#
submit_dir = '/home/tchau/code/condor_submit/corsika_22803_reader/'
logdir = '/scratch/tchau/corsika22803_logs/'
if not (os.path.exists(submit_dir)): os.makedirs(submit_dir)
if not (os.path.exists(logdir)): os.makedirs(logdir)

output_dir = "/data/user/tchau/CORSIKA_22803/"
if not (os.path.exists(output_dir)): os.makedirs(output_dir)

cfig_file = f'{submit_dir}/dagman.config'
sub_file = f'{submit_dir}/corsika.submit'
curdir=os.getcwd()
script_file = f'{curdir}/process_corsika.py'

with open(cfig_file, 'w') as c:
    c.write('DAGMAN_MAX_JOBS_SUBMITTED=500'+'\n')
    c.write('DAGMAN_MAX_SUBMIT_PER_INTERVAL=20'+'\n')
    c.write('DAGMAN_USER_LOG_SCAN_INTERVAL=10'+'\n')
    c.close()

with open(sub_file, 'w') as s:
    s.write(f'executable = {script_file}'+'\n')
    s.write('\n')
    s.write('initialdir = /data/user/tchau/'+'\n')
    s.write(f'logdir = {logdir}'+'\n')
    s.write('output = $(logdir)$(JOBNAME).$(Cluster).out'+'\n')
    s.write('error = $(logdir)$(JOBNAME).$(Cluster).err'+'\n')
    s.write('log = $(logdir)$(JOBNAME).$(Cluster).log'+'\n')
    s.write('\n')
    s.write('notification   = never'+'\n')
    s.write('universe       = vanilla'+'\n')
    s.write('\n')
    s.write('should_transfer_files = YES'+'\n')
    s.write('request_memory = 10GB'+'\n')
    s.write('getenv = True'+'\n')
    s.write('\n')
    s.write('arguments = --filelist $(filelist) --outpath $(outpath) '+'\n')
    s.write('queue')
    s.close()

#############################################################################################################
# create list of jobs in dagfile and the submit shell script

submit = f'{submit_dir}/submit.sh'
dag_file = f'{submit_dir}/corsika.dag'
listpath = glob.glob("/data/user/tchau/Sandbox/SelfVeto_DeepCore/scripts/corsika_readers/corsika_file_list/*.txt")

with open(dag_file, 'w') as f:
    for i, path in enumerate(listpath):
        JOBNAME = f"corsika_reader_{i}"
        outpath = f"{output_dir}/corsika22803_processed_{i}.i3.zst"
        f.write(f'JOB {JOBNAME}'+' corsika.submit \n')
        f.write(f'VARS {JOBNAME}'
                +f' JOBNAME="{JOBNAME}"'
                +f' filelist="{path}" outpath="{outpath}"'+'\n')
f.close()

with open(submit, 'w') as s:
    s.write("#!/bin/sh\n")
    s.write("condor_submit_dag -config dagman.config {}\n".format(dag_file))
    print("condor_submit_dag -config dagman.config {}\n".format(dag_file))
s.close()

