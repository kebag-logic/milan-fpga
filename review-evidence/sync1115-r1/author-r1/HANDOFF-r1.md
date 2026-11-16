# HANDOFF r1: [A787] sync dev 6b66f66d into dev-soft-core (#665, ruling item 3)

Status: **STOP** posted on #665 (issuecomment-6903515775): one 8x8/1if service-budget row over its bound after the merge (section 8, F2). Head `d2da3159`, local, not pushed.

TAKEN: #665 issuecomment-6899809056.

## 0. Lane

- Branch `sync-dev-6b66f66d-into-dev-soft-core`, from dev-soft-core `659d7687` (verified equal to origin/dev-soft-core at start).
- dev `6b66f66d` (verified equal to origin/dev at start). Merge base `1f29f189`, the #830 sync (11-01).
- dev's merged PRs carried: #828, #831, #836, #815, #834, #841, #842 (#840), #849, #847 (#845), #846 (#843), #852 (#851), #825, #835, #862, #875, #893 (#883), #913.

## 1. The merge, `62625941`

One `--no-ff` merge of origin/dev `6b66f66d`. Ten files conflicted, 13 hunks (receipts/merge-tree-messages.txt,
receipts/merge-cc-text.diff, receipts/merge-cc-readme.diff).

| File | Hunks | Resolution | Why |
|---|---|---|---|
| `docs/design/MAILBOX_SPLIT.md` | 1 (status block) | dev's one-sentence-per-line form and "defines the transition and end state", with the split's S1 and S6 sentences in that form before the placement-contract line | dev reflowed the block and reworded the pointer (#828 residue); the split added the S1 (contract 2.3) and S6 (placement switch) lines |
| `docs/design/MARK_II_AREA_PLAN.md` | 1 (Summary) | dev's Mark II Summary, plus one bullet after "Measured basis": the integrated split route's 29,377 LUTs at 1x1 (M8a-2), +0.274 ns, its firmware's 57.5 tiles owed to S14 | dev replaced the Mark I Summary (#828); the split's two bullet edits recorded M8a-2's measurement, which stays in the history sections and keeps a pointer in the governing summary |
| `docs/reference/FR_NFR.md` | 1 (NFR-SCOUT-01..03) | SCOUT-01: the split's RV32IM/caches text plus dev's "(firmware only after the switch-over)"; SCOUT-02: dev's (the split never changed it); SCOUT-03: the split's approved T_svc = 20 ms and min(T_svc, ceiling) with dev's audio/gPTP split of the last sentence (gPTP deadlines fabric-only while the fabric plane owns gPTP; F6 states and tests each path's bound) | each side changed different sentences of the same rows |
| `sw/builder/endstation_builder.py` | 1 (`build()` return) | both keys: the split's `nvm_split=art.nvm_split` and dev's `warnings=identity_warnings(cfg)` | independent additions to one dict |
| `tb/verilator/milan_dp/Makefile` | 3 | `ORDINARY_CASES` ends `split bootsa`; both `CASE_OPTIONS_split` and `CASE_OPTIONS_bootsa`; `clean` is the union (dev's `gptp_lat_ucode.hex`, `obj_bootsa`, the split's twin and srptx outputs) | each side added a case |
| `tb/verilator/milan_dp/README.md` | 2 | union: Contents gets the split's three entries then dev's `obj_bootsa`; the split's three sections then dev's #839 section | each side added sections at the same place |
| `docs/diagrams/submodule_boundaries.{drawio,png}`, `PNG_MANIFEST.json` | generated | `submodule_boundaries.gen.py` (reads the merged index's gitlinks), which rewrote the SVG, drawio, PNG and the manifest entry; `--check` OK; `check_diagram_pngs.py` OK | generated from the pins |
| `docs/diagrams/flash_layout.png` | binary | rendered from the auto-merged `flash_layout.svg` with the docstring's `rsvg-convert -w 1800`; the auto-merged SVG/drawio equal the generator's output; the same renderer reproduces both parents' PNGs byte for byte | generated |

Pins (the merge took them; ancestry checked):

| Submodule | base | dev | split before | result | why |
|---|---|---|---|---|---|
| gptp-processor | 135afd04 | 1616fc8f | 135afd04 | **1616fc8f** | dev's (#846); fast-forward, 42 commits |
| protocol-processor | a9e84b66 | 801ef228 | a9e84b66 | **801ef228** | dev's (#847, #852, #893); fast-forward, 50 commits |
| third_party/tsn-c-stack | 70936b77 | 70936b77 | 715589c1 | **715589c1** | split-only and newer (#892); descends from dev's 70936b77 |
| external, lwSRP, verilog-axis | unchanged | unchanged | unchanged | unchanged | neither side moved them |

## 2. Commits after the merge

| Commit | Kind | What |
|---|---|---|
| `a563a83d` | semantic conflict (RTL) | dev's #839 renamed the processor's control-lane handshake to `pp_txs_*` and gates it into `pp_tx_*`; the split's `KL_ctrl_split` still drove `pp_tx_tvalid_w`. At the merge the split build refuses: `%Error-UNDRIVEN: milan_datapath.sv:923:8: Signal is not driven: 'pp_txs_tvalid_w'` (receipts/split-tx/dp-split-at-merge-62625941.log). The split's instance now binds `pp_txs_tvalid_w`/`pp_txs_tready_w` (`hdl/milan/milan_datapath.sv`, g_sp_ctrl), as dev's all-fabric wrapper does, so the gate holds the firmware's control lane as it holds the processor's. The split firmware writes MAC_ADDR_LO then _HI in `ctrl_plat_csr_policy` before it enables MAAP/AAF/CRF (`sw/firmware/ctrl/plat/ctrl_plat_csr.c:38-39`), so the product's order releases it. |
| `dfcd8eed` | semantic conflict (test) | with the gate, the split leg's `[TX]` frame waits for a station MAC the bench never wrote: `FAIL [TX] the committed frame leaves the MAC` (receipts/split-tx/dp-split-binding-only-a563a83d.log). `sim_split.cpp` gets an AXI4-Lite `csr_wr` (sampled at dp_clk rises like the bench's other handshakes) and writes the station MAC, equal to the frame's own source (kSrcMac), as the platform does; `[TX]` now also checks the frame is held before the write and with the low half alone. 84 checks, 0 failures. Two new `split_mutants.py` arms (below). README, tb_split_top comment and the plant count (26 -> 28) follow. |

| `b84d095a` | semantic conflict (doc) | dev's area plan (`MARK_II_AREA_PLAN.md`, console UART) says #810 "is not merged" and links this line's FR_NFR as proposing 10 ms; on this line #810 merged into dev-soft-core on 2026-11-13 and FR_NFR approves 20 ms. Both stated as this line has them, dev's 10 ms kept as dev's. |
| `d8c8c4b7` | semantic conflict (test) | the two-placement simulation's stimulus hard-coded the shipping config's old identity (`twin.hpp:56-57`, `0x020000FFFE000001`, `02:00:00:00:00:01`): at the merge neither half answered one AECP command, and the split's Talker rows named the old stream IDs (receipts/twin/twin-at-dfcd8eed.txt). The constants, the stream-ID-derived hex in `twin_compare.py` (stream IDs and the Talker Failed's failure Bridge ID, the device's own MAC) and the `srp-plus-k` plant's words follow #840. The split's Talker count moves from `JoinMt x89` to `x90`: lwSRP's LeaveAll draws are seeded from the interface MAC (`srp_mbx.c:347-348`), so the 75 s run gains one transmission; a comment at the row says so. |
| `1facd42e` | semantic conflict (test) | the same seed moves the split's first MSRP LeaveAll after 20 s from 27910 to 27510 ms; the `leave-all-omission` plant is refused there, and its words follow (it escaped only by its timestamp). |
| `3c94c76c` | semantic conflict (test) | processor 801ef228 (#893) fixes the fabric's #857, #858 and #860; the twin's four owed rows for them then report "the defect has gone, ... deletes the row" (receipts/twin/twin-identity-only.txt). The rows (`entity-available-index`, `fabric-mvrp-leave-all`, `fabric-domain-one-new`, `fabric-vid2-join-in`), their six fabric plants, and the helpers only they used are deleted; `OWED_GRADES` and the fabric-plant loop stay, empty. README: the rows, the plant table and count (20 -> 14), and the fabric half's traces at the pin (Domain and VID 2 New x2 then JoinMt; MVRP LeaveAll 10201..71400 ms). `make twin` 0 findings; `make twin-plants` rc 0, 14 plants each refused twice (receipts/twin/twin-plants-and-twin-final.txt). |
| `3a5ba178` | restatement (doc) | `SPLIT_CONTROL_MEMORY.md` section 5 states the eight split images at the head; each grows 24 to 40 B (receipts/images/rom-per-image.md), so the head's figures are restated, the pre-sync ones kept as history, and the round paragraph that said "holds" now reads "then held" with the head's beside it. |
| `f5750b3d` | regeneration | `docs/DOCUMENTATION_AUDIT.md` through `docs_inventory.py --write` (the docs gate's only failure at the merge: `STALE (378 lines differ)`); `--check` OK. |
| `d2da3159` | fix of `b84d095a` (doc) | `b84d095a`'s sentence named dev's copy as a bare `FR_NFR.md`, which `docs_check` refuses (`MARK_II_AREA_PLAN.md:371: bare reference ... make it a link`, at `f5750b3d`); now "Dev's requirements page, section 3.4.1". The audit stays fresh (`--check` OK; `--write` writes the same bytes). |

New checks, each with its planted mutant and failing words (receipts/split-tx/):

| Check | Mutant | Failing words |
|---|---|---|
| `[TX] the gate holds the committed frame before the station MAC is written (#839)` | `split_mutants.py` "the control lane past the station MAC transmit gate" (both `pp_tx_tvalid_w`/`pp_txs_tready_w` ungated) | `FAIL [TX] the gate holds the committed frame before the station MAC is written (#839)` (also `...and with its low half alone`, `...byte for byte`: the frame leaves with the reset all-zero source, #839's own defect) |
| `[TX] ...and with its low half alone` | "the station MAC transmit gate opened by one half" (`tx_sa_ok_w = lo \| hi`) | `FAIL [TX] ...and with its low half alone` |
| (existing) `[TX] ...byte for byte` | lane-only plant: tvalid ungated, tready still gated | `FAIL [TX] ...byte for byte` |

Note: an arm name containing `#` builds nothing (`rc -1`): the arm's copy directory is named after the arm, and `#` in a make variable value starts a comment. The new arms' names avoid it.

## 3. gPTP items (#843) and identity (#840) on the split image

The split placement keeps the fabric gPTP plane until #665 F6: `milan_datapath.sv:9160` builds `g_gptp_plane` on
`GPTP_PLANE_EN_P` alone (not on `CTRL_SPLIT_P`), `KL_gptp_shadow` at `:9175`; its program ROM is the builder's
`gptp_ucode.hex` for the config (`milan_soc.py:1044`, generated at `endstation_builder.py:6136` with
`gptp_ucode_args(cfg)`); `board.features.fabric_gptp: false` is retired (`endstation_builder.py:4616`), so every split
build carries it. The split firmware links the builder's AEM image for its config (`sw/firmware/ctrl/aecp/aecp_entity.py`,
`builder._entity_model_image`). Receipt: receipts/gptp/split-identity-and-clock-accuracy.txt.

| Item | Clause | Where the split image gets it | Evidence |
|---|---|---|---|
| clockAccuracy 0x22 for this board | IEEE 802.1AS-2011 8.6.2.3 | board config `gptp.clock_accuracy: 0x22` (both AX7101 configs) -> (a) the engine ROM, `--clock-accuracy 0x22`, announced by the fabric engine; (b) the AEM's AVB_INTERFACE `clock_accuracy` 0x22, which the split firmware serves | both configs: `gptp_ucode_args` `--mac 0x024b4c4b4c01 --p1 248 --clk-hz 50000000 --clock-accuracy 0x22`; AVB_INTERFACE clock_accuracy 0x22, priority1/2 0xf8, clock_class 0xf8, oslv 0x436a |
| Announce at the timeout instant ages the port | 802.1AS-2011 10.3.9.1 | the fabric engine, gptp-processor `1616fc8f` (#843's adoption, the pin this sync takes) | engine suites at the pin; parent `gptp_plane`, `gptp_shadow` and milan_dp gPTP legs in the sweep |
| Follow_Up whose first TLV is unknown | 802.1AS-2011 11.4.1 | the same engine (its Follow_Up TLV walk) | as above |
| Pdelay response later than the Milan bound counts as lost | Milan v1.2 4.2.6.2.6 | the same engine | as above |
| Prototype identity 02:4B:4C:4B:4C:01 | #840 | board config `mac_address` -> builder: entity_id `024b4cfffe4b4c01`, ADP/AEM/overlay, `adp_entity_gen.h`, `gen/nvm_shape_gen.h` (the split firmware's `MILAN_ENTITY_ID_*`), the policy's `MAC_ADDR_LO/HI` writes, and the engine ROM's `--mac` (clockIdentity) | receipts/gptp/...; receipts/images/ (every split image moves by these immediates) |
| 1000BASE-T-only advertisement on 1G PHYs | #840 | **does not reach the split image**: it is in the release firmware's PHY init (`milan_baremetal.c`); the split firmware has no MDIO path (#919's scope is the link poll only) | finding F1 (section 8) |

## 4. Ledger #847, #852, #893 (fabric-processor fixes; the split's counterparts)

| PR (issue) | Fabric fix | Split counterpart (file:line) | Its test (and planted defect) |
|---|---|---|---|
| #847 (#845) | the SRP Listener applies a Talker registered before the sink's settle and on a re-bind (Milan v1.2 5.3.8.5, 5.5.3.5.18 step 4); registrars to MT on LINK_DOWN/LINK_UP (802.1Q-2022 Table 10-4) | every bind marks the interface stale (`srp_mbx.c:530`) and the walk matches every registered Talker against each bound sink, whenever it registered (`registrations`, `srp_mbx.c:695`); a LINK event rebuilds the interface's participants, so its registrars start MT (`on_event` `:910` -> `reset_interface` `:862`) | `Srp.HeldRegistrationsAreWhatAWalkCopiesAfterEveryStep` (`srp_mbx.cpp:1430`, step "a second binding of a registered Talker" `:1443`, "link down", "link up"), `Srp.SharedBindingsRetainTheListenerAndVlanUntilTheLastUnbind` (`:725`), `Srp.LinkChangeBuildsTheNewParticipantsOnTheNextPass` (`srp_app.cpp:349`); mutant `binding-change-not-copied` (`srp_mutants.py:899`) |
| #852 (#851) | each attribute value encoded at most once per MRPDU, through rLA!, own LeaveAll, periodic and join in one window (802.1Q-2022 10.7, 10.8) | lwSRP builds one MRPDU per transmit opportunity: one Message per type, one single-value vector per selected attribute, each selected once (`third_party/lwSRP/src/core/mrp_mad.c:1351` `tx_message`, `:1410` `mrp_transmit`) | srptx `[WIRE]` "no attribute value twice in one MRPDU" (`srptx_grade.py:305`), plant `doubled-declaration` (`srptx_plants.py:41`); 0 `[WIRE]` findings at the head |
| #893 (#883: #857) | MVRP keeps LeaveAll with nothing declared (802.1Q-2018 10.7.9) | lwSRP's per-participant LeaveAll machine restarts on every expiry, declaring or not (`mrp_mad.c:779` `la_event`, `:803`) | twin LeaveAll interval grade in each half (`twin_grades.py:175`); the split's MVRP LeaveAlls 14860..73600 ms in the twin |
| #893 (#860) | New on two transmit opportunities; sJ sends JoinIn only with the Registrar IN (Table 10-3, 10.7.6.3) | lwSRP's Applicant table (`mrp_mad.c:149`) and `wire_event` (`:1278`) | twin Table 10-3 grade (`twin_mrp.py`), plants `table-10-3`, `received-join`, `mvrp-join-in`, `mvrp-received-join`, `leave-all-omission` (`twin_compare.py:79-90`) |
| #893 (#858) | ENTITY `available_index` is the last ENTITY_AVAILABLE's (1722.1-2021 Table 7-2, 6.2.2.15) | `ctrl_app_aecp.c:113` | `App.EntityReadSeesTheLastAdvertisedIndex` (`test_aecp.cpp:528`); mutants `app-available-index-next`, `-unguarded` (`aecp_mutants.py:503`, `:508`) |

No counterpart is missing. The twin had owed rows for #857, #858 and #860 (the fabric's defects, the split already
right); at processor 801ef228 the fabric half meets them, so the rows went (section 2).

## 5. Figures

### 5.1 Split images, ROM (receipts/images/)

Every split image (size fixture and platform, 1x1/1if, 1x1/2if, 8x8/1if, 8x8/2if; `qimg.sh` on fixed flash maps,
runtimes and CSR map) grows 24 to 40 B of rom at the merge: the #840 identity's immediates (`nvm_klj2.o` +28 B,
`ctrl_aecp_image.o` +8 B at the 1x1/1if fixture; `.rodata` and the AEM's 7,512 B unchanged). No image leaves its banks
or tile count; no ledger entry moves (rom-per-image.md). Section 5 of SPLIT_CONTROL_MEMORY.md restated (`3a5ba178`).

### 5.2 CPU service-budget harness (receipts/budget/)

Image identity by hash does not hold (the configs' identity and clockAccuracy are image inputs), so the legs were
measured. Builds at `dfcd8eed`; every one attests at the final head `d2da3159` (`--reuse-build --regrade` from the
same checkout moved there), each table byte-identical (receipts/budget/regrade-at-final-head.txt).

1x1/1if, against the base's legs (#902's at `c274b9f5`, whose compiled firmware equals the base `659d7687`'s):

| Leg | Head | Base |
|---|---|---|
| arm A q1 (24) | 0 refusals, 0 misses (0/254 instances, 0/12 paths), 0/17,791 passes over the share, rc 0 | 0, 0 (0/254, 0/12), 0/17,839, rc 0 |
| arm A q2 (24) | 0, 0 (0/218, 0/61), 0/41,093, rc 0 | 0, 0 (0/218, 0/61), 0/41,362, rc 0 |
| arm A q3 (24) | 0, 0 (0/253, 0/11), 0/64,107, rc 0 | 0, 0 (0/253, 0/11), 0/64,540, rc 0 |
| arm A q4 (24) | 0, 7 (7/225, 4/52): `backlog-owed`'s held-egress rows (ruled), 0/16,244, rc 0 | the same 7, 0/16,291, rc 0 |
| answering-every-port (16) | 0, 0 (0/280, 0/7), 0/21,765, rc 0 | rc 0 |
| answering-ports: aecp-fanout, aecp, aecp-largest-notice | 0, 0 (0/44, 0/43), 0/339, rc 0 | rc 0 |

Model gates at the final head (receipts/budget/model-*.txt): `flip_grade.py --check --point 1x1/1if` PASS (R4 13.10,
R5 74.07, R6 69.86, first 14.66, last 127.21 of 130, R4L 188.48, ACMP 28.95, ADP 27.30, MAAP 27.42, tx 33.38, txL
48.43 ms); `load_grade.py --check` PASS (1x1/1if 0.516 at the pin, 0.512 with tsn-c-stack #32, ceiling 0.70);
`tier_grid.py --point 1x1/1if` slice 950 us chosen; self-tests rows_tiers 1033/1033, flip 585/585, load 26/26,
record_classes 11/11; `run.py --self-test` 0 failures.

8x8/1if (the point holds one interface's 1x1/1if stated costs, so every leg there exits 1 on `STATED` lines at the
base as at the head, #914's scope; the rows are what is compared):

| Leg | Head | Base (the leg the base's lanes published, or run here) |
|---|---|---|
| arm A part 0 (22) | 0 refusals, 7 misses (7/213, 4/24): `backlog-owed`'s held-egress rows (ruled); saves durable 22,829.7 and 4,817.8 ms; 221 `STATED` lines | the same 7 misses within 0.1 ms; saves 22,829.6 and 4,817.7 ms (the #914 lane's part 0) |
| arm A part 1 (24) | 0 refusals, **1 miss**: `save-held.mrpdu.leaveall.if0` 161.123 ms (the LeaveAll run-out at 14,091.0 ms built 161 ms late, past THE TRANSMIT's 49 ms) | 0 misses |
| arm A part 2 (24) | 0 refusals, **1 miss**: `save-starved.mrpdu.leaveall.if0` 161.069 ms (the same run-out, 14,091.0 ms) | 0 misses |
| arm A part 3 (25) | 0 refusals, 0 misses | 0 misses |
| answering-ports `aecp-largest-notice` | 1 of 106 passes over the share (2.025 ms), the same `STATED` lines, rc 1 | 1 of 107 (2.025 ms), rc 1 (#902's at `c274b9f5`) |
| answering-every-port `notice-every-0` | `RuntimeError: the model holds 40 notices, not AECP_NOTICES_MOST at 8x8-1if` | the same |

The miss's cause (receipts/budget/81-leaveall-phase.txt): `save-held` at 8x8/1if run three ways.

| Run | LeaveAll run-outs | MRP timers' run-outs | Misses | THE TRANSMIT's longest build |
|---|---|---|---|---:|
| base `659d7687` | 10,461.9 and 14,621.9 ms | 39 released, 34 empty | 0 | 108,118 cycles |
| head code, the pre-#840 MAC in the 8x8 config (experiment, a scratch copy) | 10,461.8 and 14,621.8 ms | 39 released, 34 empty | 0 | 108,246 |
| head | 14,091.0 and 14,921.2 ms | 41 released, 30 empty, 1 late | 1 | 109,286 |

lwSRP's LeaveAll draws are seeded from the interface MAC (`srp_mbx.c:347-348`), so #840's MAC moves the run-outs; at
14,091 ms the LeaveAll's build waits 161 ms. THE TRANSMIT's build is over the stated 95,000-cycle tier-2 slice at
8x8/1if in all three (pre-existing; #914's scope); the new phase is what exposes it as a row.

### 5.3 Routes (receipts/route/)

| Image | Directive | Slow 85/0 C WNS / WHS | Fast 85/0 C WNS / WHS | LUT | BRAM tiles |
|---|---|---|---|---:|---:|
| split 1x1/1if | ExtraPostPlacementOpt (integrated) | +0.128 / +0.102 | +1.636 / +0.036 | 31,988 | 81 |
| split 1x1/1if | ExtraTimingOpt | +0.067 / +0.102 | +1.553 / +0.036 | 32,029 | 81 |
| split 1x1/1if | AltSpreadLogic_high | **+0.399** / +0.102 | +1.660 / **+0.036** | 32,063 | 81 |

| split 8x8/1if | ExtraPostPlacementOpt (integrated) | **-0.595** (307 failing) / +0.102 | +1.636 / +0.036 | 43,580 | 92.5 |
| split 8x8/1if | ExtraTimingOpt | +0.014 (0 failing; under the floor) / +0.102 | +1.636 / +0.036 | 43,578 | 92.5 |
| split 8x8/1if | AltSpreadLogic_high | **+0.140** / +0.102 | +1.636 / **+0.036** | 43,559 | 92.5 |

8x8/1if, recipe directive: the worst setup paths run from the EDIT window's request register into the audio map's
output-claim logic in the datapath clock (`KL_mbx_cdc/u_edit/rq_r_reg[112]` -> `milan_datapath/amap_edit_oclaim_word_r_reg[230]/CE`,
20 ns, 26 levels). #810's route of the same image at `084cf7a8` (whose RTL equals the base's) met only on its other
directives: ExtraPostPlacementOpt +0.001, ExtraTimingOpt +0.292, AltSpreadLogic_high +0.093, with 42,705 LUTs and 88.5
BRAM tiles; the merged image is 875 LUTs and 4 tiles larger. **Best of three: AltSpreadLogic_high, +0.140 / +0.036 ns, the floors met at every corner** (the 8x8 board flow's own directive); ExtraTimingOpt +0.014 and the recipe's directive -0.595 do not meet it. The margin moved from #810's +0.292 (ExtraTimingOpt) to +0.140, on the same EDIT-window path class.

The release AX7101 1x1 (all-fabric) image: its gateware export at the head equals dev `6b66f66d`'s file for file
(receipts/route/release-export-dev-vs-head.txt: every `gateware/` file equal after path normalisation, the top Verilog
equal outside its comments; only this line's `journal_klj3` flash constants differ, in `csr.csv` and
`flashboot_layout.json`), and its datapath elaborates identically in all six shapes (placement identity). Its route was
not run this round: the chain was stopped before it so the sweep could run first (no route beside a sweep).

## 6. Gate table (clean clones of `d2da3159` unless stated)

| Gate | Command | Result | Receipt |
|---|---|---|---|
| **all four workflows** | `verify_wf.py d2da3159 ... docs.yml rtl-fast.yml elaborate.yml rtl.yml` | **154 steps ran rc 0, 256 not run with a reason, 0 bad** | receipts/workflows/verify-wf-final.md |
| docs workflow, every job | `run_wf.py` per job, `verify_wf.py` | every run step rc 0; skips by name with reasons (`not_run.json`, built by step name from lane 917's, `mk_not_run.py`) | receipts/workflows/ |
| rtl-fast, every job but the SRP campaign | same | rc 0: lint, yosys elaboration, publication census (57 rules, 0 unproven), split CDC, BDD 511 scenarios, firmware suites, saved-state store suites, `fw_coverage --check` PASS (39 files), control campaign 716 of 716, AECP campaign 299 of 299, TSN boundary (with the LiteX venv as its job venv, as the hosted job installs `litex_pins.txt`), firmware-verilator | receipts/workflows/ |
| rtl-fast, firmware-srp-mutants | same | rc 0: both SRP campaigns and the pin controls, 345 arms caught | receipts/workflows/ |
| elaborate, legs 0 to 4 | same, LiteX venv | rc 0. Leg 4 (LiteX simulations, leg 2 of 3) first ended `TIMED OUT (result unknown, NOT a failure): test_soc_timing_cuts` (exit 92: its 900 s wall clock on the overloaded session pool), then refused a stale receipt of that attempt in the reused job directory; on a fresh job directory and a booked range it passed, `test_soc_timing_cuts` 572 s. Both earlier attempts' logs are kept | receipts/workflows/logs/ |
| rtl.yml | full-ci-gate, yosys-shards 0..3 of 4, yosys-portability, yosys-tool | rc 0 (verilator-shards: the native sweep's partition, not run, section 9) | receipts/workflows/ |
| split leg, 28 plants | `make split-mutants` | 28 of 28 caught by the check each names | receipts/split-tx/split-mutants-28-at-final.txt |
| two-placement simulation | `make twin`, `make twin-plants` | 0 findings; 14 of 14 plants refused twice | receipts/twin/ |
| harness model gates and self-tests | flip, load, tier grid, rows_tiers/flip/load/record_classes self-tests, `run.py --self-test` | PASS; 1033, 585, 26, 11 of as many; 0 failures | receipts/budget/ |
| harness legs attested at the final head | `run.py --reuse-build --regrade` from the harness checkout moved to `d2da3159` | every build accepted against the head's inputs; all 11 graded legs' `table.md` byte-identical, each rc as first run | receipts/budget/regrade-at-final-head.txt |
| record classes over every leg | `record_classes.py` over the 1x1 and 8x8-1if results | RESULT PASS (8x8/1if reported, not held) | receipts/budget/record-classes-final.txt |
| full 65-suite sweep, 4 shards | `native-shards.py` | **not run**: no route may run beside it; the routes held the night to 05:06, then no CPU range was free and another lane's route started (section 9) | |
| all-fabric datapath identity, dev against head | `placement_identity.py --dump` (dev `6b66f66d`, head `d2da3159`), `--compare` | 6 shapes, every digest equal: the release image's datapath is dev's | receipts/route/placement-identity-dev-6b66f66d-vs-head.txt |
| routes | `chain.sh` (section 5.3), one Vivado at a time through `vivado-slot.sh` | split 1x1/1if: met at all three directives, best +0.399 / +0.036; split 8x8/1if: met on its best of three, AltSpreadLogic_high +0.140 / +0.036 (the other two not); release 1x1: not run (its gateware export equals dev's) | receipts/route/ |

## 7. Checked, no conflict

- `KL_pp_shadow` (#862): ports unchanged but for comments; the census already classifies `rx_drops_o`.
- the datapath's top ports: unchanged by dev.
- dev's added text naming the split line: only the #810 sentences (fixed, `b84d095a`).
- the split firmware writes the station MAC before it enables MAAP/AAF/CRF, so #839's gate releases the product's frames.
- `make srptx` fails at the base `659d7687` as at the head, on one finding kind, `[TIME] ... a requested transmit opportunity ... past JoinTime + T_svc` (base: wire 1,103, hold 57, licence 47; head: 1,108, 58, 49, the counts moving with the MAC-seeded draws); PR #902 states the cause as a known limitation (`srptx.hpp` mirrors a 20 cs JoinTime, the adapter 19 cs; #916). Pre-existing, not this sync's; neither twin nor srptx is a CI gate or a sweep case.

## 8. Findings to report (not fixed)

- **F1.** #840's 1000BASE-T-only advertisement is in the release firmware (`milan_baremetal.c`) only. The split firmware has no MDIO path at all, so the split image's PHY advertises its defaults. #919 (the split's PHY poll) does not list it.
- **F2 (the STOP).** 8x8/1if: `save-held` and `save-starved` each have `mrpdu.leaveall.if0` at 161 ms, over THE TRANSMIT's 49 ms (section 5.2). Not the merge's code (the head with the old MAC equals the base); #840's MAC moves lwSRP's MAC-seeded LeaveAll draw to a phase where the pre-existing over-slice build at 8x8/1if (#914's scope) holds it. Decision asked on #665: carry it as owed to #914 (recommended), or hold the sync for #914.
- **F3 (pre-existing).** `make srptx` fails at the base as at the head on `[TIME] ... requested transmit opportunity ... past JoinTime + T_svc` (section 7; #916).

## 9. Not done this round, and what the next round needs

- **The 4-shard sweep on the final head: not run.** No route may run beside it, the routes held the night until 05:06, and after that `cpu_ranges.py` had no free range (128 of 128 busy) for as long as the round waited. Spec ready: receipts/tools/sweep-spec.json (`native-shards.py sync1115-a787 <spec> <out> 4 <ranges>`).
- **The release AX7101 1x1 route: not run.** It was stopped before its Vivado run, to let the sweep go first. Its gateware export equals dev `6b66f66d`'s (section 5.3), so its timing is dev's image's.
- **Done after the STOP was posted**, recorded here and not posted: the harness attestation at the final head, `record_classes`, the elaborate and SRP campaigns, both routes of the 8x8/1if split, the release export identity and the placement identity.
- PR-BODY.md is drafted for the PR the manager opens once the STOP is ruled.

## 9b. The base moved

- At the end of the round dev is still `6b66f66d`, but dev-soft-core moved from `659d7687` to `70f4056f`: PR #901, the
  train's first member, merged at 03:38. The ruling has this sync land after #901, #898, #881, #914 and #918, each synced
  onto as it merges, so the next round syncs this branch onto dev-soft-core's tip (this round's only allowed merge was
  the one of origin/dev, so it does not).
- #914 (the 8x8/1if tier rows, which owns F2's over-slice build) is in that train ahead of this sync, so the sync will
  carry it before it merges; F2 should be measured again then.

## 10. Environment notes

- Vivado reads its licence from the account's home; my units set `HOME` to scratch, so the route units set `XILINXD_LICENSE_FILE` to that licence file (the first chain run failed at once on "a valid license was not found").
- The RV32 SDK's `bin/meson` wrapper shadows the system `meson` (it cannot import `mesonbuild`), so the release export puts `/usr/bin` before the SDK on `PATH`.
- `cpu_ranges.py pick` returned nothing for most of the night (a release hold collecting CPUs), so most units ran on this session's own pool (96-127).
- After 05:06 every range 0-95 was booked by other lanes' harness legs, and another lane started a Vivado route at 05:3x, so the sweep could not start.
