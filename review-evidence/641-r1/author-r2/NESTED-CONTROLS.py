"""Prove nested failure refusal and inventory reads under the selected make."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path.cwd()
sys.path.insert(0, str(root / 'scripts'))
import shape_consumer_inventory as inventory
consumer = root / 'tb/verilator/pp_shadow/Makefile'
source = consumer.read_text()
block = 'ifneq ($(.SHELLSTATUS),0)\n$(error ../milan_dp print-srcs failed; the datapath source list could not be derived)\nendif\n'
assert source.count(block) == 1
rows = []
with tempfile.TemporaryDirectory(prefix='nested-control-') as directory:
    for label, text, refused in [('head', source, True), ('status-check-deleted', source.replace(block, ''), False)]:
        path = Path(directory) / 'Makefile'
        path.write_text(text)
        cmd = ['make', '-s', '--no-print-directory', '-C', str(consumer.parent), '-f', str(path),
               '--eval', 'nested-control:;', 'nested-control', 'MAKE=false']
        run = subprocess.run(cmd, capture_output=True, text=True, check=False)
        assert (run.returncode != 0) == refused, (label, run.stderr)
        if refused:
            assert '../milan_dp print-srcs failed' in run.stderr
        rows.append(dict(variant=label, rc=run.returncode, expected_refusal=refused))
for name in ('tb/verilator/pp_shadow/Makefile', 'tb/verilator/milan_dp_render/Makefile'):
    path = root / name
    ok, prereqs = inventory.shape_prereqs_from_database(path.parent, path.name)
    assert ok and prereqs, (name, ok, prereqs)
    rows.append(dict(consumer=name, readable=ok, prerequisites=prereqs))
version = subprocess.check_output(['make', '--version'], text=True).splitlines()[0]
print(json.dumps(dict(make=version, controls=rows), indent=2))
