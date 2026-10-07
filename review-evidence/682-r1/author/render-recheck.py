"""Rebuild the four failed campaign cases after all shared-header writers exit."""
import importlib.util
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path('$LANES/682-pp-pin3')
work = Path('$VALIDATION_STORAGE/682-a554/render-recheck')
work.mkdir(exist_ok=True)
source = root / 'tb/verilator/milan_dp_render/tdm8_render_mutants.py'
spec = importlib.util.spec_from_file_location('render_campaign', source)
campaign = importlib.util.module_from_spec(spec)
spec.loader.exec_module(campaign)
header = 'hdl/common/csr/gen/lwsrp_csr_defaults.svh'
expected = subprocess.check_output(['git', 'show', 'HEAD:' + header], cwd=root)
def stable():
    assert (root / header).read_bytes() == expected, 'shared header differs from HEAD'
cases = [('unmutated epoch', None, [], 'ship', '--epoch-only', None)]
cases += [(name, src, edits, leg, mode, None) for name, src, edits, leg, mode in campaign.CLEAN_CONTROLS if 'acknowledgement level' in name or 'serial-reset level' in name]
cases += [row for row in campaign.MUTATIONS if row[0].startswith('uncounted repeat:')]
assert len(cases) == 4
rows = []
for index, (name, src, edits, leg, mode, required) in enumerate(cases):
    stable()
    overrides = {}
    if src:
        value, why = campaign.plant(src, edits, work, str(index))
        assert value is not None, why
        overrides[campaign.SOURCES[src][1]] = value
    target, variable, exe_name, _ = campaign.LEGS[leg]
    directory = work / ('obj_' + str(index))
    command = ['make', '-s', '-C', str(campaign.HERE), target, variable + '=' + str(directory)]
    command += [key + '=' + value for key, value in overrides.items()]
    build_log = work / ('build-' + str(index) + '.log')
    with build_log.open('w') as output:
        build = subprocess.run(command, stdout=output, stderr=subprocess.STDOUT)
    assert build.returncode == 0, (name, build.returncode)
    stable()
    rc, output = campaign.run_leg(directory / exe_name, mode)
    log = work / ('run-' + str(index) + '.log')
    log.write_text(output)
    verdict = campaign.verdict(rc, output, required)
    passed = verdict == ('caught' if required else 'pass')
    rows.append(dict(name=name, mode=mode, required_failure=required, build_command=command,
                     build_rc=build.returncode, rc=rc, verdict=verdict, campaign_case_pass=passed,
                     log=str(log), bytes=log.stat().st_size,
                     sha256=hashlib.sha256(log.read_bytes()).hexdigest(),
                     failures=[line for line in output.splitlines() if line.strip().startswith('[FAIL]')]))
    (work / 'receipts.json').write_text(json.dumps(rows, indent=2) + '\n')
    print(name, 'rc', rc, verdict, 'campaign_case_pass', passed, flush=True)
    stable()
print('Shared header SHA256', hashlib.sha256(expected).hexdigest(), flush=True)
raise SystemExit(0 if all(row['campaign_case_pass'] for row in rows) else 1)
