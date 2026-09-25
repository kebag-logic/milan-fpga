import json
from run_gate import OUT, run
for suite in ('pp_shadow', 'csr'):
    assert run('final-clean-' + suite, ['make', '-C', 'tb/verilator/' + suite, 'clean']) == 0
    label = 'final-cold-' + suite
    rc = run(label, ['timeout', '1800', 'make', '-C', 'tb/verilator/' + suite])
    if rc == 124:
        raise SystemExit('STOP: suite exceeded its 1800-second budget')
    assert rc == 0
    seconds = json.loads((OUT / (label + '.json')).read_text())['seconds']
    if seconds > 1800:
        raise SystemExit('STOP: suite exceeds its 1800-second budget')
