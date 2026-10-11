import ast
from collections import Counter
from contextlib import redirect_stdout
import hashlib
from io import StringIO
import json
from pathlib import Path
import re
import subprocess
import sys
from types import ModuleType
from unittest.mock import patch
import yaml

root = Path.cwd()
work = Path(__file__).resolve().parent
out = Path(sys.argv[1])
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(root / 'scripts'))
import test_ctrl_firmware as driver
import test_ctrl_firmware_shards as probe
import ci_events

base = '09c7231eca343607c97c0d66abebb2553688712c'
def at_base(path):
    return subprocess.check_output(['git', 'show', f'{base}:{path}'], text=True)

source = at_base('sw/firmware/ctrl/test/test_ctrl_firmware.py')
original = ModuleType('original_driver')
original.__file__ = str(root / 'sw/firmware/ctrl/test/test_ctrl_firmware.py')
sys.modules[original.__name__] = original
exec(compile(source, original.__file__, 'exec'), original.__dict__)
with patch.object(original, 'run_selected', lambda *args: original.main(
        ['--require-rv32', '--self-test', '--jobs', '4']), create=True), patch.object(original, 'cut_reuse'):
    expected = probe.inventory(original)
actual = probe.inventory(driver)
shards = [probe.inventory(driver, (i, 4)) for i in range(4)]
assert expected == actual == [call for shard in shards for call in shard]
assert len(set(expected)) == len(expected)
assert any('arm_srpcmp' in call for call in shards[0])
for name in driver.srp_pub_mutants.ROUND5:
    for interfaces in (1, 2):
        assert 'srp-if%d:' % interfaces + name in shards[3], (name, interfaces)

def stripped_coverage(text):
    return ast.dump(next(node for node in ast.parse(text).body
                         if isinstance(node, ast.FunctionDef) and node.name == 'coverage'))
assert stripped_coverage(source) == stripped_coverage(Path(driver.__file__).read_text())
coverage_paths = subprocess.check_output(['git', 'ls-files', 'sw/firmware/gtest',
                                        'sw/firmware/ctrl_nvm'], text=True).splitlines()
for path in coverage_paths:
    baseline = subprocess.check_output(['git', 'show', f'{base}:{path}'])
    assert baseline == Path(path).read_bytes(), path

baseline_wf = yaml.safe_load(at_base('.github/workflows/rtl-fast.yml'))
head_wf = yaml.safe_load(Path('.github/workflows/rtl-fast.yml').read_text())
before = ci_events.firmware_census(baseline_wf)
after = ci_events.firmware_census(head_wf)
assert ci_events.firmware_commands(before) == ci_events.firmware_commands(after)
assert before == ci_events.firmware_baseline_census()
assert head_wf['jobs']['publication-census'] == baseline_wf['jobs']['publication-census']

# Independently compare execution guards and action/cache metadata.
def steps(workflow, jobnames):
    rows=[]
    for jid in jobnames:
        job=workflow['jobs'][jid]
        for step in job['steps']:
            row={k:v for k,v in step.items() if k not in ('name','run')}
            row['job_if']=job.get('if','success()')
            if 'run' in step:
                for line in step['run'].splitlines():
                    if line.strip():
                        rows.append(json.dumps(dict(row, run=re.sub(r' --shard [0-3]/4$', '', line.strip())),sort_keys=True))
            else:
                rows.append(json.dumps(row,sort_keys=True))
    return set(rows)
assert steps(baseline_wf,['firmware-unit']) == steps(head_wf,ci_events.FIRMWARE_JOBS)
missing = shards.copy()
missing[0] = [call for call in shards[0] if 'arm_srpcmp' not in call]
assert probe.differences(expected, missing)['missing']
duplicate = shards.copy()
duplicate[1] = shards[1] + [call for call in shards[0] if 'arm_srpcmp' in call]
assert probe.differences(expected, duplicate)['duplicate_or_unexpected']

for name, value in [('ROUND2-BASELINE-INVOCATIONS.json', expected),
                    ('ROUND2-SHARD-INVOCATIONS.json', shards),
                    ('ROUND2-COMMAND-CENSUS.json',dict(base=base,before=before,after=after,preserved=True))]:
    (out/name).write_text(json.dumps(value,indent=2)+'\n')
result=dict(base=base,invocations=len(expected),shard_sizes=list(map(len,shards)),
            commands_before=len(before),commands_after=len(after),
            ordered_inventory_equal=True, independent_step_metadata_equal=True,
            publication_job_unchanged=True, coverage_function_ast_equal=True,
            coverage_support_files_equal=len(coverage_paths),
            srp_round5_mutants_both_interfaces=list(driver.srp_pub_mutants.ROUND5),
            planted_comparator_omission_rejected=True,planted_comparator_duplication_rejected=True)
(out/'ROUND2-PRESERVATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
