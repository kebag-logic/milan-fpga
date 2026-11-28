[R958] NEGATIVE - exact head 4461d77ca34ec1203321821a3313071ff1923984

R958-5 applied all five lenses independently to `3256d1d21e525e564eb92d1cf721750ddf44fde2..4461d77ca34ec1203321821a3313071ff1923984` and the published author-r13 packet. Tree: `13f3c4bb69da311a9d3a30849348c4358e9bb28d`.

**F2 is resolved. F1 remains open until the owner answers.** The corrected extractor locates 44 registering records at 44 distinct **(group, receive-commit)** identities per point and excludes six transmit probes. The maxima and comparison measurements are unchanged. The 8x8/1if load is **0.7821365**, above the approved **0.77** ceiling and below the proposed **0.79**. The final ceiling commit is separate and reverses cleanly; that does not authorize the bound.

Reconstruction followed AGENTS.md/CONTRIBUTING.md, docs/README.md, frozen issue acceptance/public decisions, linked requirements/interfaces, the source-base diff inventory/history and narrow delta, then public executable evidence. The source base inspected was `dev-soft-core` at `0b5940237e8de8bd5912db87e5e036a78f59b5a6`. Authorities included REQUIREMENTS ownership, FR_NFR 3.4.1, SPLIT_CONTROL_MEMORY section 13, the delivery contract, and the population/delivery/alone-record/deferred-cost decisions. An independent verdict and ledger were written before reading prior review findings. No private author material or other checkout was accessed. Unchanged code retains its prior assessment except for dependencies the corrected measurement affects.

**R958-4-F1 retained - MAJOR - Conformance - `tb/verilator/ctrl_service_budget/flip_grade.py:68-71`, `docs/reference/FR_NFR.md:427`, final commit `4461d77c`: owner approval for 0.79 is still missing.**

- Authority/evidence: [decision 7229657853](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7229657853), items 3-4, requires the owner's published answer before merge. The [approved ceiling remains 0.77](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7213594113). The issue snapshot has 19 comments ending with the deferred-deliveries decision; the PR and source expressly say approval is pending. `model-probe.json` reproduces 0.7821365 at 8x8/1if and 0.5325402076023392 at 1x1/1if. The 0.77 check refuses the former. `delta-audit.json` records successful reverse-application checking of the final commit, whose parent is `48c7481a8f`.
- Impact: the candidate fails the currently authorized acceptance bound. This retains the authorization finding, without asserting a new firmware or measurement defect.
- Required outcome: publish the owner answer. If approved, cite it in the ceiling authority and requirement text. If refused, revert `4461d77c`, preserve the sourced delivery term, and retain the failing 8x8/1if status pending authorized margin work (#1025).
- Verification: reconcile the public answer, FLIP/RULED_FLIP, requirement text and resulting load. A citation-only correction needs no product rebuild. Do not merge while approval is pending.

**R958-5-R1 - RESIDUE - Docs - PR #993 Contents/Status summary: publication status is stale.**

- Authority/evidence: the live PR says, "the historical index notes remain to be published." Both `author-r10/receipts/SUPERSESSION-NOTE.md` and `author-r11/receipts/SUPERSESSION-NOTE.md` exist at evidence commit `63ebbbacee3d6c366274d0b756f86433a7588a30`; both hashes and all twelve mapped receipt paths verify.
- Impact: publication-status wording only; no measurement, figure, test, executable behavior, conformance claim or privacy rule changes. No lens becomes unclean.
- Exact fix: replace the sentence with "Code corrections are applied; the historical index notes are published beside the round-10 and round-11 receipt indexes." Link both notes. Preserve archived receipt/index bytes.
- Verification: read the updated PR summary and follow both links. The archived prepublication handoff may remain historical.

**Prior findings at their causes**

| Finding | Disposition | Examined evidence |
|---|---|---|
| R958-4-F1, Conformance | OPEN, retained above | Owner/manager decisions; FLIP/RULED_FLIP; failing 0.77 calculation; reversible last commit |
| R958-4-F2, Conformance/RTL/Tests/Docs | CLOSED | `author-r13/receipts/deliv13.py.txt:41-64,88-109,150-190`; both corrected measurement receipts; independent fault probe; unchanged maxima and floor/load checks |
| R958-4-R1, Docs | CLOSED | `load_grade.py:13,374-388`, `load_deliveries.py:3-6`, `flip_grade.py:66-67` replace the comment ID with the dated deferred-deliveries decision. Markdown authority links remain. No new forbidden source-comment identifier found. |
| R958-4-R2, Docs | Publication CLOSED; current-summary residue above | Both notes are beside their historical indexes. The r10 note covers approved 80 ms, reviewer placeholders, run-count qualification and default-option restore behavior. Both map compressed names to published paths and name MANIFEST.json as hash authority. |

Earlier closures in round 4 stand where this delta changes no dependency: the baseline/floor decision, malformed-ceiling and unknown-control adapters, neutral reviewer labels, cost-method wording/deliveries exception, and documented mutation population. No unrelated firmware, loss-turn, S14, routing or CDC/reset work is reopened. The internal POSITIVE at `3256d1d2` ([7230545660](https://github.com/kebag-logic/milan-fpga/pull/993#issuecomment-7230545660)) is prior-head evidence; it supplies neither the owner answer nor current-head external approval.

**F2 evidence and focused verification**

The corrected `records()` matches the exact receive tag on the SRP channel and cross-checks the harness start where present. `scenario.py:183-189` tags each frame; `register_window.py:172-182` assigns separate tags to queued records and makes the transmit probe reference the third record; `grade.py:371-380` uses the same explicit relationship. Missing, duplicate, wrong-channel and disagreeing-start inputs are refused. All six published exclusions per point are `srp.register_tx.*` probes.

The independent synthetic triple yields commits **10000, 20000, 30000** and shares **0, 500, 1250 cycles/sink**. Substituting the old first-commit mapping yields **0, 0, 0**, proving the later-window defect is detected. Four invalid associations are refused, and a truncated window is unmeasured. The author's eight extraction controls also pass (`extractor-probe.json`, `audit.log`).

Each corrected receipt contains **44 records in 20 group logs**, **44 distinct group/commit pairs**, and **six excluded aliases**. Timestamps belong to their logs, not one global run. Every row has an after-window sample population. Recomputing all three maxima from the printed per-record values reproduces the summaries; all DEAREST lines match author-r12's. See `extraction-receipt-audit.json`.

| Point | Accepted after-window maximum | Before 50 ms comparison | Before 500 ms comparison | Load at pin |
|---|---|---|---|---|
| 1x1/1if | 18,778 cycles/sink; 200 us | 18,076; 190 us | 18,765; 200 us | 0.5325402076023392 |
| 8x8/1if | 15,104 cycles/sink; 160 us | 11,573; 125 us | 13,642; 145 us | 0.7821365 |

The 8x8 maximum remains the answering-ports swap, after-median 12,089 cycles: 135,935 / 9 = 15,103.8889 cycles/sink, giving 160 us by the rule. The 1x1 maximum remains the both-kinds record with a change owed. No maximum or stated floor needs adjustment. Independent checks refuse 155 us at 8x8 and 195 us at 1x1. Against proposed 0.79, 0.790 passes and 0.791 fails.

| Check | Result and limit |
|---|---|
| Published packet | All 28 current-packet/note entries match MANIFEST.json `published_sha256`; all twelve supersession target paths also match. `packet-integrity.json`, `supersession-links.json`. |
| Signature | The exact evidence commit has no signature header; public verification says `verified: false`, `reason: unsigned`. Hash integrity is established; a cryptographic packet signature is **not established**. `packet-signature.json`. This carries the previous limitation. |
| 80 product ELFs | Both complete maps in the exact-head identity receipt contain **80/80 matching SHA-256 pairs against 25ff0632**, comprising 72 harness and eight platform paths. Verified published build receipt, not a new build or direct rehash of unavailable binaries. `elf-identity-audit.json`. |
| Source delta | Four changed files, three commits. No firmware, RTL or gitlink change since `3256d1d2`. Three changed Python modules have equal executable ASTs after excluding docstrings. `delta-audit.json`. |
| Independent gates | Load check, load self-test **32/32**, delivery controls, both held-point flip checks, flip self-test **628/628**, source-base diff whitespace check: all rc 0. Commands/logs/rc files accompany `checks.json`. |
| Author source-head receipts | Exact-head harness, shape/kept and documentation receipts verified. Documentation receipt reports 100 steps with rc 0; its no-Git fixture explicitly skips inventory parity. These are author receipts, not a manager source bank. |
| Source preservation | **1997 parent blobs and 1377 blobs across five required submodules** match committed bytes, modes, indexes and HEADs. Required gitlinks match; optional external gitlink preserved/uninitialized. Exact tree retained and status clean. `checkout-integrity.json`. |

**Reviewer-owned lens ledger**

[R958] MAJOR Conformance - decision 7229657853; `flip_grade.py:68-71`; `model-probe.json` - corrected measurement/rate/floor arithmetic holds; F1 alone prevents acceptance at the approved ceiling.

[R958] PASS RTL - `delta-audit.json`; `elf-identity-audit.json`; `load_grade.py:374-389`; corrected extraction receipts - no runtime/interface/placement/pin change; complete corrected measurement closes F2's resource-cost dependency. Unaffected implementation coverage carries forward.

[R958] PASS Robustness - published `deliv13.py.txt:41-85,150-190`; `extractor-probe.json`; `model-probe.json` - invalid associations and truncated windows cannot provide accepted measurements in the exercised controls; floors and ceiling edges behave as stated. Unchanged product robustness coverage carries forward.

[R958] PASS Tests - `register_window.py:172-182`; `grade.py:371-380`; extraction receipts; queued-triple/old-mapping probe; `checks.json` - tag associations/exclusions agree, the old defect is detected, maxima reconcile and focused gates pass. The 0.79 result remains explicitly conditional on F1's authorization.

[R958] PASS Docs - `SPLIT_CONTROL_MEMORY.md:2548`; `load_grade.py:374-389`; authority links; both supersession notes; PR snapshot - association, baseline, maxima and pending ceiling are stated; F2's unsupported completeness claim is repaired. Publication-status wording is RESIDUE only.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN - F1 | Public decisions; FR_NFR:427; rate/floor/model checks | R958-5 applied; no clean covering round | 4461d77ca34ec1203321821a3313071ff1923984 |
| RTL | CLEAN | Runtime/gitlink delta; 80-path identity; corrected delivery-cost evidence | R958-5, retaining unaffected implementation coverage | 4461d77ca34ec1203321821a3313071ff1923984 |
| Robustness | CLEAN | Invalid-association/truncation probes; floor/edge controls | R958-5, retaining unaffected prior coverage | 4461d77ca34ec1203321821a3313071ff1923984 |
| Tests | CLEAN | Extractor, queued-record mutation, measurement tables, focused gates | R958-5 | 4461d77ca34ec1203321821a3313071ff1923984 |
| Docs | CLEAN | Corrected method/maxima; decision links; supersession notes | R958-5; publication-status residue remains | 4461d77ca34ec1203321821a3313071ff1923984 |

**Limits and pending manager duties**

Full CPU traces/group JSON and ELF binaries are absent from the published packet. This review checks extraction logic, published per-record and identity receipts, and focused fault controls; it claims no fresh product simulation, raw-trace re-extraction or independent build. No broad bank, scoped simulator, hardware, privilege, source edit, commit, push, GitHub write or merge occurred. Physical calibration is **NOT RUN**; field skips are not hardware proof. Hosted jobs were not audited in this narrow pass; no skipped context is treated as executed.

The manager must publish the owner answer, reconcile the citation or revert, carry R958-5-R1, and complete the independent-review bar. Hosted/local-replica acceptance remains the manager's duty. At merge time, build and validate the actual then-current `dev` candidate with required builder/native banks and link receipts. Supplied live `dev` is `e275d7950ef3385753e6a15d2e191ba855b171ed`; source-head evidence against `dev-soft-core` does not validate that future candidate. Explicit merge authorization, containment and issue/project completion remain separate duties.

Reproduce from the exact clone using `python3 -B <packet>/audit.py`, `python3 -B <packet>/run_checks.py`, and `python3 -B <packet>/verify_checkout.py`, with the public evidence commit available locally. Checks remain attached; at most four lightweight checks run concurrently. Disposable/extracted files stay under `scratch/`. Only files in MANIFEST.sha256 and this report are publication artifacts; scratch is excluded.

R958-5 FINISHED
