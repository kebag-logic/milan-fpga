[R382] POSITIVE - exact head c7ee5cbd4ed6215b988f3811d5e9156e21aa55c5

# R382-4 internal independent delta review: issue #607 / PR #615 (merge of dev)

Head `c7ee5cbd4ed6215b988f3811d5e9156e21aa55c5`, tree `554756a545927a7e1aba734e2b7d8f4e90ba63cd`.
The parents are `a9f5e34f` (the lane, R382-3 POSITIVE) and dev `7390b43627032c71c470e2aa8d0845eb5b740663` (after #395 / PR #605).
Scope is the merge only, under assignment 5874480647 and gitlink disposition 5874542826.

**Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR is open at this head. All five lenses are covered clean.
This round raises three SUGGESTIONs (S1 Tests, S2 Docs, S3 Docs). None of them affects the verdict.
Every prior public finding on this PR is resolved at this head (section 6).

## 1. Reconstruction and method

**Authorities read, in order:**

- AGENTS.md and CONTRIBUTING.md;
- docs/README.md;
- issue #607: the frozen acceptance 1-4 and every [A10] assignment and disposition comment;
- the #395 margin decision, as cited in BUILDING section 5;
- `git diff 7390b436..c7ee5cbd` and the merge history;
- the published merge-dev packet: branch `607-review-evidence` at `76a45e508b115decef4c10464b72231d749611cd`, path `review-evidence/607-r1/review-evidence/607-r1/author-mergedev/`.

**How the packet was checked.** All 121 blobs were downloaded, and every one hashes to its tree entry.
The assignment's link at `bae7b082` holds only the round-1 packet (see S2).

**Order of work.** Prior review findings were read only after sections 2-5 were drafted.

**What was run.** All scripts are under `scripts/`, and all raw outputs are under `receipts/`.

- **Pins-only environment:** built by the reviewer, following `.github/workflows/elaborate.yml`. `scripts/setup_pins_env.sh` provides:
  - Python 3.12.13, `pyyaml`, and exactly `sw/litex/litex_pins.txt`;
  - `ci_litex_env.py` and `apply.sh`;
  - sv2v v0.0.12, digest-checked;
  - its own HOME and no PYTHONPATH.

  `pythondata_software_picolibc` and `pythondata_software_compiler_rt` are **absent** (receipt 01).
- **Focused tests in that environment:**
  - `sw/builder/test_clock_constraints.py`, which includes the shipping arm (receipt 03);
  - `sw/builder/test_timing_grade.py <python>` (receipt 04).
- **Real shipping elaborations** of `ax7101_1x1_tdm8` and `ax7101_8x8` on e1, graded by `scripts/compose_tcl_check.py` (receipts 05, 06, 12).
- **Six disposable merge-resolution mutants.** Each ran in place and was restored from git (`scripts/merge_mutants.py`, receipt 07).
- **Sweep cross-check** against `sweep-results.json` and `sweep-summary.json`, not the prose (`scripts/sweep_crosscheck.py`, receipt 08).
- **Markdown/docs gates** in the pinned renderer environment (`scripts/md_gates.sh`, receipts 11 and `md/`). The environment is `md-venv-40cdefe08ebd`: cmarkgfm 2025.10.22 and html5lib 1.1, matching `tools/markdown/requirements.txt`, whose sha256 prefix is `40cdefe08ebd`.
- **Hosted checks** at the exact head, read only (receipts 10, 15, 16).

**What was not run:** no Vivado run, no full bank, no act, no hardware.

## 2. Merge-specific verification

### (1) Exactly three conflicts, each resolved with both lanes' behaviour kept. MET

**The conflict set.** `git merge-tree --write-tree a9f5e34f 7390b436` reports exactly three content conflicts:

- `docs/integration/BUILDING.md`;
- `sw/builder/test_builder.py`;
- `sw/litex/platforms/alinx_ax7101.py`.

`LITEX_SOC.md`, `RUNNING_TESTS.md` and `milan_soc.py` auto-merge. The auto-merged tree `80537d5b` differs from the head only in those three files.

**The lane's changes survive unaltered.** For each of the six files both sides touched, the `+`/`-` lines of `dev..HEAD` are identical to those of the lane's `54ce8773..a9f5e34f`. The six lane-only files are blob-identical to `a9f5e34f`.

**`alinx_ax7101.py:297-316`.** The resolution has three parts, in this order:

1. `Xilinx7SeriesPlatform.__init__(TIMING_GRADE["part"])`;
2. `BoundedEthVivadoToolchain()`, when the toolchain is `vivado`;
3. #395's `configure_commands()` pre-placement hooks and the `bitstream_commands` list headed by `kl_timing_grade_reports {build_name}_signoff`.

`clock_constraints.py:53-58` then **appends** the #607 reports to that list rather than replacing it.

**`test_builder.py`** (receipt 02):

- The run list has 96 unique entries: dev's 95 in dev's order, plus `test_clock_crossing_constraints` at the lane's position.
- `test_commercial_timing_grade` and `test_clock_crossing_constraints` are each defined once and run once.
- The `[gate N]` id set equals dev's.

**`BUILDING.md`.** `dev..HEAD` is +30/-0. #395's grade and corner block (`:515-565`) is byte-unchanged. #607's refusal block (`:567-575`) and Ethernet-bound block (`:577-595`) follow it. There is no contradiction:

- #607's build refusal covers emitted diagnostics.
- #395's "not automatically enforced" (`:540`, `:658`) covers slack thresholds, which #607 repeats at `:595`.

### (2) `git diff dev..c7ee5cbd` is only #607's change. MET

- The file set equals the lane's base-to-head set: 12 files, +666/-69.
- There is no `hdl/` file.
- The gitlinks equal dev's: `protocol-processor` `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`, `gptp-processor` `5dce647a`, `external` `efeb541a`.
- The reviewer's elaboration generated `ltn_rom.hex` and `ucode.hex` whose digests equal the `c951a9ff` rows in `syn/yosys/rom_digests.tsv:44-45` (receipts 09, 14).

### (3) Composition in the real emitted Tcl. MET

The reviewer's pins-only elaboration of the shipping `ax7101_1x1_tdm8` places the hooks at these lines:

| Hook | Line |
| --- | --- |
| `synth_design` | 258 |
| `milan_eth_constraints` | 271 |
| `opt_design` | 275 |
| `kl_timing_grade_configure` | 280 |
| `place_design` | 284 |
| `route_design` | 303 |
| `kl_timing_grade_reports alinx_ax7101_signoff` | 314 |
| #607 `report_clock_interaction` | 320 |
| `report_exceptions` | 321 |
| `write_bitstream` | 325 |

- These lines are identical to the `tcl_order` recorded for all three sweep seeds (receipt 12).
- The 8x8 order matches (receipt 06).
- Each hook appears once.
- The XDC carries no `mr_ff` line, no `if` and no hand-typed `crg_` clock name.

**Report names.** #607 writes `alinx_ax7101_clock_interaction.rpt` and `alinx_ax7101_exceptions.rpt`. #395 writes 17 `alinx_ax7101_signoff_*` files (`timing_grade.tcl:38-79`). The two sets are disjoint.

**Timing summary.** The log timing summary (`:309`) runs after `kl_timing_grade_configure` enabled setup and hold at both declared models.

### (4) Three-seed AX7101 1x1 TDM8 re-sweep. MET, from the JSON

The rows below are derived by `sweep_crosscheck.py` from `sweep-summary.json` and `sweep-results.json`. Values are the worst over Slow/Fast at 0 and 85 C.

| Seed | WNS ns | TNS | WHS ns | THS | eth->sys | sys->eth | eth->milan | milan->eth | CW | 12-4739 / 20-1307 / 12-5201 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AltSpreadLogic_high | +0.312 | 0 | +0.036 | 0 | +6.141 | +6.644 | +6.465 | +6.591 | 0 | 0 |
| ExtraTimingOpt | +0.309 | 0 | +0.014 | 0 | +6.279 | +6.719 | +6.583 | +6.591 | 0 | 0 |
| ExtraPostPlacementOpt | +0.063 | 0 | +0.036 | 0 | +6.136 | +6.826 | +6.443 | +6.691 | 0 | 0 |

For every seed:

- **Build:** head `c7ee5cbd`, build rc 0, report rc 0, `--vivado-max-threads 16`, and the directive matches the command.
- **Corners:** all four declared corners are present. WNS >= +0.030 and WHS >= 0 at each. TNS = THS = 0, with no negative paths.
- **Ethernet crossings:** each of the four pairs has 4 corner rows at requirement 8.000 with positive slack.
- **Interaction reports:** all 7 read `Max Delay Datapath Only` at 8.00 for the four pairs, with no `unsafe` row.
- **Log census:** zero CRITICAL WARNING, zero ERROR and zero 12-4739/20-1307/12-5201.
- **Build gate:** it accepted the build, and the bitstream is unquarantined.
- **Hooks:** `quasi_static cells=112` and `budget_ns=8.000` are applied.

The issue's REVIEW READY prose table equals the JSON-derived rows (receipt 08, `SWEEP PASS`).

### (5) Stale statements and Markdown gates. MET

**Statements checked against the combination:**

- `BUILDING.md:515-595,656-659`;
- `LITEX_SOC.md:54-60,155-175`;
- `RUNNING_TESTS.md:155-196`;
- `CLOCK_DOMAINS.md`;
- `sw/litex/sweep.sh:4-8`. The log "Design Timing Summary" it greps is emitted at Tcl `:309`, after `kl_timing_grade_configure` enabled both models, so it still reads the worst declared model;
- the `alinx_ax7101.py:301-303` hook-order comment, which is true, since every #395 hook is configured below the swap;
- the `clock_constraints.py` docstrings;
- the `milan_soc.py:1498-1519` comments;
- `docs/findings/COMMERCIAL_TIMING_395.md`, which is scoped to its pinned checkpoint (S3);
- `docs/findings/PP_SHADOW_BASELINE.md:268,433`, which predates the lane base and is scoped to its artifact.

None is made stale.

**Gates in the pinned environment, all rc 0** (receipt 11):

- `docs_check`: 174 md files;
- `check_em_dash --base 7390b436`: 0 findings over 68 added lines;
- `check_em_dash --selftest`;
- `check_doc_style`, with its selftest;
- `check_doc_paths`: 854 paths;
- `gen_toc` selftest, verify-anchors and check;
- `DOC_MAP --check`;
- `check_hygiene --check`;
- `check_solution_docs`;
- `git diff --check 7390b436 HEAD`.

### Pins-only builder tests and hosted checks

**Pins-only builder tests** (receipts 03, 04). `test_clock_constraints.py` returns rc 0 in 87 s. It prints four `[constraints] shipping ... PASS` lines (1x1/8x8 × e1/e2), and every unit arm passes. `test_timing_grade.py` returns rc 0 with all three `[timing grade]` lines.

The head's `check_implementation_log` was also applied to the published live-plant log, which has vendor rc 0, 3 × 12-4739, 1 × 20-1307 and 1 × 12-5201. It REFUSED the log and quarantined the planted `.bit` (receipts 17, 18).

**Hosted checks at `c7ee5cbd`** (receipts 15, 16, final poll 2026-09-28T20:31Z):

- Run 36477939636 (`rtl-fast`), head `c7ee5cbd`: **success**.
- **Also successful:** `yosys-elaboration`, `verilator-lint`, all four Yosys shards, Verilator shards 0 and 3, `full-ci-gate`, `docs-check-no-git` and `wire-accountability`.
- **Still in progress:** `elaborate` (run 36477939553), `docs-check`, and Verilator shards 1, 2 and 4.
- **Skipped:** `Physical gPTP (nightly and manual)`. It is not executed evidence.

## 3. Merge-resolution mutation probes (receipt 07)

| Mutant | #395 hook test | #607 shipping probe | Reviewer composition check |
| --- | --- | --- | --- |
| Control | green | green | PASS |
| MA: toolchain swap moved after all #395 hooks | **red** | green | **FAIL** |
| MB: swap moved between pre-placement and bitstream hooks | **red** | green | **FAIL** |
| MC: swap deleted | green | **red** (`bounded GMII needs the scoped MultiReg toolchain`) | no Tcl |
| MD: #607 hook replaces `bitstream_commands` | green | green | **FAIL** |
| ME: #607 hook clears `pre_placement_commands` | green | green | **FAIL** |

**What the probes show.** The actual resolution choice, the swap order against #395's hooks, is guarded by committed tests (MA, MB and MC are killed). MD and ME are hypothetical future SoC-level clobbers, not defects at this head, and see S1.

**Restoration.** Every mutant was restored with `git checkout`. After all probes, the clone was verified (receipt 13):

- `write-tree` equals `554756a5…`;
- the worktree and index are clean;
- all 954 tracked blobs rehash to their index entries, and no mode changed;
- the gitlinks equal those listed in item (2);
- the submodules are clean.

The ignored build outputs that the reviewer's runs created were removed.

## 4. Findings

No BLOCKER, MAJOR or MINOR.

### S1 - SUGGESTION - Tests

**Location.** `sw/builder/test_shipping_clock_constraints.py:66-80` and `sw/builder/test_timing_grade.py:146-163`.

**Evidence.** Receipt 07, mutants MD and ME.

- The shipping probe reads the real emitted Tcl but asserts only the Ethernet hook.
- #395's hook test inspects a bare `Platform()`, not the SoC-built toolchain.
- A later SoC-level change that replaced `bitstream_commands` or `pre_placement_commands` would drop the #395 signoff/configure hooks from shipping builds, with both committed tests green.

**Impact.** None at this head: the composition is correct and proven in the emitted Tcl. The gap is future regression coverage for the joint contract.

**Suggested outcome (optional).** In the shipping probe, which already holds the parsed Tcl, also require:

- `kl_timing_grade_configure` before `place_design`;
- `kl_timing_grade_reports` after the last `route_design` and before `write_bitstream`.

**Verification.** MD and ME turn red. The control stays green.

### S2 - SUGGESTION - Docs (evidence discoverability)

**Location.** The merge-dev packet is on branch `607-review-evidence` at `76a45e50`, under the doubly nested `review-evidence/607-r1/review-evidence/607-r1/author-mergedev/`. The review-start evidence link (`bae7b082`) holds only the round-1 packet. The [A427] REVIEW READY comment names no packet URL.

**Impact.** A cold reviewer can find it only by listing branches.

**Suggested outcome (optional).** When the round is published, link the packet's commit and path from the issue or PR, or re-home it at a non-nested path.

**Verification.** The link resolves to `sweep-summary.json` and the other packet files.

### S3 - SUGGESTION - Docs

**Location.** `docs/findings/COMMERCIAL_TIMING_395.md:136-137` and `docs/findings/README.md:12`. Both say that rejected constraints "belong to" and are "owned by" #607.

**Evidence.** Both statements remain true. The record is pinned to the `9e9954e9` checkpoint and `66001a30` source, and that artifact is unchanged.

**Impact.** A reader of the merged tree is not told that the fix has landed, or where.

**Suggested outcome (optional).** When #607 closes, add a one-line forward pointer to BUILDING section 5 and to this PR's merge.

**Verification.** The docs gates stay rc 0.

## 5. Lens results (clean-lens format)

[R382] PASS Conformance - `alinx_ax7101.py:297-316`, `clock_constraints.py:53-58` and `test_builder.py:27795-27826`, against assignment 5874480647 rules 1-4 and #607 acceptance 1-4:

- exactly three conflicts, and the lane's delta is line-identical on dev;
- the emitted Tcl order and the disjoint report names (receipts 06, 12);
- the JSON-derived sweep meets WNS >= +0.030 and WHS >= 0 at every declared corner, with 4 × 8 ns Max Delay Datapath Only pairs and a census of 0 (receipt 08);
- the log gate refuses the live plant (receipt 18);
- the gitlink equals dev's `c951a9ff` (receipt 13).

[R382] PASS RTL - `git diff 7390b436..c7ee5cbd`, with no HDL and unchanged gitlinks; emitted Tcl/XDC for both shipping shapes (receipt 06):

- the CDC exception scope (`clock_constraints.tcl`) sits unchanged before `opt_design`;
- #395's operating-condition setup runs before `place_design`, and its `finally` restore precedes the #607 reports;
- the generated ROM digests equal the `c951a9ff` rows (receipts 09, 14).

[R382] PASS Robustness - `alinx_ax7101.py:301-311`: the swap is guarded by `toolchain == "vivado"`, and each hook is emitted exactly once for both shapes and both ports.

- The swap-order mutants MA and MB are killed. The refusal paths are:
  - a missing swap raises (MC);
  - a rejected log quarantines the `.bit` (receipt 18);
  - an absent firmware data package is refused in pins-only (receipts 01, 03).
- `kl_timing_grade_reports` restores the conditions before the #607 reports run.

[R382] PASS Tests - `test_builder.py` run list (96 unique, each composition arm once, gate ids equal to dev's; receipt 02). `test_clock_constraints.py` and `test_timing_grade.py` pass in pins-only (receipts 03, 04). Merge-resolution mutants MA, MB and MC are killed (receipt 07). S1 is a SUGGESTION only.

[R382] PASS Docs - `BUILDING.md:515-595,656-659`, `LITEX_SOC.md:54-60,155-175`, `RUNNING_TESTS.md:155-196`, `sweep.sh:4-8` and `COMMERCIAL_TIMING_395.md:136`, checked for contradiction and staleness under the combination. The Markdown gates are rc 0 in the pinned environment (receipt 11). S2 and S3 are SUGGESTIONs only.

## 6. Prior public findings on this PR (read after sections 1-5)

| ID | Severity, lenses | Status at `c7ee5cbd` | Evidence |
| --- | --- | --- | --- |
| R382-1 F1 / R383-1 F1 | MINOR; Tests (and Robustness) | **Resolved.** The shipping arm is unchanged from `a9f5e34f`, and it prints four PASS lines at this head | Receipt 03 |
| R382-2 F2 / R383-2 F2 | BLOCKER; Conformance, Tests, Robustness | **Resolved.** The arm passes in a fresh pins-only environment with picolibc and compiler-rt absent, and it does not skip. The hosted `elaborate` job at this head is still in progress (manager) | Receipts 01, 03 |
| R382-1 S3 and the "#605 composition duty" noted by the other reviewer | SUGGESTION | **Discharged.** The swap precedes every #395 hook, and MA and MB, which misplace it, are killed by #395's test | Receipts 06, 07 |
| R382-3 S1 | SUGGESTION; Docs | Unchanged and optional. It concerns issue-comment wording, not the tree | None |
| R383-3 | No findings | None | None |

No prior finding remains open.

## 7. Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Conflict set; lane-delta identity; `alinx_ax7101.py:297-316`; emitted Tcl order; sweep JSON; live-plant log gate; gitlinks | R382-4 | `c7ee5cbd4ed6215b988f3811d5e9156e21aa55c5` |
| RTL | CLEAN | `dev..HEAD`, with no HDL; `clock_constraints.tcl`/`timing_grade.tcl` phase order in the emitted Tcl/XDC; ROM digests at `c951a9ff` | R382-4 | `c7ee5cbd4ed6215b988f3811d5e9156e21aa55c5` |
| Robustness | CLEAN | Toolchain guard; hook uniqueness for both shapes and both ports; refusal and quarantine paths; pins-only package absence; restore-before-report ordering | R382-4 | `c7ee5cbd4ed6215b988f3811d5e9156e21aa55c5` |
| Tests | CLEAN (S1 is a SUGGESTION only) | `test_builder.py` run list and gate ids; pins-only `test_clock_constraints.py`/`test_timing_grade.py`; six merge-resolution mutants | R382-4 | `c7ee5cbd4ed6215b988f3811d5e9156e21aa55c5` |
| Docs | CLEAN (S2 and S3 are SUGGESTIONs only) | BUILDING, LITEX_SOC, RUNNING_TESTS, CLOCK_DOMAINS, sweep.sh, findings records; pinned Markdown gates | R382-4 | `c7ee5cbd4ed6215b988f3811d5e9156e21aa55c5` |

## 8. Real limits and pending manager duties

**Limits:**

- **No vendor run by this reviewer.** The sweep verdict rests on the published, author-collected `sweep-summary.json` and `sweep-results.json`. These were checked for internal consistency and against the prose. The raw per-corner reports are published only as hashes (`sweep-artifacts.json`), so their bytes were not re-hashed here. The reviewer's independent elaboration does reproduce the recorded Tcl line order exactly.
- **Not run, as instructed:** full builder, parent, PP, gPTP and Yosys banks; act; the host `act_ci` selftest. Only focused tests ran.
- **Verilator was not used,** because the delta has no RTL, so its identity was not needed.
- **Physical calibration was NOT RUN.** Skipped hosted contexts, such as `Physical gPTP`, are not hardware proof.

**Pending manager duties:**

- Confirm the exact-head hosted `elaborate` job. It should show the four shipping PASS lines and 96 arms with the same NOT RUN set.
- Confirm `docs-check` and the remaining Verilator shards 1, 2 and 4. All were in progress at the final poll.
- Run act acceptance.
- Build and validate the current-dev candidate merge. Source base and live dev are both `7390b436` at review time.
- Complete post-merge containment.
- Update the PR body for the merge-dev round.
- Obtain the external review.
- Dispose of S1-S3 as desired.

R382-4 FINISHED
