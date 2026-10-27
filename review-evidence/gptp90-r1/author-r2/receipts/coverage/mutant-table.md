# Round-2 controls and the checks they failed

Generated from `repo-gates-head/04b-engine-mutants.log`: each new or repaired control, its verdict,
and the failed lines its named-verdict printed.

| Control | Verdict | Failing checks (as printed) |
|---|---|---|
| only an expiry that ages a slave marks the port | caught | #89 takeover: the queued receipt timeout leaves the port aged<br>#89 a lone pair heard as master: a later Announce elects nothing<br>#89 Announce lapse: a sync receipt timeout after mastership ages the next Announce |
| sync receipt ageing ignores gmPresent | caught | p1 255 #89 gmPresent: a priority1 255 grandmaster without Sync stays elected |
| an aged port refuses a priority1 255 grandmaster | caught | p1 255 #89 gmPresent: the aged port elects a priority1 255 grandmaster |
| an aged Announce is dropped rather than aged | caught | p1 255 #89 gmPresent: a priority1 1 Announce on the aged port makes this plane master |
| mastership stops the Sync receipt watch | caught | #89 Announce lapse: a sync receipt timeout after mastership ages the next Announce |
| mastership stops the Follow_Up watch | caught | #89 parked Sync: a Follow_Up 200 ms after it pairs with nothing |
| mastership voids the parked Sync | caught | #89 parked Sync: a Follow_Up 60 ms after it, after the takeover, is heard |
| a queued receipt timeout ages a master | caught | #89 takeover: the queued receipt timeout ages nothing |
| a sync receipt timeout only clears sync-ok | caught | #89 Sync stops: the plane takes mastership<br>#89 never usable: the grandmaster is aged<br>#89 no Follow_Up: the plane takes mastership within syncReceiptTimeout and one BMCA pass<br>#89 Follow_Up after the next Sync: the plane takes mastership within syncReceiptTimeout and one BMCA pass<br>#89 Follow_Up with the next sequenceId: the plane takes mastership within syncReceiptTimeout and one BMCA pass |
| an aged port takes Announces | caught | #89 never usable: the aged port stays master while Announces continue<br>#89 Sync stops: the aged port stays master while Announces continue<br>#89 no Follow_Up: the aged port stays master while Announces continue<br>#89 Follow_Up after the next Sync: the aged port stays master while Announces continue<br>#89 Follow_Up with the next sequenceId: the aged port stays master while Announces continue<br>p1 255 #89 gmPresent: a priority1 1 Announce on the aged port elects nothing |
| a master hears no Sync | caught | #89 first grandmaster: the next Announce elects the grandmaster<br>#89 Sync stops: the next Announce elects the grandmaster<br>#89 no Follow_Up: the next Announce elects the grandmaster<br>#89 a lone pair heard as master: an Announce inside its watch elects the grandmaster |
| a queued receipt timeout clears a master's sync-ok | caught | #84 takeover: a queued receipt timeout keeps sync-ok<br>#84 every master cycle publishes sync-ok |
| a receipt timeout unlocks the servo | caught | (any check) |
| an incapable port's Announces still compete | caught | #82 Pdelay loss: Announces from the incapable port elect nothing |
