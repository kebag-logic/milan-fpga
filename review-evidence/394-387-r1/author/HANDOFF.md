[A375] Bench handoff

Refs #394 acceptance 2, e1 only. Refs #387 acceptance 4.

State: ten cycles complete; full restore PASS; all nine assigned gates rc 0. No bench lock held. Local commit fddc58e43733afd90d6222e58999e0f416a30df9; not pushed. Independent review pending.
Branch: 394-387-e1-cycles
Base: 2a2a7bb655e528edc3087c88033cd3a47546feb4
Assignment: https://github.com/kebag-logic/milan-fpga/issues/394#issuecomment-5858215210

Identity: PASS, UART CRCs and AECP descriptors match assigned image. OUT4 proof: PASS in cycle 1. Switch traffic ceased, the controller carrier dropped, DUT epoch stayed 1 with continuous console replies, peer ADP available_index continued, and only OUT4 changed.
Original: all seven outlets ON; all 18 stream states unbound; DUT clock source 0 (INTERNAL). Peer clock source 0 and rate 96000 Hz. Measured bindings: DUT CRF output 1 to peer input 8, peer CRF output 2 to DUT input 1. Both advertise the same CRF format. DUT CRF source 1 was selected. Cycle 1 proved OUT4 before later cycles.
Restore: all 18 queried stream states are unbound; DUT source 0 (INTERNAL) restored; all original settings and descriptors compare equal. All seven outlets ON, matching the start. Final UART sync=1, asCapable=1, tu=0, reset epoch 1, CRF talker control 0x3, media servo IDLE.

| Cycle | Off/on UTC (recorder clock) | Link down/up | Counter deltas | Recovery | Streams | Media step/relock | Result |
|---|---|---|---|---|---|---|---|
| 1 | 17:50:07.940 / 17:50:29.033 | DUT status flat; controller edge retained | LINK_UP/DOWN +0/+0; MEDIA_LOCKED/UNLOCKED +1/+1 | gPTP 1.564 s | automatic both ways | step to locked media 8.003-8.285 s | #394 FAIL; #387 PASS (CRF) |
| 2 | 17:52:50.516 / 17:53:11.410 | DUT status flat; controller edge retained | LINK_UP/DOWN +0/+0; MEDIA_LOCKED/UNLOCKED +1/+1 | gPTP 0.680 s | automatic both ways | step to locked media 10.254-10.536 s | #394 FAIL; #387 PASS (CRF) |
| 3 | 17:54:26.337 / 17:54:47.300 | DUT status flat; controller edge retained | LINK_UP/DOWN +0/+0; MEDIA_LOCKED/UNLOCKED +1/+1 | gPTP 1.622 s | automatic both ways | step to locked media 7.503-7.784 s | #394 FAIL; #387 PASS (CRF) |
| 4 | 17:56:02.290 / 17:56:23.208 | DUT status flat; controller edge retained | LINK_UP/DOWN +0/+0; MEDIA_LOCKED/UNLOCKED +1/+1 | gPTP 1.815 s | automatic both ways | step to locked media 7.503-7.785 s | #394 FAIL; #387 PASS (CRF) |
| 5 | 17:57:38.299 / 17:57:59.203 | DUT status flat; controller edge retained | LINK_UP/DOWN +0/+0; MEDIA_LOCKED/UNLOCKED +1/+1 | gPTP 0.632 s | automatic both ways | step to locked media 11.254-11.536 s | #394 FAIL; #387 PASS (CRF) |
| 6 | 17:59:14.273 / 17:59:35.217 | DUT status flat; controller edge retained | LINK_UP/DOWN +0/+0; MEDIA_LOCKED/UNLOCKED +1/+1 | gPTP 0.638 s | automatic both ways | step to locked media 10.754-11.036 s | #394 FAIL; #387 PASS (CRF) |
| 7 | 18:00:50.615 / 18:01:11.669 | DUT status flat; controller edge retained | LINK_UP/DOWN +0/+0; MEDIA_LOCKED/UNLOCKED +1/+1 | gPTP 0.441 s | automatic both ways | step to locked media 8.253-8.535 s | #394 FAIL; #387 PASS (CRF) |
| 8 | 18:02:26.388 / 18:02:47.440 | DUT status flat; controller edge retained | LINK_UP/DOWN +0/+0; MEDIA_LOCKED/UNLOCKED +1/+1 | gPTP 0.474 s | automatic both ways | step to locked media 12.254-12.536 s | #394 FAIL; #387 PASS (CRF) |
| 9 | 18:04:02.319 / 18:04:23.336 | DUT status flat; controller edge retained | LINK_UP/DOWN +0/+0; MEDIA_LOCKED/UNLOCKED +1/+1 | gPTP 1.817 s | automatic both ways | step to locked media 8.503-8.785 s | #394 FAIL; #387 PASS (CRF) |
| 10 | 18:05:38.260 / 18:05:59.183 | DUT status flat; controller edge retained | LINK_UP/DOWN +0/+0; MEDIA_LOCKED/UNLOCKED +1/+1 | gPTP 0.680 s | automatic both ways | step to locked media 8.753-9.035 s | #394 FAIL; #387 PASS (CRF) |

#394 acceptance 2: FAIL, LINK_UP and LINK_DOWN remain flat in all ten cycles; recovery succeeded automatically in all ten.
#387 acceptance 4: PASS for the assigned CRF recovery measurement in all ten cycles; one further restart per talker, step and relock brackets retained. AAF render timing was not measured.
Validation: all nine assigned gates rc 0 at fddc58e43733afd90d6222e58999e0f416a30df9; see gate-N.txt, gates.json and validation-context.json. The committed diff also passes whitespace validation. Only docs/findings/394_387_E1_SWITCH_CYCLES.md changed.
Artifacts: MANIFEST.sha256 covers every packet file except itself. RAW-ARTIFACTS.json indexes 119 raw files (63,928,791 bytes), including large captures under /tmp/a375 and the original start/end census. Per-cycle raw-artifacts.json files pin the original inputs. No package, environment, dependency tree, capture binary or file over 200 KB is retained in this packet.

Capture prerequisite: the first preflight found the approved tap without a matching driver. No outlet action occurred. A temporary rebuild restored the same interface; the successful baseline preceded all ten cycles. The driver was unloaded and its temporary build removed during restore. See capture-prerequisite.txt and capture-cleanup.txt.

Timing limits: no DUT physical link edge was observable. Controller carrier is a different switch port. Cycle 1 carrier loss was observed late because queries shared the sampler. Final timing uses uniform analysis; console sampling is 250 ms, controller polling is coarser, and cross-host/USB uncertainty is retained. First PDUs followed wire return by 5.07-14.00 s; this does not establish the exact #75 reconnect interval.

Media limits: observed wire mr changed twice per cycle on DUT output and stayed unchanged on peer output. Hidden toggles during a capture gap cannot be counted. MEDIA_RESET resets at STREAM_START, so net endpoint deltas do not describe its trajectory. The findings table preserves each observed sequence.

No STOP condition occurred. No DUT flash, reset, reboot or power cycle was performed. Only OUT4 was cycled, ten times. No push, PR operation or merge was performed.

REVIEW READY posted: https://github.com/kebag-logic/milan-fpga/issues/394#issuecomment-5858459678
