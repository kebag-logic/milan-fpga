[R783] POSITIVE - exact head c73be9b93101fde17c5545145b21066f24f7b99b

# R783-4: issue #665 lane S5 / PR #844, round 4, internal cleared-context review

- **Head:** `c73be9b93101fde17c5545145b21066f24f7b99b`, tree `ee578c56e1bec9dc3ce8e3d7f508b8fddc2887e0`. `665-s5-hooks` -> `dev-soft-core`, source base `5b5f4336`.
- **Delta judged:** `3f8caae5..c73be9b9`, two commits (`d7cb56ef`, `c73be9b9`), `hooks_selftest.py` and `README.md` only, against the ruling issuecomment-6694276050.
- **Verdict:** POSITIVE. No BLOCKER, MAJOR, MINOR or RESIDUE is open. All five lenses are clean at this head.
  - R783-3 F1 = R784-3 F-1 is resolved at its cause. Dropping the path term from `run.py:141` now fails `another path`, and the new mutant escapes when that assertion is deleted.
  - All four ruling items are met, and the names, rule table, README rows and PR sentences agree.
  - The author's open points are stated truthfully, and each one I could test reproduced.
  - The group term hides no real defect, so it is not reported as a finding.
- **Also here:** two SUGGESTIONs, neither affecting the verdict.
- **Not closed by this verdict:** "each hook within its bound" stays open on #665 as ruled, and it is not a finding. This is one of the two positive reviews the bar needs. The manager's candidate and hosted evidence are still to come.

## Reconstruction

Read in the assigned order: AGENTS.md; CONTRIBUTING.md and docs/README by section; the #665 body and rulings 6677495623, 6692737899 and 6694276050; takeover 6694330189 and REVIEW READY 6695246318; the PR body; `git diff 3f8caae5..c73be9b9`; `run.py`, `hooks.py` and the self-test; then the round 4 receipts. REQUIREMENTS.md was not re-read: the delta is a test and its README, and no requirement clause moved.

My own pass and probes came first. Verdict and ledger were fixed in `receipts/verdict_before_prior_findings.md` before any prior review was opened, and that verdict is unchanged. The ruling and the manager's brief named the finding in outline; the reviews themselves were read afterwards.

## Focus checks

| Check | Result | Evidence |
|---|---|---|
| Dropping the path term now fails the self-test | **Holds.** rc 1, on the `another path` assertion (`hooks_selftest.py:604`). | `receipts/source_and_deletion_probe.txt` |
| `sup-no-path` is killed | **Holds, in my own spelling.** A weaker form, comparing paths by family prefix so any `acmp.` path matches, is killed by the same assertion. The published `r783_source_probe.txt` and `r784_r3_probes.txt` agree (`sup-no-path`, `sup-any-path`, `sup-table-any-path` killed). | same |
| The new case has the ruled shape | **Holds.** `:601-604`: a row of another path, in the named group, on the same interface, refusals left in place. `beside` is the real probe (`hooks.py:472-473`), and `own` gives the shape of the check's docstring. | `hooks_selftest.py:586-604` |
| A mutant fails on it | **Holds.** `a row of another path supersedes a refusal` fires `:604`. With that assertion deleted, it alone escapes. | `receipts/mutant_firing_probe.txt`, `source_and_deletion_probe.txt` |
| The old case no longer claims what it could not test | **Holds.** It is now `a path the table does not name`, with a row of its own path, so only the table stops it. `the table names a second path` fires `:600`, and alone escapes with that assertion deleted. Table guard dropped and second table entry both fail it. | same |
| Renamed mutants say what they do | **Holds for all three.** `every refusal is superseded` clears every refusal with no row read (`:754-757`) and fires `:597`. `the margin is taken from a timeout of zero` gives `margin -160.0`. `its finding by name is dropped` leaves `LATE H-COUNTERS: counters.held.if0: never served against its bound 20`, so a generic finding stays. | `receipts/mutant_firing_probe.txt` |
| `every refusal` chain | **Holds.** It fires `other interface`, then the unnamed path, then `another path`, and escapes only with all three deleted. | `receipts/source_and_deletion_probe.txt` |
| Names, table, README and PR agree | **Holds.** 96 of 96 README rows match name and check; `mutant_rules.json` has the same 96 keys; `README.md:234-237` as the PR cites; `run.py:141` is the rule; no stale name in the tree, against all three present at `3f8caae5` as a control. | `receipts/mutant_firing_probe.txt`, `mutant_firing_probe_prev_head.txt` |
| Round 3's two paragraphs corrected in place | **Holds.** Both carry a "Corrected by Round 4" statement, and the Status line points to Round 4. | `receipts/pr-body-at-review.md` |
| The one check of the rule table | **Accepted, spot-checked.** 96 by assertion, 0 by exception. 58 wrapping rows and 61 twins counted from the published table. Five twins remade at their source fail as published, and the published `TWIN SURVIVES` control is rc 1. Limits below. | `receipts/twin_spot_check.txt`, `source_and_deletion_probe.txt` |
| Nothing measured moved | **Holds.** The delta is two files. Lane-wide, all 6 changed files are in `tb/verilator/ctrl_service_hooks`. | `receipts/round4-delta.diff`, `lane_scope.txt` |

### The author's open points

| Point | Result | Evidence |
|---|---|---|
| `buckets` fires the wait's length, no mutant fires the group's assertion, its twin does | **True.** The mutant fires `:630`; no mutant fires `:638`; removing the wait from both groups fails with `0 bus cycles between the last registration and the window`. | `receipts/mutant_firing_probe.txt`, `twin_spot_check.txt` |
| Deleting `other interface` alone lets nothing escape | **True.** rc 0. Only `every refusal` fires `:597`, and it falls through. Dropping the term at the source fails that assertion. | `receipts/source_and_deletion_probe.txt` |
| The group term has no assertion of its own | **True.** Dropped at the source: no check fails, `the table names another group` escapes, rc 1. | same |
| 48 `expect` statements fired first by no mutant, down from 49 | **True, recounted independently.** 117 sites, 69 fired, 48 not; 116, 67 and 49 at `3f8caae5`. All four sites of `check_superseded` are fired. | `receipts/mutant_firing_probe.txt`, `mutant_firing_probe_prev_head.txt` |
| "The rule it names" stays a judgement | **Fair.** The published table is what a reviewer disputes. I dispute no row I read. | `rule_table_check.md` in the author's packet |
| Maintainer items unchanged | **True.** The delta touches neither the column's scope nor the one-path or per-descriptor reporting. | `receipts/round4-delta.diff` |

### The group term

It hides no real defect, so it is not reported. At the head the rule is right. Exactly two groups carry the tabled path on each interface, `acmp-disc` and `hooks-disc-aging` (`receipts/group_term_probe.txt`), so the only input the term decides is a measured `acmp-disc` row beside an unmeasured `hooks-disc-aging` probe. At the head that stays a refusal (`receipts/group_scenario_demo.txt`). With the term dropped it would be superseded with a false "measured by hooks-disc-aging", but that edit cannot pass the gate: the self-test exits 1. The hold is indirect, not absent, and the author says so.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

### S1: SUGGESTION (Tests). The rule's `any` has no holder

- **Where:** `hooks_selftest.py:594-595`, the positive case of `check_superseded`; `run.py:141`.
- **Authority/evidence:** AGENTS.md section 6 Tests. `any` turned to `all` at `run.py:141` passes 28 of 28 checks and 96 of 96 mutants, rc 0 (`receipts/source_and_deletion_probe.txt`), because the positive case has one row and `all` equals `any` there.
- **Impact:** none on any figure or verdict. Every real run has many rows, so under that edit nothing would ever be superseded, and the run would fail on a refusal: it fails closed. No published sentence claims this quantifier is held, and no run of Results supersedes anything (`README.md:200`). That is why this is not a MINOR.
- **Required outcome (optional):** give the positive case a row of another path beside its own.
- **Verification:** tried on a copy. The head stays at 28 of 28 and 96 of 96; `all` then fails the check on `superseded`, rc 1 (`receipts/all_fix_feasibility.txt`, `scripts/all_fix_feasibility.py`). The ruling's stop may well leave this out.

### S2: SUGGESTION (Tests). One continuation line is two columns off

- **Where:** `hooks_selftest.py:881`.
- **Authority/evidence:** the rewrapped row is indented 67 columns, and the text after its opening bracket starts at column 65. The sibling at `:876` aligns exactly, at 52. This is formatting, not prose, so it is not RESIDUE, and the published gates pass with it.
- **Impact:** none.
- **Required outcome (optional):** indent `missing=True), MISSING_HELD),` by 65 spaces.
- **Verification:** read the two lines together.

## Prior findings at this head

| Finding | Status | Evidence at this head |
|---|---|---|
| R783-3 F1 = R784-3 F-1, the supersede mutant and the path term | **RESOLVED** | All three outcomes of R783-3 F1 and every part of R784-3's required outcome hold: focus checks above. |
| R783-3 R1, the Grading row | **RESOLVED** | The exact words are in the PR body's Grading row. |
| R784-3 S-3, a case "unmeasured there too" | **Taken** | `:601-604`. |
| R783-3 S3, a name saying what the wrapper does | **Taken, in substance** | `every refusal is superseded`. |
| R783-3 S4, the audit raising on an escape | **Taken** | The published control prints `ESCAPED` for the new mutant, rc 1. |
| R783-3 S1, S2; R784-3 S-1, S-2 | **Retained, optional** | Out of the ruling, as the PR says. |
| R783-2 S1, S2, S3, S5's second half; R784-2 S-1, S-2, S-4 | **Retained, optional** | Unchanged by this delta. |
| All R783-2, R784-2, R783-1 and R784-1 findings | **Resolved at prior heads; nothing they depend on moved** | Recorded by R783-3 and R784-3. `run.py`, `hooks.py`, `hooks_build.py` and `hooks_soc.py` are unchanged in this delta, and it edits only `check_superseded`, the mutant list and two helpers of the self-test. |

## Lens results

```text
[R783] PASS Conformance - ruling 6694276050 items 1 to 4 against hooks_selftest.py:586-604,747-757,813-821, README.md:215,234-237,269, PR body Round 4, receipts/source_and_deletion_probe.txt - each item met; the frozen "each hook within its bound" stays open as ruled, with the PR relating to #665, not closing it
[R783] PASS RTL - receipts/round4-delta.diff, lane_scope.txt, clone_integrity.txt - no hdl, firmware or gateware file in the delta or the lane, six gitlinks unchanged, so the prior RTL result stands on nothing that moved
[R783] PASS Robustness - run.py:139-145, hooks.py:446,472-476, receipts/group_term_probe.txt, group_scenario_demo.txt - rule code unchanged; every refusal shape tried stays a refusal at the head, including another path, another interface, an unnamed path and the two real groups reversed, so the rule fails closed
[R783] PASS Tests - hooks_selftest.py:586-604,747-757,813-821, receipts/selftest_head.txt, source_and_deletion_probe.txt, mutant_firing_probe.txt, twin_spot_check.txt - 28 of 28 and 96 of 96, equal to the published receipt line for line; 11 of 12 source mutants killed, the survivor being S1; each single deletion behaves as the PR states
[R783] PASS Docs - README.md:215,234-237,269, PR body Status and Round 4, receipts/mutant_firing_probe.txt, delta_hygiene.txt - 96 of 96 rows, PR claims and open points true; 32 added lines with no bench label, lane, round, reviewer ID, comment ID or em dash; both commits one line with no trailers; check_doc_style OK
```

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling 6694276050; `hooks_selftest.py:586-604,747-757,813-821`; `README.md:215,234-237,269`; PR body Round 4; REVIEW READY 6695246318 | R783-4 | `c73be9b93101fde17c5545145b21066f24f7b99b` |
| RTL | CLEAN | Delta and lane file lists; blob equality of the four harness files; six gitlinks; `receipts/clone_integrity.txt` | R783-4 | `c73be9b93101fde17c5545145b21066f24f7b99b` |
| Robustness | CLEAN | `run.py:139-145`; `hooks.py:446,472-476`; `receipts/group_term_probe.txt`, `group_scenario_demo.txt`, `source_and_deletion_probe.txt` | R783-4 | `c73be9b93101fde17c5545145b21066f24f7b99b` |
| Tests | CLEAN | `hooks_selftest.py`; 12 source mutants; 8 deletion sets; 96 firing sites; twins remade; `receipts/selftest_vs_published.txt` | R783-4 | `c73be9b93101fde17c5545145b21066f24f7b99b` |
| Docs | CLEAN | `README.md`; 96-row table against `MUTANTS`; `mutant_rules.json`; PR body; `receipts/delta_hygiene.txt`; published docs gate summary | R783-4 | `c73be9b93101fde17c5545145b21066f24f7b99b` |

## Real limits

- **Signature:** the brief says a signed packet. Evidence commit `f640f816` reads `verified=false` on the hosting service and I found no signature file, so no signature was verified. Integrity rests on `MANIFEST.json` (23 fetched `author-r4` files, 0 differ) and `INDEX.md` (19 digests, 0 differ) (`receipts/evidence_integrity.txt`). That is a sample of the 144 files in the packet.
- **Not rerun:** the four runs, the plants, the builder, the boundary gate, any simulation, the full docs gates and `behave`. No simulator was used. The figures rest on the published tables and prior rounds, and nothing they depend on moved.
- **Docs gates:** the published summary lists 98 gates, each rc 0 with a clean tree: 96 indexed logs plus 2 large ones recorded by digest. I ran `check_doc_style.py`, which passed. `check_em_dash.py` could not run: its pinned renderer is not installed here, rc 2. In its place a direct scan found no em dash in the 32 added lines, and the published index lists `em_dash.log` at rc 0.
- **Rule table:** I confirmed what each of the 96 fires, and read the reading notes and every row the delta touched. I did not re-judge all 96 names one by one, as the ruling stops at one audit. Of the 61 twins, I remade the supersede terms, the two renamed rows and three others in my own spelling; the rest rest on the published receipt.
- **Prior scripts:** not rerun. I wrote my own equivalents and read the published receipts: `r783_source_probe.txt` (43 of 51), `r784_r3_probes.txt` for its supersede rows, and the total of `source_mutants.txt` (48 of 58). I did not check their other rows.
- **Probe scripts:** three bugs of my own were fixed during the round: a docstring read as a statement, a directory-name collision, and a filter that missed `acmp-disc` and briefly gave a wrong answer on the group term. The published receipts are the final runs.
- **Hosted evidence:** last read at 2026-11-06T21:12:45Z, six check runs at this head, all queued, none concluded and no job executed. Nothing is claimed from them (`receipts/hosted_state.txt`).
- **Scope:** code outside the delta keeps its prior lens verdict. Physical calibration NOT RUN, and field skips are not hardware proof. No manager source bank is claimed or inferred at this head.

## Pending manager duties

- Obtain the second independent review at this exact head, and decide whether S1 or S2 goes to the author.
- Validate the current-dev merge candidate at the merge turn (source base `5b5f4336`, live dev `3f6bef88bd8a78cb2833a12572b9c4a9013f9bdf`), with builder and native banks, and link its receipts.
- Own hosted and act acceptance at this head; the hosted contexts were still queued.
- Carry the maintainer decisions: the amended column's scope, and one path or per descriptor for the ALL push.
- Keep #665 open for S5's "each hook within its bound", with the owners ruled in 6677495623.
- A later commit touching the harness un-covers `Tests`, and the lenses whose artifacts it changes, under AGENTS.md section 7.

R783-4 FINISHED
