[A269] REVIEW READY

Commit: `a9636e0f670f90f411da3024a141e93efa1872df` on `387-media-rebase`, local only. One-line subject, no body or trailers; worktree clean.

Under the [round 1b assignment](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5817362105), changed only `sw/builder/test_builder.py` and `docs/integration/BAREMETAL_FIRMWARE.md`. No RTL changed.

The render pin, message and retained ADP mutant now use `media_rebase_p_w | src_recentre_p_r`. The shared re-base initializer, both readers, restart initializer and direct engine connection are pinned exactly. The PHC strobe counts remain 5 and 3; new re-base/restart counts are exactly 3 and 2. The gate print and firmware constraint rows match.

| Validation | Result |
|---|---|
| Full builder, bank wrapper with pinned SDK and `--require-rv32` | rc 0; 224/224 mutations rejected; 53/53 RTL variants elaborated; 115 RV32 census compiles; 239 audited SDK invocations |
| `python3 sw/builder/test_builder.py`, all three cross candidates masked absent | rc 0; 189/189 applicable mutations rejected; 53/53 RTL variants elaborated |
| `docs_check.py`, both CI modes; no-Git `check_feature_status.py` | rc 0 |
| `check_em_dash.py --base 57456af96b3127b9d309a995bbbd35a6113ce52d`, `check_doc_style.py`, `check_baremetal_only.py --check`, `check_py_idiom.py` | rc 0 |
| `git diff --check`, plus committed diff against that base | rc 0 |

No reduction: all 195 existing literal mutation entries remain, with seven added (202); every generated collection and conditional addition is unchanged. Restoring `gm_recentre_p_r` fails the new render pin. Adding another reader of `phc_load_ts_w` fails its exact reference census. Both controls fail by their named reasons and elaborate in both runs.

The SDK suite's only NOT RUN arm is gate 11's missing hardware-report calibration. The absent-compiler run additionally reports the expected gate 1b compiler-instrument stand-down. No coverage is claimed for those arms.

Round 1b acceptance met; no new open question. `HANDOFF.md` records every pin/row before and after, each mutation, commands, receipts and source hashes in `$HOME/milan-fpga-management/2026-09-23/387-a269/`. The SDK wrapper copy changes only its receipt destination; its compiler mapping and arguments are unchanged. The no-Git gate used a source archive of this exact head.

No push, PR edit, merge or hardware action performed. This is author evidence for independent review.
