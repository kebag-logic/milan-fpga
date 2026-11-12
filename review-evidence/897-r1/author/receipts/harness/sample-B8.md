# B8 at 8x8/2if: the sampled groups (aecp) on round 29's recorded leg and on this lane's fresh build at 6de1475f (the final head's image; section 4 of HANDOFF.md), each cost the most measured over the sample, by the round's own cost tools

| cost | recorded leg, CPU cycles | this head, CPU cycles | difference |
|---|---:|---:|---:|
| base | 21,322 | 21,491 | +169 (+0.79 %) |
| build | 118,326 | 117,620 | -706 (-0.60 %) |
| build_one | 93,256 | 93,352 | +96 (+0.10 %) |
| centisecond | 6,737 | 6,839 | +102 (+1.51 %) |
| event.ADP | 6,840 | 7,220 | +380 (+5.56 %) |
| event.LINK | 13,084 | 13,395 | +311 (+2.38 %) |
| event.MAAP | 10,098 | 10,816 | +718 (+7.11 %) |
| event.TICK | 2,323 | 2,583 | +260 (+11.19 %) |
| events_none | 1,390 | 1,544 | +154 (+11.08 %) |
| item.acmp | 0 | 0 |  |
| item.aecp | 5,019 | 5,104 | +85 (+1.69 %) |
| item.mrpdu | 0 | 0 |  |
| item.rebuild | 0 | 0 |  |
| item.reclaim | 1,699 | 1,779 | +80 (+4.71 %) |
| item.record | 0 | 0 |  |
| item.retained | 0 | 0 |  |
| item.walk | 2,388 | 2,345 | -43 (-1.80 %) |
| item.withdraw | 0 | 0 |  |
| record.aecp | 20,893 | 19,429 | -1,464 (-7.01 %) |
| step | 0 | 0 |  |

## The run
HEAD 6de1475f63b5c7771ec91613bb5ffec215e93f1c DIRTY 1 B8 8x8 aecp --variant answering-ports
1 groups graded, 0 refusals, 0 budget misses (0 of 39 probe instances, 0 of 39 paths), 0 of 136 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)
rc=0

## Probe by probe
group aecp: 39 probes on the head's build, 39 on the recorded leg's
  aecp.entity_available.if0                                                   21868      24251    +2383 (+10.90 %)
  aecp.entity_available.if1                                                   15237      17425    +2188 (+14.36 %)
  aecp.get_avb_info.if0                                                       23302      25970    +2668 (+11.45 %)
  aecp.get_avb_info.if1                                                       16604      19481    +2877 (+17.33 %)
  aecp.get_configuration.if0                                                  11837      13572    +1735 (+14.66 %)
  aecp.get_configuration.if1                                                  24154       7985   -16169 (-66.94 %)
  aecp.get_counters.if0                                                       17063      19184    +2121 (+12.43 %)
  aecp.get_counters.if1                                                       19292      20737    +1445 (+7.49 %)
  aecp.get_name.if0                                                           14295      15977    +1682 (+11.77 %)
  aecp.get_name.if1                                                           25633      10410   -15223 (-59.39 %)
  aecp.lock_entity.if0                                                        32234      28033    -4201 (-13.03 %)
  aecp.lock_entity.if1                                                        35042      30656    -4386 (-12.52 %)
  aecp.mvu_get_milan_info.if0                                                 20847      22843    +1996 (+9.57 %)
  aecp.mvu_get_milan_info.if1                                                 13732      16239    +2507 (+18.26 %)
  aecp.read_descriptor.t0.i0.c0.if0                                           27605      30416    +2811 (+10.18 %)
  aecp.read_descriptor.t0.i0.c0.if1                                           29453      13815   -15638 (-53.09 %)
  aecp.read_descriptor.t1.i0.c0.if0                                           22898      26495    +3597 (+15.71 %)
  aecp.read_descriptor.t1.i0.c0.if1                                           17569      18795    +1226 (+6.98 %)
  aecp.read_descriptor.t10.i9.c0.if0                                          14127      23785    +9658 (+68.37 %)
  aecp.read_descriptor.t12.i0.c0.if0                                          14203      15792    +1589 (+11.19 %)
  aecp.read_descriptor.t13.i0.c0.if0                                          28245      30502    +2257 (+7.99 %)
  aecp.read_descriptor.t14.i7.c0.if0                                          13850      15663    +1813 (+13.09 %)
  aecp.read_descriptor.t15.i7.c0.if0                                          22441      25731    +3290 (+14.66 %)
  aecp.read_descriptor.t2.i0.c0.if0                                           14667      16085    +1418 (+9.67 %)
  aecp.read_descriptor.t2.i0.c0.if1                                           17438      19883    +2445 (+14.02 %)
  aecp.read_descriptor.t20.i71.c0.if0                                         13992      15931    +1939 (+13.86 %)
  aecp.read_descriptor.t26.i0.c0.if0                                          14733      17780    +3047 (+20.68 %)
  aecp.read_descriptor.t36.i0.c0.if0                                          23971      26461    +2490 (+10.39 %)
  aecp.read_descriptor.t5.i8.c0.if0                                           22944      26108    +3164 (+13.79 %)
  aecp.read_descriptor.t6.i8.c0.if0                                           15209      16915    +1706 (+11.22 %)
  aecp.read_descriptor.t9.i0.c0.if0                                           22737      25907    +3170 (+13.94 %)
  aecp.register_unsolicited.if0                                               11909      14281    +2372 (+19.92 %)
  aecp.register_unsolicited.if1                                               13619      15917    +2298 (+16.87 %)
  aecp.set_name.if0                                                           35885      36697     +812 (+2.26 %)
  aecp.set_name.if1                                                           42961      27066   -15895 (-37.00 %)
  aecp.unknown_command.if0                                                    24671      26933    +2262 (+9.17 %)
  aecp.unknown_command.if1                                                    24331       8075   -16256 (-66.81 %)
  aecp.unlock_entity.if0                                                      39843      38425    -1418 (-3.56 %)
  aecp.unlock_entity.if1                                                      29520      31895    +2375 (+8.05 %)
largest difference: -16256 CPU cycles at aecp.unknown_command.if1
recorded: 4848 passes, heaviest work pass 118326 cycles (1.18326 ms)
head: 4825 passes, heaviest work pass 117620 cycles (1.1762 ms)
recorded summary 94813038 CPU cycles; head 94787126
