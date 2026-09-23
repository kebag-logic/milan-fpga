[A200] REVIEW READY: #117 bench steps 2, 4 and 5 (controller part) on the dev `ede8d48e` image. Step 3 is blocked on the owner.

**Commit:** `c3eb95fa9ac86a3f20b45f94057d6c011127db08`, branch `117-silicon-evidence`, one commit on live dev `ede8d48e`. It is not pushed; the manager publishes.

**Changed:** the new page `docs/findings/117_GPTP_SILICON_EVIDENCE.md` (SHA-256 `caa761cf911bdde486e64e5cd5d475115402b04e28755e3ab3512a372e1153cb`) and one row in `docs/findings/README.md`.

**Validation:**
- `scripts/docs_check.py`: 0 findings across 165 md files.
- `scripts/check_doc_style.py`: OK.
- `scripts/gen_toc.py --check`: OK.
- `scripts/check_em_dash.py --base ede8d48e`: 0 findings over 314 added lines.

**Identity gate: PASS.** The console CRC readback ran under the bench lock, 12:41:19 to 12:41:43 UTC.
- ROM: `f6afa4ec`.
- QSPI bitstream payload: `02036e95`, the `asl` seed. This excludes `eppo` `7b415f48`, `eto` `2567bab7` and the replaced `f6b31625` image `a6fb19bb`.
- AEM: `93742dd2`.
- `VERSION=00020060`, and the UART grader passed 10 of 10.
- `origin/dev` was still `ede8d48e`, so no byte comparison was needed.

## Per-step result

| Step | Result | Key evidence |
|---|---|---|
| Identity: VERSION, ROM, QSPI bitstream, AEM | PASS | see above |
| 2. asCapable with no software daemon; cadence; turnaround; peer firmware identity | PASS for retention and limits; the initial reach is NOT RUN (it happened before these windows) | See the notes below the table. |
| 3. GM loss and return; recovery time; stream state | NOT RUN: owner blocker B1 | see below |
| 4. Publication CSRs and `tu` against the wire | PASS (steady state); transition NOT RUN | See the notes below the table. |
| 5. la_avdecc discovery and enumeration; behave on hardware | counters probe PASS; full enumeration FAIL; Hive NOT RUN; behave NOT RUN | See the notes below the table. |
| Acceptance boxes | none checked | 1: retention PASS, reach not observed. 2: NOT RUN. 3: steady state only. 4: FAIL plus NOT RUN rows. 5: the new page. |

**Step 2:**
- asCapable held in 116 of 116 console samples and 60 of 60 controller polls, 12:41 to 13:14 UTC.
- Peer delay stayed between 380 and 391 ns.
- The DUT's Pdelay turnaround was at most 11.009 us over 568 exchanges, against the 15 ms limit.
- Sync: 4,556 intervals with a mean of 125.0 ms and a maximum of 149.4 ms. Announce and Pdelay ran at 1 s, and the DUT's Pdelay_Req at 1000.002 ms.
- The peer firmware field hash `33f0e7f9...` is unchanged since 2026-09-14.

**Step 4:**
- GM, parent, path, peer delay, domain, sync, asCapable and `tu` agree with Announce, PathTrace, ADP, the tap-derived delay and GET_AVB_INFO/GET_AS_PATH.
- For `tu` on the wire, the reference peer's primary CRF input was bound to the DUT's CRF output for 60 s. The DUT sent 34,061 PDUs, all with `tu=0`. `CLKV_STAT` read `tu=0` in 53 of 53 samples, and `CRFT_COUNT` equals the wire count.

**Step 5:**
- The counters probe gives a transcript identical to the reference peer's, verdict CLEAN.
- The full la_avdecc enumeration FAILS: Milan is downgraded to IEEE 1722.1 with "Milan mandatory counters missing for STREAM_INPUT descriptor". The CRF Stream Input returns `counters_valid` 0.
- Hive is NOT RUN (it needs a desktop). behave is NOT RUN (the suite has no hardware tier).

**Topology for box 1:** the DUT's asCapable partner is port 1 of the bench AVB switch, which is the grandmaster (priority1 246). The reference peer is a slave on another switch port with the same grandmaster; its AS path is `[GM, peer]`. Reviewers should judge whether that satisfies "against the reference peer" under the one-DUT contract.

## Owner blockers

1. **B1: no permitted way to induce GM loss and return.**
   - The grandmaster is the bench AVB switch.
   - The reference peer exposes only an IDENTIFY control, and AVDECC has no gPTP-priority command.
   - The switch has no AVDECC entity and no address on the AVB segment. It sends a DHCP request every 15 s that nothing answers. No bench host has a management path or credentials for it.
   - The repository's own procedure, checklist entry `phys.switch-cycle.gm-partition`, is a power-strip cycle of the switch, which this assignment excludes.
   - Decision: authorize that cycle under the bench lock, or provision switch management for a port or priority command.
2. **B2: no numeric recovery bound is documented.** The grandmaster-recovery design page gives none. The protocol figures are a 3 s announce receipt timeout, a 375 ms sync receipt timeout and a 0.25 s `tu` holdover. A bound must be stated before step 3 can pass or fail.
3. **B3:** the switch's firmware identity cannot be read without that management path.
4. **B4:** Hive needs an interactive desktop session.

## New findings for separate issues (outside every box; no cause assigned)

1. **The DUT's CRF talker ends its own bursts while the listener stays bound.**
   - There were four bursts: 19.67, 18.45, 15.00 and 15.00 s.
   - Each ends with the DUT stopping emission and then sending an MSRP TalkerAdvertise Leave.
   - Three of the four ends fall 15.00 s (plus or minus 2 ms) after the latest successful probe response. The last came 9.95 s after the unbind.
2. **The first burst began before any reservation.** It started 0.18 ms after the DUT answered the first probe with TALKER_DEST_MAC_FAIL, 4.7 s before any Listener Ready.
3. **Stream Output 1 FRAMES_TX reads 16** after 34,061 PDUs.
4. **The la_avdecc Milan downgrade above:** the CRF Stream Input counter gap the register map already records.

## Bench state

Restored, and the census shows it.
- The binding census matches before and after for all 18 states.
- The reference peer is unchanged: configuration 0, 96 kHz, INTERNAL clock source, the same CRF format and the same firmware hash.
- The bind window unbound on its first attempt.
- The DUT passed the grader 10 of 10 at 13:13 UTC.
- The controller registration was cleanly deregistered.
- Temporary files were removed from the bench hosts, and the bench lock is free.
- Flash, JTAG, power, wiring and instruments were not touched.

Raw artifacts are in the private bench packet with a per-file SHA-256 manifest. The findings page lists the primary hashes, for example the captures of the steady-state run `26c4529a...`, the bind run `febe8a16...` and the controller run `f07b7230...`.
