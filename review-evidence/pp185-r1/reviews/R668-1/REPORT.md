[R668] NEGATIVE - exact head b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad

One MAJOR finding remains: automatic unlock coinciding with the claim of a pending lock-notification round can emit the preceding LOCK flags and consume the pending notification. The ordinary directed suites pass; an independent clock-boundary probe fails. One comment-only RESIDUE item is also recorded.

Reviewed tree: `6ecc64cb8c3434106e71bbb191aebe9a0249db1e`. Diff base: `b48312e13b8a3ed409dbe8a66d6311f2e37cd5f2`. This is a source review, not acceptance of a final parent merge candidate or hardware qualification.

**Authority and independent reconstruction**

The supplied AGENTS instructions and their referenced command policy were read first. This repository has no tracked AGENTS.md or CONTRIBUTING.md. The reconstruction then covered `docs/README.md`, the issue bodies and public decisions, the compliance requirements and relevant interface/memory/timing contracts, the diff and author/merge history, and finally published executable evidence. No private author material, management source bank, other checkout, or other review report was used.

- [Issue #185](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/185) and its [assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/185#issuecomment-6249574548): READ_DESCRIPTOR CONTROL must reflect the current SET_CONTROL value; tests, planted mutants, processor gates and parent consumer gates are required. No register-map, top-level port or parameter change is authorized.
- [Issue #186 correction](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/186#issuecomment-6253571045) supersedes the issue body's and assignment's original timeout-flags instruction. Both unlock causes require UNLOCK and locked_id zero; a LOCK notification echoes LOCK. Authorities are IEEE 1722.1-2021 7.5.2 and 7.4.2.1/Table 7-143, with Milan v1.2 Table 5.22. For CONTROL, the authorities are IEEE 7.2.22 and 7.3.6.2/Table 7-122, and Milan 5.3.12.
- Local authorities examined include REQ-AEM-003/006/014, REQ-NOT-001/002, architecture 02's interface contracts, 06's descriptor and notification contracts, 07's descriptor/dynamic-state ownership, 08's lock timer, and 09's verification/command-table contracts. Clause reconstruction used these public statements and in-tree transcriptions; no separate licensed standards PDF was consulted.
- History examined: `198f1b1`, `c826171`, corrected timeout commit `fcb6b51`, merge `a2cf652` of `246cbc22`, README adjustment `f42c886`, and the published merge of `b48312e1`. The reviewed diff is preserved in [reviewed.diff](receipts/reviewed.diff).

The independent verdict and all five lens decisions were written to [independent-verdict-ledger.txt](receipts/independent-verdict-ledger.txt) before checking prior public review findings. The subsequent [public-review audit](receipts/prior-public-review-audit.json) found two review-start comments, zero submitted reviews, and zero inline review comments on PR #196. There were no prior public FINDINGS to resolve or retain at this observation. The issue comments contained assignment/correction and readiness notices; no additional manager source-bank receipt was present.

**F1 — MAJOR — Automatic unlock can lose its flags at the round-claim boundary**

Attributable lenses: **Conformance, RTL, Robustness, Tests, Docs**.

Artifacts: `hdl/aecp/KL_aecp_notify.sv:1391`, particularly the new flags assignment at `:1400`; the picker at `:842`; round snapshot at `:1510` and pending clear at `:1517`; `hdl/aecp/ucode/gen_ucode.py:1184`; `tb/aecp_notify/sim_main.cpp:376`; `docs/architecture/06_aecp_engine.md:813` and the PR body's coalesced-timeout guarantee.

When `exp_lock_w && lk_held_r` coincides with `N_IDLE` claiming an already-pending lock round, the expiry updates `lockf_r` to UNLOCK, but the same edge snapshots the **old** `pick_arg0_w/pick_arg1_w` into the active round. The claim clears `pe_lock_r`. Thus the active round contains the earlier LOCK flags, the lock holder has become zero, and no pending automatic-unlock round remains. Updating the pending flags register does not update the arguments already captured for emission. The existing LF coalescing test expires the lock while another round is held; it does not cover expiry on the claim edge.

Independent reproduction changes only the disposable bench. It registers a recipient, takes the lock, and supplies the lock-expiry event either immediately before the FSM returns idle or on the next edge, when it claims the round. The bench advances its millisecond input by 60,000 before delivering expiry; this is a unit event-timing test, not a measurement of the physical timer.

| Expiry placement | Prior LOCK flags | Presented notification flags | Lock held / holder | Later correcting job |
|---|---:|---:|---|---|
| One clock before claim | `0x00000000` | `0x00000001` | 0 / 0 | none needed |
| At claim | `0x00000000` | **`0x00000000`** | 0 / 0 | none |
| One clock before claim | `0x00010000` | `0x00000001` | 0 / 0 | none needed |
| At claim | `0x00010000` | **`0x00010000`** | 0 / 0 | none |

Evidence: [claim-collision.log](receipts/claim-collision.log), [bench-only patch](claim-collision.patch), [portable probe](probe-claim.py). The completed run has 65 checks and exactly two failures, both at the claim boundary. The ordinary baseline has 57 checks and no failures. This reproduction directly measures notification-job flags and the published lock state. It does not claim a full wire capture of the collision; the separately examined engine operand packing and E_LOCKUNS emission carry these arguments into the flags field and gather the current holder.

Authority/impact: the corrected #186 acceptance requires automatic unlock to carry UNLOCK with locked_id zero. This legal event coincidence violates that requirement and the documented unconditional last-cause guarantee. It is not repaired by a later notification in the probe.

Required outcome: resolve expiry and round claim consistently so the automatic unlock is represented with UNLOCK and the appropriate recipient exclusion, without losing the pending change. Preserve LOCK/UNLOCK command-word echo and #181 queue behavior. Add a standing regression for expiry immediately before, on, and after claim, with a planted control that breaks the corrected arbitration. Include both zero and nonzero preceding LOCK words and a registered former owner; verify the eventual byte-exact response and absence of a lost timeout notification. The existing RDC/LN/LF/TD/RN and occupancy/router checks must continue to pass. Make the implementation satisfy the documented guarantee; do not weaken the corrected requirement.

**F2 — RESIDUE — New source comments contain bench labels**

Attributable lens: **Docs**. Authority: the supplied owner comment rule of 2026-10-15. This is wording only; it changes no test, measurement, generated output, clause claim, or privacy rule. It does not independently make the verdict negative.

Exact locations and offending text are preserved in [comment-residue-locations.txt](receipts/comment-residue-locations.txt). Required wording fixes:

| Artifact | Exact wording change |
|---|---|
| `tb/aecp_notify/sim_main.cpp:376` | Remove the `LF:` prefix; retain the flags behavior and IEEE rationale, with issue #186 and REQ-AEM-003/REQ-NOT-001. |
| `tb/pp_top/sim_main.cpp:12138` | Remove `RDC1`, `LK2`, `RDC2 and RDC3`, and `RDC3b` from this new comment block. Describe the accepted SET, subsequent refusals, layout fallbacks, and one-octet overlay directly; retain issue #185 and add REQ-AEM-006/014. |
| `tb/pp_top/sim_main.cpp:12536`, `:12586`, `:12626` | Remove `(RDC5)`, replace `RDC6 rides the same power cycle` with `In the same power cycle`, and remove the `LN:` banner prefix. Retain the behavior, issue and requirement references. |
| `tb/ucpu/sim_main.cpp:851`, `:859`, `:860` | Remove the `RC:` banner prefix and `(P12)` reference. Replace `(tb/pp_top RDC grades that)` with `(wire order is checked at the processor boundary)`; retain the issue and clause rationale, adding REQ-AEM-006/014. |
| `tb/pp_top/notify_mutants.py:33`, `:34`, `:625`, `:626`, `:690` | Replace the L5b/L6d/AX/LN/LF references in prose with `command-driven and automatic-unlock wire checks`, `reserved-bit echo checks`, and `pending-round coalescence checks`, respectively; retain issue #186 and REQ-AEM-003/REQ-NOT-001. |

Verification: inspect only added comment/prose lines for forbidden labels after the edit. Leave assertion strings, control identifiers, execution, and recorded counts unchanged. Existing unrelated labels are outside this delta and remain under #746.

**Five-lens evidence ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — F1 | Frozen assignment/correction; REQ-AEM-003/006/014 and REQ-NOT-001/002; CONTROL offsets/current value; both unlock causes and LOCK echo | R668-1 | b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad |
| RTL | UNCLEAN — F1 | E_RDESCCT bounds/fallback/byte reconstruction; GET/SET dynamic row; engine dispatch/operand packing; internal flags wiring; notify expiry/picker/claim; occupancy and router | R668-1 | b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad |
| Robustness | UNCLEAN — F1 | Reset and power cycle, refused SETs, alternate layouts and short descriptor, coalesced causes, independent expiry/claim collision | R668-1 | b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad |
| Tests | UNCLEAN — F1 | RDC/RC/LN/LF/L5b/L6d/TD/RN assertions; all 9 descriptor and 16 lock controls; public campaigns; local baselines, five selected mutants and collision probe | R668-1 | b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad |
| Docs | UNCLEAN — F1; F2 residue | Architecture 06/09, compliance decisions 15/16, command JSON and decode record, bench READMEs, PR body; coalesced-last-cause guarantee contradicted by F1 | R668-1 | b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad |

The CONTROL path is otherwise consistent across its examined contracts: configuration-0 dispatch, locate before reads, length/offset/value-type fallback, current byte from the same volatile row as GET_CONTROL, preservation of neighboring bytes, reset zero, and no IDENTIFY persistence. Focused byte checks cover 112-byte descriptors and the microprogram checks the 113-byte one-byte tail. No unrelated top-level signature or register-map change was found.

**Execution and merge evidence**

| Reviewer execution at exact head | Result | Receipt |
|---|---|---|
| Focused processor descriptor/lock dispatch | 995 checks, 0 failures; AX 279 included | [log](receipts/descriptor-lock-baseline.log) |
| Microprogram suite | 445 PASS | [log](receipts/ucpu-baseline.log) |
| Notification suite, all three builds and cancellation runs | 86 PASS | [log](receipts/notify-baseline.log) |
| Event-router suite | 81 PASS | [log](receipts/router-baseline.log) |
| Documentation/command consistency, `make -j16 check` | rc 0 | [log](receipts/docs-check-checkout.log) |
| Descriptor controls: no overlay, wrong neighboring-byte shift, short floor 111 | Golden PASS; 3/3 KILLED by named checks | [results](receipts/descriptor-controls-results.json) |
| Notify controls: coalesced timeout flags zero; occupancy cleared beside push | Golden PASS; 2/2 KILLED by named checks | [results](receipts/notify-controls-results.json) |
| Independent expiry/claim probe | Two boundary failures; preceding-clock controls pass | [log](receipts/claim-collision.log) |

[Merge-preservation checks](receipts/merge-preservation.json) establish that the router implementation and its suite, occupancy visibility configuration, all count/occupancy lines, and the OCCUPANCY mutant set are unchanged from the review base. The notify suite still runs LF, then CQ, then OC; `cmdq_nempty_r == (cmdq_count_r != 0)` is checked at every edge in every build. The router scan uses registered valid/pending state, with acknowledgement enabling the load rather than feeding the scan. The local suites and selected simultaneous push/claim mutant support preservation of #181. The top-level parameter/port signature is byte-identical to the base.

The [published packet](https://github.com/kebag-logic/milan-fpga/tree/baba38e7bb95a25eb63d6c7864ea0a1ca01eb013/review-evidence/pp185-r1) was inspected after the diff. [Integrity verification](receipts/evidence-integrity.json) checks 227 selected indexed receipts against the manager-recomputed redacted bytes and SHA-256, also checking their published Git blob identities. The 11 intentionally absent large files are accounted for by INDEX.md and OVER-200KB.sha256; their underlying bytes were not independently inspected.

The author records processor gates at base `246cbc22` and final author head `f42c886`, all eight recorded return codes zero, including 1,030,123 suite checks at the latter. The merged-author campaigns record 67 descriptor-campaign checks PASS and 125/125 notification mutants KILLED, including all nine new descriptor and sixteen new lock controls. Parent consumer receipts record 17 return codes zero at each comparison point; the head parent records processor gitlink `f42c886` over dev `e9cbb676` with the #180 evidence-classification and #176 adoption patches. These are **author source-validation receipts**, not a manager source bank, and not a full-bank execution of the later published `b0f6f9c3` merge. See [gate identities and return codes](receipts/public-gate-summary.json).

Parent rc 0 is not blanket physical proof: the [builder classification](receipts/public-builder-classification.txt) says calibration did not run because its real report was absent. Omitted large parent logs and field/hardware skips are not promoted to executed proof.

At the final [hosted observation](receipts/hosted-final-observation.json), 2026-10-19 09:36 UTC, exact-head runs 39229352533 and 39229331955 each had completed successful portability and documentation jobs; both suites jobs were still in progress. No skipped job context appeared in that listing. Pending jobs are not counted as passing, and hosted/act acceptance remains the manager's responsibility.

**Reproduction, integrity and limits**

From this packet, use `python3 prepare.py /path/to/exact-head-clone`, then `python3 run-focused.py`, `python3 run-controls.py`, `python3 run-docs.py /path/to/exact-head-clone`, and `python3 probe-claim.py /path/to/exact-head-clone`. The probe driver records the expected simulation rc 1 in its receipt; inspect that receipt and the two named failures. `REVIEW_SIM` can name an equivalent pinned simulator launcher. The identity used here is recorded in [simulator-identity.txt](receipts/simulator-identity.txt). Drivers bound combined compilation concurrency to sixteen workers, give campaigns explicit job counts, and wait for their subprocesses in the foreground. No detached work remains.

The first archive-only documentation attempt failed because the inventories require Git metadata; the checkout rerun passed. Initial mutation attempts used the drivers' default system temporary directory before that behavior was noticed. Those attempts were discarded, their temporary trees were confirmed removed, and the reported campaigns were rerun with TMPDIR under packet/scratch. This execution-location deviation is recorded in [setup-limitations.txt](receipts/setup-limitations.txt); it is not hidden as a passing authorized run. Subsequent reproduction scripts set the scratch location explicitly.

No design fix, commit, push, GitHub write, parent bank, full processor bank, synthesis bank, hardware action, or manager bank was performed by this review. The collision probe edits bench code only in the disposable source tree and restores it. The original clone remained unchanged. [Final integrity](receipts/final-integrity.json) verifies all 657 tracked entries' bytes and modes, an index matching HEAD, the exact head/tree, and an empty status. This processor repository contains no submodule gitlinks; the required parent processor pins were checked in the published consumer receipts.

Pending manager duties: obtain a fix and renewed independent positive reviews for F1; carry F2 to the residue checklist; complete hosted/act acceptance; build and validate the eventual current-dev merge candidate with the builder and native banks, and link its receipts on the PR. Source validation does not replace that merge-turn candidate validation. Physical calibration and field/hardware qualification remain unproven wherever marked NOT RUN or skipped.

Only REPORT.md and files enumerated in MANIFEST.sha256 are publishable; scratch is excluded.

R668-1 FINISHED
