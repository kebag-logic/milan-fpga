# #665 S6a, the placement switch, round 2: [A745b] handoff

STATUS: REVIEW READY at `526f937cde45e3a591fb3b9484ffdcaddbdfa144`. Every finding of both reviews fixed; every gate rc 0 or its stated reason (section 4).

- Lane: `665-s6-placement`, worktree `$LANES/665-s6-placement`, PR #853 (target `dev-soft-core`).
- Base: `origin/dev-soft-core` `a9d69c774dee18b90eead74c9f2dda24cf8fdeb8` (the live tip, fetched 2026-11-08). Round 1 head `6584b7bfdf19e923153820c60190d87964e8f57b`. Eight commits on top; no rebase, no force. Nothing is pushed.
- Assignment: fix every finding of R791-1 and R792-1 at `6584b7bf`, the RESIDUE items too.
- TAKEN: issuecomment-6716159950. REVIEW READY: issuecomment-6717994137 (text in `REVIEW-READY-COMMENT.md`).
- Scratch (not in the output directory): `$VALIDATION_STORAGE/scratch/665s6-a745b/` holds the replay's clones and logs (`replay/`), the lane gates' clean clones (`final`, `probes`, `builder`, `fwclone`, `exportwt`, `cmp-a9d69c77`) and the placement's work tree (`place/`); the sweep's clones are `$LANES/665s6-a745b-526f937c-shard{0..3}`.

## 1. Findings and their fixes

| Finding | Severity, lens | Fix | Commit |
|---|---|---|---|
| R791-F1 two boundaries hide their unit; naming ratchet red | MAJOR RTL, Tests | `i_ctl_pub_idle_slope_bps`, `i_ctl_pt_offset_ns`, and the crossing's four ports on the same path, renamed through every binding; no ratchet exclusion | `f3f47605` |
| R791-F2 firmware boundary gate red twice | MAJOR Tests, Docs | the builder comment no longer names the firmware's tree; the firmware README states the self-test's 175 pin controls (the one edit under `sw/firmware/ctrl/`) | `7083bf97` |
| R791-F3 tap classification and the Talker declaration's encoding untested | MINOR Tests | a second `KL_ctrl_split` in the split leg, `u_tap`, holds all six accepted tuple classes and five refusals; the declaration check pins ADVERTISE | `6846011c` |
| R791-F4 the drop counter cannot count | MINOR RTL, Robustness, Tests | the count reads the FIFO's overflow indication for a frame the tap kept; the leg's `[TAP]` burst fails on round 1's RTL (3 failures) and passes now | `6846011c` |
| R791-F5 = R792 T-1 the CDC check's exemption | MINOR Tests, Docs (Conformance, Tests, Docs) | the held bus is admitted only through a `$mux` that `u_fw_req`'s `dest_pulse` selects, on its taken input; primitive resets are sinks in their own domain; every clock pin must read a clock input; the reviewers' probes are plants (12 in all) | `b09cb329` |
| R792 D-1 stale pages | MINOR Docs | `MAILBOX_SPLIT.md` publication section, `MARK_II_AREA_PLAN.md` L2, `CLOCK_DOMAINS.md` crossing map | `6855baf5` |
| R791-F6, R792 R-1 lane labels and comment IDs in source comments | RESIDUE | "(#665)" for each "(#665 F-INT PR 2)"; both ruling IDs dropped | `362e9ee1` |
| R791-F7, R792 R-2 REBOOT open item; PR body | RESIDUE | the open item names S11 and the tie; PR-BODY.md states each ruling's outcome | `362e9ee1`, PR-BODY.md |
| R792 R-3 wrong counter word | RESIDUE | "its STREAM_START counter" | `362e9ee1` |

Found in this round, not by either review: three gates of `docs-gates-0` were red at `6584b7bf` and the hosted job never reached them, since it stopped at the naming ratchet. Each passes at the base `a9d69c77`:

| Gate | At `6584b7bf` | Fix | Commit |
|---|---|---|---|
| Port contract gate (`check_port_contracts.py`) | 139 new undocumented ports (hdl 356 > 217); `u_pub.dest_req` open with no rationale | every new port documented (bundles without unit words, so the naming ratchet still passes); a rationale above the open `dest_req` | `a8ab58de` |
| Python idiom gate (`check_py_idiom.py`) | long function 10 > 9, long module 11 > 10, undocumented 8 > 0, unannotated 1 > 0, too many parameters 8 > 7, over-long line 9 > 0 | each new file brought to the ratchet; behaviour unchanged (identity digest, population and CDC self-tests reproduced) | `526f937c` |
| Test-evidence ratchet (`measure_test_evidence.py --check`) | 2 unexplained DUT-source readers; 4 wall-clock files > 3 | the two readers classified in `measure_test_evidence_readers.py`; the mutant campaign's `timeout=1800` dropped | `526f937c` |

## 2. Changes, file:line and reason

Line numbers are at the head, `526f937c`.

### R791-F1: the units in the names (`f3f47605`)

- `hdl/milan/milan_datapath.sv:714` `i_ctl_pub_idle_slope_bps`, `:731` `i_ctl_pt_offset_ns`; their readers `:9984`, `:10021`. CODE_QUALITY Rule 4: a boundary whose value has a unit carries it.
- `hdl/milan/mailbox/KL_mbx_cdc.sv:64` `m_pub_idle_slope_bps_i`, `:80` `m_fw_pt_offset_ns_i`, `:152` `d_pub_idle_slope_bps_o`, `:166` `d_pt_offset_ns_o`: the same two values on the crossing between `KL_mbx` (already `pub_idle_slope_bps_o`, `fw_pt_offset_ns_o`) and the datapath, so no hop of the path drops the unit.
- The bindings: `sw/litex/milan_soc.py:2906`, `:2910` (`CTRL_SPLIT_PORTS`), `:2934`, `:2940` (`_CTRL_CDC_DP`), `:2967` (`_CTRL_CDC_MBX`), `:3159` (the `KL_mbx_cdc` instance); `tb/verilator/milan_dp/tb_split_top.sv:227`, `:232`, `:256`, `:260`, `:316`, `:320`. The docs tables name the port group (`i_ctl_*`), not these ports, so none changes.

### R791-F2: the firmware boundary (`7083bf97`)

- `sw/builder/endstation_builder.py:4424`: the comment says "the linked platform image" without the firmware tree's path, so the builder again names that tree 0 times, as at the base. This keeps the builder out of `ctrl_configs`' classification rather than adding it there.
- `sw/firmware/ctrl/README.md:255`: 175 pin controls, the self-test's count since round 1 added four stack-pinned `milan_dp` targets. This is the only edit under `sw/firmware/ctrl/` (S2b's tree, PR #810); the PR body says so.

### R791-F3 and F4: the tap (`6846011c`)

- `hdl/milan/KL_ctrl_split.sv:184-191` `drop_track`: `last_kept_r` records, at each frame's last beat, whether the tap kept it (`TAP_BODY_S`, or `TAP_HEAD1_S` with `accept_w`); `drop_p_w = ff_overflow_w & last_kept_r`. `:232` takes the FIFO's `status_overflow`. With `FRAME_FIFO` and `DROP_WHEN_FULL`, `axis_fifo` holds `tready` high and drops a frame it has no room for by itself, pulsing `status_overflow` the cycle after that frame's last beat; a runt or a refused frame is reclaimed either way, so its overflow loses no control frame. The banner (`:38-43`) and `rx_drops_o` (`:80`) say what is counted: `PP_DIAG[15:8]`, "control frames lost to a full ingress FIFO" (`docs/reference/REGISTER_MAP.md`).
- `tb/verilator/milan_dp/tb_split_top.sv:83-93`, `:367`: `u_tap`, a second `KL_ctrl_split` from the datapath's own source (`CTLS_SRC`, so a mutant of the file reaches both), on the datapath clock, driven by the bench. The MAC boundary cannot stall the datapath's own tap, and its receive filter decides what reaches it.
- `tb/verilator/milan_dp/sim_split.cpp:522` `check_tap`: eleven tuples, each a 64-byte frame: ADP, AECP, ACMP, MAAP on 0x22F0 and MSRP and MVRP at their group addresses each handed out whole and counted; MSRP's and MVRP's EtherType at the other's group address, MSRP's at a unicast address, AAF and subtype 0xFD refused. `:565` `check_tap_drops`: with the byte side held, 100 frames of 64 bytes and eight of 16, then eight refused frames; every kept frame handed out or counted lost once, at least 4,096 bytes held, those handed out whole and in order, no refused frame counted, and 320 more frames saturate the count at 255. `:305-306` the declaration check is `== 1` (ADVERTISE), the encoding `gsi_ofail_w` (`milan_datapath.sv`) tells from FAILED.
- `tb/verilator/milan_dp/split_mutants.py:93-128`: nine arms (the reviewer's T1, T2 and D1 among them).
- Docs: `tb/verilator/milan_dp/README.md:109`, `:1120-1145` (the `u_tap` bullet, the `[PUB]` and `[TAP]` rows, twenty-two mutants); `docs/design/MAILBOX_SPLIT.md:1393-1398` (the drop count).
- Not changed: `KL_pp_shadow.sv`'s identical construction (R791-F4 asks for its own Issue; that is the manager's to open, section 5).

### R791-F5 and R792 T-1: the CDC check (`b09cb329`)

- `tb/verilator/milan_dp/split_cdc_check.py:72-85`: the allowance is `fw_r` (`HELD_FLOP`) taking the data bits of the held bus (`held_bus`: every `m_fw_*` input but `m_fw_send_i`) only on the `B` input of a `$mux` whose `S` is `u_fw_req`'s `dest_pulse` (`GATE`), straight. `Netlist.sources` (`:151`) carries a `taken` flag set only on that input; `findings` (`:212`) reports an untaken held bit as "takes the held bus ... other than through a $mux selected by u_fw_req.dest_pulse".
- `:72-74` `SRC_SINKS` and `DEST_SINKS`: a primitive's `src_rst_n` is judged in its source domain and `dest_rst_n` in its destination domain. `Netlist.sinks` (`:186`) also lists every flop's `CLK` and every primitive's two clock pins, which must read `sys_clk_i` or `dp_clk_i` straight.
- `:252-297` twelve plants (section 3). The docstring (`:4-49`) states the rule and what is not read here (KL_mbx's hold), and `docs/design/MAILBOX_SPLIT.md:1428-1440`, `tb/verilator/milan_dp/README.md:1145-1157` and the Makefile comment claim no more.

### R792 D-1: the stale pages (`6855baf5`)

- `docs/design/MAILBOX_SPLIT.md:826-832`: the split datapath reads the block through `KL_mbx_cdc` into its `i_ctl_pub_*` ports, selected by the placement switch; the `--ctrl-mailbox` SoC builds it and reads every port.
- `docs/design/MARK_II_AREA_PLAN.md:423-425`: the SoC builds the split datapath with `--ctrl-mailbox`; at `CTRL_SPLIT_P = 1` there is neither `KL_pp_shadow` nor `KL_maap`; the default build keeps them until the flip.
- `docs/litex/CLOCK_DOMAINS.md:244-245`: two rows, the frames' `ctl_rx_cdc`/`ctl_tx_cdc` and `KL_mbx_cdc`'s primitives.
- Not changed: `sw/firmware/ctrl/plat/README.md:137` (the same staleness, S2b's tree; R792 routes it to the manager).

### RESIDUE (`362e9ee1`)

- "(#665 F-INT PR 2)" became "(#665)" in each source comment R791-F6 lists (`KL_ctrl_split.sv:12`, `KL_mbx_cdc.sv:7`, `KL_mbx_cdc_window.sv:7`, `milan_datapath.sv:376`, `:9967`, `endstation_builder.py:4417`, `test_builder.py:23490`, `:23601`, `milan_soc.py:990`, `:2886`, `:3038`, `:3750`, `placement_identity.py:7`, `split_population.py:3`, `syn/yosys/run.sh:306`, the Makefile's three, `sim_split.cpp:4`, `split_mutants.py:4`, `tb_split_top.sv:6`; `split_cdc_check.py:4` in `b09cb329`). `milan_datapath.sv:380` and `:5641` drop the ruling IDs for "(#665)". Pre-existing labels at the base are untouched.
- `docs/design/MAILBOX_SPLIT.md:1751-1756`: "S11 (#665), after #810, gives the request its carrier ...; until then the split ties `reboot_req_i` to 0".
- `tb/verilator/milan_dp/sim_split.cpp:382`: "word 0, its STREAM_START counter".

### The three gates round 1 left red (`a8ab58de`, `526f937c`)

- Port docs: `KL_mbx_cdc.sv:59`, `:74`, `:147`, `:160`, `:177`, `:214` (bundle comments) and `:87-90` (three per-port); `milan_datapath.sv:747`, `:755`, `:765`, `:778` (one per window's fields); `KL_mbx_cdc_window.sv:35-45`; `KL_ctrl_split.sv:54-55`, `:75-77`. `KL_mbx_cdc.sv:244`: the open `dest_req`'s rationale, directly above its line so the line's text, which two reviewers' plants anchor on, is unchanged.
- Python idiom: `scripts/check_solution_docs.py:184`, `:208` (the module back to 998 lines: the new port group and the `Interrupt` group in the file's existing three-line form); `sw/litex/milan_soc.py:2940` (a wrapped line); `sw/mailbox/placement_identity.py:107-163` (four helpers out of `canonical`, docstrings, two wrapped lines); `syn/ooc/split_population.py:99` (`FrontEnd`, so `elaborate_tree` takes five parameters); `syn/resmap/resmap_map.py` (three wrapped lines); `tb/verilator/milan_dp/split_cdc_check.py:98` (`Netlist`, so `findings` is short); `split_mutants.py` (a docstring, two wrapped lines).
- Test evidence: `scripts/measure_test_evidence_readers.py:245-252` (the two readers' dispositions, for review to accept); `split_mutants.py:139` without `timeout=1800`, as the campaign's other benches run.

## 3. New checks, planted defects and failing words

Each campaign runs a clean control first; each defect is planted into a copy, never the tracked file.

### The split leg's `[TAP]` and `[PUB]` checks (`make split`, 66 checks, was 48)

Against round 1's `KL_ctrl_split.sv` (built with `CTLS_SRC` at the `6584b7bf` copy) the new leg fails three checks, so the test fails on the old RTL:

```text
FAIL [TAP] a burst past the FIFO's 4,096 bytes counts the frames it lost
FAIL [TAP] every frame of the burst is handed out or counted lost: got 0x41, want 0x6c
FAIL [TAP] the count saturates at 255: got 0x0, want 0xff
```

At the head: `[TAP] burst: 108 frames offered, 65 handed out, 43 counted lost`, 66 checks, 0 failures.

### `split_mutants.py` (`make split-mutants`): 22 arms, was 13

The nine new arms, each caught by the check it names (`FAIL <label>`):

| Planted defect | Source | Caught by |
|---|---|---|
| the Talker declaration published as FAILED (R791 D1) | datapath | `[PUB] TALKER_DECL.DECLARED reaches the declaration state as ADVERTISE` |
| a tap that refuses MSRP (R791 T1) | `KL_ctrl_split` | `[TAP] MSRP at 01-80-C2-00-00-0E is handed out whole, and counted` |
| a tap that refuses MVRP | `KL_ctrl_split` | `[TAP] MVRP at 01-80-C2-00-00-21 is handed out whole, and counted` |
| a tap that refuses MAAP (R791 T2) | `KL_ctrl_split` | `[TAP] MAAP (0x22F0, subtype 0xFE) is handed out whole, and counted` |
| a tap that takes MSRP at any address | `KL_ctrl_split` | `[TAP] MSRP's EtherType at MVRP's group address is refused` |
| a drop count read from the FIFO's tready (round 1's RTL) | `KL_ctrl_split` | `[TAP] a burst past the FIFO's 4,096 bytes counts the frames it lost` |
| a drop count that counts refused frames | `KL_ctrl_split` | `[TAP] ...and not the refused frames a full FIFO turns away` |
| a drop count that misses a frame kept at its second beat | `KL_ctrl_split` | `[TAP] every frame of the burst is handed out or counted lost` |
| a drop count that wraps | `KL_ctrl_split` | `[TAP] the count saturates at 255` |

### `split_cdc_check.py --selftest` (`make split-cdc`): 12 plants, was 4; 253 sinks, was 152

The sinks now include every primitive reset and every clock pin. The eight new plants, each refused by its words:

| Planted defect | Source | Failing words |
|---|---|---|
| the held bus taken on every datapath cycle (R791 R1; R792's first HOLE) | `KL_mbx_cdc` | `flop fw_r (dp) takes the held bus` |
| the held bus taken on the commit level (R791 R3; R792's second HOLE) | `KL_mbx_cdc` | `flop fw_r (dp) reads m_fw_send_i (sys)` and `flop fw_r (dp) takes the held bus` |
| the held bus taken on the request pulse in the mailbox's clock (R792's control) | `KL_mbx_cdc` | `flop fw_r (dp) reads fw_send_q_r, m_fw_send_i (sys)` and `flop fw_r (dp) takes the held bus` |
| the held bus taken while the pulse is low | `KL_mbx_cdc` | `flop fw_r (dp) takes the held bus` |
| a datapath flop other than `fw_r` sampling the held bus (R792's control) | `KL_mbx_cdc` | `flop ev_dom_r (dp) reads m_fw_identify_i (sys)` |
| a destination reset from the other domain (R791 R2) | `KL_mbx_cdc` | `u_pub.dest_rst_n (dp) reads sys_rst_n (sys)` |
| a source reset from the other domain | `KL_mbx_cdc` | `u_fw_ack.src_rst_n (dp) reads sys_rst_n (sys)` |
| a primitive clocked by a level | `KL_mbx_cdc` | `a clock that is not a clock input: u_fw_ack.dest_clk reads m_fw_send_i` |

The reviewers' own probe scripts, run unchanged at the head: R791's `cdc_plants.py` "raw crossings the check let through: 0" (R1, R2, R3 refused); R792's `cdc_check_probes.py` "probes: 5   departures from the docstring's rule: 0".

## 4. Gate table

Receipts are under `receipts/` (index: `receipts/INDEX.md`); host path prefixes in them read `<scratch>`, `<lane>`, `<tools>`, `<mgmt>` or `~`. Every row ran at `526f937c` on a clean clone (`git status` empty, submodules at their gitlinks), each command unpiped, its output to the receipt, whose first line names the head.

### The hosted jobs, replayed

Every `run:` step of every job a pull_request to `dev-soft-core` triggers in `docs.yml`, `elaborate.yml`, `rtl-fast.yml` and `rtl.yml` (matrix legs expanded: 19 Verilator and 4 Yosys shards), each job on its own fresh clone and venv (`scripts/run_job.py`); `scripts/verify_jobs.py` reads the step list from the workflows at the head and requires an rc of 0 or a rule of `scripts/not_run.json` for each.

**Result: 311 steps ran rc 0 (66 of them as a stated substitute), 316 not run with a reason, 0 bad; verifier rc 0** (`receipts/replay/jobs-table.md`, every step's log and rc in `receipts/replay/logs/`).

What stands in for the runner image, each stated in `not_run.json`: the host's pinned Verilator 5.050 build for `/opt/verilator`, its Yosys 0.66 for `/opt/yosys`, its sv2v 0.0.12, its GoogleTest headers and `rsvg-convert` for the `sudo apt-get` lines (the steps' other lines run as written), and the host's LiteX venv and sbt caches for the two elaboration legs (`--gate-env`). The pinned RV32 SDK was installed once by `scripts/ci_rv32_sdk.py` into the replay's CI HOME and verified by each job's own install step. Each venv starts with PyYAML, as the runner image's Python does. Not run at all: the hosted-context steps (step and gate receipts, manifests, fail-fast, cancel), the aggregates that read uploaded artifacts (`docs-check`, `elaborate`, `verilator-suites`, the six unions), the 19 `--ci-pieces` suite shards (the full sweep below runs the same suites), `physical-gptp` (its `if:` excludes a pull_request).

Three replay notes, for a reviewer to weigh:
- The 19 "Prove specialized suite ownership" steps ran in a venv of the host's Python 3.14: `run_all_suites.sh`'s process ownership needs `os.pidfd_open`, which the replay's Python 3.12 build lacks (the hosted runner's has it).
- `docs-gates-2`'s act-runner contract step (`gate_42`) ran the candidate's `act_ci.py --selftest` inside the replay's job on the host, and again in a `--network=none` container with the source mounted read-only (`docs-gates-2__gate_42-container.log`, rc 0), the disposable boundary AGENTS.md section 5 asks for. `act_ci.py` is unchanged from the base.
- Five install steps, `firmware-boundary`'s gate step and `bdd-conformance`'s suite ran a second time on their job's clone (`run_job.py --reuse`) after a fix to the replay itself: an exact-line sv2v version match, the `firmware-boundary` install step's `-r sw/litex/litex_pins.txt` that a first substitute dropped, and `working-directory: tests` with PyYAML for behave.

| Job (workflow) | Gate step | rc | Result |
|---|---|---|---|
| docs-gates-0 (docs) | all 43 gate steps, with `measure_naming.py --check` and `--selftest`, `check_port_contracts.py`, `measure_test_evidence.py --check`, `check_py_idiom.py`, `check_doc_style.py`, `docs_check.py`, `check_em_dash.py`, the HDL reference build | 0 each | naming PASS (95 recorded), port contract OK (hdl 217 <= 217), test evidence PASS, py idiom PASS, 0 doc findings, em dash 0 over 202 added lines |
| docs-check-no-git (docs) | `docs_check.py`, `check_feature_status.py` without `.git` | 0 | 0 findings |
| wire-accountability (docs) | `check_wire_accountability.py --self-test` | 0 | PASS |
| docs-gates-1, -2 (docs) | `ci_builder_legs.py run 0`, `run 1` -- `test_builder.py --require-rv32` | 0, 0 | `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 1b's MAKEFLAGS mutation), `EXCEPT 16 NOT RUN` (arms needing LiteX, absent as on a fresh runner; the elaboration legs run them) |
| docs-gates-2 (docs) | `ci_events.py --check`, `--selftest`; `act_ci.py --selftest` | 0 | 2199 contract items; PASS |
| elaborate-gates-0, -1 (elaborate) | `ci_builder_legs.py run 0`, `run 1` -- `test_builder.py --require-elaboration --require-rv32`; `run_litex_sims.sh` | 0, 0, 0 | `ALL GATES PASS EXCEPT 1 NOT RUN` each (gate 1b's mutation; gate 11, an earlier board build's report not on this host, as in round 1); 8 of 8 LiteX simulations |
| changes, verilator-lint (rtl-fast) | `ci_scope.py`; `lint_rtl.py --check --self-test`, `pp_srcs.py --check --selftest` | 0 | rtl=true; `LINT GATE: PASS (89 <= 89)` |
| bdd-conformance (rtl-fast) | `behave --no-capture -f plain` in `tests` | 0 | 14 features, 508 scenarios, 2,330 steps |
| yosys-elaboration (rtl-fast) | `run.sh --mode elaborate` of the three tops, the OOC, `pp_baseline*`, `pp_resource_gate*`, guard and cache self-tests | 0 each | PASS |
| publication-census (rtl-fast) | `publication_census.py --check --selftest` | 0 | 6 shapes, 246 checks, 0 failures; self-test 139 arms, 0 failed; 0 of 43 rules unproved |
| firmware-unit, -control-, -aecp-, -srp-mutants (rtl-fast) | `test_ctrl_firmware.py --require-rv32 --self-test --shard k/4`, k = 0..3 (the union is the whole self-test); `fw_rv32_selftest.py`, `test_ctrl_nvm.py`, `fw_coverage.py` | 0 each | `test_ctrl_firmware: PASS` each; control mutants 570 of 570 |
| firmware-boundary (rtl-fast) | `ctrl_boundary.py --require-rv32 --selftest --without verilator` | 0 | `ctrl_boundary: PASS` (3,258 compiled sources judged) |
| firmware-verilator (rtl-fast) | `ctrl_boundary.py --require-rv32 --selftest --only verilator` | 0 | `ctrl_boundary: PASS` (1,019); with the line above, every part |
| rtl-fast (rtl-fast) | "Require every applicable fast gate to pass", fed each job's local outcome | 0 | all twelve `success` |
| full-ci-gate (rtl) | the SHA pin, the default branch, `ci_events.py --check`, `ci_scope.py` | 0 each | default branch `dev`; run_full true |
| verilator-shards 0..18 (rtl) | the tree record, Verilator 5.050 on PATH, `suite_shards.py --selftest` and each shard's `--list` | 0 each | each shard's ownership as the workflow requires |
| yosys-shards 0..3, yosys-portability (rtl) | `run.sh --shard k/4`; `yosys_tally.py --require-structural` over the four results | 0 each | 1, 1, 30 and 30 tops, 0 failed, and shard 0's structural and tap-purity checks; `Yosys evidence: expected=62 observed=62 errors=0` |

### The lane's own gates and the findings' verification steps

| Gate | Command | rc | Result | Receipt |
|---|---|---|---|---|
| Full sweep, 4 shard units | `native-shards.py 665s6-a745b-526f937c ... 4 0-7 8-15 16-23 24-31` (each `run_all_suites.sh <logs> --wait --shard k/4`) | 0 x4 | 65 suites, 0 failed, 0 timed out; 2,192,894 checks, 0 in-suite failures; the split case 66 checks | `sweep/SUMMARY.md` |
| All-fabric identity, 6 shapes | `placement_identity.py --dump` (base `a9d69c77`, head), `--compare` | 0 | every digest equal, and equal to round 1's and R791's receipts | `gates/identity-*.log`, `gates/ident-*.json` |
| Identity self-test | `placement_identity.py --selftest --jobs 4` | 0 | 6 of 6 arms | `gates/identity-selftest.log` |
| Export compare, 5 shipped configs | `scripts/export_compare.sh` (round 1's recipe) | 0 | each 3,876 files: 3,856 identical, 20 by the stated normalisations, 0 different | `export/` |
| Full-split population | `split_population.py --check --jobs 6`, `--selftest` | 0, 0 | every role within its limits; 3 of 3 | `gates/population-*.log` |
| Builder, whole bank | `test_builder.py --require-rv32` (pinned SDK, LiteX venv) | 0 | `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11, as in round 1) | `gates/test-builder-require-rv32.log` |
| Split leg | `make -C tb/verilator/milan_dp split` | 0 | 66 checks, 0 failures | `gates/split-leg.log` |
| Split leg on round 1's tap (F4's "fails on the old RTL") | `make build-split CTLS_SRC=<6584b7bf's KL_ctrl_split.sv>`, then the leg | 1 (required) | 3 failures, all `[TAP]` drop checks; 0 frames counted of 43 lost | `gates/split-leg-old-tap.log` |
| Split mutants | `make -C tb/verilator/milan_dp split-mutants` | 0 | control passes; 22 of 22 caught by the check each names | `gates/split-mutants.log` |
| CDC structure | `make -C tb/verilator/milan_dp split-cdc` | 0 | 253 sinks in their domain; 12 of 12 plants refused | `gates/split-cdc.log` |
| R791-F5 verification | R791's `cdc_plants.py` | 0 | R1, R2, R3 refused; "raw crossings the check let through: 0" | `gates/r791-cdc-plants.log` |
| R792 T-1 verification | R792's `cdc_check_probes.py` | 0 | both HOLE probes refused; "departures from the docstring's rule: 0" | `gates/r792-cdc-check-probes.log` |
| R791-F3 verification | R791's `split_reviewer_mutants.py` | 0 | T1, T2, D1 caught by named checks; E1-E3, G1, G2, C1, W1 survive (S6b's) | `gates/r791-split-reviewer-mutants.log` |
| R791-F4 verification | R791's `ctrl_split_drop_probe.cpp` on `KL_ctrl_split` | 0 | 100 offered, 64 handed out, `rx_drops_o` 36 | `gates/r791-drop-probe.log` |
| R791-F2 verification | R791's `ctrl_boundary_probe.py` | 0 | 0 unclassified; the self-test's 175 pin controls, the README's 175 | `gates/r791-ctrl-boundary-probe.log` |
| Docs style on the touched pages | `doc_style_added.py 6584b7bf` (the gate's rules over the added lines) | 0 | `CLOCK_DOMAINS.md`, the one touched page the gate judges, 0 findings; the others are outside its population | `gates/doc-style-added-lines.log` |
| xvlog, under the Vivado lock | `xvlog_gate.py --check`, `--selftest` | 0, 0 | `PASS (0 finding(s) == ratchet)`; the planted use-before-declaration reddens it | `gates/xvlog-*.log` |
| Split image | `split-firmware.sh` (the daily recipe, with its flash map) | 0 | `ctrl_app.elf` 140,628 bytes, sha256 `547d4c70...`, byte-identical to round 1's | `image/` |

### The one Vivado placement of the split image (a measurement, not a gate)

Re-run because `KL_ctrl_split`'s drop count is a logic change in the split image. At `526f937c`, under the host lock and after both lanes' sweeps had ended: round 1's `scripts/split_place.sh` (the shipping AX7101 1x1 TDM8 argv plus `--ctrl-mailbox --ctrl-firmware`, synthesis `AreaOptimized_high`, opt `ExploreArea`, place `ExtraPostPlacementOpt`, phys_opt; not routed), with the image above. **It places**: Vivado rc 0, 0 ERROR, 0 CRITICAL WARNING, 32 minutes (`vivado/run.txt`). The unit's memory peaked at 19.0 GB; its cap was raised from 16 to 24 GB at 13.5 GB.

| Step | LUT | FF | Slices | BRAM tiles | DSP | WNS / WHS |
|---|---|---|---|---|---|---|
| Synthesis | 35,982 (56.75 %) | 45,372 | | 93 | 5 | |
| Placement | 34,228 (53.99 %) | 45,234 (35.67 %) | 14,383 of 15,850 (90.74 %) | 93 of 135 (68.89 %: 75 RAMB36, 36 RAMB18) | 5 | -0.021 ns over 22 endpoints / -0.248 ns over 431, post-placement estimates |
| Round 1, `6584b7bf` | 34,225 | 45,222 | 14,147 (89.26 %) | 93 | 5 | -0.071 ns over 24 / -0.245 ns over 350 |

Placed blocks: `milan_datapath` 18,584 LUT, 22,479 FF (round 1 18,546, 22,468); `KL_mbx` 4,433, 8,576; `KL_mbx_cdc` 1,397, 3,011; `KL_ctrl_split` 226, 270 (round 1 224, 261: the drop count's flop and the FIFO's overflow flag). The worst setup path is on the 100 MHz system clock, inside `KL_mbx`'s event block (`u_evt/gm_pend_r` to `rec_r`, 18 logic levels, 9.896 ns). Hold is short between two CRG clocks and on the RX clock, which the router normally fixes. Whether a route closes timing is not measured.

## 5. Not done, and why

- **The wrapper's identical uncounted drop.** `KL_pp_shadow.sv`'s tap counts `drop_p_w = fw_valid_w & ~fw_ready_w` under the same `FRAME_FIFO`/`DROP_WHEN_FULL` FIFO, so the all-fabric `PP_DIAG[15:8]` still reads 0 under a burst. R791-F4 asks for its own public Issue, not a change in this lane; this round may post only TAKEN, REVIEW READY or STOP, so the Issue is the manager's to open.
- **`sw/firmware/ctrl/plat/README.md:137`**, the same staleness as R792 D-1, in S2b's tree: R792 routes it to the manager (S2b or S6b).
- **Ruling 6715535566 item 5, "say so where it is defined"** (`pp_placement.py`'s `f0-f4` dead until the flip). Neither review raised it, and this round is held to what the findings need; the PR body states the outcome. A one-line comment in `syn/ooc/pp_placement.py` for whichever lane the manager names.
- **The seven split-leg paths the reviewers' mutants still pass** (E1-E3, G1, G2, C1, W1: the `EDIT` window, the face and counter-change events, the GM change and identity). Both reviews record them as S6b's two-placement comparison's, not a finding of this round; `r791-split-reviewer-mutants.log` shows them surviving and T1, T2, D1 caught.
- **The Yosys area table** is round 1's, at `61d680dd`'s RTL. The split's only logic change since is the drop count (one flop and the FIFO's overflow flag); the one Vivado placement was re-measured at the head instead (section 4).
- **Hosted-only steps**: every one is listed with its reason in `receipts/replay/jobs-table.md`, from `scripts/not_run.json`.
