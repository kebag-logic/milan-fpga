[R605] NEGATIVE - exact head ef86ea848dbfb0d869108a1987accb203a17474d

# R605-1: external independent review of PR #175 (issue #151)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #175, closes #151.
- Exact head `ef86ea848dbfb0d869108a1987accb203a17474d`, tree `544a270ded252e41a8eccb89c3f4d367b7780722`; source base `2cbed0a987c1e68402658d69459ab7e5aa571adc`; three commits (9385799, eb7e596, ef86ea8).
- Review start: PR #175 comment 6105271131. Reviewer role: external, cleared context, isolated detached clone.
- Verdict: **NEGATIVE**. The engineering is sound and every executable claim I re-ran reproduced. Two MINOR documentation findings stay open: F1 (Docs, Conformance) and F2 (Docs). Either one makes the verdict NEGATIVE under the review rules.

## 1. What was reconstructed, in order

1. Repository conventions. The repository has no `AGENTS.md` or `CONTRIBUTING.md`, so I read `README.md`, `docs/README.md` (ID registries, figure rules, editing workflow), `hdl/README.md` and `docs/guides/hdl-engineer.md` instead.
2. Issue #151: the body (frozen acceptance) and the manager's lane-scope comment 6098621173. The issue has no other scope decision.
3. The authorities. The coding rules are `hdl/README.md` and the HDL engineer guide §2. The integration contract is `docs/guides/integrator.md` §2 plus diagram 21. The verification doc is `docs/architecture/09_verification.md` §8.
4. The diff `2cbed0a9..ef86ea84` (29 files) and its history, read line by line.
5. Public executable evidence: `kebag-logic/milan-fpga@bda25e67…/review-evidence/pp151-r1`.
   - I hashed every downloaded file against its `MANIFEST.json`: 340 of 340 match.
   - I did not read the two narrative files (`author/HANDOFF.md`, `author/PR-BODY.md`). The PR body itself was read on the PR.
6. Manager comments on the issue and the PR: lane scope, TAKEN, REVIEW READY, and the two review-start notices. Neither the issue nor the PR carries a manager evidence comment yet.

## 2. Findings

### F1 - MINOR - Docs, Conformance - the integrator's contract still says the top's guards raise `$error`

- **Where:**
  - `docs/guides/integrator.md:114`: "exceeding either raises `$error` rather than silently aliasing a timer slot".
  - `docs/diagrams/21-integration-faces.svg:53`: "An over-large stream shape stops the build with $error."
- **Authority / evidence:**
  - At this head, every guard in `protocol_processor_top.sv` (lines 876, 880, 884, 897, 911) is `$fatal(1, …)`.
  - The new coding rule (`hdl/README.md` rule 6; HDL engineer guide §2 row and §2.1) forbids `$error` in a guard.
  - Both statements were true at base, and this PR's own change makes them false.
  - The PR body lists them as "outside this PR's scope and left as they are". Scope cannot cover them: the PR is what made them wrong.
  - Diagram 21 is the published integration-contract figure ("the integrator's contract", README diagram table).
- **Impact:**
  - The integration authority now names a severity the RTL no longer uses, and that severity is the one this PR measured as not stopping sv2v 0.0.13 + Yosys.
  - The integrator guide and the HDL engineer guide now contradict each other.
  - This is not RESIDUE: one half is a figure, which `docs/README.md` §3 requires to be edited, rendered and inspected.
- **Required outcome:**
  - In `integrator.md:114`, replace "raises `$error`" with the `$fatal` wording.
  - Change the SVG text to "…stops the build with $fatal." Render it to a scratch PNG and look at it, per `docs/README.md` §3. The new word is the same length, so the layout should not move.
- **Verification:**
  - `grep -rn '\$error' docs/` should leave only the measurement rows of HDL engineer guide §2.1.
  - `make check` stays rc 0, with `figures` OK.

### F2 - MINOR - Docs - the recorded rule says Verilator reports all four severity tasks as warnings; it does not report `$info` as one

- **Where:**
  - `docs/guides/hdl-engineer.md:91`: "Verilator reports all four tasks as warnings, so a guard stops a lint by its exit status".
  - `tb/elab_guards/README.md:5`: "Verilator lint reports all four as warnings".
  - `tb/elab_guards/guards.py:8` (module docstring): "Verilator lint reports every severity as a warning".
- **Authority / evidence:**
  - Issue #151 asks for the rule to be "recorded in the coding rules" with "the measurement behind it".
  - My own one-guard probe through Verilator 5.050 with `lint_hdl.sh`'s flags (`receipts/verilator_info_probe.txt`): a violating module-scope `$info` prints `-Info: r605_info_mod.sv:6:5: …` and exits **0**. It is not a warning, and it does not stop the lint.
  - The guide's own §2.1 table (row "module scope `$info`": **elaborates**) and my re-measurement (`receipts/form_table.md`) agree with the probe. The sentence contradicts the table it sits under.
  - The issue body itself said "all three" (`$fatal`, `$error`, `$warning`). This PR changed it to "four".
- **Impact:**
  - The coding-rule record misstates the measured behaviour it exists to record.
  - A reader of the prose could conclude that any severity stops `lint_hdl.sh`, which is exactly the misconception the rule guards against.
  - I classed it as MINOR, not RESIDUE, for two reasons. It misstates a tool measurement in the normative coding rules. One of the three copies is in a code file. Per the rules, a case where it is unclear whether the defect is only wording is MINOR.
- **Required outcome:** in all three places, say that Verilator reports `$fatal`, `$error` and `$warning` as warnings (`USERFATAL`, `USERERROR`, `USERWARN`), and reports `$info` as `-Info` with exit status 0.
- **Verification:** reread the three sentences against `receipts/verilator_info_probe.txt` and the §2.1 table. No test or measurement changes.

### S1 - SUGGESTION - Tests - the `< 1` boundary of three deadline guards is not graded

- **Where:** `tb/elab_guards/guards.py:83-84, 114-117`. These are `KL_acmp_nvm_shadow.g_rs_tmo_check`, `KL_aecp_nvm_writer.g_rs_tmo_check` and `g_rs_agg_check`.
- **Evidence:**
  - Their passing case is 2, not 1. This is documented: at 1 the module lints with `UNSIGNED`.
  - My mutant R6 tightens `RS_TMO_CYC_P < 1` to `< 2`, and it **survives** the bench (`receipts/probes/R6-shadow-rs-tmo-tightened-to-2.log`).
  - Conditions are unchanged by this PR (verified by diff), so this is not a defect of the PR. The bench's purpose is the severity class, and it meets that purpose.
- **Suggestion:** grade value 1 as "refused by no guard". Accept a lint `UNSIGNED` there but no `USER*` line, and require a clean elaboration in the Yosys and Vivado legs.

### S2 - SUGGESTION - Robustness - the inventory scope

- **Where:** `tb/elab_guards/guards.py:183-192`.
- **Evidence:** the inventory reads `hdl/**/*.sv` only and strips `//` comments only. A future guard in an included `.svh`/`.vh` would escape it. A `/* … $error … */` block comment would be flagged; that is fail-safe.
- **Suggestion:** glob `*.sv*`/`*.vh`. Today `hdl/` has neither (verified).

No other defect found. Section 4 lists what was checked and found correct.

## 3. Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | **UNCLEAN** (F1) | issue #151 acceptance and lane scope against the diff; inventory (independent grep: 31 severity tasks, 13 files, matches `GUARDS` and the PR table); condition-unchanged check (32 changed RTL lines, 29 pure `$error(`→`$fatal(1, ` substitutions plus the listener's 3-line move); coding-rule record (`hdl/README.md` rule 6, HDL engineer guide §2/§2.1); integration contract (integrator guide §2, diagram 21) | R605-1 | ef86ea848dbfb0d869108a1987accb203a17474d |
| RTL | CLEAN | all 13 changed RTL files: no line moves (line counts equal), messages unchanged, continuation columns unchanged, listener guard now a named module-scope generate block; sv2v-lowered trees (0.0.12 and 0.0.13) differ only on guard task lines and the listener wrapper; 42 of 42 netlists equal base vs head | R605-1 | ef86ea848dbfb0d869108a1987accb203a17474d |
| Robustness | CLEAN (S2) | the bench's grading paths (`grade`, `where`, `labelled`, `planted`); failure modes probed by 10 reviewer mutants (initial-in-block, `$info`, `$display`, label rename, `lint_off USERFATAL`, `$fatal(0, …)`, tightened condition); `elab_bounds.sh` Yosys leg; the hosted Verilator-only shape (93 checks, `YOSYS SKIP`); parent at live dev | R605-1 | ef86ea848dbfb0d869108a1987accb203a17474d |
| Tests | CLEAN (S1) | `tb/elab_guards` (155 of 155 at head under sv2v 0.0.12 and 0.0.13; 62 of 156 FAIL on the base tree); `mutants.py` re-run under both sv2v (98 of 98 killed, each); reviewer mutants 8 of 8 killed and 2 of 2 equivalence/boundary survivals as predicted; `tb/nvm_port` elab (head both sv2v rc 0, base 0.0.12 rc 2 as stated); `tb/pp_top` if/line guards; focused suites `acmp_listener` 3167 and `nvm_port` 1219 checks = author's head record; 298 of 298 `tb/` patches apply | R605-1 | ef86ea848dbfb0d869108a1987accb203a17474d |
| Docs | **UNCLEAN** (F1, F2) | HDL engineer guide §2 row and §2.1 (table re-measured: 3 of 5 columns reproduced cell for cell; Vivado columns from author receipts), `hdl/README.md` rule 6, `tb/elab_guards/README.md`, `tb/nvm_port/README.md`, `tb/pp_top/README.md`, changed script docstrings, integrator guide §2, diagram 21, 09 §8 (suites are globbed, so the absence of an `elab_guards` row is not a defect); `make check` rc 0 at base and head | R605-1 | ef86ea848dbfb0d869108a1987accb203a17474d |

## 4. Evidence, per acceptance item

The receipts are under `receipts/` and the scripts under `scripts/`. Toolchain:

- Verilator 5.050: the scoped binary, identity verified with `--version`.
- sv2v 0.0.12: the official release binary. Its zip sha256 `ff8c9eea5bc0…` matches the PR, and the binary sha256 `b29952bc…` equals the extracted release binary.
- sv2v 0.0.13.
- Yosys 0.66 (`86f2ddebc`, distribution build).

**A. Inventory complete; no condition changed.**
- An independent grep of `hdl/` for `$fatal|$error|$warning|$info|$finish|$stop|initial|final|assert` finds exactly 31 guard tasks at the PR's 31 file:line positions. The only other `initial` blocks are two `$readmemh` and one memory clear.
- There is no `.svh`/`.vh` file, and no other guard idiom (`static_assert`, divide-by-zero, missing module).
- Pairing every removed RTL line with its added line leaves 29 lines that differ only by `$error(` → `$fatal(1, `, plus the listener's move. The `if` condition is byte-identical.

**B. Per guard, per front end: refused in the tool's own words; the nearest passing set elaborates.**

| Run | Result | Receipt |
|---|---|---|
| Bench at head, Verilator + Yosys, sv2v 0.0.12 | 155 of 155 | `receipts/head_bench_sv2v012.log` |
| Bench at head, Verilator + Yosys, sv2v 0.0.13 | 155 of 155 | `receipts/head_bench_sv2v013.log` |
| Hosted shape (Verilator only) | 93 of 93, `YOSYS SKIP` | `receipts/head_elab_guards_verilator_only.log` |
| The head bench graded on the base tree | 62 FAIL: 30 Verilator (29 `USERERROR`; the listener refused only by an unrelated `ASCRANGE`), 30 Yosys (`ERROR: <message>` / `Can't resolve task name`), 2 inventory | `receipts/base_by_head_bench_sv2v012.log` |
| One-guard form table | Verilator and both Yosys columns reproduce the guide's §2.1 table exactly | `receipts/form_table.md` |
| Vivado xelab and `synth_design` | author receipts at this head: 31 GUARD + 31 ELAB per leg, 155 of 155; base 33 FAIL; mutation sample 14 of 14 | public evidence, hash-verified |

Vivado is not installed on the review host, so I did not re-run the Vivado legs.

**C. Severity graded; mutants killed by name.**

The author's campaign, re-run here:

| Toolchain | Killed | Notes | Receipt |
|---|---|---|---|
| sv2v 0.0.12 | 98 of 98 | error, warning and initial arms each killed by both legs | `receipts/head_mutants_sv2v012.log` |
| sv2v 0.0.13 | 98 of 98 | initial arms killed by Verilator alone, as the README states | `receipts/head_mutants_sv2v013.log` |

Reviewer-owned independent mutants (`scripts/my_mutants.py`, `receipts/reviewer_probes_sv2v012.log`, per-probe logs in `receipts/probes/`):

| Probe | Mutation | Result |
|---|---|---|
| R1 | listener restored to its base `initial` form | KILLED: inventory, Verilator, Yosys |
| R2 | encoder `$info` | KILLED: both legs |
| R3 | notify `$display` | KILLED: inventory |
| R4 | `initial $fatal` inside the generate block, top owner guard | KILLED: both legs |
| R5 | `$fatal(0, …)` | survived; equivalent, as expected |
| R6 | deadline tightened | survived; see S1 |
| R7 | `$error` on the planted `gen_g_tmr_aw` | KILLED: both legs |
| R8 | originator `$warning` | KILLED: both legs |
| R9 | label renamed | KILLED: inventory |
| R10 | `lint_off USERFATAL` | KILLED: Verilator leg |

Changed consumer benches:
- `tb/nvm_port` elab passes at head under both sv2v.
- At base under sv2v 0.0.12 it fails with `failed, but not at the guard's $finish`, which is the PR's pre-existing finding.
- `tb/pp_top` if- and line-guards pass, and 298 of 298 patches apply.

**D. No passing elaboration changes.**
- The sv2v-lowered `all.v` at base vs head differs only on guard task lines and the listener's `initial`→`generate` wrapper, under both sv2v (`receipts/lowered_allv_base_head_sv2v01{2,3}.diff`).
- Netlists: 42 of 42 EQUAL (`receipts/netlists_all.log`, `scripts/netlists_all.sh`). That is `protocol_processor_top` at nine shapes (default, 1x1, 2x2, 4x4, 5x5, 8x1, 1x8, 16x16, 9x9 at two AVB interfaces) plus the 12 other guard-carrying modules at defaults, under each sv2v.
  - Method: elaborated as `run.sh` does, `autoname`, `write_verilog -noattr`, source positions masked, auto-names renumbered by first appearance, line order kept.
  - A first pass without `autoname` showed only declaration-order noise from Yosys counter names (`receipts/netlists_first_pass_order_noise_sv2v012.txt`). The `autoname` pass resolves it.
- ROM digests: `ucode.hex` `518b900c…` and `ltn_rom.hex` `23cc67ee…`, identical at base and head (`receipts/rom_digests.txt`).
- `lint_hdl.sh`: 41 `LINT OK`, base and head logs identical.
- `make check`: rc 0. The only differences are `links 1187→1191` and `ids 563→567` (the files and links this PR adds).
- `gen_matrix --check`: 94 rows, 0 untested, identical.
- The author's suite records differ only by the added `elab_guards` line and the total (1,029,620 + 155 = 1,029,775).
- The author's OOC Vivado netlist digests are equal base vs head at default and 9x9.

**E. Scratch parent at live dev ac2c5e77.**
- `ac2c5e77` is 15 commits ahead of the author's `e8454e27`. The delta touches docs, LiteX Python and one gPTP bench file; it changes no parent HDL and moves no gitlink. The author's parent receipts at `e8454e27` (lint gate PASS identical, Yosys elaborate 61 tops identical, 0 USER diagnostics at the five shipping configs) therefore carry to live dev for this change.
- Independent focused check at `ac2c5e77`, with `protocol-processor/` set to this head (`scripts/parent_shapes.py`, `receipts/parent_ac2c5e77_head_shapes.log`):
  - `milan_datapath` linted as `lint_rtl.lint_one` builds it, at `endstation_arty_current`, `_arty_4x4`, `_arty_8ch`, `_ax7101_1x1_tdm8` and `_ax7101_8x8`: 0 USER diagnostics, 0 hard errors.
  - Positive control `KL_pp_shadow -GN_STREAM_IN_P=40`: the processor's `USERFATAL` is seen, at `protocol_processor_top.sv:911` and `KL_aecp_nvm_writer.sv:315`.
- **No shipping shape trips a guard.**

**Hosted CI at this head** (snapshot `receipts/hosted_checks_snapshot.txt`, 2026-10-11T04:40Z): docs-gates and portability succeeded in both runs; both `suites` jobs were still in progress. These are executed jobs, not skips. Hosted acceptance belongs to the manager.

## 5. Prior public review findings

No public review finding existed on PR #175 before this round. At my independent pass, the PR carried only the two manager review-start comments, with no reviews and no review comments. There is nothing to resolve or retain.

## 6. Real limits

- Vivado is not installed on the review host. For the xelab and `synth_design` legs, the Vivado mutation sample (14 arms, not all 93) and the OOC netlist identity, I rely on the author's hash-verified receipts at this head.
- I used the distribution build of Yosys 0.66 (`86f2ddebc-dirty`), not a tag build.
- The full banks were not run, by rule: `run_suites.sh`, `syn/yosys/run.sh`, the parent `lint_rtl.py --check` and the parent Yosys elaboration. I ran focused equivalents and used the author's receipts for the rest.
- My parent check is Verilator-only, at live dev. The parent's Yosys stop on a processor guard comes from the author's statement and receipts at `e8454e27`.
- No manager source bank ran at this head, and none is inferred. The merge-turn current-dev candidate (builder and native banks) is distinct from this source review.
- Physical calibration was NOT RUN. Field skips are not hardware proof. No hardware was used.

## 7. Pending manager duties

- Validate the current-dev merge candidate at the merge turn (source base `2cbed0a9`, live dev `ac2c5e77`): builder and native banks, plus donor and consumer banks (consumer with the pp170 parent-name-evidence patch). Link the receipts on the PR.
- Accept or reject the hosted `suites` jobs at this head (in progress at snapshot).
- Track the parent-side finding the author reports: `scripts/lint_rtl.py` drops every processor-path Verilator diagnostic and ignores Verilator's exit status, so the parent lint gate cannot see a processor guard of any severity. This needs a parent change and is outside this PR. I reproduced the underlying fact: Verilator exits 1 with the processor `USERFATAL` at `-GN_STREAM_IN_P=40`.
- After F1 and F2 are fixed, a re-review round at the new head.
- Residue checklist: none from this round.

## 8. Integrity

- The review clone was never edited. At the end it is clean, HEAD `ef86ea84…`, tree `544a270d…`; index entries equal the HEAD tree (592 files, modes and blobs); every tracked file re-hashed with 0 mismatches. The repository has no submodules, so no gitlinks need verifying (`receipts/clone_integrity.txt`).
- Probes ran only on exported copies and scratch clones under `scratch/`, which is not published.
- No GitHub write was made.

R605-1 FINISHED
