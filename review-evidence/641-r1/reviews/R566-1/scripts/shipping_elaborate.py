#!/usr/bin/env python3
"""Reviewer probe: every run.sh top, fast elaboration, a chosen sv2v, head flow.

Stages a copy of TREE/syn/yosys/run.sh whose sv2v call names the given binary
and which keeps each top's enforced lowered input, runs `--mode elaborate
--top T --no-structural` for every listed top (--jobs in parallel), and
reports per top: rc, PASS/FAIL row, and how many converted guards the
enforcement restored (`$error("Error [elaboration]` / `$error("Fatal [elaboration]`).

usage: shipping_elaborate.py TREE WORK SV2V LABEL [--jobs N]
"""
from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def main() -> int:
    tree, work, sv2v, label = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], sys.argv[4]
    jobs = int(sys.argv[6]) if len(sys.argv) > 6 and sys.argv[5] == '--jobs' else 4
    out = work / label
    dump = out / 'enforced'
    dump.mkdir(parents=True, exist_ok=True)
    text = (tree / 'syn/yosys/run.sh').read_text()
    reps = {
        'R="$(cd "$(dirname "$0")/../.." && pwd)"': 'R=' + shlex.quote(str(tree)),
        '. "$(dirname "$0")/malloc.sh"': '. ' + shlex.quote(str(tree / 'syn/yosys/malloc.sh')),
        'sv2v --top="$top" $inc $srcs': shlex.quote(sv2v) + ' --top="$top" $inc $srcs',
        '    # Written with a placeholder for this run\'s scratch directory FIRST and':
            '    cp "$TMP/$top.v" ' + shlex.quote(str(dump)) + '/"$top.v"\n'
            '    # Written with a placeholder for this run\'s scratch directory FIRST and',
    }
    for old, new in reps.items():
        if text.count(old) != 1:
            raise SystemExit(f'staging anchor not unique: {old!r}')
        text = text.replace(old, new)
    script = out / 'run.sh'
    script.write_text(text)
    tops = subprocess.run(['bash', str(tree / 'syn/yosys/run.sh'), '--list'], cwd=tree, check=True,
                          capture_output=True, text=True).stdout.split()

    def one(top: str) -> dict:
        env = dict(os.environ, TMPDIR=str(work))
        run = subprocess.run(['bash', str(script), '--mode', 'elaborate', '--top', top, '--no-structural'],
                             cwd=tree, env=env, capture_output=True, text=True)
        (out / f'{top}.log').write_text(run.stdout + run.stderr)
        row = re.search(r'\[(PASS|FAIL)\][^\n]*', run.stdout)
        enforced = dump / f'{top}.v'
        body = enforced.read_text() if enforced.is_file() else ''
        return dict(top=top, rc=run.returncode, row=row.group(0) if row else '',
                    restored_error=len(re.findall(r'\$error\(\s*"Error \[elaboration\]', body)),
                    restored_fatal=len(re.findall(r'\$error\(\s*"Fatal \[elaboration\]', body)),
                    leftover_display=len(re.findall(r'\$display\(\s*"(?:Error|Fatal) \[elaboration\]', body)))

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        rows = list(pool.map(one, tops))
    for row in rows:
        print(json.dumps(row), flush=True)
    (out / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')
    bad = [r['top'] for r in rows if r['rc'] != 0]
    print(json.dumps(dict(label=label, tops=len(rows), failed=bad,
                          tops_with_restored_guards=sum(1 for r in rows if r['restored_error'] + r['restored_fatal']),
                          restored_total=sum(r['restored_error'] + r['restored_fatal'] for r in rows))))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
