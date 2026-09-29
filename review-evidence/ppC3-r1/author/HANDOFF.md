# HANDOFF: [A446] lane C3 (ADP), issues #40, #41, #85

Status: DONE, REVIEW READY at head `9185c491b56358d6bc15b5069b612bfaa95316f3` (local branch; no push, per the lane rules)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Branch: `c3-adp-coverage`, base `main` `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`, 5 commits
- Assignment: issue #40 comment 5888002660
- TAKEN posted: issue #40 comment 5888014169
- PR body: `PR-BODY.md` (this directory); the PR is not created here
- REVIEW READY posted: issue #40 comment 5890780739 (head 9185c49)
- Parent: milan-fpga dev `9e3ccbfb` (read-only trusted checkout, untouched; gates in a scratch copy)
- Tools: Verilator 5.050 (the CI pin), yosys 0.66, sv2v 0.0.13

## Commits (on c951a9ff; one-line subjects, no body, no trailers)

| Commit | Item |
|---|---|
| `cfb7bbb` | 1. #40: overlay-fed current_configuration_index, sampled at build; unit P11, top AD1-AD4; campaign + 8 arms |
| `ee69db2` | 2. #41: boot gate over the full T-ADP-DELAY span; unit P12, top AD0, S3 pre-flush; 2 arms |
| `4a895f2` | 3. #85: MTXW walk of F04.2 (45 cells) and F04.3 (33 cells, 8 arcs); 17 arms |
| `e8ec039` | `.gitattributes`: ADP patch files' blank context lines exempt from whitespace checks (as srp_top's) |
| `9185c49` | consumer C++/Python idiom rules (array initializers, a split function, a docstring) |

## Item 1. #40 ADPDU invariance across SET_CONFIGURATION (REQ-ADP-005)

Clauses: Milan v1.2 §5.6.2 note; IEEE 1722.1-2021 §6.2.2.18; §7.4.8.2.

- Acceptance 3, the preferred way, NO top-level port change:
  - `hdl/top/protocol_processor_top.sv`, block just before `u_adp`:
    `adp_cur_cfg_w = aecp_cur_cfg_v_w ? aecp_cur_config_o : current_cfg_i`, into
    `u_adp.current_cfg_i`; `.dyn_cur_config_v_o (aecp_cur_cfg_v_w)` on `u_aecp`.
  - `hdl/aecp/KL_aecp_engine.sv`: new output `dyn_cur_config_v_o` (port list next to
    `dyn_cur_config_o`) driven by block `dyn_cfg_valid` (before `u_dyn`), one flop set by an
    accepted value-region write of SEL_CFG at row 0 on the store's write bus = the store's
    `cfg_v_r`. `dyn_ix_w` factors the store's `desc_index_i` expression.
  - `KL_aecp_dyn_state` ports untouched (the parent's nvm_cosim instantiates it by name).
- RTL defect fix (with failing arm): `hdl/adp/KL_adp_engine.sv` read `current_cfg_i` live while
  writing wire bytes 64..65; now `bld_cfg_r`, sampled in `B_SAMPLE`, passed to `frame_byte_f`
  as `cfg`. Clause IEEE 1722.1-2021 §6.2.2.18. Failing arm: unit P11c on the previous engine:
  `got 0104` (high byte of 0102, low byte of 0304); scratch log `a446-prefix-adp/run.log`
  (sha256 3961502b209cec43..., 4485 B).
- Tests:
  - Acceptance 2: unit P11a-e (`tb/adp_engine/sim_main.cpp`, `check_config_index_moves_only_its_own_bytes`).
  - Acceptance 1: top section AD1, AD1b, AD2, AD3, AD4 (`tb/pp_top/sim_main.cpp`,
    `AdpConfigPhase`; fresh model; image default configuration 1 via
    `load_descriptor_image(1)`; `make -C tb/pp_top adp-config`). Shipped RTL: AD2 and AD4 fail
    (scratch log `a446-prefix-pptop/run.log`, sha256 dcc5fea8562b67b4..., 23567 B).
- Acceptance 4, mutants (all KILLED; `tb/adp_engine/mutations/*.patch`, `mutants.py`):

| Arm | Suite | Failing checks |
|---|---|---|
| cfg-read-live | adp_engine | 1: P11c |
| cfg-dependent-field | adp_engine | 14: P11b first |
| cfg-dependent-field-top | pp_top adp-config | 5: AD2 first |
| cfg-frozen-at-top | pp_top adp-config | 3: AD2, AD4 |
| cfg-overlay-only | pp_top adp-config | 2: AD1, AD1b |
| cfg-nonzero-for-valid | pp_top adp-config | 2: AD2 |
| cfg-valid-not-sticky | pp_top adp-config | 3: AD2, AD4 |
| cfg-valid-any-selector | pp_top adp-config | 1: AD1b |

## Item 2. #41 pre-enable ADP quiescence over the full T-ADP-DELAY span (REQ-ADP-006)

Clauses: Milan v1.2 §5.6.1; §5.6.3.5.3 (T-ADP-DELAY 0..4 s). No RTL change.

- Acceptance 1: unit P12 (`check_the_boot_gate_holds_over_the_delay_span`, right after P0):
  4100 ms + 20 ms bounce + 4100 ms with enable low, timer service modeled end to end
  (`run_modeled_ms`); no draw request, no timer op, no frame/TX request, DOWN every clock,
  PRNG seeded.
- Acceptance 2: top AD0 (`boot_gate_holds_over_the_delay_span`): 4200 + 20 + 4200 ms, q_adp
  empty, snapshot word 31 DOWN at every 100 ms sample, flags {seeded, link, !enable}; plus
  S3's pre-flush `q_adp` check (queue read only).
- Acceptance 3, mutation record in `tb/adp_engine/README.md`:

| Arm | Suite | Failing checks |
|---|---|---|
| gate-enable-dropped | adp_engine | 30: all four P12 checks, P1-P5 displaced, walk NOT STARTED cells |
| gate-enable-dropped-top | pp_top adp-config | 3: AD0 (x2), AD1b |

  Full default pp_top under the mutant: only AD fails (3 of 7,766); S0 and S3 stay green
  (scratch log `a446-gate-full/run.log`, sha256 398f671bbb51f9a4..., 579 B).

## Item 3. #85 F04.2 advertise SM walked MTXW (GAP-16), acceptance 1-3 (item 4 open)

No RTL change (no defect found).

- Acceptance 1: unit P13 (`check_the_mtxw_walk`). Independent tables at the top of
  `tb/adp_engine/sim_main.cpp` (`ADV[9][5]`, `DISC[11][3]`, `F043_ARCS[8]`), transcribed from
  Milan v1.2 Table 5.51 + §5.6.3.5 (+§5.6.3.1 split, §5.6.1 column, both DELAY phases) and
  Table 5.54 + §5.6.4.5 (+ §5.6.4.1 unbound column, bind/unbind). F04.2: 45 cells
  (N 12, I 20, S 6, C 7), `CHECK(adv_cells == 45)`. F04.3: 33 cells (N 13, I 15, S 2, C 3),
  `CHECK(disc_cells == 33)`, arcs 8 of 8.
- Acceptance 2: DOWN x {DISCOVER, GM_CHANGE, SHUTDOWN} inert; DELAY x LINK_DOWN (cancel, no
  DEPARTING); DELAY x SHUTDOWN (DEPARTING byte-exact, index 0); both DELAY phases.
- Acceptance 3 (all KILLED by the named cell):

| Arm | Failing checks |
|---|---|
| walk-down-answers-discover (issue-named) | 16 |
| walk-delay-ignores-link-down (issue-named) | 4 |
| walk-down-answers-gm-change | 8 |
| walk-down-shutdown-departs | 1 |
| walk-delay-answers-discover | 9 |
| walk-delay-shutdown-silent | 4 |
| walk-stale-draw-arms | 4 |
| walk-departing-keeps-index | 6 |
| walk-foreign-discover-answered | 8 |
| walk-link-down-keeps-timer | 3 |
| disc-fresh-checks-gm | 3 |
| disc-not-discovered-checks-index | 14 |
| disc-not-discovered-checks-interface | 3 |
| disc-restart-not-rediscovered | 4 |
| disc-departing-ignores-interface | 3 |
| disc-stray-noadp-departs | 2 |
| disc-unbind-keeps-timer | 2 |

- Test weakness found by the campaign and fixed before commit: the draw-phase DISCOVER acted on
  the delivery edge (walk-delay-answers-discover green there); the column now enters one clock
  earlier.
- Item 4 open: README interop limit restated as open (#85 item 4).

## Item 4. Parent-visible list (as in PR-BODY.md)

1. No port or parameter change of `protocol_processor_top`, `KL_aecp_dyn_state`,
   `KL_acmp_nvm_shadow`, `KL_pp_nvm_port`, `KL_pp_nvm_mgr_arb`; `KL_aecp_engine` (internal)
   gains one output.
2. `current_cfg_i` = image-default fallback; after SET_CONFIGURATION the ADPDU follows
   `aecp_cur_config_o`. Parent (ADP_IDX0, one configuration): wire unchanged. milan_dp's
   configuration-face [GAP] still true. `KL_pp_shadow`'s `current_cfg_i` comment can be
   refined at adoption.
3. Test-evidence ratchet 74 <= 77 (adp_engine armed via the new CI step); can be lowered to 74;
   no reader disposition needed.
4. New entry points: `make -C tb/adp_engine mutants`, `make -C tb/pp_top adp-config`.
5. Optional parent matrix citations (5.6.3/5.6.4: the walk; 5.6.1/5.6.2: P12/AD0, P11/AD).

## Suite table at 9185c49 (`./scripts/run_suites.sh` rc 0, 5 min 17 s)

33 suites, 1,016,684 checks, 0 failing (base c951a9ff: 1,015,815). Changed:
adp_engine 1,367 (was 533), pp_top 7,786 (was 7,751). All others unchanged: acmp_listener 2544,
acmp_nvm 349, acmp_talker 1342, aecp_notify 10, ca_originator 16, desc_mem_guard 78,
desc_store 584, dispatch 211, dyn_state 89, event_router 81, lsn_admit 18, maap 75, nvm_port 136,
originator 104, prng 76, release_merge 18, resp_buf 64, rx_slots 130, rx_validator 393,
scoreboard 3705, side_port 368, srp_admission 991231, srp_decoder 190, srp_encoder 562,
srp_stream_fsms 1215, srp_top 1987, timer_map 1360, timer_service 48, tx_arbiter 66, tx_slots 95,
ucpu 386.

Other processor entry points at 9185c49: `lint_hdl.sh` rc 0 (40/40), `make check` rc 0,
`gen_matrix.py --check` rc 0, `syn/yosys/run.sh` rc 0 (35 tops + Xilinx memory map),
`git diff --check c951a9ff..9185c49` rc 0, `make -C tb/nvm_port figures` rc 0.

## Mutant table (campaigns)

| Campaign | Head | rc | Result |
|---|---|---:|---|
| `make -C tb/adp_engine mutants` (new) | 9185c49 | 0 | 2 controls pass, 27/27 arms KILLED (tables above) |
| `make -C tb/srp_top mutants` | 9185c49 | 0 | 7 controls, 56 arms, assertion coverage 49/49 |
| `tb/pp_top/gsi_mutants.py` | e8ec039 (pp_top identical at 9185c49) | 0 | 20 detected, golden and restored pass |
| `tb/pp_top/name_wr_mutant.py` | 9185c49 | 0 | decode killed |
| `tb/acmp_talker/retry_mutants.py` | 9185c49 | 0 | 62 killed, 7 equivalence + 1 performance controls |
| `tb/srp_admission/mutants.py` | 9185c49 | 0 | 12/12 |
| `tb/desc_mem_guard/mutate.py` | 9185c49 | 0 | hold-deleted detected |

## Parent consumer gate table (scratch parent: milan-fpga dev 9e3ccbfb, gitlink 9185c49)

Scratch: git archive of the trusted checkout, `external` efeb541, `gptp-processor` 5dce647,
`third_party/verilog-axis` 48ff7a7 cloned read-only at their pins, `protocol-processor` cloned
from the lane at 9185c49; `git submodule status` all at pins.

| # | Command | rc | Note |
|---:|---|---:|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | failed at e8ec039 (3 multi-declarator, 1 long function in new test code); fixed 9185c49 |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | failed at e8ec039 (1 undocumented function); fixed 9185c49 |
| 3 | `python3 scripts/xvlog_gate.py --check` | 0 | 4 == ratchet, none introduced |
| 4 | `python3 scripts/check_rtl_source_lists.py` | 0 | |
| 5 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | |
| 6 | `python3 sw/builder/test_builder.py` | 0 | all pass except 1 NOT RUN (gate 11: placement report absent on host) |
| 7 | `make -C tb/verilator/pp_shadow -j8` | 0 | 635 checks, 0 failures |
| 8 | `python3 scripts/check_port_contracts.py` | 0 | protocol-processor 111 <= 111 |
| 9 | `python3 scripts/measure_naming.py --check` | 0 | |
| 10 | `python3 scripts/measure_test_evidence.py --check` | 0 | 74 <= 77, 0 unexplained readers |
| 11 | `python3 scripts/docs_check.py` | 0 | |
| 12 | `python3 scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | no PINMISSING |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j8` | 0 | every leg passes (23 min) |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | 65/65, 152/152, 5/5 |

## Evidence logs (scratch, `$VALIDATION_STORAGE`, not copied here; sha256 prefix, bytes)

| Log | sha256 (16) | Bytes |
|---|---|---:|
| a446-base-suites.log | d323fa5b5f291096 | 1645 |
| a446-head-suites.log | ef7eb818e06278e2 | 1691 |
| a446-head-lint.log | 49e02975050b914d | 1028 |
| a446-head-check.log | c6cf9c32ad4eb6bd | 225 |
| a446-head-yosys.log | 1f37bb8fef4bf54d | 25185 |
| a446-head-adpmut.log | 75edfda84490e3c6 | 13872 |
| a446-final-srptop.log | e07c5bf7a467e839 | 4132 |
| a446-final-gsimut.log | abdb55b92fd7ce05 | 4196 |
| a446-final-nwmut.log | 4098f5dc8ade67a8 | 2594 |
| a446-final-retry.log | 71d510968c84e90a | 3911 |
| a446-final-srpadm.log | 7b6947bcbf4b8002 | 523 |
| a446-final-dmgmut.log | b9cb05ee014b6c8e | 171 |
| a446-final-nvmfig.log | 89b2ee6aba1944a3 | 3649 |
| a446-pg/01..16.log (parent gates) | 15.log 79df11c1eacb3f0d | 2003858 (15), 300766 (07), 158727 (16), others < 100 KB |

## What remains

- #85 item 4 (available_index interop vs a live controller): bench lane; #85 stays open.
- Finding, not acted on: IEEE §6.2.2.18 transmits current_configuration_index as 0 unless
  AEM_CONFIGURATION_INDEX_VALID (0x02000000) is set; F04.6 leaves it clear. Manager decision.
- Merge train with open PR #132 (restore writer into the dynamic store): keep the valid-flag
  decode on the bus the store actually takes, or a restored configuration advertises
  `current_cfg_i` until the first SET_CONFIGURATION.
- Hosted CI and the two reviews ([R406], [R407]). No hardware used.
