[R843] NEGATIVE - exact head 8883d4998496c6d2e234143b43807731e8851b63

# R843-5: internal delta review of PR #914 (issue #894, lane 894b), rounds 8 to 12

- **Head:** `8883d4998496c6d2e234143b43807731e8851b63`, tree `a169a601df764715eec1b404b16da3df73217142`.
- **Delta:** from `d539f162` (round 7) to the head: 16 first-parent commits, among them the `--no-ff` merge of dev-soft-core `70f4056f` (`d1c9023b`).
- **Source base:** `7398ec0aeea468d92ff642a03a06e291a0cd58d1`.
- **How I worked:** a cleared-context independent session. I reconstructed the task from public state only. I read no other reviewer's report before my own pass and ledger were written. Prior public findings were read afterwards and are resolved or retained below.

## Verdict

**NEGATIVE.** One MINOR is open (R843-5-F1, lenses Tests and Docs).

The #930 fix itself is correct and well tested:
- The differential test passes at 1x1/1if and 8x8/1if.
- Every new mark and copy site has a plant that is caught by name.
- Seven further reviewer plants were run. Every non-equivalent one is caught at both shapes.
- The targets hold, as I re-ran them: SRP's record is 250 us by the rule against 280 stated; the last queued notice is 136.65 ms against 140; the 8x8/1if load is 0.735 against 0.75.
- Both ledger moves follow their rulings.

What fails the bar is narrower. Round 8 keyed THE TRANSMIT's figure per shape. At 8x8/1if that figure, `CTRL_LOOP_TX_MS` = 70 ms, is a term of the withdrawn-Talker hold-off (IEEE 802.1Q-2018 35.2.2.8). No in-tree gate holds it, yet `ctrl_loop.h` says one does. I planted it at 60 ms and every grader output was identical to the head's.

Three RESIDUE items (one retained from R843-4) and two new SUGGESTIONs are also recorded. Prior SUGGESTIONs are retained as optional.

## Context reconstructed

I read, in this order:
1. AGENTS.md, then the review and lens rules it states.
2. Issue #894's body and acceptance criteria.
3. The rulings in the delta's range:
   - #894 issuecomment-6892938049 (the held-egress rule and the STOP list);
   - 6914952893 (round 8 STOP: the ledger move and the `srp-talker-held` group);
   - 6918853411 (round 9 STOP: the #930 fix and its targets);
   - 6934688411 (round 10 STOP: `service.aecp.last` to 62.16 ms, the targets accepted, the single column at the pin);
   - 6938589932 (round 11 STOP: the retargeted plants, twin owed to #935).
4. The round 8 STOP (6914891355) for the merge's resolution claims, and the freeze rule (#665 issuecomment-6939574513).
5. Issue #930's body: its fix, acceptance and targets.
6. REVIEW READY (#894 issuecomment-6939551029) and the review start comment (#914 issuecomment-6939647555).
7. Then:
   - the remerge diff of `d1c9023b`;
   - `git diff d1c9023b..8883d499` and each commit of rounds 9 to 12;
   - the author packets `author-r8` to `author-r12` from archive `88f4b944`.

## Findings

### R843-5-F1: MINOR. Lenses: Tests, Docs.

**8x8/1if's `CTRL_LOOP_TX_MS`, the hold-off's THE TRANSMIT term, is held by no in-tree gate, and `ctrl_loop.h` says it is.**

- **Where:**
  - `sw/firmware/ctrl/loop/ctrl_loop.h:355` (`#define CTRL_LOOP_TX_MS 70u` in the (1, 9, 9) block);
  - `sw/firmware/ctrl/loop/ctrl_loop.h:463-466`, which says "rows_tiers.py, the tx row, which refuses a tree whose row passes this ... 70 ms at 8x8/1if for its 69.84";
  - `tb/verilator/ctrl_service_budget/flip_grade.py:60`, `:404`, `:420`;
  - `tb/verilator/ctrl_service_budget/rows_grade.py:93`.
- **Authority and evidence:**
  - Round 8 made `CTRL_LOOP_TX_MS` a per-shape figure in THE SHAPES. At 8x8/1if it is "its own tx row by every source rounded up", and since #901 it is a term of `SRP_REDECLARE_CS` (`srp_mbx.c:35`). That is the hold-off that keeps two LeaveAllTime periods after the Leave departs (IEEE 802.1Q-2018 35.2.2.8).
  - At the other two keyed shapes the statement is held by `rows_tiers.tx_statements`. `flip_grade.py --check` runs it through `row_findings`, and the self-test plants each one under its row (`flip_grade.py:196-202`, 1x1/1if and 8x8/2if).
  - At 8x8/1if there is no such hold. 8x8/1if is `REPORTED` (`flip_grade.py:60`), so `row_findings`, and with it `tx_statements`, is never called for it (`:404`, `:420`).
  - The in-tree model cannot derive the row there anyway: `rows_grade.ROW_COSTS` has no 8x8/1if entry (`rows_grade.py:93`), and calling `tx_statements` at 8x8/1if raises `KeyError: '8x8/1if'`. The 69.84 ms figure comes from a packet-side derivation.
  - **Probe** (`scripts/tx_plant_probe.sh`, receipt `receipts/tx-plant-probe.txt`). I planted 8x8/1if's `CTRL_LOOP_TX_MS` at 60 ms in a disposable export of the head. That is under its 69.84 ms row, and low enough that the hold-off's `ceil(TX/10)` term drops from 7 cs to 6. Results:
    - `shape_costs.py --check`: PASS.
    - `flip_grade.py --check --point 8x8/1if`: PASS.
    - `load_grade.py --check`: PASS.
    - `rows_tiers.py --selftest`: 1033 of 1033.
    - `flip_grade.py --check` over every point gives the same 12 `OVER`/`RESULT` lines as the head (8x8/2if's, by design). None names 8x8/1if.
- **Impact:**
  - At this head the figure is right: 70 ms is at least 69.84, and the hold-off is 2,026 cs.
  - What is missing is any hold on it. Suppose 8x8/1if's costs grow so that its tx row passes 70 ms, or the figure is mis-edited downward. Every gate stays green, and the hold-off then undercounts the Leave's latest departure at 8x8/1if.
  - This is the one 8x8/1if figure in THE SHAPES held by nothing executable. The queued bound, the slice, the builds, the SRP unit and THE RETRY's costs are each held by a harness grader.
  - The source comment says a gate refuses the drift, and at this shape none does.
- **Required outcome:** one of the following.
  - (a) An in-tree check holds 8x8/1if's `CTRL_LOOP_TX_MS` at or over its tx row by every source, with a planted control that refuses a figure under the row at 8x8/1if, as `flip_grade.py:196-202` does for 1x1/1if and 8x8/2if.
  - (b) A maintainer ruling records 8x8/1if's figure as held by no gate, owed to #872 with its rows. `ctrl_loop.h:463-466`, section 13 and the SRP README then say so, and stop naming `rows_tiers.py` as its guard there.
  - The ruling on round 8's STOP (item 4) settled the keying's value, not how it is held. So (b) needs its own ruling.
- **Verification:**
  - For (a): re-run `scripts/tx_plant_probe.sh`. The 60 ms plant (and a 69 ms one) must be refused by name, and the head must pass.
  - For (b): read the ruling and the reworded comment and docs.

### R843-5-R1: RESIDUE. Lens: Docs.

**`load_grade.py`'s table header calls the second column "owed to the pin move", which round 10 states is already at the pin.**

- **Where:** `tb/verilator/ctrl_service_budget/load_grade.py:567`, the header `Load with tsn-c-stack#32 (owed to the pin move)`. The text predates the delta; round 10 made it false.
- **Evidence:** round 10's `11a9b4bf` states at `load_grade.py:24-28` that "The pin already carries tsn-c-stack#32 ... both columns state one image's costs". The ruling on round 10's STOP accepts the single column at the pin. The printed header still says the column is owed to a pin move that has happened (`receipts/harness-checks.txt`, load table).
- **Exact fix:** replace `Load with tsn-c-stack#32 (owed to the pin move)` with `Load at the donor's measured costs (the pin carries tsn-c-stack#32)`.
- **Verification:** a wording-only change to a printed header. No figure, column or verdict changes.

### R843-5-R2: RESIDUE (packet text, not the tree). Lens: Docs.

- **Where:** `review-evidence/894b-r1/author-r12/INDEX.md:1` in archive `88f4b944`. It reads "# 894b-a781 round 11 output index" but indexes round 12's packet.
- **Exact fix:** read "round 12" in later packets. The immutable archive need not be rewritten.

### R843-4-R1: RESIDUE, retained and widened. Lens: Docs.

- **Where:** `docs/reference/FR_NFR.md:393`, "Measured on the image whose SRP adapter copies ... which the head carries, as on each image before it (the image that merges dev-soft-core `70f4056f`, ..., and the image whose THE RETRY's round costs are its shape's ..., among them), each holds: every row the CPU decides within its bound, every join interval within the gate, every round of THE RETRY within its statement, and the load 0.735 at the pin (0.718 ...)".
- **Evidence:**
  - R843-4's point stands: round 2's image did not hold every round of THE RETRY (section 13, its 1,654 rounds).
  - The delta widened it. "Each holds ... the load 0.735" now reads as held on the composed image too, whose load was 0.718, given in brackets in the same sentence. The head's own claim is correct.
- **Exact fix:** replace "which the head carries, as on each image before it (the image that merges dev-soft-core `70f4056f`, #901's Talker declarations, and the image whose THE RETRY's round costs are its shape's, [#894's round 3 ruling](...), among them), each holds:" with "which the head carries, holds, as the image that merges dev-soft-core `70f4056f` (#901's Talker declarations) and round 3's image (whose THE RETRY's round costs are its shape's, [#894's round 3 ruling](...)) each did at their own figures:".
- **Verification:** a wording-only diff.

### R843-5-S1: SUGGESTION. Lens: Tests.

- **Where:** `sw/firmware/ctrl/test/srp_listener_mutants.py:34` and `srp_mutants.py:93-105`, `:225-237`.
- **Evidence:**
  - Round 12 moved `asking-is-ready` and `readyfailed-ignored` to the Listener's indication. Since then no table plant mutates the registrar walk's own copy, `srp_mbx.c:861` (`i->registered[n] = v[8] == 2 || v[8] == 3;`).
  - That copy still decides `registered` after every walk a Talker indication, binding or declaration owes.
  - My plants of both old mutations there (`reviewer-walk-asking-is-ready`, `reviewer-walk-readyfailed-ignored`) are caught by `Listeners.RandomRecordsMatchTheReferenceWalk` by name at 1x1/1if and 8x8/1if (`receipts/listener-plant-walk-*.txt`). So the behaviour is tested; only the campaign has lost its regression plant there.
- **Optional:** add both as `listener-copy-walk-*` entries.

### R843-5-S2: SUGGESTION. Lens: Tests.

- **Where:** `sw/firmware/ctrl/test/srp_listeners.cpp:331-337`.
- **Evidence:** the differential runs two fixed seeds of 3,000 steps each. Each of my extra plants is caught on the first seed.
- **Optional:** add a seed taken from the environment, printed on failure, so a campaign or nightly run can widen the sequence space without changing the gate.

## Prior public findings at this head

| Finding | Status | Evidence |
|---|---|---|
| R843-4-R1 (RESIDUE): FR_NFR "as on each image before it" | **RETAINED**, widened (above) | `FR_NFR.md:393` at the head |
| R843-4-S1 (SUGGESTION): packet F1 check by substring | Retained, optional | Packet tooling; no figure at this head depends on it |
| R843-3-S1 (SUGGESTION): 8x8/1if retained retry not at the unit | **Partly addressed**, retained | `poll_grade.py`'s `EIGHT_ONE` comment now says the retry is 8x8/1if's own apply measurement, 32,618 cycles, 345 us. The general rule at `:73` still says "stated at the SRP record's cost (280 and 365 us)". |
| R843-3-S2 / R843-2-S2 (SUGGESTION): debug/wire arms at the tracked contract | Retained, optional | Not in the delta |
| R843-3-F1, F2, R1, R2; R844-3-R1 to R4 | Resolved before `d539f162` (R843-4) | Not reopened. The delta keeps each fix (`record_classes.py:98`, `MAILBOX_SPLIT.md:390`, the section 13 labels). |
| R844-1-F1, R843-1/2 items | Resolved earlier | The delta does not touch their causes. `egress_ledger.py`'s refusal reading is kept, with two new mutants. |

## What I checked, item by item

1. **The sync's resolutions** (`git show --remerge-diff d1c9023b`, 17 files). Each conflict keeps both sides:
   - **1x1/1if takes #901's figures:** the slice 900 us, the queued bound 140 ms, the polls' base 225 us and the restated `TWO` costs.
   - **8x8/1if keeps its own:** the slice 1,475 us, the builds 1,795 and 1,475 us, the SRP unit 365 us, THE RETRY 165 and 25 us, and the queued bound 130 ms.
   - **The two-interface shapes** take 8x8/2if's figures: 62 and 105 ms.
   - **`AECP_QUEUED_MS`** is `CTRL_LOOP_QUEUED_MS`. `shape_costs.py` refuses it keyed on the interface count, by a planted control.
   - **The hold-off:** `SRP_REDECLARE_CS = 2*1000 + CTRL_LOOP_JOIN_CS (19) + ceil(TX/10)`. That is 2,023, 2,026 and 2,030 cs at 34, 70 and 105 ms, each at least 35.2.2.8's 2,000 cs. The `ctrl_loop.c:203` assert is keyed on shape (1, 2, 2) alone; 34 is within 49.
   - **F1** is the one gap found here.
2. **#930's fix.** `srp_mbx.c:175-192` (`listener`), `:394-404` (`listener_moved`) and `:405-432` (`moved`), with `talker_changed` keeping its mark (`:199`).
   - **Conformance of the claim:** every Registrar change into or out of MT carries an indication (IEEE 802.1Q-2018 Table 10-4). New! or Join! takes MT to IN; Lv! comes at leavetimer! or Flush! into MT. IN and LV, the moves with no indication, are both "present", as the walk counts them.
   - **Licences and declarations:** the licence is still published only where `active` changes (`:1197-1213`). The declarations are untouched.
   - **The differential** (`srp_listeners.cpp`): real lwSRP and the head's `srp_mbx.c`, with the reference run restoring the old walk schedule through renamed seams. It compares every mailbox write, licence call and state per step, and checks `holds_walk` on every settled step.
   - **My run:** 2 of 2 tests PASS at 1x1/1if and at 8x8/1if (`receipts/listener-arms.txt`).
   - **The five `listener-copy-*` plants** and the two retargeted plants:
     - In the author's SRP campaign: 436 `[ok]` and 0 `[ESCAPED]` in the verdict section of `rtl-fast__firmware-srp-mutants__ci_step_9.log`, final line `test_ctrl_firmware: PASS`.
     - My own re-plant of the two retargeted ones: caught by name at one and two interfaces (`receipts/table-retargeted-if{1,2}.txt`).
   - **Seven further reviewer plants at both shapes** (`scripts/listener_probe.py`):
     - **Caught by name (six):**
       - `dispatch-any-type` (a Talker's Registrar change taken as a Listener's presence);
       - `presence-always`;
       - `arrival-dropped`;
       - `leave-not-copied` (the Leave indication's copy dropped);
       - `indication-readyfailed-dropped`;
       - both walk-copy plants (S1).
     - **Escaped as expected (one):** `dispatch-any-slot`, which is equivalent: MVRP's attribute type 1 is never MSRP's Listener type 3.
     - **One harness note:** the first run of `leave-not-copied` failed to compile (unused parameters under `-Werror`). That is why `receipts/listener-plants-*.txt` ends RESULT FAIL from that one line. It was fixed in the probe and re-run (`receipts/listener-plant-leave-*.txt`).
   - **I found no licence or declaration left stale, and no Listener skipped whose registration changed.**
   - **Robustness:**
     - The random steps (`srp_listeners.cpp:199-262`) include LeaveAll, all six events with all four declarations, two-value messages, link down and up, allocation refusal mid-record, and bindings.
     - A reset clears presence (`:1035`). The creation marks the walk, so `registered` is rebuilt before any licence decision.
   - **Coverage:** `srp_mbx.c` is at 746 of 746 lines and 100 % of branches after the README's exclusions (`author-r11 .../rtl-fast__firmware-unit__ci_step_12.log:89`, at `05a7ea82`). Round 12 changes only `srp_mutants.py`.
3. **The targets.** My own runs at the head (`receipts/harness-checks.txt`):
   - **1x1/1if, last queued notice:** 136.65 ms by every source against 140 (`flip_grade.py --check --point 1x1/1if`).
   - **8x8/1if, load:** 0.735 at the pin against 0.75 (`load_grade.py --check`); 1x1/1if's is 0.517.
   - **Self-tests:** the flip check refuses 612 of 612 controls, the load gate 28 of 28, and the ledger self-test passes its 15 mutants.
   - **The SRP record:** 23,503 cycles is 250 us by the rule, against 280 stated, which is round 7's figure. At 8x8/1if, 32,936 cycles is 350 us, within 8x8/2if's 365.
   - **Restatements, each down to its earlier figure and never below the measurement:**
     - the retained retry: 280 and 345 us, for 245 and 345 measured;
     - the SRP unit: 280 and 365 us;
     - 8x8/1if's reclaim: 40 us for 3,446 cycles;
     - 8x8/1if's walk and base: kept at 120 and 280 us, over their measurements.
   - **Every row in `srp-talker-held`** "fits" in the author's tables at `46cf2a7d`, at both points. That includes the LeaveAll MRPDU row at 8x8/1if: `srp-talker-held.mrpdu.leaveall.if0`, 1.054 ms of 49.
4. **The ledger moves.** `egress_ledger.py` states `MERGED`, `COMPOSED` and `LISTENED` and derives each figure from the largest. I re-derived each by the rule (60 ms plus 1.05 times the service, rounded up to 0.01 ms):
   - 63.67337 → 63.86;
   - 63.90106 → 64.10;
   - 64.14858 → 64.36;
   - 64.38819 → 64.61;
   - 64.62511 → 64.86;
   - 62.49045 → 62.62;
   - `service.aecp.last` 62.04905 → 62.16.

   Each matches its ruling, and both measurements are stated beside it. Section 13's table states all three. The gates at `05a7ea82` PASS at both points (`author-r11/receipts/harness/gate-*-05a7ea82.txt`).
5. **The evidence.**
   - **The archive:** `88f4b944`'s 918 files for rounds 8 to 12 each match MANIFEST.json, with none unlisted (`receipts/packet-verify.txt`). The archive commit carries no GPG signature, so integrity rests on the commit ID and its manifest.
   - **The shards:** 1, 3, 4, 6, 10 and 17 hold 9 + 9 + 1 + 5 + 6 + 7 = 37 suites, 966,909 checks and 0 failed. Their clones are at the head, with the head's six gitlinks.
   - **The images:** the eight are byte-identical to `46cf2a7d`'s by ELF sha256. I confirmed structurally that `git diff 46cf2a7d..8883d499` touches no firmware source: two docs, two test drivers and two graders.
   - **The comment rule:** my scan of the delta's added non-Markdown lines found no issue-comment ID, lane, round, reviewer or bench label.

## Lens results

```text
[R843] PASS Conformance - sw/firmware/ctrl/srp/srp_mbx.c:28-35,175-192,394-432 against IEEE 802.1Q-2018 Table 10-4 and 35.2.2.8; ctrl_loop.h:338-375 THE SHAPES; flip_grade.py --check --point 1x1/1if (136.65 of 140 ms) and load_grade.py --check (0.735 of 0.75) at 8883d499 - the copies' indication claim holds per Table 10-4, every shape's hold-off is over 2,000 cs, and #930's targets are met
[R843] PASS RTL - srp_mbx.c/.h state flags (registered, listener_present, active, stop_owed, stale) at 8883d499; moved() noinline against plat/ctrl_split_hot.txt:181; platform-8x8-1if 130,336 of 131,072 B (56.0 RAMB36) in author-r12 qimg receipt - no HDL in the delta; firmware state paths complete, a reset clears the copies, the image within its entry
[R843] PASS Robustness - srp_listeners.cpp:199-262 random steps (LeaveAll, six events x four declarations, two-value messages, link flap, mid-record refusal, bindings) and receipts/listener-plant*.txt at 8883d499 - every non-equivalent reviewer plant caught at 1x1/1if and 8x8/1if
[R843] UNCLEAN Tests - flip_grade.py:60,404,420 and rows_grade.py:93 at 8883d499; receipts/tx-plant-probe.txt - R843-5-F1: 8x8/1if's CTRL_LOOP_TX_MS is held by no gate (a planted 60 ms passes every grader); the #930 differential and plants otherwise PASS (receipts/listener-arms.txt, table-retargeted-if{1,2}.txt)
[R843] UNCLEAN Docs - ctrl_loop.h:463-466 at 8883d499 - R843-5-F1: the comment names rows_tiers.py as refusing a tree whose row passes the figure, false at 8x8/1if; RESIDUE R843-5-R1, R843-5-R2 and R843-4-R1 recorded with exact fixes
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `srp_mbx.c:28-35,175-192,394-432` against 802.1Q-2018 Table 10-4 and 35.2.2.8; `ctrl_loop.h:338-375`; `flip_grade.py --check` (both points); `load_grade.py --check`; rulings 6914952893, 6918853411, 6934688411, 6938589932 | R843-5 | `8883d4998496c6d2e234143b43807731e8851b63` |
| RTL | CLEAN | `srp_mbx.c`/`.h` state paths; `ctrl_loop.c:203`; `plat/ctrl_split_hot.txt:181`; image and ROM receipts (`author-r12/receipts/images/*`); `git diff 46cf2a7d..8883d499` (no firmware source) | R843-5 | `8883d4998496c6d2e234143b43807731e8851b63` |
| Robustness | CLEAN | `srp_listeners.cpp`; seven reviewer plants at 1x1/1if and 8x8/1if; `reset_interface` (`srp_mbx.c:1017-1045`) | R843-5 | `8883d4998496c6d2e234143b43807731e8851b63` |
| Tests | UNCLEAN (R843-5-F1) | `srp_listeners.cpp`, `srp_listener_mutants.py`, `srp_mutants.py:93-105,225-237`, the SRP campaign log, `flip_grade.py:60,196-202,404,420`, `rows_grade.py:93`, `receipts/tx-plant-probe.txt` | R843-5 | `8883d4998496c6d2e234143b43807731e8851b63` |
| Docs | UNCLEAN (R843-5-F1) | `ctrl_loop.h:298-330,463-475`; `FR_NFR.md:393-397`; `SPLIT_CONTROL_MEMORY.md` section 11 (the walk cut) and section 13 (the 8x8/1if composition and the Listener copies); `srp/README.md:77-82,225`; `load_grade.py:21-28,567` | R843-5 | `8883d4998496c6d2e234143b43807731e8851b63` |

## Probes and receipts (this packet)

- **`scripts/listener_probe.py`:** runs the differential arms, and the reviewer's own extra plants at 1x1/1if or 8x8/1if, in disposable copies under `scratch/`.
  - Receipts: `receipts/listener-arms.txt`, `listener-plants-{1x1,8x8}.txt`, `listener-plant-leave-*.txt` and `listener-plant-walk-*.txt`, each with its `.rc`.
- **`scripts/table_plants.py`:** re-plants named defects of the head's own table.
  - Receipts: `receipts/table-retargeted-if{1,2}.txt`.
- **`scripts/tx_plant_probe.sh`:** the F1 plant in an export of the head.
  - Receipt: `receipts/tx-plant-probe.txt`.
- **`scripts/verify_packet.py`:** the archive manifest check.
  - Receipt: `receipts/packet-verify.txt`.
- **Other receipts:**
  - `receipts/harness-checks.txt`: shape table, both flip checks, load check, ledger self-test, flip and load self-tests, all at the head.
  - `receipts/hosted-evidence.txt`.
  - `receipts/clone-state-after.txt`.
- **Clone state:** the clone is restored and verified.
  - Index equals the HEAD tree by mode, blob and path (sha256 `fbc68f57...`).
  - 0 tracked, untracked or ignored changes; four `__pycache__` directories the probes' imports wrote were removed.
  - The six gitlinks are the head's, and no submodule has a change.

## Real limits

- **Images:** I did not rebuild the RV32 images. Their identity to `46cf2a7d` is the author's receipt, plus my check that no firmware source changed since `46cf2a7d`.
- **The CPU service-budget harness:** I did not run it. The `srp-talker-held` rows, the gates at `46cf2a7d` and `05a7ea82`, and the ledger measurements are the author's published receipts.
- **Not re-run by me:** the full SRP mutation campaign, the firmware unit and coverage jobs, the docs jobs and the Verilator shards. I read their receipts.
- **8x8/1if's rows by every source:** R4 21.39, tx 69.84 and the rest are a packet-side derivation, not reproducible in the tree (see F1). They are owed to #872.
- **Hosted evidence:** none at the exact head. There are 0 check runs and 0 workflow runs, and the combined status is pending with 0 contexts (`receipts/hosted-evidence.txt`). No hosted job executed, so there is nothing to tell apart.
- **Hardware:** physical calibration was NOT RUN, and field skips are not hardware proof.
- **Known items, not findings:**
  - the twin and twin-plants failures, owed to PR #935;
  - R4 by every source at 8x8/1if, 21.39 ms, owed to #872;
  - the timing floor, owed to #818;
  - rounds 11 and 12 ran partly on the usage fallback.
- **Delta start:** the brief names `d539f162` as the head of R843-4 and R844-3. R844-3's published head was `af2c4d7a`; R843-4's was `d539f162`. I reviewed from `d539f162`.

## Pending manager duties

- Rule on, or route back, R843-5-F1. It is the one item between this head and a clean ledger.
- Carry R843-5-R1, R843-5-R2 and R843-4-R1 to the residue checklist.
- The current-dev merge candidate (source base `7398ec0a`, live dev `6b66f66d`): builder and native banks, and their receipts on the PR. No manager source bank ran at this head, and I claim none.
- Hosted and act acceptance at the exact head.
- The second independent review (R844-4).
- Under the freeze rule, the composition review's list already carries the `CTRL_LOOP_TX_MS` keying (ruling 6914952893, item 4). F1 belongs beside it if the lane is frozen before it is fixed.

R843-5 FINISHED
