[R369] POSITIVE - exact head 5b6936ef9251d486307f1b28c0f81e6fa52746cb

# R369-4 composition review: issue #590 / PR #609 (#590, #592, #599) on the merge-train candidate

**Candidate:** `5b6936ef9251d486307f1b28c0f81e6fa52746cb`, tree `b5038a41dbf936219243f246a7bc324aa384512b`.
Its parents are live dev `eaa88a32eb77adeba9c1c631198c7fb516a11095` (after #607, PR #615) and PR source head `4c2a30debb031595b81c5c4bfc53b601a0fec528`. The merge base is `b5c0f69d5d11f0ec4bc847a2cfdd13e89e199a8a`.
At 2026-09-29T00:59Z, remote `dev` was still `eaa88a32` and the PR branch was still `4c2a30de`.

**Scope:** composition acceptance only. The composed tree introduces no defect beyond the reviewed sources. All five lenses were applied to the composition, each with named artifacts.

## Verdict summary

- **Findings:** no BLOCKER, MAJOR or MINOR. There is one out-of-scope SUGGESTION (S1), which does not affect coverage.
- **Mechanical composition is exact.**
  - `git merge-tree --write-tree eaa88a32 4c2a30de` gives `b5038a41`, the candidate's tree.
  - Of the PR lane's 30 changed files, 29 are byte-identical to `4c2a30de`. Of #607's 12 files, 11 are byte-identical to `eaa88a32`.
  - The one shared file is `sw/builder/test_builder.py`. Its hunks are disjoint, and each side's delta lands unaltered (`receipts/composition-file-map.txt`, `receipts/test_builder-hunk-identity.txt`).
- **Semantic interaction:** none found.
  - The builder registry runs 96/96 arms exactly once, with no duplicate name.
  - #607's `test_clock_crossing_constraints` ran and passed in both compiler modes.
  - A disposable elaboration probe (P1) shows that #607's SoC-generator changes leave the capture/service simulation SoC byte-identical after path and timestamp normalization. This covers both shapes, and two planted controls prove the comparison can fail.

## 1. What the two lanes share, and how each interaction was judged

| Surface | #607 (dev side) | This PR | Judgement and evidence |
|---|---|---|---|
| `sw/builder/test_builder.py` | Adds `test_clock_crossing_constraints` (`:27799-27804`) and registers it in `__main__` (`:27829`) | Changes gate 1b's digraph selection count 2 to 4 (`:13304`), the "four patches" text (`:23297`, `:23382`), and the gate-35 fixture stub `bios_dispatch_hook_required` (`:26647`, `:26668`) | Hunks are disjoint and each delta is carried byte for byte. Of the 96 `__main__` entries, 91 are local definitions and 5 are imported, with no duplicates. Each arm printed exactly once in both full runs (`grep -c '^test_'` = 96). |
| Patch series / LiteX tree | Shipping probe elaborates with `with_bios=False`; firmware data packages are refused | Adds `0006-bios-dispatch-hook.patch` (touches only `litex/soc/software/bios/main.c`) and the SERIES entry (`apply.sh:36`) | 0006 changes a C file that the #607 probe never compiles. Gate 23h reports "the 4 patches ... reproduces all 4 installed files byte for byte" in both runs. |
| Implementation-log refusal and `.bit` quarantine (`milan_soc.py` `main()`, `clock_constraints.py`) | New | Firmware and BIOS are compiled inside `builder.build` before gateware | The check reads only `gateware/vivado.log` and runs only on `--build`. No PR artifact writes that log. #607's own controls passed in both runs. |
| `MilanSoC` / `_CRG` (`milan_soc.py:2731-2736`, CRG clock lists, MAC XDC hooks) | New `add_eth_constraints` under `with_mac` for `board == "ax7101"`; `eth_bounded_clocks`/`eth_async_clocks` on `_CRG` | Capture harness `tb/verilator/nvm_capture_cpu/soc.py:123-157` builds `ProductSimulation(MilanSoC)` with `_CRG` patched to `SimClocks` and `with_mac=False`; the service harness wraps the same `capture_soc.build` (`fw_service_budget/build.py:93-97`) | The new code is unreachable with `with_mac=False`. The sim platform does not use the AX7101 `Platform` toolchain replacement. **P1** elaborated both shapes with pre-#607 and candidate `sw/litex` files: 27/27 generated files identical per shape. |
| Capture/service evidence bindings | n/a | `check_nvm_capture.py` binds firmware, harness and census; `fw_service_budget/run.py:158-167` hashes `sw/litex/milan_soc.py` into its bound inputs | `check_nvm_capture` passes at the candidate. No committed record pins a `milan_soc.py` hash (`git grep` for both digests: none). The retained native service evidence binds the pre-#607 `milan_soc.py`, and P1 shows the simulated product is unchanged. This is a manager note, not a defect (section 7). |
| Docs | `BUILDING.md`, `CLOCK_DOMAINS.md`, `LITEX_SOC.md`, `RUNNING_TESTS.md` | Nine pages; none shared | Cross-lane link `BOARD_PORTING_AX7101.md:126` to `BUILDING.md#41-bench-hosts-and-the-one-dut-acceptance-contract` resolves (heading `BUILDING.md:500`, not moved by #607). Neither lane's text describes the other's mechanism. TOC, anchor, em-dash and wording gates pass on the composed tree. |
| Workflow and record pins, ratchets | No workflow change | No workflow change | `ci_events --check`/`--selftest` pass at 1655 items. Naming, hygiene, py/sh/cpp/sv idiom, fail-fast, test-evidence and port-contract ratchets all pass on the union of both lanes' code. |

## 2. Gates run on the candidate (all at `5b6936ef`)

The environments were built for this review under the scratch area:
- **Pins-only LiteX interpreter:** fresh `venv` with `pip install -r sw/litex/litex_pins.txt` (freeze in `receipts/pins-venv-freeze.txt`), then `scripts/ci_litex_env.py` and `sw/litex/patches/apply.sh` ("series applied (4 patches)").
- **Markdown environment:** `pip install --require-hashes -r tools/markdown/requirements.txt`.
- **RV32 SDK:** `scripts/ci_rv32_sdk.py --verify-only` passed on archive `d42680e9...`.
- **Verilator:** 5.050, binary sha256 `44898b22...`. This equals the recorded `verilator-5.050-1` identity.

| Gate | Result | Receipt |
|---|---|---|
| Full builder, pinned SDK mapped onto the absolute selector, `--require-rv32 --require-elaboration`, pins-only interpreter | rc 0, 777 s; `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11, needs the mf48 build tree); 1,173 mapped compiler calls; the elaboration requirement holds | `builder-full-sdk-elab.{log,rc}`, `builder-sdk-audit.jsonl` |
| Full builder, every cross compiler absent, `--require-elaboration`, second pins-only interpreter, byte-identical tree copy | rc 0, 565 s; `EXCEPT 2 NOT RUN` (gate 1b compiled census by design, gate 11) | `builder-full-absent.{log,rc}`, `builder-absent-audit.jsonl` |
| `test_firmware_compiler.py --selftest`; `--absent`; `--absent --require-rv32` negative control | rc 0; rc 0 (`GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations`); rc 1 with `--require-rv32: the hosted firmware instruments must run`, as required | `static/fw_compiler_*` |
| `make -C tb/verilator/nvm_cosim` (Verilator 5.050, JOBS/POOL 6) | rc 0, 388 s: 1x1 62 case runs, 315 ok; 8x8 27 case runs, 150 ok; 39 of 39 mutants killed; 465/465 PASS | `nvm-cosim.{log,rc}` |
| `scripts/check_nvm_capture.py` | rc 0 | `static/nvm_capture.log` |
| Lane self-tests: `test_nvm_firmware.py --self-test`, `test_phy_firmware.py`, `test_disabled_writer.py`, `fw_service_budget/run.py --self-test` | All rc 0: writer gate OK over 5 shapes with every planted defect caught; `late-sample` and `ack-ignored` caught; oracle 47 checks, 0 failures | `lane/` |
| Markdown gates: `docs_check.py`, `check_em_dash.py --base eaa88a32` and `--selftest`, `gen_toc.py --check`/`--verify-anchors`/`--selftest`, `check_doc_style.py`, `check_doc_paths.py`, `DOC_MAP.gen.py --check` | All rc 0. docs_check: 0 findings over 174 md and 936 scrubbed files. em-dash: 0 findings over 555 added lines in 11 pages, arms 339/339. TOC: 116 pages OK. Anchors: 238 cross-page links reproduced. | `static/` |
| Static and pin gates: `ci_events.py --check`/`--selftest`, `ci_scope.py --selftest`, `check_baremetal_only.py`, `check_nvm_record_space.py`, `check_soc_sources.py`, `check_rtl_source_lists.py`, `check_port_contracts.py`, `check_todo_ownership.py`, `check_archive.py`, `check_solution_docs.py`, `check_feature_status.py`, naming/fail-fast/test-evidence/hygiene ratchets, sv/cpp/py/sh idiom gates, `git diff --check eaa88a32 HEAD` | All rc 0 | `static/SUMMARY.txt` |

**Probe P1** (`probe_elab.py`, `diff_elab.py`) runs the capture harness's own `build()` unchanged, with three patches: Builder compiles no software, the BIOS make variables are omitted as #607's shipping probe does, and the Verilator compile and sim make-variable steps are stubbed.
- **Base tree:** a candidate copy with `milan_soc.py`, `platforms/alinx_ax7101.py` and `sweep.sh` restored to `b5c0f69d`, and `clock_constraints.{py,tcl}` removed.
- **Result:** 27/27 files identical for `endstation_ax7101_1x1_tdm8` and for `endstation_ax7101_8x8`. The compared files include `gateware/sim.v`, `csr.json`, `sources.json` and the generated `csr.h`/`soc.h`/`mem.h`.
- **Controls:**
  - Planting `MILAN_CSR_SIZE = 0x0002_0000` makes `sim.v`, `mem.h`, `csr.*` and `sources.json` differ (rc 1).
  - Planting a SPI clock change makes `csr.*` and `soc.h` differ (rc 1).
  - Before timestamp normalization, `sim.v` also differed by its date lines only.

## 3. Findings

No BLOCKER, MAJOR or MINOR finding.

### R369-4-S1 - SUGGESTION - Docs - two untouched comments still say the series has six patches

- **Where:** `.github/workflows/elaborate.yml:26` ("carries the six patches") and `sw/litex/litex_pins.txt:30` ("# the six patches").
- **Evidence:** `sw/litex/patches/apply.sh:33-38` applies four. Gate 23h reports 4. Neither lane changed these files: they were last changed in `ab2671c0` and `dfcf83ce`. They were already stale at the merge base (three patches), and this PR's S6 correction covered `apply.sh` and `test_builder.py` only.
- **Impact:** the comments misstate what CI applies. This is not introduced by the composition.
- **Suggested outcome:** a separate Issue that aligns both comments with the SERIES array.
- **Verification:** `git grep -n -i 'six patches'` returns only the historical wording at `test_builder.py:23382`.

## 4. Prior public findings: disposition at the candidate

These were read after the independent pass above. Every PR-lane file is byte-identical to `4c2a30de` (`composition-file-map.txt`). The executable controls behind each resolution were re-run green on the candidate.

| Finding | Severity | Status at `5b6936ef` | Evidence |
|---|---|---|---|
| R369-1 F1 = R368-1 F1 (MDIO sample phase) | BLOCKER | Resolved, held | `test_phy_firmware.py`: `PHY_MUTANT late-sample: caught` (`lane/phy_firmware.log`) |
| R369-1 F2 = R368-1 F2 (dispatch for every line) | MINOR / MAJOR | Resolved, held | Patch 0006 is in the applied series; `fw_service_budget/run.py --self-test` passes "product dispatch census" |
| R368-1 F3 (record-edge guard test) | MINOR | Resolved, held | Host self-test: every planted defect reddened (`lane/host_selftest.log`) |
| R368-2 N1 (disabled-writer heartbeat) | MINOR | Resolved, held | `disabled-writer mutant: caught in both states`; nvm_cosim W2-W4 restart cases pass |
| R368-2 N2 = R369-2 F4, R369-2 F5 (doc statements) | MINOR | Resolved, held | Pages byte-identical to the source head; docs gates pass on the composed tree |
| R369-2 F6 (native evidence retained) | MINOR | Resolved at the source head | Retained evidence binds pre-#607 `milan_soc.py`; P1 shows the simulated SoC is unchanged (section 7) |
| R368-3 S1-S3, R369-3 S11/S12, R369-1 S1/S3/S4, R368-4 S1/S2 | SUGGESTION | Retained, optional | Unchanged files |

## 5. Clean-lens evidence

```text
[R369] PASS Conformance - composition-file-map.txt; test_builder-hunk-identity.txt; probe-elab-diff-{1x1_tdm8,8x8}.txt; static/nvm_capture.log - the PR's firmware, harness and acceptance evidence are byte-identical in the candidate; #607's generator change leaves the measured simulation SoC identical, so #590 acceptance 2-3 evidence still describes the composed product
[R369] PASS RTL - git ls-files -s gitlinks (external efeb541a, gptp 5dce647a, protocol-processor c951a9ff, verilog-axis 48ff7a7e, equal in both parents); no hdl/ path in either lane; probe-elab-diff-*.txt (sim.v identical) - the composition changes no RTL, and the SoC generator's composed output for the capture/service products is identical to the source's
[R369] PASS Robustness - milan_soc.py:2731-2736 (add_eth_constraints only under with_mac) vs nvm_capture_cpu/soc.py:123-157 (with_mac=False, _CRG patched); builder-full-absent.log; static/fw_compiler_absent_require.log; nvm-cosim.log W1-W4 restart cases - #607's refusal and quarantine paths are unreachable from the PR's harnesses, both compiler-absence paths behave as specified, and the restart and disabled-writer paths pass at the candidate
[R369] PASS Tests - sw/builder/test_builder.py __main__ (96 entries, 0 duplicates, 96 arms printed in each run); builder-full-sdk-elab.log; builder-full-absent.log; nvm-cosim.log (465/465, 39/39 mutants); lane/*.log; P1 planted controls - every lane's arm runs exactly once and all gates reading the shared file pass in both compiler modes
[R369] PASS Docs - static/docs_check.log, em_dash_base.log (555 added lines, 0 findings), gen_toc_check.log, gen_toc_anchors.log; BOARD_PORTING_AX7101.md:126 to BUILDING.md:500 - no shared page; cross-lane links resolve; no page states the other lane's behavior
```

## 6. Reviewer-owned completion ledger (composition round)

| Lens | Status | Composition touches its scope? | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|---|
| Conformance | CLEAN | Yes: evidence binding across `milan_soc.py` | File map, P1 diffs, `check_nvm_capture`, lane self-tests | R369-4 | `5b6936ef9251d486307f1b28c0f81e6fa52746cb` |
| RTL | CLEAN | No RTL path. The SoC generator is shared and was judged via P1. | Gitlinks, P1 `sim.v` identity | R369-4 | `5b6936ef9251d486307f1b28c0f81e6fa52746cb` |
| Robustness | CLEAN | Only through the build flow; judged unreachable | `milan_soc.py:2731-2736`, capture `soc.py:123-157`, absent and require controls, nvm_cosim restart cases | R369-4 | `5b6936ef9251d486307f1b28c0f81e6fa52746cb` |
| Tests | CLEAN | Yes: `sw/builder/test_builder.py` | Both full builder runs, registry census, nvm_cosim, lane self-tests | R369-4 | `5b6936ef9251d486307f1b28c0f81e6fa52746cb` |
| Docs | CLEAN (S1 is optional and out of scope) | Only via cross-links, TOC and anchors | Markdown gates, cross-lane link check | R369-4 | `5b6936ef9251d486307f1b28c0f81e6fa52746cb` |

Where a lens's composition exposure is nil, its source-level coverage rests on the PR's source reviews. For this lane these are R369-3 (POSITIVE, `93262f25`) and R368-4 (POSITIVE, `1f039cfe`). The merge-dev and fixture delta to `4c2a30de` is assigned to R368-5, which is started. The manager states that `4c2a30de` carries the two positives the merge requires. For #607, the source reviews are those recorded on PR #615.

## 7. Real limits

- **No hardware:** no physical calibration and no bench run. Field skips are not hardware proof.
- **Gate 11 NOT RUN in both modes:** it needs the mf48 implementation tree.
- **Gate 1b compiled census NOT RUN in the absent mode:** this is by design.
- **No vendor implementation was run.** #607's log refusal was exercised only through its own synthetic controls.
- **The native service and capture measurements were not re-run at the candidate** (about 2 h). The composition argument rests on byte-identical firmware and harness sources plus P1.
- **P1's scope:**
  - It compared generated gateware, CSR maps and headers. It did not compile or simulate them.
  - It omitted the BIOS make variables, because the pins-only interpreter has no firmware data package.
  - The service-harness wrapper was judged statically: `fw_service_budget/build.py:93-97` wraps the same `capture_soc.build` with `with_mac=False`. It was not elaborated separately.
- **Bound-input mismatch at merge:** `fw_service_budget/run.py:158-167` hashes `sw/litex/milan_soc.py`. The retained native service evidence therefore records the pre-#607 digest `c60bb994...`, while the merged tree has `2bfbaa6a...`. A later `--reuse-build` against those receipts will refuse reuse, which is correct behavior.
- **Pins-only interpreter:** it was installed from git URLs at the pinned revisions. That file carries no hashes.
- **Verilator path:** the Verilator wrapper path named in the assignment does not exist. The same package binary was used and verified by version string and sha256 against the recorded identity.
- **Hosted checks:** they were inspected read-only at the source head `4c2a30de`. `bdd-conformance`, `changes`, `docs-check-no-git`, `elaborate`, `full-ci-gate`, `rtl-fast`, `verilator-lint`, `wire-accountability`, `yosys-elaboration`, Verilator shards 0 and 3, and Yosys shards 0-3 had succeeded. `docs-check` and Verilator shards 1, 2 and 4 were in progress. "Physical gPTP (nightly and manual)" was skipped, which is not executed evidence. The candidate itself is not pushed and has no hosted run.

## 8. Pending manager duties

- **Merge-turn candidate:** build the final current-dev candidate. Dev was `eaa88a32` at review time, so this candidate is current unless dev moves.
- **Hosted and act:** complete hosted acceptance and act on the candidate. `docs-check` and Verilator shards 1, 2 and 4 at `4c2a30de` were still in progress when inspected.
- **R368-5:** confirm that the delta review of `4c2a30de` is published before merge.
- **Retained native evidence:** decide whether to accept P1 as the equivalence proof for the pre-#607 `milan_soc.py` binding, or to re-run the native service and capture at the merged tree.
- **New Issues:** consider opening one for R369-4-S1, and one for the executor's noted stale count at `tb/verilator/README.md:71`.

## 9. Receipts and post-probe state

- **Scripts:** `run_builder.py` (compiler-mode wrapper), `run_static.sh`, `probe_elab.py`, `diff_elab.py`, `sanitize.py`. The last one rewrote local path prefixes to `<CLONE>`, `<PACKET>`, `<SDK>`, `<VERILATOR_5050_PREFIX>`, `<MD_VENV>` and `$HOME`, then scanned every publishable file with the repository's own `docs_check.SCRUB_RULES`: 0 hits.
- **Receipts:** under `receipts/`. Every published file is listed in `MANIFEST.sha256`.
- **Post-probe state:**
  - All probe trees, interpreters and builds were disposable copies under the unpublished scratch area.
  - After the runs, only ignored outputs were removed from the clone (`git clean -fdX`, clone and `protocol-processor`).
  - `receipts/integrity-before.txt` equals `receipts/integrity-after.txt`. `git write-tree` gives `b5038a41`, every tracked blob re-hashes to its index entry, every mode matches, and the four gitlinks are unchanged. `git status --porcelain --ignored` is empty.

R369-4 FINISHED
