#!/usr/bin/env python3
"""Compare base/head FPGA artifacts without altering tracked files.

Usage: python3 identity_probe.py REPO PACKET
The only changed generator module is loaded from each exact Git blob.
Its __file__ retains the checkout path so unchanged pinned dependencies
are resolved identically. All output directories are under PACKET/scratch.
Both explicit placements and the configuration's own placement are covered.
"""
import concurrent.futures
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import types

BASE = '854bd7236792ce1adbd10c43b13a6a5002ad3bb6'
HEAD = '677d605f37c3a80654df1dd2cde053b57242845b'
repo, packet = map(lambda s: Path(s).resolve(), sys.argv[1:3])
os.chdir(repo)

def capture(rev):
    sys.path.insert(0, str(repo / 'sw/builder'))
    path = 'sw/builder/endstation_builder.py'
    source = subprocess.check_output(['git', 'show', rev + ':' + path])
    module = types.ModuleType('endstation_builder')
    module.__file__ = str(repo / path)
    sys.modules[module.__name__] = module
    exec(compile(source, module.__file__, 'exec'), module.__dict__)
    for folder in ('adp', 'aecp', 'srp', 'plat'):
        sys.path.insert(0, str(repo / 'sw/firmware/ctrl' / folder))
    adp = importlib.import_module('adp_entity')
    aecp = importlib.import_module('aecp_entity')
    srp = importlib.import_module('srp_entity')
    plat = importlib.import_module('ctrl_plat_gen')
    rows = {}
    def put(name, data):
        if isinstance(data, str):
            data = data.encode()
        rows[name] = hashlib.sha256(data).hexdigest()
    for config in sorted((repo / 'configs').glob('endstation_*.yaml')):
        rel = config.relative_to(repo)
        for placement in (None, 'split', 'all-fabric'):
            label = config.stem + '@' + (placement or 'own')
            art = module._derive_artifacts(str(rel), placement)
            dest, _ = module._write_artifact_dir(art, packet / 'scratch' / rev / label)
            for file in sorted(dest.rglob('*')):
                if file.is_file():
                    put(label + '/' + str(file.relative_to(dest)), file.read_bytes())
            put(label + '/sweep.sh', art.sweep)
            for name, data in module._entity_model_image(art.cfg, art.overlay).items():
                put(label + '/image/' + name, data)
        for name, data in (
            ('adp', adp.emit_header(adp.entity_fields(rel), str(rel))),
            ('aecp', aecp.emit(rel)), ('srp', srp.emit(rel)), ('plat', plat.policy_header(rel))):
            put(config.stem + '/header/' + name, data)
    (packet / ('identity-' + rev[:8] + '.json')).write_text(json.dumps(rows, indent=2) + '\n')
    print(rev, len(rows), 'artifact hashes')

if len(sys.argv) == 4:
    capture(sys.argv[3])
else:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(packet / 'scratch'))
    def run(rev):
        with (packet / ('identity-' + rev[:8] + '.log')).open('w') as log:
            rc = subprocess.run([sys.executable, '-B', __file__, str(repo), str(packet), rev],
                                stdout=log, stderr=subprocess.STDOUT, env=env, timeout=540).returncode
        (packet / ('identity-' + rev[:8] + '.rc')).write_text(str(rc) + '\n')
        assert rc == 0, (rev, rc)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(run, (BASE, HEAD)))
    old, new = [json.loads((packet / ('identity-' + r[:8] + '.json')).read_text()) for r in (BASE, HEAD)]
    changed = [key for key in old.keys() | new.keys() if old.get(key) != new.get(key)]
    receipt = dict(base=BASE, head=HEAD, artifacts=len(old), changed=changed,
                   placements=['own', 'split', 'all-fabric'], configs=5)
    (packet / 'identity-result.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))
    assert not changed
