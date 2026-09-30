# [A463] Lane C6 handoff: notifications and Identify

Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, branch `c6-notifications`
from `main` `0451d83d9d3f2ed5f4513c59ac5ac219ad9dd7ff` (origin URL and HEAD confirmed at the
start). Head `5e806296b73d04ccf095ad00e081cb790fbbaf8d`. Issues: #54, #58, #80, #86.
Assignment: #80 comment 5915639621. Design STOP: #80 comment 5915752457. Ruling: #80
comment 5915765717 (authorized, four conditions). Roles: executor [A463]; reviewers [R420]
(internal), [R421] (external); manager [A10].

## Status

**REVIEW READY at `5e80629`.** Items 1 to 5 are implemented and committed (five commits). Every
gate is rc 0:

- processor suites and entry points at the head (33 suites, 1,017,309 checks);
- the lane's 30 controls, all KILLED, and every existing processor campaign (adp_engine 30/30,
  srp_top 78/78, gsi 20/20, acmp_talker retry 62 plus 8 controls, d3 83/83, nvm_port figures);
- the parent consumer set, 16 of 16, at `ccdd07b5` with the combined adaptation and
  `parent-adoption-c6.patch`;
- LUT/FF out of context at both parameter settings.

REVIEW READY posted on #80 (comment 5920997561) with the head `5e806296b73d04ccf095ad00e081cb790fbbaf8d`. The lane stops here.

The design points the ruling left open were taken as the design stated: identifySequenceID
per burst (IEEE §7.5.1.2.1 and Figure 7-142; §7.5.1's "for every identification notification
sent" read as the notification, the triple), the re-arm measured from the burst's first frame
(Figure 7-142 sets the timeout on IDENTIFY entry), a 2FF in the core with the integrator
owning debounce (ruling condition 2's second arm), TIMER and SELF made normative in their
landed shape, MGMT documented as not supported by this build. Two refinements of the design
during implementation, both recorded in the RTL banner: t0 is the first frame's *retirement*
rounded up to the next ms boundary (so every delay is at least its T- value and a held engine
cannot bunch a burst), and IDENT-REARM carries two owner-tag generations (0xB2/0xB3) so an
expiry armed for an abandoned wait never passes for the current one.

## Commits (one-line subjects, no body, no trailer)

| Commit | Item | Content |
|---|---|---|
| `018ee6c` | 1, 2 | identify machinery (pp_pkg, KL_aecp_notify, KL_aecp_engine kind 15, gen_ucode E_IDNOTIF, top parameter/port/wiring/guard/tie-off comments), `tb/pp_top` third build + sections ID/ID0, `tb/ucpu` N6, integrator guide §1/§2/§6, diagram 21 SVG+PNG, F01.5, 02, 08 |
| `b5beed6` | 3 | section NP, the SET_STREAM_INFO fix (engine map + gen_ucode E_SINFOUNS), `tb/ucpu` N7 |
| `4ce963e` | 4 | sections ST and RN, `tb/originator` section R |
| `5cf99f7` | 4, 5 | `tb/pp_top/notify_mutants.py` (30 controls) |
| `5e80629` | 1, 3, 4 | docs: 00 (GAP-06, GAP-17, REQ-AEM-026, REQ-NOT-001/-002, disposition rows), 03 §1/§4/§5, 06 intro/§7/F06.16/command table, 09 §8.3, HDL-engineer and operator guides, `tb/pp_top` and `tb/originator` READMEs |

## Item 1: #80 and #86, the identify machinery and the producers

- RTL (no fix of existing behaviour here; new, parameter-gated logic):
  - `hdl/common/pp_pkg.sv:254-255` owner tags `PP_OWN_IDENT_C` 0xB1 (+3); `:283-285`
    `PP_UNS_IDENT_C` = 15, the Table B.1 MAC, the Table 7-180 EID.
  - `hdl/aecp/KL_aecp_notify.sv:199` `EN_IDENTIFY_NOTIF_P`, `:244-245` `identify_button_i`,
    `identify_index_i`; `:691` `core_arm_w`; `:693-822` `gen_ident` (2FF, WAITING / frame /
    gap / hold states, t0, generations, arm requests, uns-face ownership); `:823-839`
    `gen_no_ident` (the pre-lane assignments); `:850` `amap_busy_o |= id_own_w`; `:1067`
    the identify arm in a free cycle; `:1324` `core_done_w`. Clauses: IEEE §7.4.39.1,
    §7.5.1, §7.5.1.2.1, §7.5.1.3; Milan §5.4.5.4.
  - `hdl/aecp/KL_aecp_engine.sv:321` `EN_IDENTIFY_NOTIF_P`, `:893` `UPC_IDNOTIF_C`,
    `:1385-1388` kind 15 -> 0x0026 / E_IDNOTIF only with the parameter.
  - `hdl/aecp/ucode/gen_ucode.py:218` `E_IDNOTIF` = 2000, `:949` its 6 words.
  - `hdl/top/protocol_processor_top.sv:182` `EN_IDENTIFY_NOTIF_P` (default 0), `:233`
    `identify_button_i`, `:848` owner-tag guard, `:3756-3757` IDENT-BURST slot and the
    parameter to the notify block, `:3823-3824` the two inputs, the engine parameter, and the
    normalizer tie-off comments now naming the landed dispositions.
- Producers (#86 acceptance 1 and 4): 03 §4/§5 state the landed shape (RX-only dispatch,
  expiry bus, engine-internal SELF jobs, CONTROLLER_AVAILABLE through the originator, PROBE_TX
  retry in the listener with `PROBE_SLOTS_P = 0`, ADP self-writing, MGMT not supported); GAP-17
  carries the same disposition; the top's normalizer tie-offs say so.
- #86 acceptance 3: `tb/originator` section R (below).

## Item 2: #54, origination graded on the wire

Section ID (third build, 62 checks) and ID0 (default build, 3 checks); measured values in
`tb/pp_top/README.md`. Failing arms: every ID check fails against the pre-lane RTL by
construction (no frame is ever sent to 91-E0-F0-01-00-01; ID1's count is 0), and the eleven
identify mutants below each fail their named checks.

## Item 3: #58, a push per command class and the non-ATDECC path

- Section NP (47 checks): SET_CONFIGURATION (1, then 0), SET_STREAM_FORMAT, SET_STREAM_INFO,
  SET_CONTROL (255, 0), SET_SAMPLING_RATE(48000), STOP_STREAMING, START_STREAMING, then a SET
  from the second controller and two unchanged SETs.
- **RTL fix**: `hdl/aecp/KL_aecp_engine.sv:1372-1375` (PP_UNS_SINFO_C -> `UPC_SINFOUNS_C`,
  `:895`) and `hdl/aecp/ucode/gen_ucode.py:219`, `:2076` (`E_SINFOUNS`, 21 words). Clause:
  IEEE §7.4.15.1 (SET_STREAM_INFO command and response share Figure 7-40, 84 bytes), §7.5.2
  (the notification is an unsolicited response to the command), Milan §5.4.2.10 (replaces the
  GET response's format only), §5.4.2.9 (the successful response's flag and latency).
  Failing arm on the landed RTL: NP3, log `np3-failing-arm-before-fix.log` in this directory
  (94-byte frame, cdl 0x44, the GET_STREAM_INFO words, against the expected 122-byte cdl-0x60
  Figure 7-40 frame).
- Acceptance 2: `enq_dropped_configuration`, `enq_dropped_stream_info`,
  `class_4_mapped_to_rate`, `class_9_mapped_to_control` (below), recorded in
  `tb/pp_top/README.md`.
- Acceptance 3 (second arm): 06 §7 trigger class (2) and REQ-NOT-002 state MGMT-origin changes
  are not supported by this build; 03 §5 item 4 gives the reason.

## Item 4: the RND and STORM suites (#80), and #86's inflight RND

- ST (18 checks), RN (4 checks), `tb/originator` R (3 checks); values in the READMEs.
- Seeds: RN 0xC6A46301 (720 steps, 2,203 frame comparisons, zero divergence); R 0x86A46301
  (4,000 steps, 3,757 events, zero divergence).

## Mutation record: `tb/pp_top/notify_mutants.py` at the head, 30 of 30 KILLED

| Mutant | Failing checks (count, named) |
|---|---|
| ident_two_frames | 19; ID1 |
| ident_seq_per_frame | 22; ID1b |
| ident_no_rearm | 12; ID2 |
| ident_rearm_from_third_frame | 12; ID2, ID2d |
| ident_burst_100ms | 20; ID1c |
| ident_t0_at_request | 22; ID6d |
| ident_cut_on_release | 22; ID1 |
| ident_release_ignored | 35; ID1, ID2e |
| ident_unicast_da | 7; ID1 |
| ident_face_taken_mid_job | 3; ID5f (ID5b, ID5c too) |
| ident_built_at_default (EN forced to 1 in the default build) | 2; ID0 |
| enq_dropped_configuration | 2; NP1 |
| enq_dropped_stream_info | 1; NP3 |
| class_4_mapped_to_rate | 4; NP4 |
| class_9_mapped_to_control | 2; NP6 |
| requester_not_excluded | 12; NP1 |
| entry_seq_not_advanced | 13; NP1b |
| stream_info_get_body (the landed mapping) | 1; NP3 |
| counter_limit_500ms | 12; ST2, ST2b |
| fan_out_skips_row_0 | 9; ST1b |
| refresh_resets_seq | 1; RN |
| foreign_unlock_allowed | 1; RN |
| lock_taker_notified | 1; RN |
| deregister_keeps_row | 1; RN |
| registry_holds_15 | 2; RN |
| set_control_ignores_lock | 1; RN |
| inflight_highest_free_id | 15; R |
| inflight_match_ignores_seq | 7; R |
| inflight_cancel_keeps_timer | 5; R |
| inflight_shared_seq | 10; R |

The first campaign run found one weak check: `ident_rearm_from_third_frame` failed ID2's count
but not ID2d, because ID2 returned early when fewer than nine frames arrived. ID2 now grades
every burst that arrived, and the mutant fails both.

## Resource cost, out of context (condition 1)

No Vivado on this host: yosys 0.66 `synth_xilinx -family xc7 -flatten` of the whole
`protocol_processor_top` (default shape), after `sv2v`, with the generated ROM images.

| Build | LUT | FF | CARRY4 | MUXF7 / MUXF8 | RAM32M / RAM64M | RAMB36 / RAMB18 | DSP48 |
|---|---:|---:|---:|---:|---:|---:|---:|
| main `0451d83d` | 62,463 | 30,454 | 2,317 | 456 / 105 | 1,497 / 3 | 16 / 1 | 4 |
| head, `EN_IDENTIFY_NOTIF_P` = 0 | 62,783 | 30,454 | 2,317 | 602 / 160 | 1,497 / 3 | 16 / 1 | 4 |
| head, `EN_IDENTIFY_NOTIF_P` = 1 | 63,352 | 30,530 | 2,331 | 620 / 162 | 1,497 / 3 | 16 / 1 | 4 |

- At 0 the flip-flop, carry, RAM and DSP counts equal main's. The +320 LUT is the mapper, not
  logic: the netlists are formally equivalent (next section) apart from the SET_STREAM_INFO
  fix, whose ROM words are block RAM and whose map change is one constant. Evidence of the
  mapper's variance: `KL_aecp_notify` alone maps to 6,598 LUT on main and 8,002 at 0 with the
  same 1,721 FF, and the two are proven equivalent.
- The identify cost (1 - 0): +76 FF (the sequencer's 63 and 13 arm/owner bits that stop being
  constant), +14 CARRY4 (the t0 adder, the seq increment), +569 LUT as mapped (the uns-face
  mux of 165 bits plus the sequencer; the LUT figure carries the same mapper variance).
- Stat files: `receipts/yosys-stat-top-*.txt`. Logs (not copied, over 200 KB):
  `synth_top_base.log` 7.3 MB sha256 3e3d56a5...9029; `synth_top_en0.log` 7.2 MB
  cc427b58...32b1; `synth_top_en1.log` a7a6105c...ef78d.

## "At 0 the top is unchanged" (condition 4)

- yosys `equiv_make/equiv_struct/equiv_simple/equiv_induct/equiv_status -assert`:
  `KL_aecp_notify` of this head at 0 (the two unread inputs deleted as ports) against main's:
  6,365 `$equiv` cells, all proven (`receipts/equiv_notify.ys`, summary file; log 2.4 MB
  sha256 5d028ac4...9a5e).
- `KL_aecp_engine`'s own logic at 0 against main's with this lane's SET_STREAM_INFO fix alone:
  21,481 `$equiv` cells, all proven, its five submodules (byte-identical to main by
  `git diff 0451d83d`) matched as cut points (`receipts/equiv_engine_bb.ys`; log 7.6 MB
  sha256 391a3ded...29ea). A flattened attempt with the µcode ROM mapped proved 50,481 of
  50,673 cells before the SAT solver ran out of memory in the ROM's read cones.
- The top's own change at 0 is wiring only: the unread `identify_button_i`, `identify_index_i`
  to the notify block, the parameter pass-through, the elaboration-time owner guard, comments.
- Regression: every one of the default build's 7,924 pre-lane checks passes, and ID0 grades
  the button inert.

## Item 5: the parent-visible list (final)

Read against the parent at milan-fpga dev `ccdd07b5`. The adoption edits are in
`parent-adoption-c6.patch` in this directory, applied after `parent-adaptation-132-c1.patch`.

| # | Change | Parent effect | Parent disposition (in `parent-adoption-c6.patch` unless stated) |
|---|---|---|---|
| 1 | new top input `identify_button_i` (ruling condition 3) | `hdl/milan/KL_pp_shadow.sv` instantiates `protocol_processor_top` by named ports; without a connection `lint_rtl --check` fails (a new PINMISSING, measured) | `.identify_button_i (1'b0)` with a `//!` rationale: tied until a debounced board button is wired |
| 2 | new top parameter `EN_IDENTIFY_NOTIF_P`, default 0 (condition 3) | none at the default | `.EN_IDENTIFY_NOTIF_P (1'b0)` stated explicitly with a `//!` rationale, so a later default change cannot switch the parent silently |
| 3 | the port-contract and naming checks gain the port (condition 3) | `check_port_contracts.py` scans the top's ports; `measure_naming.py` scans names | no script edit needed: the port is documented (protocol-processor 111 <= 111 undocumented; 52 literal-bound, 62 unjustified, both unchanged) and the name passes (96 PASS) |
| 4 | integrator guide §1/§2/§6 and diagram 21 gain the parameter and the input (condition 3) | this repository | landed in `018ee6c`; `check-integrator-params.py` 27 = 27 = 27 |
| 5 | new mutation driver `tb/pp_top/notify_mutants.py` (assignment item 5) | `scripts/measure_test_evidence.py` counts DUT-source readers; with 132-c1 alone the evidence ratchet fails with 1 unexplained reader (measured) | a `DUT_READER_DISPOSITIONS` entry: a campaign that plants defects in an isolated copy and reads no expected value from the DUT text |
| 6 | behaviour at the parent's setting (0) | one frame changes: the unsolicited SET_STREAM_INFO (item 3's fix) now carries Figure 7-40's 84-byte body | none needed; no parent bench grades that frame |
| 7 | `make -C tb/pp_top` builds three executables and sums three tallies | only if the parent runs the processor's `tb/pp_top` directly | none |

## Gates

### Processor, every command at `5e80629`, all rc 0

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, 1,017,309 checks, 0 failing (base `0451d83d`: 1,017,162); receipt `receipts/run_suites-head-5e80629.log` |
| `make -C tb/pp_top` | 0 | 8,078 = default 7,996 + fixture 20 + identify 62 (`receipts/pp_top-head-tallies.txt`) |
| `make -C tb/pp_top identify` | 0 | third build: ID 62 checks; default build ID0 |
| `./scripts/lint_hdl.sh` | 0 | 41 modules OK; the three changed modules also at `EN_IDENTIFY_NOTIF_P` = 1 |
| `make check` | 0 | docs lint, WaveDrom, links, matrices, parameters 27 = 27 = 27, stale |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` | 0 | 36 tops OK and the memory-map check |
| `git diff --check 0451d83d..5e80629` | 0 | |

### Mutation campaigns at `5e80629`

| Campaign | rc | Result |
|---|---:|---|
| `python3 tb/pp_top/notify_mutants.py --output DIR` (new) | 0 | goldens pass; 30 of 30 KILLED (`receipts/notify-mutants-head-*.json`) |
| `make -C tb/adp_engine mutants MUTANT_OUTPUT=DIR` | 0 | 30 of 30 KILLED; 32 checks, 0 FAIL; 324 s |
| `make -C tb/srp_top mutants MUTANT_OUTPUT=DIR` | 0 | 78 of 78 KILLED; assertion coverage 65/65; 90 checks, 0 FAIL; 1,806 s |
| `python3 tb/pp_top/gsi_mutants.py --output DIR` | 0 | 20 of 20 detected by named checks; golden and restored PASS; 763 s |
| `python3 tb/acmp_talker/retry_mutants.py --logs DIR` | 0 | 62 mutants KILLED; 7 equivalence controls and 1 performance control retained; baseline and restored rc 0; 371 s |
| `python3 tb/pp_top/d3_mutants.py --output DIR --jobs 1 --only ...` in two chunks (49: OWNERSHIP, SERVICE, RESTORE, ROLLBACK, DR2C; 34: REVIEW, AGGREGATE, ADMISSION) | 0, 0 | 49 of 49 and 34 of 34 KILLED by their named checks (83 of 83); goldens PASS in both; 3,071 s and 1,755 s |
| `make -C tb/nvm_port figures` | 0 | all measured figures agree with the tree (2 waivers printed with their reasons); 234 s |

Every campaign plants its defects in private copies; `git status` was clean after each.

### Parent consumer set at milan-fpga dev `ccdd07b5`, all 16 rc 0

Scratch copy under `$VALIDATION_STORAGE` (git archive of the trusted checkout and its submodules;
the processor submodule a shared clone of this lane at `5e80629`), commits: the archive, then
`git apply parent-adaptation-132-c1.patch`, then `git apply parent-adoption-c6.patch`. Verilator
5.050, `make -j8`; the trusted checkout was not touched.

| # | Command | rc | Result |
|---:|---|---:|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | every ratchet at or under budget |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | every ratchet at or under budget (too many parameters 7 <= 7) |
| 3 | `python3 scripts/check_rtl_source_lists.py` | 0 | OK: 107 files in the milan_datapath closure, 4 of 4 consumer lists; protocol-processor 36/42 tops, 6 recorded omissions |
| 4 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | OK |
| 5 | `python3 scripts/check_port_contracts.py` | 0 | OK: 3,784 first-party ports (protocol-processor 1,751); undocumented protocol-processor 111 <= 111; 52 literal-bound, 62 without a local rationale, all recorded |
| 6 | `python3 scripts/measure_naming.py --check` | 0 | PASS: 96 candidates, all recorded by identity |
| 7 | `python3 scripts/measure_test_evidence.py --check` | 0 | PASS: 74 <= 77 suites without a mutation arm, 10 <= 10 unseeded draw sites, 0 <= 0 unexplained DUT-source readers, 3 <= 3 wall-clock suites (1 unexplained reader without adoption edit 5) |
| 8 | `python3 scripts/docs_check.py` | 0 | 0 findings across 181 md + 951 scrubbed files; scrub self-test 23/23; routing 4/4 |
| 9 | `python3 scripts/xvlog_gate.py` | 0 | 4 findings == ratchet (0 hdl/, 4 pinned processors) |
| 10 | `python3 sw/builder/test_builder.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11: the calibration report needs a local mf48 build tree); 848 s, repeated 853 s |
| 11 | `python3 scripts/lint_rtl.py --check` | 0 | 90 <= ratchet 90 (17 waived, 0 justified lint_off); without adoption edit 1: NEW PINMISSING `identify_button_i`, rc 1 |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 295 checks, 0 failures; 209 s |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | both lint passes |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 checks, 315 PASS |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | gmstep 103; 181 + 181; milan_datapath 234, 234, 231; media_aclk 190; 12 RESULT: PASS, 0 FAIL; 6 + 6 mutant arms; 1,446 s (VERILATOR_JOBS bounds compile memory only, model parameters unchanged) |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | tdm8_render 65 and 152 checks; 5 leg-defect arms caught; 316 s |

Logs over 200 KB are not copied (sha256 and size in the receipts table below).

### Receipts (`receipts/` in this directory)

| Path | Content |
|---|---|
| `run_suites-head-5e80629.log`, `pp_top-head-tallies.txt` | the processor suites at the head |
| `notify-mutants-head-{identify,pushes,rnd}.json` | the lane's 30 controls, per-mutant failing checks |
| `campaigns/` | adp_engine, srp_top, gsi, acmp_talker retry, d3 (two chunks), nvm_port figures logs |
| `parent-gates/` | test_builder, lint_rtl (with and without the adoption tie-off), xvlog_gate, nvm_cosim lint and quick, milan_dp_render logs |
| `yosys-stat-top-{main-0451d83d,en0,en1}.txt` | the resource tables |
| `equiv_notify.ys`, `equiv_engine_bb.ys`, `equiv-*-summary.txt` | the equivalence scripts and results |

Logs not copied (over 200 KB), in the scratch area:

| Log | Bytes | sha256 |
|---|---:|---|
| parent `pp_shadow` | 302,414 | `effc446411df6c394ab0ff07207b26438740e7f2186ba07bd2252cb3bd0da9b0` |
| parent `milan_dp` | 1,999,060 | `b73b5b9b68c81b5d1a02e0bb360f6babda7982f1b0e0fb60f892bc2513559ef9` |
| yosys top synthesis at main, 0, 1; the two equivalence runs | 7.3 MB, 7.2 MB, 7.2 MB, 2.4 MB, 7.6 MB | as in the two sections above |

## What remains

- Hosted CI and the reviews ([R420] internal, [R421] external).
- The parent adopts `parent-adoption-c6.patch` when it moves its processor pin past this head.
- No hardware used; no board button exists, so the parent keeps `EN_IDENTIFY_NOTIF_P` at 0.
- Resource figures are yosys (no Vivado on this host); a Vivado out-of-context run at the parent
  is the authoritative figure.
- Not attempted: the optional overflow eviction sweep (MAY; recorded decision, no work owed
  per #80). RN grades a lock-refused SET on its status and length, not its body, which is #53's decision.
- Observation outside the acceptance: a solicited DEREGISTER does not push, although IEEE §7.5.2
  lists DEREGISTER_UNSOLICITED_NOTIFICATION; recorded, not changed.

## History: STOP at the design gate (no code written, head unchanged at 0451d83d)

- TAKEN posted on #80 (comment 5915652877).
- The assignment requires a STOP for a manager ruling if the design needs a top-level port,
  a parameter, a register or any parent-visible change. It does. IDENTIFY_NOTIFICATION
  starts from a user action on the device (IEEE 1722.1-2021 §7.5.1, §7.5.1.3
  `identifyButtonPressed`; Milan §5.4.5.4), and the processor has no input that carries
  one (see D1.2). #54 acceptance 1 also asks, in its own words, for a new
  `protocol_processor_top` trigger input behind `P-EN-IDENTIFY-NOTIFICATION`.
- The STOP with this design summary is posted on #80 (comment 5915752457). No
  item was started, no commit was made, and no gate was run, because there is no change
  to gate.

### 0. Design (written before any code, as the assignment requires)

#### D1. Where IDENTIFY_NOTIFICATION originates, and what starts it

**D1.1 What the standards require.**

- IEEE 1722.1-2021 §7.4.39 and Figure 7-61 define the frame. It is an AECP AEM response
  with u = 1, command_type IDENTIFY_NOTIFICATION (0x0026), descriptor_type CONTROL
  (0x001A), and descriptor_index set to the IDENTIFY control that generates it.
  §7.4.39.2: it is never sent as a command, and an entity that receives it as a command
  answers BAD_ARGUMENTS. That is already landed and graded (`tb/pp_top` A6).
- IEEE §7.5 and §7.5.1 define the notification. It is the "first notification type": a
  button on the entity through which a user performs entity-to-controller
  identification. It is sent as a multicast AECP unsolicited response, three times,
  150 ms apart, to the "Identification Notifications" MAC address of Table B.1
  (91-E0-F0-01-00-01). controller_entity_id is the Table 7-180 value
  (90-E0-F0-FF-FE-01-00-01). sequence_id is an internal identifySequenceID that starts
  at 0 at power-up or reboot.
- IEEE §7.5.1.2.1 (txIdentify) sends three messages that all use the identifySequenceID
  value as their sequence_id. In Figure 7-142 the identify state machine runs
  INITIALIZE, then WAITING. `identifyButtonPressed` moves it to IDENTIFY, which runs
  txIdentify(), sets timeout = currentTime + 1 s and increments identifySequenceID.
  IDENTIFY re-enters when `timeout <= currentTime` and returns to WAITING on
  `!identifyButtonPressed`.
- Milan §5.4.5.4 makes this a "should" when the PAAD provides a way to report itself
  (typically a front-panel button). `identifyButtonPressed` is TRUE while the user wants
  the PAAD to report itself, and its mapping to the user action is vendor-specific. It is
  the entity-to-controller mechanism, distinct from the IDENTIFY CONTROL (Milan §5.3.12,
  controller to entity). So a SET_CONTROL on the IDENTIFY control must NOT start it.

**D1.2 What starts it, and why that trips the STOP.** The only trigger is a device-side
user action. I enumerated every `protocol_processor_top` input, and none can carry it:

- the identity inputs;
- link and gPTP;
- the SRP service face `svc_*`, whose `svc_op_i` is a KL_srp_top op code;
- the side-port host face, whose control window decodes word 0 (scratch) and word 1
  (restore status) only (`hdl/top/protocol_processor_top.sv:4465-4474`);
- the counters, audio-map and stream-info gather faces;
- the NVM device face.

The architecture documents already name the missing input: 02 F02.1/§2 `identify_button`
(D, in, optional, P-EN-IDENTIFY-NOTIFICATION, 2FF), 02 §6 row "2FF + debounce", and 06
F06.16 "button variant". The design therefore needs:

- a new top input `identify_button_i`: a level, asynchronous, 2-flop synchronised in the
  core, and ignored when the parameter is 0;
- a new top parameter `EN_IDENTIFY_NOTIF_P` (P-EN-IDENTIFY-NOTIFICATION), default 0 per
  #54 acceptance 1. F01.5 lists this parameter with default **1**, so the ruling should
  also say which default wins.

Both are parent-visible, as listed in section 2. Hence the STOP.

**D1.3 Where it originates (internal; proposed pending the ruling).** An identify
sequencer inside `KL_aecp_notify`, in a generate block on the parameter, so it has no
flops or LUTs when the parameter is off. That block already owns:

- the unsolicited job face to the engine;
- the single shared-timer arm client;
- the first singleton slot (LOCK). pp_pkg orders the singletons "LOCK, IDENT-BURST,
  IDENT-REARM, ...".

The sequencer presents one job per frame on the existing face:

| Job field | Value |
|---|---|
| `uns_kind` | new `PP_UNS_IDENT_C = 4'd15`, the one free code of the 4-bit kind, so the face does not widen |
| `uns_mac` | 91-E0-F0-01-00-01 |
| `uns_ctlr_eid` | 90-E0-F0-FF-FE-01-00-01 |
| `uns_seq` | identifySequenceID |
| `uns_desc_type` | 0x001A |
| `uns_desc_index` | the existing `identify_index_i` (Milan §5.3.3.10: the same index in every configuration) |

`KL_aecp_engine` maps kind 15 to command_type 0x0026 and a new 28-byte, no-gather
microprogram. The engine already takes a job's DA from `uns_mac`
(`hdl/aecp/KL_aecp_engine.sv:2725`), so the multicast DA needs no new mux. The frame
leaves on `LANE_AECP_UNS` through the same builder and TX slot pool as every other
unsolicited response.

The wire frame is an AECPDU of 28 bytes (cdl 16) with these fields:

- message_type AEM_RESPONSE, status SUCCESS;
- target_entity_id = `entity_id_i`;
- controller_entity_id 90-E0-F0-FF-FE-01-00-01;
- sequence_id = identifySequenceID, u = 1, command_type 0x0026;
- descriptor_type 0x001A, descriptor_index = `identify_index_i`.

The frame is padded to the Ethernet minimum.

Rules:

- The identify job is a single-shot, like the targeted DEREGISTER holder. It is picked
  ahead of the command queue, so a 15-row fan-out delays a frame by at most one job
  build.
- It is independent of the registry: it is sent with no controller registered, and it
  never touches any row's sequence_id.
- It is not lock-gated (IEEE §7.5.1 has no lock condition).
- While the AECP engine is held (the D3 restore hold), the sequencer stays in WAITING.

#### D2. The burst of three at 150 ms with the 1 s re-arm

- **Timers.** The shared timer service (08 §5, F08.4) runs the burst through the two
  reserved singletons: `TMR_MAP_C.single + 1` (T-IDENT-BURST) and `+ 2` (T-IDENT-REARM).
  They are counted in `hdl/common/pp_pkg.sv:125-130` and `:180-181` and have no user
  today, so the slot map does not move. The owner tags are 0xB1 and 0xB2, inside the
  lock's nibble; the top's owner guard (`PP_OWN_LOCK_C + 1 <= 0xC0`) extends to `+ 3`.
  T-IDENT-BURST and T-IDENT-REARM stay localparams read from F08.1. `tb/pp_top` already
  compresses the millisecond tick (`TIM_DIV_*`), so no timing parameter is needed.
- **Sequence** (Figure 7-142, with txIdentify made explicit):
  1. WAITING. When the synchronised level goes high, send frame 1 at t0 (the ms value
     at the press). Arm BURST for d1 = t0 + T-IDENT-BURST and REARM for
     t0 + T-IDENT-REARM.
  2. On the d1 expiry, send frame 2 and arm d2 = d1 + T-IDENT-BURST. Deadlines chain
     from the previous deadline, not from now, so millisecond quantisation never
     accumulates.
  3. On the d2 expiry, send frame 3, then increment identifySequenceID.
  4. HELD. If REARM expires with the level still high, start the next burst with t0 set
     to the REARM deadline and re-arm REARM.
  5. Level low after a burst: return to WAITING.
  - A press during a running burst does not restart it.
  - A release followed by a new press starts a new burst immediately (WAITING to
    IDENTIFY in Figure 7-142), but never before the running burst's third frame.
- **Grading plan (#54, #80).** On the compressed timebase, `tb/pp_top` would grade:
  - count, DA, controller EID and the byte-exact frame;
  - spacing within 150 ms plus or minus one tick;
  - the same sequence_id inside a burst and +1 per burst;
  - re-arm of at least 1000 ms while held;
  - release stops the bursts;
  - the parameter-off build sends nothing;
  - A6 unchanged.

  Mutants on the named checks: a two-frame burst, spacing re-based on now, sequence_id
  advanced per frame, and the re-arm removed.
- **Points the ruling should settle:**
  - (a) sequence_id per burst (IEEE §7.5.1.2.1 and Figure 7-142 read that way) or per
    frame (one reading of #54 acceptance 2, "an incrementing identify sequence_id");
  - (b) re-arm measured from the burst's first frame (Figure 7-142 sets timeout on
    IDENTIFY entry, so held bursts start 1000 ms apart);
  - (c) debounce: 02 §6 says "2FF + debounce", but no T- constant exists. The proposal
    is 2FF in the core and debounce by the integrator, since the mapping is
    vendor-specific (Milan §5.4.5.4);
  - (d) the parameter default: #54 says 0, F01.5 says 1.

#### D3. How the TIMER, SELF and MGMT producers stop being tied off

Today `hdl/top/protocol_processor_top.sv:1490-1498` ties `tmr/self/mgmt_valid_i` to 0
("P4"). #86 acceptance 1 accepts either wiring them or amending 03 §4/§5 and GAP-17 to
the landed shape with MGMT explicitly dispositioned.

- **TIMER and SELF. Recommended: make the landed shape normative, with no port change.**
  - TIMER: expiries reach their owners on the shared expiry bus: lock, TIME_LIMITED,
    the CONTROLLER_AVAILABLE monitor and, new, IDENT-BURST and IDENT-REARM. They are
    never normalizer transactions.
  - SELF: entity-originated AECP output is the engine-internal SELF job on the
    unsolicited face (fan-out, targeted DEREGISTER, LOCK auto-unlock and, new,
    IDENTIFY_NOTIFICATION), plus `KL_pp_originator` for command PDUs
    (CONTROLLER_AVAILABLE). ADP TX stays in `KL_adp_engine`.
  - The PROBE_TX exact-duplicate retry stays in the listener (`PROBE_SLOTS_P = 0` at the
    top). 03 §5 would say so (#86 acceptance 4).
  - The normalizer's `tmr/self` ports would carry that disposition in place of "P4".
    Their module-level arbitration stays graded by `tb/dispatch`. 03 §4, §5, F03.3 and
    GAP-17's disposition would be amended to match.
  - The alternative is wiring them: the press as a SELF transaction and each IDENT
    expiry as a TIMER transaction {AEM, 0x0026, `PP_HZ_IDENTIFY`, no rx_slot} into
    dispatch. That needs a no-RX-slot execution arm in the AECP engine, which today runs
    only RX-slot-backed transactions, and the scoreboard is unwired at the top (F06.14
    note). It is a larger change with no Milan-observable difference on the wire.
- **MGMT.** Milan §5.4.5.2 (second paragraph) and IEEE §7.5.2 ("internally, either
  through a front panel interface or its normal operation") need a non-ATDECC change to
  do two things:
  - write the processor's own state, so the pushed body (always rebuilt from current
    state) and every later GET agree;
  - take the lock check ("if the PAAD-AE is not locked").

  No face exists for this. `KL_aecp_dyn_state`'s only writer is the microcode st face.
  The side-port image and dbg windows are tied off ("P4"), and the ctrl window holds
  scratch and status only. Any MGMT producer needs a parent-visible face: new top
  change-request ports {object kind, descriptor, value} with an accept or refuse
  (locked) answer, or new ctrl-window registers.
  - **Recommended:** the second arm of #58 acceptance 3. 06 §7 trigger class (2) and the
    REQ-NOT-002 row state that this build does not support MGMT-origin changes, and the
    normalizer's `mgmt` port stays tied with that disposition.
  - If the ruling asks for the face instead, the proposal is an engine-internal MGMT job
    that runs the same SET microprograms (lock-checked, no wire response, no requester
    exclusion). That would be its own ruling on the port or register shape.

#### D4. Which command classes push an unsolicited notification on the wire

The rule is IEEE §7.5.2's list, restricted to what this build executes with SUCCESS and
"modifies the state" (Milan §5.4.5.2). Pushes go to every registered controller except
the requester, with per-entry DA, controller EID and sequence_id (Milan §5.4.5.1).

| Class (`ev_cmd_class`) | Command | Kind (`KL_aecp_notify.sv:534-541`) | On-wire push graded today | This lane (#58) |
|---|---|---|---|---|
| 1 | SET_CONFIGURATION | PP_UNS_CFG | no | byte-exact at controller B, none at requester, seq advancing |
| 2 | SET_STREAM_FORMAT | PP_UNS_SFMT | no (µcode enqueue only) | same |
| 3 | SET_STREAM_INFO | PP_UNS_SINFO | no | same |
| 4 | SET_CONTROL | PP_UNS_CTRL | no | same |
| 5 | SET_SAMPLING_RATE | PP_UNS_SRATE | partly: W9k8 grades the byte-exact push at a second controller (seq 0) and W9k9 exactly one frame (both landed after the audit); no requester-side silence or seq advance | the missing arms |
| 9 | START_STREAMING / STOP_STREAMING | PP_UNS_STRM | no | same, both opcodes |
| 6 | ADD/REMOVE_AUDIO_MAPPINGS | PP_UNS_AMAP | R15/R17 | kept |
| 7 | SET_NAME | PP_UNS_NAME | U8c | kept |
| 8 | SET_CLOCK_SOURCE | PP_UNS_CLKS | W10j8 | kept |
| (rgy) | LOCK_ENTITY lock or unlock state change | PP_UNS_LOCK | L2, L5b | kept |

These never push:

- ACQUIRE_ENTITY never succeeds (Δ7).
- Every n/i opcode in the IEEE list answers NOT_IMPLEMENTED: WRITE_DESCRIPTOR,
  SET_ASSOCIATION_ID, INCREMENT/DECREMENT_CONTROL, REBOOT and the rest.
- REGISTER is not in the list.

Observation, outside #58's acceptance: the IEEE §7.5.2 list names
DEREGISTER_UNSOLICITED_NOTIFICATION, and a solicited DEREGISTER does not push today. It
is recorded, not proposed.

The #58 mutants would be one dropped NOTIFY_ENQ (in `gen_ucode.py`) and one mis-mapped
class (`KL_aecp_notify.sv:534-541`), each recorded in `tb/pp_top/README.md`.

#### D5. The rest of the lane after a ruling (for scale)

- **STORM (#80 acceptance 2).** 16 controllers registered, one state change, and 15
  byte-exact frames with per-entry sequence_id. Then `ctr_change_i` churned above 1 Hz on
  several descriptors, checking at most one emission per descriptor per second, while a
  solicited command still answers inside T-BUDGET-AECP-WC.
- **RND (#80 acceptance 3).** Seeded register, deregister, lock and SET churn from 16 or
  more controllers against an independent C++ registry and lock model, with zero
  divergence and a README mutation record.
- **#86 acceptance 3** asks for a different RND suite: overlapping CONTROLLER_AVAILABLE
  inflights in random response, expiry and cancel order, against an independent inflight
  model. The assignment's item 4 names only #80's suites, so unless it is ruled in, #86
  would stay "Relates to".
- **Resource cost.** Rough estimate for the identify sequencer when on: about 40 to 60
  FF and 60 to 120 LUT (the 16-bit sequence, the FSM, 2FF and the job mux arm). It is
  zero when off. The out-of-context LUT and FF figures are measured at the gate.

### 1. Items at the STOP

No item was started (STOP at the design gate).

| Item | Issue(s) | State |
|---|---|---|
| 1 | #80, #86: identify machinery and producers | blocked on the ruling (top port and parameter) |
| 2 | #54: origination graded on the wire | blocked (depends on item 1) |
| 3 | #58: six command-class wire pushes, non-ATDECC path | not started (item order); MGMT arm needs the ruling |
| 4 | RND and STORM suites (#80) | not started (item order) |
| 5 | parent-visible list | proposed below |

### 2. Parent-visible list as proposed at the STOP (superseded by "Item 5" above)

| Change | Parent effect | Parent disposition needed |
|---|---|---|
| new top input `identify_button_i` | `hdl/milan/KL_pp_shadow.sv` instantiates `protocol_processor_top` (`u_pp`) by named ports: it must connect the pin (tie 1'b0, or a board button); `scripts/check_port_contracts.py` scans the top's ports | connect or tie in KL_pp_shadow; the port-contract population moves by one |
| new top parameter `EN_IDENTIFY_NOTIF_P` (default 0 proposed; F01.5 says 1) | this repo's `check-integrator-params.py` requires it in integrator guide section 2 and diagram 21; the parent's shape and declaration checks (`check_entity_shape.py`, `sw/builder/test_declarations.py`) may enumerate top parameters | decide whether the parent overrides it (to 1 plus a button) or keeps the default |
| MGMT face (only if ruled in instead of the doc disposition) | new top ports or side-port ctrl-window registers | a separate ruling |
| new `tb/pp_top` mutation driver (identify, pushes) | the parent adaptation touches `scripts/measure_test_evidence.py`; if it enumerates processor mutation drivers, a new driver needs a disposition there | checked at implementation |

### 3. Gates at the STOP

Not run: no code change exists to gate (the head is unchanged at 0451d83d). Processor
suites, entry points, mutants, the parent consumer set at `ccdd07b5` with
`parent-adaptation-132-c1.patch`, and the out-of-context LUT and FF figures all run after
the ruling, on the implementation.

### 4. STOP posted

The STOP on #80 (comment 5915752457) carries the D1 to D4 summary and the head `0451d83d`. The lane waits for
the manager's ruling on:

- (1) the `identify_button_i` input and the `EN_IDENTIFY_NOTIF_P` parameter, including
  the default;
- (2) the TIMER and SELF disposition (landed shape, recommended) against wiring them;
- (3) MGMT as a documented "not supported" against a new face;
- (4) sequence_id per burst, re-arm from the first frame, and debounce ownership;
- (5) whether #86 acceptance 3's inflight RND suite is in scope.
