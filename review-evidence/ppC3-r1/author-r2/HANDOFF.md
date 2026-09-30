# HANDOFF: [A451] lane C3 (ADP) round 2, issues #40, #41, #85 (PR #136)

Status: DONE, REVIEW READY at head `20ec92b7b190d03c46e40be89d236bc9a0702a59` (local branch; no push, per the lane rules)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Branch: `c3-adp-coverage`, round-1 head `9185c491b56358d6bc15b5069b612bfaa95316f3`
- Assignment: issue #40 comment 5893098818 (round 2: merge main `b2db3a97`, R406-1 F-1, parent-visible list)
- Reviews read: R407-1 (PR #136 comment 5891739000, POSITIVE), R406-1 (PR #136 comment 5892168191, NEGATIVE on F-1)
- TAKEN posted: issue #40 comment 5893105826
- REVIEW READY posted: issue #40 comment 5898557304 (head `20ec92b7`)
- Round-1 packet: read-only, copied into PR-BODY.md
- Tools: Verilator 5.050 (the CI pin) through a scratch wrapper that turns the Makefiles'
  `-j 0` into `-j 8` (this host reports 128 hardware threads to C++, so `-j 0` would spawn
  128 compile jobs); yosys 0.66; sv2v 0.0.13. Heavy runs one at a time.

## Commits on `9185c491` (one-line subjects, no body, no trailers)

| Commit | Item |
|---|---|
| `cae09882` | 1. merge of `main` `b2db3a97` (merge commit), the flag's resolution |
| `9c9431a` | 1. AD5 (restored configuration), AD6 (roll-back), two mutants, four patches refreshed, docs |
| `c9f915eb` | 2. R406-1 F-1: AD7 and `cfg-valid-no-reset`, the tables |
| `b27e0389` | the gate mutant's full pp_top record re-measured at the merged head (README only) |
| `20ec92b7` | the AD helper `clock()` renamed `graded_step()`: the parent's `measure_test_evidence.py --check` read it as the C library's `clock()` (C_CLOCK pattern) and failed 4 > 3 wall-clock files at `b27e0389`; 3 <= 3 after |

## Item 1. Merge of main `b2db3a97`

Merge commit `cae09882` (parents `9185c491`, `b2db3a97`; a merge, no rebase). Main added
PR #132 (D3 lane 1: `KL_aecp_nvm_writer`, the saved-state writer on the AECP engine's state
bus) and PR #133 (C1: SRP/MRP timers). Two files conflicted, as the manager's test merge said.

Resolution, file:line at the merge commit:

- `hdl/aecp/KL_aecp_engine.sv`, hunk 1 (store row): main's `u_dyn_didx_w`/`dyn_didx_w`
  (`:1782-1785`, `dyn_didx_w = d3_bus_w ? d3_sb_didx_w : u_dyn_didx_w`) replaces the
  branch's `dyn_ix_w`. The branch's flag block `dyn_cfg_valid` (`:1787-1814`) is kept and
  now decodes the bus the store takes, after the writer's 2:1 selection:
  `st_req_w`/`st_we_w`/`st_addr_w` are post-selection (`:1554-1557`), and the row is
  `dyn_didx_w == 0` (`:1809`), so a writer-owned access is judged by the writer's row
  (`sb_didx_o`, `KL_aecp_nvm_writer.sv:1087`). Its reset is now the store's own
  `store_rst_n_w` (`:1804`; `:1545` is `rst_n && !d3_rb_rst_w`, the store's `.rst_n` at
  `:1824`), so the D3 roll-back clears the flag with the row. The store's flag it mirrors:
  `take_wr_w` (`KL_aecp_dyn_state.sv:266`), count 1 for the selector (`:206`), set at
  `:329-330`, cleared at `:292`.
- `hdl/aecp/KL_aecp_engine.sv`, hunk 2 (`u_dyn` port): main's `.desc_index_i (dyn_didx_w)`
  with its comment (`:1832-1839`). The port comment of `dyn_cur_config_v_o` (`:648-654`)
  names both writers and both clears.
- `tb/pp_top/sim_main.cpp`, `main()` (`:10200-10211`): main's `--d3-only` and `--dr3a`
  with the branch's `--adp-only`; one `one_section` flag; main's order kept (Suite, GI, NW,
  D3), AD last. Every other file auto-merged (docs 02/04/09, integrator, top, ADP engine,
  `tb/pp_top/Makefile`, `tb/pp_top/README.md`); read and consistent.

**Can the restore walk write the configuration selector at row 0? Yes**, so the flag follows
that write (arm AD5 below):
record 0 is group 0, the configuration (`KL_aecp_nvm_writer.sv:336-343`, `:459-460`);
pass 1's rule for it is W_NCFG (`:734`), accepted when the value is below
configurations_count (`:616`), then W_APPLY (`:804`) drives `sb_we_o` (`:1084`), address
`{RGN_DYN_C, selector 0}` (`:847`) and `sb_didx_o = ridx_w = 0` (`:1087`), while
`bus_o` (`:1078`) selects it onto the store's bus. A pass-1 abort after that write rolls
back both stores (`rb_rst_o`, `:1106`; engine `:1545`), which is why the flag's reset had
to become the store's (arm AD6 below). ADP is enabled only after both walks
(`protocol_processor_top.sv:1707`), so the first ENTITY_AVAILABLE after a restore is built
after the write.

Merge-state check before the commit: `make -C tb/pp_top adp-config` AD 34/0;
`Vpp_top_sim --d3-only` D3 133/0; `./scripts/lint_hdl.sh` rc 0.

Commit `9c9431a` (item 1's tests). Clauses: IEEE 1722.1-2021 §6.2.2.18 (the ADPDU carries
the current configuration), §7.4.8.2 (GET_CONFIGURATION answers it); Milan v1.2 §5.6.2
note; the parent D3 contract §8.6 (the roll-back), as `KL_aecp_nvm_writer.sv` cites it.

- `tb/pp_top/sim_main.cpp` `AdpConfigPhase`: `reboot()` (a power cycle through both restore
  walks), `clock()` (renamed `graded_step()` in `20ec92b7`; counts clocks where the flag the ADPDU reads, new wrap tap
  `dbg_adp_cfg_v_o` = `u_dut.aecp_cur_cfg_v_w`, differs from the store's
  `dbg_dyn_cfg_v_o`), `first_advert_agrees()` (first ENTITY_AVAILABLE byte-exact, the
  flag equal in every clock from the reset, GET_CONFIGURATION, ENTITY.current_configuration).
  - **AD5, the restored configuration (the assignment's arm):** SET_CONFIGURATION(0)
    saved to record 0x00 (premise: the device's bytes equal `d3_record(0x00, 0, 2)`), power
    cycle keeping the device, the restore writes the row valid 0, and the first
    ENTITY_AVAILABLE, GET_CONFIGURATION and ENTITY all say 0 (image default 1).
  - **AD6, the roll-back:** record 0x00 applied in pass 1, then record 0x50 (read whole in
    pass 0, erased before pass 1; D3R4's shape) aborts with cause 5; roll-back; all three
    views fall back to 1.
- Mutants (both KILLED): `cfg-valid-ucpu-bus` (the flag on the µCPU's side of the
  selection, the branch's decode as it was) fails AD5 x2 and AD6 (3);
  `cfg-valid-hard-reset` (the flag reset on `rst_n` only, the pre-merge reset) fails AD6 x2
  (2). An arm using `u_dyn_didx_w` as the row for a writer access is equivalent and not
  armed: the writer writes the store only in its boot restore, where no command has run
  since reset and `u_dyn_didx_w` is 0 (`scfg_r`/`desc_ix_r` at reset), so the rows agree.
- Refreshed at the merge (context moved): `cfg-valid-any-selector`, `cfg-valid-not-sticky`
  (engine), `cfg-overlay-only`, `cfg-nonzero-for-valid` (top, after the comment edit).
- Docs: `protocol_processor_top.sv` `current_cfg_i` port comment and the selection's block
  comment; integrator §6; 02 §2 rule 4; 04 §3 row; 09 §8.1 row; `tb/pp_top/README.md` AD;
  `tb/adp_engine/README.md` campaign table (29 of 29).
- At `9c9431a` (tree state before commit): AD 48/0; full campaign 2 controls + 29/29
  KILLED; `make check` rc 0.

## Item 2. R406-1 F-1

Commit `c9f915eb` (required outcome items 1-3). No RTL change.

1. **pp_top reset arm, AD7** (`tb/pp_top/sim_main.cpp`,
   `AdpConfigPhase::a_reset_returns_to_the_image_default`): SET_CONFIGURATION(0) SUCCESS
   (non-default; premise: GET reads 0, the published flag set, the device idle), then
   `reboot(true, ...)`: `rst_n` pulsed with an erased device, both restore walks (premise:
   the row unset, `restore_blank_o`), link and enable. The first ENTITY_AVAILABLE is
   byte-exact `avail(0, 1)`, GET_CONFIGURATION reads 1, ENTITY.current_configuration reads
   1, and the flag the ADPDU reads equals the store's in every clock from the reset.
   Why an erased device: after the merge a reset over a device holding the saved record
   restores it (AD5, correct), which would hide the flop's reset; with nothing to restore
   the only thing that returns the ADPDU to the image default is the flag's own reset.
2. **Mutation arm `cfg-valid-no-reset`** (`tb/adp_engine/mutations/cfg-valid-no-reset.patch`,
   `mutants.py` expects `AD7`): KILLED, 5 failures: AD7 x2 (advert carries the overlay's
   reset 0 while GET reads 1; flag split 68,768 clocks), AD6 x2, AD5's flag split
   (965 clocks, until the restore writes the row).
3. **Tables:** `tb/adp_engine/README.md` campaign table gains the row (30 of 30), and the
   other pp_top rows carry their new counts; the PR body's mutation table (Round 2 section)
   gains it. `tb/pp_top/README.md` AD and 09 §8.1 name AD7.

At the tree state before this commit: AD 55/0; the 10 pp_top arms KILLED (control PASS).

## Item 3. Parent-visible list at the merged head (as in PR-BODY.md, Round 2)

Re-read at `20ec92b7` against `main` `b2db3a97` and the parent at dev `ec0cc0c1` (read-only
greps of the trusted checkout; the rest measured in the scratch parent):

1. This lane's interface change is unchanged: `KL_aecp_engine` gains `dyn_cur_config_v_o`,
   instantiated only by the processor top; `git grep` of the parent at `ec0cc0c1` finds no
   instance of `KL_aecp_engine` (prose only, `hdl/milan/KL_pp_shadow.sv:40,219,488`).
   Comment-stripped module headers, `b2db3a97` against `20ec92b7`: identical for
   `protocol_processor_top` (1,024 tokens), `KL_aecp_dyn_state`, `KL_acmp_nvm_shadow`,
   `KL_pp_nvm_port`, `KL_pp_nvm_mgr_arb`, `KL_aecp_nvm_writer`, `KL_adp_engine`;
   `KL_aecp_engine` +1 output. The new wrap tap `dbg_adp_cfg_v_o` is in
   `tb/pp_top/pp_top_wrap.sv`, which the parent does not use.
2. What the merge brings (not this lane's): PR #132's "Parent-visible for pin adoption:
   rounds 1-6, consolidated" and PR #133's section 4 (C1), with #133's composed-head note
   (their code edits share no parent file; their docs meet in
   `tb/verilator/milan_dp/README.md`). The manager's combined patch
   `parent-adaptation-132-c1.patch` (sha256 `2ba6680373831206006933dddf7c97615f4870526c476a5b371b995702ddc420`, 18,135 B,
   13 parent files)
   carries the code edits; this lane adds no parent edit (16 of 16 with that patch alone).
3. `current_cfg_i`: the image default while the configuration row is unset (from reset, and
   after a D3 roll-back); while the row is written (SET_CONFIGURATION, or the D3 restore of
   record 0x00) the ADPDU carries `aecp_cur_config_o`. Parent: `current_cfg_i` from
   ADP_IDX0 (`hdl/common/csr/milan_csr.sv:319,2819`, reset 0 at `:1586`,
   `milan_datapath.sv:7602`), one configuration (`sw/builder/test_builder.py:25328`), so the
   only legal SET is 0 and the restore's rule accepts only a saved 0: the wire is unchanged
   while ADP_IDX0 is 0. Round 1's notes stand (milan_dp's configuration-face [GAP];
   `KL_pp_shadow.sv:259`'s comment at adoption).
4. Test-evidence ratchet at `ec0cc0c1` + the patch, gitlink `20ec92b7`: PASS, 74 <= 77
   suites without an arm, 10 <= 10 unseeded draws, 0 <= 0 unexplained readers, 3 <= 3
   wall-clock files. At `b27e0389` it failed 4 > 3 on this lane's `clock()` helper (fixed
   in `20ec92b7`).
5. Entry points: `make -C tb/adp_engine mutants` (CI; 30 arms) and
   `make -C tb/pp_top adp-config` (AD0-AD7); the merge brings `--d3-only`, `--dr3a`,
   `tb/pp_top/d3_mutants.py`.
6. Optional matrix citations (`docs/reference/MILAN_COMPLIANCE_MATRIX.md:154`, 5.6.3/5.6.4):
   the MTXW walk; a 5.6.1/5.6.2 citation can use P12/AD0 and P11/AD1-AD7.

## Suite table at `20ec92b7` (`./scripts/run_suites.sh` rc 0, 7 min 30 s)

33 suites, 1,017,162 checks, 0 failing; tallies identical to the run at `c9f915eb`.
This lane's two suites: adp_engine 1,367 (main 533); pp_top 7,944 = main's 7,888 (measured:
`make -C tb/pp_top` rc 0 on a `git archive` of `b2db3a97`, 7888 checks) + section AD's 55
(AD0-AD7; was 34) + S3's pre-flush check 1. The
others: acmp_listener 2544, acmp_nvm 360, acmp_talker 1342, aecp_notify 10, ca_originator
16, desc_mem_guard 78, desc_store 584, dispatch 211, dyn_state 118, event_router 81,
lsn_admit 18, maap 75, nvm_port 136, originator 104, prng 76, release_merge 18, resp_buf 64,
rx_slots 130, rx_validator 437, scoreboard 3705, side_port 368, srp_admission 991231,
srp_decoder 190, srp_encoder 581, srp_stream_fsms 1219, srp_top 2200, timer_map 1360,
timer_service 48, tx_arbiter 66, tx_slots 95, ucpu 386.

Other entry points at `20ec92b7`: `lint_hdl.sh` rc 0 (41 modules), `make check` rc 0,
`gen_matrix.py --check` rc 0 (94 rows, 0 untested), `check_upc_map.py` rc 0 (in
run_suites), `git diff --check c951a9ff..HEAD` and `b2db3a97..HEAD` rc 0,
`syn/yosys/run.sh` rc 0 (36 tops + the Xilinx memory map), `make -C tb/nvm_port figures`
rc 0 (after `git fetch --no-tags origin refs/pull/13/head`, as CI does).

## Mutant table

| Campaign | Head | rc | Result |
|---|---|---:|---|
| `make -C tb/adp_engine mutants` | `20ec92b7` | 0 | 2 controls PASS, 30/30 KILLED by the named checks; counts equal `tb/adp_engine/README.md` (identical to the run at `c9f915eb`) |
| full default pp_top under `gate-enable-dropped` (scratch `git archive`, patch applied) | `c9f915eb` (recorded by `b27e0389`) | 2 (expected) | 4 of 7,924: AD0 x2, AD1b, D3R14 (`FAIL` lines in `gate-full.log`) |
| `make -C tb/srp_top mutants` | `20ec92b7` | 0 | 11 controls PASS, 90/90 checks, assertion coverage 65/65 |
| `tb/pp_top/gsi_mutants.py` | `20ec92b7` | 0 | 20 detected by named checks; golden and restored PASS |
| `tb/pp_top/name_wr_mutant.py` | `20ec92b7` | 0 | decode killed; golden and restored PASS |
| `tb/pp_top/d3_mutants.py --jobs 1` | `20ec92b7` | 0 | 83 of 83 KILLED by their named checks; the three goldens (pp_top, acmp_nvm, rx_validator) PASS (78 min) |
| `tb/acmp_talker/retry_mutants.py` | `20ec92b7` | 0 | 62 killed; 7 equivalence and 1 performance controls; baseline and restored rc 0 |
| `tb/srp_admission/mutants.py` | `20ec92b7` | 0 | 12 of 12 |
| `tb/desc_mem_guard/mutate.py` | `20ec92b7` | 0 | hold-deleted mutant detected by the completed byte assertion |

Also at `20ec92b7`: `make -C tb/acmp_talker lint` rc 0, `make -C tb/prng lint` rc 0, and
`make -C tb/desc_mem_guard baseline` rc 2 as its README expects (the store without the guard:
17 PASS, 1 FAIL, `third locate late_beats_never_served`, the README's wrong bytes
`00060000deadbeef cafef00d01234567`). The other extra targets (`desc_store`
generator-check, `srp_admission` and `timer_map` shapes, `pp_top` fixture-guards) are in
their suites' default targets, so `run_suites.sh` ran them.

## Parent consumer gate table (scratch parent: milan-fpga dev `ec0cc0c1`, gitlink `20ec92b7`)

Scratch: `$VALIDATION_STORAGE/a451-parent-ec0cc0c1`, a `git archive` of the trusted checkout at
`ec0cc0c1` (tree equal to it apart from the gitlink), `git init` with the four gitlinks,
`external` `efeb541`, `gptp-processor` `5dce647`, `third_party/verilog-axis` `48ff7a7` cloned
read-only from their remotes at the pins, `protocol-processor` cloned from this lane at
`20ec92b7`; `git submodule status` all at pins. `parent-adaptation-132-c1.patch` applied with
`git apply` (the working-tree diff equals the patch apart from index-hash length). The
trusted checkout was never modified.

| # | Command | rc | Note |
|---:|---|---:|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | every refused count 0, ratchets hold |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | |
| 3 | `python3 scripts/xvlog_gate.py --check` | 0 | 4 == ratchet, all predating this lane (notify, originator, rx_validator, top `srp_class_a_prio_w`) |
| 4 | `python3 scripts/check_rtl_source_lists.py` | 0 | protocol-processor 36/42 tops, 6 recorded |
| 5 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | |
| 6 | `python3 sw/builder/test_builder.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11: placement report absent on host), 16 min |
| 7 | `make -C tb/verilator/pp_shadow -j8` | 0 | four builds: 595, 595, 635, 295 checks, 0 failures |
| 8 | `python3 scripts/check_port_contracts.py` | 0 | protocol-processor 111 <= 111 undocumented |
| 9 | `python3 scripts/measure_naming.py --check` | 0 | 96 recorded |
| 10 | `python3 scripts/measure_test_evidence.py --check` | 0 | 74 <= 77, 10 <= 10, 0 <= 0 readers, 3 <= 3 wall-clock (failed 4 > 3 at `b27e0389`, fixed by `20ec92b7`) |
| 11 | `python3 scripts/docs_check.py` | 0 | 0 findings |
| 12 | `python3 scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | 0 PINMISSING, 85 warnings (PR #132's figure) |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j8` | 0 | every leg 0 failures (gmstep 103, notify 378, nxn 1,841, ...), 24 min |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | 65/65, 152/152, 5/5 |

Commands 1, 2, 4, 5, 8-11 ran first at gitlink `b27e0389` (10 failed there, see above) and
again at `20ec92b7`; 3, 6, 7 and 12-16 ran only at `20ec92b7`.

## Evidence logs (scratch `$VALIDATION_STORAGE/a451/`, not copied here; sha256 prefix, bytes)

| Log | sha256 (16) | Bytes |
|---|---|---:|
| final-suites.log | f63e273cb00171cf | 1649 |
| final-lint.log | 9a3703ba1ec6767b | 1056 |
| final-check.log | 093bf184dcfa67b2 | 225 |
| final-matrix.log | 7a2c98136a0892f1 | 33 |
| final-yosys.log | c32a850cfbbbfda5 | 25840 |
| final-adpmut.log | 280703257cc046ff | 16005 |
| final-srptop.log | 6d06b27f894e0702 | 5732 |
| final-nvmfig.log | 072ee387eb8a5a40 | 3605 |
| final-gsimut.log | 5f6d67707db7bfed | 4150 |
| final-nwmut.log | 055560a7d55d359d | 2550 |
| final-d3mut.log | aff9b2a1c30354f1 | 6042 |
| final-retry.log | 7bda8adf83703e45 | 3865 |
| final-srpadm.log | 6977d367d954c85c | 479 |
| final-dmgmut.log | de87349d19f11f7b | 129 |
| final-dmg-baseline.log | abed87546fc10be1 | 4872 |
| gate-full.log (gate mutant, full pp_top, `c9f915eb`) | d89f07ca780694d0 | 32949 |
| main-pptop.log (pp_top at `b2db3a97`) | 3c46c0d3d54335b5 | 57024 |
| mut-item1-full.log (campaign before `9c9431a`) | c6515dcfc73afde3 | 14960 |
| merge-adpcfg.log (AD at the merge state) | 2fd327f3ee7ccd01 | 23623 |
| merge-d3.log (D3 at the merge state) | 209b0b8ee401165d | 92 |
| pg/01..16.log (parent gates, numbered as the table) | 15.log 06ce8f4881b1db64 | 2006917 (15), 302475 (07), 158800 (16), others < 100 KB |

## What remains

- #85 item 4 (available_index interop against a live controller): bench lane; #85 stays open.
- AEM_CONFIGURATION_INDEX_VALID (R406-1 S-1, R407-1 O1): manager decision, unchanged.
- Suggestions not in the assignment, not taken: R407-1 S1 (F04.3 domain-mismatch fresh-index
  row), S2's refused-SET leg, S3's blank line in 09; R406-1 S-3 (graded-cell counts).
  R406-1 S-2 and R407-1 S3's "until reset" are covered by item 1's doc edits.
- Hosted CI and the delta reviews. No hardware used. No push, no PR edit (the PR body for
  the manager is `PR-BODY.md` here).
