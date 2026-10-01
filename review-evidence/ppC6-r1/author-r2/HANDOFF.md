# [A467] Lane C6 round 2 handoff: notifications and Identify

Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, branch `c6-notifications`
(PR #139), round-2 start `5e806296b73d04ccf095ad00e081cb790fbbaf8d` (origin URL and HEAD
confirmed). Assignment: #80 comment 5924910356. Reviews: R420-1 (#139 comment 5921785256, two
MINOR), R421-1 (#139 comment 5921513647, one MINOR). Roles: executor [A467], manager [A10],
reviewers [R420] (internal), [R421] (external).

## Status

REVIEW READY at `88e0bf82888d6ad83b500425a786814da467610b` (#80 comment 5929578090).
TAKEN posted on #80 (comment 5924913398). The session was cut at 07:41 by a
user-session restart (not a gate failure); the tree was clean at `2e99ab0`, and the
interrupted notify campaign is re-run whole. A second cut, the host reboot of 2026-10-01
~12:02 (not a gate failure), stopped the d3 campaign at 77 of 83; the tree was clean at
`88e0bf8`, and the six it had not reached were run at the same head (Gates).

| Item | State |
|---|---|
| 1. Merge `main` `3f3ea56b` | done, `a011b14` |
| 2. Burst spacing (R420-1 F1, R421-1 F1) | done, `6094928` |
| 3. R420-1 F2 (HDL contract names the synchronizer) | done, `48718d6` |
| 4. Suggestions | done, `2e99ab0` |
| Parent idiom gates on round 2's test code | done, `88e0bf8` (below) |
| Gates | done at the head `88e0bf8`, all rc 0 (below) |

One reading for the manager (detail under What remains): item 2 needed one new input on the
internal `KL_aecp_notify` (`uns_tx_busy_i`). The STOP was read as covering top-level ports,
parameters and changes the parent must act on. No top port, top parameter or register changed.

## 1. Merge resolution

`git fetch origin main` gave `3f3ea56ba61829718a6a288600ab4fdac73aa5ba` (first parents: #137
`3f3ea56`, #135 `d5f73ba`; #136 came in through both lanes' merges of `0451d83d` and
`d5f73bac`). Merge commit `a011b14` (parents `5e80629`, `3f3ea56`), no rebase. Main touched 48
files; six are shared with the lane. Three auto-merged with no edit (`docs/00_MILAN_COMPLIANCE_REVIEW.md`
REQ-MAAP-007 and the GAP-15 row, `docs/architecture/09_verification.md` the V3 row,
`tb/pp_top/pp_top_wrap.sv` the `acmp_bound_*` ports). Three conflicted, each resolved by
keeping both sides:

| File | Conflict | Resolution |
|---|---|---|
| `tb/pp_top/Makefile` | `.PHONY` line: lane `identify-build identify`, main `maap-internal` | one line with all of them |
| `tb/pp_top/sim_main.cpp` `main()` | `one_section`: lane `ident_only`, `notify_only`; main `acmp_only`, `maap_only` and `if (maap_only) run_maap_internal(h);` | the union of the six flags, then main's MP call, then the sections in main's order followed by the lane's |
| `tb/pp_top/README.md` | both sides appended at the end (main: sections MP and AC with the ACMP mutation table; lane: "Lane C6") | main's sections first, then the lane's, both whole |

`.gitattributes` and `.github/workflows/hdl.yml` came from main alone (the lane never touched
them), so every main entry and CI step is kept. Re-anchoring: every text-plant mutation driver
was checked against the merged tree, each planted text occurring exactly as often as the
driver requires: `tb/pp_top/acmp_mutants.py` (main's, new; 19 entries, anchors in the top the
lane also edits), `notify_mutants.py` 30, `d3_mutants.py` 83, `gsi_mutants.py` 20; none moved.
The `.patch` campaigns (`tb/adp_engine`, `tb/maap`) touch files the lane does not. Verified on
the merge: `make -C tb/pp_top` rc 0, 8,126 checks (default 8,044, fixture 20, identify 62).

## 2. Burst spacing (R420-1 F1, R421-1 F1), commit `6094928`

**Clause.** IEEE 1722.1-2021 §7.5.1 and §7.5.1.2.1 (txIdentify: the notification is sent
three times "with a 150 ms delay between transmissions"); Figure 7-142 (the 1 s timeout
from IDENTIFY entry, unchanged).

**Defect.** Frames 2 and 3 were due at `t0 + 150` and `t0 + 300` ms, absolute deadlines
from the first frame (`KL_aecp_notify.sv` round-1 `:726-728`). The timer service fires a
past deadline on the next sweep, so a late frame 2 made frame 3 due at once. The RTL
banner, F08.1, 09 §8.3, the suite README, the ID6 name and the PR body all said this could
never happen.

**Why "departure" and not retirement.** The engine retires a job (`uns_done`, A_TXW to
A_FREE) at the TX arbiter's lane grant (`KL_pp_tx_arbiter.sv`: `gnt_o` pulses when the pool
accepts the start). A stalled MAC (`tx_ready_i` low) holds a frame the engine has already
let go, so scheduling from retirement still bunches. Measured: the control
`ident_departure_is_retirement` leaves frames 1 and 2 63 clocks apart when the MAC stalls
inside frame 1 (ID7d).

**RTL fix** (line numbers at the head `88e0bf8`; `2e99ab0`'s `ASYNC_REG` comment moved the
sequencer 3 lines down from `6094928`):
- `hdl/aecp/KL_aecp_notify.sv:290`: a new input, `uns_tx_busy_i` (an unsolicited frame is
  granted and its last byte has not left yet), read only with `EN_IDENTIFY_NOTIF_P`
  (`:851-854`).
- `:736` `dep_w = (done_w || left_r) && !uns_tx_busy_i`, and `:789-790` `left_r`: the face
  is released at retirement as before, and the schedule waits for the frame itself to leave.
- `:802-827` on every departure, IDENT-BURST is armed and `gap_r` set (`:806-807`). `:746` its
  deadline is `now_ms_i + 151`, taken at or after the departure, so it is at least
  T-IDENT-BURST after the frame left and under one tick more. t0 (REARM base, `:814`) is the
  first frame's departure; REARM stays at `t0 + T-IDENT-REARM`.
- `:794`, `:840`: a burst's first frame (a fresh press or the held re-arm) also waits for
  `gap_r`. So a stall that pushes a third frame past the timeout cannot put the next burst
  straight behind it, and a release-and-press inside a burst starts the next burst
  T-IDENT-BURST after the third frame (it used to be 106 clocks after).
- `hdl/top/protocol_processor_top.sv:4314-4325` `gen_uns_departure` (only with
  `EN_IDENTIFY_NOTIF_P`; at 0 it is the constant 0): `busy_r` set on
  `arb_gnt_w[LANE_AECP_UNS_C]`, cleared on the arbiter's eof handshake. Grants are
  frame-atomic, so the first eof after a UNS grant is that frame's. This is the same
  property the ACMP prepend shim relies on. `:3223` the net, `:3870` the connection.
- No top port, no parameter, no engine change. Lint is clean for `KL_aecp_notify`,
  `KL_aecp_engine` and `protocol_processor_top` at `EN_IDENTIFY_NOTIF_P` 0 and 1.

**Tests** (`tb/pp_top/notify_phases.hpp`, third build; section ID now 106 checks, up from 62):
- `SLACK` is now 400 clocks, itemized: one tick, plus the sweep's walk to the identify
  slots (at most 91), plus the build and serialization (under 200). The largest gap
  measured is 15,309.
- **ID5i-ID5l** (R421-1 P1 shape, inside ID5 while 15 rows are registered): a SET_NAME
  fan-out fed at frame 1 + 14,450 / 14,700 / 14,950 clocks. Gap 1->2 reaches 16,147
  (ID5l anti-vacuity); the smallest gap is 15,240 (it was 14,109 from t0).
- **ID7** (the assignment's arm, MAC stalled mid-burst):
  - ID7-ID7e: 400 ms inside frame 1. Gap 1->2 is 15,270 (63 from retirement).
  - ID7f-ID7i: 400 ms after frame 1 (R420-1's probe). Gap 2->3 is 15,264 (164 from t0).
  - ID7j-ID7m: 250 ms after frame 2.
  - ID7n-ID7t: held through 900 ms after frame 1, so the timeout passes mid-burst. The
    next burst comes 15,301 after the third frame; it is never "at once".
- **ID3f** re-graded: the new burst starts T-IDENT-BURST after the third frame left
  (15,301 clocks).
- **ID6** renamed `a_press_before_the_restore_goes_out_at_the_release`. It holds the
  engine only before frame 1, so its old name "never bunches" overclaimed.
- **Failing arm on the round-1 RTL** (the new `notify_phases.hpp` built against merge
  `a011b14`'s HDL in a scratch copy): 7 of 106 fail. They are ID3f (106 clocks), ID5k
  (14,109), ID7d (63), ID7e (207), ID7i (164), ID7q (63) and ID7r (10,111). Receipt:
  `receipts/id-new-arms-on-round1-rtl.log`.

**Mutants** (`tb/pp_top/notify_mutants.py`, all KILLED):

| Mutant | Planted | Failing checks |
|---|---|---|
| `ident_burst_from_t0` (the assignment's control: round 1's schedule restored) | IDENT-BURST deadline `t0 + 150 / 300` | 5: ID3f, ID5k, ID7i, ID7q, ID7r |
| `ident_departure_is_retirement` | `dep_w = done_w` | 2: ID7d, ID7q |
| `ident_departure_unwired` | top `.uns_tx_busy_i (1'b0)` | 2: ID7d, ID7q |
| `ident_next_burst_at_once` | `gap_r` dropped from the I_WAIT and I_HOLD starts | 2: ID3f, ID7r |

Re-anchored: `ident_two_frames` (FRAME2 lost its `armb_r` line), `ident_rearm_from_third_frame`
(the REARM arm of the new deadline mux) and `ident_t0_at_request` (the WAIT anchor). Under
the new schedule t0 drives only REARM, so `ident_t0_at_request` is now named on "ID2d: burst 3
starts" (45,900 clocks) instead of ID6d. The identify subset, 15 of 15, was KILLED with both
goldens passing (`--only` the 15 `ident_*`).

**Docs corrected:**
- the RTL banner (`KL_aecp_notify.sv:154-170`) and the t0 comment;
- 08 F08.1 T-IDENT-BURST;
- 09 §8.3 TIM row (no more "never less"; it now lists the stall and contention arms);
- 06 §7 "Identify";
- integrator guide §6 (a release-and-press now starts the next burst T-IDENT-BURST after
  the running one ends; a stalled `tx_ready_i` delays and never bunches);
- `tb/pp_top/README.md` section ID (SLACK, ID1-ID3 measured values, ID5i-l, ID6, ID7, the
  round-1 failing arm, the mutation rows).

## 3. R420-1 F2, commit `48718d6`

`docs/guides/hdl-engineer.md` §2, the CDC row: it now names the one synchroniser inside the
modules (`btn_q1_r`, `btn_q2_r`, which take `identify_button_i` into `KL_aecp_notify`, built
only with `EN_IDENTIFY_NOTIF_P` = 1, under the ruling on #80) and links the integrator guide
§1/§6 and 02 §2 rule 3. Every other crossing stays the integrator's. `hdl/README.md`: "no CDC
primitive and no memory primitive", plus the same one synchroniser; every other crossing
is the integrator's. No RTL change. `make check` rc 0 (links 999, matrices, parameters
27 = 27 = 27).

## 4. Suggestions, commit `2e99ab0` (and the PR body)

| Suggestion | Disposition |
|---|---|
| R420-1 S1: `!core_arm_w` and the `gen_r` flip are not exercised | **Retained, recorded.** I re-ran the reviewer's own `extra_mutants.py` (unchanged, read from the review packet) against the round-2 tree. All three SURVIVE with every section-ID check passing. They are now listed in `tb/pp_top/README.md` as retained controls, each with its reason. The arm collision needs a registry op to arm in the single cycle after a departure, which a directed check could only find by sweeping the command arrival cycle by cycle. The stale-REARM window is a few cycles, and the departure clears `fired_r`. The missing second synchroniser flop is CDC hygiene that a two-state simulation cannot see |
| R420-1 S2 / R421-1 S2: no synchroniser marking or constraint | **Taken.** `(* ASYNC_REG = "TRUE" *)` on `btn_q1_r` and `btn_q2_r` (`KL_aecp_notify.sv`, following the tree's `ram_style` precedent). Integrator guide §1 names the two flops and makes declaring the pin-to-`btn_q1_r` path an asynchronous input (false path or max-delay) the integrator's job. Lint is clean at 0 and 1 |
| R420-1 S3 / R421-1 S4: the LUT figures | **Taken in the PR body.** The flow is now stated. The LUT deltas are mapper variance between netlists proven equivalent (the two reviewers' block-level runs disagree with each other: 6,454 vs 6,549 and 6,598 vs 8,002), so FF, CARRY4, RAM and DSP are the cost figures. The table is re-measured at the round-2 head (below) |
| R420-1 S4: ST2b accepts rounds 99,994 clocks apart | **Retained, recorded** in `tb/pp_top/README.md` ST2. The limiter predates the lane and counts "once per second" on the 1 ms timebase like every T- value (08 §3), so two rounds are at least 1,000 ticks apart, which can be up to one tick short of a second in core clocks. Changing a shared limiter that other suites grade belongs to its owner |
| R421-1 S1: a release and a press inside a burst | **Taken, as a stated reading.** In 06 §7 and F06.16 the edge is latched while txIdentify runs, and the next burst now starts T-IDENT-BURST after the third frame (item 2's gap), not at the 1 s timeout. ID3 grades it |
| R421-1 S3: `gstri_r` still set for `PP_UNS_SINFO_C` | **Kept, and the reason is now in the RTL** (a comment in `KL_aecp_engine.sv`). The flag is not dead: it selects `tix_w`, the {type, index} operand shape that `E_SINFOUNS`'s `BUILD_FLD ra=13` reads, and the job gathers nothing. Comment only, so the engine is unchanged |

## 5. The parent's idiom gates on round 2's test code, commit `88e0bf8`

The parent consumer set at `2e99ab0` (C6 patch applied) failed three commands. Two of the
failures were in this lane's round-2 code, and the round-1 versions of both files were clean:

| Gate | Finding at `2e99ab0` | Fix in `88e0bf8` |
|---|---|---|
| `check_cpp_idiom.py` (Rule 11) | `tb/pp_top/notify_phases.hpp:415` and `:416`, multi-declarator 2 > 0 (the gate's pattern reads ID5i's one-line array initializer as one; `:416` really declares two); `:489` `a_tx_stall_mid_burst_never_bunches_it`, 101 lines > 100 | the initializer split across two lines (the #137 precedent `a7ccd9e`), the two longs declared apart; ID7's four stalls each get their own function, called in the same order, every check message byte-identical |
| `check_py_idiom.py` (Rule 12) | `tb/pp_top/notify_mutants.py:111`, 122 columns > 120 | the `ident_burst_from_t0` replacement string starts on its own line; every planted and replacement string is unchanged (the module's string constants compare equal) |

Section ID after the fix: 106 checks, 0 failures, with the measured gaps unchanged (ID7: 15,270
and 15,300; ID7f 15,264; ID7n 15,273 | 15,301). Receipt: `receipts/identify-88e0bf8.log`.

The third failure, `measure_test_evidence.py --check` ("1 unexplained DUT-source reader"), is
**not this lane's**. It is `tb/pp_top/acmp_mutants.py`, main's driver from #137, which came in
through item 1's merge. It fails the same way with the processor at `main` `3f3ea56` alone, without
the C6 patch (`receipts/parent-g7-at-main-3f3ea56.log`). #137's own PR body (Round 2, item 2)
records the parent disposition line for it, verbatim. So the consumer set below applies that
line as a separate commit after the C6 patch. The C6 patch in this directory is unchanged.

## Parent-visible list

Read against the parent at milan-fpga dev `e4b771f9`. Round 2 adds no top port, no top
parameter and no register, and nothing changes at the parent's setting (`EN_IDENTIFY_NOTIF_P` = 0).

| # | Change | Parent effect | Parent disposition |
|---|---|---|---|
| 1 | `KL_aecp_notify` gains one internal input `uns_tx_busy_i` (documented `//!`), driven inside the top by `gen_uns_departure` | the parent's port-contract gate counts it: protocol-processor ports 1,748 at `main` `3f3ea56`, 1,752 at the head (round 1's three identify ports, and this one); undocumented 111 <= 111 at both | none; no budget moves. It is a module port inside the processor, not a top port. It is listed here because the parent's gate sees it |
| 2 | `gen_uns_departure` in `protocol_processor_top` | only with `EN_IDENTIFY_NOTIF_P` = 1; at 0 `uns_tx_busy_w` is the constant 0 and `KL_aecp_notify` never reads it | none |
| 3 | `(* ASYNC_REG = "TRUE" *)` on `btn_q1_r`, `btn_q2_r` | the flops exist only with `EN_IDENTIFY_NOTIF_P` = 1. When a parent sets 1, integrator guide §1 asks it to declare the pin-to-`btn_q1_r` path asynchronous | none at 0 |
| 4 | main's `tb/pp_top/acmp_mutants.py` (#137), arriving with item 1's merge | `measure_test_evidence.py`: 1 unexplained DUT-source reader without a disposition | #137's documented `DUT_READER_DISPOSITIONS` line, owed by whichever adoption first moves the parent's processor pin past `3f3ea56` (it is not part of the C6 patch) |
| 5 | `tb/pp_top/notify_mutants.py` gains 4 identify controls (34 in all) | the C6 patch's disposition entry covers the driver as a whole | none |
| 6 | behaviour at the parent's setting (0) | unchanged from round 1 | none |

## Gates

Verilator 5.050 (the CI pin, `$VALIDATION_TOOLS/verilator-v5.050`), behind a scratch shim
that caps `--build -j 0` at 8; one heavy build at a time. Yosys 0.66, sv2v.

### Processor, every command at the head `88e0bf8` (all rc 0; the same set also passed at `2e99ab0`)

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | UPC map gate PASS (58 constants, 82 entry points); 33 suites, 1,018,084 checks, 0 failing. `pp_top` 8,170 (default 8,044, fixture 20, identify 106; the merge had 8,126, and section ID grew from 62 to 106), `originator` 107, `ucpu` 396, `acmp_listener` 2,988, `rx_validator` 555, `maap` 196; 470 s. Receipts `receipts/run_suites-88e0bf8.log` (and `run_suites-2e99ab0.log`) |
| `./scripts/lint_hdl.sh` | 0 | 41 modules LINT OK; `KL_aecp_notify`, `KL_aecp_engine` and `protocol_processor_top` also clean at `EN_IDENTIFY_NOTIF_P` = 1 (the same flags, `-GEN_IDENTIFY_NOTIF_P=1`). Receipt `receipts/lint_hdl-88e0bf8.log` |
| `make check` | 0 | 41 mermaid + 18 wavedrom, links 999, matrices (115 REQ, 17 GAP; 94 rows, 0 untested), parameters 27 = 27 = 27, stale |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` | 0 | 36 tops YOSYS OK and the Xilinx memory-map check (`KL_aecp_engine`) |
| `git diff --check 3f3ea56b..HEAD`, `5e806296..HEAD` | 0, 0 | |

### Mutation campaigns at `88e0bf8`

Run one at a time by a scratch runner. The lane tree's `git status` was empty after every
campaign. Round 1's set, plus main's two new campaigns (`acmp_mutants.py` from #137, whose
anchors sit in the top that the lane edits, and `tb/maap` from #135).

| Campaign | rc | Result |
|---|---:|---|
| `python3 tb/pp_top/notify_mutants.py --output DIR --jobs 1` | 0 | 4 goldens PASS; **34 of 34 KILLED** by their named checks (the 30 of round 1, re-anchored where named above, and round 2's 4); 553 s. `receipts/campaigns/notify-mutants-88e0bf8.json` (per-mutant failing checks) |
| `python3 tb/pp_top/acmp_mutants.py --output DIR --jobs 1` (main's) | 0 | goldens PASS; 19 of 19 KILLED; 282 s |
| `make -C tb/adp_engine mutants MUTANT_OUTPUT=DIR` | 0 | 30 of 30 KILLED, 0 survived; 32 checks, 0 FAIL; 330 s |
| `make -C tb/maap mutants MUTANT_OUTPUT=DIR` (main's) | 0 | 3 controls PASS (maap 196, pp_top maap-internal 34, rx_validator 555); 29 of 29 KILLED; 32 checks, 0 FAIL; 228 s |
| `python3 tb/pp_top/gsi_mutants.py --output DIR` | 0 | 20 of 20 detected by named checks; golden and restored PASS; 786 s |
| `python3 tb/acmp_talker/retry_mutants.py --logs DIR` | 0 | 62 mutants KILLED; 7 equivalence and 1 performance controls retained; baseline and restored rc 0; 372 s |
| `make -C tb/nvm_port figures` | 0 | every measured figure agrees with the tree (baseline 136 PASS; 2 waivers printed with their reasons); 234 s |
| `make -C tb/srp_top mutants MUTANT_OUTPUT=DIR` | 0 | 78 of 78 KILLED, 0 survived; assertion coverage 65/65; 90 checks, 0 FAIL; 1,819 s |
| `python3 tb/pp_top/d3_mutants.py --output DIR --jobs 1`, then `--only` the six it had not reached | 0, 0, 0 | **83 of 83 KILLED** by their named checks; goldens PASS in each run. The whole-set run reached 77 of 83 (every one KILLED; goldens `acmp_nvm`, `pp_top`, `rx_validator` PASS) before the host reboot of 2026-10-01 ~12:02 cut it. The remaining six ran at the same head in two `--only` chunks: `proof_past_bound_needs_fired`, `agg_o_pulse`, `aecp_hold_unbounded` (golden `pp_top` PASS; 266 s), and `held_drop_uncounted`, `resident_never_returned`, `validator_admits_held_aecp` (goldens `pp_top`, `rx_validator` PASS; 211 s). Round 1 also ran this campaign in two chunks. `receipts/campaigns/d3-88e0bf8-part{1-cut,2,3}.log` |

The interrupted session's partial notify run (`2e99ab0`, 19 of 34 reached, every one KILLED)
is superseded by the whole run above.

### Resource cost, out of context (R420-1 S3, R421-1 S4)

Yosys 0.66, round 1's flow: `git archive` of `hdl/` at the revision, `sv2v` of every package
then every module, the generated `ucode.hex` and `ltn_rom.hex` beside the netlist, then
`synth_xilinx -family xc7 -flatten -top protocol_processor_top`, with the parameter set by
`chparam`. One run at a time, in the foreground: 249 s, 246 s and 257 s; peak RSS 2.8 GB.

| Build | LUT | FF | CARRY4 | MUXF7 / MUXF8 | RAM32M / RAM64M | RAMB36 / RAMB18 | DSP48 |
|---|---:|---:|---:|---:|---:|---:|---:|
| main `3f3ea56` | 63,151 | 30,454 | 2,317 | 577 / 125 | 1,497 / 3 | 16 / 1 | 4 |
| head `88e0bf8`, `EN_IDENTIFY_NOTIF_P` = 0 | 61,488 | 30,454 | 2,317 | 615 / 123 | 1,497 / 3 | 16 / 1 | 4 |
| head `88e0bf8`, `EN_IDENTIFY_NOTIF_P` = 1 | 63,283 | 30,533 | 2,339 | 659 / 190 | 1,497 / 3 | 16 / 1 | 4 |

(LUT = LUT1-LUT6, as in round 1; FF = FDRE + FDSE.)

- At 0 the FF, CARRY4, RAM and DSP counts are main's. The LUT count moves both ways with the
  mapper: main maps 688 LUT more at `3f3ea56` than round 1 measured at `0451d83d` (62,463),
  at the same 30,454 FF, and the head at 0 maps 1,663 fewer than main. At 0, round 2 adds only
  the constant-0 `uns_tx_busy_w`, which `KL_aecp_notify` does not read.
- Identify cost (1 - 0): +79 FF and +22 CARRY4. Round 1 measured +76 and +14. The extra 3 FF are
  `gap_r`, `left_r` and the top's `busy_r`. The extra 8 CARRY4 are the 32-bit
  `now_ms_i + 151` adder of the BURST deadline (`KL_aecp_notify.sv:746`). The LUT figure,
  +1,795 as mapped, carries the same mapper variance.
- Stat files: `receipts/yosys-stat-top-main-3f3ea56.txt`, `yosys-stat-top-88e0bf8-en0.txt`,
  `yosys-stat-top-88e0bf8-en1.txt`; times `receipts/yosys-time-top.txt`. Logs (not copied,
  over 200 KB):

| Log | Bytes | sha256 |
|---|---:|---|
| `synth_top_main-3f3ea56.log` | 7,691,766 | `2c43d801eb6447ff34de0bfd4cc099d4aa845b98cdf5fd6a22f1943d18a4f854` |
| `synth_top_en0.log` (head) | 7,701,831 | `81600ed7c8c4bdaba06dd14c43daf5b60b7b2a7556904557fe32b3436b3e788b` |
| `synth_top_en1.log` (head) | 7,674,994 | `729e3aa58c82af6bc2c396e6a31874355b2cfca1de7f00d1ec9f8709b4623c82` |

### Parent consumer set at milan-fpga dev `e4b771f9`

Scratch copy `$VALIDATION_STORAGE/c6r2-parent/src`; the trusted checkout was not touched. Commits:
1. `62d2e1f`: `git archive e4b771f9`, with `external`, `gptp-processor` and
   `third_party/verilog-axis` cloned at their recorded pins and `protocol-processor` a shared
   clone of this lane at `88e0bf8`; `git submodule init` registers them, with no fetch. Its
   980-entry index equals the trusted checkout's except the processor gitlink.
2. `a887e1f`: `git apply parent-adoption-c6-e4b771f9.patch` (unchanged, from this directory).
3. `7565a78`: #137's documented `DUT_READER_DISPOSITIONS` line for `acmp_mutants.py`,
   verbatim (item 5 above; not this lane's).

Verilator 5.050 behind the `-j 8` shim, `make -j8`, one heavy command at a time.

| # | Command | rc | Result |
|---:|---|---:|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | every ratchet at or under budget (multi-declarator 0 <= 0, long function 0 <= 0) |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | every ratchet at or under budget (over-long line 0 <= 0, too many parameters 7 <= 7) |
| 3 | `python3 scripts/check_rtl_source_lists.py` | 0 | OK: 107 files in the milan_datapath closure, 4 of 4 consumer lists; protocol-processor 36/42 tops, 6 recorded |
| 4 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | OK |
| 5 | `python3 scripts/check_port_contracts.py` | 0 | OK: 3,793 first-party ports (protocol-processor 1,752); undocumented protocol-processor 111 <= 111; 52 literal-bound, 62 without a local rationale, all recorded |
| 6 | `python3 scripts/measure_naming.py --check` | 0 | PASS: 96 candidates, all recorded by identity |
| 7 | `python3 scripts/measure_test_evidence.py --check` | 0 | PASS: 73 <= 77 without a mutation arm, 10 <= 10 unseeded, 0 <= 0 unexplained DUT-source readers, 3 <= 3 wall-clock. At `a887e1f` (C6 patch alone) rc 1: 1 unexplained, `acmp_mutants.py`, the same as at `main` `3f3ea56` with no patch |
| 8 | `python3 scripts/docs_check.py` | 0 | 0 findings across 181 md + 952 scrubbed files; scrub self-test 23/23; routing 4/4 |
| 9 | `python3 scripts/xvlog_gate.py --check` | 0 | PASS: 4 findings == ratchet (hdl/ 0, pinned processors 4 at `protocol-processor@88e0bf82`; the same four keys as the trusted budget); 140 s; the scratch tree clean after it. The first pass ran it without `--check` (also rc 0, the same 4), which rewrites the budget's line-number comments; that scratch file was restored before the `--check` run, the form CONTRIBUTING.md names. Receipt `receipts/parent-gates/g09-xvlog_gate-check.log` |
| 10 | `python3 sw/builder/test_builder.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11: the calibration report needs a local mf48 build tree, as in round 1); 984 s |
| 11 | `python3 scripts/lint_rtl.py --check` | 0 | PASS: 90 <= ratchet 90 (17 waived, 0 justified lint_off) |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 311 checks, 0 failures; 201 s |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | both lint passes |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 checks, 315 PASS |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | gmstep 104; 182 + 182; milan_datapath 235, 235, 232; media_aclk 191; 382, 416, 1,845, 1,847, 3,525, 1,845 and 33 checks in the other benches; 9 RESULT: PASS, 0 FAIL; the 6 + 6 mutant arms pass; 1,462 s. (`VERILATOR_JOBS` bounds compile memory only.) Round 1 counted 12 RESULT lines at dev `ccdd07b5`; the parent's bench set moved to `e4b771f9` |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | tdm8_render 65 and 152 checks, 0 failures; 5 of 5 leg-defect arms caught; 320 s |

Receipts: `receipts/parent-gates/` (every gate except 12 and 15) and
`receipts/parent-gates-round2-first-pass/` (the failures at `2e99ab0`). Logs over 200 KB,
not copied:

| Log | Bytes | sha256 |
|---|---:|---|
| parent `pp_shadow` (gate 12) | 308,347 | `23f171554ca631609f1a347648864cf6b0c0236c4bb29c74fca97d0bccc484a0` |
| parent `milan_dp` (gate 15) | 2,001,574 | `4ea4fe4c19b3dfd389f3762c88d7d38bea85948e4ab4dd95310a74b7add6daf1` |

## What remains

- Hosted CI on the PR, and the round-2 reviews ([R420] internal, [R421] external).
- The parent adopts `parent-adoption-c6-e4b771f9.patch` (unchanged) when it moves its
  processor pin past this head. #137's `acmp_mutants.py` disposition line is owed by
  whichever adoption first moves the pin past `3f3ea56` (parent-visible list, row 4).
- A reading this round relied on, stated for the manager: the round-2 STOP ("before any
  further port, parameter or parent-visible change") is read as the scope of round 1's
  ruling, i.e. top-level ports and parameters and changes the parent must act on.
  `uns_tx_busy_i` is a port of the internal `KL_aecp_notify`, and the only way the sequencer
  can see a frame's departure, which item 2 requires. No top port, top parameter or register
  changed. It is listed as parent-visible row 1 because the parent's port-contract gate
  counts it (no edit and no budget change). If the manager reads the STOP more strictly, this
  is the one point for a ruling.
- Retained with reasons (recorded in `tb/pp_top/README.md`): R420-1 S1 (three controls survive
  with every section-ID check passing) and R420-1 S4 (the shared limiter's one-tick reading).
- No hardware was used. The resource figures are yosys out of context; a Vivado
  out-of-context run at the parent is the authoritative figure.
- Unchanged from round 1: the optional overflow eviction sweep is not attempted (a recorded
  decision), and the solicited DEREGISTER that does not push is recorded, not changed.
