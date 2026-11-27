Walk only the marked sinks at an ACMP entry's completion, and compare without building

Branch `977-settle` (local, for the manager to push): two commits on `main` `a795471c` (the merge of PR 38), rebased from `69bac7c`, then `main` `c3bff8f3` (the merge of PR 40) merged in.

- `6390129` Walk only the marked sinks at an entry's completion, and read the saved record and the reported view field by field, with the same calls in the same order.
- `175cf9e` Compare the saved binding record octet by octet, and copy a view's binding and stream field by field, without out-of-line wire reads or a memcpy.
- `5d03517` Merge `main` `c3bff8f3` (PR 40: seed the ADP delay on each transition out of DOWN). It is a merge commit, and the branch is not rebased again.

milan-fpga pins this head for [#977](https://github.com/kebag-logic/milan-fpga/issues/977) for now (`pf-977-1`, through its merge of `dev-soft-core`). The pin moves to this PR's merge commit on `main` once merged, never to the branch.

Integration notes:

- **The rebase onto `a795471c`** conflicted in `CHANGELOG.md` only. Both unreleased entries are kept, this one first.
- **The merge of `c3bff8f3`** conflicted in `CHANGELOG.md` only, resolved the same way.
- **`tests/mutations.json`** merged both times without conflict. This PR's ACMP mutants and PR 40's ADP mutants are disjoint, and the needle audit and the mutation campaign below hold every anchor.
- **The branch merges with `dev-linux`** (`9e1cd60`) without conflict (`git merge-tree`).

## Why

[milan-fpga #977](https://github.com/kebag-logic/milan-fpga/issues/977): an instruction-level profile on milan-fpga's RV32 control CPU found these costs. A record replacing every input's Talker at nine sinks is followed by nine `acmp_tk_kind_changed` calls. Their completion, `finish()`, took 40,948 of THE SETTLE's 47,231 CPU cycles, about 4,550 a sink.

- Each call walked every sink four times (`publish`, `rearm`, `admit` and the persist and report loop), loading and testing the mark word for each sink.
- For the one marked sink it built a 20-octet binding record (`memset` and three `wire_put_be` calls) and an 80-octet view (`memset` and two struct copies through `memcpy`), only to compare them.

On that core a dependent instruction retires about 5 cycles after its producer, and an independent one each cycle.

## What changes

- `publish`, `admit` and the persist and report loop visit sinks `0 .. n_sinks - 1`, loading each mark word once and shifting it. They skip an unmarked sink at a register test. The sinks visited, their order and the bound are those of the walk over every sink. A mark past `n_sinks`, which the walk test's full-walk core sets, is still ignored.
- Persistence: `record_moved` compares the saved octets with the record `record_of` would write: the flags, the reserved octet, the unique ID, and the Talker's and the controller's entity IDs, all zero while unbound. Only when they differ does `record_of` write the saved record, followed by `p_persist`.
- Reporting: `view_moved` compares the fields `view_equal` compared, read from the sink: the stream, probing status, ACMP status, bound, started, Talker registered and registering failed. Only when one differs, and no change is owed, does `view_of` write the reported view, followed by `p_changed`.
- `view_of` copies the binding and the stream field by field, after its `memset`.
- The marks are cleared word by word.

The calls, their order and their arguments are unchanged ([ACMP-13](docs/REQUIREMENTS.md#acmp-changed-sink-walk)). No protocol behaviour changes, and no requirement, structure or public header changes.

## Planted defects

Nine planted defects selected the old lines. Each is re-anchored to the same defect at the new lines, killed by the same test and needle:

- `acmp-nothing-persisted`, `acmp-unbind-not-persisted`, `acmp-rebind-not-persisted`
- `acmp-discovery-notifies`, `acmp-status-not-notified`, `acmp-probing-status-not-notified`
- `walk-marked-word-zero` (now the publication walk's word load), `walk-marks-never-cleared`, `walk-clear-first-word-only`

milan-fpga's own firmware campaign plants seven defects in this file's old lines (the first six above, by the same names, and one that moves the publication behind the report); its pin commit series re-anchors them the same way.

## Validation

The quality job is reproduced on the host by `scripts/validate.py --work <dir> --jobs 8 --graphs`, with the pinned Clang 18.1.3, clang-tidy 18.1.3, GoogleTest 1.14.0 and mermaid-cli 11.16.0.

| Head | Gates | Mutation campaign | `src/acmp.c` coverage |
|---|---|---|---|
| `977-settle` `5d03517` (`main` `c3bff8f3` merged) | 28 of 28 | 512 caught, 0 escaped | 877/877 lines, 468/468 branches |
| `977-settle` `175cf9e` on `a795471c` | 28 of 28 | 489 caught, 0 escaped | 877/877 lines, 468/468 branches |
| (before the rebase) `f71c887` on `69bac7c` | 28 of 28 | 479 caught, 0 escaped | 877/877 lines, 468/468 branches |

- The 33-sink walk test compares the changed-sink walk with a core whose every mark bit is set, at 1, 8, 32 and 33 sinks, and requires the same calls. It passes under `-fsanitize=shift,undefined`. An intermediate version, which bounded the walk by the set bits alone, was caught by it (index 34 of 33).
- The evidence is of this exact head, `5d03517`. `src/adp.c`, which only PR 40 changes, is at 215/217 lines and 95/102 branches, with 100 % after the job's exclusions.
- The bare-metal job (`scripts/baremetal.py`) passes at this head: the freestanding RV32 port is built with `riscv64-elf-gcc`, audited, and run under `qemu-system-riscv32` (ADP discovery and backpressure, ACMP restore and rollback, MAAP timers and range bounds, four generated entity round trips). milan-fpga's RV32 firmware build also compiles these sources freestanding at `-Os`, and its CPU budget harness and firmware gate ran them.

## Measured effect (milan-fpga, CPU budget harness)

Every arm of milan-fpga's CPU budget harness was run at 1x1/1if and 8x8/1if with this head pinned (milan-fpga `pf-977-1`: its merge of `dev-soft-core` and this branch at `5d03517`), and every arm passes. The cut changes no frame: milan-fpga round 5's wire-level differentials against the earlier pin's image found only named timing effects. PR 40's seed adds one `NOW_MS` read to milan-fpga's LINK_UP path, which milan-fpga states.

| Image | THE SETTLE at 8x8/1if (nine sinks), cycles a sink | the registering record all in, cycles a Talker |
|---|---:|---:|
| milan-fpga round 3 (pin `715589c`) | 5,444 | 13,877 (150 us) |
| this branch pinned, the split image's hot list relearned on it (milan-fpga round 5) | 4,121 | 12,519 (135 us) |
| this head, `5d03517` (milan-fpga round 8; at most, over both registering arms) | 4,136 | 12,806 (135 us) |
| this branch + a one-entry prototype for THE SETTLE (not in this PR; round 4) | 2,302 | 11,145 (120 us) |

At 1x1/1if (two sinks) the record is at most 11,172 cycles a Talker all in at this head (120 us; 10,826 on round 5's image; 13,391 before the cut).

The change adds 488 B of text to `acmp.o` at `-Os` (13,452 to 13,940 B), 512 B of ROM in each milan-fpga image.

At nine sinks most of the remaining completion cost is the nine completions themselves, each re-arming the interface's timer over every sink. Completing them in one entry would be a new public entry, not part of this change.

