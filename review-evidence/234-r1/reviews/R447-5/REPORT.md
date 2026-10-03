[R447] NEGATIVE - exact head ec7eb2d8ff81700842f4e3a35b79879c8c3838e5

# R447-5 external review: issue #234 / PR #638, round 5

- Head `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5`, tree `f541830baddcc43387291b42719e7344045ca3f0`, source base dev `1269cdafb4bb964c757baae0f0c5a932d43f540b`.
- Round 5 is `79e53831..ec7eb2d8`: two one-line commits with no trailers, 5 files (the gate, its self-test and mutants, `AREA_BUDGET.md`, the recipe; +115 / -64). There is no HDL, constraint, Tcl, workflow or baseline-JSON change, and the gitlinks equal the base (`receipts/r5/diff_scope.log`).
- **Verdict NEGATIVE, on one MINOR finding (F1, `Tests`).** The ruling is implemented correctly. Every key of the baseline and the image manifest, open objects included, is held to the name class, and only a record's sub-block scope names may also hold `[` and `]` (`probe_r5_names.py`: 72 of 72 checks as the ruling requires). The gap is in the tests: no self-test arm or generated case puts a refused key past the first item of a list. A walk that checks only the first item of each list therefore survives the self-test, the shipped mutant campaign and `check-baseline`. Five of the six entries in A's real image manifest are past the first item.
- Four SUGGESTIONs (S1 to S4) are recorded, and R447-4 S1 and S2 stay open as suggestions, as the assignment ruled. No RESIDUE item is open.
- Conformance, RTL, Robustness and Docs are covered clean at this head. Tests is not clean because F1 is open.
- R447-4's three RESIDUE items are taken exactly. The docstring's exit contract is scoped to `check`, `record` and `check-baseline`.
- My verdict, findings and ledger came from my own pass over the round-5 diff and my own probes. The table of prior findings was written afterwards.

## Inputs, in order

1. AGENTS.md and CONTRIBUTING.md (as loaded), and the docs map.
2. Issue #234's body and comments:
   - the lane assignment (5966260488);
   - the rulings (5967852698) and the owner decision (5967924270);
   - the round-4 assignment (5969446300);
   - the **round-5 assignment (5970587136)**;
   - round-5 REVIEW READY (5970940747).
3. `git diff 79e53831..ec7eb2d8` in full. Also `1269cdaf..ec7eb2d8` by name, the commit messages, and the PR body (Description row, Round 4 and Round 5 sections, limitations).
4. Public evidence:
   - `43ad8362:review-evidence/234-r1/author/evidence` (the round-1 records), which my unchanged round-1 and round-2 probes use;
   - the A and B measurement directories, read only.
5. Exact-head hosted check runs, recorded as a snapshot only.
6. My own R447-4 report and probes, to rerun them unchanged.
7. After my verdict, findings and ledger were written: R446-4's public findings, to resolve them.

## Findings

```text
[R447] F1 MINOR Tests - syn/ooc/pp_resource_gate_selftest.py:126, :276-278, :435-438, :865-869, :959-962, :968 (arms, fixtures, generator) against syn/ooc/pp_resource_gate.py:435-436 (names() list walk) - no self-test case puts a refused key past the first item of a list, so a walk that checks only the first item survives every shipped gate
Authority: round-5 assignment item 1 and AREA_BUDGET.md:204 ("That holds for every key of the baseline, the keys inside its notes included, and of the measurement's image manifest, the keys of its entries included"); AGENTS.md section 6, Tests ("Each new test can fail for the defect it claims to detect"; "Positive, negative, and boundary behavior is covered"). R447-4 used this bar for SUGGESTION versus MINOR: a generator gap is a SUGGESTION only while no refusal is untested. The round-3 findings of the same kind (R446-3 F3, R447-3 F3: claimed refusals with no arm) were MINOR.
Evidence:
- The fixture manifest has one entry (_selftest.py:126). The manifest arms edit that entry (:276-278). The note arm puts its bracketed key in a one-item list (:435). The note operator writes `[value]`, a one-item list (:869). The entry-key operator picks one of the fixture's entries, and there is only one (:960-961). The fixture's only note list, "runs", holds one item (:968).
- So no arm and no generated self-test case reaches a list item at index 1 or later.
- receipts/r5/probe_r5_namekill.log, my mutant "reject: walk visits only the first item of a list". It replaces the list push at pp_resource_gate.py:436 with the first item only. It passes all four runs: fuzz500, fuzz5k (5,000 cases, seed 447), --selftest, and check-baseline on the committed baseline. The shipped campaign judges each mutant by --selftest, so the campaign misses it too.
- receipts/r5/probe_r5_realfuzz.log: only a manual --fuzz on A's real route, whose manifest has 6 entries, detects it (26 failures in 3,000 cases, all "baseline_images.json: entry key, broken True" exiting 0). No repository gate runs that mode.
- The head itself is correct. probe_r5_names.log refuses a bracketed key in the last real manifest entry ("in /5") and deep in a note list ("in /description/0/0/a/0"), each with exit 2.
Impact: the refusal of a key outside the class in any manifest entry but the first, or any later item of a note list, is not pinned by any gate. A walk regression that skips later items would leave keys in 5 of the 6 real manifest entries unchecked, and every gate would stay green.
Required outcome: a self-test arm, or a generated self-test case, puts a key outside the class into a list item past the first, in the image manifest and in a note, and requires exit 2. The mutant "walk visits only the first item of a list" (or the shipped equivalent) is killed by --selftest.
Verification: rerun probe_r5_namekill.py. That mutant's selftest run must exit non-zero. probe_r5_names.py must stay 72 of 72.
```

```text
[R447] S1 SUGGESTION Tests - syn/ooc/pp_resource_gate.py:98 (NAME) against the self-test arms - the accepted side of the name class is pinned for brackets only
receipts/r5/probe_r5_namekill.log: four narrowing mutants pass all four runs:
- NAME without ":";
- NAME without ".";
- NAME without "/";
- NAME capped at 64.
No arm puts one of those characters, or a key of 65 to 128 characters, into a NAME-class key. The committed baseline holds no ":" key at all. The generative oracle cannot see a false refusal, because a shape-keeping case may exit 0, 1 or 2 (receipts/r5/probe_r5_realfuzz.log: "NAME drops the colon" changes the case digest but gives 0 failures).
Why not MINOR: a narrowing refuses (exit 2, fail closed, the key named) the first time such a key appears, so it is visible and nothing passes silently.
Option: one exit-0 arm with a 128-character NAME key that uses every character of the class, in a note and in a manifest entry.
```

```text
[R447] S2 SUGGESTION Tests - syn/ooc/pp_resource_gate_mutants.py:156 ("scope path matched in full") against syn/ooc/pp_resource_gate.py:429 - the scope path is pinned at its last key only
The shipped mutant replaces the full-path match with a last-key match. The measured/scopes arm (_selftest.py:437) kills it. A match on the last two keys, `path[-2:] == scopes[-2:]`, passes all four runs (receipts/r5/probe_r5_namekill.log, "reject: scope class matched on the last two keys"). It would accept brackets in a note or manifest object reached through .../record/scopes. The head refuses that (probe_r5_names.log: "in /description/endpoints/x/record/scopes" and "in /0/endpoints/e/record/scopes", exit 2).
Why not MINOR: only a note or manifest shaped like a record reaches it, and the gate never reads notes as data.
Option: one exit-2 arm with a bracketed key under a record-shaped object inside the description note.
```

```text
[R447] S3 SUGGESTION Robustness - syn/ooc/pp_resource_gate.py:425-436 (names()) - the walk's memory grows as width x depth squared
names() pushes every child with its full path tuple, so a list W items wide at depth d keeps about W x d tuples of length d alive.
receipts/r5/probe_r5_size.log runs check-baseline on a copy of the committed baseline whose description note is nested 900 deep, 1,000 wide (2.72 MB):
- the head peaks at 3,273 MiB in 5.1 s;
- the round-4 gate peaks at 33 MiB in 0.75 s.
At 900 x 2,000 (5.42 MB), the head reaches the probe's 6 GiB address-space cap and exits 2 with "NOT COMPARABLE: MemoryError". The round-4 gate passes that file at 42 MiB.
The exit contract holds under a cap: MemoryError reaches the barrier. Without a cap, an out-of-memory kill would be a signal, which round 4 put out of scope.
Why not MINOR: the gate reads a reviewed, committed baseline (26 KB) and a recipe-written manifest. Only a hand-made multi-megabyte nested note reaches this.
Option: push each container once with its path and iterate its children in place, or hold one parent link per frame.
```

```text
[R447] S4 SUGGESTION Tests (retained) - R447-4 S1 and S2 - not taken, by assignment item 3
Both are listed as open in the PR body's limitations, which is accurate.
- S1: receipts/r4/probe_r4_oracle.log 2a/2b. The shipped oracle misses "check-baseline problems exit 1" (0 failures in 2,000). The stricter oracle detects it (42 failures).
- S2: receipts/r4/probe_r4_fuzzkill.log. "budget cell via float()" is still detected only by the arms. "manifest via json.loads" is now detected by the generated cases alone, as the PR body says.
```

## Round-5 delta review (my own pass)

### Item 1: the name class, as ruled

- **Code.**
  - `names()` (`pp_resource_gate.py:418-436`) walks a JSON tree with its own stack. Each object's keys are checked against `NAME`, or against `SCOPE_NAME` where the path equals `SCOPES = ("endpoints", None, "record", "scopes")` (`:102`, `:429`), before anything below it is pushed. List items are pushed with their index.
  - `strict()` (`:439-447`) runs `named()` (repeats only) through `json.loads`, then `names()`.
  - The gate's commands read two JSON files, and both go through `strict()`:
    - the baseline, via `load()` with `SCOPES` (`:503`), for `check`, `check-baseline` and the text `record --write` would write (`:728`);
    - the image manifest, in `inputs()` with no scope path (`:203`), for `check` and `record`.
  - The only other `json.loads` calls are in the test drivers: `fuzz()` reading its seed baseline (`:632`), and the self-test's entry-key operator. Every generated case's baseline still goes through `load()`.
  - The per-site endpoint-name and policy-figure checks were removed. The walk covers both (`probe_r5_names.log`: "in /endpoints", "in /endpoints/route-1x1/ceiling").
- **Probe** `probe_r5_names.py`: real processes, strict ASCII stdout, on A's real route and 1x1 and copies of the committed baseline. **72 checks, 0 not as ruled**, no traceback, all output ASCII. Each refusal names its key and place.
  - Exit 2:
    - a bracketed key in `description`, `schema` and `measured`;
    - `measured/scopes`, and a whole record-shaped tree inside `description`;
    - deep in a note list, plus `]`, an empty key, 129 characters, non-ASCII, a lone surrogate and a space;
    - a bracketed record, figure, identity, ceiling, endpoint or top-level key;
    - a bracketed count key one level below the scope names;
    - a scope name with a space or a brace.
  - Exit 0:
    - named keys in every note, and a 128-character note key;
    - a bracketed scope name on `route-1x1` and on `ooc-1x1`.
  - Manifest, through `check` and `record`:
    - exit 2 for a bracketed key in the first and the last of the 6 real entries ("in /5"), inside an entry's object value, at a record-shaped path in an entry, 129 characters, non-ASCII, an empty key, a repeated key, an object manifest, and the standalone measurement;
    - exit 0 for another named key and for 128 characters.
  - `record --write` onto a baseline whose note holds a bracketed key gives exit 2 and leaves the write target unchanged.
- **Mutants on both sides.**
  - Shipped: the six new or re-pointed mutants all fail in `receipts/gates/gate_mutants.log` (162 of 162; control passes): `every key named`, `baseline scope names`, `scope names at their path only`, `scope path matched in full`, `names inside lists`, `names below the top level`, plus `baseline key names` and `image manifest strict`.
  - My own 20 in `probe_r5_namekill.py`:
    - the self-test kills 12, and the generated cases alone detect 8;
    - the real `check-baseline` additionally detects the three accept-side scope mutants;
    - 7 are undetected by every run. Two are F1 and S2, four are S1, and "scope class below the scope names too" is equivalent: the shape check refuses any count key outside `SCOPE` with exit 2.
- **The generator reaches keys inside notes and manifest entries.** In `receipts/gates/gate_selftest.log` the 500 self-test cases hold 10 `note` and 7 `entry key` cases (the PR body says 10 / 7). In my 20,000-case runs: fixtures 547 / 275, A route 568 / 273. The generated cases alone detect "notes skipped by the walk", "brackets allowed in notes", "manifest read strict but without the name walk", "brackets allowed in every manifest key" and "manifest's first entry takes scope names" (fuzz500 and fuzz5k). The limit is F1: every such list has one item in the fixtures.

### Item 2: wording, taken exactly

- R447-4 R1 (`pp_resource_gate.py:22-31`):
  - "For check, record and check-baseline, main() holds one barrier around everything after argument parsing:";
  - "every line those commands print is printable ASCII";
  - "--selftest and --fuzz are test drivers outside the barrier: a non-zero exit there means the test failed or could not start."
  
  The texts are exact. The last one follows the ASCII sentence, as asked.
- R446-4 S1: "Exit status of check, record and check-baseline:" (`:22`). My unchanged round-4 structure probe gives the same 51 results, and its three test-mode tracebacks now sit outside the scoped claim.
- R447-4 R2: `AREA_BUDGET.md:208` and the recipe at `:477` are exact.
- R447-4 R3: the PR body's Description row is exact ("one of two converters, whole() (1 to 15 ASCII digits) or real() (a finite float)").
- The new prose matches the code and my probes:
  - `AREA_BUDGET.md:203-205`;
  - the recipe at `:471-472`;
  - the gate docstring at `:36-40`;
  - the PR body's Round 5 section and limitations.

### Real data and generative runs

- Real data, from `receipts/real/` (my unchanged `real_data.sh`):
  - A route 0 ("route status: complete"), A 1x1 0, A 8x8 0;
  - A 1x1 at 10 ns 2;
  - B route 1 (LUT 50,128 to 50,753, +625 over 500), B 1x1 0, B 8x8 0.
- Generative runs, from `receipts/fuzz/` (my unchanged `run_fuzz.sh`): 90,000 cases, 0 failures, no traceback. Every case digest equals the PR body's:

  | Target | Cases | Seed | Failures | Case digest |
  |---|---:|---:|---:|---|
  | fixtures | 20,000 | 234 | 0 | `9c76c8a0b096b5a6` |
  | fixtures | 20,000 | 4474 | 0 | `a11a378a10ba0a90` |
  | A real route | 20,000 | 234 | 0 | `5355bf60a587d04c` |
  | A real route | 20,000 | 4474 | 0 | `0137ba98eeae4cca` |
  | A real 1x1 | 5,000 | 234 | 0 | `734d9bfa6aabaa08` |
  | A real 8x8 | 5,000 | 4474 | 0 | `5f669519439856cf` |

### My round-1 to round-4 probes, rerun unchanged at this head

The copies are under `prior/`, and `prior/ORIGINALS.txt` binds each to its R447-4 packet copy (29 of 29 equal).

| Probe | rc | Result | Reading |
|---|---:|---|---|
| r4 `probe_r4_structure.py` | 0 | 51 cases, 0 off expectation | The OK/BAD, rc, traceback and ASCII columns are identical to R447-4's log. The three tracebacks are the `--fuzz` test-mode cases, now outside the scoped docstring claim. |
| r4 `probe_r4_resolution.py` | 0 | 11 cases, 0 off expectation | |
| r4 `probe_r4_oracle.py` | 0 | 1a/1b 0 failures; 2a 0; 2b 42; 3 117 | As round 4: S1's stricter oracle is sound. |
| r4 `probe_r4_fuzzkill.py` | 0 | 20 applied, self-test kills 20; generative alone 15; 3 not unique | The three not unique are "key name class removed", "brackets allowed in endpoint names" and "policy figure names unchecked". Round 5 removed their spans, and `probe_r5_namekill.py` plus the shipped name mutants cover their rules. "manifest via json.loads" is now detected by the cases alone. |
| r4 `run_fuzz.sh` | 0 | 90,000 cases, 0 failures | Table above. |
| r1 `check_tables.py` | 0 | 49 groups, 0 mismatches | |
| r1 `partition_check.py`, r2 `partition_r2.py` | 0 | +79 / +93; `u_pp` -23 / +107 | As round 4. |
| r1 `probe_cli.py` | 0 | 54 of 54 | It differs from round 4 only in reason text truncated at a longer scratch path. |
| r1 `probe_route_status.py` | 0 | clean 2; 37 unrouted 2 | As round 4. |
| r1 `replay_records.py` | 0 | A 0/0/0; B 1/0/0; 10 ns 2 | |
| r1 `extra_mutants.py` | 0 | 16 killed, 0 survived, 2 not unique | As round 4. |
| r2 `classify_mutants.py` | 0 | 149 ARM, 4 ESCAPED, 0 survived, control passes | As round 4. |
| r2 `probe_contract.py`, `probe_policy.py` | 0 | every edited case rc 2 in both columns; 107 of 107 | Identical to round 4 with paths stripped. |
| r2 `probe_route_real.py` A / B | 0 / 0 | 15 of 15 / 14 of 15 | The B miss is B's own +625 LUT. |
| r3 `extra_mutants_r3.py` | 0 | 13 of 13 killed | |
| r3 `probe_text.py`, `probe_bigint.py` A/B, `probe_gaps.py` | 0 | every edited case rc 2, no traceback; gaps 6 of 6 | Differences from round 4: truncation at the longer path, and the budget page's larger byte offset. |
| r3 `hier_compare.py` | 0 | 7 reports, 0 differing | Rerun by hand with absolute paths (`receipts/reruns/NOTE.txt`). |
| r3 `armq_count.py` | 0 | A 1,153, B 1,260, A-8x8 1,318 | Digests as round 4. |
| r3 `run_gates.sh` | - | 31 of 31 rc 0 | GNU Make 4.3 first on PATH (`receipts/gates/make_version.txt`). `ooc_tcl_selftest` was rerun in the foreground (58 arms, rc 0) after the detached driver ended (`receipts/gates/NOTE.txt`). |

The gates include:
- the gate self-test (254 arms and 500 cases, digest `bec87b3c7cbe1125`);
- the shipped mutant campaign (162 of 162; control passes);
- `check-baseline` (3 endpoints);
- the `pp_baseline` self-tests and mutants;
- `ci_scope` and `ci_events`;
- the docs set, with `make -C gptp-processor docs` under Make 4.3;
- the Python ratchets;
- `git diff --check 1269cdaf HEAD`.

## Prior findings at this head

(Written after the verdict, findings and ledger above.) I read R446-4 (5970466762) and my own R447-4 (5970584109) for their findings. I did not read the R446-5 report that appeared on the PR during this round. R446-4's probes are another reviewer's, so I checked its F1 with my own `probe_r5_names.py`.

| Prior finding | State at `ec7eb2d8` | Evidence (this round) |
|---|---|---|
| R446-4 F1 (MINOR Conformance, Robustness, Tests, Docs): a bracketed key outside a sub-block scope name is accepted | **RESOLVED** as ruling (a); no lens it named regresses | `probe_r5_names.log`: bracketed keys in `description`, `schema`, `measured`, `measured/scopes` and a manifest entry, plus R446-4's other-class key (a space), all rc 2 named, through `check` and `check-baseline` (manifest through `check` and `record`). Bracketed scope names rc 0. Arms at `_selftest.py:276-278`, `:357`, `:370`, `:435-438`; six shipped mutants killed. The docs (`AREA_BUDGET.md:203-205`, recipe `:470-472`, docstring `:36-40`, PR body) state the class as implemented. F1 above is a new and narrower test gap in the walk's list coverage, not a retention of this finding: the refusal R446-4 asked for is enforced and now has arms. |
| R446-4 R1 (RESIDUE Docs): "only missing arguments exit 2 through argparse" | **RESOLVED**, exact | `receipts/r5/pr_body_snapshot.md`, Round 4 paragraph: "only a command line that argparse rejects (a missing, unknown or ill-typed argument) exits 2 through argparse, before the barrier". The old text is absent. |
| R446-4 S1 (SUGGESTION Docs, Robustness): scope the docstring's exit-status sentence | **Taken** | `pp_resource_gate.py:22`: "Exit status of check, record and check-baseline:". |
| R447-4 R1 (RESIDUE Docs): the barrier sentence scoped to all of main() | **RESOLVED**, exact | `pp_resource_gate.py:24-31`. My unchanged `probe_r4_structure.py` gives the same 51 results; its three `--fuzz` tracebacks are now inside the stated test-driver exception. |
| R447-4 R2 (RESIDUE Docs): "holds every case to this contract" | **RESOLVED**, exact | `AREA_BUDGET.md:208`, recipe `:477`. |
| R447-4 R3 (RESIDUE Docs): "two bounded converters" in the PR body | **RESOLVED**, exact | Description row in `receipts/r5/pr_body_snapshot.md`. The old text is absent. |
| R447-4 S1, S2 (SUGGESTION Tests) | **Retained** as open suggestions, by assignment item 3 | S4 above. They are listed in the PR body's limitations. |
| Round-1 to round-3 findings of both reviews | Resolved earlier; no regression | My round-1 to round-3 probes, rerun unchanged (table above). |

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-5 assignment item 1 against `pp_resource_gate.py:97-102`, `:203`, `:408-447`, `:503`, `:728`; `probe_r5_names.log` (72 of 72 as ruled, both commands, both JSON files, `record --write`). Acceptance criteria as ruled (5967852698, 5967924270), unchanged by round 5; real data `receipts/real/` (A 0/0/0, B 1/0/0, 10 ns 2); hosted half of criterion 4 executed at this head (`receipts/r5/hosted_ooc_step.tsv`: `yosys-elaboration` step 9 success). | R447-5 | `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5` |
| RTL | CLEAN | `receipts/r5/diff_scope.log`: no HDL, XDC, Tcl or workflow file in round 5, gitlinks equal at base and head (`631eeb34`, `5dce647a`, `efeb541a`, `48ff7a7e`). Tooling width and overflow contract: `whole()` / `real()` unchanged; `probe_r4_resolution.log` and `probe_r4_structure.log` converter sites unchanged. Resource effect of the new walk measured (`probe_r5_size.log`; S3). | R447-5 | `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5` |
| Robustness | CLEAN (S3 optional) | `probe_r5_names.log` (72), `probe_r4_structure.log` (51), `probe_r4_resolution.log` (11), `receipts/fuzz/` (90,000 cases, 0 failures), `probe_r5_size.log` (MemoryError reaches the barrier: rc 2), reruns `r2_probe_contract`, `r3_probe_text`, `r3_probe_bigint` A/B, `r3_probe_gaps`, `r2_probe_route_real` A/B. | R447-5 | `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5` |
| Tests | UNCLEAN (F1 open; S1, S2, S4 optional) | `pp_resource_gate_selftest.py` (254 arms, 500 cases; `:126`, `:276-278`, `:435-438`, `:865-869`, `:959-962`, `:968`), `pp_resource_gate_mutants.py` (162 killed), `probe_r5_namekill.log` (20 reviewer mutants, 7 undetected), `probe_r5_realfuzz.log`, `probe_r4_fuzzkill.log`, `probe_r4_oracle.log`, reruns `r1_extra_mutants`, `r2_classify_mutants`, `r3_extra_mutants_r3`. | R447-5 | `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5` |
| Docs | CLEAN | Gate docstring `:22-43`, `NAME`/`SCOPES` comments `:97-102`, `names()`/`strict()` docstrings; `AREA_BUDGET.md:189-208`; recipe `:462-477`; PR body Description row, Round 5 section and limitations; R447-4 R1, R2, R3 and R446-4 S1 exact; `r1_check_tables` (49 groups, 0 mismatches); partition reruns equal to the prose; self-test and fuzz tallies and case digests equal to the PR body. | R447-5 | `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5` |

## Real limits

- No Vivado run. Every real-data check reads the existing A and B run directories. Physical calibration was NOT RUN, and field skips are not hardware proof.
- No RTL is in the diff, so the scoped Verilator was not used.
- Signals, argparse and a failure of standard output itself are out of scope, as in round 4. `probe_r5_size.py` runs every gate process under a 6 GiB address-space cap. The uncapped behaviour on a host without enough memory was not exercised.
- Hosted snapshot (`receipts/r5/hosted_check_runs.tsv`, read at `receipts/r5/hosted_check_runs.read_at`):
  - completed successfully: `rtl-fast`, `yosys-elaboration` (whose step 9 ran the gate self-test, mutants and `check-baseline`), `verilator-lint`, `elaborate`, `bdd-conformance`, `changes`, `full-ci-gate`, `docs-check-no-git`, `wire-accountability`, Yosys shards 0-3, and Verilator shards 0 and 3;
  - in progress: `docs-check`, and Verilator shards 1, 2 and 4;
  - `Physical gPTP` was skipped, which is not evidence.
  
  The manager owns hosted and local-replica acceptance.
- Receipts replace host paths with `$VALIDATION_STORAGE` (the A and B measurement root), `$CHECKOUT` (the review clone) and `$PACKET` (this packet). No other byte was changed. Probe scripts take every path as an argument.
- After every probe the clone was verified exact (`receipts/verify_tree.log`):
  - HEAD, tree and index tree equal the head;
  - worktree bytes and modes equal HEAD, and `ls-files -s` equals `ls-tree -r HEAD`;
  - nothing is untracked or ignored, after removing the ignored `__pycache__` directories the gates wrote (`receipts/verify_tree.NOTE.txt`);
  - the submodule worktrees are at their gitlinks.

## Pending manager duties

- Route F1 to the executor. Its required outcome and verification are above, and `probe_r5_namekill.py` and `probe_r5_names.py` are the checks.
- Hosted and local-replica acceptance at the exact head, including the contexts still in progress.
- The merge-turn candidate on live dev `bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352`, distinct from this source review (source base `1269cdaf`).
- The merge-bank Vivado `check` (manager ruling).
- Publishing this packet: `REPORT.md` and the files listed in `MANIFEST.sha256`.

R447-5 FINISHED
