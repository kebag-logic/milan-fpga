#!/usr/bin/env python3
"""Run the scoped documentation and stored-record gates with individual receipts."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
    tests = [
        ('docs', 'scripts/docs_check.py'),
        ('em-dash', 'scripts/check_em_dash.py --base 09c7231eca343607c97c0d66abebb2553688712c'),
        ('toc', 'scripts/gen_toc.py --check'),
        ('anchors', 'scripts/gen_toc.py --verify-anchors'),
        ('doc-paths', 'scripts/check_doc_paths.py'),
        ('doc-style', 'scripts/check_doc_style.py'),
        ('feature-status', 'scripts/check_feature_status.py'),
        ('solution-docs', 'scripts/check_solution_docs.py'),
        ('submodule-docs', 'scripts/check_submodule_docs.py'),
        ('gptp-docs', 'scripts/check_gptp_docs.py --with-submodule'),
        ('archive', 'scripts/check_archive.py'),
        ('resource-baseline', 'syn/ooc/pp_resource_gate.py check-baseline'),
    ]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(packet / 'scratch'))
    results = []
    for name, tail in tests:
        command = [sys.executable, *tail.split()]
        with (packet / (name + '.log')).open('w') as log:
            log.write('COMMAND python3 ' + tail + '\n')
            log.flush()
            result = subprocess.run(command, cwd=args.source, env=env, stdout=log, stderr=subprocess.STDOUT, check=False)
        (packet / (name + '.rc')).write_text(str(result.returncode) + '\n')
        results.append({'gate': name, 'command': 'python3 ' + tail, 'rc': result.returncode})
        print(f'{name}: rc={result.returncode}', flush=True)
    (packet / 'docs-results.json').write_text(json.dumps(results, indent=2) + '\n')
    return int(any(x['rc'] for x in results))

if __name__ == '__main__':
    raise SystemExit(main())
