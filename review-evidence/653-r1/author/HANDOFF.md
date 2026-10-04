# [A529] HANDOFF: milan-fpga #653, re-scoped round (CRF unbind unlock + standing [UNB] tests)

**Status: REVIEW READY** at head `77ea6cb46cc3f746a14fa717c5e49a4485fb071e`, four commits on
dev `fea346e7`, not pushed. Every ruling item is done. All gates the change touches are rc 0 except
two whose failures reproduce byte-for-byte with the dev `KL_crf_rx` (sections 6a, 6b).

- Lane: `$LANES/653-unbind-order`, branch `653-unbind-order` from dev
  `fea346e76c2a57ed5cd131af8fc68dfeff57f877` (processor pin `631eeb34`, unchanged; no submodule moved).
- Ruling (scope of this round): https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5980290102
- Round 1 (STOP at item 1, the reproduction): `HANDOFF-r1-stop.md`, `PR-BODY-r1-stop.md` here;
  https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5980272602
- PR body: `PR-BODY.md` here ("Relates to #653"; the hardware report stays open for the bench capture).
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5982287900

## Commits (one-line subjects, no trailers)

| SHA | Subject (abridged) |
|---|---|
| `061204b4` | Count a locked CRF input's unbind as one MEDIA_UNLOCKED at the bind fall, as the AAF inputs do ... and pin it in the crf_rx unit suite (#653) |
| `83f097a3` | Grade an unbind of each locked input in the timed notify leg's [UNB] section ... five planted controls in unb_mutants.py (#653) |
| `88d5de5c` | Move [UNB]'s silence-window wait and trace print into helpers and drop its uid table, so the section meets the C++ idiom ratchet (#653) |
| `77ea6cb4` | Document the CRF unbind's unlock and the [UNB] section ... (#653) |

## 1. CRF invariant fix (ruling item 1)

**Measured at dev (round 1):** after an UNBIND_RX of the locked CRF input, GET_COUNTERS read
MEDIA_LOCKED 1, MEDIA_UNLOCKED 0 until the 100 ms silence timeout counted the unlock
(+9,818,177 cycles). Table 5.6 reads that pair as "synchronized" on an unbound input.

**Fix, parent only, `hdl/ieee1722/crf/KL_crf_rx.sv`:**

- `:395` `wire w_bind_fall_w = !en_i && en_q;` (beside the existing `w_bind_rise_w`).
- `:627-631` on `w_bind_fall_w && locked_o`: `locked_o <= 0`, `cnt_unlocked_o + 1`, `dirty_p_o <= 1`.
  This is the AAF rule (`KL_avtp_rx_monitor_ctx.sv:857`, task #32): an unbind while locked is one unlock.
- The 100 ms silence path (`:540-545`) is untouched. It still unlocks a bound input that goes silent
  (crf_rx `[UNB-d0]`, and the existing `pin_silence_unlock_and_refill`). After an unbind it finds
  `locked_o` low and counts nothing (`[UNB-b1]`, notify U4). A timeout on the unbind's own edge writes the
  same `+1` through the same register, so the event counts once (`[UNB-d2]`).
- STREAM_INTERRUPTED cannot count the unbind: it counts accepted PDUs only, and `en_i` low gates `w_hit`
  (`:314`). Checked by notify U3/U4 and crf_rx `[UNB-a6]`, `[UNB-b3]`.
- Nothing resets on the falling edge (5.3.8.10's asymmetry). The bind-rise wipe (`:641-696`) stays after
  the new arm and remains the last writer of `locked_o`, which the behave counters feature checks by text.
- **No port, register-map or parameter change.** Two documented behaviours move with the fix, both
  stated in the docs commit:
  - `CRF_CTRL[31]` (RO "locked") now falls at the unbind as well as at the timeout
    (`docs/reference/REGISTER_MAP.md`). No address, field, width or access changed.
  - The datapath's two `crf_locked_w` consumers see the fall at the unbind instead of up to 100 ms
    later: the 4.4.4.3 restart request when CRF is the selected clock (`milan_datapath.sv:3231`; the
    count of falls is unchanged, one per unbind) and the servo's reference lock (`:5746`). The comment at
    `milan_datapath.sv:3174-3176` is updated in place (same line count, so no pointer into that file moves).
  - `en_i` is `cfg_crf_en | acmpl1_bound`: clearing the bench CSR lever while not ACMP-bound is the same
    fall, consistent with the bind-rise wipe already keying on `en_i`.

**Trace after the fix** (`[UNB]`, cycles after the UNBIND_RX command's last byte):

| Event | AAF input 0 | CRF input 1, dev | CRF input 1, head |
|---|---|---|---|
| listener queues its response | +193 | +193 | +193 |
| debounced bind level falls | +199 | +199 | +199 |
| MEDIA_UNLOCKED written at its source | +204 | +9,818,177 | **+200** |
| Table 5.22 pulse / delivered | +204 / +205 | +9,818,177 / +9,818,178 | +200 / +201 |
| UNBIND_RX response leaves | +277 | +277 | +277 |
| source LOCKED/UNLOCKED as the response leaves | 1/1 | 1/0 | **1/1** |
| GET_STREAM_INFO push to A / B | +887 / +1,497 | +887 / +1,497 | +887 / +1,497 |
| GET_COUNTERS push reporting the unlock, to A / B | +2,294 / +3,057 | +9,819,137 / +9,819,900 | +2,294 / +3,057 |

The response still leaves first on both inputs; the CRF push now follows it as the AAF one does.

## 2. Standing tests and planted controls (ruling item 2)

**`tb/verilator/milan_dp/sim_nxn.cpp`, `[UNB]`** (timed `obj_notify` leg; `unbind_order_section()`
`:2614`, `unb_unbind_and_grade()` `:2536`). Per sink (AAF 0, CRF 1): bind, answer PROBE_TX, lock off clean
PDUs, keep the talker streaming, wait until the row pushed nothing for one second (checked), unbind:

- U1 the UNBIND_RX response is SUCCESS;
- U2 a GET_COUNTERS push reporting the unlock reaches A and B, and every such push leaves after the response;
- U3 the source pair is 1/1 on the edge the response's last byte leaves; GET_COUNTERS right after reads
  1/1 and STREAM_INTERRUPTED 0; every later push reads LOCKED = UNLOCKED;
- U4 the wait outlasts both 100 ms timeouts (10.5 M cycles, `kUnbSilenceCyc` `:2337`; controllers keep
  alive every 10 processor s against the 5.4.5.3 monitor) and the pair still reads 1/1/0.

The leg goes from 383 checks at dev to 421 (38 `[UNB]` checks).

**`tb/verilator/milan_dp/unb_mutants.py`** (`make unb-mutants`; `CRFRX_SRC` added to the Makefile so a
mutated `KL_crf_rx` copy builds through the notify recipe). Each mutant must fail its named checks AND
still pass its named holds; submodule never edited (processor half in a temp copy).

| Planted control | Named checks failing | Holds | Failures |
|---|---|---|---|
| processor ACMP TX lane held 6,000 cycles (the push forced ahead of the response) | AAF U2 order to A; CRF U2 order to A | U1 SUCCESS and push arrived, both sinks | 4 of 421 (the four U2 order checks, nothing else) |
| CRF unbind does not count its unlock (dev behaviour) | CRF U3 as the response left; right after it | CRF U1; AAF U3 | 2 of 421 |
| CRF unbind keeps the lock, the timeout counts again (double count) | CRF U4; CRF U3 every later push | CRF U3 right after; U4 wait outlasted | 2 of 421 |
| CRF unbind also counts a STREAM_INTERRUPTED | CRF U3 STREAM_INTERRUPTED; CRF U4 | CRF U3 pair | 2 of 421 |
| CRF unbind counts its unlock but arms no push | CRF U2 a push reached A | CRF U3 pair | 2 of 421 |

Result at `77ea6cb4`: `6 checks: 6 PASS, 0 FAIL` (clean leg 421/421), 667 s.

**`tb/verilator/crf_rx/sim_main.cpp`** (unit): replica `unbind()` (`:203`); `[5t-g3]` now expects
MEDIA_UNLOCKED `keep + 1` across the unbind of its locked input (it pinned the dev behaviour; the new
expectation is exact, not loosened) plus `[5t-g2b]` (locked before) and `[5t-g3b]` (LOCKED == UNLOCKED
after); new `[UNB]` section (`pin_unbind_scores_one_unlock()` `:1485`, 20 checks): one unlock on the
unbind's own edge with one dirty pulse and no STREAM_INTERRUPTED, none at the timeout after, none for an
input unbound while settling, one when the unbind and the timeout share an edge (timeout length read off
the engine's own `tout_r`, not restated), one for a stopped input still holding its lock, and the bound
silence still unlocking. That is 22 new unit checks (2 in `[5t-g]`, 20 in `[UNB]`); the unit
reports 14287 checks at head (the dev count was not re-measured).

Recorded in `tb/verilator/milan_dp/README.md` (new section, leg row, check-count row) and the
`docs/testing/TESTING.md` explicit-campaign table. `scripts/measure_test_evidence.py` classifies the new
driver as a DUT-source reader (mutation campaign).

## 3. Area (ruling item 3): OOC 1x1, under 30 LUT / 60 FF

| Instrument | dev `fea346e7` | head | Delta |
|---|---|---|---|
| `OOC_SHAPE=configs/generated/endstation_ax7101_1x1_tdm8 syn/yosys/ooc.sh KL_crf_rx` (Yosys 0.66, sv2v 0.0.13) | 433 LUT, 544 FF, 1 RAMB18 | 368 LUT, 544 FF, 1 RAMB18 | **-65 LUT, +0 FF** |
| Vivado 2026.1 `synth_design -mode out_of_context -part xc7a100tfgg484-2`, `CLK_FREQ_HZ_P=100000000 IVAL_CYC_P=100000000` (the datapath binding), under `flock /tmp/milan-vivado.lock` | 373 LUT, 544 FF, 1 RAMB18 | 352 LUT, 544 FF, 1 RAMB18 | **-21 LUT, +0 FF** |

No register is added (the edge reuses `en_q`). Both mappers come out smaller; I did not chase why (an
extra clear term on `locked_o` lets the mapper restructure the arm), and claim only the measured figures.
Base was measured by writing `git show fea346e7:hdl/ieee1722/crf/KL_crf_rx.sv` over the file for the
Yosys run and restoring it with `git checkout HEAD --` (worktree clean after); the Vivado runs read
exported copies (base sha256 `3cc824af...ebcafdbb6`, head `b36ba339...e1624f0d39a`) from scratch.

## 4. Stale pointer (ruling item 4)

PR-BODY.md, Description, last paragraph: #653's `KL_crf_rx.sv:597-605` is the rate-ring update at
`fea346e7`; the silence-timeout arm is `:533-536` and the bind-rise arm `:619-670` (at head `:540-545`,
`:641-696`; the new unbind arm `:627-631`). The issue itself is not edited (not allowed).

## 5. Gates at `77ea6cb4` (all foreground-equivalent background jobs, pinned Verilator 5.050, never piped)

| Gate | rc | Result | Wall |
|---|---|---|---|
| `make -C tb/verilator/milan_dp` (default sweep target) | 0 | 11877 checks / 0 failures, 16 tallies; `obj_notify` 421/0; render-law and default GM-step controls pass | 2051 s |
| `make -C tb/verilator/crf_rx` | 0 | 16567 / 0 (unit 14287, discontinuity 2201, talker_step 69, mutants 10/10) | 566 s |
| `make -C tb/verilator/pp_shadow` | 0 | 2169 / 0 | 686 s |
| `make -C tb/verilator/milan_dp_render` | 0 | 315 / 0 | 718 s |
| `make -C tb/verilator/milan_dp_mclk` (leg + mclk_mutants) | 0 | 168 / 0 | 491 s |
| `make -C tb/verilator/capture_coherence` (incl. mutants) | 0 | 21194 / 0 | 728 s |
| `make -C tb/verilator/aaf_clock_meter` (incl. mutants) | 0 | 471 / 0 | 761 s |
| `make -C tb/verilator/milan_dp unb-mutants` | 0 | 6 checks: 6 PASS, 0 FAIL | 667 s |
| `make -C tb/verilator/milan_dp gsi-mutants` | 0 | 9 checks: 9 PASS, 0 FAIL (leg now 421 checks) | 1062 s |
| `make -C tb/verilator/milan_dp crflic-mutants` | 0 | 7 checks: 7 PASS, 0 FAIL | 548 s |
| `make -C tb/verilator/milan_dp gmstep-mutants` (`--all`) | 0 | 22 checks: 22 PASS, 0 FAIL | 1056 s |
| `make -C tb/verilator/milan_dp render-csr-controls` | 0 | 4 checks, 0 failures | 166 s |
| `make -C tb/verilator/pp_shadow pending-mutant` | 0 | late-mark mutant killed by K10 and K12; clean control passes | 458 s |
| `make tdm8render-mutants` in `tb/verilator/milan_dp_render` | **2** | `32 checks: 28 PASS, 4 FAIL`; **pre-existing at dev, not caused by this lane** (section 6a) | 3268 s |
| `make -C tb/verilator/milan_dp_gptp` (physical) | **2** | `139 checks, 3 failures`: audio sample order (section 6b) | 3330 s |
| `syn/yosys/run.sh` | 0 | tops 55, pass 55, fail 0; tied-input and tap-purity gates PASS | 839 s |
| `syn/yosys/ooc.sh KL_crf_rx` | 0 | section 3 | - |
| `XVLOG=<Vivado 2026.1 xvlog> flock /tmp/milan-vivado.lock scripts/xvlog_gate.py --check` | 0 | PASS, 4 findings == ratchet (all in the pinned processor), 0 in `hdl/` | 145 s |
| `scripts/lint_rtl.py --check` | 0 | 90 <= ratchet 90 | - |
| behave `cd tests && behave --tags ~@open-finding -f plain` | 0 | 14 features, 404 scenarios, 1968 steps passed | 1.5 s |
| `sw/builder/test_builder.py` (builder bank, RV32 compiler found, gate 1b ran) | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11: local Arty mf48 report not on this machine) | 1178 s |
| docs: `docs_check.py`, `check_em_dash.py --base fea346e7` (0 findings / 108 added lines) and `--selftest`, `check_doc_style.py` and `--selftest`, `gen_toc.py --check` and `--verify-anchors`, `check_doc_paths.py`, `gen_module_matrix.py --check`, `check_feature_status.py --self-test`, `check_solution_docs.py`, `DOC_MAP.gen.py --check`, `check_gptp_docs.py` (+`--with-submodule`), `submodule_boundaries.gen.py --check`, `check_submodule_docs.py`, `timesync_chain.gen.py --check`, `check_diagram_pngs.py`, `ci_events.py --check`, `ci_scope.py --selftest` | 0 each | pinned Markdown renderer in a scratch venv | - |
| code quality: `measure_test_evidence.py --check`/`--selftest`, `check_py_idiom.py` (+`--selftest`), `check_cpp_idiom.py` (+`--selftest`), `check_sv_idiom.py`, `check_sh_idiom.py`, `check_hygiene.py --check`/`--selftest`, `measure_naming.py --check`, `check_port_contracts.py`, `measure_fail_fast.py --check`, `check_todo_ownership.py`, `check_rtl_source_lists.py`, `check_soc_sources.py`, `pp_srcs.py --check`, `measure_control_flow.py --selftest`, `measure_cohesion.py --selftest` | 0 each | - | - |

**Not run:** `act_ci.py` and hosted CI (nothing is pushed; no PR exists); the whole 59-suite
`run_all_suites.sh` sweep (the ruling's bar is the milan_dp suite and every suite and campaign that
builds a changed file, all listed above); the candidate-merge validation (a merge step).

## 6a. tdm8render-mutants: four failing arms, identical with the dev `KL_crf_rx`

Failing arms at `77ea6cb4`:
1. the clean ship leg in `--epoch-only` mode fails 4 of 114 checks, all T30 CRF: "the selection under
   the running stream fired the settled-grid trigger ONCE got=0 exp=1", "...as exactly one render
   recentre pulse", "...and the stage executed exactly one recentre", "no second recentre followed the
   settled one";
2. and 3. the two clean controls "modelled arrival skew, one extra cycle on the acknowledgement level" and
   "... on the serial-reset level" (both in that mode) are reported caught;
4. the mutant "uncounted repeat: the underrun counter never increments" (ship `--serial-only`) survives.

Evidence that none of it comes from this change (the ship leg's other sources are untouched by the lane;
`milan_datapath.sv` differs from dev by a comment only):
- `obj_tdm8r` (head) and a ship build against `git show fea346e7:hdl/ieee1722/crf/KL_crf_rx.sv`
  (scratch obj dir; the tree file restored after the build, worktree clean) give **byte-identical**
  output in `--epoch-only` (both 114 checks, the same 4 failures) and in `--serial-only` (both pass).
- The "uncounted repeat" mutant built against the dev `KL_crf_rx` also survives: `--serial-only`
  53 checks, 0 failures.
- The leg is cycle-bounded and deterministic. Its last changes are #643's T30 commits
  (`22f9a244`, `e63c4279`, `ca3db9f3`).
This lane may not file Issues; it needs one (the epoch-only T30 CRF clean failure and the survivor).

## 6b. milan_dp_gptp: three audio sample-order failures

`[FAIL] audio sample order, no duplicates or gaps got=2 exp=0` (after-acquire window and recovery window)
and `[FAIL] all monitored audio sample ordering errors got=5 exp=0`; payload, packet sequence, gPTP and
accounting checks pass. The leg never writes `CRF_CTRL` and never binds a sink (`sim_ax1x1gptp.cpp`; it
prints `NOT RUN: ... CRF recovery`), so `KL_crf_rx`'s `en_i` never rises and the new arm cannot fire.
Dev comparison: the same leg built against `git show fea346e7:hdl/ieee1722/crf/KL_crf_rx.sv` (the
tree file restored after Verilation; worktree clean) gives rc 2, `139 checks, 3 failures`, the same three,
and its simulation output (every check, AUDIO, PUBLIC, Pdelay, PROGRESS, LOSS and TX-flag line, 268
lines) is identical to the head run's (`diff` rc 0). Logs: `head-milan_dp_gptp.log`,
`milan_dp_gptp-devcrf.log`. Pre-existing; needs an Issue this lane may not file.

## 6. Review notes (for the cleared-context reviewers)

- The issue's wire-order acceptance (1, 2) is graded in simulation only; the bench capture and the
  20-cycle controller session (acceptance 4) are manager items. Hence "Relates to #653".
- The order control is a processor-side mutant (the ACMP lane held 6,000 cycles), because the parent
  cannot reorder two frames of the processor's single TX stream. Its holds prove the response still
  arrives SUCCESS and the push still arrives, so the catch is the order.
- `[5t-g3]` changed expectation: MEDIA_UNLOCKED across the unbind of a locked input is now `keep + 1`.
  The old line pinned the defect; the new one is exact and is joined by `[5t-g3b]`.
- Docs line pointers into `KL_crf_rx.sv` in `docs/design/MEDIA_CLOCK_FOLLOWING.md` were all remapped
  to the post-change lines (each target re-read), and its sentence comparing the meter's unbind to
  `KL_crf_rx` was corrected.

## 7. Files in this directory

| File | What |
|---|---|
| `HANDOFF.md`, `PR-BODY.md` | this round |
| `HANDOFF-r1-stop.md`, `PR-BODY-r1-stop.md` | round 1 (STOP at item 1), kept |
| `653-unb-repro-sim_nxn.patch` | round 1's `[UNB]` reproduction patch (the starting point; now committed in its extended form) |
| `base-notify-clean-run.log`, `base-unb-trace-run.log` | round 1: dev leg 383/0, and dev + patch (the dev trace) |
| `head-notify-run.log` | `obj_notify` at head: 421/0 and the two `[i] [UNB]` trace lines |
| `head-unb-mutants.log` | `make unb-mutants` at head: 6/6 |
| `head-crf_rx-suite.log` | `make -C tb/verilator/crf_rx` at head |
| `head-tdm8render-mutants.log`, `tdm8r-epoch-only-head.log`, `tdm8r-epoch-only-devcrf.log`, `tdm8r-serial-only-uncounted-repeat-devcrf.log` | section 6a |
| `head-milan_dp_gptp.log`, `milan_dp_gptp-devcrf.log` | section 6b |
| `ooc-KL_crf_rx-head.log`, `ooc-KL_crf_rx-dev.log`, `vivado-util-KL_crf_rx-{head,dev}.rpt`, `vivado-crf_ooc.tcl` | section 3 |
| `head-yosys-run.log`, `head-xvlog-gate.log`, `head-builder-bank.log` | section 5 |
| `parent-adoption-*.patch` | supplied for option (b); unused (out of scope this round) |

Not copied (size): `milan_dp` suite log, 2,139,795 bytes, sha256 `704f28df92418650262b62694b64d79e1eebaf945ed7024a5cb00557f909e394`; behave log, 196,684 bytes,
sha256 `bed4e6dfc5a7cd406895e24164b91fb944f95b75b5cdf32009d0382c337cbb0d`. Scratch (builds, venv, logs) is under `$VALIDATION_STORAGE/653-a529/`, outside the tree.
