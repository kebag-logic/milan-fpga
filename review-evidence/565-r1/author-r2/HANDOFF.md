# Round 2 handoff

[A346]

Issue: #565. PR: #581. Branch: `565-8x8-clock`.
Assignment: [public round 2 scope](https://github.com/kebag-logic/milan-fpga/issues/565#issuecomment-5853405428).

## Commit

- Starting head: `054e59b41471ffbb3b4999a60c4cb04abcfc895f`.
- Resulting head: `7c63e453142deb4d848c41594b2246afe32a792a`.
- Subject: `docs: distinguish the declared bare-metal clock from enforced checks`.
- Exactly one commit, one-line subject, no body or trailers.
- Origin verified as `https://github.com/kebag-logic/milan-fpga.git`.
- Worktree and index clean after validation; branch is one commit ahead.
- The commit remains local. No push, PR edit or merge was performed.

## Change list

| File:line | Change | Assignment item |
|---|---|---|
| `docs/integration/BAREMETAL_FIRMWARE.md:33` | Cite both implementation files and list their shared CPU, XLEN, hart-count, L2 and Scala-override checks. Attribute the flashboot restriction to the builder and the FPU refusal to the SoC entry point. | 1 |
| `docs/integration/BAREMETAL_FIRMWARE.md:42` | Separate the declared 50 MHz target from enforced checks. State the builder's clock inequality and link enforcement follow-up #582. The product clock contract remains 50 MHz. | 1 |
| `hdl/ieee1722/aaf/README-parameters.md:37` | Explain the divider rationale through the selected shape's clock, without naming a board clock. | 2 |

Item 1 addresses [external finding F1](https://github.com/kebag-logic/milan-fpga/pull/581#issuecomment-5853297338) and [internal suggestion S1](https://github.com/kebag-logic/milan-fpga/pull/581#issuecomment-5853401533).
Item 2 addresses external suggestion F2.
The assignment routes internal S2 and external F3 to #582.

Source comparison: `sw/builder/endstation_builder.py:4224` and `:3772`;
`sw/litex/milan_soc.py:3683`.
Only the two Markdown files changed.
Code, configuration, gates and measurements remain byte-identical to the starting head.

## Gate table

All commands ran from the assigned worktree on the resulting head.
Each ran in the foreground, without a pipeline, with a 900-second timeout.
Output was redirected directly to the named log.
For Python commands, `python3` denotes `/tmp/565-a346-docs-z4wnjk65/bin/python`.
That temporary environment is outside this output directory.
It contains the hash-locked `tools/markdown/requirements.txt` dependencies and PyYAML 6.0.3.

| Gate command | rc | Evidence |
|---|---:|---|
| `python3 scripts/docs_check.py` | 0 | `docs-check-git.log`: zero findings; 23/23 scrub and 4/4 routing controls |
| `GIT_DIR=/dev/null python3 scripts/docs_check.py` | 0 | `docs-check-no-git.log`: zero findings; 22/22 scrub and 4/4 routing controls |
| `python3 scripts/check_em_dash.py --base 831f94f4` | 0 | `check-em-dash.log`: zero findings; 339/339 controls |
| `python3 scripts/check_doc_style.py` | 0 | `check-doc-style.log`: 22 current documents checked |
| `python3 scripts/gen_toc.py --check` | 0 | `gen-toc-check.log`: annotated contents checked |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | `gen-toc-anchors.log`: 176 fragment links reproduced |
| `python3 scripts/check_doc_paths.py` | 0 | `check-doc-paths.log`: 847 cited paths resolve |
| `python3 scripts/check_nvm_capture.py` | 0 | `check-nvm-capture.log`: seven controls detected; receipt passes |
| `git diff --check` | 0 | `git-worktree-diff-check.log`: no whitespace errors |
| `git diff --check 054e59b41471ffbb3b4999a60c4cb04abcfc895f HEAD` | 0 | `git-round2-diff-check.log`: round 2 commit checked |
| `git diff --check 831f94f4 HEAD` | 0 | `git-diff-check.log`: full source delta checked |

The filesystem inventory mode intentionally skips its Git-parity self-test.
That skipped control supplies no evidence.
The capture gate regraded the existing receipt; no captures were remeasured.
The receipt remains byte-identical to the starting head:
`tb/verilator/nvm_capture_cpu/measurements.json`,
SHA-256 `b44b2fc8402ccfdfb13cfe16d785a643e1a5018a93511213e38dc70294f89674`.

## Handoff state

Both assignment items are implemented and all assigned gates return zero.
Independent re-review of the corrected text remains pending.
No review verdict or completion ledger is claimed by the author.
`PR-BODY.md` is the full proposed replacement, derived from the current public PR body.
It preserves the initial implementation evidence and adds a Round 2 section.

