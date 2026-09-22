| # | fixture | class | unchanged rc / verdict | candidate rc / verdict | G1 H T |
|---|---|---|---|---|---|
| 1 | `positive-replay-far-extension` | positive | 1 STRANDED | 0 contained | Y Y Y |
| 2 | `positive-replay-two-later-commits` | positive | 1 STRANDED | 0 contained | Y Y Y |
| 3 | `two-redundant-merges` | conservative FN (one-merge cap; per-merge variant would accept) | 1 STRANDED | 1 STRANDED | N Y Y |
| 4 | `control-replay-no-later-edit` | control: existing path arm | 0 contained | 0 contained | Y Y Y |
| 5 | `control-revert-then-reapply` | control: existing path arm | 0 contained | 0 contained | Y Y Y |
| 6 | `pr62-faithful-later-rewrite` | conservative FN (mirrors actual PR62) | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 7 | `later-disabling-rewrite` | negative: reversion by edit (twin of pr62-faithful) | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 8 | `published-shape-adjacent-extension` | conservative FN (legit extension adjacent to a replayed hunk) | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 9 | `later-deletion-of-touched-file` | refused: later deletion removes replayed work | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 10 | `later-exec-bit-loss` | refused: later exec-bit reversion | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 11 | `later-binary-edit` | explicitly unresolved: binary later edit unmeasurable | 1 STRANDED | 1 UNKNOWN | Y Y ? |
| 12 | `exact-revert-whole-replay` | negative: later reversion | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 13 | `exact-revert-pr-commit` | negative: later reversion | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 14 | `partial-revert-one-hunk` | negative: later reversion | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 15 | `revert-plus-far-extension` | negative: later reversion | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 16 | `revert-under-hostile-merge-config` | negative: reversion + ours driver/textconv | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 17 | `omitted-linear-commit` | negative: omitted linear work | 1 STRANDED | 1 STRANDED | Y N N |
| 18 | `omitted-part-of-a-commit` | negative: omitted linear work | 1 STRANDED | 1 STRANDED | Y N N |
| 19 | `whitespace-different-postimage` | negative: whitespace | 1 STRANDED | 1 STRANDED | Y N N |
| 20 | `repeated-block-other-location` | negative: hunk position | 1 STRANDED | 1 STRANDED | Y N N |
| 21 | `merge-resolution-work-missing` | negative: resolution work | 1 STRANDED | 1 STRANDED | N Y N |
| 22 | `merge-resolution-work-present` | conservative FN (AC2 'unless') | 1 STRANDED | 1 STRANDED | N Y Y |
| 23 | `merge-one-byte-evil-change` | negative: resolution work | 1 STRANDED | 1 STRANDED | N N N |
| 24 | `octopus-merge` | negative: octopus | 1 STRANDED | 1 STRANDED | N Y Y |
| 25 | `octopus-absorbed-third-parent` | conservative FN (scope: two parents only) | 1 STRANDED | 1 STRANDED | N Y Y |
| 26 | `unrelated-parent-merge` | negative: unrelated parent | 1 STRANDED | 1 STRANDED | N Y Y |
| 27 | `redundant-plus-nonredundant-merge` | negative: multiple merges | 1 STRANDED | 1 STRANDED | N Y Y |
| 28 | `first-parent-is-grandparent` | conservative FN (distance 2) | 1 STRANDED | 1 STRANDED | N Y Y |
| 29 | `reversed-parent-order` | negative: shape | 1 STRANDED | 1 STRANDED | N Y Y |
| 30 | `linear-control-exact-revert` | pre-existing linear historical arm (unchanged) | 0 contained | 0 contained | N Y N |
| 31 | `linear-control-adjacent-extension` | pre-existing linear historical arm (unchanged) | 0 contained | 0 contained | N Y N |
