[R503] POSITIVE - exact head ad670a71b4d2f38f59672d51d8309d59ffed0808

Issue #42 / PR #164, round R503-2. Tree `224aadfa2ffc348ad3123bd4580b573a7d97c098`; source base `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8`. All five lenses are CLEAN. Both prior timing defects are resolved. No open BLOCKER, MAJOR, MINOR or RESIDUE was found. Two prior SUGGESTION items remain optional.

Reconstruction followed the requested order: supplied workspace instructions; repository guidance and `docs/README.md`; [issue #42](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/42), [frozen assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/42#issuecomment-6008771904) and [round-2 scope](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/42#issuecomment-6011607356); linked requirement/interface authorities; the complete base-to-head diff and history; then public evidence. No tracked AGENTS.md or CONTRIBUTING.md exists at this head. The [independent verdict and ledger](receipts/independent-verdict.md) were written before opening either prior public report; [ordering receipt](receipts/independence-order.json).

The author's round-2 commit `9be9cd7a` changes documentation and comments only. Its preceding two-parent merge incorporates main `7e5415e0` (#134). The published head's parents are `9be9cd7af428a9497a9ca2a8dad716823ca3bb6a` and `86a7b0c57831c15e9cd8b42d64cc4a9843f4e726` (#22). The manager merge changes only the originator and RX-validator declaration order. All RTL at this head is byte-identical to merged main `86a7b0c5`; the #42 lane adds no RTL change. See [provenance](receipts/provenance.json), [complete diff](receipts/source.diff) and [history](receipts/history.txt).

The Conformance pass traced REQ-NET-002 and REQ-SRP-004 through `02_interfaces.md` §4.3 and the event catalog, `06_aecp_engine.md` §§6.10/7, F08.1, and `10_srp_engine.md` §6.1. DN registers A before the differing Domain, grades exactly one complete unsolicited GET_AVB_INFO for AVB_INTERFACE 0, and rejects extra GET_AS_PATH. Returning the declared values to defaults gives one additional notification; both identical declarations remain silent. Link edges run at DEFAULTS, with an explicit no-DOMAIN_CHANGE premise, isolating the link term. DN2 uses the received-declaration adoption arm at `KL_srp_domain.sv:184`; it does not claim isolated coverage of the LINK_DOWN revert at `:157`. Live mapping contents remain the integrator's responsibility. GET_COUNTERS' limiter is unchanged.

The RTL pass examined the top's OR and independent path trigger at `protocol_processor_top.sv:4018`, Domain capture/revert/adoption at `KL_srp_domain.sv:143`, and AVB selection/pending behavior at `KL_aecp_notify.sv:666` and `:1073`. For #134, both registrar loops preserve a registering renewal while giving expiry priority over non-registering received events. Their pending-ARM guard remains intact. The unit matrix and integrated collision sweep exercise both planes. The #22 edits move declarations without changing expressions, widths or drivers; both directly affected suites pass.

The Robustness pass exercised missing registration/restore, missing Domain or link triggers, an extra path notification, wrong descriptor, repeated identical adoption, and incorrect Domain strobes. The nine controls all complete and fail their named checks, with precisely the README's failure sets. Their union covers all 15 DN checks. The golden passes; build errors and incomplete runs are not accepted as kills. Four originator controls and five SRP control/suite combinations also fail as intended, including the control that deliberately misses the expiry collision.

The Tests pass reviewed the fresh-model isolation, received vector shape, independent frame construction from injected face words, wire-derived sequence model, 1.2-second windows, dispatch flag and mutation grading. All 56 earlier notification controls retain identical definitions, edits, commands and named checks; all 65 controls plant at this head ([audit](receipts/control-preservation.json), [planting results](receipts/all-notify-planting.json)). This is a planting audit, not a claim that all 65 were rerun in this round.

The Docs pass reconciled `tb/pp_top/README.md:2496`, `notify_phases.hpp:1663`, `:1689`, `:1709`, and the current [PR body](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/164) with the print-only probe. The source record and PR now name both latency endpoints and the REGISTER exception. The PR's author-head paragraph describes `9be9cd7a`; its manager note records the later #22 merge. Historical handoff captions are superseded by the corrected round-2 account.

| Measured event | RX final byte | feed return | TX final byte | From RX final byte / feed return |
|---|---:|---:|---:|---:|
| Adopt {3,5} | 340030 | 340034 | 340529 | 499 / 495 clocks |
| Declare defaults back | 580098 | 580102 | 580597 | 499 / 495 clocks |

REGISTER's response leaves at 3464; link down occurs at 100000, a gap of 96536 clocks (965.36 ms in this bench). Link notifications leave 466 clocks after each edge. The four notifications have sequence IDs 0–3; the section spans 8167 ms after registration. [Raw trace](receipts/trace.log), [print-only patch](receipts/trace-instrumentation.patch) and [independent timing/frame-field audit](receipts/trace-verification.json) corroborate these statements without changing the 15 passing checks.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen acceptance; REQ-NET-002/REQ-SRP-004; interfaces §4.3/event catalog; AECP §§6.10/7; SRP §§6.1/6.5; DN stimulus, oracle and captured frames | R503-2; unaffected R503-1 coverage retained | ad670a71b4d2f38f59672d51d8309d59ffed0808 |
| RTL | CLEAN | Full diff; top trigger OR; Domain/notification RTL; both merged SRP FSMs; originator/validator declaration moves; four affected suites | R503-2 | ad670a71b4d2f38f59672d51d8309d59ffed0808 |
| Robustness | CLEAN | Nine DN kills; four originator kills; five SRP control/suite combinations; completed-run grading; boot, registration, silence and collision premises | R503-2 | ad670a71b4d2f38f59672d51d8309d59ffed0808 |
| Tests | CLEAN | DN, NP/ST/RN, CS; merged-file suites; timing probe; 65-arm planting and 56-arm preservation audits; prior findings reconciled | R503-2; unaffected R503-1 coverage retained | ad670a71b4d2f38f59672d51d8309d59ffed0808 |
| Docs | CLEAN | README DN/mutation record; verification §8.4; merged SRP explanation; comments and PR body against exact-head trace | R503-2 | ad670a71b4d2f38f59672d51d8309d59ffed0808 |

**Executed receipts**

| Execution | Result | Raw receipt |
|---|---|---|
| DN, unchanged source | 15 checks, 0 failures | [domain-notify.log](receipts/domain-notify.log), rc 0 |
| NP/ST/RN | 70 checks, 0 failures | [notify.log](receipts/notify.log), rc 0 |
| Counter spacing | 9 checks, 0 failures; minimum gaps 115077 / 115070 / 115077 clocks | [spacing.log](receipts/spacing.log), rc 0 |
| Nine DN controls | Golden PASS; 9/9 KILLED; build rc 0 and run rc 1 for each mutant | [results.json](receipts/domain-mutants/results.json), [campaign](receipts/domain-mutants.log) |
| Originator / RX validator | 107 / 555 checks, 0 failures | [originator.log](receipts/originator.log), [rx_validator.log](receipts/rx_validator.log), both rc 0 |
| SRP stream FSMs | Four storage-shape runs pass; main suite 1347 checks, 0 failures | [srp_stream_fsms.log](receipts/srp_stream_fsms.log), rc 0 |
| Integrated SRP | Four FIFO-shape runs pass; main suite 8656 checks, 0 failures, 210547557 clocks | [srp_top.log](receipts/srp_top.log), rc 0 |
| Existing originator controls | Golden PASS; 4/4 KILLED | [results.json](receipts/originator-controls/results.json), [campaign](receipts/originator-controls.log) |
| SRP expiry/collision controls | Two goldens PASS; five control/suite combinations KILLED; SC1/SC2/SC3 covered | [campaign](receipts/srp-controls.log); [retained collision-arm raw log](receipts/srp-controls/lv-expiry-masked-lvcoll.log) |
| Print-only timing probe | 15 checks, 0 failures; timing audit PASS | [trace.log](receipts/trace.log), [trace-verification.json](receipts/trace-verification.json) |

The SRP driver reuses one filename for the two `lv-expiry-masked` suites. A focused repeat preserved the otherwise-overwritten integrated raw log separately; it again reports exactly 16 SC2 failures. Scripts are in `scripts/`; run `run_focus.py SOURCE`, `run_trace.py`, `verify_trace.py`, and `run_merge_controls.py` in a fresh packet directory. `retain_srp_collision_receipt.py` preserves that additional raw log. Set `REVIEW_VERILATOR` to override the pinned compiler path. Identity was verified before execution ([receipt](receipts/compiler-identity.txt)). Foreground coordinators join concurrent children; campaigns use `--jobs 2`, make uses `-j16`, and the common wrapper permits at most three builds with two compile workers each. Peak unit memory was 6483660800 bytes against a 12884901888-byte cap, with no memory-limit or OOM event ([receipt](receipts/resource-final.json)).

**Prior public findings, explicitly reconciled**

Only after the independent verdict and ledger were written were [R503-1](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/164#issuecomment-6011470805) and [R502-1](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/164#issuecomment-6011601546) read. Formal reviews and inline review comments both returned zero entries.

| ID | Severity / attributable lenses | Disposition at this head | Evidence and verification |
|---|---|---|---|
| R503-1-F1 = R502-1-F1.2 | MINOR / Tests, Docs | RESOLVED | README 2496–2499 and PR body state 495 from feed return, four clocks after the input's last byte, hence 499. Independent exact-head trace reproduces both intervals; DN remains 15/15. The historical handoff is superseded. |
| R502-1-F1.1 | MINOR / Tests, Docs | RESOLVED | README 2506–2517 and comments 1663–1665/1689 explain notification-based spacing and the excluded REGISTER response. Current PR body agrees with the observed 3464 → 100000 gap. All nine DN controls retain their expected failures. |
| R502-1-S1 | SUGGESTION / Tests | RETAINED, optional | `notify_phases.hpp:1799` ends after DN3b's window. Impact: behavior beyond that final window is unobserved. Optional outcome: append a quiet window and an empty-result check. Verification: inject a late duplicate after the existing final window and require the added check to fail while the golden passes. Authority: the prior public suggestion; frozen acceptance is already met. |
| R502-1-S2 | SUGGESTION / Tests | RETAINED, optional | `notify_phases.hpp:1740`, `:1772`; `KL_srp_domain.sv:157`; top `:4018`. Impact: DN does not separately grade notification coalescing when LINK_DOWN occurs while ADOPTED. Optional outcome: add that state/edge case and require exactly one byte-exact GET_AVB_INFO. Verification: golden passes and a duplicate-notification fault fails. Authority: prior public suggestion and the §6.1/§7 event contracts; outside frozen acceptance. |

The retained suggestions do not leave a lens unclean. No new finding is raised.

**Public evidence, limits and manager duties**

The [immutable packet](https://github.com/kebag-logic/milan-fpga/tree/355c335c33fc42c3b9c406d1032ce5e4108eca2b/review-evidence/pp42-r1) contains the historical `72facc6d` handoff, PR body, #148 adoption patch and publication manifest. All three published hashes match ([verification](receipts/public-evidence-hashes.json)). It contains summary tables rather than raw broad-bank logs. The current PR body reports the author's `9be9cd7a` full suite and campaign results. These historical results are distinguished from this review's exact-head executions. The supplied manager statement that full source static/builder and native banks passed at `ad670a71` is manager evidence; those prohibited broad banks were not rerun here. No additional manager bank-log comments appeared in the fetched issue/PR discussions.

Exact-head hosted documentation and portability jobs executed successfully in both [push run](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37453477982) and [PR run](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/37453485468). Downloaded push-job logs identify this head ([docs](receipts/hosted-docs.log), [portability](receipts/hosted-portability.log)). At the final snapshot, both suite jobs remain in progress; pending campaigns are not counted as passes. The compiler-build step was skipped following cache restoration, not executed. [Final job/step snapshot](receipts/hosted-jobs-final.json).

The consumer runs at parent `28f9666feab2b2ba287643c63ed3a16b1e0bb863`, with the #148 and #22 patches, remain manager evidence. This review checked the public parent gitlinks ([receipt](receipts/parent-gitlinks.json)) and the published 966-byte #148 patch hash `bbd0301dc7e576f51f92d24c8d140eda0666f9c6699806649365110e7ecfea83`; it did not construct a parent checkout or claim independent execution of the 17 consumer gates. The historical archive contains only the earlier #148 patch/run account.

Source validation against `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8` does not certify the final current-dev candidate. At the merge turn the manager must build and validate that candidate from live dev `30e3c018b9add0cb182d8f1229eeec062218130d`, preserve the required adoption patches and submodule pins, publish its evidence, and obtain review of any resulting delta. The manager also owns hosted/act acceptance, the second independent positive review, final completion checks and publication. This positive source verdict does not authorize bypassing those duties.

No full parent/processor/gPTP/builder/synthesis bank, hardware run, container workflow, source fix, commit, push, merge or GitHub write was performed. Full pp_top six-build and full 65-control execution were not repeated here; this round used the focused executions listed above and retained unaffected prior coverage. Copyrighted specification PDFs were not inspected. Physical calibration **NOT RUN**, field skips and the historical builder NOT RUN gate are not hardware proof. There is no claim of live integrator mapping coverage or isolated LINK_DOWN Domain-revert notification coverage.

The clone remained unchanged. [Before](receipts/integrity-before.json) and [after](receipts/integrity-after.json) audits confirm all **562 tracked entries**, blob bytes, executable/symlink modes, index entries, detached HEAD and required tree. Final status including ignored files is empty. This processor repository contains **zero submodule gitlinks**; the public parent pins were checked separately without modifying any checkout. All disposable trees are under `scratch/`, excluded from publication. `MANIFEST.sha256` lists the publishable receipts and scripts with packet-relative paths.

R503-2 FINISHED
