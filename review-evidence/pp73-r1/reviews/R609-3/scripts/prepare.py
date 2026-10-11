#!/usr/bin/env python3
"""Prepare disposable source archives for the portable review scripts."""
import argparse,io,subprocess,tarfile
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--packet',type=Path,required=True);a=ap.parse_args()
for name,ref in [('head','15981b511370a8cfb58ec023fae27f8a800c058c'),('base','2cbed0a987c1e68402658d69459ab7e5aa571adc')]:
 d=a.packet/'scratch'/name
 if d.exists():raise SystemExit('Refusing to overwrite an existing disposable tree: '+str(d))
 d.mkdir(parents=True)
 data=subprocess.check_output(['git','-C',str(a.source),'archive',ref])
 with tarfile.open(fileobj=io.BytesIO(data)) as t:t.extractall(d,filter='data')
for name in ['receipts','scripts']:(a.packet/name).mkdir(exist_ok=True)
