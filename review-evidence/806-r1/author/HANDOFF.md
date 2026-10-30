# HANDOFF: #806 gPTP pin adoption (FPGA-gPTP main 135afd04) and the engine's portEnabled, executor [A701]

Status: **REVIEW READY** at `f99405af0b2caad46e84f50f8251ffbffaa80836` (worktree clean, every submodule at its gitlink, live remote dev `1e80128f` unchanged). Nothing pushed. Every gate is rc 0 at the head (gate table) except the resource gate's route-1x1 endpoint, which refuses on WNS alone (+0.032 ns, 0.408 ns under the record, tolerance 0.25): published as an owner decision. No STOP condition is met: the route fits (27 slices free) and every corner meets the build floor.

- Lane: $LANES/806-adopt-gptp, branch `806-adopt-gptp-135afd04`, from dev `1e80128f` (PR #805 merged)
- origin: https://github.com/kebag-logic/milan-fpga.git (verified)
- gptp-processor: toplevel and origin (https://github.com/Mister-M-alt/FPGA-gPTP.git) verified before every submodule git command
- gPTP pin: `f97c1803` -> `135afd04` (merge of PR #95, second parent `409c3075`; the two trees are identical, `b552de22`)
- Companion: `milan-fpga-companion.patch`, sha256 `aeeab9c8785d016c9cf7f062970034fa229c41d7849f06f8e7eb412af1ec5934`, 17,728 bytes (reviewed at `409c3075`)
- Assignment: the latest [A10] comment on #806
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/806#issuecomment-6510417817
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/806#issuecomment-6514645428

## Commits (one-line, no body, no trailer)

| # | Commit | Change |
|---|---|---|
| 1 | `f911adec` | gitlink `f97c1803` -> `135afd04` |
| 2 | `a20f458e` | the companion, `git apply --index --exclude=gptp-processor` (its gitlink hunk names `409c3075`, superseded by commit 1 at an identical tree); every pre-image and post-image blob equals the patch's |
| 3 | `e67ae2f1` | review finish, tests: preconditions and the two eff_link terms the companion's checks left unpinned |
| 4 | `f475329c` | pin-derived records through their generators |
| 5 | `12a7948f` | review finish, docs: the companion's port-enable section to the concise-style limit (7 findings), and the leg that grades it |
| 6 | `67d8d192` | behaviour docs: the loss page's detection table and the time-sync link-up re-arm rule |
| 7 | `cf3ef596` | review finish, tests: each link return's edge taken before the next phase reads asCapable (finding 5) |
| 8 | `8eea9d3c` | the gPTP integrator guide's port-enable seam row |
| 9 | `f99405af` | the adoption record: pin page section, changelog entry and Contents line, the area page's slice-headroom sentence and the gate's WNS refusal |

## Engine interface check (gptp-processor `f97c1803..135afd04`, hdl/)

- One external port: `KL_gptp_engine.port_enabled_i` (input). One internal: `KL_gptp_tx_slot.cancel_i`. One localparam added (`PE_SLOT_C`). No parameter change; source set unchanged (three files modified, none added or removed).
- Parent consumers of the engine: `KL_gptp_shadow` (companion wires it) and `tb/verilator/gptp_plane/gptp_plane_wrap.sv` (companion ties it 1). Consumers of the shadow: `milan_datapath` (companion: `eff_link_w`), `gptp_shadow_wrap.sv` and `gptp_txts_wrap.sv` (companion ties 1). `tsn_fuzz`'s co-simulation and the gptp_tables suite use `gptp_shadow_wrap`.

## Review of the companion as milan-fpga code

Verified, no change needed:
- `eff_link_w = i_link_up & cfg_sw_link & (cfg_linkg_dis | linkg_est_w)` (`milan_datapath.sv:3194-3195`); `cfg_sw_link` is `LINK_CTRL[0]` (`milan_csr.sv:2854`); `i_link_up` is a `MultiReg` into the Milan clock domain (`sw/litex/milan_soc.py:1921`); the shadow runs on `axis_clk` with root `axis_resetn`, so no synchroniser is needed and no link event resets the plane.
- `link_est_o` is receive-clock liveness only (`KL_link_guard.sv:320`), so the shadow's recovery request, which reinitialises the MAC through the guard, does not feed back into portEnabled.
- A withdrawn frame leaves nothing in the shadow: the gearbox takes `valid & ready` only (`KL_gptp_shadow.sv:799`), the ticket parses and allocates on accepted beats only (`KL_gptp_txticket.sv:147`, `:191`), and the credit is a read-only level with `outstanding` moving on the accepted end of frame.
- Clauses checked against the texts: IEEE 802.1AS-2011 10.2.4.11 (portEnabled: MAC_Operational and the administrative port state); Milan v1.2 4.2.6.2.5 (the cease ends when the link state toggles, portEnabled toggles, pttPortEnabled toggles, or after 5 minutes).

Findings fixed in this lane:
1. Tests: the companion's three checks all drive `i_link_up`, so a datapath wiring `port_enabled_i` to `i_link_up` alone (dropping `LINK_CTRL[0]` and the guard) passed every check. Added `#94 asCapable falls when LINK_CTRL[0] withdraws the link` and `#94 asCapable falls when the guard loses the receive clock` (`sim_gptp.cpp`), each with a precondition.
2. Tests: `#94 asCapable falls at link loss` passed vacuously if asCapable was never earned; added `#94 asCapable is TRUE before the link loss` (and the same precondition before the two new losses).
3. Docs: the companion's `docs/design/GPTP_PLANE.md` port-enable section failed `scripts/check_doc_style.py` with 7 findings (sentences of 11 to 15 words); rewritten to the limit, meaning unchanged.
5. Tests, found by this lane's own campaign at `67d8d192`: the donor control "the falling edge raises no event" (D2) escaped `#94 asCapable falls when LINK_CTRL[0] withdraws the link`. Its precondition polled right after the previous phase's `i_link_up = 1`, read the stale TRUE the defect left, and the rise's NOT_ENABLED commit then cleared asCapable inside the 2 ms window. Each link return's edge is now taken (2 ms) before the phase ends (commit `cf3ef596`), so the next precondition needs a TRUE earned after the return. The campaign re-ran at `cf3ef596`.
4. Docs: `docs/design/GM_LOSS_RECOVERY.md`'s detection table lacked the link loss; `docs/design/TIME_SYNC.md` said "Nothing else re-arms link-up", which the FPGA-gPTP #68 ruling words as "Only an asCapable fall and rise (or reset) re-arms", and a link loss is now such a fall.

## Changes, file:line at the head, and the clause each answers

RTL (the companion, reviewed as milan-fpga code; this lane changes no RTL statement):

| File:line | Change | Clause |
|---|---|---|
| `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:192-199` | input `port_enabled_i` with its `//!` contract | IEEE 802.1AS-2011 10.2.4.11 (portEnabled); Milan v1.2 4.2.6.2.5 |
| `KL_gptp_shadow.sv:711` | passes it to the engine's `port_enabled_i` | the same |
| `hdl/milan/milan_datapath.sv:8899-8903` | drives it from `eff_link_w`, defined at `:3194-3195` (PHY link AND `LINK_CTRL[0]` AND (guard disabled OR the guard's estimate)) | 10.2.4.11 a) MAC_Operational and b) the administrative port state |
| `tb/verilator/gptp_plane/gptp_plane_wrap.sv:150-152`, `tb/verilator/gptp_shadow/gptp_shadow_wrap.sv:322-324`, `tb/verilator/gptp_txts/gptp_txts_wrap.sv:259-261` | tie it 1: those suites' links stay up | none (test wrappers) |

Tests (`tb/verilator/milan_dp/sim_gptp.cpp`; companion lines, then this lane's):

| File:line | Change | Clause |
|---|---|---|
| `:536-538`, `:601-607` | companion: `pd_second`, a second clock identity answers each request | Milan v1.2 4.2.6.2.5 (multiple responders) |
| `:1655-1710` | companion: the 2 MHz ms and interval, `is_pdreq`, `fabric_ascapable` (CSR 0x77C[16]), `await_ascapable`, `pdreq_cyc`, `await_pdreq`, `cease_on_two_responders` | - |
| `:1717-1724` | companion: re-earn the port after the per-descriptor limiter's `LINK_CTRL[0]` toggle (setup) | Milan v1.2 4.2.6.2.4 |
| `:1729-1738` | link loss: companion check `#94 asCapable falls at link loss`; this lane adds the precondition and the 2 ms that takes the return's edge | 10.2.4.11; Figure 11-8 NOT_ENABLED with Cor1/Cor2 |
| `:1744-1755` | this lane: `#94 asCapable falls when LINK_CTRL[0] withdraws the link`, its precondition, the return's 2 ms | 10.2.4.11 b) |
| `:1760-1773` | companion: `#94 a link loss inside the cease ends it: a Pdelay_Req within one interval of the return` | 4.2.6.2.5 ("the link state toggles") |
| `:1779-1788` | companion: `#94 the cease countdown exit is unchanged: 5 s from the last request` (the leg's 3 s image; 300 s ships) | 4.2.6.2.5 ("after 5 minutes") |
| `:1792-1807` | this lane: `#94 asCapable falls when the guard loses the receive clock` and its precondition; one `i_ethrx_tgl` transition arms the guard, `DEAD_CYC_C` (4,096) cycles without another declare the clock dead; runs last | 10.2.4.11 a) MAC_Operational |
| `:2089-2093` | the phases in order, after every earlier phase | - |
| `tb/verilator/milan_dp/README.md:91` | the `obj_gptp` row names the #94 checks | - |

Documents:

| File:line | Change | Clause / gate |
|---|---|---|
| `docs/design/GPTP_PLANE.md:62` | companion: the seam row | - |
| `docs/design/GPTP_PLANE.md:98-122` | companion's port-enable section, split to the concise-style limit; `:122` names the leg | `scripts/check_doc_style.py` |
| `docs/design/GM_LOSS_RECOVERY.md:40`, `:52` | detection row and sentence: a link loss clears asCapable at once | 10.2.4.11; FPGA-gPTP #94 |
| `docs/design/TIME_SYNC.md:90-91` | a link loss clears asCapable too; only an asCapable fall and rise re-arms link-up | the FPGA-gPTP #68 ruling |
| `docs/guides/gptp/SYSTEM_INTEGRATOR.md:46` | the port-enable seam: drive portEnabled | 10.2.4.11 |
| `docs/reference/SUBMODULES.md:383-431` | the #806 adoption section: the #94 result, the port change, the wiring, the leg, the route figures and the gate's refusal | `check_doc_style.py`, `check_submodule_docs.py` |
| `CHANGELOG.md:11`, `:52-78` | Contents line (description by hand) and the entry | `gen_toc.py --write CHANGELOG.md`, then `--check` |
| `docs/design/AREA_BUDGET.md:143-144` | the shipping route at `135afd04`: 15,823 slices, 27 free; its WNS refusal and the owner decision it needs. `:145` (no slice room, owner decision for growth) kept verbatim | `pp_resource_gate.py check-baseline` (the policy table is untouched) |

Pin-derived records (commit `f475329c`), each through its generator:

| File | Change | Generator / gate |
|---|---|---|
| `syn/yosys/rom_digests.tsv` | row `135afd04 gptp_ucode.hex 99266fa9...ed32`, equal to the donor's tracked `syn/ooc/work/gptp_ucode.hex` and `tb/verilator/ucpu/gptp_ucode.hex` at the pin | `bash syn/yosys/ooc.sh --record-rom-digests` |
| `docs/reference/SUBMODULES.md:24` | pin row | `scripts/check_submodule_docs.py` |
| `docs/diagrams/submodule_boundaries.{drawio,svg,png}`, `timesync_chain.{drawio,svg,png}`, `PNG_MANIFEST.json` | pin labels only (`135afd043309`) | `python3 docs/diagrams/submodule_boundaries.gen.py`, `python3 docs/diagrams/timesync_chain.gen.py` (each `--check` rc 0) |
| 8 gPTP pages, 19 donor links | `f97c1803` -> `135afd04`; every target exists at the pin | `scripts/check_gptp_docs.py --with-submodule` |
| `scripts/port_docs.budget` | header only: `hdl 2158 -> 2162, gptp-processor 125 -> 127, protocol-processor 1764 -> 1766` (gptp-processor: `port_enabled_i`, `cancel_i`; hdl: the shadow's input plus dev's drift since #803's census) | `python3 scripts/check_port_contracts.py --write-budget` |
| `scripts/naming.budget` | byte-identical | `python3 scripts/measure_naming.py --write-budget` |
| `hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md` | unchanged: the campaign at this tree differs only in its date stamp (675 pass, freshness PASS) | `make -C tb/verilator/tsn_fuzz ptp` |

## New checks, their planted mutants and failing words

Runner: `scripts/parent_mutants.py` (the #803 lane's runner, its rows replaced). One defect at a time in a clean clone, planted exactly once, the leg rebuilt from scratch (`rm -rf obj_gptp gptp_ucode.hex`, then `make -C tb/verilator/milan_dp gptp`), the file restored and the tree proven clean after. Each of three clones at `cf3ef596` first ran the clean pass C0, which must print no FAIL: 210 checks, 210 PASS in all three. Parent defects (P) break this adoption's wiring; engine defects (D) are the donor's own texts, taken by name from `gptp-processor/tb/verilator/engine/port_mutants.py` `PORT_MUTATIONS`. Full table with every printed line: `receipts/mutants/mutant-table.md`.

| Control | Plants | Verdict | Named checks, each printed `FAIL <name> got <g> exp <e>` |
|---|---|---|---|
| P1 | `KL_gptp_shadow.sv`: `.port_enabled_i (1'b1)` | KILLED 4/4 | `#94 asCapable falls at link loss` got 1 exp 0; `#94 asCapable falls when LINK_CTRL[0] withdraws the link` got 1 exp 0; `#94 a link loss inside the cease ends it: a Pdelay_Req within one interval of the return` got 0 exp 1; `#94 asCapable falls when the guard loses the receive clock` got 1 exp 0 |
| P2 | `KL_gptp_shadow.sv`: `.port_enabled_i (1'b0)` | KILLED 3/3 | `#94 asCapable is TRUE before the link loss`, `... before LINK_CTRL[0] withdraws the link`, `... before the guard loses the receive clock`, each got 0 exp 1 (99 other lines fail with it: the port never transmits) |
| P3 | `milan_datapath.sv`: `.port_enabled_i (i_link_up)` | KILLED 2/2 | `#94 asCapable falls when LINK_CTRL[0] withdraws the link` got 1 exp 0; `#94 asCapable falls when the guard loses the receive clock` got 1 exp 0 |
| P4 | `milan_datapath.sv`: `(i_link_up & (cfg_linkg_dis \| linkg_est_w))` | KILLED 1/1 | `#94 asCapable falls when LINK_CTRL[0] withdraws the link` got 1 exp 0 |
| P5 | `milan_datapath.sv`: `(i_link_up & cfg_sw_link)` | KILLED 1/1 | `#94 asCapable falls when the guard loses the receive clock` got 1 exp 0 |
| D1 | donor "a portEnabled edge keeps the cease" (generator) | KILLED 1/1 | `#94 a link loss inside the cease ends it: ...` got 0 exp 1 (the kept cease also fails the countdown check and the guard phase's precondition) |
| D2 | donor "the falling edge raises no event" (engine) | KILLED 3/3 | `#94 asCapable falls at link loss`, `... when LINK_CTRL[0] withdraws the link`, `... when the guard loses the receive clock`, each got 1 exp 0 |
| D3 | donor "slot 6 runs no NOT_ENABLED leg" (generator) | KILLED 4/4 | the four of P1, the same words |
| D4 | donor "the countdown loads one beat less" (generator) | KILLED 1/1 | `#94 the cease countdown exit is unchanged: 5 s from the last request` got 0 exp 1 |
| D5 | donor "the cease entry ends the cease at once" (generator) | KILLED 1/1 | the countdown check, got 0 exp 1 |

Every #94 check of the leg has a killer: the three preconditions (P2), the link loss (P1, D2, D3), `LINK_CTRL[0]` (P1, P3, P4, D2, D3), the guard (P1, P3, P5, D2, D3), the toggle exit (P1, D1, D3), the countdown (D4, D5).

The first campaign, at `67d8d192` (`receipts/mutants/round-67d8d192/`), had D2 ESCAPED on the `LINK_CTRL[0]` check (finding 5 above); the leg at `cf3ef596` kills it.

## Resources: route-1x1, ooc-1x1, ooc-8x8 against the current record

Dev's own route: dev `1e80128f`'s synthesis inputs equal the #803 merge `6fc0c214` (`git diff 6fc0c214 1e80128f -- hdl sw configs gptp-processor protocol-processor third_party syn` is empty), whose route the #803 lane measured: 51,801 LUT, 53,760 FF, 15,834 slices (16 of 15,850 free), WNS +0.303 ns, WHS +0.028 ns. Record: the twelfth (#799), 52,012 / 53,707 / 15,780 / +0.440.

Bank: `scripts/vivado_bank.sh` (the #803 lane's bank, paths only; recipe `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, single-worker synthesis, `general.maxThreads` 32, Vivado 2026.1 Build 6511674), one run at a time, each under `flock -x $VIVADO_LOCK`, each started above 20 GB MemAvailable, no sweep of this lane beside it, in a clean clone at `cf3ef596`. The later commits change no synthesis input (documents only). Each endpoint then `python3 syn/ooc/pp_resource_gate.py check <dir> --endpoint <e>` against the committed twelfth record (#799).

| Endpoint | Gate rc | LUT record -> head (delta, tol.) | FF (delta, tol.) | Other |
|---|---:|---|---|---|
| route-1x1 | **1 REFUSED** | 52,012 -> 51,837 (-175, 500) | 53,707 -> 53,788 (+81, 600) | slices 15,780 -> 15,823 (+43, tol. 80): **27 of 15,850 free**; RAMB36 74, RAMB18 27, DSP 13 unchanged; **WNS +0.440 -> +0.032 (-0.408, tol. 0.25): "REGRESSION: fell by more than 0.25"**; WHS +0.036 -> +0.034 |
| ooc-1x1 | **0 PASS** | 24,346 -> 24,346 (0, 250) | 20,404 -> 20,404 (0, 250) | RAMB 16/3, DSP 8 unchanged |
| ooc-8x8 | **0 PASS** | 34,156 -> 34,156 (0, 316) | 29,782 -> 29,782 (0, 339) | RAMB 21/5, DSP 8 unchanged |

The OOC top is `KL_pp_shadow`, which instantiates none of the files this lane changes, so both equal the record in every figure.

Bank timeline (`receipts/vivado/bank-timeline.txt`, UTC): route-1x1 00:42 -> 01:41 (58.3 min), ooc-1x1 01:41 -> 01:52 (11.7 min), rtl-8x8 01:52 -> 01:54, ooc-8x8 01:54 -> 02:19 (25.7 min); every Vivado rc 0; gates 1, 0, 0. Log digests: `receipts/vivado/logs.sha256`. Run note: another lane's four-shard sweep was running on the host during the route (MemAvailable stayed at or above 43 GB), and this lane's physical leg at `cf3ef596` ran beside it in this unit; no sweep of this lane ran beside any Vivado run.

STOP conditions for the area item, none met: placement and routing complete (102,983 nets, 0 errors), 27 slices free; every corner meets the build floor (worst WNS +0.032 ns, worst WHS +0.034 ns). Not met, published as an open decision: #806's acceptance "the area gate passes", because the gate refuses route-1x1 on its WNS tolerance (0.408 ns fall against 0.25 ns).

**This adoption's share against dev's own route** (the #803 merge route, identical synthesis inputs to dev `1e80128f`): **+36 LUT, +28 FF, -11 slices, WNS -0.271 ns** (+0.303 -> +0.032), WHS +0.006 ns (+0.028 -> +0.034). Placed hierarchy, head minus dev (`receipts/vivado/route-hierarchy-head-minus-dev.txt`): `KL_gptp_shadow` +110 LUT / +0 FF (its engine +37 / +0); blocks this lane does not touch move by placement and optimisation across boundaries, `pp_shadow` +118 / +26, `adp_tx_mux` +109 / +24 against `ctl_tx_mux` -88 / -22 (a renamed instance), `ptp_clock_validity` -39 / -64 against `milan_datapath/(self)` +18 / +82.

Timing: every corner meets the build floor (`docs/integration/BUILDING.md` section 5: WNS >= +0.03 ns, WHS >= 0): Slow 0C / 85C WNS +0.032, WHS +0.052; Fast 0C / 85C WNS +1.638, WHS +0.034. The worst setup path (`receipts/vivado/route-1x1-worst-setup-path.txt`) is the SoC path `docs/design/AREA_BUDGET.md` already names: `FSM_onehot_socbushandler0_axilite2wishbone_state_reg[3]` to `milansoc_spiflash_phy_cnt_reg[8]`, 18 logic levels, data delay 9.835 ns (6.251 ns routing), outside the wrapper and the datapath; this lane changes nothing on it.

Route detail: 102,983 routable nets, 0 routing errors; IOB packing 21 PASS, 0 FAIL, 1 INERT (`eth0_rx_er`, no net). Log: no CRITICAL WARNING or ERROR line (the one match is the IOB-pack check's echoed script text); the one `Synth 8-6901` is dev's `crft_emit_en_w` (`milan_datapath.sv:3407`).

## Gate table

Head `f99405af` unless noted; every command unpiped, its own log, rc and seconds; receipts `receipts/final-f99405af/` unless noted. Clean clones from the lane (`scripts/make_clone.sh`), whose `origin/dev` and `dev` are the live remote dev `1e80128f`.

| Gate | rc | Seconds | Result | Receipt |
|---|---:|---:|---|---|
| Full sweep, 4 shard units (`native-shards.py`, CPUs 16-19 / 20-23 / 24-27 / 28-31, MemoryMax 10G, -j4) | 0 x4 | 4,678 / 4,496 / 4,982 / 4,043 | shard 0 14/14 (1,575,341 checks), 1 17/17 (14,364), 2 17/17 (251,927), 3 16/16 (350,078); every shard clone at `f99405af` | `sweep/` |
| `python3 scripts/suite_tally.py <union> --quiet --expect-suite-root tb/verilator` | 0 | - | **64 / 64 suites, 2,191,710 checks, 0 in-suite failures, 0 timed out** (`tally-per-suite.txt`) | `sweep/tally-quiet.out`, `union.sha256` |
| milan_dp `gptp` and `gptp-lat` legs (inside `milan_dp`, shard 0) | 0 | - | `210 checks: 210 PASS, 0 FAIL` each; `milan_dp` 13,773 checks over 20 tallies, 0 failures | sweep |
| milan_dp_gm_steps (shard 1) | 0 | - | 202 checks, 0 failures | sweep |
| `make -C tb/verilator/tsn_fuzz ptp` | 0 | 43 | 675 pass, 0 fail, 0 known gaps; freshness 1/1 PASS; the artifact differs only in its date stamp, so it stays as committed | `fuzz/` |
| milan_dp_gptp at `cf3ef596` (inputs equal the head's: later commits change four documents), `scripts/run_all_suites.sh <logs> --wait --physical-gptp`, `SUITE_TIMEOUT` unset, then `suite_tally.py <logs> --quiet --expect-suite-root tb/verilator --physical-gptp` | 0, 0 | 5,653 | 205 checks, 0 failures: physical 151, setup abort 6, no-TX 20, no-Pdelay 14, recentre 14; 17.992742740 simulated s, 899,637,137 cycles (as at #803); suite 81.9 % of its 6,900 s deadline | `physical-cf3ef596/` |
| Parent mutant campaign at `cf3ef596` (`parent_mutants.py`, three clones; the leg's inputs equal the head's) | 0 x3 | 1,417-2,173 | 3 clean passes (210/210 each); 10 of 10 defects KILLED on every named check | `receipts/mutants/` |
| rtl-fast replica (`rtl_fast_steps.py`, every job of the aggregate's `needs:`) | 0 | 5,913 | `rtl-fast: success; failed jobs: none`: all 12 jobs success (changes, verilator-lint, bdd-conformance, yosys-tool, yosys-elaboration, publication-census, firmware-unit, the three firmware mutation jobs, firmware-boundary, firmware-verilator); behave 14 features, 495 scenarios, 2,288 steps passed; base the live dev `1e80128f` | `rtl-fast/` |
| `syn/yosys/run.sh` (full serial; Yosys 0.66, sv2v v0.0.12) | 0 | 1,387 | tops 60, pass 60, fail 0; tied inputs 29, justified 2, unjustified 0; TAP-PURITY PASS | `yosys/` |
| Static and pin-record bank (`static_bank.sh`, 33 commands) | 0 x33 | - | pin records: `pp_resource_gate.py check-baseline` PASS 3 endpoints; `ooc.sh --record-rom-digests` then `git diff --exit-code syn/yosys/rom_digests.tsv` rc 0; both diagram `--check`; `check_submodule_docs.py` 6 exact gitlinks; `check_gptp_docs.py` with and without `--with-submodule` (8 current pages, donor checkout verified). `check_port_contracts.py` OK (4,055 ports); `lint_rtl.py --check` PASS 89 <= 89 (and `--self-test`); `xvlog_gate.py --check` under the lock, 0 findings; SV, shell, C++ (75/75 self-test) and Python (54/54) idiom gates within every ratchet (C++ long function 0 <= 0, multi-declarator 0 <= 0; Python long function 9 <= 9, long module 10 <= 10); `measure_naming.py`, `measure_test_evidence.py`, `check-integrator-params.py`, source lists, `pp_srcs.py`, hygiene, fail-fast, TODO ownership, module matrix, SoC sources, NVM capture, feature status, `docs_check.py` all rc 0; `sw/builder/test_builder.py` ALL GATES PASS EXCEPT 2 NOT RUN (gate 1b inert under Make 4.3; gate 11 needs the absent mf48 calibration build), the two arms #771 and #803 recorded | `static/` |
| Docs workflow replica (`docs_steps.py`, GNU Make 4.3, CPython 3.12.3), the LiteX builder leg, the CPython 3.12.3 Markdown gates, the no-git gates | 0, 0, 0, 0 | 2,854 | 44 steps, 0 failed, 2 skipped by rule (gate_42 runs the candidate act runner on the host; the no-git step deletes `.git`); builder leg 1 with the LiteX interpreter 1/1; the five Markdown gates on CPython 3.12.3 5/5; `docs_check.py` and `check_feature_status.py` on a `git archive` export rc 0 | `docs/` |
| Vivado bank at `cf3ef596` (synthesis inputs equal the head's): route-1x1, ooc-1x1, rtl-8x8, ooc-8x8, each `pp_resource_gate.py check` | 0 x4; gates **1**, 0, 0 | 3,500, 699, 71, 1,543 | route-1x1 REFUSED on WNS only (section Resources); ooc-1x1 and ooc-8x8 PASS | `receipts/vivado/` |

### Early signal at `67d8d192` (before the settle fix `cf3ef596`; receipts `receipts/early-67d8d192/`)

Run to find failures early; superseded by the final-head runs below. Every one rc 0:

| Gate | rc | Result |
|---|---:|---|
| Full sweep, 4 shard units (CPUs 16-19, 20-23, 24-27, 28-31; MemoryMax 10G; -j4) | 0 x4 | 64 / 64 suites; `suite_tally.py <union> --quiet --expect-suite-root tb/verilator`: 2,191,710 checks, 0 in-suite failures (shard 0 14/14 1,575,341; 1 17/17 14,364; 2 17/17 251,927; 3 16/16 350,078) |
| milan_dp_gptp (`run_all_suites.sh <logs> --wait --physical-gptp`, `SUITE_TIMEOUT` unset), then `suite_tally.py ... --physical-gptp` | 0, 0 | 205 checks, 0 failures; physical 151 over 17.992742740 simulated s, 899,637,137 cycles; suite 6,402 s of its 6,900 s deadline on a host running two sweeps |
| `make -C tb/verilator/tsn_fuzz ptp` | 0 | 675 pass, 0 fail, freshness PASS; the artifact differs only in its date stamp |
| Yosys (`syn/yosys/run.sh`) | 0 | 60 / 60 tops; tied inputs 29, justified 2, unjustified 0; TAP-PURITY PASS |
| Static and pin-record bank (33 commands) | 0 x33 | builder: ALL GATES PASS EXCEPT 2 NOT RUN (gate 1b, gate 11, as #803 recorded) |
| Docs workflow replica | 0 | 44 steps, 0 failed, 2 skipped by rule; LiteX builder leg, CPython 3.12.3 Markdown gates and no-git gates rc 0 |

## STOP conditions

- The route does not fit: not met. Placement and routing complete, 102,983 nets routed, 0 errors, 15,823 of 15,850 slices (27 free).
- Timing misses the build floor: not met. Every corner meets WNS >= +0.03 ns and WHS >= 0 (worst WNS +0.032 ns at the slow corners, worst WHS +0.034 ns at the fast corners).
- Not a STOP but not met: the resource gate refuses route-1x1 on its WNS tolerance (0.408 ns fall, tolerance 0.25), so #806's acceptance "the area gate passes" is not met. Published as an owner decision; nothing re-recorded.

## Open risks and questions

1. **The `milan_dp` gptp case's hosted window.** Each of the `gptp` and `gptp-lat` cases runs `sim_gptp.cpp`. On this host (three binaries run together, user CPU seconds, `receipts/leg-timing/`): dev 163.8 s, the companion 335.4 s, this head 351.1 s. So the companion's three phases roughly double the case, and this lane's two added losses add 15.7 s (4.7 %). Round-robin dealing puts `gptp` in `milan_dp` leg 0 (`PIECE_SECONDS` 1,429 s) and `gptp-lat` in leg 1 (508 s). The worker carrying leg 0 projects 1,551 s against the 1,620 s rule (`docs/testing/CI_WORKFLOWS.md`), 69 s of margin, so the hosted window is likely to exceed the projection. The 45-minute timeout is not at risk. The figures are hosted measurements that CI_WORKFLOWS.md says to refresh from the next complete hosted run, so this lane does not invent them.
2. **The bench scenario.** #806's acceptance includes the in-house qualification's link-toggle gPTP scenario on the built image; no image or bench access here. PR-BODY uses "Relates to #806".
3. **pttPortEnabled.** Milan v1.2 4.2.6.2.5 also ends the cease when pttPortEnabled toggles. The parent has no control for pttPortEnabled (always enabled), so nothing drives that exit; recorded, not changed.
4. **The guard term is graded at the end of the leg.** Arming the link guard starts its MAC recovery when the receive clock dies, which this leg does not model, so that check runs last.
