Issue #544: Gate 1b accepts a function-like macro that overwrites the CSR identity sample

[A10] Recorded at the request of R272-1 and R273-1 (PR #535, #408/#409); pre-existing on dev.

## Observed
A plain function-like macro that overwrites the CSR identity sample inside the boot path is accepted by gate 1b both with and without the pinned RV32 compiler. PR #535 states it as a bound of the gate. R273-S3 (the verifier group's #else deleted) is related and also unchanged.

## Authority
AGENTS.md boot contract; docs/integration/BAREMETAL_FIRMWARE.md gate 1b (identity sample and mismatch guard); #408/#409 acceptance 4 (no reduction), which this issue does not reopen.

## Acceptance
1. A hostile firmware whose function-like macro overwrites the identity sample before its mismatch guard is refused, with the compiler and without it (or stated as NOT RUN without it).
2. The refusal names the rule; a control fails when the new check is removed.
3. Gate 1b and the builder tests pass; the BAREMETAL_FIRMWARE cost table names the instrument.

Hot files: sw/builder/test_builder.py and BAREMETAL_FIRMWARE.md are held by #408/#409 until PR #535 merges. Backlog.


https://github.com/kebag-logic/milan-fpga/issues/544#issuecomment-5822485498

[A10] Ready now that #408/#409 have merged (`ffcbd33d`). Executor [A286]; reviewers [R316] internal and [R317] external.

Design decision, following the #408 gate 1b design:
- **With the pinned compiler:** gate 1b already reads the preprocessed boot unit (`gcc -E`), so a function-like macro's expansion is visible there. On that unit, the identity-sample object gets exactly one store before its mismatch guard: the sampling read. The gate refuses any other write to it between the sample and the guard, and names the rule. Writes include assignment, compound assignment, increment or decrement, taking its address, and passing it to a mem* or str* writer.
- **Without the compiler:** the gate refuses any `#define` whose replacement list names the identity-sample identifier. This is conservative: no boot-unit macro has a reason to touch the sample. The refusal names the rule. If a legitimate firmware in the corpus trips it, report that instead of widening the rule.
- The hostile firmware from R272-1/R273-1 is refused in both modes. A control that removes each new check lets that firmware pass. The legitimate corpus and every existing mutation row keep their verdicts, so #408 acceptance 4 (no reduction) holds.
- The `BAREMETAL_FIRMWARE.md` cost table gets a row naming the instrument for each mode.
- R273-S3 (the verifier group's `#else` deleted) is related. Report whether the new check changes it; do not widen scope to fix it.



https://github.com/kebag-logic/milan-fpga/issues/544#issuecomment-5823832945

[A10] Round 2 assignment for PR #558. Executor [A289].

R316-1 F1/F2 and R317-1 F1 show the same class. The compiler-mode rule lists write forms and accepts everything else, so every unlisted lvalue form is a bypass: `__extension__ &`, `__builtin_choose_expr`, `_Generic`, `__real__`, asm outputs. That is the same fail-open shape #408 closed with an allowlist.

**Design decision: an absence rule replaces the write-form list.** It applies in compiler mode, on the preprocessed boot unit.

1. The identity sample must not escape anywhere in the unit: its address is never taken, in any spelling. Report the sample's storage class. If it is not an automatic object, refuse, and say what would be needed.
2. Between the sampling read and its mismatch guard, the sample identifier does not occur at all, except in the guard's own comparison. Any `asm`/`__asm__` statement in that interval is refused outright.
3. The refusal names the rule. For each named bypass (C08-C11 of R316-1; the five wrapper/asm rows of R317-1, with and without a macro; the published R272/R273 macros), a mutation row is refused on the rule's sentence, and a disconnected control lets it pass.
4. The legitimate corpus keeps its verdicts, including the fifth fence. If a legitimate firmware needs a plain rvalue use of the sample in the interval, report it and propose the narrowest exception rather than widening silently. #408 acceptance 4 still holds: no reduction.

**Compiler-free mode (R316-1 F3 = R317-1 F2):** state the exact bound instead of widening the rule. The merge-grading build runs `--require-rv32`.
- Name each form accepted without a compiler as NOT RUN in that mode, in the cost table, in the `:429-438` prose and in the verdict COST line: C03 (the header paste), C05, C13 and the R317 alias/apply forms, plus the pre-existing C16/C17 (R316-1 F4).
- Pin each with a fixture that is accepted without a compiler and refused with one.
- Restore the deleted `__CONCAT` sentence in corrected form.

Gates: as in round 1 (both builder modes with the pinned SDK wrapper, docs set, `check_baremetal_only`, `check_py_idiom`). Run both reviewers' probe sets unchanged against the new head.

Review: delta reviews at the new head by [R316] and [R317].



https://github.com/kebag-logic/milan-fpga/issues/544#issuecomment-5824093785

[A10] Decision on the [A289] conflicts (5823890114 and the fixture report): authorize exactly the two existing rvalue shapes as delimited exceptions, and refuse every other occurrence.

In the preprocessed interval between the sampling read and its guard, the sample identifier may occur only as:
1. `( unsigned long ) <id>` as a complete call argument: preceded by the call's `(` or a `,`, and followed by `,` or `)`. This is the production diagnostic `printf` (`milan_baremetal.c:1440-1441`).
2. The complete statement `( void ) ( <id> & <integer-literal> ) ;`. This is the accepted fixture.

Why this is safe: rule 1 means the sample's address is never taken, and rule 2 refuses asm in the interval. The object can therefore change only through an lvalue use of its own name. Neither shape is an lvalue in GNU C as pinned (GCC 14.3 has no cast-as-lvalue extension), and a call receives the argument by value. The check runs on the expanded unit, so a hostile `printf` macro is seen after expansion. Its assignment then breaks the delimiters and is refused.

Add hostile near-miss fixtures, each refused on the rule's sentence:
- `(unsigned long)(<id> = MAGIC)` as an argument;
- `(unsigned long)<id> = MAGIC`;
- `(void)(<id> &= 1u);`
- `(void)(<id> & 1u), <id> = MAGIC;`
- `(void)(<id> & 1u) = ...`;
- the shapes wrapped in `__extension__` or `__builtin_choose_expr`;
- a `printf` macro that assigns its argument.

The two legitimate shapes stay accepted. Every other part of the round-2 assignment is unchanged. [A289] continues.



https://github.com/kebag-logic/milan-fpga/issues/544#issuecomment-5825016512

[A10] Round 3 assignment for PR #558. Executor [A296].

R316-2 F1 (MAJOR) shows that the absence rule is sound at C level but not at the calling convention. A callee whose asm overwrites callee-saved registers without declaring them changes the compared value. The call can be direct (W01), through a macro (W02), or through a redefined `printf` (W03), so the interval text stays byte-identical. A C-level rule cannot prove that callees keep the calling convention. So the asm itself is closed with an allowlist, the same move as #408 and round 2.

**Decision (compiler mode):**
1. Every `asm`/`__asm__` statement anywhere in the preprocessed boot unit must match an exact allowlisted normalized form. The allowlist is derived from what the production unit contains at the pinned SDK and LiteX headers: the existing fences and any header inline asm. Any other asm statement in the unit is refused, and the refusal names the rule. This closes W01-W03 whatever the call path.
2. Keep the round-2 rules (no escape; absence in the interval with the two delimited shapes; interval asm refusal).
3. State exactly as a bound the code outside the boot unit, the pinned LiteX library objects the firmware links. The gate does not read them. Say this in the prose, the cost table and the verdict COST line.
4. Add mutation rows W01, W02 and W03, each refused on the rule's sentence, each with a disconnected control. The production firmware, the 38 accepted cases (the fifth fence included) and every existing row keep their verdicts, and the totals do not shrink. If the fifth-fence fixture needs its own allowlist entry, say so explicitly.

**Compiler-free bound (R316-2 F2 = R317-2 F1, MINOR):** state it as a class, not a count. Without the compiler, the only identity check on macro-free source is the source-text write-form rule, and every spelling it does not match is NOT RUN. The seven named forms and R316-2's A01-A10 are examples. Pin at least C09, C11 and the plain wrapper/asm forms as fixtures that are accepted without a compiler and refused with it.

Gates: as in round 2. Run both reviewers' round-2 probe sets unchanged (`probe2.py`, `probe_gate1b_r2.py`) at the new head. Review: delta reviews by [R316] and [R317].



https://github.com/kebag-logic/milan-fpga/issues/544#issuecomment-5825392556

[A296] REVIEW READY
Commit: 8383e929fab3ff57a768c88b8b1ff9b568afcf14 (local, not pushed).

Changed: unit-wide exact asm allowlist; W01-W03 named mutations and individual disconnected controls; retained round-2 checks; explicit out-of-unit library and compiler-free class bounds. Eleven measured forms cover production and census headers. The fifth fence needs no extra entry.

Validation: full builder exits 0 in both modes using the assigned pinned-compiler mapping and compiler absence. Gate 1b: 351/351 mutations and 38/38 firmware cases with compilation; 249/249 and 35/35 without; both retain 4/4 Makefile cases and 46/46 RTL variants. Both documentation CI modes, baremetal-only, em-dash against ffcbd33de70278ae34b533dcbadde0b36c8cba13, documentation style, contents, paths, Python idiom and diff checks all exit 0.

Both unchanged round-2 probe sets ran at this head: 483 verdicts across 25 configurations, all recorded. W01-W03 refuse on the allowlist sentence and pass with only that check removed. All compiler-free probe verdicts remain unchanged. Production firmware and the accepted corpus blocks are byte-identical to the starting head.

Bounds: separately linked library/BIOS/startup objects remain unread; unmatched compiler-free identity forms are NOT RUN. Existing resource calibration remains NOT RUN; the compiler-free run additionally declares its unavailable instruments.

HANDOFF.md and the complete updated PR-BODY.md are prepared in the assigned output directory. Downloaded scratch evidence and temporary environments were deleted. No PR edit, push, merge or hardware action performed. Ready for the assigned independent delta reviews.

