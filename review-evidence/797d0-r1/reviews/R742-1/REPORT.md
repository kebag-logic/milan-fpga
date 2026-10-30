[R742] NEGATIVE - exact head bd16b371ae5de1c4d36ea2a018e7d756c62d4b5a

PR #815, issue #797, external independent round R742-1. Base `1e80128f0a467b58bf884b7d9bf62e013a2fb141`; tree `3a039c9e8d8fc05fa9e54a3976edba9f84b21819`.

Three release-facing pages are incorrectly marked current despite factual contradictions omitted from the audit. These are missed D0 acceptance items. Record the contradictions and regenerate the inventory; product changes and area rewrites are not requested. The population, required negative controls, and 44 focused documentation checks passed.

F1 - MAJOR - Conformance, RTL, Docs - `docs/DOCUMENTATION_AUDIT.md:274`, `docs/integration/QSPI_FLASHBOOT.md:57` - Current verdict overlooks implemented persistence.

- Authority/evidence: the frozen D0 scope requires verification of release-facing statements and a finding for each contradiction. The flash-boot page says nothing reads or writes the reserved journal, the processor receives a blank-flash responder, and every restore returns zero records. `hdl/milan/KL_pp_shadow.sv:1123` instead instantiates `KL_nvm_backend`; `sw/firmware/milan_baremetal/milan_baremetal.c:1393` implements alternating-slot erase/program/verify, `:1669` reads both slots, and `:1890` invokes the boot path. See `source-excerpts.txt`.
- Impact: the generated audit certifies a materially false integration description and gives the following area no finding to repair it.
- Required outcome: record the exact contradiction, source evidence and correction in the findings data; regenerate the page with a stale status until corrected. Distinguish implemented persistence from outstanding physical qualification.
- Verification: compare backend wiring and firmware read/write paths, inspect the generated finding/status, and rerun inventory checks.

F2 - MINOR - Conformance, Tests, Docs - `docs/DOCUMENTATION_AUDIT.md:231`, `docs/guides/VERIFICATION_DEVELOPER.md:32` - Current verdict misses the aggregate test runner.

- Authority/evidence: the guide says standalone simulations lack an aggregate runner. `scripts/run_litex_sims.sh:98` defines the inventory and `:150` implements its aggregate, including missing/unlisted-member checks. Its `--list` was independently executed in `checks/044.log`. The guide already names this runner at line 22. Its adjacent claim at `:49` about no general C harness also needs qualification against the shared host firmware framework documented in `sw/firmware/gtest/README.md:4`.
- Impact: the audit misses a false statement about the available verification entry point and retains an unjustified current verdict on a specifically reviewed page.
- Required outcome: record the aggregate-runner contradiction and correct replacement. Accurately describe the existing host framework when addressing the adjacent firmware-harness claim. Regenerate the audit; no full guide rewrite is needed.
- Verification: compare the guide with the aggregate's inventory/dispatch and shared firmware test entry points; unresolved contradictory claims must not receive an unqualified current status.

F3 - MINOR - Conformance, RTL, Docs - `docs/DOCUMENTATION_AUDIT.md:302`, `docs/reference/EGRESS_QUEUE_MAP.md:38` - Current verdict misses swapped queue roles.

- Authority/evidence: the reset table assigns q3 to gPTP and q2 to class B. `hdl/common/ethernet_packet_pkg.sv:220-221` assigns `GPTP_CLASS=2` and `SRB_CLASS=3`. The reset mapping at `hdl/common/csr/milan_csr.sv:2008` agrees, as does the document's own slope table at lines 56-57.
- Impact: readers receive contradictory numeric queue assignments, and the audit fails to flag the page despite its release-facing verification claim.
- Required outcome: record the contradiction with q3=class B and q2=gPTP as its correction; regenerate the stale status. Preserve the distinction between retained generic blocks and the shipping datapath, which does not instantiate them.
- Verification: compare both tables with the enum/reset mapping and inspect the generated finding/status. No RTL change is needed.

R1 - RESIDUE - Conformance, Docs - `scripts/docs_inventory.py:83` - New source comment names a workflow label.

- Authority/evidence: the supplied owner comment rule forbids new lane labels in source comments and classifies them as RESIDUE. Lines 83-84 describe the pages the D0 lane verified.
- Impact: source-comment wording only; no behavior, measurement or privacy change.
- Exact fix: replace both lines with `#: Release-facing pages covered by the initial verification pass required by #797.`
- Verification: inspect the replacement and rerun normal documentation checks. This does not unclean a lens.

The independent verdict and ledger were written before fetching any issue/PR comments. Subsequent reconstruction of the [frozen D0 plan](https://github.com/kebag-logic/milan-fpga/issues/797#issuecomment-6518880512), [Ethernet scope addition](https://github.com/kebag-logic/milan-fpga/issues/797#issuecomment-6489587365), takeover and [source evidence statement](https://github.com/kebag-logic/milan-fpga/issues/797#issuecomment-6520032538) confirmed this scope. This final report corrects preliminary line locators without changing the verdict/findings. At retrieval there were two PR review-start comments, zero submitted reviews and zero inline comments. No prior public findings existed to resolve or retain; no other reviewer report was opened.

The scope addition's assertions that the PHY reset is gated and nobody writes link status conflict with the implementation. Both conflicts are public in the author handoff. The SoC exports the guard without consuming it; firmware does publish link status. The proposed findings appropriately record the source behavior. Resolving actual PHY gating remains separate work. The register-map completeness gate belongs to the following reference work under the frozen plan. Submodule audits, new module READMEs, the start-here rewrite and later branch synchronization are also separate work.

| Independent check | Result / receipt |
|---|---|
| Tracked population | Exact set of 210 Markdown/README paths and every row's line count agree; submodule interiors excluded. `inventory-probes.log` |
| Inventory fields | Area grouping, audience/purpose extraction or mappings, described source/spec fields, status/evidence, generated marker and self-row count inspected. Exact render check passes. |
| Required mutations | Hand-edited audit, edited data-file finding quotation, changed source quotation, and added source-page line each return rc 1. Restored copy returns rc 0. |
| Missing dependencies | Inventory, document and feature-status gates pass both in a metadata-free archive and in a Git checkout without initialized submodules. |
| Area export | 6 overview/guide findings and 17 reference findings. |
| Focused gates | 44/44 commands rc 0. `checks.tsv` maps commands to raw logs/rc files. Includes style, paths, anchors, contents, archive, privacy, feature status, bare-metal scope, diagrams, inventory, workflow consistency and language hygiene. |
| Controls | Inventory 21; workflow contract 2,207 items / 5,270 arms; em-dash 339 arms, zero findings over 470 added lines. |
| Three corrections | The replacement simulation exists; media following is implemented in the live selection path; the closed #599 has dated link-cycle acceptance evidence. Source excerpts retained. |
| Held pages | No changes to the supplied held-page list or diagrams. No product RTL, firmware, configuration or gitlink delta. |
| Privacy | Zero gate findings across 210 Markdown files and 1,425 scrubbed text files. Added text inspected: no new private host/device identity, external test-plan identifier or assistant identity. R1 records the source-comment label. |

Freshness limit: changing the integration guide's 50 MHz claim to 99 MHz while preserving its line count and rendered fields still returns rc 0. The retained probe demonstrates generated-metadata consistency rather than semantic re-verification of arbitrary edits. The workflow comment's broad claim about edited documents has this limit. Required stale-page and edited-quote controls work; this limitation is not the basis of the negative verdict.

`sampling.md` records twenty source/public-state checks of the 23 findings and twelve current-page samples. All 23 quotations were independently located. The three clause-only findings D0-006/007/008 were not independently rederived from licensed standards. README and FR_NFR were checked through their recorded stale findings. Sampling is not a claim that every sentence was independently verified.

Reviewer-owned ledger:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1-F3 | Issue and frozen scope; requirements; inventory/data; 210-row census; twenty finding checks; twelve current-page samples | R742-1 | bd16b371ae5de1c4d36ea2a018e7d756c62d4b5a |
| RTL | UNCLEAN: F1,F3 | Complete diff; persistence backend/writer; queue enum/reset map; guard decode; placement/media wiring; three corrections | R742-1 | bd16b371ae5de1c4d36ea2a018e7d756c62d4b5a |
| Robustness | CLEAN | Generator population/quoting/status; malformed-data controls; real stale/edited-quote probes; archive/absent-submodule checks and restoration | R742-1 | bd16b371ae5de1c4d36ea2a018e7d756c62d4b5a |
| Tests | UNCLEAN: F2 | Inventory controls; workflow/template and contract pin; 44 focused executions; aggregate dispatch and shared firmware harness | R742-1 | bd16b371ae5de1c4d36ea2a018e7d756c62d4b5a |
| Docs | UNCLEAN: F1-F3 | Generated audit, all finding quotations, release-facing samples, corrections, public evidence and privacy checks | R742-1 | bd16b371ae5de1c4d36ea2a018e7d756c62d4b5a |

[R742] PASS Robustness - `scripts/docs_inventory.py:186`, `:556`, `:659`; `inventory-probes.log`; `checks/025.log` - population, stale verdicts, edited quotations, malformed data and absent-submodule behavior checked against the generation/freshness contract. This does not certify semantic completeness of the audit findings.

Source execution evidence is the [published author packet](https://github.com/kebag-logic/milan-fpga/tree/86b070d2e790153c57444a709e8fd26183502f0c/review-evidence/797d0-r1), whose exact-head summaries record 96 rc-zero commands. Selected raw receipts and both summaries are retained in `published-author/`. The public handoff explicitly excludes SDK, compiler-absent and full builder execution. Those receipts and this review's 44 checks do not establish an executed complete hosted workflow. No manager source bank exists at this head, and none is inferred. Hosted jobs were not inspected; skipped contexts are not counted as execution.

No full product banks, hardware, physical calibration, host-side workflow orchestration, source fixes, commits, pushes or GitHub writes were performed. Dependencies and disposable trees stayed in packet scratch storage. `tree-integrity.log` proves all 1,449 root tracked blobs and all tracked blobs in five initialized dependencies: exact bytes, file kinds, executable modes, indexes and expected gitlinks. The optional external dependency remains uninitialized at its recorded gitlink.

Pending manager duties: obtain corrected findings and re-review affected lenses; collect the other independent verdict; carry R1 to the residue checklist; resolve the public guard-contract question in its proper work item; validate the final current-dev merge candidate with required builder/native and local/hosted evidence; distinguish executed jobs from skipped contexts; obtain merge authorization and run containment. Physical calibration remains NOT RUN; field skips are not hardware proof. This PR does not complete or close the overall documentation sweep.

R742-1 FINISHED
