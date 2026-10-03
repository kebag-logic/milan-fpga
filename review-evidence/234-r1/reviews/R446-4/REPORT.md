[R446] NEGATIVE - exact head 79e53831a4f623a594f22765be1d05dffeb696a7

# R446-4 internal review: issue #234 / PR #638, round 4

- Head `79e53831a4f623a594f22765be1d05dffeb696a7`, tree `641203eed0fe9d67dfc01694a31dacd52b62638a`, source base dev `1269cdafb4bb964c757baae0f0c5a932d43f540b`. The round-4 delta is `b5894838..79e53831`: five one-line commits without trailers, 6 files (the gate, its self-test and mutants, `pp_baseline_rank.py`, `AREA_BUDGET.md`, the recipe) (`receipts/r4-commits.txt`, `receipts/diff-name-status.txt`).
- Rebuilt from public state, in this order:
  - AGENTS.md and CONTRIBUTING.md, and the docs map;
  - the issue body, the lane assignment (5966260488), the rulings (5967852698), the owner decision (5967924270), the round-2, round-3 and **round-4 (5969446300)** assignments, and REVIEW READY rounds 1 to 4 (round 4: 5970259375);
  - the round-4 delta in full, and the whole gate at the head;
  - the public evidence branch: `43ad8362:review-evidence/234-r1` (round-1 records and rankings) and the author round-4 packet at `6c098ef1:review-evidence/234-r1/author-r4` (fuzz receipts, kill matrix, `armq-census.tsv`);
  - the live PR body (Round 4 section); exact-head hosted check runs.
- The A and B measurement directories were read only, as the gate's inputs, through symlink mirrors with one planted file.
- This verdict and ledger were written before I read the other reviewer's round-3 or round-4 report. I read the round-3 findings (my R446-3, 5969323709, and R447-3, 5969442442) only after my own pass over the round-4 diff; the resolution table is at the end. I took my earlier packets for their probe scripts only, and ran those unchanged.
- I apply the rulings and the owner decision as given and do not count them as defects.

Verdict: **NEGATIVE** on one MINOR finding.

- **F1:** the docs state a narrower strict-JSON name class than the code applies. The code accepts brackets in every key except an endpoint or policy-figure name, not only in sub-block scope names. So a bracketed key inside a note exits 0 where the documented contract says 2, and no arm covers it.

Everything else in round 4 holds:

- the barrier;
- ASCII-safe output;
- the two converters at every conversion site;
- the generative test and its 20,000-case runs, which reproduce the author's case digests;
- the verdicts on real data;
- every round-3 finding of both reviewers;
- all my earlier probes;
- the touched gates.

## Findings

```text
[R446] F1 MINOR Conformance, Robustness, Tests, Docs - syn/ooc/pp_resource_gate.py:94, :404 (named() applies SCOPE_NAME to every key), :33-35 (docstring); docs/design/AREA_BUDGET.md:203-204; docs/testing/PP_SHADOW_BASELINE_RECIPE.md:470; PR body "The contract as it now holds" and REVIEW READY round 4 item 2 - a bracketed key outside a sub-block scope name is accepted, against the stated name class
```

- **Authority:**
  - Round-4 assignment item 2: "Every endpoint, field, scope and figure name in the baseline matches `[A-Za-z0-9_.:/-]{1,128}`. Anything else exits 2, named."
  - The author disclosed one deviation, that sub-block scope names may hold `[` and `]`. This review was asked to verify the class with that exception only.
  - The docs state it that way:
    - `AREA_BUDGET.md:203-204`: "every key is 1 to 128 of `A-Z a-z 0-9 _ . : / -`. A sub-block scope name may also hold a generate index's brackets."
    - The gate docstring says "every key a name of NAME (a scope name may also hold ...)".
    - The PR body says "scope names alone may also hold `[` and `]`; endpoint, field and figure names are held to the class exactly".
    - REVIEW READY round 4 says the image manifest is read with "every key 1 to 128 of `A-Za-z0-9_.:/-`".
- **Evidence:**
  - `named()` checks every key of every object against `SCOPE_NAME`, the bracket class (`:404`).
  - `NAME` is re-applied only to endpoint names (`load()`) and to policy-figure names (`shape_problems()`).
  - The closed objects (record, identity, figures, scope counts) are held by exact key sets.
  - So the gate accepts a bracketed key wherever an object is open: inside a note (`description`, `measured`) and in an image-manifest entry.
  - `receipts/r4-probes/probe-r4-structure.log` runs each case through the CLI against a mirror of A's real route:
    - `"description": {"x[1]": 1}`: **rc 0, RESULT: PASS** (want 2);
    - `"measured": {"x[1]": 1}`: **rc 0** (want 2);
    - a manifest entry with an extra `"x[1]"` key: rc 0;
    - the same places with a key outside both classes (`"x y"`): rc 2, as stated;
    - the controls behave as stated: a scope name `u_pp/u_srp[3]` gives 0; a bracketed endpoint name, policy figure or scope-count key gives 2.
  - No arm or generated case covers this. The arms plant brackets only in an endpoint name and a policy figure (`_selftest.py:434-437`). The generator's `bracket name` operator renames keys that exist, and the fixtures' notes are strings. My kill probe confirms it: a mutant holding every key to `NAME` is caught only by the arms, never by the generated cases (`probe-r4-generative.log`).
- **Impact:**
  - No verdict changes: the gate never reads note contents or extra manifest keys.
  - For such a file the gate returns 0, not the documented 2. The claimed refusal is neither enforced nor tested.
  - The exception in force is wider than the one the author disclosed and the manager accepted.
- **Required outcome:** one of the following.
  - (a) A bracketed key anywhere other than a sub-block scope name exits 2 with a named reason. That covers the baseline, notes included, and the image manifest. An arm covers each side and a mutant is killed.
  - (b) A recorded manager ruling extends the exception to keys the gate never reads. The docstring, `AREA_BUDGET.md:203-204`, recipe `:470` and the PR body then state the class as implemented, with an arm pinning it.
- **Verification:** `probe_r4_structure.py <checkout> <A route dir> <scratch>`. Its cases for a bracketed note key and a manifest key give the rc the stated contract implies, and the other 29 cases do not change.

```text
[R446] R1 RESIDUE Docs - PR #638 body, paragraph "The contract as it now holds" - "only missing arguments exit 2 through argparse"
```

- argparse also rejects an unknown command and a non-integer `--fuzz` or `--seed`, each with exit 2 before the barrier.
- Exact fix: replace "only missing arguments exit 2 through argparse" with "only a command line that argparse rejects (a missing, unknown or ill-typed argument) exits 2 through argparse, before the barrier".

```text
[R446] S1 SUGGESTION Docs, Robustness - syn/ooc/pp_resource_gate.py:22-27 (docstring "Exit status"), :588-643 (fuzz)
```

- The docstring states "1 a material regression ... and nothing else" for the module as a whole.
- `--selftest` and `--fuzz` both exit 1 on a failed test, by design. `--fuzz` also reads `--baseline` with plain `json.loads` outside the barrier, so a missing endpoint there gives a traceback. These are test modes: CI reads neither as a verdict, and the docs page scopes the contract to `check`.
- Optional: scope the docstring sentence to `check`, `record` and `check-baseline`.

## Round-4 structural checks (focus items), with evidence

- **Barrier:**
  - `main()` (`:655-708`) parses, dispatches `--selftest` and `--fuzz`, and refuses missing arguments through argparse. Everything after that runs inside one `try ... except Exception`.
  - The returns are:
    - `judge()`'s status (`:703-705`);
    - 0 or 2 from `check-baseline`;
    - 0 from `record`;
    - 2 from the barrier.
  - The only `print` calls in the gate are `emit()` (`:652`) and the `--fuzz` summary (`:637-641`). No `parser.error` or `sys.exit` lies inside the `try`.
  - I tried to break the barrier structurally. `probe-r4-structure.log` runs 32 cases, with no traceback and only ASCII output in any of them:
    - input paths outside the barrier: an absent directory, a directory that is a file, a baseline or budget that is a directory, a report that is a symlink loop or mode 000, a route status that is a loop or mode 000;
    - names that `emit()` must escape: a non-UTF-8 directory name in `check` and `record`, and a lone surrogate endpoint name on the command line;
    - baselines: a BOM, UTF-16, and 200,000-deep nesting.
  - Input cannot reach an exception inside `emit` itself: every value reaching it is a `str`, and `ascii()` cannot raise.
  - With standard output on `/dev/full` the gate exits 120 at interpreter flush. That is the author's disclosed limit, a failure of standard output itself, and I do not count it.
  - The 39e9329b change holds: an endpoint the baseline lacks is now a `Refusal` inside the barrier.
- **Converters:**
  - `real()` (`:374-382`) and `whole()` (`pp_baseline_rank.py:29-36`) hold the only `float()` and `int()` calls in both modules (static grep).
  - The call sites are:
    - utilization `:134`;
    - timed endpoints `:153`;
    - slack `:157`;
    - route status `:286`, now inside its `try`;
    - hierarchy counts (rank `:59`);
    - budget cells `:531`;
    - every JSON number through `parse_int`/`parse_float` (`:414`), for the baseline and the image manifest.
  - `\d` survives only in the tool-build identity regex (`:206`). That build is compared as text and never converted.
- **Generative test** (`probe-r4-generative.log`, 22 runs on copied modules):
  - The 500 seeded cases alone, without the arms, detect every converter removal I planted:
    - `whole()` grammar, digit bound and Unicode digits;
    - `real()` finiteness;
    - `strict()` replaced by plain `json.loads`;
    - `parse_int`/`parse_float` bypassed;
    - per-site `int()`/`float()` in routing, utilization, slack, endpoints and hierarchy;
    - the repeated-key check;
    - `emit()` printing raw text.
  - The name-class and endpoint-name removals need 5,000 cases.
  - The generated cases do **not** detect a narrowed barrier (`except Refusal`, or `(Refusal, OSError)`), even at 5,000, because the inner handlers already convert every generated failure. The self-test's seven planted-exception arms catch it (selftest rc 1). That matches the author's published kill matrix: the 500 cases alone miss `barrier`, and the shipped `barrier` mutant is killed.
  - Removing `record()`'s or `load()`'s own handler keeps the contract under generated cases, because the barrier holds. The arms still fail on the reason text.
  - The self-test runs 247 arms and 500 cases and passes (`receipts/gates/gate-selftest.log`).
- **20,000-case runs** (`receipts/fuzz/`, inputs sha256 equal to the author packet's):
  - fixtures 20,000: 0 failures, digest `36552f395d6ef669`;
  - A's real route 20,000: 0 failures, digest `1c07ac027c0c26b3`;
  - A's real 1x1 5,000: 0 failures, digest `9f1495ce5396f57b`.
  - All three equal the author packet's case digests (`receipts/fuzz/digests.txt`).
- **Real data** (`receipts/real/`):

  | Run | rc | Result |
  |---|---|---|
  | A route | 0 | route status complete |
  | A 1x1 | 0 | |
  | A 8x8 | 0 | |
  | B route | 1 | +625 LUT over 500 |
  | B 1x1 | 0 | |
  | B 8x8 | 0 | |
  | A 1x1 at 10 ns | 2 | standalone clock identity |
  | `check-baseline` | 0 | 3 endpoints |

## My earlier probes, rerun unchanged (`receipts/prior-probes/`, `run_prior_probes.sh`)

| Probe | Result | Reading |
|---|---|---|
| R446-1 `probe_gate_cli.py` | 116/117 | The one is `inf` with 0 endpoints at rc 2 against round 1's literal 1; round 2 ruled 2. |
| R446-1 `probe_gate_mutants.py` | 21 killed, 0 survived, 2 not applied, control passes | Shipped `count format decimals` and `baseline floor value` are killed. |
| R446-1 `probe_pr_mutant_reasons.py` | 149 of 149 ARM, 0 crash | An arm assertion kills every shipped gate-file mutant. |
| R446-1 `reconcile.py` | 2 mismatches | Both are its hard-coded round-1 sentences, as in rounds 2 and 3. |
| R446-2 `partition_rederive.py` | 0 mismatches | |
| R446-2 `probe_malformed_record.py` | 0 cases not exit 2 | |
| R446-2 `probe_policy_pin.py` | 0 not as expected | Run against the git clone, which it needs for a `git show`. |
| R446-2 `probe_route_status.py` | 15/16 | The 16th is the declined S1 layout, which fails closed at rc 2. |
| R446-2 `probe_extra_mutants.py` | 7 killed, 0 survived, 3 not applied | Their spans were rewritten; shipped `budget floors read`, `timed endpoint boundary` and `baseline route ceiling` are killed. |
| R446-3 `probe_r3_mutants.py` | 20 of 20 killed, control passes | |
| R446-3 `probe_r3_numbers.py` | 0 off contract | |
| R446-3 `probe_r3_untested.py` | 0 off contract | |
| R446-3 `probe_r447_2_cases.py` | 0 off contract | |
| R446-3 `probe_hierarchy_equiv.py` | 0 mismatches on 7 real reports | |
| R446-3 ad hoc checks, as `probe_r4_adhoc.py` | all hold | The WNS of 401 integer digits now gives rc 2. All six rankings are byte-equal to the published TSVs. All six `armq_r` census rows and digests equal the round-4 packet's `armq-census.tsv`. |

## Gates (`receipts/gates/summary.txt`)

- 31 of 31 rc 0. GNU Make 4.3 was first on `PATH`, built from the release tarball (sha256 `e05fdde4...`).
- The em-dash and TOC gates ran under the pinned Markdown environment.
- They include:
  - the gate self-test (247 arms, 500 cases);
  - its mutants (158 of 158 fail, control passes);
  - `check-baseline`;
  - the `pp_baseline` self-tests and mutants;
  - `ci_scope` and `ci_events`;
  - the docs set, including `make -C gptp-processor docs`;
  - the Python ratchets.
- `git diff --check 1269cdaf 79e53831` is clean (`receipts/diff-check.log`).

## Clean lens

```text
[R446] PASS RTL - receipts/diff-name-status.txt (1269cdaf..79e53831: 15 files, none under hdl/ and no XDC or Tcl; gitlinks external efeb541a, gptp-processor 5dce647a, protocol-processor 631eeb34 equal at base and head, third_party/verilog-axis 48ff7a7e in receipts/final-tree-verify.log); receipts/r4-probes/probe-r4-adhoc.log (armq_r FD* census of all six real cell censuses, digests equal to the packet) - no RTL, interface, clock or reset change to judge; the one RTL-facing figure (processor top's +107 FFs are its timer-arm queues, 1,153 -> 1,260 at 1x1) holds in both netlists
```

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Round-4 assignment 5969446300 items 1-6 against `pp_resource_gate.py:374-485, 646-708`; rulings 5967852698 / 5967924270; real A/B CLI runs (`receipts/real/`); `probe-r4-structure.log`; `probe-r447-3-cases.log` | R446-4 | `79e53831a4f623a594f22765be1d05dffeb696a7` |
| RTL | CLEAN | `receipts/diff-name-status.txt`; gitlinks in `receipts/final-tree-verify.log`; `probe-r4-adhoc.log` armq census | R446-4 | `79e53831a4f623a594f22765be1d05dffeb696a7` |
| Robustness | UNCLEAN (F1) | `pp_resource_gate.py:106-485`, `:646-708`; `pp_baseline_rank.py:17-63`; `probe-r4-structure.log` (32 cases); `receipts/fuzz/` (45,000 cases); `probe-r3-numbers`, `-untested`, `-r447-2-cases`, `probe-r447-3-cases` | R446-4 | `79e53831a4f623a594f22765be1d05dffeb696a7` |
| Tests | UNCLEAN (F1) | `pp_resource_gate_selftest.py` (247 arms, `cli()` :569-585, `barrier_arms` :636-665, generators :700-960); `pp_resource_gate_mutants.py` (158); `probe-r4-generative.log`; `probe-pr-mutant-reasons.log` 149/149 ARM; `probe-r3-mutants.log`; `gates/gate-mutants.log` | R446-4 | `79e53831a4f623a594f22765be1d05dffeb696a7` |
| Docs | UNCLEAN (F1) | `AREA_BUDGET.md:184-208`; recipe `:242`, `:459-478`; gate docstring `:22-43`; live PR body Round 4 section; author round-4 packet (`armq-census.tsv`, fuzz receipts) | R446-4 | `79e53831a4f623a594f22765be1d05dffeb696a7` |

## Real limits

- No Vivado or Yosys run. Every real-data check reads the existing A and B run directories. Physical calibration was NOT RUN, and field skips are not hardware proof.
- F1's inputs are hand-written keys in open objects, and no tool writes them. I report F1 because it is a stated refusal, beyond the accepted exception, that the gate neither enforces nor tests.
- Hosted, exact head (`receipts/hosted-check-runs.txt`, read at 15:10:50Z):
  - Succeeded: `rtl-fast`, `yosys-elaboration` (job steps in `receipts/hosted-yosys-elaboration-steps.txt`), `verilator-lint`, `bdd-conformance`, `changes`, `full-ci-gate`, `docs-check-no-git`, `wire-accountability`, Yosys shards 0-3, Verilator shards 0 and 3.
  - In progress: `docs-check`, `elaborate`, and Verilator shards 1, 2 and 4.
  - `Physical gPTP` was skipped, which is not evidence.
  - I could not retrieve the job log excerpt for the gate step, so accepting the hosted gate result is the manager's call.
- Not run, as instructed: the full parent, processor, gPTP, Yosys and builder banks; Docker/act and `act_ci`; hardware.
- Probe hygiene (`receipts/final-tree-verify.log`):
  - HEAD, the tree and the index tree are exact, and `ls-files -s` equals `ls-tree -r HEAD` for blob, mode and path.
  - There are no tracked changes and nothing untracked or ignored.
  - The four gitlinks are as required, and the submodules are clean.

## Pending manager duties

- Hosted and act acceptance at the exact head, including the in-progress contexts and the long aggregates.
- The merge-turn candidate on live dev `bbf704ec` (source base `1269cdaf`), which is distinct from this source review.
- The merge-bank Vivado `check` (ruling (b)).
- A ruling under F1(b), if that route is chosen.
- R1 to the residue checklist if it is not taken in a round.
- Publishing this packet.

## Prior findings at this head

I wrote this section after the verdict and ledger above, and re-planted each case with my own scripts.

| Prior finding | Status at `79e53831` | Evidence |
|---|---|---|
| R446-3 F1: an overflowing slack reads as infinity and passes | **Resolved** | `real()` finiteness on slack and the half count. `probe-r3-numbers.log` reports 0 off contract, and the 401-digit WNS gives rc 2 (`probe-r4-adhoc.log`). The shipped `finite slack`, `slack converter` and `half-count converter` mutants are killed. |
| R446-3 F2: an oversized integer reaches a traceback and exit 1 | **Resolved** | JSON integers go through `whole()` (`:414`), and the route-status `whole()` is inside its `try` (`:284-288`). `probe-r3-numbers.log` reports 0 off contract. |
| R446-3 F3: seven claimed refusals without an arm | **Resolved** | `probe-r3-mutants.log`: 20 of 20 killed. The two uncounted survivors, an upper-case digest and a slack without a fraction, now have killed shipped mutants (`baseline input digest lower case`, `slack fraction`). |
| R447-3 F1: a lone-surrogate name gives exit 1 by traceback | **Resolved** | `probe-r447-3-cases.log` cases A-D: rc 2 in both commands, no traceback, ASCII-only output. The ASCII-strict `cli()` stream and the planted `\ud800` arms; shipped `barrier`, `ASCII output` and `printable ASCII output` mutants are killed. |
| R447-3 F2: a 10**400 integer literal crashes `judge()` | **Resolved** | `probe-r447-3-cases.log`: WNS and WHS give rc 2 in both commands, on B (where `judge()` is reached). |
| R447-3 F3: six claimed refusals without an arm | **Resolved** | Arms kill the shipped mutants `routing-error row single`, `undecodable route status`, `undecodable budget page`, `hold-timed endpoints counted`, `baseline standalone clock text` and `baseline identity exact keys` (`probe-pr-mutant-reasons.log`). |
| R447-3 R1: packet file absent | **Resolved** | `author-r4/receipts/armq-census.tsv` is present, and every row reproduces (`probe-r4-adhoc.log`). |
| R447-3 S1: repeated keys accepted | **Taken** | The gate refuses them in the baseline and the manifest (`probe-r447-3-cases.log`, `probe-r4-structure.log`). |
| R447-3 S2: bool scope counts, late hierarchy cell | **Taken** | Shipped `baseline scope counts not bools` and `hierarchy counts end early` are killed. |
| Round-1 and round-2 findings of both reviewers | **Resolved; no regression** | The earlier-probe table above. |

R446-4 FINISHED
