[R892] POSITIVE - exact head 61a504eec3ec3de828ccd80076212533ef58644b

All five lenses are CLEAN. No open BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION findings were identified. The new assertion detects the specified wrong-kind defect, and the production core and ADP constants remain unchanged.

This verdict covers the test-only salvage in [stack PR #36](https://github.com/kebag-logic/tsn-c-stack/pull/36), not completion of the platform discovery fix in [milan-fpga #970](https://github.com/kebag-logic/milan-fpga/issues/970).

| Identity | Reviewed value |
|---|---|
| Head | `61a504eec3ec3de828ccd80076212533ef58644b` |
| Tree | `50c5014d5669bb8880b719445e6d737d22b9e285` |
| Base and fetched `origin/main` | `715589c1db7cf67e2f3259fd7083ebc7f0923376` |
| History | One commit; one-line subject, no body or trailers |
| Delta | Six files, 52 insertions and 33 deletions; three assertion lines, one plant, and documentation |
| Public evidence snapshot | `milan-fpga` at `7a5e1e9aec00736a7e7f5f3285d7f34448538e7e`, `review-evidence/tsn36-r1` |

The governing scope is [the public ruling, item 4](https://github.com/kebag-logic/milan-fpga/issues/970#issuecomment-7080789556): retain the assertion and plant for GM_CHANGE in WAITING against unchanged constants. The earlier sub-second narrowing was rejected and PR #35 closed without merge. The wider issue retains the declared discovery-time criterion, both grandmaster orders, platform shapes, derivation and bench obligations; its real boot-path fix is assigned to #972. Those obligations are not declared complete here.

Reconstruction covered the supplied operating instructions, CONTRIBUTING.md, README.md, coding and verification rules, requirement and traceability records, architecture, ADP port contract and deviations. There is no tracked AGENTS.md or docs/README in this stack tree. The relevant authorities are ADP-02 and MFDISC-01, Milan v1.2 5.6.3 including Table 5.51 and transition 5.6.3.5.7, and IEEE 1722.1-2021 6.2.4.2.2 as applied by the frozen ruling. The linked imported FR-DISC rows were inspected at their pinned source snapshot. The full diff and history were independently examined before public execution evidence. Other reviewers' findings were opened only after [the independent verdict and ledger](INDEPENDENT-VERDICT.md) had been written.

The assertion in `tests/test_adp.cpp:139` runs immediately after `adp_gm_change` in the existing schedule. The fixture first reaches WAITING through accepted advertisements. It then requires DELAY, `ADP_DRAW_DELAY`, equality between the callback's armed delay and the recorded draw, and the independent literal ceiling `4000u`. The delay fields are unsigned. The following expiry and advertisement assertions remain. A wrong-kind call therefore fails even when its shorter numerical delay falls below 4000 ms.

The registry entry at `tests/mutations.json:363` changes only the WAITING call in `src/adp.c:277` to `ADP_DRAW_STARTUP`. Its original fragment matches exactly once. Its required kill names `AdpCore.A0toA2Schedule` and the new assertion's unique message. The parent walk name in `original_tests` is provenance, not a substitute for a stack-owned executable kill.

`include/adp.h:86` still defines the general maximum as 4000 ms and line 87 the startup maximum as 2000 ms. The core, all public headers, examples, build definitions and CI configuration are identical to the base. No RTL, mailbox interface, register map, public layout or gitlink changes occur. The stack contains no submodule gitlinks; there is no parent pin update in this PR. The RTL lens is clean by the checked boundary and unchanged production artifacts, without claiming a new RTL simulation or hardware result.

Independent execution produced the following receipts. Return codes are retained beside the logs. [run_review.py](run_review.py) is the portable review driver; [setup_gtest.py](setup_gtest.py) installs the pinned test dependency only under the disposable directory.

| Check | Result | Receipt |
|---|---|---|
| GCC Debug stack tests | 10/10 binaries pass; registration reconciles 459 instances | [gcc-test.log](gcc-test.log), [traceability.log](traceability.log) |
| Coverage ratchet | 100% lines/branches after existing exclusions; raw ADP 205/207 lines, 97/104 branches | [coverage.log](coverage.log) |
| ADP address/undefined-behaviour sanitizers | `adp_tests`, `adp_debug`, `adp_release`: 3/3 pass | [sanitize-adp.log](sanitize-adp.log) |
| Registered plant | CAUGHT; rc 1; one completed named test; exact owned diagnostic | [results.json](registered-plant/results.json), [run.log](registered-plant/gm-change-draws-startup-kind/run.log) |
| Independent plant with base tests | Wrong-kind defect escapes: 39/39 ADP instances pass | [probe-base.log](probe-base.log), [probe-base.xml](probe-base.xml) |
| Same plant with head tests | 38 pass; only `A0toA2Schedule` fails with the new diagnostic | [probe-head.log](probe-head.log), [probe-head.xml](probe-head.xml) |
| Requirements and traceability | Current; 47 requirements, 185 declarations; metadata controls pass | [traceability.log](traceability.log) |
| Generated test inventory | Current; 185 declarations, 478 total registered plants | [test-inventory.log](test-inventory.log) |
| Assertion ownership and controls | Pass | [needles.log](needles.log) |
| Comments and mutation fragments | Pass; no new prohibited source-comment labels | [comments.log](comments.log) |
| Licence and privacy | Pass; privacy checks 51 commits, 457 historical blobs and 100 current files | [license.log](license.log), [privacy.log](privacy.log) |
| Exact bytes, modes and index | All 100 tracked entries match before and after; clean status; no gitlinks | [tree-before.json](tree-before.json), [tree-after.json](tree-after.json), [audit_tree.py](audit_tree.py) |

The standalone probe's first compile used ordinary dependency include paths and encountered a signedness warning inside the test dependency. The corrected probe uses system-header treatment, matching the repository build and mutation driver. [The setup-error receipt](probe-setup-error.log) is retained; that compile failure is not counted as sensitivity. Final probes run complete XML-reported suites. No source fixes were made.

Independent builds and campaigns ran concurrently under a foreground driver, with at most 15 requested concurrent build/compiler slots. Subsequent checks reused the completed build. Dependencies, objects, mutated copies and executables remained under `scratch/`, which is excluded from publication.

The four documentation changes are consistent with the test-only scope. TESTS.md adds the plant and updates line anchors; TRACEABILITY.md updates shifted anchors. Their own generators, run in check mode against executable registrations, reproduce the tracked content without rewriting it. VERIFICATION.md correctly changes 473 core plants to 474; with four generated configuration plants, the total is 478. CHANGELOG.md correctly states that constants and behaviour are unchanged. No new source comment contains a bench label, lane name, round, reviewer ID or issue-comment ID. The changelog's public finding reference is prose, not a source comment.

The [published author receipts](https://github.com/kebag-logic/milan-fpga/tree/7a5e1e9aec00736a7e7f5f3285d7f34448538e7e/review-evidence/tsn36-r1/author-r1/receipts/stack/gates-61a504e) bind validation to this head and tree before and after execution. They report 28/28 gates rc 0, 478 plants CAUGHT with zero escapes/errors, and Debug/Release RV32 smoke execution with no unresolved final symbols. All 11 inspected stack receipt files match their published manifest hashes; see [the hash check](public-evidence-hash-check.json). These are author source-head receipts. No manager source bank exists or is inferred. Unrelated parent and superseded implementation receipts in the larger evidence directory were not used to establish this head's success.

Both exact-head hosted workflows completed successfully: [push run 45050645679](https://github.com/kebag-logic/tsn-c-stack/actions/runs/45050645679) and [PR run 45050650666](https://github.com/kebag-logic/tsn-c-stack/actions/runs/45050650666). The job records show that portable-core and freestanding validation executed and succeeded; neither validation step was skipped. The two `hosted-*.json` receipts record these observations. Hosted/act acceptance remains the manager's responsibility.

Prior findings were reconciled after the independent verdict:

| Public item | Disposition at this exact head | Verification |
|---|---|---|
| PR #36 prior FINDINGS | None published when checked. Two review-start notices; review and inline-comment collections empty. | `pr36-comments-final.json`, `pr36-reviews.json`, `pr36-review-comments.json` |
| [R887-1-F1 on PR #35](https://github.com/kebag-logic/tsn-c-stack/pull/35#issuecomment-7080769012), MINOR / Tests | RESOLVED for the salvaged defect. The stack owns the required kind/range/callback assertion and named compiling plant. The discarded third draw kind is absent, so startup-kind substitution is the relevant plant. | Independent base/head reversal, registered CAUGHT result and current inventory. The fresh-base total is correctly 474 + 4 = 478, rather than the superseded branch's requested total. |
| [R888-1-F1 on PR #35](https://github.com/kebag-logic/tsn-c-stack/pull/35#issuecomment-7080517530), MAJOR / all five lenses | The rejected narrowing is absent. The public ruling closed that branch without merge; this head preserves original production bytes and constants. No shortened-window conformance claim is carried forward. | Full diff, `origin/main` comparison, unchanged 4000/2000 ms constants and production audit. This is not acceptance of the rejected branch. |

Earlier optional suggestions concern the discarded third kind or old parent image presentation and introduce no open requirement for this delta. No other reviewer's verdict was adopted as this review's evidence.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #970 frozen ruling; ADP-02/MFDISC-01; PORTING ADP timers; test_adp.cpp:139; adp.c:277; adp.h:86; unchanged production diff | R892-1 | 61a504eec3ec3de828ccd80076212533ef58644b |
| RTL | CLEAN | Full tree/diff; unchanged core, headers, examples, build and CI; no RTL/interface/gitlink delta; byte/mode/index audit | R892-1 | 61a504eec3ec3de828ccd80076212533ef58644b |
| Robustness | CLEAN | core_schedule fixture/state sequence; unsigned bound and armed/recorded delay consistency; ADP sanitizer/debug/release runs; wrong-kind probe; unchanged coverage | R892-1 | 61a504eec3ec3de828ccd80076212533ef58644b |
| Tests | CLEAN | mutations.json:363; named diagnostic and complete XML; base/head sensitivity reversal; 10 stack binaries; needles, registration and author gate receipts | R892-1 | 61a504eec3ec3de828ccd80076212533ef58644b |
| Docs | CLEAN | CONTRIBUTING/README and guides; four changed documentation files; generated tables/counts; source-comment rule; licence/privacy gates; PR scope/evidence claims | R892-1 | 61a504eec3ec3de828ccd80076212533ef58644b |

The checks establish the specified kind-selection regression, not a statistical proof of uniformity or exhaustive generator verification. Conformance applies the frozen public ruling and repository clause trace; a full standards-corpus re-audit was not performed. The public Milan landing page refused access and the IEEE page did not provide the full clause text. No alternative interpretation of their prescribed intervals is introduced.

No full parent, processor, gPTP, synthesis or builder banks were run. RV32/full static-analysis/full mutation/graph acceptance is supported by author exact-head gate receipts and observed hosted execution; only the focused checks above were independently rerun. No simulator timing, PHY timing, physical calibration or field skips are presented as hardware proof. No hardware was accessed; physical calibration was NOT RUN.

The manager must obtain the second independent positive review, complete hosted/act acceptance, and build and validate the actual current-dev merge candidate with builder and native banks, publishing its receipts at the merge turn. This source review uses base `715589c1`; it does not validate a composition with live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`. Any later parent pin change and associated records require their own validation. Issue #970's affected bench scenarios and discovery-time completion remain pending with the platform work, including #972.

No source edits, commits, pushes, GitHub writes, merges, author contact, private author material, management checkout material or sub-agents were used. The final clone remains at the exact published head. Publish only REPORT.md and files listed in MANIFEST.sha256; disposable `scratch/` trees are excluded.

R892-1 FINISHED
