#!/usr/bin/env python3
"""Compare malformed-board refusal and observe the host TSpec derivation.

Usage: python3 regression_probe.py REPO PACKET
Loads the exact base/head builder blobs with unchanged checkout dependencies.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import yaml

repo,packet = map(lambda s:Path(s).resolve(),sys.argv[1:3])
os.chdir(repo)
sys.path.insert(0,str(repo/'sw/builder'))
tempfile.tempdir = str(packet/'scratch')
rows=[]
for rev in ('854bd7236792ce1adbd10c43b13a6a5002ad3bb6','677d605f37c3a80654df1dd2cde053b57242845b'):
    module=types.ModuleType('endstation_builder')
    module.__file__=str(repo/'sw/builder/endstation_builder.py')
    sys.modules[module.__name__]=module
    source=subprocess.check_output(['git','show',rev+':sw/builder/endstation_builder.py'])
    exec(compile(source,module.__file__,'exec'),module.__dict__)
    doc=yaml.safe_load((repo/'configs/endstation_ax7101_1x1_tdm8.yaml').read_text())
    for value in ([], '', ['ax7101']):
        with tempfile.TemporaryDirectory(prefix='refusal-') as d:
            config=Path(d)/'invalid.yaml'
            changed=copy.deepcopy(doc)
            changed['board']=value
            config.write_text(yaml.safe_dump(changed))
            try:
                module.load_config(str(config))
                outcome='accepted'
                reason=''
            except Exception as error:
                outcome=type(error).__name__
                reason=str(error)
            rows.append(dict(revision=rev,board=value,outcome=outcome,reason=reason))

# Inspect a valid host whose second supported format is wider than its current format.
doc=yaml.safe_load((repo/'configs/host/endstation_host_example.yaml').read_text())
doc['streams']['talkers'][0]['channels']=2
doc['streams']['talkers'][0]['formats']=[f'0x{module.aaf_pcm32(n,48000):016X}' for n in (2,8)]
with tempfile.TemporaryDirectory(prefix='tspec-') as d:
    config=Path(d)/'host.yaml'
    config.write_text(yaml.safe_dump(doc))
    cfg=module.load_config(str(config))
    overlay=module.emit_aem_overlay(cfg)
    image=module._entity_model_image(cfg,overlay)['aem_desc.bin']
    row=next(row for row in cfg['srp']['rows'] if row['direction']=='talker')
    rows.append(dict(case='host current two channels, supported two/eight',
        formats=cfg['talkers'][0]['formats'],max_frame_bytes=row['max_frame_bytes'],
        current_format_geometry=module.srp_frame_geometry(2,48000,8000)['max_frame_bytes'],
        widest_format_geometry=module.srp_frame_geometry(8,48000,8000)['max_frame_bytes'],
        image_bytes=len(image)))
(packet/'regression-result.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
