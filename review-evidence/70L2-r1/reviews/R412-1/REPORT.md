[R412] NEGATIVE - exact head 597dba8593553ad85b1e94936b016907c4d2003a

Round R412-1, internal independent review of kebag-logic/milan-fpga PR #623 (issue #70, lane 2: pin adoption of processor `b2db3a97` = PR #132 D3 lane 1 plus PR #133 lane C1).
Head `597dba8593553ad85b1e94936b016907c4d2003a`, tree `c0b06e6e3b9a39f8c8f555e89957edf9a920beff`, 21 commits on dev `79c36963660c10e4c1c11a744fb5bff41a552b8b`.

Verdict: NEGATIVE, on one open MAJOR (F1: Conformance, Robustness, Tests, Docs) and one open MINOR (F2: Tests).
RTL is covered clean at this head.
The product firmware, RTL glue, harness edits, ROM digests and documents otherwise meet the assignment, the scope record and the ruling.
Both findings are in tooling/tests (`sw/builder/test_builder.py`, `tb/verilator/fw_service_budget/run.py`) and in the prose that states their guarantees.
Neither fix needs an RTL, firmware or bitstream change.

## Sources reconstructed, in order

1. `AGENTS.md`, `CONTRIBUTING.md` (section 3 verification bar), `docs/README.md`.
2. Issue #70 body; assignment 5888775832; scope record 5880276193; STOP 5894165470; ruling 5894183475 (option 1 plus the `b2db3a97` adoption); REVIEW READY 5902107952; PR #623 body.
3. Processor PR #132 body, "Parent-visible for pin adoption: rounds 1-6, consolidated"; processor PR #133 body, section 4 and "Composed head `99bfd4bc`" note.
4. `git diff 79c36963..597dba85` (53 files) and per-commit history.
5. Public evidence tree `f81af6fa2defeba95897aeeb287d6c6fd430e5d4`, `review-evidence/70L2-r1` (gate receipt `gates-597dba85.json`, native service/capture receipts at `18199bac`, sweep `sweep-a448s597d.json`).
6. Prior public review findings on PR #623: none exist at the time of this round (the PR carries only two review-start notices, 5903784852 and 5903963761). Nothing to resolve or retain.

## Item-by-item judgment

### (1) PR #132's consolidated list and PR #133's section 4

| List item | Evidence at head | Result |
|---|---|---|
| Five round-1 outputs connected, no open ports | `hdl/milan/KL_pp_shadow.sv:1243-1250` (`restore_closed_o`, `restore_rb_o`, `rs_cause_o`, `restore_cause_o`, `d3_unflushed_o`); `hdl/milan/milan_datapath.sv:2243-2247,2745-2751,7723-7729`; `hdl/common/csr/milan_csr.sv:660-664,2234-2244` | Met. PP_STAT concatenation counted bit by bit: `[16]` closed, `[17]` rb, `[20:18]` rs_cause, `[22:21]` restore_cause, `[23]` 0, `[31:24]` tag; 32 bits total, `[15:0]` unchanged |
| `pend_i = (|nvm_unflushed_o) | d3_unflushed_o`, dyn dirty diagnostic only | `KL_pp_shadow.sv:981` (plus the pre-existing sticky name/map terms) | Met |
| `alarm_i` from `nvm_alarm_o`; combined done/busy/fail/blank | `KL_pp_shadow.sv:1048,1063,1498-1517`; processor `hdl/top/protocol_processor_top.sv:2612-2623` | Met. CLOSED never raises done, so the blind latch (`done && walk_blind_r`) cannot mask it |
| `NVM_RETRY_BACKOFF_CYC_P`, `NVM_RS_AGG_CYC_P` derived from the parent clock | `KL_pp_shadow.sv:1095-1103`: left at the processor's `CLK_HZ_P`-derived defaults, bound `CLK_HZ_P` | Met |
| Evidence classifier row for `d3_mutants.py` | `scripts/measure_test_evidence.py:597-600`, text equal to PR #132's | Met |
| `nvm_cosim`: `rs_agg_i` tied, `wr_chg_o` on a named no-connect, backoff and RS_TMO derivations, B1-B4 window | `tb/verilator/nvm_cosim/cosim_top.sv` (`wr_chg_nc_w`, `.rs_agg_i (1'b0)`, ceil derivations); `cosim_cases.cpp:488` `idle(2000)` | Met |
| `milan_dp` gmstep / gptp / gptp-lat / ax1x1gptp walk starts before the first AECP command | `sim_gmstep.cpp` (after `acquire()`), `sim_gptp.cpp` (before `grade_the_committed_bank_on_the_aecp_wire`), `sim_ax1x1gptp.cpp` (top of `configure()`), each graded done 1 / CLOSED 0 | Met |
| Image-less legs end CLOSED and name it | `sim_main.cpp:257-273`, `sim_aclk.cpp:1228-1245`: busy 0, done 0, fail 1, closed 1, cause 7 | Met |
| `milan_dp_render` T8 waits one commit-to-pin bound | `sim_tdm8_render.cpp:2109` `run_fed(kFrameAxis + kCdcFloorAxis + kBitAxis + 1)` | Met |
| `sim_nxn` hold checks, degrade arm retired, WTMO after the image, word-36 re-read, three stale comments refreshed | `sim_nxn.cpp` `prove_aecp_is_held_until_the_restore()` (held, word 37 +1), held command answered at release, `[AECP-WTMO]` moved into the image arm with word 36 read at the wedge and after the heal; the three R391-5 S2 comments rewritten | Met |
| `pp_shadow` K/K10/K12 walk before enable, M2 walk after handover, P3 blank 0 | `tb/verilator/pp_shadow/sim_main.cpp:1388-1402,3702,3831` | Met. Phase M's no-memory degrade still runs after release, so the README's "no-memory degrade with recovery" stays true |
| PR #133: crflic `>= 3` plus the restart check | `sim_crf_licence.cpp:966-974`: both counts `>= 3`, and every DUT LeaveAll `>= 10 s` after the preceding switch LeaveAll with at least two such LeaveAlls | Met. The author's retained arm at `d352bbaa` fails exactly that check (public log `crflic-restart-arm-d352bbaa.log`) |
| `milan_dp/README.md` `:443`, `:528-530`, `:633-637`, `:877-883` | README `[C]` row, "What it cannot show", the walk-starter paragraph, the `[AECP]` paragraph, the contents entry, the failing-arm row | Met |
| ROM digests re-recorded with unchanged content | `syn/yosys/rom_digests.tsv` rows for `d352bbaa` and `b2db3a97`. `gen_ucode.py` does change between `c951a9ff` and `b2db3a97`, so I regenerated both ROMs at all three pins from each pin's own generator: identical digests, equal to the recorded rows (`receipts/rom_regen.tsv`; the generator change is comments only) | Met |

### (2) AEM-first boot order and every boot path

- `milan_init()` is `configure_fabric`, `load_aem_image`, `nvm_boot`, `entity_advertise` (`sw/firmware/milan_baremetal/milan_baremetal.c:1667-1677`).
- Every `nvm_boot()` path reaches `nvm_restore_walk()` unless the fabric already ended a walk since its reset: the shape-mismatch path (`:1469-1471`, blind), and all four backend branches before the common walk (`:1566-1567`).
- The only path with no walk is the CSR identity mismatch (`:1662-1665`), which never enables the entity.
- The wait ends on done or CLOSED (`nvm_restore_ended()`, `:1364-1368`).
- `restore_go` is taken once by the processor (`KL_acmp_nvm_shadow.sv:371,730`), so clearing `PP_CTRL[1]` after a firmware timeout cannot abort a walk in flight (DR3b).
- Host tests, run here on a scratch copy: `test_nvm_firmware.py --self-test` rc 0; five boot paths on all five shapes; `shape_path_skips_walk` caught by 8 findings and `wait_on_done_only` by 2 (`receipts/nvm_hosttest_selftest.log`).

### (3) Gate 1b: the kept `aem_loaded` slot

- Structure is right.
  - `kept` is either empty or exactly `{"aem_loaded"}` (`sw/builder/test_builder.py:6667`).
  - Only the call rule passes it (`:1642`); an unplaced store still forgets every slot.
  - No other static is kept, so the rule is no weaker for any other static.
- Unmodified head, gate 1b run alone on a scratch copy with the RV32 compiler required:
  - the shipping firmware is accepted with `kept=['aem_loaded']`;
  - the same assembly under forget-on-call is refused on the verdict pin (`receipts/gate1b_early2_base.log`);
  - the five planted breaks are refused by name (summary line in `receipts/gate1b_base.log`).
- The pins are not sound, though. The write and address pins are spelling rules over the source text (`verdict_write_re`, `:6521`; `verdict_address_taken`, `:6534`), and a function-like macro defeats both. See F1.

### (4) The author's unruled call, commit `18199bac`

Judgment: the rule itself is sound and hides no service gap the writer owes. The manager can accept the call. Its self-test controls do not pin it, which is F2.

- **Duties that start armed are graded exactly as before.**
  - `armed_bound()` returns `period_bound_ms` whenever `start >= armed` (`tb/verilator/fw_service_budget/run.py:357-359`).
  - At `18199bac`, `restore_walk` starts 161 cycles before arming, but its original opportunity-free span already begins at the arming tick. Its armed bound equals its whole-span bound (250.66036 ms both; public `service-8x8-all.log`).
  - `grade()` and the oracle fixtures are untouched; the self-test passes 50/50 at head.
- **Nothing the writer owes goes ungraded during `nvm_boot()`.**
  - `nvm_heartbeat_tick()` returns before any heartbeat or PHY poll until `nvm_started` (`milan_baremetal.c:933-934`).
  - So neither the liveness deadline nor PHY publication can be due before the first opportunity, under either order.
- **What does go ungraded, named:** the time from reset to the first PHY link publication.
  - No firmware duty publishes the link before the writer runs. The link-status CSR holds its reset constant (`sw/litex/milan_soc.py:1748-1761`: up, board speed, full duplex).
  - The AEM-first order lengthens that unserviced prefix by the AEM copy and CRC: 1x1 316.918 to 373.902 ms, 8x8 970.142 to 1106.142 ms (`docs/findings/397_SERVICE_BUDGET.md`, base and head).
  - Boot-to-enable is unchanged (1111.13 to 1111.33 ms at 8x8).
  - This prefix is graded only by the 20,000 ms boot deadline, as it already was. It is not a writer-service gap. See S1.
- **The controls do not discriminate as claimed.**
  - The author's three wrong rules (whole span; never grading an unarmed row; clipping an armed row) are refused.
  - Two other weakening rules pass all 50 self-test checks: arming read per duty (W3), and arming read from the last opportunity block (W4).
  - Both hide a 400 ms opportunity-free lead of an armed command duty that the head refuses. See F2.

### (5) Native groups, capture, sweep

Public receipts only; the manager owns acceptance.

- `gates-597dba85.json`: 34 gates, all rc 0.
- Native commands at `18199bac`: the twelve service plans pass. The regrade logs show the AEM row graded from arming at cycle 104,472,844 (8x8).
- `check_nvm_capture` rerun here on a scratch copy: rc 0, seven controls detected (`receipts/check_nvm_capture.log`).
- Sweep receipt `sweep-a448s597d.json`:
  - worst WNS/WHS: asl +0.064/+0.034 ns, eto +0.034/+0.034 ns, eppo +0.135/+0.014 ns;
  - all four corners of every seed meet the +0.030 ns / 0 floor;
  - `refusal_gate_accepts` true for all three;
  - eto carries one critical warning (`Route 35-39`, router ending at -0.248 ns before post-route optimization), as the PR discloses.

### (6) No port or parameter change beyond #132's declared ones

- Processor top, `c951a9ff..b2db3a97`:
  - exactly the five declared outputs;
  - the two new parameters (`NVM_RS_AGG_CYC_P`, `NVM_RETRY_BACKOFF_CYC_P`);
  - the `NVM_RS_TMO_CYC_P` ceil default;
  - comment-only edits on existing lines.
- `d352bbaa..b2db3a97`: no port or parameter line changes.
- Parent: `KL_pp_shadow` gains the four status outputs and `milan_csr` the matching inputs. This is the declared connection into PP_STAT, with no new CSR address and no parameter change.

## Findings

### F1 - MAJOR - Conformance, Robustness, Tests, Docs - `sw/builder/test_builder.py:1633-1642,6521-6604,6667`; `docs/integration/BAREMETAL_FIRMWARE.md:922-929` - the kept verdict slot survives a second write to `aem_loaded` spelled through a macro

**Authority.**
- Ruling 5894183475, "What the gate change must keep":
  - 1: the slot survives a call only while all three pins hold;
  - 2: a second assignment to `aem_loaded`, including one inside a callee such as `nvm_boot()`, is refused with the reason named.
- The ruling's premise is "Nothing else can write it, so keeping its symbol slot across a call makes the resolver no weaker".
- The soundness comment at `test_builder.py:1634-1641` and `BAREMETAL_FIRMWARE.md:928-929` state: "Then nothing anywhere writes it but that assignment, so no callee can."

**Evidence.** Probes planted into scratch copies of the head only (`scripts/plant.py`).

- `m_macro_set`: `#define NVM_FLAG_SET(flag) ((flag) = 1)` and `NVM_FLAG_SET(aem_loaded);` as the first statement of `nvm_boot()`.
- `m_macro_addr`: `#define NVM_REF(obj) (&(obj))` and `*NVM_REF(aem_loaded) = 1;` in the same place.
- Gate 1b, run alone with the RV32 compiler required and stopped right after the shipping-firmware verdict (`scripts/early_stop.py`):
  - both probes are ACCEPTED with `kept=['aem_loaded']`;
  - the same assembly is REFUSED under the old forget-on-call rule, "enters entity_advertise() with [None]" (`receipts/gate1b_early2_m_macro_set.log`, `receipts/gate1b_early2_m_macro_addr.log`).
- The compiled unit (`receipts/census_asm_m_macro_set.s`):
  - `nvm_boot:` stores 1 into `aem_loaded` (`lla a5,aem_loaded; li a4,1; sw a4,0(a5)`, line 3940);
  - `milan_init` stores `load_aem_image()`'s `a0`, calls `nvm_boot`, reloads `aem_loaded` and passes it to `entity_advertise` (lines 4573-4583).
- The complete gate-1b runs of both probes also ended in `GATE1B PASS` with "kept the slot of aem_loaded" in the summary (`receipts/gate1b_m_macro_set.log`, `receipts/gate1b_m_macro_addr.log`).
  - Those two logs were written by overlapping runs and are interleaved, so they are corroboration only.
  - A clean complete run does not fit in one foreground call (`receipts/gate1b_full_m_macro_set.log`, timeout at 590 s).
- The direct spelling `aem_loaded = 1;` in `nvm_boot()` is refused by the source rule (`receipts/gate1b_m_ctrl_direct.log`). So the gap is the spelling class, not the placement.

**Impact.**
- With the new order the choke point reads the verdict back after `nvm_boot()` returns. A firmware edit whose callee sets it to 1 through a macro advertises the entity over an image whose CRC failed, and gate 1b certifies it.
- At the base the same edit was harmless: under forget-on-call the resolver itself refused any verdict that crossed a call.
- So the resolver is weaker than before, contrary to the ruling's premise, and the stated soundness argument is false.
- The shipping firmware at this head is correct. The defect is what the gate can no longer prove.

**Required outcome.**
- The slot crosses a call only when no compiled code other than the verifier's single assignment can write `aem_loaded`, however that write is spelled. For example, read the pins on the preprocessed unit, or refuse keeping the slot when any function but the assigning one has a resolved store to the symbol, or an unplaced store exists.
- Planted controls cover a macro-spelled write and a macro-spelled address inside `nvm_boot()`, each refused with the broken pin named.
- The comment at the rule and `BAREMETAL_FIRMWARE.md` state exactly what the pins prove.

**Verification.**
- Rerun `scripts/early_stop.py` and `scripts/run_gate1b.py` on the two probe trees: each must be refused on the verdict pin.
- The unmodified head must still pass with the slot kept, and the five existing breaks must still be refused by name.

### F2 - MINOR - Tests - `tb/verilator/fw_service_budget/run.py:349-366,493-520`; `tb/verilator/fw_service_budget/README.md:147-153` - the armed-rule controls do not pin which opportunity arms the writer

**Authority.**
- The README states "Three self-test controls pin the rule and its boundary".
- AGENTS.md section 6, Tests: each new test can fail for the defect it claims to detect.
- REVIEW READY 5902107952 cites the controls as what makes the call safe to accept.

**Evidence.**
- `scripts/grader_mutants.py` plants rules into copies of `run.py` and runs the grader's own `--self-test` (`receipts/grader_mutants.log`):
  - identity control PASS;
  - W1 (whole span), W2 (unarmed never charged) and W5 (PHY stretch on the whole span) KILLED;
  - W3 SURVIVED: arming read per duty, from the first opportunity at or after the duty's start;
  - W4 SURVIVED: arming read from the last opportunity block;
  - W6 (armed bound drops the UART allowance) survives but is stricter, not weaker.
- Every armed control uses a single ticks event, so min, max and per-duty readings coincide.
- `scripts/w3_demo.py` (`receipts/grader_w3_demo.log`, `receipts/grader_w4_demo.log`): an armed `milan_status` duty with a 400 ms opportunity-free lead.
  - The head grader refuses it on both stretches.
  - W3 and W4 each return no finding.

**Impact.** A later edit that reads the arming cycle per duty, or from the wrong block, would stop charging the leading opportunity-free tail of every armed duty. That silently weakens the enforce-service verdict for every command duty, with all 50 self-test checks green.

**Required outcome.** The self-test refuses rules that take the arming cycle from anything but the first opportunity of the run: at least one control has an armed duty whose leading gap exceeds the allowance, with opportunities both before it and inside it.

**Verification.** `scripts/grader_mutants.py` reports W3 and W4 KILLED, and W0 still passes.

## Suggestions (non-blocking; they do not affect coverage)

- **S1 (Docs).** `docs/findings/397_SERVICE_BUDGET.md` could say in one line that reset-to-first-PHY-publication is graded only by the 20 s boot deadline, and that the AEM-first order lengthened it by the copy and CRC (about 57 ms at 1x1, 136 ms at 8x8).
- **S2 (new issue, pre-existing, not this lane's).** On the persistence-disabled path `nvm_started` is never set, so `phy_link_tick()` never runs for that boot. The link-status CSR keeps its reset constant (up, board speed), even though this PR now makes that path run the walk and come up on defaults. The base firmware behaves the same. Per AGENTS.md section 4 this belongs in its own issue.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts (at the head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Items 1-6 above against PR #132's consolidated list, PR #133 section 4 and composed-head note, scope record 5880276193, ruling 5894183475; `milan_baremetal.c:1364-1677`; `test_builder.py:1633-1642,6521-6667`; processor top port diff `c951a9ff..b2db3a97` | R412-1 | 597dba8593553ad85b1e94936b016907c4d2003a |
| RTL | CLEAN | `hdl/milan/KL_pp_shadow.sv:955-981,1095-1103,1243-1250,1492-1517`; `hdl/common/csr/milan_csr.sv:650-664,2229-2244` (32-bit PP_STAT width and positions counted); `hdl/milan/milan_datapath.sv:2243-2247,2745-2751,7723-7729` (declare-before-use); processor `protocol_processor_top.sv:2612-2623` combination and `KL_acmp_nvm_shadow.sv:371,730` one-shot `restore_go`; `syn/yosys/rom_digests.tsv` against `receipts/rom_regen.tsv` | R412-1 | 597dba8593553ad85b1e94936b016907c4d2003a |
| Robustness | UNCLEAN (F1) | Boot paths (identity mismatch, shape mismatch, refused window, re-attach, live window, CLOSED terminal, firmware timeout); gate-1b spelling probes `m_macro_set`, `m_macro_addr`, `m_ctrl_direct`; grader boundary (unarmed, straddling and armed duties) | R412-1 | 597dba8593553ad85b1e94936b016907c4d2003a |
| Tests | UNCLEAN (F1, F2) | `test_builder.py:14144-14230` five planted breaks; `run.py:493-520` armed controls with W0-W6 mutants; `test_boot_walk.py` both controls (rerun, caught); harness diffs `sim_nxn.cpp`, `sim_crf_licence.cpp`, `sim_main.cpp`, `sim_aclk.cpp`, `sim_gmstep.cpp`, `sim_gptp.cpp`, `sim_ax1x1gptp.cpp`, `sim_tdm8_render.cpp`, `pp_shadow/sim_main.cpp`, `nvm_cosim/cosim_top.sv`, `cosim_cases.cpp` (read; not executed, see limits) | R412-1 | 597dba8593553ad85b1e94936b016907c4d2003a |
| Docs | UNCLEAN (F1) | `docs/integration/BAREMETAL_FIRMWARE.md:922-929` (false soundness claim) and its order block; `docs/reference/REGISTER_MAP.md` PP_CTRL/PP_STAT/PP_SPADDR rows; `MILAN_COMPLIANCE_MATRIX.md`; `ieee8021q.md` MRP-4..7; `SUBMODULES.md`; `FR_NFR.md`; `milan_feature_status.json` order; `CHANGELOG.md`; `tb/verilator/milan_dp/README.md` four rows; `nvm_cosim`, `pp_shadow`, `nvm_hosttest`, `fw_service_budget` READMEs; `397_SERVICE_BUDGET.md`; `SAVED_STATE_MATERIALIZATION.md:2283` is a dated record, not stale | R412-1 | 597dba8593553ad85b1e94936b016907c4d2003a |

## Real limits of this round

- The designated pinned simulator (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host. I did not substitute another build, so no RTL harness was executed in this round (`milan_dp` legs including `crflic` and `ax1x1gptp`, `milan_dp_render`, `nvm_cosim`, `pp_shadow`). Their pass counts come from the public receipt `gates-597dba85.json` and the author's retained `d352bbaa` crflic arm.
- I did not rerun the native service/capture groups, the builder bank, Yosys or timing. Those are public receipts only.
- A complete gate-1b run exceeds the 600 s foreground limit. F1 rests on the clean early-stop receipts (shipping-firmware verdict, compiled store, forget-on-call contrast). The complete-run PASS logs for the probes are interleaved by overlapping runs and are corroboration only.
- Physical calibration was not run. No hardware was used, and field skips are not hardware proof.
- All probes ran on disposable copies under `scratch/`. The review clone was verified afterwards (`receipts/clone_integrity.log`): HEAD and index tree equal the head, no tracked or untracked change, no assume-unchanged or skip-worktree entries, and gitlinks `protocol-processor b2db3a97`, `gptp-processor 5dce647a`, `third_party/verilog-axis 48ff7a7e` checked out clean.

## Pending manager duties

- Rule on the author's call in `18199bac`. This round recommends accepting the rule, and requires F2 so its controls actually pin it.
- After F1 and F2 are fixed: re-review of the changed head, covering at least Conformance, Robustness, Tests and Docs, plus RTL again if any RTL scope moves. F1's fix is builder-only and F2's grader-only. Neither changes the firmware image or the bitstream, so the capture receipt and the sweep should stand; the manager confirms that at the new head.
- Hosted and act acceptance at the exact head, distinguishing executed jobs from skipped contexts.
- The merge-candidate build against live dev `ec0cc0c1df7d7ab3e25d973958f53f0074393d2c` (source base `79c36963`).
- The external review and the full completion bar.
- #70's remaining obligations named in the PR: lanes 3-5, the silicon cold cycle, DR2c's firmware transaction limit, the matched post-place comparison, and the 8x8 post-place obligation.

## Publishable receipts

Listed in `MANIFEST.sha256` (paths relative to this packet): `scripts/` (probe instruments and mutation drivers, portable, taking tree paths as arguments) and `receipts/` (raw logs, the census assembly of the base and both macro probes, ROM digests, clone integrity).

R412-1 FINISHED
