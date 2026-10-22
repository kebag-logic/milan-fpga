# [A662] HANDOFF -- issue #771, fourth parent pin adoption

Status: **REVIEW READY** at head `a97aea01449492b1f640924f5a34726f602cabed` (round 1b). Every step of the owner decision is done, every gate in section 7 exits 0 at that head, the worktree is clean and every submodule is at its gitlink. Nothing pushed.

- Branch: `771-pin4-93fb0b2d-55680bff`, from dev `d77a8afdbc960d70d1ceeee9af1163624f102b16`; nothing pushed.
- Assignment: [#771 comment 6325107889](https://github.com/kebag-logic/milan-fpga/issues/771#issuecomment-6325107889), steps 1 to 7 in order.
- TAKEN: [#771 comment 6325150563](https://github.com/kebag-logic/milan-fpga/issues/771#issuecomment-6325150563).
- Round 1 STOP: [#771 comment 6331294661](https://github.com/kebag-logic/milan-fpga/issues/771#issuecomment-6331294661) at `d664cf54`.
- Owner decision answering it: [#771 comment 6333175429](https://github.com/kebag-logic/milan-fpga/issues/771#issuecomment-6333175429)
  (the adoption's area accepted for now, Mark II #640 addresses it; finish from the STOP point).
- Round 1b: same checkout and branch, three new commits on `d664cf54` (no rebase, no amend).
- REVIEW READY: [#771 comment 6340721641](https://github.com/kebag-logic/milan-fpga/issues/771#issuecomment-6340721641).

## 0. Round 1b in one table

| Step (owner decision order) | Result |
|---|---|
| 1. Baseline record write through the recipe | `route-1x1`, `ooc-1x1` (`76b01906`) and `ooc-8x8` (`0ad70eab`) written with `record --write`; `check-baseline` rc 0; each `measured` note cites the decision and the per-donor 1x1 ledger |
| 2. 8x8 standalone | rc 0, 24.8 min; 32,467 LUT / 28,220 FF; against #708's record LUT +2,256 (tol. 316) and FF +769 (tol. 339), rc 1. Dev `d77a8afd` measured the same way: 30,282 / 27,451, rc 0; this adoption's own 8x8 share is **+2,185 LUT / +769 FF** |
| Documentation of the record | `a97aea01`: findings section, headroom table, area budget, Mark II plan, pin page, changelog |
| 3. Three-directive image build | all three rc 0, every corner WNS >= +0.03 ns and WHS >= 0, fully routed, IOB packing 21 PASS / 0 FAIL, offline image preflight OK; best: ExtraPostPlacementOpt, Slow +0.291 / +0.102, Fast +1.660 / +0.036 ns |
| 4. Yosys | `syn/yosys/run.sh` rc 0 (14.4 min): 58 / 58 tops PASS; tied-input gate 29 tied, 0 unjustified; tap-purity PASS |
| 5. Full parent sweep | default inventory 63 / 63 suites PASS, driver rc 0, tally rc 0: 2,189,520 checks, 0 in-suite failures, 0 timed out (3 h 37 min); physical leg milan_dp_gptp 1 / 1, rc 0, tally rc 0, 209 checks (81 min); the milan_dp gptp and gptp-lat legs run inside `milan_dp`, and `milan_dp_gm_steps` is in the default inventory |
| Hosted docs-check replica at the final head | 44 workflow steps: 42 run, all rc 0 under GNU Make 4.3; 2 skipped by rule; builder leg 1 again with the LiteX interpreter rc 0 |

Two things a reviewer should see first:

- **The 8x8 standalone growth is larger than the 1x1 figures the decision quotes.** The decision names route-1x1
  +770 and ooc-1x1 +462 (this adoption against dev); the 8x8 standalone adds +2,185 LUT / +769 FF against
  dev, over both 8x8 tolerances. It is recorded under the same exception: the decision accepts "the adoption's
  area", and its remaining STOP conditions (the patches together, timing, an interface change) do not
  include the resource gate. The record note, the findings section and the REVIEW READY comment state the
  figure so the owner can object.
- **The image build ran at reduced Vivado threads.** The launcher's own line with `--vivado-max-threads 32`
  started seven synthesis processes and hit the service's 12 GB cap within five minutes, so it was stopped
  and the three directives ran with that one argument changed (2, then 1). Section 5 has the detail.

## 1. Pin changes

| Gitlink | From | To | Commit |
|---|---|---|---|
| `protocol-processor` | `2cbed0a987c1e68402658d69459ab7e5aa571adc` | `93fb0b2d736b36588ea7321e25fba2f8819ea41f` (processor `main`, merge of PR #198) | `8f5e961f7deef77b6ee4b9109f10413f113de81f` |
| `gptp-processor` | `e4869fd0c42889b2ac806587cc5c78afb1c33461` | `55680bff3b287b9a7b0c759f51471fa617c17335` (FPGA-gPTP `main`, merge of PR #86) | `eec12fa62d6cabf477a2978330af688bb477e00f` |

Each old pin is an ancestor of its new pin. The first-parent ranges carry exactly the PRs #771 lists:
processor #173, #175, #174, #180, #182, #183, #187, #191, #194, #196, #195, #197, #199, #198 (merge order);
FPGA-gPTP #78, #83, #86. FPGA-gPTP #78's merge `b9ade3a6` has the same tree as the old pin `e4869fd0`
(the old pin was the #78 branch head), so #78 adds no change to this adoption.

Donor-to-parent interface check (raw `git diff` of each donor top between pins):

- `protocol_processor_top.sv`: one port changes, `cfg_tspec_max_frame_i` from `[15:0]` to
  `[N_STREAM_OUT_P*16-1:0]` (#190, PR #194). No parameter changes. `parent-scratch-tspec-every-slot.patch`
  carries the parent side. Other top edits are internal (`$error` to `$fatal` guards, #151; the
  listener's REGISTERING_FAILED level, #189; the LOCK_ENTITY flags wire, #186; the started/stopped
  notification term, #192).
- `KL_gptp_engine.sv`: no port or parameter change. Two output comments change meaning
  (`pub_path_count_o`/`pub_path_o` now carry thisClock appended, #85; thisClock from reset, #82).
  The engine now reads thisClock from ROM words 1022 and 1023 of `UCODE_HEX_P`.
- The processor source set is unchanged between pins (no `.sv` added, deleted or renamed; two JSON
  command-model files added under `hdl/aecp/ucode/`).

## 2. Parent adaptations (eight patches)

Each patch was checked alone at `d77a8afd` with `git apply --check` (all rc 0), then applied in this
order with `git apply --index`, one commit each, every one clean with no fuzz.

Note on history: the first application pass was committed with placeholder subjects by mistake.
Those eight local, unpushed commits were discarded with `git reset --hard eec12fa6` (the gitlink
commit) and the patches re-applied, byte-identically, under the subjects below. No other commit was
touched; nothing had been pushed.

| # | Patch (sha256) | Commit | Donor change it answers |
|---|---|---|---|
| 1 | `parent-evidence-classification.patch` (`76625170...`) | `8144d28857e443c0cc3176b8b35095e3b9917a3d` | Processor #151 (PR #175) adds `tb/elab_guards/guards.py` and `mutants.py`; #73 (PR #174) adds `tb/aecp_cmds/mutants.py`. The parent's test-evidence ratchet refuses an unclassified DUT-source reader. |
| 2 | `parent-adoption-milan_dp-67.patch` (`e142e2e7...`) | `2dc612fbd83e616d0bdfbd08547fdcd94ae1ba98` | Processor #176 (PR #183): SET_STREAM_INFO accepts the IEEE 1722.1-2013 48-byte body. |
| 3 | `parent-scratch-tspec-every-slot.patch` (`37d1b76e...`) | `c6afca8ce777fd9614c26db1bd0b63dd8b772f53` | Processor #190 (PR #194): `cfg_tspec_max_frame_i` per source. |
| 4 | `parent-adoption-milan_dp-gsi-g9.patch` (`5ed1656c...`) | `300911eaf02aa421211f4c6047ee01bc3ddeaade` | Processor #192 (PR #197): GET_STREAM_INFO on every started/stopped change, the requester included. |
| 5 | `parent-adoption-gptp_shadow-85.patch` (`32260287...`) | `1e305876b09001be80d823c6615dff96abe5fd89` | FPGA-gPTP #85 (PR #86): pathTrace is the pathSequence plus thisClock. |
| 6 | `parent-adoption-milan_dp-85.patch` (`33249548...`) | `d255806ce0b53dda3c83339d752bd2cad53281b1` | FPGA-gPTP #85 (PR #86), milan_dp legs gptp, gptp-lat and milan_dp_gptp. |
| 7 | `parent-adoption-milan_dp-82.patch` (`771fc76f...`) | `7d9d730c6728b0db6331c2cba591ab4d1f35637e` | FPGA-gPTP #82 (PR #83): thisClock is grandmaster from reset. |
| 8 | `parent-adoption-milan_dp_gptp-84.patch` (`ec49e1ee...`) | `0e4d10b256efc2b21202aab50880edc033dd5c9a` | FPGA-gPTP #84 (PR #86): sync set and tu clear while grandmaster, after the Annex B.1.1 holdover. |

### Hunks at their commits (new-file line ranges)

| # | File | Hunks (`+start,len`) |
|---|---|---|
| 1 | `scripts/measure_test_evidence_readers.py` | `+43,10` (elab_guards guards and mutants); `+119,6` (aecp_cmds mutants; offset 7 from the patch) |
| 2 | `tb/verilator/milan_dp/sim_nxn.cpp` | `+8686,4`, `+8692,2`, `+8695,2` (the #67 2013-length row; patch hunk at 7240, offset 1443) |
| 3 | `hdl/milan/KL_pp_shadow.sv` | `+1278,3` (the every-slot replication; patch hunk at 1158, offset 117) |
| 4 | `tb/verilator/milan_dp/README.md` | `+658` (G9 row) |
| 4 | `tb/verilator/milan_dp/sim_nxn.cpp` | `+1824,4` (G9 comment), `+2387` (G9 heading), `+2396,3` (G9 push count 1,1) |
| 5 | `tb/verilator/gptp_shadow/sim_main.cpp` | `+891`, `+929,4`, `+945`, `+1005` |
| 6 | `tb/verilator/milan_dp/sim_ax1x1gptp.cpp` | `+79,4` (kThisClock), `+942`, `+984`, `+986,2`, `+990` |
| 6 | `tb/verilator/milan_dp/sim_gptp.cpp` | `+50,4` (THIS_CLOCK), `+988`, `+1048`, `+1051,3`, `+1062,2`, `+1405`, `+1409,2`, `+1421`, `+1423`, `+1426,2`, `+1458,2` |
| 7 | `tb/verilator/milan_dp/sim_ax1x1gptp.cpp` | `+1153,3`, `+1203,3` |
| 7 | `tb/verilator/milan_dp/sim_gptp.cpp` | `+817,6`, `+832,4`, `+844,2` |
| 8 | `tb/verilator/milan_dp/sim_ax1x1gptp.cpp` | `+348`, `+952,2`, `+1020,2`, `+1023`, `+1025`, `+1027,2`, `+1064,20` |

### Composed hunks (two patches, one file)

| File | Patches | How they composed |
|---|---|---|
| `tb/verilator/milan_dp/sim_nxn.cpp` | 2 then 4 | Patch 4's recorded pre-image (`5d494619`) is patch 2's post-image at the patches' authoring base `e9cbb676`. At `d77a8afd` both apply by context with offsets; the hunks are disjoint (2 at 8686-8696, 4 at 1824-2398). |
| `tb/verilator/milan_dp/sim_gptp.cpp` | 6 then 7 | Exact: the base blob `b9f28d9f` is patch 6's pre-image, and patch 6's post-image `faa2f1e4` is patch 7's pre-image. Disjoint hunks. |
| `tb/verilator/milan_dp/sim_ax1x1gptp.cpp` | 6, 7, then 8 | Exact: `20f4b4c0` -> `c4109915` (6) -> `ed6b3129` (7) -> `3d1b05c6` (8), each the next patch's recorded pre-image. Disjoint hunks. |

No patch needed a design change to compose. All eight run together on this tree: the suites whose harness files they compose report 0 failures at the final head: `milan_dp` (12,910 checks, its G9, #67, gptp and gptp-lat rows among them), `gptp_shadow` (310), and the physical `milan_dp_gptp` (209) (section 7).

## 3. Re-recorded pin-derived records

Commit `dddff259e2473b14dfbbbabe965a04bf61637b12`, every file through its generator or gate:

| Record | Generator / gate | Result |
|---|---|---|
| `syn/yosys/rom_digests.tsv` | `bash syn/yosys/ooc.sh --record-rom-digests` | Three rows added. Processor `93fb0b2d`: `ltn_rom.hex` `23cc67ee...e956` (unchanged from `2cbed0a9`), `ucode.hex` `1f78804e...0a8e` (was `518b900c...37f8`). FPGA-gPTP `55680bff`: `gptp_ucode.hex` `19ed525d...0987` (was `a435fba6...b9fd`). |
| `docs/reference/SUBMODULES.md` pin table | `scripts/check_submodule_docs.py` (validates the hand-kept table against the index) | Both rows moved; gate rc 0, 6 exact gitlinks. |
| `docs/diagrams/submodule_boundaries.{drawio,svg,png}`, `PNG_MANIFEST.json` | `python3 docs/diagrams/submodule_boundaries.gen.py` | Both pin labels moved; `--check` rc 0. |
| `docs/diagrams/timesync_chain.{drawio,svg,png}`, `PNG_MANIFEST.json` | `python3 docs/diagrams/timesync_chain.gen.py` | gPTP pin label moved; `--check` rc 0. |
| FPGA-gPTP donor links in `docs/design/GPTP_PLANE.md`, `docs/design/TIME_SYNC.md`, `docs/guides/gptp/{HDL_DEVELOPER,MANAGER,SYSTEM_INTEGRATOR,TEST_DEVELOPER}.md`, `docs/traceability/ieee8021as.md`, `docs/reference/SUBMODULES.md` | `scripts/check_gptp_docs.py` (requires every donor link at the gitlink) | `e4869fd0` -> `55680bff` in 33 links; every linked file and the `#step-versus-slew-policy` anchor exist at the new pin; gate rc 0 (and `--with-submodule` rc 0). |
| `scripts/port_docs.budget` | `python3 scripts/check_port_contracts.py --write-budget` | Header only: ports per tree `hdl 2103 -> 2121` (dev drift since the header was written: this lane changes no parent port), `protocol-processor 1761 -> 1764` (the pin). Undocumented and unjustified counts unchanged. |
| `scripts/naming.budget` | `python3 scripts/measure_naming.py --write-budget` | Byte-identical (95 candidates). |

The timesync diagram and the gPTP donor links are not named in #771's list but are pin-derived
records gated in the docs workflow (the previous gPTP adoption, PR #713, moved them the same way).

Two documentation commits follow:

| Commit | Change |
|---|---|
| `8de4b80ba84967e04da38e0eaed68c0b6b5256e0` | The pin page's #771 section (both donor tables, section 8), register-map notes on `0x624`/`0x628` (thisClock before any peer, #82) and `0x7DC` (the count includes thisClock, #85), and a changelog entry with its generated Contents line (`gen_toc.py --write`) |
| `d664cf54fd57ed06e8896e7c5de1e1511c2ded0c` | The pin page cites `protocol-processor/hdl/aecp/ucode/aecp_commands.json` with its submodule prefix (the cited-path gate found the bare path) |

Fast static gates at `dddff259` (all rc 0): docs_check, check_doc_style, check_gptp_docs
(--with-submodule), DOC_MAP, check_solution_docs, check_feature_status, gen_module_matrix --check,
measure_test_evidence --check, check_rtl_source_lists, check_soc_sources, measure_fail_fast --check,
check_todo_ownership, check_hygiene --check, check_sv_idiom, check_cpp_idiom, check_py_idiom,
check_sh_idiom, check_doc_paths, gen_toc --check, check_nvm_record_space, check_nvm_capture,
check_baremetal_only --check, pp_srcs --check, check_archive. The final-head gate table is in
section 7 (`a97aea01`).

## 4. #638 re-baseline, written under the owner exception

Measured through `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, `--single-thread-synthesis`, the shipping
directives, `general.maxThreads` 32, Vivado 2026.1 Build 6511674, one run at a time under
`flock $VIVADO_LOCK`. External work directory `$HOME/litex-milan/work/a662-771/m1` (export through
`build.sh <shape> --dry-run` and the recipe's export step; `sw/builder/out` and the two ROM paths symlinked
out of the checkout during measurement and unlinked afterwards). RTL inputs: lane head `8de4b80b`; the
route-1x1 and ooc-1x1 runs ran there in round 1, the ooc-8x8 at `d664cf54` (identical synthesis inputs: only
records and documentation differ). Every input digest reproduces at `d664cf54` and at `76b01906`.

| Run | rc | Minutes | Log SHA-256 | Log bytes |
|---|---:|---:|---|---:|
| `route-1x1` | 0 | 44.3 | `8068664a26d0f2e2ef578d4652779e4483e3c7a2fdfec43771454f21e8698167` | 809,861 |
| `rtl-8x8` (RTL elaboration for the 8x8 parameters) | 0 | 1.1 | `cc370cd4b8b58ebbfab1823c346ae05d5a409777c221ecc4119978edea68c911` | 199,032 |
| `ooc-1x1` (`--integrated-clock`, 20 ns) | 0 | 12.1 | `9186250e18f104f1ab964ab08284185981c723f50b9396c33264b95e1fe289f0` | 306,714 |
| `ooc-8x8` (`--integrated-clock`, 20 ns), round 1b | 0 | 24.8 | `4ea92313bff450f6da22268ab1464823de74d71b4f3855809b418ea4eddb61d8` | 314,694 |

No `Synth 8-4445` diagnostic in any log (the one match is the echoed severity command). Each log's one
`Synth 8-6901` is the parent's `crft_emit_en_w` (`milan_datapath.sv:3233`). Route peak memory 8,352 MB;
ooc-8x8 peak 6,137 MB. All 18 memory-image manifest entries of the three measurements rehash equal.

### Verdicts against #708's record, then the write

`python3 syn/ooc/pp_resource_gate.py check <dir> --endpoint <endpoint>` (receipts `gate-head-*-vs-record.log`):

| Endpoint | rc | LUT | FF | Slice | RAMB36 / RAMB18 | DSP | CARRY4 | WNS / WHS ns |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `route-1x1` | **1** | 50,759 (**+1,146**, tol. 500) | 52,832 (+479, tol. 600) | 15,728 (+3) | 74 / 25 | 14 | 3,452 | +0.291 / +0.036 |
| `ooc-1x1` | **1** | 23,828 (**+514**, tol. 250) | 20,000 (+179) | - | 16 / 3 | 8 | 1,537 | +3.337 / +0.159 |
| `ooc-8x8` | **1** | 32,467 (**+2,256**, tol. 316) | 28,220 (**+769**, tol. 339) | - | 21 / 5 | 8 | 2,016 | +1.139 / +0.159 |

Re-running both 1x1 checks at `d664cf54` before the write reproduced the round-1 verdict files byte for
byte. Then, with the tree at the measured state:

```sh
python3 syn/ooc/pp_resource_gate.py record "$WORK/ax7101/gateware" --endpoint route-1x1 --write
python3 syn/ooc/pp_resource_gate.py record "$WORK/ax7101-ooc" --endpoint ooc-1x1 --write
python3 syn/ooc/pp_resource_gate.py record "$WORK/ax8x8-ooc" --endpoint ooc-8x8 --write
python3 syn/ooc/pp_resource_gate.py check-baseline      # baseline PASS: 3 endpoints
```

Each endpoint's `measured` note (hand-kept, as every earlier note) names the measured head, dev and both
pins, states the exceeded figures and this adoption's own share against dev, cites the owner decision
and carries the ledger it names (FPGA-gPTP #82 +278, processor #195 +190, #194 +117, #198 +102, #197 +54,
#196 +34, #183 +34). Tolerances, floors and ceilings are unchanged. The ooc-8x8 record was written,
held aside while the dev 8x8 attribution ran in the dev state, restored, and checked identical to a fresh
print before its commit.

| Endpoint | Input SHA-256 recorded |
|---|---|
| `route-1x1` | `4a26ec65ba57a50610e5cd4d6c03261d6dcfc8efe2158f74be59da172611eff7` |
| `ooc-1x1` | `9388010b698451b45c64016c6e4ab796280b0cdf6abae3f36a7f35496667ec03` |
| `ooc-8x8` | `8c12fce203505ac8f70d3f3f4be71a5b24068d5e2e92811c2bf82f1ec5fb4e66` |

### This adoption's share: dev `d77a8afd` measured the same way

Dev's RTL inputs in this worktree: both gitlinks at their `d77a8afd` pins and
`parent-scratch-tspec-every-slot.patch` reversed (wrapper byte-identical to dev's, `hdl`, `sw`, `configs`
equal to dev's), a fresh export per shape. Scripts restore both submodules and the wrapper and check
`git diff --quiet HEAD` afterwards (both did).

| Dev run | rc | Minutes | Log SHA-256 | Log bytes |
|---|---:|---:|---|---:|
| `route-1x1` (round 1) | 0 | 41.2 | `dfeffe32b806bf7b1f4af98adf6d0b5422adec2682b1019b1c668738d5e2eefa` | 720,398 |
| `ooc-1x1` (round 1) | 0 | 10.2 | `4e60bb90c316981cdfbc6761a0256397fa813f2243a10f5968a7012b4f720509` | 305,830 |
| `rtl-8x8` (round 1b) | 0 | 1.0 | `994b5b2b8b952c1bfbe77fdb009081b00e620540f112143b1b97b3fd2471d4d5` | 199,131 |
| `ooc-8x8` (round 1b) | 0 | 29.2 | `f05a4c1900f6a5364fbad616f10045b6c9c379597909a7abcd62b621c72f1bf0` | 311,625 |

| Endpoint | #708 record | dev (gate vs record) | adopted | adoption alone (head vs dev's record, gate rc) | tolerance |
|---|---:|---:|---:|---:|---:|
| `route-1x1` LUT / FF | 49,613 / 52,353 | 49,989 / 52,622 (rc 0) | 50,759 / 52,832 | **+770** / +210 (rc 1) | 500 / 600 |
| `ooc-1x1` LUT / FF | 23,314 / 19,821 | 23,366 / 19,823 (rc 0) | 23,828 / 20,000 | **+462** / +177 (rc 1) | 250 / 250 |
| `ooc-8x8` LUT / FF | 30,211 / 27,451 | 30,282 / 27,451 (rc 0) | 32,467 / 28,220 | **+2,185** / **+769** (rc 1) | 316 / 339 |

The head-against-dev verdicts use a lane-scratch baseline file (the committed one with that endpoint's
record replaced by dev's printed record, policy unchanged): `gate-head-*-vs-dev.log`. Dev's 8x8 input
digest: `06b62922151d04493ad2ca5e2d2074a76692047ed1dff08b04138c85f47fac1e`.

At 8x8 the growth sits in the SRP listener: `u_pp/u_srp/u_listener` 1,861 / 2,615 -> 3,973 / 3,335 LUT / FF
(+2,112 / +720) against #708's record; the next movers are `u_pp/u_aecp/u_resp` +146, `u_pp/u_notify`
+128 / +32 and `u_pp/u_tx_slots` +122. Processor PRs #195 and #198 both change the SRP listener; the
per-merge chain was measured at 1x1 only (section 9). Processor PR #198 reported its own 8x8 cost as
+1,335 / +618.

### Route detail (route-1x1)

100,659 of 100,659 routable nets fully routed, 0 routing errors; IOB packing PASS.

| Corner | WNS ns | WHS ns |
|---|---:|---:|
| `Slow_0C` | +0.291 | +0.102 |
| `Slow_85C` | +0.291 | +0.102 |
| `Fast_0C` | +1.660 | +0.036 |
| `Fast_85C` | +1.660 | +0.036 |

Worst setup path: `milansoc_sdram_zqcs_timer_count1_reg[26]/C` to `milansoc_sdram_twtrcon_count_reg[0]/R`
(SoC 10 ns clock, 14 levels, 9.255 ns: 1.998 logic, 7.257 routing; outside the wrapper). Worst hold:
`milansoc_rdat1_reg[22]` to `storage_43_reg/DIBDI[14]` (+0.036 ns). With WNS at +0.291 the 0.25 ns fall
limit now binds before the +0.030 ns floor (at +0.041 ns); the area budget and Mark II plan say so.

Route sub-block movements against #708's record (not gated): wrapper LUT +675 / FF +159; `u_pp` +537 / +159;
`u_pp/u_srp` +215 / +133; `u_pp/u_srp/u_listener` +203 / +139; `u_pp/u_aecp` +241 / -4; `u_nvm` +140 / 0;
`u_pp/u_srp/u_talker` +108 / -2; `u_pp/u_aecp/u_dyn` +100 / 0; `u_pp/u_srp/u_vlan` -88 / 0.

### Documentation commit `a97aea01`

| File | Change |
|---|---|
| `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` | New current section "Re-baseline of 2026-10-22, processor 93fb0b2d and FPGA-gPTP 55680bff": the owner exception, three endpoint tables, the adoption's share against dev, the per-donor 1x1 ledger, route corners and paths, input digests, run receipts (head and dev); intro and contents updated |
| `docs/design/AREA_BUDGET.md` | Record pointer, the #771 record paragraph with the exception, headroom table (50,759 LUT, 80.06 %, 12,719 over; 15,728 slices, 122 free; +0.291 / +0.036 ns), critical path, allocation (23,828 standalone; 42,248 / 23,789 routed; 11,070 needed, 12,719 to remove, 53 %), the WNS-fall sentence, the tenth re-baseline paragraph |
| `docs/design/MARK_II_AREA_PLAN.md` | Gate-comparison row (fall limit binds first at +0.041 ns) and the comparison-anchor sentence (#771's 50,759-LUT record) |
| `docs/reference/SUBMODULES.md` | #771 section: re-baselined under the owner exception, +770 over dev's route, Mark II addresses it, WNS +0.291 ns |
| `CHANGELOG.md` | Three lines in the #771 entry |

## 5. route-1x1 and the three-directive image build

route-1x1: section 4 (the recipe's integrated route; rc 0; the gate's record).

The image build is `sw/litex/build.sh ax7101 --sweep` (BUILDING.md section 1: the place-directive sweep
ExtraPostPlacementOpt, AltSpreadLogic_high, ExtraTimingOpt). Its three launch lines were taken verbatim
from `TAG=a662-771 bash sw/litex/build.sh ax7101 --sweep --dry-run` and executed one at a time under
`flock $VIVADO_LOCK`, each only above 20 GB MemAvailable (lane rule: one Vivado at a time; the
launcher's own `setsid` launch would run all three at once). Builder output and ROM paths were symlinked
into `$HOME/litex-milan/work/a662-771/img` and unlinked afterwards. Outputs:
`$HOME/litex-milan/work/build_ax7101_{eppo,asl,eto}_a662-771`. Parent head at launch `a97aea01`
(identical synthesis inputs to every later commit of this lane).

**One deviation, `--vivado-max-threads`.** The first launch (ExtraPostPlacementOpt, the launcher's
`--vivado-max-threads 32`) started seven synthesis processes, about 2 GB each beside a 4 GB parent, and
the service reached its 12 GB cap within five minutes; it was stopped, its partial directory deleted.
Vivado runs one synthesis process per `general.maxThreads` up to seven (checked on a one-module probe at
2, 3 and 4). The launch lines were rerun with that one argument changed: 2 for ExtraPostPlacementOpt, then
1 for the other two after the 2-thread synthesis peaked at 11.1 GB anon. `milan_soc.py`'s own default is
`min(cores, 32)`, so the thread count is host-dependent by design; ExtraPostPlacementOpt at 2 threads
reproduces the recipe's route-1x1 figures exactly (LUT, FF, slices, every corner).

| Directive | Threads | rc | Minutes | Slow WNS / WHS ns | Fast WNS / WHS ns | LUT | Slice | Routed nets | IOB pack | Service peak, current / anon |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| ExtraPostPlacementOpt, **selected** | 2 | 0 | 36.5 | +0.291 / +0.102 | +1.660 / +0.036 | 50,759 | 15,728 | 100,659 / 100,659, 0 errors | 21 PASS, 0 FAIL, 1 INERT | 12.13 / 11.11 GB |
| AltSpreadLogic_high | 1 | 0 | 55.6 | +0.083 / +0.004 | +1.633 / +0.011 | 50,735 | 15,783 | 100,642 / 100,642, 0 errors | 21 PASS, 0 FAIL, 1 INERT | 10.43 / 9.21 GB |
| ExtraTimingOpt | 1 | 0 | 56.8 | +0.297 / +0.004 | +1.633 / +0.008 | 50,747 | 15,783 | 100,657 / 100,657, 0 errors | 21 PASS, 0 FAIL, 1 INERT | 10.87 / 9.22 GB |

Every corner of every directive meets WNS >= +0.03 ns and WHS >= 0 (`*_signoff_{Slow,Fast}_{0C,85C}_timing.rpt`).
Each build's `milan_soc.py` printed "no 12-4739, 20-1307 or 12-5201 diagnostics", published its
`flashboot_layout.json` with the bitstream binding, and left no `*.bit.rejected`. FF 52,832, 86.5 RAM tiles
and 14 DSP in all three. The INERT IOB row is `eth0_rx_er` (no net).

**Selection: ExtraPostPlacementOpt.** It has the fewest slices (15,728 against 15,783) and the largest hold
margin (+0.036 against +0.004 / +0.008 ns); ExtraTimingOpt's setup slack is 6 ps higher. It is also the
shipping recipe's own directive (`cfg_ax7101`) and equals the resource record. Selected image:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `gateware/alinx_ax7101.bit` | 3,825,992 | `d785871ca41f9a8aecd23150c525949624be848cc19d5d29e9234b8bc63c9deb` |
| `flashboot_layout.json` | 854 | `5923922b52373cdf5e8c84c5e0dc0c2ec8d94d19cc65d2eee48907a6ccbaf41a` |
| `aem_desc.bin` | 7,512 | `4fc8d61582a965fe648abc0c15d0551153ff2b27f202d1fbc8319fbb4bdb396d` |
| `gateware/vivado.log` | 809,120 | `5a6068931d5681117a2236838c7a39d973f8a65bb2b458566ebc360be0df9a5f` |

Other bitstreams: AltSpreadLogic_high `6490ae6af937310080f08ea818cc8e7e680e63e1fa185de7f19cf984948658e1`,
ExtraTimingOpt `31413ea00abc16eb7e2b138a57f3ce5499b6b1c4491e67ae49dfbef32783da26` (both 3,825,992 bytes).

Offline image preflight, no programmer I/O, for all three:
`LAYOUT=<build>/flashboot_layout.json BIT=<build>/gateware/alinx_ax7101.bit bash sw/litex/deploy.sh check-images`
rc 0, "complete target image set prepared before programmer writes" and "image preflight OK".

Selected image, section 5 manual checks: `*_signoff_clock_interaction.rpt` has no unsafe pair; the
Ethernet pairs carry the 8 ns datapath-only bound with positive slack (5.00, 6.27, 6.65 and 6.35 ns); the
implementation log has no CRITICAL WARNING and no ERROR diagnostic (its four "ERROR" strings are echoed Tcl
of the IOB check). Receipt: `image-builds.json`.

## 6. Saved-state capture

Not re-measured: the firmware digest did not move. `scripts/check_nvm_capture.py` binds the product
firmware `sw/firmware/milan_baremetal/milan_baremetal.c` (receipt `product_firmware_sha256`
`497845e6243b919638285ce4de18e6687beff6a509d72c8e2e2f2d45ba7b1bed`, equal to the file at the head)
and the harness files of `tb/verilator/nvm_capture_cpu`; this lane changes neither
(`git diff --stat d77a8afd HEAD -- sw/firmware tb/verilator/nvm_capture_cpu` is empty). The gate
passes at the adopted pins: "PASS: capture census, clocks, both timing arms and receipt agree". The
retained maxima: 1x1 3.96548 ms, 8x8 13.86328 ms (at or under 24.5 ms), 8x8 at 100 MHz 10.42973 ms.
The receipt's `processor_pins` field (`2ad2f845`, `7dda9c3b`) is provenance, not a gated input.

## 7. Parent sweep and gate table at the final head

Run at `a97aea01` (the final head), from the physical worktree path, with the lane environment:
GNU Make 4.3 first on PATH, Verilator 5.050, `VERILATOR_JOBS=2`, `PYTHON_CPU_COUNT=4`, `MAKEFLAGS` unset
(each suite's make runs serially), `MILAN_RV32_CC` the verified SDK, and `TSN_GEN_ROOT` the tsn-gen
field oracle built at `rtl.yml`'s `TSN_GEN_REV` (section Environment), so no field campaign skips.

| Run | rc | Tally rc | Suites | Checks | In-suite failures | Wall |
|---|---:|---:|---:|---:|---:|---:|
| `bash scripts/run_all_suites.sh <logs>` (default inventory) | 0 | 0 | 63 / 63, 0 timed out | 2,189,520 | 0 | 3 h 37 min |
| `bash scripts/run_all_suites.sh <logs> --physical-gptp` (milan_dp_gptp) | 0 | 0 | 1 / 1 | 209 | 0 | 81 min |

The four legs the assignment names: `milan_dp` runs `gptp` and `gptp-lat` as its prefix cases (the suite:
12,910 checks over 17 tallies, PASS); `milan_dp_gm_steps` is in the default inventory (196 checks, PASS);
`milan_dp_gptp` is the physical leg (209 checks, PASS, its physical simulation 3,788.85 s, then the
no-Pdelay accounting and recentre controls, 14 checks each). The composed patches' suites: `milan_dp`'s
G9 rows (GET_STREAM_INFO to both controllers, the requester included) and #67 rows report ok;
`gptp_shadow` 310 checks; `pp_shadow` 2,187; `tsn_fuzz` 899 (gPTP field campaign 677 pass, AAF 164 pass, 0
known gaps). Per-suite counts: `sweep-tally-per-suite.txt`; log digests: `sweep-log-digests.txt`.

Run notes:

- The first default-sweep launch was started under `nohup` and aborted after 46 s in the driver's own
  cancellation self-test (`hard-HUP` timed out after 12 s: `nohup` makes SIGHUP ignored in the sweep and
  everything it execs). No suite had run. It was relaunched with `setsid`, which leaves SIGHUP at its
  default; the self-test then passed. The aborted output is kept in lane scratch.
- The physical leg ran beside the default sweep with its own `SUITE_SWEEP_LOCK` (the tree lock was held by
  the default sweep). It builds only `tb/verilator/milan_dp/obj_ax1x1gptp`, which the default `milan_dp` run
  does not build, and reads `ucode.hex`, `ltn_rom.hex` and `gptp_ax1x1_ucode.hex` from `milan_dp`. The two
  overlapped for 94 s (default `milan_dp` started 12:19:29; the physical leg ended 12:21:03, running only its
  recentre verifier on the built binary). In that window the default run regenerated only its own
  `gptp_ucode.hex`; the three files the physical binary reads keep their 11:01:22 timestamps from the
  physical leg's own generation.
- The field campaigns rewrite the date stamp in two tracked files,
  `hdl/ieee1722/avtp/doc/TEST_RESULTS.md` and `hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md` (counts
  unchanged: 164 and 677 pass); both were restored to their committed bytes after the run.
- Yosys and behave ran beside the default sweep; the docs-check replica ran beside it after the physical
  leg ended; xvlog ran after the sweep, alone.

### Gates at `a97aea01` (the final head)

| Gate | rc | Seconds | Result |
|---|---:|---:|---|
| `python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 | 0.1 | baseline PASS: 3 endpoints |
| `bash syn/yosys/ooc.sh --record-rom-digests` | 0 | 0.4 | the ledger regenerates |
| `git diff --exit-code syn/yosys/rom_digests.tsv` | 0 | 0.0 | byte-identical |
| `python3 protocol-processor/scripts/check-integrator-params.py` | 0 | 0.1 | parameters: top 29, guide 29, diagram 29, OK |
| `python3 scripts/lint_rtl.py --check` | 0 | 19.1 | LINT GATE: PASS (90 violation(s) <= ratchet 90; 18 waived, 0 justified lint_off) |
| `python3 scripts/check_port_contracts.py` | 0 | 2.8 | hdl, gptp and processor undocumented counts within their budgets |
| `python3 scripts/measure_naming.py --check` | 0 | 0.5 | NAMING RATCHET: PASS (95 candidate(s), all recorded by identity; 95 recorded) |
| `python3 scripts/measure_test_evidence.py --check` | 0 | 7.9 | 0 unexplained DUT-source readers (it notes the mutation ratchet could be lowered to 66) |
| `python3 scripts/pp_srcs.py --check` | 0 | 0.3 | source lists agree |
| `python3 scripts/check_submodule_docs.py` | 0 | 0.5 | submodule documentation: OK (6 exact gitlinks) |
| `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | 0.2 | gPTP documentation: OK (8 current pages, donor checkout verified) |
| `python3 scripts/check_nvm_capture.py` | 0 | 0.7 | PASS: capture census, clocks, both timing arms and receipt agree |
| `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | 0.4 | submodule diagram: OK (6 exact gitlinks, decoded PNG) |
| `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | 0.3 | time-sync diagram: OK (RTL, features, Gitlink, decoded PNG) |
| `python3 scripts/docs_check.py (the no-git job's gate, in place)` | 0 | 6.8 | docs_check: 0 finding(s) across 210 md files + 1399 scrubbed text files, scrub self-test 23/23, routing arms 4 |
| `python3 scripts/check_feature_status.py (the no-git job's gate, in place)` | 0 | 1.1 | feature_status: 0 finding(s) |
| `flock $VIVADO_LOCK python3 scripts/xvlog_gate.py --check` (after the sweep) | 0 | 149 | xvlog gate: PASS (0 findings; 0 hdl/, 0 pinned processors) |
| `syn/yosys/run.sh` (full serial gate) | 0 | 864 | tops 58, pass 58, fail 0; tied inputs 29, justified 2, unjustified 0; TAP-PURITY PASS |
| `cd tests && python3 -B -m behave -f plain` | 0 | 1.2 | 14 features, 406 scenarios, 1,977 steps passed; 0 failed, 0 skipped |
| `scripts/run_all_suites.sh` + `suite_tally.py --quiet --expect-suite-root tb/verilator` | 0, 0 | 13,034 | 63 / 63 suites; 2,189,520 checks; 0 in-suite failures; 0 timed out |
| `scripts/run_all_suites.sh --physical-gptp` + `suite_tally.py ... --physical-gptp` | 0, 0 | 4,878 | milan_dp_gptp 1 / 1; 209 checks; 0 failures |

### Hosted docs-check steps, literal, at the final head

Every `run:` body of the docs workflow's gate steps (wire-accountability, docs-gates-0, both builder
legs, the CI event gate), written out unchanged and run with `bash -e` from the physical worktree path,
GNU Make 4.3 first on PATH, `MAKEFLAGS=-j1 --no-print-directory`, each job's `env:` (`PIP_CONSTRAINT`), the
em-dash step's `pull_request` event with base `dev`, and the job budgets capped at this lane's limits
(`VERILATOR_JOBS=2`, campaigns 4). Interpreter: a lane-scratch CPython 3.12.3 venv (the runner's version)
with the workflow's own pinned installs; the Markdown gates (gate_7, gate_8, gate_9, gate_43, gate_45) with
the specified Markdown venv first on PATH. The builder legs see `HOME` set to a lane-scratch home whose
`br-milan-rv32/host` is the verified SDK. Receipts: `docs-steps-final-receipts.json`,
`docs-steps-final-leg1-litex-receipts.json`.

**44 workflow steps: 42 run, all rc 0; 2 skipped by rule; plus builder leg 1 run again with the bench
LiteX interpreter, rc 0.** The builder legs report their documented NOT RUN arms: leg 0 one (gate 1b, the
MAKEFLAGS mutation is inert under Make 4.3); leg 1 sixteen without a LiteX interpreter (as on the hosted
runner); and one (gate 11, the absent mf48 calibration report) with `MILAN_LITEX_PYTHON` set. Round 1's
replica at `d664cf54` ran the same 44-step list with the same result; its HANDOFF and STOP comment called
that "44 of 44 run steps", which miscounted the two skipped steps as run.

| Step | Name | rc | Make | Seconds | Log SHA-256 (prefix), interpreter |
|---|---|---:|---|---:|---|
| `wire-accountability/ci_step_4` | Advertised-vs-emitted gate (green since 2026-07-28, item 00) | 0 | GNU Make 4.3 | 0.6 | `7515279c4d016cf7` (5076 B), ci312 |
| `docs-gates-0/gate_1` | Build the validated HDL reference | 0 | GNU Make 4.3 | 2.8 | `0387d62aa44da0ba` (923 B), ci312 |
| `docs-gates-0/gate_7` | Link health, wording, dead-reference and local-info gate | 0 | GNU Make 4.3 | 6.9 | `c7eb3c8b2205ea6b` (128 B), md-venv |
| `docs-gates-0/gate_8` | Added-line em-dash gate | 0 | GNU Make 4.3 | 3.1 | `b4519cac289630be` (141 B), md-venv |
| `docs-gates-0/gate_9` | Concise audience documentation gate | 0 | GNU Make 4.3 | 0.5 | `94d17028bcbb08db` (167 B), md-venv |
| `docs-gates-0/gate_10` | Audience diagram no-drift gate | 0 | GNU Make 4.3 | 2.1 | `79dce4dc64e4d578` (242 B), ci312 |
| `docs-gates-0/gate_11` | Product solution source-fact gate | 0 | GNU Make 4.3 | 2.9 | `9ef43cc924919e10` (146 B), ci312 |
| `docs-gates-0/gate_12` | Verified submodule documentation gate | 0 | GNU Make 4.3 | 2.0 | `88d83848aecf8145` (227 B), ci312 |
| `docs-gates-0/gate_13` | HDL timing diagram no-drift gate | 0 | GNU Make 4.3 | 1.2 | `af9493d0e4acd65e` (241 B), ci312 |
| `docs-gates-0/gate_14` | Published diagram PNG gate | 0 | GNU Make 4.3 | 13.7 | `17d1d2360a98e818` (125 B), ci312 |
| `docs-gates-0/gate_15` | Milan feature-status consistency gate | 0 | GNU Make 4.3 | 1.2 | `77f7649b1865c0da` (1500 B), ci312 |
| `docs-gates-0/gate_16` | Traceability matrix no-drift gate | 0 | GNU Make 4.3 | 0.7 | `4e782e68ed5c0929` (118 B), ci312 |
| `docs-gates-0/gate_18` | Imported gPTP documentation gate | 0 | GNU Make 4.3 | 0.8 | `09bf8d75fba75733` (2595 B), ci312 |
| `docs-gates-0/gate_19` | Code-quality measurement self-tests | 0 | GNU Make 4.3 | 0.1 | `862838344ece59e4` (3293 B), ci312 |
| `docs-gates-0/gate_21` | Bare-metal scope gate | 0 | GNU Make 4.3 | 30.6 | `7666c17fd2628528` (115 B), ci312 |
| `docs-gates-0/gate_24` | Compiler-absent firmware controls | 0 | GNU Make 4.3 | 424.4 | `b61dde10aac8c0df` (51453 B), ci312 |
| `docs-gates-0/gate_26` | NVM record-space gate | 0 | GNU Make 4.3 | 41.3 | `f9c646f352eafc08` (9776 B), ci312 |
| `docs-gates-0/gate_27` | Capture measurement census and clock gate | 0 | GNU Make 4.3 | 0.7 | `7bb472e312a53443` (398 B), ci312 |
| `docs-gates-0/gate_28` | Saved-state writer gate | 0 | GNU Make 4.3 | 166.9 | `4cb4ddb463685c51` (23319 B), ci312 |
| `docs-gates-0/gate_29` | SoC source-list gate (Vivado would fail 40 min in without this) | 0 | GNU Make 4.3 | 2.8 | `0d36e3ad97cf5cce` (4794 B), ci312 |
| `docs-gates-0/gate_30` | RTL source-list drift gate | 0 | GNU Make 4.3 | 4.7 | `be8805dc2fee50ed` (3453 B), ci312 |
| `docs-gates-0/gate_31` | Boundary-unit naming ratchet | 0 | GNU Make 4.3 | 0.9 | `26a8c183fb059eac` (40599 B), ci312 |
| `docs-gates-0/gate_32` | Port contract gate | 0 | GNU Make 4.3 | 6.1 | `2b2161f53da63e3e` (5040 B), ci312 |
| `docs-gates-0/gate_33` | Fail-fast ratchet | 0 | GNU Make 4.3 | 3.3 | `24f772d7d3e047e7` (12426 B), ci312 |
| `docs-gates-0/gate_34` | TODO ownership gate | 0 | GNU Make 4.3 | 3.7 | `db2b593a31adcf93` (2745 B), ci312 |
| `docs-gates-0/gate_35` | Test-evidence ratchet | 0 | GNU Make 4.3 | 20.9 | `3e871434f9fea18d` (26976 B), ci312 |
| `docs-gates-0/gate_36` | Mechanical hygiene ratchet | 0 | GNU Make 4.3 | 0.8 | `fe75355ba99819b3` (3972 B), ci312 |
| `docs-gates-0/gate_37` | SystemVerilog idiom gate | 0 | GNU Make 4.3 | 0.7 | `ccd900273b796fdf` (3173 B), ci312 |
| `docs-gates-0/gate_38` | C and C++ idiom gate | 0 | GNU Make 4.3 | 3.1 | `03ce9e7f2961fe2a` (3909 B), ci312 |
| `docs-gates-0/gate_39` | Python idiom gate | 0 | GNU Make 4.3 | 11.6 | `f1bd67e36192d8b0` (2992 B), ci312 |
| `docs-gates-0/gate_40` | Shell idiom gate | 0 | GNU Make 4.3 | 0.4 | `a57f331056f1f93e` (2696 B), ci312 |
| `docs-gates-0/gate_43` | Doc cited-path gate | 0 | GNU Make 4.3 | 0.1 | `c718971efb9c2284` (101 B), md-venv |
| `docs-gates-0/gate_44` | Archive integrity gate | 0 | GNU Make 4.3 | 0.5 | `1a15e66a07892f54` (128 B), ci312 |
| `docs-gates-0/gate_45` | Per-page contents gate | 0 | GNU Make 4.3 | 10.0 | `a5b8acc246e89848` (196 B), md-venv |
| `docs-gates-0/gate_46` | AEM store generator self-test | 0 | GNU Make 4.3 | 0.1 | `9f126bf9dfc7cb55` (3596 B), ci312 |
| `docs-gates-0/gate_47` | Sweep/build shape gate | 0 | GNU Make 4.3 | 11.4 | `6d11ca230f8be88f` (19670 B), ci312 |
| `docs-gates-0/gate_48` | Deploy shape gate | 0 | GNU Make 4.3 | 0.4 | `3e0d170d186799e7` (9264 B), ci312 |
| `docs-gates-0/gate_49` | Entity shape gate | 0 | GNU Make 4.3 | 54.5 | `b8cee2d906b0cba5` (27683 B), ci312 |
| `docs-gates-0/gate_50` | CI scheduling and evidence controls | 0 | GNU Make 4.3 | 25.2 | `294ec81eee45edff` (112557 B), ci312 |
| `docs-gates-1/gate_25_0` | End-station builder gates, leg 0 of 2 | 0 | GNU Make 4.3 | 797.2 | `d47e82a2743fef05` (50435 B), ci312 |
| `docs-gates-2/gate_25_1` | End-station builder gates, leg 1 of 2 | 0 | GNU Make 4.3 | 208.0 | `8b9eac7d341c7c08` (71216 B), ci312 |
| `docs-gates-2/gate_41` | CI event and SHA contract gate | 0 | GNU Make 4.3 | 198.8 | `64abf3064cc4c7d2` (336285 B), ci312 |
| `docs-gates-2/gate_42` | Local act runner contract gate | SKIP | - | - | executes the candidate act_ci.py on the host; AGENTS.md section 5 allows the candidate copy only inside the disposable CI job |
| `docs-check-no-git/ci_step_3` | Strip git metadata, then run the docs gate | SKIP | - | - | its body runs rm -rf .git, which would delete this worktree's git link; its two gates run in place below |
| `docs-gates-2 (with MILAN_LITEX_PYTHON)/gate_25_1` | End-station builder gates, leg 1 of 2 | 0 | GNU Make 4.3 | 295.4 | `78d2ff455d3de38e` (70776 B), ci312 |

## 8. Parent-visible list

Committed on the pin page (`docs/reference/SUBMODULES.md`, "Issue #771 adopts ...") in `8de4b80b`,
with two register-map notes and a changelog entry. From each donor PR body:

| Donor PR (issue) | Parent-visible result | Parent position in this lane |
|---|---|---|
| processor #173 (#72) | REQ tags and a traceability gate; tests and docs only | Parent gates that read processor files count three more files |
| processor #175 (#151) | Every elaboration guard is `$fatal` (Verilator, sv2v with Yosys, xvlog) | Patch 1 classifies `tb/elab_guards/guards.py` and `mutants.py` |
| processor #174 (#73) | One AECP command model (`aecp_commands.json`, `aecp_fields.json`) generates F06.14 and dispatch data | Patch 1 classifies `tb/aecp_cmds/mutants.py`; firmware consumption stays follow-up (per PR #174) |
| processor #180 (#178, #179) | Unchanged SET_CONFIGURATION index: no notification; missing index: NO_SUCH_DESCRIPTOR; ucode changes | No parent change needed |
| processor #182 (#177) | GET_AVB_INFO on a non-AVB_INTERFACE descriptor: NOT_IMPLEMENTED with echo (was NOT_SUPPORTED) | No parent change needed |
| processor #183 (#176) | SET_STREAM_INFO accepts the 2013 48-byte body (cdl 60), answers in the 2021 form; other lengths BAD_ARGUMENTS | Patch 2 (milan_dp #67 rows) |
| processor #187 (#181) | Notification queue occupancy registered; router scan from registers; no cycle change | No parent change; route timing improves (PR #187's routed parent record) |
| processor #191 (#184) | MSRP Domain re-declaration JoinIn only while a peer Domain is registered, else JoinMt | No parent change needed |
| processor #194 (#190) | `cfg_tspec_max_frame_i` per source, `[N_STREAM_OUT_P*16-1:0]` (the only top port change) | Patch 3 drives every slot with the wrapper's one value; the CRF slot's own value (PR #194's "part 2") is not in this lane |
| processor #196 (#185, #186) | READ_DESCRIPTOR CONTROL serves the IDENTIFY current value; both unlock notifications carry UNLOCK; internal `rgy_flags` wire | No parent change needed |
| processor #195 (#188, #189) | A rebind keeps the owed Listener Leave; REGISTERING_FAILED follows the registered type | No parent change needed |
| processor #197 (#192) | Started/stopped change of a Stream Input pushes GET_STREAM_INFO to every controller, requester included; `act_strt_cmd_chg_o` removed (internal) | Patch 4 (milan_dp G9 rows and README) |
| processor #199 (milan-fpga #632) | SET_STREAM_INFO's notification compares the stored offset once set | No parent change in this lane; #770 consumes it |
| processor #198 (#193) | One declaring Listener applicant per StreamID (owner election in the per-sink plane) | No parent change; area in section 9 |
| FPGA-gPTP #78 (#640 M7) | Timer deadlines in distributed RAM | Already the old pin's tree: no change in this adoption |
| FPGA-gPTP #83 (#82) | thisClock is grandmaster and `{thisClock}` the path from reset release; ROM words 1022/1023 carry thisClock; gmPresent for priority1 below 255 | Patch 7 (milan_dp gptp, gptp-lat and physical-rate rows); register-map `0x624`/`0x628` note |
| FPGA-gPTP #86 (#84) | Grandmaster role sets sync-ok, so `tu` is 0 after the Annex B.1.1 holdover a grandmaster change arms | Patch 8 (physical-rate loss and recovery arms) |
| FPGA-gPTP #86 (#85) | Published path = received pathSequence + thisClock; counts + 1, GET_AS_PATH + 8 bytes | Patches 5 and 6; register-map `0x7DC` note |

Interface check: the processor top's only port change is the TSpec width; the gPTP engine's ports and
parameters are unchanged; `check-integrator-params.py` passes (29/29/29).

Not changed, reported: two parent RTL comments describe the pre-#85 count meaning
(`hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:635-638`, `hdl/milan/milan_datapath.sv:2152-2157`:
"count one is the explicit one-entry `[GM]` sequence"; now `[GM]` publishes count two and count one
is `{thisClock}`). The logic is count-agnostic. Editing them would change measured RTL inputs and is
outside the supplied patches.

## 9. 1x1 cost per separable donor change

### Predecessor versus this adoption (dev `d77a8afd` measured)

Dev's own RTL inputs measured in this worktree with the same recipe and flow: both gitlinks at their
`d77a8afd` pins (`2cbed0a9`, `e4869fd0`) and `parent-scratch-tspec-every-slot.patch` reversed, so
`hdl/milan/KL_pp_shadow.sv` is byte-identical to dev's and `hdl`, `sw` and `configs` equal dev's
(checked with `git diff --quiet d77a8afd`). Fresh export in `$HOME/litex-milan/work/a662-771/dev`.
Afterwards both submodules and the wrapper were restored and `git diff --quiet HEAD` holds.

| Run | rc | Minutes | Log SHA-256 | Log bytes |
|---|---:|---:|---|---:|
| dev `route-1x1` | 0 | 41.2 | `dfeffe32b806bf7b1f4af98adf6d0b5422adec2682b1019b1c668738d5e2eefa` | 720,398 |
| dev `ooc-1x1` | 0 | 10.2 | `4e60bb90c316981cdfbc6761a0256397fa813f2243a10f5968a7012b4f720509` | 305,830 |

| Endpoint | #708 record | dev `d77a8afd` (gate vs record) | adopted head | this adoption (head - dev) | tolerance |
|---|---:|---:|---:|---:|---:|
| `route-1x1` LUT | 49,613 | 49,989 (+376, rc 0) | 50,759 | **+770** | +500 |
| `route-1x1` FF | 52,353 | 52,622 (+269) | 52,832 | +210 | +600 |
| `route-1x1` slice | 15,725 | 15,786 (+61) | 15,728 | -58 | +80 |
| `route-1x1` WNS / WHS ns | +0.215 / +0.036 | +0.268 / +0.015 | +0.291 / +0.036 | +0.023 / +0.021 | floor +0.030 / 0 |
| `ooc-1x1` LUT | 23,314 | 23,366 (+52, rc 0) | 23,828 | **+462** | +250 |
| `ooc-1x1` FF | 19,821 | 19,823 (+2) | 20,000 | +177 | +250 |

RAMB36, RAMB18 and DSP are equal at all three points. Dev's route corners: Slow +0.268 / +0.055,
Fast +1.633 / +0.015 ns; 100,237 nets fully routed, 0 errors. Dev route input SHA-256 (the gate's
digest, read with the tree in the dev state): `d5a1779b3b168d3d7d8b975535805e484202ed10ace5526cc036369fc0bec270`.

So the predecessor (dev since #708's record) is within every tolerance, and this adoption alone
exceeds the route LUT tolerance (+770 > +500) and the standalone 1x1 LUT tolerance (+462 > +250).

Routed hierarchy, adopted head minus dev (`report_utilization -hierarchical_depth 10
-hierarchical_min_primitive_count 0`, both from the same flow):

| Instance | head LUT / FF | head - dev LUT / FF |
|---|---:|---:|
| whole image | 50,759 / 52,832 | +770 / +210 |
| `milan_datapath` | 42,248 / 41,690 | +748 / +211 |
| `milan_datapath/g_gptp_plane.u_gptp_shadow` (FPGA-gPTP #82, #84, #85) | 5,283 / 4,755 | **+415 / +5** |
| `.../u_gptp_shadow/u_engine` | 4,150 / 3,390 | +344 / +5 |
| `.../u_gptp_shadow/u_txret` | 333 / 279 | +32 / 0 |
| `milan_datapath/pp_shadow` (the 14 processor PRs) | 23,789 / 18,961 | **+353 / +161** |
| `.../pp_shadow/u_pp` | 23,075 / 18,131 | +379 / +163 |
| `.../pp_shadow/u_nvm` | 652 / 476 | -25 / 0 |
| every other block (largest: `csr` -79, `chan_map_capture` +51, `gptp_ctl_mux` -45) | | about +2 / +44 |

### Per processor merge: `KL_pp_shadow` standalone synthesis at 1x1

Method (`$HOME/litex-milan/work/a662-771/chain/<point>`): for each processor first-parent merge, the
processor submodule is checked out at that merge in place; the wrapper's TSpec connection is the
patched one from #194's merge on and the reversed (dev) one before it, matching each point's port
width; a fresh export runs `build.sh ax7101 --dry-run` and the recipe's export step, so each
point's `ucode.hex` and `ltn_rom.hex` come from that point's own generators; the recipe prepares the
standalone script (`--single-thread-synthesis --integrated-clock`, the wrapper parameters from the
head route's log, which binds the same 1x1 shape); one Vivado run under the lock. The parent tree is
otherwise the lane head (the gPTP gitlink does not enter `KL_pp_shadow`). Afterwards the processor
returned to `93fb0b2d` and the wrapper to its committed bytes (sha256 `d03881ed...`), checked by
`git diff --quiet HEAD`. Processor #173 changes no RTL or ROM input, so it equals the old pin by
construction and was not run.

| Merge (PR, processor issue) | LUT | FF | RAMB36 / RAMB18 | DSP | CARRY4 | 1x1 cost LUT | 1x1 cost FF |
|---|---:|---:|---:|---:|---:|---:|---:|
| old pin `2cbed0a9` (dev `d77a8afd` measurement) | 23,366 | 19,823 | 16 / 3 | 8 | 1,501 | | |
| #173 (#72 traceability) | = old pin | | | | | 0 (no input) | 0 |
| #175 (#151 elaboration guards) | 23,366 | 19,823 | 16 / 3 | 8 | 1,501 | **0** | **0** |
| #174 (#73 command model) | 23,366 | 19,823 | 16 / 3 | 8 | 1,501 | **0** | **0** |
| #180 (#178, #179 SET_CONFIGURATION) | 23,366 | 19,823 | 16 / 3 | 8 | 1,501 | **0** | **0** |
| #182 (#177 GET_AVB_INFO) | 23,315 | 19,818 | 16 / 3 | 8 | 1,501 | **-51** | **-5** |
| #183 (#176 SET_STREAM_INFO 2013 body) | 23,349 | 19,823 | 16 / 3 | 8 | 1,501 | **+34** | **+5** |
| #187 (#181 notification-router cut) | 23,356 | 19,828 | 16 / 3 | 8 | 1,501 | **+7** | **+5** |
| #191 (#184 MSRP Domain JoinMt) | 23,331 | 19,825 | 16 / 3 | 8 | 1,507 | **-25** | **-3** |
| #194 (#190 per-source TSpec, every slot driven) | 23,448 | 19,827 | 16 / 3 | 8 | 1,507 | **+117** | **+2** |
| #196 (#185, #186 CONTROL and UNLOCK) | 23,482 | 19,860 | 16 / 3 | 8 | 1,507 | **+34** | **+33** |
| #195 (#188, #189 Listener registration) | 23,672 | 20,000 | 16 / 3 | 8 | 1,513 | **+190** | **+140** |
| #197 (#192 started/stopped notification) | 23,726 | 19,992 | 16 / 3 | 8 | 1,513 | **+54** | **-8** |
| #199 (milan-fpga #632 SET_STREAM_INFO change gate) | 23,726 | 19,992 | 16 / 3 | 8 | 1,513 | **0** | **0** |
| #198 (#193 one Listener declaration per StreamID) = adopted head | 23,828 | 20,000 | 16 / 3 | 8 | 1,537 | **+102** | **+8** |
| total, adopted head minus old pin | | | | | | **+462** | **+177** |

The fourteen deltas sum exactly to the head-minus-dev standalone figure. RAMB36, RAMB18 and DSP
never move. Moves of a few tens of LUTs on merges whose RTL change is small (#182, #183, #187, #191)
are of the size the area budget calls synthesis noise. The largest costs are #195 (+190 / +140: the
per-sink 64-bit leave copy is flip-flops at one and two sinks), #194 (+117 LUT, even with every slot
driven by the same value), #198 (+102 / +8) and #197 (+54).

#198 at 1x1 is +102 LUT / +8 FF, against its accepted 8x8 cost of +1,335 LUT / +618 FF.

`ucode.hex` per point (sha256 prefix): old pin, #175, #174 `518b900c`; #180 to #194 `a3b62cab`;
#196 to #197 `a7b1af66`; #199 and #198 `1f78804e`. `ltn_rom.hex` is `23cc67ee` at every point.

| Point | Processor | Wrapper TSpec | rc | Minutes | Log SHA-256 (prefix) | Log bytes | `ucode.hex` |
|---|---|---|---:|---:|---|---:|---|
| `pr175-6d53686` | `6d536868ee2a` | reversed | 0 | 10.1 | `011cb03891367b4e` | 305,909 | `518b900c4a565090` |
| `pr174-22c139a` | `22c139a4323b` | reversed | 0 | 10.1 | `8f09cd4422fd2c48` | 305,907 | `518b900c4a565090` |
| `pr180-f0b1b9d` | `f0b1b9d85c22` | reversed | 0 | 10.1 | `944c35d31b9b2194` | 305,908 | `a3b62cabe2cb0913` |
| `pr182-77cf6fb` | `77cf6fb4e7ac` | reversed | 0 | 11.2 | `f6cc00621806ac13` | 305,048 | `a3b62cabe2cb0913` |
| `pr183-08ae001` | `08ae00130f09` | reversed | 0 | 11.0 | `119dbfff1737a036` | 306,799 | `a3b62cabe2cb0913` |
| `pr187-5addf29` | `5addf29759a2` | reversed | 0 | 9.8 | `096fadc3f00caf4c` | 307,066 | `a3b62cabe2cb0913` |
| `pr191-246cbc2` | `246cbc22df28` | reversed | 0 | 10.2 | `f543c4ae3f9d2288` | 305,297 | `a3b62cabe2cb0913` |
| `pr194-b48312e` | `b48312e13b8a` | patched | 0 | 9.6 | `acc56fe0ae7d378c` | 304,730 | `a3b62cabe2cb0913` |
| `pr196-24c7f85` | `24c7f8534043` | patched | 0 | 10.6 | `e46aed9cb082bc7e` | 306,261 | `a7b1af66b72cd4ae` |
| `pr195-2160169` | `21601694880e` | patched | 0 | 10.7 | `bc05cc8ad1f10055` | 306,634 | `a7b1af66b72cd4ae` |
| `pr197-0802312` | `08023123ae2d` | patched | 0 | 10.7 | `316ace5fde8da6fd` | 307,668 | `a7b1af66b72cd4ae` |
| `pr199-859b537` | `859b537b0bd3` | patched | 0 | 10.4 | `2ac7a32aa1c5458f` | 307,666 | `1f78804e448c385d` |
| dev `ooc-1x1` (old pin) | `2cbed0a987c1` | dev | 0 | 10.2 | `4e60bb90c316981c` | 305,830 | `518b900c4a565090` |
| head `ooc-1x1` (#198) | `93fb0b2d736b` | patched | 0 | 12.1 | `9186250e18f104f1` | 306,714 | `1f78804e448c385d` |

Every log: no `Synth 8-4445` diagnostic, one `Synth 8-6901` (the parent's `crft_emit_en_w`).

### Per gPTP change

FPGA-gPTP #78: no cost in this adoption (its merge `b9ade3a6` has the old pin's tree).

At synthesis (the route flow's own `alinx_ax7101_utilization_hierarchical_synth.rpt`), the adopted
head minus dev: `u_gptp_shadow` +258 LUT / +5 FF (`u_engine` +218 / +5), `pp_shadow` +465 / +160.
Routed (section above): +415 / +5 and +353 / +161.

The integrated hierarchy is too noisy to split the gPTP changes: an integrated synthesis-only run at
the old gPTP pin with the new processor (`$HOME/litex-milan/work/a662-771/gchain/gptp-old-e4869fd0`,
rc 0, 32.2 min) puts `u_gptp_shadow` at 5,124 LUTs, against 5,268 in dev's run, with the same gPTP
RTL; the second point (`gptp-pr83-43acfbc`, rc 0, 32.1 min) is retained but not used for the split.

So the gPTP cost is measured like the wrapper's: `KL_gptp_shadow` standalone synthesis at 1x1,
built by a lane-scratch preparer that mirrors `pp_baseline.py`'s standalone step (the export's own
source prefix and synthesis command, `-top KL_gptp_shadow -mode out_of_context`, the six generics
Vivado bound in that point's integrated log: `TDATA_WIDTH_P=64`, `CLK_HZ_P=50000000`, the export's
`gptp_ucode.hex`, `PHC_TICK_NS_P=0`, `INGRESS_LAT_NS_P=656`, `EGRESS_LAT_NS_P=219`; `Synth 8-4445`
promoted to an error; a 20 ns clock; the recipe's report block). Each point's export generated its
own `gptp_ucode.hex` (with the board MAC, so these differ from the ROM ledger's default-MAC rows).

| Point | `KL_gptp_shadow` LUT | FF | RAMB36 / RAMB18 | DSP | CARRY4 | 1x1 cost | `gptp_ucode.hex` | rc / minutes |
|---|---:|---:|---:|---:|---:|---:|---|---|
| old pin `e4869fd0` (and #78, same tree) | 5,111 | 4,984 | 3 / 1 | 4 | 334 | | `fd3dad06a18b` | 0 / 2.4 |
| #83 merge `43acfbcc` (FPGA-gPTP #82, boot grandmaster) | 5,389 | 4,991 | 3 / 1 | 4 | 334 | **+278 / +7** | `9257b737b919` | 0 / 2.4 |
| adopted `55680bff`, #86 (FPGA-gPTP #84 and #85) | 5,421 | 4,989 | 3 / 1 | 4 | 334 | **+32 / -2** | `e73320de5d35` | 0 / 2.4 |

Only `u_engine` moves (4,406 -> 4,684 -> 4,716 LUTs); `rx_fifo`, `tx_fifo`, `u_txret`,
`u_txticket` and the wrapper's own logic are identical at all three points.

### Gate-exact verdicts for the adoption alone

A lane-scratch baseline (`dev-baseline.json`: the committed baseline with the `route-1x1` and
`ooc-1x1` records replaced by dev's printed records, policy unchanged) judged the head measurements
with the tree back in the head state:

| Check | rc | Result |
|---|---:|---|
| head `route-1x1` against dev's record | 1 | LUT 49,989 -> 50,759, +770 > +500; FF +210, slice -58, RAM/DSP 0, WNS +0.023, WHS +0.021, all within |
| head `ooc-1x1` against dev's record | 1 | LUT 23,366 -> 23,828, +462 > +250; FF +177, RAM/DSP 0 |
| head `route-1x1` against the committed record, repeated | 1 | byte-identical to the first verdict |

Gate input digests: head route `4a26ec65ba57a50610e5cd4d6c03261d6dcfc8efe2158f74be59da172611eff7`,
head ooc-1x1 `9388010b698451b45c64016c6e4ab796280b0cdf6abae3f36a7f35496667ec03`, dev route
`d5a1779b3b168d3d7d8b975535805e484202ed10ace5526cc036369fc0bec270` (reproduced byte-identically on
a second print), dev ooc-1x1 `b37b073be98fcb1c9ac55bb081963612b0b9eb349769857067f5a9f3e409e0c5`.

### Summary of the 1x1 cost, this adoption

| Donor change | 1x1 cost (instrument) |
|---|---|
| processor #198 (#193) | +102 LUT / +8 FF (`KL_pp_shadow` standalone) |
| processor #195 (#188, #189) | +190 / +140 |
| processor #194 (#190) | +117 / +2 |
| processor #197 (#192) | +54 / -8 |
| processor #196 (#185, #186) | +34 / +33 |
| processor #183 (#176) | +34 / +5 |
| processor #187 (#181) | +7 / +5 |
| processor #191 (#184) | -25 / -3 |
| processor #182 (#177) | -51 / -5 |
| processor #173, #175, #174, #180, #199 | 0 / 0 |
| processor total | +462 / +177 (standalone); +353 / +161 in the routed image |
| FPGA-gPTP #82 (PR #83) | +278 / +7 (`KL_gptp_shadow` standalone) |
| FPGA-gPTP #84 and #85 (PR #86) | +32 / -2 |
| FPGA-gPTP #78 | 0 (same tree) |
| gPTP total | +310 / +5 (standalone); +415 / +5 in the routed image |
| whole image | +770 LUT / +210 FF / -58 slices routed (gate tolerance +500 / +600 / +80) |

## 10. Open items and limitations

- The resource growth is recorded under the owner exception, not within policy: route +770 LUT over dev
  (tolerance 500), ooc-1x1 +462 (250), ooc-8x8 +2,185 LUT / +769 FF (316 / 339). The decision quotes the
  1x1 figures; the 8x8 figure is stated in the record note, the findings section and REVIEW READY.
- The image build ran with `--vivado-max-threads` 2 and 1 instead of the launcher's 32 (section 5).
- Processor PR #194's #190 "part 2" (the CRF slot's own MaxFrameSize) is not in this lane; closing
  processor #190 after merge leaves it open.
- Two parent RTL comments describe the pre-#85 PathTrace count (`KL_gptp_shadow.sv:635-638`,
  `milan_datapath.sv:2152-2157`); the logic is count-agnostic; editing them would change measured inputs.
- #770's content is not in this lane.
- Not done by rule: push, PR, merge, hardware, bench, flashing.

## Environment

- Verilator 5.050 (`$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`, exported as `VERILATOR`).
- GNU Make 4.3, built from `make-4.3.tar.gz` (sha256 `e05fdde4...6c78e19`, verified) into lane scratch;
  binary sha256 `8e62c6e9...64d9`.
- sv2v 0.0.12 (pinned release), Yosys 0.66 (`86f2ddeb`, the workflows' `YOSYS_VERSION` build).
- RV32 SDK: `scripts/ci_rv32_sdk.py` installed and verified `riscv32-ilp32d--glibc--stable-2025.08-1`
  (archive sha256 `d42680e9...b78f`, gcc 14.3.0) into lane scratch.
- tsn-gen field oracle: `https://github.com/kebag-logic/tsn-gen.git` at `rtl.yml`'s `TSN_GEN_REV`
  `deca300c9eb4863fa13383b45ba6cb6fd0828671`, `external/rapidyaml` initialised, `packet_gen` built with the
  workflow's cmake commands into lane scratch (`TSN_GEN_ROOT`).
- LiteX: the bench venv's checkouts, `litex` `a1e1c365`, `liteeth` `276c9e37`, `migen` `4c2ae8df`,
  `litedram` `f9b75e03`, `litespi` `02d5a209`, `litei2c` `19417d61`, `pythondata-cpu-vexiiriscv`
  `15cfab52`; their local changes are the five `sw/litex/patches/` (checked with `git apply --reverse --check`).
- Vivado 2026.1 (Build 6511674), one instance at a time under `flock $VIVADO_LOCK`; no run
  started below 20 GB MemAvailable. Service memory peaks: recipe route 8.7 GB; image builds 12.13 GB
  (2 threads, end of synthesis), 10.43 and 10.87 GB (1 thread); sweep phase 7.81 GB anon / 12.67 GB current (page cache, reclaimed at the cap) while the sweep, the physical leg and the docs replica ran.
- Background jobs were started with `setsid`, not `nohup`: the sweep's cancellation self-test sends
  SIGHUP, which `nohup` makes ignored; the first sweep launch under `nohup` aborted in that self-test
  (`hard-HUP` timed out) before any suite ran, and was relaunched.
- Docs-step interpreter: a lane-scratch venv on CPython 3.12.3 (the runner's version), with the
  workflow's own pinned installs; Markdown gates with `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python`.
- Scratch outside the checkout and this directory: `$VALIDATION_STORAGE/scratch/a662` (tools, venv, scripts, logs,
  tsn-gen) and `$HOME/litex-milan/work/a662-771` (Vivado work: `m1` head, `dev`, `dev8`, `chain`, `gchain`,
  `gooc`, `img`), plus the three image builds `$HOME/litex-milan/work/build_ax7101_{eppo,asl,eto}_a662-771`.

## Work products in this directory

`HANDOFF.md`, `PR-BODY.md`; the eight supplied patches (unchanged); `docs-steps-receipts.json` (round 1,
`d664cf54`) and `docs-steps-final-receipts.json` and `docs-steps-final-leg1-litex-receipts.json` (final head `a97aea01`); gate verdicts `gate-head-*-vs-record.log`, `gate-dev-*-vs-record.log`,
`gate-head-*-vs-dev.log` (all three endpoints); printed records `record-*.json.log`; `image-builds.json`;
`yosys-run.out`; `sweep.out`, `sweep-env.txt`, `sweep-tally-per-suite.txt`, `sweep-log-digests.txt`, `physical-milan_dp_gptp.log`, `physical-tally.out`, `behave-summary.txt`, `xvlog-final.log`; `pp-shadow-1x1-chain.txt`, `gptp-shadow-1x1-*-minus-old.txt`,
`route-hierarchy-head-minus-dev.txt`; `attribution-run-log.txt`. Every file is under 200 KB.
