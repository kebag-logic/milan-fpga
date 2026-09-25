[R317] NEGATIVE - exact head b068763c849a18096b0f46cf9b18e0f904e4d708

Round R317-1: external, cleared-context, independent review of PR #558 (issue #544).
- Exact head `b068763c849a18096b0f46cf9b18e0f904e4d708`, tree `dd5e37eca811750c07abe128b2d01d13ab05e9fb`.
- Source base and live dev: `ffcbd33de70278ae34b533dcbadde0b36c8cba13`.
- All five lenses were applied: Conformance, RTL, Robustness, Tests and Docs.
- Order of work: I reconstructed scope from AGENTS.md, the issue body, the #544 decision (comment 5822485498), the executor's public comments, the public evidence tree at `5de8b40d` (including R272-1 and R273-1 on PR #535), and the diff. I then probed.
- This report was written before I read any other review of PR #558. When it was written, the PR had no published review findings, only the two "review started" notes.

## Verdict in one paragraph

The change does what it says for the shapes it enumerates, and it reduces nothing.
- Both published hostile macros are refused in both modes, on the named rule. Removing only that mode's check lets them through.
- Every base mutation row and accepted case is present at the head, byte-identical in fixture and reason pin. Both gate 1b runs pass with the stated totals (304/304 and 38 + 4/4 with the pinned SDK; 249/249 and 35 + 4/4 without a compiler).
- R273-S3 is unchanged, as the PR reports.

The verdict is NEGATIVE because the compiler-mode rule that the page calls "one store before its mismatch guard" is still defeated by a function-like macro that overwrites the sample. This is the exact class that acceptance 1 names.
- With the pinned SDK, gate 1b accepts five overwriting spellings, each invoked as `MILAN_FORGE(id);` before the guard:
  - `__builtin_choose_expr(1, x, x) = MILAN_ID_MAGIC`
  - `_Generic(0, default: x) = MILAN_ID_MAGIC`
  - `(__real__ x) = MILAN_ID_MAGIC`
  - `(__extension__ x) = MILAN_ID_MAGIC`
  - an inline-asm output operand `"=r"(x)`
- The pinned GCC 14.3 compiles each one into a guard that can never fire (R317-F1, MAJOR).
- A second, MINOR finding: without a compiler, a header-macro paste and two indirect macro invocations still forge the sample. Neither the page nor the gate print now states this. The explicit bound the page carried before this change was deleted (R317-F2).

## Findings

### R317-F1 - MAJOR - Conformance, Robustness, Tests, Docs

**Artifact:**
- `sw/builder/test_builder.py:5170-5248` (`assert_preprocessed_identity_sample`). Specifically:
  - `:5218` unwraps only `(`/`)` around the sample.
  - `:5230` tests only the single token before and after that span.
  - The mem*/str* loop follows it.
- Page: `docs/integration/BAREMETAL_FIRMWARE.md:433-437` ("Assignments ... are refused", "Parenthesized sample names remain the same protected object") and `:1369` ("the identity-sample object gets one store before its mismatch guard").

**Title:** The compiler-mode single-store rule misses an assignment or write reached through an lvalue-preserving GNU/C11 wrapper, or through an inline-asm output operand. So a function-like macro still forges the identity sample with the pinned SDK.

**Authority and evidence:**
- #544 acceptance 1: "A hostile firmware whose function-like macro overwrites the identity sample before its mismatch guard is refused, with the compiler ...".
- Decision 5822485498: "the identity-sample object gets exactly one store before its mismatch guard ... The gate refuses any other write to it between the sample and the guard".
- Measured through gate 1b's own `assert_boot_contract()` at the head with the pinned SDK (`receipts/probes/head-sdk.json`, table `receipts/probes/table.md`). Each case is `#define MILAN_FORGE(x) <replacement>` plus `MILAN_FORGE(id);` before the guard:

| replacement | head, SDK | base, SDK | head, no compiler |
|---|---|---|---|
| `__builtin_choose_expr(1, x, x) = MILAN_ID_MAGIC` | ACCEPTED | ACCEPTED | refused (macro replacement rule) |
| `_Generic(0, default: x) = MILAN_ID_MAGIC` | ACCEPTED | ACCEPTED | refused (macro replacement rule) |
| `(__real__ x) = MILAN_ID_MAGIC` | ACCEPTED | ACCEPTED | refused (macro replacement rule) |
| `(__extension__ x) = MILAN_ID_MAGIC` | ACCEPTED | ACCEPTED | refused (macro replacement rule) |
| `__asm__ volatile ("" : "=r"(x) : "0"(MILAN_ID_MAGIC))` | ACCEPTED | ACCEPTED | refused (macro replacement rule) |
| controls: `x = MILAN_ID_MAGIC`, `((x) = MILAN_ID_MAGIC)` | refused (single-store rule) | ACCEPTED | refused (macro replacement rule) |

- The same two spellings written directly in the source, without a macro, are ACCEPTED in both modes at base and head:
  - `__builtin_choose_expr(1, id, id) = MILAN_ID_MAGIC;`
  - the asm output operand.
- They are real overwrites, not reader artefacts (`receipts/semantics.txt`, source `semantics/forge_semantics.c`):
  - With `csr_id = 0xdeadbeef`, a host GCC build of each spelling returns "no mismatch" at -O0 and at -O2.
  - The pinned SDK (GCC 14.3.0, `-std=gnu99 -O2`) compiles forms 1 to 4 to `li a0,0; ret`: the guard is deleted.
  - Form 5 compiles to a comparison of `MILAN_ID_MAGIC` with itself.
  - No diagnostic is emitted.
- Why the rule misses them: after `(`/`)` unwrapping, the sample's neighbours are `,`/`,`, `:`/`)`, `__real__`/`)`, `__extension__`/`)`, and a blanked string/`)`. None of these is in the store set or is `&`, `++` or `--`.

**Impact:**
- On the configuration that grades a merge (hosted, `--require-rv32`), a firmware whose function-like macro overwrites the CSR identity sample before its mismatch guard is still accepted. The fabric is then configured on a foreign or forged identity.
- This is not a regression: base accepts the same firmware.
- But it is the class #544 exists to close. The PR closes #544 (`Closes #544`), and the page and gate print claim a single-store guarantee that the rule does not hold.

**Required outcome:**
- With the compiler, any write to the identity-sample object between the sampling read and the mismatch guard is refused. That includes a write through an lvalue-preserving wrapper (`__builtin_choose_expr`, `_Generic`, `__real__`/`__imag__`, `__extension__`, and any other the pinned GCC accepts) and through an asm output (`=`/`+`) constraint.
  - One way: refuse any occurrence of the sample in the interval other than as a plain rvalue operand.
  - Another: refuse those constructs in the interval outright.
  - Or, if a bound is chosen instead, state it exactly on the page and in the gate print, and keep #544 open.
- Add hostile controls for these spellings, pinned on the rule's sentence and failing when the check is removed.

**Verification:**
- Rerun `probe_gate1b.py` with `cases_544.py` at the fixed head with the SDK. Every `HOST macro ...` wrapper and asm row must be REFUSED on the single-store rule (or on a named successor).
- The plain `__builtin_choose_expr`/asm rows must be REFUSED as well.
- `LEGIT ...` rows keep their verdicts. The gate 1b SDK run stays green with its accepted count unchanged.

### R317-F2 - MINOR - Conformance, Robustness, Docs

**Artifact:**
- `sw/builder/test_builder.py:5120-5168` (`assert_identity_macro_free`: this file's `#define`s and direct calls only).
- The absent-mode verdict print at `:15982-15995`.
- Page `docs/integration/BAREMETAL_FIRMWARE.md:429-438` and `:1368-1370`.

**Title:** Without a compiler, the sample is still forged through a header macro paste and through indirect macro invocations. The page's explicit bound for this was deleted and not restated.

**Authority and evidence:**
- #544 acceptance 1: "... and without it (or stated as NOT RUN without it)".
- The base page's `MILAN_ID` row named the bound: "`MILAN_FORGE(id);` is not refused ... and neither is a paste through a macro a header defines, `__CONCAT(i, d) = MILAN_ID_MAGIC;`". The diff removes that sentence.
- `:431-438` now says the header paste is outside the paste ban, and that "Without the compiler, the replacement-list rule described below applies". That rule does not see a header macro.
- Measured at the head without a compiler (`receipts/probes/head-absent.json`). ACCEPTED at base and head:
  - `__CONCAT(i, d) = MILAN_ID_MAGIC;`
  - `#define MILAN_SET(y) y = MILAN_ID_MAGIC` / `#define MILAN_FORGE MILAN_SET` / `MILAN_FORGE(id);` (object-like alias)
  - `#define MILAN_APPLY(f) f` / `MILAN_APPLY(MILAN_SET)(id);` (writer name passed through an argument)
- All three are REFUSED with the SDK at the head, on the single-store rule.
- The absent-mode verdict print lists what is NOT RUN without the instruments, and none of these three is in it.
- The `:1370` wording "checks local definitions and direct calls, without general expansion" hints at the limit but does not say that these firmwares are accepted.

**Impact:**
- Hosted grading always has the compiler, so the merge-grading configuration is not affected.
- A reader of an absent-mode run, or of the page, is told that the identity sample is covered by the replacement-list rule. In fact three measured forging spellings are neither refused nor declared NOT RUN.

**Required outcome:** Do one of the following:
- refuse these shapes without a compiler; or
- state on the page's `MILAN_ID`/absent-mode rows, and in the absent-mode NOT RUN wording, that header-macro pastes and indirect invocations (an alias, or a writer name passed as an argument) forge the sample without a compiler and are NOT RUN there.

**Verification:** Read the page and the absent-mode gate print. Alternatively, the three rows are REFUSED in `probe_gate1b.py --mode absent`.

### R317-S1 - SUGGESTION - Tests

**Artifact:** `sw/builder/test_builder.py:12033-12036`: the mutation rows "identity macro memory destination" and "identity macro string destination".

**Detail:**
- `__builtin_memset((void *)(uintptr_t)id, 0, 4)` passes the sample's value as an address. It does not write the sample.
- These two rows therefore pin a conservative cost (disclosed at `:1369` and in the gate print), not a hostile write, yet they are counted among the refused hostile mutations.

**Recommended:** Label them as cost rows. Separately, add a genuine mem* destination row (`__builtin_memcpy(&id, ...)`), which the address rule refuses first.

## Probes beyond the published cases

All probes were run through `assert_boot_contract()` (`probe_gate1b.py`, `cases_544.py`, per-case table in `receipts/probes/table.md`).

Six configurations were measured:
- head SDK, base SDK, head SDK with only the single-store rule removed;
- head absent, base absent, head absent with only the replacement rule removed.

| case | head SDK | base SDK | head SDK, check removed | head absent | base absent | head absent, check removed |
|---|---|---|---|---|---|---|
| published R272 / R273 macros | single-store | ACC | ACC | replacement | ACC | ACC |
| paste via local `##` macro; paste building the writer name | paste ban | paste ban | paste ban | paste ban | paste ban | paste ban |
| paste via header `__CONCAT(i, d)` | single-store | ACC | ACC | ACC (F2) | ACC | ACC |
| macro takes address and stores | CSR pointer-cast rule | same | same | same | same | same |
| macro sets a local pointer alias and stores | -E boot-path comparison | same | same | replacement | ACC | ACC |
| pointer alias declared before the sample (local or file scope), set by macro | single-store | ACC | ACC | replacement | ACC | ACC |
| macro write in a nested block / in an `if` block | single-store | ACC | ACC | replacement | ACC | ACC |
| plain write in a nested block | text identity rule | same | same | same | same | same |
| GNU lvalue wrappers and asm output via macro | ACC (F1) | ACC | ACC | replacement | ACC | ACC |
| plain `__builtin_choose_expr` / asm output | ACC (F1) | ACC | ACC | ACC | ACC | ACC |
| object-like alias; writer name through an argument | single-store | ACC | ACC | ACC (F2) | ACC | ACC |
| `#define id milan_forged` between read and guard | guard-shape rule | same | same | same | same | same |
| string argument `")"` before the sample | single-store | ACC | ACC | replacement | ACC | ACC |
| write after the guard, plain and via macro | ACC | ACC | ACC | ACC | ACC | ACC |
| read through a function-like macro | ACC | ACC | ACC | replacement (disclosed cost) | ACC | ACC |
| `(void)(1u & id);` | text identity rule (pre-existing cost) | same | same | same | same | same |
| R273-S3, verifier `#else` deleted | ACC | ACC | ACC | ACC | ACC | ACC |

**Notes on the table:**
- The write after the guard stays accepted everywhere.
- R273-S3 is unchanged, as the PR reports.
- A pointer alias to the automatic sample cannot exist before its declaration. The measured "alias before the sample" is a pointer object declared first and aimed at the sample by a macro.
- Every refusal the new rules introduce is on the rule's named sentence.
- Every case the new rules refuse passes when only that rule is removed. This reproduces the in-suite control independently of it, using a closure-cell replacement in my own harness.

## Measured at the exact head

- **Gate 1b alone, pinned SDK** (verified by `scripts/ci_rv32_sdk.py` `verify()`; GCC 14.3.0, `riscv32-buildroot-linux-gnu`), with Verilator 5.050 (wrapper identity checked; `.github/workflows/elaborate.yml` pins `v5.050`):
  - result: `GATE 1b PASS; 0 NOT RUN; 513 actual firmware compiler invocations`;
  - 304/304 mutations refused, 38 firmware and 4/4 Makefile edits accepted, 46/46 RTL variants elaborated;
  - the in-suite control printed: "identity-sample single-store rule: hostile macros refused; removing only this check lets the hostile control pass".
  - Receipt: `receipts/gate1b/gate1b-sdk.log`.
- **Gate 1b alone, cross compilers hidden:**
  - result: `GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations`;
  - 249/249 refused, 35 + 4/4 accepted, 46/46 RTL; verdict `TEXT RULES ONLY, AND WEAKER`; the macro-replacement control line printed.
  - `--absent --require-rv32` fails with "--require-rv32: the hosted firmware instruments must run" (rc 1).
  - Receipts: `receipts/gate1b/`.
- **Row identity (#408 acceptance 4):**
  - Every accepted case and mutation row of the base gate source (sha256 `81113374...`) and the head gate source (`fa28af04...`) was dumped, as label, fixture digests and reason pin, against the same tree.
  - In both modes, the base rows are the head's unchanged prefix: 29 of 38 and 280 of 304 (SDK); 29 of 35 and 222 of 249 (absent).
  - There are no missing, changed or duplicate labels. The additions are exactly the 9/6 accepted cases and 24/27 identity rows in the diff (`receipts/rows-compact/compare.txt`).
  - Together with both passing head runs, no pre-existing row changed its verdict or its pin.
- **Focused static checks** (`receipts/static/summary.txt`):
  - rc 0: `docs_check.py` (165 md files, 0 findings), `check_doc_style.py`, `check_doc_paths.py`, `check_py_idiom.py`, `check_baremetal_only.py --check`, and `git diff --check` base..head.
  - No U+2014 in added lines.
  - `gen_toc.py --check` and `check_em_dash.py` could not run: the pinned Markdown renderer is not installed here, and a shared install is out of scope.
- **Hosted, exact head** (`receipts/hosted-check-runs.txt`):
  - Executed and successful: `docs-check`, `docs-check-no-git`, `elaborate`, `rtl-fast`, `verilator-suites` with its five shards, `yosys-portability` with its four shards, `yosys-elaboration`, `verilator-lint`, `bdd-conformance`, `wire-accountability`, `changes`, `full-ci-gate`.
  - `Physical gPTP (nightly and manual)` is a skipped context, not an executed job.
  - I inspected these results; I did not reproduce them.
- **Clone integrity after the probes:**
  - HEAD and tree are exact.
  - The worktree and index equal HEAD, with no untracked files.
  - The two changed blobs hash to their index entries (`505dc9a6...`, `96fb3f11...`), mode 100644.
  - The four submodule gitlinks are unchanged and identical at base and head.

## Issue #544 acceptance, as measured

1. **Not met for the class.**
   - The two published spellings are refused in both modes.
   - With the compiler, five further function-like macros that overwrite the sample are accepted (F1).
   - Without the compiler, three forging spellings are neither refused nor stated as NOT RUN (F2).
2. **Met.** The refusals name `identity-sample single-store rule` / `identity-sample macro replacement rule`. The in-suite and reviewer controls both pass the hostile firmware when only that check is removed.
3. **Met.** Gate 1b passes in both modes, and the focused doc gates pass (two could not run here). Cost-table rows `:1369` and `:1370` name the instrument for each mode: the preprocessed boot unit, and phase-3 definitions.

Other items:
- Decision items: R273-S3 is reported unchanged (measured ACCEPTED at base and head in both modes).
- #408 acceptance 4 (no reduction) holds.
- Prior public review findings on PR #558: none existed when this report was written, so none are retained or resolved here. R272-1 F2's request (a public Issue for the plain-macro exposure) is satisfied by #544 itself. That exposure's closure is the subject of F1 and F2 above.

## Reviewer-owned lens ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | #544 acceptance and decision 5822485498 against `test_builder.py:5120-5248`, `:11217-11225`, `:15777-15820`; the probe table; `receipts/semantics.txt` | R317-1 | b068763c849a18096b0f46cf9b18e0f904e4d708 |
| RTL | CLEAN | Diff touches no HDL: only `docs/integration/BAREMETAL_FIRMWARE.md` and `sw/builder/test_builder.py`; submodule gitlinks are identical at base and head. The new compiled check keys on `model.identity`/`model.identity_default`, which match `hdl/common/csr/milan_csr.sv:717` (`A_ID = 'h000`) and `:1940` (`32'h4D49_4C4E`). 46/46 RTL mutation variants elaborated with Verilator 5.050 in both gate 1b runs. Hosted `elaborate`, `verilator-suites`, `yosys-portability` and `rtl-fast` succeeded at this head. | R317-1 | b068763c849a18096b0f46cf9b18e0f904e4d708 |
| Robustness | UNCLEAN (F1, F2) | 30 reviewer cases (`cases_544.py`) in six configurations: pastes, address-taking macros, pointer aliases, nested blocks, post-guard writes, GNU lvalue wrappers, asm outputs, indirect macro invocations, string-argument parsing, `#define` of the sample name; `receipts/probes/` | R317-1 | b068763c849a18096b0f46cf9b18e0f904e4d708 |
| Tests | UNCLEAN (F1) | New rows and controls at `test_builder.py:12000-12053`, `:14449-14473`, `:15777-15820`; row-identity dump base vs head (`receipts/rows-compact/`); both gate 1b runs (`receipts/gate1b/`) | R317-1 | b068763c849a18096b0f46cf9b18e0f904e4d708 |
| Docs | UNCLEAN (F1, F2) | `BAREMETAL_FIRMWARE.md:418-445`, `:1366-1372`, `:1665-1703` against measured behaviour; the gate print's COST line `test_builder.py:15811-15820` and the absent-mode verdict `:15982-15995`; focused doc gates `receipts/static/` | R317-1 | b068763c849a18096b0f46cf9b18e0f904e4d708 |

One SUGGESTION (S1) is recorded under Tests. It does not affect coverage.

## Real limits

- I ran gate 1b alone, not the full builder, static or native banks. For those I rely on the manager's evidence, as the brief states. I found no separate manager bank receipt in the public evidence tree at `5de8b40d` or in the issue and PR comments; it holds the author's receipts.
- The base comparison executed the base revision's `test_builder.py` against the head tree. That tree's firmware, RTL and submodules are identical to base; only the page text differs. I did not run a separate base checkout, because populating one with submodules was not permitted in this session. The base verdicts in the probe tables come from that same arrangement.
- `gen_toc.py --check` and `check_em_dash.py` were not run (renderer dependency absent). The executor reports both at rc 0; I did not reproduce that.
- The pinned SDK used is the manager's existing verified install, which I read without modifying it. I did not extract a fresh SDK.
- The F1 semantics were executed on the host GCC 16.2.1 and shown as assembly on the pinned GCC 14.3.0. No RV32 binary was executed.
- No hardware was used. Physical calibration is NOT RUN, and skipped field contexts are not hardware proof.
- I did not build the candidate merge result on live dev. No act or hosted reruns.
- Receipts have the reviewer host's home prefix replaced by `$HOME` (`receipts/redaction.txt`). Nothing else was changed. Bulky raw dumps (the full row digests and the SDK argv audit) stay unpublished in scratch; their compact forms and digests are published.

## Pending manager duties

- Publish this report and the manifest-listed receipts.
- Route R317-F1 and R317-F2 to the executor. After a fix, re-review Conformance, Robustness, Tests and Docs at the new head, and RTL if any RTL-facing reader moves.
- Own hosted and act acceptance, the internal review, the candidate merge validation against live dev, and post-merge containment.

## Reproduction

Run from a checkout at the exact head, with `P` as this packet:
- `python3 -B $P/probe_gate1b.py --mode sdk --sdk <verified SDK> --rev head --tag head-sdk --outdir <dir>`
- Variants: `--mode absent`, `--rev base`, `--disconnect`.
- `python3 -B $P/tabulate.py <dir> head-sdk base-sdk ...`
- `python3 -B $P/dump_rows.py --mode sdk|absent [--sdk ...] [--gate-source <base test_builder.py>] --out X.json`, then `compact_rows.py` and `compare_rows.py`.
- Gate 1b alone: `python3 -B sw/builder/test_firmware_compiler.py --sdk-destination <SDK> --audit A.jsonl` or `--absent --audit A.jsonl`, with Verilator 5.050 first on `PATH`.

R317-1 FINISHED
