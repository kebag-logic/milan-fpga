[A524] ADP MTXW walk: every cell cited to Milan v1.2 and IEEE 1722.1-2021, one mutant per F04.3 arc, and the available_index interop note adjudicated (#85, GAP-16)

Closes #85
Relates to #39
Relates to #40
Relates to #41

#39, #40 and #41 were closed by PRs #144 and #136; their acceptance still holds at this head (#39: the model lint's L11 rules, their two-configuration refusal arm in `tb/desc_store/lint_mutations.py`, the reported ADP inputs and `docs/guides/integrator.md` section 6; #40: `tb/adp_engine` P11, `tb/pp_top` section AD, the overlay feed and the `cfg-*` arms; #41: `tb/adp_engine` P12, `tb/pp_top` AD0 and the `gate-enable-dropped` arms, all KILLED below).

## What this changes

Tests and the documents they cite. No RTL change: `hdl/` is untouched.

The P13 MTXW walk in `tb/adp_engine` (45 F04.2 cells, 33 F04.3 cells, from PR #136) already drove every cell, the five cells #85 found undriven among them. This PR completes #85's items against it:

1. **Every cell cited, as 04 derives it.** Each cell of the walk's two tables now carries the Milan v1.2 clause that rules its next state, frame and timer action, and the IEEE 1722.1-2021 clause it replaces or follows; both are printed in every failure message of the cell. `docs/architecture/04_adp_engine.md` gains F04.7 (every advertise cell: state, event, class, next state, transmit, timer, Milan, IEEE) and F04.8 (every F04.3 arc with its guard, action, clauses and walk cell). Two new checks count the cells that cite both: 45 of 45 and 33 of 33. Seven cells that cited the table now cite the clause that rules them: §5.6.1 for the not-started column's two timer cells and its SHUTDOWN cell, §5.6.3.5.9 for TMR_DELAY in the draw phase of DELAY, and §5.6.3.1 for an ENTITY_DISCOVER of another entity in DOWN and both DELAY phases. The walk still ends with `CHECK(adv_cells == 45)` and `CHECK(disc_cells == 33)`.
2. **The five cells** (DOWN x DISCOVER, GM_CHANGE, SHUTDOWN inert; DELAY x LINK_DOWN cancels with no ENTITY_DEPARTING; DELAY x SHUTDOWN departs and resets available_index, both DELAY phases): unchanged and re-graded.
3. **One mutant per F04.3 arc.** Eight `arc-*` arms in `tb/adp_engine/mutations`, each required to fail its arc's own check (`P13 F04.3 arc <name>: walked and graded`), not only some cell: the entry arc (an unbind no longer clears the state), the discovery's T-ADP-NOADP arm, the grandmaster and domain guard at both of its sites, the fresh-index re-arm, the restart detector at its boundary (`>=` for `>`), DEPARTING's EVT_TK_DEPARTED and the NOADP expiry's. With the two mutations #85 names (`walk-down-answers-discover`, `walk-delay-ignores-link-down`), the campaign (`make -C tb/adp_engine mutants`, `--jobs N`) kills 38 of 38 arms.
4. **The available_index interop note**, adjudicated in `tb/adp_engine/README.md` against the standard and the reference behaviour on record:
   - IEEE 1722.1-2021 §6.2.2.15 (and Figure 6-2): incremented after each ENTITY_AVAILABLE, reset to 0 on ENTITY_DEPARTING and at power-up. Milan v1.2 §5.6.2 adopts it unchanged. The engine's rule is that text. The former every-ADPDU, no-reset rule departs from it at ENTITY_DEPARTING only, and no receiver reads the index of an ENTITY_DEPARTING (IEEE §6.2.6.4, Milan §5.6.4.5.3).
   - The parent's B6, B7 and B8 bench lanes enumerated the network five times (2026-10-01 to 2026-10-03, read-only from their published evidence): this processor's index rises one per 6.96 to 6.99 s within a boot (one per ENTITY_AVAILABLE at the Milan cadence) and starts low after each restart; the reference Milan peer's rises one per 6.0 s with no repeat. Every identity gate passed.
   - No record contains an ENTITY_DEPARTING or a controller that tracks entities. The limit is restated, narrowed to that case: how a live controller (Hive, la_avdecc) handles an ENTITY_DEPARTING and the availability cycle that follows from index 0. Only a live controller can show it.

Also corrected: 04 §5 and the compliance review cited IEEE §6.2.2.9 (entity_capabilities) for available_index; it is §6.2.2.15.

## Evidence at head `a866973`

Pinned Verilator 5.050.

| Gate | Result |
|---|---|
| `./scripts/run_suites.sh` | rc 0: 33 suites, 1,021,451 checks, 0 failing (`tb/adp_engine` 1330, `tb/pp_top` 10,416) |
| `tb/adp_engine` | 1330 checks PASS (base 1328) |
| `make -C tb/adp_engine mutants` (`--jobs 4`) | 2 controls PASS, 38 of 38 arms KILLED, 40 of 40 |
| `./scripts/lint_hdl.sh` | rc 0, 41 modules |
| `./syn/yosys/run.sh` | rc 0, 42 tops, `all.v` parsed once, `KL_aecp_engine` Xilinx mapping OK |
| `make check` | rc 0 |
| `python3 scripts/gen_matrix.py --check` | rc 0, 94 rows, 0 untested |

### Mutation record (the eight new arms)

| Arm | What is broken | Failing checks |
|---|---|---|
| `arc-bind-keeps-discovered` | an unbind no longer clears the discovered state, so a sink bound again starts in TK_DISCOVERED | 46, arc 1 among them |
| `arc-discover-no-noadp-arm` | TK_NOT_DISCOVERED to TK_DISCOVERED arms no T-ADP-NOADP | 13, arcs 2 and 8 |
| `arc-not-discovered-no-guard` | TK_NOT_DISCOVERED ignores the grandmaster and domain | 14, arc 3 |
| `arc-fresh-no-rearm` | a fresh index does not restart T-ADP-NOADP | 5, arc 4 |
| `arc-restart-detector-off-by-one` | an index equal to the last one is taken as fresh | 10, arcs 5 and 6 |
| `arc-restart-skips-guard` | a stale index restarts the talker whatever its grandmaster and domain | 12, arc 6 |
| `arc-departing-silent` | ENTITY_DEPARTING departs without EVT_TK_DEPARTED | 4, arc 7 |
| `arc-noadp-expiry-silent` | a T-ADP-NOADP expiry departs without EVT_TK_DEPARTED | 4, arc 8 |

The 30 earlier arms fail exactly the counts in their README rows.

### Parent consumer set

milan-fpga dev `5fabb46e`, the processor gitlink at this head, with `parent-adoption-c8-bbf704ec.patch`, `parent-adoption-p2-p1-1269cdaf.patch` and `parent-adoption-c10-1269cdaf.patch` applied (all three apply cleanly):

| # | Command | rc | Result at dev `5fabb46e` + c8 + p2-p1 + c10, processor `a866973` |
|---:|---|---:|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 | every count 0 <= 0 (c-style cast, file-scope mutable, macro constant, unnamed enum, multi-declarator, long function, build without warnings) |
| 2 | `scripts/check_py_idiom.py` | 0 | every ratchet held |
| 3 | `scripts/check_rtl_source_lists.py` | 0 | 108 files in the `milan_datapath` closure, 4 of 4 consumer lists; protocol-processor 42/42 tops, 0 recorded |
| 3s | `scripts/check_rtl_source_lists.py --selftest` | 0 | 50 checks, 50 PASS |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 | 46 tracked sources derived, self-test passed |
| 5 | `scripts/check_port_contracts.py` | 0 | protocol-processor 1,759 ports, 111 <= 111 undocumented |
| 6 | `scripts/measure_naming.py --check` | 0 | 95 candidates, all recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0 | 72 <= 77, 10 <= 10, 0 <= 0, 3 <= 3 |
| 8 | `scripts/docs_check.py` | 0 | 0 findings across 186 md + 970 files |
| 9 | `scripts/xvlog_gate.py --check` (Vivado 2026.1 `xvlog` on `PATH`, alone, last) | 0 | `PASS (3 finding(s) == ratchet; 0 hdl/, 3 pinned processors)`; 145 s |
| 9s | `scripts/xvlog_gate.py --selftest` (alone) | 0 | PASS; 21 s |
| 10 | `sw/builder/test_builder.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (its gate 11 needs a local board build tree, as in the C10 and P1 records); 1,157 s |
| 11 | `scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j16` | 0 | 606, 606, 646, 311 checks, 0 failures; 224 s |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | lint pass |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 checks, 315 PASS, `RESULT: PASS`; 30 s |
| 15 | `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=3` | 0 | 9 `RESULT: PASS`, 0 FAIL; render and gmstep control campaigns 6 of 6 each; 1,578 s |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | **2** | two-stream leg 65 checks, 0 failures; shipping leg 155 checks, **2 failures, both T30 INTERNAL LAW** (`the fill at accept is the 8-event setpoint for every PDU got=227 exp=292`; `every PDU's first event is inside the law band got=285 exp=292`; first-event delay 18396..18821 cycles = 8.830..9.034 media ticks); 135 s. Per the assignment these go against milan-fpga #643 (open: "milan_dp_render T30 INTERNAL law depends on the feed's phase against the grid"); see the base control below |
| 16b | `python3 tdm8_render_mutants.py --leg-defects` (in `tb/verilator/milan_dp_render`, the part of gate 16's `run` recipe that make skipped after the failing leg) | 0 | 2 clean controls PASS (`ship --crf-only`, `ship --serial-only`), 3 of 3 leg defects caught; 5 of 5; 413 s |
| 17 | `scripts/check_sh_idiom.py` | 0 | every count held (no strict mode 5 <= 5, ...) |

**Base control for gate 16.** The same parent, with the processor submodule and gitlink
moved to `main` `5c71928a` and the render directory's build products removed, then
`make -C tb/verilator/milan_dp_render tdm8render -j16`: rc 2, the shipping leg's 155
checks with the same 2 failures, the same lines and the same numbers (18396..18821
cycles, got=227, got=285; T30 CRF LAW 17051..17055 cycles in both). `git diff
5c71928a a866973 -- hdl scripts syn` is empty: the render bench reads the same RTL and
generators at both. The failure is the parent's #643 at this dev revision, not this
lane's. It ran once, between gates 15 and 9 of this branch's earlier round at `1d5b680`, after
which the submodule and gitlink were restored and the render build products removed;
`hdl`, `scripts` and `syn` are identical at `5c71928a`, `1d5b680` and `a866973`. (Other records saw T30 pass: C10 at dev `1269cdaf`
with its processor, the issue #232 lane at dev `bbf704ec` with processor `3ab2e4da`; #643
records why: the law depends on the feed's phase against the grid, which the dev
revision and the processor's boot length both move.)

## Parent-visible list

- No port, parameter, register or behaviour change; the parent sees the processor of `5c71928a`.
- No parent patch beyond the three adoption patches above.
- The parent's `docs/reference/REGISTER_MAP.md` (`0x644` ADP_STATUS note) says available_index increments on every transmitted ADPDU, departing included. The processor resets it to 0 after an ENTITY_DEPARTING (IEEE §6.2.2.15). A parent lane may want to correct that sentence.

## Notes

- The engine banner (`hdl/adp/KL_adp_engine.sv`) keeps its earlier wording of the interop note, because this PR changes no RTL.
- The B6 enumeration is on the parent's `b6-review-evidence` branch; `629-review-evidence` carries a design lane's packet with no enumeration.
