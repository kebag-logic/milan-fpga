[A291] Round 3 handoff for PR #557 / issue #501

Commit: `afdd28b701e7f5849317e27ce845c31d1c87f2a6`.
Parent: `dd6a68e9063c3f7aa81536197254d187e9cb65ba`.
Branch: `501-outmap-record`.
Source base: `573f0052a0e4412e81f0845438fcec2086ce5d55`.
Commit subject: `Document current capture-copy exposure and parent measurement owner`.

The commit changes only `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`,
section 18 and UNRESOLVED 6: 25 insertions and 15 deletions.
Every byte outside the two assigned passages is unchanged.
See `round3.patch` and `scope-and-page-match.log`.

Both passages now state that `nvm_capture()` copies every CLOSED record
at each capture, whether materialized or not, and accepted RELOAD closes
every allocated record. At 8x8, the count is 12,634 bytes across 156 records,
including 4,672 output-map bytes. The 0.78x doubled-cost exposure exists at
this head. Safety holds through void and retry; shipping 1x1 is unchanged.
Both passages cite the counted copy and #559, which owns measurement and
resolution. Their donor-adoption trigger and withdrawn obligation are removed.
No other repository change is included.

Assignment items 1-3 are met. This answers R312-2 F1 and R313-2 F1;
independent delta reviews at this head remain pending.

Public authorities:

- [Round 3 assignment](https://github.com/kebag-logic/milan-fpga/issues/501#issuecomment-5824209814).
- [Corrected disposition](https://github.com/kebag-logic/milan-fpga/issues/501#issuecomment-5824117439).
- [Measurement and resolution owner #559](https://github.com/kebag-logic/milan-fpga/issues/559).
- [Internal review R312-2](https://github.com/kebag-logic/milan-fpga/pull/557#issuecomment-5824109822).
- [External review R313-2](https://github.com/kebag-logic/milan-fpga/pull/557#issuecomment-5824206585).

Probe evidence:

| Reviewer archive | Probe | Result | Receipt |
|---|---|---|---|
| R312-2, `247a9151df9948fe213d078456ff9a53ac196e89` | `capture_copy_probe.py` | rc 0, archived output matched | `R312-2-capture_copy_probe.log` |
| R312-2, same archive | `hold_margin.py` | rc 0, archived output matched | `R312-2-hold_margin.log` |
| R313-2, `8c47d0158986e832939307ebd8e56ddb14647fbc` | `capture_copy_probe.py` | rc 0, archived output matched | `R313-2-capture_copy_probe.log` |
| R313-2, same archive | `hold_margin.py` | rc 0, archived output matched | `R313-2-hold_margin.log` |

All four scripts ran unchanged. Their downloaded bytes matched the immutable
blobs and reviewer manifests, before execution. Output comparison was exact;
only the internal review's archived `rc=0` trailer was excluded.
`probe-sources.json` records the source paths, immutable commits and hashes.
`probe-runs.json` records the executed arguments and return codes.

The external review's unchanged `tree_figures.py` generated current inputs.
These matched its archived head figures, excluding only the tree location.
`hold_margin.py` used that current input and the archived base input.
The internal hold probe retains its historical 8,604-byte base-page constant;
the external probe's base table contains 8,602 bytes. Neither was edited.
Both give the same current 8x8 figures.

| Shape | Copied bytes / records | Output-map bytes | Nominal time / margin | Doubled costs / margin |
|---|---|---|---|---|
| 8x8 | 12,634 / 156 | 4,672 | 31.8816 ms / 1.57x | 63.7632 ms / 0.78x |
| 1x1 | 3,218 / 53 | 144 | 8.2532 ms / 6.06x | 16.5064 ms / 3.03x |

These are counted copy bytes and modelled times, not measured product timing.
`scope-and-page-match.log` records the page comparison.

All required gates ran in the foreground, without pipelines, with 1,800-second
command timeouts. Each returned zero at the commit above:

| Command | Mode | Receipt |
|---|---|---|
| `python3 scripts/check_nvm_record_space.py` | candidate | `record-space.log` |
| `python3 scripts/check_nvm_record_space.py --self-test` | candidate | `record-space-self-test.log` |
| `python3 scripts/docs_check.py` | tracked-file CI mode | `docs-check.log` |
| `python3 scripts/docs_check.py` | exact-head export without git metadata | `docs-check-no-git.log` |
| `python3 scripts/check_em_dash.py --base 573f0052a0e4412e81f0845438fcec2086ce5d55` | candidate | `check-em-dash.log` |
| `python3 scripts/check_doc_style.py` | candidate | `check-doc-style.log` |
| `python3 scripts/gen_toc.py --check` | candidate | `gen-toc-check.log` |
| `python3 scripts/check_doc_paths.py` | candidate | `check-doc-paths.log` |
| `git diff --check` | candidate | `diff-check.log` |
| `git diff --check dd6a68e9063c3f7aa81536197254d187e9cb65ba HEAD` | committed delta | `committed-diff-check.log` |

`gate-results.json` records the head, arguments, return codes and durations.
Both documentation modes report zero findings. The mode without git metadata
skips inventory parity as designed; its other 22 scrub controls and four
routing arms pass. The tracked mode passes 23 scrub controls and four arms.
The renderer dependencies came from the repository's hash-locked requirements,
installed in a disposable environment under `/tmp`.

`PR-BODY.md` is the full current PR body read from the public PR, updated with
[A291], this head, a short Round 3 section, current ownership and validation.
It retains `Closes #501`. It is prepared for the manager and has not been applied.

Final local state and scratch cleanup are recorded in `final-state.log`.
The public probe downloads, disposable builds, environment and metadata-free
export were confined to scratch under `/tmp` and removed before the final notice.
This output directory contains only the handoff, prepared body and evidence.

No push, PR edit, merge, hardware run, additional checkout or sub-agent was used.
The final authorized publication is `[A291] REVIEW READY` on #501.
The manager retains publication of the prepared PR body, push, independent
reviews, hosted acceptance, candidate validation and any authorized merge.
