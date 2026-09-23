# [A216] #529 / PR #534, correction round 1: handoff

- Lane: `529-crf-input-counters`, `$LANES/529-crf-input-counters`.
- Round input head: `f815577559d4922c945dcf1436d4394ff2c10567`.
- New head: `535701a06128d54c7f0f161e1c061fa02d4d1342`, tree `8c62c1a118b6bdacc0cf9b39d2cbdc633717630f`.
- Base: `ede8d48ecd7c7f589a14b957951f040d92c99c70`.
- Gitlinks are unchanged: protocol-processor `424c688f`, gptp-processor `c1b61743`,
  third_party/verilog-axis `48ff7a7e`.
- Not pushed. Pushing and editing the PR are the coordinator's.

The two new commits are one-line, with no trailers:

| SHA | Subject |
|---|---|
| `a51d5164` | Drive each CRF input tally through its own engine event at the root and hold the CRF push quiet after its release in sim_nxn |
| `535701a0` | Narrow the CRF counter evidence to what the root-wire tests prove and clear the stale REGISTER_MAP opening gap |

**No RTL change.** `git diff f8155775 HEAD -- hdl` is empty. So there is no VERSION,
descriptor, pin or synthesis consequence. `hdl/milan/milan_datapath.sv` and
`KL_crf_rx.sv` are byte-identical to the reviewed head. CHANGELOG.md is unchanged,
because this round makes no product change.

## Per-finding disposition

Severity and lens are the reviewers' own labels, unchanged.

| Finding | Severity, lens | Fix | Failing arm shown |
|---|---|---|---|
| R269 F1 = R268 F1: the root-wire tests cannot detect a permuted `KL_crf_rx` port binding, and 7 of the 10 bindings are not discriminated | MAJOR (R269; R268 filed it MINOR; the assignment takes MAJOR). Conformance, Tests, Docs | New last arm of `[CTRS-CRF]`, `grade_each_crf_input_counter_through_its_own_engine_event` (`sim_nxn.cpp:3578`). It seeds no tally. In a fresh era, real PDUs at the root move each of the ten through its own engine event. So does the engine's 100 ms silence timeout, for the unlock (see the note below). The final counts are pairwise distinct, and every quadlet is checked exactly. There are also checks of the Table 5.6 lock pair after the first lock (1/0) and after the unlock (1/1). | All 45 pairwise exchanges of the ten bindings at the instance port map are red on `nxn` and on `nxn8`. In every one, both of the pair's own quadlets are red. The reviewers' mx1-mx4 and p1-p5 are red on nxn, nxn8, nxndv and nxn4c. Against the f8155775 harness, 22 of the 45 exchanges were green on nxn. |
| R268 F2: `[NOTIFY-CRF]` cannot fail for a CRF row that keeps pushing every second | MINOR. Tests, Docs | Two checks after the release (`sim_nxn.cpp:1346-1353`): two more seconds without a change bring no further push to B, nor to A | The reviewer's `r3_crf_pend_stuck` is red on `notify`: B and A each receive 4 pushes, where 2 are expected. The marked control is green, 145/0. |
| R268 F3: the REGISTER_MAP opening status still lists the CRF counter bank as a remaining gap | MINOR. Docs | `REGISTER_MAP.md:31-35` now lists it as served and pushed since #529 | `docs_check.py` exit 0 |
| R269 F1 docs: REGISTER_MAP 846-877, the `sim_nxn.cpp` claim at 3409-3411, and README 507-521 overclaim | Part of F1. Docs | The signature arm is now described as grading the gather mux only (wire to quadlet). The binding claim rests on the event arm. The mutation claims read "each mutation turns at least one check red", which is what was run. The frozen criteria are quoted beside their evidence, which also takes up R269 S4. The compliance-matrix 5.4.2.25 evidence names the event arm. | Docs gates below |

### The unlock's 100 ms silence

`KL_crf_rx` unlocks only when its own timeout counter `tout_r` reaches
`CLK_FREQ_HZ_P / 10`. At this leg's 100 MHz fabric clock that is 10,000,000 cycles.

I measured the cost of running it whole on an interim harness
(`logs/interim_real_silence_run_nxn.txt`):

- the nxn leg went from 6.2 s to 37.6 s of wall time;
- across the four broad legs that is an estimated 2 to 3 minutes (only nxn was measured);
- milan_dp runs against a 2700 s hosted deadline and has timed out on the hosted runner before.

So the committed harness advances the engine's `tout_r`, through the engine's own
hierarchy, to 1 ms short of the limit, and runs that last millisecond for real.

- The unlock, the `cnt_unlocked_o` increment and every wire after it are the engine's.
- No tally is written.
- A port-map exchange cannot relabel `crf_rx.tout_r`, and every exchange involving
  MEDIA_UNLOCKED is red (9 of 9 on each of nxn and nxn8).

### The event plan and the counts it must produce

One PDU lands per 256-cycle observation interval, because `inject()` holds each PDU for 400 cycles.

| Counter (quadlet) | Engine event at the root | Count |
|---|---|---|
| MEDIA_LOCKED (@0) | two runs of eight clean in-order PDUs | 2 |
| MEDIA_UNLOCKED (@4) | the 100 ms silence timeout | 1 |
| STREAM_INTERRUPTED (@8) | three gaps with 2, 3 and 2 PDUs lost | 3 |
| SEQ_NUM_MISMATCH (@12) | those three gaps plus a gap of 1 | 4 |
| MEDIA_RESET (@16) | five received-`mr` toggles | 5 |
| TIMESTAMP_UNCERTAIN (@20) | six PDUs with `tu` set | 6 |
| UNSUPPORTED_FORMAT (@32) | seven `type` 2 PDUs at the followed sid | 7 |
| LATE_TIMESTAMP (@36) | eight PDUs stamped 1 ms before the PHC | 8 |
| EARLY_TIMESTAMP (@40) | nine PDUs stamped 100 ms ahead (the limit is MaxTT 2 ms plus a 10 ms margin) | 9 |
| FRAMES_RX (@44) | 21 accepted PDUs | 21 |

A `static_assert` refuses a count table with two equal entries.

The rejected PDUs come before the first lock, so the arm neither relies on nor
contradicts how a validation error affects the lock (see the out-of-scope finding below).

## Validation at the new head

Environment:

- the pinned simulator 5.050 (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin`), first on PATH;
- 8 jobs;
- harness `sim_nxn.cpp` sha256 `fe0e4c37bee03fbfbc5a083144983524d6b9f938ff504884c35e64df191c6f57`, equal to `git show HEAD:tb/verilator/milan_dp/sim_nxn.cpp`;
- datapath sha256 `2b729369b5e705cf8f76713d59720e5017c7000fdc620e72bd4269021656bcd1`.

Each leg was built with its `run` recipe line. `scripts/legs.mk` repeats those lines
with only the Mdir changed. The main leg ran the literal `make -n run` line.

| Leg | Result | At f8155775 |
|---|---|---|
| `obj_nxn` (4x4) | 1705 / 0, with 72 `[CTRS-CRF]` | 1687, with 54 |
| `obj_nxndv` (divergent 4x4) | 1707 / 0 | 1689 |
| `obj_nxn4c` (shipping Arty 4x4) | 1705 / 0 | 1687 |
| `obj_nxn8` (8x8) | 3133 / 0 | 3115 |
| `obj_notify` (timed AX 1x1) | 145 / 0, with 10 `[NOTIFY-CRF]` | 143, with 8 |
| `obj_dir` (main, sim_main 1x1) | 230 / 0, with 1 section guarded as at base | 230 |

Logs: `logs/run_*.txt` and `logs/build_*.txt`.

Gates at `535701a0` (logs `logs/gates_static.txt`, `logs/gates_docs_workflow.txt`,
`logs/gate_xvlog.txt`, `logs/gate_test_builder.txt`, `logs/gate_em_dash.txt`):

| Gate | Result |
|---|---|
| `scripts/check_rtl_source_lists.py` | exit 0 |
| `scripts/xvlog_gate.py --check` | PASS: `hdl/` has 0 findings, and the 4 pinned-processor findings equal the ratchet |
| `scripts/check_cpp_idiom.py` | exit 0; every ratchet 0 <= 0 |
| `scripts/check_py_idiom.py` | exit 0 |
| `scripts/check_baremetal_only.py --check` | exit 0 |
| `scripts/docs_check.py` | exit 0 |
| `scripts/check_em_dash.py --base ede8d48e` (the merge base, as the gate's own usage prescribes) | 0 findings over 153 added lines in 9 pages |
| `scripts/check_em_dash.py --base 759da623` (as assigned) | 1 finding, not this lane's: see the note below |
| `sw/builder/test_builder.py` | exit 0, "ALL GATES PASS EXCEPT 1 NOT RUN". Gate 11 needs the mf48 hardware build report, which is not on this host. |
| `git diff --check ede8d48e..HEAD` | clean |
| `check_doc_style`, `check_gptp_docs` (plain and `--with-submodule`), `DOC_MAP.gen --check`, `timesync_chain.gen --check`, `check_solution_docs`, `submodule_boundaries.gen --check`, `check_submodule_docs`, `check_feature_status --self-test`, `gen_module_matrix --check`, `measure_naming --check`, `check_port_contracts`, `measure_fail_fast --check`, `check_todo_ownership`, `measure_test_evidence --check`, `check_hygiene --check`, `check_sv_idiom`, `lint_rtl --check` | all exit 0 |

**The `--base 759da623` finding.** It is `CONTRIBUTING.md:342`, a file this lane never
touches: `git diff ede8d48e HEAD -- CONTRIBUTING.md` is empty.

- `759da623` is not an ancestor of the branch.
- So `759da623..HEAD` shows the base-era line that dev later rewrote.
- The candidate merge `git merge-tree --write-tree HEAD 759da623` (tree `2f139574`) keeps
  dev's CONTRIBUTING.md.
- That candidate adds 0 em dashes to any page relative to `759da623`
  (`logs/em_dash_base_note.txt`).

**Candidate merge.** Merging with the live dev tip `26d855a9` is clean
(`git merge-tree --write-tree HEAD origin/dev`, exit 0, tree `73ac527c`). Dev's
REGISTER_MAP edits since the base are in the slip-count section, far from the CRF text.
The candidate was not built or run.

## Mutation campaign

There are 197 receipts. Each one gives:

- the datapath sha256 and the harness sha256;
- the build and run exit codes;
- every `[FAIL]` line and the tally.

The receipts are in `logs/mutants/<tag>.txt`, with the full run log in `<tag>.run.log.gz`.
`MUTATION-RESULTS.md` is the table. It was written by `scripts/summarize.py`, which also
checks that in every pairwise exchange both of the pair's own quadlets are red in the
event arm's row.

How each set was produced:

- **pw_*: the 45 pairwise exchanges** of the ten tally bindings at the `KL_crf_rx`
  instance, with the mux untouched. They come from `scripts/gen_mutants.py`.
  - `pw_mr_tu`, `pw_lock_unlock`, `pw_late_early` and `pw_lock_intr` are byte-identical
    to R269's mx1, mx2, mx3 and mx4.
- **r269/*: R269's own set**, written by their archived `make_mutants.py`
  (`reviewer-scripts/`, copied verbatim from `529-review-evidence`).
  - All 11 sha256 values equal their receipt 15.
- **r268/*: R268's own set**, written by their archived `mutants.py` `make_copy()`.
  - Every copy's diff hunks equal their archived `mutant.diff`.
  - Each carries their `public_flat_rw` marking; `ctl_marked` is the marking alone.
- `mutants/` keeps each copy's diff and `MUTANTS.sha256`. Rerunning the generator
  regenerates the copies.

| Set | Legs | Result |
|---|---|---|
| 45 pairwise | nxn | 45 red; both own quadlets red in every one |
| 45 pairwise | nxn8 | 45 red; both own quadlets red in every one |
| 45 pairwise, **f8155775 harness** (counterfactual) | nxn | 23 red, **22 green**: early/lock, early/unlock, fmt/late, fmt/lock, fmt/mr, fmt/tu, fmt/unlock, late/early, late/lock, late/unlock, lock/unlock, mr/early, mr/late, mr/lock, mr/tu, mr/unlock, pdu/early, seq/intr, tu/early, tu/late, tu/lock, tu/unlock |
| R269 mx1-mx4, ma1-ma7 | nxn | 11 red |
| R269 mx1-mx4 | nxn8, nxndv, nxn4c | 12 red |
| R268 a1-a8, p1-p5 | nxn | 13 red; `ctl_marked` green, 1705/0 |
| R268 p1-p5 | nxn8, nxndv, nxn4c | 15 red |
| R268 r1-r7 | nxn | r2, r4, r5, r7 red. r1, r3, r6 green, as in R268's own receipts; see below. |
| R268 r3, a5 | notify | r3 red on the two new quiet checks (4 against 2, for B and for A). a5 red, 10 checks. `ctl_marked` green, 145/0. |

The three green r-mutants on nxn:

- **r1** (the CRF row for every index >= N): R268 found it equivalent at the wire,
  because the descriptor store refuses N+1 before the gather face.
- **r3** (stuck pending bit): nxn has no timed limiter. The mutant is red on the timed
  leg, which is F2.
- **r6** (round-robin resume point): this is R268 S1, the arbiter's no-starvation
  property, already untested at base. This round does not take it up.

R269 also ran mx1-mx3 on `notify` and `main`. Those legs carry no `[CTRS-CRF]`:

- the timed leg exits after the descriptor image and the notify section;
- `main` is `sim_main.cpp`.

So those mutants were not rerun there.

## Reproduce

Run from the lane at the head, with the pinned simulator first on PATH:

```sh
P=$MANAGEMENT/2026-09-23/529-a216
python3 $P/scripts/gen_mutants.py hdl/milan/milan_datapath.sv $P/reviewer-scripts /tmp/m529
diff <(sort /tmp/m529/MUTANTS.sha256) <(sort $P/mutants/MUTANTS.sha256)   # empty
$P/scripts/run_mutant.sh nxn /tmp/m529/pw_lock_unlock.sv nxn_pw_lock_unlock
$P/scripts/run_mutant.sh notify /tmp/m529/r268/r3_crf_pend_stuck.sv notify_r3
```

`run_mutant.sh` and `legs.mk` name this lane's paths. `legs.mk` is included after the
suite Makefile, so every build uses the suite's own SRCS, flag sets and shapes.
`run_mutant.sh` takes an optional fourth argument: a harness copy in the suite
directory. That argument is how the f8155775 counterfactual ran. Its temporary copy was
deleted afterwards, and the worktree is clean.

## Not run, and limits

- **The rest of milan_dp's `run` recipe:** nolpf, prune, ax1x1, aclk, gptp, gptplat and
  the render mutants. None of them compiles `sim_nxn.cpp`, and `hdl/` is unchanged.
- **Other suites:** pp_shadow, milan_dp_render, crf_rx, behave and milan_dp_gptp. Their
  inputs are unchanged.
- **Other gates and hardware:** Yosys, act/Docker and hardware were not run. test_builder
  gate 11 was not run (see above).
- **The candidate merge with live dev** was checked for conflicts only; it was not built.
- **The 990 ms floor** of `[NOTIFY-CRF]` (R269 S2) is unchanged. The push stamp still
  skips the lever writes, and the reviewers measured 997 ms.
- **Suggestions this round did not take up:**
  - R269 S1 = R268 S2: the `crf_sink: false` shape;
  - R269 S3: the config comments that point at B4;
  - R269 S5 = R268 S3: `Closes #529` with the silicon item still open, a manager duty;
  - R268 S1: arbiter starvation.

## Found, out of scope (for a new Issue)

The `KL_crf_rx` banner (`KL_crf_rx.sv:32-34`) says `locked_o` drops "after 100 ms
without an accepted PDU ... or on a validation error". It also says lock needs
"|delta jitter| within window". The REGISTER_MAP `CRF_CTRL` row (`0x738`) also says
"100 ms silence or a validation error to unlock".

The engine does neither:

- `locked_o` falls only on the silence timeout (`KL_crf_rx.sv:484-488`), and on reset and the
  bind rise, without scoring.
- A rejected PDU only resets the settle run (`:508-511`).
- Lock checks no jitter.

Both texts predate this lane (base `ede8d48e`). The event arm keeps its rejected PDUs
before the first lock, so it does not encode either reading.
