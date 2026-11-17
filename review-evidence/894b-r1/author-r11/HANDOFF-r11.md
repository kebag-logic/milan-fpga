# HANDOFF: lane 894b, round 11, [A781]

Status: STOP. Final head `05a7ea82fa0625e077959cd1b4eed28a7a05b064`, branch `894-8x8-1if`, tracked and untracked tree clean. Nothing pushed, no PR edit, merge, rebase, donor change or hardware access. The source commits were already present when this interrupted session resumed; this continuation changes only the packet and disposable scratch setup.

## Authority and scope

The latest [A10] ruling on #894 is issuecomment-6934688411, read live and retained at `receipts/ruling-r11.md`. It authorizes 62.16 ms for `backlog-owed.service.aecp.last.if0` at 8x8/1if, accepts the #930 targets, keeps every-source R4 owed to #872, and requires the final firmware campaigns, coverage, docs, lane gates and shards 1, 3, 4, 6, 10 and 17. It permits one STOP on a failed gate. No round-11 completion comment was present at the resume audit.

The original R843-1 and R844-1 reports were read in full and retained in `receipts/reviews/`. PR-BODY.md gives the finding-by-finding dispositions for those reports and the later findings. Author dispositions are not independent approval.

## Changes already committed before this continuation

| Commit | File:line | Reason and result |
|---|---|---|
| `7ee9342d31` | `tb/verilator/ctrl_service_budget/egress_ledger.py:70` | Add LISTENED, retaining the composed measurement 61.75319 ms and Listener-copy measurement 62.04905 ms beside the earlier merged measurement 61.84625 ms. Derive the entry from the largest under the existing rule: 62.16 ms. Name the 2026-11-17 ruling. Other ledger entries unchanged. |
| `7ee9342d31` | `docs/design/SPLIT_CONTROL_MEMORY.md:2792` | Explain the phase change and ruled figure; table includes each measurement. The self-test holds the table to the ledger. |
| `9203d89d6e` | `docs/design/SPLIT_CONTROL_MEMORY.md:2823`; `docs/reference/FR_NFR.md:396` | State the Listener-copy image at both points and its 32,936-cycle SRP record. Earlier image identity no longer describes #930's changed firmware. |
| `05a7ea82fa` | `sw/firmware/ctrl/test/test_ctrl_firmware_shards.py:70` | Let the campaign stand-in accept and distinguish its entity argument. The first run at 9203d89d refused that argument; the final run counts 1,537 live invocations exactly once. |

`receipts/source/round11.diff` contains the complete round-11 delta; `final-state.txt` records the head and clean tree.

## New checks and diagnostic controls

- The ledger self-test: 15 caught mutants, no failures. The new mutant uses the composed measurement where the Listener-copy measurement is larger; failing words: `section 13's measurement is the one the ledger derives from`. Existing unchanged-ledger and seven one-cycle/large-increase controls remain. Receipt: `receipts/gates/lane/egress_ledger_selftest.log`.
- Shard inventory: 1,537 invocations, sizes 82/717/303/435. Plants `missing suite` and `duplicate suite` are rejected; nine invalid shard combinations refuse. Receipt: first lines of `receipts/gates/workflow/rtl-fast__firmware-srp-mutants__ci_step_9.log`.
- Existing #930 plants: all five Listener-copy mutations are caught in the final full campaign, but two older SRP mutations escape. The campaign as a whole FAILS, regardless of the new plants' results.
- Original round-4 compile guards, row controls, regrade and image proofs are copied under `receipts/round4/` for the dispositions that cite them.

## STOP findings

1. **Firmware SRP campaign, rc 1.** Workflow `rtl-fast.yml`, job `firmware-srp-mutants`, step `ci_step_9`:
   - `[ESCAPED] asking-is-ready: RegisteredListenerSubtypeChangeRevokesPermission / adapter.ifs[0].active[0]`
   - `[ESCAPED] readyfailed-ignored: ReadyFailedAndUninterestingStreamsAreSeparated / Actual function call count`

   Both selected mutated tests return success. `srp_mutants.py:94` and `:224` still plant at `srp_mbx.c:861`, the registrar walk's readiness expression. #930's Listener callback copies readiness at `srp_mbx.c:185` and no longer owes that walk on these records. The old mutation sites no longer affect the behavior these tests exercise. No mutation or test is removed or weakened here. The appropriate correction needs renewed campaign evidence.

2. **Twin comparison, rc 2.** `make -C tb/verilator/milan_dp twin` reports `[DIFF] owed row split-talker-failed does not hold`. The split sends Talker Advertise for `0200000000010000`; the expectation is Talker Failed for both sources from boot, never withdrawn. This pass proves the mismatch, not its origin or that it is a new regression. See `receipts/gates/lane/twin.log`.

3. **Twin plants, rc 2.** `make -C tb/verilator/milan_dp twin-plants` reports `plant srp-plus-k: ESCAPED by "MSRP Talker Failed stream_id 0200000000010001"`. Actual protocol diagnostics concern Talker Advertise; the required words at `twin_compare.py:70` are absent. See `receipts/gates/lane/twin_plants.log`.

The launcher and lane wrapper ended rc 0 while their command logs recorded failures. This continuation audits the per-step `.rc` files, not those wrapper exits. Earlier handoff/progress language that inferred all firmware/lane passes from wrapper status is superseded by this audit. No REVIEW READY is claimed.

## Gate table

| Gate | Result / receipt |
|---|---|
| Final workflow run steps | 83 executed: 82 rc 0, one rc 1. 208 unexecuted steps have individual reasons; the suite command is separately REFUSED/INCOMPLETE. `receipts/gates/workflow-steps.md` and `.json`; `not_run.json`. |
| Firmware suites / coverage | Six unit-job steps rc 0; coverage PASS across 39 files, `srp_mbx.c` 746/746 lines. `workflow/rtl-fast__firmware-unit__ci_step_12.log`. |
| Control / AECP campaigns | Every step rc 0; 716 / 302 `[ok]` lines, no escapes. Counts are log markers, not a claim of separate test cases. `firmware-summary.json`. |
| SRP campaign | Step rc 1, two escapes above; 434 `[ok]` lines do not clear it. |
| Boundary / firmware simulation jobs | All recorded steps rc 0. |
| Six selected docs jobs | All 61 executed steps rc 0. The no-git driver's final status query fails after its three successful steps because that job deliberately removes `.git`. |
| Lane gates | 72 commands: 66 rc 0; four declared `_exits_1` reports/controls at expected rc 1; two failures above at rc 2. `lane-results.json`. |
| Quick checks | 21 rc 0. Scans over 7398ec0a..HEAD and round 9/10/11 deltas, plus R844-1's audit, report zero forbidden lines. `quick-checks.txt`. |
| Shards 1, 3, 4, 6, 10, 17 | First attempts refused donor origin; no affected-suite pass. Fresh-clone retries 1,3,4,6 stopped on the true gate failure. 10,17 not retried. No incomplete check totals counted. |
| docs_inventory --check | NOT RUN; no tracked command with that name exists at this head. Explicit reason in not_run.json. |
| git diff --check | Final-head quick/lane checks pass; round-11 delta rechecked clean. |
| Images | All eight match the measured 46cf2a7d images by ELF and loadable-byte SHA-256. `receipts/images/`. |
| Existing measurement regrades | 14 positive legs per point pass at the final head; separate transmit-aged control caught 8/8. `receipts/harness/`. |

A regrade audit initially included the intentional transmit-aged negative control among positive legs. It correctly failed on its planted late MRPDU. `control-included-refusal.txt` retains that audit; the final positive regrade excludes only that separately documented control, as the original measurement packet did. No ledger or bound changed during regrading.

## Image and measurement carry

`receipts/images/qimg-05a7ea82.txt` records all eight complete ELF and loadable hashes, ROM/SRAM sizes and tile counts. Each matches `receipts/round10/images/qimg-46cf2a7d.txt`; `identity-46cf2a7d-05a7ea82.txt` compares all eight. The 8x8/1if platform remains 56.0 RAMB36. Thus round 10's measurements carry without a new measurement. This is not an identity claim against 716a8ae7: #930 deliberately changes firmware. The incomplete shards and failed tests cannot be carried by image identity.

The ruled entry regrades at 62.04905 ms against 62.16 ms, 0.11095 ms under. Other held rows remain recorded misses within their permitted entries. #930's targets: 1x1/1if record 250 us by the rule (stated 280), last queued notice 136.65 ms (140); 8x8/1if load 0.735 (0.75). R4 by every source at 8x8/1if is 21.39 ms (20), owed to #872. Timing remains #818's floor: +0.030 ns setup, 0 ns hold, best of three directives; no route was run.

## Resume and cleanup

- Resume found HEAD 05a7ea82 and no tracked edits, with an untracked generated dispatch key directory. It was moved intact to private scratch without reading its contents; it is not in this packet.
- All 21 earlier queued workers had finished. Six selected shards had refused `source dependency origin differs: third_party/tsn-c-stack`. The offline clone helper had retained a local filesystem origin. Refusals were preserved under `receipts/gates/setup-refusals/`.
- Four fresh-clone retries restored the declared donor origin before running. They booked CPUs through the shared picker, used separate 10 GB units, and were stopped once the per-step audit found the SRP failure. Their MainPID arguments were listed before stopping each exact unit name. No unrelated process was touched. `receipts/gates/stopped-retries.txt` records this.
- Six disposable clones from the refused attempt were deleted after their logs were retained. Scratch remains below 20 GB. No toolchain, package, tree export or file above 200 KB is in the output directory. Large logs have explicit excerpts plus original size and SHA-256, indexed by `raw-manifest.json`.
- No worker or loop remains active. The current session service is not a worker to kill before handing off.

## Manager handoff

Posted exactly one `[A781] STOP` on #894: https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6936661453. Its body was read back and verified, and no duplicate round-11 STOP exists. `receipts/publication.json` records it. Do not post again. The manager owns any push or PR edit. PR-BODY.md is the full replacement body, includes `Closes #930`, current targets and figures, every-source R4 debt, timing floor, both reviews' dispositions, and the failures. Do not mark this head ready or infer a review ledger from earlier heads.

Remaining work is to resolve the two escaped SRP mutations and the twin expectations/diagnostics without weakening their behavioral checks, rerun the affected complete jobs on the corrected clean head, finish the selected exhaustive shards, then seek independent review. No new measurement is justified by this continuation's packet-only changes.
