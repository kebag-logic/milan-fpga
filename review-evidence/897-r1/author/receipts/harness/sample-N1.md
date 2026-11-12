# N1 at 1x1/1if: the sampled groups (notice-burst-0) on round 29's recorded leg and on this lane's fresh build at 6de1475f (the final head's image; section 4 of HANDOFF.md), each cost the most measured over the sample, by the round's own cost tools

| cost | recorded leg, CPU cycles | this head, CPU cycles | difference |
|---|---:|---:|---:|
| base | 13,700 | 13,534 | -166 (-1.21 %) |
| build | 61,766 | 61,269 | -497 (-0.80 %) |
| build_one | 34,197 | 33,600 | -597 (-1.75 %) |
| centisecond | 11,293 | 11,536 | +243 (+2.15 %) |
| event.ACMP | 11,888 | 12,169 | +281 (+2.36 %) |
| event.ADP | 5,981 | 6,509 | +528 (+8.83 %) |
| event.AECP | 4,606 | 5,186 | +580 (+12.59 %) |
| event.GM | 2,252 | 2,699 | +447 (+19.85 %) |
| event.LINK | 11,471 | 12,082 | +611 (+5.33 %) |
| event.MAAP | 12,765 | 13,326 | +561 (+4.39 %) |
| event.TICK | 2,206 | 2,339 | +133 (+6.03 %) |
| events_none | 1,870 | 1,865 | -5 (-0.27 %) |
| item.acmp | 0 | 0 |  |
| item.aecp | 19,060 | 18,824 | -236 (-1.24 %) |
| item.mrpdu | 0 | 0 |  |
| item.rebuild | 0 | 0 |  |
| item.reclaim | 1,151 | 1,140 | -11 (-0.96 %) |
| item.record | 24,007 | 24,034 | +27 (+0.11 %) |
| item.retained | 0 | 0 |  |
| item.walk | 1,379 | 1,379 | +0 (+0.00 %) |
| item.withdraw | 0 | 0 |  |
| record.acmp | 19,521 | 19,893 | +372 (+1.91 %) |
| record.adp | 754 | 819 | +65 (+8.62 %) |
| record.aecp | 17,951 | 18,617 | +666 (+3.71 %) |
| record.maap | 6,385 | 6,273 | -112 (-1.75 %) |
| record.srp | 24,474 | 24,423 | -51 (-0.21 %) |
| step | 80,419 | 80,103 | -316 (-0.39 %) |

## The run
HEAD 6de1475f63b5c7771ec91613bb5ffec215e93f1c DIRTY 0 N1 1x1 notice-burst-0 --variant answering-every-port
NOTICE notice-burst-0: committed 9.374 ms after its port's answer to the last of 16 recipients (bound 22 ms) within
NOTICE notice-burst-0: committed 9.579 ms after its port's answer to the last of 16 recipients (bound 22 ms) within
NOTICE notice-burst-0: committed 9.786 ms after its port's answer to the last of 16 recipients (bound 22 ms) within
NOTICE notice-burst-0: committed 9.987 ms after its port's answer to the last of 16 recipients (bound 22 ms) within
NOTICE notice-burst-0: committed 10.177 ms after its port's answer to the last of 16 recipients (bound 22 ms) within
NOTICE notice-burst-0: committed 10.376 ms after its port's answer to the last of 16 recipients (bound 22 ms) within
NOTICE notice-burst-0: committed 3.271 ms after its port's answer to the last of 16 recipients (bound 22 ms) within
NOTICE notice-burst-0: committed 3.479 ms after its port's answer to the last of 16 recipients (bound 22 ms) within
NOTICE notice-burst-0: committed 10.557 ms after its port's answer to the last of 16 recipients (bound 22 ms) within
NOTICE notice-burst-0: committed 11.741 ms after its port's answer to the last of 16 recipients (bound 22 ms) within
NOTICE notice-burst-0: committed 11.945 ms after its port's answer to the last of 16 recipients (bound 22 ms) within
NOTICE notice-burst-0: committed 4.393 ms after its port's answer to the last of 16 recipients (bound 22 ms) within
1 groups graded, 0 refusals, 0 budget misses (0 of 17 probe instances, 0 of 6 paths), 0 of 932 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)
rc=0

## Probe by probe
group notice-burst-0: 17 probes on the head's build, 17 on the recorded leg's
  notice-burst-0.held.acmp.if0                                               936472     987482   +51010 (+5.45 %)
  notice-burst-0.held.adp.if0                                                157735     161420    +3685 (+2.34 %)
  notice-burst-0.held.aecp.if0                                               960672     998123   +37451 (+3.90 %)
  notice-burst-0.held.maap.if0                                               753176     948007  +194831 (+25.87 %)
  notice-burst-0.held.srp.if0                                                583162     584044     +882 (+0.15 %)
  notice-burst-0.notices.27.9.0.if0                                         1009806    1055704   +45898 (+4.55 %)
  notice-burst-0.notices.28.9.0.if0                                         1026426    1174134  +147708 (+14.39 %)
  notice-burst-0.notices.29.36.0.if0                                         407274     439256   +31982 (+7.85 %)
  notice-burst-0.notices.29.5.0.if0                                          950536     957876    +7340 (+0.77 %)
  notice-burst-0.notices.29.5.1.if0                                          991262     998746    +7484 (+0.75 %)
  notice-burst-0.notices.29.6.0.if0                                          257267    1037566  +780299 (+303.30 %)
  notice-burst-0.notices.29.6.1.if0                                          350818     347865    -2953 (-0.84 %)
  notice-burst-0.notices.29.9.0.if0                                         1046112    1194454  +148342 (+14.18 %)
  notice-burst-0.notices.f.5.0.if0                                           929813     937384    +7571 (+0.81 %)
  notice-burst-0.notices.f.5.1.if0                                           970935     978560    +7625 (+0.79 %)
  notice-burst-0.notices.f.6.0.if0                                           236650    1017712  +781062 (+330.05 %)
  notice-burst-0.notices.f.6.1.if0                                           330164     327092    -3072 (-0.93 %)
largest difference: +781062 CPU cycles at notice-burst-0.notices.f.6.0.if0
recorded: 24760 passes, heaviest work pass 152953 cycles (1.52953 ms)
head: 24509 passes, heaviest work pass 157512 cycles (1.57512 ms)
recorded summary 323052716 CPU cycles; head 323057226
