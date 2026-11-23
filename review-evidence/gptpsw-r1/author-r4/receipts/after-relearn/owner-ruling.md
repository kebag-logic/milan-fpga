Source: https://github.com/kebag-logic/milan-fpga/issues/884#issuecomment-7084113326

[A10] Ruling on the gPTP lane's round-4 stop (2026-11-22). The held row backlog-owed.service.aecp.last.if0 is 62.182 ms at 8x8/1if, against its ledger figure of 62.16 ms.
- **The figure does not move.** Per the earlier rulings, a ledger figure is not restated for the change being measured, and a statement step is not a tolerance.
- **The cause is partly placement, and that is a real cost.** gptp_mbx.c rose from 149,287 to 214,320 cycles over backlog-owed's passes because the port's code grew ahead of it.
- **The fix:** relearn the hot list by its standard procedure (the procedure the optimisation line uses), with the gPTP port's and adapter's paths measured into it. This is the documented layout process, not tuning to the row. Then re-measure all seven held rows and round 2b's other conditions.
- **If the row still fails after a principled relearn,** it comes back for a ruling, with the phase analysis.
