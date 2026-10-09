[A572] REVIEW READY

Head: `1e68d1b62ef2facdf0e8dbad28a202297d433c61`
Branch: `665-f5-aecp`, from `5603c353137e90c1fa95429f6d00ef7a2298d9ee`. Local commits only; no push or PR mutation.

Implemented the portable AECP owner, generated-image adapter, mailbox adapter and opt-in application/saved-state composition. READ_DESCRIPTOR serves every generated descriptor. Mandatory Milan AEM/MVU commands, per-interface registrations/liveness, notifications, deferred START/STOP, final-word completion accounting, #653 response-before-MEDIA_UNLOCKED ordering and #637 atomic saved-map restore/format rollback are covered. Solicited IDENTIFY_NOTIFICATION preserves its descriptor fields with the IEEE 7.4.39.2 BAD_ARGUMENTS response. Default all-fabric behavior, shipping image, configurations, RTL and register maps are unchanged.

Validation, all completed command families rc 0:
- Full firmware bank at one/two interfaces and all five generated image shapes; composed sanitizer arm 62/62 tests. There are 66 distinct new AECP tests, all named by caught source defects: 59/59 plants. The diagnostic grader rejects crashes, wrong-test failures and missing assertion tokens.
- Firmware coverage generator/check: eight new production C units at raw 100% lines and branches, no new exclusion; full 30-file ratchet passes. Coverage, tally and RV32 reader self-tests pass.
- Unchanged regression tables: 471 control, 169 SRP, 68 interface-sensitive SRP and 109 saved-state source plants all caught. Saved-state normal bank: 435 tests across five shapes. Two dependency-pin controls pass.
- `make -C tb/verilator/mbx`: both buses, one/two interfaces, firmware co-simulation and five quick plants pass. `python3 -B sw/mailbox/gen_mailbox.py --check` passes. The scratch make driver limits nested builds to two with eight compile jobs each.
- Builder bank, real-RV32 profile gate and absent-compiler audit pass. Long gates were divided only across independent fixture tables/plants; complete original tables and selected slices were reconciled with no omission or duplicate. Initial 560-second timeouts are not counted as successes. The existing physical calibration arm is explicitly NOT RUN: its report is absent and hardware access was prohibited.
- All 73 extracted documentation workflow commands, final touched-file checks, no-git export checks, wire-accountability controls and the offline local-replica self-test pass. The latter ran inside a disposable job container, without host socket or forwarded credentials.

The wire differential passes 123 observations against processor `2ad2f845dd583f8310075fa2380cb60a04fd091a` and 128 on each ingress against the merged processor #69 revision `c9f74b6866a63dd3c0e4534724bfc07a86ad142b`. Each ingress covers 42 descriptors, 31 AEM command codes including refusal probes, three MVU commands and 17 notification types. Six observation plants per ingress are caught. Reference RTL is unchanged; only external bench providers and generated verification inputs follow the canonical shape. Exact recorded differences:
- System-ID SET/GET succeeds only in the core: Milan 5.4.4.2/3.
- First default-valued format/rate SET establishes a saved override and notifies only in the core; repeats do not: Milan 5.4.5.2.
- Bound START/STOP additionally emits GET_STREAM_INFO only in the core: Milan 5.4.5.2 Table 5.22; both emit the IEEE 7.5.2 command notification.
- Unlock notification flags differ, with owner zero in both: permitted alternatives in IEEE 7.4.2.1.

Service checks use original arrival/due times, counted mailbox accesses and explicit desk CPU/observation allowances. At one/two interfaces they cover every command/refusal, maximum bodies, fanout, stalls, controller timers and lock expiry. Maximum bounds are 1.0770 ms for command bodies, 1.1573 ms for full fanout, 2.0069 ms with a one-millisecond TX stall, and 9.0061 ms for deferred failure. These meet the 10 ms service target and the IEEE 9.3.2.6 / Milan 5.4.3.4 240 ms response limit under the stated assumptions. The endpoint is TX_HEAD acceptance; physical timing and complete call-chain stack calibration are not claimed.

| Shape / interfaces | text | rodata | data | bss | stack | Linked span | Delta from base F4 entry |
|---|---:|---:|---:|---:|---:|---:|---:|
| Shipping / 1 | 81948 | 11950 | 56 | 36908 | 8192 | 139072 | 58704 |
| Shipping / 2 | 83236 | 11950 | 56 | 48276 | 8192 | 151728 | 58704 |
| Largest / 1 | 81996 | 25158 | 448 | 76428 | 8192 | 192240 | 97072 |
| Largest / 2 | 83372 | 25158 | 448 | 102556 | 8192 | 219744 | 97072 |

The delta includes the real F1 store now retained by the composition. Against the earlier F4/F1 preflight cited in the budget ruling, deltas are 44384 bytes for shipping and 72384 for largest. All four links pass RV32I ILP32 ABI, no-heap and retained-symbol checks. Largest/two interfaces is below 224000 bytes and 224 KiB. Nominal RAMB36 counts at 4608 bytes/tile are 31, 33, 42 and 48; 32-bit data packing would require 34, 38, 47 and 54, so routed packing remains owed.

Largest BSS consumers and unimplemented reduction options: arena 48064 (audit MRP capacity peaks), saved-state staging 13264 (consider streamed groups only with atomicity proof), mutable descriptor values 11753 (sparse overlays), application state 9640 (queue/capacity audit), SRP state 5864 (deduplicate state/capacity audit). No non-AECP reduction was made.

Handoff packet `665f5-a572` contains HANDOFF.md with every changed file:line, all 66 test/defect mappings, coverage and gate tables; template PR-BODY.md; reproduction recipes; complete partition receipts; four-case sizes/static pools; per-path timing; and SHA-256/size manifests. Large artifacts remain in scratch. The fixture/regression compiler and separately verified SDK are distinguished in the packet. Memory samples exceeded the requested 9 GB target, highest observed 10.24 GB; clean file cache was reclaimed, and this execution deviation is recorded.

Open integration/review obligations: processor #73's future command model, volatile system ID pending its saved-record decision, physical observer wiring, target timing/stack calibration, and the default flip's routed resource/10% reserve proof. The image is a complete reachable size/ABI fixture with explicit unavailable physical observers, not a board image. Assigned independent reviewers remain [R564] and [R565]; no review verdict, hosted exact-head status, candidate merge or post-merge containment is claimed.
