[R884] NEGATIVE - exact head 8267b8951616cfd570baf690835d4b0d38f14596

Round R884-3, external independent review of issue #884 / PR #966. Tree `b8f11886504b95ab3f48d7553de8ef173d2a67cd`. All five lenses applied. The three prior major findings are resolved at their causes. One MINOR documentation finding leaves Docs unclean; one wording-only RESIDUE does not affect coverage. No new implementation defect was found in this delta.

Scope: nine commits from `8167b70d89d2a913a07c3b1187f4f2469109eebc` to this head, within the overall change from `59b098841b1e2826aaf7a38b557faa5345f91c82`. Untouched code retains prior dispositions unless the delta changes its dependencies. The hot-list change affects both firmware placements' timing evidence. Prior public findings were consulted after the independent delta pass; no current-round peer report was used.

Authorities read: AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #884's body and public scope rulings, REQUIREMENTS.md REQ-PTP-01 through 09 and REQ-CSR-02/03, GPTP_SOFTWARE.md, REGISTER_MAP.md, and mailbox.yaml. The [held-row ruling](https://github.com/kebag-logic/milan-fpga/issues/884#issuecomment-7084113326) authorizes relearning the existing three-window hot list while retaining the figures. The [round-2b ruling](https://github.com/kebag-logic/milan-fpga/issues/884#issuecomment-7072401468) retains the turnaround and flood conditions. The later software-owner rulings govern the resumed scope rather than the original desk-only proposal.

Primary standards checked: IEEE 802.1AS-2020 10.2.5.1, 11.2.2(c), 11.2.19.3.3/.4; Milan v1.2 4.2.6.2.4/.5/.6. `standards.sha256` identifies the local standards. Their text is not republished.

## Findings

### R884-3-F1 | MINOR | Docs

**The authoritative memory table retains the pre-growth fixture sizes.**

**Artifacts:** `docs/design/SPLIT_CONTROL_MEMORY.md:141` and `:142`; `sw/litex/ctrl_memory.py:269`; `sw/litex/ctrl_memory_ledger.py:46`. Evidence: `packet-audit.log`, `published-spotchecks.txt`, and published `author-r4/receipts/memory-631dc544/test_ctrl_memory-631dc544.log`.

**Authority/evidence:** AGENTS.md's Docs lens requires changed contracts to be reflected in authoritative documentation. The table explicitly names `ctrl_memory.LEDGERED` and the symbols identifying each exception. It still states `image_gptp` sizes of 1,096 B and 2,136 B. This delta adds eight bytes per port, and both executable ledger readers now require 1,104 B and 2,152 B. The published memory check confirms those identities. The neighboring platform row was updated to 20,160 B, but these two fixture rows were missed.

**Impact:** a reader following the documented exception identity gets the wrong symbol sizes. This does not show a memory overflow or change the accepted tile limits. It does leave the authoritative current-state table inconsistent with the executable allocation contract. Under the owner's rule it is MINOR, not RESIDUE: correcting it changes numerical figures, rather than wording alone.

**Required outcome:** change the two fixture sizes to 1,104 B and 2,152 B; retain the 59.0 and 64.0 RAMB36 limits.

**Verification:** compare those rows against `ctrl_memory.LEDGERED`, `IMG_GPTP_1/2`, and the published memory receipts. Documentation checks and focused re-review suffice; no new bank run or implementation change is required for this finding.

### R884-3-R1 | RESIDUE | Docs

**New hot-list source comments contain issue-comment IDs.**

**Artifact:** `sw/firmware/ctrl/plat/ctrl_split_hot.txt:9`, `:16`, `:21`, all added by this delta.

**Authority/evidence:** the owner's source-comment rule permits issue and requirement IDs but excludes issue-comment IDs. These lines introduce `issuecomment-7084113326`, `issuecomment-6959600243`, and `issuecomment-6967930396`.

**Impact:** wording only. The comment IDs change no entries, trace hashes, procedure, measurements, verdicts, or clause claims.

**Exact fix:** remove `issuecomment-7084113326: ` from line 9, `issuecomment-6959600243, ` from line 16, and `issuecomment-6967930396, ` from line 21. Keep the issue numbers, ruling dates and item numbers. The design page already carries the public links.

**Verification:** inspect the comment-only diff and run `ctrl_hot.py --check`; the 286 data entries and trace hashes must remain byte-identical. Carry this item to the residue checklist; it does not leave a lens unclean.

## Prior findings at this head

| Finding | Disposition and evidence |
|---|---|
| R884-2-F1; affected part of R884-1-F3 | **Resolved.** `gptp.c:314` clears `good` and calls `as_capable_set(false)` at the second response. BMCA clears the publication flags immediately; `gptp_mbx.c:125` publishes after the frame. Both in-flight and completed-response paths call it. Original `run_multi.py` cases pass: capability is zero at each multi-response exchange and throughout the cease. Committed tests cover missing/late Follow_Up, completed exchanges, same-clock duplicates and five-minute/link resume. Removing immediate invalidation fails three regressions. |
| R883-2-F1; remaining R883-1-F1 | **Resolved.** `gptp.c:523` converts all four Pdelay timestamps to PHC minus accumulated steps; `:530` preserves the rate window while voiding old exchange/response state. Unsigned accumulation and negation avoid signed overflow. The current suite passes the forward/backward sub-envelope steps and 5/10 ms cases under undefined-behavior checks. Removing LocalClock correction fails six step tests. The published expanded sweep reports 144 rows and zero capability outage, including 300/400/475 us cases. The third-party stepped-PHC envelope limitation is now explicit in GPTP_SOFTWARE.md:118. |
| R883-2-F2 | **Resolved at source; hosted acceptance remains the manager's duty.** `milan_datapath.sv:9469` ties each engine PHC knob off once under `!GPTP_PLANE_EN_P`. Census counts remain adj=4, step strobe=5, step value=4; five crossing-net counts add the timestamp unit's actual reads with the reason recorded. `test_builder.py:18069` retains fabric defaults and software ownership as an opt-in. I ran gate 1c and planted an unconditional branch and a second software-owner assignment: both were rejected. The author's final-head full builder receipt is rc=0 with two explicit NOT RUN arms. The extra-reader census plant remains present. |
| R884-2-F2; R883-2-R1/R2 | **Resolved.** Publication test/plant comments now describe live-word tearing and REQ-PTP-07, with no reviewed head or reviewer history. R884-3-R1 is a separate new residue. |
| R884-1-F1 publication tear | **Resolved disposition retained.** `KL_mbx_cdc.sv:486` captures and crosses the committed bank. These RTL bytes are untouched; the publication bench changes only commentary. Public sweep/closed-loop receipts retain the tested ordering. |
| R884-1-F2 raw Sync renewing receipt timeout | **Resolved disposition retained.** `gptp.c:627` renews on a consumed pair; raw Sync does not. Current port suite passes. |
| R884-1-F4 absent information TLV | **Resolved disposition retained.** `gptp.c:728` rejects absent/malformed mandatory TLVs before use; unchanged guards and regressions pass. |
| R884-1-F5 skipped syntax check called PASS | **Resolved.** The current executing gate receipt is head-bound and reports 142 analyzed files. Current PR and builder evidence distinguish execution from NOT RUN. |
| R883-1-F2 split-sw absent from gates | **Resolved disposition retained.** `tb/verilator/milan_dp/Makefile` retains split-sw scheduling and public sweep evidence includes it; no scheduling delta. |
| R883-1-F3 stale route claims | **Resolved.** GPTP_SOFTWARE.md:167 dates software routes to `a6323318`, with the plane at `40bd7738`. PR text disclaims a post-relearn route. No RTL changed after the routed ancestor. |
| R883-1-F4 HAL call count | **Resolved disposition retained.** `gptp.h` and GPTP_SOFTWARE.md specify three callbacks, with time entering through tick. |
| R883-1-S1 null memory arguments | **Taken; retained.** Empty-path guards remain and the current sanitized suite passes. |

Earlier optional suggestions are retained below; none leaves a lens unclean. These rows name the artifact, impact, optional outcome and verification.

| ID / severity / attributable lenses | Artifact and disposition |
|---|---|
| R883-1-S2 / SUGGESTION / Conformance, RTL, Tests | `milan_datapath.sv` owner parameters: an RTL exclusivity assertion could protect direct instantiations outside the builder. If adopted, reject conflicting owners and preserve supported shapes. |
| R883-1-S3 / SUGGESTION / RTL, Tests | Software publication decode in `milan_datapath.sv`: generated field constants could reduce future drift. If adopted, compare field correspondence and run split-sw. |
| R883-1-S4 / SUGGESTION / RTL, Robustness, Tests | `KL_mbx_cdc.sv` timestamp take/send handshake: an additional send guard could reduce reliance on credit/ack ordering. If adopted, verify reordered credit/ack and throughput. |
| R883-1-S5 / SUGGESTION / Conformance, Robustness | `KL_mbx_rx.sv` shared admission bucket: consider per-interface isolation with #962 and test asymmetric flooding. No new second-MAC acceptance requirement is inferred here. |
| R883-2-S1 / SUGGESTION / RTL | TLV ternary after the early return in `gptp.c`: retained intentionally to bound the read when the refusal is mutated. Optional simplification must preserve meaningful missing-TLV plant failure. |
| R883-2-S2 / SUGGESTION / Docs | Publication README review-history wording: taken; now states the ordering and requirement. |
| R883-2-S3 / SUGGESTION / Docs, Tests | Receipt head binding: taken; `gates-334ca4b7/SUMMARY.txt:1` records its exact head and clean status. |
| R883-2-S4 / SUGGESTION / RTL, Robustness, Tests | `tb_cdc_pub.sv` randomized phase and datapath-only reset remain optional coverage extensions. If adopted, preserve atomicity and existing negative controls. |

## Executable evidence

The [published packet](https://github.com/kebag-logic/milan-fpga/tree/98bc6f22bc3c42bd78c1585b6e3bdca2018d25f1/review-evidence/gptpsw-r1/author-r4) supplies source-head execution evidence. `audit_packet.py` verified all 367 round-four files against its published SHA-256 manifest. The evidence commit has no `gpgsig`; no detached signature was located. This verifies content integrity against the pinned publication, not cryptographic authorship. Large logs/traces published only as hash references were not independently reconstructed.

Independent focused runs:

- `run_multi.py <checkout>` passes both original cases and the matching committed case. Running its sanitized binary without a filter passes 65 cases: 63 committed tests plus the two original probes.
- `probe_delta.py <checkout>`: the old port fails exactly eight current regressions; removing LocalClock correction fails six step tests; removing immediate invalidation fails three tests. These are assertion failures, not build/sanitizer errors. The old-port control compiles the previous C implementation with the current test/header interface.
- `probe_owner_gate.py <checkout>`: gate 1c passes and both owner-control plants are rejected, without source edits.
- `ctrl_hot.py --self-test`: two controls pass, ten plants caught.
- `audit_packet.py <checkout>` regrades the published data with the current egress checker: all seven held rows pass for both the gPTP and plain 8x8/1if images. The hot list exactly equals the published filtered order: 286 entries, including 15 gPTP entries.
- `git diff --check 59b09884..HEAD` is clean. `verify_checkout.py` proves raw tracked blob bytes, executable modes, indexes and the required submodule pins, with a clean working tree.

The relearn uses the authorized backlog, backlog-adp and aecp-largest-notice windows. The filter records 288 traced entries, dropping only the two previously unlinked AECP sections across 144 maps. LINKED exempts only wholly compiled-out gPTP objects and rejects an exemption for an object that actually links. The recorded trace hashes are retained; no held figure moved.

At executable-source-equivalent `631dc544`, ACMP is 62.45305 ms against 62.62 and AECP 62.12258 against 62.16. Pdelay turnaround is 0.30882/0.29195 ms at 1if/2if; last admitted gPTP record is 6.11505/7.75006 ms, below 10 ms. Composed maxima are 1.67518/1.65729 ms, below the 2 ms share. The public flood receipt retains all 490 delivered stamps, zero unstamped deliveries and zero lost egress records; lock is 2.9 s and worst later offset 95 ns. Its baseline is 48/48, with 14/14 plants caught. These are author-executed measurements checked against available receipts, not new reviewer bank runs.

Memory identities were remeasured: fixture state 1,104/2,152 B, platform state 20,160 B; allocations remain 59/64/62 RAMB36. Platform ROM/SRAM is 152,072/99,392 B. F1 concerns the two stale documented identities only.

The seven held rows still exceed nominal 20 ms budgets and use their separate ledger. No 2if ledger exists; five 2if owed rows exceed the 1if figures. Neither fact is represented as a clean nominal-budget result. Full builder, firmware, simulation and synthesis receipts stay attached to their actual run heads. Source comparisons confirm unchanged firmware/RTL/test inputs after `631dc544`, unchanged RTL after `a6323318`, and unchanged simulation bench/RTL after `e81cecdb`; explanatory text in `ctrl_memory.py` changed later. The final-head builder's ineffective MAKEFLAGS plant and absent physical calibration report are NOT RUN, not passes.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `gptp.c:314,523,530,758,805,918,928`; primary clauses, cease/resume, current suite and multi/step probes; public held-row rulings and egress regrade | R884-3 | 8267b8951616cfd570baf690835d4b0d38f14596 |
| RTL | CLEAN | `milan_datapath.sv:9469` tie-offs; `test_builder.py:11329,18069`; gPTP publication/LocalClock transitions and adapter; unchanged committed-bank crossing; public split-sw/census execution | R884-3 | 8267b8951616cfd570baf690835d4b0d38f14596 |
| Robustness | CLEAN | Current missing/late Follow_Up, duplicate identity, cease/resume and step-boundary tests; sanitized 65-case run; fault controls; hot-list plants; public flood | R884-3 | 8267b8951616cfd570baf690835d4b0d38f14596 |
| Tests | CLEAN | `gptp_mutants.py`, eight old-port failures, causal plants, owner gate controls, `ctrl_hot.py`, current egress checker, manifest and input-equivalence audits | R884-3 | 8267b8951616cfd570baf690835d4b0d38f14596 |
| Docs | UNCLEAN | GPTP_SOFTWARE.md, SPLIT_CONTROL_MEMORY.md:141/142, hot-list header, publication README/comments, current PR and dated receipts; F1 open, R1 residue only | R884-3 applied; no clean covering round | 8267b8951616cfd570baf690835d4b0d38f14596 |

## Limits and manager duties

This is a delta review, not fresh qualification of every unchanged line. No full parent, processor, gPTP, synthesis or builder bank was run by the reviewer. No hardware, physical calibration, workflow replica, source fix, commit, push or GitHub write was performed. No scoped RTL executable was run, so no new RTL execution or simulation-tool identity check is claimed. All mutation copies/builds are under packet scratch; parent and five initialized submodule bytes/modes/indexes are exact. The unrelated `external` gitlink remains uninitialized.

There is no manager source bank at this head. The manager owns hosted/workflow-replica acceptance, distinguishes executed jobs from skipped contexts, and validates the final current-dev merge candidate with required builder/native gates. Source base `59b098841b1e2826aaf7a38b557faa5345f91c82` and supplied live-dev reference `e275d7950ef3385753e6a15d2e191ba855b171ed` are distinct from this source head. No candidate or post-merge containment verdict is given here.

Resolve F1 and obtain focused Docs re-review; carry R1 to the residue checklist. Complete independent reviews and candidate validation before an authorized merge. The software-gPTP census shape remains owed before onward integration, second-MAC work remains #962, and bench qualification remains owed under #884. Physical calibration NOT RUN and field skips provide no hardware proof. Keep the plane buildable for A/B qualification and do not close #884 on this source review alone.

R884-3 FINISHED
