[R447] NEGATIVE - exact head d5f56313dc5a5c2716211356f99796664dc843dd

# R447-6 external review: issue #234 / PR #638, round 6

- Head `d5f56313dc5a5c2716211356f99796664dc843dd`, tree `c6dcc1b61f274a3acf0479bfe47f72c25f86708d`. Source base is dev `1269cdafb4bb964c757baae0f0c5a932d43f540b`.
- Round 6 is `ec7eb2d8..d5f56313`: three one-line commits with no trailers, touching 2 files (the gate's self-test and its mutants, +55 / -37).
  - `pp_resource_gate.py` is byte-identical to round 5 (equal blob ids in `receipts/r6/diff_scope.log`).
  - There is no HDL, constraint, Tcl, workflow, doc or baseline-JSON change, and the gitlinks equal the base.
- **The verdict is NEGATIVE, on one MINOR finding (F1, `Docs`).** It is in the PR body only.
  - The body's "How to get into the same state" still checks out round 5's head `ec7eb2d8`. At that commit the expected results in "How to validate" (260 arms, 174 mutants) do not hold.
  - The Description row still states round 5's counts (254 arms, 162 mutants).
  - No code change is needed. Editing the PR body resolves it, and the head is unaffected.
- **The round-6 test work is correct and complete against the assignment (5971250916).**
  - R447-5 F1 is **RESOLVED**. My unchanged `probe_r5_namekill.py` now gives "walk visits only the first item of a list" selftest DETECTED rc 1, and `probe_r5_names.py` gives 72 of 72.
  - R447-5 S1 and S2 were taken, and every reviewer mutant they named is now killed by `--selftest`.
  - The compaction commit `c7cde331` is behaviour-preserving.
- Conformance, RTL, Robustness and Tests are covered clean at this head. Docs is not clean, because F1 is open.
- I also record one RESIDUE item (R1, PR body), one new SUGGESTION (S1, `Tests`) and two retained ones (S2, S3).
- My verdict, findings and ledger came from my own pass over the round-6 diff and my own probes. The table of prior findings was written afterwards.

## Inputs, in order

1. AGENTS.md and CONTRIBUTING.md (as loaded), and the docs map.
2. Issue #234's body and comments:
   - the rulings (5967852698) and the owner decision (5967924270), unchanged since round 2;
   - the **round-6 assignment (5971250916)**;
   - round-6 REVIEW READY (5971779548).
3. `git diff ec7eb2d8..d5f56313` in full, each commit on its own, and `1269cdaf..d5f56313` by name. The commit messages. The PR body, snapshotted in `receipts/r6/pr_body_snapshot.md` at `receipts/r6/pr_body_snapshot.read_at`.
4. Public evidence:
   - `43ad8362:review-evidence/234-r1/author/evidence`, extracted read-only to scratch for my unchanged round-1 and round-2 probes;
   - the A and B measurement directories, read only.
5. The exact-head hosted check runs, as a snapshot only.
6. My own R447-5 report and probes, to rerun them unchanged. `prior/ORIGINALS.txt` binds each of the 36 copies to its R447-5 packet copy, and all 36 are EQUAL.
7. After my verdict, findings and ledger were written: the prior public findings on this PR, to resolve them.

## Findings

```text
[R447] F1 MINOR Docs - PR #638 body (receipts/r6/pr_body_snapshot.md:391 and :40) - the body's reproduction command checks out round 5's head, and its Description row states round 5's self-test and mutant counts
Authority: AGENTS.md section 6, Docs lens ("The PR and Issue contain enough evidence for another cold reviewer"). Owner rule 2026-10-02: a defect that changes a figure or a stated state is not RESIDUE, and an uncertain case is MINOR.
Evidence:
- :389-393 "How to get into the same state" reads `git switch --detach ec7eb2d8ff81700842f4e3a35b79879c8c3838e5`. That is round 5's head. The body's own Status line (:21) names the head d5f56313.
- :410 "How to validate" expects "260 arms and 500 generated cases ... (174 for the gate)". At ec7eb2d8 those commands print 254 arms and 162 mutants (receipts/percommit/ec7eb2d8.selftest.log, ec7eb2d8.mutants.log). So a cold reviewer who follows the body as written checks out a superseded commit and does not get the stated result.
- :40, the Description row for the gate, says "254 planted arms and 500 generated cases; 162 enforcement-removal mutants, each killed". At this head the counts are 260 and 174 (receipts/gates/gate_selftest.log, gate_mutants.log). That contradicts :21, :346-347 and :410 in the same body.
- Both texts were current at round 5 (R447-5's receipts/r5/pr_body_snapshot.md:39 and :331). Round 6 edited the body and left them behind.
Impact: the PR's reproduction entry point validates the wrong commit, and the PR states two different self-test sizes for the head. The code, tests and repository docs are not affected (the repository pages state no counts).
Required outcome: the body's state command names the head under review, and the Description row's counts match the head (260 arms, 174 mutants), or the row drops the counts and points to the Status line. A PR-body edit is enough; no commit is needed.
Verification: read the body. Following its command gives a detached HEAD at the head under review, and there `pp_resource_gate.py --selftest` prints "260 arms" and the mutant campaign prints "all 174 mutants fail".
```

```text
[R447] R1 RESIDUE Docs - PR #638 body, "Authoritative references" (receipts/r6/pr_body_snapshot.md:380) - the round-6 assignment is not linked
The bullet links the lane, round-2, round-3, round-4 and round-5 assignments, but not round 6's (5971250916), which this round's table cites.
Exact fix: after "[round-5 assignment](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5970587136)" insert " and [round-6 assignment](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5971250916)".
```

```text
[R447] S1 SUGGESTION Tests - syn/ooc/pp_resource_gate.py:98-100 (NAME, SCOPE_NAME) against syn/ooc/pp_resource_gate_selftest.py:169-170 (WIDE) and :354-355 - the accepted side is pinned for NAME's character groups and length, but not for SCOPE_NAME's groups or either class's first character and lower bound
receipts/r6/probe_r6_delta.log: seven accept-side narrowings pass every run (fuzz500, fuzz5k, --selftest, the round-5 self-test, check-baseline):
- SCOPE_NAME without upper case, without ":", without "-", capped at 127, or needing two characters;
- NAME refusing a leading digit, or a leading hyphen.
"NAME needs two characters" is killed, by a fixture note key "a".
Why not MINOR: R447-5 S1 asked for NAME's groups and length, and those are now pinned (probe_r5_namekill: colon, dot, slash and 64 all DETECTED by --selftest). Each remaining narrowing refuses with exit 2, naming the key, the first time such a key appears, so it fails closed and visibly. The committed baseline's scope names use only `. 0-5 [ ] _ a-z`.
Option: a WIDE-style recorded scope name of 128 characters holding every SCOPE_NAME character, and one-character and digit- or hyphen-led keys, in the existing exit-0 arm. The self-test is at the 1,000-line limit, so extending existing arm values costs no lines.
```

```text
[R447] S2 SUGGESTION Robustness (retained) - R447-5 S3, the name walk's memory growth - not taken, by assignment item 3
receipts/r5/probe_r5_size.log is unchanged in shape. The gate module is byte-identical, and the probe's "head ec7eb2d8" label is fixed in the unchanged script.
- 900 deep x 1,000 wide peaks at 3,273 MiB.
- 900 x 2,000 exits 2 with "NOT COMPARABLE: MemoryError" under the probe's 6 GiB cap, with no traceback.
The PR body lists it as open (:424), which is accurate.
```

```text
[R447] S3 SUGGESTION Tests (retained) - R447-5 S4 (R447-4 S1 and S2) - not taken, by assignment item 3
- receipts/r4/probe_r4_oracle.log: 2a, the shipped oracle, finds 0 failures on "check-baseline problems exit 1". 2b, the stricter oracle, finds 31 in 2,000. The seed-dependent count moved from 42 because the generator changed.
- probe_r4_fuzzkill.log: 20 applied, the self-test kills 20, and the generated cases alone detect 15.
The PR body lists both as open (:423), which is accurate.
```

## Round-6 delta review (my own pass)

### Item 1: list items past the first (R447-5 F1)

- **Fixture and arms.**
  - `IMAGES` (`_selftest.py:46-47`) gives the fixture's manifest three entries (`:121-122`), and the fixture's `runs` note list has three items (`:968-969`).
  - New `check` arm (`:352-353`): `x[1]` in the last manifest entry requires exit 2 naming "... in /2".
  - New malformed baseline (`:437-438`): `x[1]` at item 2 of the `measured` note list requires exit 2 naming "/endpoints/route/measured/2", through `check` and `check-baseline`.
  - Each arm's expected text pins the index, so a walk that reaches some later item but not the right one still fails.
- **Generator.**
  - The `note` operator (`:864-869`) inserts its keyed object at index 0 to 3 of a four-item list.
  - `entry key` (`:959-962`) picks any of the three entries.
- **Shipped mutant.** `names past a list's first item` (`_mutants.py:166-167`) uses my R447-5 replacement. It is killed (`receipts/gates/gate_mutants.log`: 174 of 174, control passes).
- **Required verification, as R447-5 set it.**
  - `receipts/r5/probe_r5_namekill.log`: "walk visits only the first item of a list" gives selftest DETECTED rc 1, failing on the new `/2` manifest arm. fuzz500 detects it (8 failures) and fuzz5k detects it (76).
  - `receipts/r5/probe_r5_names.log`: 72 checks, 0 not as ruled.
  - `receipts/r5/probe_r5_realfuzz.log`: the same mutant fails 44 of 3,000 cases on A's real route (round 5: 26). The control and the other three give 0, with the control digest `889b399a228087be`.
- **My own round-6 mutants** (`probe_r6_delta.py`, 27 mutants; `receipts/r6/probe_r6_delta.log`). The "round-5 self-test" column runs the round-5 self-test against the same mutant.
  - List walk. Five variants: skips the middle, keeps only the first two, skips the first, skips the last, keeps only the last.
    - The head's self-test kills all 5.
    - The round-5 self-test kills only "skips the first" and "skips the last".
    - "Skips the middle items" is killed by the generated cases alone (4 of 500, 33 of 5,000). That is deterministic, because the self-test's seed is fixed.
  - Manifest-only walks. Three variants: the first entry only, all but the last, the first and last only.
    - The head kills all 3: the `/2` arm, and an existing arm reaching `/1`.
    - The round-5 self-test kills only "all but the last".
  - Object walk. Both variants (below the first key only, all but the last key) are killed, as in round 5.
  - Upper length bounds of 129 are killed for both classes.
- **Reach of the generator.** The generated cases alone (fuzz500 or fuzz5k) detect every list-walk and manifest-walk mutant above. So the cases reach later items in both the baseline and the manifest.

### Item 2: suggestions taken (R447-5 S1, S2)

- **S1.**
  - `WIDE` (`_selftest.py:169-170`) is 128 characters and uses every character of `NAME`'s class, with none missing and none extra (checked by import).
  - The exit-0 `check` arm (`:354-355`) puts it in a `measured` note and in a manifest entry. A narrowing of either read refuses it with exit 2.
  - Nine shipped mutants (`_mutants.py:168-176`) are all killed: one per group, plus 127.
  - My R447-5 mutants "NAME drops the colon", "drops the dot", "drops the slash" and "capped at 64" now give selftest DETECTED rc 1 on the `WIDE` key. In round 5 all four passed every run.
  - What is left is S1 above.
- **S2.**
  - The malformed baseline (`:439-441`) puts `{"x": {"record": {"scopes": {"a[1]": 1}}}}` in `description` and requires exit 2 "in /description/x/record/scopes".
  - It kills my R447-5 "scope class matched on the last two keys" (selftest DETECTED) and the shipped `_mutants.py:160-163` pair.
  - My `SCOPES any third key` mutant is killed too, by the `measured`/`scopes` arm.
  - `SCOPES any last key` passes every run, but it is exit-equivalent. `receipts/r6/probe_r6_scopes_last.log`: a bracketed key in a record's `identity` or `figures` exits 2 in the mutant too, through the closed-shape check, because a record holds no other open object.
- **Equivalent survivor.** The one unkilled `probe_r5_namekill` mutant is "scope class below the scope names too", which R447-5 found equivalent.

### The compaction commit `c7cde331`

- `receipts/percommit/SUMMARY.log` runs each commit from a git-archive export.
  - `ec7eb2d8` and `c7cde331` both give 254 arms and 162 of 162 mutants. They give the same 500-case digest `bec87b3c7cbe1125` and the same 20,000-case fixture digest `9c76c8a0b096b5a6`.
  - `80ba13d7` gives 257 arms and 163 mutants. `d5f56313` gives 260 and 174, with 500-case digest `151eb3fc6a0d989c` and 20,000-case digest `0596f2c893188fb0`.
- `receipts/r6/probe_r6_compaction.log`:
  - the docstring's word sequence is equal;
  - only `plant` and `budget_file` differ in AST, which are the folded bytes/text writes;
  - `ROUTE_ARMS` (99) and `OOC_ARMS` (8) evaluate equal;
  - the one new constant is `GROWN_FF`.
- `scripts/check_py_idiom.py` passes (`receipts/gates/py_idiom.log`, 54 of 54). The self-test is exactly 1,000 lines (`receipts/r6/diff_scope.log`).

### New prose

These comments match the code and my probes:
- `_mutants.py:19`, the `NAME` span comment;
- `_selftest.py:46`, the `IMAGES` comment;
- `_selftest.py:169`, the `WIDE` comment ("narrowing any group or the length refuses it", which is true for set narrowings).

No repository doc changed or states a count (searched `AREA_BUDGET.md` and the recipe). The PR body's Round 6 section (`:319-376`) matches my receipts:
- the digests `151eb3fc6a0d989c`, `0596f2c893188fb0`, `257c96d2f917aff4` and `55aadb1548e60ef3`;
- the seed-4474 digests;
- 18 of 20 namekill, and 44 realfuzz failures;
- the oracle's 31, and the classifier's 159 ARM, 4 ESCAPED and 2 CRASH of 165.

F1 and R1 are the body's stale parts outside that section.

### Real data and generative runs

- Real data (`receipts/real/`, my unchanged `real_data.sh`):
  - A route 0 ("route status: complete"), A 1x1 0, A 8x8 0;
  - A 1x1 at 10 ns 2;
  - B route 1 (MATERIAL REGRESSION), B 1x1 0, B 8x8 0.
- Generative runs (`receipts/fuzz/`, my unchanged `run_fuzz.sh`): 90,000 cases, 0 failures, no traceback. Every digest equals the PR body's:

  | Target | Cases | Seed | Failures | Case digest |
  |---|---:|---:|---:|---|
  | fixtures | 20,000 | 234 | 0 | `0596f2c893188fb0` |
  | fixtures | 20,000 | 4474 | 0 | `24aef427207eab7d` |
  | A real route | 20,000 | 234 | 0 | `257c96d2f917aff4` |
  | A real route | 20,000 | 4474 | 0 | `b328b11214a25d56` |
  | A real 1x1 | 5,000 | 234 | 0 | `55aadb1548e60ef3` |
  | A real 8x8 | 5,000 | 4474 | 0 | `d1ca957c50d02c76` |

### My round-1 to round-5 probes, rerun unchanged at this head

| Probe | rc | Result | Reading |
|---|---:|---|---|
| r5 `probe_r5_namekill.py` | 0 | 20 mutants; self-test kills 18 (round 5: 12); generated cases alone 10 (round 5: 8); 1 undetected | The undetected one is the equivalent "scope class below the scope names too". |
| r5 `probe_r5_names.py` | 0 | 72 checks, 0 not as ruled | |
| r5 `probe_r5_realfuzz.sh` | 0 | first-item mutant 44 failures in 3,000; the other three 0 | The other three are now killed by the self-test (namekill). |
| r5 `probe_r5_size.py` | 0 | as round 5 | S2 (retained). |
| r4 `probe_r4_structure.py` | 0 | 51 cases, 0 off expectation | The OK/BAD column is identical to R447-5's log. |
| r4 `probe_r4_resolution.py` | 0 | 0 off expectation | |
| r4 `probe_r4_oracle.py` | 0 | 1a/1b 0; 2a 0; 2b 31; 3 115 | Seed-dependent counts moved with the generator. |
| r4 `probe_r4_fuzzkill.py` | 0 | 23; self-test kills 20; generative alone 15; 3 not unique | As round 5. |
| r1 `check_tables`, `partition_check`, `probe_cli`, `probe_route_status`, `replay_records` | 0 | 49 groups 0 mismatches; partition as round 5; 54 of 54; A/B/10 ns as round 5 | |
| r2 `partition_r2`, `probe_contract`, `probe_policy`, `probe_route_real` A / B | 0 | as round 5; 107 of 107; 15 of 15 / 14 of 15 | The B miss is B's own +625 LUT. |
| r1 `extra_mutants`, r2 `classify_mutants`, r3 `extra_mutants_r3` | 0 | 16 killed, 2 not unique; ARM 159, ESCAPED 4, CRASH 2 of 165, control passes; 13 of 13 | The 2 CRASH are "names hold lower case" and "names hold digits". The self-test kills them before any arm, because the fixture's own `path` and `sha256` keys are refused. The 4 ESCAPED are as round 5. |
| r3 `probe_text`, `probe_bigint` A/B, `probe_gaps`, `armq_count`, `hier_compare` | 0 | every edited case rc 2; gaps 6 of 6; census digests as round 5; 7 reports, 0 differing | `hier_compare` was rerun by hand with absolute paths (`receipts/reruns/NOTE.txt`). |

`run_gates.sh` (my round-3 list without the GNU Make 4.3 docs build; see the limits) gives 30 of 30 rc 0 (`receipts/gates/`). That includes:
- the gate self-test (260 arms and 500 cases, digest `151eb3fc6a0d989c`);
- the campaign (174 of 174; control passes);
- `check-baseline` (3 endpoints);
- the `pp_baseline` self-tests and mutants;
- `ci_scope` and `ci_events`;
- the docs gates, the Python ratchets (`py_idiom` 54 of 54), and `git diff --check 1269cdaf HEAD`.

## Prior findings at this head

(Written after the verdict, findings and ledger above.) I read R446-5 (5971159648) and my own R447-5 (5971246937) for their findings. The R446-6 report, posted on the PR during this round, is a concurrent round and not a prior one, so I did not read it. R446-5's probes are another reviewer's, so I checked its S1 with my own mutants (`probe_r6_r446s1.sh`).

| Prior finding | State at `d5f56313` | Evidence (this round) |
|---|---|---|
| R447-5 F1 (MINOR Tests): no self-test case puts a refused key past a list's first item | **RESOLVED** | `probe_r5_namekill.log`: "walk visits only the first item of a list" gives selftest DETECTED rc 1, failing on the `/2` manifest arm. `probe_r5_names.log`: 72 of 72. Arms at `_selftest.py:352-353` and `:437-438`, the generator at `:864-869` and `:959-962`, and the shipped mutant `_mutants.py:166-167` is killed. `probe_r6_delta.log`: 8 further list and manifest walk variants, all killed. |
| R447-5 S1 (SUGGESTION Tests): the accepted side pinned for brackets only | **Taken**, resolved for NAME | Colon, dot, slash and 64 all give selftest DETECTED (`probe_r5_namekill.log`). Nine shipped mutants are killed. What is left (SCOPE_NAME's groups, first character, lower bound) is new S1, a SUGGESTION. |
| R447-5 S2 (SUGGESTION Tests): the scope path pinned at its last key only | **Taken**, resolved | "scope class matched on the last two keys" gives selftest DETECTED. `SCOPES any third key` is killed. `SCOPES any last key` is exit-equivalent (`probe_r6_scopes_last.log`). |
| R447-5 S3 (SUGGESTION Robustness): the walk's memory | **Retained**, by assignment item 3 | S2 above. Listed open in the PR body (`:424`). |
| R447-5 S4 (R447-4 S1, S2) | **Retained**, by assignment item 3 | S3 above. Listed open in the PR body (`:423`). |
| R446-5 R1 (RESIDUE Docs): the PR body's Round 5 row says "run by `strict()` on every JSON the gate reads" | **Retained** as RESIDUE, not in the round-6 assignment | `receipts/r6/pr_body_snapshot.md:285` still reads so, and `:375-376` says it is not answered. It is wording only. The manager carries it to the residue checklist with R446-5's fix. |
| R446-5 S1 (SUGGESTION Tests): three class-widening name mutants survive the self-test | **Partly resolved**; the rest **retained** as SUGGESTION | `receipts/r6/probe_r6_r446s1.log`. "SCOPES first element wildcarded" is now killed by the new `description`/`record`/`scopes` arm. "Scope name admits a space" and "admits an empty key" still pass `--selftest` and `check-baseline`. The empty-key one is detected by `fuzz(5000, 447)` (3 failures); the space one is not, at that seed. The PR body lists both as open (`:425`). I keep R446-5's SUGGESTION grading. The refusal side of SCOPE_NAME is armed by representative out-of-class keys (a lone surrogate and 129 characters, both killing mutants in `probe_r6_delta.log`). The head refuses both keys with exit 2, and neither occurs among the committed baseline's scope names. |
| Round-1 to round-4 findings of both reviews | Resolved earlier; no regression | My round-1 to round-4 probes, rerun unchanged (table above). |

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-6 assignment items 1-3 against the diff (`receipts/r6/diff_scope.log`: tests only, the gate blob unchanged). Acceptance criteria as ruled (5967852698, 5967924270), unchanged since round 2. The name ruling still enforced: `probe_r5_names.log`, 72 of 72, both JSON files, `check`, `check-baseline` and `record --write`. Real data in `receipts/real/` (A 0/0/0, B 1/0/0, 10 ns 2). The hosted half of criterion 4 executed at this head: `receipts/r6/hosted_ooc_job_steps.tsv`, `yosys-elaboration` step 9 success, head_sha d5f56313. | R447-6 | `d5f56313dc5a5c2716211356f99796664dc843dd` |
| RTL | CLEAN | `receipts/r6/diff_scope.log`: no HDL, XDC, Tcl or workflow file in round 6. Gitlinks equal at base and head (`efeb541a`, `5dce647a`, `631eeb34`; `48ff7a7e` checked out). The tooling converters are unchanged (the gate is byte-identical), and `probe_r4_resolution.log` / `probe_r4_structure.log` are unchanged. | R447-6 | `d5f56313dc5a5c2716211356f99796664dc843dd` |
| Robustness | CLEAN (S2 optional) | `probe_r5_names.log` (72), `probe_r4_structure.log` (51), `probe_r4_resolution.log`, `receipts/fuzz/` (90,000 cases, 0 failures), `probe_r5_size.log` (MemoryError reaches the barrier, rc 2), `probe_r6_scopes_last.log`. Reruns: `r2_probe_contract`, `r3_probe_text`, `r3_probe_bigint` A/B, `r3_probe_gaps`, `r2_probe_route_real` A/B. | R447-6 | `d5f56313dc5a5c2716211356f99796664dc843dd` |
| Tests | CLEAN (S1, S3 optional) | `pp_resource_gate_selftest.py` (260 arms, 500 cases; `:46-47`, `:121-122`, `:169-170`, `:352-355`, `:437-441`, `:864-869`, `:959-962`, `:968-969`). `pp_resource_gate_mutants.py` (`:19-20`, `:160-176`; 174 killed). `probe_r5_namekill.log` (F1 mutant killed; 18 of 20, 1 equivalent). `probe_r6_delta.log` (27 mutants: the head kills 19, the round-5 self-test 13; 8 pass every run, of which 1 is exit-equivalent and 7 are S1's fail-closed narrowings). `probe_r5_realfuzz.log`, `receipts/percommit/` (each commit), `probe_r6_compaction.log`, `probe_r4_fuzzkill.log`, `probe_r4_oracle.log`. Reruns: `r1_extra_mutants`, `r2_classify_mutants`, `r3_extra_mutants_r3`. | R447-6 | `d5f56313dc5a5c2716211356f99796664dc843dd` |
| Docs | UNCLEAN (F1 open; R1 residue) | PR body snapshot (`receipts/r6/pr_body_snapshot.md`): Status `:21`, Description row `:40`, Round 6 `:319-376`, references `:380`, state `:389-393`, validate `:399-410`, limitations `:412-428`. New comments at `_mutants.py:19`, `_selftest.py:46`, `:169`. `AREA_BUDGET.md:189-208` and recipe `:462-477`, unchanged and still true, with no counts stated. The body's round-6 figures were checked against `receipts/`. | R447-6 | `d5f56313dc5a5c2716211356f99796664dc843dd` |

## Real limits

- No Vivado run. Every real-data check reads the existing A and B run directories. Physical calibration was NOT RUN, and field skips are not hardware proof.
- No RTL is in the diff, so the scoped Verilator was not used.
- The GNU Make 4.3 docs build (`make -C gptp-processor docs`) was not run. No reviewer-owned Make 4.3 is on this host. Round 6 touches no doc, Makefile or `gptp-processor` file. The other docs gates ran and passed.
- Signals, argparse and a failure of standard output itself stay out of scope, as in rounds 4 and 5. `probe_r5_size.py` runs under a 6 GiB address-space cap.
- Hosted snapshot (`receipts/r6/hosted_check_runs.tsv`, read at `receipts/r6/hosted_check_runs.read_at`):
  - completed successfully: `rtl-fast`, `yosys-elaboration` (step 9 ran the gate self-test, mutants and `check-baseline` at d5f56313), `verilator-lint`, `elaborate`, `bdd-conformance`, `changes`, `full-ci-gate`, `docs-check-no-git`, `wire-accountability`, Yosys shards 0-3, and Verilator shards 0 and 3;
  - in progress: `docs-check`, and Verilator shards 1, 2 and 4;
  - `Physical gPTP` was skipped, which is not evidence.

  The manager owns hosted and local-replica acceptance.
- Receipts replace host paths with `$VALIDATION_STORAGE` (the A and B measurement root), `$CHECKOUT` (the review clone) and `$PACKET` (this packet). No other byte was changed. Probe scripts take every path as an argument.
- After every probe the clone was verified exact (`receipts/verify_tree.log`):
  - HEAD, tree and index tree equal the head;
  - worktree bytes and modes equal HEAD, and `ls-files -s` equals `ls-tree -r HEAD`;
  - nothing is untracked or ignored, after removing the two ignored `__pycache__` directories (only `.pyc` files) that the gate run wrote (`receipts/verify_tree.NOTE.txt`, `verify_tree_before_pycache_removal.log`);
  - the submodule worktrees are at their gitlinks.

## Pending manager duties

- Route F1 to the executor. It needs a PR-body edit only: the state command at the head, and the Description row's counts. Its verification is above. Carry R1 to the residue checklist.
- Hosted and local-replica acceptance at the exact head, including the contexts still in progress.
- The merge-turn candidate on live dev `546437243e87eb5a78783a9e3cd5d1badcc3423e`, distinct from this source review (source base `1269cdaf`).
- The merge-bank Vivado `check` (manager ruling).
- Publishing this packet: `REPORT.md` and the files listed in `MANIFEST.sha256`.

R447-6 FINISHED
