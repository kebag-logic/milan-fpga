[R871] NEGATIVE - exact head 502b041cc0bd0e4ea230b8a3a65f553ab69df3ff

# R871-1: internal cleared-context review of PR #953 (#943, relates to #665)

- **Head:** `502b041cc0bd0e4ea230b8a3a65f553ab69df3ff`, tree `eef553476a70ca961390ab9dbdf44a808d4c0076`. I verified both in the detached review clone before and after every probe.
- **Base:** `0839453f`, the flip train's head. The diff is thirteen one-line commits.
- **Verdict:** NEGATIVE, on one open MINOR under `Tests` (R871-F1). The other four lenses are covered clean.
- **What is right:** the fix is correct and conformant, it failed first on the old code, and the deleted owed row is genuinely answered.
- **What is open:** the new test cannot fail for two defects of the flag law it states. Both are reviewer-planted, and both survive.
- **Prior public review findings on this PR:** none. The only comment before this round is the review-start comment, and there are no PR reviews or review comments. I read that state after my own pass. Nothing is carried in from earlier rounds.

## Scope reconstructed

- **Authority:** #943's body, the #665 ruling of 2026-11-19 (item 1), the takeover comment and the REVIEW READY comment, and the PR body.
- **Defect:** on the split, a declaring STREAM_OUTPUT's GET_STREAM_INFO has these faults:
  - it carries `stream_dest_mac` 0 with STREAM_DEST_MAC_VALID set;
  - it never sets flags_ex REGISTERING;
  - it never sets REGISTERING_FAILED (`0x00000040`).
- **Clauses:** Milan v1.2 5.4.2.10.2 and Tables 5.8, 5.11 and 5.12; IEEE 1722.1-2021 7.4.16; IEEE 802.1Q-2018 35.2.2.7.2/.4.
- **Constraints:** no RTL and no mailbox-contract change (MAILBOX_SPLIT.md). The CPU rows are under FR_NFR.md 3.4.1 and NFR-SCOUT-03.
- **Out of scope by #943's own body:**
  - no notice on a Listener registration change (Table 5.22);
  - MSRP_FAILURE_VALID, the failure code and the failure bridge ID;
  - the face's declaring bit being the DA gate, not TALKER_DECL.

## The focus items, answered

1. **Destination MAC and the Listener flags, at every output and both shapes: met.**
   - **The bridge** (`sw/firmware/ctrl/app/ctrl_app_aecp.c:54-67`, gate at `:85`) completes only a whole observation of a type-6 descriptor whose face flags carry STREAM_DEST_MAC_VALID.
   - **Destination MAC:** the ACMP source port's `base + n`, which is what PROBE_TX_RESPONSE carries (`plat/ctrl_plat.c:95-103`), and 0 while MAAP holds no range.
   - **REGISTERING:** taken from `listener_present` on `ifs[source_interface[index]]`. That copy is set from the Registrar (`srp/srp_mbx.c:459-468`, `:931-944`) and cleared on Lv, at destroy and at link loss (`:623`, `:1114`).
   - **REGISTERING_FAILED:** taken from `!registered`, where `registered` means Ready or Ready Failed (`srp_mbx.c:181-195`). So it is set for Asking Failed.
   - **Undeclared:** the face's answer stands, `stream_dest_mac` 0 with neither flag and VALID clear.
   - **The release fabric agrees.** This is the same law as its `gsi_flag_law`: `hdl/milan/milan_datapath.sv:6444-6447` and `:6482-6494` give REGISTERING = decl && lreg != 0 and REGISTERING_FAILED = decl && lreg == 1. Selector 4 at `:6698-6703` gives the MAC as decl ? (maap_addr_valid ? addr : 0) : 0.
   - **REGISTERING under Asking Failed.** The ruling's parenthesis names Ready and Ready Failed. Setting REGISTERING under Asking Failed too follows Table 5.8/5.12 as the release fabric and `tb/verilator/pp_shadow/README.md:248` read it ("flags_ex REGISTERING while any Listener is registered"). It was published in the takeover comment before work began, and nobody objected. I accept it as conformant.
   - **Executed at the exact head** (`receipts/tests/`): `AppOutputs` plus `Core.TheRunningCheckObservesEveryStreamBriefly` pass at 1x1/1if, 1x1/2if, 8x8/1if and 8x8/2if. The full App arm at 1x1/2if passes, 176 of 176.
2. **The new tests fail on the old code, and the 15 plants are caught by name: met, with one gap (F1).**
   - **Failing first:** I took the head's test on the base's code (a scratch clone of `0839453f` with only `test_aecp.cpp` replaced). It fails at 1x1/1if, 1x1/2if and 8x8/1if, at every output: the destination MAC, REGISTERING and REGISTERING_FAILED (`receipts/tests/failing-first-base-*.log`).
   - **The PR's 15 rows, each planted alone at this head:**
     - At 1x1/1if: 14 caught by their named words.
     - At 8x8/1if: 14 caught.
     - `output-listener-on-interface-zero` escapes at one interface. That is expected: at one interface `ifs[0]` is the output's own interface, so the defect is equivalent there.
     - The campaign arm runs at two interfaces, and the author's gate receipt at `211c1ede` (code-identical to this head) shows all 15 caught there, `stream-read-brief` too.
   - **Nothing weakened.** The only edit to an existing check is `aecp_configuration_mutants.py`'s `stream-read-brief`. It is re-anchored on the new three lines and plants the same defect, an always-brief read, still caught by the same two words.
   - **My seven extra defects** (`receipts/probes/extra-1x1-if2.log`):
     - Four are caught: the caller's brief not kept, GET/SET_STREAM_INFO read brief, the face's flags overwritten, and the completion run without the declaring gate.
     - One survives as an equivalent: gating on STREAM_ID_VALID, which the face sets together with DEST_MAC_VALID.
     - **Two survive as real defects (F1):** an Asking Failed Listener also raising MSRP_FAILURE_VALID, and REGISTERING taken from either interface's registrar.
3. **The CPU rows.** I re-ran none of the harness. This reading is from the author's receipts at `211c1ede`, which are code-identical to this head: `git diff 211c1ede..502b041c` touches two Markdown pages and one comment in `rows_tiers.py`.
   - **Within bound at both points.**
     - Arm A covers every group (99 and 98), with 0 refusals and every AECP row fitting.
     - The only misses are the seven held-egress `backlog-owed` rows, which the base also records.
     - The answering-ports, answering-every-port and talker-notices arms have 0 misses.
     - `record_classes.py` gives PASS at both points. `flip_grade.py --check` gives PASS at both: 1x1/1if `last` is 137.97 of 140 ms, and 8x8/1if's load is 0.744 of 0.75.
   - **Is the brief map check behaviour-preserving and conformant? Yes.**
     - `idle()` (`aecp/aecp_maps.c:129-133`) uses only `ok` and `running`.
     - For a STREAM_OUTPUT, `running` is the face's `mbx_pub_licensed` whatever the brief (`aecp/aecp_face.c:184`). A brief read still proves the window answers on word 0.
     - The one difference from the base: a window that answers word 0 but fails a later word no longer refuses the edit. That matches SET_CONFIGURATION's and SET_STREAM_FORMAT's running checks since #894 (`aecp_commands.c:127-132`).
     - Only two callers of `aecp_stream_read` exist, and both set `brief` (`aecp_commands.c:380`, `aecp_maps.c:131`). `observe` is the only route to the stream port.
   - **The restatement of 8x8/1if's long record from 1,715 to 1,720 us follows the rule.** 163,520 cycles at 100 MHz, plus 5 %, rounded up to 5 us, is 1,720. Its rows are reported, not held (#872), and `flip_grade` passes.
   - **The margin note is accurate and material.** By the rule, 310 us admits at most 29,523 cycles, so 1x1/1if's paced edit at 29,422 has 101 cycles of headroom. 8x8/1if's long record has 289. Records move by thousands of cycles with placement: the same work measured 29,331 to 31,749 cycles on the paced edit, and 152,504 to 182,622 on the long record. See the pending manager duties.
   - **A formal declaring-output arm** is not required by #943's frozen acceptance, which asks to re-measure the AECP rows, and that was done. It is a decision for the owner, and the author published it as one. I recommend it (R871-S1).
4. **The twin's deleted owed row `stream-output-0-dest-mac` is genuinely answered.**
   - **At this head** (`receipts/twin-head.log`): `make twin` gives 0 findings and `make twin-plants` gives 32 refusals, both rc 0. `output-dest-mac-zero` and `output-notice-dropped` are each refused by their own words.
   - **With the completion disabled in the firmware, not just in the capture** (`receipts/twin-fix-reverted.log`), the integrated twin reports `AECP notice GET_STREAM_INFO 0x0006/0 frame 0 differs at byte 66 (fabric 91e0f00001000000, split 0000000000000000)`: 2 findings, rc 2.
   - **History agrees:** the author's `22b4def4` receipt shows the old row reporting "the difference has gone".
5. **ROM and the release image, from the author's receipts.**
   - ROM grows by 280 B at every ledger point, SRAM and RAMB36 are unchanged (45, 46, 58, 63), and `plat_ledger: PASS (0 finding(s))`.
   - The release `bios.bin` and the stripped ELF are byte-identical to the base at 1x1 and 8x8. The unstripped ELF differs only in debug strings that name the build clone.
   - No RTL, mailbox or submodule file is in the diff (`git diff --stat 0839453f..502b041c` lists none).
6. **The firmware-boundary refusal is pre-existing and not this PR's.**
   - `sw/firmware/ctrl/test/sink_mutants.py` and `tb/verilator/ctrl_service_budget/talker_notice.py` are classified nowhere in `sw/firmware/ctrl/test/ctrl_configs.py`, at the base or at the head: 0 mentions in both.
   - The diff touches neither file nor `ctrl_configs.py`. The author's receipt shows the same refusal text at both commits.
   - The new `aecp_output_mutants.py` is not refused.
7. **The items left unchanged are correctly out of #943's scope.**
   - #943's body lists all three under "Seen beside it, the same face (reported, not changed)": a notice on a Listener registration change, the Talker Failed fields, and the declaring bit as the DA gate.
   - The ruling's item 1 names only the destination MAC and the two flags.
   - The PR body's Known limitations record all three.

## Findings

### R871-F1 MINOR - Tests - `sw/firmware/ctrl/test/test_aecp.cpp:895-905` - AppOutputs cannot fail for two defects of the output flag law it states

- **Authority:** AGENTS.md section 6, `Tests`: "Each new test can fail for the defect it claims to detect" and "Positive, negative, and boundary behavior is covered". Milan v1.2 Table 5.11: for a Stream Output, MSRP_FAILURE_VALID belongs to a declared Talker Failed, not to a Listener's registration.
- **What the test claims:** its own header says a declaring output "follows the Listener registered for its stream_id on its own interface".
- **Evidence:** both probes planted alone at this head, 1x1/2if, rc 0 (`receipts/probes/extra-1x1-if2.log`).
  - **`rv-failed-adds-msrp-failure-valid` survives.** It changes `ctrl_app_aecp.c:64` to `0x08000040u`, which is exactly the constant the STREAM_INPUT branch uses at `:82`, so copying it is a plausible mistake. With a Listener registered, the test reads only `r.flags&0x40u` (`:901-903`). The full flags word is pinned only with no Listener (`:892`).
  - **`rv-listener-any-interface` survives.** It takes REGISTERING from either interface's registrar copy. No step registers output n's stream on an interface other than its own and expects nothing.
  - The twin registers no Listener, so it cannot catch either one.
- **Impact:** if either defect is introduced, every firmware gate stays green. A controller would then read MSRP_FAILURE_VALID on a running output with an Asking Failed Listener, and the zero failure code and bridge ID as valid. Or it would read REGISTERING from a Listener the output's own interface never registered.
- **Required outcome:** for each of Ready, Ready Failed and Asking Failed, AppOutputs pins the whole flags word: the face's flags, plus REGISTERING_FAILED for Asking Failed alone. At two interfaces, it registers a Listener for output n's stream on the interface that is not output n's and expects neither flag. Each fails on its own words. Adding both defects as rows in `aecp_output_mutants.py` is the natural way to keep them pinned, though the design is the author's.
- **Verification:** re-run `probe_mutants.py <head> <out> configs/endstation_ax7101_1x1_tdm8.yaml 2 extra` and expect `FAILS` for both rows. The AECP campaign stays green, with any new rows caught by name.

### R871-S1 SUGGESTION - Tests - author receipt `budget/declaring-face-measurement.txt`; `tb/verilator/ctrl_service_budget/build.py` stub `b_stream` - no formal arm runs the completion

- **The gap:** every harness arm's face answers undeclared. The cost of a declaring output's GET/SET_STREAM_INFO, and of the #936 notice fan-out of a declared Talker, is not seen by the gate that holds AECP records to their class statements.
- **The only measurement** is on an uncommitted image: 22,739 cycles, 240 of 245 us, which is 594 cycles inside the 23,333 the statement admits.
- **That same image shows placement is the risk.** One stub change moved the paced edit to 325 of 310 us and the long record to 1,920 of 1,720 us, and put two 8x8/1if passes over the 2 ms per-pass share (2.41 ms).
- **Why not a finding:** #943's acceptance does not ask for this arm. The NFR-SCOUT-03 path bound (20 ms) holds by orders of magnitude. The author has published it as an owner decision.
- **Recommendation:** the owner rules on a declaring-face arm, with a Listener registered, graded by `record_classes.py` at 1x1/1if and 8x8/1if, and on how far the AECP class statements must stand from placement. A follow-up issue records that ruling.

### R871-S2 SUGGESTION - Docs - author packet `review-evidence/943-r1/author-r1/receipts/firmware/plants-*.txt` - the per-shape plant receipts are a superseded row set

- **The stale receipts:** they report "14 output plants" under names that no longer exist: `output-dest-mac-undeclared`, `output-registering-undeclared`, `output-listener-on-the-descriptors-interface`.
- **What they lack:** they do not include `output-completed-undeclared`, `output-brief-completed`, `output-listener-on-interface-zero` or `map-idle-reads-whole`.
- **What is current:** the gate receipt (`gates/firmware-gate-211c1ede-shard2.txt:360-374`) is the final 15. My own per-shape runs at 1x1/1if and 8x8/1if cover the final set (`receipts/probes/rows-*.log`).
- **Recommendation:** label those three files as an intermediate row set in the packet index. No repository artifact is affected.

No RESIDUE items.

## Clean-lens records

```text
[R871] PASS Conformance - sw/firmware/ctrl/app/ctrl_app_aecp.c:49-92, plat/ctrl_plat.c:95-103, srp/srp_mbx.c:181-195,459-468,931-944, hdl/milan/milan_datapath.sv:6444-6496,6698-6703, test_aecp.cpp:871-945 - the completion against Milan v1.2 5.4.2.10.2 / Tables 5.8, 5.11, 5.12, IEEE 1722.1-2021 7.4.16 and 802.1Q 35.2.2.7.2/.4, and against the release fabric's gsi_flag_law; #665 ruling item 1 and #943's out-of-scope list; executed: AppOutputs at 1x1/1if, 1x1/2if, 8x8/1if, 8x8/2if PASS; failing-first on 0839453f at three shapes
[R871] PASS RTL - git diff --stat 0839453f..502b041c (no hdl/, sw/mailbox, protocol-processor or gptp-processor path; no gitlink change); aecp/aecp_internal.h:32, aecp_commands.c:115-122,380, aecp_maps.c:128-133 - the stream port's interface contract (brief now set by the caller; both callers initialise it; observe the only route), bounds (index < n_sources, < CTRL_SRP_SOURCES; source_interface < MBX_N_IF; n_sources == CTRL_SRP_SOURCES at ctrl_plat.c:320), 48-bit MAC through aecp_put48, mailbox contract unchanged
[R871] PASS Robustness - ctrl_app_aecp.c:54-67,85; srp_mbx.c:623,1114; test_aecp.cpp:905-945 - no SRP, a source past SRP's shape, an output ACMP holds no source for (unreachable at shipping shapes, the CRF output included at 8x8), MAAP holding no range, Listener Lv after LeaveTime, Talker withdrawn and declared again, brief observation, SRP destroy and link loss clearing listener_present; reviewer probes rv-brief-not-kept, rv-stream-info-brief, rv-flags-overwritten, rv-gate-brief-only all caught
[R871] PASS Docs - sw/firmware/ctrl/aecp/README.md:115-122, docs/design/SPLIT_CONTROL_MEMORY.md:2998, tb/verilator/milan_dp/README.md:1444-1460,1506-1507,1522-1523,1546, docs/DOCUMENTATION_AUDIT.md:444, rows_tiers.py:131-135, the PR body's Known limitations - each changed contract stated, the twin's OWED table and plant table match twin_compare.py/twin_plants.py, the restated record matches the receipts; the comment rule: no lane label, review round, reviewer ID or issue-comment ID in any added line (grep over the delta); hosted docs-check, docs-check-no-git and docs-gates-0/1/2 success at the exact head
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ctrl_app_aecp.c:49-92; ctrl_plat.c:95-103; srp_mbx.c:181-195, 459-468, 931-944; milan_datapath.sv:6444-6496, 6698-6703; #943 body, #665 ruling item 1; AppOutputs at four shapes; failing-first at three | R871-1 | 502b041cc0bd0e4ea230b8a3a65f553ab69df3ff |
| RTL | CLEAN | diff stat (no RTL, mailbox or gitlink change); aecp_internal.h:32; aecp_commands.c:115-122, 380; aecp_maps.c:128-133; ctrl_plat.c:320 | R871-1 | 502b041cc0bd0e4ea230b8a3a65f553ab69df3ff |
| Robustness | CLEAN | ctrl_app_aecp.c:54-67, 85; srp_mbx.c:623, 1114; test_aecp.cpp:905-945; four caught reviewer probes | R871-1 | 502b041cc0bd0e4ea230b8a3a65f553ab69df3ff |
| Tests | UNCLEAN (R871-F1 open) | test_aecp.cpp:810-945, 2207-2213; aecp_output_mutants.py; aecp_mutants.py; aecp_configuration_mutants.py; aecp_arms.py; twin_compare.py; twin_plants.py; 15 rows planted at 1x1/1if and 8x8/1if; 7 reviewer probes at 1x1/2if; twin and twin-plants at head; twin with the fix disabled | R871-1 | 502b041cc0bd0e4ea230b8a3a65f553ab69df3ff |
| Docs | CLEAN | aecp/README.md:115-122; SPLIT_CONTROL_MEMORY.md:2998; milan_dp/README.md:1444-1546; DOCUMENTATION_AUDIT.md:444; rows_tiers.py:131-135; PR body; hosted docs jobs | R871-1 | 502b041cc0bd0e4ea230b8a3a65f553ab69df3ff |

A fix for F1 that touches only `test_aecp.cpp` and the mutant tables leaves the RTL and Robustness rows standing at an ancestor. The Conformance and Docs rows stand too, as long as no code or doc they cite changes. `Tests` must be covered again at the new head.

## What I executed (receipts listed in MANIFEST.sha256)

All runs are on host builds of the firmware and the pinned Verilator 5.050, which I checked before use (`Verilator 5.050 2026-07-01 rev v5.050`).

- `receipts/tests/app-*.log`: the head's tests at four shapes, plus the full App arm at 1x1/2if (176 of 176).
- `receipts/tests/failing-first-base-*.log`: the head's test on the base's code, rc 1 at 1x1/1if, 1x1/2if and 8x8/1if.
- `receipts/probes/rows-*.log`: the PR's 15 rows at 1x1/1if and 8x8/1if.
- `receipts/probes/extra-1x1-if2.log`: the reviewer's seven defects.
- `receipts/twin-head.log`: twin plus twin-plants at head, rc 0 and 0, with 32 refusals.
- `receipts/twin-fix-reverted.log`: the twin with the completion disabled in the firmware, rc 2.
- `receipts/hosted-checks-502b041c.txt`: a snapshot of the hosted check runs at the exact head. Executed: 18 succeeded, 1 skipped (Physical gPTP, nightly and manual), 37 still queued or running.
- `receipts/clone-integrity.txt`: the review clone's HEAD, tree, index and gitlinks, identical after the probes. The `__pycache__` directories my runs created were removed, so 0 ignored files remain.
- `probe_mutants.py` and `reproduce.sh`: the portable scripts. Every probe ran in disposable clones under the packet's scratch directory, and each probe clone ended clean.

## Real limits

- **Not run by me; read from the author's receipts at `211c1ede`, code-identical to this head:**
  - the CPU service-budget harness (arm A, answering-ports, answering-every-port, talker-notices), `record_classes.py` and `flip_grade.py`;
  - the firmware gate's four shards and `fw_coverage.py`;
  - `plat_ledger.py`, `test_ctrl_memory.py`, the release-image comparison and `ctrl_boundary.py`.
- **The Milan v1.2 text is not in the repository.** My reading of Tables 5.8, 5.11 and 5.12 rests on the clauses the issue and PR quote, the release fabric's flag law, and the pp_shadow suite's graded expectation.
- **My mutant probes ran two tests only** (AppOutputs and `Core.TheRunningCheckObservesEveryStreamBriefly`), not the whole AECP campaign.
- **No manager source bank ran at this head, and I do not claim one.** Physical calibration was NOT RUN, and no hardware was used. The skipped hosted contexts are not evidence.

## Pending manager duties

- **The merge candidate.** Validate it on current dev (`e275d7950ef3385753e6a15d2e191ba855b171ed`) with the builder and native banks. Re-run `record_classes.py` and `flip_grade.py --check` at 1x1/1if and 8x8/1if on that image. The 1x1/1if paced edit is 101 cycles inside its 310 us statement, and placement moves these records by thousands of cycles. A merged image can therefore refuse where this head passes.
- **The hosted contexts.** Accept them at the exact head; 37 were still queued or running at my snapshot. `firmware-boundary` is expected to refuse the two pre-existing unclassified files.
- **R871-S1.** Put it to the owner: a formal declaring-face arm, and the AECP class statements' margin against placement.
- **File the issue the author reported:** the split's ACMP GET_TX_STATE never sets REGISTERING_FAILED (Milan v1.2 Table 5.47; `plat/ctrl_plat.c:102`, `asking_failed` false).
- **Classify the two boundary files** under #946/#936, outside this PR.

R871-1 FINISHED
