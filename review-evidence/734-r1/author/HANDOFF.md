# Lane 734 handoff

Author: [A613]
Status: REVIEW READY for independent review; local implementation complete.
Branch: `734-merge-base-scope`
Starting head: `a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0`
Review head: `0519ff3684258482a56892056edbfbb65c186f88`
Commit: `Classify pull requests from their own merge-base changes`
Assignment: issue #734, comment 6151273761, read verbatim.
TAKEN: issue #734, comment 6151299417.

The configured commit identity was used without overrides.
The initial origin and HEAD matched the assignment exactly.
The worktree is clean and the branch has one local commit.
The direct assignment authorized this lane while its project card displayed Backlog.

## Scope and decisions

The three selectors now classify the PR's recorded-base-to-own-head merge-base delta.
Both SHA inputs come from the event. `PR_HEAD_SHA` is necessary: hosted `GITHUB_SHA`
is the synthetic merge, which includes later base changes. Gate jobs still build
and record their original checked-out SHA. The fast push path retains its
before-to-after tree comparison. All three checkouts already explicitly had
`fetch-depth: 0`; those full-history settings remain contract-checked.
The replay payload still preserves its recorded base and exact PR head.
The live validation base remains the separate trust/fetch authority.

The merge-train current-dev candidate must run builder and full native banks
before every merge. This lane must follow 697c, then 696, as assigned.
Firmware behavior, linked inputs, submodule pointers, and generated files did not change.
No firmware/image STOP condition occurred.

## Changes by file and line

| File:line | Change |
|---|---|
| `.github/workflows/rtl.yml:103` and `:117` | Bind the event's PR head; use the merge-base diff. |
| `.github/workflows/rtl-fast.yml:40` and `:56` | Bind the event's PR head; change only the PR comparison. |
| `.github/workflows/elaborate.yml:88` and `:106` | Bind the event's PR head; use the merge-base diff. |
| `scripts/act_ci.py:2375`, `:6207`, `:15157` | Document the payload rule and add the real stale-base event selftest. |
| `scripts/ci_events.py:398`, `:584`, `:832`, `:1145`, `:1282`, `:6417`, `:6848` | Maintain canonical scripts and allowed inputs; add endpoint/head-binding mutations. |
| `scripts/ci_scope.py:500` and `:521` | Run the new history controls from the mandatory selftest. |
| `scripts/ci_scope_history.py:36`, `:67`, `:89`, `:108` | Build a divergent Git fixture; execute shipping scope bodies; compare file sets/verdicts and plant rule-removal defects. |
| `docs/testing/CI_WORKFLOWS.md:168` and `:1516` | Explain PR scope, merge-checkout distinction, full history, replay parity and candidate-bank safety. |

## Scope classification before and after

B16 uses recorded base `49da9fd9` and PR head `f1b2489f`.

| Case | Before | After |
|---|---|---|
| B16 endpoint versus merge-base | 65 paths, relevant | 2 paths, documentation-only |

The 65-path measurement disables rename detection, matching the workflows.
Default rename detection gives the issue body's 64 paths. The two PR paths are
`docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and `docs/findings/README.md`.
`b16.json` retains the complete path sets.

The synthetic history has a PR fork, a later recorded base and a still later live base.
Before hosted scope includes `hdl/base.sv`; before replay includes `scripts/base.py`
in reverse. After scope excludes both. The following rows execute each workflow's
actual scope body; only its recursive selftest invocation is replaced by `:`.
The mandatory outer selftest still runs all classification and reader controls.

| Workflow | Control | Before hosted: paths / relevant | Before replay: paths / relevant | After both: paths / relevant |
|---|---|---|---|---|
| `rtl.yml` | stale-base docs | 2 / true | 2 / true | 1 / false |
| `rtl.yml` | stale-base RTL | 2 / true | 2 / true | 1 / true |
| `rtl.yml` | submodule pointer | 2 / true | 2 / true | 1 / true |
| `rtl.yml` | empty delta | 1 / true | 1 / true | 0 / true |
| `rtl-fast.yml` | stale-base docs | 2 / true | 2 / true | 1 / false |
| `rtl-fast.yml` | stale-base RTL | 2 / true | 2 / true | 1 / true |
| `rtl-fast.yml` | submodule pointer | 2 / true | 2 / true | 1 / true |
| `rtl-fast.yml` | empty delta | 1 / true | 1 / true | 0 / true |
| `elaborate.yml` | stale-base docs | 2 / true | 2 / true | 1 / false |
| `elaborate.yml` | stale-base RTL | 2 / true | 2 / true | 1 / true |
| `elaborate.yml` | submodule pointer | 2 / true | 2 / true | 1 / true |
| `elaborate.yml` | empty delta | 1 / true | 1 / true | 0 / true |


After-path oracles are `docs/note.md`, `hdl/pr.sv`, `docs/pointer.md`, and an
empty list respectively. The documentation-shaped gitlink ensures the explicit
submodule rule is tested independently of suffix filtering.
`scope-classifications.json` retains every before/after path list.

## Coverage table

This is executable acceptance coverage, not an independent-review ledger.

| Obligation | Coverage | Result |
|---|---:|---|
| Four PR controls through three shipping selectors | 12 paired hosted/replay assertions, 24 executions | PASS |
| Fast push before/after behavior, including rewind | 1 assertion | PASS |
| Removed scope/classification rules | 15 planted defects | All rejected |
| Event-head bindings and merge-base shell contracts | 6 new CI-events mutations | All rejected |
| Stale-base replay event file set and endpoint counterexample | 2 new runner assertions | PASS |
| Complete classifier, reader and scope selftest | 132 ok assertions | PASS |
| Complete CI-events selftest | 2834 arms, 2021 contract items | PASS |
| Complete offline runner selftest | 533 ok records | PASS |
| Linked-image preservation | 5 shapes | Byte-identical |
| Image-audit controls | 33 checks | PASS |

Firmware coverage and protocol mutation campaigns were not changed or remeasured.
No RTL build, synthesis, hardware access, or physical compliance claim is made.

## Mutation table

| Defect | Killing control | Instances | Result |
|---|---|---:|---|
| Replace three-dot scope with endpoint-tree comparison | Stale-base documentation exact paths/verdict | 3 | Rejected |
| Use synthetic merge SHA as scope head | Hosted/replay documentation comparison | 3 | Rejected |
| Treat `hdl/` as documentation | Stale-base RTL control | 3 | Rejected |
| Remove explicit submodule precedence | Documentation-shaped gitlink control | 3 | Rejected |
| Remove empty-list fail-safe | Empty delta control | 3 | Rejected |
| Revert canonical scope command to endpoint comparison | CI-events canonical script check | 3 | Rejected |
| Bind PR head to checkout SHA | CI-events input binding check | 3 | Rejected |

The pre-existing shallow-checkout, missing-base, rename, reader, trust, process
cleanup, and output-binding controls remain green in their owning selftests.

## Linked-image hashes before and after

`ctrl_image.py` built all five configuration shapes twice using the same installed
RV32 SDK. These are linked measurement fixtures, not booted shipping images.
All ELF audits pass. Stack usage is outside this fixture's size bound.

| Shape | ELF bytes before / after | SHA-256 before | SHA-256 after |
|---|---:|---|---|
| `endstation_arty_4x4` | 50752 / 50752 | `f70be6b729d203ade7fb75e832d1ca0b1d1d9ba99f03e746cc2907174ec9cce4` | `f70be6b729d203ade7fb75e832d1ca0b1d1d9ba99f03e746cc2907174ec9cce4` |
| `endstation_arty_8ch` | 50752 / 50752 | `eb5dfe04250400df1a0546c4f52096cfbd4e8f0e7abc777388e6d55cf64802e6` | `eb5dfe04250400df1a0546c4f52096cfbd4e8f0e7abc777388e6d55cf64802e6` |
| `endstation_arty_current` | 50744 / 50744 | `9600824e12c1890edebeee455afe2244dc4fa9166c463fbb01591e284fe1f441` | `9600824e12c1890edebeee455afe2244dc4fa9166c463fbb01591e284fe1f441` |
| `endstation_ax7101_1x1_tdm8` | 50768 / 50768 | `ee7991b0b767b331d1b9fc84972b5a610ec0e9ae521ddf20689d9b4df4a9f33c` | `ee7991b0b767b331d1b9fc84972b5a610ec0e9ae521ddf20689d9b4df4a9f33c` |
| `endstation_ax7101_8x8` | 50776 / 50776 | `1b17baeb51ab66d3eeaeb97e5136fc8f516361ca6d99900d490a7953689e7018` | `1b17baeb51ab66d3eeaeb97e5136fc8f516361ca6d99900d490a7953689e7018` |


The compiler identity and library digest are in `images-before.log` and
`images-after.log`. Both build commands returned 0; their logs are identical.
`image-hashes.json` records exact sizes and both hashes. ELF files, maps, generated
headers, exported trees and installed dependencies remain outside this evidence directory.

```sh
python3 sw/firmware/ctrl/test/ctrl_image.py --shape endstation_arty_4x4 --shape endstation_arty_8ch --shape endstation_arty_current --shape endstation_ax7101_1x1_tdm8 --shape endstation_ax7101_8x8 --out "$image_output"
python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32
```

## Gates and planted controls

The interpreter was CPython 3.12.3; PyYAML was 6.0.3. Markdown dependencies came
from the repository's hash-locked requirements. Every selected final gate below
returned 0. Receipt JSON preserves the exact executable, argv, duration, log size
and SHA-256. Commands here use ordinary shell syntax without a wrapper prefix.

| Gate / command | RC | Result and planted control | Evidence |
|---|---:|---|---|
| `python3 scripts/ci_scope.py --selftest` | 0 | 132 assertions; 12 hosted/replay comparisons, push control, 15 workflow mutations; existing reader and classifier controls | `scope-accepted.log`, `scope-accepted.json` |
| `python3 scripts/act_ci.py --selftest` | 0 | 533 ok records in a disposable network-isolated job; stale-base docs payload, refused trust/fetch changes, cleanup and process controls | `act-selftest-final.log`, `act-selftest-final.json` |
| `python3 scripts/ci_events.py --check` | 0 | 2021 contract items; negative controls belong to the selftest below | `ci-events-check-final.log`, `ci-events-check-final.json` |
| `python3 scripts/ci_events.py --selftest` | 0 | 2834 arms; six new endpoint/head-binding mutations, existing shallow-checkout controls | `ci-events-selftest.log`, `ci-events-selftest.json` |
| `python3 scripts/docs_check.py` | 0 | 0 findings; 23 scrub and 4 routing controls | `docs-check-final.log`, `docs-check-final.json` |
| `python3 scripts/docs_check.py --selftest` | 0 | 23 scrub and 4 routing controls | `docs-scrub-selftest.log`, `docs-scrub-selftest.json` |
| `python3 scripts/docs_check.py` | 0 | Exported staged tree without metadata: 0 findings; 22 scrub and 4 routing controls; git-inventory parity explicitly inapplicable | `docs-no-git.log`, `docs-no-git.json` |
| `python3 scripts/check_doc_paths.py` | 0 | 974 cited paths and 10 line anchors; no standalone planted control in this gate | `docs-paths.log`, `docs-paths.json` |
| `python3 scripts/gen_toc.py --check` | 0 | 146 pages checked; planted controls in the selftest below | `toc-check.log`, `toc-check.json` |
| `python3 scripts/gen_toc.py --selftest` | 0 | 1501 renderer/navigation controls | `toc-selftest.log`, `toc-selftest.json` |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | 486 fragment links reproduced; renderer controls above | `toc-anchors.log`, `toc-anchors.json` |
| `python3 scripts/check_em_dash.py --selftest` | 0 | 339 planted controls | `em-dash-selftest.log`, `em-dash-selftest.json` |
| `python3 scripts/check_em_dash.py --base a0f39ad4` | 0 | 0 findings over 34 added Markdown lines; 339 controls | `em-dash-head.log`, `em-dash-head.json` |
| `python3 scripts/check_py_idiom.py` | 0 | 398 modules; all ratchets pass; controls below | `python-idiom-accepted.log`, `python-idiom-accepted.json` |
| `python3 scripts/check_py_idiom.py --selftest` | 0 | 54 controls, including undocumented function and budget increases | `python-idiom-selftest.log`, `python-idiom-selftest.json` |
| `python3 scripts/pp_srcs.py --check` | 0 | 46 tracked sources derived; no copied build list | `pp-sources.log`, `pp-sources.json` |
| `python3 scripts/pp_srcs.py --selftest` | 0 | Hand-written list, new consumer, extra prose literal, and stale exemption controls | `pp-sources-selftest.log`, `pp-sources-selftest.json` |
| `python3 scripts/measure_test_evidence.py --check` | 0 | No unexplained readers; all four ratchets pass | `evidence-readers.log`, `evidence-readers.json` |
| `python3 scripts/measure_test_evidence.py --selftest` | 0 | 105 controls: source readers, swallowed failures, missing mutation arms, tally and timeout rules | `evidence-readers-selftest.log`, `evidence-readers-selftest.json` |
| `python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32` | 0 | 33 controls: ISA, ABI, ELF header, undefined symbols, incompatible library and recursive helpers | `image-audit-controls.log`, `image-audit-controls.json` |
| `git diff --cached --check` | 0 | 0 whitespace findings; no planted control for this native command | `git-diff-check.log`, `git-diff-check.json` |


The runner selftest ran inside a disposable container with no network, no host
credentials, no Docker socket, dropped capabilities, and a 4 GB memory cap.
Its candidate source was mounted read-only. This was the offline runner-contract
gate; it was not a full PR workflow replay. The candidate never acted as the
host-side replay orchestrator.

Two intermediate failures were fixed before commit and retained as evidence:
`act-selftest.log` caught direct construction in the new test; the test now calls
the production resolver, preserving the original construction-site guard.
`python-idiom-final.log` caught the new nested assertion helper's missing docstring;
that helper is now documented. Their accepted reruns are named in the table.
No gate, expected result, budget, or acceptance criterion was weakened.

## Dependencies and context

Only `third_party/verilog-axis`, `protocol-processor` and `gptp-processor` were
initialized. Their top-level paths and own origins were verified before use.
Their pins are unchanged: `48ff7a7e2ef782cf778d47910cf85835c64b1bce`,
`2ad2f845dd583f8310075fa2380cb60a04fd091a`, and
`7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9` respectively.
The standalone public tsn-c-stack checkout was read for its README, import record,
boundary checker and validation driver; it was not modified or published.
Its `dev-linux` branch was not accessed. The firmware control layers, harness,
coverage reader, RV32 builder and linked-image audit were inspected as context.
No firmware or dependency publication is part of this change.

## Delivery and remaining merge obligations

`PR-BODY.md` is prepared for later publication. No push, PR creation/edit, merge,
rebase, hardware access, or flashing occurred. No existing comment was edited.
This is an author handoff, not a review verdict. Independent internal and external
reviews, a reviewer-owned lens ledger, full PR replay and hosted contexts, and
current-dev candidate validation remain required before merge. Post-merge
containment and issue closure remain subsequent maintainer work.

`validated-files.json` binds the final file bytes to the tested changes.
All output files are below 200 KB; no binaries, packages or toolchains are stored here.
