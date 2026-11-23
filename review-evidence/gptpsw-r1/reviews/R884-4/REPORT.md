[R884] POSITIVE - exact head 165476c755e4728a044c12ea6bc33ce0a0a9d28f

R884-4: external independent documentation-delta review of issue #884 / PR #966.
Tree: `7d5ec9042ef3db671fe66b143b158a0b3fb2b7ff`.

The three requested documentation findings are resolved. No new BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION was found in this delta. The prior source-comment residue remains open and nonblocking under the owner's rule.

## Scope and authority

All five lenses were independently applied to the delta from `8267b8951616cfd570baf690835d4b0d38f14596`. Only `docs/design/GPTP_SOFTWARE.md` and `docs/design/SPLIT_CONTROL_MEMORY.md` changed. Every source, test, budget, linker-layout and submodule entry equals the previously reviewed head. The owner's later-round rule preserves coverage of unaffected implementation; this is not a new full implementation review or source-bank run.

Context came from AGENTS.md, CONTRIBUTING.md, docs/README.md, [issue #884](https://github.com/kebag-logic/milan-fpga/issues/884), its public scope decisions, REQUIREMENTS.md, FR_NFR.md, and the affected design/interface descriptions. Relevant decisions are [the harness invariant](https://github.com/kebag-logic/milan-fpga/issues/884#issuecomment-6794236611), [firmware ownership and memory debt](https://github.com/kebag-logic/milan-fpga/issues/884#issuecomment-7067495546), [admission and second-MAC scope](https://github.com/kebag-logic/milan-fpga/issues/884#issuecomment-7072401468), and [the hot-list relearn](https://github.com/kebag-logic/milan-fpga/issues/884#issuecomment-7084113326). No acceptance condition or memory limit changes here.

The overall source range is `59b098841b1e2826aaf7a38b557faa5345f91c82..165476c755e4728a044c12ea6bc33ce0a0a9d28f`; its inventory and history are recorded in `source-diff-stat.txt` and `source-history.txt`. The reviewed round delta is `delta.diff`. Prior public findings were consulted only after the independent delta pass. Other reviewers' complete reports were withheld until this verdict and ledger were written.

## Named prior findings

| Finding | Disposition | Cause and verification at this head |
|---|---|---|
| R883-3-F1, MINOR, Docs | RESOLVED | `SPLIT_CONTROL_MEMORY.md:141` and `:142` give `image_gptp` as 1,104 and 2,152 B. All six table entries' keys, symbol sizes and limits match `sw/litex/ctrl_memory.py:269` and `sw/litex/ctrl_memory_ledger.py:46` / `:74`; see `audit.log`. |
| R884-3-F1, MINOR, Docs | RESOLVED | The same corrected rows identify the executable exceptions accurately after eight bytes of `local_off` growth per port (`sw/firmware/ctrl/gptp/gptp.h:181`). Limits stay 59.0 and 64.0 RAMB36; the platform symbol stays 20,160 B at 62.0. Published memory checks agree. |
| R883-3-F2, MINOR, Docs | RESOLVED | `GPTP_SOFTWARE.md:153-155` states that plain images exclude the firmware gPTP owner, while the shared relearn changes both layouts. It names the measured revisions and actual ROM growth. `ctrl_plat_image.py:168` conditionally adds the owner; the shared linker order changes in `631dc544`. The before/after receipts agree with every new numeric claim. |

The original and republished `plat_ledger.py` receipts give:

| Plain platform point | ROM at `a6323318` | ROM at `631dc544` | SRAM, unchanged | RAMB36, unchanged | `ctrl_plat`, unchanged |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | 126,632 B | 126,640 B | 56,800 B | 45.0 | 18,112 B |
| 8x8/2if | 140,952 B | 140,960 B | 115,568 B | 63.0 | 21,568 B |

The surrounding table at `SPLIT_CONTROL_MEMORY.md:701` agrees. Since measured image head `631dc544`, the only non-document change is the platform ledger's explanation string updating its ROM figures from 12,656/152,064 to 12,664/152,072 B. The exact string-only difference was checked; image-building code and ledger keys/limits are unchanged since that measurement.

## Earlier findings and optional suggestions

After writing this independent verdict and ledger, the prior disposition sections and ledgers were checked in [R883-3](https://github.com/kebag-logic/milan-fpga/pull/966#issuecomment-7092027305) and [R884-3](https://github.com/kebag-logic/milan-fpga/pull/966#issuecomment-7092139737). Both covered Conformance, RTL, Robustness and Tests clean at `8267b8951616cfd570baf690835d4b0d38f14596`; only the documentation findings addressed here remained unclean. These earlier dispositions stand under the owner's delta rule, supported by exact source/test identity, not rerun probes.

| Prior finding | Disposition at this head | Unchanged cause-level artifact / evidence |
|---|---|---|
| R884-1-F1 | RESOLVED, retained | `hdl/milan/mailbox/KL_mbx_cdc.sv:486`, committed-bank publication, corresponding host model and crossing tests. |
| R884-1-F2 | RESOLVED, retained | `sw/firmware/ctrl/gptp/gptp.c:627`, deadline renewal by consumed Sync/Follow_Up pair, pending-pair expiry and regressions. |
| R884-1-F3 and R884-2-F1 | RESOLVED, retained | `gptp.c:314`, immediate capability invalidation for a second clock, identity counting, in-flight/completed exchanges and cease/resume regressions. |
| R884-1-F4 | RESOLVED, retained | `gptp.c:728`, mandatory information-TLV refusal before use and malformed/truncated-input regressions. |
| R884-1-F5 | RESOLVED, retained | Public `author-r4/receipts/gates-334ca4b7/SUMMARY.txt` and syntax receipt; prior review distinguished 142 analyzed files from NOT RUN. No new execution claim here. |
| R883-1-F1 and R883-2-F1 | RESOLVED, retained | `gptp.c:523`, LocalClock conversion, accumulated unsigned steps and old-exchange invalidation; step-boundary regressions unchanged. |
| R883-1-F2 | RESOLVED, retained | `tb/verilator/milan_dp/Makefile`, split-sw scheduling and prior sweep evidence; no scheduling delta. |
| R883-1-F3 | RESOLVED, retained | `docs/design/GPTP_SOFTWARE.md` Memory section still dates software routes to `a6323318`, plane comparison to `40bd7738`. No post-relearn route claimed. |
| R883-1-F4 | RESOLVED, retained | `sw/firmware/ctrl/gptp/gptp.h` and design page still specify three callbacks, time entering through tick. |
| R883-2-F2 | RESOLVED at source, retained | `hdl/milan/milan_datapath.sv:9469`, one no-plane PHC tie-off block; `sw/builder/test_builder.py:18069`, software-owner opt-in; predicates unchanged. Hosted acceptance stays with the manager. |
| R884-2-F2 and R883-2-R1/R2 | RESOLVED, retained | `tb/verilator/mbx/tb_cdc_pub.sv:18` and `cdc_pub_mutants.py:48` describe committed-bank ordering and REQ-PTP-07. The hot-list residue below is separate. |

Earlier suggestions remain optional and do not leave lenses unclean. Different prior lens labels are retained as their union.

| ID / severity / all attributable lenses | Artifact, disposition, impact, optional outcome and verification |
|---|---|
| R883-1-S1 / SUGGESTION / Robustness, Tests | `gptp.c:186`: TAKEN, retained. Empty-path memory calls remain guarded; prior sanitized checks stand. |
| R883-1-S2 / SUGGESTION / Conformance, RTL, Tests | `milan_datapath.sv` owner parameters: RETAINED. An exclusivity assertion could protect direct instantiations outside builder guards. If adopted, conflicting owners must fail and supported shapes pass. |
| R883-1-S3 / SUGGESTION / RTL, Tests | `milan_datapath.sv` publication decode: RETAINED. Generated field constants could prevent drift. If adopted, compare the contract fields and run split-sw. |
| R883-1-S4 / SUGGESTION / RTL, Robustness, Tests | `KL_mbx_cdc.sv` timestamp take/send handshake: RETAINED. Another send guard could reduce dependence on credit/ack ordering. If adopted, check reordered credit/ack and throughput. |
| R883-1-S5 / SUGGESTION / Conformance, Robustness | `hdl/milan/mailbox/KL_mbx_rx.sv` shared bucket: RETAINED. Consider per-interface isolation with #962 and verify asymmetric flooding. No new second-MAC acceptance requirement. |
| R883-2-S1 / SUGGESTION / Docs, RTL | `gptp.c`, guarded ternary in `rx_follow_up`: RETAINED for bounds safety when refusal is mutated. Optional simplification must preserve meaningful missing-TLV plant failure. |
| R883-2-S2 / SUGGESTION / Docs | `tb/verilator/mbx/README.md:53`: TAKEN, retained. Ordering and requirement replace review-history wording. |
| R883-2-S3 / SUGGESTION / Docs, Tests | `author-r4/receipts/gates-334ca4b7/SUMMARY.txt`: ADDRESSED by the enclosing head-bound receipt. Inline head identity in future logs remains optional for easier detached-copy auditing. |
| R883-2-S4 / SUGGESTION / RTL, Robustness, Tests | `tb/verilator/mbx/tb_cdc_pub.sv`: RETAINED. Random clock phase and destination-only reset could widen coverage. If added, preserve atomicity and existing negative controls. |

## Retained residue

**R884-3-R1 / R883-3-R1 | RESIDUE | Docs**

Artifact: `sw/firmware/ctrl/plat/ctrl_split_hot.txt:9`, `:16`, `:21`.

Authority/evidence: the owner's source-comment rule excludes issue-comment identifiers. These unchanged comments retain `issuecomment-7084113326`, `issuecomment-6959600243`, and `issuecomment-6967930396`. This round adds no source comment.

Impact: wording only; no entries, trace hashes, procedure, measurements, verdicts or conformance claims change. Docs remains clean under the owner's residue rule.

Required outcome / exact fix: remove `issuecomment-7084113326: ` at line 9, `issuecomment-6959600243, ` at line 16, and `issuecomment-6967930396, ` at line 21. Keep the issue numbers, dates, ruling items and behavioral explanations. The design page keeps the public links.

Verification: inspect the comment-only diff and run `ctrl_hot.py --check`; all 286 data entries and trace hashes must remain identical. Carry this item to the manager's residue checklist.

## Evidence and independent checks

The [public packet](https://github.com/kebag-logic/milan-fpga/tree/f4e3a75bea92d8eb0bae6fbaafabce6fcafccd5a/review-evidence/gptpsw-r1) was fetched by immutable commit. `audit.py` verified all 18 selected round-5 receipts against the manifest's published SHA-256 values. Both republished image logs are byte-identical to the original round-4 receipts. Selected manifest entries and raw public receipts accompany this report.

The supplied publication commit has no embedded signature; no detached signature appears at the supplied packet root. This proves commit-addressed receipt integrity and manifest agreement, not cryptographic signer authentication. No signature verification is claimed.

The author's focused memory receipt reports 150 assertions, all 16 planted ledgers and three mapper mutants caught. Its platform regrade reports five original images accepted and nine controls as required. The ELF artifacts are explicitly outside that public packet. These are published execution receipts, not new builds or independent ELF remeasurements here. `plat_ledger.py:132` checks LINK/KEY/TILES separately; controls at `:225` cover stale keys, insufficient limits and missing overrides. The raw logs were inspected against those checks.

| Independent check | Result | Raw receipt |
|---|---|---|
| `python3 -B audit.py <repo> <packet>` | PASS: two-file delta, six ledger identities, both comparisons, 18 hashes | `audit.log`, `audit.rc` |
| `python3 scripts/docs_check.py` | PASS: 0 findings, 23/23 scrub controls, 4/4 routing arms | `docs_check.log`, `docs_check.rc` |
| `python3 scripts/check_doc_style.py` | PASS | `doc_style.log`, `doc_style.rc` |
| `python3 scripts/check_doc_paths.py` | PASS | `doc_paths.log`, `doc_paths.rc` |
| `python3 scripts/docs_inventory.py --check` | PASS | `docs_inventory.log`, `docs_inventory.rc` |
| `python3 scripts/check_em_dash.py --base 8267b8951616cfd570baf690835d4b0d38f14596` | PASS: five added lines, 339/339 controls | `em_dash.log`, `em_dash.rc` |
| `python3 scripts/gen_toc.py --check` | PASS: 161 annotated pages | `toc.log`, `toc.rc` |
| `python3 -B verify_checkout.py <repo>` | PASS: tracked bytes, modes, index and submodule pins | `checkout-integrity.log`, `checkout-integrity.rc` |

`run_docs.py` runs six independent gates concurrently under one foreground coordinator. Renderer dependencies were installed only in disposable `scratch/`, using the repository's hash-locked requirements. The style gate's enumerated scope excludes these two design pages; its pass is not proof of their numerical claims. Those were checked separately. No test was weakened and no source edited.

## Reviewer-owned coverage ledger

These entries cover the bounded R884-4 delta. Unaffected implementation coverage stands under the owner's rule; RTL and Robustness do not claim fresh simulations.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #884 memory-debt and relearn rulings; `GPTP_SOFTWARE.md:153-155`; `SPLIT_CONTROL_MEMORY.md:141-142`; `audit.log`. Corrections preserve approved limits, owner selection and qualification boundaries. No clause claim changes. | R884-4 | 165476c755e4728a044c12ea6bc33ce0a0a9d28f |
| RTL | CLEAN | `delta.diff`; `ctrl_memory.py:269`; `ctrl_plat_image.py:168`; `checkout-integrity.log`. No RTL, CDC, reset, interface, linker or build-selection change since prior review. The corrected owner description matches conditional composition. | R884-4 | 165476c755e4728a044c12ea6bc33ce0a0a9d28f |
| Robustness | CLEAN | `ctrl_memory_ledger.py:74-132`; `plat_ledger.py:132-169`, `:225-255`; published `ledger_tests.log` and `plat_ledger_regrade.log`; `audit.log`. Corrected identities match exact-symbol and over-limit refusals; both interface counts and disabled-owner examples checked. No new failure path. | R884-4 | 165476c755e4728a044c12ea6bc33ce0a0a9d28f |
| Tests | CLEAN | `delta.diff`; `audit.py`/`audit.log`; `run_docs.py` and six gate logs; public before/after platform logs. Tests and controls unchanged, receipt provenance agrees, gates pass. Historical images are not relabeled as new builds. | R884-4 | 165476c755e4728a044c12ea6bc33ce0a0a9d28f |
| Docs | CLEAN | `GPTP_SOFTWARE.md:153-155`; `SPLIT_CONTROL_MEMORY.md:136-143`, `:697-708`; executable ledgers and image receipts; documentation gate logs. R883-3-F1/F2 and R884-3-F1 resolved at their causes. Only retained wording residue remains. | R884-4 | 165476c755e4728a044c12ea6bc33ce0a0a9d28f |

## Limits and pending manager duties

This is source-head review evidence. There is no manager source-bank run at this head, and none is inferred. The manager validates the final current-dev candidate, including builder and native banks, and links receipts at the merge turn. Source base: `59b098841b1e2826aaf7a38b557faa5345f91c82`; supplied live dev: `e275d7950ef3385753e6a15d2e191ba855b171ed`. This round neither constructs nor approves that candidate.

The manager owns hosted/local-workflow acceptance, the second independent positive review, confirmation that no review remains in flight, merge authorization, final candidate validation, post-merge containment and issue/project completion. Skipped contexts do not mean jobs executed; none was inspected or counted here. Physical calibration is NOT RUN. Field skips are not hardware proof. Bench qualification, physical accuracy, the second MAC and deferred census integration remain subject to the public scope decisions.

No full bank, hardware run, hosted run or local workflow replica was started. No GitHub writes, source fixes, commits, pushes, author contact, sub-agents, shared installations or other checkout changes occurred. The required four submodules and initialized `lwSRP` were verified against exact gitlinks and all tracked blob bytes/modes/index entries. The optional external gitlink remains uninitialized. Only manifest-listed files and this report are publishable; `scratch/` is excluded.

R884-4 FINISHED
