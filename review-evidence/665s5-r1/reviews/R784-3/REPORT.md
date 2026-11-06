[R784] NEGATIVE - exact head 3f8caae5eca7e681c3452eacdd818d1033a89f8d

# R784-3: external review of #665 lane S5 (PR #844), round 3

Head `3f8caae5eca7e681c3452eacdd818d1033a89f8d`, tree `54c36ee7cccf492d1800bca8da915c6e55c2feef`. Delta reviewed: `26ba56e1..3f8caae5`, one commit, `hooks_selftest.py` and the README only, against the ruling in issuecomment-6692737899.

The verdict is NEGATIVE on one open MINOR finding, F-1. Nothing measured is wrong, and the harness code behaves correctly at this head.

- **What holds:** the `aging` and `amended` mutants, all six source mutants, the narrow boundary, the amended-bounds sentence, and both of my round 2 findings. Each is confirmed by a run of my own.
- **What does not hold:** the third mutant this round rewrote, `supersede: any later group supersedes a refusal`. It does not fail on the rule it names, and the rule its check is named after is not pinned. Dropping the path from the comparison at `run.py:141` passes 28 of 28 checks and 94 of 94 mutants, and a path that was never measured then stops being a refusal.

The fix is one case in `check_superseded` and an honest mutant name. I tried the case on a disposable copy: the head still passes it and the surviving mutant fails it.

## Focus checks

| Asked | Result | Evidence |
|---|---|---|
| `aging` mutant fails on its rule, and the deletion makes it escape | **Confirmed** | It fires `hooks_selftest.py:618`, `armed < mark`. My round 2 `rule_probes.py`, unedited: probe B gives 93 of 94, and this mutant is the one that escapes (`receipts/rule_probes_r2_unedited.txt`). |
| `amended` mutants fail on their rule, and the deletion makes them escape | **Confirmed** | `the column grades a path` fires `:572`, then `:575`. `a finding reads the column` fires `:575`. Probe C gives 92 of 94, and those two escape. |
| `supersede` mutant fails on the rule it names | **Not confirmed (F-1)** | It fires `:596` and then `:598`, and the deletion makes it escape, but no group varies in either case. The rule in the check's title has no case (`receipts/r3_probes.txt`). |
| All six source mutants killed | **Confirmed, two ways** | `hp-row-ms-zero`, `hp-ms`, `s-narrow-le`, `hm-cycles`, `hm-wait` and `hm-margin` are each killed by the published `source_mutants.py`, unedited: 48 killed and 10 survived, as the PR states (`receipts/source_mutants_unedited.txt`). My own restatements of the six fail the same named checks (`receipts/r3_probes.txt`). |
| Narrow boundary at slack equal to the swing and one below | **Confirmed** | `check_summary` asserts slacks of 6,490 and 6,489 (`:502`). `<=` and `- 1` are killed in `summary`, and in the finding at `run.py:153` too. Deleting the count assertion lets all four narrow mutants escape. |
| Amended-bounds sentence, README and PR body | **Confirmed** | `README.md:459` and the PR body's Grading row carry the ruled sentence. Over all 756 published rows, read through the head's `hooks.py`, exactly four rows move: `counters.all.t5.i1` to `t5.i4`, 21.70 to 57.15 ms, on the 8x8 answering run. No H-SRP row is in the 18 to 20 ms band, and no hook's verdict changes (`receipts/amended_check.txt`). |
| Author's rule table | **93 of 94 accepted, one disputed (F-1)** | My independent map of each mutant to what it fires is below. |
| The departure from D2 | **Keeps the property** | Judgement below. |
| "Each hook within its bound" | **Stays open as ruled** | Not reported as a finding. |

### The author's rule table

I read each of the 94 mutants beside the assertion it fires. The author's audit, re-run at this head, matches the published receipt line for line (`receipts/mutant_audit_repro.txt`). I checked its claims too: chain lengths 59, 24, 7, 3 and 1, and three chains ending in an exception (`aging: the sink still waits`, `summary: alone and under load are not apart`, `ALL: no descriptor has a row`), each with its rule as first assertion.

- **Accepted, 93.** Where the first assertion is a positive control (`ok.applied == 1`), the mutant's defect is that the check stops applying, so the control is its rule.
- **Disputed, 1.** `supersede: any later group supersedes a refusal` => `other interface`. See F-1.
- **A limit of the audit, not a defect.** It tests that the fired assertion carries a chosen text. It cannot see a mutant whose name and behaviour differ, which is how the disputed row passed. Its control on the previous head exits 1 regardless, because the table has rules for mutants that head lacks. The evidence that it can fail is the count of three flagged, which the PR rightly states.

### The departure from D2

The author reads the column at one interface, not two, so that deleting the two assertions lets the mutant escape. **The property is kept.**

- At one interface only SRP's verdict moves, as the PR says.
- D2 at two interfaces still fails on `the amended bounds graded a path` (`receipts/rule_probes_r2_unedited.txt`).
- Three more shapes of my own all fail named checks: a verdict reading 60 ms on the ALL rows, on the descriptor rows alone, and 20 ms on SRP alone (`verdict-queued-60`, `verdict-descriptor-60`, `verdict-srp-20`).
- Keeping the `NO` pin rather than loosening it was right. D2 failed to escape because the test is stronger, not weaker.

What it costs is recorded as S-1.

## Findings

### F-1 [R784] MINOR Tests, Conformance, Docs - `tb/verilator/ctrl_service_hooks/hooks_selftest.py:586-598,741,802`, `run.py:141`, `README.md:204,235`, the PR body's Status and "A third mutant" - the supersede mutant does not fail on the rule it names, and the rule its check is named after is unpinned

- **Authority/evidence.** AGENTS section 6 (Tests): each test can fail for the defect it claims to detect. Ruling 6692737899 item 1: the PR sentence must be true of all the mutants. The PR says each of the 94 fails "on the rule it names", and of this mutant that it "now reaches that rule". `README.md:199` states the rule: superseded "only where `hooks-disc-aging` measured the same path on the same interface". `README.md:204` says the self-test checks it.
  - **The name and the behaviour differ.** `superseded_by_any_row` (`:741`) clears every refusal, with no regard to any row. It fires `other interface`, a case where the group is the right one. Neither `:596` nor `:598` varies the group. The old table edit, now `the table names another group`, is what holds the group rule.
  - **`another path` does not test the row's path.** `:597` changes the lost probe's path to `acmp.bind_rx`, which has no `SUPERSEDED` entry, so the table lookup refuses it before the row comparison runs. No case has a row of another path, in the named group, on the same interface.
  - **So that half of the comparison is unpinned.** Source mutant `sup-any-path` drops `x['path']` from `run.py:141`: 28 of 28 checks, 94 of 94 mutants, rc 0 (`receipts/r3_probes.txt`).
  - **The case is real.** `hooks-disc-aging` measures two paths per interface. With `available.if1` measured and `tmr_no_adp.if1` not, the head reports 2 refusals. Under the mutant it reports 0 and calls both superseded, one by its own group (`receipts/supersede_consequence.txt`). README:199 says a refusal "fails the run", so a never-measured H-DISC aging path would pass.
- **Why MINOR and not SUGGESTION.** This is the class of R784-2 F-1, and the round's own claim is that the class is closed. The hole is the exact rule in the check's title, and the brief asked for this mutant to be judged.
- **Impact.** No figure or verdict changes: `run.py:141` is correct and the published runs have 0 refusals. The gap is in the gate. The refusal rule is what makes a run fail on an unmeasured path, and #810's re-grade will run this code on a new baseline.
- **Required outcome.** A case in `check_superseded` with a row of another path, in the named group, on the same interface, leaving the refusal in place. A mutant that fails on it. The name `any later group` either given to a mutant that varies the group, or replaced by what the mutant does. The rule table, README row and PR sentence updated to match.
- **Verification.** `sup-any-path` is killed by the new assertion, and deleting that assertion makes its mutant escape. Trial on a disposable copy: head 28 of 28 and 94 of 94; `sup-any-path` fails `a row of another path` (`receipts/fix_feasibility.txt`, `scripts/fix_feasibility.py`).

### SUGGESTION (optional)

- **S-1 (Tests) - `hooks_selftest.py:726-730`.** Since the mutant reads the column at one interface, no registered mutant holds the `whole['within']` half of `:572`. The assertion works, as `verdict-queued-60` shows, but the suite would not notice losing it. Registering D2 under its own name beside the current mutant would hold it. It would not need to escape probe C, because the `NO` pin stays.
- **S-2 (Tests, retained from R784-2 S-1) - `check_amended`.** A `NARROW` finding or a hook's over-its-bound count read from the column still escapes that check (`narrow-finding-reads-column`, `summary-misses-read-column`; probes D4, D5). `README.md:206` now claims only verdicts and `LATE` findings, so this is accurate, and `README.md:168` is a true statement of the code.
- **S-3 (Tests) - `hooks_selftest.py:586`.** The docstring says a path "unmeasured there too" stays a refusal, and no case has that shape. The F-1 case can be that shape at no extra cost: the scenario in `scripts/supersede_consequence.py` is one.
- **Retained, as ruled:** R784-2 S-2 and S-4; R783-2 S1, S2, S3 and S5's `KeyError`.

No RESIDUE. The delta's added source lines have no lane label, round, reviewer ID or comment ID (`receipts/doc_scan.txt`).

## Prior findings, resolved or retained at this head

Read after my verdict and ledger were recorded (`receipts/verdict_before_prior_findings.txt`).

| Finding | Status | Evidence at this head |
|---|---|---|
| R784-2 F-1, `aging` and `amended` mutants | **Resolved** | Both fire their rule, and probes B and C make them escape. The wider class is F-1 above. |
| R784-2 F-2 = R783-2 F2, amended-bounds wording | **Resolved** | `README.md:459`, the PR's Grading row, `receipts/amended_check.txt`. |
| R784-2 RESIDUE-1, "leaves" | **Resolved** | `README.md:469`, "is committed". |
| R784-2 S-3 = R783-2 S5 first half | **Taken** | `README.md:469`: 2.76 and 4.68 ms, inside the 20 ms a first notice has. |
| R783-2 F1, six source mutants | **Resolved** | All six killed. Labels pinned at `:459,:482`. `README.md:206` says only what is pinned: the two unpinned fields, `row` and `ahead`, are read by no verdict, count or table in this harness, and `held-row-text` and `held-ahead` survive accordingly. |
| R783-2 S4 | **Taken** | Same fix as R784-2 F-1. |
| R784-2 S-1, S-2, S-4; R783-2 S1, S2, S3, S5's `KeyError` | **Retained, optional** | Declined under the ruling's rule on suggestions. |
| All R784-1 and R783-1 findings | **Resolved at the prior head; nothing they depend on moved** | `run.py`, `hooks.py`, `hooks_build.py` and `hooks_soc.py` are unchanged in the delta (`receipts/head_integrity.txt`). |

## Lens results

```text
[R784] MINOR Conformance - ruling 6692737899 item 1, PR body Status - the PR sentence is not true of the supersede mutant (F-1)
[R784] PASS Conformance - ruling 6692737899 items 2 and 3, four published results.json through the head's hooks.py, receipts/amended_check.txt, r3_probes.txt - six source mutants killed, narrow boundary at 6,490 and 6,489, ruled sentence in README:459 and the Grading row, four rows move and no hook verdict; grading unchanged per 6682851386
[R784] PASS RTL - git diff --name-only 5b5f4336..3f8caae5 -- hdl (empty), git diff --name-only 26ba56e1..3f8caae5 (two files), receipts/head_integrity.txt - no RTL or firmware in the delta, hooks_soc.py unchanged, so the prior RTL result stands
[R784] PASS Robustness - run.py:87-103,141,153,174, receipts/supersede_consequence.txt (head rows), r3_probes.txt - harness code unchanged in the delta; at the head an unmeasured path with only another path's row stays a refusal; a push never sent records no service; the exact-boundary slack is correct in both the finding and the summary
[R784] MINOR Tests - hooks_selftest.py:586-598,741,802 - own-path rule unpinned, mutant name differs from behaviour (F-1)
[R784] MINOR Docs - README.md:204,235, PR body Status and "A third mutant" - claims about that mutant and rule (F-1)
[R784] PASS Docs - README.md:206,459,469, the 94-row mutant table, PR body Round 3 - all 94 mutants listed by exact name, check and order; counts 28 and 94 agree; no stale "change none" wording remains (receipts/doc_scan.txt)
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F-1) | Ruling 6692737899; 6682851386; PR body; `receipts/amended_check.txt`, `r3_probes.txt` | R784-3 | `3f8caae5eca7e681c3452eacdd818d1033a89f8d` |
| RTL | CLEAN | Delta file lists; `hdl` diff empty; `hooks_soc.py` unchanged; six gitlinks | R784-3 | `3f8caae5eca7e681c3452eacdd818d1033a89f8d` |
| Robustness | CLEAN | `run.py:87-103,141,153,174`; `receipts/supersede_consequence.txt`, `r3_probes.txt` | R784-3 | `3f8caae5eca7e681c3452eacdd818d1033a89f8d` |
| Tests | UNCLEAN (F-1) | `hooks_selftest.py` delta and every check it touches; all 94 mutants against what they fire; 22 source mutants of my own and 58 published; 10 deletion probes; `rule_probes.py` unedited | R784-3 | `3f8caae5eca7e681c3452eacdd818d1033a89f8d` |
| Docs | UNCLEAN (F-1) | README delta and lines 168, 199, 204, 206, 459, 469; mutant table; PR body Status, Grading row, Round 3; `receipts/doc_scan.txt`, `amended_check.txt` | R784-3 | `3f8caae5eca7e681c3452eacdd818d1033a89f8d` |

## What I ran

All at the exact head, in a disposable export of its tree. No simulation or build was needed this round.

- `run.py --self-test` and `hooks_selftest.py` directly: 28 of 28, 94 of 94, rc 0 (`receipts/selftest_run.txt`).
- `scripts/r3_probes.py`: 22 source mutants and 10 deletion probes, each on its own copy. A control run confirmed the copy passes unmodified.
- The author's `mutant_audit.py` with its rule table, read first, then run: output equal to the published receipt.
- The published `source_mutants.py`, read first, then run unedited, in copies: 48 of 58 killed.
- My round 2 `rule_probes.py`, unedited.
- `scripts/amended_check.py` over the four published runs. It also re-renders all four `table.md` byte for byte with the head's code.
- `scripts/doc_scan.py`, `scripts/supersede_consequence.py`, `scripts/fix_feasibility.py`.

After the probes the clone is at exact head: head, tree and index tree match; 0 status lines including ignored; 1,496 tracked files rehashed with 0 mismatches; modes 1,448 x 100644 and 48 x 100755; six gitlinks as listed in `receipts/head_integrity.txt`. Nothing was written to the clone.

## Real limits

- **The evidence packet is not signed.** The brief calls it signed, but hosted verification of `700a07e6` reports `unsigned`, and the evidence tree has no detached signature. I checked digests instead: 178 fetched files of the 619 in `MANIFEST.json`, 0 mismatches (`receipts/evidence_digests.txt`). That shows consistency, not authorship.
- **Not re-run by me:** the four point runs, the 16 plants, the no-op control, the firmware self-test, the CPU budget harness, the builder, the boundary gate, the docs gates and the candidate merge. They rest on the author's receipts at the heads the PR lists. Only the self-test and README changed since, so what they measured stands.
- **The amended column is a ceiling.** The derived bound is #810's, so nothing here tests it.
- **Independence.** The listing of PR comments showed the first line of the other reviewer's report at this head, including its verdict word. I did not open that report, before or after this verdict, so nothing here is compared with it. The ruling and REVIEW READY, read first as the brief requires, name the prior findings in summary. The author's `HANDOFF.md` files were not read.
- **Hosted, at snapshot:** 23 contexts listed, 2 passed, 21 pending, so this is no evidence of hosted success (`receipts/hosted_checks_snapshot.txt`).
- Physical calibration NOT RUN, and field skips are not hardware proof. No manager source bank exists at this head, and none is claimed or inferred.

## Pending manager duties

- Carry F-1 to the author. It needs `hooks_selftest.py`, the README, the PR body and the rule table only, so no re-measurement is implied.
- The maintainer's open questions are unchanged: the column's scope, and one path or per descriptor.
- "Each hook within its bound" stays open on #665, as ruled.
- Own hosted and act acceptance at the final head.
- Build and validate the current-dev merge candidate at the merge turn (source base `5b5f4336`, live dev `87e9d03aa2a4797957ac0124d0c7851a2eec234c`) and link its receipts on the PR.
- Merge needs the full bar: two independent positive reviews, every lens covered clean at the merge head, and maintainer authorization.

R784-3 FINISHED
