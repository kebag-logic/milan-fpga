[R751] NEGATIVE - exact head cb07597bc33106933c708a45f92c91f17a7a3e61

Internal cleared-context review, round R751-1, of kebag-logic/milan-fpga PR #824 (Issue #797, documentation lane G1, executor A712).
Head `cb07597bc33106933c708a45f92c91f17a7a3e61`, tree `5b5fff698d74f1ebe05a1661ae22928cdc670a74`, source base dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`.
Whole-PR review of `git diff 1e80128f..cb07597b` (14 files, +2668/-57).

## Summary

The guide, both generators and the CI wiring are largely sound.
The 1x1 descriptor tree, the model-ID resolution, the worked example and every resource, moves and artifact row I checked agree with the builder and with the packed descriptor image.
Both `--check` gates refused all 11 of my planted defects.

Two open MINOR findings make the verdict NEGATIVE. Both are factual errors in the generated key reference (`sw/builder/README-parameters.md`):

- **F1:** the Clause column of two keys is taken from the wrong cell, and the gate cannot see it.
- **F2:** one key's stated limit is narrower than what the builder accepts.

## Findings

### F1 - MINOR - Conformance, Robustness, Tests, Docs

**Where:** `sw/builder/gen_key_reference.py:332-336` (`contract()`). Artifact: the `sw/builder/README-parameters.md` key-reference rows `clocking.crf_output.enabled` and `clocking.crf_output.format`.

**Evidence:**
- `contract()` splits each section 3 table line on every `|`.
- Row 27 of `docs/ENDSTATION_BUILDER.md` (line 1061) has a Markdown-escaped pipe in its "Generates" cell: `CLOCK_SYNC_SOURCE\|CLASS_A (0x0003)`.
- The split therefore shifts the cells. `cells[3]`, read as "Clause ref", is really the rest of the Generates cell. Both rows print a long paragraph starting `CLASS_A (0x0003); domain wiring = ...` in the Clause column.
- Split with escapes respected, the row has five cells, and its Clause ref cell is `Milan 7.2.3, 7.3.2 (format 0x041060010000BB80), 7.3.3 (Class A); 1722.1 7.2.6, 7.2.6.1, 7.2.9.2, 7.2.32`.
- Probe `receipts/mutant_F1_clause_blind.log`: I replaced row 27's real clause cell with `Milan 9.9.9 (planted)`. `gen_key_reference.py --check` still returned rc 0, "fresh".
- So for these two keys the Clause column is not derived from the clause cell, and the gate is blind to that cell.
- Gate 32's own `_key_map_rows` reads only `cells[1]`, which comes before the escape, so the Row column is unaffected.

**Impact:** a generated table published as authoritative shows a wrong clause claim for two keys, and the freshness gate cannot detect any change to their real clause.

**Required outcome:**
- The clause cell is read with Markdown escaped pipes respected.
- A row whose cell count is not the table's column count is refused rather than read.
- The page is regenerated.
- `--selftest` gains an arm that plants a change in a clause cell behind an escaped pipe and must see the page go stale.

**Verification:**
- Regenerate. Both rows show the row 27 clause above.
- Rerun the planted-clause probe: it must give rc 1.
- `--selftest` reports the new arm.

### F2 - MINOR - Conformance, Docs

**Where:** `sw/builder/key_reference.yaml:235`. Artifact: the `clocking.audio_unit_rates_hz` row of the generated key reference, "at most `8` distinct base rates, including `sampling_rate_hz`".

**Evidence:**
- `_load_clocking` (`sw/builder/endstation_builder.py:3983-4007`) checks three things only: the number of entries (at most `MAX_AUDIO_UNIT_RATES`), that they are distinct, and that `sampling_rate_hz` is among them.
- It does not require a base rate. Only `sampling_rate_hz` is held to `BASE_RATE_HZ` (line 3955).
- Probe `receipts/probe_claims.log`: `audio_unit_rates_hz: [48000, 44100]` is accepted.
- `receipts/full_build_r441.log`: the full builder run exits 0. Its build plan marks the 44100 Hz rate "planned" (`endstation_builder.py:4725-4733`) rather than refusing it.

**Impact:** a reader is told that a value the builder accepts and advertises as a SET_SAMPLING_RATE target would be refused. That bound claim disagrees with the source.

**Required outcome:**
- Either the row states the real limit: distinct integer rates, at most `MAX_AUDIO_UNIT_RATES`, including `sampling_rate_hz`, with a rate the render path cannot run marked planned in the build plan.
- Or the builder refuses a non-base rate. That is a behaviour change for its own Issue, not this lane.
- Either way, an `ok` (or `bad`) probe value holds the statement to the builder.

**Verification:** `gen_key_reference.py --check` is fresh after regeneration, and the new probe value is accepted (or refused) as stated.

### S1 - SUGGESTION - Docs

**Where:** the `board.constraints.num_queues` row.

**Evidence:**
- Allowed reads "an integer above `srp.class_queue`".
- The builder also bounds the value to 1..8 (`endstation_builder.py:3940-3941`).
- The row's meaning says it "must equal the RTL's queue count". The builder does not enforce that: `num_queues: 6` loads, builds with rc 0 and emits `milan_csr.NUM_QUEUES: 6` (`receipts/probe_claims.log`, `receipts/full_build_nq6.log`).
- Only `test_builder.py` gate 18c pins tracked configurations to `ethernet_packet_pkg::NUMBER_OF_QUEUES` (`test_builder.py:20761`).

**Suggestion:** name the 1..8 bound and say the equality is a gate 18c check on tracked configurations, not a builder refusal.

### S2 - SUGGESTION - Tests

**Where:** `docs/diagrams/endstation_definition.gen.py:494`.

**Evidence:** the "Tracked copy" column is measured with `Path.is_file()`, not `git ls-files`. It is true at this head: I confirmed all four paths are tracked. But an untracked file at one of those paths would also read "yes".

**Suggestion:** measure tracking with `git ls-files --error-unmatch`.

### S3 - SUGGESTION - Docs

**Where:** `docs/guides/DEFINING_THE_END_STATION.md:459-465`.

**Evidence:** workflow step 4 shows one command, `make -C tb/verilator/csr`, while the table below it lists eight suites for the shipping 1x1.

**Suggestion:** name the command pattern that covers each listed suite.

No RESIDUE item was found. The comment-rule scan of the added source lines found no lane labels, review rounds, reviewer IDs or comment IDs (`lane` hits are the hardware loopback and render lanes).

## Lens evidence

### Conformance: UNCLEAN (F1, F2)

**Key reference sampled against the builder** (`sw/builder/endstation_builder.py`). I checked 30 keys by reading the source and, where marked, by a live probe (`receipts/probe_claims.log`):

| Key | What I checked |
|---|---|
| `entity.group_name` | 63 octets, line 3742 (probe) |
| `entity.serial_number`, `entity.name` | 63 octets, line 3742 |
| `entity.locale` | 64 octets via `_aem_string`, line 3768 (probe) |
| `entity.vendor_name` | no length check, lines 3733 and 3741 (probe) |
| `entity.firmware_rev` | non-negative and not a bool, line 3728 (probe) |
| `entity.firmware_version` | refused, line 3720 |
| `entity.vendor_oui` | I/G bit refused, line 3787; must match a pin or literal, line 4500 |
| `entity.model_id_pin` and `entity.entity_model_id` | resolution order, lines 4493-4499 |
| `board.constraints.sys_clk_hz` | default 100000000 on both boards, lines 201 and 207; at least `milan_clk_hz`, line 3942 (probe) |
| `board.constraints.uart_baudrate` | default 115200 and `int()` `ValueError`, line 3914 (probe) |
| `board.constraints.num_queues` | 1..8, line 3940 (see S1) |
| `board.constraints.floorplan`, `board.constraints.gtx_tx_invert` | read with `bool()`, lines 3911-3912 and 3925 |
| `board.constraints.flashboot` | default `baremetal`, lines 3913 and 3927 |
| `board.constraints.eth_port` | line 3944 |
| `board.constraints.phy` | line 3922 |
| `board.constraints.l2_bytes`, `board.constraints.milan_clk_hz` | required, lines 3907-3908 |
| `clocking.media_clock_sources` | default internal and crf, line 3958 |
| `clocking.default_source` | lines 3974-3976 |
| `clocking.audio_unit_rates_hz` | lines 3998-4007 (F2) |
| `streams.listeners[].channels` | 1..32, line 1469 (probe) |
| `streams.listeners[].buffer_length_ns` | lines 1423-1431 |
| `streams.talkers[].channels` | wire clamp 2..8, lines 804 and 1189-1190 |
| `srp.class_queue` | 3 bits and below `num_queues`, lines 348 and 2035-2041 (probe) |
| `srp.bandwidth_limit_pct` | 1..75 (probe) |
| `srp.tspec.max_frame_bytes` | line 2053 |
| `platform.pp_mem_phys` | default and 4 KiB alignment, lines 453 and 457 (probe) |
| `gptp.priority1` | probed |
| `gptp.ingress_latency_ns`, `gptp.egress_latency_ns` | 0..65535, line 4116 |
| `names.*` | 64 octets via `_aem_string`; `names.clock_sources` refused for a source the config does not emit, line 3862 |
| `board.features.*` | the seven prune flags and parameters read off `OPTIONAL_BLOCKS` |

**Descriptor tree.** I decoded the packed `aem_desc.bin` for `configs/endstation_ax7101_1x1_tdm8.yaml` independently (`scripts/decode_1x1_image.py`, `receipts/decode_1x1_image.log`).

- The counts match the tree exactly: ENTITY 1, CONFIGURATION 1, AUDIO_UNIT 1, STREAM_INPUT 2, STREAM_OUTPUT 2, AVB_INTERFACE 1, CLOCK_SOURCE 3, CLOCK_DOMAIN 1, CONTROL 1, LOCALE 1, STRINGS 1, STREAM_PORT_INPUT 1, STREAM_PORT_OUTPUT 1, AUDIO_CLUSTER 25, AUDIO_MAP 0.
- STREAM_PORT_INPUT 0 holds 8 clusters from 0, and STREAM_PORT_OUTPUT 0 holds 17 from 8, both with 0 maps (dynamic).
- The cluster names at the span ends match.
- CLOCK_SOURCE 1 (CRF Clock) is located on STREAM_INPUT 1, and CLOCK_SOURCE 2 (Stream Clock) on STREAM_INPUT 0.
- The model ID `0x001BC5C1935893E1` and ADP sources/sinks 2/2 match the moves table.
- Containment follows IEEE 1722.1-2021 7.2: STREAM_PORT under AUDIO_UNIT, AUDIO_CLUSTER under STREAM_PORT, the CONFIGURATION top-level counts of 7.2.2 (`avdecc/aem_descriptors.py:230-234`), and STRINGS reached through LOCALE.
- Milan v1.2 5.3.3.9 dynamic Stream Port Input: maps 0. The IDENTIFY CONTROL is at configuration level.

**Model ID.** `model_shape`/`derive_model_id` (`endstation_builder.py:3456-3553`) match the diagram and table:

- SHA-256 of canonical JSON, the low 40 bits of the first eight octets, the OUI as a prefix.
- `AEM_LAYOUT_REV` is unconditional.
- gPTP attributes are in the shape, the latency corrections are excluded by name, and names are excluded (IEEE 1722.1-2021 6.2.2.8).

**Worked example.** I reran it as printed (scratch paths; `receipts/worked_example.log`):

- The 2x2 summary line and the plan verdict match the page byte for byte, with rc 0 and an empty `git status`.
- The return to 1x1 with `--write-rtl --write-fragment` leaves `git status` empty.

**Other prose claims checked:**
- `build.sh` refuses a mismatched shape (`sw/litex/build.sh:439-446`).
- The sweep fragment is written only under `--write-fragment` or `--write-rtl` (`endstation_builder.py:5931-5935`).
- `srp.rtl_table` ownership: lines 6003-6007; only `endstation_arty_current.yaml` declares it.
- `--ctrl-mailbox` is off by default (`sw/litex/milan_soc.py:2621`).
- The headroom record (`docs/design/AREA_BUDGET.md:127-150`) names slices as the binding limit and says growth needs an owner decision.

### RTL: CLEAN

The PR changes no RTL. I checked every RTL parameter the new pages name against the source:

- `MCSERVO_P`, `LTAP_P`, `MAAP_P`, `I2SPB_P`, `RXFILT_P`, `LPF_P`, `DPROBES_P` and `TALKER_WIRE_CHANS_P` are each declared once in `hdl/milan/milan_datapath.sv` (for example lines 246 and 308) and mapped in `sw/litex/milan_soc.py:679-685`.
- `TALKER_WIRE_CHANS_C = 8` is in `hdl/common/gen/adp_shape_defaults.svh:110`.
- `N_NAME_MAX_C = 128` is in `hdl/milan/KL_nvm_backend.sv:248`; the builder reads it rather than restating it (`endstation_builder.py:2686-2743`).
- `NUM_QUEUES = 5` is in `hdl/common/csr/milan_csr.sv:98`, and `NUMBER_OF_QUEUES = 5` in `hdl/common/ethernet_packet_pkg.sv:93`.
- The consumers drawn in the data flow name their includes: `adp_shape_defaults.svh` in `milan_csr.sv` and `milan_datapath.sv`, and `lwsrp_csr_defaults.svh` in `milan_csr.sv`. The generator checks these.

### Robustness: UNCLEAN (F1)

- The contract parser mishandles an escaped pipe, a legitimate Markdown construct (F1).
- Otherwise the generators behave as their docstrings say:
  - probes run on temporary copies, and a probe owning a tracked header is refused (`endstation_definition.gen.py:123-124`);
  - host paths are scrubbed or refused (`gen_key_reference.py:143-148`, `endstation_definition.gen.py:130-139`);
  - a missing marker pair is refused.
- The unknown-key table reports both refusing and dropping mappings, which matches the loaders I read (`_load_board:3902`, `_load_names:3843`).
- Each run left the tree clean.

### Tests: UNCLEAN (F1)

- At the head, all four gates exited 0 (`receipts/gen_gates.rc`):
  - key reference `--check`;
  - key reference `--selftest`: stale page plus 6 planted defects;
  - definition `--check`;
  - definition `--selftest`: stale page plus 5 planted defects.
- My own mutants are in `scripts/mutants.sh` and `receipts/mutants.log`. All 11 are refused:
  - K1: a stale README cell gives rc 1.
  - K2: a moved builder default gives rc 2.
  - K3: a narrowed channel range gives rc 2.
  - K4: a narrowed group_name length gives rc 2.
  - K5: a moved descriptor-layer name default gives rc 1.
  - D1: a stale tree cell gives rc 1.
  - D2: a consumer that stops naming its file gives rc 2.
  - D3: a renamed CLOCK_DOMAIN default gives rc 1.
  - D4: a raised `N_NAME_MAX_C`, which breaks the widest-probe claim, gives rc 2.
  - D5 and D6: stale resources and moves cells give rc 1.
- The gate is blind to the clause cell behind an escaped pipe, and no selftest arm covers it (F1).

### Docs: UNCLEAN (F1, F2)

- At the head (`receipts/doc_gates.rc`), these exited 0:
  - `check_doc_style.py` and its `--selftest` (the guide joins `DOCUMENTS`, `scripts/check_doc_style.py:26`);
  - `docs_check.py`;
  - `check_em_dash.py --base 1e80128f`;
  - `check_doc_paths.py`;
  - `gen_toc.py --selftest`, `--verify-anchors` and `--check`;
  - `check_baremetal_only.py --check`, `check_archive.py`, `check_diagram_pngs.py`;
  - `ci_gate_workflows.py --check`, `ci_events.py --check` and `--selftest`;
  - `check_py_idiom.py`, `check_entity_shape.py --self-test`.
- The renderer-dependent gates were run with the pinned `tools/markdown/requirements.txt` in a scratch environment. Without it they refuse to judge, and those refusals are kept in the receipts.
- **Owner rules:**
  - The 20-word paragraph rule is enforced by the gate.
  - The three diagrams are listed in `docs/diagrams/README.md` with their generator.
  - Each diagram is generated and its labels are checked against the source (consumer tokens, builder tokens, overlay census).
  - `docs/integration/BUILDING.md` is linked, not edited.
- **CI wiring:**
  - The "Entity shape gate" step in `.github/ci-templates/docs.yml` and `.github/workflows/docs.yml:427-433` runs both `--check` and both `--selftest`.
  - The regenerated workflow matches its template (`ci_gate_workflows.py --check` rc 0).
  - `ci_events.py` carries the four commands.
  - Both digest pins in `ci/image/command-table.json` equal the files' sha256: `21489ba1...` and `bf035ad5...`.
  - The step runs after `protocol-processor` is initialised (`docs.yml:270`), which both generators need.
- The generated key reference carries F1 and F2.

## Completion ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | key reference against `endstation_builder.py` (30 keys); packed 1x1 `aem_desc.bin`; guide tree, model-ID, worked example, moves, resources | R751-1 | cb07597bc33106933c708a45f92c91f17a7a3e61 |
| RTL | CLEAN | `milan_datapath.sv` prune parameters, `adp_shape_defaults.svh`, `KL_nvm_backend.sv:248`, `milan_csr.sv:98`, `ethernet_packet_pkg.sv:93`, `milan_soc.py:679-685` | R751-1 | cb07597bc33106933c708a45f92c91f17a7a3e61 |
| Robustness | UNCLEAN (F1) | `gen_key_reference.py` `contract`/`load`/`_scrub`/`unknown_key_table`; `endstation_definition.gen.py` `write_probe`/`_clean`/`splice` | R751-1 | cb07597bc33106933c708a45f92c91f17a7a3e61 |
| Tests | UNCLEAN (F1) | both `--check`/`--selftest`; 11 reviewer mutants plus the F1 blind probe | R751-1 | cb07597bc33106933c708a45f92c91f17a7a3e61 |
| Docs | UNCLEAN (F1, F2) | guide, `README-parameters.md`, catalogs, docs gates, CI wiring and digests | R751-1 | cb07597bc33106933c708a45f92c91f17a7a3e61 |

## Real limits

- I did not run the builder bank (`test_builder.py`), any simulation suite, an FPGA build, flash or hardware. Physical calibration was NOT RUN, and field skips are not hardware proof.
- `scripts/ci_tool_inventory.py --check` refused in this environment with "CI_IMAGE_SHFMT must name the checksum-pinned Bash parser", an environment prerequisite. I verified the digest pins directly instead.
- I did not render the Mermaid diagrams. I checked their source and labels.
- At this head the hosted `docs-gates-0/1/2` shards were cancelled, not executed. `docs-check` failed only at "Require every gate exactly once", and other hosted contexts failed or were cancelled; I did not attribute their causes (`receipts/hosted_check_runs.tsv`). This is no hosted evidence for the new gates.
- No manager source bank runs at this head, and I claim none.
- Restoration after the probes (`receipts/restore_verification.log`):
  - HEAD is `cb07597b`, tree `5b5fff69`.
  - `git status --porcelain --ignore-submodules=none` is empty.
  - Each index entry's mode, blob and path equals the HEAD tree (identical digests).
  - The gitlinks `gptp-processor` `f97c1803`, `protocol-processor` `f65c8ff7` and `third_party/verilog-axis` `48ff7a7e` match their checkouts.
- Receipts have host paths replaced by `<packet>` and `<clone>`.

## Pending manager duties

- Hosted and act acceptance at the exact head.
- Current-dev merge-candidate validation (builder and native banks) at the merge turn.
- The external review.
- Re-review after F1 and F2 are fixed.

## Prior public findings

I read the PR's comments and reviews only after this verdict and ledger were on disk. The PR has no prior review findings: its comments are two review-start notices, and it has no review bodies or inline comments. So there is nothing to resolve or retain at this head.

The author's public evidence (`review-evidence/797g1-r1` at `55383a68`) reports that `ci_tool_inventory.py --check` is red at base and at head on `sw/builder/endstation_builder.py`. I confirmed that independently:

- The builder's sha256 `a489a095...` is identical at base `1e80128f` and at the head.
- The PR does not change that file.
- Its pin in `ci/image/command-table.json` is `84878e53...`.

So that refusal is pre-existing drift, not introduced by this PR. It stays with the manager's hosted acceptance.

R751-1 FINISHED
