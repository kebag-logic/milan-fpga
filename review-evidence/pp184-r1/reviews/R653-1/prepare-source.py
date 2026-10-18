#!/usr/bin/env python3
import pathlib,subprocess,sys
p=pathlib.Path(__file__).resolve().parent
repo=pathlib.Path(sys.argv[1]).resolve()
s=p/'scratch/source'
if s.exists():raise SystemExit('Use a fresh packet copy: scratch/source already exists')
s.parent.mkdir(exist_ok=True)
subprocess.run(['git','clone','--shared','--no-checkout',str(repo),str(s)],check=True)
subprocess.run(['git','-C',str(s),'checkout','--detach','e11fb36b366587b5e2403c5d47452c16aae6ec31'],check=True)
