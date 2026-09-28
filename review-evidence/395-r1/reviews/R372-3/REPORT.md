[R372] POSITIVE - exact head 3b5603e3d16a164c35329efeb633800fe4fe9f95

# R372-3: internal independent review of PR #605 for #395 items 1, 2 and 5

- **Head:** `3b5603e3d16a164c35329efeb633800fe4fe9f95`, tree `f4dd44c07795673e8434e145d7e40b355d370ae5`. The PR is open and not a draft. Its head is this commit and its base is `dev`.
- **Delta under review:** `3a0cb4cf..3b5603e3`, one commit (`3b5603e3d`). Its message is one line with no trailers.
- **Full diff:** I also re-read the full diff from `8bc97021f28fb7f729418d3a00851c84ea0b50fd`. It touches 12 files. None is HDL, a constraint source, a build script or a gate script.
- **PR body:** "Relates to #395", with no closing keyword. Items 3 and 4 stay open.
- **Context:** cleared. I rebuilt the task from public material only:
  - AGENTS.md and CONTRIBUTING.md;
  - the #395 body, the owner decision (5789765635), the assignment (5859935504), the margin decision (5860418611) and its correction (5860783553);
  - the round-3 assignment (5860820812) and the executor's TAKEN and REVIEW READY comments;
  - the diff and history;
  - the public evidence branch `395-review-evidence` at `5b4579a6`: the author packets under `review-evidence/395-r1/author`, `author-r2` and `author-r3`, and my own earlier packets `reviews/R372-1` and `reviews/R372-2`.
- **Read order:** I wrote the verdict and ledger below before reading the other reviewer's reports. I read my own round-2 report only after my own pass over the diff, to match suggestion texts. The other reviewer's findings are dealt with under "Prior public findings".

## Verdict summary

- **Round-2 BLOCKER (R372-2-F1):** resolved.
  - `scripts/check_baremetal_only.py --check` returns rc 0 with zero findings over 919 files. `--selftest` passes 700 arms.
  - The hosted `docs-check` step 23 "Bare-metal scope gate" also succeeded at this head.
  - The gate script is unchanged from `8bc97021`.
  - Restoring the old wording (`Ethernet/sys`) makes the unchanged gate fail, rc 1, on exactly that line. The exact head bytes were restored afterwards.
- **S1:** the record now names both LiteX false paths:
  - the MultiReg path at `xdc:566`, on `mr_ff` cells;
  - the AsyncResetSynchronizer path at `xdc:568`, on `ars_ff1`/`ars_ff2` PRE pins.

  It also gives the endpoint class of each crossing. Every count matches the shipping constraints and the round-2 receipt. A new read-only probe confirms that the eight milan-to-Ethernet reset endpoints are `False Path` under the shipping constraints.
- **S2:** the file's own `__main__` now runs `test_pll_grade` when it is given an interpreter. If the literal `-2` PLL speed grade is restored, the standalone entry fails at the changed-part assertion.
- **S3:** the three older locations are aligned, and so are BUILDING's flowchart and section 5, RUNNING_TESTS section 5 and LITEX_SOC section 7. They state WNS >= +0.03 ns and WHS >= 0 at every declared corner. They say the thresholds are **not automatically enforced** and that seed selection is manual. The PLL comment no longer restates the speed grade.
- **S4:** the record gives commit-pinned public locators for `crossings.tcl` and `reports/crossings-results.txt`.
  - Both resolve with HTTP 200, and the commit is reachable from `395-review-evidence`.
  - The results match the record's table.
  - `docs/findings/README.md` lists the record.
- **Scope:** items 3 and 4 remain open. There is no timing or constraint fix. The only code changes are one comment line in `sw/litex/milan_soc.py` and one test line.
- **Findings:** none at MINOR or above. There are four SUGGESTIONs, which do not affect coverage.

## Findings

No BLOCKER, MAJOR or MINOR finding at this head.

### Suggestions (no effect on coverage)

- **R372-3-S1 - SUGGESTION - Docs, RTL - `docs/findings/COMMERCIAL_TIMING_395.md:132-133`.**
  - **Evidence:** the four sys-to-Ethernet reset endpoints and the eight milan-to-Ethernet reset endpoints overlap (`receipts/s1-reset-endpoints-results.txt`).
    - `FDPE_12/PRE` to `FDPE_15/PRE` are in both sets. They are reached from `milansoc_phy_reset_storage_reg` and from `milan_datapath/link_guard/eth_rst_r_reg` respectively.
    - Only `FDPE_18` to `FDPE_21` are unique to the milan set.
    - So the Ethernet domain has 8 distinct reset PRE pins, not 4 + 8 = 12.
  - **Impact:** a reader might count twelve distinct reset endpoints when #607 decides the reset-assertion policy. The per-crossing counts are correct as stated.
  - **Outcome:** optional. Note the overlap here or in #607.
- **R372-3-S2 - SUGGESTION - Docs - `docs/BUILD_FLASH_BOOT.gen.py:26`.**
  - **Evidence:** the AX7101 build-to-boot figure still labels its build gate "GATE: WNS ≥ 0".
    - This PR moved the BUILDING flowchart (`BUILDING.md:49`) and table (`:72`) to the decided rule.
    - The figure is outside item 5's three named documents and is unchanged from `8bc97021`.
    - Changing it would mean regenerating its SVG and PNG.
  - **Impact:** someone reading only the figure sees the older gate.
  - **Outcome:** a follow-up issue, not this lane.
- **R372-3-S3 - SUGGESTION - Tests, Robustness - `sw/builder/test_timing_grade.py:186-190`.**
  - **Evidence:** without an interpreter argument, the standalone entry runs only the contract test. It returns rc 0 and prints no skip line for the platform and PLL controls (`receipts/s2-standalone-entry.txt`).
    - The builder bank records its own skip.
    - No document cites the standalone entry.
    - The silent omission predates this commit.
  - **Outcome:** optional. Print a skip line.
- **R372-3-S4 - SUGGESTION - Docs - `docs/findings/COMMERCIAL_TIMING_395.md:122, 141`.**
  - **Evidence:** the review receipts `r2-v1-crossings-r2-results.txt`, `v2-probe-results.txt` and `v3-crossings-results.txt` are named only through the linked review comments.
    - The author packet now has a commit-pinned locator.
    - The review packets are public on `395-review-evidence` under `review-evidence/395-r1/reviews/R372-2/receipts` and `.../R372-1/receipts`.
  - **Outcome:** optional. Give the review receipts the same commit-pinned form.

## Answers to the assigned checks

1. **The round-2 BLOCKER.**
   - **Gate results:**
     - `--check`: rc 0, 0 findings across 919 tracked first-party files (`receipts/baremetal-check.txt`).
     - `--selftest`: rc 0, 700 arms (`receipts/baremetal-selftest.txt`).
     - Hosted `docs-check` job 108738208969, step 23: succeeded at this head (`receipts/hosted-docs-check-steps-3b5603e3.tsv`).
   - **Gate not weakened:** `git diff 8bc97021f..3b5603e3d -- scripts/` is empty.
   - **Meaning kept:** `:117` reads "Ethernet-to-system crossings remain **unbounded false paths**, in both directions". "system" names the sys clock domain, and the new table gives both directions.
   - **Mutation:** the old spelling makes the unchanged gate fail on `:117` with `[R] prohibited target runtime/service surface '/sys'`, rc 1 (`receipts/probe-baremetal-revert.txt`, `scripts/probe_baremetal_revert.sh`).
   - **Other new lines:** the gate covers the whole tracked tree, so no other line in this PR trips it. The added-line punctuation gate reports 0 findings over 306 added lines from `8bc97021`, and 45 from `3a0cb4cf` (`receipts/docs-static-gates-3.txt`).
2. **S1.**
   - **The exceptions:** `:118-120` names both exceptions and what each targets.
     - Shipping `alinx_ax7101.xdc:566` is `set_false_path -to [get_cells -hierarchical -filter {mr_ff == TRUE}]`.
     - `:568` is `set_false_path -to` the PRE pins of `ars_ff1 || ars_ff2` cells.
     - Source: `receipts/shipping-xdc-560-575.txt`. The xdc hash matches the record.
   - **The table at `:124-129`** matches `r2-v1-crossings-r2-results.txt`.
     - Shipping constraints (part A):
       - eth-to-sys: 13 `mr_ff:D`;
       - sys-to-eth: 12 `mr_ff:D` plus 2 + 2 ARS PRE;
       - eth-to-milan: 50 untagged D;
       - milan-to-eth: 6 untagged D.
     - Exposed crossing (part B): milan-to-eth has 8 ARS PRE and 6 untagged D. The worst endpoints are `FDPE_14/PRE` and `FDPE_18/PRE`.
   - **The masking claim:** part A of that receipt never listed the eight milan-to-eth PRE endpoints. So I checked "Each exception masks its own endpoint class in the shipping constraints" directly, with a new read-only probe of the shipping checkpoint (`scripts/probe_s1_reset_endpoints.tcl`, `receipts/s1-reset-endpoints-results.txt`). At both models:
     - all eight eth-captured PRE paths from the milan clock are `False Path`;
     - the four eth-captured PRE paths from the sys clock are `False Path`;
     - the twelve eth-captured `mr_ff` D paths from the sys clock are `False Path`.
   - **#607:** it gets the reset-assertion decision explicitly (`:136-137`).
3. **S2.**
   - `python3 -B sw/builder/test_timing_grade.py <litex-python>` prints the contract, platform and PLL lines, rc 0 (`receipts/s2-standalone-entry.txt`).
   - With `S7PLL(speedgrade=-2)` restored, the standalone entry fails, rc 1, at `assert pll.call_args.kwargs["speedgrade"] == expected` with `call(speedgrade=-2)`.
   - After the restore it passes and the tree is clean (`receipts/s2-probe-pll-literal.txt`, `scripts/probe_pll_literal.sh`). The same plant survived this entry in round 2.
4. **S3.**
   - **`BUILDING.md:72`** now reads "AX7101 WNS >= +0.03 ns; WHS >= 0 ... **no**: thresholds are not automatically enforced; read the reports and select the sweep seed manually".
   - **`RUNNING_TESTS.md:155-160`** states the rule at every declared corner, the manual seed selection, and "**not automatically enforced**".
   - **The PLL comment at `milan_soc.py:206-207`:** my round-2 S3 bullet for it concerned the stale "speedgrade -2" literal. The comment now says the speed grade is "derived from the declared part". It describes the PLL clock input and speed grade, not the timing gate, so I do not expect it to repeat the margin. The code line at `:216` is unchanged.
   - **Also aligned:**
     - BUILDING contents entry (`:33`), flowchart (`:49`), section 5 (`:537-542`) and gate list (`:626-629`);
     - LITEX_SOC `:159-163`;
     - the record, `:61-66`.
   - **No stale wording remains** outside history: no "comfortable margin", "non-negative post-route" or "already enforces". The only residue is R372-3-S2.
   - **The sweep:** `sweep.sh:2-5` confirms three directives and a manual pick by WNS.
5. **S4 and the retained suggestion.**
   - **Locators:** `:143-146` gives `fa9b0b5373abcb31b2ca6b20c3616b069d8672c4` and blob URLs for `author-r2/crossings.tcl` (2163 bytes) and `author-r2/reports/crossings-results.txt` (1357 bytes).
     - Both return HTTP 200.
     - `395-review-evidence` contains the commit (`receipts/s4-locators.txt`).
   - **The script** runs `reset_timing`, recreates `clk200_p` and `eth_clocks0_rx`, and applies the 8 ns `-datapath_only` bound, as the record says.
   - **Its results** reproduce the record's second table (`:154-158`) value for value.
   - **Findings index:** `docs/findings/README.md:11` lists the record with an accurate scope and state.
6. **Scope.**
   - Items 3 and 4 stay open: "Relates to #395", and the record, BUILDING and LITEX_SOC say so.
   - There is no timing or constraint fix. The `milan_soc.py` change is comment-only. No platform, xdc-emitting or Tcl hook file changed in this delta.

**Other gates at this head**, all rc 0 (`receipts/docs-static-gates*.txt`):
- `docs_check.py` and `check_doc_paths.py`;
- `gen_toc.py --selftest`, `--verify-anchors` and `--check`, with the pinned Markdown renderer environment (its directory name matches the requirements hash prefix `40cdefe08ebd`);
- `check_em_dash.py --base` and `--selftest`;
- `check_doc_style.py` and `--selftest`, `check_solution_docs.py`, `check_feature_status.py`;
- `check_py_idiom.py` and `--selftest`, `ci_scope.py --selftest`;
- `git diff --check 8bc97021..3b5603e3`.

`docs-static-gates.txt` also keeps three invocation errors of mine (rc 2): a missing renderer on the system interpreter, and a missing and an unknown argument. The `-2` and `-3` receipts rerun those three correctly.

## Reviewer-owned ledger

| Lens | Result | Artifacts examined | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #395 body, owner decision, margin decision and correction, round-3 assignment, against: record `:55-70`, `:114-158`; BUILDING `:33`, `:49`, `:72`, `:537-542`, `:626-629`; RUNNING_TESTS `:155-173`; LITEX_SOC `:145-166`; findings index `:11`; PR body (no closing keyword); shipping `xdc:566/568`; `r2-v1-crossings-r2-results.txt`; `receipts/s1-reset-endpoints-results.txt`; `receipts/s4-locators.txt` | R372-3 | 3b5603e3d16a164c35329efeb633800fe4fe9f95 |
| RTL | CLEAN | No HDL in the diff. `milan_soc.py:205-216` (comment-only change; the PLL derivation at `:216` is unchanged); the record's CDC and constraint claims at `:114-137` against shipping `xdc:560-575` and a read-only checkpoint probe at both models (`receipts/s1-reset-endpoints-results.txt`); only R372-3-S1 (SUGGESTION) open | R372-3 | 3b5603e3d16a164c35329efeb633800fe4fe9f95 |
| Robustness | CLEAN | `test_timing_grade.py:186-190` with and without an interpreter argument (`receipts/s2-standalone-entry.txt`); the changed-part control under a restored literal (`receipts/s2-probe-pll-literal.txt`); the gate against the restored forbidden spelling (`receipts/probe-baremetal-revert.txt`); `timing_grade.tcl`, `report_timing_grade.py`, `ax7101_timing.py` and `alinx_ax7101.py` unchanged in this delta; only R372-3-S3 (SUGGESTION) open | R372-3 | 3b5603e3d16a164c35329efeb633800fe4fe9f95 |
| Tests | CLEAN | `sw/builder/test_timing_grade.py:166-190`; `test_builder.py:27556-27564`; standalone runs and the PLL-literal mutation (`receipts/s2-*`); the bare-metal gate check, self-test and restored-wording mutation; hosted `docs-check` step 23 success; docs and static gates (`receipts/docs-static-gates*.txt`) | R372-3 | 3b5603e3d16a164c35329efeb633800fe4fe9f95 |
| Docs | CLEAN | `COMMERCIAL_TIMING_395.md:55-70` and `:108-175`; `docs/findings/README.md:1-12`; BUILDING `:33`, `:44-80`, `:515-560`, `:615-640`; RUNNING_TESTS `:147-178`; LITEX_SOC `:140-166`; the `milan_soc.py` comment; `BUILD_FLASH_BOOT.gen.py:26`; `sweep.sh:1-5`; docs and static gates rc 0; only R372-3-S1, S2 and S4 (SUGGESTION) open | R372-3 | 3b5603e3d16a164c35329efeb633800fe4fe9f95 |

All five lenses are covered clean at the exact head, with no BLOCKER, MAJOR or MINOR open under any lens.

## Real limits

- **Timing analysis:**
  - I ran read-only static analysis of the saved routed checkpoint of `build_ax7101_eto_tdm8dev9e9954e9`, with the installed Vivado 2026.1 (build 6511674) at 8 threads. There was no synthesis, placement, routing or bitstream generation, and nothing was written back.
  - The five shipping inputs were hashed and stat'd before and after. They are byte-identical, their mtimes are unchanged, and the hashes match the record's input table (`receipts/shipping-inputs-before.txt`, `receipts/shipping-inputs-after.txt`).
  - The probe reads timing-path exceptions. It does not prove CDC correctness and does not cover other seeds.
- **Pre-existing constraint defect:** the rejected crossing constraints (`milan_soc.py` clock names) and the unbounded eth/sys false paths are still in the tree.
  - They are on dev and outside this lane by the manager's decision. #607 owns them.
  - The RTL lens covers the diff and the record's claims. It does not certify the shipping constraint set.
- **Scoped Verilator:** not used, because the diff contains no HDL.
- **Not run:** the full builder, parent, PP, gPTP and Yosys banks, and the local act runner. None of them is permitted in this round. The manager's source banks at this head stand as published.
- **Hardware:** physical calibration NOT RUN. No temperature or oscillator measurement was made, so items 3 and 4 remain unmeasured. The skipped "Physical gPTP" context is not hardware proof.
- **Hosted status**, read at 2026-09-28T00:20Z (`receipts/hosted-checks-3b5603e3.tsv`):
  - **Succeeded:** `bdd-conformance`, `changes`, `docs-check-no-git`, `full-ci-gate`, `verilator-lint`, `wire-accountability`, `yosys-elaboration`, Yosys shards 0 to 3, and Verilator shard 3.
  - **In progress:** `docs-check`, `elaborate`, `rtl-fast`, and Verilator shards 0, 1, 2 and 4. In `docs-check`, steps 1 to 26 had succeeded, including step 23 "Bare-metal scope gate", and step 27 "End-station builder gates" was running.
  - **Skipped:** "Physical gPTP".
  - I did not wait for completion. Hosted acceptance is the manager's.
- **Clone integrity after the probes** (`receipts/clone-integrity.txt`):
  - HEAD, the head tree and the index write-tree agree on `f4dd44c0...`.
  - The worktree is clean, including submodules.
  - All 945 tracked blobs match by hash and mode.
  - The four gitlinks match the tree and the index. `external` is unpopulated, as it was at checkout.
  - Public evidence was read through the hosting API, not fetched into the clone.

## Pending manager duties

- Publish this verdict.
- Own hosted acceptance. At review time `docs-check` (the builder and later static steps), `elaborate`, `rtl-fast` and four Verilator shards were still running.
- At the merge turn, run the local replica and build the current-dev candidate (source base `8bc97021`, live dev `63de19bd`).
- Optional relays:
  - R372-3-S1, the overlapping reset endpoint sets, to #607;
  - R372-3-S2, the build-to-boot figure's gate label, as a follow-up.
- Still unowned since round 1, per my earlier reports: GMII RX/TX I/O delay constraints, and triage of the ten Critical CDC diagnostics.
- Automatic enforcement of the +0.03 ns / WHS >= 0 rule is a separate follow-up, per the margin correction.

## Prior public findings

I read the other reviewer's reports (R373-1, R373-2) only after the verdict and ledger above were written. They change neither.

| Prior finding | Status at `3b5603e3` | Evidence |
|---|---|---|
| R372-2-F1 (BLOCKER; Docs, Tests): bare-metal gate fails on the record | **Resolved** | Answer 1. Local `--check`/`--selftest` rc 0; hosted step 23 succeeded; the restored-wording mutant fails the unchanged gate |
| R373-2 R2-F1 (BLOCKER; Tests, Docs): same line, same gate | **Resolved at the gate**; hosted completion pending | Answer 1. The executor's REVIEW READY lists this gate. Its "hosted docs-check succeeds with the builder step executed" clause was still running at review time: step 27 was in progress. That clause is the manager's hosted acceptance |
| R372-2 S1 (xdc:568 attribution) | Resolved | Answer 2 |
| R372-2 S2 / R373-2 S-F (standalone PLL control) | Resolved | Answer 3 |
| R372-2 S3 / R373-2 S-E (older margin wording) | Resolved | Answer 4. Residue in the build-to-boot figure is R372-3-S2 |
| R372-2 S4 (crossing-evidence locator) | Resolved | Answer 5 |
| R372-1 S4 (findings index) | Resolved | `docs/findings/README.md:11` |
| R372-1 F1, F2, F3; R373-1 F1 | Remain resolved | Record, test and hook text within those findings' scope is unchanged in this delta, apart from the S1 and S2 additions verified above |
| R373-1 S1 (margin) and S2 (PLL literal) | Remain resolved | Margin decision cited, now with the correction; the PLL derivation at `milan_soc.py:216` is unchanged |
| R372-1 S1 (the UG835 sentence at record `:57`) | Retained as a suggestion | `:57` unchanged |
| R372-1 S2 / R373-1 S5 / R373-2 S-C (power Tj pinned at 85 C makes `*_power.rpt` worst-case) | Retained as a suggestion | The record mentions power only at `:55` |
| R372-1 S3 / R373-1 S6 / R373-2 S-D (reporter argument edges; directory created before refusal) | Retained as a suggestion | `report_timing_grade.py` unchanged in this delta |
| R373-1 S3 residue / R373-2 S-A (trailing post-restore check mutant survives) | Retained as a suggestion | `timing_grade.tcl` unchanged; `test_timing_grade.py` changed only at `:190` |
| R373-1 S4 / R373-2 S-B (shared LiteX skip text in `test_builder.py:27561`) | Retained as a suggestion | `test_builder.py` unchanged in this delta |
| R373-1 NEW-1 (crossing exceptions never apply) | Owned by #607 | Record `:136-137` |
| R373-1 NEW-2 (GMII I/O delays), NEW-3 (Critical CDC triage) | Outside this lane; still to be filed | Listed under pending manager duties |

None of the retained items is a MINOR or above at this head.

## Publishable receipts

Everything listed in `MANIFEST.sha256`:
- the three probe scripts under `scripts/`;
- the receipts under `receipts/`.

The disposable `scratch/` tree is not published.

R372-3 FINISHED
