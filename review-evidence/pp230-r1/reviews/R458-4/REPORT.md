[R458] NEGATIVE - exact head d18270d69eea9cdf35f846c77821d5488dab97cc

# R458-4: internal independent review of kebag-logic/milan-fpga#230 / processor PR #154 (round 4)

- **Repository and head.** Mister-M-alt/protocol-processor-control-plane-avb-milan PR #154 at exact head
  `d18270d69eea9cdf35f846c77821d5488dab97cc`, tree `5ff7ea39fc74c21be0d6a1df92f07496513c5fab`, verified in an isolated
  detached clone (`receipts/clone-integrity.txt`).
- **Bases.** Source base `c4cb84ff8cecad19bedaa85dde594a8ed68012f6`. PR base `main` `c050d97153dd0480ae741102c1647eeda9b7f273`.
  `hdl/srp` and `hdl/common` are identical at both, so `c4cb84ff` is the SRP reference.
- **Scope of the PR's own change.** Against `main` `c050d971`: 50 files. Four SRP RTL files
  (`KL_srp_top.sv`, `KL_srp_talker_fsm.sv`, `KL_srp_listener_fsm.sv`, `KL_srp_admission.sv`), two documents
  (`docs/architecture/10_srp_engine.md` §5.1, `docs/guides/hdl-engineer.md` §3.1) and the SRP benches
  (`tb/srp_stream_fsms`, `tb/srp_top`, 35 patches). The rest of `c4cb84ff..d18270d6` is `main`'s PRs #149, #152 and
  #153, which came in through merges.
- **Ordering.** I finished my own pass over the scope, the diff, the evidence and the tests before reading any earlier
  round's findings. Section 4 resolves or retains each of them.
- **Verdict basis.** One open MINOR (F1, Docs: the PR body says where the Vivado figures come from, and that statement is
  wrong). No RTL, test or conformance defect. Four suggestions.

## 1. Scope reconstructed (issue acceptance and public rulings)

- **Issue body.** Reduce the SRP per-stream LUT/FF term without changing SRP behaviour or stream counts. Acceptance:
  - SRP tests pass at 1x1 and 8x8;
  - before/after hierarchical Vivado reports show a material reduction against the same baseline;
  - no logic for inactive slots at 1x1;
  - WNS not below zero;
  - scaling documented in #229.
- **Assignment (5974045353).**
  - Lever 2 (the timer-arm FIFOs) and lever 4 (per-stream evaluation) are in scope.
  - Behaviour must be identical: no port, parameter-meaning, register or protocol-visible timing change.
  - Equivalence must be proven: suites and campaigns at the same counts, plus a lockstep with planted controls.
  - 100 MHz is judged at the declared 50 MHz.
- **Ruling (5977836860).** Option (b): parallel evaluation is final for #230. The shared evaluator goes to #640, and
  #230 closes manually at the processor merge.
- **Round 2 (5978448959).** Committed coverage of the new storage paths at N <= 2 and N >= 3, every probe as a killed
  control, and area claims stated as a delta against `c4cb84ff` unless SRP HDL changes.
- **Round 3 (5980793710).** R458-3-F1: WK9/WK10 and two ready-handshake controls. R458-3-R1: the exact lead-in.
- **No AGENTS.md or CONTRIBUTING.md in this repository.** The working rules come from `docs/README.md` (conventions,
  single-source rules, `make check`), `docs/guides/hdl-engineer.md` §3.1 (storage rule) and the manager's rulings
  above.

## 2. What I ran (all at the exact head; pinned simulator 5.050, identity in `receipts/environment.txt`)

Every run used a scratch copy. The clone was never written to.

| Item | Result | Receipt |
|---|---|---|
| `tb/srp_stream_fsms` `make` (walk arms at 1/1, 2/2, 3/5, 9/9, then the suite) | 35, 46, 67, 123 walk checks; 1,219 suite checks; all PASS, rc 0 | `receipts/head/suite-srp_stream_fsms.log` |
| `tb/srp_top` `make` (TF arms at four shapes, then the suite) | 15 per shape; 2,200 checks; all PASS, rc 0 | `receipts/head/suite-srp_top.log` |
| `tb/srp_admission` `make` (N = 1, 2, 3, 5, 8) | 1,138 / 12,615 / 41,012 / 201,073 / 991,231, all PASS, rc 0 | `receipts/head/suite-srp_admission.log` |
| `tb/pp_top` `make` (builds the four changed files) | 10,416 checks PASS, rc 0 | `receipts/head/suite-pp_top.log` |
| `tb/srp_top/mutants.py --jobs 8` | 128 checks, 128 PASS; assertion coverage 80/80; rc 0 | `receipts/head/campaign.log`, `receipts/campaign-230/` |
| `tb/srp_admission/mutants.py --jobs 8` | 12/12, rc 0 | `receipts/head/srp_admission-campaign.log` |
| `scripts/lint_hdl.sh` | 41/41 LINT OK, rc 0 | `receipts/head/lint_hdl.log` |
| `-Wall` lint of the four changed modules at 1, 2, 3, 5, 9 contexts (`shape_lint.sh`) | 20/20 OK | `receipts/head/shape_lint.log` |
| `make check`, `gen_matrix.py --check` | pass (1,131 links; 94 rows, 0 untested) | `receipts/head/make-check.log`, `gen_matrix.log` |
| Own lockstep, base `c4cb84ff` against head, talker + listener + admission, all 56 outputs every clock (`lockstep/`) | 6 shapes (1/1, 2/2, 3/5, 5/3, 8/8, 9/9) x 3 seeds x 1,000,000 clocks: **0 mismatching clocks**, 17-34 mid-run resets per run, unreset state random and different in each model, walks active (677 to 23,834 encoder pushes per FSM per run) | `receipts/lockstep/RESULTS.txt` |
| Lockstep planted controls (12 checked-in campaign patches, at a shape where each arm is elaborated) | 12/12 CAUGHT | `receipts/lockstep/` |
| Own probes (`probes.py`, 18 edits the 35 controls do not name) | 17/17 non-equivalent probes CAUGHT by a committed suite. The one probe I predicted equivalent survives, and the lockstep confirms it equivalent (0 mismatches at 2/2 and 3/5) | `receipts/probes/`, `receipts/lockstep/equivalent-probe-*.log` |
| README control table re-derived from my campaign receipts (`verify_table.py`) | 31 rows: per-shape counts and caught-at match in every row; one row's named-check cell omits a counted `TF1 precondition` (S3) | `receipts/verify-table.txt` |
| README slope table: each slope patch at each admission shape, measured on its own (`slope_shapes.sh`) | all 20 cells match | `receipts/slope/slope-shapes.txt` |
| README FIFO-arm stimulus table (offered, both-offering clocks, two-word selections, held arm) | all 4 rows match the `STORE` lines | `receipts/head/suite-srp_top.log` |
| FIFO arms built with `--x-initial unique` and `+verilator+rand+reset+2`, base RTL against head | Head passes at seeds 7 and 11 at every tested shape. At seed 3, base and head fail the same 4 precondition lines (no own LeaveAll within 16 s). This predates the PR | `receipts/xinit/` |
| Vivado figures re-derived from the published reports (`marginal.py`, milan-fpga `06fe795b`) | See §3 (Conformance) | `receipts/marginal.txt` |
| Hosted checks at the exact head (read-only) | `docs-gates` x2 and `portability` x2 success; `suites` x2 still in progress when read | `receipts/hosted-checks-d18270d6.tsv` |

## 3. Lens results

### Conformance: CLEAN

- **Behaviour is identical.**
  - No port, parameter or register change. The headers diff to nothing but comments, and every changed process keeps its
    enables, addresses and data.
  - My lockstep compares all 24 talker, 27 listener and 5 admission outputs every clock against `c4cb84ff`, at six
    shapes and both elaboration arms: 0 mismatches. Its 12 controls are caught.
- **The Vivado acceptance figures re-derive from the published reports** (`06fe795b`, `author-r1/vivado/`):
  - `u_srp` 1x1, base to head: 4,558 to 3,988 LUT and 6,438 to 3,979 FF.
  - `u_srp` 8x8, base to head: 8,705 to 7,313 LUT and 11,192 to 7,747 FF.
  - Top glue: 907 to 354 LUT and 2,836 to 545 FF.
  - Wrapper F7 muxes: 639 to 343 (296 fewer).
  - Talker, listener and admission together: -37 LUT and -168 FF at 1x1; -791 LUT and -762 FF at 8x8.
  - Route: `u_srp` 4,340 (180) to 3,711 (298) LUT, 6,263 to 3,839 FF; WNS +0.079 to +0.354 ns, WHS +0.014 to +0.036 ns,
    0 routing errors at both.
  - 10 §5.1 marginal table: talker 129/168 (213/221), listener 208/278 (227/278), admission 69/69 (73/101), whole engine
    475/538 (592/679).
- **Shapes.** The OOC runs bind `N_STREAM_OUT_P = N_STREAM_IN_P = 2` at 1x1 and 9 at 8x8, base and head alike, so the
  divisor of 7 is right and no inactive slot exists at 1x1.
- **The SRP delta holds at this head.** `git diff 65324390 d18270d6 -- hdl/srp` is empty. F1 concerns how the body
  describes the whole-design rows; the acceptance evidence itself is sound.
- **Out of this lane.** "Documented in #229" is outside this lane, which the body states. The manager owns closure.

### RTL: CLEAN

- **Timer-arm FIFOs** (`KL_srp_top.sv:947-984`). There are two one-dimensional memories, each with the same push
  enable, write pointer and data as before. The registered head read is unchanged, and so are the full guard (`:963-964`),
  pointers and counts. `tf_q_r` is consumed only in TM_POP after TM_SEL picked a FIFO with a non-zero count
  (`:1105-1124`), so the missing reset is invisible.
- **Talker** (`KL_srp_talker_fsm.sv:495-537`).
  - `wtsp_r` and `g_wid_ram.wid_r` are written under `rst_n && gate_acc_w && gate_open_i`, the same condition as the
    flop record (`:587-592`).
  - The read is at `wsrc_r`, and `wval_w` is latched into `push_val_r` only under `rec_valid_r[wsrc_r]` (`:615-619`).
  - The bit slices check: 68 = 16+16+3+1+32 and 124 = 64+48+12.
  - `{prio, rank, 4'd0}` is `wtsp_w[35:32]`.
- **Listener** (`KL_srp_listener_fsm.sv:540-559`). It writes under `rst_n && ctl_acc_w && ctl_settle_i`, the only writer
  of `sid_r` (`:622-628`). `rec_valid_r` persists past A8, and the RAM keeps the word.
- **Admission** (`KL_srp_admission.sv:111-170`). The stage-3 write is unchanged in timing. Every reader of
  `slope_q_r[aidx_r]` (`:195`, `:210`, `:245`, `:258`) is gated by `fit_w`, which requires `slope_valid_r`.
- **Out-of-range writes cannot alias in synthesis.** `KL_srp_top` enters S_GATE/S_CTL only when
  `req_index_i < N_SOURCES_P` / `N_SINKS_P` (`:848-879`), so every accepted gate and control op carries an in-range
  index.
- **Lint.** `-Wall` clean at 1, 2, 3, 5 and 9 contexts.

### Robustness: CLEAN

- **Equivalence across shapes and resets.** 18,000,000 lockstep clocks over six shapes (including the shipping 2/2 and
  9/9), with 17-34 random mid-run resets per run and random, differing unreset state, gave 0 mismatches.
- **The reset gate on the new writes is redundant, and that is safe.** Dropping `rst_n` from `gate_open_acc_w` is
  equivalent (lockstep 0 mismatches): a word written during reset is never read before an open rewrites it.
- **Full guard.** It is reached by TF4/TF5 under the documented forced stall, and `tf-full-guard-31`,
  `tf-*-write-ignores-full` and my `q-tf-ls-full-of-tk-count` are killed.
- **Randomised power-up of the FIFO arms.** The head passes. The seed-3 precondition failure is identical on base, so
  the PR does not cause it (R458-1 O1 family).

### Tests: CLEAN

- **Counts.** Every count the PR and READMEs claim for this head reproduces: WK 35/46/67/123, TF 15 per shape, suites
  1,219, 2,200, 991,231 and 10,416, campaign 128/128 with 80/80, admission campaign 12/12.
- **R458-3's two handshake probes are killed** at the required shapes (`receipts/campaign-230/`):
  - `wtsp-write-ignores-ready` fails WK9 at 4 of 4 shapes;
  - `wsid-write-ignores-ready` fails WK10 at 3/5 and 9/9.
- **My 17 non-equivalent probes are all caught**, each by the arm that owns the path:
  - walk copies: neighbour reads, writes at the walk index, a write that ignores the handshake on the RAM arm only, a
    write on close on the RAM arm only, field drops and swaps;
  - FIFOs: the listener head read ahead, the listener write at the read pointer, the cancel bit dropped on either FIFO,
    the listener full guard on the talker count, a deadline bit;
  - slopes: the read at the neighbour, for both the sum and the grant.
- **Both elaboration arms run in the default `make`.**

### Docs: UNCLEAN (F1)

- **What checks.**
  - 10 §5.1's storage map names, widths and primitives match the RTL: `TFW_C = 41 + SLOT_AW_P`, 124, 68, 104, 285/19,
    and the `ram_style` sites.
  - Its marginal table re-derives.
  - The hdl-engineer lead-in is R458-3-R1's exact text, rewrapped (lines 88-94, 58 to 86 columns).
  - Both READMEs' tables re-derive (one naming suggestion, S3).
- **F1.** The PR body's statement of where the Vivado figures come from is wrong.

## 4. Findings

### R458-4-F1: MINOR. Lenses: Docs. The PR body says rounds 2 and 3 "change no HDL" and labels the Vivado head "this processor", but non-SRP HDL changed through the merges

- **Where.** These are lines of the PR #154 body as fetched at review time (`receipts/pr154.json`):
  - **Line 91:** "Head: the same with this processor."
  - **Line 123:** "Round 2 answers their findings with tests and documentation; no HDL changed."
  - **Line 244:** "`4994ada` brings C10 (PR #149) and #85 (PR #152, tests only)".
  - **Line 307:** "Rounds 2 and 3 change no HDL, so they stand."
- **Evidence.**
  - `git diff --stat 65324390 d18270d6 -- hdl` lists four files, +145/-69:
    - `KL_aecp_notify.sv`, PR #153's LUTRAM identity index (`9e29e2a`), a logic and area change in `u_aecp`;
    - `protocol_processor_top.sv`, C10's declaration reorder (`34b5246`);
    - `KL_pp_nvm_port.sv`, C10's elaboration guard (`746216b`, `6ba4659`);
    - `KL_adp_engine.sv`, #85's comments (`4298ed2`).
  - So PR #152 was not "tests only".
  - `git diff 65324390 d18270d6 -- hdl/srp` is empty.
  - The Vivado runs (`06fe795b`) were made with the round-1 processor.
- **Authority.**
  - Round-2 item 4 (5978448959): "The area claims stay base `c4cb84ff` against head as a delta, unless the merge changes
    SRP HDL. State this."
  - `docs/README.md`: figures are single-sourced and must be accurate.
  - Owner rule 2026-10-02: a statement of where a measurement comes from is not wording-only. If unsure, the rule makes
    it MINOR.
- **Impact.**
  - The `u_srp`, per-block and marginal figures and the base-to-head SRP delta stand, because SRP HDL is unchanged.
  - The whole-design rows ("Route head 51,005 LUT / 57,262 FF ...", "1x1 head 24,258 ...", "8x8 head 31,109 ...") are
    the round-1 tree's, not this head's.
  - Read as written, the body presents them as this head's. A merge-time rebuild at `d18270d6` would differ by at least
    #153's notification change.
  - No RTL or test defect follows.
- **Required outcome.** A PR body edit; no head change. For example:
  - **Line 91:** "Head: the same with this lane's processor at round 1 (`65324390`); its `hdl/srp` equals this head's."
  - **Line 123:** "...with tests and documentation; the lane changed no HDL."
  - **Line 244:** "#85 (PR #152, tests and ADP comments)".
  - **Line 307:** "Rounds 2 and 3 change no SRP HDL (`git diff 65324390 d18270d6 -- hdl/srp` is empty), so the `u_srp`,
    per-block and marginal figures and the base-to-head delta stand. The merges of `main` bring non-SRP HDL (C10's
    elaboration guard and declaration reorder, #85's ADP comments, #153's notification index), so the whole-design rows
    are those of the round-1 tree."
- **Verification.**
  - `git diff --stat 65324390 d18270d6 -- hdl` gives the 4 non-SRP files, and `-- hdl/srp` gives nothing.
  - Re-read the four body lines.

### Suggestions (not counted)

- **S1 (Tests; carries R458-2 S1 = R459-3 S1, not taken).**
  - **Idea.** Build the `tb/srp_top` storage arms with `--x-initial unique` and run them with `+verilator+rand+reset+2`,
    as the walk arms are built.
  - **New data.** Seeds 7 and 11 pass at head. Seed 3 fails four preconditions identically on base and head, from the
    random-power-up sensitivity outside the PR (R458-1 O1).
  - **So.** Adopting S1 needs a fixed passing seed, or that pre-existing issue fixed first.
- **S2 (Docs; carries R458-2 S2 = R459-3 S2, not taken).** Name the 1/1 out-of-range 64-bit alias beside WK6 in
  `tb/srp_stream_fsms/README.md`.
- **S3 (Docs).** `tb/srp_top/README.md:584` (and the matching PR body row), `tf-tk-head-read-ahead`.
  - **What is off.** The per-shape cells 4/4/3/2 include `TF1 precondition` failures: two at 1/1 and 2/2, one at 3/5
    (`receipts/campaign-230/tf-tk-head-read-ahead.log`). The "Named failing checks" cell lists only TF1 and TF4.
  - **Why only a suggestion.** It understates, so it does not overstate coverage.
  - **Suggested fix.** List "TF1 (and its preconditions)", or footnote that the counts include precondition checks.
- **S4 (RTL comment).** `KL_srp_top.sv:947-949` says the old array "mapped to 2 x 32 x TFW_C flip-flops".
  - **The measured count is lower.** The #638 baseline measured 2,304 FF at 1x1, which is less than 2 x 32 x TFW_C
    (TFW_C >= 47), because constant word bits were trimmed.
  - **Suggested fix.** Say "mapped to flip-flops (2,304 at 1x1) and a read multiplexer", as 10 §5.1 does.

## 5. Prior public findings at this head (read after my own pass)

| Finding | Status at `d18270d6` | Basis |
|---|---|---|
| R458-1 F1 (MINOR): storage paths and the N <= 2 arm untested | Resolved | WK1-WK10 and TF1-TF5 run at four shapes in the default `make`; campaign 128/128 with 80/80 here |
| R458-1 F2 = R459-1 F1 (MINOR): Vivado receipts unpublished | Resolved | `06fe795b`; every figure I checked re-derives (§3). F1 here is about the body's labelling of the figures, not the receipts |
| R458-1 F3 = R459-1 F2 (MINOR): control-count sentences | Resolved | Per-shape and caught-at cells re-derive row by row from my receipts (`receipts/verify-table.txt`); S3 is a naming nicety |
| R458-1 S1: the full boundary is never exercised | Resolved | TF4/TF5 reach it; `tf-full-guard-31` is killed |
| R458-1 O1 (observation, outside the diff) | Retained as an observation | Reproduced in the FIFO arms at seed 3, identically on base (`receipts/xinit/`) |
| R459-1 R1, R2 (RESIDUE) | Resolved | The body names `docs/architecture/10_srp_engine.md` section 5.1 and the qualified Validation header |
| R459-1 S1, S2 | S1 taken (hdl-engineer §3.1). S2: the round-1 bench is stated as published by the manager | I did not fetch the round-1 bench. My own lockstep stands in for it (limit) |
| R458-2 F1 = R459-2 F1 (MINOR): the 1/1 zero of `wsid-flops-of-control-sink` | Resolved | `tb/srp_top/README.md:623-628` names the simulator-only exception; the body row says "equivalent in simulation" |
| R458-2 R2-R1, R459-2 R1 (RESIDUE): body head line | Resolved | The body names head `d18270d6` |
| R458-2 R2-R2 / R458-3-R1 (RESIDUE): hdl-engineer lead-in | Resolved | Exact replacement at `docs/guides/hdl-engineer.md:88-90`, rewrapped to 86 columns or fewer |
| R458-3-F1 (MINOR): handshake term of the walk-copy writes unpinned | Resolved | WK9/WK10; `wtsp-write-ignores-ready` fails WK9 at 4/4 and `wsid-write-ignores-ready` fails WK10 at 3/5 and 9/9; my RAM-arm-only variant `q-wid-ram-write-ignores-ready` is caught by WK9 at 3/5 and 9/9 |
| R459-3 S1, S2 (= R458-2 S1, S2) | Not taken | Carried as S1 and S2 above |
| R459-3 S3: rewrap hdl-engineer:90 | Resolved | Lines 88-94 are 58 to 86 columns |

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #230 body and comments 5967853024-5981062645; PR body; `06fe795b` hierarchy, utilization, route-status and timing reports (base/head, 1x1/8x8 OOC, 1x1 route); `chparam`; own lockstep against `c4cb84ff` | R458-4 | `d18270d69eea9cdf35f846c77821d5488dab97cc` |
| RTL | CLEAN | Full diff of the four SRP files against `c050d971`/`c4cb84ff`; `KL_srp_top.sv:840-879`, `:947-984`, `:1098-1124`, `:1256-1257`; the talker `:350-646`; the listener `:495-664`; the admission `:100-270`; lint at 1/2/3/5/9 | R458-4 | `d18270d69eea9cdf35f846c77821d5488dab97cc` |
| Robustness | CLEAN | Lockstep at six shapes with resets and random power-up; the equivalent-probe lockstep; full guard via TF4/TF5; randomised FIFO arms, base against head | R458-4 | `d18270d69eea9cdf35f846c77821d5488dab97cc` |
| Tests | CLEAN | `walk_main.cpp`, `srp_walk_wrap.sv`, `store_main.cpp`, `srp_store_wrap.sv`, both Makefiles, `mutants.py`, 35 patches; suites, campaigns, 18 own probes, 12 lockstep controls | R458-4 | `d18270d69eea9cdf35f846c77821d5488dab97cc` |
| Docs | UNCLEAN (F1) | `docs/architecture/10_srp_engine.md` §5.1; `docs/guides/hdl-engineer.md:84-94`; both READMEs' #230 sections and tables (re-derived); RTL comments; PR body | R458-4 | `d18270d69eea9cdf35f846c77821d5488dab97cc` |

## 7. Real limits

- **No Vivado run.** I re-derived the figures from the published reports and did not resynthesise. Physical
  calibration was not run, and skipped field contexts are not hardware proof.
- **Banks not run.** I did not run the full processor `run_suites.sh` bank, the parent consumer set, gPTP, the Yosys
  gate, builder, act or Docker. I ran the SRP suites, the `pp_top` suite and the two SRP campaigns.
- **My lockstep is module-level.** It covers the talker, listener and admission under random legal stimulus (pooled
  values, in-range gate/control indices), not MRPDU-level traffic through `KL_srp_top`. The FIFO split is judged by
  inspection (enables, addresses, data and read unchanged), by TF1-TF5, by 10 killed FIFO controls and by 6 own FIFO
  probes. I did not re-run the round-1 bench (`lockstep-r1/`); it was not under the evidence path I was given.
- **Hosted `suites`.** Both runs were still in progress when read and are not judged.
- **Load.** The host was heavily loaded by other work while I ran. No verdict depends on timing.

## 8. Pending manager duties

- **F1.** Resolve it with a PR body edit (no head change needed) and re-review.
- **Hosted acceptance.** Judge the two hosted `suites` runs at `d18270d6` and own act/hosted acceptance.
- **Merge turn.** Build the final current-dev candidate (source base `c4cb84ff`, live dev `fea346e7`) and its parent
  consumer set.
- **Closure.** Close milan-fpga#230 manually at the processor merge per ruling 5977836860. The #229 documentation item
  is outside this lane.
- **Suggestions.** Carry S1-S4 at the manager's discretion. R458-1 O1 stays an observation outside this PR.

## 9. Packet and restoration

- **Scripts**, portable, with paths as arguments:
  - `probes.py`, `marginal.py`, `verify_table.py`, `slope_shapes.sh`, `shape_lint.sh`;
  - `lockstep/gen_lockstep.py`, `lockstep/ls_main.cpp`, `lockstep/run_lockstep.sh`, `lockstep/campaign.sh`.
- **Receipts** are under `receipts/`. Simulator install prefixes and local roots are replaced by `$VERILATOR_INSTALL`,
  `$PACKET`, `$CLONE` and `$PINNED_VERILATOR`; no other edit was made. Digests are in `MANIFEST.sha256`.
- **The clone was never written.**
  - HEAD `d18270d6`, `HEAD^{tree}` and `git write-tree` are both `5ff7ea39`.
  - `git status --porcelain --ignored` is empty.
  - All 554 tracked blobs and modes match the index.
  - The repository has no submodule gitlinks (0 entries of mode 160000), so none could drift.

R458-4 FINISHED
