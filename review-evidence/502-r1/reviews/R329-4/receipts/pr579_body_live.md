[A353]

Closes #502.

## Status

Round 4 at `92c6154a17d1f1192f20a3a642e6a01b616afb67` completes the documentation sweep and refusal-case diagnostic tags.
The delivered live-write behavior is unchanged.

## Description

Persistence status becomes pending on the first accepted live name write or actual parent map write. It stays pending through command completion and snapshot acknowledgement until reset; these groups still have no record writer.

Names use the accepted write export at processor pin `870ff88a`. Maps use the parent's actual phase-5 write enable, qualified by the store's existing change comparisons. An unchanged duplicate succeeds without changing the map or setting pending. Marks retain their command-completion meaning. All sources share the backend clock and reset.

The processor pin adoption, ROM ledger and boundary documentation remain included in this PR. Round 4 changes documentation, comments and diagnostic labels only.

## Reproduce

Start from a durable baseline and issue SET_NAME or ADD/REMOVE_AUDIO_MAPPINGS. Pending must assert on the first live write, before the later completion mark. From a fresh durable baseline, repeat an existing mapping: SUCCESS, unchanged map, pending clear.

The refusal controls send an out-of-range record or a two-record ADD whose second record conflicts with the first. They require status 7, an empty map, no storage change and both pending bits clear. Their status and map-count diagnostics identify the input/output case.

## Validate

Run:

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

The focused default target covers names, both map directions, duplicates, ADD, REMOVE, refusals, zero-record commands, reset, mark groups and snapshot acknowledgement. Its observer grades live storage and published status across every watched edge. Control-face preloads establish baselines without claiming persistence.

Broader evidence previously recorded at round-2 head `5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e` remains historical: 55 default suites passed with 2,125,319 checks and zero failures/timeouts; both full builder modes passed with their declared fixture exclusions; area measurements were recorded. Those checks were not repeated in Round 4. The four previously declared field/freshness skips provide no hardware evidence.

Round-3 head `867a2e38a4e3231545a0a24b97d1e5612a6659fe` added the partial-refusal controls. Independent reports record the P4 failures in both applicable legs and a passing 327-check multi-record probe. These are prior-head results, not new Round-4 runs.

## Round 4

The materialization page now records the #502 reporting window as resolved. It identifies accepted name writes, actual parent phase-5 map writes, unchanged-map exclusion and completion marks consistently. The rejected mark trigger and original release behavior are explicitly historical. Proposed D3 record-writer behavior remains separate from current pending reporting.

The whole tracked tree was searched, including documentation, READMEs, changelog, code comments and test descriptions. The sweep also corrected the backend contract comment, co-simulation coverage description and VERSION diagnostic. The retired `aecp_mark_pend_r` identifier has no matches. Every search pattern and hit has a disposition in the handoff.

The refusal status and GET_AUDIO_MAP count checks now carry their case names. Payloads, assertions, expected values and check counts are unchanged.

All assigned local gates return rc 0 at this head. The focused target passes 591 + 591 + 591 + 295 checks with zero failures. The mutation target passes its 295-check clean control and detects the required K10/K12 late-mark failures. Documentation checks pass with and without Git; the em-dash, style, TOC, anchor, path and whitespace gates pass.

The issue's [A353] REVIEW READY comment records the exact commit and reproducible commands.

## Definition of done

All three Round-4 assignment items are addressed. Current-head independent review, required hosted checks, candidate-merge validation and maintainer merge authorization remain separate merge gates. This correction adds no materialization, flash-restoration or hardware claim.

