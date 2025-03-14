#!/usr/bin/env python3
import os
import numpy as np

#############################################################################################################
#   Create .config, .submit files
#
submit_dir = '/home/tchau/code/condor_submit/nuVeto/'
logdir = '/scratch/tchau/nuVeto_log/'
if not (os.path.exists(submit_dir)): os.makedirs(submit_dir)
if not (os.path.exists(logdir)): os.makedirs(logdir)

cfig_file = f'{submit_dir}/dagman.config'
sub_file = f'{submit_dir}/nuVeto.submit'
curdir=os.getcwd()
script_file = f'{curdir}/nuVeto_oscNext.py'

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
    s.write('arguments = --cos_theta $(cos_theta) --nutype $(nutype) --depth $(depth)'+'\n')
    s.write('queue')
    s.close()

#############################################################################################################
# create list of jobs in dagfile and the submit shell script

submit = f'{submit_dir}/submit.sh'
dag_file = f'{submit_dir}/nuVeto.dag'
cos_theta = np.linspace(0, 1, 40)
nutypes = ["nu_e", "nu_mu", "nu_tau", "nu_ebar", "nu_mubar", "nu_taubar"]
depths = [2450, 2275]

with open(dag_file, 'w') as f:
    for nu in nutypes:
        for cz in cos_theta:
            for depth in depths:
                JOBNAME = f"nuVeto_{nu}{cz:.3f}{depth}m"
                f.write(f'JOB {JOBNAME}'+' nuVeto.submit \n')
                f.write(f'VARS {JOBNAME}'
                        +f' JOBNAME="{JOBNAME}"'
                        +f' cos_theta="{cz}" nutype="{nu}" depth="{depth}"'+'\n')
f.close()

with open(submit, 'w') as s:
    s.write("#!/bin/sh\n")
    s.write("condor_submit_dag -config dagman.config {}\n".format(dag_file))
    print("condor_submit_dag -config dagman.config {}\n".format(dag_file))
s.close()