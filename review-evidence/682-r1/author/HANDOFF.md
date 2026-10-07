# Issue 682 author handoff

Role: [A554], executor. Reviewers: [R520] internal, [R521] external.
Status: **REVIEW READY** at `5428b044176f95248e6916dc00dd89c0df154078`.
Branch: `682-pp-pin-2ad2f845`; origin `https://github.com/kebag-logic/milan-fpga.git`.
This is author evidence, not a review verdict. No push, PR creation or hardware operation was performed.

## Round 2

Authority: [original assignment](https://github.com/kebag-logic/milan-fpga/issues/682#issuecomment-6018127147) and [round-2 ruling](https://github.com/kebag-logic/milan-fpga/issues/682#issuecomment-6028334443).

### Ordered result and final integration

1. Merged dev `79b086d44eb62d007d38e18f5618b98e8e2a33e6` with `--no-ff` as `4d2538809d739d97c09f3f0bee194fb14e1cec18`. Changed resource inputs were remeasured and recorded as combination F in `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. The AAF packetizer is the tracked input change; fresh export hierarchy-comment ordering also changes raw digests, while its non-comment RTL and ROM contents match. `round2-fresh-input-proof.json` accounts for the differences. Recipes and generated records repeat byte-identically, with unchanged policies. Capture provenance passed with unchanged source digest.
2. The complete render differential passed at parent `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. Each full campaign completed **28/32**, raw make rc 2. All 32 actual leg outcomes, assertion text and count fields match. Both actual clean-epoch outputs are 3,746 bytes with SHA-256 `3ef42e34ca3874e90fd2929f869dd0f37343e04b9cb2cb0c5f294262448c1c6b`. Four fresh diagnostics at each pin corroborate the actual full campaigns. The prior variation changed only the gitlink and reversed the two supplied patches. The adopted tree was restored exactly. `round2-render-differential.json` records the verifier result; neither full campaign was cancelled.
3. All three routes passed every declared timing corner. ExtraPostPlacementOpt is selected and completed bitstream generation, bound manifest regeneration and complete offline image preflight. The parent-bank results and the final full sweep are distinguished below from the earlier failed sweep.
4. Acceptance 4 render result is **"unchanged from dev; #657"**, under the ruling and differential above. #657 retains its own acceptance; this exception does not waive other gates. Acceptance 5 remains the manager's post-merge #608 withdrawal cycles, #658 default-map check and stream/counter soak.

After image completion, dev `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c` was merged with `--no-ff` as `5af03224117ffef089d5031e9bb7e8b348d7abbf`. Its conflict-free tree exactly matched an independent `git merge-tree` result. Commit `591a5752e6a587b28b501e2d02d6a9d0293f3ba2` refreshes only the generated port-census header for dev's two new mailbox ports; both generator runs are identical and the port-contract and naming ratchets stay unchanged. Naming remains byte-identical. No processor or firmware source was edited by this lane.

The final authorized `--no-ff` merge takes dev `e21c1ca024d37ea188ad15b5c8f9c2dae18628df` as `5428b044176f95248e6916dc00dd89c0df154078`. It is conflict-free and exactly matches an independent merge-tree calculation. `round2-refresh-merge.json` records the merge; `round2-refresh-source-closure.json` names its 24 changed paths and eleven unchanged dependency scopes. These are imported MAAP control-firmware changes, their documentation, and the mailbox build recipe. No processor source or parent/processor interface was changed by this lane.

The completed 60-suite sweep remains evidence at its actual head `591a5752`; the changed mailbox suite, complete control-firmware campaign, combined coverage, builder and documentation gates passed fresh runs at the final merge head. Resource and capture provenance passed again there. The field campaigns passed a separate complete rerun with 899 checks and no skips after their external tsn-gen directory disappeared during the sweep. The old Make/SDK temporary prefixes and the cited Make recipe later disappeared as well: `round2-tool-prefix-recovery.json` records a real GNU Make 4.3 source build and the repository-verified pinned SDK under this lane's scratch directory. No documentation gate ran with the fallback Make 4.4.1; that version appears only on the Python-only record-repeatability receipt before restoration, followed by another identical repeated generation under the restored GNU Make 4.3.

`round2-final-merge-closure.json` records all changed paths since the measurement head and compares exact tree objects. Processor and other dependency pins, the actual render source list and its harness/recipes, all parent HDL headers, builder and shipping image sources, configurations, constraints, synthesis inputs and saved-capture sources are unchanged. Changed mailbox and control-firmware consumers receive fresh validation at the integration heads recorded below. All three retained resource records still match their exact final-tree input digests. Earlier evidence is retained only for unchanged dependency scopes, not merely because filenames in the adoption diff did not overlap.

### Pin and patch mapping

Processor gitlink: `ead8036035affd53ef4b29979190f2f4f67084c0` -> `2ad2f845dd583f8310075fa2380cb60a04fd091a`. The assigned upstream commit is public. The processor top is byte-identical at both pins: 237,956 bytes, SHA-256 `84d89afb652b3db646fd86a13e301c9de89005607b9d8fa896eb38f365a0e170`. Every explicit command within the processor is preceded by verification of its physical top-level directory.

| Patch | Parent hunk | Processor change answered |
|---|---|---|
| `parent-adoption-148-6c22d3ca.patch` | `tb/verilator/milan_dp/sim_nxn.cpp:964`, comment and loop at line 973 | PR 159 moves the counter-notification spacing stamp from selection toward each job send. The later frame can cross a 10 ms observation boundary; the harness now completes an in-progress frame for at most 2,048 additional cycles. |
| `parent-adoption-22-28f9666f.patch` | `scripts/xvlog.budget:33` | PR 162 moves existing declarations before use in the originator and RX validator. The two retired finding identities leave the processor section empty. |

Both patches applied without context repair. No expectation, parent RTL, firmware or interface was edited.

### Parent-visible list

| Processor PR | Parent-visible result |
|---|---|
| [156](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/156), C11 | Documentation now describes the landed byte interfaces, TX backpressure, synchronous reset and whole FCS-good RX frames. Parameter/timing ID and figure checks strengthen donor documentation validation. No interface change. |
| [159](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/159), 148 | GET_COUNTERS spacing follows every waiting job through grant; supplied frame-completion harness patch is required. No port, parameter or register change. MAC stalls after grant remain a disclosed wire-spacing limit. |
| [160](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/160), 134 | Registrar expiry followed by same-cycle reception preserves expiry for Lv/LeaveAll and renewal for New/Join. No parent interface change; manager repeats withdrawal cycles after merge. |
| [161](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/161), 158 | A held DEREGISTER waits for the notification round boundary, preserving later jobs. Its target and contents stay the same; delivery may be later. No port, parameter or register change. |
| [162](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/162), 22 | Declaration ordering only; supplied parent budget patch removes two findings. Synthesis warning count remains this adoption's obligation. |
| [164](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/164), 42 | Test-only Domain/link notification coverage; the parent continues to own the GET_AVB_INFO mapping words. No RTL, port, parameter or register change. |

The six PR bodies were read from public state. No private transcript was used.

### Every re-recorded record

| Record | Regeneration and result |
|---|---|
| `syn/yosys/rom_digests.tsv:15` | `bash syn/yosys/ooc.sh --record-rom-digests`; two new pin rows, unchanged ROM contents |
| `docs/reference/SUBMODULES.md:25` | Repository index pin reader plus existing parsed table metadata; processor pin updated |
| `docs/diagrams/submodule_boundaries.drawio`, `.svg`, `.png` and `PNG_MANIFEST.json` | `python3 docs/diagrams/submodule_boundaries.gen.py`; diagram pin and raster digest updated |
| `scripts/port_docs.budget:21` | `python3 scripts/check_port_contracts.py --write-budget`; census header refreshed, identities unchanged |
| `syn/ooc/pp_resource_baseline.json` | `python3 syn/ooc/pp_resource_gate.py record <report-directory> --endpoint <route-1x1, ooc-1x1 or ooc-8x8> --write`; combination F: all three repeated records are identical, with unchanged policies |
| Naming budget | `python3 scripts/measure_naming.py --write-budget`; identical output |


The ROM contents stay unchanged: LTN SHA-256 `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956`; microcode SHA-256 `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8`. Two new ledger rows bind them to the new pin. There is no dedicated pin-page writer; its table was derived using the repository's `gitlink_pins()` index reader and parsed table metadata. The diagram raster was visually checked. The adoption refreshed the parent census from 1,940 to 2,077 ports; the final dev merge adds two mailbox ports, so the final generated census is 2,079; processor count 1,759 and the port-contract ratchets are unchanged. Naming remains byte-identical at 95 identities. `round2-candidate-records.json` binds all 16 changed parent files and the gitlink to the final head. `current-records.json` is retained as the Round 1 ledger.

The final dev census refresh is in `round2-final-generated-records.json`. Resource documentation was updated in `docs/design/AREA_BUDGET.md`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` and its index. The opt-in single-worker synthesis flow, recipe documentation and its controls were committed in Round 1; default output remains byte-identical. Combination E remains historical and combination F is current. The flow change prevents attributing old-to-new resource deltas solely to the pin.

### Resource baseline F and capture

| Endpoint | LUT | FF | Slice | RAMB36 / RAMB18 | BRAM tiles | DSP | CARRY4 | WNS / WHS, ns |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Routed 1x1 image | 49,957 | 54,274 | 15,734 | 74 / 27 | 87.5 | 14 | 3,385 | +0.124 / +0.031 |
| Standalone 1x1 | 23,179 | 19,779 | n/a | 16 / 3 | 17.5 | 8 | 1,494 | -3.562 / +0.159 |
| Standalone 8x8 | 30,135 | 27,380 | n/a | 21 / 5 | 23.5 | 8 | 1,889 | -2.278 / +0.159 |

Standalone timing is an ungated synthesis estimate. The selected routed image has 116 free slices; its processor wrapper is 23,128 LUT / 18,790 FF and enclosing datapath is 41,394 LUT / 43,045 FF. The separate 60% LUT area objective remains unmet. All three synthesis logs contain **zero processor Synth 8-6901 findings across 46 directly read files**; the per-file table is in the resource evidence. Each retains one known parent `crft_emit_en_w` warning. No Synth 8-4445 or 8-7186 is emitted. This supports `Closes Mister-M-alt/protocol-processor-control-plane-avb-milan#22` without claiming the parent warning disappeared.

Exact inputs: routed `fe05182f7b303a175afa44006cd6098d34b8887b3b9296aaffda9415ea928b63`; standalone 1x1 `949b816238370a52d9b9aa89c7d77e004c7d019479e88085172ddf793fc3fe7a`; standalone 8x8 `53980010e27e5caca27d026414fab6ee7db387b3adeaddb6433d74d8339cffa5`.

Capture source SHA-256 remains `a73ecc25c77bfb7c4e1c2c711d72f0b560dd7e8d18cde92f40e67efcc84f0eb3`. `scripts/check_nvm_capture.py` passes. Retained measurements: 1x1 at 50 MHz 3.96728 ms; 8x8 at 50 MHz **13.86484 ms <= 24.5 ms**; 8x8 at 100 MHz 10.42973 ms. No firmware-source change required remeasurement.

### Three directives and complete selected image

All route processes returned zero, all routable nets are routed, and routing errors are zero. Values below are ns.

| Directive | Slow 0/85 C WNS / WHS | Fast 0/85 C WNS / WHS | TNS / THS, all corners |
|---|---:|---:|---:|
| ExtraPostPlacementOpt | +0.124 / +0.059 | +1.246 / +0.031 | 0 / 0 |
| AltSpreadLogic_high | +0.090 / +0.040 | +1.642 / +0.011 | 0 / 0 |
| ExtraTimingOpt | +0.055 / +0.057 | +1.588 / +0.020 | 0 / 0 |

The commercial release range is 0 to 85 C. Slow and Fast are fixed speed-file models, repeated at the two power-temperature endpoints; these are not four interpolated timing models. Speed file: `-2 PRODUCTION 1.23 2018-06-13`. Vivado 2026.1 build 6511674; part `xc7a100tfgg484-2`. Every corner satisfies WNS >= +0.03 ns and WHS >= 0. The alternatives remain route results; only the selected default is claimed as a complete image, as required by the round-2 assignment.

The selected route's 101,190 nets are fully routed. Its bitstream is **3,825,992 bytes**, SHA-256 `613a670a15dc7dce29c9cce0a1fc75527229575f7b43968dce6a444ffc80a8bc`; payload SHA-256 `ebc849027a5cc58394cc62dbf08995671b27f3039139c30d828c455ca416875b`. The bound manifest is 616 bytes, SHA-256 `bb3ddd51685a6b8aec8b89d06ee52d6ff030a669ed4caaf046c6630e30d45774`; two repository-generator runs produce identical bytes. The AEM image is 7,512 bytes, SHA-256 `4fc8d61582a965fe648abc0c15d0551153ff2b27f202d1fbc8319fbb4bdb396d`, within its 64 KiB slot at 4 MiB. The bitstream fits its 4 MiB slot. Owner is fabric and CPU XLEN is 32.

`round2-complete-image-evidence.json` binds the routed checkpoint, original recipe, unchanged shipping completion hook, bitstream, manifest, AEM and all reports. The generated bare-metal schema contains `complete:false` by design at `sw/litex/layout_from_soch.py:156`; acceptance is the successful complete-target preflight, not that schema field. The unchanged `do_check_images` and `materialize_images` functions were invoked without the deployment wrapper's hardware setup. They validate and materialize the entire target set. No hardware was accessed.

The selected implementation emits no CRITICAL WARNING and all stages pass the rejected-constraint reader. Both alternative logs retain a Route 35-39 warning before their final post-route optimization (original lines 3145 and 3381); final corner reports pass. `round2-signoff-details.json` retains the warning census, source locations, all four slack metrics, clock interactions, CDC, unconstrained reports and worst-path evidence. All four Ethernet pairs meet their 8 ns datapath-only bound with no unsafe pair. The selected image still reports 46 missing input-delay and 87 missing output-delay entries, and ten CDC-10 critical diagnostics. Zero no-clock, unconstrained-internal-endpoint and loop entries does not waive those disclosed limits or establish physical compliance.

### Validation result and retained qualifications

At final committed head `5428b044176f95248e6916dc00dd89c0df154078`, all affected validation returned **rc 0**: **49/49 literal documentation steps under GNU Make 4.3**; the complete control-firmware campaign with native/release/debug RV32 checks and **196/196 mutants caught**; SDK, object and tally controls; combined coverage **PASS for 17 files** (100% after documented exclusions); the mailbox suite and verdict reader; builder elaboration with required RV32; six resource/capture checks; and four Markdown gates using the specified interpreter. Port and naming generators reproduce the committed records twice under GNU Make 4.3. All 54 private tracked inputs match the final commit byte for byte.

The uninterrupted full parent sweep completed at ancestor `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`: **60/60 suites, driver rc 0, tally rc 0, 2,184,926 counted checks, zero in-suite failures**. Its four explicit tsn-gen field/freshness skips remain in that original log. They are covered by the separate final-head full field rerun: **899 checks, zero failures, zero skips**, including 164 AAF checks, 677 gPTP checks, grader/traceability controls and both report-freshness checks. The changed mailbox suite also passes again at the final head. `round2-refresh-source-closure.json` proves that the remaining suite inputs are unchanged; the earlier sweep is not relabelled as a run at the later head.

Retained exact-input evidence at `591a5752` includes 58/58 Yosys units, two structural gates, three top elaborations and their controls; BDD 14 features / 404 scenarios / 1,968 steps; native NVM **435 tests across five shapes and 109/109 mutants caught**; and vendor syntax **zero findings across 81 parent and 52 pinned-processor sources**, rc 0. The two integration audits bind retained processor, gPTP, physical-cadence, NVM quick/lint, LiteX, render and image results to unchanged final inputs. All three resource input digests and the capture source digest still match exactly. The selected bitstream and manifest pass the complete offline image preflight, and all 185 retained image/resource artifacts still match their recorded hashes (`round2-artifact-retention.json`).

The host builder's two documented NOTRUN arms remain outside its verdict: the ineffective MAKEFLAGS mutation under Make 4.3 and the absent historical calibration report. The earlier 59/60 sweep and its unresolved lifecycle cause remain disclosed as historical failed evidence; the accepted complete repeat passed. The render exception is exactly **"unchanged from dev; #657"**, supported by the manager ruling and completed differential. Hardware acceptance 5, publication, hosted checks and independent reviews remain pending; no push or hardware action was performed.

Unchanged-scope evidence includes 33 processor suites / 1,028,250 checks; gPTP contract/tests/lint; physical-cadence gPTP with 139 main and 40 failure-path checks; NVM lint and the isolated 315/315 quick check over 62 cases; LiteX driver controls and all four simulations (CPU-memory CDC, gPTP TX timestamp, processor boot freeze, processor memory bridge). The physical-cadence main run covered 849,627,826 cycles / 16.992556520 simulated seconds. Its explicit non-covered hardware/protocol arms remain disclosed in the log. The host builder retains two NOTRUN arms: the ineffective MAKEFLAGS mutation under Make 4.3 and the absent historical calibration report.

The complete sweep at `591a5752` records four explicit tsn-gen campaign/freshness skips because its external dependency directory disappeared during execution. `round2-field-oracle-recovery.json` records verified pinned source exports and the separately rerun field-campaign result; no skipped arm is counted as passing evidence.

The first round-2 sweep completed without cancellation at **59/60**, driver rc 1, with only `gptp_shadow` failing. The tally's rc 0 and 2,184,412 checks with zero in-suite assertion failures did not clear that driver result. The failure was nested-SIGTERM cleanup at `test_mutant_lifecycle.py:387`, after functional mutation controls passed. A direct diagnostic failed differently at line 149; the exact Make lifecycle target then passed. The cause remains unknown, and no source or expectation was weakened. `round2-original-sweep-evidence.json` and `round2-lifecycle-incident.json` retain all results. The final complete sweep is separate evidence. Its gPTP-shadow suite passed all nine functional controls and the complete lifecycle target, including nested SIGINT/SIGTERM cleanup; `round2-gptp-shadow-final-repeat.json` records the successful log and does not claim a root cause or code fix.

The first NVM quick check shared scenario outputs with the original full sweep and is not accepted despite raw rc 0. Its replacement isolated both builds and scenario outputs and passed. The final full sweep has no concurrent quick campaign. The initial adopted render launch selected conflicting Make versions and failed before any case; the corrected full campaign explicitly used 4.3. Prior fresh diagnostics initially did not start because of Git index-lock contention; a later coordinator check was also called too early. These startup errors are retained separately. After correct sequencing, the missing diagnostics, exact restoration and unchanged differential verifier passed. Neither full render campaign was cancelled. An alternative-route lock waiter was withdrawn only while unstarted; its rc 143 is scheduling evidence, not a route result.

### Gate table and resource discipline

Every row gives the actual committed head, Make version and raw rc. Earlier failed or qualified receipts remain visible and are not counted as final passes. `ROUND2-GATE-COMMANDS.md` and `round2-gate-receipts.json` add exact commands, physical working directories, timestamps, byte sizes and log digests. The literal hosted documentation steps each run under GNU Make 4.3. Standalone Markdown gates use `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python`. Verilator is pinned to 5.050; at most two builds overlap, with make -j8 and VERILATOR_JOBS=2, and campaign worker limits at four or fewer.

| Gate | Head | Make version | rc |
|---|---|---|---:|
| builder 01: builder-elaboration | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| final-builder 01: builder-elaboration | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-contract 01: bdd | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-firmware 01: sdk-controls | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-firmware 02: rv32-object-controls | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-firmware 03: firmware-tally-controls | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-firmware 04: firmware-ctrl | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-firmware 05: firmware-nvm | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-firmware 06: firmware-coverage-controls | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-firmware 07: firmware-coverage | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-markdown 01: markdown-docs | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-markdown 02: markdown-toc-controls | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-markdown 03: markdown-anchor-check | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-markdown 04: markdown-toc-check | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-resources 01: route-1x1 | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-resources 02: ooc-1x1 | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-resources 03: ooc-8x8 | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-resources 04: resource-policy | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-resources 05: capture-receipt | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-resources 06: exact-resource-inputs | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-sweep 01: parent-sweep | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-sweep 02: parent-tally | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-synthesis 01: lint | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-synthesis 02: pp-sources | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-synthesis 03: scope | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-synthesis 04: yosys | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-synthesis 05: yosys-tally | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-synthesis 06: fast-elaboration | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-synthesis 07: dp-source-controls | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-synthesis 08: ooc-tcl-controls | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-synthesis 09: baseline-controls | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-synthesis 10: baseline-mutants | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-synthesis 11: baseline-reports | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-synthesis 12: resource-controls | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-synthesis 13: resource-mutants | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-synthesis 14: resource-baseline | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-synthesis 15: dp-sources | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-synthesis 16: yosys-ooc-controls | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-synthesis 17: yosys-cache-controls | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-vendor 01: xvlog | `591a5752e6a5` | GNU Make 4.3 | 0 |
| firmware 01: firmware-tally-controls | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| firmware 02: firmware-ctrl | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| firmware 03: firmware-nvm | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| firmware 04: firmware-coverage-controls | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| firmware 05: firmware-coverage | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| images 01: ExtraPostPlacementOpt | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| lifecycle-diagnostic 01: gptp-lifecycle-recheck | `342f20ef1fb2` | GNU Make 4.3 | 1 |
| lifecycle-make-diagnostic 01: gptp-lifecycle-make-recheck | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| markdown 01: markdown-docs | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| markdown 02: markdown-toc-controls | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| markdown 03: markdown-anchor-check | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| markdown 04: markdown-toc-check | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| nvm-isolated-check 01: nvm-quick-isolated | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| parent 01: physical-gptp | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| parent 02: nvm-lint | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| parent 03: nvm-quick | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| parent 04: litex-driver-controls | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| parent 05: litex-sims | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| processors 01: processor-sweep | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| processors 02: gptp | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| processors 03: bdd | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| refresh-builder 01: builder-elaboration | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-field 01: oracle-configure | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-field 02: oracle-build | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-field 03: tsn-fuzz | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-field 04: tsn-verdict | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-field 05: field-completeness | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-firmware 01: sdk-controls | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-firmware 02: rv32-object-controls | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-firmware 03: firmware-tally-controls | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-firmware 04: firmware-ctrl | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-firmware 05: firmware-coverage-controls | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-firmware 06: firmware-coverage | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-mailbox 01: mbx | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-mailbox 02: mbx-verdict | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-markdown 01: markdown-docs | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-markdown 02: markdown-toc-controls | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-markdown 03: markdown-anchor-check | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-markdown 04: markdown-toc-check | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-records 01: generated-record-repeatability | `5428b044176f` | GNU Make 4.4.1 | 0 |
| refresh-records-final 01: generated-record-repeatability | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-resources 01: route-1x1 | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-resources 02: ooc-1x1 | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-resources 03: ooc-8x8 | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-resources 04: resource-policy | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-resources 05: capture-receipt | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-resources 06: exact-resource-inputs | `5428b044176f` | GNU Make 4.3 | 0 |
| resources 01: route-1x1 | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| resources 02: ooc-1x1 | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| resources 03: ooc-8x8 | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| resources 04: resource-policy | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| resources 05: capture-receipt | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| resources 06: exact-resource-inputs | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| sweep 01: parent-sweep | `342f20ef1fb2` | GNU Make 4.3 | 1 |
| sweep 02: parent-tally | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| synthesis 01: lint | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| synthesis 02: pp-sources | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| synthesis 03: scope | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| synthesis 04: yosys | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| synthesis 05: yosys-tally | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| synthesis 06: fast-elaboration | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| synthesis 07: dp-source-controls | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| synthesis 08: ooc-tcl-controls | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| synthesis 09: baseline-controls | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| synthesis 10: baseline-mutants | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| synthesis 11: baseline-reports | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| synthesis 12: resource-controls | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| synthesis 13: resource-mutants | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| synthesis 14: resource-baseline | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| synthesis 15: dp-sources | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| synthesis 16: yosys-ooc-controls | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| synthesis 17: yosys-cache-controls | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| vendor 01: xvlog | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 01: Build the validated HDL reference | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 02: Install the python gate dependencies | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 03: Install the pinned Markdown renderer | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 04: Install diagram gate dependencies | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 05: Link health, wording, dead-reference and local-info gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 06: Added-line em-dash gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 07: Concise audience documentation gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 08: Audience diagram no-drift gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 09: Product solution source-fact gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 10: Verified submodule documentation gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 11: HDL timing diagram no-drift gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 12: Published diagram PNG gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 13: Milan feature-status consistency gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 14: Traceability matrix no-drift gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 15: Fetch the builder source dependencies | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 16: Imported gPTP documentation gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 17: Code-quality measurement self-tests | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 18: Install the pinned sv2v release | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 19: Bare-metal scope gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 20: Install and verify the pinned RV32 SDK | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 21: Compiler-absent firmware controls | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 22: End-station builder gates | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 23: NVM record-space gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 24: Capture measurement census and clock gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 25: Saved-state writer gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 26: SoC source-list gate (Vivado would fail 40 min in without this) | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 27: RTL source-list drift gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 28: Boundary-unit naming ratchet | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 29: Port contract gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 30: Fail-fast ratchet | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 31: TODO ownership gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 32: Test-evidence ratchet | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 33: Mechanical hygiene ratchet | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 34: SystemVerilog idiom gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 35: C and C++ idiom gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 36: Python idiom gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 37: Shell idiom gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 38: CI event and SHA contract gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 39: Local act runner contract gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 40: Doc cited-path gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 41: Archive integrity gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 42: Per-page contents gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 43: AEM store generator self-test | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 44: Sweep/build shape gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 45: Deploy shape gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 46: Entity shape gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 47: Fetch the engine authority the builder derives from | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 48: Advertised-vs-emitted gate (green since 2026-07-28, item 00) | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| docs-workflow 49: Strip git metadata, then run the docs gate | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| render 01: adopted-full | `342f20ef1fb2` | GNU Make 4.3 | 2 |
| render 02: adopted-cases | `342f20ef1fb2` | GNU Make 4.3 | 1 |
| render 03: prior-full | `342f20ef1fb2` | GNU Make 4.3 | 2 |
| render 04: prior-cases | `342f20ef1fb2` | GNU Make 4.3 | 1 |
| render 05: differential | `342f20ef1fb2` | GNU Make 4.3 | 0 |
| final-docs-workflow 01: Build the validated HDL reference | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 02: Install the python gate dependencies | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 03: Install the pinned Markdown renderer | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 04: Install diagram gate dependencies | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 05: Link health, wording, dead-reference and local-info gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 06: Added-line em-dash gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 07: Concise audience documentation gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 08: Audience diagram no-drift gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 09: Product solution source-fact gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 10: Verified submodule documentation gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 11: HDL timing diagram no-drift gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 12: Published diagram PNG gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 13: Milan feature-status consistency gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 14: Traceability matrix no-drift gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 15: Fetch the builder source dependencies | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 16: Imported gPTP documentation gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 17: Code-quality measurement self-tests | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 18: Install the pinned sv2v release | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 19: Bare-metal scope gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 20: Install and verify the pinned RV32 SDK | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 21: Compiler-absent firmware controls | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 22: End-station builder gates | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 23: NVM record-space gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 24: Capture measurement census and clock gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 25: Saved-state writer gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 26: SoC source-list gate (Vivado would fail 40 min in without this) | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 27: RTL source-list drift gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 28: Boundary-unit naming ratchet | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 29: Port contract gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 30: Fail-fast ratchet | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 31: TODO ownership gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 32: Test-evidence ratchet | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 33: Mechanical hygiene ratchet | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 34: SystemVerilog idiom gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 35: C and C++ idiom gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 36: Python idiom gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 37: Shell idiom gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 38: CI event and SHA contract gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 39: Local act runner contract gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 40: Doc cited-path gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 41: Archive integrity gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 42: Per-page contents gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 43: AEM store generator self-test | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 44: Sweep/build shape gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 45: Deploy shape gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 46: Entity shape gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 47: Fetch the engine authority the builder derives from | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 48: Advertised-vs-emitted gate (green since 2026-07-28, item 00) | `591a5752e6a5` | GNU Make 4.3 | 0 |
| final-docs-workflow 49: Strip git metadata, then run the docs gate | `591a5752e6a5` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 01: Build the validated HDL reference | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 02: Install the python gate dependencies | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 03: Install the pinned Markdown renderer | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 04: Install diagram gate dependencies | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 05: Link health, wording, dead-reference and local-info gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 06: Added-line em-dash gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 07: Concise audience documentation gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 08: Audience diagram no-drift gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 09: Product solution source-fact gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 10: Verified submodule documentation gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 11: HDL timing diagram no-drift gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 12: Published diagram PNG gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 13: Milan feature-status consistency gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 14: Traceability matrix no-drift gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 15: Fetch the builder source dependencies | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 16: Imported gPTP documentation gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 17: Code-quality measurement self-tests | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 18: Install the pinned sv2v release | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 19: Bare-metal scope gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 20: Install and verify the pinned RV32 SDK | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 21: Compiler-absent firmware controls | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 22: End-station builder gates | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 23: NVM record-space gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 24: Capture measurement census and clock gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 25: Saved-state writer gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 26: SoC source-list gate (Vivado would fail 40 min in without this) | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 27: RTL source-list drift gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 28: Boundary-unit naming ratchet | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 29: Port contract gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 30: Fail-fast ratchet | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 31: TODO ownership gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 32: Test-evidence ratchet | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 33: Mechanical hygiene ratchet | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 34: SystemVerilog idiom gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 35: C and C++ idiom gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 36: Python idiom gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 37: Shell idiom gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 38: CI event and SHA contract gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 39: Local act runner contract gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 40: Doc cited-path gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 41: Archive integrity gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 42: Per-page contents gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 43: AEM store generator self-test | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 44: Sweep/build shape gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 45: Deploy shape gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 46: Entity shape gate | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 47: Fetch the engine authority the builder derives from | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 48: Advertised-vs-emitted gate (green since 2026-07-28, item 00) | `5428b044176f` | GNU Make 4.3 | 0 |
| refresh-docs-workflow 49: Strip git metadata, then run the docs gate | `5428b044176f` | GNU Make 4.3 | 0 |

MemoryCurrent is checked against 9,000,000,000 bytes. The isolated image-stage guard observed at most 8,000,057,344 bytes and restored the normal 7 GiB pressure threshold; historical unit peak is 8,988,643,328 bytes with zero OOM events. Final concurrent validation uses 6 GiB pressure control with a 2 GiB documentation container, restoring 7 GiB afterward. Every Vivado invocation holds `$VIVADO_LOCK`, and no heavy build in this lane overlaps it. The `/data` free-space floor is 30 GB. Completed compiler intermediates were removed with retained receipts; sources, logs, executables and image inputs were preserved. Toolchains, SDKs, exports and large artifacts stay outside this packet; only their sizes and digests are recorded. The final NVM campaign accumulated memory-backed temporary ELF artifacts. After the driver removed each completed mutation source tree, 5,044 finished ELF files (6,136,887,976 bytes) were moved to disk with identical hashes and original paths preserved by links; active cases, source files, expectations and logs were untouched. `round2-final-nvm-storage.json` records the completed operation and the size/digest of its full per-file ledger, which remains outside this packet. No campaign was interrupted. After the NVM campaign passed and its driver removed the original scratch directory, all 5,044 disk copies were checked against the ledger again and retired, releasing 6.14 GB. `round2-final-nvm-storage-cleanup.json` records that cleanup.

Publication, hosted checks, independent reviews, reviewer-owned lens coverage, candidate-merge validation, post-merge containment and manager hardware acceptance remain separate obligations. The author does not approve or merge this lane.

## Round 1

The following original handoff is preserved as historical evidence at its stated head. Its STOP and incomplete work do not describe the current round.


The following evidence belongs to the previous head and is retained as history; it is not round-2 validation.

# Issue 682 author handoff

Role: [A554], executor. Reviewers: [R520] internal, [R521] external.
Status: STOP / blocked at `1e99ad217f0747c33e03238f7d1c633c07ce572c`. Items 1-5 are complete. Full acceptance fails the render campaign at 28/32 (rc 2); fresh builds reproduce all four failed cases with committed inputs stable. Issue #682 has no exception for open #657. The worktree and processor checkout are clean; six one-line commits are retained locally. No review-ready claim is made.
Public STOP: https://github.com/kebag-logic/milan-fpga/issues/682#issuecomment-6028310880
Branch: `682-pp-pin-2ad2f845`.
Base: `bd884631684ccf5060339efa92263d5c3e5c262c`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/682#issuecomment-6018127147
The explicit assignment authorizes execution; the board still shows Backlog.

## Ordered status

1. Pin complete. Only the processor gitlink changes, from `ead8036035affd53ef4b29979190f2f4f67084c0` to `2ad2f845dd583f8310075fa2380cb60a04fd091a`. It was fetched from the assigned public upstream and checked out detached after verifying the submodule's top-level directory. The processor top is byte-identical at both pins: 237,956 bytes, SHA-256 `84d89afb652b3db646fd86a13e301c9de89005607b9d8fa896eb38f365a0e170`.
2. Both supplied patches applied without context repair. The initial xvlog check returned zero with no finding in 81 parent, 46 protocol-processor and six gPTP files. The final-head repeat also returns zero with no findings.
3. Pin-derived records regenerated and repeated byte-identically. Test-evidence dispositions are unchanged: 72/77 no-mutant, 10/10 unseeded, zero unexplained readers, three wall-clock cases, 60 default suites and 99 inventory entries.
4. Combination E recorded through the repository generator. Both standalone syntheses and the clean image synthesis and implementation have successful process receipts. All three endpoint checks and the policy check return zero at the committed head. Policies are unchanged.
5. Saved capture receipt passes at the committed head. Firmware source digest is unchanged, so remeasurement is not required.
6. Blocked. The full render mutation campaign returns rc 2, 28/32, matching #657. A fresh unmodified epoch build reproduces four T30 CRF failures with committed inputs stable. The supplied notification patch passes its direct 421-check target. The broad parent sweep was then cancelled through its repository process owner after 10/60 suites passed; rc 143 is a cancellation, not a gate result. The remaining parent bank steps and section 5 bitstream/manifest completion were not started. All three routes completed with rc 0 and fully routed, error-free nets; ExtraTimingOpt passes the numerical slack floor at every corner, but route-only checkpoints do not qualify complete images.
7. Remote dev is `79b086d44eb62d007d38e18f5618b98e8e2a33e6`: 32 commits beyond the assigned base, with no overlapping changed paths. `dev-comparison.json` records the complete file list and fetch receipt. This execution request forbids merge and rebase, so item 7 remains with the manager. Incoming changes include `KL_aaf_packetizer.sv`, firmware/NVM sources and the suite driver: no-path-overlap is not validation. Integration must recheck resource input digests, apply the re-baseline rule where inputs changed, recheck the capture source digest and remeasure if required, and rerun affected gates.

## Patch hunk mapping

| Patch | Parent hunk | Processor change answered |
|---|---|---|
| `parent-adoption-148-6c22d3ca.patch` | `tb/verilator/milan_dp/sim_nxn.cpp:964`, comment and loop at line 973 | PR 159 moves the counter-notification spacing stamp from selection toward each job send. The later frame can cross a 10 ms observation boundary; the harness now completes an in-progress frame for at most 2,048 additional cycles. |
| `parent-adoption-22-28f9666f.patch` | `scripts/xvlog.budget:33` | PR 162 moves existing declarations before use in the originator and RX validator. The two retired finding identities leave the processor section empty. |

Both patches applied without context repair. No expectation, parent RTL, firmware or interface was edited.

## Parent-visible changes

| Processor PR | Parent-visible result |
|---|---|
| [156](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/156), C11 | Documentation now describes the landed byte interfaces, TX backpressure, synchronous reset and whole FCS-good RX frames. Parameter/timing ID and figure checks strengthen donor documentation validation. No interface change. |
| [159](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/159), 148 | GET_COUNTERS spacing follows every waiting job through grant; supplied frame-completion harness patch is required. No port, parameter or register change. MAC stalls after grant remain a disclosed wire-spacing limit. |
| [160](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/160), 134 | Registrar expiry followed by same-cycle reception preserves expiry for Lv/LeaveAll and renewal for New/Join. No parent interface change; manager repeats withdrawal cycles after merge. |
| [161](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/161), 158 | A held DEREGISTER waits for the notification round boundary, preserving later jobs. Its target and contents stay the same; delivery may be later. No port, parameter or register change. |
| [162](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/162), 22 | Declaration ordering only; supplied parent budget patch removes two findings. Synthesis warning count remains this adoption's obligation. |
| [164](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/164), 42 | Test-only Domain/link notification coverage; the parent continues to own the GET_AVB_INFO mapping words. No RTL, port, parameter or register change. |

The six PR bodies were read from public state. No private transcript was used.

## Pin-derived record map

| Record | Regeneration and result |
|---|---|
| `syn/yosys/rom_digests.tsv:15` | `bash syn/yosys/ooc.sh --record-rom-digests`; two new pin rows, unchanged ROM contents |
| `docs/reference/SUBMODULES.md:25` | Repository index pin reader plus existing parsed table metadata; processor pin updated |
| `docs/diagrams/submodule_boundaries.drawio`, `.svg`, `.png` and `PNG_MANIFEST.json` | `python3 docs/diagrams/submodule_boundaries.gen.py`; diagram pin and raster digest updated |
| `scripts/port_docs.budget:21` | `python3 scripts/check_port_contracts.py --write-budget`; census header refreshed, identities unchanged |
| `syn/ooc/pp_resource_baseline.json` | `python3 syn/ooc/pp_resource_gate.py record <report-directory> --endpoint <route-1x1, ooc-1x1 or ooc-8x8> --write`; all three repeated records are identical, with unchanged policies |
| Naming budget | `python3 scripts/measure_naming.py --write-budget`; identical output |


The ROM contents stay unchanged: LTN SHA-256 `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956`; microcode SHA-256 `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8`. Two new ledger rows bind them to the new pin. There is no dedicated pin-page writer; its table was derived using the repository's `gitlink_pins()` index reader and parsed table metadata. The diagram raster was visually checked. The port census header changes from 1,940 to 2,077 parent ports; processor count 1,759 and all ratchets are unchanged. Naming remains byte-identical at 95 identities. `current-records.json` binds all 16 changed parent files and the gitlink to the committed head.

## Resource baseline E

| Endpoint | LUT | FF | Slice | RAMB36 / RAMB18 | BRAM tiles | DSP | CARRY4 | WNS / WHS, ns |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Routed 1x1 image | 49,888 | 54,267 | 15,805 | 74 / 27 | 87.5 | 14 | 3,385 | +0.101 / +0.031 |
| Standalone 1x1 | 23,179 | 19,779 | n/a | 16 / 3 | 17.5 | 8 | 1,494 | -3.562 / +0.159 |
| Standalone 8x8 | 30,135 | 27,380 | n/a | 21 / 5 | 23.5 | 8 | 1,889 | -2.278 / +0.159 |

Standalone timing is an ungated synthesis estimate. Routed timing is the acceptance result. All 101,135 routable nets are routed with zero routing errors. The routed processor wrapper has 23,094 LUT and 18,784 FF; the enclosing datapath has 41,356 LUT and 43,038 FF. The device has 45 unused slices. LUT use is 78.69%; the separate 60% area objective remains unmet by 11,848 LUT and is still tracked by the existing redesign work.

The generated flow now records the opt-in `--single-thread-synthesis` setting (`set_param synth.maxThreads 1`). The default generated output remains byte-identical. The existing six-argument preparation interface is preserved. CLI controls and all 34 baseline mutants pass, including ignored-flag and default-on defects. This is a flow change, so comparison with baseline D correctly returns diagnostic rc 2, NOT COMPARABLE. Those diagnostics are not acceptance gates. The old and new numeric rows are preserved in the authoritative finding; the raw delta is not attributed solely to the processor pin because intervening parent changes and the synthesis worker setting also differ.

The clean measurement used unchanged RTL inputs from `2a97d4e8874a90a620d2b9234620eff9aec57bcb`. Final-head endpoint checks verify those same input digests at `1e99ad217f0747c33e03238f7d1c633c07ce572c`. `effective-recipes.json` records byte-identical regeneration and the shipping-export digests; `resource-recording-receipts.json` records each generator command, repeated recording and check. `resource-artifacts.json` records sizes and SHA-256 for the large reports, logs and checkpoints retained outside this packet.

### Synthesis declaration warnings

`synth-86901.md` and `synth-86901.json` report all 46 directly read protocol-processor design files, each with zero Synth 8-6901 warnings in clean image synthesis and both standalone runs. The 52-file pinned-source xvlog census consists of these 46 files plus six gPTP files. Each synthesis separately has one parent warning for `crft_emit_en_w` at `hdl/milan/milan_datapath.sv:3168`. Processor issue #22 therefore meets its zero-count closure condition; no globally warning-free claim is made. The PR 162 diff was also inspected manually: it only relocates bare logic declarations in the originator and RX validator; it does not replace a declaration initializer with a continuous assignment. No xelab gate is claimed.

## Capture check

`python3 scripts/check_nvm_capture.py` exits 0 at `1e99ad217f0747c33e03238f7d1c633c07ce572c`. The firmware source hash, harness hashes, census, clocks and both timing arms match the saved receipt. Maxima: 1x1 at 50 MHz 3.96728 ms; 8x8 at 50 MHz 13.86484 ms; 8x8 at 100 MHz 10.42973 ms. The 8x8 acceptance limit is 24.5 ms. This validates retained measurements; it is not a new simulator timing measurement.

## Three-directive timing

| Placement directive | Minimum WNS, ns | Minimum WHS, ns | Status |
|---|---:|---:|---|
| ExtraPostPlacementOpt | +0.101 | +0.031 | All corners pass |
| AltSpreadLogic_high | -0.857 | +0.008 | Setup fails; not selected |
| ExtraTimingOpt | +0.334 | +0.021 | Best; all corners pass |

Default Slow 0/85 C corners are +0.101 / +0.085 ns; Fast 0/85 C corners are +1.492 / +0.031 ns. AltSpreadLogic_high Slow corners are -0.857 / +0.102 ns; Fast corners are +1.326 / +0.008 ns. The default's worst setup path is the CPU DMA write bridge, 21 logic levels and 9.871 ns data delay. ExtraTimingOpt Slow 0/85 C corners are +0.334 / +0.056 ns; Fast 0/85 C corners are +1.633 / +0.021 ns. Its worst setup path runs from `milansoc_write_w_buffer_level0_reg[0]/C` to `storage_10_dat1_reg[20]/D`, with 14 logic levels and 9.296 ns data delay. AltSpreadLogic_high fails in the processor notify-to-transmit-arbiter cone (`wr_ix_r_reg[0]/C` to `slot_r_reg[1]/D`), with 42 levels and 20.907 ns data delay. `timing-directives.json` retains the five worst setup and two worst hold paths, all corner values, utilization and report digests for every directive. The resource baseline remains the prescribed ExtraPostPlacementOpt cell; it is distinct from selection of the best timing directive. The acceptance floor is best-directive WNS at least +0.03 ns and WHS at least zero at every corner.

The route-only records establish slack but do not yet qualify complete images under BUILDING.md section 5. The prepared continuation opens each final routed checkpoint, reuses the shipping-generated report and bitstream tail, and performs no synthesis or placement. Its unexecuted plan runs the repository constraint-log gate, generates the flash layout through `layout_from_soch.py`, and verifies the bitstream/AEM binding through `check_gptp_owner_pair.py`. No result is claimed for that plan. Existing compiled software and AEM bytes are retained and hashed.

The completed route reports have zero no-clock and unconstrained internal endpoints. They disclose 46 input ports with no input delay under false-path constraints and 87 output ports with no output delay. CDC diagnostics remain visible, including ten CDC-10 critical rows in the best directive; positive slack does not discharge them. All four Ethernet/system-Milan clock pairs carry an 8 ns Max Delay Datapath Only constraint with positive slack and no unsafe clock pair. No emitted 12-4739, 20-1307 or 12-5201 diagnostic occurs in any completed implementation. AltSpreadLogic_high emits Route 35-39 for its setup failure. The full critical-warning census and all four slack metrics per corner are retained in `signoff-details.json`. Slow/Fast use fixed speed models; the 0 C and 85 C power-temperature endpoint reports repeat those models rather than applying temperature interpolation.

## Gate table

All rows below belong to full head `1e99ad217f0747c33e03238f7d1c633c07ce572c`; each row displays its unambiguous prefix. There are 85 completed or cancelled command records: 82 return zero, the full render campaign returns 2, its fresh four-case diagnostic returns 1, and the deliberately cancelled parent sweep returns 143. Return zero is a process result, not a claim that intentionally unrun arms were covered.

The processor sweep passes 33 suites and 1,028,250 checks. The gPTP contract/tests/lint command passes. BDD passes 14 features, 404 scenarios and 1,968 steps with no skips. The focused notification target passes 421 checks. The original synthesis sweep reports 58/58 tops and both structural gates; its two shared-header consumers pass fresh repeats, followed by passing three-top elaboration. All 49 literal documentation workflow steps use GNU Make 4.3. The host builder returns zero with two unrun arms: the ineffective MAKEFLAGS mutation under this Make version and the absent historical calibration report. The documentation job’s restricted builder environment reports 16 unrun arms; its separate compiler-absent controls report three unrun arms by design. Installed-environment checks do not erase those recorded dispositions.

`GATE-COMMANDS.md` gives every exact shell command, working directory, full head, return code, log digest and size; `gate-receipts.json` is the structured equivalent. The capture receipt is recorded separately above. `partial-parent-sweep.json` and `acceptance-cancellation.json` preserve the 10 completed suites and cancellation. The complete-image plan, parent tally, physical-gPTP simulation, NVM lint/quick, LiteX driver controls and four LiteX simulations were not run after the blocker was confirmed.

| Gate | Head | Make version | rc |
|---|---|---|---:|
| markdown 01: markdown-docs | `1e99ad217f07` | GNU Make 4.3 | 0 |
| markdown 02: markdown-toc-controls | `1e99ad217f07` | GNU Make 4.3 | 0 |
| markdown 03: markdown-anchor-check | `1e99ad217f07` | GNU Make 4.3 | 0 |
| markdown 04: markdown-toc-check | `1e99ad217f07` | GNU Make 4.3 | 0 |
| parent 01: render-full | `1e99ad217f07` | GNU Make 4.3 | 2 |
| parent 02: parent-sweep-cancelled | `1e99ad217f07` | GNU Make 4.3 | 143 |
| patch 01: notification-patch | `1e99ad217f07` | GNU Make 4.3 | 0 |
| processors 01: processor-sweep | `1e99ad217f07` | GNU Make 4.3 | 0 |
| processors 02: gptp | `1e99ad217f07` | GNU Make 4.3 | 0 |
| processors 03: bdd | `1e99ad217f07` | GNU Make 4.3 | 0 |
| processors 04: builder-elaboration | `1e99ad217f07` | GNU Make 4.3 | 0 |
| resources 01: route-1x1 | `1e99ad217f07` | GNU Make 4.3 | 0 |
| resources 02: ooc-1x1 | `1e99ad217f07` | GNU Make 4.3 | 0 |
| resources 03: ooc-8x8 | `1e99ad217f07` | GNU Make 4.3 | 0 |
| resources 04: policy | `1e99ad217f07` | GNU Make 4.3 | 0 |
| stable-header 01: yosys-stable-header | `1e99ad217f07` | GNU Make 4.3 | 0 |
| stable-header 02: fast-elaboration-stable-header | `1e99ad217f07` | GNU Make 4.3 | 0 |
| stable-header 03: render-four-cases-stable-header | `1e99ad217f07` | GNU Make 4.3 | 1 |
| synthesis 01: lint | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 02: pp-sources | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 03: scope | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 04: yosys | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 05: yosys-tally | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 06: fast-elaboration | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 07: dp-source-controls | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 08: ooc-tcl-controls | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 09: baseline-controls | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 10: baseline-mutants | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 11: baseline-reports | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 12: resource-controls | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 13: resource-mutants | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 14: resource-baseline | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 15: dp-sources | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 16: yosys-ooc-controls | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 17: yosys-cache-controls | `1e99ad217f07` | GNU Make 4.3 | 0 |
| vendor 01: xvlog | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 01: Build the validated HDL reference | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 02: Install the python gate dependencies | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 03: Install the pinned Markdown renderer | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 04: Install diagram gate dependencies | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 05: Link health, wording, dead-reference and local-info gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 06: Added-line em-dash gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 07: Concise audience documentation gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 08: Audience diagram no-drift gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 09: Product solution source-fact gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 10: Verified submodule documentation gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 11: HDL timing diagram no-drift gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 12: Published diagram PNG gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 13: Milan feature-status consistency gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 14: Traceability matrix no-drift gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 15: Fetch the builder source dependencies | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 16: Imported gPTP documentation gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 17: Code-quality measurement self-tests | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 18: Install the pinned sv2v release | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 19: Bare-metal scope gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 20: Install and verify the pinned RV32 SDK | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 21: Compiler-absent firmware controls | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 22: End-station builder gates | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 23: NVM record-space gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 24: Capture measurement census and clock gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 25: Saved-state writer gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 26: SoC source-list gate (Vivado would fail 40 min in without this) | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 27: RTL source-list drift gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 28: Boundary-unit naming ratchet | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 29: Port contract gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 30: Fail-fast ratchet | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 31: TODO ownership gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 32: Test-evidence ratchet | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 33: Mechanical hygiene ratchet | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 34: SystemVerilog idiom gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 35: C and C++ idiom gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 36: Python idiom gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 37: Shell idiom gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 38: CI event and SHA contract gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 39: Local act runner contract gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 40: Doc cited-path gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 41: Archive integrity gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 42: Per-page contents gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 43: AEM store generator self-test | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 44: Sweep/build shape gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 45: Deploy shape gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 46: Entity shape gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 47: Fetch the engine authority the builder derives from | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 48: Advertised-vs-emitted gate (green since 2026-07-28, item 00) | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 49: Strip git metadata, then run the docs gate | `1e99ad217f07` | GNU Make 4.3 | 0 |

## Execution and retained evidence

The worktree and every gate use the physical `/data` path. New simulation campaigns use the pinned Verilator 5.050. Concurrency is limited to two simulator builds, with `make -j8`, `VERILATOR_JOBS=2` and at most four campaign workers. Vendor invocations hold `$VIVADO_LOCK`; no heavy campaign runs alongside them. `/data` free space is monitored against the 30 GB floor.

The unit has a 12 GiB hard limit and a runtime 7 GiB MemoryHigh limit. The first excluded synthesis attempt reached 9.65 GiB before termination; this operating-limit excursion is not hidden. No OOM event occurred. A second attempt completed synthesis but was terminated during implementation under memory pressure. A first checkpoint restart lost its launch session without a receipt. A subsequent checkpoint route completed, but its synthesis process had been interrupted, so that route is provisional only. The accepted evidence is the later clean two-process synthesis and implementation, each rc 0. Their logs and checkpoint hashes are recorded separately. Removed large provisional checkpoints and temporary directories have recorded sizes and digests in the external cleanup receipt.

Large build products, exports and environments stay outside this packet under `$VALIDATION_STORAGE/682-a554`. Each packet file is limited to 200,000 bytes. `runtime-links.json` records the temporary ROM and builder output links required by the retained measurement inputs; these links were removed for the clean handoff and their removal is recorded in `worktree-cleanup.json`. Recreate only those recorded links to recheck the retained resource reports. The earlier `generated-record-hashes.json` predates explanatory prose; use `current-records.json` for the committed records.

The full-acceptance supervisor returns 1: its original documentation child failed before the corrected 49-step retry, and the parent bank was later cancelled after the render blocker was confirmed. No aggregate green result is claimed.

The first documentation job refused reference generation because Git emitted diagnostics for an unmounted object alternate and an inaccessible image configuration directory. Read-only mounts of the public object databases and a normal per-user configuration path corrected the environment; the literal workflow commands are unchanged. The failed attempt is retained separately. A launch-only rc 126 (non-executable wrapper) was corrected by invoking the script with Bash before any campaign ran.


### Shared generated-header dependency and confirmed blocker

The builder rollback controls temporarily rewrite `hdl/common/csr/gen/lwsrp_csr_defaults.svh`. The documentation workflow builder and host builder overlapped source consumers, so the original `milan_csr` and `milan_datapath` synthesis results and render result are not used alone as evidence of immutable committed input. The parent sweep and bank coordinators were briefly paused, the builder completed, and the header was verified byte-identical to HEAD before resumption. `parent-pause.json` records the pause, resumption and header digest. Fresh synthesis of both affected tops and fresh three-top elaboration return zero. Resource measurements preceded the overlap and are unaffected.

`render-recheck.py` imports the repository campaign and rebuilds the four failed cases through its existing recipes. It verifies the committed CSR bytes before each build and after each run. `render-recheck.json` binds the run logs, build logs, test variants and executables by digest and size:

| Fresh case | Checks | Failed assertions | Run rc | Campaign meaning |
|---|---:|---:|---:|---|
| Unmodified epoch mode | 127 | 4 | 1 | Clean control fails |
| Acknowledgement-level arrival skew | 127 | 4 | 1 | Clean control fails |
| Serial-reset-level arrival skew | 127 | 4 | 1 | Clean control fails |
| Uncounted-repeat mutant | 58 | 0 | 0 | Mutant survives |

All three clean cases fail the same four T30 CRF recentre assertions: settled-grid trigger once, recentre pulse once, stage executes once, and no second recentre after the settled event; each observes zero where one is expected. The surviving mutant fails no assertion. The full repository inventory remains 28/32, rc 2. This matches the cases in open [#657](https://github.com/kebag-logic/milan-fpga/issues/657), although the current clean leg has 127 checks rather than the older issue’s 114. No base checkout was made and no causal attribution to this pin is claimed.

Issue #682 requires every gate to pass and contains no exception for #657. The previous adoption’s exception does not clear this one. No render source, expected result, inventory or acceptance criterion was changed. The broad sweep was cancelled through its repository-owned process supervisor, which returned 143 and explicitly reported no completed sweep result. All campaign processes have ended. `diagnostic-cleanup.json` records removal of 804,200,156 bytes of diagnostic build intermediates; all four executables and their evidence logs remain outside the packet.

## Remaining work and boundaries

Full acceptance is blocked by #657. A published scope decision or the existing issue’s repair is needed before this adoption can meet its all-green criterion. Bitstream/manifest completion, the remaining 50 default suites, parent tally, physical-gPTP simulation, NVM lint/quick and the four LiteX simulations remain uncompleted. The final dev comparison is recorded; integration is prohibited in this session. Stop on an additional processor-parent interface change, non-reproducible generated record or failed best-directive timing. Independent review, hosted checks, publication, merge validation and post-merge hardware work remain outstanding. No push, PR mutation, merge, rebase, firmware edit, processor source edit or hardware access is authorized here.

## Commits

1e99ad217 Rebaseline adopted processor resources and timing
d02c2a3ea Record optional synthesis worker cap in baseline recipes
2a97d4e88 Tighten adoption documentation wording
fcaabb227 Refresh processor pin records and parent integration notes
166c2185e Adapt parent frame capture and declaration budget to processor pin
7bbb53d79 Adopt protocol processor main 2ad2f845 for issue 682

