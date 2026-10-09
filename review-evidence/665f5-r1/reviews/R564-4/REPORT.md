[R564] POSITIVE - exact head c2a4d2982fc5f9c345746ded7a0c8f6658c05cce

# R564-4: internal independent review of PR #700, round 4 (issue #665, lane F5, AECP on the bare-metal core)

Head `c2a4d2982fc5f9c345746ded7a0c8f6658c05cce`, tree `696f9317aad2a3cd40b70805e1a420ff9e6945e7`. This round reviews only the delta `fb9c57d2..c2a4d298`, which is two test-only commits: `b3187dc0` and `c2a4d298`. Rounds R564-1..3 and R565-1..3 stand for the rest of the PR.

## Summary

- **R564-3-F1 is RESOLVED.**
  - Standing tests `Core.S1_NoSubcommandSetOnRunningOutputIsRefused` and `Core.S2_NoSubcommandSetOnInputIsNotSupported` pin both no-sub-command SET_STREAM_INFO refusals. The authority is Milan v1.2 5.4.2.9 and IEEE 1722.1-2021 7.4.15.2.
  - Both tests cover flags 0/4/8/12 on every ingress, at one and two interfaces.
  - Plants X8 and X9 each fail their named test with the named diagnostic, at both interface counts, in a completed run (not a compile error).
  - The wire differential now reaches both refusal classes. It also rejects X8 and X9 end to end.
- **The delta is test-only.** Production sources are byte-identical to `fb9c57d2`: the AECP core, adapter, application, RTL, configs, mailbox and submodule gitlinks. Six files changed: five tests and the AECP README.
- **Image size.** The maximum linked span is **221728 B** (8x8 shape, two interfaces), 2272 B below 224000. The link-map `__image_start`/`__image_end` symbols and the fixture's size report agree for all four links.
- **No BLOCKER, MAJOR or MINOR.**
  - One RESIDUE: R564-4-RES1, a stale status line in the PR body.
  - One SUGGESTION: R564-4-S1, README wording.
- **Lenses.** All five lenses are covered clean at this head: Conformance, RTL, Robustness, Tests and Docs.

## Reconstruction (public sources, in order)

1. AGENTS.md (sections 3, 6, 7 and 8) and the CONTRIBUTING contract it points to. docs/README.md as the documentation map.
2. Issue #665 sources:
   - lane F5 assignment 6081266905, which defines Part A/B, the gates and one/two interfaces;
   - the owner budget ruling 6081705916, which sets a 224 KB STOP threshold for the largest shape at two interfaces;
   - the Round-4 assignment 6087150456, which asks for the S1/S2 standing tests, X8/X9 in the plant table, a wire row if reachable, and tests only;
   - the executor's REVIEW READY Round 4 comment 6087703590.
3. Clauses: Milan v1.2 5.4.2.9 (SET_STREAM_INFO: Stream Input NOT_SUPPORTED, streaming Stream Output STREAM_IS_RUNNING) and IEEE 1722.1-2021 7.4.15.1/7.4.15.2 (current fields, streaming restriction). These are applied as cited in the assignment and in `sw/firmware/ctrl/aecp/README.md`.
4. Diff and history: `git diff 5603c353..c2a4d298` (38 files) for context, then the delta `fb9c57d2..c2a4d298`, reviewed line by line.
5. Public executable evidence:
   - `review-evidence/665f5-r1` at `c7078141`, which carries the round-1 size matrix, runtime provenance and reproduction recipe;
   - the manager's issue and PR comments.
6. Prior public findings were read only after my own pass. My notes and tentative verdict were written before I read R564-3 and R565-3.

## Delta examined

| File | Change |
|---|---|
| `sw/firmware/ctrl/test/test_aecp.cpp:840-877` | New S1 test, which loops interfaces 0..N-1 and flags {0,4,8,12}. A running output gives status 12, size 122, current latency 123456 reported, the latency store unchanged, the saved override preserved, and `Changed` called 0 times. New S2 test, with the same loops: an input gives status 11, size 122. |
| `sw/firmware/ctrl/test/aecp_mutants.py:35-48` | Rows `nosub-bypasses-running-only` (X8) and `nosub-bypasses-input-refusal` (X9), each owning its S1/S2 diagnostic. |
| `sw/firmware/ctrl/test/aecp_wire.cpp:20-65, 82-97, 113` | `wire_stream_info_refusals`. It sends four input refusals. It then establishes real output streaming (PROBE_TX status 0, Listener Ready, `dbg_streaming0_o` asserted) and sends four running-output refusals, checking that the stored latency is unchanged in firmware and fabric. It then tears down (Listener leave, MAAP withdrawal, no declarations remaining) and re-registers. `ask` records `output_running` and refuses a mid-command streaming change. |
| `sw/firmware/ctrl/test/aecp_wire_model.hpp:91` | Output `running` now follows the physical model's `dbg_streaming0_o` rather than the `started` flag. |
| `sw/firmware/ctrl/test/aecp_wire_oracle.py:94-117, 131-133, 186-201, 207-256` | The oracle grades the refusal status, current fields and the absence of notices. The fabric must give the same status. A census requires exactly one row per (class, flags). Four new controls are added (false success and missing row, per class). There are 11 controls in total. |
| `sw/firmware/ctrl/aecp/README.md:146-156` | The control count (eleven), the flags covered, the clauses for the two refusal classes, and how streaming is established. |

The refusal guards are unchanged: `sw/firmware/ctrl/aecp/aecp_commands.c:317-323` (`type == 5u` gives NOT_SUPPORTED, then `info.running` gives STREAM_IS_RUNNING). Both precede the lock check and sub-command selection at `:324-336`.

**The wire-model change does not alter any earlier row.**
- Outside the new window the physical output is not streaming (`aecp_wire.cpp:54` checks this). Before the bind at `aecp_wire.cpp:136`, `started` is also false, so the old and new definitions agree for every output SET there, including `:114` and `:127`.
- They differ only after `:136`. From there on, the commands do not consult output `running`: input START/STOP and GET_STREAM_INFO, notices, register, deregister, lock and available.
- Every row at this head is graded by the oracle in any case.

## Executed evidence (this round, reviewer-run)

All runs used disposable scratch trees built from the exact head: a local clone with submodules at their gitlinks, and lwSRP at its `9197193e` pin. The review clone was never written; see "Integrity".

| Check | Result | Receipt |
|---|---|---|
| Composed application suite, interfaces 1 and 2 | 72/72 pass at each count; S1 and S2 OK | `receipts/gtest/base-app-if{1,2}.*` |
| X8 (table text) at interfaces 1 and 2 | Compiled, rc 1. Only `Core.S1_NoSubcommandSetOnRunningOutputIsRefused` fails, with `STREAM_IS_RUNNING for a no-sub-command SET`. Killed at both counts. | `receipts/gtest/X8-*` |
| X9 (table text) at interfaces 1 and 2 | Compiled, rc 1. Only `Core.S2_NoSubcommandSetOnInputIsNotSupported` fails, with `NOT_SUPPORTED for a no-sub-command SET to a STREAM_INPUT`. Killed at both counts. | `receipts/gtest/X9-*` |
| Reviewer-own variants, interface 2 | V1 (running bypass only for flags=8) is killed by S1. V2 (input bypass only for flags=12) is killed by S2. V3 (running refusal stores the requested latency) is killed by S1 "refusal preserves stored latency". V4 (running refusal echoes the requested latency) is killed by S1 "refusal reports current latency". Each is compiled, rc 1, and fails only the named test. | `receipts/gtest/V*` |
| Executor's mutation driver, rows X8 and X9 (`--shard 0 74`, `--shard 1 74`) | `[ok]` both | `receipts/driver/` |
| Plant-table ownership control | 74 rows, 76 owned tests. Exactly one planting site for X8 and for X9. No drift. | `receipts/mutation-table-controls.txt` |
| Wire differential, interfaces 1 and 2, pinned simulator 5.050 (`sha256 905795b9...`) | PASS. 142 observations at one interface, 147/147 at two. 11 oracle controls per ingress. "Current SET stream information" differences grow 7 to 15 (+8 rows). Every ingress carries all 8 refusal rows: input flags 0/4/8/12 give core 11 and fabric 11 with current latency 12345; running output flags 0/4/8/12 give core 12 and fabric 12 with current latency 67890; each emits one frame and no notice. Reference inventories are content-pinned (`2ad2f845`, `c9f74b68`). | `receipts/wire/`, `receipts/runs4/` |
| Wire differential with X8 planted in the core, interface 1 | rc 1, `AssertionError: running STREAM_OUTPUT SET refusal` | `receipts/runs6/wire-X8-*` |
| Wire differential with X9 planted in the core, interface 1 | rc 1, `AssertionError: STREAM_INPUT SET refusal` | `receipts/runs6/wire-X9-*` |
| Four RV32 links, `ctrl_srp_image.py --with-aecp` | Spans: 1x1_tdm8 if1 140400, if2 153056; 8x8 if1 194224, if2 **221728**. The link-map `__image_end - __image_start` equals the reported `ram_span` for each. The margin to 224000 is 2272 B at the maximum. | `receipts/image/spans.txt`, `*.ctrl_app.map`, `*.size.json` |
| Runtime archives for those links | Rebuilt from the published `runtime-provenance.json` recipe (25 commands). All 58 recorded source hashes match. The archive bytes differ from the published hashes (libc 5478 vs 5542 B; compiler-rt 29128 vs 29432 B), which is consistent with embedded build-path strings; this is why `receipts/runtime.rc` is 1. The linked spans equal the executor's figure exactly. | `receipts/image/runtime-report.json`, `receipts/runtime.log` |

`receipts/runs/` and `receipts/runs2/` are superseded setup attempts that never reached a test. In the first, the scratch root lacked the gPTP generator; in the second, it lacked git metadata. They are retained for completeness and carry no result.

## Findings

No BLOCKER, MAJOR or MINOR finding.

### R564-4-RES1 - RESIDUE - Docs - PR #700 body, Status, lines 18-20 (`receipts/pr/pr700-body-snapshot.md:18-20`)

- **Authority/evidence:** the PR API reports head `c2a4d2982fc5f9c345746ded7a0c8f6658c05cce` (body updated 2026-10-09T19:23:23Z). The body still says "Local implementation head `c2a4d298...`" and "PR #700 is published at `fb9c57d2...`, including both Round 3 commits. The two Round 4 commits are unpushed."
- **History:** R564-3-RES1's named sentence was replaced as instructed, so that item is resolved as worded. This is the round-4 recurrence of the same stale publication wording.
- **Impact:** wording only. It changes no measurement, figure, verdict, test, code, generated artifact, conformance or clause claim, and touches no privacy rule.
- **Exact fix:** replace the text from the start of line 18 up to "Assignment-required" on line 20 with:

  > Implementation head `c2a4d2982fc5f9c345746ded7a0c8f6658c05cce`; `665-f5-aecp` -> `dev`. PR #700 is published at `c2a4d2982fc5f9c345746ded7a0c8f6658c05cce`, including both Round 4 commits.

  Keep "Assignment-required executable gates pass; ..." as is.
- **Verification:** read the PR body after the edit.

### R564-4-S1 - SUGGESTION - Docs - `sw/firmware/ctrl/aecp/README.md:155`

- "Controls replace each refusal with success and remove each case." The four controls act on the flags-0 row of each refusal class (`aecp_wire_oracle.py:222-234`). The census and status assertions still cover all eight rows.
- Optional wording: "Per refusal class, one control turns the flags-0 refusal into success and one removes it."
- Not a defect. It does not affect any lens.

## Prior public findings at this head

| Finding | Status at c2a4d298 | Evidence |
|---|---|---|
| R564-3-F1 (MINOR, Tests): no-sub-command input/running refusals unpinned | **RESOLVED** | Every required-outcome item is met. S1/S2 cover flags 0/4/8/12. Running output gives STREAM_IS_RUNNING, current latency and an unchanged store. Input gives NOT_SUPPORTED. The plant table has X8/X9 with named diagnostics. X8/X9 are killed at both counts. 72/72 pass. |
| R564-3-RES1 (PR body status line) | RESOLVED as worded | The named sentence is replaced at body line 19. The recurrence is R564-4-RES1. |
| R565-3-RES1 (same PR-body wording, round 3) | RESOLVED as worded | Same as above. |
| R565-1-F1..F4, R564-1-F1..F5, R564-2-F1, R564-1/2 RES1 | RESOLVED (unchanged) | They were resolved at `fb9c57d2` by R564-3/R565-3. No production file changed since (`receipts/clone-integrity.txt`). |
| R564-1 S1-S3, R564-2 S1-S3 (SUGGESTIONs) | Retained, optional | Unchanged and non-blocking. |

## Lens coverage (artifacts examined at this head)

```text
[R564] PASS Conformance - sw/firmware/ctrl/aecp/aecp_commands.c:317-336; test/test_aecp.cpp:840-877; test/aecp_wire_oracle.py:94-133; receipts/wire/*.verdict.json, wire-*-ingress*.log - The no-sub-command SET_STREAM_INFO refusals were checked against Milan v1.2 5.4.2.9 and IEEE 1722.1-2021 7.4.15.1/.2. Input gives NOT_SUPPORTED and a streaming output gives STREAM_IS_RUNNING, before sub-command selection. Current fields and latency are reported, with no notice. The fabric gives the same status on all 8 rows on every ingress. The 224000 B budget (ruling 6081705916) is met at 221728 B.
[R564] PASS RTL - git diff fb9c57d2..c2a4d298 (no hdl/, submodule or generated change); receipts/wire/wire-if{1,2}.reference-sha256.json; test/aecp_wire.cpp:20-65 - The unchanged RTL is driven through its existing ports. Streaming is established via PROBE_TX and Listener Ready and withdrawn via leave and MAAP conflict. Two-interface ingress selection is restored. The streaming state is sampled before and after each command.
[R564] PASS Robustness - test/test_aecp.cpp:840-877; test/aecp_wire.cpp:43-64; test/aecp_wire_model.hpp:91 - Boundary flag combinations 0/4/8/12 are covered on every ingress at 1 and 2 interfaces. The running refusal preserves the latency store, the override and callback silence. The wire fixture checks that stored latency is unchanged in firmware and fabric, and tears its setup down (stop, withdraw, no declarations) before the later timer rows. The model change affects only type-6 running, which is false outside the new window.
[R564] PASS Tests - test/test_aecp.cpp:840-877; test/aecp_mutants.py:35-48,450-470; test/aecp_wire_oracle.py:186-256; receipts/gtest/*, receipts/driver/*, receipts/runs6/* - S1/S2 can fail for the defects they claim: X8, X9 and V1-V4 are killed by named diagnostics in completed runs at the stated counts, and X8/X9 are also caught on the wire. The suite is 72/72 at both counts. The plant-table ownership control passes (74 rows, 76 tests). The wire has 11 controls per ingress.
[R564] PASS Docs - sw/firmware/ctrl/aecp/README.md:146-156; receipts/pr/pr700-body-snapshot.md - The control count (eleven) equals the `changes` tuple at aecp_wire_oracle.py:209-210. The clauses and the streaming-establishment description match the code. No count elsewhere went stale. Only R564-4-RES1 (residue) and R564-4-S1 (suggestion) remain.
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `aecp_commands.c:317-336`; `test_aecp.cpp:840-877`; `aecp_wire_oracle.py:94-133`; wire verdicts and rows at 1/2 interfaces; image spans against the 224000 B ruling | R564-4 | c2a4d2982fc5f9c345746ded7a0c8f6658c05cce |
| RTL | CLEAN | delta scope (no RTL/submodule/generated change); reference fingerprints `2ad2f845`, `c9f74b68`; `aecp_wire.cpp:20-65` port usage | R564-4 | c2a4d2982fc5f9c345746ded7a0c8f6658c05cce |
| Robustness | CLEAN | `test_aecp.cpp:840-877`; `aecp_wire.cpp:43-64`; `aecp_wire_model.hpp:91` | R564-4 | c2a4d2982fc5f9c345746ded7a0c8f6658c05cce |
| Tests | CLEAN | S1/S2; plant table rows X8/X9; X8/X9/V1-V4 runs; driver rows; wire controls and wire plants | R564-4 | c2a4d2982fc5f9c345746ded7a0c8f6658c05cce |
| Docs | CLEAN (R564-4-RES1 is residue; R564-4-S1 is optional) | `aecp/README.md:146-156`; PR body snapshot | R564-4 | c2a4d2982fc5f9c345746ded7a0c8f6658c05cce |

**Banking note.** For files outside this delta, coverage banked by R564-3 at `fb9c57d2` carries forward: no file within those lenses' scope changed between `fb9c57d2` and this head. The six changed files are covered above at `c2a4d298`.

## Integrity

- The review clone at `$REVIEWS/r564-4-665f5` is at HEAD `c2a4d298` with a clean status, index equal to HEAD (write-tree `696f9317`), and worktree equal to the index.
- The six delta blobs hash to their HEAD blobs.
- Gitlinks are unchanged: `external efeb541a`, `gptp-processor 5dce647a`, `protocol-processor 2ad2f845`, `third_party/lwSRP 9197193e`, `third_party/verilog-axis 48ff7a7e`. The initialized submodules are clean.
- All plants and builds ran only in scratch copies (`receipts/clone-integrity.txt`).

## Real limits

- **Not run by this reviewer:** the full firmware bank, the coverage gate (`fw_coverage.py --check`), sanitizer arms, the mailbox, builder and docs banks, the NVM bank, and the full 74-row mutation campaign (only rows X8/X9 plus the table ownership control).
  - Coverage cannot regress through added tests with unchanged production sources, but the ratchet itself was not re-executed here.
  - For these gates, the source-head execution evidence is the executor's gate receipts, as reported in 6087703590. That round-4 packet is described there as local and unpublished. No manager source bank ran at this head.
- **Plant texts:** the X8/X9 texts are the plant-table texts. Their behaviour matches R564-3's public description. R564-3's original probe file was not consulted.
- **Image bytes:** byte-identity of the load images with Round 2 was not checked. Only spans and sections were measured, with runtime archives rebuilt from hash-verified sources.
- **Hosted CI:** exact-head hosted CI was not inspected. The manager owns hosted and local-replica acceptance.
- **Physical:** physical calibration is NOT RUN, and routed memory fit and reserve are not established. Field skips are not hardware proof. This is a desk and simulation review.

## Pending manager duties

- Publish this report and manifest. Carry R564-4-RES1 to the residue checklist (exact fix above).
- Obtain the external R565-4 verdict. No review round may remain in flight.
- Validate the current-dev merge candidate at the merge turn (source base `5603c353`, live dev `7c1b52be`) with the builder and native banks. Link those receipts, the hosted exact-head contexts and the local-replica result.
- Merge only with explicit maintainer authorization.

R564-4 FINISHED
