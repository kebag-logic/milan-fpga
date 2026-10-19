[R663] NEGATIVE - exact head eef90b4238b6c19b679b44adc6f09362809be153

Round R663-2: internal, cleared-context, independent review of PR #767 (issues #761 and #762).

- Head `eef90b4238b6c19b679b44adc6f09362809be153`, tree `ba15df1ef198a7d86150b4e33726fe0a4a10f589`.
- This round reviews the delta `4191b098..eef90b42`: three round-2 commits (`ba9ac06a`, `492207f7`, `2cd2750d`) and one round-2b commit (`eef90b42`).
- The branch base is dev `e9cbb676`. Live dev is `e26f1816`; composition with it is the manager's candidate duty.

All five lenses were applied at this head. The verdict is NEGATIVE because of one open MINOR, R663-2-F1 (Tests): the datapath wiring of the new `stopped_i` port is not graded by any bench. The engine logic, the rulings, the boundary law and the docs are clean. Every prior finding on this PR is resolved at this head, except R663-1-S1, which stays a suggestion.

Method: I reconstructed the task from AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue bodies of #761 and #762, the assignment (#761 comment 6256482625), the round-2 assignment (#767 comment 6260976498), the #762 scope ruling (comment 6260976223) and its extension (comment 6265746720), and the PR body. I then read the delta, history and harnesses, re-executed the changed suites and campaigns, and spot-checked the author's published receipts at `32af21b0`, `review-evidence/761-r1/author-r2/receipts/r2b-*`. My verdict and ledger were fixed in a draft of this file before I read the prior review bodies (R664-1 6260664989, R663-1 6260969105). The author's handoff notes and the other reviewers' packet files were not read.

## Findings

### R663-2-F1 MINOR: the new `stopped_i` wiring in the datapath is graded by no bench

- **Lenses:** Tests.
- **Where:**
  - The new connection is at `hdl/milan/milan_datapath.sv:6307-6308`: `.stopped_i (acmpl_stopped_v_w[N_STREAMS-1:0])`. It is the AAF half of the round-2 ruling at the entity's GET_COUNTERS face.
  - The N=4 stack wrapper ties the port off, at `tb/verilator/avtp_rxmon/avtp_rxmon_nx_wrap.sv:140`: `.stopped_i ('0)`.
  - `tb/verilator/milan_dp/sim_nxn.cpp:6570-6640`, `prove_a_stopped_stream_input_discards`, sends STOP_STREAMING to an AAF sink (`:6591`) and START_STREAMING (`:6622`). It never produces a gap or a silence while the sink is stopped, and it reads no STREAM_INTERRUPTED.
- **Authority and evidence:**
  - AGENTS section 6, Tests lens: "Real integration wiring is tested where practical."
  - I searched `tb/` and `tests/` for any file that touches both STREAM_INTERRUPTED and STOP or a stopped state. Only three groups match:
    - the unit lockstep harness, its reference and its wrappers;
    - `milan_dp/sim_nxn.cpp`, whose STOP cases (`:2320`, `:6570`) never read STREAM_INTERRUPTED, and whose STREAM_INTERRUPTED cases (`:4766`, `:5527-5656`) never STOP;
    - torture-plan text, which runs no simulation.
  - So a tie-off of `:6308` to `'0`, or a wrong vector there, passes every bench. The N=4 stack's own wrapper is exactly that tie-off.
  - I established this by inventory and RTL reading. I did not run a datapath mutant (see Limits).
  - A test is practical: `sim_nxn.cpp` already issues STOP_STREAMING and START_STREAMING to an AAF sink (`:6591`, `:6622`) and reads an AAF STREAM_INTERRUPTED (`:4766`). The CRF half of #762 already has integrated grading at the same level (`[CTRS-CRF]`, `:5656`).
- **Impact:**
  - If that one line regresses, a stopped AAF Stream Input again counts STREAM_INTERRUPTED for a silence and for a sequence gap, which is the behaviour the round-2 ruling and its extension remove.
  - It would be seen only on hardware, the way #762 itself was found.
- **Required outcome:**
  - An integrated case on a shipping datapath shape. It STOPs an AAF Stream Input with STOP_STREAMING, then shows by count that a gap while stopped (and/or a silence that expires while stopped) leaves STREAM_INTERRUPTED unchanged, while SEQ_NUM_MISMATCH or MEDIA_UNLOCKED moves to prove the case is live. After START_STREAMING, a gap counts +1.
  - A planted mutant at `milan_datapath.sv:6308` (the port tied to `'0`, or a wrong vector) fails that named check.
- **Verification:** run the milan_dp leg clean and with the mutant. Expect rc 0 clean, and the named check failing under the mutant.

### R663-2-F2 RESIDUE: two port comments still say only "silence"

- **Where:**
  - `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:151-152`: "a stopped input has no playback, so its silence is no interruption (#762)".
  - `hdl/milan/milan_datapath.sv:6307`: "#762: a stopped input's silence interrupts no playback (5.3.8.7)".
- **Why:** since `eef90b42` the same port also suppresses a gap's count (`KL_avtp_rx_monitor_ctx.sv:1025`). This is wording only; the behaviour and the other docs are correct.
- **Exact fix:**
  - `KL_avtp_rx_monitor_ctx.sv:152`: "input has no playback, so neither its silence nor its sequence gap is an interruption (#762)".
  - `milan_datapath.sv:6307`: "#762: a stopped input's silence or sequence gap interrupts no playback (5.3.8.7)".

### R663-2-F3 RESIDUE: stale status lines in the PR body

- **Where:** PR #767 body.
  - Status: "Hosted CI and the act replica have not run this head (not pushed)."
  - Known limitations: "Hosted CI and the act replica were not run: the head is not pushed."
  - Roles: both reviewers are "(to be assigned)".
- **Why:** the head is pushed. Hosted `docs-check`, `docs-check-no-git`, `docs-gates-0/1/2`, `verilator-lint` and `yosys-elaboration` succeeded at `eef90b42` (`receipts/hosted_checks_snapshot.tsv`), and the long gates were still running at the snapshot.
- **Exact fix:**
  - State the hosted state at the head, or point to the checks.
  - Drop "not pushed".
  - Name `[R663]` as the internal cleared-context reviewer.

### R663-2-S1 SUGGESTION: count-grade a CRF STOP on the edges around the timeout

- **Where:** `tb/verilator/crf_rx/sim_main.cpp:1662-1671` (`[762-ST-b]`). The STOP lands long before the timeout.
- **Why:** the AAF engine has a cycle sweep across its expiry. The CRF reads `en_i && !stop_i` on the timeout edge itself (`KL_crf_rx.sv:559`), so a late-read defect is structurally unlikely, but no check pins the edge.
- **Suggestion:** add `[762-ST]` trials with `stop_i` rising one edge before the timeout, on it and one edge after it, expecting +0, +0 and +1, alongside the existing `[UNB-d5]`.

R663-1-S1 (a dynamic row for the clock-source gate on the CRF gain edge) is retained as a SUGGESTION. The delta does not touch it, and the builder's exact-initializer pin still refuses that text statically.

## Prior findings at this head

| Finding | Status at eef90b42 | Evidence |
|---|---|---|
| R663-1-F1 BLOCKER: gate_50 over-shard control | **Resolved** | See note 1. |
| R663-1-F2 MINOR: engines disagree on a stopped input's silence | **Resolved** | See note 2. |
| R663-1-F3 MINOR: the unbind law graded only against the mirrored copy | **Resolved** | See note 3. |
| R663-1-S1 SUGGESTION | Retained, optional | Not touched by the delta. |
| R664-1-F1 MAJOR: a later Unbind erases an expired silence | **Resolved** | See note 4. |
| R664-1-F2 MAJOR: started-only restriction without a decision | **Resolved** | See note 5. |

1. **R663-1-F1.**
   - `scripts/ci_case_receipts_selftest.py:172-174` refuses `f"0/{len(names) + 1}"`. The `len(names)`-way split is still accepted by the verify loop at `:150-151`.
   - My run printed `shard 0/35 refused` and `34 driver cases`, rc 0 (`receipts/ci_case_receipts_selftest.log`).
   - The vacuous form `0/{len(names)}` makes the selftest fail with "receipt control accepted: shard 0/34", rc 1 (`receipts/probe_selftest_vacuous_len.log`).
   - All 14 gate_50 commands give rc 0 at this head (`receipts/gate50.log`).
   - Hosted `docs-gates-0/1/2` and `docs-check` succeeded at this head.
2. **R663-1-F2.**
   - Both engines apply one law: AAF at `KL_avtp_rx_monitor_ctx.sv:910` and `:1025`, CRF at `KL_crf_rx.sv:401` and `:559`. This follows rulings 6260976223 and 6265746720.
   - The docs state it at `REGISTER_MAP.md:873-896` and `MILAN_COMPLIANCE_MATRIX.md:131`.
   - The stopped-then-silent case is graded in each engine: AAF `[SI] a stopped input's silence ... counts no STREAM_INTERRUPTED`, CRF `[762-ST-b2]`, each with a mutant.
   - The integration wiring remains, as R663-2-F1.
3. **R663-1-F3.**
   - The law changed: the Unbind clear was removed. The both-planted equivalent of the old `aaf_both` edit is the mutant `consume race`, which reinstates the clear in the engine and the reference.
   - It is caught only by `[SI] boundary (an unbind, idle|busy)` at N=1 and N=8 (`receipts/avtp_rxmon_make.log:1064-1065`).
   - The oracle is exact per trial: `want = d > 0`, with E derived by the harness (`sim_lockstep.cpp:319-323`, `:867`).
4. **R664-1-F1.**
   - The bind-fall clear is gone (`KL_avtp_rx_monitor_ctx.sv:892-897`), and the mark is set only at the expiry (`:908-911`).
   - The sweep covers -200, -40, -12..+24, +40 and +80 cycles around the expiry, idle and busy, at N=1 and N=8.
   - Its live checks require samples between the MEDIA_UNLOCKED write and the STREAM_INTERRUPTED write (the R664-1 window), and some interruption writes that yielded to a PDU walk. All pass (`receipts/avtp_rxmon_make.log`).
5. **R664-1-F2.**
   - The decision is public in ruling 6260976223 and extension 6265746720.
   - Both engines implement it, and every case named in the round-2 assignment is graded by count with a mutant, in the engine and in the reference or replica.
   - The register map and the PR claim are aligned.

## Lens results

Clean-lens lines (format: `[R663] PASS <lens> - <artifact> - <what was checked>`):

- `[R663] PASS Conformance - hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:892-913,1020-1026; hdl/ieee1722/crf/KL_crf_rx.sv:396-401,546-560; hdl/milan/milan_datapath.sv:6268-6308; docs/reference/REGISTER_MAP.md (no table row changed) - checked the round-2 RTL against ruling 6260976223, extension 6265746720, Milan v1.2 5.3.8.7, 5.4.2.19, 5.4.2.20 and 5.3.8.10 Table 5.6, and IEEE 1722-2016 4.4.4.3`
  - A silence or a gap on a started input counts once. On a stopped input neither counts. After START both count again.
  - STOP with live traffic counts nothing. The AAF monitor sits upstream of the 5.3.8.7 gate, so it stays locked. The CRF lock times out uncounted.
  - An Unbind adds nothing, and one after the expiry leaves the silence counted.
  - The #761 expression is untouched since round 1. The AAF-return restart is out of scope by ruling.
  - There is no register map, top-level port or parameter change. The datapath delta is one internal instance connection.
- `[R663] PASS RTL - KL_avtp_rx_monitor_ctx.sv:153,826,892-913,1020-1026,1066-1083,1147; KL_crf_rx.sv:368,401,546-560; milan_datapath.sv:5392,6283,6308; author receipt r2b-route/check.log at eef90b42 - checked the event boundary, widths, indexing, clock domain, counter-writer exclusion and resources`
  - The watchdog scan precedes the walker, and the mark is set only at the expiry.
  - An Unbind after the expiry leaves `sil_pend_r` and `sil_si_r` set, so the walk writes MEDIA_UNLOCKED and then STREAM_INTERRUPTED once. An Unbind on or before the expiry leaves `bound_i` low, so no mark is set.
  - The mark clears at reset, at walk phase 3 and at the bind decode.
  - `stopped_i[ev_s_r]` is indexed like `sil_si_r`. It reads the same vector, with the same indexing and in the same domain, as the accept gate (`:6283`) and the clock meter (`:5952`).
  - In the CRF, the timeout write and `w_ev_si_w` are mutually exclusive: the timeout requires `!w_acc_run_w`, and `w_ev_si_w` requires `w_acc && !stop_i`.
  - `lint_rtl.py --check` gives rc 0.
  - route-1x1 at `eef90b42` (commit.txt): check PASS, LUT 49,597 (-16), WNS +0.189 ns, WHS +0.014 ns, 0 routing errors, gitlinks equal to the head's.
- `[R663] PASS Robustness - tb/verilator/avtp_rxmon/sim_lockstep.cpp:589-916; tb/verilator/crf_rx/sim_main.cpp:1635-1783; receipts/avtp_rxmon_make.log, receipts/crf_rx_make.log - executed at this head`
  - Unbind and STOP swept across the expiry, idle and busy, at N=1 and N=8, including the window between the two counter writes and yielding writes.
  - STOP and START swept across a gap's verdict, -4..+20 cycles, idle and busy.
  - Repeated stopped gaps; another input's STOP at N=8.
  - Unbind of a stopped, locked input; START recovery; rebind era wipe; reset.
  - The CRF gap's edge decided in both directions (`[762-SG-d1..d5]`); Unbind and the silence after it (`[762-ST-e]`).
  - The stopped level is idempotent under repeated STOP or START.
- Tests: **UNCLEAN (R663-2-F1).** Everything else examined is clean:
  - Every #762 rule is count-graded in both engines.
  - The 9 AAF #762 mutants are each planted in the engine and the reference, and each is caught by its named `[SI]` count check (`receipts/avtp_rxmon_make.log:1058-1075`; 14/14 with the 4 lockstep-hazard mutants).
  - The CRF has 18/18 mutants. The two engine-and-replica mutants fail only `[762-SG]` count checks, with no replica-compare failure (`receipts/crf_both_mutant_failures.log`: 6 and 4 failing checks).
  - The gate_50 control is derived from the driver's inventory, and its vacuous form is refused.
  - Lockstep reaches 116 checks at N=1 and 119 at N=8; flat 97; stack 121; crf_rx 15,202 + 2,201 + 69. All match the author's claims.
- `[R663] PASS Docs - docs/reference/REGISTER_MAP.md:873-896; docs/reference/MILAN_COMPLIANCE_MATRIX.md:131; docs/testing/TESTING.md:614,625; PR #767 body; source comments in the round-2 delta - checked each statement against the RTL and the executed harness output`
  - The suite descriptions and mutant lists match the drivers.
  - `check_doc_paths`, `check_doc_style` and `check_archive` give rc 0. `gen_toc` was not run (see Limits), and the delta adds no heading.
  - No lane label, review round, reviewer ID or comment ID appears in any added source line.
  - Residue R663-2-F2 and R663-2-F3 are recorded with their exact fixes and do not uncover the lens.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_avtp_rx_monitor_ctx.sv:892-913,1020-1026`; `KL_crf_rx.sv:396-401,546-560`; `milan_datapath.sv:6268-6308`; rulings 6260976223 / 6265746720; Milan v1.2 5.3.8.7, 5.4.2.19/20, Table 5.6 | R663-2 | eef90b4238b6c19b679b44adc6f09362809be153 |
| RTL | CLEAN | `KL_avtp_rx_monitor_ctx.sv:153,826,892-913,1020-1026,1066-1083,1147`; `KL_crf_rx.sv:368,401,546-560`; `milan_datapath.sv:5392,5952,6283,6308`; `lint_rtl --check`; r2b-route receipts | R663-2 | eef90b4238b6c19b679b44adc6f09362809be153 |
| Robustness | CLEAN | `sim_lockstep.cpp:589-916`; `crf_rx/sim_main.cpp:1635-1783`; executed sweeps in `receipts/avtp_rxmon_make.log`, `receipts/crf_rx_make.log` | R663-2 | eef90b4238b6c19b679b44adc6f09362809be153 |
| Tests | UNCLEAN (R663-2-F1) | `lockstep_mutants.py`; `crf_rx/mutants.py`; `sim_lockstep.cpp`; `crf_rx/sim_main.cpp`; `ci_case_receipts_selftest.py:150-174`; `avtp_rxmon_nx_wrap.sv:140`; `milan_dp/sim_nxn.cpp:2320,4766,5527-5656,6570-6640` | R663-2 | eef90b4238b6c19b679b44adc6f09362809be153 |
| Docs | CLEAN | `REGISTER_MAP.md:873-896`; `MILAN_COMPLIANCE_MATRIX.md:131`; `TESTING.md:614,625`; PR #767 body; round-2 source comments | R663-2 | eef90b4238b6c19b679b44adc6f09362809be153 |

## Execution receipts (all at this head)

Simulator: Verilator 5.050 (2026-07-01, rev v5.050), identity checked (`receipts/verilator_identity.txt`). Builds ran in a disposable `git archive` copy of the head, plus the `third_party/verilog-axis` gitlink content.

| Receipt | Result |
|---|---|
| `receipts/avtp_rxmon_make.log` / `.rc` | rc 0. Flat 97/0, stack 121/0, lockstep N=1 116/0 and N=8 119/0; `lockstep_mutants.py` 14/14 (twice, because `run` and `lockstep` both invoke it). |
| `receipts/crf_rx_make.log` / `.rc` | rc 0. 15,202/0, discontinuity 2,201/0, talker_step 69/0, mutants 18/18. |
| `receipts/crf_both_mutant_failures.log` | `stopped_gap_interrupts`: 6 failures, all `[762-SG]`. `sticky_stop_gap`: 4 failures, all `[762-SG]`. No replica-compare failure. |
| `receipts/gate50.log` | All 14 gate_50 commands give rc 0 (host CPython 3.14.8). |
| `receipts/ci_case_receipts_selftest.log` / `.rc` | rc 0, `shard 0/35 refused`, 34 driver cases. |
| `receipts/probe_selftest_vacuous_len.log` / `.rc` | rc 1: the `0/{len(names)}` form is refused by the selftest itself. |
| `receipts/doc_gates.log` | `check_doc_paths`, `check_archive`, `lint_rtl --check` and `check_doc_style` rc 0. `gen_toc` rc 2 (pinned renderer absent). |
| `receipts/hosted_checks_snapshot.tsv` | Hosted check runs at the exact head, with the snapshot time. |
| `receipts/tree_integrity.log` | HEAD and tree as stated; index equals the HEAD tree; 1,422 tracked blobs with 0 byte/mode mismatches; clean status; gitlinks equal to the recorded commits for the five populated submodules (`external` is uninitialised, as at the start). |
| `scripts/crf_both_mutant_failures.py`, `scripts/tree_integrity.sh` | Portable scripts behind the receipts above. |

Author receipts spot-checked at `32af21b0`:

- `r2b-route/commit.txt` reads `eef90b42…`; `check.log` gives RESULT PASS, rc 0.
- `r2b-gate50/g50.console` shows 14 rc 0.
- `r2b-sweep/shard0-4.summary` all rc 0: 63 suites, whose list equals the shard union, and 12,518 + 35,543 + 424,841 + 1,673,500 + 41,952 = 2,188,354 checks, 0 failures.
- `r2b-final` builder and yosys rc 0. `r2b-gmstep` rc 0. `r2b-focused/c2-milan_dp.rc` rc 0. An earlier milan_dp attempt in the same directory was terminated for memory and is labelled as such.

## Limits

- **No datapath mutant was run for R663-2-F1.** A milan_dp mutant needs the full protocol-processor build and was not run. The finding rests on the bench inventory search and the stack wrapper's tie-off.
- **Out of scope for this round.** The full 63-suite sweep, Yosys, builder, gm-step and route were not re-executed (not allowed, or owned by the author and manager). I rely on the author's published receipts, spot-checked as above.
- **Host interpreter.** gate_50 ran under host CPython 3.14.8, not the CI's 3.12.
- **`gen_toc`** was not run because its pinned renderer is not installed and no install was allowed. The delta adds no Markdown heading.
- **No manager source bank** exists at this head, and none is claimed.
- **No hardware proof.** Physical calibration was NOT RUN, and field skips are not hardware proof.
- **R664-1's own probes** were not executed. The resolution of R664-1-F1 rests on this head's exact-count boundary sweep, executed here.

## Pending manager duties

- **R663-2-F1.** It must be fixed and re-reviewed at the new head under the Tests lens. A change to `milan_datapath.sv` or to the harnesses un-covers the lenses whose scope it touches.
- **Residue checklist.** Carry R663-2-F2 and R663-2-F3 to it.
- **Merge candidate.** Build and validate the current-dev candidate (source base `e9cbb676`, live dev `e26f1816`), with the builder and native banks.
- **Hosted and act acceptance at the final head.** At the snapshot, the exhaustive `verilator-suites` and `yosys-portability` shards and `rtl-fast` were still in progress or queued.
- **Second review.** The external independent positive review is still required.

R663-2 FINISHED
