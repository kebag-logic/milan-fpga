# A8 at 8x8/2if: the sampled groups (aecp,aecp-fanout,acmp-cmd) on round 29's recorded leg and on this lane's fresh build at 6de1475f (the final head's image; section 4 of HANDOFF.md), each cost the most measured over the sample, by the round's own cost tools

| cost | recorded leg, CPU cycles | this head, CPU cycles | difference |
|---|---:|---:|---:|
| base | 23,354 | 23,377 | +23 (+0.10 %) |
| build | 120,238 | 118,364 | -1,874 (-1.56 %) |
| build_one | 94,977 | 93,373 | -1,604 (-1.69 %) |
| centisecond | 6,822 | 6,874 | +52 (+0.76 %) |
| event.ADP | 7,144 | 7,219 | +75 (+1.05 %) |
| event.AECP | 2,737 | 2,881 | +144 (+5.26 %) |
| event.LINK | 13,555 | 13,764 | +209 (+1.54 %) |
| event.MAAP | 10,529 | 10,938 | +409 (+3.88 %) |
| event.TICK | 2,568 | 2,497 | -71 (-2.76 %) |
| events_none | 2,045 | 2,080 | +35 (+1.71 %) |
| item.acmp | 0 | 0 |  |
| item.aecp | 25,016 | 25,024 | +8 (+0.03 %) |
| item.mrpdu | 0 | 0 |  |
| item.rebuild | 0 | 0 |  |
| item.reclaim | 1,654 | 1,824 | +170 (+10.28 %) |
| item.record | 0 | 0 |  |
| item.retained | 0 | 0 |  |
| item.walk | 3,816 | 3,737 | -79 (-2.07 %) |
| item.withdraw | 0 | 0 |  |
| record.acmp | 22,477 | 22,163 | -314 (-1.40 %) |
| record.aecp | 23,027 | 22,973 | -54 (-0.23 %) |
| step | 0 | 0 |  |

## The run
HEAD 6de1475f63b5c7771ec91613bb5ffec215e93f1c DIRTY 0 A8 8x8 aecp,aecp-fanout,acmp-cmd 
3 groups graded, 0 refusals, 0 budget misses (0 of 68 probe instances, 0 of 66 paths), 0 of 382 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)
rc=0

## Probe by probe
group aecp: 39 probes on the head's build, 39 on the recorded leg's
  aecp.entity_available.if0                                                   13923      18772    +4849 (+34.83 %)
  aecp.entity_available.if1                                                   26132      12555   -13577 (-51.96 %)
  aecp.get_avb_info.if0                                                       16913      22123    +5210 (+30.80 %)
  aecp.get_avb_info.if1                                                       28693      15942   -12751 (-44.44 %)
  aecp.get_configuration.if0                                                  22904       9687   -13217 (-57.71 %)
  aecp.get_configuration.if1                                                  16138      21514    +5376 (+33.31 %)
  aecp.get_counters.if0                                                       26923      13742   -13181 (-48.96 %)
  aecp.get_counters.if1                                                       37300      15445   -21855 (-58.59 %)
  aecp.get_name.if0                                                           24587      11378   -13209 (-53.72 %)
  aecp.get_name.if1                                                           18613      23624    +5011 (+26.92 %)
  aecp.lock_entity.if0                                                        36751      23572   -13179 (-35.86 %)
  aecp.lock_entity.if1                                                        33222      26036    -7186 (-21.63 %)
  aecp.mvu_get_milan_info.if0                                                 13793      18634    +4841 (+35.10 %)
  aecp.mvu_get_milan_info.if1                                                 24711      11331   -13380 (-54.15 %)
  aecp.read_descriptor.t0.i0.c0.if0                                           19408      29368    +9960 (+51.32 %)
  aecp.read_descriptor.t0.i0.c0.if1                                           21250      27150    +5900 (+27.76 %)
  aecp.read_descriptor.t1.i0.c0.if0                                           14997      21410    +6413 (+42.76 %)
  aecp.read_descriptor.t1.i0.c0.if1                                           18572      14705    -3867 (-20.82 %)
  aecp.read_descriptor.t10.i9.c0.if0                                          14670      19766    +5096 (+34.74 %)
  aecp.read_descriptor.t12.i0.c0.if0                                          24236      11349   -12887 (-53.17 %)
  aecp.read_descriptor.t13.i0.c0.if0                                          20604      24760    +4156 (+20.17 %)
  aecp.read_descriptor.t14.i7.c0.if0                                          24565      11594   -12971 (-52.80 %)
  aecp.read_descriptor.t15.i7.c0.if0                                          14948      20410    +5462 (+36.54 %)
  aecp.read_descriptor.t2.i0.c0.if0                                           25424      11969   -13455 (-52.92 %)
  aecp.read_descriptor.t2.i0.c0.if1                                           27920      14578   -13342 (-47.79 %)
  aecp.read_descriptor.t20.i71.c0.if0                                         24940      11444   -13496 (-54.11 %)
  aecp.read_descriptor.t26.i0.c0.if0                                          25904      13118   -12786 (-49.36 %)
  aecp.read_descriptor.t36.i0.c0.if0                                          15673      21435    +5762 (+36.76 %)
  aecp.read_descriptor.t5.i8.c0.if0                                           15493      20427    +4934 (+31.85 %)
  aecp.read_descriptor.t6.i8.c0.if0                                           26229      12936   -13293 (-50.68 %)
  aecp.read_descriptor.t9.i0.c0.if0                                           15338      20485    +5147 (+33.56 %)
  aecp.register_unsolicited.if0                                               22348      14085    -8263 (-36.97 %)
  aecp.register_unsolicited.if1                                               24246      13968   -10278 (-42.39 %)
  aecp.set_name.if0                                                           45602      32357   -13245 (-29.04 %)
  aecp.set_name.if1                                                           34983      40140    +5157 (+14.74 %)
  aecp.unknown_command.if0                                                    16808      21776    +4968 (+29.56 %)
  aecp.unknown_command.if1                                                    17074      21530    +4456 (+26.10 %)
  aecp.unlock_entity.if0                                                      28282      35204    +6922 (+24.47 %)
  aecp.unlock_entity.if1                                                      21797      27135    +5338 (+24.49 %)
largest difference: -21855 CPU cycles at aecp.get_counters.if1
recorded: 4749 passes, heaviest work pass 120238 cycles (1.20238 ms)
head: 4670 passes, heaviest work pass 118364 cycles (1.18364 ms)
recorded summary 94799971 CPU cycles; head 94804037
group aecp-fanout: 13 probes on the head's build, 13 on the recorded leg's
  aecp_fanout.lock_entity.if0                                                 51021      55640    +4619 (+9.05 %)
  aecp_fanout.lock_entity.if1                                                 51117      56646    +5529 (+10.82 %)
  aecp_fanout.set_clock_source.if0                                            67274      53277   -13997 (-20.81 %)
  aecp_fanout.set_clock_source.if1                                            54033      58730    +4697 (+8.69 %)
  aecp_fanout.set_control_identify_off.if0                                    77636      61613   -16023 (-20.64 %)
  aecp_fanout.set_control_identify_off.if1                                    65188      55230    -9958 (-15.28 %)
  aecp_fanout.set_control_identify_on.if0                                     51565      55427    +3862 (+7.49 %)
  aecp_fanout.set_control_identify_on.if1                                     64796      46598   -18198 (-28.09 %)
  aecp_fanout.set_name.if0                                                    61077      70337    +9260 (+15.16 %)
  aecp_fanout.set_name.if1                                                    71067      53133   -17934 (-25.24 %)
  aecp_fanout.set_sampling_rate.if0                                           65837      49911   -15926 (-24.19 %)
  aecp_fanout.unlock_entity.if0                                               64873      48479   -16394 (-25.27 %)
  aecp_fanout.unlock_entity.if1                                               64873      48367   -16506 (-25.44 %)
largest difference: -18198 CPU cycles at aecp_fanout.set_control_identify_on.if1
recorded: 4812 passes, heaviest work pass 120238 cycles (1.20238 ms)
head: 4715 passes, heaviest work pass 118364 cycles (1.18364 ms)
recorded summary 99204720 CPU cycles; head 99021690
group acmp-cmd: 16 probes on the head's build, 16 on the recorded leg's
  acmp.bind_rx.if0                                                            21082      20320     -762 (-3.61 %)
  acmp.bind_rx.if1                                                            18358      17744     -614 (-3.34 %)
  acmp.disconnect_tx.if0                                                      17650       9940    -7710 (-43.68 %)
  acmp.disconnect_tx.if1                                                      10873       9148    -1725 (-15.86 %)
  acmp.get_rx_state.if0                                                       10850       9921     -929 (-8.56 %)
  acmp.get_rx_state.if1                                                        9280      10556    +1276 (+13.75 %)
  acmp.get_tx_connection.if0                                                  10162      10007     -155 (-1.53 %)
  acmp.get_tx_connection.if1                                                   8603       9475     +872 (+10.14 %)
  acmp.get_tx_state.if0                                                        9445      10159     +714 (+7.56 %)
  acmp.get_tx_state.if1                                                       11240      10773     -467 (-4.15 %)
  acmp.probe_tx.if0                                                           11586      10524    -1062 (-9.17 %)
  acmp.probe_tx.if1                                                            9990      10002      +12 (+0.12 %)
  acmp.probe_tx_response.if0                                                  10167       9383     -784 (-7.71 %)
  acmp.probe_tx_response.if1                                                   9600       9293     -307 (-3.20 %)
  acmp.unbind_rx.if0                                                          14311      14291      -20 (-0.14 %)
  acmp.unbind_rx.if1                                                          15630      13775    -1855 (-11.87 %)
largest difference: -7710 CPU cycles at acmp.disconnect_tx.if0
recorded: 3605 passes, heaviest work pass 120238 cycles (1.20238 ms)
head: 3540 passes, heaviest work pass 118364 cycles (1.18364 ms)
recorded summary 73401546 CPU cycles; head 73470384
