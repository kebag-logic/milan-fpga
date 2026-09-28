[A408] REVIEW READY

Commit: `350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75`
Branch: `607-xdc-clock-names`, based on `54ce877371ee6e8878cf67294e86c2a8481b62f6`.

Changed: AX7101 crossing clock selections now follow the SoC clock objects. A
post-synthesis Tcl hook applies the quasi-static class and scopes the generic
MultiReg exception outside the four bounded Ethernet/sys/Milan data directions.
Every completed shipping build checks its implementation log and refuses 12-4739
or 20-1307 before manifest publication. Tests and authoritative build/testing docs
cover the changed contract. No RTL, firmware or installed package was edited.

Validation at this commit:

- `python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration`: rc 0.
- Complete builder bank with the three cross-compiler candidates deliberately
  unavailable, retaining required elaboration: rc 0.
- Documentation/static gate set: all final commands rc 0. The packet records
  81 final gate verdicts with exact commands, durations and log hashes,
  including both banks and the live control.
- Live wrong-name control: the planted implementation process returned 0 and
  emitted both required diagnostic IDs; the build log check refused them.
- Fresh AX7101 1x1 TDM8 sweep: all three build and report commands rc 0, at most
  16 threads per invocation, sequentially, with outputs under the physical data path.

Worst values over Slow/Fast at 0 C and 85 C:

| Place directive | WNS ns | TNS ns | WHS ns | THS ns | Eth slack vs 8 ns |
| --- | --- | --- | --- | --- | --- |
| AltSpreadLogic_high | +0.034 | 0.000 | +0.022 | 0.000 | +6.293 |
| ExtraTimingOpt | +0.268 | 0.000 | +0.022 | 0.000 | +6.290 |
| ExtraPostPlacementOpt | +0.105 | 0.000 | +0.036 | 0.000 | +6.232 |

Acceptance 1-4: met. Every fresh implementation applies the 112-cell quasi-static
class. Each Ethernet direction reports requirement 8.000 ns and positive slack;
all four crossing pairs report Max Delay Datapath Only. No reported Ethernet pair
is unsafe. All three seeds meet WNS >= +0.030 ns and WHS >= 0 at every reported
corner, with TNS = THS = 0.

Before/after emitted CRITICAL WARNING census: shipping input 14 (10 x 12-4739,
2 x 20-1307, 2 x 12-5201); every fresh seed 0. The supplied shipping artifacts
and installed constraint-source hashes remain unchanged.

Retained scope and limits: asynchronous reset PRE exceptions and the existing
2 ns reset inter-stage bound remain; the 8 ns bound covers data crossings. An
upstream generic-constraint template change causes an explicit build refusal.
Both banks report the unavailable historical Arty calibration report; absent mode
also records its intentionally unavailable compiler instruments. No required
elaboration arm was skipped.

HANDOFF.md contains the per-acceptance file:line evidence, full gate table,
per-corner timing and crossing tables, interaction rows and artifact hashes.
PR-BODY.md is prepared. Independent review remains with [R382] and [R383].
No push, PR mutation, merge or hardware action was performed.
