[R883] NEGATIVE - exact head 8267b8951616cfd570baf690835d4b0d38f14596

# R883-3: independent internal delta review of PR #966 / issue #884

All five lenses applied. The three named prior MAJOR findings are resolved at their causes. Two MINOR documentation findings remain, so Docs is UNCLEAN; Conformance, RTL, Robustness and Tests are CLEAN for this delta and its affected dependencies. One new source-comment RESIDUE is nonblocking.

Reviewed tree: `b8f11886504b95ab3f48d7553de8ef173d2a67cd`. Full PR context: `59b098841b1e2826aaf7a38b557faa5345f91c82..8267b8951616cfd570baf690835d4b0d38f14596`; this round's implementation delta: `8167b70d89d2a913a07c3b1187f4f2469109eebc..8267b8951616cfd570baf690835d4b0d38f14596`, nine commits and 18 files. Unaffected code retains its prior reviewed disposition; this is not a new full-bank or whole-PR execution claim.

## Findings

### R883-3-F1 | MINOR | Docs | Current memory-ledger table retains the pre-growth keys

**Artifacts:** `docs/design/SPLIT_CONTROL_MEMORY.md:141` and `:142`; `sw/litex/ctrl_memory.py:269`; `sw/litex/ctrl_memory_ledger.py:46`; `evidence-audit.log`.

**Authority/evidence:** AGENTS.md Docs requires changed contracts and measurements to agree with authoritative documentation. Issue #884's memory-debt ruling makes each image's measured ledger identity relevant. The current table explicitly identifies `ctrl_memory.LEDGERED` and still gives `image_gptp` as 1,096 B and 2,136 B. The LocalClock addition changes the actual keys to 1,104 B and 2,152 B. Both Python authorities and the published memory checks use those new keys; the adjacent platform row was updated to 20,160 B. This is a newly stale dependency of the reviewed 8 B state growth, not unrelated historical text.

**Impact:** a reader following the current refusal/override table gets incorrect image-identification values. The discrepancy concerns numeric measurements and the identity accepted by the memory gate, so it is MINOR rather than wording-only RESIDUE. The executable ledger is correct; no tile-limit increase or failed memory gate is alleged.

**Required outcome / exact correction:** change the one-interface table cell from `image_gptp` 1,096 B to 1,104 B, and the two-interface cell from 2,136 B to 2,152 B. Retain 59.0 and 64.0 RAMB36.

**Verification:** compare both rows against `ctrl_memory.LEDGERED`, `IMG_GPTP_1/2`, and the published `memory-631dc544/test_ctrl_memory-631dc544.log`. No new full memory bank is needed for this text correction.

### R883-3-F2 | MINOR | Docs | Byte-identical plain-image claim no longer survives the shared layout change

**Artifacts:** `docs/design/GPTP_SOFTWARE.md:153`; `sw/firmware/ctrl/plat/ctrl_split.ld:31`; `docs/design/SPLIT_CONTROL_MEMORY.md:702`; published `memory-631dc544/plat_ledger-631dc544.log` and `hotlist/gptp/kept.txt`.

**Authority/evidence:** the manager's [held-row ruling](https://github.com/kebag-logic/milan-fpga/issues/884#issuecomment-7084113326) authorizes a principled hot-list relearn. This delta changes the shared linker order in images with and without gPTP. The current design page nevertheless says that an image without the flag is byte for byte the one before. Later on the same page, the layout paragraph correctly says the relearn reorders the plain images too. The measured plain 1x1 platform ROM changes from 126,632 to 126,640 B, and plain 8x8/2if from 140,952 to 140,960 B; the shared function order also changes. These are the new measurements documented by this delta, not an inference that adding an optional feature necessarily changes a disabled build.

**Impact:** the design page asserts generated-image identity that the authorized change no longer preserves. This is an artifact/evidence claim, so it does not qualify as wording-only RESIDUE. No objection is made to the approved relearn itself.

**Required outcome / exact correction:** replace the final clause at line 153 with: `An image without the flag excludes the firmware gPTP owner. The shared hot-list relearn changes code layout in both image variants.` If a narrower identity claim is intended, name its precise compared revisions and artifact instead.

**Verification:** reconcile the sentence with the shared linker delta, the layout paragraph, and the plain-image measurements. Preserve the evidence's actual revision labels.

### R883-3-R1 | RESIDUE | Docs | New issue-comment IDs in source comments

**Artifact:** `sw/firmware/ctrl/plat/ctrl_split_hot.txt:9`, `:16`, `:21`.

**Authority/evidence:** the owner's source-comment rule forbids issue-comment IDs in newly added source comments. These added lines introduce `issuecomment-7084113326`, `issuecomment-6959600243`, and `issuecomment-6967930396`.

**Impact:** wording only. The ordered entries, trace hashes, measurements, rule and verdict do not change. This leaves the ledger unaffected.

**Required outcome / exact correction:** retain the issue numbers, dates, ruling items and behavioral explanation, but remove the three `issuecomment-...` tokens. At lines 8-9 use `#884's ruling of 2026-11-22: their paths measured into the list`; at lines 15-16 retain `#665's ruling of 2026-11-17, item 1`; at line 21 retain `#665's ruling of 2026-11-18, item 1`. Full public links can remain on the design page.

**Verification:** the parsed hot list and all three trace hashes remain identical; inspect the added comment lines. Carry to the manager's residue checklist.

## Prior findings: resolved or retained

Public prior findings were consulted after the independent pass over the current source delta. The following dispositions include both earlier reviewers' findings, rather than assuming that an author's fix label resolves them.

| Prior finding | Disposition at this head | Cause and evidence |
|---|---|---|
| R884-2-F1; affected multiple-response portion of R884-1-F3 | Resolved | `gptp.c:314` clears good-count and capability before distinct-clock counting or cease. `rx_pdelay_resp` routes both in-flight and completed requests through it. Independent `run_multi.py` passes missing-Follow_Up and completed control cases; the current suite additionally covers immediate invalidation, late Follow_Up, same-clock duplication, clean intervening requests, five-minute and link resume. The focused removal plant is killed. |
| R883-2-F1; retained part of R883-1-F1 | Resolved | `gptp.c:523` subtracts accumulated servo steps; all local/requester and reported/responder peer-delay timestamps use it. `pd_own_step` accumulates modulo 2^64 and voids the current exchange/owed response. Independent UBSan run passes 63 committed cases plus five extended matrix cases and the 144-row sweep; every sweep row has zero capability outage on both ports. Removing LocalClock correction is killed by the required own-step and five intermediate-step assertions. |
| R883-2-F2 | Resolved at source | `milan_datapath.sv:9470` is one no-plane tie-off block; the three original PHC knob counts stay 4/5/4. Five extra crossing-net references are attributed to the timestamp unit's read-only ports. Gate 1c requires the unique software owner inside `elif gptp_sw`, and the opt-in flag. The published exact-head full builder receipt passes, with two explicit NOT RUN arms. Independent bounded predicates pass controls and reject four extra-reference plants plus wrong-owner-branch, duplicate-owner and reversed-opt-in plants. Hosted acceptance remains the manager's duty. |
| R884-1-F1 publication tear | Remains resolved | `KL_mbx_cdc.sv` committed-bank capture/crossing, host model and crossing tests are unchanged from the last reviewed head; the tie-off delta does not affect them. Current sweep/split receipts retain their execution. |
| R884-1-F2 raw Sync renews deadline | Remains resolved | Pair-consumption deadline update, separate pending-Follow_Up expiry, selected-master handling and their tests remain intact. Fresh core suite passes; the LocalClock helper is confined to peer delay. |
| R884-1-F3 original late-second-response cease | Remains resolved | Interval classification and distinct clock identity counting are retained. Immediate clearing now also fixes the missing-Follow_Up extension. Fresh suite passes the early/late cease, clean interval, duplicate and resume cases. |
| R884-1-F4 missing/malformed Follow_Up information TLV | Remains resolved | Required TLV validation is unchanged; fresh suite passes absence, truncation and malformed-field cases. |
| R884-1-F5 skipped syntax check described as PASS | Remains resolved | Current PR names executed syntax checking and the two separate builder NOT RUN arms. Published `gates-334ca4b7/SUMMARY.txt` binds the syntax receipt to its actual head; 90 local and 52 pinned processor files were analyzed. No skip is counted as hardware proof. |
| R883-1-F2 split-sw omitted from gates | Remains resolved | Scheduling/Makefile unchanged; published sweep includes the integrated split software-owner case. |
| R883-1-F3 stale route figures | Remains resolved | Page now names `a6323318`; three route receipts give +0.292/+0.036, +0.281/+0.036 and +0.173/+0.067 ns. The actual routed image is distinguished from the post-relearn firmware. |
| R883-1-F4 three-call HAL | Remains resolved | HAL, design page and PR each describe send/rate/step; tick supplies time. |
| R884-2-F2 and R883-2-R1/R2 | Resolved | Crossing source comments now describe live-word tearing and REQ-PTP-07; the mutation tuples and bench behavior did not change. The new hot-list residue above is separate. |

Prior optional suggestions remain optional, without reopening clean lenses:

| ID / severity / lenses | Artifact and disposition | Impact, optional outcome and verification |
|---|---|---|
| R883-1-S1 / SUGGESTION / Robustness, Tests | `gptp.c:186`, already taken | Empty-path memory calls remain guarded; UBSan baseline passes. |
| R883-1-S2 / SUGGESTION / Conformance, RTL, Tests | `milan_datapath.sv` owner parameters, retained | A direct-RTL exclusivity assertion would protect instantiations outside builder guards; if added, reject conflicting owners and accept supported shapes. |
| R883-1-S3 / SUGGESTION / RTL, Tests | `g_gptp_sw` field decoding, retained | Generated field constants would reduce future drift; verify correspondence to the unchanged mailbox contract and split-sw behavior. |
| R883-1-S4 / SUGGESTION / RTL, Robustness, Tests | `KL_mbx_cdc.sv` timestamp credit path, retained | Explicit take gating could reduce reliance on credit/ack ordering; any change needs reordered-credit and throughput checks. No change to that path here. |
| R883-1-S5 / SUGGESTION / Conformance, Robustness | `KL_mbx_rx.sv` shared admission bucket, retained | Per-interface admission could isolate asymmetric flooding when #962 adds a physical MAC; verify isolation then. No new acceptance requirement imposed here. |
| R883-2-S1 / SUGGESTION / Docs | `rx_follow_up` guarded ternary, retained | Simplification is optional; the author retains defensive bounds behavior for a refusal-removal plant. No executable defect identified. |
| R883-2-S2 / SUGGESTION / Docs | `tb/verilator/mbx/README.md:53`, taken | The ordering and requirement replace review history; meaning is preserved. |
| R883-2-S3 / SUGGESTION / Docs, Tests | Syntax receipt head attribution, addressed by enclosing receipt | The summary names `334ca4b7`; the individual syntax log still relies on that association. Keeping an inline head in future logs would make detached copies easier to audit. |
| R883-2-S4 / SUGGESTION / RTL, Robustness, Tests | `tb_cdc_pub.sv`, retained | Random clock phase and destination-only reset would widen testing; no current delta changes its clock/reset contract. |

## Independent checks and published evidence

Reconstruction used AGENTS.md / CONTRIBUTING.md, docs/README.md, #884's body and public decisions, REQUIREMENTS.md, FR_NFR's firmware/service rules, the gPTP software design, HAL, mailbox publication and register-map authorities, then the specified diff/history. The local final editions of IEEE 802.1AS-2020 (10.2.5.1, 11.2.2, 11.2.19.3.3/.4), IEEE 802.1AS-2011 and Milan v1.2 (4.2.6.2.4-.6) were consulted; `standards.sha256` identifies them. A web lookup was not used as a substitute for those final standards. The immediate multiple-response rule is specifically 11.2.2(c), with 10.2.5.1 defining asCapable.

The LocalClock correction is applied symmetrically at every own and reported Pdelay timestamp conversion. It does not change Sync time. Existing HAL semantics require steps to apply to later timestamps; the in-flight cancellation prevents old timestamps completing the canceled transaction. State initialization zeroes the offset, and link changes retain it because the physical PHC was not reset by a link edge. The unchanged adapter publishes dirty capability/GM/verdict state in the receive callback's service pass. No new CDC, mailbox offset, routing or timestamp-correction ownership is introduced by this delta.

| Review execution | Result / receipts |
|---|---|
| `python3 -B run_focused.py CHECKOUT` | 212 UBSan tests pass: 63 current tests, five extended matrix tests, 144 sweep rows. The driver separately asserts both ports' outage is zero on every sweep row. `steps.log`, `steps.rc`. |
| Public `run_multi.py CHECKOUT`, invoked by that driver | Both prior probes pass; three multi-response requests clear capability on the first second response and remain clear through cease. `multi.log`, `multi.rc`. The current suite adds a third matching test under the script's wildcard. |
| `python3 -B run_plants.py CHECKOUT` | Normal/UBSan baselines each pass 63 tests. Both selected causal mutants are killed by every assertion named in their current campaign definition. `plant-*.log`. |
| `python3 -B check_guards.py CHECKOUT` | Exact-source census and gate-1c predicates pass controls and catch all seven text plants. `guards.log`. This is a bounded predicate check, not the full builder bank. |
| Current `ctrl_hot.py --self-test` | Both controls pass; all ten plants caught, including falsely exempted linked objects and unrelated missing entries. `hot-plants.log`. |
| `python3 -B audit_evidence.py CHECKOUT` | All 367 author-r4 files match the published SHA-256 manifest; unchanged-source claims independently checked with Git; hot-list order equals published kept order. `evidence-audit.log`, `public-packet-hashes.txt`. |
| Current `egress_ledger.py --point 8x8-1if` on each published JSON set | Both gPTP and plain pass all seven held rows; 59 measured instances each. `egress-gptp.log`, `egress-plain.log`. This regrades published measurements; it does not rerun the CPU simulation. |
| `python3 -B verify_integrity.py CHECKOUT` | All 1,962 parent blobs plus five required submodule populations match pinned bytes, modes and stage-zero indexes. Exact requested tree, clean status. `integrity.log`. |

Independent focused campaigns ran concurrently, with their foreground driver awaited; the maximum campaign concurrency was three, within the 16-job and 12 GB limits. No source files or index entries were changed by a probe. No RTL compiler was needed for these focused reruns, and no full parent/processor/gPTP/portability/builder bank was run by this review.

Published evidence is pinned to [98bc6f22](https://github.com/kebag-logic/milan-fpga/tree/98bc6f22bc3c42bd78c1585b6e3bdca2018d25f1/review-evidence/gptpsw-r1), principally `author-r4`. Selected raw receipts are retained under `published-receipts/`; their original published hashes are listed separately. These are author executions, not a manager source bank:

- Full simulation sweep at `e81cecdb`; synthesis portability and routes at `a6323318`; firmware shards, memory and CPU measurements after relearn at `631dc544`; syntax/light gates at `334ca4b7`; full builder at the exact requested head. Source-equivalence checks preserve those distinctions. The published firmware mutation tally is 826/826; full port campaign 41/41. Only the two causal port plants were independently rerun here.
- The exact-head builder driver contains 113 gate entries with pass verdicts and two explicit NOT RUN arms: an ineffective MAKEFLAGS plant and an unavailable physical calibration report. Their absence supplies no execution evidence for those arms.
- Seven held gPTP 8x8/1if rows are within unchanged figures, including ACMP 62.45305 <= 62.62 ms and AECP 62.12258 <= 62.16 ms. Plain AECP is 61.84002 ms. No figure or approved service limit moved.
- Turnaround is 0.30882 ms at 1if and 0.29195 ms at 2if; final admitted record 6.11505/7.75006 ms; composed maxima 1.67518/1.65729 ms. Published audit has no share misses or refusals. The 2if comparison is explicitly not a pass against an approved 2if ledger.
- Fresh closed-loop receipt at `334ca4b7` reports 48 checks, zero failures; the flood delivers 490 stamped records, zero unstamped or lost egress records, locks at 2.9 s, and stays within 95 ns afterward. Its 14 plants are reported caught. This is simulated timestamp/mailbox evidence, not physical calibration.
- The relearn's three recorded windows yielded 288 sections; excluding precisely `aecp owe` and `aecp owed_drain` yields the 286 committed entries, including 15 gPTP entries. No hand reorder is evident between published order, filtered order and committed list. The absent-object exception is tied to actual compilation and refuses any linked section of an allegedly absent object. The measured symbols are 1,104/2,152 B and 20,160 B; tile entries stay 59/64/62. The platform five-point receipt and nine controls pass. F1 concerns the remaining prose table only.

## Reviewer-owned coverage ledger

The exact head in every row is `8267b8951616cfd570baf690835d4b0d38f14596`. CLEAN denotes this delta, its affected dependencies, and carried prior clean dispositions, not a new execution of every repository gate.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `gptp.c:314,523,755,784,897`; final standard clauses above; #884 public rulings; `multi.log`, `steps.log`, unchanged contract and service limits | R883-3 | 8267b8951616cfd570baf690835d4b0d38f14596 |
| RTL | CLEAN | `milan_datapath.sv:9470`, PHC muxes/ports, `test_builder.py:11303,18097`; protocol state transitions and unchanged publication crossing; `guards.log` and published split/builder evidence | R883-3 | 8267b8951616cfd570baf690835d4b0d38f14596 |
| Robustness | CLEAN | `gptp.c` cancellation, timestamp conversion, cease/resume and link reset; `test_gptp.cpp:500,629,1232`; 144-row outage sweep, missing/late Follow_Up cases and causal plants | R883-3 | 8267b8951616cfd570baf690835d4b0d38f14596 |
| Tests | CLEAN | `test_gptp.cpp`, `gptp_mutants.py`, `ctrl_hot.py`, `ctrl_srp_image.py`, changed builder predicates; public memory, held-ledger, flood and regression receipts; independent bounded controls/plants | R883-3 | 8267b8951616cfd570baf690835d4b0d38f14596 |
| Docs | UNCLEAN: F1, F2 | `GPTP_SOFTWARE.md:153`, `SPLIT_CONTROL_MEMORY.md:141`; current PR body, handoff, memory/route/service receipts, source-comment delta | R883-3 (applied, not clean) | 8267b8951616cfd570baf690835d4b0d38f14596 |

## Limits and pending manager duties

The public manifest verifies content hashes. The evidence commit has no embedded cryptographic signature and no detached signing key/signature was supplied, so signer authentication is not claimed. Large raw CPU traces, PC traces and link maps are represented by hashes in the published packet rather than included bytes. Their digest identifiers and derived tables were reconciled; this review did not independently regenerate those omitted raw campaigns.

Source-head validation and current-dev merge-candidate validation remain separate. No manager source-bank run is claimed at this head. The manager still owns the eventual candidate built against live dev (the supplied tip is `e275d7950ef3385753e6a15d2e191ba855b171ed`), builder/native receipts for that candidate, hosted and act acceptance, both independent positive reviews, completion ledger, explicit merge authorization and containment. This review inspected no hosted jobs and treats no skipped context as an executed gate.

The two MINOR documentation findings need correction and re-review; untouched clean code need not be reopened merely for those text fixes. The new RESIDUE belongs on the manager's checklist. The census software-owner shape remains owed before onward integration, second physical MAC work remains #962, and bench slave/grandmaster A/B qualification remains owed before deleting plane RTL. Physical calibration is NOT RUN; field skips and simulated oscillator/PHY behavior are not hardware proof.

No source fix, commit, push, GitHub write, author contact, sub-agent, Docker/act invocation, shared installation, hardware action or other-checkout edit was performed. Only REPORT.md and MANIFEST.sha256-listed files are publishable; scratch is excluded.

R883-3 FINISHED
