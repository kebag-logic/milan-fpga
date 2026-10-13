[A612]

# F3b parent implementation handoff

Status: REVIEW READY, local author validation passed.
Branch: `665-f3b-parent`. Base: `d40e4e9827be2516f8f34b9d65f0a483fff2194c`.
Final local head: `db29bdd07529fbc697b7956827092f64b1241714`.
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
