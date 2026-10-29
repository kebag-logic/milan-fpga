[R731] NEGATIVE - exact head ec1ff275a72d885f0908fd213d8009e9e4dda4d9

# R731-1 independent review: processor issue #203 / PR #209 (AECP REBOOT)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #209
- Exact head: `ec1ff275a72d885f0908fd213d8009e9e4dda4d9`, tree `be6818cf5ccccf5d327cc43adaec34c1df51b98c`
- Source base: `f65c8ff7`. Delta reviewed: `git diff f65c8ff7..ec1ff275` (12 commits, 63 files)
- Reviewer: internal independent reviewer, cleared context, own detached clone
- Simulator for every executed receipt: the scoped Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`)

## Verdict

NEGATIVE, on one open MAJOR (R731-F1). When the entity is not advertising, `reboot_req_o`
rises while a frame from another lane is still on `tx_*`. That breaks the port's defining
contract (02 F02.10: "From its rise to `rst_n` nothing leaves on `tx_*`"). An integrator who
follows the guide and drives `rst_n` from the request then cuts that frame mid-transmission.
The advertising path, the response/notification/DEPARTING ordering, the status table, the lock
interaction, the RX and engine holds, and the transmit gate after the final DEPARTING all hold.
All 30 RBT arms and all 8 re-cut arms are KILLED by name at this head.

## Findings

### R731-F1 (MAJOR): a non-advertising REBOOT raises `reboot_req_o` while a frame is still on `tx_*`

- **Lenses:** RTL, Robustness, Tests.
- **Where:** `hdl/top/protocol_processor_top.sv:4905` (`rbt_tx_flight` tracks only the
  unsolicited-AECP and ADP lanes) and `hdl/top/protocol_processor_top.sv:4938`-`4940` (RB_DEP
  leaves on ADP's builder, ADP's lane queue and ADP's flight only).
- **Authority:**
  - 02 F02.10 (`docs/architecture/02_interfaces.md:582`): "It rises only after ... From its rise
    to `rst_n` nothing leaves on `tx_*`".
  - The port contract (`hdl/top/protocol_processor_top.sv:824`-`846`): "three things have left
    the transmit path ... a reset held back finds the entity silent".
  - Integrator guide bring-up step 7 (`docs/guides/integrator.md:697`-`702`): "the processor
    sends nothing more ... transmitting no frame, for your `rst_n`". The same guide, at line 31,
    says to drive `rst_n` from the request.
  - Operator guide (`docs/guides/operator.md:52`): "then nothing ... sends no frame".
  - The round-2 required outcome on the issue: a terminal transmit-quiet state in which "frame
    integrity and the held request are kept".
- **Mechanism:**
  - RB_NTF ends at the last REBOOT notification's last byte.
  - In the same clocks the idle arbiter may select any request already waiting, because the gate
    is still open. Examples are the lock's automatic-unlock notification (not command work, so
    `cmd_busy_o` does not cover it), a listener probe, MAAP and SRP.
  - With no advertise machine up, RB_DOWN and RB_DEP pass in one clock each. RB_DEP sees ADP idle,
    and `reboot_req_o` rises about three clocks after that frame's grant.
  - The frame is at least 64 bytes and still streams for tens of clocks. Nothing waits for a
    frame of a lane other than ADP or unsolicited AECP.
  - In the advertising case the same frame always goes before the DEPARTING, and RB_DEP waits for
    the DEPARTING's flight, so that path is safe.
  - The prepared round-2 PR body states the window ("a frame granted in those two clocks still
    goes"). It does not state that this frame overlaps the request.
- **Evidence:** `receipts/probe_window.log`, from the probe
  `probes/window-after-notification-round.patch` (a scenario added to a scratch copy of
  `tb/pp_top/sim_main.cpp`, run by `scripts/run_window_probe.sh`). The scenario is: one other
  controller registered, the requester holds the lock, and the MAC holds the REBOOT
  notification's last byte for 1 s so that the lock expires.
  - Not advertising (`PRB-NA`): `reboot_req_o` rose at clock 105454. The unsolicited
    LOCK_ENTITY (command_type 0x0001, u = 1) to the other controller took its last byte at
    105513, 59 clocks later.
  - The same scenario advertising (`PRB-ADV`) passes. The SRP frame and the DEPARTING both
    leave before the rise.
  - No RBT row covers a non-advertising REBOOT with a second producer live. RBT7 and RBT8 are
    the only non-advertising rows, and they run with nothing else to send.
- **Impact:** a reset taken on the request truncates a frame at the MAC boundary: a frame with
  no `tx_eof_o`. What the MAC FIFO then does (a runt, a bad-FCS frame, or a wedged FIFO) is the
  integrator's MAC's. The request no longer means "nothing more on `tx_*`", which is the one
  property the guide asks the integrator to rely on.
- **Required outcome:** `reboot_req_o` rises only when the transmit gate is closed and no frame
  of any lane is in flight. For example, RB_DEP (or a final state) also waits for the arbiter
  to be idle with no grant outstanding, on every path, advertising or not.
  - Add an RBT row: not advertising, a second producer live in the clocks the notification round
    ends (the lock-expiry stimulus above suffices). It asserts that the last byte offered on
    `tx_*` precedes the rise.
  - Add a named arm that removes the new wait and is killed by that row.
  - RBT1 to RBT11 and the round's arms stay KILLED.
  - The PR body's two-clock sentence is updated to match.
- **Verification:** `scripts/run_window_probe.sh <exact-head tree> <verilator>` passes both
  `PRB-NA` and `PRB-ADV`. `make -C tb/pp_top reboot` shows 0 failures. The REBOOT arms in
  `aecp_dispatch_mutants.py`, the new one included, are all KILLED by name.

### R731-S1 (SUGGESTION): state the request's clock-domain contract, or register it

- **Lenses:** RTL, Docs.
- **Where:** `hdl/top/protocol_processor_top.sv:4949` and `docs/guides/integrator.md:31`.
- **Observation:**
  - `reboot_req_o` is a combinational decode (`rbt_st_r == RB_REQ`) of a binary-encoded 3-bit
    state register.
  - The RB_DOWN to RB_DEP step is 011 to 100. In gates it can decode as 101 for a moment, unless
    synthesis re-encodes the machine.
  - Inside `clk_i` this is harmless. But the guide says to drive `rst_n` from the request "by
    whatever reset your end station uses", and an asynchronous reset input would see that pulse
    before the DEPARTING has left.
  - The general rule that class-D outputs are combinational reads of `clk_i`-domain registers
    (`docs/guides/integrator.md:46`) covers it only by implication.
  - Nor does the contract say whether a one-clock synchronous reset taken straight from the
    request is enough.
- **Suggested outcome:** register `reboot_req_o` (one flop), or state at F02.10 and in the
  guide that it is a `clk_i`-domain output to be sampled synchronously, with the minimum
  `rst_n` assertion. This answers focus item (6). The parent's use of the port is milan-fpga
  #787, and the contract leaves this point to it.

### R731-S2 (SUGGESTION): the whole-frame RX discard has no observable test

- **Lenses:** Tests.
- **Where:** `hdl/top/protocol_processor_top.sv` `rx_reboot_gate`.
- **Observation:** probe `p2-rx-gate-cuts-mid-frame` cuts the frame that is arriving at the
  acceptance (`rx_take_w = rx_valid_i && !aecp_reboot_w`). It SURVIVED, with RBT at 127 checks
  and 0 failures. The prefix it leaves in the validator never completes, and nothing after it is
  admitted until reset, so no behaviour changes. The "admitted or discarded whole" property is
  therefore stated, not graded. This is optional, because no wire effect follows.

No RESIDUE. Comment rule: the reviewed delta's source comments carry no bench lane label, lane
name, review round, reviewer ID or issue-comment ID. The scan is the comment-rule check under
"Executed evidence"; the only "round" hits are the notify block's notification round.

## Focus items

1. **Status table** (IEEE 1722.1-2021 §7.4.43, Figure 7-68; frozen acceptance on the issue).
   - ENTITY 0 is answered SUCCESS, echoing `{type, index}` at cdl 16, a padded cdl 20 included
     (RBT6, RBT8).
   - Another descriptor type gets NOT_SUPPORTED: MEMORY_OBJECT, AUDIO_UNIT, CONFIGURATION (RBT2).
     This is the issue's frozen choice, and Table 7-141's NOT_SUPPORTED is the "target not
     supported" status.
   - A non-zero index gets NO_SUCH_DESCRIPTOR (RBT3). cdl < 16 gets BAD_ARGUMENTS (RBT1).
   - Every refusal is byte-exact and leaves the entity in service.
   - The SUCCESS response is the first REBOOT frame by construction. `E_RBOOT` queues the
     notification before `SEND_RESP`, but the engine builds that unsolicited job only after the
     response's A_TXW grant. RBT6 checks the order. CONFORMS.
2. **Order** (§7.5.2, Milan v1.2 §5.4.5.2; IEEE §6.2.4/§6.2.5.2.2, Milan §5.6.3.5.8/.11).
   - The order is response, then notifications to every other registered controller (none to
     the requester), then ENTITY_DEPARTING, then `reboot_req_o` (RBT6, RBT9).
   - ADP's `enable_fall_w` is combinational on its input, so RB_DOWN's single clock sets
     `pend_dep_r` before RB_DEP reads `tx_busy_o`.
   - B_REQ hands to the lane queue on the same edge the builder goes idle, so RB_DEP has no gap
     between the two (probes p3 and p5 confirm both waits matter). CONFORMS for the advertising
     path. See R731-F1 for the non-advertising path's overlap with another lane's frame.
3. **Held, one-way request; silence after DEPARTING.**
   - RB_REQ has no exit. RBT6, RBT9 and RBT10 grade the hold.
   - The arbiter mask `arb_req_w = arb_want_w & rbt_tx_open_w` affects only selection: a lane
     selected before the gate closes is granted and sent before the queued DEPARTING. After the
     final DEPARTING nothing is offered on `tx_*` through a 75 s or 65 s withheld reset (RBT9,
     RBT10), and nothing follows when every slot is taken (RBT11).
   - Probes p1 (the gate reopening at RB_REQ), p4 (the gate at RB_DEP's entry) and p6 (the
     request dropped on RX) are each DETECTED.
   - Open: R731-F1.
4. **Lock and acquire** (§7.4.43.2, §7.4.1, §7.4.2).
   - A non-owner under lock gets ENTITY_LOCKED. The type and index refusals outrank the lock
     (RBT4, RBT4b, RBT4c).
   - The holder's REBOOT is SUCCESS (RBT6, RBT9, RBT11).
   - ENTITY_ACQUIRED cannot arise because ACQUIRE_ENTITY is NOT_SUPPORTED (Milan v1.2 §5.4.2.1;
     RBT5). Probe p8, ACQUIRE served by the LOCK program, is DETECTED by RBT5.
   - REBOOT is CFG_BARRIER with the global key. Probe p7, which drops it, survives every
     behavioural bench but is caught by the AECP command gate (`classifier: REBOOT: the table
     says CFG_BARRIER`). CONFORMS.
5. **Mutations.**
   - All 30 `rbt-*` arms are KILLED by their named checks, and the reboot control PASSES. Each
     arm's failure count equals its `tb/pp_top/README.md` cell (30 of 30).
   - Every new RBT row is named by at least one arm except RBT5, which restates the pre-existing
     ACQUIRE refusal. My probe p8 plants that defect and RBT5 kills it.
   - The re-cut arms still kill with the same named checks: `dl-kill-tied-off`,
     `acmp-waits-for-aecp`, `hz-stub-restored`, `hz-setcfg-not-barrier` (both arms),
     `if-egress-collapsed`, `if-top-ingress-live`, and the d3 arms `dispatch_not_held` and
     `enable_not_released_by_restore`.
   - The planted lines are byte-identical to the base's, or plant the same defect next to the
     new REBOOT case label.
   - The retired `a5b-reboot-success-arm` matches REBOOT's new SUCCESS answer.
6. **Port contract for milan-fpga #787.**
   - The level, held until `rst_n`, one-way, and unconnected-safe behaviour are stated.
   - The contract leaves two points ambiguous, for the parent to settle: the clock-domain
     sampling and glitch-freedom of the output, and the minimum reset length (R731-S1).
   - Its promise of no `tx_*` activity from the rise does not hold on the non-advertising path
     (R731-F1).

## Executed evidence (this review, exact head, Verilator 5.050)

| Receipt | Command | Result |
|---|---|---|
| `receipts/golden_reboot.log` | `make -C tb/pp_top reboot` | RBT: 127 checks, 0 failures (about 0.5 GB RSS) |
| `receipts/suite_pp_top.log` | `make -C tb/pp_top` (every build) | 10477 + 20 + 178 + 292 + 56 + 3 + 6 = 11,032 checks, 0 failures |
| `receipts/suite_aecp_cmds.log` | `make -C tb/aecp_cmds` | 617,956 trials; 181 of 181 PASS |
| `receipts/suite_adp_engine.log` | `make -C tb/adp_engine` | 1,359 of 1,359 PASS |
| `receipts/lint_hdl_5050.log` | `scripts/lint_hdl.sh`, pinned verilator first on PATH | 41 modules LINT OK |
| `receipts/make_check.log` | `make check` in a scratch clone at the head | rc 0; AECP command gate 32 commands, F06.14 42 rows, self-test 231 of 231; req-tags 262 tags |
| `receipts/camp_disp_rbt.log` | `aecp_dispatch_mutants.py --only <30 rbt arms> --jobs 8` | 31 checks: control PASS, 30 of 30 KILLED |
| `receipts/camp_aecp_recut.log` | `aecp_mutants.py --only` the 5 re-cut arms | 8 of 8 (3 controls PASS, 5 KILLED) |
| `receipts/camp_adp_recut.log` | `adp_engine/mutants.py --only` the 2 re-cut arms | 4 of 4 (2 controls PASS, 2 KILLED) |
| `receipts/camp_d3_recut.log` | `d3_mutants.py --only dispatch_not_held enable_not_released_by_restore` | golden PASS, 2 of 2 KILLED |
| `receipts/p1`..`p8*.log`, `receipts/probe_p*.log` | `scripts/probe.py`, reviewer probes | p1, p3, p4, p5, p6, p8 DETECTED by RBT; p7 caught by the AECP command gate; p2 SURVIVED (R731-S2) |
| `receipts/probe_window.log` | `probes/window-after-notification-round.patch` | PRB-NA FAILS (R731-F1); PRB-ADV passes |
| comment-rule check | added-line scan of `hdl tb scripts syn Makefile` for review, lane and reviewer identifiers | none found |

Clone integrity after every probe: probes and builds ran only in copies under the packet's
`scratch/`, and the review clone was never edited. At the end, HEAD is still the exact head and
the index writes tree `be6818cf5ccccf5d327cc43adaec34c1df51b98c`. Every one of the 749 tracked
blobs re-hashes to its index entry, with modes intact, and there are no untracked or ignored
files. The repository has no submodule gitlinks (0 entries of mode 160000). Receipts:
`receipts/clone_index_after.txt`, `receipts/clone_tree_after.txt`. In the published logs, paths
under the user's home (the pinned simulator's install root) are redacted to
`<verilator-5.050-root>` and `<home>`.

Hosted evidence at the exact head, read only:
- `docs-gates` and `portability` succeeded in runs 40969144341 and 40969151829.
- Both runs' `suites` jobs were still in progress when read, so no hosted suite result is
  claimed. The manager owns hosted and act acceptance.

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | §7.4.43 status table, §7.4.43.2 lock and acquire, §7.5.2 / Milan §5.4.5.2 notification and exclusion, Milan §5.6.3.3/.5.8/.5.11 and IEEE §6.2.4/§6.2.5.2.2 DEPARTING, response-first order; `E_RBOOT`, the engine routes, the ADP SHUTDOWN path; RBT1 to RBT8 | R731-1 | ec1ff275a72d885f0908fd213d8009e9e4dda4d9 |
| RTL | UNCLEAN (R731-F1) | `protocol_processor_top.sv` (port, RX gate, classifier, ADP enable, arbiter mask, REBOOT sequence), `KL_aecp_engine.sv`, `KL_aecp_notify.sv`, `KL_adp_engine.sv`, `KL_pp_tx_arbiter.sv` grant/abort, `gen_ucode.py`; lint at 5.050 | R731-1 | ec1ff275a72d885f0908fd213d8009e9e4dda4d9 |
| Robustness | UNCLEAN (R731-F1) | withheld reset, slot exhaustion, MAC stalls on each required frame, the lock-expiry race at the notification round, RX arrivals after acceptance, reset clearing | R731-1 | ec1ff275a72d885f0908fd213d8009e9e4dda4d9 |
| Tests | UNCLEAN (R731-F1) | `tb/pp_top/sim_main.cpp` section RBT and hooks, `pp_top_wrap.sv`, `aecp_dispatch_mutants.py` and 30 patches, the re-cut patches and d3 rows, `tb/aecp_cmds`, README counts | R731-1 | ec1ff275a72d885f0908fd213d8009e9e4dda4d9 |
| Docs | CLEAN | 06 §6.11 and F06.14, 02 reset rule 6 and F02.10, 03 F03.5/F03.7, 04, 00 GAP-13/REQ-FWX-001, integrator and operator guides, diagram 21 diff, tb READMEs, the comment rule; the live PR body and the prepared round-2 PR body | R731-1 | ec1ff275a72d885f0908fd213d8009e9e4dda4d9 |

The Docs lens is CLEAN because the documents state the contract the RTL must meet. R731-F1's fix
makes them true. If the fix instead narrowed the contract, F02.10, the port comment and both
guides would need the same change.

## Prior public review findings

I read the prior public review on this PR, R732-1 at round-1 head `1be824fc`, only after the
verdict and ledger above were written. I did not consult any other reviewer's report.

- **R732-F1 (MAJOR, frames after the final ENTITY_DEPARTING while the request is held): RESOLVED
  at this head for the defect it demonstrated.**
  - Its mechanism was lock-expiry notifications after the DEPARTING, with the request held.
  - That mechanism is closed by the arbiter mask from the clock ADP has built its last
    DEPARTING (`hdl/top/protocol_processor_top.sv` `rbt_tx_gate`).
  - RBT9, RBT10 and RBT11 grade it, with no byte offered on `tx_*` after the final DEPARTING
    through a withheld reset. Its 13 gate arms are KILLED in `receipts/camp_disp_rbt.log`.
  - My probes p1 and p4 are DETECTED. `PRB-ADV`, with lock expiry stimulated around the
    notification round, passes.
  - R731-F1 is a separate residual of the same required outcome ("frame integrity and the held
    request are kept"). It is on the non-advertising path, where there is no DEPARTING and a
    frame granted before the gate closes overlaps the request's rise. It is a new mechanism, so
    it is tracked as R731-F1 rather than by retaining R732-F1.
- **R732-F2 (RESIDUE, the port heading's requirement ID): RESOLVED.**
  - `hdl/top/protocol_processor_top.sv:824` reads
    `//! ---- REBOOT request (REQ-FWX-001; IEEE 1722.1-2021 §7.4.43; issue #203) ----`.
  - Commit `aede92e` changes only that line.

## Real limits

- No IEEE 1722.1-2021 or Milan v1.2 text was available in this environment. Clause readings are
  from the standards as cited in the issue and the reviewed documents, checked for internal
  consistency, not quoted from the PDFs.
- I ran no full bank: no `run_suites.sh`, no Yosys or elaboration-guard bank, no parent sweep.
  The suites executed are pp_top (every build), aecp_cmds and adp_engine. The campaigns executed
  are only the REBOOT and re-cut arms. The other campaign totals the author reports at this head
  (aecp_dispatch 99 of 99, aecp 67, d3 110, notify 137, acmp 101 and others) are author
  receipts published in the public evidence tree, not re-run here.
- Gate-level behaviour of `reboot_req_o` (R731-S1) is reasoned from the encoding, not simulated.
- Physical calibration was NOT RUN. No hardware, Vivado route or parent consumer gate ran here.

## Pending manager duties

- Publish the prepared round-2 PR body. The live PR #209 description is still the round-1 text:
  79 checks, 17 arms, 86 of 86, 1,030,845 checks, -101 LUT, and no transmit gate. The prepared
  `author-r2/PR-BODY.md` in the public evidence tree carries this head's figures.
- Hosted and act acceptance: the `suites` jobs at this head were still in progress.
- The current-dev merge candidate (builder and native banks) at the merge turn, against live dev
  `1e80128f0a467b58bf884b7d9bf62e013a2fb141`.
- The parent adoption edits listed in the PR body, and milan-fpga #787's use of the port.

R731-1 FINISHED
