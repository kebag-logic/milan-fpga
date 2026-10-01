# [A485] Lane C5a round 3b — HANDOFF

Status: DONE (2026-10-01 23:30 CEST). Head `ee0e2b72ea10c83f983ec9e35878fb0193223ccb`, the merge commit; unpushed.

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #140, branch `c5a-aecp-deadlines`
- Start head: `d4ca85c60e1e12b9fa0923e83bdfe39ce16e7d59` (round 3, unpushed)
- Assignment: issue #81, [A10] Round 3b comment (merge processor `main` `16ea10ac`)
- TAKEN: issue #81 comment 5936577660; REVIEW READY `ee0e2b72ea10c83f983ec9e35878fb0193223ccb`: comment 5940939453
- Toolchain: Verilator 5.050 (CI pin), under an eight-CPU mask, one heavy job at a time

## Item 1 — merge `main` `16ea10ac` (`git merge --no-ff`, no rebase)

Main brings PR #138 (lane C5b, AECP dispatch). Conflicts, each kept on both sides:

| File | Resolution |
|---|---|
| `.gitattributes` | both whitespace lines (`tb/pp_top/mutations/`, `tb/pp_top/aecp_dispatch_mutations/`) |
| `.github/workflows/hdl.yml` | both campaign steps: `aecp-mutants`, then `aecp-dispatch-mutants` |
| `tb/pp_top/Makefile` | four builds: default, DV fixture, C5b's line build (third, AX), this lane's timebase build (fourth, TB); the tally awk expects 4; both mutant outputs; `.PHONY` carries every target of both sides; `clean` removes `obj_line` and `obj_tim` |
| `tb/pp_top/pp_top_wrap.sv` | both tap groups (DL/HZ taps, AX taps); both define-driven overrides; banner names four builds |
| `tb/pp_top/sim_main.cpp` | `load_descriptor_image(entity_cfg, extra_ents, extra_bodies, sigmux_len)`: C5b's appended rows and this lane's SIGNAL_MULTIPLEXER length (TB passes `{}, {}, SIGMUX_LEN`); sections AX then DL, TB, HZ; `main()` has the fixture, line and timebase builds and every focus flag of both sides (`--aecp-dispatch-only`, `--deadline-only`, `--hazards-only`) |
| `tb/pp_top/README.md` | build paragraph (four builds); both mutation tables; the build table with four rows |
| `tb/ucpu/sim_main.cpp` | `disp_batch_i = batch || batch_base >= 0`, `disp_resp_base_i` from `batch_base` |
| `tb/ucpu/README.md` | the count re-measured: 427 (base 386, main 398 = +12, this lane 415 = +29) |

Semantic merge fixes (no textual conflict, but needed to keep both sides true):

- C5b's arms `ov-oversize-never` and `ov-oversize-at-576` no longer applied: `txs_oversize_o`
  (`hdl/aecp/KL_aecp_engine.sv:2583-2585`) is now this lane's three-line expression (the MVU echo term; Milan
  v1.2 §5.4.1, §5.4.3.3 Table 5.19). Both patches regenerated on the merged engine with the same defect
  (`1'b0` for the whole request; `>=` for `>` on the frame-length term). Every other patch of both campaigns
  applies unchanged (75 of 77 before, 77 of 77 after). Both arms re-measured at their README counts (18, 4).
- Main's #82 makes READ_DESCRIPTOR overlay the current sampling rate, clock source and stream format (IEEE
  1722.1-2021 §7.2.3, §7.2.32, §7.2.6). The round-3 classifier comment and 03 §6 said READ_DESCRIPTOR reads
  only descriptor-image fields. Both now say no ACMP step writes what it reads: image fields or those overlay
  rows, which only the AECP engine's state port writes (`KL_aecp_dyn_state` has one write port, driven inside
  `KL_aecp_engine`). Comment only, no logic: `hdl/top/protocol_processor_top.sv:1469-1473`,
  `docs/architecture/03_packet_engine.md:229-231` (F03.7 RO_SNAPSHOT rule).
- No new test and no RTL logic fix in this round; no failing arm was added. The merge's tests are both sides'
  (sections AX, DL, TB, HZ; `tb/ucpu` P9b, P11b/c, P20) with both campaigns intact.
- "third build" for section TB is now "fourth build" in 08 §4, 09 §8.3, the `tb/pp_top` README, the bench and
  `aecp_mutants.py`.

Gates run on the resolved tree before the first build: `check_upc_map.py` PASS (59 constants, 87 entry points),
`check_m9_opcodes.py` PASS (30 opcodes) and `--selftest` 9 of 9, `gen_ucode.py` 2048 words, 87 programs.

Merge commit: `ee0e2b72ea10c83f983ec9e35878fb0193223ccb` (parents `d4ca85c`, `16ea10ac`). The top's port and
parameter header is byte-identical to main's and declaration-identical (comments stripped) to `d4ca85c`,
`3f3ea56` and `0451d83d`: main changed two parameter comments only.

## Item 2 — re-measure at the merge commit

Every step ran at `ee0e2b7` with every build product deleted first (`.venv-wavedrom` kept), Verilator 5.050,
eight-CPU mask, one job at a time. Receipts: `$VALIDATION_STORAGE/a485-receipts/` (copied at the end).

| Step | rc | Result |
|---|---|---|
| `./scripts/run_suites.sh` | 0 | µPC map gate (59 constants, 87 entry points), M9 selftest 9/9 and gate (30 opcodes); 33 suites, 1,018,843 checks, 0 failing (736 s) |
| `./scripts/lint_hdl.sh` | 0 | 41 modules |
| `make check` | 0 | 1,017 links, 115 REQ rows, 17 GAPs, 94 rows 0 untested, 26 parameters |
| `scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `make -C tb/ucpu run` | 0 | 427 / 427 |
| `./syn/yosys/run.sh` | 0 | 36 tops + the Xilinx check of `KL_aecp_engine` |

Check totals, no check lost: `tb/pp_top` 8,901 = 8,288 (lane, `d4ca85c`) + 8,605 (main, #138's record) − 7,992
(base `3f3ea56`, #137's record); builds 8,607 default + 20 fixture + 218 line + 56 timebase. `tb/ucpu` 427 =
415 + 398 − 386 (main and base measured here from `git archive` exports). Sweep 1,018,843 = 1,018,218 +
1,018,518 − 1,017,893.

`tb/pp_top` entry points, each alone, rc 0, 0 failures: `name-writes` 85, `gsi-internal` 6,182,
`maap-internal` 34, `adp-config` 55, `deadline` 64, `d3` 133, `hazards` 176, `budget` 56, `--acmp-only` 43
(all as round 3); main's `aecp-dispatch` 915 (A5b, M9 and AX 218), `aecp-line` 218 (DESC_LINE_BYTES_P 584),
`line-guards` 6 of 6.

Campaigns:

| Campaign | rc | Result |
|---|---|---|
| `make -C tb/pp_top aecp-mutants` | 0 | 5 controls PASS, 55 of 55 KILLED; every failing count equals `tb/pp_top/README.md` (49 cells read by script, the 6 "the same N" cells 12, 12, 12, 13, 7, 7 by hand) |
| `make -C tb/pp_top aecp-dispatch-mutants` | 0 | 3 controls PASS, 35 of 35 KILLED; every failing count equals its README cell (35 of 35 by script), the two re-cut arms 18 and 4 as recorded |
| `python3 tb/pp_top/acmp_mutants.py --jobs 1` | 0 | 3 goldens PASS, 19 of 19 KILLED; each failing count equals #137's table (acmp_listener 93/50/40/30, rx_validator 27, pp_top AC 1, 19, 7 x4, 6, 1, 1, 2 x3, 5 x2) |
| `make -C tb/maap mutants` | 0 | 32 of 32: 3 controls (maap 196, pp_top MP 34, rx_validator 555), 29 arms KILLED; 29 of 29 cells equal `tb/maap/README.md` by script |
| `make -C tb/adp_engine mutants` | 0 | 32 of 32: 2 controls, 30 arms KILLED; 30 of 30 cells equal `tb/adp_engine/README.md` by script |
| `make -C tb/srp_top mutants` | 0 | 90 of 90, assertion coverage 65/65 (no input of this campaign changed in the merge) |
| `make -C tb/nvm_port figures` | 0 | every measured figure agrees with the README |
| `python3 tb/pp_top/d3_mutants.py --jobs 2` | 0 | 83 of 83 KILLED, goldens PASS; 82 counts equal `tb/pp_top`/`tb/acmp_nvm` README cells by script, `validator_admits_held_aecp` equals `tb/rx_validator` README M4 (4) |
| `python3 tb/pp_top/gsi_mutants.py` | 0 | 20 detected, golden and restored PASS (the README records no per-arm counts) |
| `python3 tb/pp_top/name_wr_mutant.py` | 0 | killed, golden and restored PASS |
| `python3 tb/acmp_talker/retry_mutants.py` | 0 | 62 killed, 7 equivalence, 1 performance control |
| `python3 tb/srp_admission/mutants.py` | 0 | 12 of 12 |
| `python3 tb/desc_mem_guard/mutate.py` | 0 | hold-deleted mutant detected |

No arm lost in any campaign. The merge (vs `d4ca85c`) touches only docs, CI, `hdl/aecp`, `hdl/top`, scripts,
`tb/pp_top` and `tb/ucpu`, so the SRP, NVM, retry, srp_admission and desc_mem_guard inputs are unchanged.

## Item 3 — parent consumer gates at milan-fpga dev `d4dd7426`

Scratch parent `$VALIDATION_STORAGE/a485-parent`: `git archive` of the read-only checkout
`$LANES/trusted-dev-20261001-d4dd7426` (982 index entries; the scratch commit's tree object equals the
checkout's, `84d57ec2`). Submodules: `gptp-processor` `5dce647a` and `third_party/verilog-axis` `48ff7a7e` cloned
from their URLs at the pins; `external` recorded, uninitialised (as in the checkout); `protocol-processor` a clone
of this lane at `ee0e2b7`, gitlink staged to it; all three registered with `git submodule init`. #137's disposition
line applied first (`parent-adaptation-137-acmp-disposition.patch` in this directory, +4 lines in
`scripts/measure_test_evidence.py`). `git status` after the gates: only that file and the gitlink. The trusted
checkout was not modified. Verilator 5.050 (the parent's `elaborate.yml` pin). Receipts:
`$VALIDATION_STORAGE/a485-receipts/pg/`.

| # | Gate | rc | Result |
|---|---|---|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 | every ratchet held |
| 2 | `scripts/check_py_idiom.py` | 0 | every ratchet held |
| 3 | `scripts/xvlog_gate.py --check` | 0 | 4 findings == ratchet, none new; pinned at protocol-processor@ee0e2b72 (145 s) |
| 4 | `scripts/check_rtl_source_lists.py` | 0 | 107 files, 4 of 4 lists; protocol-processor 36/42 tops, 6 recorded |
| 5 | `scripts/pp_srcs.py --check --selftest` | 0 | 46 sources, self-test passed |
| 6 | `sw/builder/test_builder.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 needs the mf48 board report, not on this host) (995 s) |
| 7 | `make -C tb/verilator/pp_shadow -j8` | 0 | 606, 606, 646, 311 checks, 0 failures |
| 8 | `scripts/check_port_contracts.py` | 0 | 48 literal-bound, 59 without rationale, lowerable by 3 |
| 9 | `scripts/measure_naming.py --check` | 0 | 96 recorded |
| 10 | `scripts/measure_test_evidence.py --check` | 0 | 72 <= 77, 10 <= 10, 0 <= 0 unexplained DUT readers, 3 <= 3 |
| 11 | `scripts/docs_check.py` | 0 | 0 findings |
| 12 | `scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j8` | 0 | 9 RESULT PASS, none failing (1,580 s) |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | leg defects 5/5 |

## Parent-visible list

- No top-level port, parameter or register-map change: the top's header is main's byte for byte; declarations
  equal `0451d83d`, `3f3ea56` and `d4ca85c`. The merge resolution edits one RTL comment (the classifier banner)
  and no RTL logic.
- The merge brings #138 (C5b); its own list applies at pin adoption: `DESC_LINE_BYTES_P` legal range enforced
  (multiple of 8, 576..1008; the parent's 576 is the floor); GET_AUDIO_MAP pages of 63..71 records served whole;
  READ_DESCRIPTOR serves the current values a SET stored (#82); ENTITY_LOCKED carries the value in force (#53);
  #74 commands graded; new entry points `make -C tb/pp_top aecp-dispatch`, `aecp-line`, `line-guards`,
  `aecp-dispatch-mutants`, `--aecp-dispatch-only`. No parent registry entry for C5b: gate 10 counts 0 unexplained
  DUT-source readers with only #137's line added.
- #137's `DUT_READER_DISPOSITIONS` line is still owed by the pin bump (applied in the scratch parent only).
- `tb/pp_top` 8,901 checks over four builds, `tb/ucpu` 427, sweep 1,018,843.
- Docs: 03 §6 and the classifier banner name READ_DESCRIPTOR's overlaid rows; 08 §4 and 09 §8.3 name section TB's
  build as the fourth.
- Wire changes are #138's; this lane's merge adds none.

## What remains

Unchanged from round 3 (see PR-BODY.md "What remains"): #81 acceptance 4; #84 (REGISTRY_OP without a reachable
conflict, acceptance 4, GET_DYNAMIC_INFO's GET_STREAM_INFO records not serialized); F03.3 kill count/trace; ACMP
has no deadline kill consumer; the `KL_aecp_notify` tracking item (the manager's). Hosted CI, the review of the
merge head and hardware were not run here. PR-BODY.md keeps `Closes #57`, `Relates to #81`, `Relates to #84`.
