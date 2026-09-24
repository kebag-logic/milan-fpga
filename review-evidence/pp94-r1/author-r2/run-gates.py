#!/usr/bin/env python3
"""Run the repository's CI gates in the foreground, retaining every return code."""
import json
import os
from pathlib import Path
import subprocess
import time

PACKET = Path(__file__).resolve().parent
ROOT = Path('$LANES/pp94-desc-mem-guard')
ENV = dict(os.environ)
ENV['PATH'] = '$VALIDATION_STORAGE/pp94-manager-cc077a6f/pinned-tool-bin:' + ENV['PATH']
GATES = [
    ('version', ['verilator', '--version']),
    ('links', ['python3', 'scripts/check-links.py']),
    ('matrix', ['python3', 'scripts/check-matrix.py']),
    ('wavedrom', ['python3', 'scripts/render-wavedrom.py', '--check']),
    ('stale', ['make', 'stale']),
    ('lint', ['./scripts/lint_hdl.sh']),
    ('suites', ['./scripts/run_suites.sh']),
    ('gen-matrix', ['python3', 'scripts/gen_matrix.py', '--check']),
    ('fetch-pr13', ['git', 'fetch', '--no-tags', 'origin', 'refs/pull/13/head']),
    ('nvm-figures', ['make', '-C', 'tb/nvm_port', 'figures']),
    ('portability', ['./syn/yosys/run.sh']),
    ('make-check', ['make', 'check']),
]


def main() -> int:
    """Execute each gate without a pipeline and save its direct verdict."""
    results = []
    for name, command in GATES:
        print(f'START {name}: {" ".join(command)}', flush=True)
        start = time.monotonic()
        with (PACKET / f'ci-{name}.log').open('w') as stream:
            try:
                rc = subprocess.run(command, cwd=ROOT, env=ENV, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=7200).returncode
            except subprocess.TimeoutExpired:
                rc = 124
        result = {'gate': name, 'command': command, 'rc': rc,
                  'seconds': round(time.monotonic() - start, 2)}
        results.append(result)
        (PACKET / 'ci-results.json').write_text(json.dumps(results, indent=2) + '\n')
        print(f'END {name}: rc={rc}; seconds={result["seconds"]}', flush=True)
    return int(any(result['rc'] for result in results))


if __name__ == '__main__':
    raise SystemExit(main())
