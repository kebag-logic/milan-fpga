# [A755] processor #217: ENTITY descriptor available_index from ADP

Status: REVIEW READY at 794f844 (2026-11-09; posted on #217 as "[A755] REVIEW READY
794f8442c3d9da158c99d358d825c7b277516bba", issuecomment-6746766008). Every acceptance item is met; every gate below
ended rc 0. Push
nothing from here: the manager pushes and opens the PR from PR-BODY.md. This round was resumed twice: at 07:21
after the session host's authentication failure at 06:4x, and at 10:56 after the owner's planned reboot at 10:34
(neither a STOP).

## Acceptance (issue #217)

| Item | Met by |
|---|---|
| READ_DESCRIPTOR(ENTITY) returns the last sent ENTITY_AVAILABLE's `available_index` | the RTL changes below; pp_top section AI (`AI: 16 checks, 0 failures`) and IF4 at the head |
| A test reads it after several advertisements and after ENTITY_DEPARTING; a planted mutant that serves the constant fails it | section AI reads after 4 advertisements, after ENTITY_DEPARTING and after the re-enable; `ai-entity-image-copy` and `ai-gather-constant` serve the constant and are KILLED (4 failures each); at the base the section fails 4 |
| No change to the AEM image's other fields or to ADP's timing | `hdl/aecp/desc` untouched; every response graded whole against the image; ADP's wire path untouched and its suite passes; the twin's fabric capture identical in time and bytes but octets 36..39 of one response |
| The parent's gates that read AECP and ADP pass on a scratch parent with this head pinned | milan_dp, the firmware AECP and ADP campaigns and every rtl-fast job rc 0 (table below), plus five more benches |

Note for the manager: the parent issue kebag-logic/milan-fpga#858 cites "Table 7.1"; in IEEE 1722.1-2021 the
ENTITY descriptor is Table 7-2 (Table 7-1 is Descriptor Types), as this issue says. Checked in the PDF.

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan (origin, checked before the first commit)
- Base: 044cb25f4ed2187bd238490650e73d5d189855d1 (processor main, Merge PR #215)
- Branch: 217-available-index
- Head: 794f8442c3d9da158c99d358d825c7b277516bba
- Commits (base..head), one-line subjects:
  - 07f7b04 Read ENTITY's available_index after each ENTITY_AVAILABLE and after ENTITY_DEPARTING in pp_top section AI (issue #217)
  - db131cb Serve the last ENTITY_AVAILABLE's available_index in READ_DESCRIPTOR(ENTITY) from ADP, per the command's interface (issue #217)
  - 9bd6b43 Grade the last available_index in ADP P2, P3, P7, IF4 and IF9 and per interface in pp_top IF4, take the served index in the ENTITY reads, and plant five arms (issue #217)
  - 43149fb Record the ENTITY descriptor's available_index from ADP, section AI, IF4 and the five arms in 04 5, 06 6.1, REQ-ADP-011 and the suite READMEs (issue #217)
  - 794f844 Re-anchor the rdc-base-no-overlay and store-link-detector-resets-up arms on the E_RDESCENT and harness-reset lines issue #217 moved
- hdl/srp: not touched (0 files). MRP timers (Milan v1.2 4.2.7.2.2, Table 4.3): not touched.
- No top-level port, parameter or register-map change: `protocol_processor_top`'s port list and parameters are
  unchanged. The two new ports are on the internal modules `KL_adp_engine` (output) and `KL_aecp_engine` (input).
- AEM image: `hdl/aecp/desc` not touched; the image's bytes are unchanged (the descriptor's octets other than 36..39
  are graded whole against it).

## Clauses (read in the standards PDFs; receipts/STANDARDS.txt)

- IEEE 1722.1-2021 7.2.1 Table 7-2 (ENTITY descriptor): available_index, offset 36, 4 octets, "the same as the
  available_index field in ATDECC Discovery Protocol. See 6.2.2.15."
- IEEE 1722.1-2021 6.2.2.15: incremented after transmitting an ENTITY_AVAILABLE, reset to zero when transmitting
  an ENTITY_DEPARTING or after a power cycle. 6.2.4.3 Figure 6-2: INITIALIZE sets it to 0.
- IEEE 1722.1-2021 7.4.5.2 Figure 7-31 (READ_DESCRIPTOR response), 6.2.2.8 and 7.6.5.1 (a dynamic field).
- Milan v1.2 5.4.2.4 (READ_DESCRIPTOR as 1722.1 7.4.5), 5.6.3 and 5.6.3.5.1 to 5.6.3.5.11 (one advertise machine
  per AVB interface; SHUTDOWN sends ENTITY_DEPARTING).

## Reproduction at the base (first commit, 07f7b04, run on the base tree with the new section only)

`make -j8 avail-index` in tb/pp_top on the base RTL with section AI added: rc 2,
`AI: 16 checks, 4 failures` (receipts/repro-base). The failing words:

    FAIL: AI2: READ_DESCRIPTOR(ENTITY) after that ENTITY_AVAILABLE carries available_index 1, the image's other octets byte-exact (got 354 B, available_index 0)
    FAIL: AI2: ... carries available_index 2 ... (got 354 B, available_index 0)
    FAIL: AI2: ... carries available_index 3 ... (got 354 B, available_index 0)
    FAIL: AI4: READ_DESCRIPTOR(ENTITY) after the second ENTITY_AVAILABLE re-enabled carries available_index 1, ... (got 354 B, available_index 0)

AI1 (before any ADPDU), AI2 after the first advertisement and AI3 (after ENTITY_DEPARTING) pass at the base
because the constant 0 happens to equal the right value there; the four reads after the second to fourth
advertisement and after the second re-enabled one fail.

## Changes (head 794f844)

| File:line | What | Clause |
|---|---|---|
| hdl/adp/KL_adp_engine.sv:182 | new output `last_avail_index_o[N_IF_P*32]`, per interface the available_index the last ENTITY_AVAILABLE handed to TX carried | 1722.1-2021 6.2.2.15, Table 7-2 |
| hdl/adp/KL_adp_engine.sv:977-988 | `last_aidx_r[]`: takes the builder's own wire sample `bld_aidx_r` on the cycle an ENTITY_AVAILABLE is handed to TX (`bld_done_avail_w`), 0 on the cycle an ENTITY_DEPARTING is (`bld_done_dep_w`), 0 at reset. `aidx_r` is the next frame's index and cannot stand in. Nothing on the wire reads it, so ADP's frames and timing are unchanged | 6.2.2.15; Milan v1.2 5.6.3 |
| hdl/adp/KL_adp_engine.sv:1120-1123 | flatten to the port, interface 0 in the low word | |
| hdl/aecp/KL_aecp_engine.sv:587 | new input `adp_avail_index_i[32]` | Table 7-2 |
| hdl/aecp/KL_aecp_engine.sv:1086, 2819, 2914, 3015, 3359 | `rdent_r`: set only where READ_DESCRIPTOR(ENTITY) is re-dispatched to `E_RDESCENT`, cleared at reset and at every other dispatch | 7.4.5 |
| hdl/aecp/KL_aecp_engine.sv:2266, 2481 | the gather mux: with `rdent_r` the one `GATHER_EXT` of `E_RDESCENT` returns `{32'd0, adp_avail_index_i}` (routed like the started bit's 0xD0) | Table 7-2 |
| hdl/aecp/ucode/gen_ucode.py:382-389 | `ENT_AIDX_OFF = 36`, `ENT_AIDX_TAIL = 40`, `GX_ADP_AIDX` (selector 0xE0) | Table 7-2 offset 36 |
| hdl/aecp/ucode/gen_ucode.py:787-830 | `E_RDESCENT`: COPY_BUF bytes 0..35, BUILD_FLD the 4-byte index at 36, COPY_BUF TAIL 40..309, then current_configuration as before; an assert pins the gather's slot | Table 7-2; 7.4.5.2 |
| hdl/top/protocol_processor_top.sv:1095-1096, 2118, 4053 | internal wires from ADP to AECP | |
| hdl/top/protocol_processor_top.sv:4148-4160 | the index served is that of the interface the AECP command came in on (`aecp_cmd_if_r`, the registry port's latch); one interface, or an index past the last, reads interface 0's | Milan v1.2 5.6.3 (one advertise machine per interface) |
| tb/aecp_cmds/aecp_cmds_wrap.sv:254, tb/aecp_cmds/decode.json | the engine's new input tied to 0 in the command bench; its input digests re-recorded through `make record` | |
| docs/architecture/04_adp_engine.md:135-144, docs/architecture/06_aecp_engine.md:318-331 and 602-605, docs/00_MILAN_COMPLIANCE_REVIEW.md:399 (REQ-ADP-011) | the rule and where it is served | Table 7-2, 6.2.2.15 |
| tb/pp_top/README.md:2749 (section AI), 3487 (IF4), 1397 and 1495 (the AI arms); tb/adp_engine/README.md:32, 263, 322-329, 390-394 | the suite records | |
| tb/pp_top/aecp_dispatch_mutations/rdc-base-no-overlay.patch, tb/pp_top/ctr_mutations/store-link-detector-resets-up.patch | re-anchored on the head's context (the `rdent_r` line and the harness reset line moved them); the mutation is identical (the same removed and inserted lines). All 507 tracked patches apply at the head | |

## New checks, each with its planted mutant and failing words

Every read is graded whole: the expected response is built from the image's ENTITY descriptor with the expected
index written at octet 36, so every other octet is held to the image's (acceptance item 3).

| Check (file:line) | What it grades | Mutant (arm) | Failing words (count) |
|---|---|---|---|
| tb/pp_top/avail_index_phases.hpp AI1 to AI4 (section AI, `make avail-index`) | READ_DESCRIPTOR(ENTITY) before any ADPDU (0), after each of four ENTITY_AVAILABLE (0, 1, 2, 3, each frame byte-exact), after ENTITY_DEPARTING (which carries 4) (0), after re-enable (0, then 1) | `ai-entity-image-copy` (E_RDESCENT copies the image whole: the constant, the defect itself) | `AI2: READ_DESCRIPTOR(ENTITY) after that ENTITY_AVAILABLE carries available_index 1` (4: AI2 at 1, 2, 3, AI4 at 1) |
| same | same | `ai-gather-constant` (the engine's gather answers 0: the constant) | the same words (4) |
| same | same | `last-index-is-next-top` (ADP serves the next frame's index `aidx_r`) | `AI2: READ_DESCRIPTOR(ENTITY) after that ENTITY_AVAILABLE carries available_index 0` (6: AI2 x4, AI4 x2) |
| same | same | `last-index-kept-after-departing-top` (the last index not cleared by ENTITY_DEPARTING) | `AI3: READ_DESCRIPTOR(ENTITY) after ENTITY_DEPARTING` (1) |
| tb/pp_top/interface_phases.hpp:284-323 IF4 (`make interfaces`) | with two interfaces and interface 1's index run ahead, one read per interface carries that interface's last index | `if-top-aidx-interface-0` (the top serves interface 0's to either interface) | `IF4: READ_DESCRIPTOR(ENTITY) on each interface` (1) |
| tb/adp_engine/sim_main.cpp:760-764 P2, 795-797 P3.1-3, 919-923 P7, 940-943 P7 restart | `last_avail_index_o` is the frame's own index (0 after the first, k after frame k), 0 after DEPARTING, 0 after the restart advert while the next index is 1 | `last-index-is-next` | `P2 last ENTITY_AVAILABLE's available_index` (5) |
| same | same | `last-index-kept-after-departing` | `P7 last ENTITY_AVAILABLE's available_index 0 after DEPARTING` (1) |
| tb/adp_engine/sim_if2.cpp:373 IF4 (`make interfaces`) | each interface's last index is its own last frame's | `last-index-is-next` against the two-interface build (a one-off measurement in a scratch copy, receipts/engine-if; the campaign runs this arm on the default build) | `IF4: each interface's frames carry its own available_index, ... and each interface's last available_index is its own last frame's (3 and 3 frames; next indices 3 and 3, last 3 and 3)` (1 of 11; control 11 checks, 0 failures) |
| tb/adp_engine/sim_if2.cpp:495 IF9 (`make interfaces`) | after disable both last indices are 0 | `last-index-kept-after-departing`, the same one-off measurement | `IF9: disabling the entity sends one ENTITY_DEPARTING per interface, ... and both indices, next and last, return to 0 (1 and 1 frames)` (1 of 11) |

The two constant-serving arms are the issue's "planted mutant that serves the constant" (acceptance item 2): both
are KILLED in the dispatch campaign at 794f844 (`ai-entity-image-copy: rc=2 failures=4 named=1 KILLED`,
`ai-gather-constant: rc=2 failures=4 named=1 KILLED`, `108 checks: 108 PASS, 0 FAIL`).
The other sections that compare READ_DESCRIPTOR(ENTITY) with the image (A1, A10, N5b, M7, B4, B4b, B7, B11, K7, U7,
G8) take octet 36 from the bench's own wire oracle (`H::adp_last_aidx`, tb/pp_top/sim_main.cpp:855, filled from
each captured ADPDU at 1745, reset at 2169; `H::served_entity` at 859), never from the DUT.

## ADP timing and the image's other fields (acceptance item 3)

- ADP: the only RTL change is a register written from signals ADP already had and read only by the new port; the
  builder, the timers and the TX path are untouched. The ADP suite's timing checks (P1 to P12, the walk, IF1 to
  IF9) pass unchanged at the head, and the twin's capture diff (below) shows the fabric's 195 frames identical in
  time and bytes at base and head except the one READ_DESCRIPTOR(ENTITY) response's octet 36..39.
- Image: section AI and IF4 grade every other octet of the descriptor against the image; the twin's diff confines
  the byte difference to descriptor octets 36..39.

## Area (the processor's yosys flow: sv2v of hdl/, the generated ROMs, synth_xilinx -family xc7 -flatten)

At base 044cb25f and at the head's RTL (43149fb; 794f844 changed only two test patches, so the synthesized inputs
are the same: all.v, ucode.hex and ltn_rom.hex digests in receipts/area/head/out/inputs.sha256).

| run | LUT1-6 base | head | INV base | head | FF base | head | MUXF7/8 base | head | RAM, CARRY4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| protocol_processor_top 2x2 | 42028 | 41954 (-74) | 13934 | 13648 | 20820 | 20853 (+33) | 353 | 406 | unchanged (986, 2157) |
| protocol_processor_top 8x8 | 65192 | 65634 (+442) | 16273 | 16001 | 29891 | 29924 (+33) | 597 | 888 | unchanged (1060, 2481) |
| KL_adp_engine | 1470 | 1619 | 435 | 440 | 513 | 545 (+32) | 396 | 412 | unchanged |
| KL_aecp_engine | 10019 | 10256 | 2293 | 2218 | 4662 | 4663 (+1) | 2598 | 2693 | unchanged |

+33 FF at the top is the one 32-bit last index (one interface) and `rdent_r`. The LUT moves are synthesis noise of
the flattened top around the new mux (2x2 drops 74, 8x8 adds 442, 0.7 %).

## Gate table, processor at 794f844 (clean clone at the head; receipts/proc)

Every gate the change touches, run in order by `tools/proc-gates.sh` on a clean clone at 794f844 (0 uncommitted
entries before and after), CI's pinned Verilator 5.050 and sv2v v0.0.12, none piped. The gates that ended rc 0
before the 10:34 reboot were kept (`resume.txt`); `aecp_mutants` was killed by the reboot and re-run from the
start with every later gate. The sweep and its traceability half were re-run unpiped at 17:52 (below).

| Gate | Command (in the clone; campaigns in tb/pp_top unless named) | rc | min | Result |
|---|---|---:|---:|---|
| make_check | `make check` | 0 | 0.9 | `figures: 3 draw.io, 18 WaveDrom, 5 hand-authored, OK` |
| lint_hdl | `bash scripts/lint_hdl.sh` | 0 | 0.3 | `LINT OK  protocol_processor_top` |
| gen_matrix_check | `python3 scripts/gen_matrix.py --check` | 0 | 0.0 | `matrix: OK (94 rows, 0 untested)` |
| diff_check | `git diff --check 044cb25f HEAD` | 0 | 0.0 | no whitespace errors |
| run_suites | `env MAKEFLAGS=-j8 REQ_TAG_LOG=req-tags.txt bash scripts/run_suites.sh` | 0 | 31.6 | `suites: 1032052 checks total, 0 failing`; 39 suites PASS, pp_top 11082, adp_engine 1365, aecp_cmds 181 |
| check_req_tags_exec | `python3 scripts/check-req-tags.py --suites run_suites.log --evidence req-tags.txt` | 0 | 0.0 | `req-tags: 115 REQ rows: 101 traced, 8 waived, 6 need no check; 270 tags in 21 files, OK`; `req-tags executed: 270 evidence lines, 14 suites, OK` |
| aecp_dispatch_mutants | `python3 aecp_dispatch_mutants.py --jobs 8` | 0 | 55.6 | `108 checks: 108 PASS, 0 FAIL` (controls incl. `avail-index`: `AI: 16 checks, 0 failures`; `ai-entity-image-copy`, `ai-gather-constant`, re-anchored `rdc-base-no-overlay` KILLED) |
| aecp_mutants | `make aecp-mutants` | 0 | 27.3 | `67 checks: 67 PASS, 0 FAIL` |
| aecp_cmds_mutants | `make mutants` (tb/aecp_cmds) | 0 | 8.3 | `17 of 17 detected by their named failures; golden and restored PASS` |
| adp_mutants | `python3 mutants.py --jobs 8` (tb/adp_engine) | 0 | 11.3 | `68 checks: 68 PASS, 0 FAIL`: 6 controls PASS, 62 arms KILLED, incl. the five new ones |
| ctr_mutants | `make ctr-mutants` | 0 | 7.7 | `18 checks: 18 PASS, 0 FAIL` (re-anchored `store-link-detector-resets-up` KILLED, 11 failures) |
| acmp_mutants | `python3 acmp_mutants.py --jobs 8` | 0 | 51.7 | `103 of 103 KILLED by their named checks; goldens PASS` |
| d3_mutants | `python3 d3_mutants.py --jobs 8` | 0 | 145.1 | `110 of 110 KILLED by their named checks; goldens PASS` |
| gsi_mutants | `python3 gsi_mutants.py` | 0 | 17.6 | `30 detected by named checks; golden and restored PASS` |
| notify_mutants | `python3 notify_mutants.py --jobs 8` | 0 | 50.9 | `137 of 137 KILLED by their named checks; goldens PASS` |
| name_wr_mutant | `python3 name_wr_mutant.py` | 0 | 2.4 | `decode killed; golden and restored PASS` |
| maap_mutants | `make mutants` (tb/maap) | 0 | 2.9 | `32 checks: 32 PASS, 0 FAIL` |
| srp_top_mutants | `make mutants` (tb/srp_top, the CI-listed SRP campaign) | 0 | 59.2 | `314 checks: 314 PASS, 0 FAIL` |
| portability | `./syn/yosys/run.sh`, then `python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4` | 0 | 3.8 | `YOSYS XILINX OK` (rc 0); `elab guards: 93 checks: 93 PASS, 0 FAIL` (rc 0) |

The processor's suite sweep (`scripts/run_suites.sh`) has no shard option, and the shard runner drives a
`scripts/run_all_suites.sh --shard` sweep the processor does not have, so the sweep ran serially in this lane's
own unit (MAKEFLAGS=-j8).

## Scratch parent consumer gate table (milan-fpga dev ac0a01e3, protocol-processor pinned at 794f844)

A clone of the trusted dev checkout (ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36) in scratch, local branch
`pp217-consumer-gate`, never pushed (its only remote is the local trusted checkout). Four local commits: the pin
and digests at 43149fb (4f5527255b, a5313026c5), then `ebf807fcc5 Pin protocol-processor at 794f844 (processor
issue #217), scratch consumer gate` and `d2267f2608 Record the ROM content digests at protocol-processor 794f844,
scratch consumer gate` (the digests written by the parent's recorder, `syn/yosys/ooc.sh --record-rom-digests`). Gitlink `protocol-processor` =
794f8442c3d9da158c99d358d825c7b277516bba; 0 uncommitted entries. The commands are rtl-fast's run steps
(`tools/parent-gates.sh`) with CI's pinned Verilator 5.050, sv2v v0.0.12, GoogleTest 1.14.0 and a CPython 3.12.3
venv of the parent's ci/constraints-ci.txt, CI_CAMPAIGN_JOBS 4. Gates rc 0 before the reboot were kept; `fw_shard0`
was killed by it and re-run. `ci_scope_classify` first ran as `git diff | tee | ci_scope.py`; it was re-run in
CI's own form (the list written to a file, then `ci_scope.py < file`), the piped record kept apart.

| Gate (rtl-fast job) | Command | rc | min | Result |
|---|---|---:|---:|---|
| rom_digests (recorder) | `./syn/yosys/ooc.sh --record-rom-digests` | 0 | 0.0 | `recorded ROM content digests for protocol-processor pin 794f8442...` |
| ci_scope_selftest (changes) | `python3 scripts/ci_scope.py --selftest` | 0 | 0.5 | `selftest: PASS` |
| ci_changed_files (changes) | `git diff --no-renames --name-only ac0a01e3 HEAD` | 0 | 0.0 | `protocol-processor`, `syn/yosys/rom_digests.tsv` |
| ci_scope_classify (changes) | `python3 scripts/ci_scope.py < changed-files` | 0 | 0.0 | `true` (RTL relevant: every fast gate runs) |
| lint_rtl (verilator-lint) | `python3 scripts/lint_rtl.py --check --self-test --jobs 4` | 0 | 0.2 | `LINT GATE: PASS (89 violation(s) <= ratchet 89; ...)` |
| pp_srcs (verilator-lint) | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0.0 | rc 0 |
| behave (bdd-conformance) | `behave --no-capture -f plain` (in tests/) | 0 | 0.1 | rc 0 |
| yosys_elaborate (yosys-elaboration) | `syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow` | 0 | 6.6 | rc 0 |
| ooc_read_sets (yosys-elaboration) | the step's ten commands (`dp_srcs.py --selftest` ... `pp_resource_gate.py check-baseline` ...) | 0 | 27.9 | `baseline PASS: 3 endpoints` |
| ooc_selftest (yosys-elaboration) | `python3 syn/yosys/ooc_selftest.py` | 0 | 1.7 | `75 arm(s) passed` |
| guard_selftest (yosys-elaboration) | `python3 syn/yosys/guard_selftest.py` | 0 | 1.6 | `36 controls passed` |
| cache_selftest (yosys-elaboration) | `python3 syn/yosys/cache_selftest.py` | 0 | 2.9 | `cache selftest: OK` |
| publication_census | `python3 sw/mailbox/publication_census.py --check --selftest --jobs 4` | 0 | 31.1 | `mutations: 0 of 31 rule(s) no arm proves` |
| fw_tally_selftest (firmware-unit) | `python3 sw/firmware/gtest/tally_selftest.py` | 0 | 0.1 | `18 of 18 planted cases read as planted` |
| fw_rv32_sdk_selftest (firmware-unit) | `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | 0.0 | `OK` |
| fw_rv32_selftest (firmware-unit) | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | 0.2 | `17 checks PASS` |
| fw_shard0 (firmware-unit: the suites phase, incl. the ADP arm, the ADP walk cut from the processor's tb/adp_engine, and the AECP arms) | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4` | 0 | 7.0 | `test_ctrl_firmware: PASS` |
| fw_ctrl_nvm (firmware-unit) | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | 2.5 | `OK across 5 shape(s), 435 tests` |
| fw_coverage_selftest, fw_coverage (firmware-unit) | `python3 sw/firmware/gtest/fw_coverage.py --selftest`; `... --check --jobs 4` | 0, 0 | 0.0, 7.3 | `29 of 29 planted`; `firmware coverage: PASS (30 files)` |
| fw_shard1 (firmware-control-mutants) | `... test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 1/4` | 0 | 35.5 | `mutants: 523 of 523 caught`, `test_ctrl_firmware: PASS` |
| fw_shard2 (firmware-aecp-mutants: the AECP campaign) | `... --shard 2/4` | 0 | 4.7 | 78 arms `[ok]`, `test_ctrl_firmware: PASS` |
| fw_shard3_srp (firmware-srp-mutants) | `... --shard 3/4` | 0 | 21.7 | `test_ctrl_firmware: PASS` |
| fw_boundary (firmware-boundary) | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator` | 0 | 35.5 | `ctrl_boundary: PASS` |
| fw_verilator (firmware-verilator) | `... ctrl_boundary.py --require-rv32 --selftest --only verilator` | 0 | 33.4 | `ctrl_boundary: PASS` |
| milan_dp (the AECP and ADP datapath bench) | `make -C tb/verilator/milan_dp SIM_JOBS=2` | 0 | 47.7 | 19 x `RESULT: PASS`, 0 `FAIL` lines; log 1,429,000 B (sha256 in receipts) |
| pp_shadow (extra: builds the processor) | `make -C tb/verilator/pp_shadow` | 0 | 24.0 | `RESULT: PASS` |
| nvm_cosim (extra: AECP saved state) | `make -C tb/verilator/nvm_cosim` | 0 | 20.4 | `RESULT: PASS` |
| milan_dp_mclk (extra) | `make -C tb/verilator/milan_dp_mclk` | 0 | 47.1 | `34 checks: 34 PASS, 0 FAIL` |
| capture_coherence (extra) | `make -C tb/verilator/capture_coherence` | 0 | 163 (incl. a 142 min pause, below) | `42 checks: 42 PASS, 0 FAIL` |
| milan_dp_render (extra) | `make -C tb/verilator/milan_dp_render` | 0 | 15.2 | both clean legs, then `5 checks: 5 PASS, 0 FAIL (--leg-defects ...)` |

rtl-fast's aggregate job only requires the jobs above; every one is rc 0. The full-RTL workflow's union jobs gather
pieces of the sharded native sweep, which this assignment does not ask for; the five benches marked extra build
the processor inside the datapath and were run whole instead.

## Two-placement simulation (milan-fpga #665 lane S6b, `make -C tb/verilator/milan_dp twin`)

Read only on the lane (a88772f1, 0 uncommitted entries); run on scratch copies with one local pin commit each.

- Head (protocol-processor 794f844): the owed row reports

      [DIFF] owed row entity-available-index: the difference has gone, both halves send [READ_DESCRIPTOR to the first controller status 0 ...]; the lane that fixed it (#858 (a release-image defect)) deletes the row

  The row `entity-available-index` is in the twin's `OWED` list (a difference between the halves), whose vanished
  form the twin words "the difference has gone" (its own arm `vanished-available-index` expects exactly these
  words); "the defect has gone" is the wording of its `OWED_GRADES` rows (the #857 and #860 ones). It is the row
  for this defect and it reports that the defect is gone.
- Base control (protocol-processor 044cb25f): the row holds: `[OWED] entity-available-index: the fabric sends the
  ENTITY descriptor with available_index 0 after the ENTITY_AVAILABLE that carried 1, the split ... 1`.
- Findings: base 3, head 4. The added one is the vanished row above (by the twin's design a finding: the lane that
  fixes it deletes the row in milan-fpga). The other three are identical at base and head: two `[MRP]` MVRP VID 2
  JoinIn findings and `owed row fabric-vid2-join-in does not hold`, all the all-fabric MVRP's (the twin's rows owe
  them to milan-fpga #857 and #860; MRP is not touched here). The twin exits rc 2 at both because findings are
  present; it is the measurement the assignment names, not a gate of this change.
- Capture diff (receipts/twin/capture_diff.txt): fabric 195 frames at both, one difference: frame 59 at 7501 ms,
  wire byte 81, inside descriptor octets 36..39, base 0, head 1. Split 260 frames, 0 differences.

## Resume log

- 07:2x: the final AECP dispatch campaign at 43149fb ended rc 1: the existing arm `rdc-base-no-overlay` no longer
  applied, because the E_RDESCENT re-dispatch gained the `rdent_r` line inside its context. A check of all 507
  tracked `*.patch` files found one more, `store-link-detector-resets-up` (tb/pp_top/ctr_mutations), whose context
  the new harness reset line moved. Both re-anchored in 794f844 with the identical mutation; every patch applies.
- 08:09: scratch parent re-pinned at 794f844, ROM digests re-recorded through `syn/yosys/ooc.sh
  --record-rom-digests`, both committed locally (never pushed). 08:20: twin at 794f844 done.
- 10:34: host reboot killed the processor's `aecp_mutants` (the gate after the dispatch campaign) and the parent's
  `fw_shard0`. Only byte-code caches had been written in the trees after 10:31. Their partial logs are kept in the
  runs' `interrupted-1034/`; both drivers restarted at 10:59 keeping every gate already rc 0 at 794f844.
- 14:59 to 15:02, memory over target: this unit's anonymous memory reached 14.4 GB (memory.current peak 16.8 GB),
  above the 10 GB it must stay under, for about three minutes. No OOM event and no process killed
  (memory.events: oom 0, oom_kill 0); the governor's reclaims brought it back under 8 GB by 15:02. Cause: the
  extra parent bench `milan_dp_mclk` began its full-datapath build beside the processor's D3 campaign (8 jobs).
  From 15:05 to 17:27 the extra parent chain was paused (SIGSTOP, then SIGCONT, `tools/pause_tree.sh`; its gates
  keep no host-time deadline) until the processor's campaigns ended, so no two heavy builds ran together again.
  capture_coherence's recorded duration includes that pause.
- 17:2x: two gates had been run through a pipe: the processor's sweep (`run_suites.sh | tee`, under pipefail, rc
  0) and the parent's `git diff | tee | ci_scope.py` (rc 0). Both were re-run unpiped (the sweep's stdout is now the
  gate's own log, which check-req-tags reads; the classification in CI's own file-redirect form). The piped records
  are kept in the runs' `superseded-piped/`.

## Receipts (receipts/INDEX.md, generated from the files present; host paths written as $SCRATCH, $PARENT, $OUT)

- receipts/IDENTITY.txt, receipts/STANDARDS.txt: the identities above and the clauses read.
- receipts/repro-base: section AI at the base (rc 2, 4 failures).
- receipts/proc: every processor gate at 794f844 (cmd, rc, start, end, log); `aecp-dispatch-out`, `adp-out` and
  `ctr-out` hold the controls and the arms of this issue; `interrupted-1034` the killed `aecp_mutants`;
  `superseded-piped` the first, piped, sweep.
- receipts/engine-if: the one-off measurement of the two engine arms on the two-interface build.
- receipts/parent: every scratch-parent gate at 794f844; logs over 200 KB as sha256, size and last 60 lines.
- receipts/twin: base, head (794f844) and head-43149fb runs, findings, report.json, capture_diff.txt.
- receipts/area: base and head synthesis stats and summaries (logs as sha256 and tail).
- receipts/at-43149fb, receipts/dev, receipts/campaigns/dev: the earlier head's gates and the development runs,
  kept as history; nothing above cites them as the head's.
- tools/: the scripts that ran the gates (gate scripts, collector, index, gate table, pause helper).
