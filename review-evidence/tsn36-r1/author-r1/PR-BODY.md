[A820]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN. These all pass: the firmware gate (four shards, every planted-defect campaign), fw_coverage, the twin and its plants, the split boot simulation at both shapes with its self-test (7 of 7 plants), the platform ledger at every point, the docs workflow steps (104 of 104) and both builder legs. The CPU budget legs change nothing: the harness's images are byte-identical to the base. The platform images differ in `ctrl_plat_phy.o` alone.

`pf-972-1` -> `dev-soft-core`, on the flip PR's reviewed head `dd163e41` (#960). This change is the six commits after `dd163e41`; the final head is `0f508a01`. The tsn-c-stack submodule stays at its pin `715589c1`, and the ADP draws are unchanged (the ruling on #970).

## Linked Issue / roles

Closes #972
Relates to #970, #665

Executor: `[A820]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

**#972, the boot path.** Two things delayed and confused the first discovery after a boot:
- The published link word, `milan_mac_link_status`, resets to link up. So until the PHY poll's first publication, the datapath's effective link was up: the gPTP plane's port, the fabric MAAP engine and the mailbox's LINK level all followed it. ADP even drew a startup delay on that link. At 1x1 the first publication came 27.3 ms after reset, just before READY.
- The poll then restarted autonegotiation at every boot, whatever the PHY held. Any frame sent on the link the PHY formed before that restart went out on a link that then dropped. ADP's LINK_UP, and its 0 to 4 s draw, came only after the renegotiation.

The fix, in `sw/firmware/ctrl/plat/ctrl_plat_phy.c`:

| Change | Effect |
|---|---|
| `ctrl_plat_phy_arm` publishes link down first, right after the CSR identity check and before its first MDIO frame | The datapath sees no link until a poll publishes the PHY's verified one. ADP starts DOWN and draws its LINK_UP delay on the published link (Milan v1.2 5.6.3.5.3). A bus with no MDIO pair publishes nothing, and keeps the reset value, the only link such a board has |
| The arm owes the advertisement without its restart (`CTRL_PLAT_PHY_ADV_OWED`, not `\| ADV_RENEGOTIATE`) | At boot, as after a link loss, registers 9 and 4 are written and read back. Negotiation restarts only where they did not hold the advertisement, so the boot forms the link once. THE OUTCOME check is unchanged: a negotiation in force that shares no 1000BASE-T mode is still published down and restarted. So #840's link-speed behaviour is unchanged: 1000BASE-T full duplex only, and a 100BASE-TX-only partner gets no link |

The tests and plants:
- Host, `test_plat_phy.cpp`:
  - P11 restated: a PHY that holds the advertisement at boot is written, not restarted.
  - P19: the boot forms the link once. A PHY holding the advertisement, with its link up before the boot and a restart that would latch a loss, is never restarted, and its link is published once.
  - P20: arming publishes link down before any frame.
  - P21: THE OUTCOME stands behind a boot that restarts nothing. A held advertisement with a 100 Mb/s negotiation still in force is published down and restarted.
  - P9: a bus with no MDIO pair publishes nothing.
- Composed, `test_plat_boot.cpp`:
  - L4: the gPTP port enable is down from the arm until the first publication.
  - L2/L3/L5 restated: the boot's publications move each AVB_INTERFACE counter once. That is how a boot whose PHY has no link yet at its first poll already moves them.
- Plants (`plat_mutants.py`):
  - `plat-phy-boot-restarts-whatever-held` (the old behaviour). It replaces `plat-phy-boot-restart-dropped`, which planted what is now the fix.
  - `plat-phy-arm-publishes-nothing`.
  - `plat-phy-outcome-unchecked` gains a P21 kill.
- Split boot simulation (`run.py`):
  - the PHY grade requires the arm's link-down publication before the first frame, and reports when it lands;
  - new plant `phy-arm-unpublished`;
  - the `phy-unadvertised` anchor follows the arm.

**#970, salvaged after its ruling.** `test_adp.cpp` group G, on the unchanged core, against Milan's literal draws:
- G1/G5: 64 LINK_UPs. Each first ENTITY_AVAILABLE comes within its 0 to 4 s draw, and each quarter of the range holds at least 8 of the 64. available_index goes up by one per frame across link-ups. The TMR_ADVERTISE delays are spread over 0 to 4 s.
- G2: 32 startups, each within the 0 to 2 s draw, each half of the range holding at least 8.
- G3: a grandmaster change inside the delay re-arms nothing. The frame leaves at the LINK_UP's own deadline and carries the new grandmaster.
- G4: the bench's order, a change 4.5 s after LINK_UP. It starts a delay at once and is announced by a new ENTITY_AVAILABLE with the new gptp_grandmaster_id and the next index. That draw passes 2 s across the link-ups.

Plants (`adp_first_mutants.py`):
- moved from `ctrl_mutants.py` with G kills added: `gm-change-ignored`, `link-up-draws-startup-kind`, `draw-kinds-merged`;
- new:
  - `link-up-draws-half-a-second` (round 1's narrowing, now a defect);
  - `first-delays-not-drawn`;
  - `gm-change-in-delay-restarts-the-delay`;
  - `gm-change-draws-the-startup-kind`;
  - `link-loss-resets-the-index`.

**The declared discovery time.** `docs/reference/FR_NFR.md` 2.1.1 derives the declared 6.0 s term by term, each term cited, for a sum of 4,311 ms:

| Term | Bound |
|---|---:|
| The link publication (the release's bound) | 250 ms |
| The PHY link time (the link guard's 41.94 ms settle, inside the publication) | 0 ms added |
| The LINK event | 30 ms |
| The 0 to 4 s draw | 4,000 ms |
| The expiry to the frame | 30 ms |
| The egress | 1 ms |

The ADP slice in MAILBOX_SPLIT.md and the G tests cite it.

## Authoritative references

- #972's acceptance; the [A10] ruling on #970 (Milan's draws prescribed: 5.6.3.5.2 and 5.6.3.5.3, uniform per IEEE 1722.1-2021 6.2.4.2.2).
- Milan v1.2 5.6.3.5.2, 5.6.3.5.3, 5.6.3.5.7 and Tables 5.50/5.51; IEEE 1722.1-2021 6.2.2.15 and 6.2.2.16.
- IEEE 802.3 22.2.4.1.7, 22.2.4.2.13 and 28.2.4.1.3; #840 (the advertisement); #919 (the PHY poll).
- `sw/firmware/ctrl/plat/ctrl_plat_phy.h` (THE ADVERTISEMENT, THE LINK BEFORE THE FIRST POLL, THE OUTCOME); `sw/firmware/ctrl/plat/README.md`.

## How to get into the same state

```sh
git fetch origin pull/<this PR>/head:pf-972-1
git switch pf-972-1
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
```

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 1/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 2/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 3/4
python3 sw/firmware/gtest/fw_coverage.py --selftest && python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir <dir>/1x1
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir <dir>/8x8 --shape endstation_ax7101_8x8
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir <dir>/plants --self-test
make -C tb/verilator/milan_dp twin twin-plants twin-maps twin-maps-plants
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir <dir>/plat
```

Expected result / pass criteria:
- Every firmware shard ends `test_ctrl_firmware: PASS`, and the control campaign catches every plant by its named test and words.
- The boot simulation reports "PHY the arm published link down at ... ms, before the first frame" at both shapes, and its self-test catches `phy-arm-unpublished`.
- fw_coverage, the twin and `plat_ledger` pass.

Evidence. The firmware gate, twin, images and CPU legs ran at the code head `48c39b5b`; the boot simulation and builder leg 0 at `ba0f80ed`; the docs steps and builder leg 1 at the final head `0f508a01`. The commits after `48c39b5b` change only the boot simulation's stand-in and README and the documentation audit.

| Gate | Result |
|---|---|
| Firmware gate, four shards | PASS: 75 of 75 suite verdicts; control campaign 832 of 832 caught (826 at the base; 5 ADP and 1 net platform plant new); AECP 385 and SRP 543 `[ok]`; 0 escaped |
| fw_coverage | PASS, 40 files |
| Twin and its plant and map legs | PASS, 0 findings, every plant refused |
| Split boot simulation | 1x1 and 8x8 PASS, ready 27.978 / 67.228 ms (base 27.952 / 67.223); the arm's link down at 2.636 / 4.434 ms, before the first frame (27.125 / 66.186 ms); self-test 6 of 6 native controls, 7 of 7 plants (`phy-arm-unpublished` new) |
| Platform ledger, base and head | PASS; RAMB36 45 / 46 / 58 / 63 unchanged; rom +16 B at every point |
| Image diff | platform images: `ctrl_plat_phy.o` only, `ctrl_plat_phy_arm` 176 -> 192 B (the arm's write, the owed flag); size-fixture images byte-identical |
| CPU budget legs, 9 groups, 1x1/1if and 8x8/1if | harness images byte-identical to the base; 63 of 63 probes equal; 0 verdicts changed; 0 misses |
| Docs workflow steps | 104 of 104 |
| Builder legs 0 and 1 | PASS, each with the one NOT RUN arm the tree declares on this host |

## Known limitations / out of scope

- The window before the arm. From the datapath's reset to the CSR identity check, the word still holds its reset value, link up: about 2.6 ms at 1x1 and 4.4 ms at 8x8, the split boot simulation measures. On a power-up or a REBOOT the PHY has no link then, since its reset and autonegotiation take seconds. A gateware reload that keeps the PHY's link could still let a frame out in that window. Closing it would take the word's reset value at link down, which is a gateware (RTL) change and outside this lane. It is left as an open decision.
- A PHY at its defaults (10/100 advertised, as after a power-up or a REBOOT's PHY reset) is still written and restarted once, as #840 requires. That renegotiation now happens before the first publication, so nothing is sent before it.
- The release (all-fabric) image's PHY init is unchanged: it restarts at every boot, and its ADP engine is the processor's.
- The bench re-run of the discovery scenarios is the manager's, after merge.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (the bench item is pending, after merge)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
