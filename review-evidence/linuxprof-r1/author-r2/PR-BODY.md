## Status

READY FOR REVIEW, local evidence only: `pf-linuxprof-1` -> `dev-soft-core`, two commits on `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`: `677d605f37c3a80654df1dd2cde053b57242845b` (round 1) and `66b4def34dcbc0d371ce4eb339d3d0226875befa` (round 2, answering R900-1).

Published head: `677d605f37c3a80654df1dd2cde053b57242845b`. Round 2's head `66b4def34dcbc0d371ce4eb339d3d0226875befa` is committed locally and becomes the published head when it is pushed. The evidence below is local source-head evidence; hosted acceptance is tracked separately.

Round 2 (at `66b4def3`): gates 32, 41, 42 and `test_bad_configs_rejected` pass. Docs and quality gates: 24 of 24 pass. FPGA artifact identity: 245 of 245 byte-identical to the base and to `677d605f`, over 5 configs at own, split and all-fabric placements. Round 1 (at `677d605f`): builder suite 114 of 115 gates pass, each run once in four subsets; gate 1b did not complete inside the ten-minute command bound (see limitations). The full suite was not re-run at `66b4def3`.

## Linked Issue / roles

Closes #983
Relates to kebag-logic/ti-sitara-am65x-bsp#29

Executor: `[A830]`
Internal cleared-context reviewer: to be assigned
External reviewer: `[R900]` (round R900-1 NEGATIVE at `677d605f`; round 2 answers it)

## Description

A descriptor-only host profile for the end-station generators. It covers a board that runs the split control firmware as a host program on the mailbox model (`sw/firmware/ctrl/host/mbx_model.c`), with its own PHC as gPTP owner.

| Piece | Change |
|---|---|
| `sw/builder/endstation_builder.py` | `board.target: host` (`HOST_TARGET`), outside `BOARDS`. `load_config` reads the target with `_req`, as `_load_board` does, so a `board` that is a list or a string is refused by the same `ConfigError` as before the profile. The profile has its own board loader (`board.gptp_owner: host-phc`, `board.constraints.link_mbps`/`num_queues`), its own gPTP loader (every Announce field and `port_number` stated, latency corrections refused) and the `usb_audio` interface family (`HOST_INTERFACES`, width from `audio_interface.channels`). It has no SoC, fabric blocks, render-lane bound or framer supply cap. Every other loader and check is the FPGA path's, unchanged. `build()` refuses the profile by name. An FPGA target that names `board.gptp_owner` is now refused instead of ignored. The FPGA features block moved into `_load_fabric_features` unchanged. |
| `configs/host/endstation_host_example.yaml` | The annotated example: #983's first inventory. One AAF input (48 kHz, 8 ch, 32-bit), one CRF input and one AAF output; ADP 1 source, 2 sinks. It is outside `configs/endstation_*.yaml`, so no FPGA gate enumerates it. |
| `sw/firmware/ctrl/loop/ctrl_loop.h` | THE SHAPES gains `#elif defined(CTRL_HOST_PLATFORM) && CTRL_LOOP_SHAPE(1u, 1u, 2u)`. Its figures are 1x1/1if's, held as a stated host scheduling profile; the comment says what that profile claims and what it does not. The FPGA rows and the `#error` are untouched. No build input in this tree defines the macro, and gate 41 holds that. |
| `sw/builder/test_builder.py` | Gate 41: the example feeds the overlay, the AEM image (packer lint), `adp_entity.py`, `aecp_entity.py` and `srp_entity.py`, which agree with each other. ENTITY serves 1/2 and AVB_INTERFACE carries the stated dataset octet for octet. `build()` refuses the profile. THE SHAPES builds (1, 1, 2) with the macro alone, and the macro moves no listed FPGA row. Section 6's key table is held to the host loaders, gate 32's twin. The host TSpec rule is held too: a talker whose current format is 2 channels and which advertises 2 and 8 reserves the 8-channel 217 octets, not 73. Gate 42: 31 planted defects, 8 on the FPGA 1x1 (three malformed `board` values, five missing-fabric-owner and retarget cases) and 23 on the host example. `_key_map_rows` takes an optional heading; gate 32's call is unchanged. |
| `docs/ENDSTATION_BUILDER.md` | New section 6: the profile, what it feeds, what is unchanged, the keys that differ, the TSpec rule and its clause, the station MAC substitution a board owns, and the host shape row. Row 5d for `board.gptp_owner`. The section 3 Contents counts are corrected to the table's (75 rows, 116 keys), from the stale 66 and 107. |

**The host TSpec rule.** MaxFrameSize uses the widest `channels_per_frame` any talker advertises (`framer_declared_channels`). Every talker row shares that width at `clocking.sampling_rate_hz`. It is not each talker's current format. The clause is IEEE 802.1Q-2018 35.2.2.8.4 a): MaxFrameSize is "the maximum frame size that the Talker will produce".
- The control firmware declares one fixed TSpec per source (`ctrl_plat.c` `configure_sources`).
- SET_STREAM_FORMAT moves a STREAM_OUTPUT that is not streaming to any format it advertises (`aecp_commands.c`), and the declaration stays in place.
- MSRP changes no FirstValue of a declared StreamID short of a withdrawal and two LeaveAllTime periods (35.2.2.8).

So the widest advertised format's frame is one the talker can produce. Milan v1.2 4.3.3.2 Table 4.4 gives each format's value, and the profile takes the largest. The FPGA path keeps its supply cap because its fabric emits a fixed width. Round 2 changed the documentation of this rule, not the calculation. The generated image for the board's `config/endstation_pb2_bridge.yaml` (kebag-logic/ti-sitara-am65x-bsp at `cce8c9a4`) is unchanged: 5784 bytes, the same sha256, talker MaxFrameSize 217.

Material assumption, stated rather than chosen privately: the tracked tree is bare-metal only (#259, `scripts/check_baremetal_only.py`). So the profile and its fixtures use the tree's existing host-program vocabulary, never the retired-stack terms. No tracked YAML carries a false `fabric_gptp`; the host profile has no such key. Planted defects are written to temporary files at test time. The bare-metal scope gate passes on the head (0 findings over 1909 files, self-test 867 arms).

## Authoritative references

- IEEE 1722.1-2021 7.2.1 (a Configuration descriptor is required), 7.2.8 and Table 7-13 (AVB_INTERFACE gPTP fields), Table 7-2 (ENTITY fields repeat ADP's).
- Milan v1.2 7.2.2 (an AAF talker requires a CRF input), 7.2.3 (two AAF inputs require a CRF output), 5.3.3.4, 5.3.3.6, 5.3.3.9, 6.4; 4.3.3.2 Table 4.4 (MaxFrameSize per format).
- IEEE 802.1Q-2018 35.2.2.8.4 a) (MaxFrameSize: the maximum frame the Talker will produce), 35.2.2.8 (no FirstValue change for a declared StreamID short of a withdrawal and two LeaveAllTime periods).
- IEEE 802.1AS-2011 8.1 (domain 0), 8.6.2.3; IEEE 1588-2008 7.6.2.5 Table 6.
- `docs/ENDSTATION_BUILDER.md` sections 3 and 6; `ctrl_loop.h` THE SHAPES.

## How to get into the same state

```sh
git fetch origin && git checkout pf-linuxprof-1   # head 66b4def34dcbc0d371ce4eb339d3d0226875befa once pushed
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt && python3 -m pip install pyyaml
```

## How to validate

```sh
python3 sw/builder/test_builder.py --gates test_builder_doc_key_map,test_host_profile_feeds_the_generators,test_host_profile_refusals
python3 sw/builder/test_builder.py --gates test_bad_configs_rejected
for t in adp/adp_entity aecp/aecp_entity srp/srp_entity; do
  python3 sw/firmware/ctrl/$t.py configs/host/endstation_host_example.yaml -o /tmp/$(basename $t).h; done
python3 sw/builder/endstation_builder.py configs/host/endstation_host_example.yaml   # refused by name, exit 1
python3 scripts/check_baremetal_only.py --check && python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base 854bd7236792ce1adbd10c43b13a6a5002ad3bb6
python3 scripts/check_py_idiom.py
```

Expected:
- Gate 32: 116 keys == 116.
- Gate 41: two report lines, the first ending "a talker advertising 2 and 8 channels at current 2 reserves 217 octets, the widest format's, not the current 73".
- Gate 42: 31/31 refused (8 FPGA, 23 host).
- The three headers carry ADP 1/2, `CTRL_SRP_SOURCES 1u`/`CTRL_SRP_SINKS 2u`, and the image CRC.
- Every gate exits 0.

FPGA identity, at base, `677d605f` and `66b4def3` on the same tree: every `configs/endstation_*.yaml` is built at its own placement, `split` and `all-fabric`. Each revision's builder blob is loaded against unchanged dependencies. That covers the builder outputs, the sweep script, the AEM image pair and the four firmware generator headers (adp, aecp, srp, ctrl_plat policy). All 245 artifacts are byte-identical across the three revisions, and the tracked tree is clean.

## Known limitations / out of scope

- Gate 1b (`test_baremetal_profile_contract`, the builder's leg 0) did not complete in round 1. It runs one gate past the ten-minute bound on every command here. Its builder-dependent arms printed PASS (5 product configs, 11 refusal arms) before the bound; its remaining arms read firmware, SoC and RTL sources this change does not touch. The hosted `docs` and `elaborate` legs owe it.
- Round 2 re-ran only the gates its change touches (32, 41, 42, `test_bad_configs_rejected`), the 24 docs and quality gates, and the identity gate. The full builder suite at `66b4def3` is owed with the final candidate.
- `ci_builder_legs.py`'s own union was not used, because each leg exceeds the bound. Round 1's four subset receipts were judged by a lane-local script instead: every other gate ran exactly once and passed. The one NOT RUN row is gate 11's calibration report, which is not on this machine.
- The firmware gate's four shards each exceed the bound. In their place, at round 1:
  - `ctrl_loop.h` is token- and macro-identical at base and head for no shape header, 1x1 and 8x8.
  - The three Arty shapes are refused at both, and their diagnostics differ only in the `#error`'s line, 397 to 424.
  - The arms that read THE SHAPES or compose AECP and the platform ran on the gate's own tree and passed: service bounds and every-shape SRP builds with RV32 (21), AECP (18), split platform (8).
  - The mutation campaigns (shards 1 to 3) were not run.

  Round 2 touches no firmware.
- A `board` that cannot be iterated (`null`, an integer) raises TypeError at the base and still does. That is base behaviour, outside the host dispatch, and not changed here.
- The host shape row is a stated scheduling profile, not a measurement, and no board measurement is claimed. Its millisecond bounds rest on thread preemption, which nothing here measures.
- The profile does not build, package or install the host program; that is the board repository's (kebag-logic/ti-sitara-am65x-bsp#29).

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (profile generates image and ADP fields through the AEM checks; identity gate; docs)
- [x] New or changed behavior has self-checking tests (gates 41, 42; each check has a planted control, and the round 2 additions fail at `677d605f` or under a mutant)
- [ ] Required local verification bar passes (gate 1b and the firmware mutation shards not completed here; full builder suite not re-run at `66b4def3`)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive (R900-1 NEGATIVE at `677d605f`; re-review of `66b4def3` pending)
- [ ] Blocking and major findings are fixed and re-reviewed (R900-1's two MINOR findings and the residue addressed at `66b4def3`; re-review pending)
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
