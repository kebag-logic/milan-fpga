# [A850] pins1125 (#1013, PR #1016): HANDOFF round 2

**Status (11-26 05:35): REVIEW READY at `e5d8a71b6fa90352eca72314c7bd2275a1b20285`.** One commit on `a6864a49`, on branch `1013-pins`. Local, not pushed, nothing posted. ETA: done; no unit is running.

## What changed

- `tb/verilator/gptp_shadow/sim_main.cpp`: phase 22's graded pair is built 400 ns off (`kGradedOffsetNs`), where the background pairs are at 0. It is graded by two checks:
  - `the graded Follow_Up is used: its offset is fresh`: the offset moved by more than 200 ns;
  - `its offset uses the delay floored at -800 ns`: within 64 ns of the previous offset less 400.
  - 483 checks become 490.
- `mutants.py`: two controls, `public_bank_keeps_a_stale_offset` and `graded_follow_up_not_sent`. The lifecycle test and README now count 16.
- `milan_dp/sim_gptp.cpp`: the harness-model check is renamed a precondition (R937-S1).
- Docs:
  - `GPTP_PLANE.md`: which suite grades which column, and the "then" sentence;
  - `SUBMODULES.md` and the change log: route equality for the paired routes only;
  - `gptp_plane/README.md`: the blank line removed.
- PR body: one `[A850]` line; the old-generator claim backed by an executed `milan_dp` `gptp` run (3 of 242 FAIL); route claims restricted to the measured pairs; the placement-identity claim dropped; counts updated.

## Judgement calls

- **Fresh by offset, not by a counter.** The wrapper exposes no adjfine strobe. An attributable offset grades exactly what the reviewers asked for: a stale bank, an unused pair, and an absent pair. The 400 ns step sits far inside the servo's slew band (step thresholds are 20 us and 100 us), and no PHC step is taken. The check reads the pre-pair offset, so the servo's residual between trials does not matter.
- **One control on the product, one on the harness.** The stale-bank control is product RTL in a private copy. The unsent pair is a harness control, the reviewers' own probe.
- **R938-F3: restated, not re-measured.** I did not route the base's AltSpreadLogic_high. The selected images are paired, and the unpaired row is marked as such.

## Not done

- The disk cleanup of my disposable scratch was refused twice by this session's permission system, so I did not retry it. The list is in the round-1 HANDOFF.md. The data disk is at 45 GB free now.
- Not re-run this round, as untouched by it: the firmware gate, the boundary gate, tables, txts, fuzz, gm_steps, the physical leg, the ledgers and the routes (see REVIEW-READY.md).

## For the manager

- Replace PR #1016's body with `round2/PR-BODY.md`. It has no tool attribution line.
- Receipts: `round2/receipts/INDEX.md` (10 files, host paths replaced).

REVIEW READY e5d8a71b6fa90352eca72314c7bd2275a1b20285
