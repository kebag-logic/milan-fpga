# HANDOFF r1 — #970 ([A820]) — the first ENTITY_AVAILABLE after link-up

STATUS (15:10 CET 2026-11-22): **REVIEW READY** at `27495a06` (the stack at `5d14a6d8`). Every gate passes (section 5);
the reproduction fails on the base stack and passes on the head (section 4). ETA: none, round done. No unit of this
lane is left running. Nothing pushed; no PR opened (the manager's: PR-BODY.md).
Posted: `[A820] TAKEN` issuecomment-7077038835 (TAKEN-comment.md) and `[A820] REVIEW READY` issuecomment-7080275766
(REVIEW-READY.md).

Branch `pf-970-1` at the FLIP PR's reviewed head `dd163e41` (PR #960), PR base `dev-soft-core`; five commits:
`1352f319` (pin, tests, plants, pin records), `b000faa5` (docs), `87d749d7` (the plants' table in its own module),
`b7b845c2` (docs style), `27495a06` (the G tests read only ENTITY_AVAILABLEs; G4's exercise check stated by what it
counts).

**Delivery shape (manager action needed).** The ADP core is the pinned tsn-c-stack submodule. Its porting contract says
`timer_start` "delivers adp_timer_expired once after delay_ms", so shortening the delay in the adapter would break a
documented contract, and the fix has to be the core's. The lane therefore carries two branches:
- tsn-c-stack branch `970-first-advertise`, two commits on `715589c1`. `7e03f71c` is the change with its tests, plants
  and docs; `5d14a6d8` is the static-analysis fix. The branch is local, in the lane's submodule checkout
  (`third_party/tsn-c-stack`). It is to be pushed and opened as a tsn-c-stack PR, which needs that repository's own
  two reviews under its CONTRIBUTING. The CI materialisation of this PR needs `5d14a6d8` to be fetchable.
- milan-fpga `pf-970-1`: the gitlink at `5d14a6d8`, plus this repository's tests, plants and docs.

SPLIT_CONTROL_MEMORY.md, "What is left", states the rule: the stack's changes reach this repository only through the
stack's review, then a pin move. After the stack PR merges, the gitlink moves to its merge commit, and so do these
records:
- the SUBMODULES.md row and its #970 paragraph;
- the diagram, through `docs/diagrams/submodule_boundaries.gen.py`;
- the `adp.h` links in MAILBOX_SPLIT.md:517 and in the firmware README:65;
- CHANGELOG's pin line.

The images do not change if the merge carries these `src/` and `include/` bytes.

## 1. Task and authority
- Issue #970, which relates to #665.
- Milan v1.2 5.6.3: Tables 5.49 to 5.51, and 5.6.3.5.2, .3, .5, .7 and .9.
- IEEE 1722.1-2021 6.2.2.15 and 6.2.2.16, 6.2.4 (6.2.4.2.2, randomDeviceDelay) and 6.2.5.

## 2. Cause (named from the code, reproduced in section 4)
In the split firmware, an interface's first ENTITY_AVAILABLE after a link-up waits for one thing only: its TMR_DELAY.
- In tsn-c-stack `src/adp.c`, `adp_link_change` (DOWN to LINK_UP, Milan 5.6.3.5.3) called
  `enter_delay(a, ADP_DRAW_DELAY)`: a uniform draw of 0 to `ADP_DELAY_MAX_MS`, 4,000 ms. `adp_set_enable` with the link
  up (5.6.3.5.2) drew 0 to 2,000 ms.
- Reproduced on the base stack (section 4): the first ENTITY_AVAILABLE up to **3,990 ms** after LINK_UP over 64
  link-ups; 3,649 ms with a grandmaster change inside the delay; 3,364 ms with one 4.5 s after the link-up.

From the code, the first advertise waits for nothing else:
- not asCapable: the firmware never reads it;
- not the grandmaster: a GM_CHANGE in DELAY is ignored (Table 5.51), and the frame samples GM_LO/GM_HI when it is
  built (6.2.2.16). A change before the first frame is carried by it (G3); a change after it re-advertises (G4);
- not a settle timer: there is none in the adapter or the app;
- not the link debounce. The PHY poll publishes the link within its 125 ms period (`ctrl_plat_phy.h`, THE PACE). The
  link guard's 42 ms settle holds the MAC's reset after a clock death, and its estimate (`rx_alive`) returns at the
  first RX clock edges (`hdl/common/KL_link_guard.sv:320`);
- not a pass of the loop: milliseconds, with the LINK event taken by pass 2 (`adp_mbx.h`).

On the CPU budget harness (the real CPU and the mailbox RTL), the base's one deterministic draw put the first
ENTITY_AVAILABLE 730.108 ms after LINK_UP at 1x1/1if and 719.315 ms at 8x8/1if. That is why no harness run ever
showed the defect.

The issue's 5.76 to 6.82 s is past the 4 s draw, so some 1.8 to 2.8 s comes before ADP's LINK_UP. From the code, the
candidate is the boot path, not ADP:
- `milan_mac_link_status` resets to link up (`ctrl_plat_phy.h`), so the datapath transmits on a link the PHY formed
  before the first poll;
- the poll then restarts autonegotiation once at every boot, whatever the PHY held (#840, `ctrl_plat_phy.h` THE
  ADVERTISEMENT), which drops that link for a renegotiation;
- ADP's LINK_UP, and its fresh draw, come only after it.

This is not measurable here (no bench). It is recommended as a new issue (section 8) and not fixed in this lane.

## 3. Changes (file:line at the head, reason)
tsn-c-stack (`970-first-advertise`, `5d14a6d8`):
- `include/adp.h:87-88`: `ADP_DELAY_STARTUP_MAX_MS 500u` (was 2000u) and the new `ADP_DELAY_LINK_UP_MAX_MS 500u`;
  `:116` the new `ADP_DRAW_LINK_UP` kind. Both are within Milan's ranges (0 to 2 s and 0 to 4 s): a value drawn from
  0 to 0.5 s is "a random value between 0 and 4 seconds" (Table 5.50). 500 ms leaves the 1 s bound 0.5 s for the PHY
  poll's 125 ms publication, the LINK event's pass and the frame's pass.
- `src/adp.c:55-61`: `draw_ms` picks the range by kind with two independent tests. clang-tidy's branch-clone check
  refused an else-if chain whose two bodies expand alike (`7e03f71c`'s static-analysis finding).
- `src/adp.c:265`: LINK_UP draws `ADP_DRAW_LINK_UP`. DISCOVER, TMR_ADVERTISE and GM_CHANGE in WAITING keep
  `ADP_DRAW_DELAY`, 0 to 4 s.
- `tests/test_adp.cpp`:
  - A0: LINK_UP draws the new kind, 0 to 0.5 s.
  - A3: startup draws 0 to 0.5 s.
  - A9: restated for three kinds against literals (`kFirstDrawMaxMs` 500, `kDelayDrawMaxMs` 4000), so a planted
    header constant is seen.
  - A18 and A20: the LINK_UP kind.
- `tests/mutations.json`: `link-up-draws-startup-kind` and `draw-kinds-merged` restated; 5 new plants (section 4).
  477 plants become 482.
- Docs:
  - `docs/PORTING.md`: the draw rows and the rule;
  - `docs/requirements.json` MFDISC-01, with `REQUIREMENTS.md`, `TRACEABILITY.md` and `TESTS.md` regenerated by
    `traceability.py --write` and `test_inventory.py --write`;
  - `docs/VERIFICATION.md`: 478 core plants;
  - `CHANGELOG.md`;
  - `scripts/check_port_contracts.py`: the new name in its guide section.

milan-fpga (`pf-970-1`):
- `1352f319`:
  - the gitlink `third_party/tsn-c-stack` moves to `5d14a6d8`;
  - `sw/firmware/ctrl/test/test_adp.cpp:553-815`: group G, with tests at `:902-915` (section 4);
  - `adp_walk.cpp:268-277`: the LINK_UP x DOWN cell's draw is the LINK_UP kind, the firmware's one difference from
    the processor's T-ADP-DELAY; P1's words follow;
  - `ctrl_mutant.py:14`: `ADP_H`;
  - `ctrl_mutants.py`: the new kill for `gm-change-ignored`;
  - `docs/reference/SUBMODULES.md`: the pin row and the #970 paragraph; the submodule diagram regenerated by its
    generator.
- `b000faa5`:
  - `docs/design/MAILBOX_SPLIT.md:533-544`: the ADP slice's schedule; the `adp.h` link at the new pin;
  - `sw/firmware/ctrl/README.md:65,82-85`;
  - `docs/reference/FR_NFR.md:415-416`: the two ADP derivation rows. The split's 0.5 s windows give 50 ms, above
    ADP's 30 ms row bound, which does not move;
  - `CHANGELOG.md`.
- `87d749d7`: `sw/firmware/ctrl/test/adp_first_mutants.py` (new) holds the #970 plants and the two restated draw
  plants. Without it, `ctrl_mutants.py` would have grown past the Python idiom ratchet's 1,000-line module limit
  (the long-module count went 10 to 11); it is now 996 lines.
- `b7b845c2`: CHANGELOG and SUBMODULES.md sentences kept within `check_doc_style.py`'s lengths.
- `27495a06`: `test_adp.cpp:576-590` the `Wire` reader keeps only ENTITY_AVAILABLEs (a DEPARTING count was kept
  and never judged); `:810-811` G4's exercise check says what it counts (at least four different change-to-frame
  delays), not "most runs". Found on my own review before handing off; behaviour and figures unchanged.
- No RTL, mailbox contract, CPU budget bound or CPU-budget harness file changed.

## 4. Reproduction and new checks
The host test is group G of `sw/firmware/ctrl/test/test_adp.cpp`, run on the mailbox model through the app and the
adapter. Its figures are stated independently of the core's names: 1,000 ms is the acceptance, 500 ms the draw and
4,000 ms Table 5.50.

| Test | What | Base stack `715589c1` | Head `5d14a6d8` |
|---|---|---|---|
| G1/G5 `WithinOneSecondOfEveryLinkUp` | 64 LINK_UPs: the first ENTITY_AVAILABLE within 1 s; the delay still random; available_index +1 per frame across link-ups; the TMR_ADVERTISE delays 0 to 4 s and past 0.5 s | FAIL: latest 3,990 ms | PASS: latest 499 ms, 56 distinct |
| G2 `WithinOneSecondOfAStartupWithTheLinkUp` | 32 startups (32 entity IDs) with the link up | FAIL: latest 1,981 ms | PASS: latest 496 ms, 32 distinct |
| G3 `AGrandmasterChangeBeforeItIsCarriedByIt` | a GM change inside the link-up's delay, 32 link-ups: within 1 s, carrying the new GM | FAIL: latest 3,649 ms | PASS: latest 457 ms |
| G4 `AGrandmasterChangeAfterItIsAnnounced` | the bench's order, a GM change 4.5 s after LINK_UP: a delay starts at once, then a new ENTITY_AVAILABLE with the new GM and the next index within 4 s | FAIL: first latest 3,364 ms | PASS: first 421 ms; new GM within 3,994 ms |

The base receipts are `repro/base-stack-715589c1-adp-tests.txt` and `repro/head-stack-adp-and-walk.txt`.

Planted defects, in the firmware campaign (`adp_first_mutants.py`). All are caught in the gate's control campaign,
832 of 832, at `b000faa5`, `b7b845c2` and the final head `27495a06`:

| Plant | Caught by | Failing words |
|---|---|---|
| `link-up-draws-the-delay-kind` (the base) | adp G1G5; adp G3; walk LINK_UP_x_DOWN | "G1 the first ENTITY_AVAILABLE leaves within 1 s of every LINK_UP"; "G3 a grandmaster change before the first ENTITY_AVAILABLE does not hold it past 1 s"; "the draw is the 0..0.5 s LINK_UP kind" |
| `startup-range-two-seconds` | adp G2 | "G2 the first ENTITY_AVAILABLE, index 0, leaves within 1 s of a startup with the link up" |
| `gm-change-in-delay-restarts-the-delay` | adp G3 | "G3 a grandmaster change before the first ENTITY_AVAILABLE does not hold it past 1 s" |
| `every-draw-the-first-range` | adp G1G5 | "G5 only the link-up's delay is shortened: the TMR_ADVERTISE delays pass 0.5 s" |
| `first-delays-not-drawn` | adp G1G5; adp G2 | "G1 the delay stays a random draw across the link-ups"; "G2 the startup delay stays a random draw across the entities" |
| `link-loss-resets-the-index` | adp G1G5 (the only test that sees it) | "G1 each ENTITY_AVAILABLE carries the next available_index, across every link-up" |
| `gm-change-ignored` (existing; new kill) | walk GM_CHANGE_x_WAITING; adp G4 | "GM_CHANGE x WAITING"; "G4 a grandmaster change after the first ENTITY_AVAILABLE starts a delay at once" |
| `link-up-draws-startup-kind` (restated) | walk LINK_UP_x_DOWN | "LINK_UP x DOWN" |
| `draw-kinds-merged` (restated) | adp AdpCore.A9DrawKinds | "A9 every startup draw and every LINK_UP draw is 0..0.5 s" |

The control campaign goes from 826 plants at the base to 832.

In the stack's campaign (`tests/mutations.json`), five plants are new: `link-up-draws-delay-kind`,
`link-up-range-is-the-delay-range`, `every-draw-the-first-range`, `startup-range-two-seconds` and
`link-up-range-four-seconds`. Two are restated. At `5d14a6d8` the campaign gives
`{"CAUGHT": 482, "ESCAPED": 0, "ERROR": 0}`.

## 5. Gate table
The firmware gate, the docs steps and the builder legs ran at the final head `27495a06`, and the firmware gate also at
`b000faa5` and `b7b845c2`. The twin, the boot simulation, the images and the CPU legs ran at `b000faa5`. After it,
`87d749d7` moves only test Python (the plants' table), `27495a06` changes only `test_adp.cpp` and `b7b845c2` is docs,
so no image input changes (`change/after-b000faa5.txt`).

| Gate | Result |
|---|---|
| Firmware gate, 4 shards (`--require-rv32 --self-test`), at `27495a06`, and before at `b000faa5` and `b7b845c2` | PASS at each: 75 of 75 suite verdicts; control campaign 832 of 832 caught; AECP campaign 385 `[ok]`; SRP campaigns 543 `[ok]`; 0 escaped |
| `fw_coverage.py --selftest`, `--check --jobs 4` | PASS (29 of 29 planted cases; 40 files) |
| Twin, twin-plants, twin-maps, twin-maps-plants | PASS: 0 findings, every plant refused. The split's first ENTITY_AVAILABLE is 91 ms after boot (the fabric's 756 ms) |
| Split boot simulation 1x1, 8x8, `--self-test` | PASS, PASS (ready 27.961 / 67.161 ms; base 27.952 / 67.223 ms, also PASS); self-test 6 of 6 native controls, 6 of 6 plants |
| Platform images at every ledger point (`plat_ledger.py`), base and head | PASS both. RAMB36 45 / 46 / 58 / 63 at both; rom +8 B at 1x1, +0 at 8x8; sram unchanged |
| Image diff, platform and size-fixture images (8 pairs) | Only `adp.o` differs: `.text.enter_delay` 176 -> 180 B. The canonical listings differ in 5 lines (the draw's range, the LINK_UP kind), and the relinks equal the built images. The 12 budget images are linked at both heads (hashes in `images/`) |
| CPU table graders (`flip_grade --check`, `--point 1x1/1if`, `load_grade --check`, `shape_costs --check`) | Byte-identical at base and head. flip_grade FAILs at 8x8/2if only, by design, as at the base |
| CPU legs, 9 groups (adp-link, adp-gm, adp-discover, adp-advertise, control, backlog-adp, backlog-adp-refill, aecp, datapath-events), base vs head | 1x1/1if and 8x8/1if: 0 refusals, 0 budget misses each side; 63 of 63 probes paired; 0 verdicts changed. Largest difference −0.074 ms (1x1/1if) and +0.097 ms (8x8/1if) against 20 ms. 13 and 20 passes differ by an instruction count (the `enter_delay` change, or a pass composed differently) |
| First ENTITY_AVAILABLE after LINK_UP on the harness (real CPU, mailbox RTL) | head 91.142 ms (1x1/1if) and 89.366 ms (8x8/1if); base 730.108 / 719.315 ms |
| Docs workflow steps at `27495a06` (and `b7b845c2`) | PASS, 104 of 104, tracked files unchanged. The first run at `b000faa5` had two findings, both fixed: doc style (`b7b845c2`) and the idiom ratchet's long-module count (`87d749d7`) |
| Builder legs 0 and 1 at `27495a06` (and `b7b845c2`) | PASS and PASS. Each has one NOT RUN arm the tree declares: leg 0 the MAKEFLAGS note, leg 1 gate 11's mf48 build tree, which is not on this host, as in lane 951's run. The first runs were refused (submodule origins; the SDK link in the scratch home) and rerun after both were set (`gates/b7b845c2/builder-*.txt`) |
| tsn-c-stack `validate.py --graphs` and `baremetal.py` at `5d14a6d8` | rc 0 and rc 0. At `7e03f71c`, static-analysis's branch-clone finding (fixed by `5d14a6d8`) and graphs' browser path (environment) |

Not run:
- The full Verilator sweep (`native-shards.py`): no RTL, testbench or harness file changed, and the round's gate list
  does not name it.
- The candidate's `act_ci.py` self-test: AGENTS.md runs it only inside the CI job.
- Vivado: no RTL change, and the RAMB36 counts are unchanged.

## 6. Receipts
`receipts/` (INDEX.md, generated from the files present by `tools/receipts.py.txt` and
`tools/receipts_spec.py.txt`). Host paths are replaced by placeholders, files over 200 KB are not copied, and the
commit receipts carry no author identities.

## 7. Notes
- Scratch: `/data-2/milan/tmp/970-a820`, with clones under `clones/`. Units `milan-970-a820-*` only, each pinned to a
  range booked through `cpu_ranges.py pick`. The coverage, the docs steps and, at the final head, firmware shards 0, 2
  and 3 (campaign drivers, --jobs 8, 8, 4) ran inside the session unit while every range was booked; its memory
  stayed under 3 GB.
- `go.sh` now waits until a started unit's affinity is its booked range before the next pick. One earlier sequence
  looked like three starts on one range; each had in fact ended before the next started, so no CPUs were shared.
- Before git commands in the submodules, `rev-parse --show-toplevel` and the origin were checked. In the two builder
  clones (scratch, not the lane), the submodule origins were set to their `.gitmodules` URLs for the legs' origin check.
- The split boot README's results table records 27.540 / 66.615 ms at an older head. This change moves the figures by
  +0.009 / −0.062 ms, so they are left as recorded.

## 8. Open questions / recommendations
1. Recommended new issue (not filed: this lane posts only on #970). At boot the published link word's reset value is
   up, and the PHY poll restarts autonegotiation once whatever the PHY held. So frames can leave on a link the
   restart then drops, and ADP's first LINK_UP follows the renegotiation. The bench should show whether that is the
   1.8 to 2.8 s past the draw.
2. Reading for review: Milan's TMR_DELAY is "a random value between 0 and 4 seconds" (Table 5.50), and 0 to 0.5 s is
   such a value. IEEE 1722.1-2021 6.2.4.2.2's uniform 0 to valid_time/5 belongs to the Advertising Entity machine,
   which Milan 5.6.3's machine replaces.
3. The startup draw is nearly the same at every boot of one entity: the seed is the entity ID and NOW_MS at enable,
   and the first xorshift output moves little with a few milliseconds of NOW_MS (G2 needs 32 entity IDs to spread).
   This is pre-existing; noted, not changed.
4. The all-fabric placement's ADP engine (protocol-processor) still draws 0 to 4 s on LINK_UP. It is out of scope.

## 9. Posting
- `[A820] TAKEN`: #970 issuecomment-7077038835.
- `[A820] REVIEW READY`: #970 issuecomment-7080275766 (the text is REVIEW-READY.md).
- Nothing else posted; no existing comment edited. Nothing pushed. The PR body is PR-BODY.md (base `dev-soft-core`,
  `Closes #970`, `Relates to #665`), for the manager to open.

REVIEW READY 27495a06d5569336a098da20381ced3e331ba665
