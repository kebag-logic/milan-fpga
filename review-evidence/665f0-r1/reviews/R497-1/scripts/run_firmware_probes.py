#!/usr/bin/env python3
import pathlib,subprocess,sys,os
p=pathlib.Path(__file__).resolve().parents[1];r=pathlib.Path(sys.argv[1]).resolve();fw=r/'sw/firmware/ctrl'
sys.path.insert(0,str(fw/'test'));from ctrl_build import PORTABLE,INCLUDE_DIRS
cmd=['gcc','-std=c11','-O2','-Wall','-Wextra','-Werror','-pedantic',*["-I"+str(fw/d) for d in INCLUDE_DIRS],*[str(fw/s) for s in PORTABLE],str(fw/'host/mbx_model.c'),str(fw/'host/mbx_plat_host.c'),str(p/'scripts/firmware_probes.c'),'-o',str(p/'scratch/firmware_probes')]
print('Compile:', ' '.join(cmd),flush=True);subprocess.run(cmd,check=True)
sys.exit(subprocess.run([str(p/'scratch/firmware_probes')]).returncode)
