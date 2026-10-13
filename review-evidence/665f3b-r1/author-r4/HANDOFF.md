[A612]

# F3b parent implementation handoff

Status: REVIEW READY under the round 4 local-validation assignment. Hosted acceptance remains manager-owned.
Candidate: `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5`.
Round 4 below is the current status and handoff. Earlier STOP statements are historical.
Round 2 remains the latest firmware image, coverage and mutation measurement.
Rounds 3 and 4 change no firmware, image builder, test campaign or dependency pin.
Branch: `665-f3b-parent`. Base: `d40e4e9827be2516f8f34b9d65f0a483fff2194c`.
Round 1 local head: `db29bdd07529fbc697b7956827092f64b1241714`.
Commit: `Publish F3b declaration demand through the mailbox`.
The worktree and all five initialized dependencies are clean.
No push, PR mutation, merge or hardware operation is authorized or performed.

Scope follows the [assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6151273346)
and corrected [F3b ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6151422598).
The two permitted behavior changes are the declaration predicate and the reviewed stack pin effects.
The assignment's earlier exact-#25-only statement is superseded by that ruling.

## Implementation and controls

| File:line | Change and evidence |
|---|---|
| `third_party/tsn-c-stack:1` | Pin 405dc683 to 70936b77; reviewed range below |
| `sw/firmware/ctrl/acmp/acmp_mbx.c:102` | Configure the 15000 ms freshness window |
| `sw/firmware/ctrl/acmp/acmp_mbx.h:136` | Accepted-probe timestamp funds one additional mailbox access |
| `sw/firmware/ctrl/maap/maap_mbx.c:36` | Query ACMP outside every MAAP callback; snapshot demand after observed expiry |
| `sw/firmware/ctrl/maap/maap_mbx.c:53` | Combine valid MAAP allocation, source interface and fresh-probe/Listener demand |
| `sw/firmware/ctrl/maap/maap_mbx.c:94` | Publish each interface's gate before its allocation report |
| `sw/firmware/ctrl/maap/maap_mbx.c:166` | Refresh changed gates even when no transmission is owed |
| `sw/firmware/ctrl/maap/maap_mbx.h:19` | Conservative event/RX/poll bounds 65/64/65; ACMP owner and cached publication state |
| `sw/firmware/ctrl/app/ctrl_app.c:28` | Bind the composed ACMP owner before MAAP attaches |
| `sw/firmware/ctrl/app/ctrl_app.c:78` | Enable idle service ticks so probe expiry closes the gate |
| `sw/firmware/ctrl/srp/srp_mbx.c:583` | Track any registered Listener separately from the existing Ready licence |
| `sw/firmware/ctrl/srp/srp_mbx.c:623` | Rebuild Listener presence on snapshot and clear it on destroy |
| `sw/firmware/ctrl/srp/srp_mbx.h:53` | Store Listener presence per interface/source |
| `sw/firmware/ctrl/app/ctrl_app_srp.c:53` | Forward presence on the configured interface; withdrawal/detach clears demand |
| `sw/firmware/ctrl/test/test_maap_mbx.cpp:252` | Fresh probe, Listener, neither, 14999/15000/15001 ms and invalid-DA controls |
| `sw/firmware/ctrl/test/test_maap_mbx.cpp:197` | Both interfaces retain gate-before-own-report assertions |
| `sw/firmware/ctrl/test/test_acmp_mbx.cpp:447` | Real mailbox PROBE_TX and idle tick wake close the composed gate at 15 s |
| `sw/firmware/ctrl/test/srp_feedback.hpp:4` | Real Asking Failed registration, Leave, rejoin, destroy and interface routing |
| `sw/firmware/ctrl/test/srp_mbx.cpp:333` | Registered Listener subtype control distinguishes demand from Ready licence; Ignore cannot create a registrar |
| `sw/firmware/ctrl/test/test_adp.cpp:564` | All 0..81-byte discoveries, versions 1..7 and wrong CDL are refused by parent adapter |
| `sw/firmware/ctrl/test/test_adp.cpp:590` | Complete 82-byte discovery with CDL 56 still advertises |
| `sw/firmware/ctrl/test/adp_walk.cpp:1` | Valid discovery fixtures carry required CDL 56 |
| `sw/firmware/ctrl/test/ctrl_mutants.py:504` | Predicate, composition, idle wake, publication ordering and ADP plants |
| `sw/firmware/ctrl/test/acmp_mutants.py:26` | Preserve source-count refusal plant against new pin's adjacent freshness validation |
| `sw/firmware/ctrl/test/acmp_review_mutants.py:38` | Preserve composition controls after owner binding is inserted |
| `sw/firmware/ctrl/test/maap_mutants.py:224` | Work-overrun plant exceeds the updated conservative bound |
| `sw/firmware/ctrl/test/srp_mutants.py:43` | Listener forwarding, interface, Asking Failed and withdrawal plants |
| `sw/mailbox/mailbox.yaml:323` | DA_GATE contract equals processor acmp_declaring_o; licence remains separate |
| `sw/firmware/ctrl/mbx/mbx_contract.h:1`, `hdl/milan/mailbox/KL_mbx_pkg.sv:1`, `docs/reference/MAILBOX_CONTRACT.md:255` | Generator-produced contract comments; register layout and contract hashes unchanged |
| `sw/mailbox/publication_census.py:178` | Current predicate in the consumer disposition |
| `sw/firmware/ctrl/README.md:77`, `sw/firmware/ctrl/maap/README.md:112` | Pin effects, ownership, freshness and service bounds |
| `docs/design/MAILBOX_SPLIT.md:702`, `:823`, `:1057` | Updated bounds and equivalence; removed obsolete DA_GATE egress choice |
| `sw/firmware/gtest/README.md:318` | Remove obsolete conditional-arc exclusion after composition no longer has that conditional |
| `docs/reference/SUBMODULES.md:27` | Exact pin and adopted effects |
| `docs/diagrams/submodule_boundaries.svg:1`, `.drawio:1`, `.png`, `PNG_MANIFEST.json:12` | Regenerated through submodule_boundaries.gen.py |

The firmware still uses the caller's source owner. The query is outside MAAP
callbacks because protocol ports must not call cores synchronously. Tests keep
the owner's DA invalid until its allocation callback, proving publication does
not depend on an already-updated owner. Querying inside the callback is planted
and rejected. No destination, licence, binding or shipping placement policy is changed.

The new Listener flag is not the licence: Asking Failed registers demand but
cannot license media. Ignore creates no registrar; an Ignore received while a
Listener exists does not erase that existing registrar. Leave and destroy clear
it. The real SRP composition tests cover these distinctions at one and two interfaces.

No existing differential drives firmware DA_GATE against processor
acmp_declaring_o. The existing MAAP differential covers the unchanged MAAP core
and passes; no broader predicate differential result is claimed.

## Pin scope, commits and reviews

Old: `405dc68310a18f669049ffc10cc23eef7300dcff`.
New: `70936b77dc41981e192438388cd0aced69954f18`.
The target tree equals reviewed #25 head `f13c9c16c2b300d158f980dd7c7f071dcb84df5b`.
All 45 changed paths belong to the union of authorized #19, #20 and #25.

| Stack PR | Merge | Exact-head review links |
|---|---|---|
| [#19](https://github.com/kebag-logic/tsn-c-stack/pull/19) | `51870377c5012766a8ea1d9798e3c499ca1060a3` | [review 1](https://github.com/kebag-logic/tsn-c-stack/pull/19#issuecomment-6085778617), [review 2](https://github.com/kebag-logic/tsn-c-stack/pull/19#issuecomment-6086078198) |
| [#20](https://github.com/kebag-logic/tsn-c-stack/pull/20) | `98dc9e3076714bebe113982ee18c3c1c496cf3c9` | [review 1](https://github.com/kebag-logic/tsn-c-stack/pull/20#issuecomment-6088675209), [review 2](https://github.com/kebag-logic/tsn-c-stack/pull/20#issuecomment-6088680624) |
| [#23](https://github.com/kebag-logic/tsn-c-stack/pull/23) | `1ba273540abbdf51ea5d235c0a7e81c0bcb5d475` | [review 1](https://github.com/kebag-logic/tsn-c-stack/pull/22#issuecomment-6116467700), [review 2](https://github.com/kebag-logic/tsn-c-stack/pull/22#issuecomment-6116469528) |
| [#25](https://github.com/kebag-logic/tsn-c-stack/pull/25) | `70936b77dc41981e192438388cd0aced69954f18` | [review 1](https://github.com/kebag-logic/tsn-c-stack/pull/25#issuecomment-6130754591), [review 2](https://github.com/kebag-logic/tsn-c-stack/pull/25#issuecomment-6130759174) |

PR #23 is the reviewed integration of the publication work already present in
the old pin, not an additional new parent behavior. Its ACMP source/header are
byte-identical to the old pin. Before #25, the only changed parent-built core
source is ADP from #19. The integration verdicts are explicitly separate in the
linked reviews; the [merge-bar record](https://github.com/kebag-logic/tsn-c-stack/pull/23#issuecomment-6116472923)
confirms both targets. No unreviewed or unmerged content was found.

#19 changes the ADP minimum from a partial header to 82 bytes, rejects nonzero
versions and CDL other than 56. Four parent tests above and their four mutants
cover those effects. #20 adds standalone entity generation; the parent keeps
its existing generator. Golden entity checks, generated-example controls and
the parent's per-shape entity tests pass. #25 adds the freshness/Listener core
predicate; its parent integration and controls are described above.

### Target-only commits

- `70936b77dc41981e192438388cd0aced69954f18` Gate ACMP declaration on a fresh probe or Listener (#25)
- `f13c9c16c2b300d158f980dd7c7f071dcb84df5b` Complete ACMP freshness contract mutation coverage
- `1edff3180c2ff435b855cc770fb8be371f2096b3` Protect ACMP freshness expiry across masked clock wraps
- `0868387deab21bd0db414424f306c7ea62498e29` Address ACMP freshness review findings
- `9ef7bd5281c0bb3f2967b11c5a5d8d74a75755d1` Prove ACMP freshness terms with mutation and target coverage
- `917201098395f1f1acc635ea1722e6c9a91a3ec0` Gate ACMP declaration on configured probe freshness or Listener demand
- `1ba273540abbdf51ea5d235c0a7e81c0bcb5d475` Integrate the ACMP publish port with main (#23)
- `98dc9e3076714bebe113982ee18c3c1c496cf3c9` Specify the entity in YAML and generate the cores' C configuration (#20)
- `51870377c5012766a8ea1d9798e3c499ca1060a3` Discard malformed ADP discovery frames (#19)

### Old-pin publication commits integrated by #23

- `405dc68310a18f669049ffc10cc23eef7300dcff` Identify ACMP cache assertions by owner and definition location
- `bc68ad8f3577e8f3dc24c4336e9b80a933df6c79` Require per-field ACMP publication cache coverage
- `f3dc2ae5bad02aa05a504b43c207e8b304d2bed5` Close ACMP publication review gaps
- `2dcbe91ead981591d5bfb652f6616f6edb325875` Publish ACMP sink state before responses and completion callbacks

### Exact changed-file set

| Stack path | Authorized PR file sets containing it |
|---|---|
| `.github/workflows/quality.yml` | #20 |
| `CMakeLists.txt` | #20 |
| `configs/ax7101.yaml` | #20 |
| `configs/compat/ax7101.json` | #20 |
| `configs/duplex.yaml` | #20 |
| `configs/listener.yaml` | #20 |
| `configs/talker.yaml` | #20, #25 |
| `docs/CODING_STANDARD.md` | #20 |
| `docs/DEVIATIONS.md` | #19 |
| `docs/ENTITY_YAML.md` | #20, #25 |
| `docs/PORTING.md` | #19, #20, #25 |
| `docs/REQUIREMENTS.md` | #19, #20, #25 |
| `docs/TESTS.md` | #19, #20, #25 |
| `docs/TRACEABILITY.md` | #19, #20, #25 |
| `docs/VERIFICATION.md` | #19, #20, #25 |
| `docs/requirements.json` | #19, #20, #25 |
| `examples/entities/ax7101/entity_config.c` | #20, #25 |
| `examples/entities/ax7101/entity_config.h` | #20 |
| `examples/entities/duplex/entity_config.c` | #20, #25 |
| `examples/entities/duplex/entity_config.h` | #20 |
| `examples/entities/listener/entity_config.c` | #20, #25 |
| `examples/entities/listener/entity_config.h` | #20 |
| `examples/entities/talker/entity_config.c` | #20, #25 |
| `examples/entities/talker/entity_config.h` | #20 |
| `examples/entity_roundtrip.c` | #20, #25 |
| `examples/entity_roundtrip.h` | #20, #25 |
| `examples/rv32/smoke.c` | #19, #20, #25 |
| `include/acmp.h` | #25 |
| `scripts/baremetal.py` | #20 |
| `scripts/conditional_policy.py` | #20 |
| `scripts/entity_selftest.py` | #20, #25 |
| `scripts/entity_yaml.py` | #20, #25 |
| `scripts/milan_entity.py` | #20 |
| `scripts/mutation.py` | #20 |
| `scripts/requirement_records.py` | #20, #25 |
| `scripts/static_analysis.py` | #19, #20 |
| `scripts/traceability.py` | #20 |
| `scripts/validate.py` | #20 |
| `src/acmp.c` | #25 |
| `src/adp.c` | #19 |
| `tests/coverage.ratchet` | #19, #25 |
| `tests/mutations.json` | #19, #20, #25 |
| `tests/test_acmp.cpp` | #25 |
| `tests/test_adp.cpp` | #19 |
| `tests/test_entity.cpp` | #20, #25 |

## Before/after image evidence

Release load bytes are text + read-only data + initialized data. The corrected
[ceiling](https://github.com/kebag-logic/tsn-c-stack/issues/24#issuecomment-6126295947)
is +2048 bytes; maximum measured parent growth is +1320. BSS and ELF file size
are recorded separately in `image-hashes.json`; no Debug ceiling is asserted.
Each pair uses the same compiler, flags and external runtime archives.
RV32I/ILP32 linked-image audits pass for every row.
The all-fabric default load image is byte-identical:

| Artifact | Before bytes | After bytes | Before and after SHA-256 |
|---|---:|---:|---|
| Default AX7101 1x1 BIOS binary | 52988 | 52988 | `5a2c937f40542238114c7bdd267d0eb2977a70a5cb0eb72889cc4ec3d1c0d4f3` |
| Default AEM descriptor binary | 7512 | 7512 | `4fc8d61582a965fe648abc0c15d0551153ff2b27f202d1fbc8319fbb4bdb396d` |

Generated HDL includes timestamps/source-path comments, and debug
ELF paths differ; raw HDL and debug ELF equality is not claimed. No bitstream or
hardware measurement was made. Firmware fixtures are link/audit images, not a
claim that every experimental composition fits a shipping memory placement.

| Composition / shape | Load before | Load after | Growth | ELF SHA-256 before | ELF SHA-256 after |
|---|---:|---:|---:|---|---|
| ADP-ACMP-MAAP / `endstation_arty_4x4` | 34820 | 35824 | +1004 | `8c27ee19b7a4f0a6266834c43c50d8a397469c612fe86860ecc2296ae44ebb5e` | `e0cfb018b6a36bb1c36c9816c0b5608e7ad89462e0bc8b911e6455e6313a28ab` |
| ADP-ACMP-MAAP / `endstation_arty_8ch` | 34820 | 35824 | +1004 | `b7976d5cc2e0bc8889bbe471472e4817a6368df9a31d48ec8c2e8a1d63c23af7` | `2d7e9190a2d2b920c38ed67a459715dd465b31659dd379af8806bf3ed56fe9e5` |
| ADP-ACMP-MAAP / `endstation_arty_current` | 34812 | 35816 | +1004 | `b119b2b56911120eeb424276525ca53d2e34340bf169bbb4a788efe65cb8a092` | `001fbd8a7cf9a8c0bed98d761a98f32c52d5252e7bb2fd017d4b67f576c6ee65` |
| ADP-ACMP-MAAP / `endstation_ax7101_1x1_tdm8` | 34836 | 35840 | +1004 | `5a4086ce0245a5e2ad198aa0db56e62b982b7c4c6d177fe4929dca4da6b2dfff` | `a41dcaf35c23a13370af3deeea8589eb41500b2dfa395012cdb8fe30457b927b` |
| ADP-ACMP-MAAP / `endstation_ax7101_8x8` | 34840 | 35844 | +1004 | `acb380ee815698bcd99f31920c09e55c3e93d44d7d09b4d1ae8f2d6a2a03c1bd` | `883b7d033cd9d01d0556c9f56df8446e5c0216afa98e75767d57d521bf3dc8d0` |
| SRP / `endstation_arty_4x4` | 50430 | 51734 | +1304 | `228c4d2d4da86158199c99b08a0b895661fec07eb56c9554fc2ad32ee0f276c4` | `4ac42f3bab06478e968ff5967123836ffe7c44b7421b0c1e23c462ee9e189552` |
| SRP / `endstation_arty_8ch` | 50430 | 51734 | +1304 | `fed8b54f96ec1c60797841de476947215550b234b3785442e88e96e1b8ed4be8` | `2eb0db3e4585a368f562e2e0bd55bfdf5af51d956d170528bc01329d091069e4` |
| SRP / `endstation_arty_current` | 50006 | 51218 | +1212 | `7c8ecec43b7a6f829490d84ba46ef485265965188329ee4f412b8eae86d8d245` | `5ca38cd5b8ef95100954a6b8a452b9f375973842594306d4692e340867cd7664` |
| SRP / `endstation_ax7101_1x1_tdm8` | 50362 | 51674 | +1312 | `db0fb58e7ebfec18465210871c83e560c8f71f4149932775bf8423f5b7becb19` | `c9614ded233748d6451b4747bde58f3f800ca48cc4924c76076e4355a91c48c3` |
| SRP / `endstation_ax7101_8x8` | 50466 | 51786 | +1320 | `b9bf08715abcd58e7b7a66781e1e27e9a6762d9560366f68df5c9b2b42487af4` | `08651209017bfe204cdddd43655c22d9630e230730629e27915203d0418d9341` |
| SRP-AECP / `endstation_arty_4x4` | 100066 | 101370 | +1304 | `82e5ce706c7736fa6778c6477a5d43233415fac26efc851aaeb2776146ce34cf` | `c9ab051aa615d8f763af631b5902fba44c838ffcb1eda504b561cfe8800fe422` |
| SRP-AECP / `endstation_arty_8ch` | 105818 | 107122 | +1304 | `c2799ea46a854c45e54992800c3cdc93175a364193d41d37f2eefacb966d2118` | `5fa5d9b7322472d4e164a43fff82b6c0c4e6008274819157c233be724cc458d1` |
| SRP-AECP / `endstation_arty_current` | 94338 | 95550 | +1212 | `7f2bac9275054548497234c7d8c5042c1525c822775f1391a394d7abb65ff4dc` | `6e5ba04f811205be89167cf4505c14f5c3752844023fe1edc5c4c682082f82ed` |
| SRP-AECP / `endstation_ax7101_1x1_tdm8` | 96534 | 97846 | +1312 | `74a12209e0301a9a7313861e6e944f972a3ba84374a147e476cf2f12814fdcda` | `e39a024245f86e8bceb9a472d428250a3aede53d4bf36844920deb38173d7ee2` |
| SRP-AECP / `endstation_ax7101_8x8` | 110250 | 111570 | +1320 | `1721078bbde9510b60ba82f4c4cf7cc0639709bc3b419c0aad1260eb407d5d99` | `9394599a0abf68b9d587f5def0b6c1ce60703cca4bcd36032983b6689556a061` |

Image controls reject a one-byte default-image change; the growth boundary
accepts +2048 and rejects +2049. `image-controls.json` records these controls.

The basic three-protocol image uses its repository arithmetic helpers. The
larger SRP/AECP fixture links generated minimal runtime archives. The AECP
runtime was built with stack protection disabled because this freestanding link
has no stack protector runtime; the same archive is used for both sides.
An initial link with the SDK's default stack protector failed on the baseline
as well. It is diagnostic evidence, not a firmware regression or a passing gate.

## Coverage

`fw_coverage.py --check --jobs 4` passes for 30 files. Raw counters below
preserve excluded unreachable lines/arcs; adjusted coverage is 100%/100% for
each file. No new exclusion was introduced. The one obsolete composition arc
was removed because that conditional no longer exists.

```text
file                                                 lines    branches   after exclusions
sw/firmware/ctrl/acmp/acmp_mbx.c                  81/81       28/28      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/acmp/acmp_nvm.c                  38/38       10/10      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/adp/adp_mbx.c                    83/83       38/40      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp.c                     357/357     308/308     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp_commands.c            424/424     362/362     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp_image.c                77/77       80/80      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp_maps.c                222/222     290/290     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp_mbx.c                 101/101      40/40      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp_nvm.c                 102/102      86/86      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp_state.c                63/63       69/69      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/app/ctrl_app.c                   46/47       43/46      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/app/ctrl_app_aecp.c             107/107      64/64      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/app/ctrl_app_srp.c               87/87       70/70      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/loop/ctrl_loop.c                101/101      62/62      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/maap/maap_csr.c                  39/39       18/18      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/maap/maap_mbx.c                 129/129      84/84      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/mbx/mbx.c                       243/243     102/102     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/mbx/mbx_wire.h                   15/15       12/12      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/plat/mbx_plat_mmio.c             10/10        0/0       lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/port/ctrl_debug.c                19/19        6/6       lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/port/ctrl_pool.c                 99/99       60/60      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/port/shlan_port.c                22/22        6/6       lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/srp/srp_mbx.c                   543/543     486/486     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl_nvm/nvm_klj2.c                  198/199     106/110     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl_nvm/nvm_store.c                 434/434     259/266     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c    100/100      63/64      lines 100.00 %  branches 100.00 %
third_party/tsn-c-stack/include/wire.h            10/10        2/2       lines 100.00 %  branches 100.00 %
third_party/tsn-c-stack/src/acmp.c               792/792     392/392     lines 100.00 %  branches 100.00 %
third_party/tsn-c-stack/src/adp.c                206/208      99/106     lines 100.00 %  branches 100.00 %
third_party/tsn-c-stack/src/maap.c               209/209     140/140     lines 100.00 %  branches 100.00 %
firmware coverage: PASS (30 files)
```

## Gate and mutation ledger

| Gate | Command | Result | Planted control |
|---|---|---|---|
| Normal firmware/RV32 suites | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 4` | 60 arms, 1534 reported checks; rc 0 | Missing/duplicate shard members and invalid shard combinations refused; every behavior has mutation campaign below |
| Firmware coverage | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4` | 30 files, adjusted 100% lines/branches; rc 0 | --selftest: 29/29 planted missing/wrong exclusion cases |
| Host/RV32 boundary | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator` | 2852 compiled sources / 3082 invocations; rc 0 | 112 boundary, 120 pin and 4 figure controls, 0 misbehaved |
| Verilator boundary and live builders | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator` | 829 compiled sources / 926 invocations; rc 0 | 6 boundary, 120 pin and 4 figure controls, 0 misbehaved; mailbox co-simulation, MAAP differential and AECP wire gates run |
| Linked-image audit | `python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32` | 33/33 checks; rc 0 | M/C/A/F/privileged opcodes, ABI/header corruption, incompatible runtime and recursive helper refused |
| Five-shape image matrix | `python3 sw/firmware/ctrl/test/ctrl_image.py --base d40e4e9827be2516f8f34b9d65f0a483fff2194c --shape endstation_arty_4x4 --shape endstation_arty_8ch --shape endstation_arty_current --shape endstation_ax7101_1x1_tdm8 --shape endstation_ax7101_8x8` | 10 Release links audited; rc 0 | Linked-image controls above; +2048 boundary accepted and +2049 refused |
| Mailbox generator | `python3 sw/mailbox/gen_mailbox.py --check --crosscheck --selftest` | Current generated bytes; rc 0 | Missing/malformed contract fields and generated drift controls |
| Source lists | `python3 scripts/check_rtl_source_lists.py` | 108-file closure, 4/4 consumers, 42/42 processor tops; rc 0 | --selftest: 50/50 controls, including each consumer with one source removed |
| SoC source lists | `python3 scripts/check_soc_sources.py` | Live registered sources resolve; rc 0 | --selftest: 25/25 controls, including omitted live CDC source |
| Evidence readers | `python3 scripts/measure_test_evidence.py --check` | Ratchet and current reader dispositions pass; rc 0 | --selftest: 105/105 controls, including unexecuted mutation arms and unexplained readers |
| RTL lint | `python3 scripts/lint_rtl.py --check --self-test --jobs 2` | 90 findings <= ratchet 90; rc 0 | 8 pragma/resolution controls reject malformed waiver forms and missing source trees |
| Standalone stack | `python3 third_party/tsn-c-stack/scripts/validate.py --jobs 2` | 27 component statuses rc 0 | 388/388 core/entity plants; test-removal, unknown-test and baseline-failure campaign controls; each source/metadata gate selftest |
| Documentation paths | `python3 scripts/check_doc_paths.py` | 978 citations and 10 line anchors; rc 0 | Disposable fixture: valid passes, missing path and past-end anchor each return 1; driver rc 0 |
| docs | `python3 scripts/docs_check.py` | rc 0 | docs_check built-in scrub/routing plus --selftest |
| doc-style | `python3 scripts/check_doc_style.py` | rc 0 | check_doc_style --selftest |
| cpp-idiom | `python3 scripts/check_cpp_idiom.py` | rc 0 | check_cpp_idiom --selftest |
| python-idiom | `python3 scripts/check_py_idiom.py` | rc 0 | check_py_idiom --selftest |
| em-dash | `python3 scripts/check_em_dash.py --base d40e4e9827be2516f8f34b9d65f0a483fff2194c` | rc 0 | check_em_dash --selftest |
| toc | `python3 scripts/gen_toc.py --check` | rc 0 | gen_toc --selftest |
| submodule-docs | `python3 scripts/check_submodule_docs.py` | rc 0 | check_submodule_docs --selftest: wrong table pin and diagram boundary |
| hygiene | `python3 scripts/check_hygiene.py --check` | rc 0 | check_hygiene --selftest |
| tally-controls | `python3 sw/firmware/gtest/tally_selftest.py` | rc 0 | tally_selftest.py: false green, missing test and failure accounting |
| diagram | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | rc 0 | submodule_boundaries.gen.py --selftest: valid but wrong PNG pixels |
| Control mutations | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 1/4 --jobs 4` | 519/519 caught; rc 0 | Every named defect reaches its assigned assertion, including all F3b/ADP arms |
| AECP mutations | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 2/4 --jobs 4` | 76/76 caught; rc 0 | Mailbox, descriptor, state and debug contract plants |
| SRP mutations | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 3/4 --jobs 4` | 202 two-interface + 76 one-interface plants caught; 2 pin controls; rc 0 | Asking Failed, Listener withdrawal and wrong-interface forwarding; poisoned source and wrong checkout pin controls |
| Publication census | `python3 sw/mailbox/publication_census.py --check --selftest --jobs 2` | 234 checks over six elaborated shapes; rc 0 | 120/120 controls; every one of 31 removed rules lets its own plants through |
| Stack RV32 | `python3 third_party/tsn-c-stack/scripts/baremetal.py --jobs 2` | Debug and Release build, import/ABI audit and emulator smoke; rc 0 | Smoke exercises ADP refusal/backpressure, ACMP restore/rollback, MAAP bounds and four entity round trips |
| Composed SRP/AECP images | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/$SHAPE.yaml --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a" --output "$WORK/$SHAPE"` | 20 before/after links over five shapes; rc 0 | Linked-image forbidden instruction/ABI controls; exact image and +2048/+2049 comparisons |

### Mutation totals

| Campaign | Caught | Escaped/errors | Receipt |
|---|---:|---:|---|
| Parent control | 519 | 0 | `mutations-control.csv` |
| Parent AECP | 76 | 0 | `mutations-aecp.csv` |
| Parent SRP, two interfaces | 202 | 0 | `mutations-srp.csv` |
| Parent SRP, one-interface subset | 76 | 0 | `mutations-srp.csv` |
| Standalone stack | 388 | 0 | `mutations-stack.csv` |
| Publication census rule removal | 31 | 0 | `evidence/publication-census-verified.log` |

SRP additionally rejects two corrupted-pin controls. Normal suite dispatch is
60 arms and reports 1534 checks. The current shard inventory is 936 invocations
with sizes 60/520/77/279; baseline invocations explain the difference from the
mutant counts. The SRP/AECP runs preceded the extra control-table nonreentry
plant; their own source, tests and mutation tables did not change afterwards.
The final normal/control runs prove the updated complete shard inventory.

### Predicate and adopted-pin controls

| Plant | Assigned test | Required failing assertion | Result |
|---|---|---|---|
| `f3b-query-inside-allocation` | `MaapHost.DaGateIsPublishedBeforeEachAllocationIsReported` | declaration query stays outside MAAP callbacks | CAUGHT |
| `f3b-composition-owner` | `AcmpMailbox.F3bComposedGateExpiresAfterIdleTickWake` | composed mailbox publishes the accepted probe demand | CAUGHT |
| `f3b-idle-tick` | `AcmpMailbox.F3bComposedGateExpiresAfterIdleTickWake` | service tick wakes an idle platform for freshness expiry | CAUGHT |
| `f3b-config-interval` | `AcmpMailbox.F3bComposedGateExpiresAfterIdleTickWake` | mailbox composition supplies the Milan freshness interval | CAUGHT |
| `f3b-fresh-probe-arm` | `MaapHost.DaGateFreshProbeDeclaresOnlyItsSource` | fresh probe opens only its configured source | CAUGHT |
| `f3b-listener-arm` | `MaapHost.DaGateListenerDeclaresWithoutProbe` | registered Listener opens the gate without a probe | CAUGHT |
| `f3b-no-demand-arm` | `MaapHost.DaGateWithoutDemandStaysClosed` | neither probe nor Listener keeps the gate closed | CAUGHT |
| `f3b-expiry-arm` | `MaapHost.DaGateProbeExpiresAtFifteenSeconds` | probe expires at 15000 milliseconds without a Listener | CAUGHT |
| `f3b-expiry-refresh` | `MaapHost.DaGateProbeExpiresAtFifteenSeconds` | probe expires at 15000 milliseconds without a Listener | CAUGHT |
| `pin-adp-short-discovery` | `AdpAdapter.PinRejectsEveryTruncatedDiscovery` | malformed discovery changes only the discard count | CAUGHT |
| `pin-adp-discovery-version` | `AdpAdapter.PinRejectsUnsupportedDiscoveryVersions` | malformed discovery changes only the discard count | CAUGHT |
| `pin-adp-discovery-length` | `AdpAdapter.PinRejectsWrongDiscoveryControlLength` | malformed discovery changes only the discard count | CAUGHT |
| `pin-adp-valid-discovery` | `AdpAdapter.PinAcceptsCompleteDiscoveryThroughMailbox` | complete discovery restarts advertising through the mailbox | CAUGHT |
| `four-way-f3b-listener-not-forwarded` | `AcmpMailbox.F3bListenerRegistrationControlsItsOwnGate` | registered Listener controls only its source interface gate | CAUGHT |
| `f3b-listener-wrong-interface` | `AcmpMailbox.F3bListenerRegistrationControlsItsOwnGate` | registered Listener controls only its source interface gate | CAUGHT |
| `four-way-f3b-asking-failed-excluded` | `AcmpMailbox.F3bListenerRegistrationControlsItsOwnGate` | registered Listener controls only its source interface gate | CAUGHT |
| `four-way-f3b-withdrawal-stale` | `AcmpMailbox.F3bListenerRegistrationControlsItsOwnGate` | registered Listener controls only its source interface gate | CAUGHT |

The existing publication plants remain caught: skipped or late gate writes,
invalid DA, one source short, wrong interface, and a source beyond the block.
The MAAP callback source guard proves no synchronous core query is introduced.
The fixed freshness window and idle wake each have independent composition plants.

The original one-clock overrun plant no longer exceeded the new conservative
bound; it now adds one more access than the funded source-query allowance.
The original constant-true no-demand plant made its local pointer unused and
failed compilation; the corrected plant preserves the operand references and
reaches the intended failing assertion. Neither change weakens a test.
Earlier tool-setup and stale-anchor diagnostics are superseded by the complete
zero-status runs above; they are not reported as passing evidence.

Standalone core coverage independently reports:

```text
file                                                 lines    branches   after exclusions
include/wire.h                                    10/10        2/2       lines 100.00 %  branches 100.00 %
src/acmp.c                                       792/792     392/392     lines 100.00 %  branches 100.00 %
src/adp.c                                        205/207      97/104     lines 100.00 %  branches 100.00 %
src/maap.c                                       209/209     140/140     lines 100.00 %  branches 100.00 %
```

## Reproduction

Use the final commit with clean pinned submodules. CPython 3.12.3 matches the
hosted version. Parent host coverage used GCC/gcov 16.2.1 and GTest 1.18.0.
Standalone stack validation used GTest 1.14.0 and Clang/clang-tidy 18.1.3.
The parent RV32 fixture used GCC 14.3.0 from the pinned SDK; Release flags are
`-march=rv32i -mabi=ilp32 -Os -DNDEBUG -ffreestanding -fno-stack-protector`.
Verilator was pinned 5.050; the census used sv2v 0.0.12 and Yosys 0.66.
The installed Clang wrapper referenced removed scratch, so private wrappers
selected the existing compiler and matching resource/C++ headers. Neither shared
installations nor the pinned stack were modified. Runtime source and command
manifests accompany this report; binaries and installed packages remain outside it.

Set `WORK` and `TMPDIR` to disk-backed scratch, `MILAN_RV32_CC` to the pinned
compiler, `VERILATOR` and `SV2V` to the pinned executables. The four parent
campaigns and full local command list are in `PR-BODY.md`. Every recorded gate
ran as a foreground command without a pipe; commands below use plain shell.

```sh
python3 sw/firmware/ctrl/test/ctrl_image.py --base d40e4e9827be2516f8f34b9d65f0a483fff2194c --shape endstation_arty_4x4 --shape endstation_arty_8ch --shape endstation_arty_current --shape endstation_ax7101_1x1_tdm8 --shape endstation_ax7101_8x8 --out "$WORK/images"
python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32 --out "$WORK/image-controls"
python3 sw/firmware/ctrl/test/ctrl_image_runtime.py --picolibc "$PICOLIBC" --compiler-rt "$COMPILER_RT" --litex-software "$LITEX_SOFTWARE" --output "$WORK/runtime"
```

For the complete AECP composition, generate a second runtime using the same
compiler with `-fno-stack-protector` appended, then restore `MILAN_RV32_CC` to
the raw compiler for the firmware build. The runtime archive digest/size table
is `runtime-artifacts.json`. Its provenance records every source/dependency,
command and digest. The basic SRP rows use `runtime`; SRP-AECP rows use
`runtime-freestanding`, identically on both sides.

The first command above exports the baseline source and its own old stack pin.
For each of the five shapes, run these two commands, then repeat with
`--with-aecp` and the freestanding runtime archives:

```sh
python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config "configs/$SHAPE.yaml" --ctrl-source "$WORK/images/base-tree/sw/firmware/ctrl" --stack-source "$WORK/images/base-tree/tsn-c-stack" --libc "$WORK/runtime/libc.a" --compiler-runtime "$WORK/runtime/libcompiler_rt.a" --output "$WORK/srp-before/$SHAPE"
python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config "configs/$SHAPE.yaml" --libc "$WORK/runtime/libc.a" --compiler-runtime "$WORK/runtime/libcompiler_rt.a" --output "$WORK/srp-after/$SHAPE"
```

The all-fabric pair used separate baseline/candidate source exports with the
same dependency pins except the authorized stack move. The ordinary entity
builder generated `endstation_ax7101_1x1_tdm8`. The SoC invocation was the
following in each export, with its own `$ENTITY` and `$FABRIC_OUT`, without
`--build` or `--load`. `PYTHONHASHSEED=0` and `SOURCE_DATE_EPOCH=1791849600` were
shared. The call limited the build's CPU count to eight.

```sh
python3 -c 'import os,runpy,sys; os.cpu_count=lambda:8; sys.path.insert(0,os.path.abspath("sw/litex")); sys.argv[0]=os.path.abspath("sw/litex/milan_soc.py"); runpy.run_path(sys.argv[0],run_name="__main__")' --board ax7101 --milan-clk-freq 50e6 --gtx-tx-invert --floorplan --eth-port e1 --no-i2s-playback --no-render-lpf --num-streams 1 --audio-interface tdm8 --audio-interface-master --audio-interface-render 8 --talker-wire-chans 8 --loopback-lane --fabric-gptp --gptp-ingress-lat-ns 656 --gptp-egress-lat-ns 219 --cpu vexiiriscv --software-profile baremetal --xlen 32 --full --with-spiflash --flashboot baremetal --timing-opt --l2-bytes 0 --uart-baudrate 115200 --cpu-count 1 --entity-gen-dir "$ENTITY" --output-dir "$FABRIC_OUT"
```

Generated repository files were regenerated only with their generators:

```sh
python3 sw/mailbox/gen_mailbox.py --write
python3 docs/diagrams/submodule_boundaries.gen.py
```

## Delivery and remaining merge duties

The candidate is committed and no work remains running. `PR-BODY.md` is prepared
from the repository template. The evidence index records SHA-256 and byte size;
no binary, toolchain, installed package, tree export or file over 200 KB is
included. The generated diagram remains in the repository, with its digest and
size recorded in `candidate-files.json`.

Independent reviews and their lens ledger remain pending. No author verdict is
an approval. No new-head hosted context or local workflow replica was started:
this assignment prohibits pushing or changing a PR. Full repository merge
validation, the live-dev integration, hosted contexts and post-merge containment
remain the integration owner's duties. This handoff claims the executed gates
above, not a full repository sweep, synthesis, hardware timing or RAM-fit proof.

A new REVIEW READY comment with this head is the final authorized public action.
No prior issue or PR comment was edited or deleted.


## Round 2

Status: STOP only on the required new-head hosted proof. Local corrections and
all affected local gates are complete. No push is authorized or performed.
Candidate: `651ccb5aea1bc4d99f356503c188947d39e0c9e4`.
Resume head: `db29bdd07529fbc697b7956827092f64b1241714`.

The [round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6153927545)
requires hosted `rtl-fast`, including `firmware-boundary` and
`firmware-verilator`, to pass at the new head, and also says not to push.
PR #736 still points at the resume head. Therefore hosted success at this local
candidate is unproven; local success is not substituted for that requirement.
The R582-1 and R583-1 findings need independent re-review at the corrected head.
The author publishes no review verdict or clean-lens ledger.

### Commits and changes

| Commit | Change |
|---|---|
| `d8cae51e0f0813a69f45d30ba2506b7bb00800cb` | Publish the authoritative per-source declaration predicate |
| `2748ed52d60c1c80b9a47665b35b34e8e760edbc` | Prevent scratch repository maintenance from racing pin controls |
| `651ccb5aea1bc4d99f356503c188947d39e0c9e4` | Verify service bounds and correct the adopted stack documentation |

| File:line | Round 2 change |
|---|---|
| `sw/firmware/ctrl/maap/maap_mbx.c:36` | Cache the return value of `acmp_declaring` outside MAAP callbacks; retain allocation and interface gating |
| `sw/firmware/ctrl/maap/maap_mbx.h:45` | State that the cached predicate includes source destination validity |
| `sw/firmware/ctrl/maap/README.md:127` | Explain predicate ownership, gate-before-report ordering and next-poll validity updates |
| `sw/firmware/ctrl/mbx/mbx.h:95` | Describe DA_GATE as the allocated source's core predicate |
| `sw/firmware/ctrl/test/test_maap_mbx.cpp:47` | Separate source validity from MAAP range validity; preserve callback-order/reentry assertions; add invalid-source acquisition at line 303 |
| `sw/firmware/ctrl/test/test_acmp_mbx.cpp:490` | Exercise both demand arms and false/true/false source validity; compare every interface's bit with the core at IF1 and IF2 |
| `sw/firmware/ctrl/test/ctrl_mutants.py:533` | Restore the rejected source-validity bypass as a mutation; require five named tests to kill it; existing arm mutations now target the authoritative core expression |
| `sw/firmware/ctrl/test/ctrl_build.py:194` | Supply both disabled maintenance settings on every helper Git command; admit only those exact local values |
| `sw/firmware/ctrl/test/ctrl_pin_env.py:62` | Centralize scratch init/clone with both settings persisted, including the clone command itself |
| `sw/firmware/ctrl/test/ctrl_pin_store.py:105` | Use that constructor for loose-object, superproject and sparse-index controls |
| `sw/firmware/ctrl/test/ctrl_pin.py:735` | Ignore only FileNotFoundError during fresh-clone removal; other errors propagate; run lifecycle controls |
| `sw/firmware/ctrl/test/ctrl_pin_lifecycle.py:94` | Six executable controls cover configuration, loose fetch, disappearing files, permission errors and I/O errors |
| `sw/firmware/ctrl/test/ctrl_configs.py:74` | Register the new lifecycle module with the boundary gate's own modules |
| `sw/firmware/ctrl/README.md:199` | Document exact configuration exceptions, deletion policy and 126 pin controls |
| `sw/firmware/ctrl/test/ctrl_service_bounds.py:80` | Compile composition headers at both interface counts and check every published dependent row and conclusion |
| `sw/firmware/ctrl/test/ctrl_arms.py:18` | Expose the service-bound arm through the normal arm registry |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py:162` | Run that arm in the normal population, preserving exhaustive shard dispatch |
| `docs/design/MAILBOX_SPLIT.md:755` | Correct all four bounds and access thresholds; both event envelopes exceed 10 ms |
| `docs/reference/SUBMODULES.md:256` | State that the adopted pin includes #19's ADP discovery refusals |
| `sw/firmware/gtest/README.md:246` | Update five stack permalinks on four lines to the adopted pin; wording only |

The exact source predicate is `dest_mac_valid && (answered || listener_registered)`
after the core observes freshness expiry. The adapter additionally requires a valid
allocation, the source within its allocation count and its configured interface.
It queries the core in dispatch, never synchronously from a MAAP callback.
Each interface's gate is still written before that interface's allocation report.

### Predicate and harness controls

| Control | Evidence / result |
|---|---|
| Invalid source DA with valid MAAP and registered Listener | `AcmpMailbox.F3bListenerRequiresSourceDestination`; IF1 and IF2 pass, core=false and gate=false |
| Invalid source DA with valid MAAP and answered probe | `AcmpMailbox.F3bProbeRequiresSourceDestination`; IF1 and IF2 pass, core=false and gate=false |
| Valid source positive and subsequent invalidation | Both tests run false/true/false and compare every published interface bit with the core |
| Allocation cannot supply source validity | `MaapHost.DaGateWaitsForSourceOwnerAfterAllocation`; gate closed at report, opens on the next poll after source validity becomes true |
| Restored old bypass | `f3b-source-validity` caught by both composition tests at both interface counts and the allocation test |
| Other F3b and publication predicates | 16 selected plants caught; the full 520-entry campaign also passes |
| Unchanged review probe | `probe_owner.cpp` SHA-256 `075a798733cc16164568123cdfc7911e967ab2b27822c48cecd4e93b1fcd0d82`, 2108 bytes; rc 0, both invalid-source assertions pass |
| Missing command gc or maintenance switch | Both harness mutations killed by the command-scope configuration control |
| Missing clone gc or maintenance switch | Both harness mutations killed by the persisted configuration control |
| Rethrow disappearing-file error | Killed by the real removal race control |
| Swallow all deletion errors | Killed by the permission-error control; I/O errors are independently exercised |
| Stale service bounds | 38/38 missing or altered numeric/conclusion plants caught; 47 total checks pass |

The probe source is byte-for-byte equal to the reviewer branch at
`92d917b89f7b150c8ee9027efd50ad6f131fad34`. Its driver was adjusted only to return
the corrected test's result: the original driver returns success for reproducing
the defect. The probe itself was unchanged. Receipts and portable reproduction
drivers are under `round2/`; this distinction is recorded in `owner-probe.json`.

### Pin integrity

No round 2 gitlink move occurred. The target remains
`70936b77dc41981e192438388cd0aced69954f18`. Its tree equals the reviewed #25 head
`f13c9c16c2b300d158f980dd7c7f071dcb84df5b` exactly. The 24 files in the merge's
first-parent delta equal #25's recorded file set. The original old-to-target
45-file delta is unchanged and belongs to the corrected authorized #19/#20/#25
scope described in the earlier pin table. The original exact-#25-only claim is
not revived. `round2/pin-integrity.json` records both file lists and the tree hash.
The stack checkout and its public origin were independently verified; it is clean.

### Image evidence

The following table supersedes the round 1 image table. Before is `d40e4e98`
with its own stack pin; after is the round 2 firmware. Every pair was rebuilt
with equal compiler flags and runtime archives, and passed its linked-image
audit. All 15 images use 16 fewer load bytes than round 1. Growth over the
original baseline is 988 to 1304 bytes, below the unchanged +2048 Release ceiling.
Raw ELF byte sizes, sections and hashes are in `round2/image-hashes.json`.
The comparison accepts +2048 and rejects +2049.

| Composition / shape | Load before | Load after | Growth | ELF SHA-256 before | ELF SHA-256 after |
|---|---:|---:|---:|---|---|
| ADP-ACMP-MAAP / `endstation_arty_4x4` | 34820 | 35808 | +988 | `f70be6b729d203ade7fb75e832d1ca0b1d1d9ba99f03e746cc2907174ec9cce4` | `9060072441800c7ceb2d01cab468eb6e1213cbc376fac9540135ccfcb676ccd9` |
| ADP-ACMP-MAAP / `endstation_arty_8ch` | 34820 | 35808 | +988 | `eb5dfe04250400df1a0546c4f52096cfbd4e8f0e7abc777388e6d55cf64802e6` | `91ed8f02cd8cfc0fc05ba9a0791c16ddf98afeb5da9132961b3addf8048fa82b` |
| ADP-ACMP-MAAP / `endstation_arty_current` | 34812 | 35800 | +988 | `9600824e12c1890edebeee455afe2244dc4fa9166c463fbb01591e284fe1f441` | `7e398af8cfb393a948af2d618af7a900955e2deb7127459c803ba5c8167b622f` |
| ADP-ACMP-MAAP / `endstation_ax7101_1x1_tdm8` | 34836 | 35824 | +988 | `ee7991b0b767b331d1b9fc84972b5a610ec0e9ae521ddf20689d9b4df4a9f33c` | `1c422c8096ebeaa109827ef29743322b8328b58e933d0917cfddc8410c1f1390` |
| ADP-ACMP-MAAP / `endstation_ax7101_8x8` | 34840 | 35828 | +988 | `1b17baeb51ab66d3eeaeb97e5136fc8f516361ca6d99900d490a7953689e7018` | `6a00a71d9d67fb5f8848a0e2dcc064551fcc199bd8985e3d83263f4bfa72d760` |
| SRP / `endstation_arty_4x4` | 50430 | 51718 | +1288 | `c5ccb78e4bb18a7d4ea8926564524d4b865bd0a955738c5d35b505f8bf5b8a3d` | `80bf935cc69ef7da26e74ef918da6fdf92332217d15e769271e100939a1d7863` |
| SRP / `endstation_arty_8ch` | 50430 | 51718 | +1288 | `6e265c3b796fabd9edae6f5e52baabb4845513e9bccba2409a053915d6ebccd5` | `512ca8bd22de32cae8192935f1f8565cd1326555a4fdc43cdff472d90f9f530f` |
| SRP / `endstation_arty_current` | 50006 | 51202 | +1196 | `2d0d89202c0e9d790cc247cabbbe9d96b9cc731cc3621a17345ec5e963d1265a` | `1bf47d8f359a0474d03c795b689e699aab495cc7576347f3ee5a81c7c99e6cbe` |
| SRP / `endstation_ax7101_1x1_tdm8` | 50362 | 51658 | +1296 | `863666a08cdc823e6599e52b042f84ce4eaac296625471faac69a55209fb3121` | `d3244df6176809f6fdebd8b36c8c7830daa48ed1e2de4f68247ca61aca000a08` |
| SRP / `endstation_ax7101_8x8` | 50466 | 51770 | +1304 | `ea60f397fef49c802bbf3c1e0e96b274f215d18e0023f39f9f2c4a5d4f4d25ca` | `5a22cedcb18f25374f480c6bfa596cf333169f9f991acc3bc480d1361a4e9b98` |
| SRP-AECP / `endstation_arty_4x4` | 100066 | 101354 | +1288 | `180088cdc4a37cdf1281d9d64bce2d4d60ba040adafdbc8907ceafdd5dfbbf73` | `338f6cc8303c03035fdc52541284bb512b60f7b2c5a0d93d7429228cf490ed12` |
| SRP-AECP / `endstation_arty_8ch` | 105818 | 107106 | +1288 | `a9832cff9c849e539cbeedd71dc5fd98edffa340f052d7b7369fa4ff90ae4c20` | `536445f1db8f5d1f21336a67bb175fe5234f56629138d4f5ab947fd916484fa4` |
| SRP-AECP / `endstation_arty_current` | 94338 | 95534 | +1196 | `caa8874683dd01abaf7aa6673015b03d9e35d753810b36a0b2f1cc408095ebfa` | `70c3c14eb67c942c842e93e5f42849b5c881060ffd5cbeac95c7b2796519f79b` |
| SRP-AECP / `endstation_ax7101_1x1_tdm8` | 96534 | 97830 | +1296 | `0c9a9ff7f516df33e6a5f3a9f885489bb1705943fd0e48a65d7493d848c665f6` | `01affe2224817a9b098435415a7bfd7d99ab3b1c8a44e058c67ca48288b79e3a` |
| SRP-AECP / `endstation_ax7101_8x8` | 110250 | 111554 | +1304 | `0336f8328dd2aa5e19ea065dbb5694ed9b3490c90dd9c5abc8216f531aff3f2f` | `7698a20ec3e9a520c33b260af5be114f10799518d1754c244b47540ccfededa5` |

| All-fabric artifact | Before / round 1 / round 2 bytes | SHA-256, identical on all three |
|---|---:|---|
| AX7101 1x1 BIOS binary | 52988 / 52988 / 52988 | `5a2c937f40542238114c7bdd267d0eb2977a70a5cb0eb72889cc4ec3d1c0d4f3` |
| AEM descriptor binary | 7512 / 7512 / 7512 | `4fc8d61582a965fe648abc0c15d0551153ff2b27f202d1fbc8319fbb4bdb396d` |

The default firmware was rebuilt in a separate scratch checkout. Neither a
bitstream nor a hardware timing/RAM-fit claim is part of this evidence.
One-byte corruption of either all-fabric artifact fails the identity comparison.
All runtime archives and large artifacts remain in scratch; only their hashes
and sizes are included in the packet.

### Coverage and mutation tables

The coverage exclusions are unchanged. Raw counts and adjusted percentages:

```text
file                                                 lines    branches   after exclusions
sw/firmware/ctrl/acmp/acmp_mbx.c                  81/81       28/28      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/acmp/acmp_nvm.c                  38/38       10/10      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/adp/adp_mbx.c                    83/83       38/40      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp.c                     357/357     308/308     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp_commands.c            424/424     362/362     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp_image.c                77/77       80/80      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp_maps.c                222/222     290/290     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp_mbx.c                 101/101      40/40      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp_nvm.c                 102/102      86/86      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp_state.c                63/63       69/69      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/app/ctrl_app.c                   46/47       43/46      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/app/ctrl_app_aecp.c             107/107      64/64      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/app/ctrl_app_srp.c               87/87       70/70      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/loop/ctrl_loop.c                101/101      62/62      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/maap/maap_csr.c                  39/39       18/18      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/maap/maap_mbx.c                 127/127      82/82      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/mbx/mbx.c                       243/243     102/102     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/mbx/mbx_wire.h                   15/15       12/12      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/plat/mbx_plat_mmio.c             10/10        0/0       lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/port/ctrl_debug.c                19/19        6/6       lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/port/ctrl_pool.c                 99/99       60/60      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/port/shlan_port.c                22/22        6/6       lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/srp/srp_mbx.c                   543/543     486/486     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl_nvm/nvm_klj2.c                  198/199     106/110     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl_nvm/nvm_store.c                 434/434     259/266     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c    100/100      63/64      lines 100.00 %  branches 100.00 %
third_party/tsn-c-stack/include/wire.h            10/10        2/2       lines 100.00 %  branches 100.00 %
third_party/tsn-c-stack/src/acmp.c               792/792     392/392     lines 100.00 %  branches 100.00 %
third_party/tsn-c-stack/src/adp.c                206/208      99/106     lines 100.00 %  branches 100.00 %
third_party/tsn-c-stack/src/maap.c               209/209     140/140     lines 100.00 %  branches 100.00 %
```

| Campaign | Caught | Escaped | Evidence |
|---|---:|---:|---|
| Parent control | 520 | 0 | `round2/mutations-control.csv`, four 130-entry slices |
| AECP | 76 | 0 | `round2/mutations-aecp.csv` |
| SRP IF2 | 202 | 0 | `round2/mutations-srp.csv`, disjoint 68/67/67 batches |
| SRP IF1 | 76 | 0 | Same table; two dependency-pin controls also pass |
| Scratch lifecycle harness | 6 | 0 | `round2/evidence/lifecycle-mutants--results.json` |
| Service documentation | 38 | 0 | `round2/evidence/bounds.log` |

The complete dispatch census has 938 invocations in exactly one shard:
61 normal, 521 control, 77 AECP and 279 SRP. The standalone stack's 388-mutant
round 1 evidence is retained at the unchanged pin; it is not described as a
new round 2 standalone campaign. The round 2 boundary gates rerun the stack's
boundary checks and self-tests.

### Gates and reproduction

Every final command below returned zero. Initial monolithic control, SRP and
host-boundary runs exceeded the 570-second foreground budget and do not count
as passing evidence. Bounded campaign batches cover the exact same live tables.
Three complete build-only captures replace the long host capture; the unchanged
boundary checker judges their union with all its own image builds and controls.
The boundary inventory omission and dispatch registration issue found during
development were corrected before the final successful runs.

Use the earlier compiler/runtime setup. Set `WORK` to disk-backed scratch and
`PACKET` to this packet. Each command is foreground, with at most four campaign
jobs. The observed service-unit memory peak was 5688520704 bytes, below 9 GB.
The Verilator gate used the pinned 5.050 executable; Python was CPython 3.12.3.
Use these packet drivers for the bounded runs:

```sh
export WORK PACKET
export PYTHONDONTWRITEBYTECODE=1
python3 "$PACKET/round2/reproduce/control_slice.py" 1
python3 "$PACKET/round2/reproduce/control_slice.py" 2
python3 "$PACKET/round2/reproduce/control_slice.py" 3
python3 "$PACKET/round2/reproduce/control_slice.py" 4
python3 "$PACKET/round2/reproduce/srp_batch.py" 2 1 3
python3 "$PACKET/round2/reproduce/srp_batch.py" 2 2 3
python3 "$PACKET/round2/reproduce/srp_batch.py" 2 3 3
python3 "$PACKET/round2/reproduce/srp_batch.py" 1 1 1
mkdir -p "$WORK/review"
cp "$PACKET/round2/reproduce/probe_owner.cpp" "$WORK/review/probe_owner.cpp"
python3 "$PACKET/round2/reproduce/run_probes_fixed.py" --repo . --packet "$WORK/review"
```

The packet drivers only schedule the repository's campaigns and retain their
ordinary refusal/failure checks. The SRP driver derives both tables by observing
the live dispatcher, then checks each partition for exhaustive, disjoint coverage.
For host capture, run the following as separate foreground commands:

```sh
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$WORK/capture-control" -- python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --build-only --jobs 4
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$WORK/capture-coverage" -- python3 sw/firmware/gtest/fw_coverage.py --build-only --jobs 4
python3 "$PACKET/round2/reproduce/capture_small.py"
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator --capture "$WORK/capture-control" --capture "$WORK/capture-coverage" --capture "$WORK/capture-small"
```

The fabric driver expects a detached candidate checkout at `$WORK/fabric-tree`
with its required dependencies initialized and verified. `PICOLIBC_PYTHON` and
`COMPILER_RT_PYTHON` name the existing runtime source package roots. It uses the
ordinary entity builder and the same SoC command recorded above.

The full gate ledger includes the paired planted controls and each image link:

| Gate | Command | Result | Planted control / paired control |
|---|---|---|---|
| normal-suites | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 4 --build-dir $WORK/normal-suites` | rc 0 | 520 control, 76 AECP and 278 SRP plants; normal failures stop mutations |
| coverage | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep $WORK/coverage` | rc 0 | 29 coverage exclusions, moved/missing line and branch controls; adjusted 100% over 30 files |
| focused | `python3 $PACKET/round2/reproduce/run_focused.py --repo . --packet $WORK/review --jobs 2` | rc 0 | Fresh-source and invalid-source arms, both interfaces, Listener/probe, source/interface isolation |
| owner-probe | `python3 $PACKET/round2/reproduce/run_probes_fixed.py --repo . --packet $WORK/review` | rc 0 | Unchanged reviewer probe; old source-validity behavior is killed by f3b-source-validity |
| pins | `python3 $PACKET/round2/reproduce/pins.py` | rc 0 | 126 pin controls, including command/local maintenance and deletion race/error cases |
| lifecycle-mutants | `python3 $PACKET/round2/reproduce/lifecycle_mutations.py` | rc 0 | 6/6 harness mutations killed: either command/clone switch absent, ENOENT propagated, all errors swallowed |
| bounds | `python3 $PACKET/round2/reproduce/bounds.py` | rc 0 | 38/38 stale/missing numeric and conclusion plants; compiled headers at IF1/IF2 |
| predicate-controls | `python3 $PACKET/round2/reproduce/predicate_controls.py` | rc 0 | 16/16 F3b/publication mutations caught, including source validity at IF1/IF2 |
| boundary-host-split | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator --capture $WORK/capture-control --capture $WORK/capture-coverage --capture $WORK/capture-small` | rc 0 | 112 boundary, 126 pin and 4 figure controls; 2854 sources / 3084 compiler invocations |
| boundary-rtl | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator` | rc 0 | 6 boundary, 126 pin and 4 figure controls; 829 sources / 926 compiler invocations |
| images | `python3 sw/firmware/ctrl/test/ctrl_image.py --base d40e4e9827be2516f8f34b9d65f0a483fff2194c --shape endstation_arty_4x4 --shape endstation_arty_8ch --shape endstation_arty_current --shape endstation_ax7101_1x1_tdm8 --shape endstation_ax7101_8x8 --out $WORK/images` | rc 0 | Five shapes before/after; linked RV32I/ILP32 audits; image-controls supplies planted linked-image failures |
| image-controls | `python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32 --out $WORK/image-controls` | rc 0 | 33 helper, ELF instruction/ABI, relocation and undefined-symbol checks |
| image-evidence | `python3 $PACKET/round2/reproduce/image_evidence.py` | rc 0 | 15 image pairs within +2048; +2048 accepted, +2049 rejected |
| fabric | `python3 $PACKET/round2/reproduce/fabric.py` | rc 0 | Baseline, round 1 and round 2 binary hashes match; one-byte corruption rejected for BIOS and AEM |
| lint-rtl | `python3 scripts/lint_rtl.py --check --self-test --jobs 2` | rc 0 | 8 pragma/resolution controls; 90 findings at ratchet 90 |
| docs | `python3 scripts/docs_check.py` | rc 0 | 23 scrub and 4 routing controls |
| docs-selftest | `python3 scripts/docs_check.py --selftest` | rc 0 | 23 scrub and 4 routing controls |
| doc-style | `python3 scripts/check_doc_style.py` | rc 0 | Paired doc-style-selftest plants forbidden prose forms |
| doc-style-selftest | `python3 scripts/check_doc_style.py --selftest` | rc 0 | Forbidden prose forms are refused |
| cpp-idiom | `python3 scripts/check_cpp_idiom.py` | rc 0 | Paired cpp-controls: 75 idiom controls |
| cpp-controls | `python3 scripts/check_cpp_idiom.py --selftest` | rc 0 | 75 idiom controls |
| python-idiom | `python3 scripts/check_py_idiom.py` | rc 0 | Paired python-controls: malformed/forbidden Python constructs |
| python-controls | `python3 scripts/check_py_idiom.py --selftest` | rc 0 | Forbidden Python constructs and required metadata controls |
| em-dash | `python3 scripts/check_em_dash.py --base d40e4e9827be2516f8f34b9d65f0a483fff2194c` | rc 0 | Paired em-dash-controls: 339 added-line/mirrored-label arms |
| em-dash-controls | `python3 scripts/check_em_dash.py --selftest` | rc 0 | 339 added-line/mirrored-label arms |
| toc | `python3 scripts/gen_toc.py --check` | rc 0 | Paired toc-controls: 1501 document/section arms |
| toc-controls | `python3 scripts/gen_toc.py --selftest` | rc 0 | 1501 document/section arms |
| doc-paths | `python3 scripts/check_doc_paths.py` | rc 0 | Paired doc-path-controls: bad paths and line anchors |
| doc-path-controls | `python3 scripts/check_doc_paths.py --selftest` | rc 0 | Bad paths and line anchors are refused |
| submodule-docs | `python3 scripts/check_submodule_docs.py` | rc 0 | Paired submodule-controls: stale pin and diagram/contract claims |
| submodule-controls | `python3 scripts/check_submodule_docs.py --selftest` | rc 0 | Stale pin, link and generated-document claims are refused |
| hygiene | `python3 scripts/check_hygiene.py --check` | rc 0 | Paired hygiene-controls: 35 filename/whitespace arms |
| hygiene-controls | `python3 scripts/check_hygiene.py --selftest` | rc 0 | 35 filename/whitespace arms |
| mailbox-controls | `python3 sw/mailbox/gen_mailbox.py --check --crosscheck --selftest` | rc 0 | Missing/malformed contract fields and generated-byte drift refused |
| coverage-controls | `python3 sw/firmware/gtest/fw_coverage.py --selftest` | rc 0 | 29 exclusion/coverage corruption controls |
| tally-controls | `python3 sw/firmware/gtest/tally_selftest.py` | rc 0 | 18 false-green, absent-test and failure-accounting controls |
| diagram | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | rc 0 | Paired diagram-controls: stale pin/edge and generated drift |
| diagram-controls | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | rc 0 | Stale pin/edge and generated drift refused |
| source-lists | `python3 scripts/check_rtl_source_lists.py` | rc 0 | Paired source-controls: 50 omission/consumer controls |
| source-controls | `python3 scripts/check_rtl_source_lists.py --selftest` | rc 0 | 50 omission/consumer controls |
| evidence-readers | `python3 scripts/measure_test_evidence.py --check` | rc 0 | Paired evidence-controls: 105 reader/runner mutation controls |
| evidence-controls | `python3 scripts/measure_test_evidence.py --selftest` | rc 0 | 105 reader/runner mutation controls |
| dispatch-controls | `python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py` | rc 0 | Missing/duplicate/new suite, nine invalid selectors, failed-normal stopping rule; 938 invocations partitioned |
| control-1 | `python3 $PACKET/round2/reproduce/control_slice.py 1` | rc 0 | 130/130 planted mutations caught; four slices exactly cover the live 520-entry table |
| control-2 | `python3 $PACKET/round2/reproduce/control_slice.py 2` | rc 0 | 130/130 planted mutations caught; four slices exactly cover the live 520-entry table |
| control-3 | `python3 $PACKET/round2/reproduce/control_slice.py 3` | rc 0 | 130/130 planted mutations caught; four slices exactly cover the live 520-entry table |
| control-4 | `python3 $PACKET/round2/reproduce/control_slice.py 4` | rc 0 | 130/130 planted mutations caught; four slices exactly cover the live 520-entry table |
| aecp-campaign | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 2/4 --jobs 4 --build-dir $WORK/aecp-campaign` | rc 0 | 76/76 planted defects caught |
| srp-if1-1 | `python3 $PACKET/round2/reproduce/srp_batch.py 1 1 1` | rc 0 | Live dispatcher supplies the 202 IF2 and 76 IF1 defects; disjoint batches; IF1 also refuses two poisoned dependency states |
| srp-if2-1 | `python3 $PACKET/round2/reproduce/srp_batch.py 2 1 3` | rc 0 | Live dispatcher supplies the 202 IF2 and 76 IF1 defects; disjoint batches; IF1 also refuses two poisoned dependency states |
| srp-if2-2 | `python3 $PACKET/round2/reproduce/srp_batch.py 2 2 3` | rc 0 | Live dispatcher supplies the 202 IF2 and 76 IF1 defects; disjoint batches; IF1 also refuses two poisoned dependency states |
| srp-if2-3 | `python3 $PACKET/round2/reproduce/srp_batch.py 2 3 3` | rc 0 | Live dispatcher supplies the 202 IF2 and 76 IF1 defects; disjoint batches; IF1 also refuses two poisoned dependency states |
| capture-control | `python3 sw/firmware/ctrl/test/ctrl_capture.py --out $WORK/capture-control -- python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --build-only --jobs 4` | rc 0 | Build-only prerequisite capture, judged with all other captures by the full boundary controls |
| capture-coverage | `python3 sw/firmware/ctrl/test/ctrl_capture.py --out $WORK/capture-coverage -- python3 sw/firmware/gtest/fw_coverage.py --build-only --jobs 4` | rc 0 | Build-only prerequisite capture, judged with all other captures by the full boundary controls |
| capture-small | `python3 $PACKET/round2/reproduce/capture_small.py` | rc 0 | Build-only prerequisite capture, judged with all other captures by the full boundary controls |
| aecp-base-endstation_arty_4x4 | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_arty_4x4.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libcompiler_rt.a --output $WORK/composed-images/aecp/base/endstation_arty_4x4 --ctrl-source $WORK/images/base-tree/sw/firmware/ctrl --stack-source $WORK/images/base-tree/tsn-c-stack --with-aecp` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| aecp-base-endstation_arty_8ch | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_arty_8ch.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libcompiler_rt.a --output $WORK/composed-images/aecp/base/endstation_arty_8ch --ctrl-source $WORK/images/base-tree/sw/firmware/ctrl --stack-source $WORK/images/base-tree/tsn-c-stack --with-aecp` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| aecp-base-endstation_arty_current | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_arty_current.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libcompiler_rt.a --output $WORK/composed-images/aecp/base/endstation_arty_current --ctrl-source $WORK/images/base-tree/sw/firmware/ctrl --stack-source $WORK/images/base-tree/tsn-c-stack --with-aecp` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| aecp-base-endstation_ax7101_1x1_tdm8 | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_1x1_tdm8.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libcompiler_rt.a --output $WORK/composed-images/aecp/base/endstation_ax7101_1x1_tdm8 --ctrl-source $WORK/images/base-tree/sw/firmware/ctrl --stack-source $WORK/images/base-tree/tsn-c-stack --with-aecp` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| aecp-base-endstation_ax7101_8x8 | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libcompiler_rt.a --output $WORK/composed-images/aecp/base/endstation_ax7101_8x8 --ctrl-source $WORK/images/base-tree/sw/firmware/ctrl --stack-source $WORK/images/base-tree/tsn-c-stack --with-aecp` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| aecp-head-endstation_arty_4x4 | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_arty_4x4.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libcompiler_rt.a --output $WORK/composed-images/aecp/head/endstation_arty_4x4 --with-aecp` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| aecp-head-endstation_arty_8ch | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_arty_8ch.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libcompiler_rt.a --output $WORK/composed-images/aecp/head/endstation_arty_8ch --with-aecp` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| aecp-head-endstation_arty_current | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_arty_current.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libcompiler_rt.a --output $WORK/composed-images/aecp/head/endstation_arty_current --with-aecp` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| aecp-head-endstation_ax7101_1x1_tdm8 | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_1x1_tdm8.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libcompiler_rt.a --output $WORK/composed-images/aecp/head/endstation_ax7101_1x1_tdm8 --with-aecp` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| aecp-head-endstation_ax7101_8x8 | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime-freestanding/libcompiler_rt.a --output $WORK/composed-images/aecp/head/endstation_ax7101_8x8 --with-aecp` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| srp-base-endstation_arty_4x4 | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_arty_4x4.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime/libcompiler_rt.a --output $WORK/composed-images/srp/base/endstation_arty_4x4 --ctrl-source $WORK/images/base-tree/sw/firmware/ctrl --stack-source $WORK/images/base-tree/tsn-c-stack` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| srp-base-endstation_arty_8ch | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_arty_8ch.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime/libcompiler_rt.a --output $WORK/composed-images/srp/base/endstation_arty_8ch --ctrl-source $WORK/images/base-tree/sw/firmware/ctrl --stack-source $WORK/images/base-tree/tsn-c-stack` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| srp-base-endstation_arty_current | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_arty_current.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime/libcompiler_rt.a --output $WORK/composed-images/srp/base/endstation_arty_current --ctrl-source $WORK/images/base-tree/sw/firmware/ctrl --stack-source $WORK/images/base-tree/tsn-c-stack` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| srp-base-endstation_ax7101_1x1_tdm8 | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_1x1_tdm8.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime/libcompiler_rt.a --output $WORK/composed-images/srp/base/endstation_ax7101_1x1_tdm8 --ctrl-source $WORK/images/base-tree/sw/firmware/ctrl --stack-source $WORK/images/base-tree/tsn-c-stack` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| srp-base-endstation_ax7101_8x8 | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime/libcompiler_rt.a --output $WORK/composed-images/srp/base/endstation_ax7101_8x8 --ctrl-source $WORK/images/base-tree/sw/firmware/ctrl --stack-source $WORK/images/base-tree/tsn-c-stack` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| srp-head-endstation_arty_4x4 | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_arty_4x4.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime/libcompiler_rt.a --output $WORK/composed-images/srp/head/endstation_arty_4x4` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| srp-head-endstation_arty_8ch | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_arty_8ch.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime/libcompiler_rt.a --output $WORK/composed-images/srp/head/endstation_arty_8ch` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| srp-head-endstation_arty_current | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_arty_current.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime/libcompiler_rt.a --output $WORK/composed-images/srp/head/endstation_arty_current` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| srp-head-endstation_ax7101_1x1_tdm8 | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_1x1_tdm8.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime/libcompiler_rt.a --output $WORK/composed-images/srp/head/endstation_ax7101_1x1_tdm8` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |
| srp-head-endstation_ax7101_8x8 | `python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml --libc $VALIDATION_STORAGE/665f3b-a612/runtime/libc.a --compiler-runtime $VALIDATION_STORAGE/665f3b-a612/runtime/libcompiler_rt.a --output $WORK/composed-images/srp/head/endstation_ax7101_8x8` | rc 0 | Real runtime-linked image audit; paired image-controls and growth boundary controls |

No new generated repository file was edited in round 2. Generated test contracts,
entity fixtures and images were produced by their generators under scratch.
The all-fabric setup used the existing runtime source packages and kept the
selected Python environment first on PATH; initial setup failures are not
reported as gate passes.

### Delivery boundary

The worktree is clean and contains three new commits, with no amend or rebase.
All five required implementation dependencies are clean and at their recorded pins.
No build or campaign remains running. No existing public comment was changed.
HANDOFF.md and PR-BODY.md are prepared; the round 2 index records digests and
sizes, and contains no binary, toolchain, installed package, tree export or file
over 200 KB. The hosted acceptance item and independent re-review remain open.
A new `[A612] STOP` comment with the candidate head is the final authorized
public action. Publication, hosted execution and the remaining merge duties
belong to the integration owner.



## Round 3

[A612] REVIEW READY: `532ab871272597d83fa08506bcb05298fbe87806`.
Parent/resume: `651ccb5aea1bc4d99f356503c188947d39e0c9e4`.
One new one-line commit: `fix(ci): classify mailbox service bounds as a gated input`.
Origin and branch match the assignment. No push was performed.
All 26 recorded final local validations return zero.
Three diagnostic attempts are recorded separately, never counted as passes.

Authority: [round 3 assignment, comment 6155487551](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6155487551).
It accepts local validation for REVIEW READY and reserves hosted acceptance for the manager.
[R582-2](https://github.com/kebag-logic/milan-fpga/pull/736#issuecomment-6155478463)
and [R583-2](https://github.com/kebag-logic/milan-fpga/pull/736#issuecomment-6154961424)
identify the same missing document dependency.
The [failed hosted run 38464016325](https://github.com/kebag-logic/milan-fpga/actions/runs/38464016325)
was read directly: the classifier failed before the firmware jobs executed.
No corrected-head hosted result is claimed here.

### Changes and review dispositions

| File:line or artifact | Change | Review item |
|---|---|---|
| `scripts/ci_scope.py:67` | Name the service-bound reader and firmware job | R582-2-F1 / R583-2-F1 |
| `scripts/ci_scope.py:72` | Register the service-bound page in `GATE_READ_DOCS` | R582-2-F1 / R583-2-F1 |
| `scripts/ci_scope.py:293` | Add the relevant-path case; removing the registration now fails its mutation arm | R582-2-F1 / R583-2-F1 |
| `docs/testing/CI_WORKFLOWS.md:201` | List the page, reader, firmware job and absence from docs-check | R582-2-F1 / R583-2-F1 |
| `sw/firmware/ctrl/maap/README.md:135` | Explain receive/link refresh freshness within a pass and that pass's poll | R582-2-S1 documentation option |
| `PR-BODY.md`, Status and Known limitations | State the published round 2 head; delete both stale limitation bullets | R582-2-R1, prepared body only |
| `PR-BODY.md`, Description | Distinguish #23's integration of already adopted publication code | Prior optional provenance clarification |

The suggestion's optional deferred-ANNOUNCE and out-of-allocation-demand tests
were not added. No new firmware mutation coverage is claimed for them.
The receive/link explanation follows `maap_mbx.c:127,157,166` and the loop's
receive/event-before-poll order. It does not weaken either retained refresh.
The parent firmware, generated files and all gitlinks remain unchanged.
The latest reviews already resolve the per-source declaration predicate defect.
The hosted portion of R582-1-F1 remains a manager acceptance duty.
Only an independent corrected-head review can clear review findings.

### Complete gate-read inventory

The live branch scan examined 330 gated files and 185 documentation candidates.
All eight discovered pages are registered and classified relevant.
No missing or stale page remains.
The self-test passes 109 checks, including reader-spelling and table-removal controls.
The page's direct classifier invocation prints `true`.
This is the repository's documented scan, with its existing static-scan limits;
it is not a claim to resolve computed document names outside that contract.

| Page | First reader | Registered / relevant |
|---|---|---|
| `docs/AAF_LATENCY_TAPS.md` | `sw/builder/test_clock_contract.py:321` | yes / yes |
| `docs/design/AREA_BUDGET.md` | `syn/ooc/pp_resource_gate.py:72` | yes / yes |
| `docs/design/MAILBOX_SPLIT.md` | `sw/firmware/ctrl/test/ctrl_service_bounds.py:13` | yes / yes |
| `docs/design/SPLIT_CONTROL_MEMORY.md` | `sw/litex/test_ctrl_memory.py:94` | yes / yes |
| `docs/reference/MAILBOX_CONTRACT.md` | `sw/mailbox/gen_mailbox.py:77` | yes / yes |
| `docs/reference/REGISTER_MAP.md` | `tb/tools/torture_campaign.py:3209` | yes / yes |
| `docs/reference/TRACE_EVENTS.md` | `sw/trace/gen_trace_events.py:28` | yes / yes |
| `docs/testing/MILAN_V12_AUDIT_2026-08-16.md` | `tests/steps/milan_streaming_licence_steps.py:27` | yes / yes |

The full lane delta from `d40e4e98` was inspected for added readers.
`ctrl_service_bounds.py:13` is the new gate-read document dependency.
The firmware coverage exclusion page stays under `sw/`, already relevant.

### Round 3 gates and controls

Commands below are plain shell commands.
Use the CPython 3.12.3 environment with the project's locked Markdown packages
and PyYAML installed. `WORK` is disk-backed scratch; `EVIDENCE` names this packet.
No gate command was piped. Independent gates ran concurrently.
No simulator build or synthesis run was needed for this correction.
The measured service-unit memory sample was 363245568 bytes, below 9 GiB.

| Gate | Command | Result | Planted control / proof |
|---|---|---|---|
| ci-events-check | `python3 scripts/ci_events.py --check` | rc 0 | ci-events-controls: 3064 arms over 2169 contract items |
| ci-events-controls | `python3 scripts/ci_events.py --selftest` | rc 0 | 3064 workflow/policy mutations and negative controls |
| doc-path-controls | `python3 "$EVIDENCE/round3/doc_path_controls.py" --repo .` | rc 0 | Three disposable tracked fixtures; expected statuses 0, 1, 1 |
| doc-paths | `python3 scripts/check_doc_paths.py` | rc 0 | doc-path-controls: valid passes, missing path and past-end anchor fail |
| doc-style-controls | `python3 scripts/check_doc_style.py --selftest` | rc 0 | Positive and refusal style fixtures |
| doc-style | `python3 scripts/check_doc_style.py` | rc 0 | doc-style-controls: documented positive/negative fixtures |
| docs-controls | `python3 scripts/docs_check.py --selftest` | rc 0 | 23 scrub and 4 routing arms |
| docs | `python3 scripts/docs_check.py` | rc 0 | docs-controls: 23 scrub and 4 routing arms |
| em-dash-controls | `python3 scripts/check_em_dash.py --selftest` | rc 0 | 339/339 planted controls |
| em-dash | `python3 scripts/check_em_dash.py --base d40e4e9827be2516f8f34b9d65f0a483fff2194c` | rc 0 | 339/339 embedded controls; separate em-dash-controls also passes |
| evidence-controls | `python3 scripts/measure_test_evidence.py --selftest` | rc 0 | 105/105 controls; inactive mutations and unexplained readers refused |
| evidence-readers | `python3 scripts/measure_test_evidence.py --check` | rc 0 | evidence-controls: 105/105 controls |
| gate-read-inventory | `python3 "$EVIDENCE/round3/gate_read_inventory.py" --repo .` | rc 0 | Exact eight-page set; no missing/stale entry; classifier reader/removal controls above |
| hygiene-controls | `python3 scripts/check_hygiene.py --selftest` | rc 0 | 35/35 controls |
| hygiene | `python3 scripts/check_hygiene.py --check` | rc 0 | hygiene-controls: 35/35 controls |
| integrity | `python3 "$EVIDENCE/round3/integrity.py" --repo .` | rc 0 | Direct raw-blob/mode and parent/changed-path identity check; no synthetic control claimed |
| python-controls | `python3 scripts/check_py_idiom.py --selftest` | rc 0 | 54/54 scanner, population and ratchet checks |
| python-idiom | `python3 scripts/check_py_idiom.py` | rc 0 | python-controls: 54/54 checks |
| scope-after | `python3 scripts/ci_scope.py --selftest` | rc 0 | 109 checks; removal of each gate-read page is caught; independent scan still names each removed page; 16 reader spellings |
| scope-classification | `python3 scripts/ci_scope.py docs/design/MAILBOX_SPLIT.md` | rc 0 | New page case and table-removal mutation in scope-after |
| service-bounds-portable | `python3 "$EVIDENCE/round3/service_bounds.py" --repo . --out "$WORK/portable-bounds"` | rc 0 | Same 38 controls through the published portable runner |
| service-bounds | `python3 "$WORK/bounds.py"` | rc 0 | 38/38 stale-value/deletion controls; 47 total checks |
| source-controls | `python3 scripts/check_rtl_source_lists.py --selftest` | rc 0 | 50/50 controls |
| source-lists | `python3 scripts/check_rtl_source_lists.py` | rc 0 | source-controls: 50/50 controls; source removals from each consumer |
| toc-controls | `python3 scripts/gen_toc.py --selftest` | rc 0 | 1501/1501 rendering controls |
| toc | `python3 scripts/gen_toc.py --check` | rc 0 | toc-controls: 1501/1501 controls |

Portable evidence runners are in `round3/`; raw receipt hashes, sizes, exits and
normalized commands are in `round3/gate-ledger.json`.
Large raw logs remain in scratch and are represented by size and SHA-256.
No toolchain, installed package, tree export or file over 200000 bytes was added
under the output directory.

Diagnostic attempts:

- `scope-before`: expected rc 1 at the resume tree, reproducing the missing
  page reported by both reviews. The corrected self-test returns zero.
- `service-bounds-setup`: the bare matching interpreter lacked PyYAML.
  The existing virtual environment is also CPython 3.12.3 and supplies it.
  The actual compiled check and published portable runner both pass there.
- `integrity-precleanup`: detected five ignored mailbox build directories
  retained from previous work. Their 246 files were moved intact into scratch.
  No tracked file was removed. Final raw-byte/mode and clean-tree checks pass.

### Retained image hashes and growth

Round 3 changes only the three files listed above.
`round3/final-state.json` verifies the exact parent and changed-file set,
1311 superproject blobs, and 1043 dependency blobs at unchanged gitlinks.
Thus production source, configuration, image builder and runtime inputs retain
the round 2 versions. No fresh firmware build is claimed in this round.
All 30 retained before/after ELF files were rehashed against the table below;
every size and SHA-256 matched (`round3/retained-image-audit.json`).
The before column is the original `d40e4e98` baseline; after is the round 2
measurement at `651ccb5a`, retained for round 3's unchanged firmware inputs.

| Composition / shape | Load before | Load after | Growth | ELF SHA-256 before | ELF SHA-256 after |
|---|---:|---:|---:|---|---|
| ADP-ACMP-MAAP / `endstation_arty_4x4` | 34820 | 35808 | +988 | `f70be6b729d203ade7fb75e832d1ca0b1d1d9ba99f03e746cc2907174ec9cce4` | `9060072441800c7ceb2d01cab468eb6e1213cbc376fac9540135ccfcb676ccd9` |
| ADP-ACMP-MAAP / `endstation_arty_8ch` | 34820 | 35808 | +988 | `eb5dfe04250400df1a0546c4f52096cfbd4e8f0e7abc777388e6d55cf64802e6` | `91ed8f02cd8cfc0fc05ba9a0791c16ddf98afeb5da9132961b3addf8048fa82b` |
| ADP-ACMP-MAAP / `endstation_arty_current` | 34812 | 35800 | +988 | `9600824e12c1890edebeee455afe2244dc4fa9166c463fbb01591e284fe1f441` | `7e398af8cfb393a948af2d618af7a900955e2deb7127459c803ba5c8167b622f` |
| ADP-ACMP-MAAP / `endstation_ax7101_1x1_tdm8` | 34836 | 35824 | +988 | `ee7991b0b767b331d1b9fc84972b5a610ec0e9ae521ddf20689d9b4df4a9f33c` | `1c422c8096ebeaa109827ef29743322b8328b58e933d0917cfddc8410c1f1390` |
| ADP-ACMP-MAAP / `endstation_ax7101_8x8` | 34840 | 35828 | +988 | `1b17baeb51ab66d3eeaeb97e5136fc8f516361ca6d99900d490a7953689e7018` | `6a00a71d9d67fb5f8848a0e2dcc064551fcc199bd8985e3d83263f4bfa72d760` |
| SRP / `endstation_arty_4x4` | 50430 | 51718 | +1288 | `c5ccb78e4bb18a7d4ea8926564524d4b865bd0a955738c5d35b505f8bf5b8a3d` | `80bf935cc69ef7da26e74ef918da6fdf92332217d15e769271e100939a1d7863` |
| SRP / `endstation_arty_8ch` | 50430 | 51718 | +1288 | `6e265c3b796fabd9edae6f5e52baabb4845513e9bccba2409a053915d6ebccd5` | `512ca8bd22de32cae8192935f1f8565cd1326555a4fdc43cdff472d90f9f530f` |
| SRP / `endstation_arty_current` | 50006 | 51202 | +1196 | `2d0d89202c0e9d790cc247cabbbe9d96b9cc731cc3621a17345ec5e963d1265a` | `1bf47d8f359a0474d03c795b689e699aab495cc7576347f3ee5a81c7c99e6cbe` |
| SRP / `endstation_ax7101_1x1_tdm8` | 50362 | 51658 | +1296 | `863666a08cdc823e6599e52b042f84ce4eaac296625471faac69a55209fb3121` | `d3244df6176809f6fdebd8b36c8c7830daa48ed1e2de4f68247ca61aca000a08` |
| SRP / `endstation_ax7101_8x8` | 50466 | 51770 | +1304 | `ea60f397fef49c802bbf3c1e0e96b274f215d18e0023f39f9f2c4a5d4f4d25ca` | `5a22cedcb18f25374f480c6bfa596cf333169f9f991acc3bc480d1361a4e9b98` |
| SRP-AECP / `endstation_arty_4x4` | 100066 | 101354 | +1288 | `180088cdc4a37cdf1281d9d64bce2d4d60ba040adafdbc8907ceafdd5dfbbf73` | `338f6cc8303c03035fdc52541284bb512b60f7b2c5a0d93d7429228cf490ed12` |
| SRP-AECP / `endstation_arty_8ch` | 105818 | 107106 | +1288 | `a9832cff9c849e539cbeedd71dc5fd98edffa340f052d7b7369fa4ff90ae4c20` | `536445f1db8f5d1f21336a67bb175fe5234f56629138d4f5ab947fd916484fa4` |
| SRP-AECP / `endstation_arty_current` | 94338 | 95534 | +1196 | `caa8874683dd01abaf7aa6673015b03d9e35d753810b36a0b2f1cc408095ebfa` | `70c3c14eb67c942c842e93e5f42849b5c881060ffd5cbeac95c7b2796519f79b` |
| SRP-AECP / `endstation_ax7101_1x1_tdm8` | 96534 | 97830 | +1296 | `0c9a9ff7f516df33e6a5f3a9f885489bb1705943fd0e48a65d7493d848c665f6` | `01affe2224817a9b098435415a7bfd7d99ab3b1c8a44e058c67ca48288b79e3a` |
| SRP-AECP / `endstation_ax7101_8x8` | 110250 | 111554 | +1304 | `0336f8328dd2aa5e19ea065dbb5694ed9b3490c90dd9c5abc8216f531aff3f2f` | `7698a20ec3e9a520c33b260af5be114f10799518d1754c244b47540ccfededa5` |

The maximum Release load growth remains 1304 bytes, below 2048 bytes.
The earlier +2048 accepted / +2049 refused controls remain recorded.
The all-fabric identity receipts retain these before/round 1/round 2 values:

| Artifact | Bytes | SHA-256 before / after |
|---|---:|---|
| BIOS binary | 52988 | `5a2c937f40542238114c7bdd267d0eb2977a70a5cb0eb72889cc4ec3d1c0d4f3` |
| AEM descriptor | 7512 | `4fc8d61582a965fe648abc0c15d0551153ff2b27f202d1fbc8319fbb4bdb396d` |

These are retained load-artifact receipts, not new routed-image measurements.
No round 3 edit reaches an all-fabric build input.

### Retained pin and predicate controls

The pin remains `70936b77dc41981e192438388cd0aced69954f18`.
The corrected assignment permits reviewed #19, #20 and #25, with #23 integrating
already adopted publication code; the original exact-#25-only premise was corrected.
The complete merge commits, review links and 45-path net file list remain in
this handoff's pin section and `pin-proof.json`.
Round 3 moves no pin and introduces no additional stack content.
The final integrity check independently verified the stack root, own origin,
head, every tracked blob and clean state.

The retained predicate is valid source DA AND (answered probe younger than
15000 ms OR registered Listener), further constrained by interface and allocation.
The round 2 source-validity control, original fresh-probe / Listener / neither /
expired-probe controls, and two-interface gate control remain unchanged.
Those campaign receipts and killer mappings remain in the earlier sections.

### Retained coverage and mutation tables

These are round 2 measurements, carried with unchanged measured code, test
sources, exclusion table and mutation tables. No new campaign is claimed.

| Campaign | Caught | Escaped | Receipt |
|---|---:|---:|---|
| Parent control | 520 | 0 | `round2/mutations-control.csv` |
| Parent AECP | 76 | 0 | `round2/mutations-aecp.csv` |
| Parent SRP | 278 (76 IF1, 202 IF2) | 0 | `round2/mutations-srp.csv` |

Coverage is adjusted 100% lines and branches across all 30 measured files.
The raw covered/total counts below precede the documented exclusions:

```text
file                                                 lines    branches   after exclusions
sw/firmware/ctrl/acmp/acmp_mbx.c                  81/81       28/28      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/acmp/acmp_nvm.c                  38/38       10/10      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/adp/adp_mbx.c                    83/83       38/40      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp.c                     357/357     308/308     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp_commands.c            424/424     362/362     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp_image.c                77/77       80/80      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp_maps.c                222/222     290/290     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp_mbx.c                 101/101      40/40      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp_nvm.c                 102/102      86/86      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/aecp/aecp_state.c                63/63       69/69      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/app/ctrl_app.c                   46/47       43/46      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/app/ctrl_app_aecp.c             107/107      64/64      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/app/ctrl_app_srp.c               87/87       70/70      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/loop/ctrl_loop.c                101/101      62/62      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/maap/maap_csr.c                  39/39       18/18      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/maap/maap_mbx.c                 127/127      82/82      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/mbx/mbx.c                       243/243     102/102     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/mbx/mbx_wire.h                   15/15       12/12      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/plat/mbx_plat_mmio.c             10/10        0/0       lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/port/ctrl_debug.c                19/19        6/6       lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/port/ctrl_pool.c                 99/99       60/60      lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/port/shlan_port.c                22/22        6/6       lines 100.00 %  branches 100.00 %
sw/firmware/ctrl/srp/srp_mbx.c                   543/543     486/486     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl_nvm/nvm_klj2.c                  198/199     106/110     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl_nvm/nvm_store.c                 434/434     259/266     lines 100.00 %  branches 100.00 %
sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c    100/100      63/64      lines 100.00 %  branches 100.00 %
third_party/tsn-c-stack/include/wire.h            10/10        2/2       lines 100.00 %  branches 100.00 %
third_party/tsn-c-stack/src/acmp.c               792/792     392/392     lines 100.00 %  branches 100.00 %
third_party/tsn-c-stack/src/adp.c                206/208      99/106     lines 100.00 %  branches 100.00 %
third_party/tsn-c-stack/src/maap.c               209/209     140/140     lines 100.00 %  branches 100.00 %
```

### Final handoff and remaining duties

The working tree and five initialized dependencies are clean, including ignored
and untracked files. The unused external dependency remains uninitialized.
No new submodule initialization, dependency branch change or push occurred.
The one new commit uses the existing configured identity, with a one-line
subject and no body or trailers. No generated repository file was hand-edited.

The prepared PR body follows the repository template, starts with `[A612]`,
and says `Relates to #665`. It contains the requested Round 3 section and
residue corrections. No PR or existing issue/PR comment was edited.

The manager owns the push and local workflow replica, followed by exact-head
hosted acceptance: `changes`, `firmware-boundary`, `firmware-verilator`,
`rtl-fast`, `verilator-suites`, and `yosys-portability` must execute successfully.
The remaining repository contexts, independent corrected-head reviews,
current-dev candidate validation, explicit merge authorization and post-merge
containment also remain manager duties. No review verdict is supplied here.
No hardware, bench, flashing or physical timing evidence is claimed.

A new `[A612] REVIEW READY` comment with this head is the final authorized
public write for this round. No TAKEN comment is repeated.

## Round 4

[A612] REVIEW READY: `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5`.
Parent/resume: `532ab871272597d83fa08506bcb05298fbe87806`.
One new one-line commit: `docs(ci): describe the gate-read pages without a count`.
Origin and branch match the assignment. No push was performed.
All 23 recorded final local validations return zero.
One diagnostic run is recorded separately and is not counted as a pass.

Authority: [round 4 assignment, comment 6156987825](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6156987825).
It answers [R582-3](https://github.com/kebag-logic/milan-fpga/pull/736#issuecomment-6156867741)
and [R583-3](https://github.com/kebag-logic/milan-fpga/pull/736#issuecomment-6156980716).
Both reviews were negative at `532ab871` for the same MINOR.
The assignment allows this docs fix and the PR body head, and nothing else.

### Round 4 changes and review dispositions

| File:line or artifact | Change | Review item |
|---|---|---|
| `docs/testing/CI_WORKFLOWS.md:179` | "Seven pages under `docs/`" becomes "These pages under `docs/`" | R582-3-F1 / R583-3-F1 (MINOR, Docs) |
| `PR-BODY.md`, Status | Names `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5` as the published head | R582-3-R1 / R583-3-R1 (residue), prepared body only |
| `PR-BODY.md`, Round 4 and references | Records this round's change, gates and review links | Round 4 assignment item 2 |

The sentence now gives no count, so it cannot go stale when `GATE_READ_DOCS` changes.
Its paragraph, `CI_WORKFLOWS.md:179-210`, still links all eight registered pages.
`scripts/ci_scope.py:69-78` holds the same eight; the self-test prints eight `ok gate-read page` lines.
No other count of these pages exists in `CI_WORKFLOWS.md` or the `ci_scope.py` comment.

R583-3-S1 (optional: no check reads the count) is not adopted in the tree.
The assignment says nothing else changes, and the count no longer exists.
`round4/gate_read_paragraph.py` is packet evidence only, not a repository gate.
It compares the paragraph's links with `GATE_READ_DOCS` and refuses a stated count.

The firmware, generated files, scripts, tests, gitlinks and pin are unchanged.
Only an independent review of the new head can clear R582-3-F1 and R583-3-F1.

### Round 4 gates and controls

Commands are plain shell, run from the checkout at the committed head.
Use the CPython 3.12.3 environment with the project's locked Markdown packages
and PyYAML installed. `WORK` is disk-backed scratch; `EVIDENCE` names this packet.
No gate command was piped. Up to four independent gates ran concurrently.
No simulator build, synthesis or firmware build was needed for this correction.
The service unit's peak memory was 414175232 bytes, below 9 GiB.
Each gate was also run before the commit, on the edited working tree; all were rc 0.

| Gate | Command | Result | Planted control / proof |
|---|---|---|---|
| ci-events-check | `python3 scripts/ci_events.py --check` | rc 0 | ci-events-controls: 2169 contract items, 3064 arms |
| ci-events-controls | `python3 scripts/ci_events.py --selftest` | rc 0 | 3064 workflow/policy mutations and negative controls |
| doc-style | `python3 scripts/check_doc_style.py` | rc 0 | doc-style-controls: positive and refusal fixtures |
| doc-style-controls | `python3 scripts/check_doc_style.py --selftest` | rc 0 | Positive and refusal style fixtures |
| docs | `python3 scripts/docs_check.py` | rc 0 | docs-controls: 23 scrub and 4 routing arms |
| docs-controls | `python3 scripts/docs_check.py --selftest` | rc 0 | 23 scrub and 4 routing arms |
| em-dash | `python3 scripts/check_em_dash.py --base d40e4e9827be2516f8f34b9d65f0a483fff2194c` | rc 0 | 0 findings over 132 added lines; 339/339 embedded arms |
| em-dash-controls | `python3 scripts/check_em_dash.py --selftest` | rc 0 | 339/339 planted controls |
| doc-paths | `python3 scripts/check_doc_paths.py` | rc 0 | 979 cited paths; doc-path-controls below |
| doc-path-controls | `python3 "$EVIDENCE/round3/doc_path_controls.py" --repo .` | rc 0 | Three disposable fixtures; expected statuses 0, 1, 1 |
| toc | `python3 scripts/gen_toc.py --check` | rc 0 | toc-controls: 1501/1501 arms |
| toc-anchors | `python3 scripts/gen_toc.py --verify-anchors` | rc 0 | 486 cross-page fragment links reproduced |
| toc-controls | `python3 scripts/gen_toc.py --selftest` | rc 0 | 1501/1501 rendering controls |
| baremetal | `python3 scripts/check_baremetal_only.py --check` | rc 0 | 0 findings over 1285 files; baremetal-controls: 700 arms |
| baremetal-controls | `python3 scripts/check_baremetal_only.py --selftest` | rc 0 | 700 planted arms, including this policy page's pattern |
| scope-controls | `python3 scripts/ci_scope.py --selftest` | rc 0 | 109 checks; eight gate-read pages; each page's removal and docs-only filing refused |
| scope-classification | `python3 scripts/ci_scope.py docs/testing/CI_WORKFLOWS.md` | rc 0 | Prints `false`: the edited page stays documentation only |
| hygiene | `python3 scripts/check_hygiene.py --check` | rc 0 | hygiene-controls: 35/35 |
| hygiene-controls | `python3 scripts/check_hygiene.py --selftest` | rc 0 | 35/35 controls |
| doc-map | `python3 docs/DOC_MAP.gen.py --check` | rc 0 | doc-map-controls: wrong-raster control |
| doc-map-controls | `python3 docs/DOC_MAP.gen.py --selftest` | rc 0 | Valid wrong-raster control |
| gate-read-paragraph | `python3 -I "$EVIDENCE/round4/gate_read_paragraph.py" --repo .` | rc 0 | 8 linked = 8 registered; 6/6 planted controls refused |
| integrity | `python3 -I "$EVIDENCE/round4/integrity.py" --repo .` | rc 0 | Parent, one changed path, raw blobs, modes, pins and clean state |

The gate-read-paragraph controls restore "Seven", state "Eight" and state "8".
They also unlink `MAILBOX_SPLIT.md`, add an unlinked registration and drop a registration.
Each is refused. Diagnostic `paragraph-before` runs the same check on the
`532ab871` page and table and returns rc 1 on line 179's "Seven pages".
That reproduces both reviews' finding.

`round4/gate-ledger.json` records each command, exit, duration, raw-log size and
SHA-256, and receipt hash. Receipts are in `round4/evidence/`, with host
directories replaced by `$EVIDENCE` and `$WORK`. No receipt exceeds 200000 bytes.
No toolchain, installed package, tree export or file over 200000 bytes was added.

### Round 4 retained image, pin, predicate, coverage and mutation evidence

`round4/final-state.json` verifies the parent `532ab871`, the single changed path,
1311 superproject blobs, and 1043 dependency blobs at unchanged gitlinks.
No production source, configuration, image builder or runtime input changed.
No firmware was rebuilt. All 30 retained before/after ELF files in scratch were
rehashed against the Round 3 image table; 30/30 sizes and SHA-256 values match
(`round4/retained-image-audit.json`). That table, its 988 to 1304 byte Release
growth, and the byte-identical BIOS and AEM descriptor remain current.

The pin remains `70936b77dc41981e192438388cd0aced69954f18`, verified by the
integrity check at the stack root, own origin, head and every tracked blob.
The pin section and `pin-proof.json` keep the merge commits and 45-path file list.
The predicate and its fresh-probe, Listener, neither, expired-probe,
source-validity and two-interface controls are unchanged.
Coverage stays adjusted 100% lines and branches over 30 files.
The mutation tables stay 520, 76 and 278 caught, with no escapes.
These are the round 2 measurements, carried with unchanged inputs.

### Round 4 handoff and remaining duties

The working tree and five initialized dependencies are clean, including ignored
and untracked files. The unused external dependency remains uninitialized.
The one new commit uses the configured identity, a one-line subject and no body or trailers.
No generated repository file was edited.

The prepared PR body starts with `[A612]`, says `Relates to #665`, names the
new head as the published head, and adds a Round 4 section. No PR or existing
issue/PR comment was edited.

The manager owns the push, the local workflow replica and exact-head hosted
acceptance. Independent new-head reviews, current-dev candidate validation,
explicit merge authorization and post-merge containment also remain open.
No review verdict is supplied here. No hardware, bench, flashing or physical
timing evidence is claimed.

The `[A612] REVIEW READY` comment with this head is
[comment 6157070074](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6157070074),
the final authorized public write for this round. No TAKEN comment is repeated.
