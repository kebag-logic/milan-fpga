[R596] POSITIVE - exact head 17834d8f09dfaa5fde513dd7afa3d455b5e0df2c

# R596-2: composition review of issue #711 / PR #718 (merge-train candidate)

- Candidate: `17834d8f09dfaa5fde513dd7afa3d455b5e0df2c`, tree `24d0b37e2f808229b09c628d0ff8c654aa3ff99b`. Its parents are the F-INT candidate `8c8f82f628a24223e4ff7459f46a51735915351e` (PR #704 over dev `6bfeeb132fa0b1ad8a5b957446c66a498e633af7`) and the PR source head `49b437f445e34b558106c8799c1ffc0a5dc844cf`.
- Scope: composition acceptance only. The source head already has two independent POSITIVE source reviews: R596-1 (comment 6103803276) and R597-1 (comment 6103829274).
- Verdict: **POSITIVE**. The composed tree adds no defect beyond the reviewed sources. There is no open BLOCKER, MAJOR, MINOR or RESIDUE item. Three prior SUGGESTIONs are retained unchanged; they do not block.

## 1. What the composition is

- **The diff carries no conflict resolution.** `git diff 8c8f82f6..17834d8f` and `git diff e8454e27..49b437f4` have identical hunk bodies and the same stable patch-id, `1bc2626697d05b95895d451fb7477f10aeaa4639`. The PR's merge base is `e8454e27`. Receipts: `receipts/composed_diff.patch`, `receipts/pr_source_diff.patch`.
- **11 paths changed:** the `third_party/lwSRP` gitlink `9197193e` → `08ee86e8`, `ctrl_arms.LWSRP_REV`, `srp_latency.cpp`, five docs pages and the regenerated submodule diagram set.
- **Files that both a predecessor and this PR change.** I confirmed these with `git log e8454e27..8c8f82f6 -- <path>`:
  - `docs/design/MAILBOX_SPLIT.md`: 14 predecessor commits, including F-INT's census and publication text.
  - `sw/firmware/ctrl/README.md`: 5 commits, including F-INT's `srpcmp` arm and the publication block.
  - `sw/firmware/ctrl/srp/README.md`: 3 commits, including F-INT's publication term and the B13/TALKER_DECL tests.
  - `sw/firmware/ctrl/test/ctrl_arms.py`: 2 commits, F-INT's `arm_srpcmp` and its named control and plant sets.
  - No predecessor touches the other 7 paths: the diagram files, `PNG_MANIFEST.json`, `SUBMODULES.md`, `srp_latency.cpp` and the gitlink.
- **Semantic interactions I checked:**
  - F-INT's SRP publication code (`srp_mbx.c`, +65 lines), its tests (`srp_mbx.cpp`, +274; `srp_app.cpp`) and its plants (`srp_pub_mutants.py`, ROUND5) all run against the new lwSRP grouped encoder.
  - F-INT's `srp_wire_compare.py` comparator (the `srpcmp` arm).
  - The SRP access envelope in `srp_bounds.h` and the README (1,676 / 2,486 at IF=1/2, 383 per transmit call), which F-INT's publication term extends.
  - The saved-state capture digest binding.
  - The submodule ledger, diagram and PNG manifest.
  - TOC and anchors.
  - CI event and SHA contracts.
- **lwSRP pin facts.** I checked these against a fresh public clone:
  - `08ee86e8` is "Merge pull request #18" and an ancestor of public `main` (now `97677fcb`).
  - `9197193e` (PR #15) is its ancestor, and PR #18's head `a44eeedf` is contained in it.
  - `src/ports/` is unchanged between the two pins, so the `shlan_port.h` restatement still holds.
  - The `integrator.md#L324-L326` and `mrp.h#L292-L294` permalinks show the same contract text as the old L321-L323 and L288-L290.

## 2. Executed evidence on the candidate

All results below were measured in this clone at the exact candidate head, with `third_party/lwSRP` initialized at its gitlink `08ee86e8`. Compilers: host gcc/g++/gcov 16.2.1, GoogleTest/GoogleMock 1.18.0, and the pinned RV32 SDK at `~/br-milan-rv32/host`.

| Gate | Result | Receipt |
|---|---|---|
| `fw_rv32_selftest.py --require-rv32` | rc 0, 17 checks PASS | `receipts/fw_rv32_selftest.log` |
| `test_ctrl_firmware.py --require-rv32 --jobs 4` (all arms) | rc 0. 60 arms `[ok]`, none failed: the 59 at the source base plus F-INT's `srpcmp`. Includes `lwsrp` at `08ee86e8` and the F4 SRP set `srp_mbx`, `debug`, `srp_rx_retry`, `srp_app`, `test_acmp_mbx`, `srp_latency` and `srp_walk` at IF=1 and IF=2. Also `srp_shape` and `rv32` at both IFs for all six shapes, and the AECP compositions. | `receipts/test_ctrl_firmware_arms.log` |
| `srpcmp` arm (F-INT comparator self-test) | 5 named controls PASS, including `frame_grouping`; 18 of 18 named plants caught; none missing | same log, lines 244-247 |
| Mutation campaigns (the `--self-test` calls, run as partitions through `run_mutants.py`) | control 506/506; AECP 76/76; SRP two-interface 198/198, including F-INT's publication plants; SRP one-interface subset 73/73, including ROUND5; lwSRP pin 2/2 (edited source and old revision `9197193e` both refused by name). 855 of 855 caught, every partition rc 0. | `receipts/mutants/*.log`, `*.rc` |
| `fw_coverage.py --selftest` / `--check --jobs 8` | rc 0 / rc 0: 28 of 28 planted cases; coverage PASS on 30 files, `srp_mbx.c` 540/540 lines and 486/486 branches | `receipts/fw_coverage_selftest.log`, `receipts/fw_coverage_check.log` |
| `check_nvm_capture.py` | rc 0: "capture census, clocks, both timing arms and receipt agree". The capture binds `milan_baremetal.c`, which only writes the lwSRP CSRs and compiles no lwSRP source. Neither predecessor nor PR changes it, so the digest is unaffected. | `receipts/docs-gates/15.log` |
| 27 docs/static gates (`run_docs_gates.sh`): `docs_check.py` (+selftest), `check_em_dash.py --base 8c8f82f6` (+selftest), `check_doc_style.py` (+selftest), `DOC_MAP.gen.py --check`, `check_solution_docs.py`, `submodule_boundaries.gen.py --check/--selftest`, `check_submodule_docs.py` (+selftest), `check_diagram_pngs.py` (+selftest), `check_nvm_capture.py`, `measure_test_evidence.py --check`, `check_hygiene.py --check`, `check_cpp_idiom.py`, `check_py_idiom.py`, `ci_events.py --check/--selftest`, `check_doc_paths.py`, `check_archive.py`, `gen_toc.py --selftest/--verify-anchors/--check`, `git diff --check 8c8f82f6 HEAD` | 27 of 27 rc 0. Em dash: 0 findings over 11 added lines in 4 pages. TOC: 143 pages OK; 477 cross-page fragments reproduced. Submodule diagram and docs: OK, 5 exact gitlinks. The renderer-dependent gates ran under the hash-locked `tools/markdown/requirements.txt`, installed in a private environment. | `receipts/docs-gates/summary.tsv`, `NN.log` |
| Walk-reversal probe on the composed tree (`probe_latency_walk.py`) | The pre-#711 single-vector MVRP walk, with the new EndMark assertion, FAILS `SrpLatency.StartupJoinPeriodicAndLeaveAllCommitWithinOneBudget` at IF=1 and IF=2. Exact bytes restored (sha256 equal); the head walk passes at both IFs. | `receipts/probe_latency_walk.log` |
| Clone integrity after probes | HEAD, index tree and worktree equal `24d0b37e…`; no tracked diff in bytes or modes; 0 untracked non-ignored files. All 5 gitlinks match the index, and lwSRP `src/` is clean. | `receipts/clone_integrity.txt` |

## 3. Findings

No new finding. Prior public findings on this PR, resolved or retained at this head:

- **R596-1 S1. SUGGESTION, retained. Lenses: Docs, Conformance.**
  - Location: `sw/firmware/ctrl/srp/README.md:379` (line 344 at the source head; F-INT's text above moved it).
  - Evidence: "(IEEE 802.1Q-2018 10.8.1.2)" can read as a mandate for grouping. The clause permits all three layouts.
  - Composition: unchanged. Optional outcome as R596-1 stated.
  - Verification: read the line.
- **R596-1 S2 / R597-1 S1. SUGGESTION, retained. Lens: Tests.**
  - Location: `sw/firmware/ctrl/test/srp_latency.cpp:76-84`.
  - Evidence: the end-of-walk assertion cannot see a walk that drops the Message EndMark skip, because MVRP has one AttributeType.
  - Composition: unchanged. F-INT does not touch `srp_latency.cpp`. My reversal probe confirms the load-bearing half still holds on the composed tree: the old walk fails.
  - Optional outcome as R597-1 stated.

## 4. Reviewer-owned ledger

| Lens | Result | Examined artifacts (at exact head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | **Touched by the composition**: the grouped lwSRP encoder now runs under F-INT's class-D publication and SRP adapter. Evidence: lwSRP pin ancestry and contract permalinks (section 1); `srpcmp` arm 5/5 controls and 18/18 plants; F4 SRP arms at IF=1/2 and every shape (`receipts/test_ctrl_firmware_arms.log`); issue #711 acceptance 1-5 re-read against the composed tree (1: gitlink `08ee86e8` is the only lwSRP change; 2: arms, coverage and kills, section 2; 3: `check_nvm_capture.py` rc 0 with the digest binding unaffected; 4: diagram, manifest and ledger generator checks rc 0; 5: no shipping-image input changed by the composed diff). | R596-2 | `17834d8f09dfaa5fde513dd7afa3d455b5e0df2c` |
| RTL | CLEAN | **Not touched by the composition.** The composed diff (`receipts/composed_diff.patch`) changes no `.sv`/`.v`/`.tcl`/`.xdc`/SoC file. lwSRP is compiled only into the control firmware and is not in gateware or the capture firmware (`sw/firmware/milan_baremetal/milan_baremetal.c:38-39,1599-1600` writes only the lwSRP CSRs). The lens is covered by the source reviews R596-1 and R597-1 at `49b437f4`; the composed hunks are identical to that head's. | R596-1, R597-1 (source); R596-2 (composition: no RTL scope) | `49b437f445e34b558106c8799c1ffc0a5dc844cf`; composition `17834d8f09dfaa5fde513dd7afa3d455b5e0df2c` |
| Robustness | CLEAN | **Touched**: refusal, retry, backpressure, reset and envelope paths of F-INT's publication with the new encoder. Evidence: arms `srp_rx_retry`, `debug`, `srp_app` (the access envelope 1,676 / 2,486, with named plants for one extra read) and `srp_mbx` at IF=1/2; SRP plants 198/198 and 73/73, including `srp-poll-extra`, `srp-send-extra`, `srp-bound-*` and ROUND5; lwSRP pin refusals 2/2. | R596-2 | `17834d8f09dfaa5fde513dd7afa3d455b5e0df2c` |
| Tests | CLEAN (SUGGESTION retained) | **Touched**: F-INT's tests and plants against the new pin, and this PR's `srp_latency.cpp`. Evidence: 60/60 arms; 855/855 plants; coverage 30 files at 100 %, ratchet held; the walk-reversal probe fails as claimed on the composed tree. Plant tables unchanged by the PR (`git diff 8c8f82f6 HEAD` empty for `*_mutants.py`). | R596-2 | `17834d8f09dfaa5fde513dd7afa3d455b5e0df2c` |
| Docs | CLEAN (SUGGESTION retained) | **Touched**: the three shared docs pages plus `SUBMODULES.md` and the diagram. One account: `08ee86e8` appears in `MAILBOX_SPLIT.md:299`, `ctrl/README.md:353,355`, `srp/README.md:76-77,378-380`, `SUBMODULES.md:26,229`, `ctrl_arms.py:360,363`, `.svg:72` and `.drawio`. The only `9197193e` left is the true PR #15 history line, `srp/README.md:297`. F-INT's envelope and "one frame per call" statements (`MAILBOX_SPLIT.md:731-734`, `srp/README.md:274-283`) still hold under the grouped encoder, since the `srp_app` arms pass. The 27 docs gates are rc 0, including the TOC and anchors. | R596-2 | `17834d8f09dfaa5fde513dd7afa3d455b5e0df2c` |

## 5. Real limits

- **The mutation campaigns ran as 17 partitions through `run_mutants.py`.** It calls the same campaign functions, defect tables and IF=1 selection that `test_ctrl_firmware.py --self-test` uses. It is not the single CLI invocation. The arms ran through the gate's own CLI.
  - The first background attempt was killed by the session and left empty logs; I discarded them and reran everything in the foreground.
  - The first SRP partition run used a relative work path and could not build. Rerun with absolute paths, every partition passed.
- **Not run here** (outside composition scope or authority): parent Verilator/Yosys/PP/gPTP/builder banks, `test_ctrl_nvm.py` (untouched by the PR), act and `act_ci.py --selftest`, hosted runs, Vivado and the shipping-image export.
- **The manager candidate bank `$VALIDATION_STORAGE/711-candidate-0923` was not finished at review time.** There was no `complete.json`, and `manager-builder/results.json` named head `ae2825f5dbe1871550042248e590f97ffc523286`, not this candidate. I relied on none of it.
- **No hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Host toolchain.** GoogleTest and GoogleMock are 1.18.0 and host gcc is 16.2.1, which may differ from the CI distribution packages.

## 6. Pending manager duties

- Complete the candidate banks and publish their receipts for this exact candidate. Reconcile or replace the `manager-builder/results.json` head mismatch noted above.
- Hosted and act acceptance at the merge turn (`rtl-fast` including `firmware-unit`, and the ready-gated suites), distinguishing executed jobs from skipped contexts.
- Current-dev candidate validation at the merge turn, if dev moves past `6bfeeb13` or the F-INT candidate changes.
- Carry the three retained SUGGESTIONs at the manager's discretion. None blocks.

R596-2 FINISHED
