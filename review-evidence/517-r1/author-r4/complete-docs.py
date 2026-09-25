from pathlib import Path
import json
import re

out = Path(__file__).resolve().parent
head = 'f36b40ddb5bf7fa5b12bba47d136e0b9d429403c'
base = '5c78ce2e9d831e588e759b696ed549804327e4d8'
aggregate = json.loads((out/'sweep-aggregate.json').read_text())
integrity = json.loads((out/'final-integrity.json').read_text())
rows = [json.loads(line) for line in (out/'gates.jsonl').read_text().splitlines()]
latest = {row['name']:row for row in rows}
assert aggregate['exit_code']==0 and aggregate['suites']==55 and aggregate['failures']==0
assert integrity['parent']['head']==head
assert all(latest[f'sweep-{i}']['exit_code']==0 for i in range(5))
assert all(row['exit_code']==0 for row in rows if row['head']==head)
checks = aggregate['checks']
chunk_table = '| Chunk | Suites | Checks | Exit | Seconds |\n| --- | --- | --- | --- | --- |\n'
for i in range(5):
    owned = [row for row in aggregate['ownership'].values() if row['chunk']==f'{i}/5']
    gate = latest[f'sweep-{i}']
    chunk_table += f"| {i}/5 | {len(owned)} | {sum(row['checks'] for row in owned)} | {gate['exit_code']} | {gate['seconds']:.3f} |\n"

path = out/'HANDOFF.md'
text = path.read_text()
status = (f'Status: assigned local rebase round complete at `{head}`. All requested final-head commands exit 0, including both builder modes, pool/cancellation controls, four complete-suite measurements and all five default sweep chunks. '
          f'The combined sweep covers all 55 selected suites exactly once: {checks} checks, zero failures, four declared field-campaign/freshness skips. Independent review and publication remain open.')
text = re.sub(r'^Status:.*$',status,text,count=1,flags=re.M)
start = text.index('## Final state\n')
end = text.index('## Measurement interpretation\n',start)
final = f'''## Final state

Local candidate: `{head}`, based on `{base}`. The parent worktree and index match the committed tree; all required submodule worktrees and indexes match their exact pinned commits. `final-integrity.json` records the file counts and pins. Final whitespace checks cover both the working tree and the complete base-to-head diff. Commit subjects are one line, with no bodies or trailers.

The source is local and unpublished by this round. R245 F1 remains MAJOR under all five lenses pending independent re-review; its correction is retained and the author does not clear the finding. R246 external review, reviewer-owned lens coverage, trusted local replication, hosted gates/timing, candidate validation, authorized merge and post-merge containment remain open. The authorized final issue comment is in `REVIEW-READY.md`; this is author evidence, not a review verdict.

`PR-BODY.md` retains the full current PR body structure and Closes line, adds the rebase and measured results, and is a local replacement for the manager. No push, PR edit, merge, additional checkout, hardware action or donor edit was performed.

'''
text = text[:start]+final+text[end:]
text = text.replace('All four full-suite measurements and their equivalence check pass; the five-chunk default sweep is active.', 'All four full-suite measurements, their equivalence check and every default sweep chunk pass.')
text += f'''\n## Combined sweep result

`sweep-aggregate.json` checks exact ownership against `sweep-inventory.json`: 55 default suites, no duplicate, missing or unexpected suite logs. The combined tally is {checks} checks with zero in-suite failures and four declared skips. `sweep-accounting.log` contains the full suite-by-suite table and skip reasons. Every chunk exits 0; no suite timed out.

{chunk_table}
Commands in the gate table use `$EVIDENCE` for this handoff directory. `run-gate.py` pins the validation environment and affinity and records each subprocess exit without a pipeline. The benchmark and builder helper files retain their exact invocation setup; `tool-identity.json`, `environment.json`, `source-scope.json` and `policy-union.json` provide the corresponding identities and scope checks. Preliminary failures remain in the table with their actual exits and are resolved by the later final-head runs.
'''
path.write_text(re.sub(r'\n{3,}','\n\n',text))

path = out/'PR-BODY.md'
text = path.read_text()
text = text.replace('the complete default sweep is running.',f'the complete default sweep also passes: all 55 suites, {checks} checks, zero failures and four declared skips.')
old = 'The\nmanager owns full native banks, trusted local replication, hosted timing/gates and candidate checks.'
text = text.replace(old,'The author also ran every requested static gate, both builder modes and the complete five-chunk default sweep. The manager retains trusted local replication, hosted timing/gates and candidate checks.')
text = text.replace('## DoD',f'''The pool unit controls pass 17/17, blocked-output cancellation controls 28/28, and phase controls 24/24. Both builder modes and every requested static/documentation/HDL/idiom gate exit 0. The policy self-test passes 700 arms; CI event checks pass 1647 contract items and 2188 self-test arms; BDD passes 344 scenarios and 1739 steps. Existing xvlog and RTL-lint ratchets are unchanged. The full default sweep has no suite failure or timeout:

{chunk_table}
## DoD''')
assert text.startswith('[A321]\n') and 'Closes #517' in text and '/home/' not in text
assert 'will be recorded after validation' not in text and 'sweep is running' not in text
path.write_text(text)

comment = f'''[A321] REVIEW READY

Commit: `{head}` (local; not pushed).
Base: `{base}`.
Scope: [assignment items 1-3](https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5835674224).

Changed: rebased all three original commits with their one-line subjects; retained the full dev/PR policy-mask and self-test union; reconciled the Makefile, inventory documentation and cancellation fixtures with all eleven ordinary legs, including CRF licence, #508 GSI and #443 CSR coverage. The five shared-header writers remain exclusive and ordered. Directory overrides, prerequisites, focused targets and post-pool campaigns retain their original phases. The cancellation runner is byte-identical to the validated starting correction. Workflows, budgets, HDL, firmware, campaign drivers and required submodule pins are unchanged from the requested base.

Validation: every requested final-head command exits 0. Pool unit controls 17/17; blocked-output cancellation controls 28/28; phase controls 24/24. Both builder modes pass. The policy self-test passes 700 arms, BDD 344 scenarios/1739 steps, CI event check 1647 contract items and CI event self-test 2188 arms. Both CI documentation modes, all requested style/source/HDL/idiom/contract/traceability gates and final whitespace checks pass; existing ratchets are unchanged.

Complete default milan_dp measurements on CPUs 16-23, eight build jobs, Verilator 5.050:

| Build state | SIM_JOBS=1 | SIM_JOBS=2 | Reduction |
| --- | --- | --- | --- |
| Cold | 1421.094 s | 1370.953 s | 50.140 s (3.53%) |
| Warm | 1230.269 s | 1170.273 s | 59.996 s (4.88%) |

Each run reports 10074 checks and zero failures. All eleven leg logs, ordered replay, executable hashes and recorded inputs match; tracked headers are unchanged. Observed concurrency is at most two ordinary children and one exclusive writer. The unchanged budget is 3600 s; pooled cold/warm margins are 2229.047/2429.727 s. These are local shared-host measurements, one pair per build state.

Full default sweep: `scripts/run_all_suites.sh <chunk-output> --shard I/5`, I=0 through 4, with every preflight retained. Exact union: all 55 selected suites, {checks} checks, zero failures, no timeouts, four declared skips.

{chunk_table}
Declared limits: `tsn-gen` is absent, so its two field campaigns and two freshness arms ran no checks. The builder's utilization-report calibration arm lacks its hardware report; the no-compiler mode also stands down compiler instruments, which are graded by the SDK mode. No hardware evidence is claimed.

Acceptance evidence: assignment items 1-3 are met locally. Parent and required submodule bytes, indexes and pins match the committed candidate. HANDOFF.md records every conflict hunk with file/line resolutions, the before/after leg inventory, all commands/exits, every sweep chunk and the measured comparisons. PR-BODY.md contains the full updated local PR body with the Closes line retained, in the assigned output directory.

Open review state: R245 F1 remains MAJOR under all five lenses until independent re-review; R246 external review, reviewer-owned lens coverage, publication, trusted local replication, hosted gates/timing and candidate validation remain open. This is author evidence, not approval. No push, PR edit or merge was performed.
'''
(out/'REVIEW-READY.md').write_text(comment)
print(f'Completed handoff, PR body and issue-comment text for {head}; {checks} combined sweep checks.')
