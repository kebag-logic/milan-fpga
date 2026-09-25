# [A320] Merge-dev handoff

Status: author merge-round work complete. Every assigned local gate returns 0. Independent merge-delta review remains pending; the head is local and unpushed.

## Scope and head

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/545#issuecomment-5835673886
- Repository remote verified: `https://github.com/kebag-logic/milan-fpga.git`.
- Branch: `545-crf-servo-slew`.
- Initial head / first parent: `4538d7c03dc4f56d7ed4c971603e15bda82050a8`.
- Fetched dev / second parent: `5c78ce2e9d831e588e759b696ed549804327e4d8`.
- Merge head: `ddf8151c478fc54c98608589c1afe9525739d6a4`.
- Commit subject: `Merge dev into 545-crf-servo-slew`; no body or trailers.
- Command: `git merge --no-ff origin/dev -m "Merge dev into 545-crf-servo-slew"`.
- Only conflict resolutions were written manually. No additional source, test, ratchet, or contract change was made.
- No push, PR creation/edit, merge into dev, extra checkout, hardware operation, or donor edit was performed. No delegation was used.

## Every conflict hunk

The original conflict record is `conflicts.diff`. `merge-remerge.diff` records the committed resolution against Git's automatic merge.

| Hunk | Final location | Resolution |
| --- | --- | --- |
| Changelog Contents | `CHANGELOG.md:11`, `CHANGELOG.md:12` | Retained the complete #545 and #443 entries, in the same order as their sections. |
| Changelog release sections | `CHANGELOG.md:33`, `CHANGELOG.md:47` | Retained both complete sections unchanged, with a blank line separating them. |
| Evidence-reader campaign dispositions | `scripts/measure_test_evidence.py:634`, `scripts/measure_test_evidence.py:638` | Kept the lane's complete #387/#545 gmstep disposition and dev's complete #443 render-CSR disposition. Removed the stale dev-only eleven-control gmstep ending. |

The eight-defect #545 servo disposition remains at `scripts/measure_test_evidence.py:597`. Dev's receiver-validation disposition automatically merged at line 603. Both complete campaign classifications were read against their executable inventories. All remaining incoming files are the automatic merge result; see `merge-first-parent.stat`.

## Submodules and regeneration

`git submodule update --init` returned 0. No pin changed in this merge, and no missing pinned commit required a fetch. Recursive checkout status and cleanliness checks passed.

| Path | Merged gitlink |
| --- | --- |
| `external` | `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5` |
| `gptp-processor` | `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` |
| `protocol-processor` | `990f96526bb89356c963a260ebbdcf2a77e6623a` |
| `third_party/verilog-axis` | `48ff7a7e2ef782cf778d47910cf85835c64b1bce` |

`python3 scripts/gen_toc.py --write CHANGELOG.md` returned 0 with `TOC: 0 page(s) written`. Thus no generated tracked file required updating. The matrix check also confirms its generated output is current. The OOC recipe regenerated its temporary ROM images and validated them against the unchanged committed ledger. Datapath build commands regenerated disposable divergent-shape, AEM-build and image artifacts; the exact commands are in `dp-commands.json` and their individual logs. No such artifact is committed.

The first Contents-generation attempt refused because pinned `html5lib` was missing. This was an environment setup failure, not a source repair. Dependencies were installed outside the output directory:

```sh
python3 -m venv --system-site-packages /tmp/milan-a320-python
/tmp/milan-a320-python/bin/python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

Subsequent commands prepend that environment to `PATH`. See `python-setup.log` and `regen-toc-final.log`. No toolchain, installed package, virtual environment, tool prefix or tree export is in the output directory.

## Gate method and limitations

All gate commands run synchronously in their process, without pipelines or background shell jobs, with a 21,600-second outer timeout. The timed clean default servo run is restricted to CPUs 8 and 9. Other simulation and build processes use CPUs 10 through 15. These are shared-host local samples.

The no-git documentation mode uses a `git archive HEAD` source export in `/tmp`, with no `.git` and no additional checkout. It reports the same 165 Markdown and 869 text files as the Git mode. The inventory-parity self-test is necessarily skipped without Git metadata; the other scrub and routing controls pass.

The default datapath recipe was expanded with `make --no-print-directory -C tb/verilator/milan_dp -n run`. `dp-dry-run.txt` preserves that recipe; `dp-commands.json` holds all 33 executable commands at the existing generated-file state. Only echo separators were omitted. `dp-chunk.py` executes consecutive ranges 1-9, 10-20, 21-31 and 32-33, preserving each exit and full log. The repository source/parameter recipes are unchanged. The GM-step leg is command 9 and is also rerun by `make gmstep-mutants`.

The builder returns 0 with one NOT RUN arm: gate 11 board-report calibration, because the required utilization report is absent. No compiler-related arm is skipped. Some datapath checks are explicitly guarded out in shapes where they do not apply; the full per-shape logs preserve those counts. The gPTP shadow campaign also retains its two named non-separately-observable cases. None is presented as new coverage.

No hardware was run. This local head has not been pushed, so no new hosted verdict is claimed. The assignment calls for an independent merge-delta review; this handoff is author evidence, not a review verdict.

## Area comparison

The repository `syn/yosys/ooc.sh KL_mmcm_drp_servo` recipe uses `synth_xilinx -family xc7 -flatten`, default servo parameters, and the existing system allocator selection. Current and baseline use identical common inputs and mapping. For baseline, `git show 5c78ce2e9d831e588e759b696ed549804327e4d8:hdl/ieee1722/crf/KL_mmcm_drp_servo.sv` supplies the old servo into a temporary directory. A temporary copy of the repository recipe anchors its root and malloc helper to this worktree and substitutes only that servo source; it does not create another checkout or edit tracked inputs.

| Source | LUT | FF | LUTRAM | RAMB36 | RAMB18 | DSP | CARRY4 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Dev servo | 864 | 790 | 0 | 0 | 0 | 1 | 150 |
| Merged servo | 871 | 792 | 0 | 0 | 0 | 1 | 150 |
| Delta | +7 | +2 | 0 | 0 | 0 | 0 | 0 |

The servo is byte-identical to the initial lane head: the merge adds zero servo area. This reproduces the existing isolated estimate, not a whole-datapath or placement measurement. The release-alignment and adopted-processor costs are outside this standalone measurement. The standalone `area-reproduce.py` records the exact source-only recipe substitutions for replay from the repository root. Exact commands and summary output: `area-base.log`, `area-current.log`; full synthesis evidence: `area-base-synthesis.log`, `area-current-synthesis.log`.

## Clean servo timing

`make -C tb/verilator/mmcm_servo clean` precedes the default run. `/usr/bin/time -p taskset -c 8,9 make -C tb/verilator/mmcm_servo` returns 0: real 938.63 seconds, user 943.62 seconds, sys 1.22 seconds. All 100 unit, 8 rail, 113 step and 90 slew checks pass. The unchanged 1,800-second budget retains 861.37 seconds (47.9%) of local margin. No timeout or budget was edited.

## Final validation summary

- Clean servo default: 100 unit, 8 rail, 113 step and 90 slew checks; 938.63 seconds on CPUs 8 and 9.
- Explicit slew campaign: 10/10, comprising two positive controls and eight named defect rejections.
- Connected GM-step/slew leg: 58/58; full explicit campaign: 16/16, comprising two positive controls and fourteen named defect rejections.
- Default datapath sweep: all 33 executable commands returned 0 across four chunks. The clock-ratio leg passed 190 checks; render and default GM-step controls passed 6/6 and 4/4.
- Receiver and shadow default suites returned 0. Receiver controls passed 10/10; shadow controls reported nine with zero failures, retaining the documented non-observable cases.
- Builder returned 0 with only gate 11 board-report calibration NOT RUN; no compiler-related arm was skipped.
- Both documentation modes and every assigned static gate returned 0. Evidence-reader self-test: 101/101. Existing frontend and lint ratchets were unchanged.
- Behavior tests: 344 scenarios, 1,739 steps; no failures or skipped scenarios.
- Final root and recursive submodule status is clean. No source repair was needed after the merge. The initial missing renderer dependency was resolved as environment setup and is recorded above.

## Gate table

Full commands, working directories, durations and exits are also recorded in `gates.jsonl`. Each named log contains unpiped command output.

| Gate | Exact command | Exit | Seconds | Evidence |
| --- | --- | ---: | ---: | --- |
| regen-toc-final | `python3 scripts/gen_toc.py --write CHANGELOG.md` | 0 | 0.164 | `regen-toc-final.log` |
| mmcm-clean | `make -C tb/verilator/mmcm_servo clean` | 0 | 0.008 | `mmcm-clean.log` |
| docs | `python3 scripts/docs_check.py` | 0 | 4.272 | `docs.log` |
| em-dash | `python3 scripts/check_em_dash.py --base 5c78ce2e9d831e588e759b696ed549804327e4d8` | 0 | 3.026 | `em-dash.log` |
| doc-style | `python3 scripts/check_doc_style.py` | 0 | 0.064 | `doc-style.log` |
| toc-check | `python3 scripts/gen_toc.py --check` | 0 | 2.418 | `toc-check.log` |
| toc-anchors | `python3 scripts/gen_toc.py --verify-anchors` | 0 | 1.517 | `toc-anchors.log` |
| doc-paths | `python3 scripts/check_doc_paths.py` | 0 | 0.064 | `doc-paths.log` |
| module-matrix | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | 0.966 | `module-matrix.log` |
| source-lists | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.367 | `source-lists.log` |
| sv-idiom | `python3 scripts/check_sv_idiom.py` | 0 | 0.465 | `sv-idiom.log` |
| cpp-idiom | `python3 scripts/check_cpp_idiom.py` | 0 | 1.216 | `cpp-idiom.log` |
| py-idiom | `python3 scripts/check_py_idiom.py` | 0 | 3.120 | `py-idiom.log` |
| port-contracts | `python3 scripts/check_port_contracts.py` | 0 | 2.318 | `port-contracts.log` |
| naming | `python3 scripts/measure_naming.py --check` | 0 | 0.465 | `naming.log` |
| docs-no-git | `python3 scripts/docs_check.py` | 0 | 4.132 | `docs-no-git.log` |
| test-evidence | `python3 scripts/measure_test_evidence.py --check` | 0 | 5.534 | `test-evidence.log` |
| test-evidence-selftest | `python3 scripts/measure_test_evidence.py --selftest` | 0 | 5.486 | `test-evidence-selftest.log` |
| diff-check | `git diff --check` | 0 | 0.033 | `diff-check.log` |
| behave | `behave --no-capture -f plain` | 0 | 8.079 | `behave.log` |
| lint | `taskset -c 10-15 python3 scripts/lint_rtl.py --check` | 0 | 12.231 | `lint.log` |
| area-current | `taskset -c 10-15 env OOC_TMP=/tmp/milan-a320-area-y4e3qvq2/current syn/yosys/ooc.sh KL_mmcm_drp_servo` | 0 | 5.027 | `area-current.log` |
| xvlog | `taskset -c 10-15 python3 scripts/xvlog_gate.py --check` | 0 | 154.170 | `xvlog.log` |
| area-base | `taskset -c 10-15 env OOC_TMP=/tmp/milan-a320-area-y4e3qvq2/base bash /tmp/milan-a320-area-y4e3qvq2/ooc-base.sh KL_mmcm_drp_servo` | 0 | 4.228 | `area-base.log` |
| gptp-shadow | `taskset -c 10-15 make -C tb/verilator/gptp_shadow -j8` | 0 | 284.130 | `gptp-shadow.log` |
| builder | `taskset -c 10-15 python3 sw/builder/test_builder.py` | 0 | 841.418 | `builder.log` |
| mmcm-default | `/usr/bin/time -p taskset -c 8,9 make -C tb/verilator/mmcm_servo` | 0 | 938.645 | `mmcm-default.log` |
| crf-rx | `taskset -c 10-15 make -C tb/verilator/crf_rx` | 0 | 795.597 | `crf-rx.log` |
| gmstep-mutants | `taskset -c 10-15 make -C tb/verilator/milan_dp gmstep-mutants` | 0 | 770.091 | `gmstep-mutants.log` |
| mmcm-slew-mutants | `taskset -c 10-15 make -C tb/verilator/mmcm_servo slew-mutants` | 0 | 1267.927 | `mmcm-slew-mutants.log` |
| final-state | `python3 $MANAGEMENT/2026-09-23/545-a320/final-state.py` | 0 | 0.214 | `final-state.log` |
| final-diff | `git diff --check` | 0 | 0.032 | `final-diff.log` |

### Datapath command exits

Exact commands appear by position in `dp-commands.json`.

| Command | Exit | Seconds | Evidence |
| --- | ---: | ---: | --- |
| dp-01 | 0 | 0.114 | `dp-01.log` |
| dp-02 | 0 | 21.752 | `dp-02.log` |
| dp-03 | 0 | 91.428 | `dp-03.log` |
| dp-04 | 0 | 23.707 | `dp-04.log` |
| dp-05 | 0 | 92.524 | `dp-05.log` |
| dp-06 | 0 | 0.215 | `dp-06.log` |
| dp-07 | 0 | 0.064 | `dp-07.log` |
| dp-08 | 0 | 24.406 | `dp-08.log` |
| dp-09 | 0 | 30.416 | `dp-09.log` |
| dp-10 | 0 | 20.600 | `dp-10.log` |
| dp-11 | 0 | 24.411 | `dp-11.log` |
| dp-12 | 0 | 22.553 | `dp-12.log` |
| dp-13 | 0 | 24.257 | `dp-13.log` |
| dp-14 | 0 | 23.806 | `dp-14.log` |
| dp-15 | 0 | 21.249 | `dp-15.log` |
| dp-16 | 0 | 20.000 | `dp-16.log` |
| dp-17 | 0 | 20.605 | `dp-17.log` |
| dp-18 | 0 | 21.853 | `dp-18.log` |
| dp-19 | 0 | 26.963 | `dp-19.log` |
| dp-20 | 0 | 21.881 | `dp-20.log` |
| dp-21 | 0 | 6.388 | `dp-21.log` |
| dp-22 | 0 | 22.272 | `dp-22.log` |
| dp-23 | 0 | 26.412 | `dp-23.log` |
| dp-24 | 0 | 7.978 | `dp-24.log` |
| dp-25 | 0 | 11.534 | `dp-25.log` |
| dp-26 | 0 | 12.045 | `dp-26.log` |
| dp-27 | 0 | 7.030 | `dp-27.log` |
| dp-28 | 0 | 5.723 | `dp-28.log` |
| dp-29 | 0 | 0.665 | `dp-29.log` |
| dp-30 | 0 | 6.376 | `dp-30.log` |
| dp-31 | 0 | 492.640 | `dp-31.log` |
| dp-32 | 0 | 375.238 | `dp-32.log` |
| dp-33 | 0 | 175.214 | `dp-33.log` |

## Delivery

PR-BODY.md retains the complete fetched public body, changes its first line to [A320], and adds the current merge-dev record. All validation is complete. Posted [A320] REVIEW READY as the final external action: https://github.com/kebag-logic/milan-fpga/issues/545#issuecomment-5836177064 . The merge remains local and unpushed; independent delta review is pending.
