# Round-2 check coverage

Generated from the mutation arm's log: each named check, and every control
whose verdict printed that check as failed.

| Check | Controls that fail it |
|---|---|
| #89 takeover: the queued receipt timeout leaves the port aged | only an expiry that ages a slave marks the port |
| #89 a lone pair heard as master: a later Announce elects nothing | only an expiry that ages a slave marks the port |
| #89 a lone pair heard as master: an Announce inside its watch elects the grandmaster | a master hears no Sync |
| #89 Announce lapse: a sync receipt timeout after mastership ages the next Announce | only an expiry that ages a slave marks the port<br>mastership stops the Sync receipt watch |
| #89 parked Sync: a Follow_Up 200 ms after it pairs with nothing | mastership stops the Follow_Up watch |
| #89 parked Sync: a Follow_Up 60 ms after it, after the takeover, is heard | mastership voids the parked Sync |
| p1 255 #89 gmPresent: a priority1 1 Announce on the aged port elects nothing | an aged port takes Announces |
| p1 255 #89 gmPresent: the aged port elects a priority1 255 grandmaster | an aged port refuses a priority1 255 grandmaster |
| p1 255 #89 gmPresent: a priority1 255 grandmaster without Sync stays elected | sync receipt ageing ignores gmPresent |
| p1 255 #89 gmPresent: a priority1 1 Announce on the aged port makes this plane master | an aged Announce is dropped rather than aged |
| #82 Pdelay loss: Announces from the incapable port elect nothing | an incapable receipt timeout keeps the elected peer<br>an incapable port's Announces still compete |

Controls in the log: 98; caught: 98.
