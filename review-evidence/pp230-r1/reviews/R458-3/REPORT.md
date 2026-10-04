[R458] NEGATIVE - exact head b59e99cb928939f5c4089964dea8f4628d06ede7

# R458-3: internal independent review of kebag-logic/milan-fpga#230 / processor PR #154 (round 3)

- **Repository and head.** Mister-M-alt/protocol-processor-control-plane-avb-milan PR #154 at exact head
  `b59e99cb928939f5c4089964dea8f4628d06ede7`, tree `06d80d967d2c7baa550a66dd2572a787e8adead6`. The clone was
  verified at both before any work.
- **Bases.** Source base `c4cb84ff8cecad19bedaa85dde594a8ed68012f6`. PR base `main` is `c050d97153dd0480ae741102c1647eeda9b7f273`;
  `hdl/srp` and `pp_pkg.sv` are byte-identical at both.
- **Scope.** The PR diff against `main` is 48 files: four SRP RTL files, two documents, and the SRP test benches,
  patches and READMEs. The larger `c4cb84ff..b59e99cb` range adds the two merges of `main` (ADP, AECP notify, nvm_port,
  Yosys gate). Those carry no SRP change and were reviewed in their own lanes.
- **Ordering.** My own pass over the diff and evidence was complete before I read the earlier rounds' findings, and
  this verdict and ledger were drafted first. I read no other reviewer's packet, and no private author material.

## 1. Scope reconstructed

There is no `AGENTS.md` or `CONTRIBUTING.md` in this repository. I read `README.md` and `docs/README.md` (authoring
conventions, single-source rules, the `make check` gate).

**Issue #230's frozen acceptance:**

- (A1) current SRP tests pass at 1x1 and 8x8;
- (A2) before-and-after hierarchical Vivado reports show a material reduction against the same baseline;
- (A3) 1x1 contains no logic for seven inactive slots;
- (A4) 100 MHz timing does not regress below zero WNS;
- (A5) scaling and latency trade-offs are documented in #229.

**Public scope decisions (manager comments on #230):**

- 5967853024 adds the SRP timer-arm FIFOs (lever 2).
- 5974045353 fixes the lane's rules:
  - behaviour is identical, with no port, parameter-meaning, register or protocol-visible timing change;
  - prove the equivalence: every processor suite and SRP campaign at the same counts, plus a lockstep bench of old
    against new `KL_srp_top` with planted controls;
  - the 100 MHz criterion is judged at the declared 50 MHz;
  - measure with #638's recipe.
- 5977836860 rules (b): the parallel per-stream evaluation stays as landed and is final for #230. The shared evaluator
  (a) moves to #640, and #230 closes manually at the processor merge.
- The round-2 assignment preferred committed directed arms to a frozen copy of the base RTL. This is recorded in
  the published `lockstep-r1/README.md`.

**Acceptance mapping at this head:**

| Item | Evidence I checked | Status |
|---|---|---|
| A1 | `srp_top` 2,200 (head and `main`), `srp_stream_fsms` 1,219 (head and `main`), `srp_admission` 991,231 at N = 1, 2, 3, 5, 8, `pp_top` 10,416, all rc 0. The suites run 8 contexts and the new arms 1/1, 2/2, 3/5, 9/9; the 1x1 product is 2/2 | met |
| A2 | Published reports (`06fe795b`), re-derived in `receipts/vivado-rederive.txt`. `u_srp` at the route goes from 4,340 LUT / 6,263 FF to 3,711 / 3,839. At 1x1 it goes from 4,558 / 6,438 to 3,988 / 3,979, and at 8x8 from 8,705 / 11,192 to 7,313 / 7,747 | met |
| A3 | Every per-stream array is sized by `N_SOURCES_P`/`N_SINKS_P`, bound from `N_STREAM_OUT_P`/`N_STREAM_IN_P` (`protocol_processor_top.sv:2485-2486`). The 1x1 run binds 2/2 (`baseline_chparam.txt`) | met |
| A4 | Judged at the declared 50 MHz per ruling. Route WNS goes from +0.079 to +0.354 and WHS from +0.014 to +0.036. The out-of-context estimates go from -2.059 to -1.874 (1x1) and -2.161 to -1.495 (8x8); their worst paths are outside `u_srp` (notify / rx_validator to tx_arbiter) | met as ruled |
| A5 | Recorded in `docs/architecture/10_srp_engine.md` §5.1. #229 is not updated by this lane, as assigned | manager duty (section 8) |

## 2. What I ran (all at the exact head unless named; receipts in `receipts/`, scripts in `scripts/`)

The simulator was the pinned Verilator 5.050 (identity in `receipts/tools-and-sources.txt`), through
`scripts/verilator-capped.sh`, which caps build parallelism at 2. Each job ran in a `git archive` copy, with its own
log and rc file (`scripts/job.sh`).

- **SRP suites.**
  - `tb/srp_top` `make`: TF arms 15/15 at 1/1, 2/2, 3/5 and 9/9, and the suite 2,200/2,200.
  - `tb/srp_stream_fsms` `make`: WK arms 23, 30, 43 and 79, and the suite 1,219.
  - `tb/srp_admission`: 1,138, 12,615, 41,012, 201,073 and 991,231.
  - `tb/pp_top` `make run`: 10,416.
  - `main` `c050d971`'s `srp_top` (2,200) and `srp_stream_fsms` (1,219) give equal tallies.
- **The srp_top campaign** (`mutants.py --jobs 4`): 126 checks, 126 PASS, assertion coverage 78/78. The slope-control
  counts equal the README's (1,333 / 1,521 / 1,201 / 578 at N = 2).
- **Lint** (`receipts/lint-srp-shapes.log`): `-Wall` over the four changed modules at 1, 2, 3 and 9 contexts gives 0
  warnings.
- **Lockstep** (the published round-1 bench, `00f848e5` `lockstep-r1/`), rerun with the reference rebuilt from
  `c4cb84ff`.
  - Head against base: 5 shapes (2/2, 3/5, 9/9 and 1/1 compressed; 2/2 at the default cadences) x 4 seeds x 1,000,000
    cycles. This gives 0 top-output and 0 internal mismatching cycles (`receipts/lockstep-head.log`).
  - The three scripts' published digests differ from `MANIFEST.sha256` only because they are path-redacted. The
    archive's `MANIFEST.json` records `path_redacted: true` with the original digests, which equal `MANIFEST.sha256`.
  - `build.sh` needed its execute bit restored, as the PR body already notes.
- **Vivado figures.** All rows of the PR body's Vivado table and of 10 §5.1's marginal-cost table re-derive from the
  published reports (`scripts/vivado_rederive.py`):
  - talker 128.7 / 168.1 (base 212.6 / 221.0);
  - listener 208.3 / 278.3 (227.4 / 278.3);
  - admission 68.6 / 68.9 (73.3 / 100.9);
  - whole engine 475.0 / 538.3 (592.4 / 679.1).
- **Reviewer probes** (`scripts/make_probes.py`, diffs in `receipts/probe-*.diff`):
  - **Registered-read probes.** `r3-wtsp-registered-read` and `r3-wsid-registered-read` are killed by
    `srp_stream_fsms` (WK) and the suites.
  - **Ready-handshake probes.** `r3-wtsp-write-ignores-ready` and `r3-wsid-write-ignores-ready` survive every
    committed suite (finding F1).
  - **Directed arm.** A disposable arm (`scripts/r3_stall_walk_main.cpp`, `receipts/r3-stall-arm.log`) shows that
    both can be killed deterministically.
- **The round-2b claim.** Verilator 5.050 reads a one-element 64-bit packed array at an out-of-range index as element 0
  (`receipts/oor-verilator-probe.txt`), as the README now states.
- **Hosted checks at the exact head** (`receipts/hosted-checks-b59e99cb.tsv`, read-only). `docs-gates` and
  `portability` executed and succeeded, twice each. `suites` was still `in_progress` when read.
- **Redaction.** The simulator's install prefix in the build logs is replaced by `$VERILATOR_ROOT`. No other edit was
  made to any receipt.

## 3. Findings

### R458-3-F1: MINOR. Lenses: Tests. The handshake term of the new walk-copy writes is pinned by no committed test

- **Where.** The new memories have their own write processes, each re-deriving the flop record's write enable:
  - talker: `hdl/srp/KL_srp_talker_fsm.sv:498`, `gate_open_acc_w = rst_n && gate_acc_w && gate_open_i`, used at
    `:500-505` (`wtsp_r`) and `:510-514` (`g_wid_ram.wid_r`);
  - listener: `hdl/srp/KL_srp_listener_fsm.sv:543-546`, `if (rst_n && ctl_acc_w && ctl_settle_i)`.

  The walk arms offer a gate or control op only with the event bus idle (`tb/srp_stream_fsms/walk_main.cpp:212-218`,
  `:235-239`), so `gate_ready_o` and `ctl_ready_o` are always 1 at an offer. No control in `tb/srp_top/mutants.py`
  edits the handshake term.
- **Evidence.**
  - **Talker probe.** `r3-wtsp-write-ignores-ready` replaces `gate_acc_w` with `gate_valid_i` at `:498`. Every
    committed suite that builds the edited file passes at full tally:
    - `srp_stream_fsms`: 23/30/43/79 and 1,219;
    - `srp_top`: 4 x 15 and 2,200;
    - `pp_top`: 10,416, equal to the head's 10,416.

    Receipts: `receipts/probe-suites-a.log` and `receipts/probe-pp_top-wtsp-write-ignores-ready.log`.
  - **The talker probe is not equivalent.** The published lockstep bench at 3/5 (seed 521) shows 3 mismatching
    `KL_srp_top` output cycles on `wr_data_o`, first at cycle 7,902, through `tk_ev_value_w` and `enc_ev_value_w`
    (`receipts/lockstep-probes.log`). So the transmitted MRPDU bytes differ.
  - **Mechanism.** A gate open is offered while a decoder value holds `gate_ready_o` low. The edited enable writes
    the new record before acceptance, and a walk in that window publishes it.
  - **Listener probe.** `r3-wsid-write-ignores-ready` (`ctl_acc_w` replaced by `ctl_valid_i` at `:544`) also passes
    `srp_stream_fsms` and `srp_top` at full tally. The lockstep bench did not observe it in 3 x 300,000 cycles at three
    shapes.
  - **Directed arm.** A disposable arm offers the op through a busy event bus during a txLA! walk:
    - the head passes it at 1/1, 2/2, 3/5 and 9/9 (151, 161, 179 and 231 checks);
    - the talker probe fails it at all four shapes;
    - the listener probe fails it at 3/5 and 9/9, where its RAM arm is elaborated.
- **Authority.**
  - **The lane's rules (5974045353).** Behaviour is identical, and the equivalence is proven with planted controls.
  - **The round-2 regime the PR adopts.** The PR body says: "Committed coverage of the new storage paths, at both
    arms", and "Every reviewer probe and every own control is a killed control". It also states "Each copy has a
    single writer, the one that also writes the flop record". Because each copy re-derives that writer's enable in
    a separate process, the handshake term is a new point where the copies can diverge, and a committed test should
    be able to fail for it.
  - **The assignment's preference.** It chose committed directed arms over the frozen lockstep bench, so the
    committed suites are the regression net.
- **Impact.**
  - No RTL defect at this head: the lockstep shows 0 mismatches over 20,000,000 cycles.
  - A later edit that drops the handshake qualifier from either walk-copy write would put an unaccepted record into a
    walk's MRPDU. That is wire-visible, and every committed suite would still pass.
  - Only the uncommitted bench sees the talker case, rarely, and nothing sees the listener case.
- **Required outcome.** A test-only commit, with no HDL change:
  - Add walk arms (for example WK9 talker, WK10 listener) in `tb/srp_stream_fsms/walk_main.cpp`. Each offers a gate
    open or settle with a different record for a declared context while a decoder value holds the ready low through
    a walk. It checks that this walk publishes the old record and that the walk after acceptance publishes the new
    one.
  - Plant both probes as killed controls in `tb/srp_top/mutants.py`, with checked-in patches.
  - Update the two READMEs' tables and counts, and extend the assertion-coverage tag list.
- **Verification.**
  - The talker control fails the new check at 4 of 4 shapes, and the listener control at 3/5 and 9/9 (n/e at 1/1 and
    2/2).
  - The head passes.
  - The campaign stays all-PASS, with coverage including the new tags.
  - `make check` passes.

### R458-3-R1: RESIDUE (wording only). Lenses: Docs

- **Where.** `docs/guides/hdl-engineer.md:88-90` says: "What the SRP walks read one context per cycle (the stream
  FSMs' tick walks and the admission walk) is distributed RAM read in the cycle of its address, with no latency:".
- **Problem.** The lead-in is broader than the exact list after the colon. The walks also read per-context flops
  (`app_r`, `fail_r`, `rec_valid_r` at `KL_srp_talker_fsm.sv:536`, `:615-617`; `slope_valid_r` at
  `KL_srp_admission.sv:196-200`). Line 90 is also 125 columns in a block wrapped near 85.
- **Exact fix.** Replace the quoted words with: "The per-context records the SRP walks read one context per cycle
  (the stream FSMs' tick walks and the admission walk) are distributed RAM read in the cycle of their address, with
  no latency:". Rewrap lines 88-93 to the block's width.

### Suggestions (not counted)

- **S1 (carried from R458-2 S1, not taken).** Build the `tb/srp_top` storage arms with `--x-initial unique` and
  `+verilator+rand+reset+2`, as the walk arms are built.
- **S2 (carried from R458-2 S2, not taken).** Name the 64-bit out-of-range limit beside WK6 in
  `tb/srp_stream_fsms/README.md`.

## 4. Prior public findings at this head (read after my own pass)

| Finding | Status at `b59e99cb` | Basis |
|---|---|---|
| R458-1 F1 (MINOR): storage paths and N <= 2 arm untested | Resolved | The WK1-WK8 and TF1-TF5 arms run at four shapes, and the campaign gives 126/126 and 78/78 here. F1 above is a new probe, not a regression of this finding |
| R458-1 F2 = R459-1 F1 (MINOR): Vivado receipts unpublished | Resolved | `06fe795b`, and every figure re-derives (`receipts/vivado-rederive.txt`) |
| R458-1 F3 / R459-1 F2 (MINOR): control-count sentences | Resolved | The PR body tables match the README and the campaign log |
| R458-1 O1 (observation, outside the diff) | Retained as an observation | Not re-measured |
| R459-1 R1, R2 (RESIDUE) | Resolved | As R459-2 recorded. No change since |
| R458-2 F1 = R459-2 F1 (MINOR): the 1/1 zero of `wsid-flops-of-control-sink` | Resolved | `tb/srp_top/README.md:621-625` names the simulator-only exception. PR body line 211 and the HANDOFF (r2b) lines 146 and 156 say "equivalent in simulation". The claim is confirmed by `receipts/oor-verilator-probe.txt` |
| R458-2 R2-R1, R459-2 R1 (RESIDUE): PR body head, suite and campaign lines | Resolved | Body lines 9, 255 and 263 now name `b59e99cb` / `9160f7d7`, `7365022` and `1199255` |
| R458-2 R2-R2 (RESIDUE): hdl-engineer attribution | Resolved as written | The remaining overbreadth is R1 above |
| R458-2 S1, S2; R459-1 S1, S2 | S1/S2 of R458-2 not taken (carried above); R459-1's taken or substituted | Not counted |

## 5. Lens results

- **Conformance: CLEAN.**
  - Ruling (b) holds: the matcher, the Table 10-3/10-4 transitions and the published levels stay parallel.
  - No port, parameter or register changes (diff of `hdl/`).
  - Lockstep against `c4cb84ff` shows no output change at 5 shapes, so the SRP clause-35 timing is identical.
  - A1-A4 are met as ruled; A5 is a manager duty.
- **RTL: CLEAN.**
  - Each new memory's write enable equals the flop record's enable (`KL_srp_talker_fsm.sv:587-592` against
    `:498-514`; `KL_srp_listener_fsm.sv:622-626` against `:543-546`; admission's unconditional stage-3 write).
  - Every read is gated by a valid bit written with it (talker `:615`, listener `KL_srp_listener_fsm.sv:655`; admission `fit_w`/`pend_w`; the FIFO count).
  - The top refuses out-of-range indices before S_GATE or S_CTL (`KL_srp_top.sv:848-879`), so no out-of-range write
    reaches a depth-1 memory.
  - Lint is clean at 1, 2, 3 and 9 contexts. 10 §5.1's widths match the RTL (124, 68, 104, 41 + `SLOT_AW_P`, 285/19,
    12 + 5).
- **Robustness: CLEAN.**
  - Unreset memories start random in the WK arms and in the lockstep (`--x-initial unique`). Mid-run resets (lockstep
    and WK5) give no mismatch.
  - The FIFO full guard is reached under the documented single force (TF4/TF5).
  - Behaviour under a held ready matches base (the lockstep at 5 shapes, and the directed arm passes at the head).
- **Tests: UNCLEAN (F1).**
  - Suites and the campaign pass at the claimed tallies, the arms run at both elaboration arms, and every earlier
    probe is killed.
  - One non-equivalent, wire-visible edit of the new RTL survives all committed suites.
- **Docs: CLEAN** (R1 is residue).
  - 10 §5.1's table and figures re-derive from the published reports.
  - The READMEs' tallies and control tables match my campaign.
  - The round-2b sentence is accurate.

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #230 body and manager comments 5967853024, 5974045353, 5977836860; PR body; `hdl/` diff against `main` and `c4cb84ff`; lockstep at 5 shapes | R458-3 | `b59e99cb928939f5c4089964dea8f4628d06ede7` |
| RTL | CLEAN | `KL_srp_top.sv:942-984, 840-880`; `KL_srp_talker_fsm.sv:352-372, 495-537, 540-646`; `KL_srp_listener_fsm.sv:531-560, 620-635`; `KL_srp_admission.sv:102-262`; lint at 1/2/3/9 | R458-3 | `b59e99cb928939f5c4089964dea8f4628d06ede7` |
| Robustness | CLEAN | lockstep with random unreset state and resets; WK5; TF4/TF5 forced stall; directed held-ready arm at the head | R458-3 | `b59e99cb928939f5c4089964dea8f4628d06ede7` |
| Tests | UNCLEAN (F1) | `tb/srp_stream_fsms/{walk_main.cpp,srp_walk_wrap.sv,Makefile}`; `tb/srp_top/{store_main.cpp,srp_store_wrap.sv,Makefile,mutants.py,mutations/*}`; suites, campaign, lockstep, 4 reviewer probes | R458-3 | `b59e99cb928939f5c4089964dea8f4628d06ede7` |
| Docs | CLEAN (R1 residue) | `docs/architecture/10_srp_engine.md` §5.1; `docs/guides/hdl-engineer.md:84-93`; `tb/srp_top/README.md:497-626`; `tb/srp_stream_fsms/README.md`; PR body; published Vivado reports | R458-3 | `b59e99cb928939f5c4089964dea8f4628d06ede7` |

## 7. Real limits

- **No Vivado run.** I re-derived the figures from the published reports; I did not resynthesise. Physical
  calibration was NOT RUN, and field skips are not hardware proof.
- **Banks not run.** I did not run the full processor, parent, gPTP, Yosys or builder banks, `run_suites.sh` over all
  33 suites, or `make check`. The manager's banks passed at this head; the hosted `docs-gates` succeeded.
- **Listener probe at the top level.** The listener probe's effect at `KL_srp_top` level was not observed in
  900,000 lockstep cycles. Its non-equivalence is shown at the FSM level by the directed arm, and `pp_top` was not
  run for it.
- **Hosted `suites`.** It was in progress when read and is not judged here.

## 8. Pending manager duties

- Route F1 to the lane, as a test-only change.
- Carry R1 to the residue checklist.
- Own hosted and act acceptance: `suites` at `b59e99cb` was in progress.
- Build the final current-dev candidate at the merge turn (source base `c4cb84ff`, live dev `fea346e7`).
- Record #230's scaling and latency trade-offs in #229 (acceptance A5), and close #230 manually at the processor
  merge, per ruling 5977836860.

## 9. Restoration

- No file in the clone was edited.
- My `mutants.py --help` call wrote `tb/common/__pycache__/mutant_pool.cpython-314.pyc`, which is ignored and
  untracked. I removed it and its directory.
- After removal (`receipts/clone-integrity.txt`):
  - HEAD `b59e99cb` and tree `06d80d96` are unchanged;
  - the index equals the HEAD tree;
  - 552 of 552 tracked blobs and modes match by `git hash-object`;
  - `git status --ignored --untracked-files=all` is empty;
  - the repository has 0 gitlinks, so no submodule pin applies.
- Every probe ran in `git archive` copies under the packet's `scratch/`.

R458-3 FINISHED
