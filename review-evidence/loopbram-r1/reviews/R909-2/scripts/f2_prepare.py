#!/usr/bin/env python3
"""Disabled release-top export for one source tree (reviewer re-derivation of the
PR #987 F2 claim). Mirrors the author's prepare_builds.py / export_off.py:
builder output, platform firmware link, SoC export with the measurement hook.

usage: f2_prepare.py <tree> <work>
"""
import json
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
work.mkdir(parents=True, exist_ok=True)
SHAPES = ('endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8')

sys.path.insert(0, str(root / 'tb/verilator/ctrl_split_boot'))
import run as boot  # noqa: E402
import plat_ledger  # noqa: E402

builds = work / 'builds'
builds.mkdir(exist_ok=True)
archives = boot.runtime(builds)
for name in SHAPES:
    csr, flash = plat_ledger.maps(builds, name)
    out = builds / (name + '-off')
    if (out / 'ctrl_app.elf').exists():
        print(name, 'LINK reused', flush=True)
        continue
    args = [sys.executable, '-B', str(root / 'sw/firmware/ctrl/test/ctrl_plat_image.py'),
            '--config', str(root / 'configs' / f'{name}.yaml'), '--csr-csv', str(csr),
            '--flash-map', str(flash), '--output', str(out),
            '--libc', str(archives[0]), '--compiler-runtime', str(archives[1])]
    if '8x8' in name:
        args += ['--ledgered-point', 'platform-8x8-one-interface']
    with (builds / (name + '-off.log')).open('w') as log:
        rc = subprocess.run(args, cwd=root, stdout=log, stderr=subprocess.STDOUT, timeout=3600).returncode
    print(name, 'LINK', rc, flush=True)
    if rc or not (out / 'ctrl_app.elf').exists():
        raise SystemExit(f'link failed for {name}')

sys.path.insert(0, str(root / 'sw/builder'))
import endstation_builder as b  # noqa: E402

measure = work / 'measure_soc.py'
measure.write_text(f'''import sys,json
from pathlib import Path
sys.path.insert(0,{str(root / 'sw/litex')!r})
import ctrl_memory
original=ctrl_memory.plan
def plan(image,**kw):
 try:
  return original(image,**kw)
 except ctrl_memory.Refusal as error:
  if error.rule!='budget': raise
  print('MEASUREMENT ONLY:',error,flush=True)
  return original(image,budget=float('inf'))
ctrl_memory.plan=plan
import milan_soc
def scratch_output(entity_gen_dir,name):
 path=Path(entity_gen_dir)/name
 if not path.is_file(): raise RuntimeError(path)
 return str(path)
milan_soc._builder_out=scratch_output
milan_soc.main()
''')
gen_root = root / 'sw/builder/out/review_off'  # the SoC records overlay paths relative to the tree
for name in SHAPES:
    subprocess.run([sys.executable, str(root / 'sw/builder/endstation_builder.py'),
                    str(root / 'configs' / (name + '.yaml')), '-o', str(gen_root)],
                   cwd=root, check=True, timeout=600)
    gen = gen_root / name
    (gen / 'gen').mkdir(exist_ok=True)
    (gen / 'gen/adp_shape_defaults.svh').write_bytes((gen / 'adp_shape_defaults.svh').read_bytes())
    cfg = b.load_config(root / 'configs' / (name + '.yaml'))
    args = b.emit_soc_argv(cfg)
    args[args.index('--ctrl-firmware') + 1] = str(builds / (name + '-off') / 'ctrl_app.elf')
    out = work / 'export' / name
    out.mkdir(parents=True, exist_ok=True)
    args += ['--entity-gen-dir', str(gen), '--output-dir', str(out), '--no-compile-software',
             '--synth-directive', 'AreaOptimized_high', '--opt-directive', 'ExploreArea',
             '--place-directive', 'ExtraPostPlacementOpt', '--vivado-max-threads', '8']
    cmd = [sys.executable, str(measure), *args]
    (out / 'export-command.json').write_text(json.dumps(cmd, indent=2))
    with (out / 'export.log').open('w') as log:
        rc = subprocess.run(cmd, cwd=root, stdout=log, stderr=subprocess.STDOUT, timeout=3600).returncode
    print(name, 'EXPORT', rc, flush=True)
    if rc:
        print((out / 'export.log').read_text()[-3000:])
        raise SystemExit(rc)
