[R564] NEGATIVE - exact head fb9c57d2ae3484804ff90f67feb57bf420c93dfa

# R564-3: internal independent review of PR #700, round 3 (issue #665, lane F5, AECP on the bare-metal core)

- **Reviewed head:** `fb9c57d2ae3484804ff90f67feb57bf420c93dfa`, tree `762bda168ec58bfdd05f1c9394fea28b0696b9a5`. This is the published PR head (`gh pr view 700`, re-checked at the end of the round).
- **Round delta:** `0ded1f269a44d107498f177c8276665656e07d30..fb9c57d2`, two commits, six files, all tests or prose: `aecp/README.md`, `test/aecp_mutants.py`, `test/aecp_wire.cpp`, `test/aecp_wire.py`, `test/aecp_wire_oracle.py` and `test/test_aecp.cpp`. No production C, RTL, configuration, mailbox contract or submodule pin changed (`receipts/scope-and-size-inputs.txt`).
- **R564-2-F1 is RESOLVED.** All five assigned items are met and verified by execution (see "R564-2-F1 at this head").
- **Verdict: NEGATIVE** on one new MINOR, R564-3-F1, under Tests. The no-sub-command path is now successful, and two Milan 5.4.2.9 "shall" refusals on it are pinned by no test. Plants that bypass them escape all 70 tests at both interface counts. The code at this head is correct: reviewer probes pass. The fix is test-only.
- **Prior findings:** every R565-1, R564-1 and R564-2 finding is resolved at this head. R564-2's residue item is resolved. A new residue item about the same PR-body sentence is recorded as R564-3-RES1.
- **Lenses:** Conformance, RTL, Robustness and Docs are covered clean at this head. Tests is unclean (R564-3-F1).

## Reconstruction

I read the following in the required order:

1. AGENTS.md (CONTRIBUTING.md is cited by it for workflow).
2. The docs/README map.
3. The issue #665 body.
4. The F5 assignment (6081266905), the 224 KB ruling (6081705916) and the round-3 assignment (6086491737).
5. REVIEW READY round 3 (6086832557).
6. The clause text, from the standards documents available in this environment:
   - Milan v1.2 5.4.2.9;
   - IEEE 1722.1-2021 7.4.15.1, 7.4.15.2 and Table 7-145.
7. The core `aecp_commands.c:281-353`, the raw delta and its history.
8. The executable evidence.

My own pass over the delta, my plants and my probes came before I read the prior public findings on PR #700 (R564-2, 6086483772, and the earlier rounds). After that pass, I re-ran R564-2's published plant driver and Q1-Q5 probes unchanged. I verified their SHA-256 against R564-2's manifest. I used no private author material, lane scratchpad or other reviewer's report from this round.

**Clause check (verified against the standards text this round).** Milan v1.2 5.4.2.9 reads: "In a successful response, the PAAD-AE shall set the MSRP_ACC_LAT_VALID flag to the same value as in the command, and when the flag is set, the returned msrp_accumulated_latency is the same value as in the command."

IEEE 7.4.15.1 says the response's `msrp_accumulated_latency` "is set to the accumulated_latency of the stream's MSRP Talker Advertise", which is the current value. It also says SAVED_STATE and STREAMING_WAIT "are ignored in the command".

So the decided rule is the clause rule:

- with MSRP_ACC_LAT_VALID clear, a success reports the current latency with the flag clear;
- with the flag set, a success echoes the request.

The same clause also requires:

- "shall not implement the SET_STREAM_INFO command on Stream Inputs (NOT_SUPPORTED shall be returned)";
- "If the Stream Output is streaming then the PAAD-AE shall refuse the command with the STREAM_IS_RUNNING error code."

Neither requirement is conditional on a sub-command. IEEE 7.4.15.2 restates the streaming and lock restrictions. The Table 7-145 bit assignment confirms the refusal mask `0xdaf80000` (`aecp_commands.c:330`). It covers FORMAT, ID, DEST_MAC, FAILURE, VLAN and the five IP sub-commands. It leaves out the response-only CONNECTED and NOT_REGISTERING_SRP flags, and MSRP_ACC_LAT.

## R564-2-F1 at this head: RESOLVED

| Item (assignment 6086491737) | Status | Evidence |
|---|---|---|
| 1. The native no-sub-command and ignored-flag loop sends a request latency different from the stored one, and asserts that the response carries the stored value and the store is unchanged. | Met | See item 1 below. |
| 2. The oracle expects the current latency when MSRP_ACC_LAT_VALID is clear and the requested latency only when it is set, with distinct stored and requested values in the differential. | Met | See item 2 below. |
| 3. The README states the exception. | Met | `sw/firmware/ctrl/aecp/README.md:154` states it under IEEE 7.4.15.1 and Milan 5.4.2.9: echo only when MSRP_ACC_LAT_VALID is set; otherwise current latency, with stored latency, saved override and notifications unchanged. `README.md:146-149` counts the seven controls. Both are accurate against the code and the oracle. |
| 4. R564-2's plants `nosub-applies-request-latency` and `nosub-reports-request-latency` are killed by named tests. | Met | See item 4 below. |
| 5. The core is unchanged, and the linked image stays at 221,728 B under 224 KB. | Met | See item 5 below. |

**1. Native loop.**

- `test_aecp.cpp:794-796` sends 765432 against stored 123456 for flags 0, 4, 8 and 12.
- `Core.SetStreamInfoWithoutSubcommandPreservesState` (`test_aecp.cpp:810-838`) runs flags 0/4/8/12 twice: once on the observed latency (12345, not overridden) and once after a saved override (123456). It asserts:
  - the response latency equals the current value, not 765432;
  - MSRP_ACC_LAT_VALID is clear in the response;
  - the whole latency store is unchanged;
  - the override bit is unchanged;
  - the Changed callback is silent;
  - no notice is sent to a registered peer.
- Verified by the plants in item 4.

**2. Oracle and differential.**

- `aecp_wire_oracle.py:103-107`:
  - expects the request latency only for `status == 0 && MSRP_ACC_LAT_VALID`, otherwise 67890;
  - self-checks that a no-sub-command stimulus differs from 67890.
- `aecp_wire.cpp:58-61` sends 765432 on the no-sub-command row.
- The seventh control (`aecp_wire_oracle.py:190-215`) plants a request echo and requires the exact diagnosis.
- Fresh runs:
  - one interface, reference `2ad2f845`: rc 0, 132 observations, 7 controls;
  - two interfaces, reference `c9f74b68`: rc 0, 274 observations, 7 controls per ingress.
- Reviewer oracle probes on all three ingress logs: 21/21 behave as required (`receipts/oracle-*.log`, `oracle-probes-*.json`):
  - the head oracle accepts;
  - **the pre-round-3 rule now rejects the core's correct output** with "SET requested or current latency", so the stimulus distinguishes current from requested;
  - a request echo on the no-sub-command row is rejected;
  - an off-by-one latency on the no-sub-command row is rejected;
  - a set MSRP_ACC_LAT_VALID on the no-sub-command row is rejected ("SET response validity");
  - a missing echo on a sub-command success is rejected;
  - a no-sub-command stimulus equal to the stored value trips the stimulus self-check.
- The census shows 7 SET rows and 1 no-sub-command row per ingress, request 765432 and core reply 67890.

**4. Named plants.**

- R564-2's published driver, re-run unchanged (SHA-256 `9a671047…` matches its manifest; `receipts/r564-2-plants-rerun.log`): all 5 plants are caught. Both former escapes now fail `Core.SetStreamInfoReportsCurrentFieldsOnSuccessAndRefusal` and `Core.SetStreamInfoWithoutSubcommandPreservesState`. The three controls are caught.
- The maintained table (`aecp_mutants.py`, 2 shards): 72/72 caught, including `nosub-applies-request-latency`, `nosub-reports-request-latency` and `nosub-notifies-change`. The table's own grader requires the named diagnostic in a completed run.
- My plants X1-X6, run against the complete suite at 1 and 2 interfaces: 12/12 killed with the expected diagnostic in the expected test (`receipts/plants.log`). They are:
  - the two R564-2 texts;
  - a set MSRP_ACC_LAT_VALID on the no-sub-command response;
  - a store-only write;
  - an override-only mark, which is caught only by the new test;
  - the current latency ignoring the override;
  - the no-sub-command path refused;
  - the sub-command echo dropped.
- Baselines pass 70/70 at both counts.

**5. Core and image.**

- `git diff --name-only 0ded1f26..fb9c57d2` outside `sw/firmware/ctrl/test` and `*.md` is empty.
- No file used by `ctrl_srp_image.py` references the changed files (`receipts/scope-and-size-inputs.txt`). Every linked input is therefore byte-identical to round 2.
- R564-2 relinked round 2 independently. Its stub-runtime figures agree with the author's 140400 / 153056 / 194224 / 221728 B within the runtime text. The largest shape with two interfaces stays at 221,728 B, below 224,000 B with a 2,272 B margin.
- I did not relink this round; see the limits.

## Finding

### R564-3-F1 - MINOR - Tests - `sw/firmware/ctrl/test/test_aecp.cpp:810-838` (no-sub-command SET_STREAM_INFO): the STREAM_INPUT and STREAM_IS_RUNNING refusals are unpinned on the path this PR made successful

**Authority**

- Milan v1.2 5.4.2.9: SET_STREAM_INFO on a Stream Input shall return NOT_SUPPORTED, and a streaming Stream Output shall refuse with STREAM_IS_RUNNING. Neither is conditional on a sub-command.
- IEEE 1722.1-2021 7.4.15.2 restates the streaming restriction.
- AGENTS.md section 6, Tests: "Positive, negative, and boundary behavior is covered."

**Evidence**

- In round 2, a SET with no XXX_VALID sub-command became a success (`aecp_commands.c:333-336`). Its refusals rely only on the guards before it: `type == 5u` at `:318-320`, `info.running` at `:321-323` and the foreign lock at `:324-326`.
- No test sends a no-sub-command SET to a STREAM_INPUT or to a running output:
  - the refusal cases at `test_aecp.cpp:773-775` and `:801-807` all carry MSRP_ACC_LAT_VALID;
  - the dedicated new test `:810-838` covers only success.
- The lock guard is pinned. `Core.ConfigurationAndLockedSetRefusals` (`:890`) sends a flags-0 body under a foreign lock, and reviewer plant X7 is caught there.
- Reviewer plants, each run against the complete composed suite at 1 and 2 interfaces, with all other tests passing:

| Plant | What it does | Result |
|---|---|---|
| X8 `nosub-bypasses-running-only` | A no-sub-command SET to a running output returns SUCCESS. | **Escapes all 70 tests at both interface counts** (`receipts/plants-x8.log`). |
| X9 `nosub-bypasses-input-refusal` | A no-sub-command SET to a STREAM_INPUT returns SUCCESS. | **Escapes all 70 tests at both interface counts** (`receipts/plants-x9.log`). |

- The wire differential has one no-sub-command row, to output 6 while stopped, so it does not reach these cases either.
- The head behaves correctly. Probes `Core.S1_NoSubcommandSetOnRunningOutputIsRefused` and `Core.S2_NoSubcommandSetOnInputIsNotSupported` (`probes/r564-3_probes.cpp`) pass at both counts (`receipts/r564-3-probes-head.log`). S1 fails under X8 and S2 fails under X9 (`receipts/r564-3-probes-x8.log`, `-x9.log`).

**Impact**

A refactor that gives the "nothing to set" path an early exit would answer SUCCESS where Milan requires NOT_SUPPORTED or STREAM_IS_RUNNING. No native, wire or coverage gate would notice. The 100% branch ratchet is met either way, because only the order of the guards changes.

This is the same class of gap R564-2-F1 closed for latency, on the same path. It is less severe because the path changes no state. Hence MINOR.

**Lens attribution**

- Recorded under Tests only. The defect is the missing negative pin in the test suite.
- Conformance and Robustness of the implementation were applied to the same lines and are clean. The guard order at `:318-336` meets 5.4.2.9 and 7.4.15.2, as S1 and S2 show at this head.

**Required outcome**

- For flags 0, 4, 8 and 12 (no XXX_VALID sub-command), a named test asserts:
  - STREAM_INPUT gives NOT_SUPPORTED;
  - a running STREAM_OUTPUT gives STREAM_IS_RUNNING, with the current latency reported and the store unchanged.
- The plant table gains plants for both bypasses, each requiring its named diagnostic.
- No production change is needed.

**Verification**

- X8 and X9 (texts in `probes/core_plants.py`) fail the new named assertions at both interface counts.
- The maintained table stays fully caught.
- The bank stays green.

## Residue (wording only)

- **R564-3-RES1 (Docs, PR body).** The PR #700 body's status line (`receipts/pr700-body-snapshot.md:19`, body updated 2026-10-09T18:26:56Z) says "PR #700 is published at `0ded1f269a44d107498f177c8276665656e07d30`. The two Round 3 commits are unpushed." The published PR head is `fb9c57d2ae3484804ff90f67feb57bf420c93dfa`.
  - Exact fix: replace those two sentences with "PR #700 is published at `fb9c57d2ae3484804ff90f67feb57bf420c93dfa`, including both Round 3 commits."
  - This changes no measurement, verdict, test, code or clause claim.

## Prior findings at this head

There has been no production change since `0ded1f26`, where R565-2 and R564-2 judged all round-1 findings resolved. Their plants are re-run here in the maintained table.

| Prior finding | Status at `fb9c57d2` | Evidence |
|---|---|---|
| R565-1-F1 / R564-1-F1: root READ_DESCRIPTOR configuration_index | RESOLVED | Plant `root-configuration-refused` caught; R564-2 Q3 passes at both counts. |
| R565-1-F2: SET_STREAM_INFO echoes request | RESOLVED | `stream-info-request-echo` and `stream-info-flags-echo` caught. |
| R564-1-F2: SAVED_STATE/STREAMING_WAIT and no sub-command | RESOLVED | `stream-info-noop-refused` caught; R564-2 control `saved-state-refused` caught. |
| R565-1-F3 / R564-1-F5: unavailable-snapshot blocking | RESOLVED | `unavailable-head-blocks-notices`, `unavailable-retry-spins` and `retry-timer-lost` caught; R564-2 `unavailable-event-dropped` caught; Q1 passes. |
| R565-1-F4: cross-instance callback guard | RESOLVED | `cross-instance-guard-removed` caught; R564-2 `init-guard-after-memset` caught; Q5 passes. |
| R564-1-F3: non-AEM message types | RESOLVED | `hdcp-data-length-echo` caught; Q4 passes. |
| R564-1-F4: ENTITY available_index | RESOLVED | `entity-available-index-static` caught. |
| R564-2-F1: no-sub-command latency | RESOLVED | See above. |
| R564-1 RES1, R564-2 RES1 | RESOLVED as worded | The sentence R564-2 named is gone. Its replacement is stale again, so R564-3-RES1 records it. |
| R564-1 S1-S3, R564-2 S1-S3 | Unchanged, optional | Not counted. |

## Executed evidence (exact-head clone, source-head execution only)

The scoped simulator identified as `Verilator 5.050 2026-07-01 rev v5.050` before use. The RV32 compiler is the pinned SDK's `riscv32-linux-gcc`. Submodules:

- gPTP `5dce647a`;
- processor `2ad2f845`;
- verilog-axis `48ff7a7e`;
- lwSRP `9197193e`, initialized for the run at its unchanged gitlink and de-initialized afterwards.

The two-interface wire reference was a separate checkout of processor `c9f74b68`.

| Gate | Result | Receipt |
|---|---|---|
| `test_ctrl_firmware.py --require-rv32 --jobs 4` | rc 0; 59 arms `[ok]`, 65 tallies, 1408 checks, 0 failures; AECP 70/70 at each interface count; rv32 arm with 15 objects | `receipts/fwbank.log` |
| `aecp_mutants.py --shard 0 2` and `--shard 1 2` | rc 0 each; 72/72 caught | `receipts/mut0.log`, `mut1.log`, `aecp-mutants-results.json` |
| `aecp_arms.py --app --interfaces 1/2`, native and `--asan` | rc 0; 70/70 each (4 runs) | `receipts/arms-*.log` |
| `aecp_wire.py`, 1 interface, `2ad2f845` | rc 0; 132 observations; 7 controls | `receipts/wire1.log`, `wire-one-b-*.json` |
| `aecp_wire.py`, 2 interfaces, `c9f74b68` | rc 0; 274 observations; 7 controls per ingress | `receipts/wire2.log`, `wire-two-b-*.json` |
| Reviewer oracle probes (`probes/oracle_probes.py`) | rc 0; 21/21 | `receipts/oracle-wire-*.log` |
| Reviewer plants X1-X6 plus baseline (`probes/core_plants.py`) | 12/12 killed; baseline 70/70 at each count | `receipts/plants.log`, `reviewer-plants-results.json` |
| Reviewer plants X7, X8, X9 | X7 caught (lock guard pinned); **X8 and X9 escape** (R564-3-F1) | `receipts/plants-x7.log`, `-x8.log`, `-x9.log` |
| Reviewer probes S1/S2 (`probes/run_r564_3_probes.py`) | Head: 2/2 at each count; X8 fails S1; X9 fails S2 | `receipts/r564-3-probes-*.log` |
| R564-2 plant driver, unchanged | rc 0; 5/5 caught | `receipts/r564-2-plants-rerun.log` |
| R564-2 Q1-Q5, unchanged | rc 0; 5/5 at each count | `receipts/r564-2-probes-rerun.log` |
| `make -C tb/verilator/mbx` (pinned simulator) | rc 0; 0 failures in every tally (Wishbone 382/384, AXI4-Lite 427/429, cosim 32, host model 369 checks); mailbox plants 5 of 5 caught | `receipts/mbx-make.log` (install root redacted) |
| `gen_mailbox.py --check` | rc 0; 0 findings | `receipts/gen-mailbox-check.log` |
| `scripts/docs_check.py` | rc 0; 0 findings across 201 md files | `receipts/docs-check.log` |
| Clone integrity after all work | rc 0; 1269 entries byte- and mode-exact; index equals tree; gitlinks unchanged; status empty | `receipts/clone-integrity.txt` |

**Run notes**

- A first launch of the bank and the plant table refused because the clone's lwSRP submodule was not initialized. Its partial logs are kept in `receipts/aborted/`.
- A first pair of wire runs passed, but their rc wrappers were lost when that launch was stopped. Those logs are in `receipts/first-wire/`. Both were re-run cleanly with rc files.

**Hosted checks at the exact head** (`receipts/gh-pr-checks.txt`, `check-runs-head-2.tsv`; all rows on `fb9c57d2`, second snapshot 2026-10-09T18:42:20Z):

- **Completed successfully:** bdd-conformance, changes, docs-check-no-git, full-ci-gate, verilator-lint, wire-accountability, yosys-elaboration, Yosys shards 0-3 and Verilator shard 3/5.
- **In progress:** docs-check, elaborate, firmware-unit and Verilator shards 0, 1, 2 and 4.
- **Skipped, not executed:** Physical gPTP (nightly and manual).

No hosted acceptance is claimed.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | See note C. | R564-3 | fb9c57d2ae3484804ff90f67feb57bf420c93dfa |
| RTL | CLEAN | See note R. | R564-3 | fb9c57d2ae3484804ff90f67feb57bf420c93dfa |
| Robustness | CLEAN | See note B. | R564-3 | fb9c57d2ae3484804ff90f67feb57bf420c93dfa |
| Tests | UNCLEAN (R564-3-F1) | See note T. | R564-3 | fb9c57d2ae3484804ff90f67feb57bf420c93dfa |
| Docs | CLEAN (R564-3-RES1 is residue) | See note D. | R564-3 | fb9c57d2ae3484804ff90f67feb57bf420c93dfa |

**C (Conformance).**

- `aecp_commands.c:281-353`, checked against the Milan v1.2 5.4.2.9 text and IEEE 7.4.15.1, 7.4.15.2 and Table 7-145.
- The oracle rule at `aecp_wire_oracle.py:103-107`.
- Wire verdicts at 1 and 2 interfaces.
- Probes S1/S2, Q2 and the oracle probes.

**R (RTL: architecture, widths, error and default paths).**

- No RTL, mailbox-contract or production-C change in the round delta (`receipts/scope-and-size-inputs.txt`); the PR as a whole touches nothing outside `sw/firmware/` and `docs/`.
- `aecp_commands.c:327-347`:
  - 32-bit unsigned masks against Table 7-145 bit positions;
  - the 0x80000000 latency bound;
  - `cfg.latency[index]` reached only after `aecp_find` validated the descriptor.
- `mbx-make.log` and the bank's rv32 arm.

**B (Robustness).**

- No-sub-command success is idempotent over four flag sets, before and after a saved override (`test_aecp.cpp:810-838`; plants X1-X5).
- The refusal order for a STREAM_INPUT, a running output and a foreign lock precedes the success path (`aecp_commands.c:318-336`; probes S1/S2; plant X7).
- Unsupported sub-commands are atomic (`test_aecp.cpp:798-802`).
- The short body (83 B) gives BAD_ARGUMENTS (`:775`).
- Sanitizer arms are 70/70 at both counts.

**T (Tests).**

- The `test_aecp.cpp` delta (`:794`, `:810-838`).
- `aecp_mutants.py:35-59` and the full table.
- `aecp_wire.cpp:58-61`, `aecp_wire.py:165-166` and `aecp_wire_oracle.py:103-107` and `:190-215`.
- 12 reviewer plants, 21 oracle probes and 2 reviewer probes.
- R564-3-F1 is open.

**D (Docs).**

- `sw/firmware/ctrl/aecp/README.md:146-155`.
- `docs_check.py`.
- The PR #700 body snapshot and REVIEW READY 6086832557.
- R564-3-RES1 is wording-only.

**Banking note.** R564-3-F1 can be fixed in tests alone. Such a fix leaves the scope of Conformance, RTL, Robustness and Docs untouched, except for a plant-table or README count update under Docs and Tests. Any change to `aecp_commands.c` would un-cover Conformance, RTL and Robustness.

## Real limits

- **Image relink.** I did not relink the image this round. The bare-metal runtime archives are not available here. The 221,728 B figure rests on:
  - byte-identity of every linked input with round 2 (shown);
  - R564-2's independent stub-runtime relink at `0ded1f26`;
  - the author's round-3 receipt.
- **Not run:**
  - the builder bank;
  - the saved-state bank;
  - `fw_coverage.py --check`. Production C is unchanged and the delta only adds tests, so coverage cannot decrease. The 100% ratchet is not re-measured here.
  - the firmware bank `--self-test` over the inherited control, SRP and saved-state tables;
  - act or the local replica;
  - hosted acceptance;
  - any hardware.
- **Physical calibration is NOT RUN**, and field skips are not hardware proof.
- **Latency and service figures** were not re-derived beyond the bank's passing Latency tests. They remain desk bounds.

## Reproduction

Use an exact-head clone with initialized submodules as `TREE` and this packet as `PACKET`.

- **Plants:** `python3 -B $PACKET/probes/core_plants.py $TREE <out> [--only NAME...]`.
- **Probes:** `python3 -B $PACKET/probes/run_r564_3_probes.py $TREE <out> [X8.nosub-bypasses-running-only|X9.nosub-bypasses-input-refusal]`.
- **Oracle probes:** `python3 -I -B $PACKET/probes/oracle_probes.py $TREE <aecp_wire output dir> <out>`.
- **Integrity:** `python3 -I $PACKET/probes/verify_clone.py <clone> fb9c57d2ae3484804ff90f67feb57bf420c93dfa`.

The gate command lines are in the evidence table.

## Pending manager duties

- Publish this report and manifest, and carry R564-3-RES1 to the residue checklist.
- Hosted acceptance at the exact head, distinguishing executed from skipped contexts. At capture: docs-check, elaborate, firmware-unit and four Verilator shards were in progress, and Physical gPTP was skipped.
- Validate the current-dev merge candidate at the merge turn, with the builder and native banks plus act. The source base is `5603c353137e90c1fa95429f6d00ef7a2298d9ee` and live dev is `7c1b52bee26b497080ee22b1c1986109f80a5ee7`. No manager source bank ran at this head, and none is claimed or inferred.
- Owner visibility, carried from R564-2: the largest shape with two interfaces is 49 nominal and 55 packed RAMB36 tiles against the "about 50" in ruling 6081705916. Routed fit and the 10% reserve are owed before the default flip.
- Processor #73 adoption, physical observer wiring, target timing and stack calibration remain the stated later obligations.
- Re-review after R564-3-F1 is answered. No review round may remain in flight before merge, and merge needs explicit maintainer authorization.

R564-3 FINISHED
