#!/usr/bin/env python3
"""Exercise the public board-owned entity.conf adapter against the exact head.

Usage: python3 entity_conf_probe.py REPO PACKET [--fetch]
--fetch downloads three exact public source files using read-only GitHub API calls.
Without --fetch the files are expected under PACKET/scratch.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

repo, packet = map(lambda s: Path(s).resolve(), sys.argv[1:3])
scratch = packet / 'scratch'
revision = 'cce8c9a4143548c80800b2def821431ff45e3698'
files = {
    'board-gen-entity-conf.sh': 'milan-linux/tools/gen-entity-conf.sh',
    'endstation_pb2_bridge.yaml': 'milan-linux/config/endstation_pb2_bridge.yaml',
    'board-entity.conf': 'milan-linux/config/entity.conf',
}
if '--fetch' in sys.argv:
    for name,path in files.items():
        result = subprocess.check_output(['gh','api',f'repos/kebag-logic/ti-sitara-am65x-bsp/contents/{path}?ref={revision}'])
        (scratch/name).write_bytes(base64.b64decode(json.loads(result)['content']))
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
records = []
for label, config in [('example',repo/'configs/host/endstation_host_example.yaml'),
                      ('board',scratch/'endstation_pb2_bridge.yaml')]:
    command = ['sh', str(scratch/'board-gen-entity-conf.sh'), str(repo),str(config)]
    generated = subprocess.check_output(command, env=env, stderr=subprocess.STDOUT).decode()
    fields = dict(line.split('=',1) for line in generated.splitlines() if '=' in line and not line.startswith('#'))
    assert int(fields['talker_stream_sources'],16) == 1
    assert int(fields['listener_stream_sinks'],16) == 2
    assert int(fields['entity_capabilities'],16) == 0xC588
    assert int(fields['talker_capabilities'],16) == 0x4001
    assert int(fields['listener_capabilities'],16) == 0x4801
    if label == 'board':
        expected = dict(line.split('=',1) for line in (scratch/'board-entity.conf').read_text().splitlines()
                        if '=' in line and not line.startswith('#'))
        assert fields == expected
        # The exported-tree revision marker is absent from a Git clone.
        # Only this provenance comment differs; no configuration value is normalized.
        expected_text = (scratch/'board-entity.conf').read_text().strip()
        normalized = generated.replace('at milan-fpga unknown,',
            'at milan-fpga 677d605f37c3a80654df1dd2cde053b57242845b,').strip()
        assert normalized == expected_text
    (packet/(label+'-entity.conf')).write_text(generated)
    records.append(dict(config=label,fields=fields,sha256=hashlib.sha256(generated.encode()).hexdigest()))
receipt = dict(board_revision=revision, inputs=[dict(path=path,
    url=f'https://github.com/kebag-logic/ti-sitara-am65x-bsp/blob/{revision}/{path}',
    sha256=hashlib.sha256((scratch/name).read_bytes()).hexdigest()) for name,path in files.items()],
    outputs=records, limit='Board daemon, runtime MAC substitution, media service and hardware not executed.')
(packet/'entity-conf-result.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
