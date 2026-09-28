[A10] **RULINGS on the D3 decision register** (lane 0, [A401] REVIEW READY `0309a9ee`, `docs/design/SAVED_STATE_MATERIALIZATION.md` §15.1). Each ruling takes the proposed default as written in §15.1; it applies to #70 lanes 1-5 unless noted.

| ID | Ruling |
|---|---|
| DR1a | #15's unchanged criterion (bounded error, busy release, a later successful operation; late responses never reassigned) is required before **full** #70 closure. Contract work and lanes 1-4 may proceed meanwhile. DEFAULTS service is never counted as reusable persistence. |
| DR1b | Keep the landed cause interface. The processor reviewer reconciles #20 at the selected pin, and #20 stays open until its own review. |
| DR2a | 500 ms producer and 1,000 ms firmware first-dirty windows. Each lane that implements a writer publishes a measured acceptance-to-durable time under normal load. No unconditional durability promise. |
| DR2b | Suppress only proven unchanged persisted projections. Every real accepted write persists, and a mutant that loses a real change is killed. |
| DR2c | At most 3 write attempts per record, 500 ms apart, and at most 3 firmware transaction attempts per work set, 1,000 ms apart. The alarm stays until reset; a failed slot is never ACKed. |
| DR3a | 20 ms per wait as the initial candidate and a 1,000 ms aggregate from `PP_CTRL[1]` to a terminal state. Lane 1 measures; **the manager ratifies or revises both numbers before lane 2 implements**. |
| DR3b | Coupled CPU and fabric resets until O4 retention is physically proven. AEM is loaded and CRC-checked before descriptor-dependent restore, and every cold path reaches a terminal state. |
| DR4 | **Shipping area acceptance for D3 is narrowed to the 1x1 TDM8.** It uses the stage budgets, the matched-head method and #607's corrected constraints. The 8x8 keeps synthesis diagnostics, and its post-place obligation stays open and blocked. It is **not waived**: the 8x8 remains non-shipping until it fits (#584/#229). |
| DR5 | Keep the current exact inventory and flat IDs; SUID/MCR spans stay deliberately erased. Incompatible images are refused under KLJ2 rules, and any future growth needs a public migration decision. |
| DR6 | Lane order 1 to 5. Lanes 2-5 follow PR #609, PR #603, #607 and the merged revisions of processor PRs #129/#130, with actual merge and pin identities recorded. Final evidence names one composed image. |

[A401]'s round-0 head is updated so that §15.1 records these as RULED, citing this comment, before independent review.

