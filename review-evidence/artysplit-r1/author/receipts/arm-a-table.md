### arty-1x1

Clock: CPU 80 MHz on sys, the product's split CPU clock, bus 80 MHz.

4 of 22 paths and 7 of 35 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.337 (3.612) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.283 (2.596) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.742 (4.052) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.578 (3.894) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.595 (1.890) | fits | 0 aecp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 3.708 (4.291) | fits | 7 adp | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.792 (62.957) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.334 (63.502) | MISS ceiling | 10 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-adp.service.acmp.first.if0` (backlog-adp) | 2.919 | fits | 0 acmp | 2 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.104 | MISS ceiling | 10 acmp | 2 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp.service.adp.first.if0` (backlog-adp) | 2.908 | fits | 0 adp | 2 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 4.224 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 2.343 | fits | 0 aecp | 2 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.887 | MISS ceiling | 15 aecp | 2 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp.service.maap.first.if0` (backlog-adp) | 2.952 | fits | 0 maap | 2 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 4.270 | fits | 6 maap | 2 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 5.200 | fits | 0 srp | 2 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 11.005 | fits | 31 srp | 2 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.848 (0.987) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.424 (0.424) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.154 (0.154) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.869 (0.966) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp | 0 | 11.431 | 13 | 118,770 (1.485) | yes | - |
| backlog-owed | 0 | 63.785 | 27 | 117,142 (1.464) | yes | - |

Composed maximum over 2 of 4 backlog windows, a partial figure (backlog, backlog-adp-refill not run): 118,770 CPU cycles (1.485 ms), backlog-adp.
Over the windows that released their whole load only: 118,770 (1.485 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 160,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp | 290 | 0 | 49,832 (0.623) | fits |
| backlog-adp | 317 | 0 | 118,770 (1.485) | fits |
| backlog-owed | 313 | 0 | 117,142 (1.464) | fits |
| aecp-largest-notice | 107 | 0 | 132,439 (1.655) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp | 271 | 14,928 (0.187) | 2,443 (0.031) |
| backlog-adp | 271 | 14,928 (0.187) | 2,443 (0.031) |
| backlog-owed | 276 | 14,928 (0.187) | 2,443 (0.031) |
| aecp-largest-notice | 78 | 14,896 (0.186) | 2,443 (0.031) |

Longest pass that carries a step: 14,928 CPU cycles (0.187 ms), srp; longest step: 2,443 (0.031 ms), srp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| startup declarations (LINK_UP) | `srp.startup.if0` | 69,543 | 0.869 | 20 | 20 | fits | 28,282 | 8 | 0.846 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 33,882 | 0.424 | 20 | 20 | fits | 33,948 | 12 | 0.888 |
| malformed MRPDU discard | `srp.malformed.if0` | 12,289 | 0.154 | 20 | 20 | fits | 12,355 | 12 | 0.653 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 67,841 | 0.848 | 220 | 220 | fits | 49,832 | 6 | 0.903 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 296,664 | 3.708 | 20 | 20 | fits | 105,894 | 200 | 0.260 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 232,626 | 2.908 | 20 | 200 | fits | 118,770 | 199 | 0.367 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 337,904 | 4.224 | 20 | 200 | fits | 105,894 | 200 | 0.260 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 233,550 | 2.919 | 20 | 20 | fits | 118,770 | 199 | 0.367 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 338,608 | 4.233 | 20 | 20 | fits | 105,894 | 200 | 0.260 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 118,420 | 1.480 | 20 | 24 | fits | 118,591 | 145 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 236,200 | 2.953 | 20 | 24 | fits | 118,770 | 199 | 0.367 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 236,134 | 2.952 | 20 | 50 | fits | 118,770 | 199 | 0.367 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 341,632 | 4.270 | 20 | 50 | fits | 105,894 | 200 | 0.260 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 416,037 | 5.200 | 20 | 20 | fits | 64,872 | 27 | 0.829 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 880,419 | 11.005 | 20 | 20 | fits | 25,340 | 12 | 0.813 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 5,023,391 | 62.792 | 20 | 20 | MISS ceiling | 10,955 | 13 | 0.429 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 5,034,290 | 62.929 | 20 | 20 | MISS ceiling | 10,975 | 13 | 0.412 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 5,045,192 | 63.065 | 20 | 20 | MISS ceiling | 10,959 | 13 | 0.412 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 5,055,973 | 63.200 | 20 | 20 | MISS ceiling | 10,857 | 13 | 0.429 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 5,066,684 | 63.334 | 20 | 20 | MISS ceiling | 10,774 | 13 | 0.438 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 112,186 | 1.402 | 20 | 200 | fits | 113,436 | 237 | 0.230 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 111,570 | 1.395 | 20 | 200 | fits | 113,436 | 237 | 0.230 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 107,864 | 1.348 | 20 | 20 | fits | 113,436 | 237 | 0.230 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 4,968,299 | 62.104 | 20 | 20 | MISS ceiling | 20,809 | 15 | 0.667 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 187,413 | 2.343 | 20 | 24 | fits | 75,909 | 107 | 0.410 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 4,950,976 | 61.887 | 20 | 24 | MISS ceiling | 117,142 | 106 | 0.382 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 110,448 | 1.381 | 20 | 50 | fits | 113,436 | 237 | 0.230 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 110,052 | 1.376 | 20 | 50 | fits | 113,436 | 237 | 0.230 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 252,794 | 3.160 | 20 | 20 | fits | 66,899 | 62 | 0.732 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 705,164 | 8.815 | 20 | 20 | fits | 23,895 | 12 | 0.790 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 127,586 | 1.595 | 20 | 24 | fits | 132,439 | 136 | 0.309 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 266,935 | 3.337 | 20 | 24 | fits | 125,759 | 113 | 0.287 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 182,645 | 2.283 | 20 | 24 | fits | 34,060 | 17 | 0.659 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 299,332 | 3.742 | 20 | 24 | fits | 69,012 | 18 | 0.648 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 286,246 | 3.578 | 20 | 24 | fits | 81,598 | 17 | 0.657 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
