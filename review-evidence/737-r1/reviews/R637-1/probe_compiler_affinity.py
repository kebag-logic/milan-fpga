#!/usr/bin/env python3
"""Observe the pinned compiler's actual make invocation; do not compile a model.

The make substitute records argv and exits. This proves the -j 0 dispatch
budget only; it is not simulation or build-success evidence.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

tool = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
work = packet / 'scratch' / 'compiler-affinity'
work.mkdir(parents=True, exist_ok=True)
version = subprocess.check_output([str(tool), '--version'], text=True).strip()
assert version.startswith('Verilator 5.050 '), version
(work / 'budget_probe.sv').write_text('module budget_probe(input logic a, output logic y); assign y = a; endmodule\n')
(work / 'main.cpp').write_text('int main() { return 0; }\n')
observer = work / 'make-observer'
observer.write_text('#!/usr/bin/env python3\nimport json,os,sys\nfrom pathlib import Path\nPath(os.environ["PROBE_RECORD"]).write_text(json.dumps(sys.argv[1:]))\n')
observer.chmod(0o755)
available = sorted(os.sched_getaffinity(0))
assert len(available) >= 16
for count in (4, 12, 16):
    record = work / (str(count) + '.json')
    def affinity():
        os.sched_setaffinity(0, available[:count])
    command = [str(tool), '--cc', '--exe', '--build', '-j', '0', '--top-module', 'budget_probe',
               '--Mdir', str(work / ('obj_' + str(count))), str(work / 'budget_probe.sv'), str(work / 'main.cpp')]
    result = subprocess.run(command, cwd=work, text=True, capture_output=True, preexec_fn=affinity,
                            env=dict(os.environ, MAKE=str(observer), PROBE_RECORD=str(record),
                                     VERILATOR_JOBS=str(count // 4)))
    (work / (str(count) + '.log')).write_text(result.stdout + result.stderr)
    assert result.returncode == 0, result.stderr
    args = json.loads(record.read_text())
    actual = int(args[args.index('-j') + 1])
    assert actual == count
    print(json.dumps({'version': version, 'affinity_count': count,
                      'exported_VERILATOR_JOBS': count // 4, 'verilator_argument_j': 0,
                      'observed_make_j': actual, 'actual_compilation_performed': False}, sort_keys=True))
