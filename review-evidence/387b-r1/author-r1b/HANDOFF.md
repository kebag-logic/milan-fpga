# [A269] PR #555 round 1b handoff

Assignment: https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5817362105

Issue: #387. Branch: `387-media-rebase`.
Starting head: `e68c1b1ac08c8b1e12a28e281b266d06f881e402`.
Final head: `a9636e0f670f90f411da3024a141e93efa1872df`.
Tree: `4f328e01ee2fc5d5cc81109e6be70fc2cf336b92`.
One commit: `Pin gate 1b to the decided media re-base consumers`.
The subject is one line, with no body or trailers. Worktree clean.

Only `sw/builder/test_builder.py` and
`docs/integration/BAREMETAL_FIRMWARE.md` changed. No RTL changed.

## Each changed pin and census row

Expressions below omit insignificant whitespace. `|` denotes RTL OR.

| Item | Before | After |
|---|---|---|
| `cfg_ptp_cmd_load` census | Exactly 5; comment admits the render initializer | Exactly 5; comment admits the media re-base initializer |
| `eff_ptp_adjust_w` census | Exactly 3; comment admits the render initializer | Exactly 3; comment admits the media re-base initializer |
| `media_rebase_p_w` census | Not present | Exactly 3: initializer, render reader, restart reader |
| `mcr_restart_p_w` census | Not present | Exactly 2: initializer and restart-engine port |
| `media_rebase_p_w` initializer | Not pinned | `eff_ptp_adjust_w \| cfg_ptp_cmd_load` |
| Media re-base diagnostic | Not present | `media re-base pulse must read only adjtime and settime` |
| `mcr_restart_p_w` initializer | Not pinned | `(crf_clk_selected_r & ((tkd_crflk_q_r & ~crf_locked_w) \| crf_mr_toggle_p_w)) \| media_rebase_p_w` |
| Media restart diagnostic | Not present | `media restart pulse must read only selected CRF disruption and the ungated media re-base` |
| `media_clock_restart.restart_p_i` | Not pinned here | One direct connection to `mcr_restart_p_w`, in its unconditional instance |
| Restart-port diagnostic | Not present | `media restart engine must consume mcr_restart_p_w directly` |
| `render_recentre_p_w` initializer | `gm_recentre_p_r \| eff_ptp_adjust_w \| cfg_ptp_cmd_load \| src_recentre_p_r` | `media_rebase_p_w \| src_recentre_p_r` |
| Render diagnostic | `render recentre pulse must read only the GM-change, adjtime, settime and settled clock-source discontinuities` | `render recentre pulse must read only the media re-base and settled clock-source discontinuities` |
| Initializer comment | The render initializer is the extra PHC reader; four admitted terms | Media re-base is the extra PHC reader; both consumers are pinned; GM identity alone adds no render event |

Every other PHC census count is unchanged. The new restart term
is outside the CRF-selection condition. Exact initializers, reference
counts and the restart-port pin admit only the specified consumers.

## Mutation entries and documentation

| Entry | Before | After / required refusal |
|---|---|---|
| ADP term spliced into the render recentre pulse | Old four-term expression plus ADP; old render reason | Retained label, new two-term expression plus ADP; new render reason |
| GM identity restored as a render recentre term | Absent | Adds `gm_recentre_p_r`; new render reason |
| ADP term spliced into the media re-base pulse | Absent | Adds ADP while preserving counts; media re-base initializer reason |
| ADP term spliced into the media restart pulse | Absent | Adds ADP while preserving counts; media restart initializer reason |
| media restart engine port gated by ADP | Absent | Gates the engine input; direct restart-port reason |
| additional PHC crossing reader | Absent | New net reads `phc_load_ts_w`; exactly 4 references required, found 5 |
| additional media re-base reader | Absent | New net reads `media_rebase_p_w`; exactly 3 required, found 4 |
| additional media restart reader | Absent | New net reads `mcr_restart_p_w`; exactly 2 required, found 3 |

`mutation-census.json` compares the literal entries in the three main
tables: 195 before, 202 after, seven added, none lost.
`mutation-collection-integrity.json` proves every other mutation collection
and all conditional/generated additions are AST-identical. The existing
render-ADP entry remains; its expected diagnostic follows the decided pin.

The gate's closing integration statement now names the shared re-base,
its two readers, the settled source change and the ungated restart.
Previously it described only the direct PHC and transport seams.

The firmware document gains four constraint rows matching the exact census,
render initializer and restart initializer/port above. Its existing PHC row
is retained. A new paragraph records all seven new controls and the retained
render-ADP control, including their compiler-absent structural checks and
elaboration requirement. No refusal or documented limitation was removed.

## Reproduction and receipts

Every gate runs synchronously through `run_gate.py`, with a 10800-second
timeout, output directly to a file and the actual exit code recorded in JSON.
No gate is piped. SDKs and environments remain outside this packet.

The SDK command runs the bank's `full-builder-sdk.py` with `python3 -u`
from the repository root. The packet copy changes only the argv-receipt
pathname so the manager's existing failed receipt remains intact.
The exact compiler mapping and `--require-rv32` are unchanged.
`sdk-wrapper-provenance.json` records both script hashes.
`full-builder-sdk-argv.jsonl` records requested and executed argv.

The compiler-absent command is `python3 sw/builder/test_builder.py`.
`PYTHONPATH=$VALIDATION_STORAGE/387-a269-absent-control` supplies the recorded
`compiler-absent-sitecustomize.py`: only the three RV32 compiler candidates
raise `FileNotFoundError`, and only in the full builder process.
Host commands, shared compiler files and HOME are unchanged.
`full-builder-absent-argv.jsonl` records those refusals.

The receipt runner reuses the bank's pinned environment. Each gate JSON
records its command, working directory, environment, exit code, duration
and log hash. `tested-files.json` records the tested source hashes.

## Gate table

| Gate | Exit | Result | Receipt |
|---|---|---|---|
| Full builder with pinned SDK: `python3 -u full-builder-sdk.py` | 0 | 224/224 mutations rejected; 53/53 RTL variants elaborated; 115 census compiles state RV32, none unstated; 239 audited SDK invocations | [builder-sdk-1.log](builder-sdk-1.log), [JSON](builder-sdk-1.json) |
| Full builder without cross compiler: `python3 sw/builder/test_builder.py` | 0 | 189/189 applicable mutations rejected; 53/53 RTL variants elaborated; all three RV32 candidates audited as absent | [builder-no-compiler.log](builder-no-compiler.log), [JSON](builder-no-compiler.json) |
| `python3 scripts/docs_check.py`, Git CI mode | 0 | 0 findings; 165 Markdown / 859 text files; 23/23 scrub controls, 4/4 routing arms | [docs-check.log](docs-check.log) |
| Same command, no-Git CI mode | 0 | 0 findings; same file population; 22/22 scrub controls, 4/4 routing arms; Git inventory-parity arm inapplicable | [docs-check-no-git.log](docs-check-no-git.log) |
| `python3 scripts/check_feature_status.py`, no-Git CI companion | 0 | 0 findings | [feature-status-no-git.log](feature-status-no-git.log) |
| `python3 scripts/check_em_dash.py --base 57456af96b3127b9d309a995bbbd35a6113ce52d` | 0 | 0 findings; 339/339 controls | [em-dash.log](em-dash.log) |
| `python3 scripts/check_doc_style.py` | 0 | OK | [doc-style.log](doc-style.log) |
| `python3 scripts/check_baremetal_only.py --check` | 0 | 0 findings | [baremetal-only.log](baremetal-only.log) |
| `python3 scripts/check_py_idiom.py` | 0 | Every category within its existing budget | [py-idiom.log](py-idiom.log) |
| `git diff --check` | 0 | Clean | [diff-check.log](diff-check.log) |
| `git diff --check 57456af96b3127b9d309a995bbbd35a6113ce52d HEAD` | 0 | Clean committed candidate | [diff-check-base.log](diff-check-base.log) |

Both full builder runs executed every suite function. The SDK run reports
`ALL GATES PASS EXCEPT 1 NOT RUN`: only gate 11's hardware-report calibration
lacks its external report. The compiler-absent run reports two NOT RUN arms:
that same calibration and the intentionally unavailable gate 1b compiler
instruments. Structural refusal coverage remains active in both modes.
Neither run claims those absent measurements.

The restored-GM and additional-PHC-reader mutants are reason-pinned entries
in both successful mutation loops. Both are among the 53 elaborated variants.
The GM control fails the new render initializer reason; the added PHC reader
fails `phc_load_ts_w must have exactly 4 live references, found 5`.
All seven new controls, and the retained render-ADP control, are in both runs.

The no-Git mode uses `git archive` of the final commit, extracted at
`$VALIDATION_STORAGE/387-a269-no-git`. This is a source export, not a checkout.
`candidate.tar` retains the exact export. Both changed files in the export
and final commit match the SHA-256 values measured for both builder runs.
`final-integrity.json` records the clean worktree, single parent and exact
changed-file set. All required submodules match their pins.

## Disposition

The round 1b assignment is met: the full SDK suite exits 0, the absent
control exits 0, no mutation entry is lost, both required negative controls
fail, every new consumer is admitted exactly, and RTL is unchanged.
The correction adds no open question. The existing calibration limitation
above is reported, not waived. This is author evidence for independent review.

No push, PR edit, merge, additional checkout, delegation or hardware action
was performed. The public handoff is posted as `[A269] REVIEW READY` on #387.

