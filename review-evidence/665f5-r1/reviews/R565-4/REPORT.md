[R565] POSITIVE - exact head c2a4d2982fc5f9c345746ded7a0c8f6658c05cce

External independent delta review, round R565-4, issue #665 / PR #700 (lane F5, AECP on the bare-metal core).
Tree: `696f9317aad2a3cd40b70805e1a420ff9e6945e7`. Delta: `fb9c57d2ae3484804ff90f67feb57bf420c93dfa..c2a4d2982fc5f9c345746ded7a0c8f6658c05cce`, two one-line test commits (`b3187dc0`, `c2a4d298`) changing six test and prose files. Source base: `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.

R564-3-F1 is **RESOLVED** at its original severity, not downgraded or moved. All five lenses are CLEAN at this head. No BLOCKER, MAJOR or MINOR finding is open. One wording residue is recorded in the PR body (R565-4-RES1, a repeat of R564-3-RES1 and R565-3-RES1 for this round). This verdict covers the reviewed source head only. It does not declare merge readiness, and it is not a manager source bank.

## Reconstruction

Reading order:

1. AGENTS.md and CONTRIBUTING.md (one-line commits with no trailers; review and completion bar).
2. docs/README.md.
3. Issue #665: body, the F5 assignment 6081266905, the 224 KB ruling 6081705916, and the round-4 assignment 6087150456 (frozen scope: S1/S2 standing tests at one and two interfaces, X8/X9 table rows each killed by its named test, a wire row if reachable, tests only).
4. Clause text: Milan v1.2 5.4.2.9 and IEEE 1722.1-2021 7.4.15.2.
5. The core handler `sw/firmware/ctrl/aecp/aecp_commands.c:281-353`.
6. The raw delta and its history.
7. Executable evidence: my own runs, the author's REVIEW READY round 4 (issue comment 6087703590), and the published evidence branch.

My own pass over the delta and my plants came first. Only after that did I read the prior public findings on this PR, specifically R564-3 (6087141878) and R565-3 (6087077112). I read no private author material, no lane scratchpad and no other reviewer's report from this round. The author's round-4 packet is not published on the evidence branch: its tip is `b33217b9`, which has no `author-r4`. The author's round-4 claims below are therefore cited only from the public REVIEW READY comment.

## R564-3-F1 at this head: RESOLVED

| Assignment item | Status | Evidence |
|---|---|---|
| Standing test: a no-sub-command SET_STREAM_INFO to a running Stream Output returns STREAM_IS_RUNNING | Met | `test_aecp.cpp:841-861`, `Core.S1_NoSubcommandSetOnRunningOutputIsRefused`. Flags 0/4/8/12 on every ingress (`AECP_TEST_INTERFACES`). It asserts status 12, a 122-byte response, current latency 123456 against requested 765432, and an unchanged store and saved override. `Changed` is expected zero times. |
| Standing test: the same SET to a Stream Input returns NOT_SUPPORTED | Met | `test_aecp.cpp:863-877`, `Core.S2_NoSubcommandSetOnInputIsNotSupported`. Flags 0/4/8/12 on every ingress; it asserts status 11 and a 122-byte response. |
| Run at one and two interfaces | Met | `receipts/baseline-if1.log` and `baseline-if2.log`: `Core.*`, 50/50 pass, including S1 and S2, rc 0. |
| X8 `nosub-bypasses-running-only` killed by S1 | Met | I re-applied it myself (`scripts/focused_review.py`). `receipts/X8-...-if1/if2.log`: rc 1, `verdict: FAIL (its tallies report ...`, with `STREAM_IS_RUNNING for a no-sub-command SET` inside S1's RUN/FAILED block. That is 4 named failures at if1 and 8 at if2. It completed and is not a compile error. |
| X9 `nosub-bypasses-input-refusal` killed by S2 | Met | `receipts/X9-...-if1/if2.log`: rc 1, with `NOT_SUPPORTED for a no-sub-command SET to a STREAM_INPUT` inside S2's block at both counts. |
| Both plants in the mutation table | Met | `aecp_mutants.py:35-49`. Plant strings and named checks match R564-3's. The table drift control (`controls()`: every test claimed, unique names) PASSES (`receipts/table-probe.out`). |
| Wire-differential row if reachable | Met | `aecp_wire.cpp:21-66`. PROBE_TX plus Listener Ready establish real streaming, and `dbg_streaming0_o` is checked before and around each command (`:42`, `:83`, `:95`). Oracle: `aecp_wire_oracle.py:93-117` and `:128-138`, census `:186-201`, controls `:209-255`. |
| Tests only, core unchanged | Met | `receipts/scope-and-size-inputs.txt`: no path outside `sw/firmware/ctrl/test` and `aecp/README.md` changed. `aecp_commands.c` blob `4c483e0e` is identical at fb9c57d2, at HEAD and on disk (`receipts/integrity.txt`). |

Independent formulations, as a check that the tests do not just mirror the reviewer's plant text. V8 moves the running-output guard below the no-sub-command early return, and V9 does the same with the input guard (`scripts/delta_probes.py`). Each completes and fails its named test with its named diagnostic: 4 failures at if1 and 8 at if2 (`receipts/V8-*`, `receipts/V9-*`, `receipts/delta-probes.json`).

Wire differential at this head, using the pinned simulator (Verilator 5.050, sha256 `905795b9…e92f`, `receipts/simulator-identity.json`):

- **One interface** (`receipts/wire-clean-if1/`): reference `2ad2f845` (content-pinned). 142 observations, 11 controls, PASS.
- **Two interfaces** (`receipts/wire-clean-if2/`): reference `c9f74b68` (content-pinned). 147 + 147 observations, 11 controls per ingress, PASS.
- **Refusal rows on every ingress:**
  - Input, flags 0/4/8/12: fabric status 11, core status 11.
  - Running output, flags 0/4/8/12: fabric status 12, core status 12.
  - Each refusal emits exactly one frame and no notification.
- **Census:** the 'IEEE 7.4.15.1 and Milan 5.4.2.9: current SET stream information' difference moves from 7 to 15, which is exactly the eight new rows. The reference echoes the command, and the core reports current fields, as documented in `README.md:161`.
- **Wire-path plants** (X8/X9 applied to a scratch copy of the core):
  - X8 fails with `AssertionError: running STREAM_OUTPUT SET refusal` at both counts.
  - X9 fails with `AssertionError: STREAM_INPUT SET refusal` at both counts.
  - Receipts: `receipts/wire-X8-if*/`, `receipts/wire-X9-if*/`.

Image size. The RV32 image inputs (`ctrl_srp_image.py`: portable C, AECP/app/SRP/NVM C sources, the lwSRP pin, `ctrl_image.ld`) are not among the seven paths changed since `0ded1f26`. At `0ded1f26` this reviewer role's round 2 linked the 8x8 two-interface image independently: sections 84356 + 25158 + 448 + 103556 + 8192 = 221710 B, span 221728 B (public receipt sha256 `ce65be11…f102`, `receipts/size-retention.txt`). The span is unchanged at this head: 2272 B under 224000 B and 7648 B under 224 KiB. The author's round-4 statement of four unchanged links at a maximum of 221728 B agrees. I did not relink this round and did not read the link maps themselves; see limits.

## Findings

No BLOCKER, MAJOR or MINOR finding.

**R565-4-RES1 | RESIDUE | Docs | PR #700 body, "Status" paragraph**
- Authority/evidence: the live PR head is `c2a4d2982fc5f9c345746ded7a0c8f6658c05cce` (`gh api pulls/700`, head.sha). The body still says "Local implementation head `c2a4d298…`… PR #700 is published at `fb9c57d2…`, including both Round 3 commits. The two Round 4 commits are unpushed." It also introduces checkout with "After the authorized owner publishes the candidate:". This is the round-4 instance of R564-3-RES1 and R565-3-RES1.
- Impact: stale publication wording only. No measurement, test, code, figure, conformance claim or verdict changes.
- Exact fix: replace the first Status sentences with "Implementation head `c2a4d2982fc5f9c345746ded7a0c8f6658c05cce` is the published PR head on `665-f5-aecp` targeting `dev`, including both Round 4 commits." Replace "After the authorized owner publishes the candidate:" with "To check out the published candidate:". Keep the gate and independent-review qualifications.
- Verification: compare the body against `head.sha` at publication.

**R565-4-S1 | SUGGESTION | Tests | `test_aecp.cpp:863-877`**: S2 runs only with the input unbound and stopped. Milan 5.4.2.9's input refusal does not depend on state, and the core checks `type == 5u` first, so this is optional. A bound or streaming iteration would pin that order against a future reshuffle with the bound/running checks.

## Prior findings at this head

| Prior item | Status at `c2a4d298` | Evidence |
|---|---|---|
| R564-3-F1 MINOR (Tests) | RESOLVED | Section above. |
| R564-3-RES1 / R565-3-RES1 (PR body publication wording) | RETAINED as R565-4-RES1 (residue, non-blocking) | The live body still describes an older publication state. |
| R565-1, R564-1, R564-2 findings | RESOLVED, unchanged | No production, RTL, configuration or generated change since `0ded1f26`, where they were judged resolved (R565-2, R564-2) and re-confirmed at `fb9c57d2` (R565-3, R564-3). Unchanged files were not re-reviewed, per the round scope. |
| Earlier SUGGESTIONs | Optional, unchanged | Not coverage-affecting. |

## Lens results

- [R565] PASS Conformance — `aecp_commands.c:317-323`, `test_aecp.cpp:841-877`, `aecp_wire_oracle.py:93-117`; Milan v1.2 5.4.2.9 and IEEE 7.4.15.2 text. Input gives NOT_SUPPORTED (11) and a streaming output gives STREAM_IS_RUNNING (12). Both come before sub-command selection and neither depends on XXX_VALID. Status codes match the AECP status table. The fabric reference agrees on status for all 8 rows per ingress.
- [R565] PASS RTL — `receipts/scope-and-size-inputs.txt`, `receipts/integrity.txt`, `receipts/size-retention.txt`. No RTL, mailbox contract, submodule pin or production C changed. The wire fixture reads only `dbg_streaming0_o`, `aecp_pt_offset_o` and `acmp_declaring_o` (`aecp_wire.cpp:21-66`), and drives the bench's existing inputs. Image inputs are unchanged since the 221728 B independent link.
- [R565] PASS Robustness — `test_aecp.cpp:841-877`, `aecp_wire.cpp:21-66`, `receipts/wire-clean-if2/`. The ignored-flag variants 0/4/8/12 are covered on every ingress. A refusal preserves the stored latency, the override and the PT offset, and emits no notification. Streaming stability is asserted across each command. Teardown (Listener Leave, MAAP withdrawal, declarations cleared) is checked before the later liveness cases, and the later rows still match the fabric.
- [R565] PASS Tests — `receipts/X8-*`, `X9-*`, `V8-*`, `V9-*`, `wire-X8-*`, `wire-X9-*`, `baseline-if*`, `table-probe.out`. The new tests pass at head and fail on the reviewer plants and on independent reorderings, at both counts and on their own named diagnostics. Wire oracle controls (false success and missing row) are mandatory on every ingress, and the census is exact.
- [R565] PASS Docs — `sw/firmware/ctrl/aecp/README.md:146-161`, checked against `aecp_wire_oracle.py:209-255` and the clause text. "Eleven" controls = 7 + 4, matching `planted_controls: 11`. The clause citations, the flags list and the description of the PROBE_TX / Listener Ready fixture are accurate. The PR-body wording is residue only (R565-4-RES1).

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `aecp_commands.c:281-353`; `test_aecp.cpp:841-877`; `aecp_wire_oracle.py:93-138`; Milan 5.4.2.9, IEEE 7.4.15.2; wire rows in `receipts/wire-clean-if1/`, `wire-clean-if2/` | R565-4 | c2a4d2982fc5f9c345746ded7a0c8f6658c05cce |
| RTL | CLEAN | `receipts/scope-and-size-inputs.txt`; `receipts/integrity.txt`; `receipts/size-retention.txt`; `aecp_wire.cpp:21-66`; `aecp_wire_model.hpp:91` | R565-4 | c2a4d2982fc5f9c345746ded7a0c8f6658c05cce |
| Robustness | CLEAN | `test_aecp.cpp:841-877`; `aecp_wire.cpp:21-66,83-96`; `receipts/wire-clean-if2/` | R565-4 | c2a4d2982fc5f9c345746ded7a0c8f6658c05cce |
| Tests | CLEAN | `test_aecp.cpp:841-877`; `aecp_mutants.py:35-49`; `aecp_wire_oracle.py:186-255`; plant and variant receipts; `receipts/delta-probes.json`; `receipts/focused-results.json` | R565-4 | c2a4d2982fc5f9c345746ded7a0c8f6658c05cce |
| Docs | CLEAN (residue R565-4-RES1 carried) | `sw/firmware/ctrl/aecp/README.md:146-161`; PR #700 body (live) | R565-4 | c2a4d2982fc5f9c345746ded7a0c8f6658c05cce |

## Limits

- **Table campaign not executed.** The two new table rows were not run through the table's own app-mode campaign. The driver refused because `third_party/lwSRP` is an uninitialised gitlink in this review clone (`receipts/table-campaign/NOTE.txt`). The identical plant strings were run in core mode at both counts instead. The author reports 74/74 caught across both shards; that is the author's claim, not verified here.
- **No full suites.** App-mode, sanitizer and coverage suites, the firmware bank, and builder/documentation banks were not run. They are outside this delta's allowed scope.
- **No independent relink.** I did not relink the RV32 image this round, because the runtime archives and lwSRP are absent, and I did not read the link maps themselves. The 221728 B span is retained from an earlier independent link receipt, because no image input has changed since then.
- **First harness attempt superseded.** The first wire-plant attempt failed in my own harness (an incomplete scratch root) before any build (`receipts/delta-probes.out`), and the wire section of `scripts/focused_review.py` was cut by the earlier session interruption. Both were superseded by the `--wire-plants-only` rerun and the clean wire runs in `scripts/delta_probes.py`.
- **No hardware claims.** Physical calibration was NOT RUN. Field skips are not hardware proof. No routed fit, no target timing and no stack bound are claimed.
- **Hosted checks were still running.** At snapshot time (`receipts/hosted-check-runs.tsv`), Verilator shards 0/1/2/4, firmware-unit and docs-check were in progress. Physical gPTP is skipped, which is a skipped context, not an executed job. The manager owns hosted and act acceptance.

## Pending manager duties

- Publish this report. Carry R565-4-RES1 to the residue checklist.
- Validate the current-dev merge candidate (source base `5603c353`, live dev `7c1b52be`) with the builder and native banks, and link those receipts.
- Accept the exact-head hosted contexts and the local replica, and confirm the second independent positive review and the full completion ledger before any authorized merge.

Clone restored and verified: HEAD and index tree are `696f9317`, the worktree is clean with no untracked files, and the submodule gitlinks are unchanged (`receipts/integrity.txt`).

R565-4 FINISHED
