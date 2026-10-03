[R446] POSITIVE - exact head ec7eb2d8ff81700842f4e3a35b79879c8c3838e5

# R446-5: internal review of PR #638 (issue #234), round 5

- **Role:** [R446], cleared-context internal reviewer. Executor [A516]; external reviewer [R447].
- **Head:** `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5`, tree `f541830baddcc43387291b42719e7344045ca3f0`, in an isolated detached clone. Source base `1269cdafb4bb964c757baae0f0c5a932d43f540b`.
- **Round 5:** `79e53831..ec7eb2d8`, two one-line commits with no trailers (`receipts/r5-commits.txt`). Five files change: the gate, its self-test and mutants, `AREA_BUDGET.md` and the recipe (`receipts/r5-diff-name-status.txt`). No RTL, XDC, Tcl, workflow, baseline JSON or policy value changes.
- **Inputs, read in this order:**
  1. AGENTS.md and CONTRIBUTING.md.
  2. Issue #234: the body, rulings 5967852698 and 5967924270, the round-5 assignment 5970587136 and REVIEW READY 5970940747.
  3. The diff and history.
  4. Public evidence: `43ad8362:review-evidence/234-r1` (round-1 records and rankings), `6c098ef1:.../author-r4/receipts/armq-census.tsv`, and the executor's round-5 packet `b7a59a04:.../author-r5` (fuzz digests only).
  5. The live PR body, read 2026-10-03T16:23Z (body updated 16:14:36Z).
  6. The prior findings, R446-4 (this reviewer's) and R447-4 (5970584109). I read these only after my own pass over the diff and after recording a draft verdict.
- **Real measurements:** the A and B Vivado run directories that rounds 1 to 4 used. Each was read only through symlink mirrors, never written. Every result equals round 4 byte for byte.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open.

- R446-4 F1 is resolved by ruling (a). Every key of the baseline and the image manifest is held to `[A-Za-z0-9_.:/-]{1,128}`, the keys of open objects included. A record's sub-block scope names alone may also hold `[` and `]`.
- Every wording item assigned for round 5 was taken exactly.
- One new RESIDUE (R1, PR-body wording) and one SUGGESTION (S1, three class-widening name mutants the self-test does not kill) are recorded. Neither affects the verdict or a lens.
- All five lenses are covered clean at this head.

## Findings

```text
[R446] R1 RESIDUE Docs - PR #638 body, Round 5 table, row "R446-4 F1" (and REVIEW READY 5970940747 item 1) - "run by `strict()` on every JSON the gate reads"
```

- **Evidence:**
  - The three commands read JSON only through `strict()`:
    - the baseline, in `load()` (`syn/ooc/pp_resource_gate.py:503`), which also covers the text `record --write` would write (`:728`);
    - the image manifest (`:203`).
  - The `--fuzz` test driver also reads `--baseline`, with plain `json.loads` (`:632`). Each generated case then goes back through `load()`, and a baseline the walk refuses makes the unchanged control exit 2, so `--fuzz` fails closed.
  - The gate docstring already scopes its contract to `check`, `record` and `check-baseline`, and the budget page and recipe make no such claim. The sentence is accurate for the gate's commands and over-broad only as written.
- **Why RESIDUE:** it is wording in the PR body only. No measurement, test, code or verdict changes.
- **Exact fix:** in that row, replace "run by `strict()` on every JSON the gate reads" with "run by `strict()` on every JSON that `check`, `record` and `check-baseline` read".

```text
[R446] S1 SUGGESTION Tests - syn/ooc/pp_resource_gate_selftest.py:427-437 (MALFORMED name arms); syn/ooc/pp_resource_gate.py:100, :102 - three class-widening name mutants survive the self-test
```

- **Evidence:** `receipts/r5-probes/probe-r5-names.log` runs 21 mutants of the walk, the `SCOPES` path and the two classes, each against the full `--selftest`. 17 are killed. Of the four that survive:
  - **Exit-equivalent:** "every level below the scopes object also scope". The shape check still refuses a bracketed scope-count key with exit 2, only with a different reason (equivalence check below).
  - **`SCOPE_NAME` admits a space.** The 500 self-test cases miss it; `--fuzz 5000` detects it.
  - **`SCOPE_NAME` admits an empty key.** Missed at 5,000 cases.
  - **`SCOPES` first element wildcarded**, `(None, None, "record", "scopes")`. Under it, a bracketed key at `description/x/record/scopes` gives exit 0.
- **The behaviour at head is correct in every case.** `receipts/r5-probes/probe-r5-cases.log` gives exit 2, through both commands, for:
  - a scope name with a space, an empty one, a brace, or 129 characters;
  - a bracketed key at `description/x/record/scopes`.
- **Where the gap came from:** round 5 moved the bad-name arms from the bracket class onto `NAME`. So the scope class's refusal side is now pinned only by the lone-surrogate arm (`:427`) and the 129-character arm (`:429`).
- **Impact:** no current input is affected. A later edit that widens `SCOPE_NAME`, or loosens the `SCOPES` path at its first element, would not be caught by the hosted self-test.
- **Optional:** add `MALFORMED` arms for a scope name with a space and an empty scope name, and one for a description note shaped as `{"x": {"record": {"scopes": {"a[1]": 1}}}}`, each expecting exit 2.

## Round-5 focus items, with evidence

1. **One walk on every JSON the gate reads.**
   - `names()` (`pp_resource_gate.py:418-436`) is iterative. It checks an object's keys before descending, and it descends both objects and lists.
   - `strict()` (`:439-447`) runs it after `json.loads`:
     - `load()` passes `SCOPES` (`:102`, `:503`);
     - the manifest read passes no scope path (`:203`).
   - `named()` (`:408`) now refuses repeated keys only.
   - The scope test `len(path) == len(scopes) > 0 and all(...)` is exact. Only the keys of `endpoints/<any>/record/scopes` take the bracket class. A path of the same depth under a note, or a deeper level, does not. The manifest has no scope path.
   - `probe-r5-cases.log` reaches every keyed place, through `check` and `check-baseline`:
     - **Exit 2:** a bracketed key in a ceiling, the identity, the record figures, a scope's counts, `schema` replaced by an object, and a `measured` list of objects.
     - **Manifest:** an entry's extra bracketed key, a nested object and a nested list exit 2. A named extra key exits 0.
     - **Scope names:** a bracketed scope name and `[]` alone exit 0.
   - The one JSON read outside `strict()` is the `--fuzz` test driver's (R1).
2. **The ruling's arms and mutants, on both sides.**
   - **Exit 2:**
     - a bracketed manifest key (`_selftest.py:276`);
     - a bracketed key in the file's `description` note (`:435`) and under a `measured` note's `scopes` (`:437`), both through both commands.
   - **Exit 0:**
     - a named manifest key (`:278`);
     - a bracketed scope name through `check` (`:357`) and `check-baseline` (`:370`).
   - **Mutants:** six new and one re-pointed (`_mutants.py:145-162`). All 162 shipped mutants are killed (`receipts/gates/gate-mutants.log`), and each new one is killed by an arm on the side it breaks (`receipts/prior-probes/r1-probe-pr-mutant-reasons.log`).
3. **The generator reaches keys inside open objects.**
   - The `note` operator (`:865-869`) writes a key from `OPEN_KEYS` (`:708`), as `{k: v}`, `[{k: v}]` or `{"scopes": {k: v}}`, into either file note or any endpoint's `measured`.
   - The `entry key` operator (`:959-962`) does the same in a manifest entry.
   - The fixture notes are now objects with a nested list (`:968`).
   - Only `text` and `run.2:a/b-c_d` are counted unbroken, which matches the ruling.
   - Generator-only detection in `probe-r5-names.log`:
     - **Detected:** dropping the walk, dropping list descent, dropping descent below the top level, a prefix match, `NAME` widened to brackets, a space, an empty key or no length bound, and the manifest left unchecked.
     - **Not detected:** the over-refusal mutants, which the oracle cannot see by design, and the S1 survivors.
4. **The wording residue was taken exactly.** Each item was checked against its finding's text:
   - **R447-4 R1:** the three-command barrier sentence, "every line those commands print", and the test-driver sentence (`pp_resource_gate.py:22-31`).
   - **R446-4 S1:** "Exit status of check, record and check-baseline:" (`:22`).
   - **R447-4 R2:** the exact sentences in `AREA_BUDGET.md:208` and recipe `:477`.
   - **R447-4 R3:** the Description row "one of two converters, whole() (1 to 15 ASCII digits) or real() (a finite float)".
   - **R446-4 R1:** Round 4 paragraph, "only a command line that argparse rejects (a missing, unknown or ill-typed argument) exits 2 through argparse, before the barrier".
5. **The docstring's exit contract is scoped to `check`, `record` and `check-baseline`** (`:22-31`).
   - An argparse rejection with a non-ASCII argument exits 2 with an escaped message and no traceback, under strict-ASCII streams. I checked an unknown command, an extra argument, a missing value and a bad `--seed`.
6. **Proportionality.** Round 5 is +115/-64 in the five assigned files and adds nothing outside the assignment. The self-test is 999 lines, inside the ratchet (`receipts/gates/py-idiom.log`).

## Executable evidence at this head

| Run | Result |
|---|---|
| Touched gates, GNU Make 4.3 built from the checksummed 4.3 tarball (`receipts/gates/summary.txt`) | 31 of 31 rc 0. The three Markdown gates were rerun under the pinned renderer environment (`gates/NOTE.txt`). |
| Gate self-test | 254 arms and 500 generated cases PASS |
| Shipped mutant campaign | control passes, 162 of 162 killed |
| `check-baseline` | PASS, 3 endpoints |
| Real data (`receipts/real/`) | A route, 1x1 and 8x8: rc 0. A 10 ns control: rc 2. B route: rc 1 (+625 LUT). B 1x1 and 8x8: rc 0. Every output byte-equal to round 4. |
| `--fuzz`, seed 234 (`receipts/fuzz/digests.txt`) | Fixtures 20,000, A route 20,000 and A 1x1 5,000: 0 failures. Each case digest equals the executor's round-5 receipt. |
| `probe_r4_structure.py`, unchanged (`r4-probes/structure-vs-r4.txt`) | 32 cases. The two note cases go from rc 0 to rc 2, and the manifest bracketed key from 0 to 2: the ruling. Its built-in `want=0` predates the ruling, so it prints BAD. The other 29 cases are unchanged. |
| `probe_r4_generative.py`, unchanged | As in round 4. The two barrier-narrowing mutants are killed by the self-test. Four spans no longer apply because round 5 rewrote them; all four are re-pointed in `probe_r5_names.py`, and each is killed. |
| `probe_r4_adhoc.py`, `probe_r447_3_cases.py`, unchanged | 0 not as expected. Six rankings and six `armq_r` census rows are equal to the published evidence. |
| Rounds 1-3 probes, unchanged (`receipts/prior-probes/`) | Every rc equals round 4. Text differs only in temporary paths, the new name-refusal reasons and the arm count (247 to 254). `probe_pr_mutant_reasons`: every shipped mutant ARM. |
| `probe_r5_names.py` (new) | 21 mutants: 17 killed, 1 exit-equivalent, 3 SUGGESTION survivors (S1). The control passes. |
| `probe_r5_cases.py` (new) | 37 checks, 0 not as expected. `record --write` of A's route into a copy is byte-equal to the committed baseline and keeps its 5 bracketed scope names. Under `copy[1]` it gives rc 2 and leaves the file unchanged. |
| Tree after probes (`receipts/final-tree-verify.log`) | 985 tracked blobs: bytes and modes equal. Index and worktree clean, nothing ignored or untracked. Gitlinks: external `efeb541a`, gptp-processor `5dce647a`, protocol-processor `631eeb34`, verilog-axis `48ff7a7e`, each equal to base and checked out clean. |

**S1 exit-equivalence check** (`receipts/r5-probes/s1-equivalence.log`). I ran a bracketed scope-count key, and a bracketed key at `description/x/record/scopes`, through `check-baseline`.

| Gate | Scope-count key | Note key |
|---|---|---|
| Head | 2 | 2 |
| "every level" mutant | 2 | 2 |
| `SCOPES` first-element wildcard mutant | 2 | **0** |

## Prior findings at this head

| Finding | Status | Evidence |
|---|---|---|
| R446-4 F1 MINOR (Conformance, Robustness, Tests, Docs): bracketed keys accepted outside scope names | **Resolved** by ruling (a) | `names()`; the arms and mutants above; `structure-vs-r4.txt`; `probe-r5-cases.log` |
| R446-4 R1 RESIDUE | **Taken exactly** | live PR body, Round 4 paragraph |
| R446-4 S1 SUGGESTION | **Taken** | docstring `:22` |
| R447-4 R1, R2, R3 RESIDUE | **Taken exactly** | docstring `:22-31`; `AREA_BUDGET.md:208`; recipe `:477`; PR body Description row |
| R447-4 S1, S2 SUGGESTION | **Retained, open, non-blocking** | Not taken under assignment item 3, and listed under the PR body's limitations. S2's manifest-key part is now covered by the `entry key` operator. |
| R446-1 to R446-3, R447-1 to R447-3 | **Remain resolved** | Each prior probe reproduces its round-4 rc. R446-2 S1 (the wholly unrouted layout, exit 2) is still declined, as ruled. |

## Lens results

```text
[R446] PASS Conformance - pp_resource_gate.py:22-43, :98-102, :203, :408-447, :499-512; assignment 5970587136 items 1-3; rulings 5967852698/5967924270; receipts/real/ (A/B CLI, byte-equal to round 4); probe-r5-cases.log - the name class and its one exception hold as ruled for every key of the baseline and manifest; the acceptance-criteria status is unchanged from round 4 as ruled
[R446] PASS RTL - receipts/diff-name-status.txt (1269cdaf..ec7eb2d8: no hdl/, XDC or Tcl path); receipts/final-tree-verify.log (gitlinks equal to base); r4-probes/probe-r4-adhoc.log (armq_r census equal to the packet) - no RTL, interface, clock or reset change to judge
[R446] PASS Robustness - pp_resource_gate.py:418-447 (iterative walk), :683-736 (barrier); r4-probes/probe-r4-structure.log (32 cases); r5-probes/probe-r5-cases.log (37 checks); receipts/fuzz/ (45,000 cases, 0 failures); argparse non-ASCII checks - malformed, nested, deep, non-UTF-8 and out-of-class keys exit 2 without traceback, ASCII only
[R446] PASS Tests - pp_resource_gate_selftest.py:276-278, :336-370, :427-437, :708, :865-869, :959-968; pp_resource_gate_mutants.py:145-162; gates/gate-selftest.log, gate-mutants.log (162/162); r5-probes/probe-r5-names.log; prior mutant probes - both sides of the ruling have arms and killed mutants, and the generator reaches note and manifest keys (S1 optional)
[R446] PASS Docs - AREA_BUDGET.md:189-209; PP_SHADOW_BASELINE_RECIPE.md:456-479; gate docstring :3-50; live PR body (Description row, Round 4 paragraph, Round 5 section, limitations :362-363) - the docs state the class and the oracle as implemented; the five wording items were taken exactly (R1 is RESIDUE)
```

## Completion ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | gate `:22-43`, `:98-102`, `:203`, `:408-512`; assignment 5970587136; rulings 5967852698, 5967924270; `receipts/real/`; `probe-r5-cases.log` | R446-5 | `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5` |
| RTL | CLEAN | `receipts/diff-name-status.txt`; gitlinks in `receipts/final-tree-verify.log`; `probe-r4-adhoc.log` census | R446-5 | `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5` |
| Robustness | CLEAN | gate `:418-447`, `:683-736`; `probe-r4-structure.log`; `probe-r5-cases.log`; `receipts/fuzz/`; prior-probe reruns | R446-5 | `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5` |
| Tests | CLEAN (S1 optional) | self-test `:276-968` (254 arms, 500 cases); mutants `:145-162` (162 killed); `probe-r5-names.log`; `probe-r4-generative.log`; prior mutant probes | R446-5 | `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5` |
| Docs | CLEAN (R1 RESIDUE) | `AREA_BUDGET.md:189-209`; recipe `:456-479`; gate docstring; live PR body (read 2026-10-03T16:23Z, updated 16:14:36Z) | R446-5 | `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5` |

## Real limits

- **Physical calibration was NOT RUN.** Field skips are not hardware proof.
- **No Vivado run.** I re-judged the existing A and B run directories only. I did not regenerate those reports.
- **No full banks.** I ran no full parent, PP, gPTP, Yosys or builder bank, and no `act`.
- **Hosted checks were still running.** At `receipts/hosted-check-runs.txt`, read 2026-10-03T16:24Z, these were in progress at the exact head:
  - `docs-check`, `elaborate` and `yosys-elaboration`;
  - Verilator shards 0-4.

  These had passed: `changes`, `full-ci-gate`, `verilator-lint`, Yosys shards 0-3, `bdd-conformance`, `wire-accountability` and `docs-check-no-git`. "Physical gPTP" was skipped.
- **Exit-1 provenance is not checked by the generative oracle.** That is R447-4 S1, still open; the arms cover it.
- **The measurement inputs came from the executor's local run tree, read-only.** Their reproduction is anchored by the published records, rankings and census, and by fuzz digests equal to the executor's round-5 receipts.

## Pending manager duties

- Exact-head hosted acceptance: `rtl-fast`, `verilator-suites` and `yosys-portability` once the PR is marked ready, plus the act replica.
- The merge-turn candidate on live dev `bbf704ec`, which is distinct from this source validation on base `1269cdaf`.
- The merge-bank Vivado comparison under ruling (b), and post-merge containment.
- Carry R1 to the residue checklist with its exact fix.
- S1, and R447-4 S1 and S2, are optional.

R446-5 FINISHED
