"""Falsify the unknown-inline rejection with ordinary interpreter invocations."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(sys.argv[1]).resolve()
PACKET = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'ci/image'))
import exec_audit as audit

names = audit.allowlist()
scratch = PACKET / 'scratch/inline'
scratch.mkdir(parents=True, exist_ok=True)
results = []
for name, argv in [('perl', ['/usr/bin/perl', '-e', 'print "marker-perl\\n"']),
                   ('node', ['node', '-e', 'console.log("marker-node")']),
                   ('python', ['python3.12', '-c', 'print("marker-python")'])]:
    run = subprocess.run(argv, text=True, capture_output=True, check=True)
    instance = {'program': '/usr/bin/' + ('python3.12' if name == 'python' else name),
                'argv': argv, 'directory': str(scratch), 'streams': {}}
    origin = object.__new__(audit.Origin)
    origin.texts = set()
    origin.pinned = names['inline_programs']
    instance['provenance'] = origin.judge(instance)
    population, findings = audit.judge({'instances': [instance], 'exit_status': run.returncode}, names)
    results.append({'case': name, 'actual_output': run.stdout, 'instance': instance,
                    'population': population, 'findings': findings})
    print(name, instance['provenance'], 'findings', len(findings), repr(run.stdout))

# A real trace, without changing the source or installing anything.
command = '''perl -e 'print "marker-traced-perl\\n"' '''
report = audit.audit_step({'job': 'inline-probe', 'label': 'unlisted Perl inline',
                          'argv': ['/bin/bash', '-e', '-c', command], 'text': command},
                         names, scratch, {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C.UTF-8'},
                         PACKET / 'inline-trace.jsonl')
results.append({'case': 'actual-traced-perl', 'report': report})
command = "printf 'puts marker-traced-tcl\\n' | tclsh"
tcl_report = audit.audit_step({'job': 'inline-probe', 'label': 'unlisted Tcl stdin',
                              'argv': ['/bin/bash', '-e', '-c', command], 'text': command},
                             names, scratch, {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C.UTF-8'},
                             PACKET / 'tcl-trace.jsonl')
results.append({'case': 'actual-traced-tcl', 'report': tcl_report})
(PACKET / 'inline-probes.json').write_text(json.dumps(results, indent=2) + '\n')
print('Actual Perl trace clean:', report['clean'], 'findings:', report['findings'])
print('Actual Tcl trace clean:', tcl_report['clean'], 'findings:', tcl_report['findings'])
