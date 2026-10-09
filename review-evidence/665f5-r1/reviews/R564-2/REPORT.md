[R564] NEGATIVE - exact head 0ded1f269a44d107498f177c8276665656e07d30

# R564-2: internal independent review of PR #700, round 2 (issue #665, lane F5, AECP on the bare-metal core)

- **Reviewed head:** `0ded1f269a44d107498f177c8276665656e07d30`, tree `634c2f44c08cc5f976ca74634daec54273de66b4`.
- **Round delta:** `1e68d1b62ef2facdf0e8dbad28a202297d433c61..0ded1f26`, 11 commits and 18 files. The full PR diff from `5603c353137e90c1fa95429f6d00ef7a2298d9ee` was checked for scope.
- **Verdict: NEGATIVE.** One MINOR finding is open (R564-2-F1), under Conformance, Tests and Docs.
- **Prior findings:** every finding from R565-1 and R564-1 is RESOLVED at this head. R564-1's residue item is resolved too.
- **Lenses:** RTL and Robustness are covered clean in this round.
- **Other items:** three suggestions and one residue item are recorded below.

## Reconstruction

I read the following in the required order:

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.md.
3. The issue #665 body.
4. The F5 assignment (6081266905), the 224 KB budget ruling (6081705916) and the round-2 assignment (6085423196).
5. REVIEW READY round 2 (6086042169).
6. The linked authorities: NFR-SCOUT-02/03/08 and `docs/design/MAILBOX_SPLIT.md`.
7. The interface authorities: `aecp.h`, `aecp_mbx.h` and `aecp_state.h`.
8. The raw delta and its commit history.

I wrote my own pass over the delta, including the plants and probes I designed, before reading the prior public findings on PR #700 (R565-1 6085319671 and R564-1 6085414859). I did not use any private author material, lane scratchpad or other reviewer's report from this round.

The standards are the oracle and the fabric is a differential. Clause wording is taken from the assignment, the prior public findings and the processor's in-tree commentary, for example `protocol-processor/hdl/aecp/KL_aecp_engine.sv:1256-1273` on 9.7.4 and Table 9-1. The standards text itself was not available in this environment; see the limits.

## Finding

### R564-2-F1 — MINOR — Conformance, Tests, Docs — SET_STREAM_INFO with no sub-command: latency behaviour is untestable by the suite and contradicted by the oracle and README

**Artifacts**

- `sw/firmware/ctrl/test/test_aecp.cpp:793-795`, in `Core.SetStreamInfoReportsCurrentFieldsOnSuccessAndRefusal`.
- `sw/firmware/ctrl/test/aecp_wire_oracle.py:103`.
- `sw/firmware/ctrl/aecp/README.md:153`.
- `sw/firmware/ctrl/aecp/aecp_commands.c:333-336`.

**Evidence**

The no-sub-command and ignored-flag loop (flags 0, 4, 8, 12 and others) sends a request whose `msrp_accumulated_latency` is 123456. That is the same value the preceding SET stored. So the assertion `"ignored flags and no subcommand preserve latency"` and the response-latency check cannot tell the stored value from the requested one.

Two reviewer plants in a disposable copy confirm this (`receipts/review-mutants/`). The complete composed AECP suite ran at two interfaces, 69 tests, rc 0, for each plant:

| Plant | What it does | Result |
|---|---|---|
| `nosub-applies-request-latency` | On a SET with no sub-command, writes the request latency into the persistent store and marks the saved override | Escapes all 69 tests |
| `nosub-reports-request-latency` | The no-sub-command response reports the request latency | Escapes all 69 tests |

The three control plants in the same run were caught: `saved-state-refused`, `unavailable-event-dropped` and `init-guard-after-memset`.

The artifacts also disagree on what this path should report:

- **Core:** reports the current latency. Probe Q2 stores 111 and sends 999; the response carries 111 and the stored value stays 111 (`receipts/probes-r564-2.log`).
- **Wire oracle:** expects the *requested* latency on every successful SET, flags 0 included (`aecp_wire_oracle.py:103`).
- **README:** states "Milan 5.4.2.9 retains requested latency on success" with no exception for this case.

The differential passes only because its stored and requested values coincide (67890).

**Authority**

- IEEE 1722.1-2021 7.4.15.1: SAVED_STATE and STREAMING_WAIT are ignored; XXX_VALID flags select what is set.
- Milan v1.2 5.4.2.9: requested-latency echo, and MSRP_ACC_LAT_VALID as in the command.
- The round-2 assignment item 2 asks for "clause-based assertions with nonzero current state … plus planted request-echo defects".
- AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect."

**Impact**

A regression that applies an un-requested latency would go undetected by every native and wire check. That regression would create a persistent saved override and change the presentation offset the framers stamp. The decided wire behaviour for this path is also unrecorded, and the shipped documents disagree with each other. The current code behaves under the current-field reading, so this is a MINOR, not a defect in the shipped behaviour.

**Required outcome**

1. Decide by clause what a successful SET_STREAM_INFO without MSRP_ACC_LAT_VALID reports in `msrp_accumulated_latency`: the current value or the command's value.
2. Make the core, the oracle and the README state the same rule.
3. Assert it natively and in the differential with a request latency different from the stored latency. Also assert that the stored latency, the override bit and the change notifications are untouched.
4. Add a plant that applies or echoes the request latency on this path.

**Verification**

- Both reviewer plants are caught by named assertions.
- Probe Q2 passes, or is replaced by the decided rule.
- The oracle's latency expectation for the flags-0 row distinguishes current from requested.

## Prior findings at this head

Each finding is judged under its original severity against the standard.

| Prior finding | Status | Evidence at `0ded1f26` |
|---|---|---|
| R565-1-F1 MAJOR / R564-1-F1 MINOR: root READ_DESCRIPTOR configuration_index | **RESOLVED** | See note 1. |
| R565-1-F2 MAJOR: SET_STREAM_INFO echoes request | **RESOLVED** | See note 2. |
| R564-1-F2 MINOR: SAVED_STATE/STREAMING_WAIT and no-sub-command refused | **RESOLVED** in behaviour | See note 3. |
| R565-1-F3 MAJOR / R564-1-F5 MINOR: unavailable snapshot head-of-line blocking and busy loop | **RESOLVED** | See note 4. |
| R565-1-F4 MINOR: callback guard across instances | **RESOLVED** | See note 5. |
| R564-1-F3 MINOR: non-AEM message types | **RESOLVED** | See note 6. |
| R564-1-F4 MINOR: ENTITY available_index | **RESOLVED** | See note 7. |
| Item 7: linked image under 224 KB | **RESOLVED** | See note 8. |
| R564-1 RES1: MAILBOX_SPLIT wording | **RESOLVED** | `docs/design/MAILBOX_SPLIT.md:568` now names the F5 application bridge. |
| R564-1 S1-S3: suggestions | Unchanged, optional | Not required and not counted. |

**1. Root READ_DESCRIPTOR configuration_index.**

- `aecp_commands.c:84-89` forces configuration 0 and response bytes 0 for ENTITY and CONFIGURATION. Descriptor-index validation and the other types' configuration check are kept.
- `Core.RootDescriptorConfigurationIsIgnored` (`test_aecp.cpp:565`) covers indices 1 and 65535, an invalid root index, and STREAM_INPUT with cfg 1 still BAD_ARGUMENTS.
- Plant `root-configuration-refused` is caught.
- The R565-1 probe and R564-1 P1 pass. Probe Q3 shows CONFIGURATION index 1 → NO_SUCH_DESCRIPTOR with cfg 0.
- The wire differences are recorded as "IEEE 7.4.5.1/2: ignored root configuration", 4 per ingress.

**2. SET_STREAM_INFO current fields.**

- `aecp_commands.c:300-317` forms format, stream_id, destination MAC, VLAN and flags from current state on success and on refusal. The requested latency is echoed on MSRP_ACC_LAT_VALID success (`:346-347`).
- The new test uses nonzero current state over success, every unsupported VALID sub-command, BAD_ARGUMENTS, STREAM_IS_RUNNING, ENTITY_LOCKED and STREAM_INPUT.
- Plants `stream-info-request-echo`, `stream-info-flags-echo` and `stream-info-noop-refused` are caught.
- The R565-1 probe passes.
- The no-sub-command latency path is weak; see R564-2-F1. That finding is new evidence against this round's tests, not a retained part of F2.

**3. SAVED_STATE, STREAMING_WAIT and no sub-command.**

- `aecp_commands.c:329-336`: mask `0xdaf80000` refuses only the VALID sub-commands other than MSRP_ACC_LAT. Flags 0, 4, 8 and 12 succeed.
- R564-1 P2 passes for all four flag sets.
- Plant `stream-info-noop-refused` and the control plant `saved-state-refused` are both caught.
- R564-2-F1 covers the latency-evidence gap on this path.

**4. Unavailable snapshot blocking.**

- `aecp.c:461-497`: a failed snapshot keeps its pending bit, sets `retry_pending` and `retry_at = now + 1` (`:495`), and the scan continues to other descriptors.
- `arm()` (`aecp.c:96-105`) arms the timer for the earliest retry and suppresses the counter deadline while a counter retry is pending.
- `Core.UnavailableSnapshotsDoNotBlockIndependentNoticesOrSpin` (`test_aecp.cpp:985`) covers progress past failures, two-interface fanout, backpressure, sleep, timed retry, recovery, counter spacing and clock wrap. `Core.CounterTimerArmsOnlyEligibleCompletedSnapshots` covers timer priority.
- Plants `unavailable-head-blocks-notices`, `unavailable-retry-spins` and `retry-timer-lost` are caught. The reviewer plant `unavailable-event-dropped` is caught.
- R565-1 probe 3 and R564-1 P6 pass: 1 AVB and 1 clock-domain notice, 2 busy polls out of 100.
- Probe Q1 shows the retry is paced by the timer: 1000 port reads in 1000 ms at 5 polls per ms, with 0 busy polls. See S1.

**5. Callback guard across instances.**

- `aecp.c:5-30` adds a single `port_owner` shared by all instances. All 15 core and saved-state public inputs refuse entry while any instance is inside a port, enumerated in `aecp_callback_inputs.hpp`. `aecp_init` checks before its memset and charges the active caller.
- `Core.CrossInstanceInputsAreRefusedInsideRealCallbacks` (`test_aecp.cpp:580`) exercises a real Changed callback and checks the refusal count and that destination state is byte-identical. `AecpDebug.EveryInputRejectsSynchronousPortDelivery` runs 15 EXPECT_EXIT cases from a real `now_ms` port with `CTRL_REENTRY_ASSERT`.
- Plant `cross-instance-guard-removed` and the reviewer plant `init-guard-after-memset` are caught.
- The R565-1 probe passes. Q5 confirms the lock query refuses without writing `*owner`.
- The README documents the scope (`README.md:58-63`). Adapter entry points are outside that scope; see S2.

**6. Non-AEM message types.**

- `aecp.c:282-316`:
  - HDCP_APM_COMMAND (8) is answered with HDCP_APM_RESPONSE / NOT_IMPLEMENTED, length 0, and the flags byte and fragment offset preserved. A PDU shorter than its 28-byte fixed header counts as malformed.
  - AA (2) and AV/C (4) are answered with NOT_IMPLEMENTED and the body echoed.
  - Types 10, 12 and 14 and unsolicited responses are ignored.
- Each decision is recorded by clause, with its reference wire difference, in `README.md:99-112`. This matches the processor's own record that 10..13 and 14 have no PDU format (`KL_aecp_engine.sv:1256-1266`).
- `Core.NonAemMessageTypesFollowTheirOwnContracts` (`test_aecp.cpp:1267`) covers both interfaces, stalls and the fixed header. A latency case checks the 9.7.2.7 15 ms deadline (`:1521`).
- Plant `hdcp-data-length-echo` is caught.
- R564-1 P3 passes: types 2, 4 and 8 are answered and 14 is ignored. Q4 shows the minimum 28-byte HDCP PDU is answered.

**7. ENTITY available_index.**

- The new port `aecp_ports.available_index` (`aecp.h:98`) is read on READ_DESCRIPTOR(ENTITY) for the ingress interface (`aecp_commands.c:101-106`).
- The application reads the composed ADP owner's per-interface value (`ctrl_app_aecp.c:105-109`). The image bytes are not mutated.
- `App.EntityReadSeesTheRealAdpAdvertisementCount` (`test_aecp.cpp:388`) sends N real advertisements per interface, then reads N. `Core.EntityAvailableIndexUsesTheIngressObservation` (`:1257`) checks the core path.
- Plant `entity-available-index-static` is caught by both tests.

**8. Linked image.**

The author's figures are 140400 / 153056 / 194224 / 221728 B. I relinked independently; see "Linked image".

## Linked image

I linked the opt-in AECP size fixture (`ctrl_srp_image.py --with-aecp`) myself at both the round-1 and round-2 heads, for all four shape and interface points.

- **SDK:** the CI-pinned SDK, tarball SHA-256 `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f` per `.github/workflows/rtl-fast.yml:270`, extracted to scratch.
- **Runtime:** a reviewer stub with byte-loop memory primitives and shift/subtract integer helpers (`sizeprobe/stub_runtime.c`), identical across heads. Picolibc and compiler-rt sources were not available.
- **Receipts:** `receipts/sizes/` and `scripts/run_sizes.sh`.

| Shape / interfaces | Reviewer span, round 1 → round 2 | Author round 2 | Delta, reviewer / author | Nominal RAMB36 tiles (4608 B) | Tiles with 32-bit packing (4096 B) |
|---|---|---:|---|---:|---:|
| 1x1_tdm8 / 1 | 137920 → 139264 | 140400 | +1344 / +1328 | 31 | 35 |
| 1x1_tdm8 / 2 | 150592 → 151904 | 153056 | +1312 / +1328 | 34 | 38 |
| 8x8 / 1 | 191088 → 193088 | 194224 | +2000 / +1984 | 43 | 48 |
| 8x8 / 2 | 218592 → 220592 | 221728 | +2000 / +1984 | 49 | 55 |

- **Sections:** my rodata, data and bss equal the author's round-1 table exactly. Text differs only by the runtime, about 1.14 KB.
- **Round-2 growth:** text +984 B. BSS +344 B for the shipping shape and +1000 B for the largest, which is 8 B per descriptor event for the new `retry_at` and `retry_pending` fields.
- **Deltas:** they agree with the author's within link alignment (±16 B).
- **Threshold:** the largest shape with two interfaces is below 224000 B (margin 2272 B) and below 224 KiB (margin 7648 B).
- **Tiles:** the 32-bit-packed tile count (55) exceeds the "about 50" in the ruling. The ruling's threshold is in bytes, so this is a pending owner-visibility item, not a finding.

## Suggestions (non-blocking)

- **S1 (Robustness, RTL).** A permanently absent observer with a pending event is retried every 1 ms for as long as it is absent: 1000 port reads and timer re-arms per second (probe Q1). This is timer-paced, meets "no unbounded busy loop", and keeps the event. A capped back-off would reduce steady-state load, for example doubling to the 1 s counter spacing. `aecp.c:495`.
- **S2 (Robustness).** The adapter entry points are not covered by the 15-input guard:
  - `aecp_mbx_init` clears `m` before the core's guard runs (`aecp_mbx.c:103`).
  - The adapter poll dequeues a completion even when `aecp_tx_complete` is refused (`aecp_mbx.c:150-152`). In a release build, a forbidden re-entrant loop service would leave that counter event `awaiting_output`.
  - This matches the merged ADP and ACMP adapters (`adp_mbx.c:59`, `acmp_mbx.c:68`) and is outside the stated contract. Either guard the adapter or state in the README that the guard is core-scoped.
- **S3 (Conformance).** For a STREAM_OUTPUT, the SET response clears MSRP_FAILURE_VALID as "input-only" (`aecp_commands.c:305`). GET_STREAM_INFO for the same output passes the observer's flags through unchanged. No in-tree observer sets it for outputs. Apply one rule to both, consistent with Milan Tables 5.11/5.12.

## Residue (wording only)

- **RES1.** The PR #700 body "Status" section says "Local implementation head `0ded1f26…` … This local head is unpushed; PR #700 remains at the round 1 head." The PR head is now `0ded1f269a44d107498f177c8276665656e07d30` (`receipts/pr700-body-snapshot.md`). Exact fix: replace that sentence with "Implementation head `0ded1f269a44d107498f177c8276665656e07d30` is the published PR head."

## Executed evidence

All runs used a disposable exact-head clone under scratch: `receipts/gate-tree-integrity.txt` shows 1269 entries byte-exact and status empty. The submodules were gPTP `5dce647a`, processor `2ad2f845`, lwSRP `9197193e` and verilog-axis `48ff7a7e`. A separate checkout of processor `c9f74b68` served as the two-interface reference. The scoped simulator was identified before use as `Verilator 5.050 2026-07-01 rev v5.050` (`receipts/verilator-version.txt`).

Receipt paths are relative to `receipts/`.

| Gate | Result | Receipt |
|---|---|---|
| `test_ctrl_firmware.py --require-rv32 --jobs 4` (firmware bank: every arm, AECP app at 1 and 2 interfaces, five image arms, debug guard, RV32 with the CI-pinned SDK) | rc 0; 59 arms `[ok]`, 0 failures; AECP 69/69 at each interface count; debug 1/1 | `bank.log` |
| `aecp_mutants.py`, 3 shards (complete plant table) | rc 0 each; 69/69 plants caught, including all 10 new plants | `aecp-mutants/*.json` |
| Reviewer plants (5), `scripts/run_review_mutants.py` | 3 caught; 2 escape (F1) | `review-mutants/` |
| R565-1 `probe_cases.cpp`, unchanged (SHA-256 matches its manifest) | 4/4 pass, rc 0 | `probes-r565-1.log` |
| R564-1 P1-P6, unchanged sources, on the full exact-head suite | P1, P2, P3 and P6 pass; P4 and P5 are informational; rc 0 | `probes-r564-1-full.log` |
| R564-1's original fixture-cut harness | Setup failure, not a probe failure; see note below | `probes-r564-1-fixture-cut-setup-failed.log` |
| Reviewer probes Q1-Q5 (`probes/r564-2_probes.cpp`), at 1 and 2 interfaces | 5/5 pass at each | `probes-r564-2.log` |
| Wire differential, 1 interface, `2ad2f845` | rc 0; 132 observations, 31 commands, 17 notifications, 42 descriptors, 6 controls | `wire-if1.log`, `wire/` |
| Wire differential, 2 interfaces, `c9f74b68` | rc 0; 137 on each ingress, 6 controls each | `wire-if2.log`, `wire/` |
| `fw_coverage.py --check --lwsrp third_party/lwSRP` | rc 0; 30 files; all eight AECP/app units at 100% lines and branches; no new exclusion in the delta | `coverage-check.log` |
| `aecp_arms.py --app --asan`, 1 and 2 interfaces | rc 0; 69/69 each | `asan-app-if*.log` |
| `make -C tb/verilator/mbx -j4` (pinned simulator) | rc 0; host model 369 checks; mailbox plants 5 of 5 caught | `mbx-make.log`, with the simulator install root redacted |
| `gen_mailbox.py --check` | rc 0; 0 findings | `gen-mailbox-check.log` |
| `docs_check.py` | rc 0; 0 findings | `docs-check.log` |
| Independent relink at both heads, four points each | 8/8 rc 0 | `sizes.log`, `sizes/` |
| Review-clone integrity after all work | 1269 entries byte- and mode-exact; index equals tree; status empty; gitlinks unchanged | `clone-integrity.txt` |

**Fixture-cut note.** R564-1's original harness keeps only the fixture lines of `test_aecp.cpp`. At this head that cut includes the new `aecp_callback_inputs.hpp`, whose static helper is unused there and fails `-Werror`. This is a harness boundary failure, not a probe failure. The same unchanged probe sources pass when appended to the full suite.

**Scope.** The full PR diff touches no `hdl/`, `syn/`, `configs/`, `tb/`, `sw/mailbox/` or submodule path. The default build and the shipping image are unchanged.

**Hosted checks at the exact head**, two snapshots (`hosted-check*-1/2`, all rows on `0ded1f26`):

- Completed successfully: bdd-conformance, changes, docs-check, docs-check-no-git, full-ci-gate, verilator-lint, wire-accountability, yosys-elaboration, Yosys shards 0-3 and Verilator shard 3/5.
- Still in progress at the second snapshot: elaborate, firmware-unit and Verilator shards 0, 1, 2 and 4.
- Skipped, not executed: Physical gPTP (nightly and manual).

No hosted acceptance is claimed.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R564-2-F1) | See note C. | R564-2 | 0ded1f269a44d107498f177c8276665656e07d30 |
| RTL | CLEAN | See note R. | R564-2 | 0ded1f269a44d107498f177c8276665656e07d30 |
| Robustness | CLEAN | See note B. | R564-2 | 0ded1f269a44d107498f177c8276665656e07d30 |
| Tests | UNCLEAN (R564-2-F1) | See note T. | R564-2 | 0ded1f269a44d107498f177c8276665656e07d30 |
| Docs | UNCLEAN (R564-2-F1) | See note D. | R564-2 | 0ded1f269a44d107498f177c8276665656e07d30 |

**C (Conformance).**

- `aecp_commands.c:72-110` and `:281-353`; `aecp.c:255-333`, `:423-499`.
- Checked against the IEEE 7.4.5.1/2, 7.4.15.1, 9.7.4, Table 9-1 and Milan 5.4.2.9 / Table 5.22 requirements as stated in the assignment and the prior public findings.
- Wire verdicts in `receipts/wire/`; probes P1-P6, R565 and Q1-Q5.

**R (RTL: architecture, widths, error paths, backpressure).**

- `aecp.c:5-30`: guard state.
- `aecp.c:81-110`: timer arbitration including the retry deadline and wrap.
- `aecp.c:282-316`: bounds of the non-AEM bodies within `response[1514]`.
- `aecp.h:97-117`: the new port and the event fields.
- `aecp_mbx.c` and `ctrl_app_aecp.c:105-109`: interface index bounded by `aecp_mbx_init`.
- `mbx-make.log`, 8 independent links, no RTL in diff.
- Adapter observation recorded as S2.

**B (Robustness).**

- Malformed and short HDCP (`aecp.c:287-290`; Q4).
- Unavailable and recovering observers, backpressure and clock wrap (`test_aecp.cpp:985-1019`; Q1; P6).
- Re-entry from real callbacks across instances (`aecp_callback_inputs.hpp`; Q5; reviewer plant `init-guard-after-memset`).
- Invalid root indices (Q3).
- ASAN arms.
- Suggestions S1 and S2 recorded.

**T (Tests).**

- `test_aecp.cpp` delta (`:388-413`, `:565-599`, `:778-799`, `:985-1019`, `:1193-1202`, `:1257-1301`, `:1516-1523`).
- `test_aecp_debug.cpp`, `aecp_mutants.py` (69 plants) and the wire driver, model and oracle.
- 5 reviewer plants; `coverage.ratchet` and the coverage run.

**D (Docs).**

- `sw/firmware/ctrl/aecp/README.md` delta (`:10-35`, `:58-68`, `:99-112`, `:152-165`) and `docs/design/MAILBOX_SPLIT.md:568`.
- The PR #700 body snapshot, REVIEW READY 6086042169, and `docs_check.py`.

R564-2-F1 is the only open item. RTL and Robustness bank clean at this head. A fix to F1 that touches only tests, the oracle and the README leaves those two lenses' scope unchanged. Any change to `aecp_commands.c` would un-cover them.

## Real limits

- **Standards text.** The IEEE 1722.1-2021 and Milan v1.2 text was not available in this environment. Clause content is taken from the assignment, the prior public findings, which quote it, and the processor's in-tree commentary. Three points are therefore not independently verified:
  - The exact HDCP APM field layout. The response keeps byte 24 and the fragment offset and zeroes byte 25.
  - The disposition of EXTENDED_COMMAND (14).
  - Which latency a no-sub-command SET should report (the decision F1 asks to record).
- **Relink.** The relink used a reviewer stub runtime, so absolute spans differ from the author's by the runtime text, about 1.14 KB. Agreement is shown on rodata, data and bss, and on round-to-round deltas, not byte-for-byte on the final span.
- **Count reconciliation.** I did not reconcile the author's "1406 checks / 65 tallies" figure with my bank log's tally format; the bank rc and arm verdicts are the evidence used.
- **Not run:** the builder bank, the saved-state bank, the inherited control/SRP/saved-state mutation tables, the firmware bank `--self-test`, act or the local replica, hosted acceptance, and any hardware. Physical calibration is **NOT RUN**, and field skips are not hardware proof.
- **Latency.** The latency and service figures were not re-derived beyond the bank's passing Latency tests. They remain desk bounds.

## Reproduction

Use an exact-head clone with initialized submodules as `TREE` and this packet as `PACKET`. Set `MILAN_RV32_CC` to the CI-pinned SDK's `riscv32-linux-gcc`.

- **Probes:** `python3 -B $PACKET/scripts/run_probes.py $TREE $PACKET r565-1|r564-1-full|r564-2`.
- **Reviewer plants:** `python3 -B $PACKET/scripts/run_review_mutants.py $TREE $PACKET`.
- **Relink:** `$PACKET/scripts/run_sizes.sh $PACKET`. This expects `scratch/tree`, `scratch/tree-r1` and the stub archives built from `sizeprobe/stub_runtime.c` with `-march=rv32i -mabi=ilp32 -Os -ffreestanding -fno-builtin -fno-stack-protector`.
- **Integrity:** `python3 -I $PACKET/scripts/verify_clone.py <clone> 0ded1f269a44d107498f177c8276665656e07d30`.
- **Gates:** started with `scripts/launch.sh` and joined with `scripts/wait_jobs.sh`. The exact command line heads each receipt log.

## Pending manager duties

- Publish this report and manifest, and carry RES1 to the residue checklist.
- Hosted acceptance at the exact head, distinguishing executed from skipped contexts. At capture: elaborate, firmware-unit and four Verilator shards were in progress, and physical gPTP was skipped.
- Validate the current-dev merge candidate at the merge turn: builder and native banks, plus act. Source base and live dev are both `5603c353137e90c1fa95429f6d00ef7a2298d9ee`. No manager source bank ran at this head, and none is claimed or inferred.
- Owner visibility: the largest shape with two interfaces needs 49 nominal RAMB36 tiles but 55 with 32-bit packing, against the "about 50" in ruling 6081705916. Routed fit and the 10% reserve are owed before the default flip.
- Processor #73 adoption, physical observer wiring, target timing and stack calibration remain the stated later obligations.
- Re-review after R564-2-F1 is answered. No review round may remain in flight before merge, and merge needs explicit maintainer authorization.

R564-2 FINISHED
