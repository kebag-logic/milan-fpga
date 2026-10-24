"""Collect a four-shard sweep's receipts: per shard the runner's results.json and summary, a manifest (size, sha256) of
every suite log, the shard clone's head, tree and submodule pins; then the union of suites, required to be the full
list `scripts/run_all_suites.sh --list` prints at that head, each exactly once and PASS.

usage: python3 -I sweep_receipts.py <sweep-out> <dest> <expected-head> <lane-clone-prefix>
Host paths are replaced by placeholders (<tmp>, <scratch>, <tools>, <lanes>, <home>). Exit 0 only if every shard's
runner exit code is 0, every suite passed, none timed out, and the union is complete.
"""
from pathlib import Path
import hashlib, json, re, subprocess, sys

out, dest, head, prefix = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
SUBS = [('$VALIDATION_STORAGE/773-a664', '<tmp>'), ('$VALIDATION_STORAGE/scratch/773-a664', '<scratch>'),
        ('$VALIDATION_TOOLS', '<tools>'), ('$LANES', '<lanes>'), ('$WORKSPACE_HOME', '<home>')]


def red(text):
    for a, b in SUBS:
        text = text.replace(a, b)
    return text


def git(clone, *a):
    return subprocess.run(['git', '-C', str(clone), *a], check=True, capture_output=True, text=True).stdout.strip()


dest.mkdir(parents=True, exist_ok=True)
fail, suites, summary = 0, {}, []
for shard in sorted(out.glob('shard-*')):
    k = shard.name.split('-')[1]
    d = dest / shard.name
    d.mkdir(exist_ok=True)
    res = json.loads((shard / 'results.json').read_text()) if (shard / 'results.json').exists() else None
    if res is None:
        # run-recorded-gates writes its results beside the spec
        cands = sorted(shard.glob('**/results.json'))
        res = json.loads(cands[0].read_text()) if cands else {}
    (d / 'results.json').write_text(red(json.dumps(res, indent=2)) + '\n')
    rcs = [r.get('exit_code') for r in res.get('results', [])]
    log = (shard / 'spec' / '01.log').read_text(errors='replace')
    tail = log[log.rfind('shard: '):] if 'shard: ' in log else log[-3000:]
    (d / 'runner.txt').write_text(red(tail))
    clone = Path(f'{prefix}{k}')
    ident = [f'clone head {git(clone, "rev-parse", "HEAD")}', f'clone tree {git(clone, "rev-parse", "HEAD^{tree}")}',
             f'tracked changes: {len(git(clone, "status", "--porcelain", "--untracked-files=no").splitlines())}',
             'submodules:', git(clone, 'submodule', 'status')]
    (d / 'clone_identity.txt').write_text(red('\n'.join(ident)) + '\n')
    lines = []
    for f in sorted((shard / 'logs').rglob('*')):
        if f.is_file():
            b = f.read_bytes()
            lines.append(f'{len(b)} {hashlib.sha256(b).hexdigest()} ./{f.relative_to(shard / "logs")}')
    (d / 'suite_logs.manifest.txt').write_text('\n'.join(lines) + '\n')
    for m in re.finditer(r'^(PASS|FAIL|TIMEOUT|TIMED OUT)\s+(\S+)$', tail, re.M):
        suites.setdefault(m.group(2), []).append((k, m.group(1)))
    tot = re.search(r'suites: (\d+)\s+passed: (\d+)\s+failed: (\d+)\s+timed out: (\d+)', tail)
    chk = re.search(r'checks: (\d+)\s+in-suite failures: (\d+)', tail)
    ok = rcs == [0] and tot and tot.group(3) == '0' and tot.group(4) == '0' and git(clone, 'rev-parse', 'HEAD') == head
    fail += not ok
    summary.append(f'shard {k}: runner rc {rcs}, {tot.group(0) if tot else "no total"}, '
                   f'{chk.group(0) if chk else "no checks line"}, seconds {[r.get("seconds") for r in res.get("results", [])]}'
                   f' -> {"PASS" if ok else "FAIL"}')
lst = subprocess.run(['bash', 'scripts/run_all_suites.sh', '--list'], cwd=f'{prefix}0', capture_output=True, text=True)
expected = [s for s in lst.stdout.split() if s] if lst.returncode == 0 else []
missing = sorted(set(expected) - set(suites))
dup = sorted(s for s, v in suites.items() if len(v) != 1)
bad = sorted(s for s, v in suites.items() if any(r != 'PASS' for _, r in v))
fail += bool(missing or dup or bad or not expected)
summary += [f'suites run: {len(suites)}; expected (run_all_suites.sh --list, rc {lst.returncode}): {len(expected)}',
            f'missing: {missing}', f'run more than once: {dup}', f'not PASS: {bad}',
            f'{"PASS" if not fail else "FAIL"}: head {head}']
(dest / 'SUMMARY.txt').write_text('\n'.join(summary) + '\n')
print('\n'.join(summary))
sys.exit(1 if fail else 0)
