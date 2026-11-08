# [A750] HANDOFF: tsn-c-stack issue #26 (ACMP owed bound)

Status: REVIEW READY at 3d57262c3614740244de40c40f667908ce6310f7. Every gate returns 0 on both targets.

- Repository: kebag-logic/tsn-c-stack
- Branch: `26-acmp-owed`, from `main` 70936b77dc41981e192438388cd0aced69954f18
- Head: 3d57262c3614740244de40c40f667908ce6310f7, "Decline, never drop, an ACMP command at the owed bound".
  One commit, as hackerman-kl <hackerman-kl@kebag-logic.com> (author and committer), one-line subject.
- Issue #26: "[A750] TAKEN" posted at start. "[A750] REVIEW READY" is posted at the end with the head.
- Not pushed; no PR opened. PR text: `PR-BODY.md` (starts "[A750]", "Relates to #26").

## Decision and clause

**Choice: queue until room returns, not an immediate error status.**
With all `ACMP_OWED_MAX` (8) frames owed, `acmp_rx` declines a command addressed to this
entity's listener or talker. It returns `false`, changes no state, makes no port call and
counts `busy_declined`. The port keeps the frame and delivers it again after `acmp_poll`
accepts an owed frame. The command is then served normally, and its specified response
leaves behind the frames owed ahead of it. `acmp_rx_ready()` is a const predicate: a port
can test it before taking a frame from its receive ring and leave the frame in the ring
meanwhile. milan-fpga's loop already has this hook, `ctrl_loop_set_rx_ready`.

Clause basis (also cited in the code comment at `src/acmp.c:325-326`, above `room()`):

- **IEEE 1722.1-2021 8.2.4** (Listener state machine) and **8.2.5** (Talker state machine):
  each received command is answered through `txResponse` with the status its handling
  function returns. **Table 8-3** has no status that means "the response queue is full".
  `COULD_NOT_SEND_MESSAGE` is assigned only by 8.2.4.2.4, to a Listener whose own command
  to a Talker could not be sent (for example, no free InFlightCommand entry). A Milan
  Listener never relays such a command for a controller (Milan v1.2 5.5.2.2 and 5.5.2.7).
- **Milan v1.2 5.5.3.5 and 5.5.4** fix each response's fields and status. For example,
  Table 5.34 answers GET_RX_STATE in UNBOUND with SUCCESS. None of these clauses assigns a
  busy status. An error answer would contradict them, and the controller would have to
  repeat a command that only needed to wait.
- **Milan v1.2 5.5.2.3, Table 5.26**: 200 ms for every command this core answers.
  IEEE 1722.1-2021 Table 8-1 allows 200 ms or more for each command, so Table 5.26 is the
  tighter bound and the tests use 200 ms.
- While the egress is held, no answer can leave at once. An error frame would need the
  same storage as the deferred command, so "answer at once" gains nothing in the held case.
- Numbering note: the issue cites 8.2.2, the 1722.1-2013 numbering. There, 8.2.2 is
  "Protocol Specification" and the Listener and Talker state machines are 8.2.2.5 and
  8.2.2.6. In the 2021 edition, 8.2.2 holds the shared types (8.2.2.1 defines
  ACMPCommandResponse) and the state machines are 8.2.4 and 8.2.5. The code and docs cite
  the 2021 numbering.

Bounded memory cannot hold an unbounded burst while the egress is held, so no design can
store every command. This design adds no memory to the core and never discards a command
it receives: each command is either served, or declined to its caller with nothing
changed. The declined command waits in the port's receive queue, whose depth and overflow
accounting are the port's, as for any receive ring.

## Changes (file:line, head 3d57262)

- `src/acmp.c:325-334`: `room()` cites the clauses (ACMP-12) and counts `busy_declined`
  instead of `busy_drops`.
- `src/acmp.c:899` and `src/acmp.c:958`: `listener_command` and `talker_command` no longer
  test `room()`. The single decline point moved to `acmp_rx`.
- `src/acmp.c:1036-1040`: new `acmp_rx_ready()`, `!in_port && owed_count < ACMP_OWED_MAX`.
- `src/acmp.c:1042-1095`: `acmp_rx` returns `bool`:
  - `false` on refused re-entry (`:1044-1046`);
  - `true` for malformed frames (`:1050`);
  - `talker && !room(a)` declines a talker command (`:1061-1063`);
  - `listener && !room(a)` declines a listener command (`:1073-1075`);
  - `true` after `finish` (`:1094`).
  A declined command returns before `finish`, so it makes no port call.
- `include/acmp.h:436-437`: `busy_drops` is renamed `busy_declined` (REQ: ACMP-12).
- `include/acmp.h:452-454`: `bool acmp_rx(...)` and `bool acmp_rx_ready(const struct acmp *)`.
- `examples/rv32/smoke.c:274-304` and `:330`: new RV32 check `acmp_owed_smoke`.
- `tests/test_acmp.cpp:1096-1114`: `A19AFullQueueDropsTheCommandBeforeItActs` is rewritten as
  `A19AFullQueueDeclinesTheCommandBeforeItActs`.
- `tests/test_acmp.cpp:2561-2766`: new `AcmpOwed` fixture (a port model that keeps declined
  frames and delivers them again in order) and five tests.
- `tests/mutations.json`: 22 new plants (`owed-*`), and `acmp-full-queue-acts` updated
  (renamed counter, new killers). Total 410 plants: 406 core and 4 generated configuration.
- `docs/PORTING.md:74-91`: new "ACMP owed bound" contract, covering:
  - the bound and its memory;
  - the decline, redelivery and arrival-order rules;
  - the readiness query;
  - the cost of a declined command;
  - the served response, the pass count and the 200 ms budget;
  - the clauses.
  `docs/PORTING.md:68` drops the old drop sentence. `docs/PORTING.md:319` is the
  `busy_declined` counter row.
- `docs/REQUIREMENTS.md:38-51`: new "ACMP owed bound" section and the ACMP-12 row.
  `docs/requirements.json:220-241`: the ACMP-12 record (origin: issue 26).
  `scripts/requirement_records.py:17-20`: the ACMP-12 origin.
- `scripts/check_port_contracts.py:34-40` and `:279-285`: the "ACMP owed bound" names and
  their critical meanings. `:209` uses `busy_declined`.
- `docs/VERIFICATION.md:24`: plant count 384 becomes 406. `:138`: RV32 smoke row
  "ACMP owed bound".
- `docs/ARCHITECTURE.md:11`, `CHANGELOG.md:5`: storage line and change-log entry.
- Generated: `docs/TRACEABILITY.md` (ACMP-12 row 26), `docs/TESTS.md`,
  `tests/coverage.ratchet:5` (acmp.c lines 792/792 → 795/795, branches 392/392 → 400/400).

## Tests and the planted mutants they kill

"Sole" means the plant fails exactly that test in the full 106-test ACMP suite. Excluding
that test (`--gtest_filter=-Test`) then gives rc 0 with no failures, so the plant escapes
without the test. Evidence: `escape-evidence.json`, from the final campaign's mutant
binaries.

| Test | Proves | Plants it kills (sole killer **bold**) | Escape without the test |
|---|---|---|---|
| `AcmpOwed.HeldEgressDefersTheCommandBehindTheOwedSet` (`tests/test_acmp.cpp:2620`) | Fills the owed set (8 GET_RX_STATE) with the egress held, then offers a ninth. It is declined (`false`, no port call, counted), held 60 ms, delivered again after the first accepted frame, and answered with the Milan Table 5.34 SUCCESS fields. The answer comes 69 ms after arrival, in pass 9 after the egress returns; 69 ≤ 200 ms. All 9 answers leave in order. | **owed-get-rx-state-drop-restored**, owed-listener-drop-restored, acmp-full-queue-acts, owed-decline-uncounted | owed-get-rx-state-drop-restored escapes (rc 0, 105 tests pass) |
| `AcmpOwed.TalkerCommandsBehindTheOwedSetAreAnsweredInTime` (`:2649`) | PROBE_TX, DISCONNECT_TX and GET_TX_CONNECTION behind the full set are declined. The declined PROBE_TX reads no source state. Each is answered after the egress returns with its Milan Table 5.43, 5.45 or 5.48 fields, within 200 ms and in arrival order. | **owed-probe-tx-drop-restored**, **owed-disconnect-tx-drop-restored**, **owed-get-tx-connection-drop-restored**, owed-talker-drop-restored, owed-talker-acts-then-declines | all three per-command plants escape |
| `AcmpOwed.DeclinedUnbindChangesNothingUntilItIsTaken` (`:2694`) | An UNBIND_RX for a bound sink behind the full set changes no instance byte except its counter (whole-struct compare) and calls no port, environment or publish service. It unbinds only when taken, and its Milan Table 5.36 answer arrives within 200 ms. | **owed-unbind-rx-drop-restored**, owed-listener-acts-then-declines, owed-decline-uncounted | owed-unbind-rx-drop-restored escapes |
| `AcmpOwed.ReadyPredicateMatchesTheOwedBound` (`:2720`) | Boundary: 7 owed is ready and the 8th command is taken; 8 owed is not ready; one accepted frame makes it ready again. Inside a port callback it is not ready, and `acmp_rx` declines (re-entry counted, not `busy_declined`). | **owed-ready-ignores-full**, **owed-ready-ignores-reentry**, **owed-ready-off-by-one**, **owed-reentry-taken**, owed-room-off-by-one, owed-served-reported-declined | all four sole plants escape |
| `AcmpOwed.OnlyOwnCommandsAreDeclined` (`:2745`) | With the set full, malformed, foreign-listener, foreign-talker and probe-response frames are still taken (`true`) and never counted as declined. | **owed-malformed-declined**, **owed-declines-every-frame**, **owed-declines-foreign-listener**, **owed-declines-foreign-talker**, owed-served-reported-declined | all four sole plants escape |
| `AcmpCore.A19AFullQueueDeclinesTheCommandBeforeItActs` (`:1097`, rewritten) | BIND_RX and GET_TX_STATE behind the full set each return `false`, leave the sink UNBOUND, make no port call and count 2. | **owed-bind-rx-drop-restored**, **owed-get-tx-state-drop-restored**, acmp-full-queue-acts, owed-listener-drop-restored, owed-talker-drop-restored | both per-command plants escape |

The planted mutant that **restores the silent drop**: each `owed-<command>-drop-restored`
plant makes the core take that one command type behind the full set and lose its response,
as main does. The test for that command type kills it. The broader
`owed-listener-drop-restored` and `owed-talker-drop-restored` plants (decline returns
`true`) and `acmp-full-queue-acts` (no bound at all) are killed by two to four tests each.

Mutation campaign: final run 410/410 CAUGHT, 0 ESCAPED, 0 ERROR. main: 388/388.

## Boundary evidence

- Owed count 7 → taken; 8 → declined; after one accepted frame (7) → ready and taken.
  Hosted: `ReadyPredicateMatchesTheOwedBound`. RV32: `acmp_owed_smoke` (codes 91-94).
- Declined → no state change: whole-instance byte compare in
  `DeclinedUnbindChangesNothingUntilItIsTaken`, with only `busy_declined` and the per-entry
  `now_read` scratch flag masked. No port or publish call.
- Timing: with a 60 ms hold and a port that polls once per 1 ms pass, the deferred answer
  leaves exactly `kHoldMs + ACMP_OWED_MAX + 1` = 69 ms after arrival, at most 200 ms
  (Milan v1.2 Table 5.26). The core adds no pass beyond the frames owed ahead of the command.
- RV32 (Debug and Release): with the egress held, 8 commands are taken; the ninth returns
  `false` with `acmp_rx_ready` false, no port call and `busy_declined == 1`. After one poll
  it is taken. The ninth frame sent is its GET_RX_STATE_RESPONSE (seq 8, SUCCESS).
- Coverage: `src/acmp.c` 795/795 lines and 400/400 branches (100%), no new exclusions.

## Gate table (Linux hosted and bare-metal RV32)

Toolchain: GoogleTest/GMock 1.14.0 (pinned prefix), host GCC and Clang, Clang 18.1.3 for
lexing. Static analysis uses Ubuntu 24.04's clang-tidy 18.1.3, as CI does (see Environment
notes); host cppcheck 2.22.0. The graph gate uses Mermaid CLI 11.16.0, the CI pin, installed
in scratch.

| Gate | main 70936b77 | lane | Bare-metal RV32 / scope |
|---|---|---|---|
| entity-golden | 0 | 0 | Shared source gate. |
| entity-controls | 0 | 0 | Shared source gate. |
| boundary | 0 | 0 | Hosted symbol and dependency audit. |
| needles | 0 | 0 | Assertion contract. |
| assertion-templates | 0 | 0 | Assertion contract. |
| dependencies | 0 | 0 | Hosted. |
| comments | 0 | 0 | Comment contract; includes the RV32 cross-compiled controls. |
| conditionals | 0 | 0 | Conditional matrix. |
| port-contracts | 0 | 0 | Porting guide names and meanings (29 meaning controls). |
| acmp-cache | 0 | 0 | Hosted. |
| registration-controls | 0 | 0 | Hosted. |
| license | 0 | 0 | Shared. |
| traceability | 0 | 0 | 46 requirements; 155 test declarations. |
| test-inventory | 0 | 0 | 155 declarations; 410 plants. |
| coverage-controls | 0 | 0 | Hosted. |
| privacy-selftest | 0 | 0 | Shared. |
| privacy | 0 | 0 | Also run after the commit: 15 commits, 271 blobs, 98 files, rc 0. |
| gcc-configure / build / test | 0 / 0 / 0 | 0 / 0 / 0 | Hosted. |
| coverage | 0 | 0 | acmp.c 100% lines and branches. |
| clang-sanitizers-configure / build / test | 0 / 0 / 0 | 0 / 0 / 0 | Address and undefined-behaviour sanitizers, leak detection. |
| static-analysis | 1 with host clang-tidy 23 (padding check absent from CI's 18); 0 with clang-tidy 18 | 0 (clang-tidy 18) | Hosted. |
| mutation | 0 (388 CAUGHT) | 0 (410 CAUGHT) | Hosted campaign. |
| mutation-controls | 0 | 0 | Hosted. |
| graphs | 0 (4 rendered) | 0 (4 rendered) | Shared. |
| `baremetal.py` Debug | rc 0 | rc 0 | RV32I ILP32 freestanding link and QEMU smoke, including `acmp_owed_smoke`. |
| `baremetal.py` Release | rc 0 | rc 0 | Same, -O3. |

Final run on head 3d57262 (`validate.py --jobs 8 --graphs`): 28/28 gates rc 0 (`final-gates.json`).
Mutation: 410/410 CAUGHT. Coverage: acmp.c 795/795 lines, 400/400 branches.
GCC and Clang-sanitizer suites: 8/8 binaries pass.
`baremetal.py --jobs 8`: Debug rc 0 and Release rc 0; both smoke logs say "ADP, ACMP and MAAP smoke checks: rc 0" (`final-rv32-results.json`).
The working tree is clean at the head.

Commands (from the lane):

```sh
python3 scripts/validate.py --work build-validation --jobs 8 --graphs
python3 scripts/baremetal.py --work build-rv32 --jobs 8
```

## Bare-metal image size and ACMP record path cost, before and after

`scripts/baremetal.py` images (`rv32_smoke.elf`). The ELF includes the new smoke function;
the `acmp.c` object isolates the core.

| Build | ELF bytes | `.text` | `.rodata` | `.bss` | `acmp.c` object text |
|---|---|---|---|---|---|
| Release, before → after | 46552 → 47512 | 34856 → 35752 | 1961 → 1961 | 8 → 8 | 18053 → 18213 (+160) |
| Debug, before → after | 141440 → 144192 | 45460 → 46928 | 2048 → 2048 | 8 → 8 | 20729 → 20869 (+140) |

ELF sha256:

- main: Debug 1c86985e508eeece8d2b5b9f06e08f27fb824c29bc2893a812ac035746ceb13c;
  Release 0d8f38768802427a7add67ff7dfde00749e501e385101fe4a765acdf6a9655f0.
- lane, final run at 3d57262: Debug 5c8c483eafe3ec6d17fa081bb5313e9fa3414578190d7b7a8e04143b07699e9a;
  Release a9fad2c0b84ec9358029634e4e58b69bd971455c84bc154221d89386def9f356.
- The Release ELF is byte-identical to the earlier lane run. The Debug ELF differs only
  because its debug info records the build directory.

With the split firmware's flags (`-march=rv32im -Os`), the `acmp.c` object text goes from
10697 to 10689 bytes (−8).

**Owed set memory:** 8 × 80 = 640 bytes, plus `owed_head` and `owed_count`, on RV32 and
x86-64. It is unchanged. `sizeof(struct acmp)` is unchanged: 5064 bytes RV32, 5072 bytes
x86-64, measured by compiling `sizeof` into both targets.

**Record path cost** is RV32 instructions retired per `acmp_rx` call. QEMU `virt` runs with
`-icount shift=0`, so `minstret` counts exactly one per instruction; two back-to-back reads
differ by 1. Configuration: 16 sinks, 16 sources, 1 interface, stub ports. Harness:
`measure/measure.c` and `measure/build.sh`, outside the repository. These are instruction
counts, not cycles: cycles on a given core add its pipeline and memory waits.

| Step | Gate Release (rv32i -O3): main | lane | Split flags (rv32im -Os): main | lane |
|---|---:|---:|---:|---:|
| **Worst `acmp_rx` step measured**: BIND_RX behind 6 owed (response and probe copied) | **7882** | **7899** (+17) | **24374** | **24381** (+7) |
| BIND_RX sent directly | 7397 | 7414 | 23789 | 23796 |
| BIND_RX behind 7 owed (probe lost, as on main) | 7626 | 7643 | 23760 | 23767 |
| GET_RX_STATE sent directly | 6250 | 6269 | 19758 | 19763 |
| GET_RX_STATE behind 7 owed (copied) | 6621 | 6640 | 20384 | 20389 |
| **A command behind the full owed set** | 5408 (dropped, then a full `finish` pass) | **197** (declined) | 16522 | **344** |
| PROBE_TX behind the full owed set | 5404 | 195 | 16518 | 340 |
| PROBE_TX sent directly | 6445 | 6464 | 20255 | 20262 |
| `acmp_poll`, one owed frame | 5436 | 5436 | 16454 | 16454 |
| `acmp_rx_ready` | n/a | 9 | n/a | 9 |

Measurement binaries (sha256):

| Build | main | lane |
|---|---|---|
| Release (rv32i -O3) | 687241ce7280550bfc0438b1a94615a1f7ddba32fc393a168f81163bb90e5aa5 | 54bc99ab00b5eb06cbf1e5eb05c217b01e285f62081744aec8a5595d40e5a51a |
| Split flags (rv32im -Os) | e9ee7908fbfa3b388eeaeb1ade6e014a988707b552905f75585cda4f93a88320 | ce7bd1448fba8d01ba13ec267ff84800d3f820024ca51a56863e75e583c85394 |

Raw outputs: `measure/*-result.txt`.

## Acceptance items (issue #26)

| Item | Status | Evidence |
|---|---|---|
| Past the bound the entity still answers every command, either queued or refused, never silently dropped; bound and behaviour stated in the docs | Met in the core, given a port that follows the contract | `docs/PORTING.md:74-91`, ACMP-12. A port that ignores the return value still loses the command. |
| A test fills the owed set with the egress held, sends a further command, and it is answered within its timeout after the egress returns | Met | `AcmpOwed.HeldEgressDefersTheCommandBehindTheOwedSet`: 69 ms ≤ 200 ms. The other six command types are covered by the talker, unbind and A19 tests. RV32 smoke covers the same path. |
| A planted mutant restoring the silent drop is caught | Met | `owed-*-drop-restored` (7 per-command, 2 generic), all CAUGHT; each per-command plant escapes without its test. |
| milan-fpga's harness row "an ACMP command behind the owed input" gets an answer time | **Not met here** | Needs milan-fpga to bind `ctrl_loop_set_rx_ready(l, MBX_CH_ACMP, ...)` to `acmp_rx_ready` (or keep declined frames), and the harness measured again. Out of scope for this repository and lane. Its `acmp_mutants.py` room fragment also names `busy_drops` and needs updating when it adopts. |

Hence the PR says "Relates to #26".

## Environment notes

- The pinned `$VALIDATION_TOOLS/clang-18/bin/clang-18` wrapper points at a deleted scratch
  path. A scratch-local wrapper runs the same Clang 18.1.3 install from
  `$VALIDATION_TOOLS/clang-18/root`.
- The host's clang-tidy 23 enables `clang-analyzer-optin.performance.Padding`, which flags
  `struct acmp_sink` on main and fails `static-analysis` there. CI (ubuntu-24.04) installs
  clang-tidy 18. Ubuntu's `clang-tidy-18_18.1.3-1ubuntu1_amd64.deb` (sha256
  4880055c77877bce65de8733f0931021a28826bbae3f450b4dc0065fb6b70363) was unpacked in scratch
  and run against the pinned libLLVM 18. main and the lane both pass with it.
- No Mermaid CLI on the host. Node 22.11.0 (checksum verified) and
  `@mermaid-js/mermaid-cli@11.16.0`, the CI pin, were installed in scratch only.
- Scratch: `$VALIDATION_STORAGE/tsn26-a750/`. Nothing large is in this directory.
- Memory stayed under 9 GB (`--jobs 8`); peak observed was about 10.7 GB including page
  cache, during the first baseline at `--jobs 16`.
