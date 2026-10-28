# Round-3 check coverage

Generated from the mutation arm's log: each named check, and every control
whose verdict printed that check as failed.

| Check | Controls that fail it |
|---|---|
| p1 255 #89 gmPresent: a priority1 255 grandmaster's usable Sync raises sync-ok | a consumed pair leaves sync-ok down |
| p1 255 #89 gmPresent: when its Sync stops, sync-ok clears within syncReceiptTimeout and the peer stays elected | a sync receipt timeout that ages nothing keeps sync-ok |
| #84 takeover: the queued receipt timeout commits after it | an expiry takes a master's own vector for a peer's |

Controls in the log: 100; caught: 100.
