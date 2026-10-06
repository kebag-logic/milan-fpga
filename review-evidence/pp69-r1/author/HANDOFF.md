# [A550] HANDOFF - processor #69, the redundancy seam in the fabric build

Status: DONE at head `d723574a2b760f9dd2b866081135d5e0bd9c68cd`, not pushed. Every item of the
assignment and every acceptance item of #69 met; OOC 1x1 delta 0 LUT, 0 FF; every processor
gate, every campaign and the parent consumer set of 17 rc 0 at base and head. One deviation,
inherent to items 1 and 2 (two new ports in the Yosys statistics, no cell change), is stated
under the count-1 proof.

- Repository: the processor repository (origin verified), branch `pp69-if-seam`.
- Base: `main` `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8`. Head: `d723574a2b760f9dd2b866081135d5e0bd9c68cd`.
- TAKEN posted on #69 (comment 6010222994); REVIEW READY with the head posted on #69
  (comment 6015728233). No push, no PR.
- Pinned Verilator 5.050 first on PATH through a scratch wrapper that admits at most four
  (three for the first base runs) simultaneous builds and runs each C++ build at `-j 4`
  (12 GB memory cap); the host default 5.052 is not used.

## Commits (base..head)

| Commit | What |
|---|---|
| `1673e56` | RTL (`protocol_processor_top.sv`, `KL_aecp_notify.sv`), the two ADP patches' context refresh, and the docs that describe the RTL (F01.5, REQ-SCP-003, 02, 06, the integrator guide, diagram 21) |
| `3b6a25b` | the checks: `tb/adp_engine` second build (section IF), `tb/aecp_notify` third build (PT, CK), `tb/pp_top` seventh build (IF) and `if-guards`, 09 section 8.9 |
| `a8f7983` | the controls: nine `if-` arms in the ADP campaign, seven arms in `notify_mutants.py` |
| `c3cac3a` | the suite READMEs: adp_engine section IF, aecp_notify sections PT and CK, pp_top section IF, the new controls |
| `d723574` | a failing control for every new check: seven more `if-` arms, two AVB_INTERFACE counter arms, PT1 folded into PT2 (it was PT2's first half), the READMEs' records |

## Changes, file:line at the head

RTL (`1673e56`; unchanged since):
- `hdl/top/protocol_processor_top.sv`
  - :77-93 banner: the seam, what is keyed at 2 and what is not.
  - :102 `parameter int unsigned N_AVB_IF_P = 1` (F01.5 P-N-AVB-INTERFACES).
  - :235 the F08.4 timer map takes `N_AVB_IF_P`.
  - :313 `input wire [1:0] rx_if_index_i = 2'd0`.
  - :871-877 `gen_g_avb_if`: 1 or 2, else `$error` naming `N_AVB_IF_P`; :886 the timer-map fit
    guard counts `N_AVB_IF_P` advertise slots.
  - :1546-1564 `hdr_if_latch`: `rx_if_index_i` read with the frame's last byte, carried to its
    header beat (only above 1).
  - :1720 normalizer `.rx_if_index_i ((N_AVB_IF_P > 1) ? hdr_if_r : 2'd0)`, replacing the hardwired
    `2'd0` (ticket's :1329).
  - :1973 `KL_adp_engine` `.N_IF_P (N_AVB_IF_P)`, replacing the literal 1 (ticket's :1569); :1989-1994
    the class-D levels replicated per interface; :1952 and :1048 the debug buses widened, interface 0
    shown.
  - :4005-4017 `aecp_cmd_if_latch`: the command's `interface_index` on the engine's `cmd_r`
    handshake.
  - :4029 `KL_aecp_notify` `.N_IF_P (N_AVB_IF_P)`; :4052 `.rgy_port_i ((N_AVB_IF_P > 1) ?
    aecp_cmd_if_r : 2'd0)`.
- `hdl/aecp/KL_aecp_notify.sv`
  - :16-30 banner (the ticket's :17-20): the port, when it is stored, what is not keyed by port.
  - :148-150 the served counter set.
  - :219 `parameter int unsigned N_IF_P = 1`; :252 `input wire [1:0] rgy_port_i`.
  - :415 `N_CTR_DESC_C` gains one slot per interface above 0.
  - :521-539 `g_port` / `g_no_port`: `port_r` per row, the REGISTER/DEREGISTER port latched in
    N_IDLE, written in N_APPLY, compared in the walk; nothing at 1.
  - :738 the pick fix-up naming AVB_INTERFACE i's slot; :1153 the intake setting it.

Docs (`1673e56`, `3b6a25b`):
- `docs/00_MILAN_COMPLIANCE_REVIEW.md:523`, REQ-SCP-003's Arch cell: keyed and not keyed, each named.
- `docs/architecture/01_overview.md:159`, section 7, P-N-AVB-INTERFACES: range, keyed, not keyed.
- `docs/architecture/02_interfaces.md:57`, `:148`, `:364`: the RX face, the `rx_if_index_i` row, the
  catalog.
- `docs/architecture/06_aecp_engine.md:638-647`, `:905-919`, `:970-971`: section 6.6's counter push
  per interface, section 7's registry tuple, the storage table's `port_r`.
- `docs/architecture/09_verification.md:418-435`, section 8.9: the three builds and `if-guards`.
- `docs/guides/integrator.md:78`, `:133`: the parameter and the RX face.
- `docs/diagrams/21-integration-faces.svg:33`, `:61-63`: inventory and RX box.

Checks (`3b6a25b`, item 5):
- `tb/adp_engine/sim_if2.cpp` (new, IF0 to IF9), `sim_main.cpp` (`[build default]` tally line),
  `Makefile` (second build `interfaces`).
- `tb/aecp_notify/port_tuple.hpp` (new, PT2 to PT7, CK1 to CK5), `sim_main.cpp`, `Makefile` (third
  build `interfaces`).
- `tb/pp_top/interface_phases.hpp` (new, IF1, IF2, IF3, IF3b), `pp_top_wrap.sv` (`PP_TOP_IF2`:
  `N_AVB_IF_P` 2, `rx_if_index_i`, an advertise-state tap), `sim_main.cpp`, `if_guards.py` (new),
  `Makefile` (seventh build, `if-guards` before `run`).

Controls (`a8f7983`, `d723574`): `tb/adp_engine/mutants.py` and 15 `mutations/if-*.patch` (16 arms;
`if-top-count-collapsed-lint` reuses the count patch), `tb/pp_top/notify_mutants.py` (9 arms).
The two refreshed context lines (item 7): `tb/adp_engine/mutations/cfg-nonzero-for-valid.patch`,
`cfg-overlay-only.patch`.

## Decisions

- Legal range of `N_AVB_IF_P`: 1 or 2 (one interface, or Milan's redundant pair). The top
  refuses any other value at elaboration, naming the parameter. The 2-bit transaction field
  could carry 4, but nothing grades 3 or 4, and 4 does not elaborate at the 8x8 shape (the
  F08.4 timer address passes the 8-bit owner tag ADP publishes).
- Count-1 identity technique: every new register sits in an `always_ff` whose body is
  wrapped in `if (N_AVB_IF_P > 1)` (or `N_IF_P > 1`), every new loop runs over interfaces
  1 to N - 1, and every consumer reads through `(N > 1) ? new : old`. At 1, Yosys folds all
  of it away: every cell count of every one of the 42 tops is identical to base.
- C7's counter patches (`tb/pp_top/ctr_mutations/ctr-notify-*.patch`) hold every line of
  `KL_aecp_notify`'s `counter_event_map`, so that block is untouched: AVB_INTERFACE 1 gets
  the slot after CLOCK_DOMAIN 0, set by a count-guarded intake and named by a count-guarded
  fix-up after the counter pick loop. Index 0's and CLOCK_DOMAIN's slots do not move.
- Registry port source: the top latches the AECP command's `interface_index` on the same
  handshake that loads the engine's `cmd_r` and drives `KL_aecp_notify.rgy_port_i`. The
  engine is untouched (its statistics stay byte-identical).
- Ports and parameters added, each the assignment's interface count or index threaded
  through, and nothing else: top `N_AVB_IF_P` and `rx_if_index_i[1:0]` (default `2'd0`);
  `KL_aecp_notify` `N_IF_P` and `rgy_port_i[1:0]`. No register-map change: side-port word 31
  shows interface 0's advertise state, `adp_next_avail_index_o` interface 0's index.

## Item 7: pre-edit grep and planting (done before the RTL edit)

- Drafts were made in scratch copies. Every base line they remove or modify (21 lines) was
  searched with `git grep -n -F` across `tb/**/*.patch` and `tb/**/*.py`, in the lane at
  `e6a759de`, as the full line and stripped: 42 searches, 2 with a match. The one match is
  `.N_IF_P                (1),`, the trailing context line of
  `tb/adp_engine/mutations/cfg-nonzero-for-valid.patch` and `cfg-overlay-only.patch`. Item 1
  replaces that literal, so those two patches had that context line refreshed (their `-`/`+`
  lines and leading context are byte-identical).
- Planting (patches through `git apply --check`; exact-text arms through each driver's own
  `plant()` or count rule):
  - base: 476 of 476 and 96 of 96;
  - drafts before the refresh: 474 of 476 (the two above), 96 of 96;
  - RTL with the refresh: 476 of 476 and 96 of 96;
  - head `a8f7983` with the new arms: 491 of 491 (476 + 8 patches + 7 notify arms), 96 of 96;
  - head `d723574`: 500 of 500 (476 + 15 `if-` patches + 9 notify arms), 96 of 96.
- Planted identity: every one of the 123 base arms that plants into a file the lane changed
  (the top, `KL_aecp_notify.sv`) plants the same design at base and at `d723574`: the planted
  base, with the lane's diff of that file applied, equals the planted head byte for byte.

## Count-1 identity proof (item 4)

Yosys `stat -json` after `hierarchy -check; proc; opt_clean` for every top of
`syn/yosys/run.sh`'s array (42), base vs head; re-run at `d723574`, every JSON byte-identical to
the RTL commit's:

- 40 of 42 JSON files byte-identical.
- `KL_aecp_notify`: every cell count identical; +1 port (`rgy_port_i`, 2 bits): ports
  84 -> 85, port bits 1227 -> 1229, wires 6029 -> 6030, wire bits, public wires and public
  wire bits +2/+1/+2.
- `protocol_processor_top`: every cell count of every module identical; the top's own
  module +1 port (`rx_if_index_i`, 2 bits) and its wire; the notify child as above; two
  derived module names change (`KL_adp_engine`, `KL_aecp_notify`): Yosys names a
  parameterised child by a hash of the parameters its instance passes, and both instances
  now pass the count (ADP the same value 1, now an unsigned parameter instead of a literal).
- With the derived names masked: 18 differences in the top and 12 in `KL_aecp_notify`, all in
  the six port and wire counters (ports, port bits, wires, wire bits, public wires, public wire
  bits), none in any cell count.

Deviation, stated plainly: item 4 asks for byte-identical statistics of the top and every
touched module, but item 1 requires a new top input, so the top's port counters must move,
and item 2 requires the port to reach `KL_aecp_notify`. The new ports and the two derived
names are the whole difference; no cell changes, and the OOC census below is byte-identical.
#69's own acceptance list (1 to 7) is fully met, so the PR says "Closes #69".

## Two interfaces (item 5)

- `tb/adp_engine` `interfaces`: `KL_adp_engine` at `N_IF_P = 2`, 11 checks (IF5 once per
  interface), grading per-interface advertising: reset, link up and down per interface,
  byte-exact ENTITY_AVAILABLE and ENTITY_DEPARTING with each interface's index, grandmaster
  and available_index, ENTITY_DISCOVER and GM_CHANGE restarting only their interface, and
  ingress keyed by interface.
- `tb/aecp_notify` `interfaces`: `KL_aecp_notify` at `N_IF_P = 2`, 11 checks: the registry
  tuple (PT2 to PT7) and the AVB_INTERFACE counter slots (CK1 to CK5).
- `tb/pp_top` `interfaces`: the real `protocol_processor_top` at `N_AVB_IF_P = 2`, 6 checks
  (IF1, IF2 per interface, IF3, IF3b, the bench's boot check).
- `tb/pp_top` `if-guards`: lint-only elaborations of the real top at 1 and 2 (clean) and 0 and
  3 (refused with the top's message naming `N_AVB_IF_P`); runs before every `make` of pp_top.
- The item 5 mutant: `if-ingress-collapsed` (ADP's ingress interface tied to 0) fails IF5, IF6,
  IF8; `if-top-ingress-collapsed` (the top's index tied to 0) fails pp_top IF2, IF3, IF3b;
  `rgy_port_tied_zero` fails IF3, IF3b. The full table is under Controls.

## OOC 1x1 (#638's recipe) - 0 LUT, 0 FF

Recipe: `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` in the scratch parent (dev `28f9666f` +
the 148 patch), shape ax7101 (1x1): the launcher's preview with `--build` dropped (builder
output and ROMs redirected outside the checkout), RTL elaboration (`synth_design -rtl
-rtl_skip_mlo`, `Synth 8-4445` promoted to error) as the integrated log, then
`syn/ooc/pp_baseline.py ... --integrated-log ... --integrated-clock` (20 ns from `CLK_HZ_P`)
and `baseline_ooc.tcl`. Vivado 2026.1, `xc7a100t-fgg484-2`, every run under
`flock $VIVADO_LOCK` with nothing else of this lane running beside it.

| `KL_pp_shadow` standalone 1x1 | LUT | FF | RAMB tiles | DSP | run |
|---|---:|---:|---:|---:|---|
| base `e6a759de` | 23,211 | 19,777 | 17.5 | 8 | rc 0, 1,286 s |
| head `a8f7983` (RTL as at `d723574`: later commits touch only `tb/` READMEs, drivers and benches) | 23,211 | 19,777 | 17.5 | 8 | rc 0, 1,292 s |
| delta | **0** | **0** | 0 | 0 | |

- `baseline_cells.tsv` (the cell census) byte-identical: sha256 `87278975...f5da71` at both.
- `baseline_hierarchy.rpt` identical past its dated header; `baseline_parameters.json` and
  `baseline_chparam.txt` identical; the six image hashes of `baseline_images.json` identical.
- #638's gate (`syn/ooc/pp_resource_gate.py check <dir> --endpoint ooc-1x1`): rc 0, PASS at
  both, with the same per-row deltas against its recorded baseline.

## Controls: every new check and the arm that fails it

Spot runs on the working tree that became `d723574` (the full campaigns are below). Every arm
was KILLED by the checks named; each driver's controls/goldens PASS.

| Arm | Driver (build) | Failing checks |
|---|---|---|
| `if-ingress-collapsed` | adp (`interfaces`) | IF5, IF6, IF8 |
| `if-egress-collapsed` | adp (`interfaces`) | IF3, IF4, IF5, IF6, IF9 |
| `if-pdu-index-collapsed` | adp (`interfaces`) | IF3, IF9 |
| `if-gm-sample-collapsed` | adp (`interfaces`) | IF3, IF9 |
| `if-link-collapsed` | adp (`interfaces`) | IF1, IF6 |
| `if-gm-slice-reversed` | adp (`interfaces`) | IF2, IF3, IF6, IF8, IF9 |
| `if-link-fall-collapsed` | adp (`interfaces`) | IF7 |
| `if-aidx-reset-by-index` | adp (`interfaces`) | IF0, IF3, IF4 |
| `if-ingress-forced-one` | adp (`interfaces`) | IF5 (interface 0), IF8 |
| `if-top-count-collapsed` | adp (pp_top `interfaces`) | IF1, IF2 x2 |
| `if-top-ingress-collapsed` | adp (pp_top `interfaces`) | IF2, IF3, IF3b |
| `if-top-ingress-live` | adp (pp_top `interfaces`) | IF2 x2 |
| `if-top-count-collapsed-lint` | adp (pp_top `if-guards`) | if guard 2 |
| `if-top-range-unguarded` | adp (pp_top `if-guards`) | if guard 3 |
| `if-top-range-floor-off-by-one` | adp (pp_top `if-guards`) | if guard 1 |
| `if-top-range-floor-dropped` | adp (pp_top `if-guards`) | if guard 0 |
| `port_not_compared` | notify (aecp_notify `interfaces`) | PT2, PT3, PT4, PT6, PT7 |
| `port_not_latched` | notify (aecp_notify `interfaces`) | PT2, PT3, PT4, PT6, PT7 |
| `port_not_stored` | notify (aecp_notify `interfaces`) | PT3, PT5, PT6, PT7 |
| `avb_counter_row_dropped` | notify (aecp_notify `interfaces`) | CK1, CK3 |
| `avb_counter_row_collapsed` | notify (aecp_notify `interfaces`) | CK1, CK2, CK3 |
| `avb_counter_named_clock` | notify (aecp_notify `interfaces`) | CK1, CK3 |
| `avb_counter_any_index` | notify (aecp_notify `interfaces`) | CK1, CK2, CK3, CK4, CK5 |
| `avb_counter_name_overlaps_clock` | notify (aecp_notify `interfaces`) | CK5 |
| `rgy_port_tied_zero` | notify (pp_top `interfaces`) | IF3, IF3b |

By check: adp_engine IF0 to IF9, aecp_notify PT2 to PT7 and CK1 to CK5, pp_top IF1, IF2,
IF3, IF3b and `if guard` 0 to 3 each fail under at least one arm above.

## Processor gates, base `e6a759de` and head `d723574`

Every gate rc 0 at both, run on clean extractions (`git archive`), never piped.

| Gate | base | head `d723574` |
|---|---|---|
| `scripts/run_suites.sh` | rc 0, 1,021,651 checks, 0 failing | rc 0, 1,021,679 checks, 0 failing |
| `scripts/lint_hdl.sh` | rc 0 | rc 0, log identical to base's |
| `syn/yosys/run.sh` | rc 0 | rc 0 |
| `make check` | rc 0 | rc 0 |
| `scripts/gen_matrix.py --check` | rc 0 | rc 0 (94 rows, 0 untested) |

Suite records: 30 of 33 lines identical; the three that move are the three suites this lane
adds a build to (item 5's ADP and top builds, and the registry's), each by that build alone:

| Suite | base | head | new checks |
|---|---:|---:|---|
| `adp_engine` | 1,348 | 1,359 | +11: `[build interfaces]` IF0 to IF9, IF5 once per interface; `[build default]` still 1,348 |
| `aecp_notify` | 45 | 56 | +11: the third build, PT2 to PT7 and CK1 to CK5 |
| `pp_top` | 10,444 | 10,450 | +6: the seventh build, IF1, IF2 once per interface, IF3, IF3b, and the notify bench's boot check at two interfaces; `if-guards` (4 cases) prints its own line |

## Campaigns, base vs head

Every driver whose campaign builds a changed file, `--jobs 2`, each run rc 0. Records
compared per arm file (graded lines, temporary paths masked) and per `results.json` row.

| Campaign | base | head | arm records |
|---|---|---|---|
| `tb/adp_engine/mutants.py` | 43 of 43 (2 controls, 41 arms) | 62 of 62 (5 controls, 57 arms) | 42 identical; the run control gains the IF build's tally; 19 head-only (3 controls, 16 `if-` arms) |
| `tb/pp_top/notify_mutants.py` | 56 of 56 KILLED, goldens PASS | 65 of 65 KILLED, goldens PASS | 62 identical, `results.json` 63 rows identical; `golden-aecp_notify-run` gains the third build (45 -> 56); 11 head-only (9 arms, 2 goldens) |
| `tb/maap/mutants.py` | 32 of 32 | 32 of 32 | 32 identical |
| `tb/pp_top/ctr_mutants.py` | 18 of 18 | 18 of 18 | 18 identical |
| `tb/pp_top/aecp_mutants.py` | 67 of 67 | 67 of 67 | 67 identical |
| `tb/pp_top/aecp_dispatch_mutants.py` | 44 of 44 | 44 of 44 | 44 identical, `results.json` 44 rows identical |
| `tb/pp_top/d3_mutants.py` | 110 of 110 KILLED, goldens PASS | 110 of 110 KILLED, goldens PASS | 116 identical (110 arms, 6 goldens), every verdict row identical; run in two parts at each side (below) |
| `tb/pp_top/acmp_mutants.py` | 33 of 33 KILLED, goldens PASS | 33 of 33 KILLED, goldens PASS | 37 identical, `results.json` 37 rows identical |
| `tb/pp_top/gsi_mutants.py` | 20 detected, golden and restored PASS | 20 detected, golden and restored PASS | 44 identical, `results.json` identical |
| `tb/pp_top/name_wr_mutant.py` | decode killed, golden and restored PASS | decode killed, golden and restored PASS | 6 identical, `results.json` identical |

The ADP and notify campaigns ran at `d723574`, the others at `a8f7983`: `a8f7983..d723574`
touches only `tb/adp_engine` (README, `mutants.py`, `if-` patches), `tb/aecp_notify` (README,
`port_tuple.hpp`) and `tb/pp_top` (README, `notify_mutants.py`), none of which the other
drivers build or read.

d3 in two parts: the first run of each side was ended by the session's two-hour limit on a
background command (base after 83 arms, head after 76), each with its goldens PASS and every
finished arm KILLED. The driver's `--only` then ran the arms with no verdict line (27 and 34),
goldens included, rc 0 at both. The merged record of each side is the first part's finished
arms plus the resumed part; an arm cut off mid-run is graded only by the resumed part.

## Parent consumer set of 17

Scratch parent: dev `28f9666f` with the 148 patch applied by `git apply` (no other parent
patch: the wiring needs none, since `N_AVB_IF_P` defaults to 1 and `rx_if_index_i` to `2'd0`).
The processor worktree and the staged gitlink were moved by a script that checks
`git rev-parse --show-toplevel` of both first; nothing committed, the push URL disabled.
Base: processor `e6a759de`; head: `d723574` (`a8f7983` earlier, every record the same except
the py idiom's line count). Every gate rc 0 at both. The scratch parent is left at the head:
the processor gitlink staged, the 148 patch in the worktree, nothing committed or pushed.

| # | Gate | Record, base vs head |
|---|---|---|
| 01 | `check_cpp_idiom.py` | 174 -> 177 translation units: the three new C++ files |
| 02 | `check_py_idiom.py` | 316 -> 317 modules (`if_guards.py`), 199,989 -> 200,132 lines |
| 03 | `check_rtl_source_lists.py` | identical |
| 04 | `pp_srcs.py --check --selftest` | identical |
| 05 | `check_port_contracts.py` | 3,824 -> 3,826 ports (`rx_if_index_i`, `rgy_port_i`), undocumented 111 <= 111 unchanged; literal-bound connections 49 -> 48 (ADP's `.N_IF_P (1)` now names the parameter), so the gate notes its budget can be lowered (not lowered: a parent change); 317 -> 318 test-only observations (`pp_top_wrap.sv`'s advertise-state tap) |
| 06 | `measure_naming.py --check` | +2 ports and +2 parameters (`N_AVB_IF_P`, `N_IF_P`) scanned, +1 excluded match; 95 candidates unchanged |
| 07 | `measure_test_evidence.py --check` | identical |
| 08 | `docs_check.py` | identical (0 findings) |
| 09 | `xvlog_gate.py --check` | PASS at both, run under `flock` on the Vivado lock with nothing else of this lane running: 2 findings == ratchet, the same two (`KL_pp_originator.sv:194`, `KL_pp_rx_validator.sv:383`, untouched here); logs identical except the pinned commit |
| 10 | `sw/builder/test_builder.py` | identical, masked: ALL GATES PASS EXCEPT 1 NOT RUN at both (gate 11 needs an external build tree) |
| 11 | `lint_rtl.py --check` | identical (90 <= 90) |
| 12 | `tb/verilator/pp_shadow` | tallies identical (311, 606 x2, 646 checks, 0 failures; RESULT PASS x4), 2,169 PASS lines |
| 13 | `tb/verilator/nvm_cosim` lint | identical |
| 14 | `tb/verilator/nvm_cosim` quick | identical, 315 checks |
| 15 | `tb/verilator/milan_dp` | tallies identical (RESULT PASS x9), 1,133 PASS lines |
| 16 | `tb/verilator/milan_dp_render` | identical, 5 checks |
| 17 | `check_sh_idiom.py` | identical |

The make-driven gates run at `-j16`, so their logs interleave lines. They are compared by
their tally lines and PASS/FAIL tokens; the others line by line, with temporary names and
timings masked.

## Evidence kept outside this directory (sha256, bytes)

The scratch area holds the extractions, logs and OOC runs; none is copied here.

| Artifact | sha256 | bytes |
|---|---|---:|
| OOC `baseline_cells.tsv`, base | `87278975d62fe2b7082322a20e5d085a7bf427f5b48388f52d8319e7f5f5da71` | 2,197,888 |
| OOC `baseline_cells.tsv`, head | `87278975d62fe2b7082322a20e5d085a7bf427f5b48388f52d8319e7f5f5da71` | 2,197,888 |
| OOC `baseline_utilization.rpt`, base | `96d389f98a0e4ec27637449544489de3d77998fc54c5e4e6dbac0ccae97f84b2` | 9,297 |
| OOC `baseline_utilization.rpt`, head | `142adc5b81360422187460735a989ba095e5c8d31e8d4237bd7d87bab70f692c` | 9,297 |
| Yosys `stat-*.json`, base (42; hash of the sorted `sha256sum` list) | `afdc0b5e5b5698b8eccb24d95d4c889cfc30e6b6d056d1ef6e05f292b8f382b8` | |
| Yosys `stat-*.json`, head `d723574` (42; same) | `9c9a29bfc0bf1881a209c9514b6bdb268b2da5e3cd16c3f52a28f39ba922d43a` | |
| `run_suites.sh` log, base | `299897e701fa15cbc20b6007e1566749c48499ace9118db456ef35d48f409f69` | 1,750 |
| `run_suites.sh` log, head | `4a7decfc01503cd6cd949d704c7d9862a4d01c8b9ae2f609e8d941dc4a5df250` | 1,750 |
| ADP campaign log, head | `d36021e5adee8ea0a6a1c2d1c87d432c5a7145591c2c6014ab8e3fa0f3f6b545` | 41,166 |
| notify campaign log, head | `3dfc4ea08668700e5e7b5f2d7bc7b3c1d9ff952114ba1717eba1b6c6bbf51631` | 5,383 |
| d3 merged verdicts, base / head | `3afc136f...c87f9` / `f4a25114...1546d` | 8,063 / 8,063 |

The two utilization reports differ only in their `Date` line; the census above is
byte-identical. The parent patch here: `parent-adoption-148-6c22d3ca.patch`, sha256
`bbd0301d...ea83`, applied unchanged.

## Incident

The first base OOC run was taken for dead while it sat silently in timing optimization:
its directory was renamed and a duplicate run was queued on the Vivado lock. The duplicate
was stopped before it started Vivado (it never held the lock), the original finished, and
the names were restored. The figures above are the original run's.

The sequential campaign chains of both sides (adp, maap, notify, ctr, then d3) were ended by
the session's two-hour limit on a background command while d3 ran; d3 was resumed with the
driver's `--only` as described under Campaigns, and the chains' after-d3 watchers were
stopped by hand. Nothing else was lost: every other driver had finished, or ran in the
parallel chains, which completed.
