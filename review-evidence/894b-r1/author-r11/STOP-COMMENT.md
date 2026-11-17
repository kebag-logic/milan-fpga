[A781] STOP

Round 11, head `05a7ea82fa0625e077959cd1b4eed28a7a05b064` (`894-8x8-1if`, PR #914). Nothing pushed; the checkout is clean.

The [round-11 ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6934688411) is implemented: `backlog-owed.service.aecp.last.if0` at 8x8/1if derives 62.16 ms. The ledger retains 61.75319 ms on the composed image and 62.04905 ms with the Listener copies, plus the earlier merged measurement. Final-head regrades pass; this row is 0.11095 ms under its ruled figure. All eight images match the measured `46cf2a7d` images by ELF and loadable-byte SHA-256.

**The final gates fail:**

| Gate | rc | Failure |
|---|---:|---|
| `firmware-srp-mutants`, `ci_step_9` | 1 | `asking-is-ready` and `readyfailed-ignored` escape. Both still mutate the registrar-walk expression (`srp_mutants.py:94,224`, `srp_mbx.c:861`); #930 now copies readiness in the Listener callback (`srp_mbx.c:185`), without that walk on these records. The selected mutated tests return success. |
| `make -C tb/verilator/milan_dp twin` | 2 | `owed row split-talker-failed does not hold`: the split sends Talker Advertise; the row expects Talker Failed. This pass does not establish when the mismatch originated. |
| `make -C tb/verilator/milan_dp twin-plants` | 2 | `plant srp-plus-k: ESCAPED by "MSRP Talker Failed stream_id 0200000000010001"`. The emitted diagnostics concern Talker Advertise; the required diagnostic is absent. |

The launcher returned zero despite recorded failed steps. The per-step audit is authoritative: 83 workflow commands ran, 82 rc 0 and the SRP step rc 1. The lane has 72 commands: 66 rc 0, four expected report/control exits at 1, and the two failures above at 2. Coverage passes across 39 files, including `srp_mbx.c` 746/746 lines; the docs jobs and the control/AECP campaigns pass.

Shards 1, 3, 4, 6, 10 and 17 first refused the local clone's donor-origin provenance. Fresh-clone retries of 1, 3, 4 and 6 were stopped on discovery of the gate failure; 10 and 17 were not retried. No partial sweep pass is claimed. `docs_inventory --check` is NOT RUN: no tracked executable with that name exists at this head. Each unrun workflow step has a reason.

#930's numerical targets remain met: 1x1/1if SRP record 250 us by the rule (stated 280), last queued notice 136.65 ms against 140; 8x8/1if load 0.735 against 0.75. R4 by every source at 8x8/1if, 21.39 ms against 20, remains owed to #872. The timing floor is #818's +0.030 ns setup and 0 ns hold, best of three directives; no route ran.

The round11 packet contains HANDOFF-r11.md, the full PR-BODY.md with `Closes #930`, original/final image hashes, regrades, individual failed logs, step inventory, not_run.json and an index generated from the files present. Large logs are represented by explicit excerpts with their original SHA-256 and size. All worker units and loops are stopped. No test, bound, ledger rule or donor was weakened to clear these failures. REVIEW READY remains blocked on correcting and rerunning them and completing the selected shards.
