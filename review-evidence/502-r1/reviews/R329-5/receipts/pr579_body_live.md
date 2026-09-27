[A354]

Closes #502.

## Status

Round 5 at `90ab4a3da5b676f90b768b4f22b77ce7d0bd911d` addresses the full-read assignment and R329-4 F1, S1 and S2. The delivered live-write behavior remains unchanged.

## Description

Persistence status becomes pending on the first accepted live name write or actual parent map write. It stays pending through command completion and snapshot acknowledgement until reset; these groups still have no record writer.

Names use the accepted write export at processor pin `870ff88a`. Maps use the parent's phase-5 write enable, qualified by the store's change comparisons. An unchanged duplicate succeeds without changing the map or setting pending. Marks retain their command-completion meaning. All sources share the backend clock and reset.

The processor pin adoption, ROM ledger and boundary documentation are included in this PR. Round 5 changes documentation, comments and diagnostic labels only.

## Reproduce

Start from a durable baseline and issue SET_NAME or ADD/REMOVE_AUDIO_MAPPINGS. Pending must assert on the first live write, before the completion mark. From a fresh durable baseline, repeat an existing mapping: SUCCESS, unchanged map, pending clear.

The refusal controls send an out-of-range record or a two-record ADD whose second record conflicts with the first. They require status 7, an empty map, no storage change and both pending bits clear. GET_AUDIO_MAP diagnostics identify their input/output case, including successful exact-record checks and preloaded baselines.

## Validate

```sh
make -C tb/verilator/pp_shadow
make -C tb/verilator/pp_shadow pending-mutant
python3 scripts/docs_check.py
GIT_DIR=/dev/null python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base 831f94f4
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_doc_paths.py
git diff --check
```

Use the hash-locked Markdown environment in `tools/markdown/requirements.txt`. All assigned gates return rc 0 for this revision. The default target passes 591 + 591 + 591 + 295 checks with zero failures. The mutation target passes its 295-check clean control and detects 12 required K10/K12 failures under the historical late-mark trigger.

The focused target covers names, both map directions, duplicates, ADD, REMOVE, refusals, zero-record commands, reset, mark groups and snapshot acknowledgement. Its observer grades live storage and published status across every watched edge. Control-face preloads establish baselines without claiming persistence.

Broader regression, builder, area and additional mutation evidence in earlier reports applies to the heads named there. Those checks were not repeated in Round 5. No hardware evidence is added.

## Round 5

Both design pages were read end to end. The handoff records every section's disposition and the complete results of `git grep -n -E "pend_i *=|D2 sticky|D2 bit"` across the tracked tree.

Snapshot ownership section 13 now gives the current composition:

```text
pend_i = aecp_dyn_dirty_o | (|nvm_unflushed_w) | aecp_live_wr_w | aecp_live_pend_r
aecp_live_wr_w = aecp_name_wr_w | amap_live_wr_i
```

The materialization page states the same current equation. Historical evidence and proposed D3 behavior are explicitly distinguished. Proposed stage retirement accounts for both the direct pulse and sticky history. Reset and terminal summaries now follow the existing ownership rules: pending can clear when every record closes and no producer work remains, while dirty or writer retirement still prevents a durable reading in the no-load terminal state.

The exact-record diagnostic carries its case tag, and the CSR comment is rewrapped. Stimuli, assertions, expected values and check counts are unchanged. The shadow, datapath and backend files are byte-identical to the Round-5 starting head; the CSR code tokens are unchanged.

The issue's [A354] REVIEW READY comment records the exact commit and reproducible evidence.

## Definition of done

All three Round-5 assignment items are addressed. Independent review of the corrected head, required hosted checks, candidate-merge validation and maintainer merge authorization remain required. This correction adds no materialization, flash-restoration or hardware claim.
