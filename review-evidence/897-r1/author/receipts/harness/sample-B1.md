# B1 at 1x1/1if: the sampled groups (aecp) on round 29's recorded leg and on this lane's fresh build at 6de1475f (the final head's image; section 4 of HANDOFF.md), each cost the most measured over the sample, by the round's own cost tools

| cost | recorded leg, CPU cycles | this head, CPU cycles | difference |
|---|---:|---:|---:|
| base | 11,830 | 12,381 | +551 (+4.66 %) |
| build | 61,240 | 61,837 | +597 (+0.97 %) |
| build_one | 33,665 | 33,636 | -29 (-0.09 %) |
| centisecond | 2,058 | 2,211 | +153 (+7.43 %) |
| event.ADP | 6,355 | 6,877 | +522 (+8.21 %) |
| event.LINK | 11,154 | 11,761 | +607 (+5.44 %) |
| event.MAAP | 8,487 | 8,802 | +315 (+3.71 %) |
| event.TICK | 2,312 | 2,393 | +81 (+3.50 %) |
| events_none | 1,297 | 1,012 | -285 (-21.97 %) |
| item.acmp | 0 | 0 |  |
| item.aecp | 5,126 | 4,760 | -366 (-7.14 %) |
| item.mrpdu | 0 | 0 |  |
| item.rebuild | 0 | 0 |  |
| item.reclaim | 1,088 | 1,088 | +0 (+0.00 %) |
| item.record | 0 | 0 |  |
| item.retained | 0 | 0 |  |
| item.walk | 1,379 | 1,379 | +0 (+0.00 %) |
| item.withdraw | 0 | 0 |  |
| record.aecp | 15,737 | 15,943 | +206 (+1.31 %) |
| step | 0 | 0 |  |

## The run
HEAD 6de1475f63b5c7771ec91613bb5ffec215e93f1c DIRTY 1 B1 1x1 aecp --variant answering-ports
1 groups graded, 0 refusals, 0 budget misses (0 of 25 probe instances, 0 of 25 paths), 0 of 110 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)
rc=0

## Probe by probe
group aecp: 25 probes on the head's build, 25 on the recorded leg's
  aecp.entity_available.if0                                                   15758      11026    -4732 (-30.03 %)
  aecp.get_avb_info.if0                                                       18200      20834    +2634 (+14.47 %)
  aecp.get_configuration.if0                                                  12811       8419    -4392 (-34.28 %)
  aecp.get_counters.if0                                                       19119      15805    -3314 (-17.33 %)
  aecp.get_name.if0                                                           16220      11006    -5214 (-32.15 %)
  aecp.lock_entity.if0                                                        25129      19374    -5755 (-22.90 %)
  aecp.mvu_get_milan_info.if0                                                 12005       8386    -3619 (-30.15 %)
  aecp.read_descriptor.t0.i0.c0.if0                                           23765      25685    +1920 (+8.08 %)
  aecp.read_descriptor.t1.i0.c0.if0                                           17700      14108    -3592 (-20.29 %)
  aecp.read_descriptor.t10.i2.c0.if0                                          17559      14327    -3232 (-18.41 %)
  aecp.read_descriptor.t12.i0.c0.if0                                          14992      10211    -4781 (-31.89 %)
  aecp.read_descriptor.t13.i0.c0.if0                                          20683      16016    -4667 (-22.56 %)
  aecp.read_descriptor.t14.i0.c0.if0                                          16937      20379    +3442 (+20.32 %)
  aecp.read_descriptor.t15.i0.c0.if0                                          17111      12900    -4211 (-24.61 %)
  aecp.read_descriptor.t2.i0.c0.if0                                           17716      19987    +2271 (+12.82 %)
  aecp.read_descriptor.t20.i24.c0.if0                                         18936      19851     +915 (+4.83 %)
  aecp.read_descriptor.t26.i0.c0.if0                                          13378      13933     +555 (+4.15 %)
  aecp.read_descriptor.t36.i0.c0.if0                                          18036      14208    -3828 (-21.22 %)
  aecp.read_descriptor.t5.i1.c0.if0                                           18946      14387    -4559 (-24.06 %)
  aecp.read_descriptor.t6.i1.c0.if0                                           15175      11276    -3899 (-25.69 %)
  aecp.read_descriptor.t9.i0.c0.if0                                           14162      10614    -3548 (-25.05 %)
  aecp.register_unsolicited.if0                                               21014      19540    -1474 (-7.01 %)
  aecp.set_name.if0                                                           33188      26329    -6859 (-20.67 %)
  aecp.unknown_command.if0                                                    16436      12082    -4354 (-26.49 %)
  aecp.unlock_entity.if0                                                      25436      18852    -6584 (-25.88 %)
largest difference: -6859 CPU cycles at aecp.set_name.if0
recorded: 7252 passes, heaviest work pass 61240 cycles (0.6124 ms)
head: 7535 passes, heaviest work pass 61837 cycles (0.61837 ms)
recorded summary 81531552 CPU cycles; head 81415404
