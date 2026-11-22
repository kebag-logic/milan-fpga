[A817] REVIEW READY
Commit: f863258d2a455697d85a5ab48813be8f0783e2d4 (branch `pf-969-1` on the flip PR's reviewed head `dd163e41`, PR #960; the PR's base is dev-soft-core)

Changed:
- Cause: ACMP binds SRP only once the probe succeeds (Milan v1.2 5.5.3.5.18 step 4), and the split SRP's receive filter (`srp_mbx.c` `interested_msrp`) refused every Talker of a StreamID no binding held, before lwSRP allocated anything. A Talker declared before the binding was never registered, and the talker stays quiet until a LeaveAll. The release processor keeps N port registrars for this (`KL_srp_listener_fsm.sv`, protocol-processor #212).
- Fix (split firmware; no mailbox-contract, lwSRP or RTL change): the filter keeps a Talker of a StreamID no binding holds, up to one per STREAM_INPUT of the shape (`keep_talker`). The kept count is made before a receive, outside lwSRP's callbacks (`count_kept`). A StreamID no binding holds keeps its latest kind (#925). The pool is unchanged: its fixed blocks fund the kept. No hot-list function moves or changes size.
- Ledger: the platform's 8x8 images at 58.5 (8x8/1if) and 63.5 (8x8/2if) RAMB36, 720 and 256 B of `rom` past 58.0 and 63.0, by the owner's rule of 2026-11-15 (debt owed to S14). The shipping 1x1/1if image is 45.5, 248 B past 45.0, within 56.

Validation:
- Failing first: the head's new and restated tests against the base's `srp_mbx.c`/`srp_mbx.h` fail at all 6 arms (srp_mbx.cpp at 1x1 and 8x8, one and two interfaces; platsinks at 8x8/1if and 1x1/1if) on every case the fix owns; the order that always worked, an ended registration and UNBIND_RX then BIND_RX pass at the base, as they should.
- `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard k/4`, k = 0..3, at `4c5018eb` (the firmware as final): exit 0 each. Shard 0: 88 arms PASS. Shard 1 (control campaign): 827 of 827 caught. Shard 2 (AECP): 385 caught, 0 escaped. Shard 3 (SRP campaigns): 565 caught, 0 escaped, the 11 new plants at each interface count and at 8x8/1if.
- `fw_coverage.py --check` at `4c5018eb`, `c6ef2329` and `f863258d`: PASS (40 files); `srp_mbx.c` 854/854 lines, 773/773 branches, recorded in the ratchet.
- `plat_ledger.py` and `test_ctrl_memory.py`: PASS, 0 findings; 1x1/1if 45.5, 1x1/2if 46, 8x8/1if 58.5, 8x8/2if 63.5 RAMB36.
- `make -C tb/verilator/milan_dp twin twin-plants` (and the maps legs): PASS, 0 findings, every plant refused.
- CPU budget, base against head on the groups that run the changed paths (srp, acmp-cmd, fixture, backlog, backlog-owed) at 1x1/1if and 8x8/1if: 0 refusals, 0 passes over the share, the same 7 owed backlog-owed misses as the base. `flip_grade.py --check` at both points, `load_grade.py --check` and `shape_costs.py --check`: PASS (last 127.31 of 130 ms, ACMP 29.06 of 30 ms, txL 47.88 of 49 ms; 8x8/1if THE TRANSMIT 76.81 against 77).
- Docs workflow, 103 commands, on a clean clone at `f863258d`: 99 PASS; the 4 rows that need the CI environment refuse here as on the base.
- Final head: the platform images' loadable bytes at `f863258d` equal those at `4c5018eb` at 1x1/1if and 8x8/1if; against the base no hot-list function moves or changes size.
- Release (all-fabric) export: bios.bin byte-identical to the base's.
- Routes at 1x1/1if and 8x8/1if (the gating recipe, ExtraPostPlacementOpt, images with the final head's rom and sram banks): #818's floor met at every signoff corner, worst WNS +0.437 / WHS +0.017 ns (1x1/1if, 81 of 135 BRAM tiles) and +0.058 / +0.036 ns (8x8/1if, 94.5 of 135); image identity passes. The base's images at the same directive had +0.131 and +0.176 ns.

Acceptance criteria:
- A binding made or restored while the Talker is registered declares its Listener within one transmit of the probe's success, after a power-on settle and after a bind while bound, at 8x8/1if and 1x1/1if, on every STREAM_INPUT: met on the host model. `test_plat_sinks.cpp` `Early.S13` (power cut, saved bindings restored, Talker declared before discovery and probe) and `Early.S14` (BIND_RX while bound) check the Listener in THE TRANSMIT's next MRPDU within a JoinTime; `srp_mbx.cpp` `SrpEarlyTalker` checks it on every input at 1x1 and 8x8, one and two interfaces. The bench re-run is the manager's.
- A host test covers both orders, with a planted defect for each: met. Registration then binding: `feedback-early-talker-ignored`, `feedback-early-rebind-ignored`, and the control campaign's `early-talker-ignored` (S13, S14 at both shapes). Binding then registration: `feedback-early-bound-first-sink-only`. Nine more plants cover the bound, the count and the latest kind.
- REGISTERING / REGISTERING_FAILED in GET_STREAM_INFO follow: met. S13 reads flags_ex bit 31 (REGISTERING) and flags 0x40 (REGISTERING_FAILED) for Advertise and Failed on every input; at the base both fail.

Open risks/questions:
- The kept Talkers are funded from the pool's 16 fixed medium blocks an interface, which hold the Domain's and the default VID's attributes; a static assertion holds `SRP_KEPT_TALKERS + 4 <= 16`. If those blocks ever hold something else, the bound must be revisited.
- Past the bound (one per STREAM_INPUT an interface), a Talker no binding holds is ignored as before, and a binding made later declares with the talker's next declaration (at most a LeaveAll period).
- Block RAM: the 8x8 platform images take half a tile more each (58.5 and 63.5 RAMB36), recorded as debt by the owner's rule of 2026-11-15; the 1x1/1if image is 45.5, within 56.
- The CPU budget was re-measured on the five groups that run the changed paths, not on every group: the host's load put a full re-measure past the day.
- The 8x8/1if route's slack is 0.118 ns thinner than the base's at the same directive (+0.058 against +0.176 ns), above the +0.030 ns floor; the other two directives were not run.
- The bench re-run after merge is the physical check; there was no bench access here.
