# Lane 190 round 2 (processor #190, per-source TSpec MaxFrameSize) — HANDOFF, author [A654]

**Status: DONE, REVIEW READY.** One commit on processor main, not pushed, no PR opened.

- Repository: processor, branch `190-per-source-tspec`, base main `5addf29759a22372ed6aa3e1d52a3aad29e3ecd7`
  (origin/main was still this commit when fetched).
- Head: `90321bffbf48a271e9862cad92973bd862827d5f`, "Take the engine-driven DECLARE_TALKER's TSpec
  MaxFrameSize per source (#190)". The lane is clean: no untracked or ignored files.
- Assignment: issue #190 ruling comment 6256563927, PART 1 only. The ruling approves this one top-level port
  change; no other port, parameter or register-map change is made.
- TAKEN: comment 6256580298 (`receipts/r10-taken-comment.md`). REVIEW READY: see section 8.
- Round 1 (the milan-fpga STOP) is kept unchanged under `round1/`.

## 1. Changes (file:line at the head)

| File:line | Change |
|---|---|
| `hdl/top/protocol_processor_top.sv:300-303` | `cfg_tspec_max_frame_i` is `[N_STREAM_OUT_P*16-1:0]`, flat `[16*s +: 16]` like `cfg_stream_id_i` (was `[15:0]`) |
| `hdl/top/protocol_processor_top.sv:2703` | the talker stage `st_tk_r` captures `cfg_tspec_max_frame_i[32'(tkr_gate_src_w) * 16 +: 16]`, the slot of the source whose gate opened or closed (was the one scalar) |
| `tb/pp_top/pp_top_wrap.sv:79` | the wrap's port is `[8*16-1:0]` (the wrap runs the top's default eight sources) |
| `tb/pp_top/sim_main.cpp:1495-1500` | `H::set_tspec(s, mfs)` writes slot `s` |
| `tb/pp_top/sim_main.cpp:2061` | the main model drives 1024 on every slot, the old scalar's value, so no existing check moves |
| `tb/pp_top/sim_main.cpp:11362-11471` | section TS: `TspecPhase` (fresh model) and `run_tspec` |
| `tb/pp_top/sim_main.cpp:14575, 14583, 14607` | `--tspec-only`; the full run runs TS last |
| `tb/pp_top/Makefile:89-92, 249` | target `tspec` (section TS alone) |
| `tb/pp_top/acmp_mutants.py:16-20, 326-344, 346` | docstring; the issue #190 group (`PP_TOP_TS`, `TS_SLOT`, three arms) in `MUTANTS`; `TS` in the tally pattern |
| `tb/pp_top/README.md:2174-2212` | section TS and its control table |
| `docs/architecture/02_interfaces.md:255, 277-283` | anchor `sec-02-srp` on §4.1; the tspec is per source, with the port and its packing |
| `docs/architecture/10_srp_engine.md:137-139` | each source declares its own slot |
| `docs/architecture/09_verification.md:778-789` | §8.12, the property, its checks and its controls |
| `docs/guides/integrator.md:270, 327-339` | the SRP row's width; four per-source vectors; what to drive in each slot |

The service path (`svc_max_frame_i`) was already per request, and the SRP core already stores the TSpec per
source (`KL_srp_top.sv:844,910`), so nothing else changes. The ROMs are byte-identical at base and head
(`receipts/r13-repo-state.txt`).

## 2. Accepted values and refusal cases

- The port accepts any 16-bit value in each slot. Source *s*'s engine-driven DECLARE_TALKER (gate open and gate
  close) carries slot *s* unchanged into the SRP request. Nothing at the port is range-checked or refused, as
  with the old scalar.
- The values are the integrator's: Milan v1.2 4.3.3.2 Table 4.4 per format (AAF PCM32 48 kHz 24·N + 24 + 1,
  CRF 1 ts/pdu 28 + 1). IEEE 802.1Q-2018 35.2.2.8.4 a): the largest frame the talker produces for the stream.
- The only refusal downstream is unchanged: the Σ-slope admission round refuses a source whose slope does not
  fit 75 % of the port rate, and that source declares Talker Failed with the same TSpec. Section TS exercises it:
  sources 0 to 6 take 74.368 of 75 Mb/s, and source 7 (193) is refused and declares Talker Failed carrying 193.
  This was measured with a temporary debug print, removed before the commit.
- Seen on the wire in TS at the head (first Talker attribute per source, NumberOfValues 1 each, because the
  values differ): 217, 29, 73, 97, 121, 145, 169 as Talker Advertise, and 193 as Talker Failed.

## 3. New checks, planted arms, failing words

Section TS (`tb/pp_top`, 9 checks, fresh model; slots: source 0 = 217 (AAF 8 ch), source 1 = 29 (CRF), sources
2-7 = 24·s + 25):

- `TS0: AECP is released and every source's PROBE_TX_RESPONSE is SUCCESS (mask 0x..)`
- `TS1: source <s> declares its own slot's MaxFrameSize <v> (got <g>)`, for s = 0..7, range-matched per
  802.1Q-2018 35.2.2.8 (FirstValue + k steps the Unique ID and DA, carries the TSpec unchanged).

Arms in `tb/pp_top/acmp_mutants.py` (exact edits in an extract; KILLED only if the run completes, exits non-zero
and the named check fails). Head campaign run, `receipts/r14-ts-arms-head.json`:

| Arm | Edit at `protocol_processor_top.sv` | Named check (must fail) | Failing words in the run |
|---|---|---|---|
| `tspec_slot_zero` | `mfs: cfg_tspec_max_frame_i[15:0],` | `TS1: source 1 declares its own slot's MaxFrameSize` | `FAIL: TS1: source 1 declares its own slot's MaxFrameSize 29 (got 217)` and sources 2-7 the same (got 217): 7 of 9 |
| `tspec_slot_last` | `mfs: cfg_tspec_max_frame_i[N_STREAM_OUT_P*16-16 +: 16],` | `TS1: source 0 declares its own slot's MaxFrameSize` | `FAIL: TS1: source 0 declares its own slot's MaxFrameSize 217 (got 193)` and sources 1-6 the same (got 193): 7 of 9 |
| `tspec_no_allocator` | `: maap_req_ready_i;` → `: 1'b0;` (talker MAAP request face never ready) | `TS0: AECP is released and every source's PROBE_TX_RESPONSE is SUCCESS` | `FAIL: TS0: ... SUCCESS (mask 0x00)` and every TS1 (got -1): 9 of 9 |

Golden `golden-pp_top--tspec-only`: PASS. Every one of the 9 TS checks fails under at least one arm.

## 4. Base and head records

Base `5addf297` and head `90321bff`. Base run_suites and the base campaigns ran from the scratch parent's
submodule checked out at 5addf297. Base lint, make check, matrix and Yosys ran in the lane before any edit. Head
runs were all in the lane. Each `.rc` is the command's own exit status, written by a wrapper, never through a
pipe. Records are in `receipts/records/` (sanitized copies; host roots replaced by tokens), with sha256 and size
of every scratch record in `EXTERNAL-RECORDS.csv`. Base vs head diffs are `*.cmp.diff` (paths, times and order
normalized).

| Processor gate | Base | Head | Identical? |
|---|---|---|---|
| `scripts/run_suites.sh` | rc 0, 1,030,013 checks, 0 failing | rc 0, 1,030,022 | only `pp_top` 10,519 → 10,528 (TS0 + 8 × TS1) |
| `scripts/lint_hdl.sh` | rc 0, 41 LINT OK | rc 0, 41 | yes |
| `make check` | rc 0 | rc 0 | yes except `links: 1196` → `1200 checked` (the four links added) |
| `scripts/gen_matrix.py --check` | rc 0, 94 rows, 0 untested | rc 0 | yes |
| `syn/yosys/run.sh` (Yosys 0.33, sv2v 0.0.12) | rc 0, 42 tops + Xilinx engine OK | rc 0 | yes (times normalized) |

| Campaign (builds the top or `tb/pp_top`) | Base | Head | Identical? |
|---|---|---|---|
| `tb/pp_top/acmp_mutants.py --jobs 4` | rc 0, 51 of 51 KILLED | rc 0, 54 of 54 | only + golden `--tspec-only` and the three `tspec_*` arms |
| `make -C tb/pp_top aecp-mutants` | rc 0, 61 KILLED | rc 0, 61 | yes |
| `make -C tb/pp_top aecp-dispatch-mutants` | rc 0, 54 KILLED | rc 0, 54 | yes |
| `make -C tb/pp_top ctr-mutants` | rc 0, 17 KILLED | rc 0, 17 | yes |
| `tb/pp_top/gsi_mutants.py` | rc 0, 20 detected | rc 0, 20 | yes |
| `tb/pp_top/name_wr_mutant.py` | rc 0, killed | rc 0, killed | yes |
| `tb/pp_top/notify_mutants.py --jobs 4` | rc 0, 109 of 109 | rc 0, 109 of 109 | yes |
| `tb/pp_top/d3_mutants.py --jobs 4` | rc 0, 110 of 110 | rc 0, 110 of 110 | yes |
| `make -C tb/adp_engine mutants` | rc 0, 57 KILLED | rc 0, 57 | yes |
| `make -C tb/maap mutants` | rc 0, 29 KILLED | rc 0, 29 | yes |
| `make -C tb/name_state mutants` | rc 0, 16 KILLED | rc 0, 16 | yes |
| `make -C tb/elab_guards mutants` | rc 0, 160 of 160 | rc 0, 160 of 160 | yes after normalizing `protocol_processor_top.sv:N` (+3) |
| `tb/elab_guards/guards.py --frontend yosys --jobs 4` | rc 0, 93 of 93 | rc 0, 93 | yes after the same line normalization |

Not run (they build no changed file): `tb/srp_top`, `tb/srp_admission`, `tb/aecp_cmds` mutants,
`tb/acmp_talker` retry mutants, `tb/nvm_port` figures. No Vivado run of the processor, and no hardware.

Run notes (all set aside under `receipts/records/**/void/`, none used as a record):

- The first base sweep was started detached and a second one as a unit in the same tree. They collided in
  `tb/pp_top`'s obj_dir (`FAIL: 14 build tallies, expected 7` in one). Both were discarded, and the base sweep
  was rerun alone in the scratch submodule at 5addf297. That clean record has the same suite lines as the
  collided detached one.
- Base `elab_guards` and `name_state` campaigns first refused a pre-created output directory (rc 2 at 0 s).
  They were rerun with the directory left to the campaign.
- The first base `behave` had no `behave` on the unit's PATH (rc 127). It was rerun.

## 5. Scratch-parent consumer gate table

Scratch parent: kebag-logic/milan-fpga dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f` (its own pin 2cbed0a9),
every submodule initialised. The protocol-processor gitlink was staged (never committed or pushed) at 5addf297,
then at 90321bff fetched from the lane. Every git command in the submodule was preceded by a top-level
identity check. `receipts/records/cons/{base,head}/STATE.txt` records each state. Working-tree patches:

- base: `pp178-a634/parent-evidence-classification.patch` (sha256 76625170…495e) and
  `pp176-a629/parent-adoption-milan_dp-67.patch` (e142e2e7…66d3); diff sha256 `ef322a60…2dac`.
- head: the same two plus `parent-scratch-tspec-every-slot.patch` (this directory, sha256 37d1b76e…34a8), which
  drives the new port with the old scalar on every slot: `.cfg_tspec_max_frame_i({N_STREAM_OUT_P{cfg_tspec_max_frame_i}})`
  at `hdl/milan/KL_pp_shadow.sv:1161` (the brief's `hdl/common/KL_pp_shadow.sv` is this file; the parent has
  no `hdl/common/KL_pp_shadow.sv`). Diff sha256 `278f0632…8f23`.

Tools: Verilator 5.050, sv2v 0.0.12, Yosys 0.66 (the parent's `YOSYS_VERSION`), Vivado xvlog only under
`flock $VIVADO_LOCK` (exclusive).

| Parent consumer gate | Base 5addf297 | Head 90321bff | Base vs head |
|---|---|---|---|
| `check_cpp_idiom.py` | 0 | 0 | identical |
| `check_py_idiom.py` | 0 | 0 | only the line total 258,851 → 258,871 (+20, `acmp_mutants.py`) |
| `check_rtl_source_lists.py` | 0 | 0 | identical |
| `pp_srcs.py --check --selftest` | 0 | 0 | identical |
| `check_port_contracts.py` | 0 | 0 | identical |
| `measure_naming.py --check` | 0 | 0 | identical |
| `measure_test_evidence.py --check` | 0 | 0 | identical |
| `docs_check.py` | 0 | 0 | identical |
| `check_sh_idiom.py` | 0 | 0 | identical |
| `check_hygiene.py --check` | 0 | 0 | identical |
| `check_sv_idiom.py` | 0 | 0 | identical |
| `check_submodule_docs.py` | 1 | 1 | identical: `protocol-processor: documented pin differs from Git` and the stale submodule diagram; it fails for any gitlink the parent's docs do not record, so the adoption owns it |
| `check_baremetal_only.py --check` | 0 | 0 | identical |
| `check_soc_sources.py` | 0 | 0 | identical |
| `check_todo_ownership.py` | 0 | 0 | identical |
| `lint_rtl.py --check` | 0 | 0 | identical |
| `behave --no-capture -f plain` (tests/) | 0 | 0 | identical: 14 features, 406 scenarios, 1,977 steps |
| `flock $VIVADO_LOCK xvlog_gate.py --check` | 0 | 0 | identical except the line naming the pin; 0 findings |
| `sw/builder/test_builder.py` | 0 | 0 | `ALL GATES PASS EXCEPT 1 NOT RUN` at both (gate 11 needs a build tree not on this host); 266 gate lines, differing only in timings |
| `make -j16 -C tb/verilator/pp_shadow` | 0 | 0 | 609 + 609 + 649 + 317 = 2,184 checks, 0 failures at both (four binaries interleave their output) |
| `make -j16 -C tb/verilator/nvm_cosim lint` | 0 | 0 | identical |
| `make -j16 -C tb/verilator/nvm_cosim quick JOBS=4 POOL=2` | 0 | 0 | identical |
| `make -j16 -C tb/verilator/milan_dp_render` | 0 | 0 | check lines identical (5 of 5) |
| `make -j16 -C tb/verilator/milan_dp SIM_JOBS=2` | 0 | 0 | every check line identical: 10,465 `[ok]`, 1,127 `[PASS]`, 0 `[FAIL]` |

23 of 24 are rc 0 at both; `check_submodule_docs` fails identically at both.

Control (head, without the every-slot patch; `records/cons/head-nopatch/`): `lint_rtl.py --check` rc 1,
`NEW hdl/milan/KL_pp_shadow.sv:1161:8: WIDTHEXPAND Input port connection 'cfg_tspec_max_frame_i' expects 128
bits ... generates 16 bits` (`LINT REGRESSION: hdl/milan has 3 violation(s), ratchet allows 2`).
`check_port_contracts` and `check_sv_idiom` rc 0. The patch was re-applied afterwards; the parent ends at
diff `278f0632…` with the gitlink staged at 90321bff.

## 6. Scope decisions to confirm

- The session brief's scope line ("any change outside E_SCFG, its tests, generators ... STOP") and its
  "Closes #179" item are from issue #179's template. #179 (SET_CONFIGURATION, closed) is unrelated to #190.
  The brief lifts the STOP rule for exactly this port and points at `protocol_processor_top.sv:2700`. So I read
  the scope as #190 part 1: the port, its capture, its tests and the docs that record it. Nothing in E_SCFG or
  any generator changed. PR-BODY.md therefore has neither "Closes #179" nor "Refs #179".
- "Closes #190" is not used. The issue's first "Done when" item (the CRF stream declaring 29) needs part 2 in
  the parent. PR-BODY.md says "Refs #190".
- The brief's reading list (gen_ucode.py, OP_*_C, check_upc_map.py, the ROM generators) belongs to that
  template too. Their relevance here is that nothing they generate moved: both ROM digests are equal at base and
  head, and the uPC map gate passes.

## 7. Part 2, for the adoption lane (not done here)

Drive the CRF slot (`CRF_TUID_C = N_STREAM_OUT_P` in the parent) with 20 + 8 × timestamps_per_pdu + 1 from the
`KL_crf_tx` constants, and the AAF slots with `tctx_maxf_w[s]` as today. Pin it with a suite case against the
PDU length and a planted mutant. Correct the stale comment at `KL_crf_tx.sv:206-211`. Drop the every-slot patch,
which is scratch only. Record the new pin for `check_submodule_docs`.

## 8. Public trail

- TAKEN: issue #190 comment 6256580298.
- REVIEW READY: issue #190 comment 6258817891 (`receipts/r15-review-ready-comment.md`), head 90321bff.
- No push, no PR, no edit of any existing comment.

## 9. Receipts

See `INDEX.md`, generated from the files present. Tool identities: `receipts/r11-tool-identities.txt`.
