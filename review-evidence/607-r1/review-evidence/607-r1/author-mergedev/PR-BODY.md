[A408]

Closes #607

The shipping XDC selected nonexistent clocks, rejected conditional Tcl, and left the
Ethernet delay budget masked by a generic synchronizer exception. AX7101 crossing clock selections
now come from the SoC objects. A post-synthesis Tcl hook applies the quasi-static
multicycles and scopes the MultiReg exceptions so all four Ethernet/sys/Milan data
directions receive the intended 8 ns bound. Existing asynchronous-reset exceptions
and the reset inter-stage bound remain.

Every completed shipping build now checks its implementation log and fails on
12-4739 or 20-1307 before publishing the flash manifest. Tests cover generated
names, optional domains, both Ethernet ports, exception scope and a live planted
wrong name that the vendor process accepts with rc 0 but the build check refuses.

Validation at `350af5dcf0aab9fc8ad8d6c6cde3552c63e26a75`: both complete builder banks, required elaboration,
documentation/static gates and the live negative control pass. The compiler-present
bank requires RV32. The historical Arty calibration report is unavailable; the
compiler-absent run records its expected compiler-dependent omissions.

Fresh AX7101 1x1 TDM8 results, using at most 16 threads:

| Place directive | Worst WNS ns | Worst WHS ns | Worst eth slack ns |
| --- | --- | --- | --- |
| AltSpreadLogic_high | +0.034 | +0.022 | +6.293 |
| ExtraTimingOpt | +0.268 | +0.022 | +6.290 |
| ExtraPostPlacementOpt | +0.105 | +0.036 | +6.232 |

All three seeds meet WNS >= +0.030 ns and WHS >= 0 at every reported corner. TNS and THS are zero. All four Ethernet pairs report Max Delay Datapath Only, with requirement 8.000 ns and no unsafe pair. Every implementation log has zero critical warnings and applies the quasi-static class to 112 cells.

No RTL, firmware or installed package changes. Exact commands, per-corner tables,
clock-interaction rows, warning counts and artifact hashes are retained in the
handoff packet. Independent review remains pending.


## Round 2

The builder bank now elaborates both shipping AX7101 shapes on e1 and e2,
without firmware compilation or a vendor run. It inspects the real emitted Tcl
for exactly one Ethernet hook, using the CRG output objects and placed between
synthesis and optimization, and rejects a generic MultiReg mask in the XDC.
M07, M16 and deletion of the hook call now fail this check.

The implementation-log gate also refuses 12-5201 and renames rejected bitstreams
to `.bit.rejected`, keeping them outside automatic bitstream discovery. Controls
cover all three diagnostic IDs, both board filenames, missing logs and retries.
The sweep instructions, clock-domain guide and stale GMII comment are corrected.
The optional toolchain swap stays after base construction: the installed platform
constructor takes a toolchain name, not a subclass, so moving it would duplicate
that initialization or change the installed package. A comment now requires every
hook to be configured after the replacement.

Validation at `f3bd6b6694ab61b8f70b7f13f1049a14a6fb3461`: both complete builder banks,
required elaboration, all documentation/static gates and the live wrong-name
control pass. The historical Arty calibration report remains unavailable, and the
compiler-absent bank records its expected omissions. The committed-head mutation
campaign rejects all nine planted defects; the unmodified control passes.

No timing result changes. The production constraint Tcl is byte-identical to
round 1 and placement-generating Python is unchanged. Regenerated Tcl/XDC for all
three seeds matches the retained inputs after output-directory normalization, so
the sweep was not repeated. All 117 retained sweep artifacts match their recorded
hashes, and the per-seed timing and Ethernet bounds above reproduce from the raw
reports.


## Round 3

At the round-2 head the required `elaborate` job failed in the new shipping-constraint arm.
LiteX resolves the picolibc and compiler-rt data packages for its firmware make variables
before it writes the gateware Tcl/XDC. The pinned install (`sw/litex/litex_pins.txt`) carries
neither package. Local banks were green only because the bench interpreter has both.

The arm still runs the real `milan_soc.main()`/Builder path. LiteX's include step now omits only
the firmware make and linker inputs (`variables.mak`, `output_format.ld`, `regions.ld`). No
firmware is built there, and the gateware does not read those files. The arm refuses firmware
data package imports on every interpreter, so a local bank fails as the hosted job would. It
also asserts that the include step ran through the probe. No pin, workflow, constraint, RTL or
firmware file changes, and the arm never skips. For all four shape/port pairs, the probe's
Tcl/XDC are byte-identical to a full Builder elaboration with the same arguments.

Validation at `a9f5e34faf51e01c9ecf95807d4a7e695b3eb1c3` used a fresh environment built as the
`elaborate` workflow builds it:
- Python 3.12, exactly the pinned LiteX set, the VexiiRiscv checkout and patch series, and the
  pinned sv2v and RV32 SDK. No firmware data package is installed.
- The hosted command `python3 sw/builder/test_builder.py --require-elaboration --require-rv32`
  ran all 91 arms and printed the four `[constraints] shipping ... PASS` lines. It passed with
  the historical Arty calibration report as the only recorded omission.
- The reviewers' no-picolibc reproduction now passes.
- M07, M16 and the in-guard call deletion stay red on the missing-hook assertion, in both the
  pinned and bench environments. The rest of the reviewer mutant set, and three new probe
  mutants, are red too.
- Both complete bench builder banks, the documentation/static gates and the live wrong-name
  control pass.

Timing is unchanged. No generated constraint or placement input changed, and all 117 retained
sweep artifacts still match their recorded hashes, so the per-seed table above stands. The
exact-head hosted `elaborate` confirmation follows the push.


## Merge with dev

Dev `7390b43627032c71c470e2aa8d0845eb5b740663` (after #395, PR #605) is merged at
`c7ee5cbd4ed6215b988f3811d5e9156e21aa55c5`. Only the three expected files conflicted, all with #395,
and each keeps both lanes' behaviour:
- `sw/litex/platforms/alinx_ax7101.py`: the scoped MultiReg toolchain is still installed first. #395's
  timing-grade setup before placement and its signoff reports after routing are then added to it.
- `sw/builder/test_builder.py`: `test_commercial_timing_grade` and `test_clock_crossing_constraints`
  each run once. No gate number or test name collides.
- `docs/integration/BUILDING.md`: #395's grade and corner text comes first, then this change's refusal
  gate and Ethernet bound.

The processor gitlink takes dev's `c951a9ff` (PR #613); this change pins nothing of its own. No
stale statement needed a separate commit.

The shipping builds prove the composition. In each, the emitted Tcl runs the Ethernet hook between
`synth_design` and `opt_design`, #395's grade configuration before `place_design`, and #395's signoff
reports after routing. Every seed wrote all 17 signoff reports.

Fresh AX7101 1x1 TDM8 sweep at the merge head, using at most 16 threads. Values are the worst over
#395's four declared corners, Slow and Fast at 0 and 85 C:

| Place directive | Worst WNS ns | Worst WHS ns | Worst eth slack ns |
| --- | --- | --- | --- |
| AltSpreadLogic_high | +0.312 | +0.036 | +6.141 |
| ExtraTimingOpt | +0.309 | +0.014 | +6.279 |
| ExtraPostPlacementOpt | +0.063 | +0.036 | +6.136 |

- Every seed meets WNS >= +0.030 ns and WHS >= 0 at every corner. TNS and THS are zero.
- All four Ethernet pairs read `Max Delay Datapath Only` at 8 ns in every interaction report, and no
  pair is unsafe.
- Each implementation log has zero critical warnings and applies the quasi-static class to 112 cells.
  The build gate accepted all three bitstreams.
- The round-1 table above describes the pre-merge head.

Validation at `c7ee5cbd`, all rc 0:
- the hosted `elaborate` command in a fresh pins-only environment: 96 arms and the four shipping PASS
  lines;
- both bench builder banks;
- the shipping-hook and timing-grade tests, in both environments;
- the live wrong-name control;
- the documentation and static gates, with the Markdown gates in the pinned environment and dev as
  the diff base.

The historical Arty calibration report remains the recorded omission. The delta review is pending.
