# CPU budget harness, 8x8/1if: the legs the round's change reaches, base (round 1's head runs: 8845364d's images, which are 0d80f0ed's) against the code head b4a1dde2 (its images 847b2e21's)

Each arm built as run.py builds it (legs.py build) and run with the formal measurement's options (run.py --reuse-build --record-budget-findings --record-share-findings --fetch-l1 split). Head image sha256 (ctrl_app.elf): none 04b7c59e, valid-destinations 44396d89, declaring-outputs 1366ffb3; each equal to the harness images build.firmware links at b4a1dde2. The legs: arm A's srp, backlog-owed, aecp and datapath-events; valid-destinations' srp-talker-held and srp-talker-loss; declaring-outputs' aecp-outputs. Run rc: none 0, declaring-outputs 0, srp-talker-held 0, srp-talker-loss 0.

valid-destinations' first run ran both groups at once and was stopped at the author's tool's time limit, srp-talker-loss complete (its log ends RESULT: PASS) and srp-talker-held at about 82%. srp-talker-loss is graded from that log (run.py --regrade); srp-talker-held ran again alone, on the same build, in its own unit, to completion (rc 0: 1 group graded, 0 refusals, 0 budget misses, 0 of 25,334 work passes over the share). The base's two groups are round 1's two runs; each side's two are merged for the comparison.

## Every graded probe, none (probe_cmp.py)
| Probe | base ms | head ms | head-base | budget ms | verdict base / head | pass instructions base / head |
|---|---:|---:|---:|---:|---|---|
| `aecp/aecp.entity_available.if0` | 0.206 | 0.211 | +0.004 | 20 | fits / fits | 4947 / 4947 |
| `aecp/aecp.get_as_path.if0` | 0.147 | 0.122 | -0.026 | 20 | fits / fits | 5213 / 5219 |
| `aecp/aecp.get_avb_info.if0` | 0.214 | 0.215 | +0.001 | 20 | fits / fits | 5279 / 5279 |
| `aecp/aecp.get_configuration.if0` | 0.183 | 0.187 | +0.003 | 20 | fits / fits | 4897 / 4897 |
| `aecp/aecp.get_counters.if0` | 0.249 | 0.253 | +0.005 | 20 | fits / fits | 5314 / 5314 |
| `aecp/aecp.get_name.if0` | 0.204 | 0.205 | +0.001 | 20 | fits / fits | 5286 / 5286 |
| `aecp/aecp.lock_entity.if0` | 0.232 | 0.234 | +0.001 | 20 | fits / fits | 6263 / 6269 |
| `aecp/aecp.mvu_get_milan_info.if0` | 0.178 | 0.179 | +0.001 | 20 | fits / fits | 4894 / 4894 |
| `aecp/aecp.read_descriptor.t0.i0.c0.if0` | 0.266 | 0.269 | +0.003 | 20 | fits / fits | 5823 / 5823 |
| `aecp/aecp.read_descriptor.t1.i0.c0.if0` | 0.207 | 0.208 | +0.001 | 20 | fits / fits | 5342 / 5342 |
| `aecp/aecp.read_descriptor.t10.i9.c0.if0` | 0.198 | 0.199 | +0.001 | 20 | fits / fits | 5141 / 5141 |
| `aecp/aecp.read_descriptor.t12.i0.c0.if0` | 0.229 | 0.233 | +0.003 | 20 | fits / fits | 5260 / 5260 |
| `aecp/aecp.read_descriptor.t13.i0.c0.if0` | 0.278 | 0.272 | -0.006 | 20 | fits / fits | 6108 / 6108 |
| `aecp/aecp.read_descriptor.t14.i7.c0.if0` | 0.198 | 0.201 | +0.003 | 20 | fits / fits | 5145 / 5145 |
| `aecp/aecp.read_descriptor.t15.i7.c0.if0` | 0.225 | 0.228 | +0.003 | 20 | fits / fits | 5145 / 5145 |
| `aecp/aecp.read_descriptor.t2.i0.c0.if0` | 0.228 | 0.232 | +0.004 | 20 | fits / fits | 5193 / 5193 |
| `aecp/aecp.read_descriptor.t20.i71.c0.if0` | 0.199 | 0.200 | +0.001 | 20 | fits / fits | 5149 / 5149 |
| `aecp/aecp.read_descriptor.t26.i0.c0.if0` | 0.234 | 0.238 | +0.003 | 20 | fits / fits | 5356 / 5356 |
| `aecp/aecp.read_descriptor.t36.i0.c0.if0` | 0.204 | 0.205 | +0.001 | 20 | fits / fits | 5311 / 5311 |
| `aecp/aecp.read_descriptor.t5.i8.c0.if0` | 0.232 | 0.235 | +0.003 | 20 | fits / fits | 5189 / 5189 |
| `aecp/aecp.read_descriptor.t6.i8.c0.if0` | 0.210 | 0.210 | +0.001 | 20 | fits / fits | 5430 / 5430 |
| `aecp/aecp.read_descriptor.t9.i0.c0.if0` | 0.230 | 0.233 | +0.003 | 20 | fits / fits | 5160 / 5160 |
| `aecp/aecp.register_unsolicited.if0` | 0.173 | 0.175 | +0.002 | 20 | fits / fits | 5020 / 5020 |
| `aecp/aecp.set_name.if0` | 0.294 | 0.299 | +0.005 | 20 | fits / fits | 7304 / 7314 |
| `aecp/aecp.unknown_command.if0` | 0.217 | 0.221 | +0.004 | 20 | fits / fits | 4878 / 4884 |
| `aecp/aecp.unlock_entity.if0` | 0.126 | 0.241 | +0.116 | 20 | fits / fits | 6238 / 6248 |
| `backlog-owed/backlog-owed.service.acmp.first.if0` | 1.607 | 1.595 | -0.012 | 20 | fits / fits | 33302 / 33302 |
| `backlog-owed/backlog-owed.service.acmp.last.if0` | 62.171 | 62.239 | +0.068 | 20 | MISS / MISS | 7309 / 7302 |
| `backlog-owed/backlog-owed.service.adp.first.if0` | 1.650 | 1.638 | -0.012 | 20 | fits / fits | 33302 / 33302 |
| `backlog-owed/backlog-owed.service.adp.last.if0` | 3.108 | 3.076 | -0.032 | 20 | fits / fits | 32605 / 32605 |
| `backlog-owed/backlog-owed.service.aecp.first.if0` | 1.643 | 1.631 | -0.012 | 20 | fits / fits | 33302 / 33302 |
| `backlog-owed/backlog-owed.service.aecp.last.if0` | 61.853 | 61.566 | -0.287 | 20 | MISS / MISS | 28408 / 28420 |
| `backlog-owed/backlog-owed.service.maap.first.if0` | 1.632 | 1.621 | -0.012 | 20 | fits / fits | 33302 / 33302 |
| `backlog-owed/backlog-owed.service.maap.last.if0` | 3.093 | 3.061 | -0.032 | 20 | fits / fits | 32605 / 32605 |
| `backlog-owed/backlog-owed.service.srp.first.if0` | 3.092 | 3.060 | -0.032 | 20 | fits / fits | 32605 / 32605 |
| `backlog-owed/backlog-owed.service.srp.last.if0` | 6.380 | 6.271 | -0.109 | 20 | fits / fits | 20237 / 20858 |
| `backlog-owed/backlog.owed.if0` | 63.180 | 63.252 | +0.073 | 20 | MISS / MISS | 4793 / 4793 |
| `backlog-owed/backlog.owed_behind0.if0` | 63.393 | 63.466 | +0.073 | 20 | MISS / MISS | 4805 / 4805 |
| `backlog-owed/backlog.owed_behind1.if0` | 63.607 | 63.680 | +0.073 | 20 | MISS / MISS | 4802 / 4802 |
| `backlog-owed/backlog.owed_behind2.if0` | 63.819 | 63.892 | +0.073 | 20 | MISS / MISS | 4796 / 4796 |
| `backlog-owed/backlog.owed_behind3.if0` | 64.032 | 64.104 | +0.073 | 20 | MISS / MISS | 4789 / 4789 |
| `srp/srp.domain.if0` | 0.736 | 0.732 | -0.003 | 220 | fits / fits | 9653 / 9638 |
| `srp/srp.listener_ready.if0` | 0.407 | 0.403 | -0.004 | 20 | fits / fits | 7091 / 7091 |
| `srp/srp.malformed.if0` | 0.212 | 0.218 | +0.005 | 20 | fits / fits | 4400 / 4400 |
| `srp/srp.startup.if0` | 0.788 | 0.796 | +0.008 | 20 | fits / fits | 5904 / 5882 |

probes: base 45, head 45, paired 45, only base 0, only head 0
verdicts changed: 0
misses each side: base 7, head 7
largest differences: backlog-owed/backlog-owed.service.aecp.last.if0 -0.287 ms (61.853 -> 61.566, budget 20); aecp/aecp.unlock_entity.if0 +0.116 ms (0.126 -> 0.241, budget 20); backlog-owed/backlog-owed.service.srp.last.if0 -0.109 ms (6.380 -> 6.271, budget 20); backlog-owed/backlog.owed_behind3.if0 +0.073 ms (64.032 -> 64.104, budget 20); backlog-owed/backlog.owed_behind1.if0 +0.073 ms (63.607 -> 63.680, budget 20)
passes with another instruction count: 10 of 45 (aecp/aecp.get_as_path.if0 5213 -> 5219; aecp/aecp.lock_entity.if0 6263 -> 6269; aecp/aecp.set_name.if0 7304 -> 7314; aecp/aecp.unknown_command.if0 4878 -> 4884; aecp/aecp.unlock_entity.if0 6238 -> 6248; backlog-owed/backlog-owed.service.acmp.last.if0 7309 -> 7302; backlog-owed/backlog-owed.service.aecp.last.if0 28408 -> 28420; backlog-owed/backlog-owed.service.srp.last.if0 20237 -> 20858; srp/srp.domain.if0 9653 -> 9638; srp/srp.startup.if0 5904 -> 5882)

## Every graded probe, valid-destinations (probe_cmp.py)
| Probe | base ms | head ms | head-base | budget ms | verdict base / head | pass instructions base / head |
|---|---:|---:|---:|---:|---|---|
| `srp-talker-held/srp-talker-held.held.acmp.if0` | 4.101 | 4.467 | +0.365 | 20 | fits / fits | 33543 / 31118 |
| `srp-talker-held/srp-talker-held.held.adp.if0` | 3.316 | 3.379 | +0.062 | 20 | fits / fits | 32851 / 33057 |
| `srp-talker-held/srp-talker-held.held.aecp.if0` | 4.517 | 4.485 | -0.032 | 20 | fits / fits | 29116 / 29323 |
| `srp-talker-held/srp-talker-held.held.maap.if0` | 3.707 | 4.072 | +0.365 | 20 | fits / fits | 33543 / 31118 |
| `srp-talker-held/srp-talker-held.held.srp.if0` | 11.375 | 11.519 | +0.144 | 20 | fits / fits | 31005 / 31005 |
| `srp-talker-held/srp-talker-held.mrpdu.join.if0` | 1.401 | 1.452 | +0.051 | 49 | fits / fits | None / None |
| `srp-talker-held/srp-talker-held.mrpdu.leaveall.if0` | 1.401 | 1.050 | -0.351 | 49 | fits / fits | None / None |
| `srp-talker-held/srp-talker-held.mrpdu.periodic.if0` | 6.975 | 6.549 | -0.426 | 49 | fits / fits | None / None |
| `srp-talker-held/srp.listener_ready.s0.if0` | 0.565 | 0.568 | +0.003 | 20 | fits / fits | 9616 / 9620 |
| `srp-talker-held/srp.listener_ready.s1.if0` | 0.546 | 0.577 | +0.031 | 20 | fits / fits | 9111 / 9788 |
| `srp-talker-held/srp.listener_ready.s2.if0` | 0.581 | 0.581 | +0.000 | 20 | fits / fits | 9977 / 9969 |
| `srp-talker-held/srp.listener_ready.s3.if0` | 0.591 | 0.594 | +0.003 | 20 | fits / fits | 10190 / 10170 |
| `srp-talker-held/srp.listener_ready.s4.if0` | 0.570 | 0.573 | +0.003 | 20 | fits / fits | 9650 / 9632 |
| `srp-talker-held/srp.listener_ready.s5.if0` | 0.574 | 0.577 | +0.003 | 20 | fits / fits | 9831 / 9825 |
| `srp-talker-held/srp.listener_ready.s6.if0` | 0.639 | 0.616 | -0.022 | 20 | fits / fits | 10713 / 10697 |
| `srp-talker-held/srp.listener_ready.s7.if0` | 0.594 | 0.599 | +0.005 | 20 | fits / fits | 10193 / 10183 |
| `srp-talker-held/srp.listener_ready.s8.if0` | 0.638 | 0.613 | -0.026 | 20 | fits / fits | 11095 / 10356 |
| `srp-talker-held/srp.talker_declare.s0.if0` | 0.633 | 0.640 | +0.008 | 220 | fits / fits | 7659 / 7644 |
| `srp-talker-held/srp.talker_declare.s1.if0` | 185.760 | 185.638 | -0.122 | 220 | fits / fits | 6437 / 6422 |
| `srp-talker-held/srp.talker_declare.s2.if0` | 189.577 | 189.541 | -0.037 | 220 | fits / fits | 7727 / 9277 |
| `srp-talker-held/srp.talker_declare.s3.if0` | 189.278 | 189.522 | +0.244 | 220 | fits / fits | 9638 / 7982 |
| `srp-talker-held/srp.talker_declare.s4.if0` | 179.444 | 179.379 | -0.065 | 220 | fits / fits | 5898 / 5876 |
| `srp-talker-held/srp.talker_declare.s5.if0` | 8.862 | 9.313 | +0.451 | 220 | fits / fits | 13803 / 13788 |
| `srp-talker-held/srp.talker_declare.s6.if0` | 189.294 | 189.357 | +0.063 | 220 | fits / fits | 10112 / 10097 |
| `srp-talker-held/srp.talker_declare.s7.if0` | 186.816 | 188.709 | +1.893 | 220 | fits / fits | 10385 / 10370 |
| `srp-talker-held/srp.talker_declare.s8.if0` | 188.478 | 186.619 | -1.859 | 220 | fits / fits | 9392 / 11400 |
| `srp-talker-loss/srp.talker_declare.s0.if0` | 0.633 | 0.640 | +0.008 | 220 | fits / fits | 7659 / 7644 |
| `srp-talker-loss/srp.talker_declare.s1.if0` | 185.760 | 185.638 | -0.122 | 220 | fits / fits | 6437 / 6422 |
| `srp-talker-loss/srp.talker_declare.s2.if0` | 189.577 | 189.541 | -0.037 | 220 | fits / fits | 7727 / 9277 |
| `srp-talker-loss/srp.talker_declare.s3.if0` | 189.278 | 189.522 | +0.244 | 220 | fits / fits | 9638 / 7982 |
| `srp-talker-loss/srp.talker_declare.s4.if0` | 179.444 | 179.379 | -0.065 | 220 | fits / fits | 5898 / 5876 |
| `srp-talker-loss/srp.talker_declare.s5.if0` | 8.862 | 9.313 | +0.451 | 220 | fits / fits | 13803 / 13788 |
| `srp-talker-loss/srp.talker_declare.s6.if0` | 189.294 | 189.357 | +0.063 | 220 | fits / fits | 10112 / 10097 |
| `srp-talker-loss/srp.talker_declare.s7.if0` | 186.816 | 188.709 | +1.893 | 220 | fits / fits | 10385 / 10370 |
| `srp-talker-loss/srp.talker_declare.s8.if0` | 188.478 | 186.619 | -1.859 | 220 | fits / fits | 9392 / 11400 |
| `srp-talker-loss/srp.talker_loss.if0` | 186.045 | 188.130 | +2.085 | 220 | fits / fits | 22495 / 22480 |

probes: base 36, head 36, paired 36, only base 0, only head 0
verdicts changed: 0
misses each side: base 0, head 0
largest differences: srp-talker-loss/srp.talker_loss.if0 +2.085 ms (186.045 -> 188.130, budget 220); srp-talker-loss/srp.talker_declare.s7.if0 +1.893 ms (186.816 -> 188.709, budget 220); srp-talker-held/srp.talker_declare.s7.if0 +1.893 ms (186.816 -> 188.709, budget 220); srp-talker-loss/srp.talker_declare.s8.if0 -1.859 ms (188.478 -> 186.619, budget 220); srp-talker-held/srp.talker_declare.s8.if0 -1.859 ms (188.478 -> 186.619, budget 220)
passes with another instruction count: 32 of 36 (srp-talker-held/srp-talker-held.held.acmp.if0 33543 -> 31118; srp-talker-held/srp-talker-held.held.adp.if0 32851 -> 33057; srp-talker-held/srp-talker-held.held.aecp.if0 29116 -> 29323; srp-talker-held/srp-talker-held.held.maap.if0 33543 -> 31118; srp-talker-held/srp.listener_ready.s0.if0 9616 -> 9620; srp-talker-held/srp.listener_ready.s1.if0 9111 -> 9788; srp-talker-held/srp.listener_ready.s2.if0 9977 -> 9969; srp-talker-held/srp.listener_ready.s3.if0 10190 -> 10170; srp-talker-held/srp.listener_ready.s4.if0 9650 -> 9632; srp-talker-held/srp.listener_ready.s5.if0 9831 -> 9825; srp-talker-held/srp.listener_ready.s6.if0 10713 -> 10697; srp-talker-held/srp.listener_ready.s7.if0 10193 -> 10183)

## Every graded probe, declaring-outputs (probe_cmp.py)
| Probe | base ms | head ms | head-base | budget ms | verdict base / head | pass instructions base / head |
|---|---:|---:|---:|---:|---|---|
| `aecp-outputs/aecp_outputs.declared.if0` | 1.448 | 1.468 | +0.021 | 20 | fits / fits | 9458 / 9458 |
| `aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o0.if0` | 0.302 | 0.264 | -0.037 | 20 | fits / fits | 6866 / 6866 |
| `aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o1.if0` | 0.327 | 0.291 | -0.036 | 20 | fits / fits | 6899 / 6902 |
| `aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o2.if0` | 0.287 | 0.249 | -0.038 | 20 | fits / fits | 6862 / 6865 |
| `aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o3.if0` | 0.328 | 0.289 | -0.038 | 20 | fits / fits | 6899 / 6902 |
| `aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o4.if0` | 0.328 | 0.289 | -0.039 | 20 | fits / fits | 6862 / 6862 |
| `aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o5.if0` | 0.285 | 0.249 | -0.035 | 20 | fits / fits | 6899 / 6902 |
| `aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o6.if0` | 0.330 | 0.292 | -0.038 | 20 | fits / fits | 6862 / 6862 |
| `aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o7.if0` | 0.285 | 0.248 | -0.036 | 20 | fits / fits | 6899 / 6902 |
| `aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o8.if0` | 0.297 | 0.260 | -0.037 | 20 | fits / fits | 6862 / 6865 |
| `aecp-outputs/aecp_outputs.held_get_stream_info.if0` | 4.085 | 4.162 | +0.077 | 20 | fits / fits | 5958 / 5967 |
| `aecp-outputs/aecp_outputs.held_set_stream_info.if0` | 9.122 | 9.198 | +0.077 | 20 | fits / fits | 5958 / 5967 |
| `aecp-outputs/aecp_outputs.set_stream_info.set_stream_info_locked.if0` | 0.135 | 0.302 | +0.167 | 20 | fits / fits | 6881 / 6881 |
| `aecp-outputs/aecp_outputs.set_stream_info.set_stream_info_stream_id.if0` | 0.329 | 0.290 | -0.039 | 20 | fits / fits | 6883 / 6883 |

probes: base 14, head 14, paired 14, only base 0, only head 0
verdicts changed: 0
misses each side: base 0, head 0
largest differences: aecp-outputs/aecp_outputs.set_stream_info.set_stream_info_locked.if0 +0.167 ms (0.135 -> 0.302, budget 20); aecp-outputs/aecp_outputs.held_get_stream_info.if0 +0.077 ms (4.085 -> 4.162, budget 20); aecp-outputs/aecp_outputs.held_set_stream_info.if0 +0.077 ms (9.122 -> 9.198, budget 20); aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o4.if0 -0.039 ms (0.328 -> 0.289, budget 20); aecp-outputs/aecp_outputs.set_stream_info.set_stream_info_stream_id.if0 -0.039 ms (0.329 -> 0.290, budget 20)
passes with another instruction count: 8 of 14 (aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o1.if0 6899 -> 6902; aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o2.if0 6862 -> 6865; aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o3.if0 6899 -> 6902; aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o5.if0 6899 -> 6902; aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o7.if0 6899 -> 6902; aecp-outputs/aecp_outputs.get_stream_info.get_stream_info_o8.if0 6862 -> 6865; aecp-outputs/aecp_outputs.held_get_stream_info.if0 5958 -> 5967; aecp-outputs/aecp_outputs.held_set_stream_info.if0 5958 -> 5967)

## Passes given whole and the pass classes, by group (passes_cmp.py; CPU cycles, joins in ms)
| Group | build-one heaviest (limit), base / head | build | step | longest build slice | joins ms (base) | joins ms (head) | late joins b/h | over the share b/h | findings b/h |
|---|---|---|---|---|---|---|---|---|---|
| `aecp` | 27267 / 28013 (147500) | 0 / 0 | 0 / 0 | 27267 / 28013 | 188.045 to 189.988 | 188.064 to 190.001 | 0 / 0 | 0 / 0 | 0 / 0 |
| `aecp-outputs` | 35416 / 35943 (147500) | 0 / 0 | 0 / 0 | 35416 / 35943 | 187.978 to 190.023 | 187.996 to 190.045 | 0 / 0 | 0 / 0 | 0 / 0 |
| `backlog-owed` | 27267 / 28013 (147500) | 0 / 0 | 0 / 0 | 27267 / 28013 | 188.045 to 189.988 | 188.064 to 190.001 | 0 / 0 | 0 / 0 | 0 / 0 |
| `datapath-events` | 27267 / 28013 (147500) | 0 / 0 | 0 / 0 | 27267 / 28013 | 188.045 to 189.988 | 188.064 to 190.001 | 0 / 0 | 0 / 0 | 0 / 0 |
| `srp` | 44816 / 45643 (147500) | 0 / 0 | 0 / 0 | 44816 / 45643 | 188.045 to 189.988 | 188.064 to 190.001 | 0 / 0 | 0 / 0 | 0 / 0 |
| `srp-talker-held` | 125209 / 126644 (147500) | 0 / 0 | 0 / 0 | 125209 / 126644 | 187.376 to 190.201 | 187.201 to 190.403 | 0 / 0 | 0 / 0 | 0 / 0 |
| `srp-talker-loss` | 85936 / 86360 (147500) | 0 / 0 | 0 / 0 | 85936 / 86360 | 187.376 to 190.425 | 187.201 to 190.561 | 0 / 0 | 0 / 0 | 0 / 0 |

head findings over all groups: 0

## Every stated cost the tree makes of each measured cost: the most CPU cycles each side, the head's figure by the rule (cycles / 100 x 1.05, rounded up to 5 us), its statement (survey_point4.py, statements.py)
| Cost (8x8/1if) | Base cycles | Head cycles | Head rule, us | Stated, us | Head verdict | Statement; where (head) |
|---|---:|---:|---:|---:|---|---|
| base | 26,911 | 26,518 | 280 | 300 | within | load_grade.stated(8x8/1if) GRADED base; held/srp-talker-held |
| base | 26,911 | 26,518 | 280 | 300 | within | load_grade.stated(8x8/1if) STATED_US base; held/srp-talker-held |
| base | 26,911 | 26,518 | 280 | 300 | within | poll_grade.STATED_US[(1, 9, 9)] base; held/srp-talker-held |
| build | 0 | 0 | 0 | 1795 | within | load_grade.stated(8x8/1if) GRADED build; declaring-outputs/aecp-outputs |
| build | 0 | 0 | 0 | 1795 | within | load_grade.stated(8x8/1if) STATED_US build; declaring-outputs/aecp-outputs |
| build | 0 | 0 | 0 | 1795 | within | whole_grade.stated_us((1, 9, 9)) build (ctrl_loop.h); declaring-outputs/aecp-outputs |
| build_one | 125,209 | 126,644 | 1330 | 1475 | within | load_grade.stated(8x8/1if) GRADED build_one; held/srp-talker-held |
| build_one | 125,209 | 126,644 | 1330 | 1475 | within | load_grade.stated(8x8/1if) STATED_US build_one; held/srp-talker-held |
| build_one | 125,209 | 126,644 | 1330 | 1475 | within | whole_grade.stated_us((1, 9, 9)) build-one (ctrl_loop.h); held/srp-talker-held |
| centisecond | 27,966 | 24,469 | 260 | 510 | within | load_grade.stated(8x8/1if) GRADED centisecond; held/srp-talker-held.log |
| centisecond | 27,966 | 24,469 | 260 | 510 | within | load_grade.stated(8x8/1if) STATED_US centisecond; held/srp-talker-held.log |
| event.ADP | 6,788 | 6,815 | 75 | 120 | within | load_grade.stated(8x8/1if) GRADED event.ADP; TIMER#0, 14 taken |
| event.ADP | 6,788 | 6,815 | 75 | 120 | within | load_grade.stated(8x8/1if) STATED_US event.ADP; TIMER#0, 14 taken |
| event.AECP | 5,633 | 5,357 | 60 | 120 | within | load_grade.stated(8x8/1if) GRADED event.AECP; TIMER#3, 12636 taken |
| event.AECP | 5,633 | 5,357 | 60 | 120 | within | load_grade.stated(8x8/1if) STATED_US event.AECP; TIMER#3, 12636 taken |
| event.AMAP_LIVE_WRITE | 1,494 | 1,526 | 20 | 30 | within | rows_tiers.DATAPATH_US[8x8/2if] AMAP_LIVE_WRITE; datapath-events.log@71824947 |
| event.AS_PATH_CHANGED | 1,866 | 2,129 | 25 | 40 | within | rows_tiers.DATAPATH_US[8x8/2if] AS_PATH_CHANGED; datapath-events.log@74620393 |
| event.AVB_INFO_CHANGED | 2,455 | 2,467 | 30 | 40 | within | rows_tiers.DATAPATH_US[8x8/2if] AVB_INFO_CHANGED; datapath-events.log@71410483 |
| event.GM | 2,427 | 2,437 | 30 | 320 | within | load_grade.stated(8x8/1if) GRADED event.GM; GM, 15 taken |
| event.GM | 2,427 | 2,437 | 30 | 320 | within | load_grade.stated(8x8/1if) STATED_US event.GM; GM, 15 taken |
| event.LINK | 15,999 | 15,761 | 170 | 300 | within | rows_grade.ROW_COSTS[8x8/2if] event.LINK; LINK, 7 taken |
| event.MAAP | 18,815 | 18,710 | 200 | 225 | within | load_grade.stated(8x8/1if) GRADED event.MAAP; TIMER#2, 20 taken |
| event.MAAP | 18,815 | 18,710 | 200 | 225 | within | load_grade.stated(8x8/1if) STATED_US event.MAAP; TIMER#2, 20 taken |
| event.TICK | 2,385 | 2,362 | 25 | 85 | within | load_grade.stated(8x8/1if) GRADED event.TICK; TICK, 3556 taken |
| event.TICK | 2,385 | 2,362 | 25 | 55 | within | load_grade.stated(8x8/1if) STATED_US event.TICK; TICK, 3556 taken |
| events_none | 2,809 | 2,895 | 35 | 45 | within | load_grade.stated(8x8/1if) GRADED events_none; held/srp-talker-held.log |
| events_none | 2,809 | 2,895 | 35 | 45 | within | load_grade.stated(8x8/1if) STATED_US events_none; held/srp-talker-held.log |
| item.acmp | 6,710 | 6,313 | 70 | 80 | within | load_grade.stated(8x8/1if) GRADED item.acmp; none/backlog-owed |
| item.acmp | 6,710 | 6,313 | 70 | 80 | within | load_grade.stated(8x8/1if) STATED_US item.acmp; none/backlog-owed |
| item.acmp | 6,710 | 6,313 | 70 | 80 | within | poll_grade.STATED_US[(1, 9, 9)] acmp; none/backlog-owed |
| item.acmp_declined | 2,386 | 2,386 | 30 | 30 | within | load_grade.stated(8x8/1if) GRADED item.acmp_declined; none/backlog-owed |
| item.acmp_declined | 2,386 | 2,386 | 30 | 30 | within | load_grade.stated(8x8/1if) STATED_US item.acmp_declined; none/backlog-owed |
| item.acmp_declined | 2,386 | 2,386 | 30 | 30 | within | poll_grade.STATED_US[(1, 9, 9)] acmp_declined; none/backlog-owed |
| item.acmp_kept | 8,838 | 8,937 | 95 | 440 | within | load_grade.stated(8x8/1if) STATED_US record.acmp; none/backlog-owed |
| item.aecp | 12,898 | 12,796 | 135 | 145 | within | poll_grade.STATED_US[(1, 9, 9)] aecp; declaring-outputs/aecp-outputs |
| item.aecp.notice | 12,898 | 12,796 | 135 | 275 | within | load_grade.stated(8x8/1if) GRADED item.aecp.notice; declaring-outputs/aecp-outputs (16 frame(s)) |
| item.aecp.notice | 12,898 | 12,796 | 135 | 275 | within | load_grade.stated(8x8/1if) STATED_US item.aecp.notice; declaring-outputs/aecp-outputs (16 frame(s)) |
| item.aecp.response | 2,215 | 2,149 | 25 | 65 | within | load_grade.stated(8x8/1if) GRADED item.aecp.response; none/backlog-owed (1 frame(s)) |
| item.aecp.response | 2,215 | 2,149 | 25 | 65 | within | load_grade.stated(8x8/1if) STATED_US item.aecp.response; none/backlog-owed (1 frame(s)) |
| item.aecp_long | 0 | 0 | 0 | 320 | within | poll_grade.STATED_US[(1, 9, 9)] aecp_long; declaring-outputs/aecp-outputs |
| item.mrpdu | 0 | 0 | 0 | 1475 | within | load_grade.stated(8x8/1if) GRADED item.mrpdu; declaring-outputs/aecp-outputs |
| item.mrpdu | 0 | 0 | 0 | 1475 | within | load_grade.stated(8x8/1if) STATED_US item.mrpdu; declaring-outputs/aecp-outputs |
| item.mrpdu | 0 | 0 | 0 | 1475 | within | poll_grade.STATED_US[(1, 9, 9)] mrpdu; declaring-outputs/aecp-outputs |
| item.rebuild | 0 | 0 | 0 | 590 | within | poll_grade.STATED_US[(1, 9, 9)] rebuild; declaring-outputs/aecp-outputs |
| item.reclaim | 1,044 | 1,000 | 15 | 40 | within | load_grade.stated(8x8/1if) GRADED item.reclaim; none/srp |
| item.reclaim | 1,044 | 1,000 | 15 | 40 | within | load_grade.stated(8x8/1if) STATED_US item.reclaim; none/srp |
| item.reclaim | 1,044 | 1,000 | 15 | 40 | within | poll_grade.STATED_US[(1, 9, 9)] reclaim; none/srp |
| item.record | 35,044 | 35,177 | 370 | 375 | within | poll_grade.STATED_US[(1, 9, 9)] retained; held/srp-talker-held |
| item.retained | 0 | 0 | 0 | 375 | within | load_grade.stated(8x8/1if) GRADED item.retained; declaring-outputs/aecp-outputs |
| item.retained | 0 | 0 | 0 | 375 | within | load_grade.stated(8x8/1if) STATED_US item.retained; declaring-outputs/aecp-outputs |
| item.retained | 0 | 0 | 0 | 375 | within | poll_grade.STATED_US[(1, 9, 9)] retained; declaring-outputs/aecp-outputs |
| item.walk | 3,300 | 3,137 | 35 | 120 | within | load_grade.stated(8x8/1if) GRADED item.walk; held/srp-talker-held |
| item.walk | 3,300 | 3,137 | 35 | 120 | within | load_grade.stated(8x8/1if) STATED_US item.walk; held/srp-talker-held |
| item.walk | 3,300 | 3,137 | 35 | 120 | within | poll_grade.STATED_US[(1, 9, 9)] walk; held/srp-talker-held |
| item.withdraw | 0 | 0 | 0 | 110 | within | poll_grade.STATED_US[(1, 9, 9)] withdraw; declaring-outputs/aecp-outputs |
| record.acmp | 11,233 | 11,206 | 120 | 305 | within | load_grade.stated(8x8/1if) GRADED record.acmp; declaring-outputs/aecp-outputs.log |
| record.acmp | 11,233 | 11,206 | 120 | 440 | within | load_grade.stated(8x8/1if) STATED_US record.acmp; declaring-outputs/aecp-outputs.log |
| record.adp | 1,618 | 1,638 | 20 | 135 | within | load_grade.stated(8x8/1if) GRADED record.adp; held/srp-talker-held.log |
| record.adp | 1,618 | 1,638 | 20 | 240 | within | load_grade.stated(8x8/1if) STATED_US record.adp; held/srp-talker-held.log |
| record.maap | 17,259 | 17,014 | 180 | 185 | within | load_grade.stated(8x8/1if) GRADED record.maap; loss/srp-talker-loss.log |
| record.maap | 17,259 | 17,014 | 180 | 185 | within | load_grade.stated(8x8/1if) STATED_US record.maap; loss/srp-talker-loss.log |
| record.srp | 35,273 | 35,507 | 375 | 375 | within | load_grade.stated(8x8/1if) GRADED record.srp; held/srp-talker-held.log |
| record.srp | 35,273 | 35,507 | 375 | 375 | within | load_grade.stated(8x8/1if) STATED_US record.srp; held/srp-talker-held.log |
| step | 0 | 0 | 0 | 1030 | within | load_grade.stated(8x8/1if) GRADED step; declaring-outputs/aecp-outputs |
| step | 0 | 0 | 0 | 1030 | within | load_grade.stated(8x8/1if) STATED_US step; declaring-outputs/aecp-outputs |
| step | 0 | 0 | 0 | 975 | within | whole_grade.stated_us((1, 9, 9)) step (ctrl_loop.h); declaring-outputs/aecp-outputs |

66 head rows, 0 not within; 66 base rows

## The largest legal notice (compare-long)
# aecp-largest-notice: its notices against the largest legal notice's statement at 8x8/1if (poll_grade aecp_long)
# 0 exceeded
