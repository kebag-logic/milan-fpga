[R317] NEGATIVE - exact head 77e9ca5ea9e04a7618c577ab511baec63b39dc05

External independent delta review, round R317-2, of issue #544 / PR #558 at exact head
`77e9ca5ea9e04a7618c577ab511baec63b39dc05` (tree `2748915e23ce414f483eeb0f0f2f7f83018caae7`),
source base `ffcbd33de70278ae34b533dcbadde0b36c8cba13`. Cleared context. Reconstructed from
AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue body and the maintainer/manager
comments (assignment 5823832945, decision 5824093785), `docs/integration/BAREMETAL_FIRMWARE.md`,
the diff `ffcbd33d..77e9ca5e`, and the public evidence at
`97bcef23df2cd44a1c769f019936e1d3ad6930ee:review-evidence/544-r1`.

## Verdict in one paragraph

The compiler-mode design is implemented as decided, and it holds against everything I
threw at it. The sample's address is refused anywhere in the unit, in every spelling I
tried: unevaluated, `__typeof__`, asm `m`/`+m`, pointer initializer, and macro-hidden.
Nested functions are refused unit-wide. Asm in the read..guard interval is refused. Only
the two delimited shapes may name the sample there. All 30 of my round-1 probes, the
other reviewer's round-1 C08-C11 spellings, and 22 new near misses of the two exceptions
answer as specified with the pinned SDK. Each refusal is on the rule's sentence, and each
rule refusal of valid C passes when only that check is disconnected. The production firmware and
corpus keep their verdicts, and the totals grow: 348/348 and 249/249, against 280 and 222.

One MINOR stays open, so the verdict is NEGATIVE. The compiler-free bound is presented as
a closed list of seven forms, but it is not exact. Seven macro-free forgeries of the
sample are accepted without a compiler and refused with one, and none of them is
declared: the lvalue wrappers, `__extension__ &` and the asm outputs, written directly.
They are the gate's own `plain ...` fixtures. The assignment asked for "the exact bound".

Three SUGGESTIONs are recorded. None of them blocks.

**Order of discovery, for transparency.** Before I read any prior report, my independent
pass concluded POSITIVE. That conclusion is recorded in `receipts/verdict-before-prior.txt`.
I found F1 afterwards, while resolving the prior round-1 findings. The other reviewer's
C09/C11 and my own round-1 F1 table both carry macro-free spellings, so I graded those
spellings in compiler-free mode. The ledger below reflects F1.

## Findings

### R317-2-F1 - MINOR - Conformance, Robustness, Tests, Docs

**Artifacts:**
- `docs/integration/BAREMETAL_FIRMWARE.md:463`: "These seven pinned forms are accepted without compilation", followed by the list at `:465-471`.
- `docs/integration/BAREMETAL_FIRMWARE.md:1409`: row "Without the compiler: seven identity protections are NOT RUN".
- `docs/integration/BAREMETAL_FIRMWARE.md:1406`: the `MILAN_ID` row, "The original source-text check remains active in both modes".
- `sw/builder/test_builder.py:16034-16041`: the absent-mode COST string, which lists seven forms as "NOT RUN without a compiler".
- `sw/builder/test_builder.py:15960-15995`: the `identity_bypasses` `plain ...` fixtures, built at `:12111-12130`, are graded only when `not instruments_down`. The compiler-free branch at `:15991-15995` pins only `identity_absent_fixtures` (`:12201-12224`).
- Pre-existing and unchanged from base: the absent-mode verdict at `:16401-16402` says the text rules grade "the unmodified CSR identity sample".

**Title:** Without a compiler, seven further macro-free forgeries of the identity sample are accepted, and none is named in the stated "exact" bound.

**Authority:**
- Assignment 5823832945, compiler-free mode: "state the exact bound instead of widening the rule. Name each form accepted without a compiler as NOT RUN in that mode, in the cost table, in the `:429-438` prose and in the verdict COST line ... Pin each with a fixture that is accepted without a compiler and refused with one."
- #544 acceptance 1: "(or stated as NOT RUN without it)".
- AGENTS.md section 8: "Never hide a material assumption".

**Evidence:** `receipts/probes-r2/table-d.md`. Each form was written directly before the guard, graded through gate 1b's own `assert_boot_contract()`:

| form (no macro) | head, SDK | head, SDK, check removed | head, no compiler | base, no compiler |
|---|---|---|---|---|
| `(*(__extension__ &(id)) = MILAN_ID_MAGIC);` | refused, absence rule | ACC | ACC | ACC |
| `__asm__ volatile("li %0, 0x4d494c4e" : "=r"(id));` | refused, absence rule | ACC | ACC | ACC |
| `__builtin_choose_expr(1, id, id) = MILAN_ID_MAGIC;` | refused, absence rule | ACC | ACC | ACC |
| `_Generic(0, int: id) = MILAN_ID_MAGIC;` | refused, absence rule | ACC | ACC | ACC |
| `(__real__ id) = MILAN_ID_MAGIC;` | refused, absence rule | ACC | ACC | ACC |
| `(__extension__ id) = MILAN_ID_MAGIC;` | refused, absence rule | ACC | ACC | ACC |
| `__asm__ volatile ("" : "=r"(id) : "0"(MILAN_ID_MAGIC));` | refused, absence rule | ACC | ACC | ACC |

- These are the gate's own `identity_bypass_bodies`, with `x` replaced by the sample name. Round-1 public evidence showed them to be real overwrites: the pinned SDK deletes or neutralises the comparison.
- They were already public at round 1. My F1 table recorded plain `__builtin_choose_expr` and the plain asm output as "ACCEPTED in both modes". The other reviewer's C09 and C11 are the `__extension__ &` and `li %0` forms.
- They are the same class as C16/C17: no macro, pre-existing, missed by the source-text write-form regex at `test_builder.py:11140-11146`. The assignment brought C16/C17 into the NOT RUN list, but not these.

**Impact:**
- Merge grading always has the compiler (`--require-rv32`), so the merge-grading configuration is unaffected. That is why this is MINOR, not MAJOR.
- The page, the cost table and the absent-mode COST line give a reader of a compiler-free run a closed list of seven accepted forgeries. The verdict clause says the "unmodified CSR identity sample" is graded.
- At least seven more forgeries pass silently in that mode. No declaration covers them and no fixture pins them. This is the undisclosed compiler-free bound that R317-1 F2 and R316-1 F3 were raised for, now narrowed to the macro-free spellings.

**Required outcome:** one of the following must be true.
1. Each of these macro-free forms is named as NOT RUN without a compiler, in the cost table, the `:427-471` prose and the absent-mode COST line. The existing `plain ...` fixtures are pinned accepted without a compiler and refused with one.
2. The compiler-free bound is stated generically instead of as a closed list. For example: without the compiler the only identity check on unmacroed source is the source-text write-form list, and any lvalue form or asm output it does not list is NOT RUN. The seven named forms are then examples, and the wording says so.
3. A recorded maintainer decision scopes macro-free forms beyond C16/C17 out of #544, with a follow-up Issue, and the page wording no longer implies the list is exhaustive.

**Verification:**
- Rerun `probe_gate1b_r2.py --cases cases_544_r2d --mode absent`. Each row is either declared on the page and in the COST line, or covered by the generic statement.
- If option 1 is chosen, the gate's absent-mode run prints each form as a compiler-free bound.

### R317-2-S1 - SUGGESTION - Robustness, Docs

**Artifact:**
- `receipts/clobber/`: the reduced reproduction `clobber_repro.c`, with its `-O0`, `-Os` and `-O2` assembly.
- `receipts/probes-r2/table.md`, row "LIM callee asm clobbers a callee-saved register, called in interval".

**Detail:**
- A function defined outside `milan_init()` holds `__asm__ volatile("li s1, 0x4d494c4e")` without declaring the clobber. A call to it placed in the interval is ACCEPTED in every mode.
- The interval names no asm and no sample, so the decided rule is met.
- With the pinned SDK at `-Os`/`-O2`, the level a LiteX `common.mak` build conventionally uses, the sample lives in a callee-saved register (`s0` in the reduced unit) across calls. A callee writing that register undeclared therefore replaces the compared value (`lw s0,0(a5)` ... `call milan_clobber` ... `beq s0,a5`).
- The census compiles at `-O0 -fno-inline`, where the sample is a stack slot.
- This is a violation of the asm contract (undefined behaviour), outside the C-semantic model that decision 5824093785 reasons in: "can change only through an lvalue use of its own name".
- It is the same class as any hostile asm elsewhere in the firmware. It is not introduced or widened by this PR.

**Recommended:** record it as a stated bound of the identity rule, and of gate 1b's asm model generally, or open a follow-up Issue. For example: register effects of asm outside the interval, and the difference between the census optimisation level and the shipped one.

### R317-2-S2 - SUGGESTION - Conformance, Tests, Docs

**Artifact:**
- `sw/builder/test_builder.py:5183-5190`: the `parents` stack tracks `(` only.
- `sw/builder/test_builder.py:5203-5214`: the argument shape.
- `receipts/probes-r2/table-e.md`.

**Detail:**
- `printf("%lu\n", (unsigned long[]){ 0ul, (unsigned long)id, 1ul }[1]);` in the interval is ACCEPTED as the "complete call argument" shape. The `,` before the cast separates initializer elements inside braces, not call arguments.
- The two parenthesised variants of the same literal are refused.
- The accepted occurrence is still a non-lvalue cast, so no write is possible, and I found no way to turn it into one. That is why this is a SUGGESTION.
- It is still a third shape that the page's "Every other sample occurrence in that interval is refused" (`BAREMETAL_FIRMWARE.md:447`) and the decision's "exactly" exclude.

**Recommended:** track `{`/`}` (and `[`/`]`) in the delimiter parent test, and add this row as a near miss. Alternatively, state the lexical reading of the argument rule.

### R317-2-S3 (retained R317-1-S1) - SUGGESTION - Tests

**Artifact:** `sw/builder/test_builder.py:12088-12091`, the rows "identity macro memory destination" and "identity macro string destination".

**Detail:**
- `__builtin_memset((void *)(uintptr_t)id, 0, 4)` passes the sample's value, not its address.
- Under the absence rule the row is a valid refusal of an interval occurrence, but its label still calls it a destination write.

**Recommended:** relabel it as an occurrence or cost row.

## Prior public findings, resolved or retained at this head

I read these only after the independent pass above.

| prior finding | status at 77e9ca5e | evidence |
|---|---|---|
| R317-1-F1 MAJOR: lvalue wrappers and asm outputs via macro, plus plain choose/asm, accepted with SDK | RESOLVED. Every wrapper/asm row, macro and plain, is refused on the absence rule with the SDK and accepted with only that check removed. | `receipts/probes/table.md`, rows HOST macro/plain `__builtin_choose_expr`, `_Generic`, `__real__`, `__extension__`, asm output |
| R317-1-F2 MINOR: compiler-free header paste, alias and apply accepted and undeclared | RESOLVED. C03, C05, C13, writer alias and writer apply are named NOT RUN in the page prose (`:461-471`), the cost table (`:1409`) and the COST line (`:16034-16041`). Each is pinned: accepted without a compiler, refused with one. A remaining, different gap in the same mode is R317-2-F1. | `receipts/probes-r2/table.md`, BOUND rows; manager full logs, lines "identity compiler-free bound ..." |
| R317-1-S1 SUGGESTION: mem/str "destination" labels | RETAINED as R317-2-S3 | `test_builder.py:12088-12091` |
| R316-1-F1 MAJOR: `__extension__ &` (C08 macro, C09 plain) accepted with SDK | RESOLVED with the SDK. Both are refused on the absence rule and accepted with it removed. C09 without a compiler is part of R317-2-F1. | `receipts/probes-r2/table-c.md` |
| R316-1-F2 MAJOR: asm output (C10 macro, C11 plain) accepted with SDK | RESOLVED with the SDK. Both are refused on the absence rule and accepted with it removed. C11 without a compiler is part of R317-2-F1. | `receipts/probes-r2/table-c.md` |
| R316-1-F3 MINOR: C03, C05, C13 undeclared without compiler | RESOLVED, as for R317-1-F2 | BOUND rows |
| R316-1-F4 SUGGESTION: C16/C17 without compiler, outside #544 | ADDRESSED by disclosure. They are named NOT RUN and pinned. They are still accepted without a compiler, as declared. | BOUND C16/C17 rows |
| Inherited R272-1 and R273-1 published macros | RESOLVED in both modes, on the named rules, with disconnected controls | `receipts/probes/table.md`, CTRL rows |
| Inherited R273-S3, verifier `#else` deleted | RETAINED unchanged, as scoped by the issue. Accepted at base and head, in both modes, with and without the new checks. | `receipts/probes/table.md`, S3 row |

## What was verified, per the assignment

- **The sample never escapes.** `assert_preprocessed_identity_sample` (`test_builder.py:5227-5303`) compiles a copy of the preprocessed unit with the sample declared `register`. The pinned SDK refuses every address spelling I tried (`receipts/probes-r2/table.md`, ESC rows):
  - `sizeof(&id)`
  - `__typeof__(&id)`
  - asm `"m"` and `"+m"`
  - `&id + 0`
  - a pointer initializer
  - a macro `&(x)` after the guard

  Each refusal is on the absence rule, and each row passes with the check removed. The in-gate rows cover `__extension__ &`, choose, generic, real and wrapped extension address. Nested functions are refused unit-wide, in another function and before the read as well as capturing (`table-b.md`), and so is a forged system-header linemarker (refused earlier by the directive pin).
- **Storage class.** The COST line reports automatic storage with no specifier. Every explicit storage prefix on the real sample (`auto`, `register`, `const`, `volatile`, `static`) is refused by the pre-existing statement rule before the new check (`table-b.md`), so that report is accurate for any accepted firmware. The in-gate boundary loop exercises the new check's own storage branch.
- **The interval.**
  - The two exceptions accept these spellings: hex, `ull`, compact and macro-literal masks, a second diagnostic call, and two sample arguments in one call.
  - 22 new near misses, all macro-borne. Without a compiler, all 22 are refused on the macro replacement rule.
  - With the compiler, 19 are refused on the absence rule's sentence. 18 of those 19 are accepted with the rule disconnected. The 19th, a trailing `& 2u` on a void operand, is invalid C and is then refused by the compile itself. The 19 cover `+`, `?:`, extra parentheses, a comma assignment, postfix `++`, `unsigned long int` and `unsigned int` casts, a parenthesised callee, `sizeof`, a subscript, a double mask, a negative literal, a char literal, `if (1)`, the trailing `& 2u`, a reversed mask, a comma assignment after the mask, and two valid hostile `printf` macros.
  - The other 3 are refused earlier with the compiler by the pre-existing -E boot-path comparison, with the new check connected or not: the assigning statement expression, the `__typeof__` declaration, and `++` in the next statement.
  - The exception is S2.
  - A bare asm, and asm naming no sample, is refused (in-gate rows). Asm in a callee is S1.
  - Goto-based and magic-redefinition forgeries are refused by pre-existing rules.
- **Round-1 probe set rerun unchanged** (`cases_544.py` and `probe_gate1b.py`, byte-identical to the round-1 packet; sha256 in MANIFEST). Six configurations, 30 cases each, `receipts/probes/table.md`. Every prior bypass is refused with the SDK on the absence rule and passes with the rule disconnected. Legitimate rows are unchanged, apart from the disclosed conservative read-through-macro cost and the pre-existing text-rule cost of `(void)(1u & id)`.
- **Corpus and totals, #408 acceptance 4.** In the manager's full source runs at this head, the source hashes match this checkout for `test_builder.py` (`a8f6ee12...`), `BAREMETAL_FIRMWARE.md`, `milan_baremetal.c` and `milan_csr.sv`:
  - SDK: 348/348 mutations refused, and 38/38 firmware plus 4/4 Makefile edits accepted.
  - Compiler-free: 249/249 mutations refused, and 35/35 plus 4/4 accepted.
  - Base: 280 and 222 mutations, 29 firmware edits accepted.

  The only deleted builder lines are the two-line `assert_preprocessed_boot_path(...)` call, which was split rather than removed, so no row or accepted case was dropped. The row arithmetic: 280 + 68 = 348, and 222 + 27 = 249.
- **Compiler-free declarations.** The seven named forms are NOT RUN in the prose, the cost table and the COST line. They are pinned accepted without a compiler and refused with one. The `__CONCAT` sentence is restored in corrected form (`BAREMETAL_FIRMWARE.md:430-432`, `:461-462`). The gap is F1.
- **Static gates at this head, run here.** All exited 0 (`receipts/static/`):
  - `docs_check`
  - `check_doc_style`
  - `gen_toc --check`
  - `check_doc_paths`
  - `check_py_idiom`
  - `check_em_dash --base ffcbd33d`
  - `check_baremetal_only --check`
  - `git diff --check ffcbd33d HEAD`

  `gen_toc` and `check_em_dash` ran in a private virtual environment, installed from `tools/markdown/requirements.txt` with `--require-hashes`, under the unpublished scratch directory.
- **Hosted, exact head, at 00:59Z** (`receipts/hosted-check-runs.txt`): 16 success and 1 skipped (Physical gPTP, nightly/manual, not hardware proof). Three were still in progress: `docs-check`, Verilator shards 1/5 and 4/5. The manager owns hosted and act acceptance.

## Reviewer-owned lens ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 open) | issue #544 acceptance; assignment 5823832945; decision 5824093785; `test_builder.py:5120-5303`, `:11270-11281`, `:12052-12224`, `:15944-16047`; `BAREMETAL_FIRMWARE.md:427-471`, `:1406-1409`; all probe tables | R317-2 | 77e9ca5ea9e04a7618c577ab511baec63b39dc05 |
| RTL | CLEAN | diff `ffcbd33d..77e9ca5e` touches no HDL (2 files: builder test, doc); `hdl/common/csr/milan_csr.sv` hash `420b4866...` equals the manager's run; the new check ties the compiled read address and guard magic to the RTL model (`test_builder.py:5253-5254`, `model.identity`, `model.identity_default`); the magic-redefinition probe is refused on the RTL A_ID default rule; 46/46 RTL variants elaborate in both manager runs | R317-2 | 77e9ca5ea9e04a7618c577ab511baec63b39dc05 |
| Robustness | UNCLEAN (F1 open) | tokenizer, delimiter and fail-closed paths at `test_builder.py:5170-5226` (unbalanced input, index guards, literal forms); diagnostic compile env and returncode (`:5290-5303`); macro-free and macro-borne near misses in both modes; storage, nested-function, linemarker, goto and frame-address probes (`receipts/probes-r2/*`) | R317-2 | 77e9ca5ea9e04a7618c577ab511baec63b39dc05 |
| Tests | UNCLEAN (F1 open) | new mutation rows, accepted cases, storage boundary loop, disconnected-control loops (`test_builder.py:14619-14643`, `:15944-16047`); independent closure-cell disconnection in `probe_gate1b*.py`; manager full-run counts | R317-2 | 77e9ca5ea9e04a7618c577ab511baec63b39dc05 |
| Docs | UNCLEAN (F1 open) | `BAREMETAL_FIRMWARE.md:427-471`, `:1404-1411`, `:1704-1748` against measured behaviour and counts; static doc gates rc 0 | R317-2 | 77e9ca5ea9e04a7618c577ab511baec63b39dc05 |

## Real limits

- **Harness scope.** My probes grade through gate 1b's own `assert_boot_contract()`, hooked before `assert_subset_refuses()`. They are not the full gate bank. The full-bank totals quoted are the manager's public runs, whose source hashes I matched.
- **Disconnection method.** The "check removed" configurations replace the whole `assert_preprocessed_identity_sample` or `assert_identity_macro_free` closure cell. Rows refused by an earlier or unrelated rule, marked `other`, are not evidence for the new rule.
- **SDK identity.** The pinned SDK is `riscv32-linux-gcc`, GCC 14.3.0, Buildroot 2021.11-18033. `test_firmware_compiler.sdk.verify()` verified it on every SDK run.
- **Verilator was not used.** No HDL changed.
- **The clobber reproduction is a reduced standalone unit**, not the gate's stubbed census input. The shipped firmware's actual optimisation level was not built here; LiteX `common.mak` is the conventional source of `-Os`.
- **Blocked, in-flight and not-run evidence.** No Docker, act, full builder, PP, gPTP or Yosys bank, or hardware. Physical calibration was NOT RUN. Field skips are not hardware proof. Hosted jobs were still in flight at capture.
- **Clone state.** The `external` submodule is uninitialised in this clone. Its gitlink is unchanged.
- **Restore check.** After the probes, the clone was verified exact (`receipts/restore-check.txt`):
  - HEAD and tree match the head under review.
  - The index is identical to the HEAD tree (modes and blob ids).
  - The worktree is clean and holds no ignored or untracked files.
  - The submodules sit at their gitlinks with no changes: `gptp-processor e5dcea6e`, `protocol-processor 09f9bf38`, `third_party/verilog-axis 48ff7a7e`, `external efeb541a`.

## Pending manager duties

- Publish this report and the MANIFEST-listed receipts.
- Route F1 to the executor for one of the three outcomes, or record a maintainer decision.
- Decide whether S1 becomes a follow-up Issue.
- After a new head, run a re-review covering at least Conformance, Robustness, Tests and Docs.
- Accept hosted and act evidence at the exact head. The three in-flight jobs must conclude.
- Build and validate the final current-dev candidate at the merge turn: source base `ffcbd33d`, live dev `c266432d`.
- Post-merge containment.
- Physical calibration remains NOT RUN.

## Reproduction

From a checkout at the head, with the verified pinned SDK directory as `SDK`:

```sh
python3 -B PACKET/probe_gate1b.py --mode sdk --sdk SDK --rev head --tag head-sdk --outdir OUT
python3 -B PACKET/probe_gate1b_r2.py --cases cases_544_r2d --mode absent --rev head --tag r2d-head-absent --outdir OUT
python3 PACKET/tabulate2.py OUT r2d-head-sdk r2d-head-sdk-disconnect r2d-head-absent r2d-base-absent
```

Add `--disconnect` to replace only the #544 check of that mode, and `--rev base` to read the builder at `ffcbd33d`. Case modules:
- `cases_544.py`: round 1, unchanged.
- `cases_544_r2.py`: exceptions, near misses, escapes, bounds and limits.
- `cases_544_r2b.py`: storage and nested functions.
- `cases_544_r2c.py`: prior C08-C11.
- `cases_544_r2d.py`: macro-free forms, F1.
- `cases_544_r2e.py`: brace delimiter, S2.

Receipts had the reviewer host's home prefix replaced by `$HOME` (`receipts/redaction.txt`).

R317-2 FINISHED
