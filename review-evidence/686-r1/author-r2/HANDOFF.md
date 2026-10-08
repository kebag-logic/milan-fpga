# [A565] HANDOFF: issue #686 (fabric MAAP engine vs IEEE 1722-2016 Annex B)

## Round 2

Status: REVIEW READY at `48f12dc14099a3630a98eb07e9ec790695a72bfb`. Every gate exited 0 at the final head (table "Round 2 gate table, final head"). No STOP condition was met: the area is within budget, the route meets both floors, there is no register-map, filter or mailbox change, and nothing is outside scope. Part A was committed at `30fce4b0a989dedc93969fbc27053985894d9438` on `c7b69cd0`, and every Part A gate exited 0 there too. PR #692 (#682) was OPEN at 23:52 and 00:10 CEST, then merged into dev at 00:52 CEST (`291710b1`), which the 01:10 check found before a STOP was posted. So Part B proceeded: dev was merged with `--no-ff` as `e519e31ff55af7dcae253da280baad531a7ad40c`, and the three records were re-recorded on that result in `48f12dc14`. No push, PR edit or other comment; the only issue comment is REVIEW READY: comment 6050832603.

- Assignment: issue #686 comment 6047563934. Reviews answered: R548-1 (PR #695 comment 6047555468) and R549-1 (comment 6047415775); their packets and probe scripts were read from `review-evidence/686-r1/reviews/` on `686-review-evidence`.
- HEAD confirmed `c7b69cd0fb2bdf980546ab413b3b82198267cbd8` before work; remote `https://github.com/kebag-logic/milan-fpga.git`. No push, no rebase, no amend. One merge: dev with `--no-ff` (Part B).
- Commits (one-line, no trailers, configured identity):
  - `b2e786bb1` Seed KL_maap's LFSR with a nonzero constant when the station MAC folds it to zero, and grade a zero-seed MAC's B.3.4 timer draws
  - `359c42da7` Grade a conflicting PROBE parsed while an ANNOUNCE is mid-frame and this station's empty range, each with a planted defect
  - `30fce4b0a` State KL_maap's frame snapshot, pool and seed bounds as built, the missed fourth PROBE as Table B.7 settles it, and refresh stale KL_maap comments
  - `e519e31ff` Merge dev 291710b1 (#682, processor 2ad2f845 and baseline F) into the #686 lane, the resource records and their text from dev until the re-record on this result
  - `48f12dc14` Re-record the resource gate's three endpoints on the merge with dev 291710b1, single-thread synthesis as F, every tolerance, floor and ceiling unchanged

### Round 2 changes (file:line at `30fce4b0a`)

| Finding | file:line | Change |
|---|---|---|
| A1, LFSR zero state (R549-1-F1 = R548-1-F3, MAJOR) | `hdl/ieee1722/maap/KL_maap.sv:141-149`, `:292` | The MAC seed `0xACE1 ^ mac[15:0] ^ mac[31:16]` is now a wire (`mac_seed_w`). Reset loads `0xACE1` when it is zero, otherwise the seed itself, so every other MAC keeps its round-1 seed. The LFSR step is an invertible linear map, so zero is reachable only from zero: no station MAC can reach the zero state. The timer draws (`:170-171`, 518 + lfsr[5:0] ms and 30488 + lfsr[9:0] ms) and their bounds are unchanged. |
| A1 harness | `tb/verilator/maap/sim_main.cpp:56-64`, `:571-622` (section [11]) | Re-resets with `02:00:00:00:AC:E1`. Over three walks plus four ANNOUNCEs, it requires more than one distinct timer-to-timer probe interval and more than one distinct announce interval, each strictly inside 500..600 ms or 30..32 s. Only timer-started sends are compared: they leave one cycle after a ms tick, so the interval equals the draw. The at-once sends (first PROBE, first ANNOUNCE) start at another tick phase and are excluded, so a frozen draw cannot pass through the phase alone. |
| A1 campaign | `tb/verilator/maap/mutants.py:34`, `:57-60` | Two rows restore the zero seed (`mac_seed_w` as the reset value), one graded by each named check |
| A1 docs | `docs/design/MAAP_FABRIC.md:91-95` (was `:85`) | "successive intervals differ" replaced by the seed rule and "the draws are random for every station MAC" |
| A2, mid-frame PROBE (R548-1-F1) | `tb/verilator/maap/sim_main.cpp:419-441` (section [6a]) | Under backpressure an ANNOUNCE is requested, two beats leave, then the stall holds it. A conflicting PROBE is injected and parsed. The frame must leave byte-identical to Figure B.1 (golden), no DEFEND may follow (`defends_o` unchanged, exactly one frame), and the state and range must be kept. No RTL change. |
| A2 campaign | `tb/verilator/maap/mutants.py:91-93` | `defend_rewrites_the_frame_on_the_wire` removes `&& !tx_busy_r` from `defend_w` |
| A3, missed fourth PROBE (R548-1-F2) | `docs/design/MAAP_FABRIC.md:135-140` (was `:125-126`) | Table B.7: probetimer! repeats PROBEs one to three, so the next one can be defended. A missed fourth is not repeated: probeCount! sends the prober's ANNOUNCE at once, and that ANNOUNCE with compare_MAC (B.3.6.4, note d) settles the overlap, which can move this station off its range. Checked against the Table B.7 rows and B.3.6.2/B.3.6.3 in the standard. |
| A4, snapshot claim (R549-1-F2 = R548-1-F4) | `KL_maap.sv:222-228`, `MAAP_FABRIC.md:64-69` (was `:62-63`), PR-BODY | R548-1-F4's text: the fields a protocol event can change (message type, destination, requested offset, conflict range) are latched; requested_count and the source MAC follow `count_i` and `station_mac_i` and are not protected against reconfiguration during a frame |
| A5, pool claim (R549-1-F3 = R548-1-F5) | `MAAP_FABRIC.md:51-54` (was `:51-52`), `:142-144`; `KL_maap.sv:45-57`, `:280-281`; `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:5`, `:27` | A random block is clipped to the pool; a supplied seed is used as given, not range-checked. Supplied-seed validation is added to the follow-up deviation list (MAAP_FABRIC `:142-144`) and not implemented. |
| S1 (optional), own empty range | `sim_main.cpp:491-497`; `mutants.py:94-95` | `count_i` = 0 and a received range straddling the offset must not conflict. Mutant `own_empty_range_conflicts` removes `(count_i != 8'd0)`. |
| S3 (optional), campaign labels | `mutants.py:4-15`, `:35`, `:86-95`, `:137` | Item 0 (`SUPPORTING`) labels mutants that grade a supporting change: `restart_rewrites...`, `overlap_count_to_our_end`, and the two new ones. They do not count toward the guard that items 1-4 each have a mutant. |
| S4 (recommended), stale comments | `hdl/milan/milan_datapath.sv:267`, `:281-284`; `KL_maap.sv:45-50` | "621 LUT / 268 FF" becomes the Yosys OOC figure at this head (515 / 278). "3-probe / 500 ms" becomes the four-PROBE walk with three 500..600 ms intervals (about 1.6e8 cycles at 100 MHz). The banner deviation list adds the undefended mid-frame PROBE and the unchecked seed. |
| S2 (not done) | -- | Truncated PDUs (`rbeat_r >= 3'd5` gate untested) are pre-existing and outside #686. They are a follow-up candidate, listed below. |

### Round 2 tests and the planted defect each catches

Harness: 130 checks (was 120). Campaign: clean control plus 26 mutants (was 22), 27 rows, each mutant required to fail its named `[FAIL]`.

| Named check (sim_main.cpp line) | Planted defect (mutants.py row) | Result |
|---|---|---|
| `B.3.4.2 probe T randomized (zero-seed MAC)` (:618) | `zero_seed_freezes_the_probe_draw` (:57): reset value back to the zero-capable seed | caught |
| `B.3.4.1 announce T randomized (zero-seed MAC)` (:621) | `zero_seed_freezes_the_announce_draw` (:59): same defect | caught |
| `PROBE mid-frame: frame on the wire byte-identical` (:435) | `defend_rewrites_the_frame_on_the_wire` (:91): `!tx_busy_r` removed from `defend_w` | caught (also fails `PROBE mid-frame: no DEFEND`) |
| `note b: this station's empty range never conflicts` (:496) | `own_empty_range_conflicts` (:94) | caught |

Reviewer probes re-run at the Part A tree (scripts from the review packets, unchanged):

- R548 `r548_probes.py`: 13 of 14 killed, including `defend_while_busy` and `own_empty_range_conflicts`, which survived at `c7b69cd0`. `truncated_pdu_accepted` still survives (S2, pre-existing, outside #686).
- R548 `r548_crosscheck.cpp`: the zero-seed MAC now gives 25 distinct announce intervals (was 1). The ordinary MAC gives 25, identical values to round 1. Seed `0xFEFF` still claims a block ending at `0x0FF07`, as the corrected docs now state.
- R548 `r548_inflight.cpp`: in-flight ANNOUNCE intact, PROBE unanswered, rc 0.
- R549 `probe.cpp`: the 144-case matrix and `zero-state MAC randomized announce` pass (23 distinct intervals, was 1). rc is 1 because two checks encode the two withdrawn prose claims, which the assignment settles in the docs, not the RTL: `every per-frame field remains latched under stall` (count is live by design, now documented) and `documented pool containment includes seed` (supplied seed not range-checked, now documented).

### Round 2 coverage

| Item | Clause | Graded by (new in round 2 in bold) | Defects caught |
|---|---|---|---|
| 1 | B.2.1 | unchanged from round 1 | 4 (the B.2.8 overlap row moved to supporting) |
| 2 | B.3.3/B.3.4 | round 1 plus **a zero-seed MAC's timer-to-timer probe and announce draws: random and strictly in bounds** | 7 |
| 3 | B.3.2/Table B.7 | unchanged from round 1 | 7 |
| 4 | Table B.7 | unchanged from round 1 | 4 |
| supporting | frame integrity, B.2.8 overlap, own empty range | Restart! on the wire, **PROBE parsed mid-frame (byte-identical frame, no DEFEND)**, DEFEND overlap count, **this station's empty range** | 4 |

Line coverage (`make -C tb/verilator/maap coverage`): `KL_maap.sv` 100.0 % (169/169), gate 95 %: PASS.

### Round 2 gate table, Part A head `30fce4b0a`

Pinned Verilator 5.050 (every suite log records it), `VERILATOR_JOBS=2`, at most two Verilator builds at once. Peak unit memory 15.7 GB including page cache. Each command ran unpiped with its own log and rc.

| Gate | Command | rc | Result |
|---|---|---|---|
| maap suite | `make -C tb/verilator/maap` | 0 | `KL_maap: 130 checks, 0 failures`; `maap mutants: checks: 27   failures: 0` (197 s) |
| maap coverage | `make -C tb/verilator/maap coverage` | 0 | `KL_maap.sv` line 100.0 % (169/169), gate 95 % PASS |
| milan_dp | `make -C tb/verilator/milan_dp` | 0 | 12,065 checks, 0 failures, including the crflic leg's 417 (2,584 s) |
| crflic campaign | `make -C tb/verilator/milan_dp crflic-mutants` | 0 | leg 417 checks 0 failures; campaign `7 checks: 7 PASS` (control plus 6 mutants caught) |
| pp_shadow | `make -C tb/verilator/pp_shadow` | 0 | 2,184 checks, 0 failures (734 s) |
| capture_coherence | `make -C tb/verilator/capture_coherence` | 0 | 21,194 checks, 0 failures (647 s) |
| milan_dp_mclk | `make -C tb/verilator/milan_dp_mclk` | 0 | 168 checks, 0 failures (518 s) |
| milan_dp_render | `make -C tb/verilator/milan_dp_render` | 0 | 334 checks, 0 failures (829 s) |
| suite tally | `scripts/suite_tally.py` over the six logs | 0 | 36,102 checks, 0 in-suite failures (round 1: 36,088; maap +14) |
| ctrl suite | `MILAN_RV32_CC=<verified SDK>/bin/riscv32-linux-gcc test_ctrl_firmware.py --require-rv32 --jobs 4` | 0 | `test_ctrl_firmware: PASS`, the RV32 arm included |
| differential | `maap_differential.py` / `--self-test` | 0 / 0 | 12/12; 16/16 controls caught |
| lint ratchet | `scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| parser ratchet | `scripts/xvlog_gate.py --check` (Vivado 2026.1 xvlog, under the lock, alone) | 0 | 0 hdl/ findings; 2 pre-existing pinned-processor findings == ratchet (157 s) |
| Verilator -Wall lint, `KL_maap` alone (informational) | `verilator --lint-only -Wall` | 1 (warnings fatal) | the same two warnings as `c7b69cd0` (`rx_msg_r` WIDTHTRUNC, unused `rx_tkeep_i`); nothing new |
| Yosys OOC | `syn/yosys/ooc.sh KL_maap` | 0 | 515 LUT / 278 FF / 59 CARRY4 |
| Yosys portability | `syn/yosys/run.sh --top KL_maap` | 0 | PASS, 1,972 cells; tied-input and tap-purity PASS |
| test evidence | `measure_test_evidence.py --check` / `--selftest` | 0 / 0 | 0 unexplained readers; 105/105 |
| docs and code quality | the 24-command docs/code-quality set of round 1 (docs_check, check_em_dash `--base e21c1ca0` and selftest, gen_toc check/anchors, doc_style, doc_paths, module_matrix, feature_status, DOC_MAP, solution/submodule docs, naming, port_contracts, fail_fast, todo_ownership, test_evidence, hygiene, sv/cpp/py idiom, rtl_source_lists, pp_srcs, `git diff --check e21c1ca0 HEAD`) | all 0 | before commit C on the working tree, and again at `30fce4b0a` |
| resource baseline | `pp_resource_gate.py check-baseline` | 0 | `baseline PASS: 3 endpoints` (the `c7b69cd0` records) |
| reviewer probes | R548 `r548_probes.py`, `r548_crosscheck.cpp`, `r548_inflight.cpp`; R549 `probe.cpp` | 0 / 0 / 0 / 1 | see "Round 2 tests" above (R549's rc 1 is its two withdrawn-claim checks) |

Head each gate saw: everything above ran on the tree of `30fce4b0a` (the maap harness and campaign, coverage, lint and the reviewer probes ran on the identical working tree before the three commits were cut, then the suites, the docs set and lint again at the committed head).

### Round 2 gate table, final head `48f12dc14`

The suites ran on the tree of `48f12dc14`. The re-record commit changes only the resource JSON and three docs, none of them a suite or build input, so its parent `e519e31ff` has the same RTL, testbenches and firmware. Pinned Verilator 5.050, `VERILATOR_JOBS=2`, at most two Verilator builds at once. Each command ran unpiped with its own log and rc.

| Gate | Command | rc | Result |
|---|---|---|---|
| maap suite | `make -C tb/verilator/maap` | 0 | `KL_maap: 130 checks, 0 failures`; `maap mutants: checks: 27   failures: 0` (186 s) |
| maap coverage | `make -C tb/verilator/maap coverage` | 0 | `KL_maap.sv` line 100.0 % (169/169), gate 95 % PASS |
| milan_dp | `make -C tb/verilator/milan_dp` | 0 | 12,065 checks, 0 failures, including the crflic leg's 417 (2,641 s) |
| crflic campaign | `make -C tb/verilator/milan_dp crflic-mutants` | 0 | leg 417 checks 0 failures; `7 checks: 7 PASS` (748 s) |
| pp_shadow | `make -C tb/verilator/pp_shadow` | 0 | 2,184 checks, 0 failures (732 s), at processor `2ad2f845` |
| capture_coherence | `make -C tb/verilator/capture_coherence` | 0 | 21,194 checks, 0 failures (645 s) |
| milan_dp_mclk | `make -C tb/verilator/milan_dp_mclk` | 0 | 168 checks, 0 failures (535 s) |
| milan_dp_render | `make -C tb/verilator/milan_dp_render` | 0 | 334 checks, 0 failures (820 s) |
| suite tally | `scripts/suite_tally.py` over the six logs | 0 | 36,102 checks, 0 in-suite failures |
| ctrl suite | `MILAN_RV32_CC=<verified SDK>/bin/riscv32-linux-gcc test_ctrl_firmware.py --require-rv32 --jobs 4` | 0 | `test_ctrl_firmware: PASS`, RV32 arm included (dev's merged firmware) |
| differential | `maap_differential.py` / `--self-test` | 0 / 0 | 12/12; 16/16 controls caught |
| lint ratchet | `scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| parser ratchet | `scripts/xvlog_gate.py --check` (Vivado 2026.1 xvlog, under the lock, alone) | 0 | `0 finding(s) == ratchet; 0 hdl/, 0 pinned processors` (535 s; #682's pin cleared the two processor findings) |
| Yosys OOC | `syn/yosys/ooc.sh KL_maap` | 0 | 515 LUT / 278 FF / 59 CARRY4 |
| Yosys portability | `syn/yosys/run.sh --top KL_maap` | 0 | PASS; tied-input and tap-purity PASS |
| test evidence | `measure_test_evidence.py --check` / `--selftest` | 0 / 0 | 0 unexplained readers; 105/105 |
| docs and code quality | the 24-command set (as Part A), plus `check_em_dash.py --base 291710b1` and `git diff --check 291710b1 HEAD` against the dev tip | all 0 | at `48f12dc14` |
| shipping route and standalone endpoints | the recipe, `--single-thread-synthesis` (Part B section) | 0 / 0 | route 2,937 s; standalone 3,881 s |
| resource gate | `pp_resource_gate.py check` x3 against F; `record --write` x3; `check-baseline`; `check` x3 against the new record | all 0 | PASS x3 (route LUT +434 of +500, slices +54 of +80, WNS +0.241, WHS +0.029); `baseline PASS: 3 endpoints` at `48f12dc14` |
| gate self-tests | `pp_resource_gate.py --selftest`, `pp_resource_gate_mutants.py` | 0 / 0 | 260 arms + 500 cases; 174 of 174 mutants fail |
| receipts | `regen_record.py` x3 per record set, `--git 48f12dc1` and `--git c7b69cd0` | 0 x6 | `record EQUAL` x6 |

### Area (Part A)

Yosys OOC `KL_maap` (`syn/yosys/ooc.sh`): 515 LUT / 278 FF / 59 CARRY4 (round 1: 474 / 278 / 59; dev: 637 / 268 / 74). The zero-seed substitution adds a 16-bit zero detect and a reset-value mux. abc's mapping of equivalent netlists also moves by about 20 LUTs. In the same Yosys flow, the round-1 source maps to 474 LUTs. The identical logic with only the seed routed through the new `mac_seed_w` wire maps to 496. The fix maps to 515. Against dev the module is -122 LUT / +10 FF, within +40 / +40.

The Vivado measurements were not run at the Part A head itself. The assignment places them in Part B, on the merge result with #682, under `--single-thread-synthesis`. That option arrived with the merge, and the Part A tree's multi-threaded recipe peaked at 18.44 GB in round 1, above the 17 GB ceiling.

### Part B: merge and re-record

**Merge.** `git merge --no-ff --no-commit origin/dev` (dev `291710b180ca9196780a6d17f2517957c9bcb89c`, which contains the PR #692 merge) conflicted in four files, all record or record-description files: `syn/ooc/pp_resource_baseline.json`, `docs/design/AREA_BUDGET.md`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` and `docs/findings/README.md`. The lane's side of each held only round 1's record and its description. Each was resolved to dev's side (baseline F with its own text), which is coherent with itself. The re-record below then replaced records and text together, so no lane's JSON survives by textual choice. `sw/firmware/ctrl/maap/README.md` auto-merged; dev's hunks are in other sections. The protocol-processor gitlink moved `ead80360` -> `2ad2f845` (the submodule toplevel was verified before its checkout); gptp-processor and verilog-axis are unchanged. Merge commit `e519e31ff55af7dcae253da280baad531a7ad40c`, parents `30fce4b0a` and `291710b18`.

**Recipe on the merge result** (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md` as merged). The work directory was fresh, and every `pp_baseline.py` step had `--single-thread-synthesis`. The route Tcl starts `set_param synth.maxThreads 1` and keeps `general.maxThreads 32`, as F. Each Vivado step ran under `flock $VIVADO_LOCK` with nothing else heavy in this unit.

| Step | rc | Duration |
|---|---|---|
| export, ax7101 and ax8x8 (SDK verified, `pp_baseline.py --selftest`) | 0 | 13 s |
| shipping route 1x1, `ExtraPostPlacementOpt`, default seed, synthesis and implementation in one process | 0 | 2,937 s |
| standalone 1x1 (`--integrated-clock`), 8x8 RTL elaboration, standalone 8x8 (`--integrated-clock`) | 0 | 3,881 s |
| recipe symlink removal (`sw/builder/out`, `configs/generated/{ltn_rom,ucode}.hex`), `git diff --check` | 0 | 0 s |

Memory: peak 12.37 GB current / 11.57 GB anonymous (01:47, route synthesis); the 17 GB guard never fired.

**Gate against F, then the record.**

| Endpoint | F | This measurement | Delta | Tolerance | `check` rc |
|---|---|---|---|---|---|
| route-1x1 LUT / FF / slices | 49,957 / 54,274 / 15,734 | 50,391 / 54,263 / 15,788 | +434 / -11 / +54 | +500 / +600 / +80 | 0 |
| route-1x1 RAMB36 / RAMB18 / DSP | 74 / 27 / 14 | 74 / 27 / 14 | 0 | 0 | |
| route-1x1 WNS / WHS | +0.124 / +0.031 ns | +0.241 / +0.029 ns | +0.117 / -0.002 | floors +0.03 / 0, fall 0.25 | |
| route status | | 100,934 / 100,934 routable nets routed, 0 routing errors | | | |
| ooc-1x1 LUT / FF / RAMB36 / RAMB18 / DSP | 23,179 / 19,779 / 16 / 3 / 8 | identical | 0 | | 0 |
| ooc-8x8 LUT / FF / RAMB36 / RAMB18 / DSP | 30,135 / 27,380 / 21 / 5 / 8 | identical | 0 | | 0 |

Then `record --write` x3 (rc 0), the three `measured` notes rewritten to name this measurement (`e519e31f`, dev `291710b1`, processor `2ad2f845`, one synthesis worker, one process), `check-baseline` (rc 0, `baseline PASS: 3 endpoints`), and `check` x3 against the new record (rc 0). The JSON diff is 44 leaves under the three records (route figures and scopes, three input digests) plus the three notes; no tolerance, floor, ceiling or identity moved. Gate self-tests: `pp_resource_gate.py --selftest` rc 0 (260 arms, 500 generated cases), `pp_resource_gate_mutants.py` rc 0 (174 of 174).

Where the route moved. `KL_maap` in the routed hierarchy (`milan_datapath/g_maap.maap_engine`) is 429 LUT / 279 FF, against 479 / 267 for the previous `KL_maap` in the 649 resource map: -50 / +12, within the +40 / +40 item budget. The wrapper scopes moved -47 LUT / -2 FF against F. The repository inputs differ from F's parent `4d253880` only in `KL_maap.sv` and the comment lines of `milan_datapath.sv`, and the submodule pins are F's. Against the round-1 route on `c7b69cd0`, the largest movements are in blocks this lane does not touch: the gPTP shadow's own logic +690 against its engine -452 (a flattening boundary moving), `ts_counter` +75, `crf_rx` +73, `csr` +63. The worst setup path is now 41 logic levels inside the processor, `u_pp/u_notify/wr_ix_r_reg[1]_replica_1` to `u_pp/u_tx_arbiter/slot_r_reg[2]`, 19.494 ns data delay. Corners: Slow 0/85 C WNS +0.241, WHS +0.102; Fast 0/85 C WNS +1.434, WHS +0.029. No STOP condition: the gate passes, the route completes and meets both floors, and `KL_maap` is inside its budget.

**Docs for the new record.** `docs/design/AREA_BUDGET.md` names #686's measurement as the gate's record. It updates the headroom table (50,391 LUT, 79.48 %, 12,351 over NFR-RES-01; 54,263 FF; 15,788 slices, 62 free; +0.241 / +0.029 ns), the critical-path and previous-image lines, the allocation (`milan_datapath` 41,809 LUT, 65.9 %; wrapper 23,081, at most 10,730, a 12,351-LUT cut, 54 %) and the fall-limit sentence (the floor binds first after a fall of 0.211 ns). It adds the fifth re-baseline's delta from F. The #234 findings header and the findings index say F was the record until #686's 2026-10-08 re-baseline and point to the area budget for it.

### Receipts (R549-1-F4)

`resource-receipts/` in this directory holds the raw receipts of both record sets:

- `r2-48f12dc1/`: the records the branch now carries, measured on `e519e31f` and committed in `48f12dc1`.
- `r1-c7b69cd0/`: the round 1 records that R549-1 reviewed.

Each set has the executed Tcl, the utilization, hierarchy, route status and timing-summary reports, the CARRY4 census rows, an input manifest per endpoint with the non-repository inputs' digested bytes, `record.json`, the Vivado logs, the export and orchestration receipts, every `pp_resource_gate.py` output, and `files.sha256` of every original. `scripts/collect_receipts.py` wrote them and refuses unless the manifest reproduces the record's input digest. `scripts/regen_record.py <clone> <set>/<endpoint> <endpoint> --git <commit>` rebuilds identity, input digest, figures and scopes with that commit's own gate parsers, and requires equality with the committed record. It prints `record EQUAL` for all six (each `regen.log`). Every file is under 200 KB; larger ones are gzipped or reduced to the part the gate reads. Host path prefixes are replaced by role placeholders. See `resource-receipts/README.md`.

### Open item: dev moved after the merge

At the final fetch (04:17 CEST) dev was `99e4eb6c14462aafa84bb1ac597fd241abc1a240`, which is PR #693 merged on top of `291710b1`. It keeps GMII RX pad captures in ILOGIC: `sw/litex/patches/0007-liteeth-gmii-rx-capture.patch`, `sw/litex/gmii_rx_capture.xdc`, the IOB-pack check and tests, and regenerated `tb/verilator/gptp_txts` models. It records no resource baseline. It changes the shipping export, so a merge of this head with that tip moves the image again, and the area budget's re-baseline rule applies to the candidate merge result. The assignment's Part B was one `--no-ff` merge of the dev that contained #682, followed by the re-record. This lane did not merge again; candidate-merge validation is the manager's merge turn.

### Round 2 resources and hygiene

- The unit's memory peak over the whole round was 16.56 GB (`memory.peak`, page cache included), with no `high`, `max` or OOM event. The Vivado chain peaked at 12.37 GB current / 11.57 GB anonymous. The Verilator phases ran two lanes at `VERILATOR_JOBS=2`.
- Vivado ran strictly one job at a time under `flock $VIVADO_LOCK`: the parser ratchet twice and the recipe chain once. Nothing else heavy ran in this unit beside it.
- The recipe's three temporary symlinks were created by the export and removed by the chain's last step, before the re-record commit. `git status` is clean at `48f12dc14`, with no untracked symlink and the submodules clean at their pins.
- While the receipt regenerator was being developed, four small temporary directories and one small file were written under `/tmp`. They were removed at once. The script now runs under `TMPDIR` and deletes only its own directory.
- Scratch (exports, checkpoints, logs and builds) stays under `$VALIDATION_STORAGE/686-a565/r2/`. Nothing over 200 KB is in this directory. `/data` has 149 GB free.
- The `Round 2 changes` file:line references are at `30fce4b0a`. The merge and the re-record do not touch those files, so they hold at `48f12dc14` too.

### Follow-up deviation list (for the manager to file; not implemented here)

1. compare_MAC in the rProbe!/PROBE and rDefend!/DEFEND cells (Table B.7 note d).
2. DEFEND requested_* echo (B.3.6.6).
3. generate_address generator period, distribution and seed (B.3.6.1).
4. No PortOperational! input (B.3.5.9).
5. A PROBE parsed while a frame is on the wire is not defended. A missed fourth PROBE is settled by the prober's ANNOUNCE and compare_MAC.
6. Tagged MAAP PDUs are not parsed.
7. **New:** supplied-seed validation against the Table B.9 pool.
8. **Candidate (R548-1-S2):** truncated-PDU acceptance gate (`rbeat_r >= 3'd5`) has no check.

## Round 1

Status: REVIEW READY at `c7b69cd0fb2bdf980546ab413b3b82198267cbd8`. Every gate rc 0: maap suite and campaign, every datapath suite that instantiates `KL_maap`, the crflic campaign, ctrl + differential, lint, parser ratchet, docs and code-quality gates, Yosys OOC/portability, the shipping route (meets setup and hold floors), the standalone endpoints, the resource gate x3 and the re-record. No STOP condition: area within budget, route met, no register-map/filter/mailbox change, nothing outside scope. Not pushed (push and PR are outside this session's authority).

- Lane: branch `686-maap-annexb` from dev `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`
- Remote: `https://github.com/kebag-logic/milan-fpga.git` (confirmed)
- Assignment: issue #686 comment 6043036997. TAKEN: comment 6043296747. REVIEW READY: comment 6046944192 (head `c7b69cd0`).
- Authority: IEEE 1722-2016 Annex B (cited by clause; no text copied). Table B.7 was read from the rendered PDF page as well as the text extraction.
- Commits (one-line, no trailers, configured identity):
  - `a8364df1c` Conform KL_maap to IEEE 1722-2016 Annex B on the #686 items and grade each against its clause
  - `c6f5357a5` Document the Annex B contract of KL_maap and the deviations outside #686
  - `70297b2b4` Classify the maap mutation campaign as a DUT-source reader for the test-evidence ratchet
  - `7b2896568` Probe the crflic leg's Run B opening while KL_maap still probes, not after its ANNOUNCE
  - `c7b69cd0f` Re-record the resource gate's three endpoints after the KL_maap Annex B change, every tolerance, floor and ceiling unchanged

## Decisions made in public (TAKEN)

- Item 3 includes Table B.7 note b's conflict predicate. It is one predicate for PROBE, DEFEND and ANNOUNCE reception, so it became half-open (adjacent ranges no longer conflict, an empty range never conflicts) for all three.
- Item 3 includes the whole rAnnounce! row: compare_MAC (note d) in DEFEND, unconditional yield in PROBE.
- Out of the four items and NOT changed (recorded in MAAP_FABRIC.md and to be listed in REVIEW READY for a follow-up decision): compare_MAC in rProbe!/PROBE and rDefend!/DEFEND; the DEFEND requested_* echo (B.3.6.6); the generate_address generator/seed (B.3.6.1); no PortOperational! input (B.3.5.9); a PROBE parsed while a frame is on the wire is not defended.

## Changes (file:line at `7b2896568`)

| Item / purpose | Clause | file:line | Change |
|---|---|---|---|
| 1 cdl | B.2.1 | `hdl/ieee1722/maap/KL_maap.sv:114`, `:234` | `CDL_C` = 16 in every frame (was 28) |
| 1 DEFEND destination | B.2.1 | `KL_maap.sv:227-228`, `:320-324`, `:372` | RX captures the source MAC (bytes 6..11); DEFEND latches it into `tx_dst_r` and sends to it; PROBE/ANNOUNCE stay multicast |
| 2 probe timer | B.3.3 Table B.8, B.3.4.2 | `KL_maap.sv:120-124`, `:161` | draw 518 + lfsr[5:0] ms (was 500 + lfsr[6:0]) |
| 2 announce timer | B.3.3 Table B.8, B.3.4.1 | `KL_maap.sv:125`, `:162` | draw 30488 + lfsr[9:0] ms (was 3000 + lfsr[10:0]) |
| 3 range per message type | B.2.5-B.2.8, Table B.7 note b | `KL_maap.sv:164-190`, `:330-337` | one capture set: requested_* for PROBE/ANNOUNCE, conflict_* for DEFEND (same lanes, beat chosen by type) |
| 3 conflict predicate | Table B.7 note b | `KL_maap.sv:192-199` | half-open 17-bit overlap, zero counts never conflict |
| 3 DEFEND overlap | B.2.7, B.2.8 | `KL_maap.sv:200-203` | max/min overlap from the shared range |
| 3 compare_MAC | B.3.6.4, Table B.7 note d | `KL_maap.sv:205-210`, `:257-261` | octet-reversed compare; rAnnounce! in ANNOUNCE (DEFEND) re-addresses only when this station is not the lower |
| 4 four PROBEs | Table B.7, Table B.8 | `KL_maap.sv:118-119`, `:355`, `:365`, `:388-396` | `PROBE_SENDS_C` = 4 (ReserveAddress! sProbe + 3 retransmissions) |
| 4 first PROBE at once | Table B.7 ReserveAddress! | `KL_maap.sv:356` (Begin!), `:366` (Restart!) | timer loaded 0 |
| 4 ANNOUNCE at once | Table B.7 probeCount! | `KL_maap.sv:388-391` | ANNOUNCE state with timer 0 after the 4th PROBE |
| frame integrity | B.3.6.5-B.3.6.7 | `KL_maap.sv:213-220`, `:237`, `:373`, `:381` | `tx_off_r` latched at every send; a Restart! cannot rewrite a frame on the wire |
| one decision per cycle | Table B.7 / B.3.2 sequential execution | `KL_maap.sv:253-264`, `:345-399` | priority disable > Restart! > sDefend > timer send |
| banner | -- | `KL_maap.sv:6-49` | Annex B contract and remaining deviations |
| harness | all items | `tb/verilator/maap/sim_main.cpp` | re-pointed to the clauses (table below) |
| campaign | all items | `tb/verilator/maap/mutants.py` (new) | 22 planted defects + clean control |
| suite target | -- | `tb/verilator/maap/Makefile` | `all: run mutants`; `MAAP_RTL`, `MDIR`, `VERILATOR_JOBS` overrides |
| differential | items 1-4 | `sw/firmware/ctrl/test/test_maap_differential.cpp:112-206`, `:208-237` | #686 deltas become equalities; parent graded on Annex B |
| differential controls | -- | `sw/firmware/ctrl/test/maap_differential.py:4`, `:55-64` | test renamed `ProbeTimingAndCount`; parent bound 581, count 5 controls |
| consumer timing | -- | `tb/verilator/milan_dp/sim_crf_licence.cpp:39`, `:832-854`, `:868-870` | probe while the claim is in flight; ANNOUNCE check and offset read move to phase A |
| evidence ratchet | -- | `scripts/measure_test_evidence_readers.py:72-76` | disposition for the new DUT-source reader |
| resource baseline | -- | `syn/ooc/pp_resource_baseline.json` (records of `route-1x1`, `ooc-1x1`, `ooc-8x8`; `measured` notes at `:450`, `:917`, `:1374`) | written by `pp_resource_gate.py record --write` from this lane's recipe run; every tolerance, floor and ceiling unchanged |
| area budget | -- | `docs/design/AREA_BUDGET.md:102-104`, `:114-126`, `:132-137`, `:165`, `:198-199` | names the #686 record as the gate's record; headroom table, slice/critical-path lines, allocation figures and fall-limit sentence follow it; the third re-baseline's delta |
| findings | -- | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:5`, `docs/findings/README.md:25` | the 2026-10-05 D record is no longer called the current record |
| docs | -- | `docs/design/MAAP_FABRIC.md:36`, `:42-135`, `:138-139`, `:171-177` | Annex B contract, cells table, remaining deviations, history, TB bullet |
| requirement trace | FR-MAAP-01 | `docs/reference/FR_NFR.md:167` | ledger row names the conformed clauses and links the deviations |
| docs | -- | `docs/testing/TESTING.md:519`, `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:3-5`, `sw/firmware/ctrl/maap/README.md:165-187`, `tb/verilator/milan_dp/README.md:455`, `:961-962`, `tb/verilator/pp_shadow/README.md:363` | wording follows the new contract |

## Tests and the planted defect each catches

Harness `tb/verilator/maap/sim_main.cpp` (120 checks). Campaign `tb/verilator/maap/mutants.py` (22 mutants, each must exit 1 with its named `[FAIL]`).

| Item | Named check (sim_main.cpp line) | Planted defect (mutants.py name) |
|---|---|---|
| 1 | `B.2.1 cdl 16 (Begin! PROBE 1)` (:223) | `cdl_28` |
| 1 | `B.2.1 DEFEND DA = PROBE source (above)` (:309) | `defend_to_multicast` |
| 1 | `B.2.1 DEFEND DA latched at send` (:343) | `defend_destination_not_latched` (reads the live RX register) |
| 1 | `B.2.1 PROBE DA multicast (Begin! 1)` (:225) | `every_frame_to_the_prober` |
| 1 (B.2.8) | `B.2.8 conflict_count = overlap (below)` (:317) | `overlap_count_to_our_end` |
| 2 | `B.3.4.2 probe T < 600 ms (campaign)` (:506) | `probe_draw_7_bits` |
| 2 | `B.3.4.2 probe T > 500 ms (campaign)` (:505) | `probe_base_500` |
| 2 | `B.3.4.1 announce T > 30 s` (:295) | `announce_base_3s` |
| 2 | `B.3.4.1 announce T < 32 s` (:296) | `announce_draw_11_bits` |
| 2 | `B.3.4.1 announce T randomized` (:298) | `announce_not_randomized` |
| 3 | `B.2.7 ANNOUNCE conflict_* is not its range` (:375) | `announce_judged_on_conflict_fields` (the old behaviour) |
| 3 | `note b adjacent above: no conflict` (:378) | `inclusive_range_end` |
| 3 | `note b adjacent below: no conflict` (:381) | `inclusive_range_start` |
| 3 | `note b empty range: no conflict` (:384) | `empty_range_conflicts` |
| 3 | `T.B7 note d: lower MAC keeps range` (:372) | `no_compare_mac` |
| 3 | `T.B7 rAnnounce!/PROBE: no compare_MAC` (:404) | `compare_mac_while_probing` |
| 3 | `T.B7 rAnnounce!/DEFEND: re-address` (:390) | `compare_mac_unreversed` |
| 3/4 | `frame on the wire keeps its offset` (:421) | `restart_rewrites_the_frame_on_the_wire` |
| 4 | `T.B7 Begin!: four PROBEs before ANNOUNCE` (:251) | `three_probes` |
| 4 | `T.B7 Begin!: first PROBE at once` (:249) | `first_probe_after_a_timer` |
| 4 | `T.B7 Restart!: first PROBE at once` (:396) | `restart_probe_after_a_timer` |
| 4 | `T.B7 probeCount!: ANNOUNCE at once (Begin!)` (:253) | `announce_after_a_timer` |

The campaign refuses to run unless every item 1-4 has a mutant, and every anchor must occur exactly once. A build failure or abnormal exit never counts as a kill. First campaign run caught 22/23 rows: `announce_draw_11_bits` escaped its named check because the wait budget equalled the bound, so the over-long interval timed out instead of being measured. Budgets were widened past the bounds (`sim_main.cpp:33-36`); the rerun caught 23/23.

Differential (`maap_differential.py --self-test`): 12 positive cases; 16/16 controls caught (core wire, release, nine Table B.7 cells, 1/500/600 ms probe defects, parent bound 581 -> 499, parent count 5 -> 4).

crflic leg (`make -C tb/verilator/milan_dp crflic-mutants`): pending in the chain (see gate table).

## Coverage table

| Item | Clause | Graded by | Defects caught |
|---|---|---|---|
| 1 | B.2.1 | golden frames (B.2/Figure B.1) for every PROBE/ANNOUNCE of two walks; cdl in PROBE, ANNOUNCE, DEFEND; DEFEND DA from two probers and under backpressure; multicast after a DEFEND; differential raw-frame equality with the core | 5 |
| 2 | B.3.3/B.3.4 | 456 probe intervals over 150 walks (517.2..581.0 ms observed, both ends of the draw reached); 24 announcement intervals (30.53..31.50 s observed); differential parent intervals over 1024 phases (517.2..581.1 ms) | 5 |
| 3 | B.3.2/Table B.7 | every conflict cell in both states, note b edges (adjacent above/below, empty, one shared address), compare_MAC both ways with octet-reversal sensitive MACs, conflict fields ignored for ANNOUNCE | 8 |
| 4 | Table B.7 | first PROBE latency at Begin!, Restart! and the seeded Begin!; 4 PROBEs then ANNOUNCE at once in 152 walks | 4 |

Line coverage (`make -C tb/verilator/maap coverage`): `KL_maap.sv` 100.0 % (167/167), gate 95 %: PASS.

## Gate table

| Gate | Command | rc | Result |
|---|---|---|---|
| maap suite | `make -C tb/verilator/maap` | 0 | 120 checks 0 failures; mutants 23/23 (tally 143 checks) |
| maap coverage | `make -C tb/verilator/maap coverage` | 0 | 100.0 % (167/167) |
| milan_dp | `make -C tb/verilator/milan_dp` | 0 | 12,065 checks, 0 failures, 1,985 s (first run rc 2 on the crflic leg, fixed in `7b2896568`) |
| pp_shadow | `make -C tb/verilator/pp_shadow` | 0 | 2,184 checks, 0 failures |
| capture_coherence | `make -C tb/verilator/capture_coherence` | 0 | 21,194 checks, 0 failures |
| milan_dp_mclk | `make -C tb/verilator/milan_dp_mclk` | 0 | 168 checks, 0 failures |
| milan_dp_render | `make -C tb/verilator/milan_dp_render` | 0 | 334 checks, 0 failures |
| suite tally | `scripts/suite_tally.py` over the six logs | 0 | 36,088 checks, 0 in-suite failures |
| crflic campaign | `make -C tb/verilator/milan_dp crflic-mutants` | 0 | obj_crflic leg 417 checks, 0 failures; campaign 7/7 (control passes, 6 mutants caught), 747 s |
| ctrl suite | `test_ctrl_firmware.py --require-rv32` (verified SDK) | 0 | PASS |
| differential | `maap_differential.py` / `--self-test` | 0 / 0 | 12/12; 16/16 controls |
| lint ratchet | `scripts/lint_rtl.py --check` | 0 | 90 <= 90; maap 1 <= 1 (pre-existing `rx_msg_r` truncation) |
| parser ratchet | `scripts/xvlog_gate.py --check` (Vivado 2026.1 xvlog, under the lock) | 0 | PASS: 81 hdl/ + 52 pinned files; 0 hdl/ findings; 2 pre-existing pinned-processor findings == ratchet; 218 s |
| Yosys OOC | `syn/yosys/ooc.sh KL_maap` | 0 | 474 LUT / 278 FF / 59 CARRY4 (dev 637 / 268 / 74) |
| Yosys portability | `syn/yosys/run.sh --top KL_maap` | 0 | PASS, 1,949 cells; tied-input and tap-purity PASS |
| test evidence | `measure_test_evidence.py --check` / `--selftest` | 0 / 0 | 0 unexplained readers (`--check` re-run 0 at `c7b69cd0`) |
| docs | docs_check, check_em_dash (base e21c1ca0) + selftest, gen_toc check/anchors, doc_style, doc_paths, module_matrix, feature_status, DOC_MAP, solution/submodule docs | all 0 | at `7b2896568` and again at `c7b69cd0` (after the area-budget and findings edits) |
| code quality | naming, port_contracts, fail_fast, todo_ownership, hygiene, sv/cpp/py idiom, rtl_source_lists, pp_srcs, `git diff --check e21c1ca0 HEAD` | all 0 | at `7b2896568` and again at `c7b69cd0` |
| shipping route | recipe "Integrated measurements", 1x1 `endstation_ax7101_1x1_tdm8`, `place_design -directive ExtraPostPlacementOpt`, Vivado 2026.1 | 0 | 1,891 s. WNS +0.317 ns (floor +0.03), TNS 0; WHS +0.036 ns (floor 0), THS 0; WPWS +0.264 ns; 100,981/100,981 routable nets routed, 0 routing errors. 50,088 LUT / 54,188 FF / 15,843 slices / 74 RAMB36 / 27 RAMB18 / 14 DSP |
| standalone endpoints | recipe "Standalone measurements": 1x1 with `--integrated-clock`; 8x8 RTL elaboration then standalone | 0 | 2,548 s. ooc-1x1 23,178 LUT / 19,776 FF / 16 / 3 / 8; ooc-8x8 29,853 / 27,370 / 21 / 5 / 8 (both identical to the previous record) |
| resource gate | `pp_resource_gate.py check <dir> --endpoint` route-1x1 / ooc-1x1 / ooc-8x8 against the 2026-10-05 record | 0 / 0 / 0 | PASS x3 (route: LUT -230, FF -26, SLICE +54 of +80, WNS +0.209, WHS 0) |
| resource record | `record --write` x3, then `check-baseline`, then `check` x3 against the new record | 0 x3, 0, 0 x3 | baseline PASS: 3 endpoints; rechecks PASS |
| gate self-tests | `pp_resource_gate.py --selftest`, `pp_resource_gate_mutants.py` | 0 / 0 | 260 arms + 500 generated cases PASS; control passes, all 174 mutants fail |

Head each gate saw: milan_dp (20:35-21:08) and the crflic campaign ran at `7b2896568`. The other Verilator suites, ctrl, lint, Yosys and the first docs pass ran at `70297b2b4`. From `70297b2b4` to `c7b69cd0`, only `tb/verilator/milan_dp/{sim_crf_licence.cpp,README.md}` (built only by `tb/verilator/milan_dp/Makefile`), the resource JSON and three docs change. The route, standalone endpoints and parser ratchet read the tree at `7b2896568`, whose RTL is that of `c7b69cd0`. The docs/code-quality pass and `check-baseline` re-ran at `c7b69cd0`.

## Area

Yosys OOC (`syn/yosys/ooc.sh KL_maap`, the repository's OOC measurement): dev 637 LUT / 268 FF; branch 474 LUT / 278 FF. Delta -163 LUT / +10 FF, within +40 / +40. One shared range register and one comparator set replace the two 48-bit range captures and two inclusive predicates; the source MAC, DEFEND destination and frame offset latches add FFs.

Vivado in context (shipping route hierarchy, `milan_datapath/g_maap.maap_engine`): branch 435 LUT / 279 FF. Dev's figure is 479 LUT / 267 FF in `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:223` (dev `241f9184`; `KL_maap.sv` is unchanged from 2026-08-25 to `e21c1ca0`). Delta -44 LUT / +12 FF, within +40 / +40.

Image against the 2026-10-05 record (which spans dev `506d91db`..`e21c1ca0` as well as this change): -230 LUT, -26 FF, +54 slices (tolerance +80), WNS +0.108 -> +0.317 ns. Slice headroom is now 7 of 15,850 (was 61): a packing effect, with LUTs and FFs both lower. The worst setup path moved to the CPU's DMA bridge (21 logic levels).

Evidence (scratch, not copied here; sha256, bytes):

| Artifact | sha256 | bytes |
|---|---|---|
| route `baseline.log` | `94ea82713519d3c2c4abf02212a7baa32e2f920531196f2d85f56e6de0726d90` | 977,052 |
| route `baseline_timing.rpt` | `0267fd270778a8d537ec9f558a7baeda0afd8e184097baaf759e0f0ec2f256b7` | 1,277,551 |
| route `baseline_utilization.rpt` | `3002be04511894c51ade488389aa533e0867a9b111815e93d0513aa9f34dfd2d` | 13,319 |
| route `alinx_ax7101_route_status.rpt` | `d7846c034fbf8b962f2695ef7ef90c0ce5eb1b048c90ae5fc7888854f5c6d1b8` | 651 |
| route `baseline_hierarchy.rpt` | `57c9f897433b75feeca45219af4c2b22160d7f9e090d6cb7dc25e562eaa0daed` | 46,405 |
| ooc-1x1 `baseline.log` | `60794406ac1d2208b44e3caa022ef162f850647a921ee5081758da89a0106540` | 312,103 |
| ooc-1x1 `baseline_utilization.rpt` | `ef16c058577ba7f86bfd6a4fcf05ba11d9c92e423aba6ff0ffae545076a58cff` | 9,297 |
| ooc-8x8 `baseline.log` | `19aef6f97537e0af187bc673f093d75d7d33ba7f163dffab731306c913c16951` | 315,788 |
| ooc-8x8 `baseline_utilization.rpt` | `a2bb4512f3f5c2dc80985441e2c52af34c46340b7d97404fdd44db3dd0447b2f` | 9,297 |
| xvlog gate log | `4bf5acfc38c97c5c8e3f36282fb007db13bf83e7cc4a98f097edd9881a7732d3` | 1,025 |

## Incidents (process handling, no evidence affected)

- The first `crflic-mutants` start inherited no `VERILATOR` (an `export` placed before one `&` job applied only to that job) and began re-Verilating `obj_crflic` with the system 5.052 while the full milan_dp rerun started. Both were stopped, `obj_crflic` was deleted, and milan_dp was rerun from scratch with the pinned 5.050; every suite log records 5.050.
- A later chain was believed dead because this host rewrites `ps` output through a filter, so `ps | grep` showed nothing. Its script file was then overwritten while bash was still reading it, which started a second campaign in the same directory. Both process groups were terminated (their temp dirs cleaned by the driver's handler), `obj_crflic` was deleted again, and one chain was restarted from a read-only copy (`chain-run2.sh`). No route or standalone Vivado step had started. Process checks now use `/proc` and `pgrep -a`.
- The first shipping route (lock acquired 21:44:20) was OOM-killed at 21:48 with the whole session when Vivado's parallel synthesis took the 12 GB unit to its cap. No report was written. The run's directory was discarded and a fresh one rebuilt from the 19:58 export (the RTL is unchanged since: `7b2896568` touches only the crflic testbench and a README), and the route restarted at 21:50:50 under a 20 GB unit with a unit-scoped memory guard (`chain-mem3.log`).
- Memory on the restarted route: synthesis runs seven parallel worker processes beside the main Vivado (about 2.2 GB each). The unit peaked at 18.44 GB memory.current / 17.43 GB anonymous at 21:59:05 (samples 21:58:50 17.76 GB, 21:59:20 14.05 GB), about 1.4 GB over the 17 GB target for under 45 s; the first guard's stop threshold (18 GiB anonymous) was not reached. The guard was then tightened (5 s polling, page-cache reclaim above 16 GB, stop this unit's Vivado above 17 GB anonymous); synthesis finished at 22:00 and the unit fell to 6.5 GB for implementation. The guard never fired. A first pattern-based stop of the old logger also ended two idle tool shells in this unit; the chain and Vivado were unaffected (checked through `cgroup.procs`).

## Resources and hygiene

- Toolchains, the verified RV32 SDK copy, exports, logs and checkpoints stay in scratch; nothing over 200 KB here.
- Memory: the Verilator suites stayed under 9 GB (max about 4.1 GB in the 12 GB unit). The Vivado steps ran in the 20 GB unit one at a time under the lock: route synthesis peaked at 18.44 GB current / 17.43 GB anonymous for under 45 s (see Incidents), the 8x8 standalone at 16.18 GB / 14.53 GB, implementation at about 7 GB.
- The recipe's temporary symlinks (`sw/builder/out`, `configs/generated/{ltn_rom,ucode}.hex`) were removed after the last Vivado step, before the last commit; `git status` is clean at `c7b69cd0`.
