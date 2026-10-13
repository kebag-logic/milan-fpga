# Lane 734 handoff

Author: [A613]
Status: REVIEW READY for Round 2 independent re-review.
Branch: `734-merge-base-scope`; source base: `a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0`.
Resumed head: `0519ff3684258482a56892056edbfbb65c186f88`.
Local review head: `33ac35b54648ef919227c5dd8b9abc97fa6bedbd`.
New commit: `Classify PR scope against the live validation base`.
The configured identity was used; one-line subject, no body or trailers.
The worktree is clean and one commit ahead of the pushed PR #735.
No push, PR edit, merge, rebase, hardware access or flashing occurred.
No existing issue or PR comment was changed. No second TAKEN was posted.

## Round 1 baseline

The original assignment (issue #734 comment 6151273761) was read verbatim.
Round 1 changed the three selectors to recorded-base merge-base scope.
The original base and origin were verified in that round.
On resume, origin and local/remote PR head matched the assignment exactly.
The earlier measurements and receipts remain in this directory.
Round 1 measured B16 at 65 endpoint paths with rename detection disabled,
or 64 with default rename detection, versus two PR documentation paths.
R632-1 found that merging newer dev and restoring RTL defeats that rule.
Its BLOCKER stands until independent re-review clears the corrected head.
R633-1's positive verdict applies only to the previous head.
No prior clean-lens result is claimed for this new commit.

## Round 2

The newest assignment, issue #734 comment 6151933918, was read verbatim.
Both reviews, comments 6151873947 and 6151927790, were read.
Their public evidence was fetched from `734-review-evidence`.
The assignment supersedes Round 1's frozen-base scope rule.

Hosted scope now compares `GITHUB_SHA^1` with `GITHUB_SHA`.
That first parent is the live base used by the job's synthetic merge.
Source-head replay uses the already fetched and verified
`refs/remotes/origin/<base-ref>`, selected by `PR_BASE_REF`.
It compares the unique merge base with `PR_HEAD_SHA`.
The event's recorded oid remains metadata and never enters scope selection.
This works with the existing trusted runner payload, without executing the
candidate runner as a host-side orchestrator.
The runtime `ACT` marker selects replay; workflow-defined overrides remain
outside the contract's environment allowlists.
Full-history checkouts, validation SHA binding and the push before/after rule remain.
Missing revisions or missing/multiple replay merge bases fail the scope step.

R632-1-F1 is addressed by the live-base selectors and REV/REV+E controls.
R632-1-F2 is addressed in every cited contract passage and adjacent stale count.
The optional F3 suggestion about separately pinning the history-selftest call
was not added to the structural contract; the call remains present and executed.
This is an author claim with executable evidence, not a review verdict.
The reviewer owns lens classification and final coverage acceptance.

## Changes by file and line

| File:line | Round 2 change |
|---|---|
| `.github/workflows/rtl.yml:102`, `:115`, `:122` | Bind the base ref; source-head replay uses verified live ancestry; hosted scope compares the merge to its first parent. |
| `.github/workflows/rtl-fast.yml:39`, `:47`, `:54` | Apply the same PR rule while retaining push endpoint comparison and unknown-push fallback. |
| `.github/workflows/elaborate.yml:87`, `:104`, `:111` | Apply the same PR rule; describe missing-ancestry refusal accurately. |
| `scripts/act_ci.py:2375`, `:6199` | State the live-base rule; execute all three selectors with production event payloads on seven histories. |
| `scripts/ci_events.py:397`, `:413`, `:833`, `:1285`, `:1291`, `:6424` | Pin base-ref bindings, canonical shell bodies and new defect mutations. |
| `scripts/ci_scope_history.py:38`, `:49`, `:94`, `:128`, `:149`, `:159`, `:169` | Model seven cases; create true synthetic merge checkouts; execute hosted/replay bodies; plant frozen-base defects and test missing/ambiguous ancestry. |
| `docs/testing/CI_WORKFLOWS.md:168`, `:658`, `:673`, `:878`, `:950`, `:1163`, `:1521` | Explain live-base selection, the frozen-base failure, replay compatibility, candidate-bank safety and exact environment bindings/counts. |

## Scope classification before and after

Before means `0519ff36`; after means `33ac35b5`.
Each row executes the actual shipping shell text, replacing only its recursive
selftest invocation. Every row's hosted and replay path lists agree both before
and after. Full lists are retained in `r2-scope-table.log`.

| Workflow | Case | Before: paths / rtl | After: paths / rtl |
|---|---|---|---|
| `rtl.yml` | stale-base docs | 1 / false | 1 / false |
| `rtl.yml` | B16 shape | 2 / false | 2 / false |
| `rtl.yml` | stale-base RTL | 1 / true | 1 / true |
| `rtl.yml` | submodule pointer | 1 / true | 1 / true |
| `rtl.yml` | empty delta | 0 / true | 0 / true |
| `rtl.yml` | REV | 1 / false | 2 / true |
| `rtl.yml` | REV+E | 1 / false | 2 / true |
| `rtl-fast.yml` | stale-base docs | 1 / false | 1 / false |
| `rtl-fast.yml` | B16 shape | 2 / false | 2 / false |
| `rtl-fast.yml` | stale-base RTL | 1 / true | 1 / true |
| `rtl-fast.yml` | submodule pointer | 1 / true | 1 / true |
| `rtl-fast.yml` | empty delta | 0 / true | 0 / true |
| `rtl-fast.yml` | REV | 1 / false | 2 / true |
| `rtl-fast.yml` | REV+E | 1 / false | 2 / true |
| `elaborate.yml` | stale-base docs | 1 / false | 1 / false |
| `elaborate.yml` | B16 shape | 2 / false | 2 / false |
| `elaborate.yml` | stale-base RTL | 1 / true | 1 / true |
| `elaborate.yml` | submodule pointer | 1 / true | 1 / true |
| `elaborate.yml` | empty delta | 0 / true | 0 / true |
| `elaborate.yml` | REV | 1 / false | 2 / true |
| `elaborate.yml` | REV+E | 1 / false | 2 / true |
| `rtl.yml` | B16 actual | 2 / false | 2 / false |
| `rtl-fast.yml` | B16 actual | 2 / false | 2 / false |
| `elaborate.yml` | B16 actual | 2 / false | 2 / false |

B16 actual uses recorded base `49da9fd9`, source head `f1b2489f`,
landed merge `6c810c45`, and live first parent `e81ce82f`.
Its two paths remain `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`
and `docs/findings/README.md`.
REV/REV+E before lists only `docs/note.md`; after also lists `hdl/x.sv`.
The unrelated later dev path never enters the corrected scope.

The review probe was run unchanged first (`r2-probe-unchanged.log`).
Because its source hard-codes the old head, `r2-replay_probe.py` imports that
same unchanged file, sets only its HEAD/PARENT revision globals, calls its
unchanged main, and grades the nine current-head cases.
`r2-probe-current.log` records all nine PASS outcomes and the probe digest.
Its REV fixture fast-forwards the final merge, so its current hosted path list
contains only `hdl/x.sv`; it still correctly detects RTL relevance.
The shipping fixture uses explicit merge commits and additionally proves the
complete two-path composition and hosted/replay equality.
The probe's XX row only observes native Git ambiguity; shipping tests separately
prove replay refuses it and rejects a mutation selecting one arbitrary base.

## Coverage table

This table measures executed acceptance checks, not independent-review coverage.

| Obligation | Coverage | Result |
|---|---:|---|
| Seven histories through three selectors | 21 paired hosted/replay assertions | PASS |
| Historical B16, before and after | 3 paired workflow rows | Two docs paths, docs-only |
| Reviewer probe at corrected head | 9 graded workflow cases | PASS |
| Full scope selftest | 180 assertions, including 42 scope mutations | PASS |
| Missing hosted merge / replay base / replay head | 9 refusal assertions | PASS |
| Ambiguous replay ancestry | 3 refusals and 3 killing mutations | PASS |
| Push rewind behavior | 1 unchanged endpoint assertion | PASS |
| Production replay event path | 21 hosted/replay assertions within 552 runner checks | PASS |
| Workflow contracts | 2021 items, 2846 mutation/selftest arms | PASS |
| Linked images | 5 shapes, byte-for-byte comparison | Identical |
| Linked-image audit | 33 controls | PASS |

Firmware branch/line coverage and protocol mutation campaigns were not rerun:
no product behavior, image input, submodule pin or firmware test changed.
Their existing ratchets remain unchanged. No physical measurement is claimed.

## Scope mutation table

| Planted defect | Killing control | Instances | Result |
|---|---|---:|---|
| Hosted frozen-base endpoint comparison | Stale docs, B16 shape, REV and REV+E | 12 | Rejected |
| Replay live-base endpoint comparison | Stale docs and B16 shape | 6 | Rejected |
| Replay frozen merge base | REV and REV+E | 6 | Rejected |
| Hosted frozen merge base | REV and REV+E | 6 | Rejected |
| Treat HDL as documentation | Stale-base RTL | 3 | Rejected |
| Remove explicit pointer rule | Documentation-shaped gitlink | 3 | Rejected |
| Remove empty-list fail-safe | Empty delta | 3 | Rejected |
| Select an arbitrary merge base | Criss-cross ancestry | 3 | Rejected |

The CI-events mutations additionally reject frozen hosted scope, replay endpoint
scope, forcing hosted down the replay path, removing all-base enumeration and
rebinding PR_HEAD_SHA in all three workflows. Existing shallow-checkout,
environment, failure-propagation, input-binding and trust controls remain green.

## Linked-image hashes before and after

Round 2 rebuilt every shape with the same compiler and library as Round 1.
The before files are the retained Round 1 head measurements, also equal to the
original source-base builds. These are linked measurement images, not deployed
images. Stack usage is not bounded by this fixture's static size result.

| Shape | Bytes before / after | SHA-256 before | SHA-256 after |
|---|---:|---|---|
| `endstation_arty_4x4` | 50752 / 50752 | `f70be6b729d203ade7fb75e832d1ca0b1d1d9ba99f03e746cc2907174ec9cce4` | `f70be6b729d203ade7fb75e832d1ca0b1d1d9ba99f03e746cc2907174ec9cce4` |
| `endstation_arty_8ch` | 50752 / 50752 | `eb5dfe04250400df1a0546c4f52096cfbd4e8f0e7abc777388e6d55cf64802e6` | `eb5dfe04250400df1a0546c4f52096cfbd4e8f0e7abc777388e6d55cf64802e6` |
| `endstation_arty_current` | 50744 / 50744 | `9600824e12c1890edebeee455afe2244dc4fa9166c463fbb01591e284fe1f441` | `9600824e12c1890edebeee455afe2244dc4fa9166c463fbb01591e284fe1f441` |
| `endstation_ax7101_1x1_tdm8` | 50768 / 50768 | `ee7991b0b767b331d1b9fc84972b5a610ec0e9ae521ddf20689d9b4df4a9f33c` | `ee7991b0b767b331d1b9fc84972b5a610ec0e9ae521ddf20689d9b4df4a9f33c` |
| `endstation_ax7101_8x8` | 50776 / 50776 | `1b17baeb51ab66d3eeaeb97e5136fc8f516361ca6d99900d490a7953689e7018` | `1b17baeb51ab66d3eeaeb97e5136fc8f516361ca6d99900d490a7953689e7018` |

`r2-image-hashes.json` retains the measurements. `r2-images.log` and the
Round 1 `images-after.log` are identical, including compiler/library identity.
No firmware/image STOP condition occurred.
ELFs, generated outputs, SDKs, installed packages and exported trees stay in scratch.

## Gates and planted controls

Every accepted command below returned 0 under CPython 3.12.3.
Each named receipt has a JSON command/return-code/duration/digest record and a log.
The runner selftest was confined to a disposable network-isolated job, with
read-only candidate source, dropped capabilities, no credentials or service
socket, four CPUs and a 4 GB memory cap. It did not run a full PR replay.
Other gates ran as foreground commands with a 550-second limit, never piped.
Observed service memory stayed far below 9 GB. No RTL build or Vivado run was needed.

| Command | RC | Result / planted control | Receipt prefix |
|---|---:|---|---|
| `python3 scripts/ci_scope.py --selftest` | 0 | 180 assertions; 42 scope mutations; missing inputs and ambiguous ancestry refuse | `r2-scope-final` |
| `python3 scripts/act_ci.py --selftest` | 0 | 552 assertions inside a disposable isolated job; production event payload across 21 hosted/replay pairs; existing trust, fetch, cleanup and policy controls | `r2-act-final` |
| `python3 scripts/ci_events.py --check` | 0 | 2021 contract items; planted controls in the next row | `r2-check-final` |
| `python3 scripts/ci_events.py --selftest` | 0 | 2846 arms; frozen hosted base, replay endpoints, routing, arbitrary merge-base and head-binding controls | `r2-events-accepted` |
| `python3 scripts/docs_check.py` | 0 | 0 findings; 23 scrub and 4 routing controls | `r2-docs-final` |
| `python3 scripts/docs_check.py --selftest` | 0 | 23 scrub and 4 routing controls | `r2-docs-controls` |
| `python3 scripts/docs_check.py` | 0 | Exported staged tree; 0 findings, 22 scrub and 4 routing controls; metadata parity inapplicable | `r2-docs-no-git` |
| `python3 scripts/check_doc_paths.py` | 0 | 974 paths and 10 line anchors; no standalone planted-control mode | `r2-docpaths` |
| `python3 scripts/check_doc_style.py` | 0 | 22 current documents; no standalone planted-control mode | `r2-doc-style` |
| `python3 scripts/gen_toc.py --check` | 0 | 146 pages; controls in the next row | `r2-toc-final` |
| `python3 scripts/gen_toc.py --selftest` | 0 | 1501 renderer/navigation controls | `r2-toc-controls` |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | 486 links; renderer controls above | `r2-toc-anchors` |
| `python3 scripts/check_em_dash.py --base a0f39ad4` | 0 | 73 added Markdown lines at the committed head; 0 findings | `r2-dash-head` |
| `python3 scripts/check_em_dash.py --selftest` | 0 | 339 planted controls | `r2-dash-controls` |
| `python3 scripts/check_py_idiom.py` | 0 | 398 modules; unchanged ratchets all pass | `r2-idiom-after-edges` |
| `python3 scripts/check_py_idiom.py --selftest` | 0 | 54 controls, including undocumented functions, excessive parameters and budget increases | `r2-py-controls` |
| `python3 scripts/pp_srcs.py --check` | 0 | 46 derived sources; no copied list | `r2-source-list` |
| `python3 scripts/pp_srcs.py --selftest` | 0 | Copied list, new consumer, extra prose literal and stale exemption controls | `r2-source-controls` |
| `python3 scripts/measure_test_evidence.py --check` | 0 | All four evidence ratchets pass; no unexplained readers | `r2-readers` |
| `python3 scripts/measure_test_evidence.py --selftest` | 0 | 105 controls for readers, mutation wiring, swallowed failures, tallies and timeouts | `r2-reader-controls` |
| `python3 sw/firmware/ctrl/test/ctrl_image.py --shape endstation_arty_4x4 --shape endstation_arty_8ch --shape endstation_arty_current --shape endstation_ax7101_1x1_tdm8 --shape endstation_ax7101_8x8 --out "$image_output"` | 0 | Five rebuilt linked images; ISA/ABI/symbol audits; byte identity with Round 1 | `r2-images` |
| `python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32` | 0 | 33 controls for ISA, ABI, ELF header, symbols, runtime library and recursive helpers | `r2-image-controls` |
| `git diff --cached --check` | 0 | No whitespace findings; no planted-control mode | `r2-diff-check` |
| `python3 r2-scope_table.py "$repo"` | 0 | 24 before/after rows, 96 shipping-shell executions; compares to independent path/verdict oracles | `r2-scope-table` |
| `python3 r2-probe_scope.py "$repo" "$probe_work"` | 0 | Unchanged reviewer script at its original hard-coded revisions reproduces F1; rc 0 is ungraded by design | `r2-probe-unchanged` |
| `python3 r2-replay_probe.py r2-probe_scope.py "$repo" "$probe_work" 33ac35b54648ef919227c5dd8b9abc97fa6bedbd` | 0 | Same unchanged probe functions with current/previous head globals; 9 graded current-head cases pass | `r2-probe-current` |

Two development failures are retained and excluded from accepted evidence:
`r2-events-selftest` caught an accidentally unchanged negative binding control;
its original frozen-oid mutation was restored, then all 2846 arms passed.
`r2-python-idiom` caught excessive helper parameters and a long canonical line;
the helper now accepts an input mapping and the literal is wrapped.
No threshold, expectation, budget or acceptance criterion was relaxed.
`r2-dash-staged` examined the previous committed head; only `r2-dash-head`
counts for the final Markdown diff.

## Dependencies, integrity and publication

The resumed processor/axis submodules were already initialized.
Their top-level paths and own origins were verified; no additional submodule
was initialized or advanced. The standalone public control-core checkout was
read without modifying or publishing it; its protected development branch was
not used. Firmware module contracts, harness and coverage gates, image builder,
linked audits, source-list gate and evidence readers were inspected as context.

`r2-head.json` binds the tested file hashes to the local commit.
All product-input trees and gitlinks equal the original source base.
`r2-MANIFEST.sha256` inventories this round's portable packet and receipts.
Every output file is below 200 KB; none is a package, toolchain or tree export.

`PR-BODY.md` follows the repository template and is ready for later publication.
The final status body is `r2-review-ready.md`, for a new comment on issue #734 only.
Independent re-review must clear F1/F2 and publish its own exact-head lens ledger.
The manager owns push, trusted full replay, hosted acceptance, current-dev
candidate builder/native banks and merge sequencing after 697c then 696.
Full merge acceptance, merge authorization, containment and issue closure remain
pending. No hosted or full-bank success is claimed for the local unpushed head.
