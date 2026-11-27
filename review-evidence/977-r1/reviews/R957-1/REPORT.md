[R957] NEGATIVE - exact head 095995243bc354b8a41755f3fdfae343511cc668

# R957-1: internal independent review of PR #993 (#977) at exact head

- Head `095995243bc354b8a41755f3fdfae343511cc668`, tree `843b1ede3d27b14048269ce9c3b2f9cde65bfdff`.
- Source base `dev-soft-core` `4df125b8`, merged at `163e467f`.
- Pins: tsn-c-stack `5d03517f` (tsn-c-stack PR 41, open), lwSRP `73007b48`, protocol-processor `801ef228` and gptp-processor `3ce71b76` (both unchanged from the base).
- Review scope: the full delta `4df125b8..0959952` (70 files, +2,269/-531) with its history.
- Inputs read: #977's body and every public comment (the rulings of 2026-11-22, 11-23, 11-25 and 11-26), the cited clauses, and the published packet `review-evidence/977-r1` at `f7a322f9`.
- PR #993 has no prior public review finding to resolve or retain. Its only comments are the two review-start notices, and it has no review bodies.

Verdict: NEGATIVE. Two MAJOR and two MINOR findings are open, plus two RESIDUE items. Every lens is unclean (see the ledger).

## Findings

### R957-1-F1 MAJOR (Conformance, RTL, Robustness, Tests): THE DRAIN charges a LeaveAll MRPDU of lwSRP's own shape at the unit, whatever Talkers it registers

- Location: `sw/firmware/ctrl/srp/srp_mbx.c:1038` (`rx_charge`: `if (count == 0u) { break; }`). The claim is at `srp_mbx.c:999` and `ctrl_loop.h:345-346` ("a bound read ... never under that count").
- Authority:
  - #977's ruling of 2026-11-23, item 4: "The count comes from a bound read before parsing, never under it".
  - IEEE 802.1Q-2018 10.8.2.8 f) and g): a VectorAttribute may carry LeaveAll with NumberOfValues 0, its FirstValue still present.
- Evidence:
  - The charge treats any vector whose NumberOfValues is 0 as the end of its Message and moves to the next Message.
  - lwSRP's parser treats only a VectorHeader of 0 as the EndMark (`third_party/lwSRP/src/core/mrp_pdu.c:171`). It goes on to parse, and register, every vector after a LeaveAll-only vector in the same Message.
  - lwSRP itself sends exactly that shape on every LeaveAll: each Message opens with `0x20 0x00` and a zeroed FirstValue, then one single-value vector per attribute (`mrp_mad.c:1507`, `:1572`, `:1729`). Any peer running this stack therefore sends it.
  - Probe (`scripts/probe_leaveall_charge.cpp`, `receipts/probe-leaveall-{1x1,8x8}.log`): one Talker Advertise Message of [LeaveAll, 0 values][a, JoinIn][b, JoinIn] at both one-interface shapes.
    - The record registers both Talkers (`registered_kinds` 2 and 2).
    - The charge is 285 us at 1x1/1if and 375 us at 8x8/1if, the bare unit. It should be at least 505 and 625.
    - The existing `TheDrainChargesARecordTheTalkersItsVectorsCanRegister` passes in the same build.
- Tests gap: no charge case has a zero-value vector. The burst group's LeaveAll sets the LeaveAll bit on the value vector itself (`tb/verilator/ctrl_service_budget/frames.py:175`, `register_window.py` `declared`), so neither the gate nor the harness ever sends the shape lwSRP sends.
- Impact (derived, not measured):
  - At 8x8/1if, a LeaveAll MRPDU registering 9 Talkers is charged 375 us instead of 1,500 us.
  - It can therefore start with only the unit left in its 1,475 us slice and run about 1.1 ms past the slice's end.
  - That is a pass past THE SHARE (2 ms), which ruling item 2 says must hold under a legal burst.
  - Registrations in a LeaveAll MRPDU are legal at the MRP state machines' rate, the count the ruling adopted, for example a kind swap or new Talkers at the opportunity whose leavealltimer ran out.
- Required outcome:
  - The charge's bound is never under the Talker values lwSRP can register from the record.
  - A zero-value vector skips its FirstValue and continues within the Message, as `parse_pass` does.
  - The registering measurement includes a LeaveAll MRPDU in the shape lwSRP sends.
- Verification:
  - A charge case with a LeaveAll-only vector ahead of Talker vectors fails at the head and passes after the fix, with a planted defect re-introducing the early `break`.
  - A registering group whose LeaveAll record has lwSRP's layout, graded within THE SHARE and its slice at both points.

### R957-1-F2 MAJOR (Conformance, Docs): the lwSRP pin is an unpublished commit, and the "own PR" it cites does not exist

- Location: the gitlink `third_party/lwSRP` = `73007b4807977517045e8aa485c61ebb8f5ee843` (base `d1bb4f4e`, lwSRP `main`).
- Authority:
  - #977's ruling of 2026-11-23, item 3: "an lwSRP PR beyond opt-exec-1".
  - AGENTS.md section 1: project state must be public.
  - The PR body: "lwSRP is pinned at `opt-exec-3` (its own PR against lwSRP `main`)", and its "How to get into the same state" step `git submodule update --init third_party/lwSRP`.
- Evidence (`receipts/lwsrp-pin-published.txt`):
  - `git ls-remote https://github.com/kebag-logic/lwSRP.git` lists `opt-exec-1` and `opt-exec-2`, but no `opt-exec-3` and no ref at `73007b48`.
  - The commits API answers "No commit found" for `73007b48`.
  - lwSRP's pull requests (all states) hold none for this work.
  - The pinned delta over `main` is 20 commits, +724/-13 in `src/`. `srp_entity.py` enables it at both product shapes: the buckets, `LWSRP_ONE_PORT_MAP`, `LWSRP_LEAN_VALIDATE`, `LWSRP_RAPID_REPLACE`, `LWSRP_LEAN_COPY`, `LWSRP_LEAN_TX`, and `LWSRP_TX_MERGE` at 8x8/1if.
- Impact:
  - A cold checkout cannot fetch the pinned commit, so the PR's own validation commands cannot be reproduced from public state.
  - No hosted run exists at this head (`receipts/hosted-and-pins.txt`: 0 workflow runs, 0 check runs).
  - Product code compiled into both one-interface images has no public review lane.
- Required outcome:
  - `73007b48` is reachable on the lwSRP remote under a named branch, with its own lwSRP PR against `main`.
  - The PR body's claim is true and linked.
  - Whether the pin later moves to that PR's merge commit is recorded, as ruling item 4 records it for tsn-c-stack.
- Verification: a fresh clone with `git submodule update --init third_party/lwSRP` checks out `73007b48`, and the lwSRP PR link resolves.

### R957-1-F3 MINOR (Tests): THE DRAIN's "alone" rule is gated only on its settle condition

- Location: `sw/firmware/ctrl/loop/ctrl_loop.c:355` (`alone = !settled && l->stats.rx_records == taken && l->stats.ticks == ticks`). The test is `sw/firmware/ctrl/test/test_port_loop.cpp:1556` (L23b).
- Authority:
  - Ruling item 4 (a record alone in a slice starts on the unit).
  - `ctrl_loop.h` THE TIERS: alone means "the first of a pass whose THE SETTLE did nothing and that took no tier-1 record and dispatched no centisecond".
  - AGENTS.md section 6, Tests: each claimed behaviour has a test that can fail for it.
- Evidence (`scripts/run_mutant.py`; `receipts/mutant-alone-after-tier1.log`, `receipts/mutant-alone-after-tick.log`):
  - Dropping the tier-1-record condition leaves the port loop suite (53 checks) and the SRP mailbox suite at 1x1/1if and 8x8/1if (114 checks each) passing. So does dropping the centisecond condition.
  - Both mutants ESCAPE. `loop_step_mutants.charge_mutants` plants only the settle condition, the charge and `n == 0`.
- Impact: a regression that starts an over-slice record after tier 1's drain has spent its time, the case the condition exists for, passes the firmware gate.
- Required outcome: L23b (or a test of its own) drives a pass that takes a tier-1 record, and one that dispatches a centisecond, before an over-slice record. Each condition gets a planted defect the test catches.
- Verification: both mutants above are caught by name.

### R957-1-F4 MINOR (Docs): the decision this round implements is not public

- Location: the PR #993 body, Status ("Round 8 applies the owner's decision on the one open item ... (option (a))"). The published `HANDOFF-r8.md` calls the same decision a manager decision.
- Authority: AGENTS.md section 2 ("A future cold reviewer must be able to reconstruct the task from GitHub and the repository alone") and section 4.
- Evidence:
  - #977's last public comment is the ruling of 2026-11-26. Neither #977 nor #993 carries round 7's STOP or the decision on it.
  - The decision sets the published mailbox bound `ADP_MBX_LAT_LINK` 11 -> 12 (`adp_mbx.h:114`, `MAILBOX_SPLIT.md:693`).
  - The PR and the packet name its decider differently.
- Impact: a cold reviewer cannot confirm who chose option (a) over the alternatives (for example #1015's clock), or what the decision bounds.
- Required outcome: round 7's STOP and the decision are on #977 (or #993) with the decider named, and the PR body links them.
- Verification: the link resolves, and the PR body and the packet name the same decider.

### R957-1-R1 RESIDUE (Docs): comment-rule wording in the reviewed delta (owner rule 2026-10-15)

27 new instances, from `scripts/comment_rule_scan.py` (`receipts/comment-rule-scan.txt`). Each is wording only. The exact fix is to drop the round, lane, role or comment-ID token and keep the behaviour, the figure and the issue or ruling ID.

- Review rounds:
  - `sw/firmware/ctrl/aecp/aecp_mbx.h:78` ("round 2's walk of 80 us"). Fix: "#977's earlier walk of 80 us".
  - `sw/firmware/ctrl/loop/ctrl_loop.h:383` ("its round 2's walk"). Fix: "#977's earlier walk of 80 us".
  - `tb/verilator/ctrl_service_budget/load_grade.py:233-235,336-352` (rounds 2 to 6). Fix: name each image by its commit alone, as the same lines already do (for example `3de17804`, `8b4a79d5`, `fda89791`).
  - `tb/verilator/ctrl_service_budget/poll_grade.py:108,114,116,148,152,153` (rounds 2, 3 and 5). Same fix.
  - `tb/verilator/ctrl_service_budget/whole_grade.py:11` ("the manager's answer to its round 2's first question"). Fix: "(#977)".
- Issue-comment ID: `tb/verilator/ctrl_service_budget/flip_grade.py:64` ("issuecomment-7160202807"). Fix: "#977's owner decision of 2026-11-25".
- Lane name: `sw/litex/ctrl_memory.py:275-344` (+6 "owed to S14"). Fix: "owed to the hybrid XIP lane's issue", or the issue number.

### R957-1-R2 RESIDUE (Docs): stale PR title

The PR title reads "(#977, round 2 of 3)", while its Status section describes round 8. Exact fix: "Register Talkers at the MRP state machines' rate within THE SHARE (#977)".

## Checked and clean within each lens (artifact evidence; the lenses stay unclean by the findings above)

- **Conformance**
  - The LINK_UP window: `scenario.py:263-270` waits 4,200 ms. That is right for Milan v1.2 5.6.3.5.3 and Table 5.50 (LINK_UP out of DOWN draws 0 to 4 s, where 5.6.3.5.2's startup draw is 0 to 2 s): the scenario raises the link after enable (`ready(..., link=False)`).
  - The negative control (`receipts/harness/adp-link-up-window-control.txt` in the packet): under the 2.2 s window, 1x1 `adp-advertise` is refused in both arms, with the TMR_DELAY expiry at cycle 355,700,083. The head's regrades of the same arms pass.
  - `ADP_MBX_LAT_LINK` 12 and the `LINK_UP / LINK_DOWN 12 / 9` row are byte-equal to #1015's `35d29eb7` (`adp_mbx.h:123`, `MAILBOX_SPLIT.md:697` there). So are the `seed-left-at-zero` plant and `scenario.py`, apart from #977's own `register_window` import.
  - C0 measures 12 accesses against its bound of 12 (`receipts/own/arm-adp.log`). The author's gate logs catch `latency-extra-read`.
  - The rate premise matches IEEE 802.1Q-2018 10.7.11 (at most three transmit opportunities in any 1.5 x JoinTime) and Milan v1.2 Table 4.3 (JoinTime at least 180 ms).
- **RTL**
  - No HDL, synthesis or constraint file is in the delta. The protocol-processor and gptp-processor gitlinks are unchanged.
  - Read in full: the loop's drain and charge, THE SETTLE, `mbx_rx_next_len`/`_byte` (the ring index is masked), `mbx_tick_pending` (consumes nothing), `transmit_aged`, the sink index, the held and kept octet sets, and `declared_alone`. Apart from F1, I found no width, ordering or reset defect. `reset_interface` clears `declared_alone` and the kept octets.
- **Robustness**: `rx_charge` is bounded by the record's length. It needs a waiting record (`rx_ready` requires `mbx_rx_waiting`). A bad header can only charge more, and `mbx_rx_take` then resyncs. The EndMark, a list length past the record, and the eight-Message cap all over-count, never under.
- **Tests**
  - My own runs at the head, under `receipts/own/`:
    - Port loop: 53 checks, 0 failures.
    - ADP: 77 checks, 0 failures.
    - ACMP: 165 checks, 0 failures.
    - SRP mailbox: 114 checks, 0 failures, at each of 1x1/1if and 8x8/1if.
    - SrpBinding and SrpGate: 22 checks, 0 failures, at each point.
    - SRP Talker declarations: 219 checks, 0 failures, at each point.
    - `load_grade --check`: PASS, 1x1/1if 0.518 of 0.70.
    - `load_grade --selftest`: 28 of 28 controls refused.
    - `flip_grade --check`: PASS at both points (1x1/1if: last 132.95 of 135 ms, ACMP 29.40 of 30, txL 47.98 of 49; 8x8/1if: load 0.757 of 0.76, THE TRANSMIT 76.86 of 77 ms).
    - `flip_grade --selftest`: 616 of 616 refused.
    - `shape_costs`: `--check` PASS; `--selftest` 25 of 25 refused.
    - `kept_grade --selftest`: 33 checks PASS.
    - `egress_ledger --selftest`: 18 mutants PASS.
    - `check_py_idiom`: long module 10 <= 10, with `scenario.py` at 1,000 lines.
    - `ctrl_hot --check`: 279 entries, in the recorded order.
    - `run.py --self-test`: partial (stopped by the session's process limit). Its first 1,242 lines are byte-identical to the author's receipt at this head.
  - Published receipts:
    - All 16 arms exit 0.
    - The two large arms at each point carry only the seven `backlog` / `backlog-owed` rows over 20 ms, and 0 passes over THE SHARE.
    - The firmware gate's four shards pass at `ea52ec11`.
- **Docs**: FR_NFR 3.4.1 records 0.76 and the second-hart trigger met at 0.757. `SPLIT_CONTROL_MEMORY.md`, `MAILBOX_SPLIT.md` and the harness README carry no stale LINK_UP window figure.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | `srp_mbx.c:999-1047`, `mrp_pdu.c:129-240`, `mrp_mad.c:1507-1590`, IEEE 802.1Q-2018 10.7.11 and 10.8.2.8, Milan v1.2 5.6.3.5.2-3, Table 5.50 and Table 4.3, `adp_mbx.h:114`, `scenario.py:263-270`, #1015 `35d29eb7`, `receipts/lwsrp-pin-published.txt` | R957-1 | 095995243bc354b8a41755f3fdfae343511cc668 |
| RTL | UNCLEAN (F1) | `ctrl_loop.c:176-360`, `ctrl_loop.h:200-440`, `ctrl_app_srp.c:47-196`, `mbx.c:505-695`, `srp_mbx.c` delta; no `hdl/`, `syn/` or constraint file in `git diff --name-only 4df125b8..HEAD` | R957-1 | 095995243bc354b8a41755f3fdfae343511cc668 |
| Robustness | UNCLEAN (F1) | `rx_charge` against malformed, over-long and EndMark records; `rx_ready`; `mbx_rx_take` resync; `reset_interface`; `receipts/probe-leaveall-*.log` | R957-1 | 095995243bc354b8a41755f3fdfae343511cc668 |
| Tests | UNCLEAN (F1, F3) | `srp_mbx.cpp:473`, `test_port_loop.cpp:1556`, `srp_drain_mutants.py`, `loop_step_mutants.py` `charge_mutants`, `register_window.py`, `frames.py:175`, `receipts/mutant-alone-*.log`, `receipts/own/*` | R957-1 | 095995243bc354b8a41755f3fdfae343511cc668 |
| Docs | UNCLEAN (F2, F4) | PR #993 body and title, #977 comments, packet `REVIEW-READY.md` and `HANDOFF-r8.md`, `FR_NFR.md` 3.4.1, `MAILBOX_SPLIT.md:530-536,693`, `receipts/comment-rule-scan.txt` | R957-1 | 095995243bc354b8a41755f3fdfae343511cc668 |

## Merge notes (conflicts beyond the stated ones)

All trial merges used `git merge-tree` (receipts `receipts/merge-tree-*.txt`).

- With #1015 (`35d29eb7`): conflicts only in the tsn-c-stack pin's docs and diagram (`SUBMODULES.md`, `submodule_boundaries.*`, `PNG_MANIFEST.json`), as the PR states.
- With #1017 (`079c4fa1`): a further conflict in `docs/design/SPLIT_CONTROL_MEMORY.md` (the ledger's section 3 and 5 figures). #1017 adds 72 B of `rom` at the 1x1 points and 64 B at the 8x8 points to images #977 sits near the edge of. So the composed ledger entries need re-measuring at the merge, not only re-wording.
- With live `dev-soft-core` `ba13338b` (PR #1019 merged after `4df125b8`): a conflict in `sw/firmware/ctrl/test/test_ctrl_firmware.py`.
  - #1019 slices each SRP campaign table by `[share]`, while #977 filters out its drain plants and adds `srp_drain_mutants` and `srp_lane_mutants` prefixes.
  - A resolution that keeps only one side silently drops either the shard slicing or #977's plants.
- In the landing order #1017, then #1015, then this PR, all three conflict sets appear together.

## Real limits

- The full firmware gate with planted defects, the CPU budget harness arms, routes, the twin and the builder legs were not run by this review. I used the author's published receipts for them, and checked them against the PR's claims.
- My background runs of `run.py --self-test` and of the firmware gate without plants were stopped by the session's process limit. Neither result is claimed.
- The lwSRP delta (20 commits) was read only where F1 needed it (`mrp_pdu.c` parse, `mrp_mad.c` LeaveAll encoding). It has no public review (F2).
- tsn-c-stack PR 41 is reviewed separately, and was not reviewed here.
- F1's pass-length impact is derived from the stated costs and the probe's charge, not measured on the harness.
- No hosted job exists at this head. Physical calibration was NOT RUN, and nothing here is hardware evidence.
- No manager source bank ran at this head, and none is claimed.

## Pending manager duties

- Publish lwSRP `opt-exec-3` (`73007b48`) and its lwSRP PR, or re-pin (F2).
- Publish round 7's STOP and its decision on #977 (F4).
- Carry R1 and R2 to the residue checklist.
- At the merge turn:
  - Resolve the `test_ctrl_firmware.py` conflict, keeping both #1019's `[share]` slicing and #977's plant filters, and re-run the planted-defect campaign.
  - Re-measure the memory ledger after #1017.
  - Regenerate the pin docs and diagram after #1015.
  - Move the tsn-c-stack pin to PR 41's merge commit and re-measure there (ruling item 4).
  - Own the hosted and act acceptance at the candidate.

R957-1 FINISHED
