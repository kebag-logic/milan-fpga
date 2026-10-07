[R530] NEGATIVE - exact head 4f6216abff01b6f859d348aaf6a71e47c5a5a2a8

Internal cleared-context review R530-2 of issue #665 lane F3, PR #688, at exact head `4f6216abff01b6f859d348aaf6a71e47c5a5a2a8` (tree `ff7dc21ef660db87721e80f59c498f925708c04e`). This round reviews the delta `351ae81f..4f6216ab`: two `--no-ff` merges (FC round 2 `db9aa8c9`, dev `910f338d`), round 2 (the `adp` bound-talker term and the R530-1/R531-1 fixes) and round 3 (the table in distributed RAM).

## Verdict

NEGATIVE. Three MINOR findings are open: F1 (Tests), F2 (Conformance, Docs) and F3 (Docs).

- **RTL is clean.** The bound-talker table in distributed RAM is correct as far as I could probe it. The byte-serial compare over wire bytes 18 to 25, the copier, reset, `BOUND_EN`, interface selection, both adapters and `run-if2` all behave as documented.
- **Every round-1 finding is resolved at its root.** That covers all eleven: R530-1 F1 to F5 and R1, and R531-1 F1 to F5. Each was re-probed with my own planted defects.
- **What keeps the verdict NEGATIVE:**
  - F1: two of my interface mix-up defects escape the lane's suite.
  - F2: the linked-image size report owed under acceptance addition 6030870481 is missing.
  - F3: one stale latency figure in the design doc.
- Three RESIDUE items and three SUGGESTIONs are listed. None of them affects the verdict.

## Findings

### R530-2-F1 MINOR (Tests): two interface mix-ups in the bound-talker term escape the mailbox suite

- **Where:**
  - The timing checks run on interface 0 only: `tb/verilator/mbx/suite.hpp:1494-1553` (`check_bound_timing`, Q18 to Q21), through `offer_stalled`, which hard-codes interface 0 (`suite.hpp:230`, `:233`).
  - Every bound-talker check offers one frame and drains it before the next (`offer()`, `suite.hpp:194-216`; Q13 at `:1383-1410`).
  - The RTL lines left ungraded:
    - `hdl/milan/mailbox/KL_mbx_rx.sv:306`: the verdict's table is the latched `if_r`.
    - `KL_mbx_rx.sv:309`: liveness reads the owed flag of the frame's interface.
- **Authority/evidence:**
  - The assignment asks for the term's checks and planted defects "on both adapters and `run-if2`" (6030067436). It also asks for a planted defect for each check (6026721148).
  - Round 3 introduced two new interface-dependent mechanisms:
    - an entry is live only while no copy of it is owed, per interface;
    - the verdict now reads per-entry match flags at FIN, after the last byte, while the next frame (and its `rx_if_i`) may already be presented.
  - Two reviewer-planted defects keep every check of the suite green (`receipts/rtl_probes.log`):
    - `X13-frame-table-from-live-if-input`: the table is chosen from `rx_if_i` instead of the latched `if_r`. It escapes at one and at two interfaces, 380/380.
    - `X17-live-of-other-interface-if2`: interface 1's liveness reads interface 0's owed flag. It escapes at two interfaces, 380/380.
  - Both are real defects, not equivalent mutants. I added two checks to a disposable copy of the suite (`scripts/r530_2_suite_patch.py`):
    - RV1: a bound talker's ENTITY_AVAILABLE on interface 0 with the next frame, index 1, queued right behind it.
    - RV2: Q19 repeated on interface 1.
  - The head passes them: 381/426 at one interface and 383/428 at two, Wishbone and AXI4-Lite (`receipts/rv_suite_controls.log`). X13 fails RV1 at one and at two interfaces, and X17 fails RV2 (`receipts/rv_suite_escapes.log`).
- **Impact:** a regression that breaks admission is graded green by every check. Two cases matter in the two-interface (redundancy-path) build:
  - back-to-back announcements on different interfaces;
  - a frame whose identity overlaps a copy on interface 1.
  The silent result is a dropped bound talker's ENTITY_AVAILABLE, and so a false TMR_NO_ADP, or a match against a half-copied identity.
- **Required outcome:** the suite grades both mechanisms through both adapters:
  - the arrival interface held to the verdict with the next frame presented on another interface (or index);
  - the owed-copy gating on an interface other than 0 under `run-if2`.
  Each check gets a planted defect in `mutants.py` (X13 and X17, or equivalents) that fails it by name.
- **Verification:** X13 (one and two interfaces) and X17 (two interfaces) from `scripts/r530_2_rtl_probes.py` fail named checks. `mutants.py` stays at N of N caught with its controls.

### R530-2-F2 MINOR (Conformance, Docs): the linked RV32 image of the composed `ctrl_app` is not reported (acceptance addition 6030870481)

- **Where:** the round-3 handoff (`review-evidence/665f3-r1/author-r3/HANDOFF.md`, gate table and lines 248-250) and the PR body report object sizes only: "RV32I text 25,888 bytes ... data 0, bss 170".
- **Authority/evidence:** #665 comment 6030870481 is an "Acceptance addition for every F-lane". It requires each lane to report "the linked RV32 image of the composed `ctrl_app` at its head: text, rodata, data and bss, plus the static pools sized from the entity model ... for the shipping shape and the largest supported shape, with the delta from its base". It says explicitly that "Today the F-lanes report object sizes only". The manager applied it to F2 (6033552374 item 4) and to F4 (6033558691, R533-1-F4). I found no linked-image figure for F3 in the issue, the PR body, the handoff or the docs at this head.
- **Impact:**
  - F3 adds the largest firmware block so far: ACMP object text grew from 11,756 to 25,888 bytes.
  - The block-RAM budget (about 128 KB) cannot be tracked for the default flip without a linked image and its static pools.
  - The lane's acceptance is not met as stated.
- **Required outcome:** report the linked `ctrl_app` image at the head (text, rodata, data, bss and static pools) for the shipping and the largest supported shape, with the delta from the base. Otherwise, the manager publicly schedules this item for F3's merge round.
- **Verification:** the figures and the command that produced them appear in the PR or issue evidence.

### R530-2-F3 MINOR (Docs): a stale per-access figure in the design doc's open items

- **Where:** `docs/design/MAILBOX_SPLIT.md:920`: "ACMP's backlog bounds fit T_svc only at 0.92 us per access or less".
- **Authority/evidence:**
  - Round 2 raised the full-acmp-ring bound from 10,835 to 10,956 accesses. The table at `MAILBOX_SPLIT.md:662` now gives 0.91 us (10 ms / 10,956 = 0.913 us), and so do the PR body and REVIEW READY 6032434205.
  - The open item still carries round 1's 0.92 us (blame: commit `6afca717`, unchanged since).
  - I recomputed every table row (2,988; 10,956; 21,912; 8,964) against 10 ms and the 20 ms ceiling, and each matches its column.
- **Impact:** the authoritative design doc states two different access-time limits for the same bound. This is a figure, not wording.
- **Required outcome:** the open item states 0.91 us, or derives it from the table.
- **Verification:** read `MAILBOX_SPLIT.md` "Open items" against the "ACMP service latency" table.

### R530-2-R1 RESIDUE (Docs): the area open item predates the ruling

- **Where:** `docs/design/MAILBOX_SPLIT.md:925-927`: "the two contract changes measured there are the owner's to take or refuse".
- **Evidence:** ruling 6033962557 accepted +357 LUT / +86 FF as measured and refused both contract changes. This is status prose only.
- **Exact fix:** "**The bound-talker term's area** is 57 LUTs over its target of 300 ([Measured area](#measured-area)), accepted as measured on #665 (6033962557); the two measured contract changes were not taken."

### R530-2-R2 RESIDUE (Docs): the contents line for "Open items" still lists the decided adp term

- **Where:** `docs/design/MAILBOX_SPLIT.md:33`: "The datapath tap, the adp channel's AVAILABLE and DEPARTING term, lwSRP's transmit hook, ...".
- **Evidence:** the section no longer has that item (decided in 6029368753 and implemented by this PR). It now carries the term's area instead. The TOC gate passes, so this is wording only.
- **Exact fix:** "The datapath tap, lwSRP's transmit hook, the CPU-cycle measurement with what ACMP's bounds need of it, ACMP's wire round trip, the bound-talker term's area and MMRP."

### R530-2-R3 RESIDUE (Docs): the PR body's status predates the ruling

- **Where:** PR #688 body:
  - Status: "BLOCKED at `4f6216ab...` (round 3, area) ... ends in a STOP on #665 (comment 6033939473) for a decision";
  - Known limitations: "Those are contract changes, the owner's to take or refuse (the STOP on #665)".
- **Evidence:** ruling 6033962557. This is wording in the PR body.
- **Exact fix:**
  - Status: "Round 3 (area) at `4f6216ab`: the term costs 357 LUT and 86 FF against a target of 300 and 120, accepted as measured on #665 (6033962557)."
  - Known limitations: "Those are contract changes; the ruling on #665 (6033962557) did not take them."

### Suggestions (optional; no lens effect)

- **S1.** Publish the round-3 OOC `report_utilization -hierarchical` and timing summary, or their exact-head excerpts. Today only a sha256 of a report kept in the author's scratch is recorded (HANDOFF "Measured area").
- **S2.** State the copy semantics in the contract's `BOUND_EN` doc (`mailbox.yaml`, and so `MAILBOX_CONTRACT.md`):
  - an entry takes part once the fabric has copied it;
  - setting `BOUND_EN`, or writing `BOUND_EID` while it is set, suspends the entry for that window.
  Also state the general bound, about 11 x interfaces x entries clocks plus one per host access to the tables. "176 clocks" holds for one interface's sixteen entries only. The host model has no such window, and Q18 to Q21 are RTL-only as documented.
- **S3.** Add the unlisted blocks to the area table so the rows sum to the totals. They are 21, 21 and 15 LUT (`receipts/area_record.log`).

## Prior public review findings at this head (read after my own pass)

| Finding | Status at `4f6216ab` | Evidence |
|---|---|---|
| R531-1-F1 MAJOR, AVTP version | RESOLVED | `acmp.c:986`, `:1034` check `AVTP_VERSION` before any decode. A26 covers versions 1 to 7: commands, responses, AVAILABLE and DEPARTING. B9 runs it through the adapter. My probes FW14 (mask reads bit 4 only) and FW15 (check bypassed when sinks exist) are caught (`receipts/fw_probes.log`). |
| R531-1-F2 MAJOR, TMR_NO_RESP from the accepted send | RESOLVED | `acmp.c:660-698` (`timer_held`, `probe_left` matched on sink and sequence_id), `sm_running` in `rearm` and expiry. A27 has three tests. My probes FW6 (sequence check dropped), FW7 (stop keeps the hold) and FW8 (held deadline counted for the earliest) are caught. |
| R531-1-F3 MINOR, slot range | RESOLVED | `acmp_mbx.c:71` compares and never sums. The B7 test covers the last legal value, the first illegal one, 0x100, the truncating values and UINT_MAX (`test_acmp_mbx.cpp:416-417`). FW11 (off by one) and FW12 (summed form) are caught at one and two interfaces. |
| R531-1-F4 MINOR, owed-frame conclusion | RESOLVED | `MAILBOX_SPLIT.md:666-672` states that the owed-frame bound (8,964) fits at 1 us. All four rows recomputed. (A separate stale figure is F3 above.) |
| R531-1-F5 MINOR, poll contract | RESOLVED | `acmp.h:424-425` carries the reviewer's exact text. |
| R530-1-F1 MINOR, two-interface adapter | RESOLVED | The `acmpif2` arm passes with 19 tests at two interfaces. My FW17 (one slot for every interface) fails B3 at two interfaces, and FW2 (admit on interface 0) fails `acmpif2` (`receipts/fw_probes_r530_1_roots.log`, `fw_probes.log`). |
| R530-1-F2 MINOR, BINDING layout pin | RESOLVED | A24 pins flags 0x01, 0x03 and 0x05 byte for byte against `KL_acmp_nvm_shadow.sv:484` (`{5'd0, sw, started, vld}`) and refuses other lengths. My FW18 (symmetric flag swap) and FW19 (longer record applied) are caught. |
| R530-1-F3 MINOR, D3 roll-back | RESOLVED | N7 (`test_acmp_nvm.cpp:250`). My FW13 (a D3 roll-back drops the bindings) fails `acmpnvm`. |
| R530-1-F4 MINOR, 32-bit wrap | RESOLVED | A28 has two tests. My FW9 (`due` unsigned) and FW10 (`earliest` unsigned) are caught. |
| R530-1-F5 MINOR, TD1 ruling text | RESOLVED | `MAILBOX_SPLIT.md:683-707`, `sw/firmware/ctrl/README.md:128-141`, `acmp_walk.cpp:43-60`, `acmp.h` and the PR body all match the ruling: 5.5.4.2 governs and 5.5.2.7 is an overview. `KL_acmp_talker.sv:1301-1306` is cited as read from source, and I confirmed those lines are the DISCONNECT_TX arm. "Field for field" is limited to LD1 to LD3. |
| R530-1-R1 RESIDUE, adp term "open decision" | RESOLVED | No "open decision" phrasing remains in `MAILBOX_SPLIT.md`, the ctrl README or the PR body. (The TOC remnant is R2 above.) |
| Run-cosim relink (decision 6029368753) | RESOLVED | `tb/verilator/mbx/Makefile:65-80`. In a built copy, a firmware-only planted defect made `make run-cosim` relink and fail ("the firmware answered ACMP on the model", rc 2). Restored, it passed 32/32 (`receipts/cosim_relink_*.log`). |

## What each lens examined

### Conformance

- **Decision 6029368753, bound talkers only.**
  - Contract 2.1 (`mailbox.yaml`) adds term 2 `eq_bound` with offset 18, message types 0 and 1, and field `entity_id`.
  - `MAILBOX_CONTRACT.md` regenerates; `gen_mailbox.py --check --crosscheck` reports 0 findings and `--selftest` 0 failed.
  - The RTL compares wire bytes 18 to 25 big-endian against `BOUND_EID_HI:LO`. I derived this from the copier: step s shifts in byte 7 - s, so tap b is identity byte b.
  - Q12 refuses ENTITY_DISCOVER and every other message type for a bound talker; both the eq_zero and eq_own DISCOVER terms still pass.
- **Milan v1.2 5.6.4.1.**
  - The core still filters exactly by bound state, interface and talker (`acmp.c:1052`).
  - The admit port keeps the table equal to each bound sink's talker (`acmp.c:441-452`). It writes EN=0, LO, HI, EN=1 on a bind or rebind and EN=0 on an unbind (`mbx.c:118-134`; D13).
  - Restored bindings are written at `ctrl_app_open` (A29; my FW16 is caught).
- **AVTP version and TMR_NO_RESP (5.5.3.5.3 steps 5 to 7, 5.5.3.5.16):** as in the table above.
- **Scope.**
  - The lane delta changes RTL only in `hdl/milan/mailbox` (`git diff b03929fc..head`).
  - `sw/litex`, `sw/builder`, `configs`, `constraints` and `syn` are unchanged against the FC head.
  - The `KL_mbx`, `KL_mbx_wb` and `KL_mbx_axil` port lists are identical to FC round 2.
  - The mailbox is instantiated only under `ctrl_mailbox` (`sw/litex/milan_soc.py:3293-3295`, default `False` at `:2590`). The default all-fabric build and the shipping image are therefore unchanged.
  - The merges' conflict resolutions (`git show --remerge-diff`) touch only README text and an import list, and they keep both sides.
- **Unclean:** F2.

### RTL

`KL_mbx_rx.sv:217-360` read line by line:

- **Table and compare.**
  - Distributed-RAM read-back memory with asynchronous read, shared by host and copier with the host first.
  - Per-entry SRL taps addressed by `cnt_r - BO_C`.
  - Match flags are armed at byte 18, ANDed per byte, and lost in any cycle the entry is not live.
- **Copier.** An owed entry costs 10 clocks. A rewrite restarts the copy. Writes need all four strobes (`KL_mbx.sv:77`), so a host write cycle is never a copy step.
- **Reset.**
  - `en`, `vlo`, `vhi`, `owed`, the copier and the match flags clear.
  - The SRLs and the RAM keep their contents, but no entry is live until a copy completes.
  - Unwritten words read 0 and copy as 0.
- **Widths.** `KW_C` and `RW_C` are correct at one and two interfaces. The 5-bit entry decode is guarded: entries above 32 trigger an elaboration `$error`, and the generator refuses strides that are not powers of two. The `entry < N_BOUND` decode bound is redundant with stride 0x100/0x10: my X12 relaxes it and stays green, as an equivalent mutant should.
- **My RTL probes** (`scripts/r530_2_rtl_probes.py`, `receipts/rtl_probes.log`) cover wrong byte index, stale match flag, off-by-one entry and interface mix-up.
  - 15 of 19 non-equivalent probes are caught: X1 to X6, X8 to X11, X14 to X16, and X5 and X14 also through AXI4-Lite.
  - X7 (match flags not cleared by reset) is equivalent: the flags clear one clock after reset because no entry is live.
  - X13 and X17 escape the suite. The head handles both correctly (RV1/RV2 pass), so they are a Tests finding (F1), not RTL.
- **Area record.**
  - The block table sums to the stated totals once the unlisted 21/21/15 LUT are included.
  - The deltas give +357 LUT and +86 FF.
  - 128 SRL16E / 2 = 64 LUT, and (34 RAMD32 + 10 RAMS32) / 2 = 22 LUT; 64 + 22 + 271 = 357 (`receipts/area_record.log`).
  - WNS +0.402 ns is as reported. I did not re-run Vivado (see limits).
- **Lint and synthesis.** `lint_rtl.py --check` holds at the ratchet (90 <= 90). Yosys passes all three mailbox tops.
- **Clean.**

### Robustness

- Covered with the following evidence:
  - frames stalled inside the identity (Q18, Q19), host reads beside a copy (Q20), a rewrite at each of 32 clocks (Q21) and reset (Q17);
  - frames cut inside `entity_id` (Q12; my X6 is caught);
  - back-to-back frames on different interface indices, and the owed gating on interface 1 (my RV1 and RV2 pass at the head at one and two interfaces, through both adapters);
  - firmware boundaries at UINT_MAX, the 32-bit wrap, roll-back and owed probes past unbind or rebind (A27, A28, N7, B7).
- Host starvation of the copier is an acknowledged design limit (handoff risk 3), not a defect: the adapters leave every other cycle free.
- **Clean.**

### Tests

- At the head:
  - mbx suite: 380 (Wishbone), 425 (AXI4-Lite), 32 cosim, and 380/425/369 at two interfaces (`receipts/mbx_suite_head.log`, rc 0);
  - the lane's RTL campaign `mutants.py --jobs 2`: 141 of 141 caught with four controls (`receipts/mbx_mutants_head.log`);
  - `test_ctrl_firmware.py --require-rv32`: every arm PASS (`acmp` 78, `acmpwalk` 127, `acmpnvm` 7, `acmpif2` 19, `model` 23; `receipts/ctrl_fw_head.log`);
  - `fw_coverage.py --check --jobs 4`: `acmp.c` at 729/729 lines and 342/342 branches, `acmp_mbx.c` 73/73 and 26/26, `acmp_nvm.c` 38/38 and 10/10, `mbx.c` 185/185 and 68/68, 17 files PASS (`receipts/fw_coverage_check.log`).
- My 19 firmware probes (`scripts/r530_2_fw_probes.py`) are all caught.
- **Unclean:** F1.

### Docs

- Checked:
  - `MAILBOX_SPLIT.md` design, verification, area and open items;
  - `tb/verilator/mbx/README.md`, `sw/firmware/ctrl/README.md` and `sw/firmware/gtest/README.md`;
  - the contract doc;
  - the PR body and the handoff, against code and receipts.
- Gates:
  - `docs_check.py`: 0 findings;
  - `check_em_dash.py --base 910f338d`: 0 findings over 931 added lines;
  - `gen_toc.py --check`: OK;
  - the SV, Python and C++ idiom gates: OK.
  The two Markdown gates ran with the pinned renderer in a private scratch environment.
- **Unclean:** F2 (missing evidence) and F3. R1 to R3 are RESIDUE.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R530-2-F2) | `mailbox.yaml` 2.1, `MAILBOX_CONTRACT.md`, `KL_mbx_rx.sv:217-360`, `acmp.c:441-452`, `:660-698`, `:986`, `:1034`, `:1052`, `mbx.c:118-134`, `milan_soc.py:2590`, `:3293`, scope diffs, remerge-diffs, #665 6030870481 | R530-2 applied; not clean | `4f6216abff01b6f859d348aaf6a71e47c5a5a2a8` |
| RTL | CLEAN | `KL_mbx_rx.sv:86-360`, `KL_mbx.sv:71-135`, `:246-247`, `:512-525`, `mailbox_skeleton.py` round-3 diff, `receipts/rtl_probes.log`, `receipts/area_record.log`, `receipts/lint_rtl.log`, `receipts/yosys_mbx.log` | R530-2 | `4f6216abff01b6f859d348aaf6a71e47c5a5a2a8` |
| Robustness | CLEAN | `suite.hpp:1321-1553`, `receipts/rv_suite_controls.log` (RV1, RV2), A27, A28, B7, N7 in `receipts/ctrl_fw_head.log`, `receipts/fw_probes.log` | R530-2 | `4f6216abff01b6f859d348aaf6a71e47c5a5a2a8` |
| Tests | UNCLEAN (R530-2-F1) | `suite.hpp`, `mutants.py:297-400`, `receipts/mbx_suite_head.log`, `mbx_mutants_head.log`, `ctrl_fw_head.log`, `fw_coverage_check.log`, `rtl_probes.log`, `rv_suite_escapes.log`, `fw_probes*.log`, `cosim_relink_*.log` | R530-2 applied; not clean | `4f6216abff01b6f859d348aaf6a71e47c5a5a2a8` |
| Docs | UNCLEAN (R530-2-F2, R530-2-F3) | `MAILBOX_SPLIT.md:33`, `:576-610`, `:655-725`, `:846-927`, the three READMEs, PR body, `author-r3/HANDOFF.md`, `receipts/docs_check.log`, `em_dash.log`, `gen_toc.log` | R530-2 applied; not clean | `4f6216abff01b6f859d348aaf6a71e47c5a5a2a8` |

## Commands (each waited on in the foreground, with its own log and rc under `receipts/`)

- **mbx suite.** In a copy of the exact head, `make clean` then `make run-wb run-axil run-cosim run-if2` with the pinned Verilator 5.050 (identity checked: "Verilator 5.050 2026-07-01 rev v5.050"). Result rc 0.
- **Lane RTL campaign.** `python3 -B mutants.py --jobs 2`, rc 0.
- **Reviewer RTL probes.** `scripts/r530_2_rtl_probes.py --jobs 2`, rc 1 by design: it records the X13 and X17 escapes.
- **Reviewer suite checks.** `scripts/r530_2_suite_patch.py` (RV1, RV2, applied to a disposable copy only), then the controls (rc 0) and the escapes (rc 1: X13 and X17 caught, X7 equivalent).
- **Firmware gate.** `test_ctrl_firmware.py --require-rv32`, run in the review clone with builds in scratch. Result rc 0.
- **Coverage.** `fw_coverage.py --check --jobs 4`, rc 0.
- **Reviewer firmware probes.** `scripts/r530_2_fw_probes.py`, 16 of 16 caught, plus 3 of 3 for the R530-1 roots.
- **Relink check.** `make run-cosim` with a firmware-only planted defect (rc 2), then restored (rc 0, 32/32).
- **Contract generator.** `gen_mailbox.py --check --crosscheck` and `--selftest`, both rc 0.
- **Lint and synthesis.** `lint_rtl.py --check` and `syn/yosys/run.sh --top KL_mbx --top KL_mbx_wb --top KL_mbx_axil`, both rc 0.
- **Docs gates.** `docs_check.py`, `check_em_dash.py --base 910f338d`, `gen_toc.py --check` and the three idiom gates, all rc 0.
- **Clone state.** After every probe: HEAD, tree and index tree are `ff7dc21e`. The worktree and index are clean, with no untracked or ignored files. Tracked blob and mode digests are equal to HEAD's. The submodule gitlinks are unchanged and their worktrees clean (`receipts/clone_state.txt`).

## Real limits

- **Vivado not re-run.** I did not repeat the OOC place-and-route: other lanes' heavy builds were running on the host, and Vivado must not run beside them. The +357 LUT / +86 FF record was checked for internal consistency only, and the report it cites is not public (S1).
- **Full ctrl campaign not re-run.** The 348-defect `--self-test` campaign was not run. The firmware is unchanged in round 3. In its place: my 19 firmware probes, and the lane's RTL campaign re-run in full.
- **Not run:** the builder bank, `xvlog_gate.py` (no `xvlog` on PATH), hosted CI and `act` (not permitted), and physical calibration. Field skips are not hardware proof.
- **RV32 compiler.** The RV32 arm used the first compiler on the harness's candidate list (an ilp32 `riscv32-linux-gcc`), not a fresh CI SDK extraction.
- **Copy latency** is derived from the RTL. The access-time bounds (A4) remain unmeasured, as decided.

## Pending manager duties

- Rule on F1 to F3. The RESIDUE items R1 to R3 go to the residue checklist.
- Decide whether acceptance addition 6030870481 is owed at this round or at F3's merge round, and record that publicly (F2).
- At the merge turn: merge dev `d51b373a` (#677) and validate the candidate merge result on current dev, together with hosted and `act` acceptance on the exact head.
- Publish this report and the receipts listed in `MANIFEST.sha256`.

R530-2 FINISHED
