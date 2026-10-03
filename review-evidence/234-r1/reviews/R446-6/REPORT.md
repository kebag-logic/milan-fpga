[R446] POSITIVE - exact head d5f56313dc5a5c2716211356f99796664dc843dd

# R446-6: internal review of PR #638 (issue #234), round 6

- **Role:** [R446], cleared-context internal reviewer. Executor [A516]; external reviewer [R447].
- **Head:** `d5f56313dc5a5c2716211356f99796664dc843dd`, tree `c6dcc1b61f274a3acf0479bfe47f72c25f86708d`, in an isolated detached clone. Source base `1269cdafb4bb964c757baae0f0c5a932d43f540b`.
- **Round 6 (`ec7eb2d8..d5f56313`):**
  - Three one-line commits with no trailers (`receipts/r6-commits.txt`).
  - Two files change: the gate's self-test and its mutant campaign, +55 / -37 (`receipts/r6-diff-name-status.txt`).
  - `syn/ooc/pp_resource_gate.py` is byte-identical to round 5.
  - No RTL, XDC, Tcl, workflow, baseline JSON, documentation page or policy value changes. Over the whole PR, `1269cdaf..d5f56313` has 15 paths and no `hdl/` path (`receipts/diff-name-status.txt`).
- **Inputs, read in this order:**
  1. AGENTS.md and CONTRIBUTING.md.
  2. Issue #234:
     - the body;
     - the rulings 5967852698 and 5967924270;
     - the round-6 assignment 5971250916;
     - REVIEW READY 5971779548.
  3. The diff and history.
  4. Public evidence:
     - `43ad8362:review-evidence/234-r1` (the round-1 records and rankings);
     - `6c098ef1:.../author-r4/receipts/armq-census.tsv`.
  5. The live PR body, read 2026-10-03T18:05:53Z (PR updated 17:44:49Z; `receipts/pr/`).
  6. The prior findings: R447-5 (5971246937) and R446-5 (this reviewer's, 5971159648). I read R447-5 only after my own pass over the diff and after recording a draft verdict (`receipts/draft-verdict-before-prior-findings.txt`).
- **Real measurements:** the A and B run directories that rounds 1 to 5 used, read only through symlink mirrors. All 242 files hash the same before and after the probes (`receipts/run-dirs-unchanged.txt`).

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open.

- **R447-5 F1 is resolved** (the only open MINOR at round 5):
  - Two new arms each put a refused key past the first item of a list and require exit 2: one in the last of three manifest entries, one in a note list.
  - The generator reaches every index.
  - The shipped "names past a list's first item" mutant is killed by `--selftest`.
- **R447-5 S1 and S2 were taken**, and their mutants are killed.
- **The compaction commit preserves behaviour.** Every arm and every data table is unchanged.
- **New items:**
  - R1 (RESIDUE, PR body): the reproduction checkout names round 5's head.
  - S1 (SUGGESTION): mutants of the list walk and the scope class that the self-test does not kill. The head behaves correctly on every input that reaches them.
- All five lenses are covered clean at this head.

## Findings

```text
[R446] R1 RESIDUE Docs - PR #638 body, "How to get into the same state" (line 391 of receipts/pr/pr-body-read-2026-10-03T18-05Z.md) and "Authoritative references" (line 380) - the reproduction checkout names round 5's head, and the round-6 assignment is not linked
```

- **Evidence:**
  - The body detaches at `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5`, which is round 5's head.
  - Its "How to validate" section, a few lines later, expects 260 arms and 174 mutants. Those are round 6's numbers: `ec7eb2d8` gives 254 and 162.
  - The references list links the lane and round-2 to round-5 assignments, but not round 6's (5971250916). The Round 6 section does cite it by number.
- **Why RESIDUE:** this is PR-body text only. No measurement, test, code or verdict changes.
- **Exact fix:**
  1. In "How to get into the same state", replace `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5` with `d5f56313dc5a5c2716211356f99796664dc843dd`.
  2. In "Authoritative references", after the round-5 link, add `and [round-6 assignment](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5971250916)`.

```text
[R446] S1 SUGGESTION Tests - syn/ooc/pp_resource_gate_selftest.py:352-355, :437-441 (the round-6 arms) against syn/ooc/pp_resource_gate.py:100, :102, :429-436 - list-walk, scope-path and scope-class mutants beyond the shipped ones survive the self-test
```

- **Evidence:** `receipts/r6-probes/probe-r6-lists.log` runs 28 mutants of the list walk, the `SCOPE_NAME` class and the scope path, each against the full `--selftest`. 19 are killed. Of the nine survivors:
  - **Exit-equivalent on every input probed:**
    - "visit order reversed". It changes only which of two refused keys is named first.
    - "scope path: last key free". Under it, a bracketed key in a record's `figures` or `identity` is still refused with exit 2, by the record's shape check (`probe-r6-equiv.log`).
  - **Over-acceptance:**
    - **"a list inside a list not descended".** Also missed by `--fuzz 5000`. A key in `[[{"x[1]": 1}]]` would pass.
    - **"first three items only".** Missed by the 500 self-test cases and detected at 5,000. The arms place keys at index 2 at most.
    - **"scope path matched as a suffix at any depth".** A bracketed key at `description/endpoints/x/record/scopes` would pass. The round-6 S2 arm pins depth 4 only.
  - **Over-refusal, the accepted side of `SCOPE_NAME`:** "no upper case", "no colon", "no hyphen" and "127 characters". The committed baseline's scope names hold none of those characters and are at most 28 long. So hosted `check-baseline` would not catch these either (`probe-r6-equiv.log`, "committed baseline unchanged": the head and each of these mutants exit 0).
- **The head is correct on each such input.** `receipts/r6-probes/probe-r6-equiv.log` runs `check-baseline` with the head's gate and with each mutant:
  - **Head exit 2:**
    - a key in a list inside a list;
    - a key in a note list's fourth item;
    - a record-shaped note at depth 5;
    - a bracketed key in a record's figures or identity.
  - **Head exit 0:** scope names with upper case, a colon or a hyphen, and a 128-character scope name holding every `SCOPE_NAME` character.
  - **Mutants:** each of the seven survivors that is not exit-equivalent gives the opposite exit on at least one of these cases.
- **Impact:** no current input is affected. A later edit of this kind would not be caught by the hosted self-test.
  - Two of the edits widen what the gate accepts: dropping nested-list descent, and matching the scope path as a suffix. Reaching either needs a hand-made note shape.
  - Narrowing `SCOPE_NAME` fails closed, with exit 2 at the next re-baseline.
- **Optional:**
  - **Scope names:** an exit-0 arm with a 128-character scope name holding every `SCOPE_NAME` character, `[` and `]` included. This mirrors R447-5 S1's `WIDE` arm for scope names.
  - **Note shapes:** exit-2 arms for `[[{"x[1]": 1}]]` and for a record-shaped note at depth 5.
  - **Line budget:** the self-test is at the 1,000-line module limit (`receipts/gates/py-idiom.log`), so these arms need the restructuring the executor already notes.

## Round-6 focus items, with evidence

1. **List items past the first (R447-5 F1, assignment item 1).**
   - **Fixture:** the image manifest now has three entries, `IMAGES` (`_selftest.py:47`, written at `:121-122`).
   - **Manifest arm:** `check` with `x[1]` in the last entry (`:352-353`) requires exit 2 naming "in /2". Round 5's arm at `:273` still covers index 0.
   - **Note arm:** `[{"a": 1}, [], {"x[1]": 1}]` in `measured` (`:437-438`) requires exit 2 naming "in /endpoints/route/measured/2", through `check` and `check-baseline`.
   - **Generator:**
     - The `note` operator inserts its key into a list of four at `rng.randint(0, 3)` (`:867-869`).
     - `entry key` picks any of the three entries (`:961`).
     - The fixture's `runs` note has three items (`:968`).
     - `receipts/r6-probes/probe-r6-generator.log` calls the self-test's own operators over 20,000 seeds. Note-list indices 0/1/2/3 occur 98/89/106/124 times, and entry indices 0/1/2 occur 885/945/886 times.
   - **Shipped mutant:** "names past a list's first item" (`_mutants.py:166`) is killed (`receipts/gates/gate-mutants.log:106`). It is an ARM kill (`receipts/prior-probes/r1-probe-pr-mutant-reasons.log`), and the round-5 self-test missed it (`probe-r6-newkill.log`).
   - **My own list mutants** (`probe-r6-lists.log`): the self-test kills "first item only", "last item only", "every item but the first", "every item but the last", "even indices only", "odd indices only", "the index a refusal names is always 0", "the top-level list not descended" and "lists below the top level not descended". The two non-equivalent list survivors are in S1.
2. **The accepted side of the name class (R447-5 S1).**
   - **Arm:** the `WIDE` key (`:170`) holds all 67 characters of `NAME` and is 128 characters long. It goes into a `measured` note and the last manifest entry, and must exit 0 (`:354-355`).
   - **Mutants:** nine shipped mutants (`_mutants.py:168-176`) each narrow `NAME` by one group, or to 127 characters. All nine are killed.
   - **Against round 5's self-test** (`probe-r6-newkill.log`): it misses five of the nine (dot, colon, slash, hyphen, 128). It misses eight of all twelve new mutants, and round 6's self-test kills all twelve. This matches REVIEW READY.
   - **Why two of them crash:** the lower-case and digit mutants refuse the fixture's own `path` and `sha256` keys. The reasons probe therefore counts them as CRASH: 163 ARM and 2 CRASH of 165.
3. **The scope path from its first key (R447-5 S2).**
   - **Arm:** a `description` note `{"x": {"record": {"scopes": {"a[1]": 1}}}}` must exit 2 through both commands (`:439-441`).
   - **Mutants:** it kills "scope path matched from its first key" and "scope path rooted at the endpoints table" (`_mutants.py:160-163`). It also kills my round-5 survivor "SCOPES: any top-level key" (`receipts/r5-probes/probe-r5-names.log`).
   - **Exit-equivalence probe, rerun unchanged** (`probe-r5-equiv.log`): the head exits 2 on both cases.
4. **The compaction commit `c7cde331`.**
   - `receipts/r6-probes/probe-r6-compaction.log` loads the self-test at `ec7eb2d8` and at `c7cde331`. It compares every module-level name: data by value, and functions by bytecode and constants.
   - **Arm tables:** all four are identical: route 99, standalone 8, command line 17 and malformed 45.
   - **New name:** `GROWN_FF` is new, and its expansion equals the two plants it replaces.
   - **Changed functions:** only `plant()` and `budget_file()` differ. Each now chooses `write_bytes` or `write_text` in one expression, which I judged equivalent by reading.
5. **Gate unchanged, behaviour unchanged.**
   - **Real data:** every scrubbed log is byte-equal to round 5 (`receipts/r5-rerun-comparison.txt`).
     - A route, 1x1 and 8x8: rc 0.
     - B route: rc 1 (+625 LUT).
     - B 1x1 and 8x8: rc 0.
     - The A 10 ns control: rc 2.
     - `check-baseline`: 3 endpoints.
   - **Generative digests** (`receipts/fuzz/digests.txt`) equal the PR body's Round 6 table:
     - self-test `151eb3fc6a0d989c`;
     - fixtures `0596f2c893188fb0`;
     - A route `257c96d2f917aff4`;
     - A 1x1 `55aadb1548e60ef3`.

## Executable evidence at this head

| Run | Result |
|---|---|
| Touched gates, GNU Make 4.3 built from the checksummed 4.3 tarball (`receipts/gates/summary.txt`) | 31 of 31 rc 0. The three Markdown gates were rerun under the pinned renderer environment (`gates/NOTE.txt`). |
| Gate self-test | 260 arms and 500 generated cases PASS |
| Shipped mutant campaign | control passes, 174 of 174 killed |
| `py-idiom` | over-long lines 0; long modules 10 <= 10. The self-test is 1,000 lines, at the limit. |
| `--fuzz`, seed 234 | fixtures 20,000; A route 20,000; A 1x1 5,000. 0 failures. `note` / `entry key` cases: 545 / 279, 569 / 283, 151 / 77. |
| `probe_r5_names.py`, rerun unchanged | 21 mutants: 18 killed and 3 survived (round 5: 17 and 4). The survivors are R446-5 S1's: one exit-equivalent, `SCOPE_NAME` space and `SCOPE_NAME` empty. |
| `probe_r5_cases.py`, `probe_r5_equiv.py`, rerun unchanged | 37 checks, 0 not as expected. Equivalence probe as in round 5. |
| Rounds 1-4 probes, rerun unchanged (`receipts/r5-rerun-comparison.txt`) | Every rc equals round 5. Logs differ only in temporary paths, the arm count (254 to 260), seed-dependent failure counts and the 12 added mutant rows. |
| `probe_r6_lists.py` (new) | 28 mutants: 19 killed and 9 survived, two of them exit-equivalent (S1). The control passes. |
| `probe_r6_equiv.py`, `probe_r6_generator.py`, `probe_r6_newkill.py`, `probe_r6_compaction.py` (new) | As described above. |
| Hosted checks at the exact head (`receipts/hosted-check-runs.txt`, read 18:08:57Z) | **Success:** `rtl-fast`, `changes`, `full-ci-gate`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3, Verilator shards 0 and 3, `bdd-conformance`, `wire-accountability`, `docs-check-no-git`. **In progress:** `docs-check`, `elaborate`, Verilator shards 1, 2 and 4. **Skipped:** "Physical gPTP". |
| Tree after probes (`receipts/final-tree-verify.log`) | 985 tracked blobs, bytes and modes equal. The index and worktree are clean, with nothing ignored or untracked. Gitlinks equal base and are checked out clean: external `efeb541a` (not initialised), gptp-processor `5dce647a`, protocol-processor `631eeb34`, verilog-axis `48ff7a7e`. |

## Prior findings at this head

| Finding | Status | Evidence |
|---|---|---|
| R447-5 F1 MINOR Tests: no case puts a refused key past a list's first item | **Resolved** | Focus item 1: arms `:352-353` and `:437-438`, generator `:867-869` and `:961`, the shipped mutant killed, and nine of my list mutants killed |
| R447-5 S1 SUGGESTION Tests: the name class's accepted side pinned for brackets only | **Taken, resolved** | `WIDE` arm; nine killed mutants; `probe-r6-newkill.log` |
| R447-5 S2 SUGGESTION Tests: the scope path pinned at its last key only | **Taken, resolved** for depth 4 | `:439-441`; two killed mutants. The deeper suffix variant is part of this round's S1. |
| R447-5 S3 SUGGESTION Robustness: the walk's memory growth | **Retained, open, optional** | Not taken under assignment item 3, and listed in the PR body's limitations. The gate is byte-identical, so this is unchanged. I did not re-measure it. |
| R447-5 S4 (R447-4 S1, S2) SUGGESTION Tests | **Retained, open, optional** | Listed in the PR body's limitations |
| R446-5 R1 RESIDUE Docs: Round 5 row, "run by `strict()` on every JSON the gate reads" | **Retained** (not in the round-6 assignment) | The text is still in the live body. The exact fix stands: replace it with "run by `strict()` on every JSON that `check`, `record` and `check-baseline` read". |
| R446-5 S1 SUGGESTION Tests: three class-widening name mutants survive | **Partly taken** | "SCOPES: any top-level key" is now killed. `SCOPE_NAME` with a space and with an empty key still survive (`probe-r5-names.log`). The PR body lists both as open. The head refuses both (`probe-r5-cases.log`). |
| R446-1 to R446-4, R447-1 to R447-4 | **Remain resolved** | Each prior probe reproduces its round-5 rc (`r5-rerun-comparison.txt`). |

## Lens results

```text
[R446] PASS Conformance - pp_resource_gate.py byte-identical ec7eb2d8..d5f56313 (receipts/r6-diff-name-status.txt); receipts/real/ (A/B CLI, byte-equal to round 5); rulings 5967852698/5967924270; assignment 5971250916 items 1-3 - the gate's behaviour and the acceptance-criteria status as ruled are unchanged; every assigned item is delivered
[R446] PASS RTL - receipts/diff-name-status.txt (1269cdaf..d5f56313: no hdl/, XDC or Tcl path); receipts/final-tree-verify.log (gitlinks equal to base); r4-probes/probe-r4-adhoc.log (armq_r census equal to the published packet) - no RTL, interface, clock or reset change to judge
[R446] PASS Robustness - pp_resource_gate.py:418-447 (names(), strict(), unchanged); r6-probes/probe-r6-equiv.log (nested lists, a fourth item, a depth-5 record shape, record figures and identity: exit 2; wide and mixed-character scope names: exit 0); receipts/fuzz/ (45,000 cases, 0 failures); prior probes (rc equal to round 5) - the refusals hold at every list index and depth probed
[R446] PASS Tests - pp_resource_gate_selftest.py:47, :170, :352-355, :437-441, :867-869, :961, :968; pp_resource_gate_mutants.py:160-176; gates/gate-selftest.log (260 arms), gate-mutants.log (174/174); r6-probes/probe-r6-newkill.log, probe-r6-lists.log, probe-r6-generator.log, probe-r6-compaction.log - each new arm fails for the defect it claims, the generator reaches every index, and the compaction preserves every arm (S1 optional)
[R446] PASS Docs - AREA_BUDGET.md:189-214 and PP_SHADOW_BASELINE_RECIPE.md:456-498 (unchanged; still true of the gate); live PR body Round 6 section and limitations (receipts/pr/) - the Round 6 claims match my digests, counts and probe reruns; R1 is RESIDUE
```

## Completion ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | gate byte-identity; `receipts/real/`; rulings 5967852698, 5967924270; assignment 5971250916 | R446-6 | `d5f56313dc5a5c2716211356f99796664dc843dd` |
| RTL | CLEAN | `receipts/diff-name-status.txt`; gitlinks in `receipts/final-tree-verify.log`; `probe-r4-adhoc.log` census | R446-6 | `d5f56313dc5a5c2716211356f99796664dc843dd` |
| Robustness | CLEAN | gate `:418-447`; `probe-r6-equiv.log`; `receipts/fuzz/`; prior-probe reruns | R446-6 | `d5f56313dc5a5c2716211356f99796664dc843dd` |
| Tests | CLEAN (S1 optional) | self-test round-6 hunks (260 arms, 500 cases); mutants `:160-176` (174 killed); `probe-r6-lists`, `-newkill`, `-generator`, `-compaction`; `probe-r5-names.log` | R446-6 | `d5f56313dc5a5c2716211356f99796664dc843dd` |
| Docs | CLEAN (R1 RESIDUE) | `AREA_BUDGET.md:189-214`; recipe `:456-498`; gate docstring; live PR body (read 2026-10-03T18:05:53Z, updated 17:44:49Z) | R446-6 | `d5f56313dc5a5c2716211356f99796664dc843dd` |

## Real limits

- **Physical calibration was NOT RUN.** Field skips are not hardware proof.
- **No Vivado run.** I re-judged the existing A and B run directories only.
- **No full banks.** I ran no full parent, PP, gPTP, Yosys or builder bank, and no `act`.
- **Hosted checks were still running** at the read time listed above.
- **R447's round-5 probes are not mine to run.** That is `probe_r5_namekill.py` and R447's `probe_r5_names.py`. The assignment's verification of them is R447's and the manager's. I verified the same property with the shipped campaign, `probe-r6-lists.log` and `probe-r6-newkill.log`.
- **R447-5 S3's memory figures were not re-measured.**
- **The measurement inputs came from the executor's local run tree, read-only.** Their reproduction is anchored by the published records, rankings and census, and by fuzz digests equal to the executor's round-6 table.

## Pending manager duties

- **Hosted acceptance at the exact head:** the remaining `verilator-suites` shards, `docs-check` and `elaborate`, plus the act replica.
- **The merge-turn candidate** on live dev `546437243e87eb5a78783a9e3cd5d1badcc3423e`, which is distinct from this source validation on base `1269cdaf`.
- **The merge-bank Vivado comparison** under ruling (b), and post-merge containment.
- **The residue checklist:** carry R1 and R446-5 R1 there, each with its exact fix.
- **Optional items:** S1, R446-5 S1's remainder, and R447-5 S3 and S4.

R446-6 FINISHED
