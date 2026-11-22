#!/usr/bin/env python3
import pathlib, shutil, subprocess, sys
repo,out=map(pathlib.Path,sys.argv[1:]); scratch=out/'scratch/diagram'; scratch.mkdir(exist_ok=True)
shutil.copy2(repo/'docs/BUILD_FLASH_BOOT.gen.py',scratch/'BUILD_FLASH_BOOT.gen.py')
subprocess.run([sys.executable,'BUILD_FLASH_BOOT.gen.py'],cwd=scratch,check=True)
subprocess.run(['rsvg-convert','-w','2400','BUILD_FLASH_BOOT.svg','-o','BUILD_FLASH_BOOT.png'],cwd=scratch,check=True)
for ext in ('svg','png','drawio'):
 name='BUILD_FLASH_BOOT.'+ext
 assert (scratch/name).read_bytes()==(repo/'docs'/name).read_bytes()
 print(name,'regenerates byte-identically')
