#!/usr/bin/env python3
"""Selected builder gates, not the full bank. Usage: builder_checks.py REPO PACKET."""
import os
from pathlib import Path
import sys
import time
repo, packet = map(Path, sys.argv[1:3])
os.environ['TMPDIR'] = str(packet / 'scratch')
sys.path.insert(0, str(repo / 'sw/builder'))
import test_builder as t
t.OUT = packet / 'scratch/builder-out'
t.OUT.mkdir(parents=True, exist_ok=True)
standard = repo / 'sw/builder/out'
if not standard.exists():
 standard.symlink_to(t.OUT)
assert standard.is_symlink() and standard.resolve()==t.OUT.resolve(), 'Use a disposable checkout with output linked to packet scratch'
names = [
 'test_control_placement_key', 'test_placement_recipe',
 'test_firmware_version_derived_from_rtl', 'test_schema_11_configs_accepted_unchanged',
 'test_datapath_params_match_the_instance', 'test_datapath_params_gate_bites',
 'test_gptp_plane_reaches_the_instance', 'test_gptp_plane_instance_gate_bites',
 'test_every_recipe_elaborates', 'test_recipe_smoke_gate_bites',
 'test_image_identity_gate',
]
failed = []
for name in names:
 print('START', name, flush=True)
 start = time.monotonic()
 try:
  getattr(t, name)()
 except Exception as exc:
  print('FAIL', name, type(exc).__name__, str(exc), flush=True)
  failed.append(name)
 else:
  print('PASS', name, round(time.monotonic()-start, 2), flush=True)
print('SKIPPED', t.SKIPPED, flush=True)
print('FAILED', failed, flush=True)
sys.exit(bool(failed or t.SKIPPED))
