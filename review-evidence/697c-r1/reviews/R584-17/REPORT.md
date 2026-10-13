[R584] POSITIVE - exact head 97e713168470bfae2685521fa557dc462b782b32

Internal independent review R584-17 of issue #697 / PR #705, round 19 (merge of dev `d5858bbe`, M8a / PR #721, and the scope extension in #697 comment 6137497435). Exact head `97e713168470bfae2685521fa557dc462b782b32`, tree `e4c0561c897f787ce72c0258fb5caab1c79cf8a1`. This is a delta review from `27ee16b5` (POSITIVE R584-16 and R585-17) to `97e71316`.

All five lenses were applied, each with its own artifacts at this head. No BLOCKER, MAJOR or MINOR is open, so the verdict is POSITIVE. This round records two RESIDUE items (PR-body wording) and two SUGGESTIONs.

## What was reconstructed, and from what

- **Contract.** AGENTS.md, CONTRIBUTING.md and docs/README.md. Issue #697: its body (acceptance 1-5) and the round-19 assignment 6134939296. Also the executor's STOP 6135151826, the scope extension 6137497435 and REVIEW READY 6138131373.
- **Authorities.** `sw/firmware/ctrl/README.md` (boundary section) and `docs/testing/CI_WORKFLOWS.md` (the `firmware-boundary` bullet). The gate's registry `ctrl_configs.py`, its Places taxonomy in `ctrl_boundary.py:30-60` and `:138-152`, and the controls in `ctrl_plants.py` / `ctrl_runs.py`.
- **Diff and history.** `git diff c20c85bd..97e71316` was scoped to the delta `27ee16b5..97e71316`. The merge `95ca54cb` has parents `27ee16b5` and `d5858bbe`. The continuation `97e71316` touches 8 files, +87/-27.
- **Executable evidence.** Every local result below was re-run by this review at the exact head, in this clone or in a disposable probe clone at the same head. I did not consult the author's evidence tree. Hosted logs were read for exact-head jobs only. I read prior public findings (R584-16, R585-17) only after my own pass over the diff.

## Judgement of the round-19 focus items

1. **The conflict resolution keeps both sides.** `git merge-tree --write-tree 27ee16b5 d5858bbe` reproduces the merge tree except for one file, `sw/firmware/ctrl/test/ctrl_srp_image.py`. Its combined diff (`git diff-tree --cc 95ca54cb`) is the docstring only: dev's split-layout sentence plus the lane's stack-source sentence. Everything else auto-merged. The lane's added and removed lines over its merge base `dc4d06cb` equal its lines over dev at the merge (hunk offsets aside).
   - **Dev's side stands:** `import ctrl_memory`, `link()` with `--layout flat|split` (`ctrl_srp_image.py:80-94`, `:107`), the split report (`:194-197`), and `plat/ctrl_split.ld` / `plat/ctrl_split_start.S` blob-equal to dev.
   - **The lane's side stands:** `--stack-source` (`:103`), `source_tree()` with the legacy refusal and `stack_pin()` (`:41-48`), and `lwsrp_pin` (`:138`).
   - No check is dropped or doubled. Receipt: `receipts/merge_resolution.txt`.
2. **The fifth mandatory capture.** `ctrl_configs.py:121` adds `test_ctrl_memory.py --build-only` to `BUILDERS`, the known set the `firmware-boundary` step runs (`rtl-fast.yml:515`). It ran and was judged locally (`boundary_firmware.log:10`, exit 0) and hosted (`hosted_firmware_boundary_markers.txt`).
   - Census over my five captures: `ctrl_split_start.S` is compiled once, only in the fifth capture, and reads only itself (`reset_entry_census.txt`).
   - The full suite's compiles are the same probe and reset entry with the same flags; only the link script varies (`test_ctrl_memory.py:541-588`). Its SoC arm passes `--no-compile-software` (`:668`). So `--build-only` is representative.
   - The extracted `PROBE` and `link` have ASTs identical to `95ca54cb`'s. `PLAT` resolves to the same directory (`probe_extraction_ast.txt`).
   - **Within the 60 % headroom:** hosted `firmware-boundary` (job 115129383559) took 592 s, 32.9 % of 30 min, including the new uncached install. Locally a cold, uncached pip install of that line took 33 s (`pip_cold_install.log`).
3. **The OUTSIDE classifications are true by evidence of what the programs run.**
   - `ctrl_memory.py` imports no subprocess and launches nothing. Its only imports are stdlib and the NVM Python modules at `:330-332`.
   - `milan_soc.py` launches two Python ROM generators (`:996`, `:1007`). It reads the prelinked control ELF at `:2765` and builds the BIOS and `milan_baremetal` only when `--ctrl-mailbox` is off (`:4217-4220`). `milan_baremetal.c:3-17` includes only libc, LiteX-generated and BIOS headers, and no control-tree or stack file.
   - The reason text states exactly that. One vocabulary note is S2.
4. **Each classification has a load-bearing control.** The author's five new controls pass in the gate's self-test, locally (`boundary_firmware.log:36-40`) and hosted. I also ran independent probes on captures made in a probe clone at the head (`receipts/probes.log`, `receipts/probes/`):

   | Probe | Result |
   |---|---|
   | P0 baseline | rc 0 |
   | P1 fifth capture omitted | rc 2, "the capture holds no invocation of sw/litex/test_ctrl_memory.py from a run of its own" |
   | P2 builder removed from `BUILDERS` | rc 2, named |
   | P3 `ctrl_memory.py` unclassified | rc 2, named |
   | P4 `milan_soc.py` unclassified | rc 2, named |
   | P6 a different private stack file in the reset entry (`examples/adp_port.h`, not the author's `string.h`), fifth capture re-made | rc 1, two findings naming `ctrl_split_start.S` and the builder |
   | P7 same planted file judged against the clean fifth capture | rc 0, so the finding comes only through the fifth capture |
   | P5 `PART_OF` entry for `ctrl_memory_probe.py` removed | rc 0, see S1 |

   `--build-only` refuses with rc 2 without an RV32 compiler and fails on a broken reset entry (`build_only_refusals.txt`). Dropping the LiteX pins from the job's install line is refused by `ci_events.py --check` (`ci_contract_probes.txt`).
5. **65/65 images equal dev `d5858bbe`.** I built them independently at the head and at a clean clone of `d5858bbe`, with identical runtime archives: 5 standalone, 30 flat and 30 split runtime images, every shape × 1/2 interfaces × without-SRP/SRP/AECP. All 65 are byte-identical, and the manifests are equal (`images_cmp.log`, `images_head.sha256`, `images_dev.sha256`). Runtime archive caveat: see limits.
6. **The pins are unchanged.** lwSRP is `08ee86e8` at `c20c85bd`, `27ee16b5`, `d5858bbe` and the head. tsn-c-stack is `405dc683` at `27ee16b5` and the head. Both checkouts are verified in `clone_integrity.txt`.
7. **Round 18's bar, re-run at the head by this review.**

   | Run | Result |
   |---|---|
   | Firmware boundary (`--selftest --without verilator`, no capture) | PASS: 2824 sources / 3052 invocations, 0 findings, 110 boundary, 106 pin and 4 figure controls, 0 misbehaved |
   | Verilator boundary (`--selftest --only verilator`, pinned Verilator 5.050) | PASS: 829 / 926, 0 findings, 6 / 106 / 4 controls, 0 misbehaved |
   | The four firmware job commands (`rtl-fast.yml` shards 0-3) | all PASS: 933 `[ok]` = listener 18 + 60 arms + 506 control + 76 AECP + 273 SRP/lwSRP (198 + 73 + 2) |
   | Store | 435 tests across 5 shapes |
   | Coverage | `fw_coverage.py --selftest` 29/29; `--check` PASS, 30 files, every row 100 % lines and branches |
   | M8a memory suite | 0 failures, 44/44 mutants caught |
   | CI contract | `--check` 2169 items; `--selftest` 2169 items / 3064 arms |
   | Other gates | `ci_scope.py --selftest`, `check_py_idiom.py`, and `check_em_dash.py` over `c20c85bd..HEAD` (0 findings, 339/339 arms) |
8. **Hosted runs at the head.** Read at 2026-10-13T04:59:36Z (`hosted_jobs_at_head.tsv`). The jobs ran on GitHub's pull-request merge ref `ba848d8` (the head merged into live dev `49da9fd9`).
   - `docs` succeeded, and so did `elaborate`.
   - In `rtl-fast`:

     | Job | Duration | Share of timeout |
     |---|---|---|
     | `firmware-boundary` | 592 s | 32.9 % |
     | `firmware-verilator` | 648 s | 27.0 % |
     | `firmware-control-mutants` | 919 s | 34.0 % |
     | `firmware-srp-mutants` | 728 s | 27.0 % |
     | `firmware-aecp-mutants` | 273 s | 10.1 % |

     `verilator-lint`, `changes` and `bdd-conformance` also succeeded.
   - Still running: `firmware-unit`, `yosys-elaboration`, `publication-census` and `rtl-full`.
   - Acceptance of the hosted contexts is the manager's.
9. **R584-16-RES-1 and RES-2 in the body.** RES-1 is applied with its exact text (Round 18, item (c)). RES-2 is applied in the table cell and the sentence. The Status bullet it also named no longer exists, because the Status was rewritten for round 19, so the mislabel is gone.

## Findings

### R584-17-RES-1 - RESIDUE - Docs - the PR body calls the published head "unpushed"

- **Artifact:** PR #705 body, `## Status`: "This head is unpushed and still needs independent review and protected hosted evidence." Also `## Round 19`, last paragraph: "No hosted run or PR-head act replica is claimed for this unpushed commit."
- **Evidence:** the PR head is `97e71316`, and hosted runs exist at it: `docs` 38345881726 and `elaborate` 38345881939 succeeded, and in `rtl-fast` 38345881915 `firmware-boundary` succeeded (`hosted_jobs_at_head.tsv`). This is the same wording defect as R584-15-RES-1, R584-16-RES-1 and R585-17-RES-1, now in the round-19 text.
- **Impact:** wording only. No measurement, figure, verdict, test or code depends on it.
- **Exact fix:**
  - Status: replace "This head is unpushed and still needs independent review and protected hosted evidence." with "This head was pushed after this text was prepared; it needs independent review, and its protected hosted runs are the manager's to accept."
  - Round 19: replace "No hosted run or PR-head act replica is claimed for this unpushed commit." with "No hosted run or PR-head act replica is claimed for this commit; it was pushed after this section was prepared, and its hosted runs are the manager's to accept."
- **Verification:** re-read both places.

### R584-17-RES-2 - RESIDUE - Docs - the carried R585-16-RES-1 fix cites a README line that has moved

- **Artifact:** PR #705 body, `## Round 18`, Residue paragraph: "in `sw/firmware/ctrl/README.md:181`, "and no key that names a program, …"".
- **Evidence:** at the head that sentence is `sw/firmware/ctrl/README.md:193`. The merge and the continuation added lines above it. The text is unchanged, and `ctrl_build.py:199` and `:551-552` are still exact.
- **Impact:** wording only. The carried fix still names its text verbatim.
- **Exact fix:** in that paragraph, replace "`sw/firmware/ctrl/README.md:181`" with "`sw/firmware/ctrl/README.md:193` (`:181` before round 19)".
- **Verification:** `grep -n 'no key that names a program, a promisor remote or its transport' sw/firmware/ctrl/README.md` prints 193.

### R584-17-S1 - SUGGESTION - Tests, Docs - the `PART_OF` entry for `ctrl_memory_probe.py` is not load-bearing

- **Artifact:** `sw/firmware/ctrl/test/ctrl_configs.py:140`. The PR body Round 19 table says "its shared probe module is PART_OF that builder at line 140".
- **Evidence:** probe P5 deletes the entry, and the gate still passes on five fresh captures (`receipts/probes/gate-P5-probe-unclassified.log`). The module has no `__main__` block and compiles in the capture, because the audit hook names it on the reset-entry compile (P6's findings list `sw/litex/ctrl_memory_probe.py`). So the registry's module rule (`ctrl_configs.py:24-27`) already holds it. The `--only verilator` run skips the text cross-check altogether.
- **Impact:** none on the boundary. The entry is true, but no control shows it matters. The ruling asked for load-bearing controls for the three M8a programs, and those exist.
- **Suggested outcome:** drop the entry or say in the body that it is documentary, or plant a control that only it satisfies.

### R584-17-S2 - SUGGESTION - Conformance, Docs - "the firmware's" means two things where `milan_soc.py` is classified

- **Artifact:** `ctrl_configs.py:148` ("whose compiles, if any, are none of the firmware's") and `:151-152`, against `ctrl_boundary.py:53-58` and `FIRMWARE_REL = "sw/firmware"` at `:142`.
- **Evidence:**
  - The registry defines the firmware's tree as `sw/firmware/ctrl` (`ctrl_configs.py:22`).
  - Under that meaning, `milan_soc.py`'s compiles (BIOS, `sw/firmware/milan_baremetal/milan_baremetal.c`) are none of the firmware's. The reason text says exactly what is excluded, "compile no control-stack source", which is true by the include list.
  - The gate's Places taxonomy, however, calls every file under `sw/firmware` outside test equipment "the firmware's", and that covers `milan_baremetal.c`.
  - The ruling's own condition ("If either does compile firmware, treat it like test_ctrl_memory.py") is met only under the broader reading. The executor stated the narrower reading publicly for review. The uncaptured `milan_baremetal` compile predates this PR, since `milan_soc.py` was never found by text before M8a's help string.
- **Impact:** none today, because `milan_baremetal.c` reads no stack or control-tree file. A future stack include there would not be judged by this gate, as before this PR.
- **Suggested outcome:** say in the `OUTSIDE` comment, or in the README's boundary paragraph, that "the firmware's" there means the control firmware's tree and the stack, and that `milan_baremetal` is outside the capture. Alternatively, record the manager's acceptance of the narrower reading on #697.

## Prior public findings at this head

| Finding | Status at `97e71316` | Evidence |
|---|---|---|
| R584-16-RES-1 (Round 18 (c) "head not pushed") | APPLIED with its exact text | live PR body, Round 18 item (c) |
| R584-16-RES-2 (merge-versus-head timing label) | APPLIED: the table cell and the sentence are exact. The Status bullet it named was replaced by the round-19 Status, so no mislabel remains. | live PR body |
| R585-17-RES-1 (same pushed-head correction) | APPLIED (same exact text) | live PR body, Round 18 item (c) |
| R585-16-RES-1 (allowlist "names a program") | RETAINED RESIDUE, carried. The text is unchanged at `README.md:193` (was `:181`; see RES-2), `ctrl_build.py:199`, `:551-552`. | source |
| R584-16-S1 / R585-17-S1 (boundary timeouts unpinned) | RETAINED SUGGESTION. `firmware-boundary` 30→31 still passes `ci_events.py --check` at this head. The new install line is pinned. | `receipts/ci_contract_probes.txt` |
| R584-15-S1, R585-16-S1, R585-14-S1/S2/S3, R584-13-S1, R585-13-S1/S3, R584-11-S1, R584-9-S1, R585-2-S2, R584-8-RES-1, #495 residue | RETAINED. The files they name are untouched by `27ee16b5..97e71316`, apart from the README line shift above. Not re-verified one by one. | `git diff --stat 27ee16b5 97e71316` |

## Lens results

[R584] PASS Conformance - receipts/merge_resolution.txt, images_cmp.log, images_head.sha256, images_dev.sha256, clone_integrity.txt; ctrl_configs.py:121,140,150-152; milan_soc.py:996,1007,2765,2774,4217-4220; ctrl_memory.py:34-42,330-332; sw/firmware/milan_baremetal/milan_baremetal.c:3-17 - The assignment and the extension are checked item by item. Both sides of `ctrl_srp_image.py` stand and no other file differs from a clean 3-way merge. There is a fifth capture, the three programs are classified on what they run, and 65/65 images equal dev `d5858bbe`. Pins are unchanged, and #697 acceptance 1-5 is unaffected. S2 is vocabulary only.

[R584] PASS RTL - git diff --stat 27ee16b5 97e71316 (no .sv/.v/.vh; only sw/firmware/ctrl/plat/ctrl_split.ld and ctrl_split_start.S from dev, blob-equal to d5858bbe); test_ctrl_memory.py:541-588 and :621-672 (SoC child runs with --no-compile-software); rtl-fast.yml:484-515 (needs/if/timeout unchanged) - No HDL is in the delta. M8a's reset entry and linker script enter unchanged, and their linked images equal dev's at both layouts. The CI job graph is unchanged but for the install line.

[R584] PASS Robustness - receipts/build_only_refusals.txt, probes.log (P1-P4, P7), ci_contract_probes.txt, pip_cold_install.log, memory_build_only.log - Without RV32, `--build-only` refuses with rc 2 by name. A broken reset entry fails the build, which fails the gate. A missing fifth capture is refused by name; a stale one yields no finding. The job's new dependency is pinned by the CI contract, and in an unpatched pinned-only venv the build-only run passes (rc 0). The firmware-verilator job neither needs nor runs it (named LEFT OUT).

[R584] PASS Tests - receipts/boundary_firmware.log (110/106/4, 0 misbehaved; the five new controls at :36-40), boundary_verilator.log (6/106/4), hosted_firmware_boundary_markers.txt, probes.log and probes/ (P0-P7), fw_shard0-3.log, store_suite.log, coverage.log, memory_suite.log (44/44), ci_events_selftest.log, ci_scope_selftest.log, reset_entry_census.txt, probe_extraction_ast.txt - Each new control fails for the defect it names, confirmed independently with a different plant file and with registry deletions. Round 18's bar holds at the head: firmware 915 verdicts plus 18 listener, store 435, coverage 30 files at 100 %, and both boundary sides. S1 notes one classification no control needs.

[R584] PASS Docs - sw/firmware/ctrl/README.md:126-133,159-164; docs/testing/CI_WORKFLOWS.md:76-79; ctrl_configs.py:100-101,137-152; test_ctrl_memory.py:53-55; PR #705 body Status/Round 18/Round 19 (line references at ctrl_configs.py:121/140/150/151, milan_soc.py:2765/2774/4217, ctrl_plants.py:193, rtl-fast.yml:499, ci_events.py:2450 all verified); em_dash.log; figure controls in boundary_firmware.log:251-254 - The fifth capture, its dependency, the classification reasons and the 101/8 control counts are stated and true; the README figures are held by the gate's own figure controls. Two wording residues (RES-1, RES-2) go to the checklist, and S2 is a vocabulary suggestion.

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | merge 3-way reproduction, `ctrl_srp_image.py` both sides, registry, `milan_soc.py` / `ctrl_memory.py` / `milan_baremetal.c` compile paths, 65-image comparison, pins | R584-17 | `97e713168470bfae2685521fa557dc462b782b32` |
| RTL | CLEAN | delta file list (no HDL), `ctrl_split.ld` / `ctrl_split_start.S` from dev, split/flat images, `rtl-fast.yml` job graph | R584-17 | `97e713168470bfae2685521fa557dc462b782b32` |
| Robustness | CLEAN | build-only refusal paths, capture-missing/stale probes, CI-contract pin of the install line, pinned-only venv run | R584-17 | `97e713168470bfae2685521fa557dc462b782b32` |
| Tests | CLEAN (SUGGESTION S1) | both boundary sides with self-tests (local and hosted firmware side), P0-P7, four firmware jobs, store, coverage, memory suite 44/44, CI contract/self-test | R584-17 | `97e713168470bfae2685521fa557dc462b782b32` |
| Docs | CLEAN (RESIDUE RES-1, RES-2; SUGGESTION S2) | README boundary section, `CI_WORKFLOWS.md` boundary bullet, registry comments, `--build-only` docstring, PR body sections and line references, em-dash gate | R584-17 | `97e713168470bfae2685521fa557dc462b782b32` |

## Real limits

- **Runtime archives for the image comparison** were built from the bench's picolibc, compiler-rt and LiteX sources. They used `ctrl_image_runtime.py`'s command plus `-fno-stack-protector` (`scripts/runtime_nossp.py`), because this SDK enables stack protection by default and the unmodified archives left `__umoddi3` unresolved in the AECP links. The same archives were used for both sides, so the comparison is fair. My manifest hash (`c5d041f1…`) is therefore not comparable with the author's (`96f55deb…`).
- **Harness errors I corrected.** My first comparison run (`images_compare.log`, rc 1) reported 65 byte differences while its SHA-256 manifests were equal. The fault was a path bug in my compare loop, fixed in `scripts/compare_images.sh`. `images_cmp.log` is the corrected byte comparison over the same ELFs. Similarly, my first memory-suite run, before the documented LiteX provisioning (VexiiRiscv source plus the five repository patches), failed only in the SoC arm. It is not published; the receipt is the provisioned run.
- **Not re-run by this review:** the entry-point (252), hook-rule, configuration-variant and Git/Python-matrix campaigns, the disposable runner self-test, the store `--self-test` mutation campaign, and the docs job's full command list. No file those campaigns exercise changed in `27ee16b5..97e71316`, except the registry and plants that the boundary self-test covers. Their figures are the author's.
- **Local environment.** Local runs used CPython 3.12.13, Git 2.56.0, the pinned RV32 SDK and the pinned Verilator 5.050 (identity checked: `Verilator 5.050 2026-07-01 rev v5.050`). Host compilers are this machine's, not the runner's Ubuntu 24.04. The coverage rows are this compiler's.
- **Hosted ref.** Hosted jobs ran on the pull-request merge ref `ba848d8` (the head plus live dev `49da9fd9`), not on the bare head. They are cited as exact-head contexts only in that sense.
- **No manager source bank** ran at this head, and none is claimed or inferred. Physical calibration was NOT RUN. Skipped hosted contexts are not evidence. No hardware was touched.

## Pending manager duties

- Hosted acceptance at `97e71316`. When this report was written, `firmware-unit`, `yosys-elaboration`, `publication-census` and `rtl-full` were still running.
- The current-dev merge candidate (source base `c20c85bd`, live dev `49da9fd9`) and its builder and native banks at the merge turn.
- Carry R584-17-RES-1, R584-17-RES-2 and the retained R585-16-RES-1 to the residue checklist with their exact fixes. S1, S2 and the retained suggestions are optional. S2 also asks the manager to confirm or reject, on #697, the narrower reading of "compiles firmware" applied to `milan_soc.py`.

R584-17 FINISHED
