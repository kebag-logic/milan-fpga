Status: REVIEW READY for the bounded round-6 gate repair. ETA: complete. The full PR remains blocked on the separately owned 100 Mb/s egress grader and outstanding integration, physical validation and review obligations.

Local head: `b4a1df4a0913d7a9b03c8ed0678a035ba2eda5d6` on `1011-usbnet`. Round-5 head `ddda29e1e28ec5b1a58786a750fd1f21b8f6c0d0` is preserved. Nothing pushed or posted; no bench or flash access.

The supplied patch was adapted to the actual head. The Contents list already existed; its eight entries now match the supplied wording exactly. `MAX_LEN_OCTETS_P` was already implemented by `af139adc5b7d2ebfc1ab7b73493216f632982663`, including the local-receiver instantiation and the mutation trigger. Byte comparison proves that earlier RTL change was exactly the identifier substitution. Its current 1514-octet receive default and 1515-octet local override are preserved; the obsolete 2000-octet patch context was not restored. This round changes only `docs/design/USB_NET_PATH.md`.

The exact Contents CI sequence exposed one additional problem in that same page: the FR_NFR 3.4.1 link used a stale fragment. It now points to the existing `3.4.1 Control service budget and normative timing` heading. This is an anchor correction only; no requirement, scheduling row, bound or allowance changes.

In this head's generated workflow, `gate_31` is the boundary-unit naming ratchet and `gate_45` is the per-page Contents gate (the request listed the numbers in reverse). Both complete command blocks from `.github/workflows/docs.yml`, job `docs-gates-0`, pass. Naming includes 66/66 self-checks. Contents includes 1501/1501 self-checks, all 764 existing cross-page fragment targets, and its final contents check. The initial missing-renderer refusal and the subsequent stale-anchor failure are retained. The locked Markdown dependencies were installed in isolated scratch; the final gate is not a skipped or reduced check.

The USB-network RTL suite passes 92,755 checks and four real SET_CLOCK_SOURCE command cases. All 72 planted defects are caught by their named checks; every individual log is retained. The tests, firmware builds and generated-logic comparison ran at `f773819b81ab8ba77066df0e49a25e69fecf54ce`. The only later change corrects the document link; `receipts/final-head-evidence.json` carries those results by exact input identity. The final source check verifies every other tracked blob and both trees' five build-relevant dependency checkouts against their pinned Git objects. The unused external dependency is checked by gitlink identity only.

Six fresh firmware builds prove candidate/comparison identity at the same pins. The comparison remains #1004 `4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1` plus only its two updated dependency pins, comparison head `b646e520eb0c51b5e16ae94cbabf2cb835ef9226`.

| Image | Matching ELF SHA-256 |
|---|---|
| Arty | `f08cac5b313b85ad48a5835d0c9071b261829d5e0d35d58b3100aa86643265ea` |
| ALINX 1x1 | `286f9c0d6bdc8943e6fa8238c77dd235716611072f0248ece111a672a174ee5e` |
| ALINX 8x8 | `1ca3c0b24fd310aa6c2d38c34f482eef8a98f32b7c996bd57681547463c54e06` |

All six map headers match SHA-256 `5f0c602687dacba302959ebb99763e5922aff8ad19f76e7c7c05919b45a936fa`. Both trees use tsn-c-stack `a795471c0abc4e38f7e5146b4e539dd607b6f501` and gptp-processor `3ce71b768a2f6f6a5274c127080146e755d02275`; all remaining gitlinks also match. The complete pin table is in `receipts/source/source-identity.json`.

There is no gateware change in this round. A fresh Arty generation through `vivado-slot.sh` at priority 19 matches the retained generated logic after removing comments only; the raw diff is retained. Constraints and all six memory-initialization files are byte-identical. No synthesis or route was rerun, because no netlist input changed. Round-5 route and CDC evidence carries with its existing limitations. No new all-corners result or whole-ALINX-bitstream identity is claimed.

The same-pin round-5 147-case census remains the retained CPU evidence: slice 1250 us, pace 10 ms, load 0.5004771140, ACMP 29.77 ms, txL 48.82 ms, last notice 117.47 ms, longest pass 1.7846875 ms. It was not rerun for this documentation change. Its #969 disposition and seven held-egress observations remain unchanged. Firmware identity does not discharge the separate 100 Mb/s egress proof.

The [100 Mb/s ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7216971645) is explicitly outside round 6. #1004 must first supply the held-row grader: replay all commits from all 147 traces through the shipping queue, preserve each free-space outcome, and prove the maximum wait plus 5% and fixed-path costs stays within 1000 us. This lane then adds the longest injected frame per busy period and the measured injection handshake. Any changed free-space outcome requires a link-rate census under the unchanged row rule. The 254-record correction belongs with that grader. No ring, owner bound or allowance moves here.

The FX3 attachment, board LED observations, full current-candidate gates and independent re-review remain open. The round-5 whole-image CDC/I/O limitations and inherited documentation findings are not cleared by these two gates. The PR draft uses Relates to #1011 and Relates to #1018; neither issue is declared complete. This packet is executor evidence, not an independent review verdict.

All execution was foreground in the assigned CPU-weight-200 unit, using the shared compiler cache. Final scratch use: 7610646528 bytes, below 25 GB; final free space: 33956507648 bytes, above 18 GB. Audited removals were logged before execution with literal absolute paths. Exact commands, source checks, failed setup attempts and final receipts are indexed in [receipts/INDEX.md](receipts/INDEX.md).
