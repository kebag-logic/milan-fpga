The two reviews' own probes, run at da8a8b84 on a clean clone, from copies of the reviewers' scripts under this
round's scratch (no review packet was written to).

- `r852-retry-probe-da8a8b84.log`, `r852-retry-control-da8a8b84.log`: R852-1's retry probe (`retry_probe.py` with
  its `retry_probe.cpp` in place of the PHY suite) and its control. Fault case: `register4=0001
  advertised-at-last-restart=0001 active-Mbps=0 restarts=2 owed=0`, 34 of 34 pass; control `restarts=1`, 34 of 34.
- `r851-retry-probe-da8a8b84.log`: R851-1's `retry_probe.sh` (the head's suite plus its added test, on a copy of
  `phy_peer.hpp` that records register 4 at each restart): 18 of 18 pass, `register4=0001
  advertised-at-last-restart=0001 restarts=2 adv-owed=0 published=13`. At afa3ea19 it failed (R851-F1).
- `r851-mutants-da8a8b84.txt`: R851-1's `mutants.sh`. m1, m2, m3, m3b, m4, m5, m7 and m8 are caught; m6 survives,
  the review's equivalent mutant (an unacknowledged read, -1, reads as all ones).
- `r851-m3-m3b-words-da8a8b84.txt`: m3's and m3b's failing test and words, P14 "... restarted once, register 4
  alone" and "... register 9 alone" (R851-F2); P15 fails under both too.
The generated headers these probes need were the head-equal tree's platboot arm's (the configs are unchanged).
