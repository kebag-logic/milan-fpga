#!/usr/bin/env python3
"""Focused read-only regression and mutation probes. Usage: REPO PACKET."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import yaml

repo, packet = (Path(x).resolve() for x in sys.argv[1:3])
os.chdir(repo)
os.environ.update(PYTHONDONTWRITEBYTECODE='1', GIT_NO_REPLACE_OBJECTS='1', TMPDIR=str(packet/'scratch'))
tempfile.tempdir = str(packet/'scratch')
sys.path.insert(0, str(repo/'sw/builder'))
import test_builder as tb
base = '854bd7236792ce1adbd10c43b13a6a5002ad3bb6'
prior = '677d605f37c3a80654df1dd2cde053b57242845b'
head = '66b4def34dcbc0d371ce4eb339d3d0226875befa'
path = 'sw/builder/endstation_builder.py'
def load(rev):
    src = subprocess.check_output(['git', 'show', rev+':'+path])
    module = types.ModuleType('probe_builder_'+rev[:8])
    module.__file__ = str(repo/path)
    sys.modules[module.__name__] = module
    exec(compile(src, module.__file__, 'exec'), module.__dict__)
    return module
modules = {rev:load(rev) for rev in (base, prior, head)}
fpga = tb.CONFIGS['ax7101_1x1_tdm8']
rows = []
for value in ([], '', ['ax7101'], None, 5):
    doc = yaml.safe_load(fpga.read_text())
    doc['board'] = value
    fixture = packet/'scratch'/'malformed.yaml'
    fixture.write_text(yaml.safe_dump(doc))
    for rev, mod in modules.items():
        try:
            mod.load_config(str(fixture))
        except Exception as exc:
            kind, message = type(exc).__name__, str(exc)
        else:
            raise AssertionError('malformed board accepted')
        expected = ('AttributeError' if rev == prior else
                    'TypeError' if value is None or value == 5 else 'ConfigError')
        assert kind == expected, (rev, value, kind)
        rows.append(dict(revision=rev, board=value, outcome=kind, message=message))
    if value == []:
        cli = subprocess.run([sys.executable, '-B', 'sw/firmware/ctrl/adp/adp_entity.py', str(fixture),
                              '-o', str(packet/'scratch'/'should-not-exist.h')], capture_output=True, text=True)
        assert cli.returncode == 2 and 'Traceback' not in cli.stderr
        assert "board: missing required key 'target'" in cli.stderr
        cli_receipt = dict(rc=cli.returncode, stdout=cli.stdout, stderr=cli.stderr)
mod = modules[head]
tb.eb = mod
assert tb._check_host_tspec() == (217, 73)
real_width = mod.framer_declared_channels
mod.framer_declared_channels = lambda cfg: max(mod.fmt_channels(t['formats'][0]) for t in cfg['talkers'])
try:
    tb._check_host_tspec()
except AssertionError as exc:
    mutant = str(exc)
    assert '73 octets' in mutant and '217' in mutant
else:
    raise AssertionError('current-format mutant survived')
finally:
    mod.framer_declared_channels = real_width
images = []
for rev in (prior, head):
    cfg = modules[rev].load_config(str(tb.HOST_EXAMPLE))
    data = modules[rev]._entity_model_image(cfg, modules[rev].emit_aem_overlay(cfg))['aem_desc.bin']
    images.append(dict(revision=rev, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
assert images[0]['sha256'] == images[1]['sha256'] == '9a59e2741913d93e9ad71bba890ce65d75fc4101170e9427997a00aa15ee29dd'
expected = json.loads((packet/'scratch/published/author-r2/receipts/identity-66b4def3.json').read_text())
spot = {}
for name in ('ax7101_1x1_tdm8', 'ax7101_8x8', 'arty_current'):
    config = tb.CONFIGS[name]
    art = mod._derive_artifacts(str(config.relative_to(repo)), None)
    dest, _ = mod._write_artifact_dir(art, packet/'scratch'/'spotcheck'/name)
    label = config.stem+'@own/'
    objects = {label+str(f.relative_to(dest)):f.read_bytes() for f in dest.rglob('*') if f.is_file()}
    objects[label+'sweep.sh'] = art.sweep.encode() if isinstance(art.sweep,str) else art.sweep
    for filename,data in mod._entity_model_image(art.cfg, art.overlay).items():
        objects[label+'image/'+filename] = data
    for key,data in objects.items():
        if isinstance(data, str):
            data = data.encode()
        digest = hashlib.sha256(data).hexdigest()
        assert digest == expected[key], key
        spot[key] = digest
result = dict(head=head, malformed_boards=rows, adp_cli=cli_receipt,
              tspec=dict(reserved=217, current_format=73, literal_formula='24*N + 24 + 1', mutant_rejected=mutant),
              example_images=images, regenerated_fpga_artifacts=spot)
packet.joinpath('delta-probes.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: 15 board outcomes across base/prior/head; ADP CLI controlled rc=2')
print('PASS: independent Table 4.4 arithmetic: 24*8+24+1=217; 24*2+24+1=73')
print('PASS: current-format mutant rejected; original gate restored in memory')
print('PASS: host example image identical; FPGA artifact spot-checks:',len(spot))
