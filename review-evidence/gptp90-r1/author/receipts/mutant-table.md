| Mutant | Verdict | Failing words (named checks, as printed) |
|---|---|---|
| a sync receipt timeout only clears sync-ok | caught | #89 Sync stops: the plane takes mastership<br>#89 never usable: the grandmaster is aged<br>#89 no Follow_Up: the plane takes mastership within syncReceiptTimeout and one BMCA pass<br>#89 Follow_Up after the next Sync: the plane takes mastership within syncReceiptTimeout and one BMCA pass<br>#89 Follow_Up with the next sequenceId: the plane takes mastership within syncReceiptTimeout and one BMCA pass |
| adoption leaves the Sync receipt watch off | caught | #89 never usable: the grandmaster is aged<br>#89 never usable: within syncReceiptTimeout of its adoption |
| an aged port takes Announces | caught | #89 never usable: the aged port stays master while Announces continue<br>#89 Sync stops: the aged port stays master while Announces continue<br>#89 no Follow_Up: the aged port stays master while Announces continue<br>#89 Follow_Up after the next Sync: the aged port stays master while Announces continue<br>#89 Follow_Up with the next sequenceId: the aged port stays master while Announces continue |
| a master steers on its aged peer's Sync | caught | #89 first grandmaster: Sync recovery is heard as master and steers nothing<br>#89 Sync stops: Sync recovery is heard as master and steers nothing<br>#89 no Follow_Up: Sync recovery is heard as master and steers nothing |
| a master hears no Sync | caught | #89 first grandmaster: the next Announce elects the grandmaster<br>#89 Sync stops: the next Announce elects the grandmaster<br>#89 no Follow_Up: the next Announce elects the grandmaster |
| a queued receipt timeout ages a master | caught | #89 takeover: the queued receipt timeout ages nothing |
| the Sync receipt watch is 100 ms | caught | #89 Sync stops: within syncReceiptTimeout and one BMCA pass<br>#89 first grandmaster: usable Sync keeps it elected<br>#89 Sync every 250 ms keeps the plane deferring |
| the Sync receipt watch is 500 ms | caught | #89 Sync stops: within syncReceiptTimeout and one BMCA pass<br>#89 no Follow_Up: the plane takes mastership within syncReceiptTimeout and one BMCA pass<br>#89 Follow_Up with the next sequenceId: the plane takes mastership within syncReceiptTimeout and one BMCA pass |
| a parent refresh expires the Sync watch | caught | #89 Sync stops: the Announce leaves the grandmaster elected |
| the adoption watch is 100 ms | caught | #89 never usable: within syncReceiptTimeout of its adoption<br>still slave inside the Sync receipt watch |
| a Follow_Up pairs whatever its sequenceId | caught | #89 Follow_Up after the next Sync: no unusable pair is consumed<br>#89 Follow_Up with the next sequenceId: no unusable pair is consumed |
| the Follow_Up watch is 50 ms | caught | #89 a Follow_Up 60 ms after its Sync is used |
| the tracking band is empty | caught | slew: second return pair stays inactive |
| lost responses clear asCapable at the first | caught | #90 no response: one loss keeps asCapable<br>#90 no follow-up: one loss keeps asCapable<br>#91 duplicated response: one loss keeps asCapable<br>#91 three responses: one loss keeps asCapable |
| lost responses clear asCapable at the fourth | caught | #90 no response: four losses keep asCapable<br>#90 no follow-up: four losses keep asCapable<br>#91 duplicated response: four losses keep asCapable<br>#91 three responses: four losses keep asCapable |
| lost responses clear asCapable at the sixth | caught | #90 no response: the fifth loss clears asCapable<br>#90 no follow-up: the fifth loss clears asCapable<br>#91 duplicated response: the fifth loss clears asCapable<br>#91 three responses: the fifth loss clears asCapable |
| the fifth loss stops the requests | caught | #90 no response: request 6 goes out<br>#90 no follow-up: runs from a capable plane<br>#90 no follow-up: runs from a completed exchange |
| a second response re-arms the pairing | caught | #91 duplicated response: the fifth loss clears asCapable<br>#91 duplicated response: no exchange completes<br>#91 three responses: the fifth loss clears asCapable<br>#91 three responses: no exchange completes |
| a third response re-arms the reset exchange | caught | #91 three responses: the fifth loss clears asCapable<br>#91 three responses: no exchange completes |
| same-identity duplicates are a storm | caught | #91 duplicates are not a storm: requests keep going out |
| a later response re-arms the frozen pair | caught | (any check) |
| a receipt timeout unlocks the servo | caught | (any check) |
| an incapable port's Announces still compete | caught | #82 Pdelay loss: Announces from the incapable port elect nothing |
| a queued receipt timeout clears a master's sync-ok | caught | #84 takeover: a queued receipt timeout keeps sync-ok<br>#84 every master cycle publishes sync-ok |
| lost Sync cancels the requester exchange | caught | (any check) |
| lost response cancels the requester exchange | caught | (any check) |
