"""Assemble the author handoff only from completed receipts."""
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
SCRATCH = Path((OUT / 'scratch-path.txt').read_text().strip())
REPO = Path('$LANES/514-containment-retention')
OLD = '20b7bdaa307eba722ec6cc89d2683ba1636a0cb6'
BASE = '3d2f3e3131c9db5898e1db9dd3e2a35149843109'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO, text=True).strip()

head = git('rev-parse', 'HEAD')
assert head == 'b0347a4fd668f8d40bdf40a142ac0ea70167acd1'
assert git('rev-parse', 'HEAD^') == OLD
assert git('branch', '--show-current') == '514-containment-retention'
assert not git('status', '--porcelain=v1', '--untracked-files=all')
assert git('diff', '--name-only', OLD, 'HEAD') == 'scripts/merge_containment_selftest_linear.py'
assert len(git('show', '-s', '--format=%B', 'HEAD').splitlines()) == 1

after_dir = OUT / 'after/R293-1'
for path in (SCRATCH / 'r293-after').glob('*.log'):
    shutil.copy2(path, after_dir / path.name)
shutil.copy2(OUT / 'r293-after.json', after_dir / 'mutation-probe.json')

before292 = {}
for match in re.finditer(r'^(M\S+) (KILLED|SURVIVED) exit=(\d+) fails=(\d+)',
                         (OUT / 'before/R292-1/mutants.log').read_text(), re.M):
    name, status, rc, count = match.groups()
    before292[name] = dict(status=status, rc=int(rc), failing_count=int(count))
after292 = json.loads((OUT / 'after/R292-1/mutants.json').read_text())
before293 = {row['mutant']: row for row in json.loads((OUT / 'before/R293-1/mutation-probe.json').read_text())}
after293 = json.loads((OUT / 'r293-after.json').read_text())

def supplemental(directory):
    rows = []
    text = (directory / 'targeted-mutants.log').read_text()
    for match in re.finditer(r'^== ([^:]+): rc=(\d+) PASS=(True|False) FAIL-lines=(\d+)', text, re.M):
        name, rc, passed, count = match.groups()
        rows.append(dict(mutant=name, rc=int(rc), failing_count=int(count),
                         status='SURVIVED' if passed == 'True' and int(rc) == 0 else 'KILLED'))
    assert len(rows) == 2
    text = (directory / 'probe-stranded-mutant.log').read_text()
    match = re.search(r'mutant self-test: rc=(\d+) PASS=(True|False) FAIL-lines=(\d+)', text)
    assert match
    rc, passed, count = match.groups()
    rows.append(dict(mutant='retained-beside-stranded', rc=int(rc), failing_count=int(count),
                     status='SURVIVED' if passed == 'True' and int(rc) == 0 else 'KILLED'))
    return rows

before293.update({row['mutant']: row for row in supplemental(OUT / 'before/R293-1')})
after293.extend(supplemental(after_dir))
assert len(before292) == len(after292) == 15
assert len(before293) == len(after293)
for before, after in ((before292, after292), (before293, after293)):
    for row in after:
        old = before[row['mutant']]
        assert row['status'] in ('KILLED', 'SURVIVED', 'PASS')
        if old['status'] == 'KILLED':
            assert row['status'] == 'KILLED', row['mutant']
        if row['status'] == 'KILLED':
            assert row['rc'] == 1 and row['failing_count'] > 0, row['mutant']
required292 = ('M01-', 'M09-', 'M10-', 'M12-')
assert all(row['status'] == 'KILLED' for row in after292 if row['mutant'].startswith(required292))
required293 = {'ancestry-diagnostic-dropped', 'H-error-ignored', 'measurement-except-certifies',
               'retained-diagnostic-blank', 'retained-beside-stranded'}
assert all(row['status'] == 'KILLED' for row in after293 if row['mutant'] in required293)
assert after293[0]['status'] == 'PASS' and after293[0]['rc'] == 0

gates = json.loads((OUT / 'gates.json').read_text())
assert all(row['rc'] == 0 for row in gates)
cases = json.loads((OUT / 'case-comparison.json').read_text())
assert all(row['unchanged_in_order'] for row in cases)
stats = dict(head=head, before=OLD,
             r292_before_killed=sum(r['status'] == 'KILLED' for r in before292.values()),
             r292_after_killed=sum(r['status'] == 'KILLED' for r in after292), r292_total=len(after292),
             r293_before_killed=sum(r['status'] == 'KILLED' for r in before293.values()),
             r293_after_killed=sum(r['status'] == 'KILLED' for r in after293),
             r293_total=sum(r['mutant'] != 'control-unmutated' for r in after293),
             every_previous_kill_preserved=True)
(OUT / 'mutation-comparison.json').write_text(json.dumps(stats, indent=2) + '\n')

def table(before, after):
    lines = ['| Mutant | Before | After | After rc | Failing cases |',
             '|---|---|---|---:|---:|']
    for row in after:
        lines.append(f"| `{row['mutant']}` | {before[row['mutant']]['status']} | {row['status']} | {row['rc']} | {row['failing_count']} |")
    return '\n'.join(lines)

gate_table = ['| Gate command | rc | Receipt |', '|---|---:|---|']
for row in gates:
    prefix = ' '.join(f'{key}={value}' for key, value in row['env'].items())
    command = (prefix + ' ' + row['command']).strip()
    gate_table.append(f"| `{command}` | {row['rc']} | [{row['gate']}]({row['log']}) |")

handoff = f'''[A251] Round 2 author handoff: PR #552 / Issue #514

## Head and scope

- Branch: `514-containment-retention`.
- Starting head: `{OLD}`.
- Review-ready head: `{head}`; tree `{git('rev-parse', 'HEAD^{tree}')}`.
- Local commit: `test(containment): cover unmeasurable retention and scoped claims`.
- One-line subject, no body or trailers. One file changed, 83 insertions.
- Only `scripts/merge_containment_selftest_linear.py` changed. Production verdicts, parsing, diagnostic wording, documentation, and every existing test expectation remain unchanged.
- [Assignment](https://github.com/kebag-logic/milan-fpga/issues/514#issuecomment-5812011094), [R292-1](https://github.com/kebag-logic/milan-fpga/pull/552#issuecomment-5811949459), [R293-1](https://github.com/kebag-logic/milan-fpga/pull/552#issuecomment-5811996262).

## Assigned outcomes

| Finding | Added executable evidence | Outcome |
|---|---|---|
| F1: arm-level unmeasurable result | `linear-empty-delta`: distinct exact replays of source change and revert, with empty net source delta | Optional `UNKNOWN/1`; explicit arm-level diagnostic; default landing still `contained/0` |
| F1: H measurement failure | `linear-H-measurement-failure`: real exact-path landing, then injected failure of H's Git source enumeration | Optional `UNKNOWN/1`; failing Git read observed once; default path proof does not call it |
| F2: ancestry claim | `linear-ancestry-default-claim` and `linear-ancestry-optional-claim` | The `contained` line itself names historical inclusion and disclaims current retention |
| F2: no retention on failed landing | STRANDED source and nonexistent UNKNOWN target, both with the option | Failed landing and exit 1 preserved; no `retained` line or optional retention result |
| R293-F2: positive retained detail | Six positive retained examples | The `retained` line names raw current retention at the target and historical replay |

Optional parsing suggestion R292-S1 / R293-S2 was not taken. Other documentation suggestions remain outside the assigned tests-only change. These are author evidence claims, not review verdicts or a reviewer-owned coverage ledger.

## Existing self-test preservation

The committed head passes **799/799** full self-test cases. All **778** case lines at `{OLD}` are preserved verbatim and in order, verified independently against both archived reviewer logs. The original **678** base case lines are also preserved verbatim and in order. The change adds **21** checks.

The linear entry point passes **121** linear checks plus **12** shared preflight/cleanup checks (133 total). `run_linear.py` selects `linear_retention_cases` through the existing fixture harness. No locale arm reported `NOT RUN`.

Receipts: [full self-test](gates/selftest.log), [linear entry point](gates/linear.log), [case comparison](case-comparison.json), [patch](round2.patch).

## Mutation method and provenance

Before results are the reviewers' published runs at `{OLD}`, copied from these immutable archives:

- R292-1: `185549cf74b00568f5462f57961d1de8ad52dc38`, `review-evidence/514-r1/reviews/R292-1/`.
- R293-1: `c3d6a0e682bff1fe50121528e4d8ef991f10845b`, `review-evidence/514-r1/reviews/R293-1/`.

After results are new runs against script bytes exported from `{head}`. All four copied reviewer scripts were verified byte-identical to their archive blobs; see [script integrity](script-integrity.json).

The R292 runner ordinarily creates a shared clone. To obey the no-other-checkouts instruction, `run_r292_no_checkout.py` imports its unchanged `MUTANTS` table and applies each exact replacement to a disposable scripts copy, then runs the full self-test from the assigned repository. Every mutation site must occur exactly once. No mutant definition or expected outcome was changed. R293's main, targeted, and STRANDED runners ran unchanged with their documented arguments. The unmutated R293 control passes.

All commands ran in foreground processes and were awaited. Recorded gates wrote raw output to files, without shell pipelines. Mutant scripts and disposable copies lived under the single scratch directory recorded in `scratch-path.txt`; its removal is recorded in `cleanup.json` before the review-ready comment.

### R292-1 before/after

{table(before292, after292)}

R292: **{stats['r292_before_killed']} -> {stats['r292_after_killed']} killed, of {stats['r292_total']}**. M01, M09, M10, and M12 now fail genuine new cases. Every previous kill remains killed. The unchanged survivors are M11 (merge-count digit parsing, not an assigned finding) and M13 (summary wording, not a contract in the review).

Receipts: [before](before/R292-1/mutants.log), [after JSON](after/R292-1/mutants.json); full per-mutant logs are beside that JSON.

### R293-1 before/after

{table(before293, after293)}

R293: **{stats['r293_before_killed']} -> {stats['r293_after_killed']} killed, of {stats['r293_total']}**, plus a passing unmutated control. This includes both targeted mutants and the separate STRANDED mutant. Every required equivalent is killed, including the blank retained diagnostic, and every previous kill remains killed. The merge-count digit-guard mutant remains the sole survivor.

Receipts: [before main set](before/R293-1/mutation-probe.json), [after main set](after/R293-1/mutation-probe.json), [targeted](after/R293-1/targeted-mutants.log), [STRANDED](after/R293-1/probe-stranded-mutant.log). Full main-set logs are beside its JSON.

Some existing broad mutants still collide with the self-test's own source-mutation guard strings and subsequently abort. Each killed mutant first records at least one genuine failing test case. The two targeted mutations preserve those guard strings and still fail the mode/kind examples. No kill is credited solely to an exception.

## Gate table

All gates ran at `{head}` and returned 0. `PYTHONDONTWRITEBYTECODE=1` was set for the gates; disposable bytecode caches were removed after validation. The no-Git docs mode uses the same filesystem discovery path as its CI mode.

{chr(10).join(gate_table)}

The receipt comparison helper initially matched `FAILS` inside a passing case description. Its result-line check was corrected and the comparison alone rerun successfully; no repository test or expectation changed. Individual gate exits were all 0 throughout.

## Reproduction

Run from the assigned lane. Export `HEAD:scripts` and the two immutable reviewer packets into a fresh scratch directory before the mutation commands. `$PACKET` below is this output directory, `$SCRATCH` is that temporary directory, and `$REPO` is the assigned lane.

```sh
python3 -B -u "$PACKET/run_gates.py"
python3 -B -u "$PACKET/run_r292_no_checkout.py" "$SCRATCH/review-evidence/514-r1/reviews/R292-1/scripts/mutants.py" "$SCRATCH/head/scripts" "$SCRATCH/r292-after" "$REPO" "$PACKET/after/R292-1"
python3 -B -u "$SCRATCH/review-evidence/514-r1/reviews/R293-1/mutation_probe.py" "$SCRATCH/head/scripts" "$SCRATCH/r293-after" "$REPO" "$PACKET/r293-after.json" 4
python3 -B -u "$SCRATCH/review-evidence/514-r1/reviews/R293-1/targeted_mutants.py" "$SCRATCH/head/scripts" "$SCRATCH/r293-targeted" "$REPO"
python3 -B -u "$SCRATCH/review-evidence/514-r1/reviews/R293-1/probe_stranded_mutant.py" "$SCRATCH/head/scripts" "$SCRATCH/r293-stranded" "$REPO"
```

## Remaining workflow and limits

The local worktree is clean at the named head. No push, PR edit, merge, other checkout, sub-agent, hardware run, or local workflow replay was performed. The existing checker self-tests create their own disposable Git fixtures as part of the required gate.

`PR-BODY.md` is the complete replacement body for manager publication. Independent re-review, reviewer-owned coverage decisions, publication, hosted evidence, required local workflow replication, current-dev candidate validation, merge authorization, and post-merge containment remain pending. This handoff supplies no review verdict or completion ledger.
'''
(OUT / 'HANDOFF.md').write_text(handoff)

pr_body = f'''[A251] Separate historical linear inclusion from optional current retention

Closes #514

## Status

Round 2 is ready for independent re-review at `{head}`. The round adds tests only. Publication of this local head and the remaining merge workflow are pending.

## Description

An exact linear replay followed by a revert still returns `contained/0`, preserving the decided historical-inclusion policy. Add `--current-retention` to request a separate `retained` or `UNKNOWN` result using #423's unchanged raw-entry and no-op three-way merge criterion. Diagnostics and the containment documentation identify the claim each result makes.

The optional arm requires a nonempty source-only linear range and distinct exact replays. Ancestry-only, squash-only and merge-shaped histories remain unsupported by this arm. Unmeasurable or unproved retention returns `UNKNOWN/1`; declared supersession intent does not supply proof.

## Round 2

Address the Tests findings in [R292-1](https://github.com/kebag-logic/milan-fpga/pull/552#issuecomment-5811949459) and [R293-1](https://github.com/kebag-logic/milan-fpga/pull/552#issuecomment-5811996262):

- Exercise an exact replay with an empty source delta and an H measurement failure. Both require optional `UNKNOWN/1` while preserving the default landing result.
- Assert that the ancestry `contained` line names historical inclusion and disclaims current retention, with and without the option.
- Assert that STRANDED and UNKNOWN landing targets emit no `retained` line or optional retention result.
- Assert that positive `retained` lines identify current raw retention and historical replay.

Only `scripts/merge_containment_selftest_linear.py` changes in this round. Existing expectations, production behavior, diagnostics and parsing remain unchanged. The optional parsing suggestion was not taken. Re-review of the corrected head is required.

## How to reproduce

Run unchanged fixture 30 and `linear-patch-fallback`: both remain `contained/0`. Adding `--current-retention` reports `UNKNOWN/1`, naming `mod.txt` and `linear` respectively. The baseline reproductions are recorded in the linked reviews and their immutable evidence packets.

The new empty-delta fixture replays a change and its revert exactly. Its source endpoint equals its starting tree, so optional current retention must be unmeasurable. The H-failure fixture has exact current paths, allowing default landing to pass before an injected Git enumeration failure reaches the optional arm.

## How to validate

Run `python3 scripts/check_merge_containment.py --selftest` and the `linear_retention_cases` entry point through the existing fixture harness. Run the docs gate in both discovery modes, `check_em_dash` against `{BASE}`, documentation style, TOC, paths, Python idiom and `git diff --check`.

Reapply both reviewers' unchanged mutant sets. M01, M09, M10, M12 and their R293 equivalents must fail, as must every previously killed mutant. The handoff contains the before/after tables, unchanged script hashes, raw gate logs and preservation comparison. Self-test results are evidence for re-review, not approval.

## DoD

- Historical verdicts and all existing test expectations preserved.
- Optional retention proof, claim-naming diagnostics and authoritative wording implemented.
- Assigned Round 2 measurement and diagnostic coverage added; required mutant sensitivity demonstrated.
- Assigned local gates pass. Independent re-review and the remaining hosted, candidate, merge and post-merge workflow are still required.
'''
(OUT / 'PR-BODY.md').write_text(pr_body)

comment = f'''[A251] REVIEW READY
Commit: {head} (local, not pushed)
Changed: tests only in scripts/merge_containment_selftest_linear.py. F1 covers empty-net-delta replay and H measurement failure as UNKNOWN/1. F2 pins ancestry and retained claim text and forbids retained output beside STRANDED/UNKNOWN.
Validation: python3 scripts/check_merge_containment.py --selftest passes 799 cases; all 778 prior case lines remain verbatim and in order. The linear entry point passes 121 linear checks plus 12 shared checks. Both docs discovery modes, check_em_dash --base {BASE}, check_doc_style, gen_toc --check and --verify-anchors, check_doc_paths, check_py_idiom, and git diff --check all exit 0.
Mutation evidence: unchanged R292 set {stats['r292_after_killed']}/{stats['r292_total']} killed (previously {stats['r292_before_killed']}); unchanged R293 sets {stats['r293_after_killed']}/{stats['r293_total']} killed (previously {stats['r293_before_killed']}), with its unmutated control passing. M01/M09/M10/M12 and all R293 equivalents are killed; every previous kill remains killed. The unrelated prior survivors remain documented. R292 definitions ran through a scripts-copy adapter to honor the no-other-checkouts restriction; all four reviewer scripts remained byte-identical to their archives.
Acceptance criteria: assigned Round 2 outcomes met with executable evidence; behavior and every existing expectation unchanged. Optional parsing suggestion not taken. HANDOFF.md and the full PR-BODY.md are prepared in the assigned output directory.
Open risks/questions: independent re-review and the remaining publication/merge workflow are pending. No author review verdict is claimed.
'''
(OUT / 'REVIEW-READY.md').write_text(comment)
print(json.dumps(stats, indent=2))
print('Wrote HANDOFF.md, PR-BODY.md, REVIEW-READY.md')
