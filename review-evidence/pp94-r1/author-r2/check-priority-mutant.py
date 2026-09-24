#!/usr/bin/env python3
"""Show the priority mutant and require the new completed assertion to kill it."""
import difflib
import json
from pathlib import Path
import subprocess
from runpy import run_path

CONFIG = run_path(str(Path(__file__).with_name('run-gates.py')))
ROOT = CONFIG['ROOT']
PACKET = CONFIG['PACKET']
ENV = CONFIG['ENV']
SOURCE = ROOT / 'hdl/aecp/KL_aecp_desc_mem_guard.sv'
ORIGINAL = """    end else if (m_req_valid_o && m_req_ready_i) begin
      owed_r <= 1'b1;
    end else if (m_rsp_valid_i && m_rsp_ready_o
                 && (m_rsp_last_i || m_rsp_err_i)) begin
      owed_r <= 1'b0;
"""
MUTATED = """    end else if (m_rsp_valid_i && m_rsp_ready_o
                 && (m_rsp_last_i || m_rsp_err_i)) begin
      owed_r <= 1'b0;
    end else if (m_req_valid_o && m_req_ready_i) begin
      owed_r <= 1'b1;
"""


def main() -> int:
    """Run both builds; accept only the exact simulated priority failure."""
    source = SOURCE.read_text()
    assert source.count(ORIGINAL) == 1
    mutant = source.replace(ORIGINAL, MUTATED)
    mutant_path = PACKET / 'KL_aecp_desc_mem_guard.clear_priority.sv'
    mutant_path.write_text(mutant)
    (PACKET / 'priority-mutant.diff').write_text(''.join(difflib.unified_diff(
        source.splitlines(True), mutant.splitlines(True),
        fromfile='a/hdl/aecp/KL_aecp_desc_mem_guard.sv',
        tofile='b/hdl/aecp/KL_aecp_desc_mem_guard.sv')))
    results = []
    for label, extra in [('guard', []), ('priority-mutant', [
            f'GUARD_SRC={mutant_path}', 'OBJ_DIR=obj_priority_mutant'])]:
        command = ['make', '-C', 'tb/desc_mem_guard', 'run', *extra]
        with (PACKET / f'{label}.log').open('w') as stream:
            rc = subprocess.run(command, cwd=ROOT, env=ENV, stdout=stream,
                                stderr=subprocess.STDOUT, timeout=1800).returncode
        results.append({'name': label, 'command': command, 'rc': rc})
    text = (PACKET / 'priority-mutant.log').read_text()
    failures = [line for line in text.splitlines() if line.startswith('FAIL:')]
    expected = 'FAIL: request acceptance must win over a coincident stray terminal beat'
    detected = (results[0]['rc'] == 0 and results[1]['rc'] == 2
                and failures == [expected] and '78 checks: 77 PASS, 1 FAIL' in text
                and '78 checks: 78 PASS, 0 FAIL' in (PACKET / 'guard.log').read_text())
    (PACKET / 'priority-results.json').write_text(json.dumps(
        {'runs': results, 'detected': detected, 'failures': failures}, indent=2) + '\n')
    print(f'guard rc={results[0]["rc"]}; priority mutant rc={results[1]["rc"]}; detected={detected}')
    print('\n'.join(failures))
    return 0 if detected else 1


if __name__ == '__main__':
    raise SystemExit(main())
