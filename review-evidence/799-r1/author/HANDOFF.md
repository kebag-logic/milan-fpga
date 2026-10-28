# HANDOFF: issue #799 (and #790), executor [A692]

**Status: STOP** at head `f67a4ca1b32f2b247b772007e9731f26d2a82440` (14 commits on dev `97aab1d0`, not pushed). The required `rtl-fast` job `publication-census` fails, and fixing it needs a mailbox publication-block (register map) field or an owner ruling: the assignment's STOP condition. Every other gate passes. The resource gate refuses all three endpoints (owner decision). STOP text in `STOP.md`.

- Lane: `$LANES/799-adopt6`, branch `799-adopt-processor-f65c8ff7`, from dev `97aab1d0f28bd753a3e11df6278d5cac54f964dd` (still the live remote dev tip).
- Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
- Processor submodule: toplevel and origin verified before every git command in it (`https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git`); pin `ed211803` -> `f65c8ff7c673aaa8e2ea8da654f081ddb13588d8` (processor main: PR #204 for #202, #207 for #205, #208 for #206). gPTP stays `55680bff`.
- Assignment: the [A10] comment on #799. STOP on any top-level port or register-map change of milan-fpga beyond the `src_stream_id_o` routing the patch carries, or if any resource figure moves more than 2 % on route-1x1. The register-map condition fired, through the publication census (section "The STOP"); the 2 % condition did not (largest route move +1.47 %).
- Starting patch: the manager copy, sha256 `ff5068d295872d1f872b89890ff76f9bb1d3fd0738ad650282dbe45d9e171275`, 70,091 bytes, `git apply --check --index` clean on dev `97aab1d0`; applied, then reviewed and finished as milan-fpga code (below).
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/799#issuecomment-6449718026 (text in `TAKEN.md`).
- STOP: https://github.com/kebag-logic/milan-fpga/issues/799#issuecomment-6455859642 (text in `STOP.md`), posted at head `f67a4ca1`.
- Nothing pushed. No PR opened. No bench, hardware or flashing.

## Commits (one-line subjects, no body, no trailers)

| Commit | Change |
|---|---|
| `a7235498` | `protocol-processor` gitlink `ed211803` -> `f65c8ff7` |
| `ed07eea3` | Pin-derived records, each through its generator: ROM ledger (`bash syn/yosys/ooc.sh --record-rom-digests`), boundary diagram (`python3 docs/diagrams/submodule_boundaries.gen.py`), pin table row (`scripts/check_submodule_docs.py`) |
| `18444ac6` | The #202 source-stream-ID wiring: the patch, reviewed and finished (the AAF stamp wire declared ahead of its reader, #193; the packetizer's TCTX record note), with its two MAAP-conflict recovery legs |
| `fbc0723a` | #790 in milan_dp: `[GSI]` G11, three processor-copy arms in `gsi_mutants.py`, the datapath ledger restated |
| `897459bc` | #790 in pp_shadow: the `[GSI]` group |
| `9e1c8741` | The torture plan's MAAP conflict entry, which expected the old two-LeaveAll wait |
| `05b26476` | Testing guide, compliance matrix, register map, MAAP fabric page |
| `aabfd834`, `c0b7ebe0` | milan_dp README: G11 and the measured #790 arms; which older rows fail more checks with G11 |
| `856797ed` | Pin page adoption section and CHANGELOG section |
| `6ab0adc5` | The two REGISTER_MAP rows the change touched, without the em dash (the em-dash gate judges a touched line whole) |
| `1f7420d1` | `sw/firmware/ctrl/README.md`: 171 tsn-c-stack pin controls (the four new sidmove targets; `ctrl_boundary` caught the stale 167) |
| `3ee2d969` | Pin page: the measured route and standalone growth |
| `f67a4ca1` | The adoption's CHANGELOG and pin page sentences written to the audience style limits (`scripts/check_doc_style.py`), the resource growth as a table |

`git diff 05b26476 f67a4ca1` is Markdown only (5 files), so the Vivado bank at `05b26476` measures the final RTL; `git diff 3ee2d969 f67a4ca1` is `CHANGELOG.md` and `docs/reference/SUBMODULES.md` only.

## The STOP

`rtl-fast`'s required `publication-census` job (`python3 sw/mailbox/publication_census.py --check --selftest`)
fails at `3ee2d969` with 5 findings (`receipts/rtl_fast-3ee2d969/publication-census.log`):

```
[FAIL] the wrapper declares class-D output src_stream_id_o, which CLASS_D_PORTS does not list: review it [every shape]
[FAIL] unmapped read: pp_cd_src_stream_id_w -> aaf_tx_sid_w reaches the wire; name its block field or its ruled exclusion [every shape]
[FAIL] unmapped read: pp_cd_src_stream_id_w -> gsi_osid_w reaches processor; name its block field or its ruled exclusion [every shape]
[FAIL] unmapped read: pp_cd_src_stream_id_w -> crft_tx_sid_w reaches the wire; ... [endstation_arty_4x4, endstation_arty_8ch, endstation_ax7101_1x1_tdm8, endstation_ax7101_8x8]
[FAIL] the reads differ between the shapes: pp_cd_src_stream_id_w -> crft_tx_sid_w reaching wire only in ...
```

The census (#665, ruling 6088423771, decision 2 (a)) requires a read that reaches the wire to be carried by a field
of the mailbox publication block (`sw/mailbox/mailbox.yaml`), which the split placement's firmware writes in place
of the processor; the block has no per-source Stream ID field. The two edits that need no decision
(`src_stream_id_o` in `CLASS_D_PORTS`; `(pp_cd_src_stream_id_w, gsi_osid_w)` as a `processor` row, like
`(pp_cd_acmp_bound_sid_w, gsi_sid_w)`) leave 3 findings, all on the two stamps (scratch-clone probe,
`receipts/census-probe-3ee2d969/`). They are not committed: the rest of the fix is the decision.

- (A) a per-source current-Stream-ID publication register in the mailbox contract, with its `KL_mbx` port, the two
  stamps mapped to it, and the CRF stamp's read made shape-independent: a register-map change (the STOP);
- (B) an owner ruling that the split placement stamps the configured ID, with a census exclusion mechanism.

Recommended: (A), so the plane that owns the Stream ID publishes the ID it declares. The processor consumer banks of
#204, #207 and #208 never ran this job, which is how the patch reached the adoption with it red.

## Changes (file:line, clause)

| File:line (at `3ee2d969`) | Change | Clause |
|---|---|---|
| `protocol-processor` gitlink | `ed211803` -> `f65c8ff7` | processor #202, #205, #206 |
| `syn/yosys/rom_digests.tsv` (2 rows) | `f65c8ff7` rows; `ltn_rom.hex` `23cc67ee...`, `ucode.hex` `1f78804e...`, equal to the `ed211803` rows | ROM ledger rule (`syn/yosys/ooc.sh`) |
| `hdl/milan/KL_pp_shadow.sv:716`, `:1451` | output `src_stream_id_o[N_STREAM_OUT_P*64-1:0]`, the processor's port passed out (the routing the assignment allows) | processor #202 |
| `hdl/ieee1722/aaf/KL_aaf_packetizer.sv:132`, `:168`, `:505` | `SID_PP_P` (default 0) and `stream_id_i` (default `'0`): with `SID_PP_P = 1` every talker stamps the processor's current ID, t0 included, and a TCTX uid is read only by the standalone derivation | IEEE 1722-2016 4.4.4.8; Milan v1.2 5.3.7.5 Table 5.3 |
| `hdl/milan/milan_datapath.sv:1463`, `:1530`, `:1553`, `:2554` | `aaf_tx_sid_w` declared ahead of `aaf_packetizer` (its first reader, #193; the patch read `pp_cd_src_stream_id_w` 1,000 lines before its declaration), `.SID_PP_P (1'b1)`, assigned from sources 0..N_STREAMS-1 | same |
| `hdl/milan/milan_datapath.sv:2549-2561`, `:7498` | `pp_cd_src_stream_id_w`; the CRF Media Clock Output stamps its current ID where the shape has a CRF source, the CSR value otherwise | same |
| `hdl/milan/milan_datapath.sv:6187` | GET_STREAM_INFO selector 2 of an output reads the current ID | IEEE 1722.1-2021 7.4.16.2 ("the current id of the stream") |
| `hdl/milan/milan_datapath.sv:5998-6013` | the ledger restated: an input's three fields and flags are valid only while settled, and the processor applies that rule (processor #206) because this face cannot see probing_status; this face's `gsi_setl_w` is wider; an output's stream_id is the current one | Milan v1.2 5.4.2.10.1, Table 5.9; 5.3.8.5, Table 5.5 |
| `tb/verilator/milan_dp/sim_sid_move.cpp`, `sidmove_probes.vlt`, `Makefile:333-359`, `:684` | two recovery legs (1x1 shipping shape, 8x8 with a named TCTX uid): a peer ANNOUNCEs the claimed block; the wire, PROBE_TX, GET_STREAM_INFO selector 2 and the Talker Advertise name `src_stream_id_o` before and after the move | IEEE 1722-2016 Annex B (B.3.6.4 compare_MAC); 802.1Q-2018 35.2.2.8 |
| `tb/verilator/milan_dp/sim_nxn.cpp:7604` | the nxn leg's talker 1 is told by uid 1 (the processor's), no longer the TCTX uid 5 | IEEE 1722-2016 4.4.4.8 |
| `tb/verilator/capture_coherence/mutants.py` | the AAF_IN anchor matches the binding alone (another parameter follows it) | -- |
| `tests/features/milan_streaming_licence.feature`, `tests/steps/milan_streaming_licence_steps.py` | the integrated framer stamps the processor's ID over any TCTX uid | same |
| `tb/verilator/milan_dp/sim_nxn.cpp:2515-2636` | `[GSI]` G11: four named cases (below) | Milan v1.2 5.4.2.10.1 Table 5.9, 5.5.3.5.18, 5.5.3.5.36 |
| `tb/verilator/milan_dp/gsi_mutants.py:90-101`, `:197-205` | three processor-copy arms | same |
| `tb/verilator/pp_shadow/sim_main.cpp:3706-3895`, `:176` | the `[GSI]` group: four named cases | same |
| `tb/tools/torture_campaign.py:2645-2672`, `tests/features/torture_campaign_plan.feature:241-250`, `tests/steps/torture_plan_steps.py` | the MAAP conflict entry grades the move to another Stream ID declared at once, and limits the two-LeaveAll wait to the same StreamID; a new assertion `stream.id-follows-the-move` | Milan v1.2 5.3.7.5 Table 5.3; 802.1Q-2018 35.2.2.8; 1722-2016 4.4.4.8; 1722.1-2021 7.4.16.2 |
| `docs/reference/REGISTER_MAP.md:1596`, `:1599` | documents existing behaviour: the STRMW talker SID words read the ID a source starts with; the TCTX w2 unique ID is no longer stamped (no field, address or reset change) | -- |
| `docs/reference/MILAN_COMPLIANCE_MATRIX.md:122`, `docs/testing/TESTING.md:275`, `:405-418`, `docs/design/MAAP_FABRIC.md:307-318` | evidence and inventory: the #790 rule and its gates; seventeen ordinary milan_dp commands; the conflict moves the Stream ID | -- |
| `tb/verilator/milan_dp/README.md:89-90`, `:636-648`, `:675`, `:726-748`; `tb/verilator/pp_shadow/README.md:152` | the legs, G11, the #790 arms with measured counts, the pp_shadow GSI row | -- |
| `sw/firmware/ctrl/README.md:255` | 171 pin controls (was 167) | -- |
| `docs/reference/SUBMODULES.md:25`, `:276-317`; `CHANGELOG.md:11`, `:50-73` | pin row, adoption section, resource sentences; CHANGELOG section | the three processor clauses |

**#205** needed no parent change: no parent test, model or document expected zeroed listener fields for an unknown
talker_unique_id. The firmware ACMP path (#665) is tsn-c-stack's, whose `echo()` (`src/acmp.c:269-281`) already
copies the command's listener fields.

**The assignment's STOP conditions.** No milan-fpga top-level port changes (milan_datapath's ports are untouched;
`KL_pp_shadow` gains only `src_stream_id_o`), no register map field, address or reset changes (two rows gain notes
on existing behaviour). Route-1x1 figures move at most +1.47 % (LUT).

## New checks, planted mutants, failing words

**milan_dp `[GSI]` G11** (`obj_notify`, the shipping AX 1x1 shape, compressed processor time), on sink 0 after G10's
reset. Each case grades probing_status, acmp_status, BOUND, the three Table 5.9 flags and stream_id,
stream_dest_mac and stream_vlan_id:

| Case (check name prefix) | Expected | Premise |
|---|---|---|
| `[GSI] G11 sink 0 bound and probing, before the first answer` | ACTIVE; flags clear; fields 0 | the bind's PROBE_TX was sent |
| `[GSI] G11 sink 0 settled` | COMPLETED; `0x52` set; the talker's stream_id, DA, VLAN 2 | the binding view (`strtbl_sid_w`) names the stream |
| `[GSI] G11 sink 0 back in PROBING_PASSIVE after TMR_NO_TK, the stale ID` | PASSIVE; BOUND; flags clear; fields 0 | the binding view still names the settled stream; no new PROBE_TX |
| `[GSI] G11 sink 0 unbound after it settled` | DISABLED; not BOUND; flags clear; fields 0 | the binding view is cleared |

Clean: 499 checks, 0 failures (461 before G11). `make gsi-mutants` at `fbc0723a`: rc 0, the clean control passes and
all 14 arms are caught by their named checks (`receipts/gsi-mutants/`). The three new arms, planted in a copy of the
processor's hdl tree:

| Arm | Planted | Failing words (the named check) | Failures |
|---|---|---|---|
| the processor passes selectors 0, 2 and 4 through while unsettled (#790) | `if (!gsi_settled_w) begin` -> `if (1'b0) begin` | `[GSI] G11 sink 0 back in PROBING_PASSIVE after TMR_NO_TK, the stale ID: stream_id is zero` | 3 of 499 |
| ... selector 0's three flags through | `4'd0: ... & ~64'h0000_0000_5200_0000;` -> `4'd0: aecp_gsi_data_w = gsi_data_i;` | `...the stale ID: STREAM_ID_VALID, STREAM_DEST_MAC_VALID and STREAM_VLAN_ID_VALID clear` | 1 of 499 |
| ... selector 4's stream_dest_mac through | `4'd4: aecp_gsi_data_w[63:16] = 48'd0;` -> `4'd4: begin end` | `...the stale ID: stream_dest_mac is zero` | 1 of 499 |

The full pass-through fails only the stale case: before the first answer and after unbind the binding view holds no
stream, so the datapath's own rule already reads unsettled; selector 6's VLAN stays the processor's in every arm.

**pp_shadow `[GSI]`** (base leg; also in the vid73 and crf legs), after [U]: UNBIND_RX of U's binding, then the same
four cases on sink 0 with a stream no Talker attribute names, the premise read from `ACMPL_STATE` (`0x6A4` [3] bound,
[27:16] the binding view's VLAN). Clean: 651 checks, 0 failures (41 `[GSI]`). Planted probe, not committed
(`receipts/pp_shadow-probe/`): in a scratch clone at `05b26476` the processor copy got the full pass-through; the base
leg then failed 3 of 651:

```
[FAIL] [GSI] sink 0 back in PROBING_PASSIVE after TMR_NO_TK, the stale ID: STREAM_ID_VALID, STREAM_DEST_MAC_VALID and STREAM_VLAN_ID_VALID clear got=0x00000052 exp=0x00000000
[FAIL] [GSI] sink 0 back in PROBING_PASSIVE after TMR_NO_TK, the stale ID: stream_id is zero got 0x0200000000020790
[FAIL] [GSI] sink 0 back in PROBING_PASSIVE after TMR_NO_TK, the stale ID: stream_dest_mac is zero got 0x91E0F0002A90
```

That is #790's bench capture reproduced: a passive bound sink reporting the stream it settled on, flags set.

**The recovery legs** (`obj_sidmove`, `obj_sidmove8`, from the patch, now in milan_dp's default run): graded in the
sweep (below).

**The torture plan**: `tests/features/torture_campaign_plan.feature` now requires `stream.id-follows-the-move` and a
35.2.2.8 citation with "another Stream ID"; the old plan text fails the new steps by construction (it named neither).

## Resources (before / after, route timing)

Vivado 2026.1, the recipe's flows (`scripts/vivado_bank.sh`, the #780 bank with paths changed), one run at a time
under the exclusive lock, at `05b26476`. Against the eleventh record (`syn/ooc/pp_resource_baseline.json`, which
this lane does not change):

| Endpoint | Figure | Record | Head | Delta | % | Tolerance | Gate verdict |
|---|---|---:|---:|---:|---:|---:|---|
| `route-1x1` | LUT | 51,259 | 52,012 | +753 | +1.47 % | 500 | REGRESSION |
| | FF | 53,208 | 53,707 | +499 | +0.94 % | 600 | ok |
| | SLICE | 15,835 | 15,780 | -55 | -0.35 % | 80 | ok, below |
| | RAMB36 / RAMB18 / DSP | 74 / 27 / 13 | 74 / 27 / 13 | 0 | 0 | 0 | ok |
| | WNS / WHS ns | 0.236 / 0.028 | 0.440 / 0.036 | +0.204 / +0.008 | | 0.25 fall | ok |
| `ooc-1x1` | LUT / FF | 23,828 / 20,000 | 24,346 / 20,404 | +518 / +404 | +2.2 / +2.0 % | 250 / 250 | REGRESSION both |
| | RAMB36 / RAMB18 / DSP | 16 / 3 / 8 | 16 / 3 / 8 | 0 | 0 | 0 | ok |
| `ooc-8x8` | LUT / FF | 32,467 / 28,220 | 34,156 / 29,782 | +1,689 / +1,562 | +5.2 / +5.5 % | 316 / 339 | REGRESSION both |
| | RAMB36 / RAMB18 / DSP | 21 / 5 / 8 | 21 / 5 / 8 | 0 | 0 | 0 | ok |

Each endpoint's `pp_resource_gate.py check` printed `RESULT: MATERIAL REGRESSION` (exit 1). The assignment's STOP is
"more than 2 % on route-1x1": the largest route move is +1.47 %, so it did not fire. The standalone endpoints are not
the STOP's criterion. The record is not re-baselined: accepting growth over a tolerance is a reviewed owner decision
(`docs/design/AREA_BUDGET.md:455-466`; the record itself says "the next growth needs its own owner decision").

Route complete: 102,632 routable nets fully routed, 0 routing errors. Signoff: Slow 0C/85C WNS +0.440 ns, WHS
+0.074 ns; Fast 0C/85C WNS +1.660 ns, WHS +0.036 ns; TNS and THS 0.

Where it is (the gate's sub-block movements): route `u_pp` +712 LUT, +452 FF (`u_srp` +352, its talker +201: the
#202 owed-Leave copy; `u_talker` +190: the #202 move and quarantine; `u_aecp` +164; `u_notify` +71; `u_dispatch`
-83); the wrapper +717, so the parent's wiring and everything else outside the processor is about +41 LUT. ooc-1x1
`u_pp` +519 / +404; ooc-8x8 `u_pp` +1,684 / +1,564 (`u_srp/u_talker` +949 / +1,146, `u_talker` +686 / +414 at
nine sources), in line with processor PR #204's own report.

## Gate table

All in clean clones of the lane (submodules from the lane's checkouts; `origin/dev` the live remote dev tip
`97aab1d0`), each rc the command's own. Heads: `3ee2d969` for everything but the docs gates, which ran at the final
head `f67a4ca1`; `git diff 3ee2d969 f67a4ca1` is `CHANGELOG.md` and `docs/reference/SUBMODULES.md` only.

| Gate | Command | Result | Receipt |
|---|---|---|---|
| Full sweep, 4 shard units | `bash scripts/run_all_suites.sh <logs> --wait --shard k/4` (native-shards, MemoryMax 10G) | 64 / 64 suites (15 + 17 + 16 + 16), **2,191,637 checks, 0 in-suite failures**, 0 timed out; `scripts/suite_tally.py <union> --quiet --expect-suite-root tb/verilator` rc 0. Shard 2's first attempt was OOM-killed at its 10 GB cap in `capture_coherence` (its mutation bank sizes jobs from the 16-CPU affinity); re-run whole on 8 CPUs with `VERILATOR_JOBS=2`: 16 / 16, 380,086 checks, 0 failures | `receipts/sweep-3ee2d969/` |
| milan_dp | the sweep's milan_dp | 18 legs RESULT: PASS, 13,723 checks, 0 failures (notify 499 incl. G11; sidmove 50, 1,735 ms; sidmove8 52, 1,816 ms; gptp and gptp-lat prefix legs) | `receipts/milan_dp/summary.txt` |
| pp_shadow | the sweep's pp_shadow | base 651, vid73 651, crf 691, pending 317 checks, 0 failures; 123 `[GSI]` passes | `receipts/pp_shadow/` |
| milan_dp_gptp (physical) | `bash scripts/run_all_suites.sh <logs> --wait --physical-gptp` | rc 0: `milan_dp_gptp` PASS, 209 checks, 0 failures, 0 timed out (the physical leg 155 checks in 4,293 s; `verify_abort.py` 14; `verify_recentres.py` 14); tally rc 0; 5,412 s with preflight | `receipts/gptp-physical-3ee2d969/` |
| gsi-mutants | `make -C tb/verilator/milan_dp gsi-mutants` (at `fbc0723a`; nothing it reads changed after) | rc 0: clean 499 / 499, 14 / 14 arms caught by name | `receipts/gsi-mutants/` |
| Firmware gate set | the eight commands of the CI firmware block | at `05b26476`: 7 rc 0, `ctrl_boundary` rc 1 (`sw/firmware/ctrl/README.md gives the pin controls as 167, where the self-test has 171`; fixed in `1f7420d1`). At `3ee2d969`: all 8 rc 0 (`test_ctrl_firmware` 2,556 s, `test_ctrl_nvm` 1,318 s, `fw_coverage --check` 325 s, `ctrl_boundary` PASS 1,376 s); clone clean after | `receipts/firmware-*/` |
| rtl-fast replica | the workflow's `run:` bodies (`scripts/rtl_fast_steps.py`) | **11 / 12 `needs:` jobs success; `publication-census` failure (the STOP)**. bdd-conformance: 14 features, 406 scenarios, 1,979 steps passed; verilator-lint PASS at 89 <= 89; yosys-elaboration success; six firmware jobs success | `receipts/rtl_fast-3ee2d969/` |
| behave | in rtl-fast | as above | same |
| Yosys | `syn/yosys/run.sh --results <dir>` (Yosys 0.66, sv2v v0.0.12) | rc 0: 60 / 60 tops, tied-input gate PASS (2 justified ties), tap-purity PASS | `receipts/yosys-3ee2d969/` |
| Static and pin records | 22 commands (`scripts/static_bank.sh`): resource baseline check, ROM digests re-recorded with no diff, both diagram checks, submodule and gPTP docs, port contracts, naming and test-evidence measures, integrator params, lint and its self-test, xvlog (Vivado front end, 0 findings), both idiom gates and self-tests, RTL source lists and self-test, `pp_srcs --check --selftest`, `sw/builder/test_builder.py` | all 22 rc 0; clone clean after | `receipts/static-3ee2d969/` |
| Docs gates (GNU Make 4.3) | the docs workflow's step bodies (`scripts/docs_steps.py`), then builder leg 1 with the LiteX interpreter, the markdown gates on CPython 3.12.3, the no-git step's two gates | at `f67a4ca1`: all 42 steps rc 0 (2 skipped by rule), LiteX leg rc 0, markdown 3.12 rc 0, no-git docs_check and feature_status rc 0 | `receipts/docs-f67a4ca1/` |
| Publication census probe | the census at `3ee2d969` with the two no-decision edits, scratch clone | rc 1, 3 findings, all on the two stamps | `receipts/census-probe-3ee2d969/` |
| route-1x1, ooc-1x1, ooc-8x8 | the recipe's Vivado flows, then `pp_resource_gate.py check` | MATERIAL REGRESSION at all three (above) | `receipts/vivado/` |

The first docs run, at `3ee2d969`, had three failures, all resolved before the run above:
- the concise-documentation gate on my CHANGELOG and pin page sentences (rewritten in `f67a4ca1`);
- the em-dash gate's base fetch (the replica clone's origin, the lane, has no local `dev`; the clone's own `dev` is the
  live tip now);
- builder leg 0's SDK selector (the replica's HOME had no provisioned SDK; installed from the pinned archive with
  `scripts/ci_rv32_sdk.py --archive`).

The `tsn_fuzz` suite rewrites the date stamp of `hdl/ieee1722/avtp/doc/TEST_RESULTS.md` and `hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md` in the clone that runs it (its design: "written into the folder of the RTL it validates"); no other shard clone was left with a tracked or untracked change, the sidmove legs included.

The physical gPTP run failed twice at the driver's preflight before it ran: its hard-HUP cancellation control timed
out because the runs were started under `nohup` (SIGHUP ignored and inherited); started without it, the preflight
passed.

## Open risks / questions

- **The resource gate refuses all three endpoints** (above). Owner decision needed: accept and re-baseline (as #771
  and #770 did under owner exceptions) or not. This lane does not re-record.
- **8x8 and 4x4 shapes**: the datapath's maap-face source index (`milan_datapath.sv` `PP_SRC_IDX_W_C`,
  `$clog2(N_STREAMS)`) is one bit narrower than the processor's (`$clog2(N_STREAM_OUT_P)`, nine sources on 8x8), so
  the CRF output's ALLOC_DA and conflict arrive as source 0's. Processor PR #204 noted it for the pin adoption; it is
  outside #799's Required list and is not fixed here. The shipping 1x1 shape is unaffected (both 1 bit). A new issue
  is recommended.
- The STRMW talker SID words (`0x814`/`0x818`) read the configured ID, not the moved one. Making them follow is a
  register-map behaviour change (a STOP condition), so it is documented, not changed.
- Acceptance includes the in-house qualification re-runs on the image, with the gPTP adoption: not possible in this
  lane (no bench), so PR-BODY uses "Relates to".
