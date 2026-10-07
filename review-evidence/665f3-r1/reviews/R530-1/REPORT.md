[R530] NEGATIVE - exact head 351ae81f33efc1ca818c1fea21d360260ecc2587

# R530-1: internal cleared-context review of PR #688 (#665 lane F3, ACMP on the bare-metal core)

- Head under review: `351ae81f33efc1ca818c1fea21d360260ecc2587`, tree `746bf35efabe70aadff87b6dcd3bcb7cca4fbf70`, stacked on the FC head `021b9c1fb966e9a1a4acef6b5233edd3518f32a0` (an ancestor, verified).
- Delta reviewed: `git diff 021b9c1f..351ae81f`, six one-line commits with no trailers, 32 files (`sw/firmware/ctrl/acmp/*`, `ctrl_app`, tests, the mutant tables, the coverage ratchet, `tb/verilator/mbx` co-simulation, docs).
- Authorities read: AGENTS.md, CONTRIBUTING.md (by reference), the F3 assignment (#665 6026721148) and TAKEN (6026823815), REVIEW READY (6029338230), the term decision (6029368753); Milan v1.2 5.5.2 to 5.5.4 (Tables 5.22 to 5.48) and 5.6.4 (Table 5.54); IEEE 1722.1-2021 8.2.1 (Tables 8-2 to 8-4) and 6.2.2.5; FR_NFR.md 3.4.1 and 3.4.2 (H-ACMP, H-DISC); `nvm_state.h`; `docs/design/SAVED_STATE_FASTCONNECT.md` 2; the processor sources `pp_acmp_pkg.sv`, `KL_pp_acmp_listener.sv`, `KL_acmp_talker.sv`, `KL_acmp_nvm_shadow.sv`, `rom/gen_ltn_rom.py` and `tb/acmp_talker/sim_main.cpp` at the pinned gitlink `ead80360`. Standards text: a plain-text extraction of the Milan v1.2 consolidated revision (sha256 `8264854244415e364e1968b1da8e2bae7c067fa3cc98594ea54db08fc8a152c7`) of IEEE 1722.1-2021 (sha256 `966138f9a20368c94ee24456ca485b69956777f3821adf0b1d019685dd1c8a9a`), and, for the version clause only, of IEEE 1722-2016 (sha256 `f8725b4553a4afdecfc1adf888c7fc7ca44a14d67056b4836a151eb177caf40d`).
- Public evidence read: archive `c961acab` `review-evidence/665f3-r1` (MANIFEST.json, author HANDOFF.md and PR-BODY.md).

## Verdict

NEGATIVE. My own pass found no defect in the shipped C's state machines. Every Table 5.30 cell, the talker's 5.5.4 answers, the Table 5.54 discovery machine, the lock and its status code, the response keying, the #653 release and the store use match Milan v1.2 5.5 and 5.6.4. I also tested them with my own planted defects: 46 of 52 were caught by the test I expected. Three of the four processor differences are confirmed outright.

The verdict is negative for five MINOR findings of my own. Four are test gaps where a defect I planted escapes every gate: the adapter at two interfaces (F1), the binding record's flag layout and length (F2), the D3 roll-back rule (F3) and the millisecond-clock wrap (F4). The fifth (F5) is the record of the fourth processor difference, DISCONNECT_TX of an unknown source. It omits Milan v1.2 5.5.2.7, the clause that supports the processor's answer.

After my verdict and ledger were written, I read the public findings of the concurrent external round R531-1 at the same head. On reading I confirm all five, and they stay open here: two MAJOR and three MINOR (see "Prior public review findings"). Two of them are code defects my pass missed: AVTP version not checked on receive (IEEE 1722-2016 4.4.3.4), and TMR_NO_RESP started before a deferred probe leaves. Because they are open, I record the RTL lens as unclean at this head, although my own RTL pass was clean.

## Findings

### R530-1-F1 MINOR (Tests, Robustness): the mailbox adapter is never built or run at more than one AVB interface

- Where: `sw/firmware/ctrl/acmp/acmp_mbx.c:63-65` (interface `k` on slot `first_slot + k`), `acmp_mbx.c:81-93` (the expiry routed per slot), `acmp_mbx.c:38-42` (the gPTP pair per interface). The adapter tests build against the tracked contract, `sw/firmware/ctrl/mbx/mbx_contract.h:27` `#define MBX_N_IF 1u` (`test_acmp_mbx.cpp:61-62`). `tb/verilator/mbx/Makefile` `run-if2` builds only the RTL and the host model at two interfaces, not the firmware.
- Authority/evidence: the assignment's common rule ("Key protocol state per AVB interface, which keeps the redundancy path open"); `acmp_mbx.h:162-163` ("interface i's timer on slot first_slot + i"); FR_NFR.md 3.4.2 ("Each hook MUST run at every supported stream/channel/rate shape"); the review assignment's "per-interface isolation at one and two interfaces". Probe `X3-one-slot-for-all-interfaces` puts every interface on one slot, and it escaped all three arms with 0 `[FAIL]` lines (`receipts/r530/probes_3.log`). The core's two-interface behaviour is tested over fakes (A17, A22Only, TW4); the adapter's is not.
- Impact: the adapter's per-interface wiring can be broken and still pass every gate: the slot map, the expiry routing, the tag per interface and the gPTP sample. In a two-interface build, interface 1's sinks would then take interface 0's expiries or none, and its probes would stall or fire late.
- Required outcome: the adapter's slot, tag, gPTP and latency checks (B3, B4, B6 and the C paths at least) run on the two-interface contract variant (`gen_mailbox.py --variant-interfaces 2`). A planted defect in the slot map must fail a named test.
- Verification: `X3-one-slot-for-all-interfaces` (`scripts/r530_probes.py`) fails a named two-interface test.

### R530-1-F2 MINOR (Tests): the BINDING payload's flag bits and length are not pinned to the processor's layout

- Where: `sw/firmware/ctrl/acmp/acmp.c:59-62` (`BIND_VALID 0x01`, `BIND_STARTED 0x02`, `BIND_STREAMING_WAIT 0x04`), `acmp.c:391-401` and `acmp.c:1096-1119`. Tests: `test_acmp.cpp:1296-1337` (A24 restores flags `0x07`, `0x06` and `0x03`, then round-trips) and `test_acmp_nvm.cpp:157-169` (N3 round-trips through the store).
- Authority/evidence: `acmp.h:79-82` claims the record is the processor's `KL_acmp_nvm_shadow` BINDING payload. The processor packs `b = {5'd0, f.sw, f.started, vld}` (`protocol-processor/hdl/acmp/KL_acmp_nvm_shadow.sv:484`), and `SAVED_STATE_FASTCONNECT.md` 2 defines the shared 20-byte record. The code matches that byte for byte today (verified: flags, reserved byte, talker_unique_id, talker_entity_id and controller_entity_id, all big-endian). Two probes escaped every gate. `S3-flag-bits-swapped` exchanges `BIND_STARTED` and `BIND_STREAMING_WAIT` on both the read and the write side (`probes_3.log`). `S8-longer-record-applied` accepts a payload longer than 20 bytes, although A24 states "a payload of another length is refused" (`probes_b2_2.log`). The author's own `acmp-record-flags-swapped` changes only the write side, so a round trip catches it. A symmetric swap is not caught.
- Impact: an edit that moves a flag bit passes every gate. A record written by the all-fabric build (or by an earlier firmware) would then restore with `started` and STREAMING_WAIT exchanged after a placement change.
- Required outcome: a test pins the record byte for byte to vectors with one flag set at a time (valid only, valid with started, valid with STREAMING_WAIT), taken from the processor's layout. A test refuses a payload longer than 20 bytes. Each has a planted defect.
- Verification: `S3-flag-bits-swapped` and `S8-longer-record-applied` fail named tests.

### R530-1-F3 MINOR (Tests): the rule "a D3 roll-back leaves the bindings applied" is untested

- Where: `sw/firmware/ctrl/acmp/acmp_nvm.c:31-39`. Test: `test_acmp_nvm.cpp:213-244` (N6). Line 236 issues the `NVM_W_D3` roll-back after line 220 has already dropped the applied binding, so the test cannot see the binding dropped.
- Authority/evidence: `sw/firmware/ctrl_nvm/nvm_state.h:21-25` ("a D3 roll-back leaves a completed binding walk applied") and `:38-41` ("NVM_W_D3 ... the bindings untouched"). Probe `S4-d3-rollback-drops-bindings` makes every roll-back drop the bindings before forwarding, and it escaped (`probes_3.log`).
- Impact: a regression that drops the restored bindings when the D3 walk rolls back would pass every gate. An entity-model CRC failure at boot is one such roll-back, and the fast connect would then be lost.
- Required outcome: a test applies a binding, rolls back `NVM_W_D3`, and requires the binding kept with no unbind. It has a planted defect.
- Verification: `S4-d3-rollback-drops-bindings` fails that test.

### R530-1-F4 MINOR (Tests, Robustness): the 32-bit millisecond clock's wrap is never exercised

- Where: `sw/firmware/ctrl/acmp/acmp.c:281-284` (`due`) and `acmp.c:320-326` (`earliest`). Both use the signed difference, which is correct. The tests' clock starts at 50000 (`acmp_fake.hpp:107`), at 70000 (`test_acmp.cpp:1081`) or 1234 ms past the model's origin (`test_acmp_mbx.cpp:248`), and it never nears 2^32.
- Authority/evidence: FR_NFR.md 3.4.2 ("Test saturation, reset, timer wrap, CPU stalls and both bus adapters", line 448, for every H- hook). NOW_MS is a free-running 32-bit millisecond counter, so it wraps after about 49.7 days. Probes `W1-due-unsigned-compare` and `W2-earliest-unsigned-compare` replace the signed difference with a plain unsigned comparison. Both escaped `acmp` and `acmpwalk` with 0 `[FAIL]` lines (`probes_b3.log`).
- Impact: a regression to an unsigned comparison passes every gate. In the field it fires TMR_NO_RESP, TMR_NO_ADP and the others at once, or never, from the first wrap on. Every sink then churns or wedges. Long uptime is the normal case for an end station.
- Required outcome: tests arm each connection timer and TMR_NO_ADP so that the deadline crosses the wrap, and require each expiry at its deadline and not before. A test does the same for the interface timer's earliest-deadline choice. Each has a planted defect.
- Verification: `W1-due-unsigned-compare` and `W2-earliest-unsigned-compare` fail named tests.

### R530-1-F5 MINOR (Conformance, Docs): difference TD1 is recorded as a processor defect without the clause that supports the processor

- Where: `docs/design/MAILBOX_SPLIT.md:620-623` ("DISCONNECT_TX for a source that does not exist ... Each is the processor's to fix"), `sw/firmware/ctrl/README.md:126-128`, `sw/firmware/ctrl/test/acmp_walk.cpp:53-54` and `:790-793`, `acmp.h:51-56`, and the PR body ("asserted field for field in `acmpwalk`").
- Authority/evidence: Milan v1.2 5.5.4.2 step 1 and Table 5.44 give TALKER_UNKNOWN_ID, which the firmware sends. But Milan v1.2 5.5.2.7 says "The DISCONNECT_TX_COMMAND always returns SUCCESS without modifying the state of the Talker", and that is what the processor does (`protocol-processor/hdl/acmp/KL_acmp_talker.sv:1301-1306`: the DISCONNECT_TX arm answers SUCCESS without reading `uid_valid_w`). I read the firmware's choice as right, because 5.5.2.7 itself ends "The complete specification of the talker's behavior is defined in Section 5.5.4". The record states neither clause's text against the other. The walk also asserts only the firmware half: the talker arm cuts the processor suite's constants, not a model, and that suite has no unknown-source DISCONNECT_TX check. So TD1 is not "asserted field for field" as LD1 to LD3 are. Its processor half is a reading of the RTL.
- Impact: the processor issue the manager will file from this record would lack the 5.5.2.7 sentence its owners will cite. The PR overstates the executed evidence for one of its four differences.
- Required outcome: the TD1 record names the 5.5.2.7 and 5.5.4.2 tension and why 5.5.4.2 governs. It cites the processor RTL line as the evidence for the processor half, or says that half is read from source and not walked. The PR body's "field for field" claim is limited to LD1 to LD3.
- Verification: read the changed docs and PR body.

### R530-1-R1 RESIDUE (Docs): the adp filter term is still described as an open decision

- Where: `docs/design/MAILBOX_SPLIT.md:542` ("The decision is open on #665"), `:733-736` ("which term it is waits for the decision on #665"), `sw/firmware/ctrl/README.md:62-64` ("as an open decision"), and the PR body's "Known limitations" and Definition of Done.
- Evidence: #665 comment 6029368753 decided the term (bound talkers only) and assigned it to F3 round 2. The decision post-dates this head's REVIEW READY. This is status prose only. It changes no measurement, test, code, figure or clause claim.
- Exact fix: replace each "open decision" phrase with "decided on #665 (6029368753): ENTITY_AVAILABLE and ENTITY_DEPARTING of a talker bound on the receiving interface; F3 round 2 adds the term".

### Not findings, recorded for the manager

- **One new coverage exclusion, justified.** `sw/firmware/gtest/README.md` adds one row: `ctrl_app.c` `ctrl_app_compose`, `return cfg->acmp == NULL`, arc 6 of 6, where `acmp_mbx_attach` refuses. I checked it as unreachable. The statement above it binds ADP's handler on the adp channel, and ADP takes one of eight sinks and one of eight polls in a loop initialised empty. The refusals are tested on the adapter itself (B7). The three ACMP files are at 100 % raw (690/690 and 316/316, 66/66 and 26/26, 38/38 and 10/10). `ctrl_app.c` is 20/21 lines and 17/20 branches raw: two arcs and one line are pre-existing rows, one arc is new.
- **The differential walk is honest for the listener and discovery.** `ctrl_reuse.py` cuts the processor's `tb/acmp_listener/sim_main.cpp` F05.3 matrix model and frame builder and the `tb/adp_engine` Table 5.54 transcription. It proves the pin and blob first. `acmp_walk.cpp:406-481` drives model and firmware in lock step and compares the frames byte for byte. LD1 to LD3 are patched only after asserting that the processor differs in exactly that way. The talker arm reuses constants only (see F5).
- **Processor differences verified against the clauses:**
  - LD1 is confirmed. Table 5.36 gives talker fields 0; `KL_pp_acmp_listener.sv:672-677` echoes them.
  - LD2 is confirmed. 5.5.3.5.30 step 2 sets no status; the processor's A12 (`KL_pp_acmp_listener.sv:1242-1245`) zeroes it.
  - LD3 is confirmed. IEEE 1722.1-2021 Table 8-3: 13 is TALKER_MISBEHAVING and 16 is CONTROLLER_NOT_AUTHORIZED; `pp_acmp_pkg.sv:123` has 13.
  - TD1 holds against 5.5.4.2 but is contested by 5.5.2.7 (F5).
  - Not listed among the differences, and within the clause: 5.5.4.1 step 2 permits either answer to a PROBE_TX from the wrong interface. The processor ignores it (`KL_acmp_talker.sv:1298`); the firmware answers INCOMPATIBLE_REQUEST. TW4 states this.
- **Known open item (not a finding):** the adp channel passes no ENTITY_AVAILABLE or ENTITY_DEPARTING. The firmware half is correct and testable as delivered. The tap (`acmp_mbx.c:109-117`) hands message types 0 and 1 to `acmp_adp_rx` and all else to ADP's handler (B5, my X2 and X11). The machine filters exactly by talker, bound state and interface (`acmp.c:984-995`; D7). H-DISC is shown with records written into the adp ring (F5, C10, C11, C12).
- **A4 (not a finding):** the T_svc full-backlog bounds (10,835, 21,670 and 8,865 accesses) depend on the unmeasured access time. I checked `ACMP_MBX_PASS_MAX` = 8 x 41 + 16 x 22 + 2 x 43 + 2 x 83 + 31 + 22 = 985 against `acmp_mbx.h:129-134`.

## What each lens examined

### Conformance

- **Listener:** `acmp.c:686-830` (bind, unbind, get_rx_state, listener_command, probe_response) and `acmp.c:470-523`, `:648-672` (timers, delay, passive, reprobe, the EVT_TK_* handlers). I checked each against Milan v1.2 5.5.3.1, 5.5.3.5.1 to 5.5.3.5.48 and Tables 5.27, 5.31 to 5.39:
  - all eight states and every Table 5.30 cell;
  - step 2 of the same-source re-bind;
  - the response before the probe;
  - TMR_NO_RESP 200 ms, then the duplicate with the same sequence_id, then status 7 and TMR_RETRY 4 s;
  - TMR_RETRY step 1 and step 2 (status kept);
  - TMR_DELAY 0 to 1000 ms;
  - TMR_NO_TK 10 s;
  - the lock before any change, and GET_RX_STATE never locked;
  - LISTENER_UNKNOWN_ID echoing the command;
  - PROBE_TX_RESPONSE routed by listener_unique_id and matched on the sent probe's controller, talker, talker_unique_id and sequence_id.
- **Talker:** `acmp.c:834-882` against 5.5.4.1 to 5.5.4.4 and Tables 5.40 to 5.48.
- **Discovery:** `acmp.c:525-596`, `:963-1000` against 5.6.4.1 and 5.6.4.5.1 to 5.6.4.5.4: the GM and domain on this port, interface_index, the available_index restart with DEPARTED before the GM check, the departing, the expiry, and valid_time in two-second units (IEEE 1722.1-2021 6.2.2.5).
- **Wire:** the ACMPDU offsets (`acmp.c:36-49`, Figure 8-1), the flags (Table 8-4), the status codes (`acmp.h:164-171`, Table 8-3) and the ADPDU offsets (`acmp.c:52-57`).
- Finding: F5.

### RTL and architecture

There is no RTL in the delta: 0 files under `hdl`, `sw/litex`, `configs`, `sw/mailbox`, `syn`, `constraints` or any gitlink (`receipts/r530/clone_state.txt`). Applied to the firmware's architecture:

- **Widths:** status 5 bits, `1u << k` with k < 16, `change_owed` at most 8, `valid_ms` at most 62 s, and the uint16 sequence and tag wraps.
- **Signedness:** the deadline comparisons (`acmp.c:281-326`).
- **FSM completeness:** `sm_expired`'s final branch is reachable only in SETTLED_NO_RSV, and the "x" cells are counted (`acmp.c:1039-1057`).
- **Interfaces:**
  - the #678 guard (`acmp.c:83-170`);
  - `ctrl_app_compose`/`ctrl_app_open` (U5: composing touches no register);
  - the `ctrl_loop` bindings;
  - the per-interface timer multiplexing with the tag rule (`acmp_mbx.c:24-36`, `:75-94`);
  - the latency arithmetic (`acmp_mbx.h:109-145`).
- Co-simulation on the RTL: `make run-cosim`, 28 checks with 0 failures over 12 identical frames (`receipts/r530/cosim.log`).
- No finding of my own. The lens retains R531-1-F1, F2 and F3 (see "Prior public review findings").

### Robustness

- **Malformed and truncated input:** `acmp.c:920-924` and `:968-972`, plus the tap's fixed buffer (`acmp_mbx.c:103-108`).
- **Boundaries:** sink and source off-by-one (probes L15, T6, L16).
- **Invalid ordering:** responses outside probing, and stray expiries.
- **Repeated commands:** A25 and the same-source re-bind.
- **Backpressure:** the owed queue, a dropped command before it acts, and a lost probe recovered by TMR_NO_RESP.
- **Reset and roll-back:** `acmp_restore_rollback`.
- **Configuration-dependent behaviour:** one interface against two.
- **Clock wrap.**
- Findings: F1 and F4.

### Tests

- **Reviewer probes:** 52 defects of my own across listener cells, discovery, talker, adapter and ordering, and the store (`scripts/r530_probes.py`). 46 were caught by the expected named test. 6 escaped: X3, S3, S4, S8, W1 and W2. One more (D3) was refused because it did not compile, and was re-planted as D3b, which was caught.
- **The author's table:** a 26-defect sample from `acmp_mutants.py` (`scripts/r530_author_sample.py`), graded with the campaign's own `caught()`. 26 of 26 failed their named test on the named words.
- **Counts:** `ctrl_mutants.MUTANTS` has 288 entries (195 from `acmp_mutants.py`), and `unnamed_tests()` is empty.
- **Gate runs:** `test_ctrl_firmware.py --require-rv32` returned rc 0 with every arm passing (`acmp` 67, `acmpwalk` 127, `acmpnvm` 6). `fw_coverage.py --check --jobs 2` returned rc 0 with 17 files at 100 % after exclusions.
- **Walk honesty:** checked (above).
- Findings: F1, F2, F3 and F4.

### Documentation

- **Examined:** `docs/design/MAILBOX_SPLIT.md` "The ACMP module" (lines 484 to 623) and its Open items (730 to 745); the READMEs of `sw/firmware/ctrl`, `sw/firmware/gtest` (the exclusion row), `sw/firmware/ctrl_nvm` and `tb/verilator/mbx`; the headers' clause maps (`acmp.h:4-109`, `acmp_mbx.h:4-92`, `acmp_nvm.h:4-31`); the PR body and HANDOFF in `c961acab`.
- **Figures checked against my runs:** 67, 127 and 6 tests; 195 and 288 defects; 690/690 and 316/316; 28 co-simulation checks over 12 frames; 985 accesses a pass.
- Findings: F5 and the residue R1. Also retains R531-1-F4 and F5.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F5; retains R531-1-F1, F2, F3) | `acmp.c:470-1000`, `acmp.h:131-183`, MAILBOX_SPLIT.md:605-623, `acmp_walk.cpp:42-55`, the processor's `pp_acmp_pkg.sv:123`, `KL_pp_acmp_listener.sv:672-677,1242-1245`, `KL_acmp_talker.sv:1276-1306`, against Milan v1.2 5.5 and 5.6.4 and IEEE 1722.1-2021 Tables 8-3 and 8-4 | R530-1 | `351ae81f33efc1ca818c1fea21d360260ecc2587` |
| RTL | UNCLEAN at this head: my pass left no finding (CLEAN in the ledger as first written), but it retains R531-1-F1, F2 and F3, confirmed on reading | delta file list (0 RTL or gitlink files), `acmp.c:83-433,1007-1094`, `acmp_mbx.c:1-130`, `acmp_mbx.h:109-145`, `ctrl_app.c:10-47`, `receipts/r530/cosim.log` | R530-1 | `351ae81f33efc1ca818c1fea21d360260ecc2587` |
| Robustness | UNCLEAN (F1, F4; retains R531-1-F1, F2, F3) | `acmp.c:240-326,915-1000`, `acmp_mbx.c:24-117`, probes L15, L16, T6, X3, W1, W2 | R530-1 | `351ae81f33efc1ca818c1fea21d360260ecc2587` |
| Tests | UNCLEAN (F1 to F4; retains R531-1-F1, F2, F3) | `test_acmp.cpp`, `test_acmp_mbx.cpp`, `test_acmp_nvm.cpp`, `acmp_walk.cpp`, `acmp_mutants.py`, `ctrl_reuse.py`, `coverage.ratchet`, `receipts/r530/probes_*.log`, `author_sample_*.log`, `ctrl_gate.log`, `coverage_check.log` | R530-1 | `351ae81f33efc1ca818c1fea21d360260ecc2587` |
| Docs | UNCLEAN (F5; retains R531-1-F4, F5; R1 is residue) | MAILBOX_SPLIT.md:484-745, `sw/firmware/ctrl/README.md`, `sw/firmware/gtest/README.md` (exclusion row), `sw/firmware/ctrl_nvm/README.md:494-501`, `tb/verilator/mbx/README.md`, header comments, PR-BODY.md and HANDOFF.md at `c961acab` | R530-1 | `351ae81f33efc1ca818c1fea21d360260ecc2587` |

## Prior public review findings on this PR

I checked after writing this round's verdict and ledger: PR #688's issue comments, its review bodies and its inline comments (0). Before this round there were only the two review-start notices (6029365541, 6029366108). The concurrent external round R531-1 (6029581606, posted 02:26Z at the same head) has five findings. None can be resolved at this head, because nothing has changed since. I checked each against the code and the clause, and each is **retained, open**. The lens labels are R531's, and so are the severities.

| Finding | Severity (R531) | My check at this head | State |
|---|---|---|---|
| R531-1-F1: AVTP version not checked on receive | MAJOR | Confirmed. IEEE 1722-2016 4.4.3.4 says a version the receiver does not support "shall" be discarded (PICS AVTP-7, mandatory). IEEE 1722.1-2021 6.2.2.3 and 8.2.1.3 fix version 0. `acmp.c:920-924` and `:968-972` test the EtherType, subtype and length, but never byte 15 bits 6:4. `decode` masks only the message_type (`acmp.c:176`). My Robustness pass missed it. | retained, open |
| R531-1-F2: TMR_NO_RESP starts before a deferred probe leaves | MAJOR | Confirmed by reading. `send_probe` sets the 200 ms deadline (`acmp.c:615`) before `transmit` knows whether the frame went, and `acmp_poll` (`acmp.c:1077-1094`) sends an owed probe without moving it. So an owed probe or duplicate gets 200 ms less its wait. Milan v1.2 5.5.3.5.16 steps 1 and 2, and 5.5.3.5.3 steps 5 to 7, start the timer after the send. My pass checked that a lost probe recovers (A19), not the length of an owed one's window. | retained, open |
| R531-1-F3: `first_slot + MBX_N_IF` wraps in `acmp_mbx_init` | MINOR | Confirmed. `acmp_mbx.c:54` is an unsigned sum; `first_slot = UINT_MAX` passes the check and `acmp_mbx.c:64` narrows it to `uint8_t`. The app passes the constant `MBX_N_IF`, so the composition is unaffected. | retained, open |
| R531-1-F4: MAILBOX_SPLIT.md:595-596 counts the seven-owed-frames bound among those that miss T_svc at 1 us | MINOR | Confirmed. 8,865 accesses at 1 us is 8.87 ms, under 10 ms, and the table beside it gives 1.13 us as that row's limit. | retained, open |
| R531-1-F5: `acmp.h:396-398` promises retries "until one is refused" | MINOR | Confirmed. `acmp_poll` sends at most one owed frame per call (`acmp.c:1082-1092`). That is what A19, E2 and `acmp_mbx.h:84-86` rely on. | retained, open |

My TD1 reading (F5 here) differs from R531-1's. R531 judges TD1 justified despite 5.5.2.7. I agree the firmware is right, but I find the record incomplete without that clause. Both readings are recorded.

## Commands run (foreground, at the exact head; receipts under `receipts/r530/`)

| Command | rc | Receipt |
|---|---|---|
| `scripts/run_pair.sh <clone> <packet>`: `fw_coverage.py --check --jobs 2` | 0 | `coverage_check.log` |
| the same script: `test_ctrl_firmware.py --require-rv32 --build-dir <scratch>` | 0 | `ctrl_gate.log` |
| `make run-cosim VERILATOR=<pinned 5.050>` in a `git archive HEAD` export | 0 | `cosim.log` |
| `r530_probes.py <clone> <scratch> K/3 0`, K = 1 to 3 (batch 1, 39 probes) | 0 each | `probes_1.log` to `probes_3.log` |
| `r530_probes.py <clone> <scratch> K/2 39`, K = 1, 2 (batch 2, 11 probes) | 0 each | `probes_b2_1.log`, `probes_b2_2.log` |
| `r530_probes.py <clone> <scratch> 1/1 50` (batch 3, 2 probes) | 0 | `probes_b3.log` |
| `r530_author_sample.py <clone> <scratch> K/2`, K = 1, 2 (26 author defects) | 0 each | `author_sample_1.log`, `author_sample_2.log` |
| clone integrity after every probe | - | `clone_state.txt` |

In `cosim.log` the home-directory prefix of the tool's include path is replaced by `~`; nothing else in any receipt is edited.

The probe driver exits 0 by design. A probe's result is its `[CAUGHT]` or `[ESCAPED]` line. Every probe plants into a copy of `sw/firmware/ctrl` under the scratch tree. The clone was never edited: its index equals the HEAD tree (mode, blob and path), its tracked bytes match, it has no untracked or ignored file, and its gitlinks equal their checkouts.

## Real limits

- Not run, by the assignment's limits: the full parent, processor, gPTP, Yosys and builder banks; `make -C tb/verilator/mbx` in full and its mutants; the full 288-defect campaign; `test_ctrl_nvm.py`; the docs workflow; the hosted and act runs. For these I rely on the manager's public evidence at this head.
- The RV32 arm ran (rc 0) with the host's RV32 compiler. The firmware runs on no target, so there is no target-time result.
- The standards were read from plain-text extractions (hashes above), not the published PDFs.
- Physical calibration: NOT RUN. Field skips are not hardware proof.
- The adp filter term and the access time (A4) are open items owned elsewhere, as stated above.

## Pending manager duties

- Carry F1 to F5 to the lane's next round, together with the retained R531-1-F1 to F5. Each of mine needs a named test that fails on its probe, which the probe scripts here can replay.
- Carry R1 to the residue checklist.
- File the processor issues for LD1 to LD3 as confirmed. File TD1 with both 5.5.2.7 and 5.5.4.2 cited (F5).
- The current-dev candidate merge and its gates (live dev `79b086d44eb62d007d38e18f5618b98e8e2a33e6`), and the `--no-ff` dev merge once FC lands.
- Hosted and act acceptance at the exact head.
- Measuring the access time at the F2 to F5 bench pass (A4), and the round 2 filter term.

R530-1 FINISHED
