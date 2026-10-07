#!/usr/bin/env python3
"""Select historical fixture/source population; keep runtime and shape generation fixed."""
import importlib.util,sys
from pathlib import Path
repo=Path(sys.argv.pop(1));mode=sys.argv.pop(1);export=Path(sys.argv.pop(1))
sys.path.insert(0,str(repo/'sw/firmware/ctrl/test'))
if mode=='round5':
 spec=importlib.util.spec_from_file_location('historical_image',export/'sw/firmware/ctrl/test/ctrl_image.py')
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 module.HERE=export/'sw/firmware/ctrl/test'
 module.PORTABLE=tuple(p for p in module.PORTABLE if not p.startswith('maap/'))
else:
 import ctrl_image as module
 if mode=='base':module.PORTABLE=tuple(p for p in module.PORTABLE if not p.startswith('maap/'))
raise SystemExit(module.main())
