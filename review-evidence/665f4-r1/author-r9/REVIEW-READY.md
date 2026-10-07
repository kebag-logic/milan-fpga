[A560] REVIEW READY — F4 Round 7

Commit: f74b9403b330ce316eeec6f724846f16def98443
Parent: cce554f64f6bdab1f6d26e5c4d7b46d54d228c52 (PR #690 Round 6).

Changed: bound continuing SRP receive-allocation refusal to 1000 ms from original arrival at the next eligible attempt; count expired records once in rx_discarded, separately from received/malformed. Successful recovery and pending-event/TX ordering remain intact. Six regressions and twelve new defect plants cover over-capacity input, later-interface withdrawal and binding progress, original-arrival timing, clock wrap, failed recreation and Domain floods. R532-6-F2 size attribution and S1 README wording are included.

Validation: all 99 final assigned invocations exit 0. Three foreground firmware shards jointly catch 196 control/MAAP plants; all 102 SRP plants pass, with the twelve new plants also checked at IF=1. All 19 measured files retain 100% line/branch coverage after unchanged exclusions. Unchanged R532 HOL N=30/150, flood/retry and R533-5 recovery probes pass at IF=1/2; all original receive-recovery cases remain unchanged and pass. Mailbox integration, SRP walk/differential, MAAP differential, NVM, dependency profiles and the documentation bank pass.

Linked size: twelve links use identical verified runtime inputs at lane base, Round 5 and candidate. RAM spans are 62688/75264 bytes (1x1, IF=1/2) and 77376/104720 (8x8). Deltas against Round 5 are +8096/+9424; attribution separates MAAP composition/state and the 1528-byte shared retained record. Round 7 itself adds 112–128 span bytes and no BSS.

Evidence packet: 665f4-a560/HANDOFF.md and PR-BODY.md, with ROUND7-GATES.md/json, ROUND7-TESTS.md, ROUND7-SIZE.md, source/integrity records and normalized receipts. The manager's mailbox recipe and publication corrections are preserved.

The commit remains local; no push or PR edit. Parent, submodules and dependency clone are clean. Independent re-review/finding closure remains owed. The compiler-absent check and builder bank remain manager-owned under comment 6036016117, as do publication, hosted gates, trusted local replication and merge validation. No new integration, target-timing or merge approval is claimed.
