# A1 at 1x1/1if: the sampled groups (aecp,aecp-fanout,acmp-cmd) on round 29's recorded leg and on this lane's fresh build at 6de1475f (the final head's image; section 4 of HANDOFF.md), each cost the most measured over the sample, by the round's own cost tools

| cost | recorded leg, CPU cycles | this head, CPU cycles | difference |
|---|---:|---:|---:|
| base | 14,287 | 14,951 | +664 (+4.65 %) |
| build | 61,769 | 62,775 | +1,006 (+1.63 %) |
| build_one | 33,846 | 34,283 | +437 (+1.29 %) |
| centisecond | 2,173 | 2,345 | +172 (+7.92 %) |
| event.ADP | 6,910 | 6,396 | -514 (-7.44 %) |
| event.AECP | 2,380 | 3,141 | +761 (+31.97 %) |
| event.LINK | 11,142 | 11,105 | -37 (-0.33 %) |
| event.MAAP | 8,167 | 8,691 | +524 (+6.42 %) |
| event.TICK | 2,384 | 2,309 | -75 (-3.15 %) |
| events_none | 1,486 | 1,383 | -103 (-6.93 %) |
| item.acmp | 0 | 0 |  |
| item.aecp | 18,640 | 18,637 | -3 (-0.02 %) |
| item.mrpdu | 0 | 0 |  |
| item.rebuild | 0 | 0 |  |
| item.reclaim | 1,101 | 1,110 | +9 (+0.82 %) |
| item.record | 0 | 0 |  |
| item.retained | 0 | 0 |  |
| item.walk | 1,732 | 1,732 | +0 (+0.00 %) |
| item.withdraw | 0 | 0 |  |
| record.acmp | 19,123 | 18,839 | -284 (-1.49 %) |
| record.aecp | 17,603 | 17,129 | -474 (-2.69 %) |
| step | 0 | 0 |  |

## The run
HEAD 6de1475f63b5c7771ec91613bb5ffec215e93f1c DIRTY 0 A1 1x1 aecp,aecp-fanout,acmp-cmd 
3 groups graded, 0 refusals, 0 budget misses (0 of 42 probe instances, 0 of 41 paths), 0 of 302 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)
rc=0

## Probe by probe
group aecp: 25 probes on the head's build, 25 on the recorded leg's
  aecp.entity_available.if0                                                   13255      14072     +817 (+6.16 %)
  aecp.get_avb_info.if0                                                       12488      11996     -492 (-3.94 %)
  aecp.get_configuration.if0                                                   8485      18139    +9654 (+113.78 %)
  aecp.get_counters.if0                                                       16752      17874    +1122 (+6.70 %)
  aecp.get_name.if0                                                           10816      21175   +10359 (+95.77 %)
  aecp.lock_entity.if0                                                        19660      23835    +4175 (+21.24 %)
  aecp.mvu_get_milan_info.if0                                                  7655      14068    +6413 (+83.78 %)
  aecp.read_descriptor.t0.i0.c0.if0                                           15357      15074     -283 (-1.84 %)
  aecp.read_descriptor.t1.i0.c0.if0                                           16071      17035     +964 (+6.00 %)
  aecp.read_descriptor.t10.i2.c0.if0                                          15566      16282     +716 (+4.60 %)
  aecp.read_descriptor.t12.i0.c0.if0                                          10333      20303    +9970 (+96.49 %)
  aecp.read_descriptor.t13.i0.c0.if0                                          17869      18785     +916 (+5.13 %)
  aecp.read_descriptor.t14.i0.c0.if0                                          10005      19543    +9538 (+95.33 %)
  aecp.read_descriptor.t15.i0.c0.if0                                          14753      14919     +166 (+1.13 %)
  aecp.read_descriptor.t2.i0.c0.if0                                            9749      20475   +10726 (+110.02 %)
  aecp.read_descriptor.t20.i24.c0.if0                                          9332       9916     +584 (+6.26 %)
  aecp.read_descriptor.t26.i0.c0.if0                                          15137      22039    +6902 (+45.60 %)
  aecp.read_descriptor.t36.i0.c0.if0                                          10230      15614    +5384 (+52.63 %)
  aecp.read_descriptor.t5.i1.c0.if0                                           15373      16596    +1223 (+7.96 %)
  aecp.read_descriptor.t6.i1.c0.if0                                           11155      17639    +6484 (+58.13 %)
  aecp.read_descriptor.t9.i0.c0.if0                                           10826      10441     -385 (-3.56 %)
  aecp.register_unsolicited.if0                                               11699      21586    +9887 (+84.51 %)
  aecp.set_name.if0                                                           27437      28765    +1328 (+4.84 %)
  aecp.unknown_command.if0                                                    13823      14334     +511 (+3.70 %)
  aecp.unlock_entity.if0                                                      19427      18751     -676 (-3.48 %)
largest difference: +10726 CPU cycles at aecp.read_descriptor.t2.i0.c0.if0
recorded: 7197 passes, heaviest work pass 61769 cycles (0.61769 ms)
head: 7045 passes, heaviest work pass 62775 cycles (0.62775 ms)
recorded summary 81376503 CPU cycles; head 81525800
group aecp-fanout: 9 probes on the head's build, 9 on the recorded leg's
  aecp_fanout.add_audio_mappings.if0                                          36602      46604   +10002 (+27.33 %)
  aecp_fanout.lock_entity.if0                                                 46554      44969    -1585 (-3.40 %)
  aecp_fanout.remove_audio_mappings.if0                                       43829      41335    -2494 (-5.69 %)
  aecp_fanout.set_clock_source.if0                                            42866      39289    -3577 (-8.34 %)
  aecp_fanout.set_control_identify_off.if0                                    40205      45150    +4945 (+12.30 %)
  aecp_fanout.set_control_identify_on.if0                                     34599      45028   +10429 (+30.14 %)
  aecp_fanout.set_name.if0                                                    41392      51151    +9759 (+23.58 %)
  aecp_fanout.set_sampling_rate.if0                                           35281      43810    +8529 (+24.17 %)
  aecp_fanout.unlock_entity.if0                                               41297      46292    +4995 (+12.10 %)
largest difference: +10429 CPU cycles at aecp_fanout.set_control_identify_on.if0
recorded: 7112 passes, heaviest work pass 61769 cycles (0.61769 ms)
head: 6963 passes, heaviest work pass 62775 cycles (0.62775 ms)
recorded summary 81685125 CPU cycles; head 81853498
group acmp-cmd: 8 probes on the head's build, 8 on the recorded leg's
  acmp.bind_rx.if0                                                            18382      18053     -329 (-1.79 %)
  acmp.disconnect_tx.if0                                                       8964       8918      -46 (-0.51 %)
  acmp.get_rx_state.if0                                                       10290      10183     -107 (-1.04 %)
  acmp.get_tx_connection.if0                                                   9309       8894     -415 (-4.46 %)
  acmp.get_tx_state.if0                                                        9287       9276      -11 (-0.12 %)
  acmp.probe_tx.if0                                                            9881      11065    +1184 (+11.98 %)
  acmp.probe_tx_response.if0                                                   8920      11964    +3044 (+34.13 %)
  acmp.unbind_rx.if0                                                          13087      13003      -84 (-0.64 %)
largest difference: +3044 CPU cycles at acmp.probe_tx_response.if0
recorded: 5998 passes, heaviest work pass 61769 cycles (0.61769 ms)
head: 5860 passes, heaviest work pass 62775 cycles (0.62775 ms)
recorded summary 67981084 CPU cycles; head 67991942
