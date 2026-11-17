Both reviews' own probes, at 1a1e6665 on a clean clone, from copies of the reviewers' scripts under this round's
scratch (no review packet was written to). The generated headers they need were this round's platboot arm's.

- `r852-retry-probe-1a1e6665.log`, `r852-retry-control-1a1e6665.log`: R852-1's retry probe and its control, rc 0,
  37 of 37 each; fault `register4=0001 advertised-at-last-restart=0001 active-Mbps=0 restarts=2 owed=0`, control
  `restarts=1`.
- `r851-retry-probe-1a1e6665.log`: R851-1's retry_probe.sh, rc 0, 21 of 21, `register4=0001
  advertised-at-last-restart=0001 restarts=2 adv-owed=0 published=13`.
- `r851-mutants-1a1e6665.txt`: R851-1's mutants.sh as written (m3, m3b and m8 refused: their anchors name this
  round's renamed flag and old owed test), then an executor's copy with only those three anchors renamed (the diff
  is in the file): m1 to m8 and m3b caught, m6 surviving as the review's equivalent mutant.
