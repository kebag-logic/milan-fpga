[A383] REVIEW READY

Commit: `49012143b335ea48d6a71c441a05d0c1796887ff`, local branch `602-phc-step-mr`, based on `6d5ebd7357c1e468e446f18a61527c5be6118a04`. No push or PR operation performed.

The [scope correction](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859621253) is applied in separate test-only commit `49012143b`: the PHC-net census, restart initializer, related mutation anchors, diagnostics and comments now follow the ruling. Commit `81893de43` corrects the remaining restart input-port comment. The executable RTL remains exactly the removal of the PHC re-base contribution implemented in `f7660247e`; source changes, selected-CRF causes, render and tu behavior remain intact.

Validation at this head: all 34 recorded commands return 0, run in the foreground with explicit timeouts from the physical `$LANES/602-phc-step-mr` path, without pipes.

| Command or gate | Result |
|---|---|
| `make -C $LANES/602-phc-step-mr/tb/verilator/milan_dp run` | rc 0; 1642.38 s; render and default gmstep campaigns 6/6 each |
| `make -C $LANES/602-phc-step-mr/tb/verilator/milan_dp gmstep-mutants` | rc 0; clean gmstep 64/64; 16/16 mutants caught; both clean controls pass |
| `make -C $LANES/602-phc-step-mr/tb/verilator/tkdiag` | rc 0; 96 assertions and four caught mutants |
| `python3 sw/builder/test_builder.py --require-rv32` | rc 0; gate 1b rejects 358/358 mutations; 53/53 RTL variants elaborate |
| Full `test_builder.py` entry point with only its three cross-compiler candidates hidden | rc 0; gate 1b rejects 256/256 mutations; 53/53 RTL variants elaborate; compiler-dependent instruments explicitly NOT RUN |
| `python3 scripts/lint_rtl.py --check --jobs 8`; `python3 scripts/ci_scope.py --selftest`; `python3 scripts/check_baremetal_only.py --check` and `--selftest` | all rc 0 |
| Documentation, source-list, idiom, hygiene and test-evidence gates; `git diff --check 6d5ebd7357c1e468e446f18a61527c5be6118a04 HEAD` | all rc 0; exact commands and receipts in HANDOFF.md |
| `syn/yosys/ooc.sh` recipe, shaped datapath defaults, `synth_xilinx -family xc7 -flatten` | all six shape runs rc 0: base, changed source and neutral base edit at both AX shapes |
| Five generated configurations | All 50 artifacts byte-identical to the saved base manifests |

Both builder modes explicitly skip gate 11 because its historical placed-calibration report is absent. Absent mode additionally records its RV32-dependent instruments as not run; the separate RV32-required bank executes them. These are disclosed coverage limits, not counted passes.

| AX shape | Base LUT | Changed LUT | Functional delta | Neutral LUT | Neutral delta |
|---|---:|---:|---:|---:|---:|
| 1x1 TDM8 | 97630 | 97812 | +182 | 97630 | 0 |
| 8x8 | 141366 | 142972 | +1606 | 141366 | 0 |

The neutral edit renames only `tkd_crflk_q_r` to `tkd_crf_lock_prev_r` at all four references in the base datapath; inverse renaming is byte-identical to base. Both neutral runs reproduce every base cell count. The control therefore does not reproduce or explain the positive functional LUT delta. FF, LUTRAM, block RAM, DSP and carry counts remain unchanged by the functional edit. Release area is judged on the placed build, which is outside this evidence.

Acceptance: the PHC-only gmstep causes zero outgoing mr transitions and zero MEDIA_RESET increment; tu rises/holds/clears, one render re-base occurs, and media transport continues. Genuine source-change and selected-CRF propagation controls pass, and all three required defects are caught by their named assertions. The disabled-render control fails the counted-event check under the recorded #387 correction. No physical-clock or lwSRP-reservation proof is claimed by the compressed gmstep leg.

Evidence packet `602-a383`: HANDOFF.md, PR-BODY.md, per-gate logs/receipts, neutral-control comparison and artifact manifests. The worktree is clean, all 566 pinned submodule blobs match their commit objects, and every output file is below 200 KB. Larger logs and build artifacts are retained outside the packet with size and SHA-256 receipts. Open implementation blockers: none. Independent review remains pending.
