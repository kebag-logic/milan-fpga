# CPU budget harness, 1x1/1if: the legs the round's change reaches, base (round 1's head runs: 8845364d's images, which are 0d80f0ed's) against the code head b4a1dde2 (its images 847b2e21's)

Each arm built as run.py builds it (legs.py build: CPU regions cover, the split placement's L1, no XIP) and run with the formal measurement's options (run.py --reuse-build --record-budget-findings --record-share-findings --fetch-l1 split), every group of an arm at once. Head image sha256 (ctrl_app.elf): none a0338c2c, valid-destinations 864b4dcc, declaring-outputs 8b7fce18; each equal to the harness images build.firmware links at b4a1dde2 (rom-ledger-images receipt). The legs: arm A's srp, backlog-owed, aecp, datapath-events and aecp-largest-notice; valid-destinations' srp-talker-held and srp-talker-loss (one leg here, two at the base); declaring-outputs' aecp-outputs. Run rc: none 0, valid-destinations 0, declaring-outputs 0.

## Every graded probe, none (probe_cmp.py)
| Probe | base ms | head ms | head-base | budget ms | verdict base / head | pass instructions base / head |
|---|---:|---:|---:|---:|---|---|
| `aecp-largest-notice/aecp_long.add_audio_mappings.if0` | 3.397 | 3.069 | -0.327 | 20 | fits / fits | 29671 / 29671 |
| `aecp-largest-notice/aecp_long.refused.collision_indices.if0` | 2.426 | 2.426 | +0.000 | 20 | fits / fits | 5828 / 5828 |
| `aecp-largest-notice/aecp_long.refused.collision_values.if0` | 3.668 | 3.665 | -0.003 | 20 | fits / fits | 18912 / 18912 |
| `aecp-largest-notice/aecp_long.refused.conflict_last.if0` | 3.520 | 3.522 | +0.002 | 20 | fits / fits | 22868 / 22868 |
| `aecp-largest-notice/aecp_long.remove_audio_mappings.if0` | 1.377 | 1.380 | +0.003 | 20 | fits / fits | 30117 / 30117 |
| `aecp/aecp.entity_available.if0` | 0.108 | 0.107 | -0.000 | 20 | fits / fits | 3584 / 3584 |
| `aecp/aecp.get_as_path.if0` | 0.156 | 0.175 | +0.019 | 20 | fits / fits | 3861 / 3858 |
| `aecp/aecp.get_avb_info.if0` | 0.178 | 0.152 | -0.026 | 20 | fits / fits | 3916 / 3916 |
| `aecp/aecp.get_configuration.if0` | 0.129 | 0.129 | +0.000 | 20 | fits / fits | 3534 / 3534 |
| `aecp/aecp.get_counters.if0` | 0.153 | 0.152 | -0.001 | 20 | fits / fits | 3951 / 3951 |
| `aecp/aecp.get_name.if0` | 0.161 | 0.160 | -0.001 | 20 | fits / fits | 3923 / 3923 |
| `aecp/aecp.lock_entity.if0` | 0.216 | 0.219 | +0.003 | 20 | fits / fits | 4893 / 4893 |
| `aecp/aecp.mvu_get_milan_info.if0` | 0.188 | 0.193 | +0.006 | 20 | fits / fits | 3531 / 3531 |
| `aecp/aecp.read_descriptor.t0.i0.c0.if0` | 0.196 | 0.195 | -0.001 | 20 | fits / fits | 4463 / 4463 |
| `aecp/aecp.read_descriptor.t1.i0.c0.if0` | 0.147 | 0.146 | -0.001 | 20 | fits / fits | 3979 / 3979 |
| `aecp/aecp.read_descriptor.t10.i2.c0.if0` | 0.139 | 0.138 | -0.001 | 20 | fits / fits | 3936 / 3936 |
| `aecp/aecp.read_descriptor.t12.i0.c0.if0` | 0.156 | 0.157 | +0.000 | 20 | fits / fits | 3772 / 3772 |
| `aecp/aecp.read_descriptor.t13.i0.c0.if0` | 0.163 | 0.162 | -0.001 | 20 | fits / fits | 4092 / 4092 |
| `aecp/aecp.read_descriptor.t14.i0.c0.if0` | 0.152 | 0.152 | -0.001 | 20 | fits / fits | 3726 / 3726 |
| `aecp/aecp.read_descriptor.t15.i0.c0.if0` | 0.128 | 0.160 | +0.031 | 20 | fits / fits | 3726 / 4313 |
| `aecp/aecp.read_descriptor.t2.i0.c0.if0` | 0.158 | 0.158 | -0.001 | 20 | fits / fits | 3830 / 3830 |
| `aecp/aecp.read_descriptor.t20.i24.c0.if0` | 0.158 | 0.133 | -0.025 | 20 | fits / fits | 3786 / 3786 |
| `aecp/aecp.read_descriptor.t26.i0.c0.if0` | 0.166 | 0.165 | -0.001 | 20 | fits / fits | 3993 / 3993 |
| `aecp/aecp.read_descriptor.t36.i0.c0.if0` | 0.137 | 0.135 | -0.002 | 20 | fits / fits | 3921 / 3921 |
| `aecp/aecp.read_descriptor.t5.i1.c0.if0` | 0.144 | 0.173 | +0.029 | 20 | fits / fits | 4067 / 4654 |
| `aecp/aecp.read_descriptor.t6.i1.c0.if0` | 0.166 | 0.143 | -0.023 | 20 | fits / fits | 4067 / 4067 |
| `aecp/aecp.read_descriptor.t9.i0.c0.if0` | 0.157 | 0.158 | +0.001 | 20 | fits / fits | 3797 / 3797 |
| `aecp/aecp.register_unsolicited.if0` | 0.220 | 0.220 | +0.000 | 20 | fits / fits | 3660 / 3660 |
| `aecp/aecp.set_name.if0` | 0.200 | 0.201 | +0.001 | 20 | fits / fits | 5941 / 5941 |
| `aecp/aecp.unknown_command.if0` | 0.116 | 0.116 | -0.000 | 20 | fits / fits | 3521 / 3521 |
| `aecp/aecp.unlock_entity.if0` | 0.178 | 0.205 | +0.026 | 20 | fits / fits | 4885 / 4872 |
| `backlog-owed/backlog-owed.service.acmp.first.if0` | 1.417 | 1.418 | +0.002 | 20 | fits / fits | 30470 / 30470 |
| `backlog-owed/backlog-owed.service.acmp.last.if0` | 62.078 | 62.075 | -0.003 | 20 | MISS / MISS | 5291 / 5291 |
| `backlog-owed/backlog-owed.service.adp.first.if0` | 1.460 | 1.462 | +0.002 | 20 | fits / fits | 30470 / 30470 |
| `backlog-owed/backlog-owed.service.adp.last.if0` | 2.258 | 2.267 | +0.009 | 20 | fits / fits | 21645 / 21642 |
| `backlog-owed/backlog-owed.service.aecp.first.if0` | 1.453 | 1.455 | +0.002 | 20 | fits / fits | 30470 / 30470 |
| `backlog-owed/backlog-owed.service.aecp.last.if0` | 61.839 | 61.835 | -0.004 | 20 | MISS / MISS | 26381 / 26381 |
| `backlog-owed/backlog-owed.service.maap.first.if0` | 1.443 | 1.444 | +0.002 | 20 | fits / fits | 30470 / 30470 |
| `backlog-owed/backlog-owed.service.maap.last.if0` | 2.243 | 2.252 | +0.009 | 20 | fits / fits | 21645 / 21642 |
| `backlog-owed/backlog-owed.service.srp.first.if0` | 3.049 | 3.037 | -0.012 | 20 | fits / fits | 14171 / 14171 |
| `backlog-owed/backlog-owed.service.srp.last.if0` | 6.450 | 6.309 | -0.141 | 20 | fits / fits | 16030 / 17697 |
| `backlog-owed/backlog.owed.if0` | 62.871 | 62.866 | -0.005 | 20 | MISS / MISS | 3101 / 3101 |
| `backlog-owed/backlog.owed_behind0.if0` | 63.034 | 63.029 | -0.005 | 20 | MISS / MISS | 3107 / 3107 |
| `backlog-owed/backlog.owed_behind1.if0` | 63.196 | 63.191 | -0.005 | 20 | MISS / MISS | 3107 / 3107 |
| `backlog-owed/backlog.owed_behind2.if0` | 63.359 | 63.354 | -0.005 | 20 | MISS / MISS | 3110 / 3110 |
| `backlog-owed/backlog.owed_behind3.if0` | 63.520 | 63.515 | -0.005 | 20 | MISS / MISS | 3097 / 3097 |
| `srp/srp.domain.if0` | 0.771 | 0.755 | -0.015 | 220 | fits / fits | 8419 / 8403 |
| `srp/srp.listener_ready.if0` | 0.398 | 0.392 | -0.006 | 20 | fits / fits | 5341 / 5341 |
| `srp/srp.malformed.if0` | 0.178 | 0.173 | -0.005 | 20 | fits / fits | 2896 / 2896 |
| `srp/srp.startup.if0` | 0.729 | 0.725 | -0.004 | 20 | fits / fits | 5796 / 5773 |

probes: base 50, head 50, paired 50, only base 0, only head 0
verdicts changed: 0
misses each side: base 7, head 7
largest differences: aecp-largest-notice/aecp_long.add_audio_mappings.if0 -0.327 ms (3.397 -> 3.069, budget 20); backlog-owed/backlog-owed.service.srp.last.if0 -0.141 ms (6.450 -> 6.309, budget 20); aecp/aecp.read_descriptor.t15.i0.c0.if0 +0.031 ms (0.128 -> 0.160, budget 20); aecp/aecp.read_descriptor.t5.i1.c0.if0 +0.029 ms (0.144 -> 0.173, budget 20); aecp/aecp.unlock_entity.if0 +0.026 ms (0.178 -> 0.205, budget 20)
passes with another instruction count: 9 of 50 (aecp/aecp.get_as_path.if0 3861 -> 3858; aecp/aecp.read_descriptor.t15.i0.c0.if0 3726 -> 4313; aecp/aecp.read_descriptor.t5.i1.c0.if0 4067 -> 4654; aecp/aecp.unlock_entity.if0 4885 -> 4872; backlog-owed/backlog-owed.service.adp.last.if0 21645 -> 21642; backlog-owed/backlog-owed.service.maap.last.if0 21645 -> 21642; backlog-owed/backlog-owed.service.srp.last.if0 16030 -> 17697; srp/srp.domain.if0 8419 -> 8403; srp/srp.startup.if0 5796 -> 5773)

## Every graded probe, valid-destinations (probe_cmp.py)
| Probe | base ms | head ms | head-base | budget ms | verdict base / head | pass instructions base / head |
|---|---:|---:|---:|---:|---|---|
| `srp-talker-held/srp-talker-held.held.acmp.if0` | 2.406 | 2.397 | -0.008 | 20 | fits / fits | 17513 / 17506 |
| `srp-talker-held/srp-talker-held.held.adp.if0` | 1.547 | 1.551 | +0.004 | 20 | fits / fits | 37617 / 37617 |
| `srp-talker-held/srp-talker-held.held.aecp.if0` | 3.029 | 2.999 | -0.030 | 20 | fits / fits | 13689 / 13689 |
| `srp-talker-held/srp-talker-held.held.maap.if0` | 2.011 | 2.003 | -0.008 | 20 | fits / fits | 17513 / 17506 |
| `srp-talker-held/srp-talker-held.held.srp.if0` | 8.430 | 8.394 | -0.036 | 20 | fits / fits | 14913 / 14913 |
| `srp-talker-held/srp-talker-held.mrpdu.join.if0` | 0.594 | 0.535 | -0.059 | 49 | fits / fits | None / None |
| `srp-talker-held/srp-talker-held.mrpdu.periodic.if0` | 2.868 | 2.944 | +0.076 | 49 | fits / fits | None / None |
| `srp-talker-held/srp.listener_ready.s0.if0` | 0.410 | 0.409 | -0.001 | 20 | fits / fits | 5745 / 5745 |
| `srp-talker-held/srp.listener_ready.s1.if0` | 0.420 | 0.417 | -0.004 | 20 | fits / fits | 5931 / 5931 |
| `srp-talker-held/srp.talker_declare.s0.if0` | 0.600 | 0.592 | -0.007 | 220 | fits / fits | 6463 / 6447 |
| `srp-talker-held/srp.talker_declare.s1.if0` | 185.724 | 185.876 | +0.152 | 220 | fits / fits | 6362 / 6346 |
| `srp-talker-loss/srp.talker_declare.s0.if0` | 0.600 | 0.592 | -0.007 | 220 | fits / fits | 6463 / 6447 |
| `srp-talker-loss/srp.talker_declare.s1.if0` | 185.724 | 185.876 | +0.152 | 220 | fits / fits | 6362 / 6346 |
| `srp-talker-loss/srp.talker_loss.if0` | 189.659 | 189.522 | -0.137 | 220 | fits / fits | 6606 / 6590 |

probes: base 14, head 14, paired 14, only base 0, only head 0
verdicts changed: 0
misses each side: base 0, head 0
largest differences: srp-talker-loss/srp.talker_declare.s1.if0 +0.152 ms (185.724 -> 185.876, budget 220); srp-talker-held/srp.talker_declare.s1.if0 +0.152 ms (185.724 -> 185.876, budget 220); srp-talker-loss/srp.talker_loss.if0 -0.137 ms (189.659 -> 189.522, budget 220); srp-talker-held/srp-talker-held.mrpdu.periodic.if0 +0.076 ms (2.868 -> 2.944, budget 49); srp-talker-held/srp-talker-held.mrpdu.join.if0 -0.059 ms (0.594 -> 0.535, budget 49)
passes with another instruction count: 7 of 14 (srp-talker-held/srp-talker-held.held.acmp.if0 17513 -> 17506; srp-talker-held/srp-talker-held.held.maap.if0 17513 -> 17506; srp-talker-held/srp.talker_declare.s0.if0 6463 -> 6447; srp-talker-held/srp.talker_declare.s1.if0 6362 -> 6346; srp-talker-loss/srp.talker_declare.s0.if0 6463 -> 6447; srp-talker-loss/srp.talker_declare.s1.if0 6362 -> 6346; srp-talker-loss/srp.talker_loss.if0 6606 -> 6590)

## Every graded probe, declaring-outputs (probe_cmp.py)
| Probe | base ms | head ms | head-base | budget ms | verdict base / head | pass instructions base / head |
|---|---:|---:|---:|---:|---|---|
| `aecp-outputs/aecp_outputs.declared.if0` | 1.439 | 1.290 | -0.149 | 20 | fits / fits | 7924 / 7927 |
| `aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o0.if0` | 0.216 | 0.174 | -0.042 | 20 | fits / fits | 5191 / 5191 |
| `aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o1.if0` | 0.172 | 0.136 | -0.036 | 20 | fits / fits | 5156 / 5156 |
| `aecp-outputs/aecp_outputs.held_get_stream_info.if0` | 4.121 | 4.124 | +0.004 | 20 | fits / fits | 4240 / 4237 |
| `aecp-outputs/aecp_outputs.held_set_stream_info.if0` | 9.161 | 9.160 | -0.002 | 20 | fits / fits | 4240 / 4237 |
| `aecp-outputs/aecp_outputs.set_stream_info.set_stream_info_locked.if0` | 0.199 | 0.197 | -0.002 | 20 | fits / fits | 5206 / 5206 |
| `aecp-outputs/aecp_outputs.set_stream_info.set_stream_info_stream_id.if0` | 0.227 | 0.184 | -0.043 | 20 | fits / fits | 5214 / 5208 |

probes: base 7, head 7, paired 7, only base 0, only head 0
verdicts changed: 0
misses each side: base 0, head 0
largest differences: aecp-outputs/aecp_outputs.declared.if0 -0.149 ms (1.439 -> 1.290, budget 20); aecp-outputs/aecp_outputs.set_stream_info.set_stream_info_stream_id.if0 -0.043 ms (0.227 -> 0.184, budget 20); aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o0.if0 -0.042 ms (0.216 -> 0.174, budget 20); aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o1.if0 -0.036 ms (0.172 -> 0.136, budget 20); aecp-outputs/aecp_outputs.held_get_stream_info.if0 +0.004 ms (4.121 -> 4.124, budget 20)
passes with another instruction count: 4 of 7 (aecp-outputs/aecp_outputs.declared.if0 7924 -> 7927; aecp-outputs/aecp_outputs.held_get_stream_info.if0 4240 -> 4237; aecp-outputs/aecp_outputs.held_set_stream_info.if0 4240 -> 4237; aecp-outputs/aecp_outputs.set_stream_info.set_stream_info_stream_id.if0 5214 -> 5208)

## Passes given whole and the pass classes, by group (passes_cmp.py; CPU cycles, joins in ms)
| Group | build-one heaviest (limit), base / head | build | step | longest build slice | joins ms (base) | joins ms (head) | late joins b/h | over the share b/h | findings b/h |
|---|---|---|---|---|---|---|---|---|---|
| `aecp` | 29872 / 29556 (73500) | 0 / 0 | 0 / 0 | 29872 / 29556 | 188.937 to 189.986 | 188.043 to 189.984 | 0 / 0 | 0 / 0 | 0 / 0 |
| `aecp-largest-notice` | 29872 / 29556 (73500) | 0 / 0 | 0 / 0 | 29872 / 29556 | 188.937 to 189.986 | 188.043 to 189.984 | 0 / 0 | 0 / 0 | 0 / 0 |
| `aecp-outputs` | 38364 / 37929 (73500) | 0 / 0 | 0 / 0 | 38364 / 37929 | 187.99 to 189.895 | 187.826 to 189.991 | 0 / 0 | 0 / 0 | 0 / 0 |
| `backlog-owed` | 29872 / 29556 (73500) | 0 / 0 | 0 / 0 | 29872 / 29556 | 188.937 to 189.986 | 188.043 to 189.984 | 0 / 0 | 0 / 0 | 0 / 0 |
| `datapath-events` | 29872 / 29556 (73500) | 0 / 0 | 0 / 0 | 29872 / 29556 | 188.937 to 189.986 | 188.043 to 189.984 | 0 / 0 | 0 / 0 | 0 / 0 |
| `srp` | 53168 / 52531 (73500) | 0 / 0 | 0 / 0 | 53168 / 52531 | 188.937 to 189.986 | 188.043 to 189.984 | 0 / 0 | 0 / 0 | 0 / 0 |
| `srp-talker-held` | 42176 / 40542 (73500) | 0 / 0 | 0 / 0 | 42176 / 51697 | 187.204 to 190.123 | 187.463 to 190.027 | 0 / 0 | 0 / 0 | 0 / 0 |
| `srp-talker-loss` | 40024 / 38490 (73500) | 0 / 0 | 0 / 0 | 40024 / 38490 | 187.204 to 190.163 | 187.463 to 190.027 | 0 / 0 | 0 / 0 | 0 / 0 |

head findings over all groups: 0

## Every stated cost the tree makes of each measured cost: the most CPU cycles each side, the head's figure by the rule (cycles / 100 x 1.05, rounded up to 5 us), its statement (survey_point4.py, statements.py)
| Cost (1x1/1if) | Base cycles | Head cycles | Head rule, us | Stated, us | Head verdict | Statement; where (head) |
|---|---:|---:|---:|---:|---|---|
| base | 19,342 | 19,515 | 205 | 225 | within | load_grade.stated(1x1/1if) GRADED base; valid-destinations/srp-talker-held |
| base | 19,342 | 19,515 | 205 | 225 | within | load_grade.stated(1x1/1if) STATED_US base; valid-destinations/srp-talker-held |
| base | 19,342 | 19,515 | 205 | 225 | within | poll_grade.STATED_US[(1, 2, 2)] base; valid-destinations/srp-talker-held |
| build | 0 | 0 | 0 | 1010 | within | load_grade.stated(1x1/1if) GRADED build; declaring-outputs/aecp-outputs |
| build | 0 | 0 | 0 | 1010 | within | load_grade.stated(1x1/1if) STATED_US build; declaring-outputs/aecp-outputs |
| build | 0 | 0 | 0 | 1010 | within | whole_grade.stated_us((1, 2, 2)) build (ctrl_loop.h); declaring-outputs/aecp-outputs |
| build_one | 53,168 | 52,531 | 555 | 735 | within | load_grade.stated(1x1/1if) GRADED build_one; none/srp |
| build_one | 53,168 | 52,531 | 555 | 735 | within | load_grade.stated(1x1/1if) STATED_US build_one; none/srp |
| build_one | 53,168 | 52,531 | 555 | 735 | within | whole_grade.stated_us((1, 2, 2)) build-one (ctrl_loop.h); none/srp |
| centisecond | 16,064 | 14,213 | 150 | 170 | within | load_grade.stated(1x1/1if) GRADED centisecond; valid-destinations/srp-talker-held.log |
| centisecond | 16,064 | 14,213 | 150 | 170 | within | load_grade.stated(1x1/1if) STATED_US centisecond; valid-destinations/srp-talker-held.log |
| event.ADP | 6,753 | 7,338 | 80 | 115 | within | load_grade.stated(1x1/1if) GRADED event.ADP; TIMER#0, 9 taken |
| event.ADP | 6,753 | 7,338 | 80 | 115 | within | load_grade.stated(1x1/1if) STATED_US event.ADP; TIMER#0, 9 taken |
| event.AECP | 4,416 | 5,251 | 60 | 75 | within | load_grade.stated(1x1/1if) GRADED event.AECP; TIMER#3, 1934 taken |
| event.AECP | 4,416 | 5,251 | 60 | 75 | within | load_grade.stated(1x1/1if) STATED_US event.AECP; TIMER#3, 1934 taken |
| event.AMAP_LIVE_WRITE | 1,261 | 1,291 | 15 | 30 | within | rows_tiers.DATAPATH_US[1x1/1if] AMAP_LIVE_WRITE; datapath-events.log@70331709 |
| event.AS_PATH_CHANGED | 2,264 | 2,072 | 25 | 35 | within | rows_tiers.DATAPATH_US[1x1/1if] AS_PATH_CHANGED; datapath-events.log@68335288 |
| event.AVB_INFO_CHANGED | 2,294 | 2,384 | 30 | 35 | within | rows_tiers.DATAPATH_US[1x1/1if] AVB_INFO_CHANGED; datapath-events.log@67522297 |
| event.GM | 2,365 | 2,365 | 25 | 40 | within | load_grade.stated(1x1/1if) GRADED event.GM; GM, 15 taken |
| event.GM | 2,365 | 2,365 | 25 | 40 | within | load_grade.stated(1x1/1if) STATED_US event.GM; GM, 15 taken |
| event.LINK | 10,564 | 10,443 | 110 | 155 | within | rows_grade.ROW_COSTS[1x1/1if] event.LINK; LINK, 7 taken |
| event.MAAP | 12,705 | 12,808 | 135 | 170 | within | load_grade.stated(1x1/1if) GRADED event.MAAP; TIMER#2, 20 taken |
| event.MAAP | 12,705 | 12,808 | 135 | 165 | within | load_grade.stated(1x1/1if) STATED_US event.MAAP; TIMER#2, 20 taken |
| event.TICK | 2,230 | 2,138 | 25 | 55 | within | load_grade.stated(1x1/1if) GRADED event.TICK; TICK, 2459 taken |
| event.TICK | 2,230 | 2,138 | 25 | 55 | within | load_grade.stated(1x1/1if) STATED_US event.TICK; TICK, 2459 taken |
| events_none | 2,991 | 3,187 | 35 | 40 | within | load_grade.stated(1x1/1if) GRADED events_none; valid-destinations/srp-talker-held.log |
| events_none | 2,991 | 3,187 | 35 | 40 | within | load_grade.stated(1x1/1if) STATED_US events_none; valid-destinations/srp-talker-held.log |
| item.acmp | 4,319 | 4,522 | 50 | 55 | within | load_grade.stated(1x1/1if) GRADED item.acmp; none/backlog-owed |
| item.acmp | 4,319 | 4,522 | 50 | 55 | within | load_grade.stated(1x1/1if) STATED_US item.acmp; none/backlog-owed |
| item.acmp | 4,319 | 4,522 | 50 | 55 | within | poll_grade.STATED_US[(1, 2, 2)] acmp; none/backlog-owed |
| item.acmp_declined | 1,476 | 1,476 | 20 | 20 | within | load_grade.stated(1x1/1if) GRADED item.acmp_declined; none/backlog-owed |
| item.acmp_declined | 1,476 | 1,476 | 20 | 20 | within | load_grade.stated(1x1/1if) STATED_US item.acmp_declined; none/backlog-owed |
| item.acmp_declined | 1,476 | 1,476 | 20 | 20 | within | poll_grade.STATED_US[(1, 2, 2)] acmp_declined; none/backlog-owed |
| item.acmp_kept | 6,932 | 7,099 | 75 | 280 | within | load_grade.stated(1x1/1if) STATED_US record.acmp; none/backlog-owed |
| item.aecp | 13,832 | 13,631 | 145 | 150 | within | poll_grade.STATED_US[(1, 2, 2)] aecp; declaring-outputs/aecp-outputs |
| item.aecp.notice | 13,832 | 13,631 | 145 | 150 | within | load_grade.stated(1x1/1if) GRADED item.aecp.notice; declaring-outputs/aecp-outputs (16 frame(s)) |
| item.aecp.notice | 13,832 | 13,631 | 145 | 150 | within | load_grade.stated(1x1/1if) STATED_US item.aecp.notice; declaring-outputs/aecp-outputs (16 frame(s)) |
| item.aecp.response | 2,844 | 2,844 | 30 | 60 | within | load_grade.stated(1x1/1if) GRADED item.aecp.response; none/backlog-owed (1 frame(s)) |
| item.aecp.response | 2,844 | 2,844 | 30 | 60 | within | load_grade.stated(1x1/1if) STATED_US item.aecp.response; none/backlog-owed (1 frame(s)) |
| item.aecp_long | 0 | 0 | 0 | 315 | within | poll_grade.STATED_US[(1, 2, 2)] aecp_long; declaring-outputs/aecp-outputs |
| item.mrpdu | 0 | 0 | 0 | 735 | within | load_grade.stated(1x1/1if) GRADED item.mrpdu; declaring-outputs/aecp-outputs |
| item.mrpdu | 0 | 0 | 0 | 735 | within | load_grade.stated(1x1/1if) STATED_US item.mrpdu; declaring-outputs/aecp-outputs |
| item.mrpdu | 0 | 0 | 0 | 735 | within | poll_grade.STATED_US[(1, 2, 2)] mrpdu; declaring-outputs/aecp-outputs |
| item.rebuild | 0 | 0 | 0 | 290 | within | poll_grade.STATED_US[(1, 2, 2)] rebuild; declaring-outputs/aecp-outputs |
| item.reclaim | 1,688 | 1,683 | 20 | 25 | within | load_grade.stated(1x1/1if) GRADED item.reclaim; none/srp |
| item.reclaim | 1,688 | 1,683 | 20 | 25 | within | load_grade.stated(1x1/1if) STATED_US item.reclaim; none/srp |
| item.reclaim | 1,688 | 1,683 | 20 | 25 | within | poll_grade.STATED_US[(1, 2, 2)] reclaim; none/srp |
| item.record | 24,029 | 23,625 | 250 | 285 | within | poll_grade.STATED_US[(1, 2, 2)] retained; valid-destinations/srp-talker-held |
| item.retained | 0 | 0 | 0 | 285 | within | load_grade.stated(1x1/1if) GRADED item.retained; declaring-outputs/aecp-outputs |
| item.retained | 0 | 0 | 0 | 285 | within | load_grade.stated(1x1/1if) STATED_US item.retained; declaring-outputs/aecp-outputs |
| item.retained | 0 | 0 | 0 | 285 | within | poll_grade.STATED_US[(1, 2, 2)] retained; declaring-outputs/aecp-outputs |
| item.walk | 2,105 | 2,032 | 25 | 35 | within | load_grade.stated(1x1/1if) GRADED item.walk; none/srp |
| item.walk | 2,105 | 2,032 | 25 | 35 | within | load_grade.stated(1x1/1if) STATED_US item.walk; none/srp |
| item.walk | 2,105 | 2,032 | 25 | 35 | within | poll_grade.STATED_US[(1, 2, 2)] walk; none/srp |
| item.withdraw | 0 | 0 | 0 | 90 | within | poll_grade.STATED_US[(1, 2, 2)] withdraw; declaring-outputs/aecp-outputs |
| record.acmp | 10,433 | 10,458 | 110 | 265 | within | load_grade.stated(1x1/1if) GRADED record.acmp; declaring-outputs/aecp-outputs.log |
| record.acmp | 10,433 | 10,458 | 110 | 280 | within | load_grade.stated(1x1/1if) STATED_US record.acmp; declaring-outputs/aecp-outputs.log |
| record.adp | 1,649 | 1,649 | 20 | 105 | within | load_grade.stated(1x1/1if) GRADED record.adp; valid-destinations/srp-talker-held.log |
| record.adp | 1,649 | 1,649 | 20 | 105 | within | load_grade.stated(1x1/1if) STATED_US record.adp; valid-destinations/srp-talker-held.log |
| record.maap | 10,001 | 9,981 | 105 | 115 | within | load_grade.stated(1x1/1if) GRADED record.maap; valid-destinations/srp-talker-loss.log |
| record.maap | 10,001 | 9,981 | 105 | 115 | within | load_grade.stated(1x1/1if) STATED_US record.maap; valid-destinations/srp-talker-loss.log |
| record.srp | 24,266 | 23,874 | 255 | 285 | within | load_grade.stated(1x1/1if) GRADED record.srp; valid-destinations/srp-talker-held.log |
| record.srp | 24,266 | 23,874 | 255 | 285 | within | load_grade.stated(1x1/1if) STATED_US record.srp; valid-destinations/srp-talker-held.log |
| step | 0 | 0 | 0 | 975 | within | load_grade.stated(1x1/1if) GRADED step; declaring-outputs/aecp-outputs |
| step | 0 | 0 | 0 | 975 | within | load_grade.stated(1x1/1if) STATED_US step; declaring-outputs/aecp-outputs |
| step | 0 | 0 | 0 | 975 | within | whole_grade.stated_us((1, 2, 2)) step (ctrl_loop.h); declaring-outputs/aecp-outputs |

66 head rows, 0 not within; 66 base rows

## The largest legal notice (compare-long)
# aecp-largest-notice: its notices against the largest legal notice's statement at 1x1/1if (poll_grade aecp_long)
item.aecp_long (the polls): 29,554 CPU cycles, 315 us by the rule, against aecp_long 315 us at 1x1/1if: within; none/aecp-largest-notice
the notice kind (aecp_kinds.py): 29,554 CPU cycles, 315 us by the rule, against aecp_long 315 us at 1x1/1if: within; none/aecp-largest-notice (15 frame(s))
# 0 exceeded
