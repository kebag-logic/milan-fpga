## Status

READY FOR REVIEW, local evidence only.

- Branch: `pf-linuxprof-1` -> `dev-soft-core`.
- Three commits on `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`:
  - `677d605f37c3a80654df1dd2cde053b57242845b` (round 1);
  - `66b4def34dcbc0d371ce4eb339d3d0226875befa` (round 2, answering R900-1);
  - `58f7673b8c57a80230e716bc1774ff9cc2f71ddc` (round 3, answering R902-1).

Published head: `58f7673b8c57a80230e716bc1774ff9cc2f71ddc`. The evidence below is local source-head evidence; hosted acceptance is tracked separately.

Round 3, at `58f7673b`:

- The FPGA rows of THE SHAPES are byte-identical to the base, and the host shape is stated outside them.
- The service-budget harness reads the table as at the base:
  - `shape_costs.py --check` passes;
  - `shape_costs.py --selftest` refuses 25 of 25 controls;
  - `load_grade.py --check` passes;
  - `flip_grade.py --check --point 1x1/1if` passes;
  - each of those outputs is identical to the base's.
- `flip_grade.py --check` over all points produces output byte-identical to the base's.
- Gates 32, 41, 42 and `test_bad_configs_rejected` pass.
- Docs and quality gates: 25 of 25 pass.
- FPGA artifact identity: 245 of 245 byte-identical to the base.
- The board repository's host build compiles to byte-identical objects and binary at `66b4def3` and `58f7673b`.

Earlier rounds:

- Round 1, at `677d605f`: the builder suite ran 114 of 115 gates, each once, in four subsets. Gate 1b did not complete inside the ten-minute command bound (see limitations).
- The full suite has not been re-run since.

## Linked Issue / roles

Closes #983
Relates to kebag-logic/ti-sitara-am65x-bsp#29

Executor: `[A830]`
Internal cleared-context reviewer: `[R902]` (R902-1 NEGATIVE at `66b4def3`; round 3 answers it)
External reviewer: `[R900]` (R900-1 NEGATIVE at `677d605f`; R900-2 POSITIVE at `66b4def3`; round 3 changes artifacts in the Conformance, RTL, Tests and Docs lenses, so those need covering again at `58f7673b`)

## Description

A descriptor-only host profile for the end-station generators. It covers a board that runs the split control firmware as a host program on the mailbox model (`sw/firmware/ctrl/host/mbx_model.c`), with its own PHC as gPTP owner.

| Piece | Change |
|---|---|
| `sw/builder/endstation_builder.py` | Details below this table. |
| `configs/host/endstation_host_example.yaml` | The annotated example: #983's first inventory. One AAF input (48 kHz, 8 ch, 32-bit), one CRF input and one AAF output; ADP 1 source, 2 sinks. It is outside `configs/endstation_*.yaml`, so no FPGA gate enumerates it. |
| `sw/firmware/ctrl/loop/ctrl_loop.h` | A guard before THE SHAPES, `#if defined(CTRL_HOST_PLATFORM) && CTRL_LOOP_SHAPE(1u, 1u, 2u)`, includes the host shape's header in their place; `#else` is THE SHAPES as at the base, byte for byte (the 39-line chain, its four FPGA rows and its `#error`). No figure is defined in `ctrl_loop.h` outside the chain, so `shape_costs.py`, which the service-budget gates read the table through, and every reader that takes a figure's first definition read the FPGA table unchanged. No build input in this tree defines the macro. |
| `sw/firmware/ctrl/host/ctrl_loop_host.h` | New. The host shape's figures, which are 1x1/1if's, held as a stated host scheduling profile; its comment says what that profile claims and what it does not. It refuses any build but a `CTRL_HOST_PLATFORM` one at (1, 1, 2) through `ctrl_loop.h`. It sits in `host/`, beside the mailbox model, and not in `loop/`, whose headers the firmware's base plant compiles on their own. |
| `sw/builder/test_builder.py` | Gate 41 and gate 42. Details below this table. |
| `docs/ENDSTATION_BUILDER.md` | New section 6: the profile, what it feeds, what is unchanged, the keys that differ (rows `H1` to `H9`, apart from section 3's numbering), the TSpec rule and its clause, the station MAC substitution a board owns, and the host shape and where it is stated. Row 5d for `board.gptp_owner`. The section 3 Contents counts are corrected to the table's (75 rows, 116 keys), from the stale 66 and 107. |

**`endstation_builder.py` in detail.**

- `board.target: host` (`HOST_TARGET`) sits outside `BOARDS`.
- `load_config` reads the target with `_req`, as `_load_board` does. So a `board` that is a list or a string is refused by the same `ConfigError` as before the profile.
- The profile has its own loaders:
  - a board loader: `board.gptp_owner: host-phc`, `board.constraints.link_mbps` and `num_queues`;
  - a gPTP loader: every Announce field and `port_number` stated, latency corrections refused;
  - the `usb_audio` interface family (`HOST_INTERFACES`), its width from `audio_interface.channels`.
- It has no SoC, fabric blocks, render-lane bound or framer supply cap. Every other loader and check is the FPGA path's, unchanged.
- `build()` refuses the profile by name.
- An FPGA target that names `board.gptp_owner` is now refused instead of ignored.
- The FPGA features block moved into `_load_fabric_features` unchanged.

**Gate 41 in detail.**

- The example feeds the overlay, the AEM image (packer lint), `adp_entity.py`, `aecp_entity.py` and `srp_entity.py`, and these agree with each other.
- ENTITY serves 1/2, and AVB_INTERFACE carries the stated dataset octet for octet.
- `build()` refuses the profile.
- Section 6's key table is held to the host loaders, gate 32's twin.
- The host TSpec rule: a talker whose current format is 2 channels and which advertises 2 and 8 reserves the 8-channel 217 octets, not 73.
- THE SHAPES are read through `shape_costs.py` itself. The table must read, list no host row, and define each figure once per listed row and nowhere else. Two plants are refused: the host row inside the chain, and the host figures beside it in `ctrl_loop.h`.
- The macro selects the host figures. They must be the 1x1/1if row's, and the shape is refused without the macro and at two interfaces.
- At one and at two interfaces (the contract force-included, `MBX_N_IF` printed and checked), every FPGA config's compiled row equals its row with the macro and the row `shape_costs.py` reads.
- Only the guard, the host header, the docs and the gate name the macro.

**Gate 42 in detail.** 31 planted defects:

- 8 on the FPGA 1x1: three malformed `board` values, and five missing-fabric-owner and retarget cases;
- 23 on the host example.

`_key_map_rows` takes an optional heading; gate 32's call is unchanged.

**The host TSpec rule.** MaxFrameSize uses the widest `channels_per_frame` any talker advertises (`framer_declared_channels`). Every talker row shares that width at `clocking.sampling_rate_hz`. It is not each talker's current format. The clause is IEEE 802.1Q-2018 35.2.2.8.4 a): MaxFrameSize is "the maximum frame size that the Talker will produce".
- The control firmware declares one fixed TSpec per source (`ctrl_plat.c` `configure_sources`).
- SET_STREAM_FORMAT moves a STREAM_OUTPUT that is not streaming to any format it advertises (`aecp_commands.c`), and the declaration stays in place.
- MSRP changes no FirstValue of a declared StreamID short of a withdrawal and two LeaveAllTime periods (35.2.2.8).

So the widest advertised format's frame is one the talker can produce. Milan v1.2 4.3.3.2 Table 4.4 gives each format's value, and the profile takes the largest. The FPGA path keeps its supply cap because its fabric emits a fixed width. Round 2 changed the documentation of this rule, not the calculation. The generated image for the board's `config/endstation_pb2_bridge.yaml` (kebag-logic/ti-sitara-am65x-bsp at `cce8c9a4`) is unchanged: 5784 bytes, the same sha256, talker MaxFrameSize 217.

**The host shape and the board's build.**

- The board repository's host build compiles every firmware unit with `-DCTRL_HOST_PLATFORM` and its generated shape header. Its commit `afc35064` pins `66b4def3`.
- At `66b4def3` and at `58f7673b`, its unmodified Makefile builds the control program to 35 byte-identical objects and a byte-identical binary. `ctrl_loop.o` is sha256 `204afd95...` at both.
- The host shape's macros are identical at both revisions: 950, 1010, 735, 285, 85, 34, 130 and 35, at `MBX_N_IF 1u`.
- Its generated `aecp_entity_gen.h` and `srp_entity_gen.h` are byte-identical (`CTRL_SRP_SOURCES 1u`, `CTRL_SRP_SINKS 2u`). Its `entity.conf` and `nvm_shape_gen.h` differ only in the milan-fpga revision line they record.
- Moving its pin to this head is the board repository's change.

**Material assumptions, stated rather than chosen privately.**

- The tracked tree is bare-metal only (#259, `scripts/check_baremetal_only.py`). So the profile and its fixtures use the tree's existing host-program vocabulary, never the retired-stack terms. No tracked YAML carries a false `fabric_gptp`; the host profile has no such key. Planted defects are written to temporary files at test time. The bare-metal scope gate passes on the head: 0 findings over 1910 files, self-test 867 arms.
- An FPGA config whose shape is (1, 1, 2), the all-fabric `arty_current`, would take the host figures under the macro, as it would have at `66b4def3`. No build input defines the macro, and gate 41 reports that point separately.

## Authoritative references

- IEEE 1722.1-2021 7.2.1 (a Configuration descriptor is required), 7.2.8 and Table 7-13 (AVB_INTERFACE gPTP fields), Table 7-2 (ENTITY fields repeat ADP's).
- Milan v1.2 7.2.2 (an AAF talker requires a CRF input), 7.2.3 (two AAF inputs require a CRF output), 5.3.3.4, 5.3.3.6, 5.3.3.9, 6.4; 4.3.3.2 Table 4.4 (MaxFrameSize per format).
- IEEE 802.1Q-2018 35.2.2.8.4 a) (MaxFrameSize: the maximum frame the Talker will produce), 35.2.2.8 (no FirstValue change for a declared StreamID short of a withdrawal and two LeaveAllTime periods).
- IEEE 802.1AS-2011 8.1 (domain 0), 8.6.2.3; IEEE 1588-2008 7.6.2.5 Table 6.
- `docs/ENDSTATION_BUILDER.md` sections 3 and 6; `ctrl_loop.h` THE SHAPES; `tb/verilator/ctrl_service_budget/shape_costs.py` (the table's reader, unchanged).

## How to get into the same state

```sh
git fetch origin && git checkout pf-linuxprof-1   # head 58f7673b8c57a80230e716bc1774ff9cc2f71ddc
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
cd tb/verilator/ctrl_service_budget && for a in "shape_costs.py --check" "shape_costs.py --selftest" \
  "load_grade.py --check" "flip_grade.py --check --point 1x1/1if"; do python3 -B $a; done; cd -
python3 scripts/check_baremetal_only.py --check && python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base 854bd7236792ce1adbd10c43b13a6a5002ad3bb6
python3 scripts/check_py_idiom.py
```

Expected:

- Gate 32: 116 keys == 116.
- Gate 41: three report lines.
  - The first ends "a talker advertising 2 and 8 channels at current 2 reserves 217 octets, the widest format's, not the current 73".
  - The second names the 4 FPGA rows `shape_costs.py` reads and the two refused placements.
  - The third says the macro moves none of the 4 compiling FPGA points' rows.
- Gate 42: 31/31 refused (8 FPGA, 23 host).
- The three headers carry ADP 1/2, `CTRL_SRP_SOURCES 1u`/`CTRL_SRP_SINKS 2u`, and the image CRC.
- The four budget commands print `RESULT: PASS` or "25 of 25 planted controls refused".
- Every command exits 0.

FPGA identity, at base and `58f7673b`:

- Every `configs/endstation_*.yaml` is built at its own placement, `split` and `all-fabric`. That covers the builder outputs, the sweep script, the AEM image pair and the four firmware generator headers (adp, aecp, srp, ctrl_plat policy).
- All 245 artifacts are byte-identical to the base and to round 2's receipt.
- A full-tree run, each revision with its own builder and generators, gives 240 of 240 byte-identical.
- `ctrl_loop.h`'s full macro set and diagnostics match the base at 12 points: 5 FPGA shape headers and none, each at `MBX_N_IF` 1 and 2. The 6 points that compile give byte-identical `ctrl_loop.o`.

## Known limitations / out of scope

- **Gate 1b and the full suite.** Gate 1b (`test_baremetal_profile_contract`, the builder's leg 0) did not complete in round 1. It runs one gate past the ten-minute bound on every command here. Before the bound, its builder-dependent arms printed PASS: 5 product configs and 11 refusal arms. Its remaining arms read firmware, SoC and RTL sources this change does not touch. The hosted `docs` and `elaborate` legs owe it. The full builder suite has not been re-run since round 1 and is owed with the final candidate.
- **Rounds 2 and 3 ran only what they touch.** Round 2 re-ran gates 32, 41, 42 and `test_bad_configs_rejected`, the docs and quality gates, and the identity gate. Round 3 re-ran those as well as the service-budget harness, the preprocessing and object comparison, and the board's host build.
- **The builder legs' union.** `ci_builder_legs.py`'s own union was not used, because each leg exceeds the bound. Round 1's four subset receipts were judged by a lane-local script instead: every other gate ran exactly once and passed. The one NOT RUN row is gate 11's calibration report, which is not on this machine.
- **The firmware gate's four shards** each exceed the bound, and the mutation campaigns (shards 1 to 3) were not run. In their place:
  - at round 3, `ctrl_loop.h`'s full macro set and diagnostics match the base at the 12 points above, and `ctrl_loop.o` is byte-identical at the 6 that compile;
  - the host header is reached only under `CTRL_HOST_PLATFORM`, which no arm defines;
  - at round 1, the arms that compose AECP and the platform passed: service bounds and every-shape SRP builds with RV32 (21), AECP (18), split platform (8).
- **The service-budget harness** is not in the builder or firmware banks, and no hosted workflow runs it. So the manager's candidate validation should run it explicitly. `run.py --self-test` reached its 580 s bound at both base and head, with identical output up to the bound, so its verdict is not established at either.
- **`board` values that cannot be iterated.** A `board` of `null` or an integer raises TypeError at the base and still does. That is base behaviour, outside the host dispatch, and not changed here. So is a non-integer `gptp.clock_accuracy`, which raises ValueError on both paths.
- **The host shape** is a stated scheduling profile, not a measurement, and no board measurement is claimed. Its millisecond bounds rest on thread preemption, which nothing here measures.
- **Building and installing the host program** is the board repository's work (kebag-logic/ti-sitara-am65x-bsp#29); this profile does not do it.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (profile generates image and ADP fields through the AEM checks; identity gate; FPGA scheduler-shape guard and rows unchanged and read unchanged; docs)
- [x] New or changed behavior has self-checking tests (gates 41, 42; each check has a planted control; round 3's checks fail on the round-2 placement and four other mutants)
- [ ] Required local verification bar passes (gate 1b and the firmware mutation shards not completed here; full builder suite not re-run since round 1)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive (R902-1 NEGATIVE at `66b4def3`; re-review of `58f7673b` pending)
- [ ] External review is positive (R900-2 POSITIVE at `66b4def3`; the lenses round 3 touches need covering at `58f7673b`)
- [ ] Blocking and major findings are fixed and re-reviewed (R902-1-F1 addressed at `58f7673b`; re-review pending)
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
