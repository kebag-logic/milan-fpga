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
