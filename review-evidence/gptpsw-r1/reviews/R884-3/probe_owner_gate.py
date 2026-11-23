#!/usr/bin/env python3
"""Run gate 1c and inject source-read plants without editing the checkout."""
from pathlib import Path
import importlib.util
import os
import sys
import tempfile
from unittest.mock import patch

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
tempfile.tempdir = str(out/'scratch')
os.environ['TMPDIR'] = tempfile.tempdir
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('review_builder', root/'sw/builder/test_builder.py')
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)
read = Path.read_text
soc = root/'sw/litex/milan_soc.py'
text = read(soc)
cases = [
    ('control', text, False),
    ('unconditional software ownership', text.replace('elif gptp_sw:', 'elif True:'), True),
    ('second software owner', text + '\nself._gptp_owner = "software"\n', True),
]
for name, source, fail in cases:
    def replacement(path, *args, **kwargs):
        return source if path == soc else read(path, *args, **kwargs)
    with patch.object(Path,'read_text',replacement):
        try:
            mod.test_gptp_product_default_and_legacy_option()
        except AssertionError as exc:
            assert fail, str(exc)
            print(name + ': caught: ' + str(exc))
        else:
            assert not fail, name + ' escaped'
            print(name + ': PASS')
