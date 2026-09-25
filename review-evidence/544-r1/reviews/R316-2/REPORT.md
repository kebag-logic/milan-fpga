[R316] NEGATIVE - exact head 77e9ca5ea9e04a7618c577ab511baec63b39dc05

Round R316-2: internal, cleared-context, independent delta review of PR #558 (issue #544), round 2 of executor [A289].

- Exact head `77e9ca5ea9e04a7618c577ab511baec63b39dc05`, tree `2748915e23ce414f483eeb0f0f2f7f83018caae7`. Source base `ffcbd33de70278ae34b533dcbadde0b36c8cba13`.
- All five lenses were applied: Conformance, RTL, Robustness, Tests and Docs.
- My own pass over the diff, the probes and the findings below came before I read any prior review report. Prior findings are mapped in their own section.

## Summary

The round-2 absence rule does what the assignment and decision 5824093785 describe. It holds for everything written between the sampling read and its guard:

- Every bypass from my round 1 (C01-C25) and from R317-1 is refused with the pinned SDK on the rule's sentence. That covers wrappers, `__extension__ &`, asm outputs, and each form with and without a macro. Each one passes again with only the new check disconnected.
- Escapes anywhere in the unit are refused, including unevaluated ones.
- The two authorized shapes are exactly delimited, and every hostile near miss I tried is refused.
- The production firmware and the legitimate corpus keep their verdicts, and totals grow: 348/348 and 249/249 mutations against 280 and 222 at base.

Two findings remain open.

- **F1, MAJOR.** The rule reads only names and asm inside the interval, and the interval may call code. A helper whose asm overwrites the callee-saved registers, called before the guard, forges the verdict on the pinned SDK at the product's `-Os`. The helper can be reached directly, through a function-like macro invoked as `MILAN_FORGE(id);`, or through a `#define printf` that leaves the interval text byte-identical to production. Gate 1b accepts all three in both modes. The compiled code keeps `id` in `s0` and the guard is `bne s0,a5`.
- **F2, MINOR.** The compiler-free bound is published as a closed list of seven forms. At least ten more plain spellings are accepted without a compiler and are neither named nor pinned. They include my round-1 C09 and C11 and R317-1's plain wrapper and asm rows.

## Authorities read

- AGENTS.md; CONTRIBUTING.md sections 3 and 6 (the verification bar, and the wording, privacy and em-dash rules).
- docs/README.md, as the documentation map.
- Issue #544: body and acceptance 1-3.
- Issue #544 comments:
  - decision 5822485498;
  - [A286] 5822559016, 5822819158 and 5823103330;
  - the round-2 assignment 5823832945;
  - [A289] conflict reports 5823881519 and 5823890114;
  - decision 5824093785;
  - [A289] REVIEW READY 5824702131.
- PR #558 body.
- `docs/integration/BAREMETAL_FIRMWARE.md` at head, gate 1b section and cost table.
- `git diff ffcbd33d..77e9ca5e` and the two commits `b068763c` and `77e9ca5e`.
- The surrounding gate code:
  - `preprocess_take`, `blanked`/`_c_phases`, `boot_path_anchors`, `braced_span`, `constant_value` and `census_take`;
  - the source-text identity rule at `test_builder.py:11140-11150`.
- Public evidence tree `97bcef23:review-evidence/544-r1`: only its file list and my own round-1 probe scripts before my pass; the R316-1 and R317-1 reports only after it.
- Hosted check runs at the exact head, read-only.

## Findings

### F1 - MAJOR - Conformance, Robustness, Tests, Docs

**Where:**
- `sw/builder/test_builder.py:5170-5225` (`assert_identity_interval`: asm is refused only inside the interval) and `:5227-5302` (`assert_preprocessed_identity_sample`).
- Page: `docs/integration/BAREMETAL_FIRMWARE.md:432-458` and cost-table row `:1407`.

**Title:** a function-like macro invoked with the sample before its guard still forges the identity verdict with the pinned SDK. It does this by calling code whose asm overwrites the register that holds the sample, and gate 1b accepts it.

**Authority:**
- #544 acceptance 1: "A hostile firmware whose function-like macro overwrites the identity sample before its mismatch guard is refused, with the compiler ...".
- Decision 5824093785 gives the safety argument the rule rests on: "rule 1 means the sample's address is never taken, and rule 2 refuses asm in the interval. The object can therefore change only through an lvalue use of its own name."
- The page repeats that argument: "cannot escape" (`:1407`), and "Every `asm` ... statement there is refused" (`:448`).

**Evidence** (`receipts/r2set-matrix.md`, `receipts/w-machine.txt`, cases in `scripts/r316-2/probe2.py`). Each case goes through the real `assert_boot_contract`:

| case | edit | head SDK | head absent | base SDK |
|---|---|---|---|---|
| W01 | `static void __attribute__((noinline)) milan_settle(void)` whose only statement is `__asm__ volatile("li s0, 0x4d494c4e ... li s11, 0x4d494c4e")`, called as `milan_settle();` before the guard | ACCEPTED | ACCEPTED | ACCEPTED |
| W02 | the same helper, plus `#define MILAN_FORGE(x) milan_settle()`, invoked as `MILAN_FORGE(id);` before the guard | ACCEPTED | ACCEPTED | ACCEPTED |
| W03 | a variadic `milan_diag` with the same asm, plus `#define printf milan_diag`. The text between the read and the guard is the unchanged production text | ACCEPTED | ACCEPTED | ACCEPTED |
| S06 | the same asm written directly in the interval | REFUSED (asm rule) | - | - |

The overwrite is real in the compiled code. I compiled with the pinned SDK (GCC 14.3.0), `-std=gnu99 -Os -fomit-frame-pointer -fno-builtin -fno-stack-protector`, which is LiteX `BASEFLAGS`. The stub tree was gate 1b's own `census_headers()` plus LiteX's `bios/init.h`, so `milan_init` is emitted.

- Production `milan_init` loads the sample with `lw s0,0(a5)` and passes it to `printf`. The guard is `bne s0,a5` against `a5 = 0x4d494c4e`.
- In W01, W02 and W03 the only change inside `milan_init` is one more `call` before that `bne`: `call milan_settle`, or `call milan_diag` in place of `printf`.
- The helper body is the twelve `li sN, 0x4d494c4e` instructions and `ret`. It saves nothing.
- So the guard compares the magic with itself whatever the CSR returned.
- S06 shows that the asm ban exists for exactly this write. With only the asm sub-rule mutated off, S06 is ACCEPTED (`receipts/r2sub-matrix.md`). W01 moves the same instructions one call away.

**Why the rule misses it:**
- The absence rule reads the sample's identifier and the asm keywords, and only inside the interval.
- The production interval contains a call (the diagnostic `printf`), so calls are admitted. Any callee may break the calling convention, and nothing reads asm outside the interval.
- The C-level argument in the decision is sound for the abstract machine. It does not hold for code that writes callee-saved registers without declaring them.

**Impact:**
- On the configuration that grades a merge (`--require-rv32`), a hostile firmware configures the fabric on a foreign identity. W02 is literally the shape acceptance 1 names.
- W03 leaves every line between the read and the guard byte-identical.
- This is not a regression: base accepts all three. But the PR says `Closes #544`, and the page presents the absence rule as closing the sample.

**Required outcome.** With the compiler, one of the following:
- A firmware that changes the compared value between the read and the guard, through code the interval calls, is refused on a named rule. That includes asm in a callee writing callee-saved state, reached directly, through a macro, or through a redefined diagnostic. Each shape gets a mutation row pinned on the rule's sentence and a disconnected control. The design is the executor's.
- Or a recorded decision accepts this as a bound. The page (`:432-458`), row `:1407` and the verdict COST line then state it exactly, and #544 acceptance 1 is reconciled publicly rather than closed by this PR.

**Verification:**
- `probe2.py` W01-W03 at the new head with the pinned SDK are REFUSED on the named rule, or are the stated bound.
- A disconnected control accepts them.
- The production firmware, the 38 accepted cases (including the fifth fence) and every existing row keep their verdicts.
- The totals do not shrink.

### F2 - MINOR - Conformance, Tests, Docs

**Where:**
- `docs/integration/BAREMETAL_FIRMWARE.md:460-476` ("These seven pinned forms are accepted without compilation").
- Cost-table row `:1409` ("Without the compiler: seven identity protections are NOT RUN").
- The verdict COST line built at `sw/builder/test_builder.py:16034-16056` ("These seven pinned forgeries are ACCEPTED in this mode").
- The fixtures at `:12201-12219`.

**Title:** the compiler-free identity bound is published as seven forms, but the class accepted without a compiler is open.

**Authority:**
- Assignment 5823832945: "Name each form accepted without a compiler as NOT RUN in that mode ... Pin each with a fixture that is accepted without a compiler and refused with one."
- #544 acceptance 1: "(or stated as NOT RUN without it)".

**Evidence:** `receipts/r2set-matrix.md`, and `receipts/r1set-matrix.md` for C09 and C11. With no compiler, the only identity protection for a spelling without a macro is the source-text rule at `test_builder.py:11140-11150`. That rule matches `id` directly followed by an assignment, `++` or `--`, or `&` directly before `id`. The following are ACCEPTED at head without a compiler and REFUSED at head with the SDK. None is named, and none is pinned:
- A01 = my round-1 C09: `*(__extension__ &(id)) = MILAN_ID_MAGIC;`.
- A02 = my round-1 C11: the plain asm output `"=r"(id)`.
- A03, A04, A05 and A06: plain `__builtin_choose_expr(1, id, id)`, `_Generic(0, int: id)`, `(__real__ id)` and `(__extension__ id)` used as assignment targets. A03 is R317-1's plain row.
- A07: a plain asm tied output.
- A08: `__builtin_memcpy(&(id), ...)`.
- A09: `(id) |= MILAN_ID_MAGIC;`.
- A10: `*(&(id) + 0) = MILAN_ID_MAGIC;`.

C16 and C17, which are named, are two members of the same class.

**Impact:**
- A reader of a compiler-free run, or of the page, is told that exactly seven forgeries pass there. That implies the rest are graded, and they are not.
- The hosted builder requires the compiler, which is why this is MINOR and not MAJOR.

**Required outcome:**
- State the compiler-free identity bound as the class it is, in the prose, row `:1409` and the COST line: every spelling the source-text rule does not match, with representative examples. Do not state it as a closed count.
- Pin representative plain forms with fixtures accepted without a compiler and refused with it, at least C09 and C11.
- Alternatively, refuse them without a compiler.

**Verification:**
- Read the page and the compiler-free COST line.
- `probe2.py` A01-A10 stay ACCEPTED without a compiler and REFUSED with the SDK, matching the text.
- The new fixtures print alongside the existing seven.

### S1 - SUGGESTION - Conformance, Docs

**Where:** `sw/builder/test_builder.py:5203-5213`, the argument shape's exclusion list.

**Detail:**
- `(unsigned long)id` is admitted inside `__alignof(...)` (N04) and `__typeof(...)` (N06). Both are GCC keyword operators, not calls.
- The list excludes `_Alignof`, `__alignof__`, `typeof` and `__typeof__`, but not their alternate spellings `__alignof` and `__typeof`.
- This is harmless: the operand is an unevaluated cast rvalue and cannot write.
- It does, however, differ from the decision's "complete call argument" and from the list's evident intent.

**Suggested:** add the alternate spellings, or state that identifier-spelled keyword operators are admitted. This does not affect coverage.

## Prior findings, resolved or retained at this head

| Finding | Status at 77e9ca5e | Evidence |
|---|---|---|
| R316-1 F1: `__extension__ &` | RESOLVED. Refused with the SDK on the absence rule; base ACCEPTED. The builder has rows "identity macro/plain extension address" with a disconnected control. | C08, C09 (`r1set-matrix.md`) |
| R316-1 F2: enumerated write forms, asm outputs | RESOLVED for its measured cases. Any asm in the interval is refused, and an occurrence outside the two shapes is refused. The same impact through a callee is the new F1. | C10, C11, S03, S06 |
| R316-1 F3: compiler-free C03, C05, C13 unstated | RESOLVED. They are named NOT RUN at `:463-470`, `:1409` and in the COST line. The fixtures print ACCEPTED without a compiler and are refused with it. | `gate1b-absent.log` lines 5-11, `gate1b-sdk.log` 348/348 |
| R316-1 F4 (SUGGESTION): C16 and C17 without a compiler | Named and pinned. The wider class is F2. | A01-A10 |
| R317-1 F1: wrapper and asm writes with the compiler | RESOLVED, both with and without a macro, on the SDK. The plain forms without a compiler are retained under F2. | A03, A07, and the builder `identity_bypasses` rows |
| R317-1 F2: alias, apply and header paste without a compiler | RESOLVED. Named and pinned. | `gate1b-absent.log` |
| R317-1 S1: mem* and str* rows pass the value, not the address | Retained as a SUGGESTION of that round. Under the absence rule these rows are occurrence refusals on the rule's own sentence. A genuine `&(id)` destination is refused with the SDK. | A08, C24 |
| R272-1 and R273-1 published macros (PR #535) | Refused in both modes on the named rules. With the new check disconnected they are ACCEPTED. | C01, C02, C12, C21, C22 |
| R273-S3: verifier `#else` deleted | RETAINED, ACCEPTED at base and head in both modes, per the decision not to widen scope. | C19 |

## What was verified, per the assignment

**The sample never escapes.**
- The storage class is read and reported. Automatic spellings are accepted. `static`, `extern` and `_Thread_local static` are refused with "storage class" in the rule's sentence. This is the builder's own print, and ST rows in `r2sub-matrix.md`.
- The `register` diagnostic copy refuses the sample's address anywhere in the unit, including after the guard:
  - `sizeof(&id)`;
  - the unselected arm of `__builtin_choose_expr`;
  - an unselected `_Generic` association;
  - `__typeof__(&id)`;
  - a `__builtin_memcpy` source.
  
  These are E01-E05, which base accepts.
- Nested functions, including the `__extension__` old-style form, are refused.
- The necessity of each sub-rule was measured by mutating it alone, in memory:
  - with the nested-function rule off, S01 and S02 are accepted;
  - with `__extension__` blanking off, S02 is accepted;
  - with the `register` substitution off, S04 and S05 are accepted;
  - with the storage rule off, the ST rows are accepted;
  - with the asm rule off, S03 and S06 are accepted.

**The interval.**
- Only the guard comparison and the two delimited shapes are admitted. All of decision 5824093785's near misses are builder rows, reason-pinned. So are the `printf` macro that assigns and the `__extension__` and `__builtin_choose_expr` wrappers.
- My new near misses, all refused by the absence rule's shape sentence (base ACCEPTED):
  - N09: a character-literal mask;
  - N10: a parenthesized callee;
  - N11: a comma operator in a nested paren;
  - N12: a `__builtin_choose_expr` hidden inside a call;
  - N14: the mask as the body of an `if`.
- N07 (an assigning second argument) and N13 (`(unsigned long)id += 1`) are refused earlier, by the source-text rule.
- The legitimate shapes stay accepted: N01 (a second diagnostic), N02 (an `ull` literal) and N03 (split over lines).

**The corpus and totals.**
- Gate 1b alone ran through `sw/builder/test_firmware_compiler.py`, with the scoped Verilator 5.050 (`--version`: `Verilator 5.050 2026-07-01 rev v5.050`):
  - SDK: `348/348 mutations`, `38/38 legitimate firmware edits`, `4/4` Makefile, `46/46` RTL variants, `GATE 1b PASS; 0 NOT RUN`, 819 compiles;
  - no compiler: `249/249`, `35/35`, `4/4`, `46/46`, `GATE 1b PASS; 1 NOT RUN`, 0 compiles.
- Base, per the page, is 280 and 222 mutations and 29 firmware edits. #408 acceptance 4 holds: the diff removes only the two lines of the restructured `assert_preprocessed_boot_path` call, and everything else is appended.
- One provenance note. The discarded-mask fixture was added at round-1 head `b068763c`, not at base. Decision 5824093785 authorizes it explicitly.

**Compiler-free bounds.** The seven named forms print `ACCEPTED, identity protection NOT RUN without a compiler` and are refused with the SDK. The corrected `__CONCAT` sentence is restored at `:430-432` and `:461-462`. The open remainder is F2.

**My round-1 probe set** (`scripts/r316-1-unchanged/`, byte-identical to the published copies) was re-run in all six configurations (`r1set-matrix.md`):
- head SDK refuses C01-C13, C16, C17 and C20-C25 on the absence rule;
- C14, C15 (writes after the guard) and C19 stay ACCEPTED;
- C04 and C18 are refused by the older rules, as at base;
- head without a compiler refuses the macro forms on the replacement rule and accepts C03, C05, C13, C16 and C17, which are named, and C09 and C11, which are not (F2);
- disconnected controls accept every new refusal in both modes.

**Static gates** at head, all exit 0 (`receipts/static.log`):
- `docs_check.py`;
- `check_em_dash.py --base ffcbd33d` (75 added lines, 0 findings);
- `check_doc_style.py`;
- `gen_toc.py --check`;
- `check_doc_paths.py`;
- `check_py_idiom.py`;
- `check_baremetal_only.py --check`;
- `git diff --check`.

The two renderer-dependent gates ran from a private environment holding the hash-pinned `tools/markdown/requirements.txt`.

**Hosted, exact head** (`receipts/hosted-checks.txt`, read at review time):
- Succeeded: rtl-fast, yosys-elaboration, verilator-lint, Verilator shards 0-3, Yosys shards 0-3, docs-check, docs-check-no-git, full-ci-gate, elaborate, bdd-conformance, wire-accountability and changes.
- Verilator shard 4/5 was still in progress.
- `Physical gPTP (nightly and manual)` was SKIPPED. That is not hardware proof.

## Lens ledger (reviewer-owned)

| lens | result | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | #544 acceptance 1-3; decisions 5823832945 and 5824093785 against `test_builder.py:5120-5302` and `:15947-16056`; probe matrices `r1set`, `r2set` and `r2sub`; `w-machine.txt` | R316-2 | 77e9ca5ea9e04a7618c577ab511baec63b39dc05 |
| RTL | CLEAN | `git diff --stat ffcbd33d..77e9ca5e`: only `sw/builder/test_builder.py` and the page, with no `hdl/`, `tb/` or gitlink change. The new check binds the read address and guard magic to the RTL decode through `CsrModel` (`model.identity`, `model.identity_default`, `:5246-5256`). `gate1b-sdk.log` and `gate1b-absent.log`: 46/46 RTL mutation variants elaborated with the pinned Verilator 5.050 | R316-2 | 77e9ca5ea9e04a7618c577ab511baec63b39dc05 |
| Robustness | UNCLEAN (F1) | hostile near misses N04-N15, escapes E01-E05, writes W01-W05 and plain forms A01-A10 through `assert_boot_contract`, at head, at base and with checks disconnected; storage units; `w-machine.txt` | R316-2 | 77e9ca5ea9e04a7618c577ab511baec63b39dc05 |
| Tests | UNCLEAN (F1, F2) | the new mutation rows and disconnected controls at `test_builder.py:15947-16056`; accepted cases at `:14619-14643`; sub-rule necessity (`r2sub-matrix.md`); gate 1b totals in both modes | R316-2 | 77e9ca5ea9e04a7618c577ab511baec63b39dc05 |
| Docs | UNCLEAN (F1, F2) | `BAREMETAL_FIRMWARE.md:429-476`, `:1406-1409` and `:1728-1748`; verdict COST lines in `gate1b-*.log`; `static.log` | R316-2 | 77e9ca5ea9e04a7618c577ab511baec63b39dc05 |

## Real limits

**What I did not run:**
- The builder bank, the parent, PP and gPTP banks, and Yosys, as assigned.
- Gate 1b ran alone, through the repository's `sw/builder/test_firmware_compiler.py`.
- R317-1's probe set, which was not assigned to me.

**How the probes work:**
- My probes stop the suite at its first corpus call, with a hook placed before `assert_subset_refuses()`. Each verdict is therefore the whole per-firmware contract, not the suite's closing verdict.
- The sub-rule mutations edit the builder source in memory only.

**The machine-level check (F1):**
- It used gate 1b's census stub headers and LiteX `bios/init.h` at LiteX `-Os -fomit-frame-pointer`, and the SDK's default `-march`/`-mabi` (rv32gc/ilp32d). `-mabi=ilp32` does not compile against this SDK's glibc sysroot.
- The product's architecture flags, `-flto` and the real LiteX headers could change which callee-saved register holds the sample. The helper overwrites all of `s0`-`s11`, so the conclusion does not depend on which one.
- Nothing was linked or run on hardware.

**Tools:**
- The pinned SDK install in the validation storage was used read-only, after `scripts/ci_rv32_sdk.py` verified it: `riscv32-ilp32d--glibc--stable-2025.08-1`, GCC 14.3.0, archive sha256 `d42680e9...`.
- The audit maps only the settled selector's argv[0].

**Not run:** physical calibration. The hosted physical context was skipped. Neither is hardware proof.

**Receipts:** absolute paths are redacted to `$PACKET`, `$CANDIDATE`, `$VALIDATION_STORAGE`, `$WORKSPACE_HOME` and `$DATA_ROOT` (`receipts/redaction.txt`).

**The clone is byte-exact at head** (`receipts/restore-check.txt`):
- `write-tree` equals `2748915e`.
- `git status --porcelain --ignored` is empty.
- All 882 tracked blobs rehash to the index, with no mode differences.
- The four gitlinks are unchanged: external `efeb541a`, gptp-processor `e5dcea6e`, protocol-processor `09f9bf38` and third_party/verilog-axis `48ff7a7e`, all at stage 0.
- The only thing removed was the `__pycache__` directories my runs created.

## Pending manager duties

- Publish this report.
- Decide the F1 route: a fix, or a recorded bound with #544 acceptance 1 reconciled publicly.
- After changes, run a re-review round at the new head. That round covers Conformance, Robustness, Tests and Docs, plus RTL again if any RTL-scope artifact changes.
- Hosted and act acceptance of the final head, including Verilator shard 4/5, which was in progress here.
- The current-`dev` candidate build and merge validation at the merge turn: source base `ffcbd33d`, live dev `c266432d`.

R316-2 FINISHED
