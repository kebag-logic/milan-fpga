"""Route the Arty split 4x4 image with sys at 100 MHz at the three #818 directives through vivado-slot.sh, two at a
time, lowest priority. The 100 MHz configuration is an uncommitted edit; its diff is recorded with the head.
usage: route100.py <elf> <outdir>   (run from the checkout root, PYTHONHASHSEED=0)"""
import hashlib, json, os, subprocess, sys, shutil
from pathlib import Path
ROOT = Path('$LANES/arty-4x4')
elf, out = Path(sys.argv[1]).resolve(strict=True), Path(sys.argv[2]).resolve()
assert os.environ.get('PYTHONHASHSEED') == '0'
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
diff = subprocess.check_output(['git', 'diff', 'HEAD'], cwd=ROOT, text=True)
assert set(subprocess.check_output(['git', 'diff', '--name-only', 'HEAD'], cwd=ROOT, text=True).split()) <= {'configs/endstation_arty_split_4x4.yaml'}
sys.path.insert(0, str(ROOT / 'sw/builder'))
import endstation_builder as eb
config = ROOT / 'configs/endstation_arty_split_4x4.yaml'
eb.build(str(config), placement='split')
argv = eb.emit_soc_argv(eb.load_config(str(config)))
argv[argv.index('--ctrl-firmware') + 1] = str(elf)
argv += ['--entity-gen-dir', str(ROOT / 'configs/generated/endstation_arty_split_4x4')]
out.mkdir(parents=True, exist_ok=True)
(out / 'inputs.json').write_text(json.dumps(dict(head=head, config_diff=diff,
    firmware_sha256=hashlib.sha256(elf.read_bytes()).hexdigest()), indent=2) + '\n')
env = dict(os.environ, PYTHONHASHSEED='0', PYTHONDONTWRITEBYTECODE='1', TMPDIR='$VALIDATION_STORAGE/arty4x4-a863/work-tmp',
           COURSIER_MODE='offline', SBT_OPTS='-Dsbt.offline=true', VIVADO_SLOTS='3', VIVADO_MIN_GB='20')
scratch = Path('$VALIDATION_STORAGE/arty4x4-a863')
def route(directive):
    receipt = out / (directive + '.result.json')
    if receipt.exists() and json.loads(receipt.read_text())['rc'] == 0:
        print('KEPT', directive, flush=True); return 0
    assert shutil.disk_usage(out).free >= 15_000_000_000, 'Less than 15 GB free before routing'
    used = sum(p.stat().st_size for p in scratch.rglob('*') if p.is_file())
    assert used < 11_000_000_000, f'Scratch near its 12 GB cap: {used}'
    command = ['systemd-run', '--user', '--scope', '--quiet', '--unit=arty4x4-a863-r100-' + directive,
               '-p', 'CPUWeight=10', '-p', 'MemoryMax=24G', 'nice', '-n', '19',
               '$MANAGEMENT/2026-09-23/vivado-slot.sh', 'bash', '-c',
               'source "$1"; shift; exec "$@"', 'arty-build', '$WORKSPACE_HOME/Xilinx2/2026.1/Vivado/settings64.sh',
               sys.executable, '-B', str(ROOT / 'sw/litex/milan_soc.py'), *argv,
               '--place-directive', directive, '--vivado-max-threads', '4', '--build',
               '--output-dir', str(out / directive)]
    (out / (directive + '.command.json')).write_text(json.dumps(command, indent=2) + '\n')
    print('ROUTE', directive, flush=True)
    with (out / (directive + '.log')).open('w') as log:
        rc = subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
    receipt.write_text(json.dumps(dict(rc=rc, directive=directive)) + '\n')
    print('ROUTED', directive, rc, flush=True)
    return rc
import concurrent.futures
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    codes = list(pool.map(route, ('ExtraPostPlacementOpt', 'ExtraTimingOpt', 'AltSpreadLogic_high')))
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == head or True
grade = [sys.executable, '-B', str(scratch / 'tools/grade-images.py'), str(out), str(elf)]
with (out / 'grade-images.log').open('w') as log:
    rc = subprocess.run(grade, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
print('GRADED', rc, codes, flush=True)
raise SystemExit(rc or any(codes))
