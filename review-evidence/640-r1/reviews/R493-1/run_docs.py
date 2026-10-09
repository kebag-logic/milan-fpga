#!/usr/bin/env python3
"""Run independent lightweight documentation checks; wait for every child."""
import concurrent.futures
import json
import os
import subprocess
import sys
import time
from pathlib import Path

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
scratch = out.parent / 'scratch'
(scratch / 'tmp').mkdir(parents=True, exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch / 'tmp'), PYTHONDONTWRITEBYTECODE='1',
           PATH=str(Path(sys.executable).parent) + os.pathsep + os.environ['PATH'])
commands = [
 ('docs', 'scripts/docs_check.py'),
 ('docs-self', 'scripts/docs_check.py --selftest'),
 ('feature', 'scripts/check_feature_status.py --self-test'),
 ('em-dash', 'scripts/check_em_dash.py --base 5603c353137e90c1fa95429f6d00ef7a2298d9ee'),
 ('style', 'scripts/check_doc_style.py'),
 ('style-self', 'scripts/check_doc_style.py --selftest'),
 ('gptp-docs', 'scripts/check_gptp_docs.py --with-submodule'),
 ('gptp-docs-self', 'scripts/check_gptp_docs.py --selftest'),
 ('doc-map', 'docs/DOC_MAP.gen.py --check'),
 ('doc-map-self', 'docs/DOC_MAP.gen.py --selftest'),
 ('timesync', 'docs/diagrams/timesync_chain.gen.py --check'),
 ('timesync-self', 'docs/diagrams/timesync_chain.gen.py --selftest'),
 ('solution', 'scripts/check_solution_docs.py'),
 ('solution-self', 'scripts/check_solution_docs.py --selftest'),
 ('submodule-diagram', 'docs/diagrams/submodule_boundaries.gen.py --check'),
 ('submodule-diagram-self', 'docs/diagrams/submodule_boundaries.gen.py --selftest'),
 ('submodule-docs', 'scripts/check_submodule_docs.py'),
 ('submodule-docs-self', 'scripts/check_submodule_docs.py --selftest'),
 ('diagram-pngs', 'scripts/check_diagram_pngs.py'),
 ('diagram-pngs-self', 'scripts/check_diagram_pngs.py --selftest'),
 ('matrix', 'docs/traceability/gen_module_matrix.py --check'),
 ('baremetal', 'scripts/check_baremetal_only.py --check'),
 ('baremetal-self', 'scripts/check_baremetal_only.py --selftest'),
 ('doc-paths', 'scripts/check_doc_paths.py'),
 ('archive', 'scripts/check_archive.py'),
 ('archive-self', 'scripts/check_archive.py --selftest'),
 ('toc-self', 'scripts/gen_toc.py --selftest'),
 ('toc-anchors', 'scripts/gen_toc.py --verify-anchors'),
 ('toc-check', 'scripts/gen_toc.py --check'),
 ('todo', 'scripts/check_todo_ownership.py'),
 ('hygiene', 'scripts/check_hygiene.py --check'),
 ('wire', 'scripts/check_wire_accountability.py --self-test'),
 ('resource-baseline', 'syn/ooc/pp_resource_gate.py check-baseline'),
 ('ci-scope', 'scripts/ci_scope.py --selftest'),
 ('ci-events', 'scripts/ci_events.py --check'),
 ('wavedrom-self', 'scripts/gen_wavedrom.py --selftest'),
 ('wavedrom-axis', 'scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check'),
 ('wavedrom-cdc', 'scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check'),
 ('wavedrom-gptp', 'scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check'),
 ('pp-sources', 'scripts/pp_srcs.py --check --selftest'),
 ('docs-nogit', 'scripts/docs_check.py'),
]

def run(item):
    name, command = item
    argv = [sys.executable, *command.split()]
    child_env = dict(env)
    if name == 'docs-nogit':
        child_env['GIT_DIR'] = '/dev/null'
    start = time.monotonic()
    with (out / (name + '.log')).open('wb') as log:
        try:
            rc = subprocess.run(argv, cwd=root, env=child_env, stdout=log,
                                stderr=subprocess.STDOUT, timeout=240).returncode
        except subprocess.TimeoutExpired:
            rc = 124
    (out / (name + '.rc')).write_text(str(rc) + '\n')
    result = {'name':name, 'argv':['python3', *command.split()], 'rc':rc,
              'seconds':round(time.monotonic()-start, 3)}
    print(json.dumps(result), flush=True)
    return result

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(run, commands))
(out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
raise SystemExit(1 if any(r['rc'] for r in results) else 0)
