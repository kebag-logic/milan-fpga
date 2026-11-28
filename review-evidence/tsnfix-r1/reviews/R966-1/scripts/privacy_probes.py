#!/usr/bin/env python3
"""Privacy gate probes, each on a disposable local clone of the reviewed repository.

usage: privacy_probes.py <clone> <head-sha> <base-sha> <scratch-dir>

A. The head's gate and self-test at the head.
B. The base's own gate at the base: the defect being repaired.
C. The head's gate file run over the base's history only (main as it stands today).
D. New commits on top of the head through the real gate (not the self-test table):
   two-paragraph messages under each permitted identity pair must be refused;
   a one-line commit under the holder pair must pass.
E. Planted defects in a copy of the gate: which self-test controls refuse each,
   and what the real gate over the real history says.
"""
import os, re, shutil, subprocess, sys
from pathlib import Path

clone, head, base, scratch = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3], Path(sys.argv[4]).resolve()
HOLDER = ('hackerman-kl', 'hackerman-kl@kebag-logic.com')
WEB = (('hackerman-kl', '161579364+Mister-M-alt@users.noreply.github.com'), ('GitHub', 'noreply@github.com'))
failures = []


def run(argv, cwd, env=None):
    r = subprocess.run(argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return r.returncode, r.stdout.strip()


def fresh(name, rev):
    d = scratch / name
    if d.exists():
        shutil.rmtree(d)
    subprocess.run(['git', 'clone', '-q', '--no-hardlinks', str(clone), str(d)], check=True)
    subprocess.run(['git', '-c', 'advice.detachedHead=false', 'checkout', '-q', rev], cwd=d, check=True)
    return d


def gate(d, *args, script=None):
    return run([sys.executable, str(script or d / 'scripts/check_privacy.py'), *args], d)


def expect(label, ok, detail):
    print(f"{'ok  ' if ok else 'FAIL'} {label}\n       " + detail.replace('\n', '\n       '))
    if not ok:
        failures.append(label)


def commit(d, author, committer, message):
    env = dict(os.environ, GIT_AUTHOR_NAME=author[0], GIT_AUTHOR_EMAIL=author[1],
               GIT_COMMITTER_NAME=committer[0], GIT_COMMITTER_EMAIL=committer[1])
    subprocess.run(['git', 'commit', '-q', '--allow-empty', '-m', message], cwd=d, env=env, check=True)
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=d, text=True).strip()


print('== A. head gate at head', head)
d = fresh('priv-head', head)
rc, out = gate(d, '--selftest'); expect('A1 self-test passes at head', rc == 0 and '17 commit controls pass' in out, f'rc {rc}: {out}')
rc, out = gate(d); expect('A2 gate passes over the head history', rc == 0 and out.endswith('pass'), f'rc {rc}: {out}')
n = subprocess.check_output(['git', 'rev-list', '--count', 'HEAD'], cwd=d, text=True).strip()
print('       commits reachable from head:', n)

print('== B. base gate at base', base)
b = fresh('priv-base', base)
rc, out = gate(b, '--selftest'); expect('B1 base self-test (before the change)', rc == 0, f'rc {rc}: {out}')
rc, out = gate(b)
expect('B2 base gate fails on its own merge commit, and on nothing else',
       rc == 1 and [l for l in out.splitlines() if not l.startswith('privacy:')] == [base + ': commit message must be one line'], f'rc {rc}: {out}')

print('== C. head gate file over the base history (main today)')
script = d / 'scripts/check_privacy.py'
target = b / 'scripts/check_privacy.py'
saved = target.read_bytes()
target.write_bytes(script.read_bytes())          # the gate reads ROOT from its own location
rc, out = gate(b); expect('C1 head gate passes on main\'s whole history', rc == 0 and out.endswith('pass'), f'rc {rc}: {out}')
target.write_bytes(saved)

print('== D. new commits through the real gate, on top of head')
cases = [
    ('D1 holder pair, one-line message', HOLDER, HOLDER, 'Subject', 0, None),
    ('D2 holder pair, two paragraphs', HOLDER, HOLDER, 'Subject\n\nBody', 1, 'commit message must be one line'),
    ('D3 GitHub pair, two paragraphs (a merge recorded like #41)', WEB[0], WEB[1], 'Merge PR #99: subject\n\nReviews: body', 1, 'commit message must be one line'),
    ('D4 GitHub pair, one line', WEB[0], WEB[1], 'Subject (#99)', 0, None),
    ('D5 foreign identity, one line', ('someone', 'a@b.c'), ('someone', 'a@b.c'), 'Subject', 1, 'unexpected identity'),
    ('D6 holder pair, subject and a trailer line', HOLDER, HOLDER, 'Subject\n\nSigned-off-by: x <x@y.z>', 1, 'commit message must be one line'),
]
for label, author, committer, message, want, needle in cases:
    w = fresh('priv-new', head)
    sha = commit(w, author, committer, message)
    rc, out = gate(w)
    lines = [l for l in out.splitlines() if not l.startswith('privacy:')]
    ok = rc == want and (needle is None or lines == [sha + ': ' + needle])
    expect(label, ok, f'rc {rc}: ' + ' / '.join(l.replace(sha, '<new commit>') for l in (lines or out.splitlines()[-1:])))

print('== E. planted defects in a copy of the head gate')
source = script.read_text()
plants = [
    ('E1 one-line rule removed',
     'and len([line for line in lines[2:] if line.strip()]) != 1:', 'and False:', True),
    ('E2 exemption widened to every commit under the GitHub pair',
     'commit not in TWO_LINE_MERGES and', 'commit not in TWO_LINE_MERGES and lines[:2] != WEB_FLOW and', True),
    ('E3 exemption widened to every message that starts with Merge',
     'commit not in TWO_LINE_MERGES and', 'commit not in TWO_LINE_MERGES and not lines[2].startswith("Merge") and', True),
    ('E4 exemption matched on a 39-digit prefix',
     'commit not in TWO_LINE_MERGES and', 'not any(commit[:39] == m[:39] for m in TWO_LINE_MERGES) and', True),
    ('E5 exempt merges skip the identity check too',
     'if commit != OWNER_SQUASH and not identity_ok(lines):', 'if commit != OWNER_SQUASH and commit not in TWO_LINE_MERGES and not identity_ok(lines):', True),
    ('E6 the #41 merge dropped from the exemptions (self-test has nothing to say; the gate over history must fail)',
     ', "5a07d9b7d87298f04b15aa28f0304ec88b0aef81"}', '}', False),
    ('E7 exemption allows two non-blank lines on every commit',
     'len([line for line in lines[2:] if line.strip()]) != 1:', 'len([line for line in lines[2:] if line.strip()]) not in (1, 2):', True),
    ('E8 the self-test loop reads only the first exempt merge (the earlier next(iter()) shape)',
     'for merge in sorted(TWO_LINE_MERGES):', 'for merge in sorted(TWO_LINE_MERGES)[:1]:', None),
]
for label, old, new, selftest_must_fail in plants:
    if source.count(old) != 1:
        expect(label, False, f'anchor occurs {source.count(old)} times'); continue
    w = fresh('priv-plant', head)
    (w / 'scripts/check_privacy.py').write_text(source.replace(old, new))
    rc_s, out_s = gate(w, '--selftest')
    rc_g, out_g = gate(w)
    last = [l for l in out_g.splitlines() if not l.startswith('privacy: exact')]
    detail = f'self-test rc {rc_s}: {out_s}\ngate over history rc {rc_g}: ' + ' / '.join(l.replace(head, '<head>') for l in last[-2:])
    if selftest_must_fail is True:
        expect(label + ' -> self-test refuses', rc_s == 1 and 'fail' in out_s, detail)
    elif selftest_must_fail is False:
        expect(label + ' -> gate over history refuses', rc_s == 0 and rc_g == 1 and base + ': commit message must be one line' in out_g, detail)
    else:
        print('note ' + label + '\n       ' + detail.replace('\n', '\n       '))
for name in ('priv-head', 'priv-base', 'priv-new', 'priv-plant'):
    shutil.rmtree(scratch / name, ignore_errors=True)
print('RESULT', 'FAIL ' + '; '.join(failures) if failures else 'all expectations met')
raise SystemExit(bool(failures))
