[R316] NEGATIVE - exact head b068763c849a18096b0f46cf9b18e0f904e4d708

Round R316-1. Internal, cleared-context, independent review of issue #544 / PR #558.
Head `b068763c849a18096b0f46cf9b18e0f904e4d708`, tree `dd5e37eca811750c07abe128b2d01d13ab05e9fb`.
Source base and live `dev`: `ffcbd33de70278ae34b533dcbadde0b36c8cba13`.
Review start: PR #558 comment 5823304892.

## Summary

The two published hostile macros from R272-1 and R273-1 are refused in both modes, and each rule names itself. Removing either new check lets those macros pass. I did not find a legitimate corpus firmware that is refused. The totals rose to 304/304 with the SDK and 249/249 without it, and no existing row was edited or reversed. I reproduced all of this myself on the pinned tools.

The with-compiler rule still has holes. It is the rule that grades a merge, because the hosted builder runs `--require-rv32`. The design (issue comment 5822485498) says: "the identity-sample object gets exactly one store before its mismatch guard ... The gate refuses any other write to it." With the pinned SDK, gate 1b at this head still accepts a function-like macro that overwrites the sample before its guard. That is what the issue title describes. Two spellings do it: `__extension__ &(x)` (F1) and an asm output operand (F2). Compiled on the pinned SDK, the first removes the identity comparison entirely. Without a compiler, three hostile forms are accepted and are neither refused nor stated as a bound (F3). Acceptance 1 permits exactly one of those two outcomes.

## Authorities read

- AGENTS.md and CONTRIBUTING.md (sections 3, 6 and 7), and docs/README.md.
- Issue #544: the body, with acceptance 1 to 3 frozen. Design decision comment 5822485498. [A286] TAKEN 5822559016. The compiler-free interpretation, comment 5822819158, extends the replacement-list rule to direct substitutions into a used parameter. It is public and more conservative than the decision. Acceptance 1 requires both published macros to be refused without a compiler, and the literal-only rule cannot do that, so I accept the extension. REVIEW READY: 5823103330.
- PR #558 body.
- The diff `ffcbd33d..b068763c`, which touches two files: `sw/builder/test_builder.py` (+262/-2) and `docs/integration/BAREMETAL_FIRMWARE.md` (+29/-7).
- The published hostile sources at evidence commit `c8598794`. `review-evidence/408-r1/reviews/R272-1/scripts/cases_r3.py` gives `#define MILAN_FORGE(x) x = MILAN_ID_MAGIC`. `R273-1/scripts/make_more_cases.py` gives `((x) = MILAN_ID_MAGIC)`. `R273-1/scripts/make_cases.py` H8 is R273-S3. My C01, C02 and C19 reproduce these byte-for-byte.
- Public executable evidence at `5de8b40d/review-evidence/544-r1`: VALIDATION.md, run-builder.py, the full, probe and disconnect logs, and the retained-rows log.
- Exact-head hosted check runs (`receipts/hosted-checks.txt`).

A concurrent external round was posted on this PR during my round. I did not read it before writing this verdict and ledger. There were no earlier review findings on PR #558. The earlier findings this issue inherits from PR #535 are dispositioned under "Prior findings" below.

## Findings

### F1 - MAJOR - Conformance, RTL, Robustness, Tests, Docs
**Where:** `sw/builder/test_builder.py:5225-5230`, `docs/integration/BAREMETAL_FIRMWARE.md:1369` and `:433-437`.
**Problem:** with the pinned compiler, an address taken behind `__extension__` passes the identity-sample single-store rule, so a function-like macro can still forge the identity sample.

- **Authority:** design decision 5822485498 says "refuses any other write to it between the sample and the guard ... Writes include ... taking its address." Acceptance 1 and the issue title require it too. The cost table (`:1369`) says the rule "refuses ... address-taking" and "Parentheses cannot hide the object".
- **Evidence:** the classifier treats `&` as binary whenever the token to its left is any identifier outside a fixed keyword list (`return case sizeof _Alignof __alignof__ else do`). That is a default that fails open. `__extension__` is a GCC keyword that may prefix a unary expression. It is not on the list, so `&` after it is treated as binary.
  - C08, `#define MILAN_FORGE(x) (*(__extension__ &(x)) = MILAN_ID_MAGIC)` invoked as `MILAN_FORGE(id);` before the guard, is ACCEPTED by the whole gate 1b contract with the verified pinned SDK. It is REFUSED without a compiler (`receipts/probe-head-sdk.json`, `probe-head-absent.json`, `probe-matrix.md`).
  - C09 is the same write with no macro, and it is also ACCEPTED with the SDK. The rule reads the preprocessed interval, so the no-macro form is in its scope.
  - The pinned SDK at `-O2 -Wall -Wextra` compiles the C08 spelling with no diagnostic. It deletes the comparison entirely: `milan_read` is followed directly by `tail configure_fabric` (`receipts/forge-semantics.log`, VARIANT 8, against the VARIANT 0 control, which keeps the `beq`).
- **Impact:** on the mode that grades merges, a one-token change to the published hostile macro forges the CSR identity verdict. Fabric is then configured on a mismatched identity. The defect #544 was opened for remains reachable, and the documentation says it is closed.
- **Required outcome:** an `&` whose operand is the sample in the interval is refused whatever token precedes it. In particular, an unrecognised identifier to the left must not default to "binary". The cost table must say exactly what the rule refuses.
- **Verification:** C08 and C09 are refused by the named `identity-sample single-store rule` with the pinned SDK, and a mutation row pins that. Removing the fix makes the row fail. C14, C15 and C20 stay accepted with the SDK, and the 304 existing rows keep their verdicts.

### F2 - MAJOR - Conformance, RTL, Robustness, Tests, Docs
**Where:** `sw/builder/test_builder.py:5212-5233` and `docs/integration/BAREMETAL_FIRMWARE.md:1369`.
**Problem:** with the pinned compiler, an asm output operand writes the sample and passes the single-store rule.

- **Authority:** as for F1. The decision says "any other write". The cost-table row heading is "the identity-sample object gets one store before its mismatch guard".
- **Evidence:** the rule enumerates write forms: an assignment or compound token after the name, `++`/`--`, a unary `&`, and a `mem*`/`str*` first argument. Any other use of the name is accepted. Inline asm is allowed in the boot unit; the corpus holds four fence statements and accepts a fifth.
  - C10, `#define MILAN_FORGE(x) __asm__ volatile("li %0, 0x4d494c4e" : "=r"(x))` invoked before the guard, is ACCEPTED with the SDK and REFUSED without a compiler.
  - C11 is the same asm with no macro, and it is ACCEPTED with the SDK.
  - The pinned SDK compiles the C10 spelling so that the value compared is the asm result `li a4, 0x4d494c4e` (`receipts/forge-semantics.log`, VARIANT 10).
- **Impact:** same as F1. A function-like macro forges the identity sample, and gate 1b accepts it on the merge-grading mode.
- **Required outcome:** the sample in an asm operand in the interval is refused, or any use not proven read-only is refused. If some form is left accepted, it is stated as a bound in the cost table and the verdict COST line.
- **Verification:** C10 and C11 are refused by the named rule with the SDK, pinned by a mutation row and its disconnected control. The accepted corpus still passes, including the fifth fence.

### F3 - MINOR - Conformance, Robustness, Tests, Docs
**Where:** `sw/builder/test_builder.py:5120-5167` and `docs/integration/BAREMETAL_FIRMWARE.md:429-438`, `:1365`, `:1370`.
**Problem:** without a compiler, three hostile forms that overwrite the sample through a function-like macro are accepted and not stated. Acceptance 1 asks for "refused ... or stated as NOT RUN".

- **Authority:** acceptance 1 reads "refused, with the compiler and without it (or stated as NOT RUN without it)".
- **Evidence:** each of these is ACCEPTED at head without a compiler and REFUSED with the SDK (`probe-matrix.md`):
  - C13: an object-like alias `#define MILAN_ALIAS MILAN_FORGE` of the published R273 macro, invoked as `MILAN_ALIAS(id);`. The direct-call scan searches only for the function-like macro's own name.
  - C05: a local function-like macro `#define MILAN_FORGE2(a) __CONCAT(a, d) = MILAN_ID_MAGIC`, invoked as `MILAN_FORGE2(i);`.
  - C03: `__CONCAT(i, d) = MILAN_ID_MAGIC;`, which is [R273] F2 on PR #535.

  The base document stated the C03 bound explicitly in the identity row ("is not refused, on dev or here"). The head removes that sentence. The prose at `:429-438` now says the paste is "outside" the paste ban, that the compiler check reads its expansion, and that "Without the compiler, the replacement-list rule described below applies". That reads as though the compiler-free rule covers it, and it does not. The row at `:1370` says only "local definitions and direct calls, without general expansion". No accepted-in-absent-mode fixture pins these bounds, so the tests encode the implementation's own assumption that only direct calls matter.
- **Impact:** a reader of the cost table cannot tell that these forgeries pass the compiler-free mode. The docs job runs that mode on every commit. The hosted builder requires the compiler, which is why this is MINOR and not MAJOR.
- **Required outcome:** either refuse these forms without a compiler, or name each one as a compiler-free bound (NOT RUN in that mode) in the cost table, the `:429-438` prose and the verdict COST line. Then pin that with fixtures, accepted without a compiler and refused with one.
- **Verification:** the C03, C05 and C13 verdicts in both modes match the updated text. The docs gates pass.

### F4 - SUGGESTION - Robustness
**Where:** the pre-existing source-text identity check, `sw/builder/test_builder.py:11084-11097`.
**Problem:** without a compiler, `(id) = MILAN_ID_MAGIC;` (C16) and `*&(id) = MILAN_ID_MAGIC;` (C17) are ACCEPTED, at base and at head. They involve no macro, so they are outside #544's scope. The new rule refuses both with the SDK, which improves the SDK mode.
**Suggested outcome:** open a separate Issue. Under AGENTS.md section 4 this is new work, not a reason to widen this lane. It does not affect lens coverage.

## Prior findings (inherited from PR #535, named in issue #544)

| Finding | Status at this head | Evidence |
|---|---|---|
| The R272-1 plain function-like macro forging `id` | RESOLVED for the published spelling in both modes. The same defect class remains open through F1 and F2 (SDK) and F3 (absent). | C01 |
| The R273-1 parenthesized macro | RESOLVED for the published spelling in both modes, with the same caveat. | C02, C12, C21, C22 |
| [R273] F2 on PR #535: a `__CONCAT(i, d)` header paste | RESOLVED with the compiler. RETAINED without it, and no longer stated (F3). | C03 |
| R273-S3: the verifier's `#else` deleted | RETAINED unchanged. ACCEPTED at base and head in both modes, with and without the new checks. That matches the PR's report and the decision's instruction not to widen scope. | C19 |

## What was verified, per the assignment

- **The SDK rule reads the preprocessed unit.** `assert_preprocessed_identity_sample` reads `preprocess_take(source)`, which is the same `-E` unit as `assert_preprocessed_boot_path`. `ran` is false only when no target compiler was adopted, and a failed `-E` asserts (fails closed).
  - Refused by the named `identity-sample single-store rule`: assignment (C01, C02, C23), compound assignment (C25), address taken (C06, C07, C24), writes in a nested block (C12), a variadic forwarder (C21), and double parentheses (C22).
  - The in-suite fixtures also cover `++`/`--`, all ten compound operators, `sizeof &` and the `mem*`/`str*` first argument.
  - Exceptions: F1 and F2.
- **The compiler-free rule.** Any `#define` whose replacement list names `id` is refused by the named `identity-sample macro replacement rule`. That includes object-like, continued and unused definitions (C23, and the in-suite cost rows). Direct substitutions into a used parameter are refused too (C01, C02, C06, C07, C12, C20, C21, C22, C24, C25). Exception: F3.
- **The published hostile firmware is refused in both modes.** C01 and C02. C12 is the R273 macro inside a nested block.
- **Controls.** With only `assert_preprocessed_identity_sample` disconnected, every SDK refusal above becomes ACCEPTED. With only `assert_identity_macro_free` disconnected, every absent-mode refusal becomes ACCEPTED (`probe-head-*-disabled.json`). The in-suite necessity controls at `test_builder.py:15792-15810` rebind the enclosing local, which `assert_boot_contract` reads as a closure cell, and restore it in `finally`. They exercised the same property in my gate runs.
- **No legitimate corpus firmware is refused, and existing rows keep their verdicts.** The whole diff removes two lines, and both are the restructured `assert_preprocessed_boot_path` call (`git diff`). Every other change is an append: `mutations +=` and `accepted_cases.update`.
  - I ran gate 1b alone (`sw/builder/test_firmware_compiler.py`, not the builder bank) at this head, on the verified pinned SDK and Verilator 5.050.
  - With the SDK: 304/304 mutations rejected, 38/38 firmware and 4/4 Makefile edits accepted, 46/46 RTL variants elaborated, `GATE 1b PASS; 0 NOT RUN; 513 actual firmware compiler invocations`.
  - With every cross compiler hidden: 249/249, 35/35 and 4/4, 46/46, `GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations`.
  - The growth is 24 SDK rows (22 fixtures plus 2 published) and 27 absent rows (plus the 3 cost rows) over 280 and 222. Six accepted cases were added, plus 3 with the SDK. So #408 acceptance 4 (no reduction) holds.
- **My own hostile variants.**
  - Token pasting: C04, the local `##`, is refused in both modes by the existing paste ban. C03 and C05 go through the header `__CONCAT`; the SDK refuses them and absent mode accepts them (F3).
  - A macro that takes the address: C06 and C07, refused in both modes.
  - A pointer alias set before the sample: a local cannot be aliased before its declaration. The only construction, a `goto` back over the read with the alias taken in the mismatch block (C18), is refused by the existing `milan_init() must not contain 'goto'` ban. A loop-carried pointer would point into a dead lifetime.
  - A nested block: C12, refused in both modes.
  - A write after the guard: C14 (macro) and C15 (plain) are ACCEPTED in both modes, as the assignment requires.
- **Cost-table rows.** `:1369` and `:1370` name each instrument and its pin. They disclose the conservative refusals: an address taken for reading, an ambiguous `&` after `)`, read-only `mem*`/`str*` calls, unused and read-only replacements, and used-parameter reads. The verdict COST line at `test_builder.py:15811-15820` matches them. The over-claims are F1 and F2, and the missing bound is F3.
- **Static gates at head.** All exit 0 (`receipts/static.log`):
  - `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `check_py_idiom.py`, `check_baremetal_only.py --check` and `git diff --check ffcbd33d HEAD`.
  - `gen_toc.py --check` and `check_em_dash.py --base ffcbd33d`, both under the existing pinned-renderer environment. The default interpreter lacks html5lib, and those two commands exit 2 there without judging.
- **Hosted exact-head contexts.** All completed successfully: rtl-fast, verilator-suites (shards 0 to 4), yosys-portability (shards 0 to 3), docs-check, docs-check-no-git, full-ci-gate and the others listed. `Physical gPTP (nightly and manual)` was SKIPPED. That is not hardware proof.

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3) | Issue #544 acceptance 1 to 3, decision 5822485498, interpretation 5822819158; `test_builder.py:5120-5248`, `:11218-11225`, `:15777-15820`; C01 to C25 in both modes; gate 1b counts in both modes | R316-1 | b068763c849a18096b0f46cf9b18e0f904e4d708 |
| RTL | UNCLEAN (F1, F2) | No HDL in the diff, per `git diff --numstat`. Architecture: the new checks' default paths (the `&` classifier's fail-open identifier default; write forms enumerated rather than failing closed); fail-closed `-E` (`preprocess_take`, `test_builder.py:5060-5084`); the mode switch aligned with `instruments_down`; 46/46 RTL mutants elaborated on Verilator 5.050 in both modes | R316-1 | b068763c849a18096b0f46cf9b18e0f904e4d708 |
| Robustness | UNCLEAN (F1, F2, F3) | Hostile variants C03 to C13, C16 to C18, C21 to C25; boundary and benign C14, C15, C20; base and disabled controls | R316-1 | b068763c849a18096b0f46cf9b18e0f904e4d708 |
| Tests | UNCLEAN (F1, F2, F3) | New fixtures `test_builder.py:12000-12053`, accepted cases `:14449-14473`, mutation rows and necessity controls `:15777-15810`; `receipts/gate1b-*-v5050.log`; disabled-check probes | R316-1 | b068763c849a18096b0f46cf9b18e0f904e4d708 |
| Docs | UNCLEAN (F1, F2, F3) | `BAREMETAL_FIRMWARE.md:429-438`, `:1365-1371`, `:1665-1702`; the static docs gates in `receipts/static.log` | R316-1 | b068763c849a18096b0f46cf9b18e0f904e4d708 |

All five lenses were applied in this round. None is covered clean at this head.

## Real limits

- I did not run the builder bank, the parent, PP or gPTP banks, or Yosys, as the assignment requires. I ran gate 1b alone, through the repository's own `sw/builder/test_firmware_compiler.py`.
- My probes execute the real `assert_boot_contract`. I stop the suite at its first corpus call, with a hook of my own before `assert_subset_refuses()`. So a probe verdict is the whole per-firmware contract, not the suite's closing verdict.
- I used the existing pinned SDK install at `$VALIDATION_STORAGE/504-manager-r1/sdk-install` read-only, after `ci_rv32_sdk.verify`: release `riscv32-ilp32d--glibc--stable-2025.08-1`, GCC 14.3.0. The user-home selector points at a different Buildroot 14.3.0 and was never executed as the compiler; my audit maps the selector's argv[0] only.
- The Verilator used for the recorded gate runs is the scoped 5.050 wrapper, checked with `--version`. Two earlier gate runs used an unpinned host Verilator by mistake. They are superseded and are not in the manifest.
- The receipts have absolute paths redacted to `$PACKET`, `$CANDIDATE`, `$VALIDATION_STORAGE`, `$WORKSPACE_HOME` and `$DATA_ROOT`. Nothing else was altered.
- Physical calibration was NOT RUN, and the hosted physical context was skipped. Neither is hardware proof.
- After the probes, the clone is byte-exact at this head (`receipts/restore-check.txt`):
  - `write-tree` equals `dd5e37ec`, and the porcelain status is empty, including ignored files.
  - All 882 tracked blobs rehash to the index, with no mode differences.
  - The four gitlinks are unchanged: external `efeb541a`, gptp-processor `e5dcea6e`, protocol-processor `09f9bf38`, third_party/verilog-axis `48ff7a7e`.
  - The only thing removed was the `__pycache__` directories that my runs created.

## Pending manager duties

- Publish this report. After F1 to F3 are fixed, run a re-review round on the new head covering all five lenses.
- Hosted and act acceptance of the final head.
- The current-`dev` candidate build and merge validation at the merge turn.
- File F4 as a separate Issue if accepted.
- A merge needs two independent POSITIVE reviews, the full completion bar, and explicit maintainer authorization.

R316-1 FINISHED
