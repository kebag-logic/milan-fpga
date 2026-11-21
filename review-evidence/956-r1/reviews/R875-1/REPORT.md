[R875] NEGATIVE - exact head 0d80f0ed2a880c3a3b2429c669f104801203ec05

Round R875-1, internal cleared-context review of PR #958 (Issues #956 and #957, part of #665). Head
`0d80f0ed2a880c3a3b2429c669f104801203ec05`, tree `14c4607eaceb3369f6debb279ed83d59ad098846`, reviewed as the delta
from the flip train's head `15168e14`. All five lenses were applied. One MAJOR and two MINOR findings are open, so the
verdict is NEGATIVE.

## Contents

- **[Summary](#summary)**: the verdict, and why.
- **[Findings](#findings)**: F1 (MAJOR), F2 and F3 (MINOR).
- **[The five checks in the brief](#the-five-checks-in-the-brief)**: each check's result.
- **[Clean results by lens](#clean-results-by-lens)**: what was examined and found clean, with its artifact.
- **[Ledger](#ledger)**: each lens, its state, the covering round and the head.
- **[Prior public findings](#prior-public-findings)**: what other public review this head had.
- **[Limits and pending manager duties](#limits-and-pending-manager-duties)**: what was not done or proved here.
- **[Receipts](#receipts)**: the published files.

## Summary

- **#956 meets its acceptance in the model.** `SRP_REDECLARE_CS` is derived from the named LeaveAll constant with
  both terms inside it. It gives 2,977, 2,973 and 2,970 cs. The latest case is 29,995 ms and the earliest is 29.70 to
  29.77 s after the request. The tests and plants pass at the head and catch #951's value. The bench measurement
  belongs to the manager after merge.
- **#957 works for every case its tests exercise.** The record misses one case: a change after a link reset.
  - `listener` records a change only against `declaration[]`. Nothing clears that array when a link reset destroys
    the participants, and their registrations end with no indication.
  - The ordinary recovery order is: link back, Talker declared again, then the bridge declares the Listener again.
    In that order the returning Listener matches the stale entry. The answer goes from no REGISTERING to REGISTERING
    and no unsolicited notice is sent.
  - A probe reproduced this at 1x1/1if, 1x1/2if and 8x8/1if (F1).
- **Two documents state wrong figures.**
  - The FR_NFR SRP row this PR edits still says the hold-off "stays 2,027". It also says the terms "above" 2,000 cs
    make the declaration 10 ms later at two interfaces (F2).
  - The SRP README says 18 bytes of rom are left at 8x8/1if. The ledger and the memory design page say 16 (F3).

## Findings

### F1: MAJOR, Conformance / RTL / Robustness / Tests: a link reset leaves a stale Listener record, so the Listener's return is not noticed

- **Where.** `sw/firmware/ctrl/srp/srp_mbx.c:228-229` (`listener`, the comparison against `declaration[n]`), with
  `sw/firmware/ctrl/srp/srp_mbx.c:1172-1226` (`reset_interface`).
  - `reset_interface` clears `listener_present[]`, so the answer drops REGISTERING. It destroys the participants with
    no Leave indication, and it leaves `declaration[]` holding the last copied declaration.
  - The struct comment is `sw/firmware/ctrl/srp/srp_mbx.h:62-65`. The documented scope is
    `sw/firmware/ctrl/srp/README.md:319-320` ("A link reset is not recorded here").
- **Authority.**
  - #957's frozen acceptance: "A registration change for an output's stream raises exactly one unsolicited response
    with the new flags, at every output and both shapes".
  - Milan v1.2 5.4.5.2 and Table 5.22 (a Stream Output's MSRP Listener attribute registration state). IEEE
    1722.1-2021 7.5.2 (unsolicited notifications).
  - The answer that has to stay matched is `sw/firmware/ctrl/app/ctrl_app_aecp.c:54-66` (`output`: REGISTERING from
    `listener_present`, REGISTERING_FAILED from `!registered`).
- **Evidence.** The reviewer probe `scripts/probe_link_reset_957.cpp` was appended to a disposable copy of
  `test_aecp.cpp`, in the `AppOutputs` fixture, with real Listener MRPDUs and the notices read on the wire. Its steps:
  1. The Listener Ready is registered: 1 notice to each controller.
  2. The link goes down: the DA gate closes and the Talker withdrawal is noticed.
  3. The link comes up: MAAP is valid again, and the Talker is declared again with a notice whose `flags_ex` is 0.
  4. Before the Listener returns, the answer's `flags_ex` is 0, `listener_present` is 0 and `declaration` is still 2
     (Ready).
  5. The Listener Ready returns: the answer's `flags_ex` is 1, with **0 notices** to either controller over 3 s.
  - Same result at 1x1/1if, 1x1/2if and 8x8/1if (`receipts/probe-link-reset-*.log`). The two existing `AppOutputs`
    tests pass in the same build.
  - Counter-probe: also clearing `declaration[k]` beside `listener_present[k]` in `reset_interface` makes the probe
    pass at 1x1/1if (`receipts/counterprobe.diff`, `receipts/probe-link-reset-1x1-1if-counterprobe.log`). The stale
    record is the cause.
- **Impact.** After any link flap the controller's cached STREAM_OUTPUT state says "no Listener" while every
  GET_STREAM_INFO answer says REGISTERING (or REGISTERING_FAILED). This holds until some other change notices the
  output.
  - This is the ordinary recovery sequence. The bridge declares the Listener toward the Talker only after it
    registers the Talker again, and that comes after the gate and the Talker return.
  - A Listener that left during the flap and later returns with the same declaration is missed the same way.
  - The PR's disclosed limit ("A link reset records no Listener change") covers the reset itself. It does not cover
    this later missed change, and neither does any test.
- **Required outcome.** After a link reset, the first Listener registration seen for a source's stream is recorded
  as a change whenever what the output shows changes. The record must agree with what the answer shows after a reset.
  No duplicate notice may be added for an unchanged state. A self-checking test must cover reset then return at the
  SRP level and in `AppOutputs`, with a plant showing the test fails on the current head.
- **Verification.** Re-run `AppOutputs.*` at 1x1/1if, 1x1/2if and 8x8/1if, `Talker.*` at 1x1/1if and 8x8/2if, the
  new plant and the existing `talker-registration-*` and `registration-notice-*` plants. Re-run `plat_ledger.py` at
  8x8/1if: the rom has 16 bytes left, so any added code must still fit the ledgered 58 RAMB36, or a public budget
  decision is needed.

### F2: MINOR, Docs: the FR_NFR SRP row this PR edits keeps the old hold-off's figures and direction

- **Where.** `docs/reference/FR_NFR.md:427`, the SRP/MRP row, edited in this delta.
  - The sentence now reads "counts it and a JoinTime inside two nominal longest LeaveAll periods (#951, #956),
    follows it: 2,970 cs at two interfaces (2,971 at 99 ms), 2,977 at 1x1/1if, and 2,973 at 8x8/1if ...".
  - It continues "(`tx_held`; 2,026 at 70 ms before the row reached 74.26) and at most 80 ms, so the hold-off stays
    2,027".
  - It ends "IEEE 802.1Q-2018 35.2.2.8 sets only the least, 2,000 cs, and the terms above it cover the Leave's latest
    departure, so a changed destination is declared 10 ms later at two interfaces, on the safe side".
- **Evidence.** These conflict with the code and with the edited figures just before them:
  - `srp_mbx.c:47` gives 2,973 at 8x8/1if, not 2,027.
  - The terms are now subtracted, and they cover the declaration's latest departure, not the Leave's.
  - At two interfaces, 105 ms gives 2,970 against 2,971 at 99 ms. That is 10 ms sooner, not later.
- **Impact.** The authoritative requirements reference states a figure and a direction of the hold-off that the code
  no longer has, inside the very sentence this PR restated.
- **Required outcome.** The row states the head's hold-off and its direction consistently, or marks each older
  figure as history.
- **Verification.** Read the row against `srp_mbx.c:47` and `ctrl_loop.h` (`CTRL_LOOP_TX_MS`, `CTRL_LOOP_JOIN_CS`),
  then re-run `scripts/docs_check.py`.

### F3: MINOR, Docs: the SRP README states 18 bytes of rom left at 8x8/1if; the ledger gives 16

- **Where.** `sw/firmware/ctrl/srp/README.md:321`: "The record takes 40 bytes of code at 8x8/1if, whose image has 18
  bytes of its 34 RAMB36 of `rom` left (#957)".
- **Evidence.**
  - `plat_ledger.py` reports `rom 139,248 B` at 8x8-if1 on the author's head image (author receipt
    `images-15168e14-vs-8845364d.txt`). 34 RAMB36 is 139,264 B, so 16 bytes are left.
  - `docs/design/SPLIT_CONTROL_MEMORY.md:3220` says "139,248 B, 16 left".
  - `ctrl_memory.plan` counts `rom_end`, the end of `.data`'s load address. The receipt's sections give that: `.rodata`
    ends at 113,064 + 25,662 = 138,726, `.data` loads at 138,728 (8-byte aligned), and 138,728 + 520 = 139,248.
  - 139,246 B (18 left) is the section sum without that alignment, which the ledger does not use.
- **Impact.** Two authoritative documents disagree on the product image's rom margin, which is the constraint any fix
  (F1 included) must meet.
- **Required outcome.** The README states the ledger's figure: 139,248 of 139,264 B, 16 bytes left. Or it restates
  whatever the head's `plat_ledger.py` reports after a fix.
- **Verification.** Run `plat_ledger.py` at the fixed head and read both documents against it.

RESIDUE: none recorded. Each wording defect found states a figure or a behaviour, so each is MINOR above.

## The five checks in the brief

1. **#956.**
   - The derivation: `srp_mbx.c:47` is `2u * SRP_LEAVEALL_LONGEST_CS - SRP_JOIN_CS - (CTRL_LOOP_TX_MS + 9u) / 10u`.
     `SRP_LEAVEALL_LONGEST_CS` is 1.5 x `SRP_LEAVEALL_CS` (1000), `SRP_JOIN_CS` is `CTRL_LOOP_JOIN_CS` (19), and
     `CTRL_LOOP_TX_MS` is 35, 77 and 105. So the constant is derived, not mirrored, and gives 2,977, 2,973 and 2,970.
   - The latest case: `ChangedDestinationReachesTheWireWithinTwoLongestLeaveAllPeriodsAtTheLatest`
     (`srp_talker.cpp:362`) holds the loop a JoinTime and the figure from the tick that ends the count. It asserts the
     wire time equals end + 190 + TX (29,995 ms) and is at most at + 30,000.
   - The earliest case: TALKER_DECL is held at at + hold-off - 1 and declared at at + hold-off. That is 29.70 to 29.77
     s, at least 29 s. Mid-centisecond requests may end the count 1 cs sooner, as the PR discloses.
   - At the head, `srp_talker.cpp` passes at 1x1/1if and 8x8/2if (17/17) and `SrpGate.*` passes at 8x8/2if (9/9).
   - All 14 hold-off plants are caught at both SRP campaigns. Among them `talker-hold-off-adds-its-terms` (#951's
     value) and its `-at-the-latest` and `-after-a-conflict` forms fail on their own words.
   - Met in the model. The bench (29 to 30 s at both points) is the manager's after merge.
2. **#957.**
   - Every case the tests name holds, and the 8 plants are caught:
     - `talker-registration-*`, 5 at each SRP campaign.
     - `registration-notice-*`, 3 at 1x1/2if.
     - `AppOutputs.*` passes at 1x1/1if, 1x1/2if and 8x8/1if.
   - No duplicate with #936's path. Both use the one `noticed` bitmask, which the composition ORs and AECP drains, so
     one pass yields one notice an output.
   - Nothing is recorded behind a closed gate or for another interface, per the test and the `-ungated` plants.
   - **Not met** after a link reset: F1.
3. **Memory.**
   - The 8x8/1if product image is 139,248 B of 139,264, 16 bytes left (not 139,246 and 18: see F3), within its
     ledgered 58 RAMB36. `ctrl_plat` is 18,944 B at 8x8-if1 on both sides of the author's ledger receipt.
   - `ctrl_memory_ledger.py` (`PLAT_*`, the 58.0 and 63.0 tiles) and `ctrl_memory.py` are not in the delta, so no
     budget changed.
   - My own RV32I objects: `listener` grows 128 to 168 B at 8x8 and 132 to 172 B at 1x1, the author's 40 B
     (`receipts/rv32-srp-listener-size-base-vs-head.txt`).
     - In that portable RV32I build, `on_event`, `poll` and `transmit` also move at 8x8 (field offsets). The
       author's platform (RV32IM) listings show `listener` alone.
   - I could not relink the platform image here (no LiteX on this host). The image figure is the author's receipt.
4. **Harness.**
   - `declaring_outputs.py` is stricter than before, not looser. Before, it required no count before the first GET.
     Now `order_findings` requires exactly 2 x registrations notices of output 0, and `answer_findings` requires
     REGISTERING from the Listener's notices on.
   - The arm's 18 self-test checks pass, its three new planted orders refused among them.
   - `record.maap`: 17,259 cycles x 1.05 is 181.2 us, rounded up to 5 us gives 185, by the rule.
   - At the head `load_grade.py --check` passes (8x8/1if 0.744 of 0.75). `flip_grade.py --check` passes at 8x8/1if,
     with THE TRANSMIT 76.86 ms against its 77, and at 1x1/1if. `shape_costs.py --check` passes.
5. **The later commits.** `8845364d..0d80f0ed` touches only docs, `declaring_outputs.py`, `flip_grade.py`,
   `load_grade.py` and the plant table. None is an image input. The plant table regroup keeps 63 rows, the same set
   (`receipts/plant-rows-8845364d-vs-head.txt`). `scripts/docs_check.py` gives 0 findings at the head.

## Clean results by lens

These are the parts of each lens that were applied and found clean. They do not clean a lens that has an open
finding.

- **Conformance, `sw/firmware/ctrl/srp/srp_mbx.c:29-49`.** The #956 constant was checked against the owner's
  2026-11-21 decision, IEEE 802.1Q-2018 35.2.2.8, 10.7.4.3 and Table 10-7, and Milan Table 4.3.
  - The two periods bound the wire time at 30.0 s, with the earliest at 29.70 s or later.
  - At least two LeaveAllTime periods (20 s) pass between the Leave and the new declaration.
- **Conformance, `srp_mbx.c:215-232` against `ctrl_app_aecp.c:54-66`.** The mapping holds for the cases tested:
  Ignore is no flags, Asking Failed is REGISTERING with REGISTERING_FAILED, and Ready or Ready Failed is REGISTERING.
  The Ready to Ready Failed notice with the same flags is the public assumption made in TAKEN.
- **RTL / architecture, `ctrl_app_srp.c:66-75` and `ctrl_app_aecp.c:236-247`.** The record reuses #936's take path,
  with no new poll, bound or mailbox change.
  - The precedence of `(x << n) & i->gate` is correct.
  - `declaration[]` sits in existing padding per the author's ledger (`ctrl_plat` unchanged).
  - No RTL file is in the delta.
- **Robustness, `srp_talker.cpp:788-845` and `test_aecp.cpp:966-1058`.** Covered: unchanged JoinIn and New, LeaveAll
  re-registration, another interface, a closed gate, another source, a leave, and no change over a pass.
- **Tests.**
  - The new tests pass at the head: `receipts/suites-srp-talker-head.log`, `receipts/suites-aecp-app-head.log`.
  - The firmware gate's suites shard passes (`receipts/fw-gate-shard0-head.log`).
  - Each new plant fails its named test on its own words: `receipts/plants-*.log`.
  - #951's value fails three tests by name.
- **Docs.**
  - `docs/design/SPLIT_CONTROL_MEMORY.md:3214-3224`, `docs/design/MAILBOX_SPLIT.md:1287-1297` and
    `sw/firmware/ctrl/aecp/README.md:118-123` agree with the code.
  - `scripts/docs_check.py` gives 0 findings (`receipts/docs-check-head.log`).
  - The source-comment rule: the added source, test and Python lines carry no bench lane labels, lane names, review
    rounds, reviewer IDs or issue-comment IDs (`receipts/comment-rule-scan.txt`).

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `srp_mbx.c:29-49, 205-232, 1172-1226`; `ctrl_app_aecp.c:54-92, 236-247`; `ctrl_app_srp.c:50-80`; #956 owner decision; #957 acceptance; probe logs | R875-1 | `0d80f0ed2a880c3a3b2429c669f104801203ec05` |
| RTL | UNCLEAN (F1) | the same firmware state and reset path; `srp_mbx.h:45-121`; `maap_mbx.c:60-75, 128-158, 208-240`; delta has no RTL file | R875-1 | `0d80f0ed2a880c3a3b2429c669f104801203ec05` |
| Robustness | UNCLEAN (F1) | reset during an active registration (probe), gate closed and open, another interface, repeated and unchanged declarations, LeaveAll | R875-1 | `0d80f0ed2a880c3a3b2429c669f104801203ec05` |
| Tests | UNCLEAN (F1) | `srp_talker.cpp`, `srp_gate.hpp`, `test_aecp.cpp`, `srp_talker_mutants.py`, `aecp_registration_mutants.py`, `declaring_outputs.py` checks; 14 + 5 + 3 plants run; suites run | R875-1 | `0d80f0ed2a880c3a3b2429c669f104801203ec05` |
| Docs | UNCLEAN (F2, F3) | `docs/reference/FR_NFR.md:427`; `sw/firmware/ctrl/srp/README.md:226-330, 566-571`; `sw/firmware/ctrl/aecp/README.md:118-123`; `docs/design/SPLIT_CONTROL_MEMORY.md:3177-3224`; `docs/design/MAILBOX_SPLIT.md:1287-1297`; harness texts | R875-1 | `0d80f0ed2a880c3a3b2429c669f104801203ec05` |

## Prior public findings

There were no public review findings on PR #958, #956 or #957 when this round started. The PR then carried only the
two review-start comments. An external round's report was published at 20:48Z, during this round. Per the brief, it
was not read before this verdict and ledger were written. See the addendum below.

### Addendum: the external round's findings at this head (read after the verdict and ledger above were written)

The report is at https://github.com/kebag-logic/milan-fpga/pull/958#issuecomment-7069018804. Nothing has changed
since it was written, so each of its findings is open at this head.

- **R876-1-F1 (MAJOR, reset leaves a stale Listener record): retained, open.** It is the same defect as F1 here. It
  was found independently, with a different probe and at different shapes (1x1/1if and 8x8/2if there; 1x1/1if,
  1x1/2if and 8x8/1if here).
- **R876-1-F3 (MINOR, `FR_NFR.md:427`): retained, open.** It is the same as F2 here.
- **R876-1-F2 (MAJOR, #956's latest case with a join timer active at the count's end): retained, open, and
  reproduced here.**
  - I did not find this before reading that report. Afterwards I ran a disposable probe,
    `scripts/probe_phase_956.cpp`, appended to a copy of `srp_talker.cpp`.
  - It varies the withdrawal phase from 100 to 900 ms. Phase 0 is a setup artifact of the probe: the source is not
    yet declared, so there is no Leave to measure.
  - **The held loop** (the shipped latest-case test's own model, without its idle-timer precondition) goes past the
    30.0 s bound:
    - **1x1/1if:** phase 300 reaches the wire at **30,700 ms**.
    - **8x8/2if:** phase 400 reaches interface 0's wire at **30,600 ms**.
    - **8x8/1if:** every phase is within 29,997 ms.
    - Every other phase is at most 29,997 ms.
  - **The loop serviced throughout** keeps every phase at every shape within 29,700 to 29,890 ms.
  - So the counterexample needs the held loop's burst of ticks while a join timer is active. That is the model the
    head's own at-the-latest test uses to establish the bound, and its 700 ms phase avoids that case.
  - The PR discloses the symptom under "Seen beside it, not changed". AGENTS.md section 7 does not let a finding
    deferred to another Issue count as resolved.
  - Lenses: Conformance, RTL, Robustness and Tests, as that round filed it. Each was already UNCLEAN here (F1).
  - Receipts: `receipts/probe-phase-1x1-1if.log`, `receipts/probe-phase-8x8-1if.log` and
    `receipts/probe-phase-8x8-2if.log`.
- **Its other statements agree with this round:**
  - The memory accounting: 139,246 B of payload against a 139,248 B aligned charge.
  - The `declaring_outputs.py` correction.
  - The `record.maap` restatement.
- **The verdict stays NEGATIVE.** Open at this head: F1, F2, F3, and the external round's F2. Every lens stays
  UNCLEAN as tabled above.

## Limits and pending manager duties

- **The firmware gate's suites phase passed at the head.** I ran
  `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4` with the pinned RV32 SDK, its archive digest
  verified. It exits 0, `test_ctrl_firmware: PASS`, with 88 `[ok]` arm lines and no failure
  (`receipts/fw-gate-shard0-head.log` and `.rc`).
- **Not run here.**
  - Mutation shards 1 to 3 in full. I ran the focused suites and the 22 new plants instead.
  - `fw_coverage.py`, the twin targets, the CPU budget harness legs and `plat_ledger.py`. The last needs LiteX, which
    this host does not have.
  - The platform image figures (rom 139,248 B, `ctrl_plat` 18,944 B, the release image's identity) are the author's
    receipts, not reproduced here.
- **The hosted check-runs at the exact head, as of 21:04Z** (`receipts/hosted-checks-0d80f0ed.txt`).
  - 31 report success, 1 skipped, and the Verilator and Yosys long shards are queued or in progress.
  - Among the successes are `firmware-unit`, `firmware-srp-mutants`, `firmware-control-mutants`,
    `firmware-aecp-mutants` and `firmware-boundary`. I read their conclusions, not their logs for internal skips.
  - Hosted and act acceptance is the manager's.
- **Physical calibration was NOT RUN.** No hardware was used. The 29 to 30 s bench measurement at 1x1/1if and
  8x8/1if is the manager's after merge.
- **The manager validates** the current-dev merge candidate (builder and native banks, live dev `e275d795`) at the
  merge turn. No manager source bank is claimed for this head.
- **After the probes**, the clone was restored: head, tree, index, modes and blobs are identical to HEAD, the six
  submodule gitlinks are as recorded, and no untracked or ignored files remain (`receipts/restore-verification.txt`).
  Probes ran only in disposable copies under `scratch/`.

## Receipts

Listed in `MANIFEST.sha256`. Scripts are under `scripts/` and raw logs under `receipts/`.

R875-1 FINISHED
