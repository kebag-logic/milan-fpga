[A820] REVIEW READY
Commit: `27495a06d5569336a098da20381ced3e331ba665` (`pf-970-1`, five commits on `dd163e41`). The tsn-c-stack gitlink is at `5d14a6d816a43a49299172a34e3eeaea44c267c6` (stack branch `970-first-advertise`, two commits on `715589c1`).

Cause: in the split firmware, an interface's first ENTITY_AVAILABLE after a link-up waits on its TMR_DELAY alone. The core drew that delay from 0 to 4,000 ms on LINK_UP (Milan v1.2 5.6.3.5.3) and from 0 to 2,000 ms at a startup with the link up (5.6.3.5.2). The host reproduction on the base stack measures the first ENTITY_AVAILABLE up to 3,990 ms after LINK_UP over 64 link-ups, and up to 1,981 ms after a startup. With a grandmaster change inside the delay it is up to 3,649 ms, and with one 4.5 s after the link-up, up to 3,364 ms. The first advertise does not wait for anything else:
- not asCapable, which the firmware never reads;
- not the grandmaster: a GM_CHANGE in DELAY is ignored (Table 5.51), and the frame samples the grandmaster when it is built (IEEE 1722.1-2021 6.2.2.16);
- not a settle timer or a debounce in the adapter;
- not the loop's passes, which take milliseconds;
- not the PHY poll, which publishes within its 125 ms period.

Changed:
- tsn-c-stack: an interface leaving DOWN draws its delay from 0 to 500 ms. `ADP_DELAY_STARTUP_MAX_MS` goes from 2000 to 500, and the new `ADP_DRAW_LINK_UP` kind uses `ADP_DELAY_LINK_UP_MAX_MS` 500. Both are within Milan's ranges. DISCOVER, TMR_ADVERTISE and GM_CHANGE in WAITING keep 0 to 4 s. The stack's tests, its plants (2 restated, 5 new) and its docs are updated, the generated tables by their generators.
- This repository: the gitlink and the host test group G in `sw/firmware/ctrl/test/test_adp.cpp`:
  - G1/G5: 64 LINK_UPs; the first ENTITY_AVAILABLE within 1 s; the delay still random; available_index +1 per frame across link-ups; later delays still 0 to 4 s.
  - G2: 32 startups with the link up.
  - G3: a grandmaster change inside the delay, carried by the first frame.
  - G4: a grandmaster change 4.5 s after LINK_UP, announced by a new ENTITY_AVAILABLE with the new gptp_grandmaster_id and the next index.
- The walk's LINK_UP x DOWN cell now expects the LINK_UP kind.
- `adp_first_mutants.py`: 6 new plants and 2 restated, plus a G4 kill for `gm-change-ignored`.
- Docs: MAILBOX_SPLIT.md (the ADP slice), the firmware README, SUBMODULES.md and its diagram, FR_NFR.md's two derivation rows (the bounds do not move), and CHANGELOG.

Validation (the twin, the boot simulation, the images and the CPU legs ran at `b000faa5`; the commits after it change test code and docs only, so no image input changes):
- Firmware gate, all four shards (`test_ctrl_firmware.py --require-rv32 --self-test`):
  - at `b000faa5`: PASS, 75 of 75 suite verdicts, the control campaign 832 of 832 caught, 0 escaped in the AECP and SRP campaigns;
  - at `b7b845c2` and at the final head `27495a06`: the same, PASS.
- fw_coverage: PASS, 40 files.
- Twin and its three plant and map legs: PASS, 0 findings. The split's first ENTITY_AVAILABLE is 91 ms after boot.
- Split boot simulation: 1x1 and 8x8 PASS, ready at 27.961 and 67.161 ms (base 27.952 and 67.223 ms). Its self-test catches 6 of 6 plants.
- Platform ledger: PASS at every point on base and head, with the same RAMB36 counts (45, 46, 58, 63).
- Image diff, 8 platform and fixture images:
  - only `adp.o` differs: `.text.enter_delay` grows from 176 to 180 bytes;
  - the canonical listings differ in 5 lines, the draw's range and the LINK_UP kind;
  - the 12 CPU budget images are linked at both heads (hashes in the receipts).
- CPU budget legs, base against head, 9 groups (the ADP groups, the ADP backlog, aecp, datapath-events) at 1x1/1if and 8x8/1if:
  - 63 of 63 probes paired at each point, 0 verdicts changed, 0 misses on either side;
  - the largest difference is −0.074 ms at 1x1/1if and +0.097 ms at 8x8/1if, each against 20 ms.
- The CPU table graders give byte-identical output on base and head.
- On the real CPU with the mailbox RTL, the first ENTITY_AVAILABLE after LINK_UP comes 91.142 ms after it at 1x1/1if and 89.366 ms at 8x8/1if. The base gives 730.108 and 719.315 ms (the harness's one deterministic draw).
- Docs workflow steps at `27495a06`: 104 of 104. Builder legs 0 and 1 at `27495a06`: PASS, each with the one NOT RUN arm the tree declares (leg 1's needs a build tree that is not on this host).
- tsn-c-stack at `5d14a6d8`: `validate.py --graphs` rc 0 (482 of 482 plants caught) and `baremetal.py` rc 0.

Acceptance criteria:
- First ENTITY_AVAILABLE within 1 s of the interface's link-up, at 1x1/1if and 8x8/1if, with and without a grandmaster change in the first 6 s: met.
  - G1 to G4 at head: the latest is 499 ms after LINK_UP, 496 ms after a startup, 457 ms with a change inside the delay and 421 ms with one 4.5 s after LINK_UP.
  - On the budget harness: 91.1 ms at 1x1/1if and 89.4 ms at 8x8/1if.
- The grandmaster change is still announced: met. G4: a new ENTITY_AVAILABLE with the new gptp_grandmaster_id and the next available_index, within 4 s of the change (latest 3,994 ms). G3: a change before the first frame is carried by it.
- A host test of both orders with a planted defect: met. G3 and G4, with plants such as `gm-change-in-delay-restarts-the-delay` and `gm-change-ignored`, each caught by its test's own words. On the base stack, G1 to G4 fail.
- The bench re-run: not met here. It is the manager's, after merge.

Open risks/questions:
1. The stack change must pass tsn-c-stack's own review first. The pin then moves to its merge commit, and the five pin records move with it (PR body).
2. My reading: Milan's TMR_DELAY is "a random value between 0 and 4 seconds" (Table 5.50), and 0 to 0.5 s is such a value. IEEE 1722.1-2021 6.2.4.2.2's uniform 0 to valid_time/5 belongs to the Advertising Entity machine, which Milan 5.6.3 replaces.
3. Part of the observed 5.76 to 6.82 s is past the 4 s draw, so it comes before ADP's LINK_UP. From the code, the candidate is the boot path. The link word resets to up, so the datapath transmits on a link the PHY formed before the first poll. The poll then restarts autonegotiation at every boot (#840), which drops that link, and ADP's LINK_UP comes after the renegotiation. This is not measurable here. I recommend a new issue; it is not changed in this lane.
