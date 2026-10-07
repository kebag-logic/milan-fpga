[R541] NEGATIVE - exact head a29f8d13ff4869e54997d9adf05d83a4ace4b8bd
<!-- SPDX-License-Identifier: Apache-2.0 -->
Independent verdict recorded before reading previous public review findings.

The new direct-receive protections pass their assigned tests and sampled reversals.
A cross-port receive can still overwrite a pending Flush value through propagation.
Both profiles reproduce 36 wrong-value withdrawals, covering three types, three reservation faults, IN/LV, and timer/receive completion.
The saved-value withdrawal contract remains unfulfilled.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN | Frozen acceptance, round-six assignment, public interface, state transitions, independent cross-port probe | R541-5 | a29f8d13ff4869e54997d9adf05d83a4ace4b8bd |
| RTL | CLEAN | Complete changed-file inventory, host and embedded source lists; no HDL or gitlink change | R541-5 | a29f8d13ff4869e54997d9adf05d83a4ace4b8bd |
| Robustness | UNCLEAN | Reservation rollback, pending flag, propagation FIFO, receive and timer interleavings | R541-5 | a29f8d13ff4869e54997d9adf05d83a4ace4b8bd |
| Tests | UNCLEAN | Eight suites, both profiles, 16 sampled reversals, selective JoinMt plant, independent public-interface probes | R541-5 | a29f8d13ff4869e54997d9adf05d83a4ace4b8bd |
| Docs | UNCLEAN | Contribution rules, reader guides, saved-value contract, sentence/reference/link checks, 27 rendered graphs | R541-5 | a29f8d13ff4869e54997d9adf05d83a4ace4b8bd |

No hardware or parent banks were executed.
Historical finding reconciliation and checkout restoration remain finalization tasks.
