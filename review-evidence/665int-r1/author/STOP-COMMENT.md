[A582] STOP
Head: 79efa393ccb92dd80f4ed219a932a1e5c3cae52d
Branch: 665-int-split. Resumed round 1d; worktree clean, pins unchanged.

Commits on 7c1b52be: 780a199c (canonical SRP comparator from this round's interrupted session, reviewed and kept) and 79efa393 (a separate duplicated-declaration plant). Per ruling 6087654804 the comparator sorts once within each transmit opportunity, keeps multiplicity and compares opportunities in order. Its self-test catches 18 plants; the order-only swap and packing-only controls pass. Three comparator mutations (dedupe, unordered opportunities, no sort) are caught. Existing engine-level captures compare equal: bench, 3 opportunities x 2 declarations; 8x8 at two firmware interfaces, 3 x 9.

**Decision 1 (blocking): fabric ADP/ACMP/SRP cannot be removed while fabric AECP stays, at processor pin 2ad2f845.** `protocol_processor_top.sv` instantiates ADP (:1918), ACMP admission/listener/talker/binding store (:2070, :2100, :2231, :2741), MRP strip and SRP (:2441, :2494) and its MAAP (:2341) unconditionally beside AECP and its notifier (:3733, :3957). Its only engine-shaping parameter is EN_IDENTIFY_NOTIF_P (:207). P-EN-SRP-ENGINE is specified (processor docs/architecture/01_overview.md:199) but has no RTL parameter. `hdl/milan/KL_pp_shadow.sv:22` instantiates the top unconditionally. Fabric AECP reads those engines: STREAM_INFO triggers (:3494-3509 into :3993) and GET_STREAM_INFO answers (`milan_datapath.sv:4912`). Only parent KL_maap (`milan_datapath.sv:7168`) is removable here.
1. Full split after F5 (#700) merges: omit KL_pp_shadow and KL_maap; F0-F5 own all five protocols; M0s's partial route folds into the complete-split route. Recommended (L2's complete flip, MARK_II_AREA_PLAN.md:425).
2. Processor placement parameters first (processor lane, pin adoption), with faces for the state and triggers fabric AECP reads. Needed for any shipped mixed placement (ARCHITECTURE_HW_SW_SPLIT.md:34, :36); slowest.
3. Keep the processor whole, isolated to AECP frames: no removal or area credit, and fabric AECP would report idle fabric ACMP/SRP state (contradicts :36).
4. A parent AECP-only fork of the processor top. Not recommended.

**Decision 2 (blocking under any option): no firmware-to-fabric publication.** Fabric consumers read the processor's class-D outputs: talker DA gate (`milan_datapath.sv:5335`), listener accept and bound stream_id (:5349, :5399), SRP stream gate, idle slope and Domain adoption (:7265-7307), the GET_STREAM_INFO face (:4912-5182). The mailbox contract has no such face. F4's licence port (`srp_mbx.h:62`) and ACMP's bindings have no fabric sink; only MAAP writes existing CSRs (`maap_csr.c`).
(a) A publication block inside the mailbox window, applied before the response that promises it (ARCHITECTURE_HW_SW_SPLIT.md:55). Recommended, in F-INT or a lane before it.
(b) Existing CSRs behind fallback multiplexers: no new register, but changed meaning in the split build.
(c) A protocol-only split image for now (media gates closed), with publication a separate lane before the flip.

**Item 3 (please confirm):** ARCHITECTURE_HW_SW_SPLIT.md:228 gives split images major 3; :237 lands the version chain with the flip PR. Recommended: VERSION unchanged in both placements in F-INT.

Implemented integration-ledger rows: 0. Gates run: the comparator self-test and mutation driver, the Python idiom, hygiene and documentation checks, and the whitespace check, all rc 0. No build switch, datapath change, image, simulation, linked size or resource figure is claimed. No default, map, pin or generated source changed. HANDOFF.md and PR-BODY.md are updated, with file:line anchors, plants, coverage/gate tables and receipts. No push, PR operation, merge or device access. Independent review pending.
