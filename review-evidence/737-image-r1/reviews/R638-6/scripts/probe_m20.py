#!/usr/bin/env python3
"""M20: make's abspath is lexical; a committed symlink under it must not change the walked script."""
import os, sys, tempfile, json
from pathlib import Path
from probe_lib import Fixture, walker, yaml
with tempfile.TemporaryDirectory(prefix='r638-6-m20-') as d:
    fx = Fixture(Path(d))
    fx.file('Makefile', 'all: ; bash $(abspath sub/link/../run.sh)\n')
    fx.file('sub/run.sh', 'brand_new_command\n')
    fx.file('other/run.sh', 'echo okay\n')
    (Path(d) / 'other/deep').mkdir(parents=True)
    os.symlink('../other/deep', Path(d) / 'sub/link')
    fx.workflow.write_text(yaml.safe_dump({'jobs': {'gate': {'steps': [{'run': 'make'}]}}}))
    res = walker(fx)
    print(json.dumps({'probe': 'M20_abspath_symlink_lexical_committed_link', 'write': res['--write'], 'check': res['--check']}))
