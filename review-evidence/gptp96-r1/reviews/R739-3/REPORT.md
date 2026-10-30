[R739] NEGATIVE - exact head 411b35fcc56d11c2361d861e7205307587a04a1d

# Independent delta review R739-3: Mister-M-alt/FPGA-gPTP PR #97 (issue #96)

- Head `411b35fcc56d11c2361d861e7205307587a04a1d`, tree `131a1ffff543977e1881e3ba5b70a2871f7a6d89`. Base main `135afd04`. Previously reviewed head `806957b3`.
- Delta `806957b3..411b35f`: four commits, five files. Four are Markdown pages: `docs/INTEGRATION.md`, `docs/MANAGER.md`, `docs/HDL_DEVELOPER.md` and `docs/history/v1/RESOURCE_DELTAS_2026_10.md`. The fifth is `scripts/check_docs.py`. The delta has no mode change, no gitlink, and no RTL, generator, generated, test-bench or Makefile path (`receipts/clone_integrity.txt`).
- Scope: the delta, and each named prior finding at its cause. Code the delta does not touch keeps its round-2 lens verdict.

## Order of work and isolation

- PR data came only from `gh pr view` with the permitted fields (`receipts/pr_view.json`). Source came from git.
- I read three comments: this reviewer's round-2 report, the R740-2 report (the brief lists it as this reviewer's own), and the manager's round-3 ruling (issue comment linked in the brief).
- I did not read any other reviewer's round-3 report or packet, the PR comment thread, or the `reviews/` directory of the evidence packet.
- Every claim about the gate was checked two ways. First, I read `scripts/check_docs.py`. Second, I planted at least one defect per claim in a disposable copy of the head tree. Prior findings are resolved below, after that independent pass.

## Verdict basis

All three named prior findings are resolved at their cause.
- R739-2 F1: the constants-duplicate rule now has a self-test arm.
- R739-2 F2: decimal and unit-word restatements are no longer claimed to be rejected.
- R740-2 F1: the history page links the four `.rpt` files at `4999d8d6`.

Both new RTL-facing sentences hold against the engine and microCPU source. Every gate passes at the head.

The manager's ruling for this class is: "every sentence about the gate states what it checks, and only that". Three sentences in the new gate description, and their PR-body counterparts, do not meet it. A planted defect contradicts each one:
- **F1:** the rule for where a row's unit comes from is wider than the checker. A Meaning cell ending "in ms" ends in ms, as the page says, yet it gives no unit, and a copy of that value escapes. The PR body's minute line also claims digit forms the checker misses ("5min").
- **F2:** two stated passes fail. "Decimals ... pass" is false for minute values such as "2.5 min". "Fenced code ... exempt" is false for `~~~` fences.

These are two MINOR findings in the same class as round-2 F2. Narrowing the words closes each one; a small checker change is the alternative. Open MINORs make the verdict NEGATIVE.

## Resolution of named prior findings

| Prior finding | Resolution at this head | Evidence |
|---|---|---|
| R739-2 F1: no self-test arm for the duplicate constants row | **Resolved.** `scripts/check_docs.py:713-718` adds an arm. It appends a second true `SYNC_RTO_MS_C` row and expects the finding "duplicate constant row: SYNC_RTO_MS_C". With the rule removed (`weak_no_const_duplicate`) or its finding silenced (`silence_const_duplicate`), `--selftest` fails at that arm with rc 1. The unmutated self-test passes 42 arms; the base had 10. | `receipts/checker_mutants_r3.txt`, `receipts/selftest_arms.txt` |
| R739-2 F2: the copy rule claimed to reject decimal and unit-word restatements | **Resolved at its cause.** The claim is narrowed to the generated forms (`docs/INTEGRATION.md:860-874`). The two round-2 limit probes now pass, as the page says: "0.375 s" and "375 milliseconds". The integer, seconds, microseconds and minute forms are listed and fail as listed (planted probes below). Two of the new sentences are inexact in other ways; see F1 and F2. | `receipts/claim_probes.txt` (`d_decimal_s`, `d_word_ms`, `i_*`, `s_*`, `m_*`) |
| R740-2 F1: the history page must link the `.rpt` files themselves | **Resolved.** `docs/history/v1/RESOURCE_DELTAS_2026_10.md:32-37` links four blob URLs at `4999d8d6344e373e0204995cb36c93cf616e8f9e`. Each resolves to a file of that path (blob SHAs recorded). The link text has no labels. The figures on the page match the reports: LUTs 4,773 and 4,853 (+80), registers 3,646 and 3,652 (+6), memory LUTs 466 in both, and WNS +2.249 and +1.773 ns. | `receipts/history_link_targets.txt` |

Round-2 residue and suggestions:
- **RES-1 (applied):** `docs/INTEGRATION.md:567` reads "The commit cycle always presents a complete tuple." That drops the overstated "only" and holds against the RTL (see below).
- **RES-2 (applied):** `docs/HDL_DEVELOPER.md:12` reads "Sample on `pub_commit_o`; staging writes change outputs first."
- **RES-3 (applied):** the three comments now end "(#96)".
- **S-2 (Meaning-cell comma):** now stated on the page, but stated wider than the code. It becomes part of F1.
- **S-3 (unitless rows):** now disclosed by "Rows without such a unit are not checked for copies." That sentence is accurate. Closed by disclosure.
- **S-4 (other seeded images):** disclosed. `docs/MANAGER.md:59` names `--seq-seed 0x200000`, and the PR body says no other seeded image is checked. Both match `scripts/check_docs.py:129,556`. Closed by disclosure.
- **S-1 (coincident values) and S-5 (`make lint` uses the `verilator` on `PATH`):** unchanged, carried below.

## Findings

### F1 - MINOR - Robustness, Tests, Docs

- **Where:**
  - `docs/INTEGRATION.md:860`, "Units come from Meaning cells ending ms, ns or ppm.";
  - the PR body, "A row has a unit when its Meaning cell ends in ms, ns or ppm.", and "a ms value as one to ten whole minutes, in digits or as a number word";
  - the PR body, "Each statement below is what the checker enforces."
- **Checker:**
  - `scripts/check_docs.py:123` is `UNIT_CELL_RE = re.compile(r",\s*(ms|ns|ppm)\s*$")`. A unit needs a comma before the symbol.
  - `scripts/check_docs.py:454` builds the minute patterns `\b{N}[\s-]min` and `\b{word}[\s-]minutes?\b`. Both need a space or hyphen, and the word form also needs the word "minute".
- **Evidence:** planted defects in disposable copies of the head (`receipts/claim_probes.txt`, `receipts/make_docs_contradictions.txt`):
  - `u_meaning_ends_in_ms`: the `SYNC_RTO_MS_C` Meaning cell becomes "syncReceiptTimeout in ms", and "The watch is 375 ms." is added to `docs/HDL_DEVELOPER.md`. `make docs` gives rc 0. The cell ends in ms, so the page says the row has a unit and the copy should fail. The control with the true ", ms" cell fails with rc 1.
  - `m_nospace` ("A 5min countdown.") and `m_word_min` ("A five min countdown.") give rc 0. Both are `CEASE_MS_C` written as whole minutes "in digits or as a number word", which the PR body says are rejected.
- **Impact:** a stated gate rule is wider than the check. An editor who follows the stated rule, for example by writing "Sync receipt timeout in ms" for a new or reworded row, silently turns off copy detection for that row. The PR body's "Each statement below is what the checker enforces" is then untrue for these two statements. This is the class the manager's ruling closes.
- **Required outcome:** do one of the following, whichever is smaller.
  - (a) Narrow the words to the checker. The page could read: "A Meaning cell ending in a comma and ms, ns or ppm gives the unit, as in `syncReceiptTimeout, ms`." The PR body's unit line should match. Its minute line could read: "N min or N minutes, or a number word and minute or minutes, spaced or hyphenated".
  - (b) Extend the checker so that the stated rule is the rule, with a planted self-test arm for each extension.
- **Verification:** rerun `scripts/claim_probes.sh`.
  - With (a), the `u_meaning_*` and `m_*` probes must agree with the new text.
  - With (b), `u_meaning_ends_in_ms`, `m_nospace` and `m_word_min` must give rc 1. The control must stay rc 0.

### F2 - MINOR - Tests, Docs

- **Where:**
  - `docs/INTEGRATION.md:872`, "Decimals and other unit words, such as milliseconds, pass.";
  - `docs/INTEGRATION.md:868`, "Fenced code and this section are exempt.";
  - the PR body, "Decimal forms (for example "0.375 s") ... are not matched";
  - the PR body, "The stated passes (decimals, unit words, fenced code, the home section, historical pages) pass as stated."
- **Checker:**
  - The minute digit pattern `\b{N}[\s-]min` (`scripts/check_docs.py:454`) has no number lookbehind, unlike the integer patterns at `:447`. So the "5 min" inside "2.5 min" matches.
  - The copy rule recognises a fence only by a line starting with three backticks (`scripts/check_docs.py:475`). A `~~~` fence is fenced code in GitHub Markdown, but the checker does not exempt it.
- **Evidence:** planted defects, run through the full `make docs` target (`receipts/make_docs_contradictions.txt`, `receipts/claim_probes.txt`):
  - `d_decimal_min` "A 2.5 min hold." gives rc 2, "'5 min' restates CEASE_MS_C".
  - `d_decimal_minutes` "A 7.5 minutes hold." gives rc 1 with the same finding.
  - `x_fenced_tilde`, a `~~~` block holding `sleep 375 ms`, gives rc 2, "'375 ms' restates SYNC_RTO_MS_C".
  - The stated passes that do hold: "0.375 s", "375.0 ms", "375 milliseconds", "20 microseconds", a backtick fence, the home section and a historical page all give rc 0.
  - The author's published probe set (`author-r3/receipts/copy_probes.log`) covers only "0.375 s" and a backtick fence among these, so its "pass as stated" result does not reach these cases.
- **Impact:** the page and the PR state passes and exemptions the gate does not grant. The failure is loud: the gate rejects the input rather than silently accepting it. Still, the PR's verification statement is untrue for two classes it names. No Current page contains either form today (no `~~~` fence in the tree), so no current page is wrongly failed.
- **Required outcome:** do one of the following, whichever is smaller.
  - (a) Narrow the words. For example: "Code fenced with three backticks, and this section, are exempt." Also state the decimal-minute exception, or say only "Decimal seconds and milliseconds pass".
  - (b) Give the minute digit pattern the same `(?<![\d.,])` lookbehind the integer patterns use, and treat `~~~` as a fence in the copy rule. Add a self-test pass arm for "2.5 min" and for a `~~~` fence.
- **Verification:**
  - With (a), the `d_decimal_min*` and `x_fenced_tilde` probes must match the new text.
  - With (b), all three must give rc 0, and every `m_*` and `i_*` probe must still give rc 1.

### RESIDUE (wording only; does not change the verdict)

None is new in this delta. Round-2 RES-1, RES-2 and RES-3 are applied, as listed above.

### SUGGESTION (non-blocking)

- **S-1:** the minute patterns also match inside other words and numbers. Neither page claims these pass, so they are not F2.
  - `f_twenty_five_minutes`: "A twenty-five minutes soak." is reported as `CEASE_MS_C` ("five minutes").
  - `f_five_minimum`: "At least 5 minimum samples." is reported as "5 min".

  Fix: put `(?<![\w-])` before the word form and `\b` after `min`.
- **S-2 (round-2 S-1, carried):** a coincident unrelated figure is reported as a copy, for example a "125 ms" cadence as `FU_RTO_MS_C`. Consider naming the possible coincidence in the finding text.
- **S-3 (round-2 S-5, carried):** the top-level `make lint` recipe uses `verilator` from `PATH`, with no override variable. A `VERILATOR ?=` variable would make the pinned identity explicit.
- **S-4 (outside the delta):** `docs/history/v1/RESOURCE_DELTAS_2026_10.md:30` reads "WNS moves from +2.249 ns; timing remains met." It does not give the value it moves to. The candidate timing report the page now links gives +1.773 ns. This is a historical page, and the sentence predates this PR's round 3.

## Statements checked against source

### New RTL-facing statements

- **`docs/INTEGRATION.md:567`, "The commit cycle always presents a complete tuple": holds.**
  - Every `pub_*_o` output is a continuous assign of its staging register (`hdl/top/KL_gptp_engine.sv:1134-1146`). The only extra inputs are `rom_gm_capable_w`, which is fixed by configuration, and the `pub_gm_r == 0` path gate, which is a function of staged state.
  - The staging registers have only two writers: reset (`:889-896`), and microcode state writes to region 3 (`:992-1053`), which are gated by `st_req_w && st_we_w`.
  - In `hdl/ucpu/KL_gptp_ucpu.sv`, both the store request (`:338-367`, `vld_e_r` and `uop_e_r.op == OP_WRITE_ST`) and `eff_commit_o` (`:442`, `advance_e_w && op == OP_COMMIT`) come from the single execute-stage instruction. So no state write can share the commit cycle, and every earlier write has landed at the preceding edge.
  - The boot pulse `boot_pub_commit_r` (`:870-872`, `:924`) fires one cycle after release, when no handler has run. It presents the reset self tuple.
  - "Complete" here means what microcode staged before `OP_COMMIT`, which `docs/HDL_DEVELOPER.md:317-318` states as the contract. The simulation assertions at `KL_gptp_engine.sv:932-936` guard the path-contest ordering and the empty-path invariant.
- **`docs/HDL_DEVELOPER.md:12`, "Sample on `pub_commit_o`; staging writes change outputs first": holds**, for the same reasons. Each staging write is visible on the outputs at the next edge, before the commit pulse.

### Gate statements and their planted defects (`scripts/claim_probes.sh`; `receipts/claim_probes.txt`)

The probe set has 46 planted defects plus one control. "Agrees" means the checker outcome matches what the page or PR states.

| Statement | Plants | Result |
|---|---|---|
| `INTEGRATION.md:854` "fails when a row drifts from its constant" | `k_drift` (375 to 376); `k_generator_changed` (generator `NPD_HI_C` 800 to 900, docs untouched) | rc 1, named finding. Agrees. |
| `:856` "missing, duplicate or formatted row" | `k_missing`, `k_duplicate`, `k_formatted` (`**375**`) | rc 1, named finding each. Agrees. |
| `:860` "Units come from Meaning cells ending ms, ns or ppm" | `u_meaning_comma_control` (rc 1); `u_meaning_ends_in_ms` (rc 0); `u_meaning_paren` (rc 0) | **F1** |
| `:862` "Elsewhere on current pages" | `x_integration_elsewhere`, `x_tb_readme`, `x_inline_code` (rc 1); `x_history_page` (rc 0) | Agrees. An HTML comment is also checked (`x_html_comment`, rc 1). No exemption is claimed for it. |
| `:864` integer and unit symbol | `i_space`, `i_nospace`, `i_hyphen`, `i_grouped`, `i_ungrouped_ns`, `i_ppm` | rc 1 each. Agrees. |
| `:865` whole seconds or microseconds, by symbol | `s_seconds` (300 s), `s_us` (20 us), `s_micro_sign` (100 µs), `s_greek_mu` (100 μs) | rc 1 each. Agrees. |
| `:866` one to ten whole minutes | `m_digits`, `m_digits_minutes`, `m_word`, `m_word_hyphen` (rc 1); `m_nospace`, `m_word_min` (rc 0) | The page's two examples agree. The PR body's "in digits or as a number word" does not (**F1**). |
| `:868` fenced code and the home section exempt | `x_fenced_backtick`, `x_home_section` (rc 0); `x_fenced_tilde` (rc 1) | **F2** |
| `:870` rows without a unit not checked | `u_unitless_ordinal`, `u_unitless_depth` | rc 0. Agrees. |
| `:872` decimals and other unit words pass | `d_decimal_s`, `d_decimal_ms`, `d_word_ms`, `d_word_us` (rc 0); `d_decimal_min`, `d_decimal_minutes` (rc 1) | **F2** |
| `MANAGER.md:57` "fails when this table drifts" | `r_shipping_drift`, `r_seeded_drift`, `r_seeded_duplicate` | rc 1, named finding each. Agrees. |
| `MANAGER.md:59` seeded row checked with `--seq-seed 0x200000` | `r_seeded_drift` reports "generator builds 1023 of 1024"; the generator run with that seed reports 1,023 real words, and the shipping run 1,022 | Agrees (`receipts/rom_generator_counts.txt`; checker `:556`). |

### PR-body self-test and weakening statements (`scripts/checker_mutants_r3.sh`; `receipts/checker_mutants_r3.txt`)

- "42 arms, up from 10 at the base": confirmed (`receipts/selftest_arms.txt`).
- "Except the five below, silencing any one finding of these four rules makes the self-test fail": confirmed.
  - I silenced each of the 18 findings of the status, constants, copy and ROM rules one at a time.
  - The 13 findings outside the exception list each make `--selftest` fail at the matching arm.
  - The five that survive are exactly the five the PR lists: "no document status rows", the missing archive row, "is not a generator constant", "no protocol constant rows", and non-decimal ROM counts.
- The eight named weakenings: duplicate row, required-name set, strict decimals, µs conversion, minute words, home exemption, ROM duplicate and number lookbehind. Each makes `--selftest` fail.

### Gates at the head (`receipts/head_gates.txt`, `receipts/head_*.log`)

- `make -j16 docs` rc 0: 14 Current and 18 historical pages; docs self-test 42 arms; source evidence 20 exact, with a 7-arm self-test.
- `make diagrams-check` rc 0, `make contract` rc 0.
- `make lint` rc 0, run with the pinned Verilator 5.050 first on `PATH`. The log shows only `Verilator 5.050 2026-07-01 rev v5.050`; the identity is in `receipts/verilator_identity.txt`.
- `git diff --check` rc 0 from both `135afd04` and `806957b3`.
- Each gate ran in its own archive copy of the head.

### Published author evidence (milan-fpga `2f8fce3a`, `review-evidence/gptp96-r1/author-r3`)

- All 60 `author-r3/` entries match `MANIFEST.json` `published_sha256` (`receipts/evidence_manifest_check.txt`).
- The evidence commit reports `unsigned` (`receipts/evidence_commit_verification.txt`). The packet's integrity rests on its hash list, not a signature.
- Spot checks:
  - The head gate `rc.txt` reports rc 0 for docs, diagrams-check, contract, lint and both diff checks.
  - `identity.txt` names head `411b35f` and Verilator 5.050.
  - The 23 rows of `copy_probes.log` agree with my overlapping probes.
- The author's parent-consumer gate logs are present for `806957b3`, `411b35fc` and `f97c1803`, and hash-verified. I did not re-execute them: it is outside this brief.

### Comments, labels and privacy

- The delta's added lines carry no lane, round, reviewer or comment-ID label, no host or device name, and no private path (`receipts/delta_added_lines.txt`).
- The three edited source comments state behaviour and reason, and now carry "(#96)".
- The one round-labelled path is inside the history blob URLs. Those URLs are the target R740-2 F1 required, and their visible text is label-free.

### Clone integrity (`receipts/clone_integrity.txt`)

- HEAD, the index tree and the worktree match `411b35f` / `131a1fff`.
- `git status --ignored` is empty, and there is no `__pycache__`.
- `ls-files -s` equals `ls-tree -r HEAD` in modes, blobs and paths.
- The tree has no gitlinks and no `.gitmodules`, and none are required.
- Every probe, mutant and gate ran in an archive copy under the packet's `scratch/`. The clone was never modified.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The delta has no clause or Milan citation change. History traceability: the four `.rpt` blobs at `4999d8d6` and their figures (R740-2 F1 resolved). The round-2 clause verdicts are unaffected. | R739-3 delta; earlier rounds for unchanged citations | 411b35fcc56d11c2361d861e7205307587a04a1d |
| RTL | CLEAN | `KL_gptp_engine.sv:870-936,980-1053,1134-1146`; `KL_gptp_ucpu.sv:338-367,439-442`. Both new publication sentences hold. No RTL in the delta. | R739-3 | 411b35fcc56d11c2361d861e7205307587a04a1d |
| Robustness | UNCLEAN (F1) | `check_docs.py:113-129,405-503,544-560`. Unit source, minute patterns, fence and home handling. 46 planted defects and a control. | R739-3 | 411b35fcc56d11c2361d861e7205307587a04a1d |
| Tests | UNCLEAN (F1, F2) | New self-test arm `:713-718`; 42-arm self-test. 18 finding-silencing mutants and 8 weakenings, all as the PR states. Head gates. The PR-body coverage and stated-pass claims (F1, F2). Author receipts (hash-verified). | R739-3 | 411b35fcc56d11c2361d861e7205307587a04a1d |
| Docs | UNCLEAN (F1, F2) | All four changed pages. `INTEGRATION.md:567,854-874`, `MANAGER.md:57-59`, `HDL_DEVELOPER.md:12`, `RESOURCE_DELTAS_2026_10.md:32-37`. The PR body. | R739-3 delta; R739-2 for unchanged pages | 411b35fcc56d11c2361d861e7205307587a04a1d |

## Real limits

- This was a delta review. Pages, code and suites the delta does not touch keep their round-2 verdicts. I re-ran no engine, microCPU, parser, gasket or decode suites, because the delta changes none of their inputs.
- The author's parent-consumer gate results are hash-verified receipts. I did not re-execute them.
- The author evidence commit is unsigned. Its integrity rests on the manifest hashes only.
- I checked the history report figures against the four linked reports, not against a fresh synthesis run.
- Physical calibration was NOT RUN. No hardware or field result is claimed, and field skips are not hardware proof.
- No manager source bank ran at this exact head, and none is claimed or inferred.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `135afd04`, live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`) with the builder and native banks at the merge turn, and link those receipts on the PR.
- Hosted and act acceptance at the exact head.
- Carry any RESIDUE to the residue checklist. This round adds none.
- The parent gitlink bump and the parent page pins, which the PR body says any bump needs.

R739-3 FINISHED
