[R783] NEGATIVE - exact head 26ba56e1d5749a71668f9e4436f28e8635f03f95

# R783-2: issue #665 lane S5 / PR #844, round 2, internal cleared-context review

- **Head:** `26ba56e1d5749a71668f9e4436f28e8635f03f95`, tree `47d25f3f8b51c5917f2575950612e5977562b730`. `665-s5-hooks` -> `dev-soft-core`, source base `5b5f4336`.
- **Delta judged:** `eef3d97a..26ba56e1`, four commits. Against the base, only the six files of `tb/verilator/ctrl_service_hooks/` differ.
- **Verdict:** NEGATIVE, on two MINOR findings. **No measurement, figure or verdict in the tree is wrong.**
  - F1 (Tests, Conformance, Docs): round 2 item 2 asks for a check of every grading rule. Some rules of `held_row` and `summary` are still unpinned, while the README says every rule is.
  - F2 (Docs): "the amended bounds would change none of them" is false at path level. Four 8x8 per-descriptor rows move inside the 60 ms ceiling.
- **Everything else asked of this round holds.** All prior findings are resolved, no verdict reads the amended column, all 732 round 1 paths reproduce, and the ceiling reaches only the ALL-push rows.
- **Also here:** five SUGGESTIONs and no RESIDUE. "Each hook within its bound" stays open as ruled and is not reported as a finding.

## Reconstruction

Read in the assigned order: AGENTS.md; CONTRIBUTING.md sections 3 and 6; the #665 body; the S5 assignment 6513150371 and takeover 6513247351; the clock decision 6514866239; the ruling 6677495623; the maintainer's decisions 6681686082; the grading answer 6682851386; the STOP 6682623686 and REVIEW READY 6692163137. Then `git diff 5b5f4336..26ba56e1` and its history, then the published evidence at `17981cf5`. R783-1 and R784-1 were read only after the independent pass over the diff.

## Focus checks

| Check | Result | Evidence |
|---|---|---|
| Verdicts stay on the base's bounds; no verdict reads the column | **Confirmed, statically and dynamically.** `amended_ms` and `amended_service_ms` are called only from `run.table` and `run.amended_cell`, and `table` feeds only `table.md`. On real head logs, regrading with the amended constants at 1e6 and at 0 gives an identical grade, and no table cell but the amended one changes (21 of 69 lines at 8x8, 7 of 39 at 1x1). `T_SVC_MS`, `LAYOUT_SWING_CYCLES`, `NORMATIVE_MS` and `bound_ms` are unchanged in the delta. | `receipts/sim_compare.txt` |
| Per-descriptor rows beside the ALL-push row | **Confirmed.** 5 rows at 1x1 and 19 at 8x8, beside `counters.all.if0`, in `results.json`, `table.md` and the README. Same start, recipients and barrier as the whole push. The last row ties the whole push, and the summary names `counters.all.if0`. | `receipts/amended_audit.txt`, `receipts/doc_checks.txt` |
| All 732 round 1 paths reproduce to the cycle | **Confirmed, recomputed from the raw `results.json`, not from the author's summary.** 732 of 732 identical in all 12 compared fields; 0 gone; 24 added, all per-descriptor. Findings: none lost; the 20 gained are all per-descriptor rows. The author's `build different executable` is benign: the firmware ELF digest is equal at each point. | `receipts/compare_rounds.txt` |
| Reviewer's own simulation at this head | **Reproduced.** `hooks-counters` built and run at both points on the answering arm: 8 + 22 rows, 0 field differences, same findings, same ELF digest. Every "first notice", "last notice" and "own fan-out" figure of both README tables reproduces from the raw log, in push order. These could not be checked from `results.json`. | `receipts/sim_compare.txt`, `receipts/sim-*.log`, `receipts/sim-*-table.md` |
| Each of the 79 mutants fails on its own rule | **Holds for 78; one is collateral (S4).** All 79 fail by assertion, 0 by a crash. The two disclosed round 1 mutants now fail on their rule. `amended: the column grades a path` fails on `SRP 22.0`, the column arithmetic, before reaching `the amended bounds graded a path`. That assertion is live: my `a-within-reads-column` and `a-queued-within-reads-column` reach it. | `receipts/mutant_audit.txt`, `receipts/source_mutants.txt` |
| The column applies the queued ceiling only to ALL-push rows | **Confirmed as the author assumes.** Replayed over all 756 published rows: the only non-SRP rows whose amended bound differs are `counters.all` and its 19 descriptors at 8x8, 20 rows beside 21 H-SRP rows. At 1x1 the ceiling equals the bound. `counters.first`, `counters.held`, `counters.loaded` and every H-NOTIFY path keep 20 ms. Whether that scope is right stays the maintainer's, as disclosed. | `receipts/amended_audit.txt` |

## Findings

### F1: MINOR (Tests, Conformance, Docs). Round 2 item 2 is not fully met: some grading rules of `held_row` and `summary` have no check, and the README says every rule is pinned

- **Where:** `tb/verilator/ctrl_service_hooks/run.py:99` and `:92`, `:174`; `hooks_selftest.py:434` (`check_held_grade`), `:455` (`check_missing_held`), `:472` (`check_summary`); `README.md:206`.
- **Authority:** ruling 6677495623 item 2: "a self-test check for every grading rule in `run.py:81-96, 156-172`, each failing on its defect". AGENTS.md section 6 Tests.
- **Evidence:** source-level mutants, each one edit in a scratch copy, against the harness's own self-test. Each of these leaves 28 of 28 checks and 79 of 79 mutants green (`receipts/source_mutants.txt`):
  - `hp-row-ms-zero` and `hp-ms`: the measured held row reports `ms=0.0`, or `held['ms'] + 1`. `check_held_grade` never reads the row's `ms`.
  - `s-narrow-le`: the summary's narrow count uses `<=` for `<`. `check_summary`'s only near fit has a slack of 1,000 cycles, so the boundary is not exercised. The matching rule in `grade_all` is pinned (`n-finding-le` is killed), so the two can disagree.
  - `hm-cycles`, `hm-wait`, `hm-margin`: the never-sent row's recorded CPU cycles, W and margin.
- **Impact:** `within` is computed from `held['ms']`, not the row's `ms`. So a held row could publish 0.000 ms marked within its bound, and `summary` could mis-rank it, while the self-test stays green. That is the class R784-1 F-2 named: "misreport a hook's published verdict while the self-test reports" full marks. At this head the figures are right, and my simulation reproduces `counters.held`. The gap is in the gate, and `README.md:206` claims it is closed.
- **Required outcome:** a check fails on each of those six mutants, the narrow boundary tested at slack equal to the swing and one below it. The row's labels (`hm-group`, `hm-path`, `hm-interface`, `hm-family`) may be pinned or not, but then line 206 must not say "every rule".
- **Verification:** `source_mutants.py` reports those six as killed.

### F2: MINOR (Docs). "The amended bounds would change none of them" is false at path level and contradicts the same section

- **Where:** `README.md:444`; the PR body's Grading row ("the amended bounds change no verdict"); REVIEW READY 6692163137.
- **Authority:** AGENTS.md section 6 Docs; ruling 6677495623, which keeps the one-path and per-descriptor readings open, reported both ways.
- **Evidence:** four 8x8 answering-arm rows are `NO` at this base and within the column's 60 ms (`receipts/amended_audit.txt`):
  - `counters.all.t5.i1.if0`, 21.70 ms;
  - `counters.all.t5.i2.if0`, 33.43 ms;
  - `counters.all.t5.i3.if0`, 44.89 ms;
  - `counters.all.t5.i4.if0`, 57.15 ms.

  `README.md:454` states the same fact: 18 of 19 rows over 20 ms, but 14 of 19 over the ceiling. The sentence is true of each hook's verdict and of the ALL push as one path, and false of path verdicts, which is what "verdict" means elsewhere: `README.md` Grading says "no verdict, finding or count reads it", and the PR body says the 732 paths keep "the same verdicts".
- **Impact:** the per-descriptor question is the open owner decision, and these four rows are exactly where the two readings differ. A maintainer relying on "change no verdict" is told there is no difference.
- **Why MINOR and not RESIDUE:** the fix is words only, but the sentence is itself a claim about verdicts on a question under ruling. The owner's rule sends an unsure case to MINOR.
- **Required outcome (exact fix), in the README, and likewise in the PR body:** "For information, the amended bounds would change no hook's verdict: no H-SRP path lies between 18 and 20 ms, and the ALL push as one path stays over its ceiling at both points. Per descriptor, four 8x8 rows would move inside the 60 ms ceiling: `t5.i1` to `t5.i4`, 21.70 to 57.15 ms."
- **Verification:** `amended_audit.py` lists exactly the rows the sentence names.

### Suggestions (optional, none affects the verdict)

- **S1 (Tests):** `hooks_selftest.py:424`. The self-test's unplanted findings exclude the plant's own path by construction. So moving `counters-late` onto `counters.all.if0` leaves the self-test green, while the real unplanted findings then report it caught, the round 1 defect at path level (`receipts/vacuity_probe.txt`, `p-counters-probe-all`). Not MINOR because item 1's rule is met and the published real controls show 0 of 16 plants matching unplanted, which I confirmed independently. That evidence is a one-off receipt, though, and #810's re-grade changes the baseline. Pin each plant's path as the bounds are pinned, or refuse a plant on a path known to miss.
- **S2 (Tests):** `check_amended` covers `within`, `LATE` findings and the misses count. Three mutants survive: `a-slack-reads-column` (`NARROW`), `a-exit-reads-column` (exit status) and `a-loaded-queued` (`counters.loaded` takes the ceiling, the one row where that would flip a verdict, 36.62 ms at 8x8). The tree behaves correctly on all three; add the expects.
- **S3 (Tests):** `hooks.py:354`. "The ALL push ... is listed first" decides which row `summary` names on the tie, and `c-whole-last` survives. Add an expect.
- **S4 (Tests):** have `graded_by_amended` (`hooks_selftest.py:700`) leave `bound_ms` as written, so the mutant fails on its own assertion and the audit's claim holds for all 79.
- **S5 (Conformance, Docs):** 6682851386 also gives the first notice 20 ms. The column gives `t6.i0` at 8x8 the 60 ms ceiling. That is defensible, because the row ends on a queued notice, but a clause would help: the ALL push's first notice leaves at 2.76 and 4.68 ms, inside 20. Separately, `AMENDED_QUEUED_CEILING_MS[interfaces]` raises `KeyError` after a whole simulation if a third interface count ever joins `POINTS`.

The other survivors are not defects: `a-hook-srp-all` is equivalent, every other family being 20 ms; `p-contains` differs on no finding the format can produce; `hm-ahead` and `hp-ahead` set a field no table reads; `hp-margin-round` needs a non-integer margin; `c-wait-count` is a stimulus wait the self-test does not model.

## Prior findings at this head

| Finding | Status | Evidence at this head |
|---|---|---|
| R784-1 F-1 = R783-1 F1, `counters-late` plant | **RESOLVED** | `run.py:251-259`: a late plant is caught only on its own path. On the published unplanted findings it matches 0. The real no-op run prints `ESCAPED`, rc 1. All 16 plants are caught, each late plant's path within its bound unplanted (`receipts/doc_checks.txt`). |
| R784-1 F-2, three unpinned rules | **RESOLVED as filed** | Its three mutants each fail a named check. The ruling's wider "every grading rule" is F1 above. |
| R783-1 F2, `ctrl_configs.py` | **RESOLVED** | Blob `afde4f28` equals the base. No file outside the harness directory differs. The published trial merges with #810, #812 and `a68536fa` report 0 conflicts. Boundary gate receipts at this head: `ctrl_boundary: PASS` in both modes. |
| R783-1 R1, R2; R784-1 RESIDUE-1, 2, 3 | **RESOLVED** | Each exact fix is in the diff and PR body. A scan of all 2,662 added `.py` lines, with positive controls, finds no lane label, round, reviewer ID or comment ID (`receipts/comment_scan.txt`). |
| R784-1 S-2 | **Taken** | `hooks_selftest.py` now runs standalone: 28 of 28, 79 of 79. |
| R783-1 S1 P1, P12 | **Taken** | Both are now named mutants. |
| R783-1 S1 P2, P3, P4, P9; S2, S3, S5, S6; R784-1 S-1, S-3 | **Retained, optional** | Disclosed as not taken. |

## Round 2 items

| Item | Result |
|---|---|
| 1. Plant caught only when applied, with a self-test | Met (S1 optional) |
| 2. A check for every grading rule, each failing on its defect | **Not fully met: F1** |
| 3. `ctrl_configs.py`, option 2 | Met |
| 4. Per-descriptor rows beside the ALL-push row | Met |
| 6682851386: base bounds, marked; one information column; no numerical rule changed | Met; the claim about its effect is F2 |

## Lens results

```text
[R783] MINOR Conformance - hooks_selftest.py:434,455,472 against ruling 6677495623 item 2 - not every grading rule has a check (F1)
[R783] PASS RTL - git diff 5b5f4336..26ba56e1 --name-only; hooks_soc.py blob equal to eef3d97a; six gitlinks equal to the base; ELF digests equal to round 1 - no hdl/ or firmware file in the diff, nothing the prior RTL verdict depends on moved, hooks_build.py:93-96 changes paths only
[R783] PASS Robustness - run.py:251-259,328-331; hooks.py:92-103; hooks_build.py:93-96; receipts/doc_checks.txt - a plant path left unmeasured becomes a refusal, so ESCAPED rc 1, never caught; Plant field order and the late() signature checked at every call; head code re-renders the four published table.md byte for byte; standalone entry runs; S5's KeyError is unreachable with the two POINTS
[R783] MINOR Tests - hooks_selftest.py:434,455,472 - six surviving mutants on held_row and summary (F1)
[R783] MINOR Docs - README.md:444,206 - the amended-bounds claim (F2) and the every-rule claim (F1)
```

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Rulings 6677495623, 6681686082, 6682851386; `hooks.py:71-103`; `run.py:187-218`; 756 published rows; `receipts/amended_audit.txt`, `compare_rounds.txt` | R783-2 | `26ba56e1d5749a71668f9e4436f28e8635f03f95` |
| RTL | CLEAN | Delta file list; `hooks_soc.py` blob; `hooks_build.py:93-96`; gitlinks; ELF digests | R783-2 | `26ba56e1d5749a71668f9e4436f28e8635f03f95` |
| Robustness | CLEAN | `run.py:251-259,328-331`; `hooks.py:92-103,129-131,325-358`; `hooks_build.py:93-96`; `receipts/doc_checks.txt` | R783-2 | `26ba56e1d5749a71668f9e4436f28e8635f03f95` |
| Tests | UNCLEAN (F1) | `hooks_selftest.py` (28 of 28, 79 of 79 reproduced); `receipts/mutant_audit.txt`; 58 source mutants; `receipts/vacuity_probe.txt`; 16 plant receipts; 30 rows re-simulated | R783-2 | `26ba56e1d5749a71668f9e4436f28e8635f03f95` |
| Docs | UNCLEAN (F1, F2) | README delta; both per-descriptor tables against the raw log; 79-row mutant table against `MUTANTS`; PR body; REVIEW READY; `receipts/comment_scan.txt` (comment rule, and U+2014 over all 3,166 added lines: 0) | R783-2 | `26ba56e1d5749a71668f9e4436f28e8635f03f95` |

## Real limits

- **The packet is not signed.** GitHub reports commit `17981cf5` as unverified, reason `unsigned`, and the tree holds no detached signature. What I verified is its `MANIFEST.json`: 432 of 432 published digests match and no file is unlisted. That shows consistency, not authorship. 21 files are path-redacted, so their published digest differs from the original.
- **Re-simulated:** only `hooks-counters`, 30 rows, on the answering arm at both points, with Verilator 5.050 (identity checked). The other paths rest on the published `results.json`.
- **Not run by me; these rest on the author's receipts:** the 16 plants and the no-op plant (at `78415f7a`, README-only change since); the full point runs (at `d5add6f9`, regraded at the head); the firmware self-test; the CPU budget harness; `test_builder.py`, whose registered NOT RUN gate 11 arm its verdict does not cover; the boundary gate; the 98 docs and CI gates; behave; the candidate merge.
- **The amended column is a ceiling.** The derived bound is #810's, so nothing here tests it.
- **Not read:** the author's `HANDOFF.md` files in the packet, as lane material, and all private material.
- **No manager source bank exists at this head; none is claimed or inferred.**
- **Hosted, at snapshot:** 9 success, 1 skipped, 39 queued or in progress (`receipts/hosted_checks_snapshot.tsv`). The skipped context is not executed evidence, and the manager owns acceptance.
- **Physical calibration NOT RUN.** No hardware was used, and field skips are not hardware proof.
- **Clone after probes:** head, tree and index tree exact; 1,496 tracked files rehashed, 0 differ; modes 1,448 x 100644 and 48 x 100755; six gitlinks unchanged; 0 status lines including ignored (`receipts/verify_clone.txt`). My build left two ignored `__pycache__` directories, which I removed.

## Pending manager duties

- Round 3 for F1 and F2. Only the self-test, the README and the PR body need change, so no re-measurement is implied.
- The maintainer's disclosed question: the column's scope, settled by #810's re-grade, and the one-path or per-descriptor decision. F2's four rows are where they differ.
- Hosted and act acceptance at the final head, and the current-dev merge candidate with its builder and native banks.
- S5's "each hook within its bound" stays open on #665, as ruled.

R783-2 FINISHED
