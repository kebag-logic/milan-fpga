[R413] NEGATIVE - exact head 597dba8593553ad85b1e94936b016907c4d2003a

Round R413-1, external independent review of kebag-logic/milan-fpga PR #623 (issue #70, lane 2): adoption of processor pin `b2db3a97` (processor PR #132, D3 lane 1, plus PR #133, lane C1).
Head `597dba8593553ad85b1e94936b016907c4d2003a`, tree `c0b06e6e3b9a39f8c8f555e89957edf9a920beff`, 21 commits on dev `79c36963660c10e4c1c11a744fb5bff41a552b8b`.
All five lenses were applied. One MAJOR and one MINOR finding are open, so the verdict is NEGATIVE.
The author's unruled call (commit `18199bac`, the service grader) is **sound, and I recommend the manager accept it** (item 4 below).

## Reconstruction (public state only)

- Contract: AGENTS.md, CONTRIBUTING.md, docs/README.md.
- Issue #70: the body, the lane-2 scope record 5880276193, the assignment 5888775832, the STOP 5894165470, the ruling 5894183475 (option 1 plus the `b2db3a97` adoption) and REVIEW READY 5902107952.
- Processor PR #132's body, section "Parent-visible for pin adoption: rounds 1-6, consolidated". Processor PR #133's body: section 4 and the "Composed head `99bfd4bc`" note.
- `docs/design/SAVED_STATE_MATERIALIZATION.md`: sections 3 (decision item 10), 5.1-5.3, 8.7 and 18.2.
- Interface authority: `protocol-processor/hdl/top/protocol_processor_top.sv` at `b2db3a97`.
- The diff `79c36963..597dba85` and its history. The PR body.
- The public evidence tree `f81af6fa:review-evidence/70L2-r1`: gates, sweep, native receipts and logs.
- Prior public review findings on PR #623: none exist. The only comments are the two review-start notices, so there is nothing to retain or resolve.

## Findings

### F1 - MAJOR - lenses: Tests, Conformance, Docs

**Where:** `sw/builder/test_builder.py:1633-1640` (the call rule), `:6521-6604` (`verdict_write_re`, `verdict_address_taken`, `aem_verdict_pins`), `:6667`, and `docs/integration/BAREMETAL_FIRMWARE.md:922-936`.

**The problem.** Gate 1b keeps `aem_loaded`'s slot across a call based on pins read from the raw source text. That text can miss a write the compiler emits.

**Authority.** The ruling 5894183475 says: "The slot survives a call **only** while all three pins hold at the same head." Its premise is "nothing else can write it, so keeping its symbol slot across a call makes the resolver no weaker."

The gate's own design says text rules do not see phase-2 splices or `##` pastes outside the six boot-path bodies. Those constructs are "RETIRED onto the resolved census, which reads the call or the store a splice or a paste builds, by address" (`test_builder.py:5734-5760`). `nvm_boot()` is not one of the six bodies.

The new pin 1 (`verdict_is_the_verifiers`) and pin 2 (`verdict_address_taken`) are regexes over `blanked(source)`, the same text view. Nothing checks the pins against the compiled code: nothing asks the resolved census whether any function other than `milan_init()` stores to `aem_loaded`.

**Evidence** (probes on a disposable copy; `receipts/gate1b_*.log`, `probes/`):

- The shipping head passes gate 1b with the slot kept: `gate1b_baseline.log`, `kept= ['aem_loaded']`.
- Under the forget-on-call rule the same firmware is refused: `gate1b_none_forget.log`. That is the STOP's reproduction, so the kept rule is the only reason the gate accepts.
- Plant `aem_loaded = 1;` at the end of `nvm_boot()`: refused by pin 1 (`gate1b_plain_write.log`), as designed.
- Plant `aem_\<newline>loaded = 1;` at the same place: **ACCEPTED**, slot kept (`gate1b_splice_write.log`).
- Plant `#define MILAN_R413_JOIN(a, b) a##b` and then `MILAN_R413_JOIN(aem_, loaded) = 1;` at the same place: **ACCEPTED**, slot kept (`gate1b_paste_write.log`).
- Plant a GNU `alias("aem_loaded")` written by its other name: refused, but by the store census ("a STORE this gate cannot PLACE"), not by a pin (`gate1b_alias_write.log`).
- Both accepted spellings compile to a real store of the static (`receipts/splice_paste_compile.txt`, the pinned RV32 compiler).

**Impact.** Each accepted plant is a firmware that sets `PP_CTRL[0]` and `ADP_CTRL[0]` whatever `load_aem_image()` returned. That is the bypass gate 1b exists to refuse.

At the base the same statement was harmless, because `nvm_boot()` ran before the verdict was assigned. This head's rule is the first that trusts a text pin over the compiled code for a value crossing a call. So the resolver is weaker for `aem_loaded`, contrary to the ruling's premise and to the soundness comment.

Two statements are false for these spellings:

- the soundness comment "Then no code anywhere can write it except that one assignment" (`:1638`);
- `BAREMETAL_FIRMWARE.md:928`, "Then nothing anywhere writes it but that assignment, so no callee can".

The shipping firmware itself is correct. The defect is in the instrument that proves it.

The rule is no weaker for any other static. `kept` is `{"aem_loaded"}` or empty (`:6667`), only the call rule passes it, and an unplaced store still forgets every slot (`_rv32_forget_symbols`).

**Required outcome:**

- The slot crosses a call only when the single-writer and no-address pins hold on what the compiler compiled. Two ways to get there: read the resolved census's per-function stores to `aem_loaded` (only `milan_init()`'s one store from the verifier's return), or read the phase-3/preprocessed view.
- Planted controls must refuse a phase-2 splice and a `##` paste write inside `nvm_boot()`, each naming the broken pin.
- The comment at the rule and the firmware page must state only what is actually proven.

**Verification:** rerun `probes/plants.py` with `splice_write` and `paste_write` through `probes/run_gate1b.py`. Both must be refused. The shipping head must still pass with the slot kept, and the five existing controls must still be refused by name.

### F2 - MINOR - lens: Docs

**Where:** the PR #623 body ("What remains for lanes 3-5" / "Still with #70 beyond lane 2's list"), the D3 page status header, and `sw/firmware/milan_baremetal/milan_baremetal.c:1380` and `:1619`.

**Authority.** The accepted D3 decision item 10 (`SAVED_STATE_MATERIALIZATION.md:386-389`) and section 5.3 change 3 (`:630-634`) require the restore-wait timeout and the enable line to report that the fabric holds the enable. Section 18.2 lists "Implement the three firmware boot changes in section 5.3" in lane 2's acceptance.

**The problem.**

- This PR implements changes 1 and 2 but not change 3. That is consistent with its frozen assignment, which does not list change 3.
- Neither the PR's remaining-work lists nor #70 record change 3 as open. The D3 status header names change 1 only.
- Since this pin the product can end CLOSED, which is fail and never done, with ADP dark. `entity_advertise()` still prints "fabric entity enabled; UART diagnostics ready." whenever the AEM verdict is non-zero, including after a CLOSED restore.

**Impact.** A cold reviewer, or an operator reading the UART, cannot tell that change 3 is outstanding. The boot line can claim an enabled entity that the fabric is withholding. The `closed=` field printed just before mitigates this.

**Required outcome:** record D3 section 5.3 change 3 as open in #70's lane-2 remainder and in the PR's remaining-work list, or implement it.

**Verification:** a cold read of the PR body and the #70 record names change 3 as open, or the firmware line reports "requested" per section 5.3.

### S1 - SUGGESTION - lens: Tests

The one startup service quantity no row grades is the time from reset to the first service opportunity, meaning the first heartbeat, PHY publication and console dispatch. The 20 s boot comparison is the only bound on it.

That interval grows under the ruled order by the AEM copy: the boot unarmed prefix goes from 316.9 to 373.9 ms at 1x1 and from 970.1 to 1106.1 ms at 8x8 (`docs/findings/397_SERVICE_BUDGET.md`, base against head). At 8x8 the first PHY readback is at system cycle 104,538,153 (1,045 ms).

Printing this interval in the receipt would make the next order change visible. This is optional and does not affect coverage.

### S2 - SUGGESTION - lens: Docs

The sweep receipt `sweep-a448s597d.json` binds to the head only through its tag and directory names, and carries no source-head field. Recording the head and tree in the JSON would make the binding checkable. This is optional; the manager owns sweep acceptance.

## Judgments on the assigned questions

1. **PR #132's consolidated list and PR #133's parent edits: applied, item by item.**
   - `pp_shadow` connections: the five round-1 outputs connect. `restore_closed_o`, `restore_rb_o`, `rs_cause_o` and `restore_cause_o` go straight to `PP_STAT[16]`, `[17]`, `[20:18]` and `[22:21]` (`milan_csr.sv:2234-2244`; the 32-bit packing checked bit by bit). `d3_unflushed_o` feeds `pend_i`, `aecp_dyn_dirty_o` leaves it, and the name/map live terms stay (`KL_pp_shadow.sv:970-982`).
   - Alarm: `alarm_i` takes the combined alarm.
   - Parameters: `NVM_RS_AGG_CYC_P` and `NVM_RETRY_BACKOFF_CYC_P` are not restated. They derive from `CLK_HZ_P`, which carries `MILAN_CLK_FREQ_HZ`.
   - Evidence classifier: the `d3_mutants.py` row is added.
   - `nvm_cosim`: `rs_agg_i` tied, `wr_chg_o` on a named no-connect, `RETRY_BACKOFF_CYC_P` and the ceiling `RS_TMO_CYC_P` both match the top's formulas (`protocol_processor_top.sv:136-151`), and the B1-B4 window is 2,000 ms.
   - Restore-walk starts: `gmstep`, `gptp`/`gptp-lat` and `ax1x1gptp` each start the walk before their first AECP command and grade done 1, CLOSED 0.
   - Image-less legs (`sim_main` main, `nolpf`, `ax1x1` and `aclk`) end on either terminal and grade CLOSED with cause 7.
   - `milan_dp_render` T8 waits out `kFrameAxis + kCdcFloorAxis + kBitAxis`.
   - `sim_nxn`: the degrade arm is retired. The hold check, the word-37 drop and the held answer at release are added. `[AECP-WTMO]` moved after `[AECP-IMG]` in every leg, before the timed return. Word 36 is read at the wedge and after the heal, and all three stale comments were refreshed.
   - `pp_shadow`: the walk is in the shared `pending_boot()` used by K, K10 and K12. M2 walks after the handover, and P3 expects blank 0.
   - PR #133: `sim_crf_licence.cpp` asserts `>= 3` for both counts and adds the restart check (every DUT LeaveAll at least 10 s after the switch's). The author's public log at `d352bbaa` fails exactly that check (5/5 LeaveAlls, soonest lag 2,210 ms; 1 of 416).
   - README rows `:443`, `:528-530`, `:633-637` (new paragraph) and `:877-883` are rewritten as the composed-head note asks. `ieee8021q.md` MRP-4..7 and compliance-matrix rows 4.2.7.1 and 4.2.7.3/4.4.1 are updated.
   - ROM digests: I regenerated `ucode.hex` and `ltn_rom.hex` from both pins' generators, because `gen_ucode.py` did change. Both digests are identical to the recorded rows (`receipts/rom_regen.txt`).
2. **Boot order and walk coverage: correct.**
   - `milan_init()` is `configure_fabric`, `load_aem_image`, `nvm_boot`, `entity_advertise`.
   - Every `nvm_boot()` path reaches `nvm_restore_walk()` unless the walk already ended: shape mismatch (blind), a backend without contract 3, no accepted load (retired), re-attach, the walk already sequenced, and a refused window. The wait ends on done or CLOSED.
   - The only path without a walk is the CSR-identity mismatch, which never enables the entity.
   - My host run passes on all five shapes, and both planted boot defects are caught (`receipts/nvm_hosttest_selftest.log`).
   - Reversing the order in a copy is refused by `check_feature_status.py` (naming both sequences) and by `check_nvm_capture.py` (`receipts/check_*_restore_before_aem.log`).
3. **Gate 1b:**
   - Single verifier assignment, no address taken and file-scope static are all implemented, with the soundness comment at the rule.
   - The five planted controls are refused by name, as the builder banks report.
   - The rule is no weaker for any other static.
   - However, the single-writer and no-address pins are text reads, blind to splices and pastes outside the six bodies. **F1.**
4. **The author's unruled call (`18199bac`): sound. I recommend acceptance. No real service gap is hidden.**
   - `armed_bound()` (`run.py:349-366`) changes a duty's bound only if the duty starts before the first heartbeat opportunity. A duty that starts armed returns its old `period_bound_ms` unchanged, and the PHY bound uses the same value.
   - The recorded oracle traces regrade unchanged: 25 rows each, the rule changes none (`receipts/service_regrade_compare.log`). They predate the BACKING line, so `service_findings()` raises for base and head alike; the claim holds at bound level.
   - On the public 18199bac native receipts the rule changes exactly one row, `aem_copy_crc`. At 8x8 it moves from 1265.35 to 253.16 ms; at 1x1 from 533.13 to 253.75 ms. The base grader gives exactly the two findings from the first native run, and the head grader gives none.
   - The self-test passes 50 checks at head (`receipts/service_selftest_head.log`). I planted six wrong rules of my own and all six are killed by the three controls (`receipts/service_rule_mutants.log`): skip every unarmed start, anchor on the last tick, anchor on the first heartbeat write, span from the duty start, exempt the AEM row by name, and drop the 250 ms base.
   - What is not graded in the prefix: no heartbeat, PHY poll or console service runs before the first opportunity. That was already true of the old order's prefix, which covered `nvm_boot()`'s pre-walk part.
   - The only newly unarmed span is the AEM copy and CRC (58 ms at 1x1, 137 ms at 8x8). The writer is not live then, and continuous backing is graded from its first assertion (`BACKING armed=1 unbacked_cycles=0`).
   - Nothing the product needs during `nvm_boot()` loses grading it had. The residual worth naming is the reset-to-first-service interval, now 374 / 1106 ms. It is ungraded in both orders (S1).
5. **Native groups, capture and sweep.**
   - `check_nvm_capture.py` passes at head with all four controls (`receipts/check_nvm_capture.log`).
   - The public gates receipt `gates-597dba85.json` records 34 gates at rc 0, with head and head_after equal to `597dba85` and a clean tree.
   - The public sweep receipt has three seeds, all meeting WNS >= +0.030 ns and WHS >= 0 at all four corners, with the refusal gate accepting. The worst is `eto` at +0.034 / +0.034 ns, which carries one critical warning (Route 35-39, the router's -0.248 ns). The receipt's post-route closure is recorded in the PR.
   - I did not rerun any native group or the sweep. The manager owns their acceptance.
6. **No port or parameter change beyond #132's declared ones.**
   - The processor top's interface diff `c951a9ff..b2db3a97` adds exactly the five outputs and three parameters of #132, and PR #133 adds none (`d352bbaa..b2db3a97` has no port or parameter lines).
   - On the parent side, the new `KL_pp_shadow` outputs and `milan_csr` inputs carry those processor outputs to `PP_STAT`'s reserved bits. There is no new CSR, and each module has a single instance on the same `axis_clk`.

## Per-lens results

[R413] UNCLEAN Tests: F1.

[R413] UNCLEAN Conformance: F1 (ruling 5894183475 condition 1).

[R413] UNCLEAN Docs: F1 (`test_builder.py:1638`, `BAREMETAL_FIRMWARE.md:928`) and F2.

[R413] PASS RTL - `hdl/milan/KL_pp_shadow.sv:684-696,957-982,1095-1105,1240-1250,1492-1516`; `hdl/common/csr/milan_csr.sv:650-664,2229-2244`; `hdl/milan/milan_datapath.sv:2240-2245,2745-2752,7473,7723-7730`; `protocol-processor/hdl/top/protocol_processor_top.sv:136-151,449-516,2611-2623` at `b2db3a97`; `tb/verilator/nvm_cosim/cosim_top.sv:262-280` - checked the port connections against the top's interface (no open port; widths [2:0]/[1:0]), the PP_STAT 32-bit packing and bit positions against REGISTER_MAP, the single clock and reset (`axis_clk` for both instances, no new crossing), the `pend_i` composition against D3 section 5.2, the deadline and backoff derivations (ceilings identical to the top), and the ROM digests regenerated at both pins.

[R413] PASS Robustness - `sw/firmware/milan_baremetal/milan_baremetal.c:1362-1385,1448-1580,1656-1678`; `sw/firmware/nvm_hosttest/test_boot_walk.py`; `tb/verilator/fw_service_budget/run.py:349-414`; `tb/verilator/pp_shadow/sim_main.cpp` (`pending_boot`, M2, P3); `tb/verilator/nvm_cosim/cosim_cases.cpp:485-490` - checked every boot path, including CLOSED, shape mismatch, refused window, no accepted load, re-attach and walk-already-sequenced, and the bounded wait ending on either terminal. Ran the host tests (5 shapes x 5 paths, both defects caught). Checked the grader for boundary, pre-arm and ends-before-arm cases, with six mutants killed, and the deadline-terminated walks in `pp_shadow` and the B1-B4 give-up window.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #70 assignment/STOP/ruling; processor PR #132 consolidated list and PR #133 section 4 and composed note, item by item; D3 sections 5.2, 5.3, 8.7, 18.2; processor top interface at `b2db3a97` | R413-1 | 597dba8593553ad85b1e94936b016907c4d2003a |
| RTL | CLEAN | `KL_pp_shadow.sv`, `milan_csr.sv`, `milan_datapath.sv`, processor top `b2db3a97`, `nvm_cosim/cosim_top.sv`, `syn/yosys/rom_digests.tsv` (regenerated) | R413-1 | 597dba8593553ad85b1e94936b016907c4d2003a |
| Robustness | CLEAN | `milan_baremetal.c` boot paths, `nvm_host.c`, `test_boot_walk.py`, `fw_service_budget/run.py`, `pp_shadow/sim_main.cpp`, `nvm_cosim/cosim_cases.cpp` | R413-1 | 597dba8593553ad85b1e94936b016907c4d2003a |
| Tests | UNCLEAN (F1) | `sw/builder/test_builder.py` gate 1b (probed), `fw_service_budget` self-test and rule (probed), host boot-walk tests (run), `sim_crf_licence.cpp` restart check and the public `d352bbaa` failing log, `sim_nxn.cpp`/`sim_gmstep.cpp`/`sim_gptp.cpp`/`sim_ax1x1gptp.cpp`/`sim_main.cpp`/`sim_aclk.cpp`/`sim_tdm8_render.cpp` (read) | R413-1 | 597dba8593553ad85b1e94936b016907c4d2003a |
| Docs | UNCLEAN (F1, F2) | REGISTER_MAP, BAREMETAL_FIRMWARE, the three SAVED_STATE pages, the compliance matrix, `ieee8021q.md`, CHANGELOG, TROUBLESHOOTING, `397_SERVICE_BUDGET.md`, the `milan_dp`/`pp_shadow`/`nvm_cosim`/`nvm_hosttest`/`fw_service_budget` READMEs, the feature ledger, the PR body | R413-1 | 597dba8593553ad85b1e94936b016907c4d2003a |

## Real limits

- The scoped Verilator binary at `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. I therefore ran no Verilator simulation: no `milan_dp`, `pp_shadow`, `nvm_cosim` or `milan_dp_render` leg, and no harness mutant.
  - The harness judgments rest on reading the source against PR #132/#133's lists, on the author's public failing-arm logs, and on the manager's gates receipt.
- Gate 1b was probed through `test_baremetal_profile_contract()` on the shipping-firmware pass only, via an environment-guarded early return in a scratch copy. The rest of the builder bank was not run on the plants, and no other builder test is known to grade this property.
- I did not rerun the native service and capture groups or the timing sweep. My item 4 and item 5 conclusions regrade the public raw receipts and read the public sweep JSON.
- No hardware was used. Physical calibration was NOT RUN, and field skips are not hardware proof.
- I did not judge hosted/act evidence. Source validation at `79c36963` is distinct from the current-dev merge candidate (live dev `ec0cc0c1`).

## Pending manager duties

- Rule on F1 and F2, and on the recommendation to accept `18199bac`.
- Current-dev candidate build and validation at the merge turn, hosted/act acceptance, and sweep acceptance.
- A second positive review, and a reviewer-owned ledger at the final head. Any fix commit for F1 changes `sw/builder/test_builder.py` and firmware docs, which un-covers Tests, Conformance and Docs, and those lenses must be covered again at that head.

R413-1 FINISHED
