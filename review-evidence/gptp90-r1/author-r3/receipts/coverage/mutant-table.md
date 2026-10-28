# Mutation arm at 42f9541e: every control's verdict

Generated from `repo-gates-head/04b-engine-mutants.log`. Failing words are the named checks the arm printed as failed.

| Control | Round 3 | Verdict | Failing words |
|---|---|---|---|
| slew level tied low |  | caught | slew: policy decision starts at +101 ns |
| slew clears at the first in-band pair |  | caught | slew: first in-band pair cannot clear |
| the tracking band is empty |  | caught | slew: second return pair stays inactive |
| slew clears before the replacement rate |  | caught | slew: no clear precedes the replacement rate |
| slew idle lapse arms qualification |  | caught | slew: in-band pair after idle timeout stays inactive |
| slew idle asCapable loss arms qualification |  | caught | slew: in-band pair after asCapable recovery stays inactive |
| slew mastership keeps qualification |  | caught | slew: in-band return from GM stays inactive |
| result face always ready |  | caught | (plain verdict) |
| result value taken without an accepted beat |  | caught | (plain verdict) |
| result tag taken without an accepted beat |  | caught | (plain verdict) |
| recorded t1 survives reset |  | caught | (plain verdict) |
| byte face advances without ready |  | caught | (plain verdict) |
| lost t1 fabricates a time and a companion |  | caught | (plain verdict) |
| lost Sync cancels the requester exchange |  | caught | (plain verdict) |
| lost response cancels the requester exchange |  | caught | (plain verdict) |
| a later response re-arms the frozen pair |  | caught | (plain verdict) |
| the tail runs before its own t1 |  | caught | (plain verdict) |
| a new request leaves the old pair live |  | caught | (plain verdict) |
| credit gate removed from the Pdelay_Req leg |  | caught | (plain verdict) |
| credit gate removed from the Sync leg |  | caught | (plain verdict) |
| credit gate removed from the Announce leg |  | caught | (plain verdict) |
| every pair uses the locked threshold |  | caught | (plain verdict) |
| every pair uses the link-up threshold |  | caught | (plain verdict) |
| exactly the threshold steps |  | caught | (plain verdict) |
| the step arm is unreachable |  | caught | (plain verdict) |
| a grandmaster change unlocks the servo |  | caught | (plain verdict) |
| a receipt timeout unlocks the servo | re-planted | caught | (plain verdict) |
| becoming grandmaster unlocks the servo |  | caught | (plain verdict) |
| the locked threshold is 200 us |  | caught | (plain verdict) |
| asCapable's rise keeps the lock |  | caught | (plain verdict) |
| the whole trim is not clamped |  | caught | (plain verdict) |
| the trim clamp is one unit wider than the envelope |  | caught | (plain verdict) |
| the integrator is not clamped |  | caught | (plain verdict) |
| reset leaves the grandmaster zero |  | caught | #82 cold release: every cycle to the first beat names thisClock<br>#82 cold release: every cycle to the first beat has {thisClock}<br>#82 cold release: that commit carries thisClock and {thisClock}<br>#82 warm reset: it names thisClock, not the elected peer<br>pre-init deep Announce: GM stays thisClock |
| reset keeps the elected grandmaster |  | caught | #82 warm reset: it names thisClock, not the elected peer |
| the thisClock words are read swapped |  | caught | #82 cold release: every cycle to the first beat names thisClock<br>#82 cold release: that commit carries thisClock and {thisClock} |
| reset leaves the path empty |  | caught | #82 cold release: every cycle to the first beat has {thisClock}<br>#82 cold release: that commit carries thisClock and {thisClock}<br>#82 warm reset: its path is {thisClock} with a zero tail |
| reset keeps the elected tail |  | caught | #82 warm reset: its path is {thisClock} with a zero tail<br>#82 every commit naming thisClock carries {thisClock} |
| no engine commit after reset |  | caught | #82 cold release: one commit before the first beat<br>#82 warm reset: one commit in the first 2 ms |
| the boot commit fires twice |  | caught | #82 cold release: one commit before the first beat<br>#82 warm reset: one commit in the first 2 ms |
| the boot commit never retires |  | caught | #82 cold release: one commit before the first beat |
| the boot commit waits for the timer bootstrap |  | caught | #82 cold release: that commit is the first edge after release<br>#82 warm reset: that commit is the first edge after release<br>pre-init deep Announce: no commit |
| a warm reset keeps the retained best record |  | caught | #82 warm reset: a worse-than-local peer leaves thisClock<br>#82 warm reset: the live worse peer wins, not the absent A<br>#82 warm reset: the live peer carries its own path |
| an unwritten best record reads as the best vector |  | caught | #82 warm reset: a worse-than-local peer leaves thisClock<br>#82 warm reset: the live worse peer wins, not the absent A |
| a winning peer's grandmaster is not published |  | caught | #82 peer wins: its commit names the peer GM<br>#82 warm reset: the live worse peer wins, not the absent A<br>#84 the run hands mastership to a peer<br>#85 direct grandmaster: elected<br>#85 multi-hop grandmaster: elected<br>#85 seven received entries: elected<br>#85 eight received entries: elected<br>#85 absent path: elected     |
| a winning peer's path is not staged |  | caught | #82 peer wins: its commit carries the peer path<br>#82 warm reset: the live peer carries its own path |
| the self publication keeps the departed grandmaster |  | caught | #82 peer leaves: the mastership commit names thisClock<br>#82 Pdelay loss: thisClock is committed within 2 ms of the fall<br>#82 Pdelay loss: that mastership names thisClock, {thisClock}<br>#85 direct grandmaster: the degraded grandmaster yields<br>#85 multi-hop grandmaster: the degraded grandmaster yields<br>#85 seven received entries: the degraded grandmaster yields<br>#85 eight received entries: the degraded grandmaster yields<br>#85 absent path: the degraded grandmaster yields |
| the self publication keeps the departed path |  | caught | #82 peer leaves: the mastership commit path is {thisClock}<br>#82 Pdelay loss: that commit carries {thisClock}<br>#82 Pdelay loss: that mastership names thisClock, {thisClock}<br>#82 every commit naming thisClock carries {thisClock} |
| the self publication keeps the departed record |  | caught | #82 Pdelay loss: once capable, a live peer worse than D wins |
| an asCapable fall leaves the receipt watch running |  | caught | #82 Pdelay loss: thisClock is committed within 2 ms of the fall |
| an incapable receipt timeout keeps the elected peer |  | caught | #82 Pdelay loss: thisClock is committed within 2 ms of the fall<br>#82 Pdelay loss: that commit carries {thisClock}<br>#82 Pdelay loss: Announces from the incapable port elect nothing |
| an incapable port's Announces still compete |  | caught | #82 Pdelay loss: Announces from the incapable port elect nothing |
| the asCapable drop keeps the flags word |  | caught | #82 Pdelay loss: the drop commit's flags are gmPresent alone<br>p1 255 #82 Pdelay loss: the drop commit's flags are gmPresent alone |
| an incapable port's receipt watch is not re-armed |  | caught | #82 Pdelay loss: once capable, with no Announce, master in 3 s<br>#82 Pdelay loss: that mastership names thisClock, {thisClock}<br>p1 255 #82 Pdelay loss: once capable, with no Announce, master in 3 s |
| the published flags leave gmPresent to the microcode |  | caught | #82 cold release: every cycle to the first beat has gmPresent<br>#82 cold release: that commit's flags are gmPresent alone<br>#82 warm reset: its flags are gmPresent alone<br>#82 peer leaves: the mastership commit has gmPresent<br>#82 Pdelay loss: the drop commit's flags are gmPresent alone<br>#82 Pdelay loss: that mastership commit has gmPresent |
| the image does not mark thisClock grandmaster-capable |  | caught | #82 cold release: every cycle to the first beat has gmPresent<br>#82 cold release: that commit's flags are gmPresent alone<br>#82 warm reset: its flags are gmPresent alone<br>#82 peer leaves: the mastership commit has gmPresent<br>#82 Pdelay loss: the drop commit's flags are gmPresent alone<br>#82 Pdelay loss: that mastership commit has gmPresent |
| the capability mark ignores priority1 |  | caught | p1 255 #82 cold release: every cycle to the first beat has gmPresent<br>p1 255 #82 cold release: that commit's flags are gmPresent alone<br>p1 255 #82 Pdelay loss: the drop commit's flags are gmPresent alone<br>p1 255 #82 Pdelay loss: that mastership commit has gmPresent |
| mastership sets the microcode's presence bit |  | caught | p1 255 #82 Pdelay loss: that mastership commit has gmPresent |
| becoming grandmaster clears sync-ok |  | caught | #84 first mastership: the master flags carry sync-ok<br>#84 takeover: its commit names thisClock with sync-ok<br>#84 every master cycle publishes sync-ok<br>p1 255 #84 first mastership: the master flags carry sync-ok<br>p1 255 #84 every master cycle publishes sync-ok |
| a queued receipt timeout clears a master's sync-ok | re-planted | caught | #84 takeover: a queued receipt timeout keeps sync-ok<br>#84 every master cycle publishes sync-ok |
| an expiry takes a master's own vector for a peer's | re-planted | caught | #84 takeover: the queued receipt timeout commits after it |
| a sync receipt timeout only clears sync-ok | re-planted | caught | #89 Sync stops: the plane takes mastership<br>#89 never usable: the grandmaster is aged<br>#89 no Follow_Up: the plane takes mastership within syncReceiptTimeout and one BMCA pass<br>#89 Follow_Up after the next Sync: the plane takes mastership within syncReceiptTimeout and one BMCA pass<br>#89 Follow_Up with the next sequenceId: the plane takes mastership within syncReceiptTimeout and one BMCA pass |
| only an expiry that ages a slave marks the port | re-planted | caught | #89 takeover: the queued receipt timeout leaves the port aged<br>#89 a lone pair heard as master: a later Announce elects nothing<br>#89 Announce lapse: a sync receipt timeout after mastership ages the next Announce |
| sync receipt ageing ignores gmPresent | re-planted | caught | p1 255 #89 gmPresent: a priority1 255 grandmaster without Sync stays elected |
| a sync receipt timeout that ages nothing keeps sync-ok | new | caught | p1 255 #89 gmPresent: when its Sync stops, sync-ok clears within syncReceiptTimeout and the peer stays elected |
| a consumed pair leaves sync-ok down | new | caught | p1 255 #89 gmPresent: a priority1 255 grandmaster's usable Sync raises sync-ok |
| adoption leaves the Sync receipt watch off |  | caught | #89 never usable: the grandmaster is aged<br>#89 never usable: within syncReceiptTimeout of its adoption |
| an aged port takes Announces | re-planted | caught | #89 never usable: the aged port stays master while Announces continue<br>#89 Sync stops: the aged port stays master while Announces continue<br>#89 no Follow_Up: the aged port stays master while Announces continue<br>#89 Follow_Up after the next Sync: the aged port stays master while Announces continue<br>#89 Follow_Up with the next sequenceId: the aged port stays master while Announces continue<br>p1 255 #89 gmPresent: a priority1 1 Announce on the aged port elects nothing |
| an aged port refuses a priority1 255 grandmaster | re-planted | caught | p1 255 #89 gmPresent: the aged port elects a priority1 255 grandmaster |
| an aged Announce is dropped rather than aged |  | caught | p1 255 #89 gmPresent: a priority1 1 Announce on the aged port makes this plane master |
| mastership stops the Sync receipt watch |  | caught | #89 Announce lapse: a sync receipt timeout after mastership ages the next Announce |
| mastership stops the Follow_Up watch |  | caught | #89 parked Sync: a Follow_Up 200 ms after it pairs with nothing |
| mastership voids the parked Sync |  | caught | #89 parked Sync: a Follow_Up 60 ms after it, after the takeover, is heard |
| a master steers on its aged peer's Sync |  | caught | #89 first grandmaster: Sync recovery is heard as master and steers nothing<br>#89 Sync stops: Sync recovery is heard as master and steers nothing<br>#89 no Follow_Up: Sync recovery is heard as master and steers nothing |
| a master hears no Sync |  | caught | #89 first grandmaster: the next Announce elects the grandmaster<br>#89 Sync stops: the next Announce elects the grandmaster<br>#89 no Follow_Up: the next Announce elects the grandmaster<br>#89 a lone pair heard as master: an Announce inside its watch elects the grandmaster |
| the Sync receipt watch is 100 ms |  | caught | #89 Sync stops: within syncReceiptTimeout and one BMCA pass<br>#89 first grandmaster: usable Sync keeps it elected<br>#89 Sync every 250 ms keeps the plane deferring |
| the Sync receipt watch is 500 ms |  | caught | #89 Sync stops: within syncReceiptTimeout and one BMCA pass<br>#89 no Follow_Up: the plane takes mastership within syncReceiptTimeout and one BMCA pass<br>#89 Follow_Up with the next sequenceId: the plane takes mastership within syncReceiptTimeout and one BMCA pass |
| a parent refresh expires the Sync watch |  | caught | #89 Sync stops: the Announce leaves the grandmaster elected |
| the adoption watch is 100 ms |  | caught | #89 never usable: within syncReceiptTimeout of its adoption<br>still slave inside the Sync receipt watch |
| a Follow_Up pairs whatever its sequenceId |  | caught | #89 Follow_Up after the next Sync: no unusable pair is consumed<br>#89 Follow_Up with the next sequenceId: no unusable pair is consumed |
| the Follow_Up watch is 50 ms |  | caught | #89 a Follow_Up 60 ms after its Sync is used |
| lost responses clear asCapable at the first |  | caught | #90 no response: one loss keeps asCapable<br>#90 no follow-up: one loss keeps asCapable<br>#91 duplicated response: one loss keeps asCapable<br>#91 three responses: one loss keeps asCapable |
| the fifth loss stops the requests |  | caught | #90 no response: request 6 goes out<br>#90 no follow-up: runs from a capable plane<br>#90 no follow-up: runs from a completed exchange |
| same-identity duplicates are a storm |  | caught | #91 duplicates are not a storm: requests keep going out |
| lost responses clear asCapable at the fourth |  | caught | #90 no response: four losses keep asCapable<br>#90 no follow-up: four losses keep asCapable<br>#91 duplicated response: four losses keep asCapable<br>#91 three responses: four losses keep asCapable |
| lost responses clear asCapable at the sixth |  | caught | #90 no response: the fifth loss clears asCapable<br>#90 no follow-up: the fifth loss clears asCapable<br>#91 duplicated response: the fifth loss clears asCapable<br>#91 three responses: the fifth loss clears asCapable |
| a second response re-arms the pairing |  | caught | #91 duplicated response: the fifth loss clears asCapable<br>#91 duplicated response: no exchange completes<br>#91 three responses: the fifth loss clears asCapable<br>#91 three responses: no exchange completes |
| a third response re-arms the reset exchange |  | caught | #91 three responses: the fifth loss clears asCapable<br>#91 three responses: no exchange completes |
| dispatch ignores a busy serializer |  | caught | #84 takeover: nothing commits while dispatch is held |
| mastership never publishes the master bit |  | caught | #84 master cycles were graded<br>p1 255 #84 master cycles were graded |
| a handover to a peer keeps sync-ok |  | caught | #84 every handover to a peer grandmaster clears sync-ok<br>p1 255 #84 every handover to a peer grandmaster clears sync-ok |
| the received path is published without thisClock |  | caught | #85 direct grandmaster: count<br>#85 direct grandmaster: tail 1<br>#85 direct grandmaster: its commit names the grandmaster and path<br>#85 multi-hop grandmaster: count<br>#85 multi-hop grandmaster: tail 5<br>#85 multi-hop grandmaster: its commit names the grandmaster and path<br>#85 seven received entries: count<br>#85 seven received entries: tail 7<br>#85 seven received entries: its commit names the grandmaster and path<br>#85 every peer path ends with thisClock<br>p1 255 #85 every peer path ends with thisClock<br>#82 peer wins: its commit carries the peer path<br>#82 warm reset: the live peer carries its own path<br>#82 Pdelay loss: once capable, a live peer worse than D wins<br>adopt appends thisClock as path tail 4<br>worse announce retains path A tail 4<br>worse TLV-less announce retains path A tail 4<br>parent refresh appends thisClock<br>unknown before path current parent: tail 3<br>post-release C appends thisClock |
| thisClock is appended to an absent path |  | caught | #85 absent path: count      <br>#85 absent path: its commit names the grandmaster and path |
| eight received entries take a ninth |  | caught | #85 eight received entries: count<br>#85 eight received entries: its commit names the grandmaster and path |
| seven received entries leave thisClock out |  | caught | #85 seven received entries: count<br>#85 seven received entries: tail 7 |
| thisClock lands one slot early |  | caught | #85 direct grandmaster: tail 1<br>#85 multi-hop grandmaster: tail 5<br>#85 every peer path ends with thisClock |
| thisClock fills every later slot |  | caught | #85 direct grandmaster: tail 2<br>#85 direct grandmaster: tail 3<br>#85 direct grandmaster: tail 4<br>#85 direct grandmaster: tail 5<br>#85 direct grandmaster: tail 6<br>#85 direct grandmaster: tail 7<br>#85 multi-hop grandmaster: tail 6<br>#85 multi-hop grandmaster: tail 7 |
| the appended entry is the announcing source |  | caught | #85 direct grandmaster: tail 1<br>#85 multi-hop grandmaster: tail 5<br>#85 every peer path ends with thisClock |
| the received entries are not copied |  | caught | #85 multi-hop grandmaster: tail 1<br>#85 multi-hop grandmaster: tail 2<br>#85 multi-hop grandmaster: tail 3<br>#85 multi-hop grandmaster: tail 4<br>#85 seven received entries: tail 1<br>#85 seven received entries: tail 2<br>#85 seven received entries: tail 3<br>#85 seven received entries: tail 4<br>#85 seven received entries: tail 5<br>#85 seven received entries: tail 6<br>#85 eight received entries: tail 1<br>#85 eight received entries: tail 2<br>#85 eight received entries: tail 3<br>#85 eight received entries: tail 4<br>#85 eight received entries: tail 5<br>#85 eight received entries: tail 6<br>#85 eight received entries: tail 7 |
| every received path is published empty |  | caught | #85 peer commits with a path were graded<br>p1 255 #85 peer commits with a path were graded |

Controls caught: 100. Arm tally: 101 checks: 101 PASS, 0 FAIL
