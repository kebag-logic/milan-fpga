#!/usr/bin/env python3
"""Build the pinned unit-test dependency inside packet scratch, without installing it."""
import pathlib,subprocess
packet=pathlib.Path(__file__).resolve().parents[1];src=packet/'scratch/cgreen-src';build=packet/'scratch/cgreen-build'
if not src.exists():
 subprocess.run(['git','clone','--depth','1','--branch','1.6.4','https://github.com/cgreen-devs/cgreen.git',str(src)],check=True)
head=subprocess.check_output(['git','-C',str(src),'rev-parse','HEAD'],text=True).strip()
if head!='91ba387904d7f43c6564486690386e76d4f8bc76':raise SystemExit('Unexpected dependency revision')
subprocess.run(['cmake','-S',str(src),'-B',str(build),'-DCMAKE_BUILD_TYPE=Release','-DCGREEN_WITH_UNIT_TESTS=OFF','-DCGREEN_WITH_LIBXML2=OFF','-DCMAKE_POLICY_VERSION_MINIMUM=3.5'],check=True)
subprocess.run(['make','-C',str(build),'-j16'],check=True)
