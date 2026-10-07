#!/usr/bin/env python3
"""Copy only parent mailbox inputs into the disposable build tree."""
import pathlib,sys,shutil
repo=pathlib.Path(sys.argv[1]).resolve();packet=pathlib.Path(__file__).resolve().parents[1]
for name in ['hdl/milan/mailbox','sw/firmware/ctrl','tb/verilator/mbx','tb/common']:
 shutil.copytree(repo/name,packet/'scratch/mailbox'/name,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','obj_*'))
