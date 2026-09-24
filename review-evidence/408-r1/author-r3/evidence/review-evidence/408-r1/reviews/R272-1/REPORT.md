[R272] NEGATIVE - exact head a13b6e2e461695cdb8d978444ae499a5a6745429

Round R272-1, internal cleared-context independent review of PR #535 (issues #408 and #409).
Exact head `a13b6e2e461695cdb8d978444ae499a5a6745429`, tree `44729af1c6f9e164d8ca82eda5a47d3708b96a6d`, source base `759da623072358afdb0e9d570a7b4b6a788492c9`.
All five lenses were applied: Conformance, RTL, Robustness, Tests and Docs.

## Verdict in one paragraph

Most of the retirement ledger is measured and holds.
The two issues, the page and the gate print agree on which rules are retired, narrowed or kept.
Every accepted case is refused at base on its retired rule's own sentence and accepted at head, in both compiler environments.
Every hostile control fails when its replacement is disconnected.
Compiler absence is a registered `NOT RUN` that is never counted as coverage, and both hosted builder jobs still require the pinned RV32 compiler.
The verdict is NEGATIVE because protection is weakened, measured with the pinned SDK (the hosted grading configuration).
The per-selection grading that replaces the conditional-reach ban and the ordered cast, store and asm sets does not see a conditional whose `#` follows a form feed, a vertical tab or a NUL byte.
GCC 14.3 honours all three as directives.
So a product-only arm storing into `ADP_CTRL` from a UART command handler is refused at base and accepted at head (F1, BLOCKER).
The `-E` comparison carries the retired splice and `##` bans only for its eight boot tokens.
So a splice or paste that rebuilds the identity local inside `milan_init()` is refused at base and accepted at head (F2, MAJOR).
Two MINOR findings cover an undisclosed new cost and a pre-existing blanking bound on the new "every conditional is graded" claim (F3, F4).

## Findings

### F1 - BLOCKER - Conformance, Robustness, Tests, Docs

**Artifact:** `sw/builder/test_builder.py:2543-2544` (`cpp_directive_re`), `:2609` (`error_line_re`), `:3544` (`directive_re`), `:2700-2742` (`arm_selections`) and `:8396` (its only call).
Docs: `docs/integration/BAREMETAL_FIRMWARE.md:270-277`, `:1282` and `:1317`.

**Title:** Per-selection grading misses conditionals whose `#` follows a form feed, vertical tab or NUL, which drops protection the retired cast and asm sets gave.

**Authority and evidence:**
- #408 and #409 acceptance 4 ("No reduction").
- The round's requirement that no protection weakens.
- The page's own claim at `:275-277`: "Whatever the product's headers select, the product builds one of the firmwares graded, so no arm is read in one state and compiled in another."
- The pinned SDK's GCC 14.3 (`-std=gnu99`) treats a line starting with `\f`, `\v` or NUL before `#ifdef`/`#endif` as a directive (`receipts/cpp/cpp-results.txt`).
- Every C directive reader in gate 1b anchors on `^[ \t]*#`, so it sees no conditional there.
- The census then compiles only the arm the stub tree selects.

Measured through the gate's own `assert_boot_contract()` with the pinned SDK (`receipts/probes/r1-*-sdk.*`, `r2-*-sdk.*`).
Every case sits in `#ifdef CSR_UART_BASE`, which the product's LiteX header defines and the census stub tree does not.
All but the last row are at the end of the first UART command handler.

| Hostile firmware | base 759da623 | head a13b6e2e |
|---|---|---|
| form feed before `#`; `*(volatile unsigned int *)((csr_page << 16) \| MILAN_ADP_CTRL) = 1u;` | REFUSED (cast set) | ACCEPTED |
| form feed before `#`; `*(volatile unsigned int *)0x90000600u = 1u;` | REFUSED (cast set) | ACCEPTED |
| form feed before `#`; `lui`/`sw` inline-asm store to 0x90000600 | REFUSED (asm set) | ACCEPTED |
| NUL before `#`; literal-address cast store | REFUSED (cast set) | ACCEPTED |
| the paged-cast, literal-cast and `lui` stores with a plain `#` (controls) | REFUSED | REFUSED (selection + census/resolver) |
| form feed or vertical tab before `#`; the `0 &&` product-only arm in the choke point's verdict test, which this PR says it closes | ACCEPTED (pre-existing) | ACCEPTED |

Also recorded, for an exact reading of base's own exposure (`receipts/probes/r3-*`):
- A plain-`#` product-only struct-overlay store in a UART handler is ACCEPTED at base and REFUSED at head, which is this head's improvement.
- Its form-feed spelling is ACCEPTED at both.
- The form-feed arm moving `MILAN_ADP_EID_LO` onto `ADP_CTRL` (product arm last) is ACCEPTED at both.

The kept directive-set closure (`:3544`) reads with the same anchor, so `\f#undef`, `\f#pragma` and `\f#include` are outside it too. That part is pre-existing.

**Impact:** On the configuration that grades a merge (hosted, `--require-rv32`), gate 1b accepts a firmware that sets `ADP_CTRL` bit 0 from a UART command handler with no AEM verdict. That is the core boot-contract property, and base refused those spellings. The PR's central claim that every conditional is graded is false for spellings GCC honours.

**Required outcome:**
- Every line the pinned GCC treats as a preprocessing directive must be a directive to every C directive reader in gate 1b: the conditional readers, the `#error` reader, the directive-set closure and the definition readers.
- Either accept the whitespace GCC skips before `#` (space, tab, form feed, vertical tab, NUL) or refuse those bytes before a `#` outside comments and literals.
- Add hostile controls for the form-feed, vertical-tab and NUL spellings, pinned on the replacement's own sentence and failing when it is disconnected.
- Bound the page and gate-print claims to what is measured.

**Verification:** Rerun `scripts/cases_r1.py` and `scripts/cases_r2.py` through `scripts/probe_gate1b.py` at the fixed head with the SDK. Every form-feed, vertical-tab and NUL hostile case must be REFUSED, the plain-`#` controls still REFUSED, and gate 1b's accepted loop still 27/27 plus 4/4.

### F2 - MAJOR - Conformance, Robustness, Tests, Docs

**Artifact:** `sw/builder/test_builder.py:4208-4210` (`boot_path_tokens`), `:3960-3964` (the `PREPROCESSED_PIN` claim) and `:9095-9124` (the identity rule reads blanked, unspliced text).
Docs: `docs/integration/BAREMETAL_FIRMWARE.md:292-304`, `:1283-1284` and `:1318`.

**Title:** The retired splice and `##` bans are carried inside the six boot-path bodies only for the eight boot tokens. A splice or paste that rebuilds any other name a boot-path text rule reads is not compared.

**Authority and evidence:**
- #408 acceptance 2 and 4.
- The pin comment at `:3960-3964`: "Every mutant that makes this gate read a boot path the compiler does not compile fails on it, whether a conditional, a token-joining splice or a paste spelled it."
- The page row at `:1283`.

Measured with the pinned SDK (`receipts/probes/r3-*-sdk.*`): the CSR identity sample is forged inside `milan_init()` before its mismatch guard.

| Spelling | base | head |
|---|---|---|
| `i\` newline `d = MILAN_ID_MAGIC;` (token-joining splice) | REFUSED (splice ban) | ACCEPTED |
| `MILAN_CAT(i, d) = MILAN_ID_MAGIC;` with `#define MILAN_CAT(a, b) a##b` | REFUSED (`##` ban) | ACCEPTED |
| `MILAN_FORGE(id);` with a plain function-like macro | ACCEPTED (pre-existing) | ACCEPTED |

The statement count and the eight tokens agree between the text and `-E`, so the comparison reports nothing. The identity rule reads `i\` + `d`, not `id`.

**Impact:**
- The cost-table row "The `MILAN_ID` local is not assigned or addressed between its CSR read and mismatch guard" is defeated by two spellings base refused.
- The pin comment and page describe a coverage the instrument does not have.
- The same property is already open at base through a plain macro, so the exposure of the property is not new. The spelling-level reduction and the false claim are new.

**Required outcome:**
- Either the text rules inside the six bodies read names after phases 1 and 2 and after pasting (for example, refuse a `##`-built or splice-built name there, or compare every identifier those rules key on), or narrow the retirement and state exactly which names are compared, at the site and in the page.
- Record the pre-existing plain-macro exposure of the identity rule on a public Issue.

**Verification:** Both `cases_r3` splice and paste identity cases are REFUSED at the fixed head with the SDK. Otherwise the site comment, the page and the gate print state the bound, and the Issue link is published.

### F3 - MINOR - Conformance, Docs

**Artifact:** `sw/builder/test_builder.py:2700-2742` (`arm_selections` grades every combination) and `:4015` with `:8405` (`SELECTION_PIN`, "one of the firmwares the product may build").
Docs: `docs/integration/BAREMETAL_FIRMWARE.md:1236` (cost row) and the gate print's COSTS paragraph (`sw/builder/test_builder.py:13577`).

**Title:** Grading every combination of arms creates an undisclosed new cost for correlated conditionals, and the refusal names a firmware the product cannot build.

**Authority and evidence:**
- #408 acceptance 2 and 5: costs restated, and the page and gate print match what survives.
- Measured with the pinned SDK (`receipts/probes/r4-*`):
  - A debug helper defined under `#ifdef MILAN_DEBUG_TOD` and called under a second `#ifdef MILAN_DEBUG_TOD` in a UART handler is ACCEPTED at base and REFUSED at head.
  - A debug-only counter declared and incremented the same way is ACCEPTED at base and REFUSED at head.
  - Each refusal names the selection "no arm taken; ... arm 1 of 1 taken" as "one of the firmwares the product may build", which no build selects, and fails on the census compile.
  - Both are ACCEPTED at head with no compiler.

The page discloses only "more than 16 selections" and "code inside a disabled `#if 0`".

**Impact:** A common debug pattern is newly refused, with a message that misdescribes the product, and the cost list does not say so.

**Required outcome:** Disclose the cost in the cost table and the gate print with a remedy, and word the selection sentence so it does not claim the product may build an inconsistent combination. Alternatively, grade groups on the same controlling macro consistently.

**Verification:** Read the page and gate print. Or, if the grading changes, `cases_r4` is ACCEPTED with the SDK and a new accepted case pins it.

### F4 - MINOR - Robustness, Docs

**Artifact:** `sw/builder/test_builder.py:2431-2436` (`blanked()` scans a character or string literal across newlines), relied on by `conditional_groups()`/`arm_selections()`.
Docs: `docs/integration/BAREMETAL_FIRMWARE.md:270-277`.

**Title:** A pre-existing blanking desync hides a conditional from the per-selection grading.

**Authority and evidence:**
- GCC ends an unterminated character literal at the end of its line with a warning.
- The census compile (`:4130-4133`) has no `-Werror`.
- `blanked()` instead scans to the next quote, across lines.
- `#define MILAN_Q '` and `#define MILAN_R '` bracketing an `#ifdef CSR_UART_BASE` literal-address store in a UART handler are ACCEPTED at base and at head, with and without the compiler (`receipts/probes/r2-*`).

This is not a regression: base's text sets blanked the same region.

**Impact:** The new claims "Every preprocessor conditional is graded one arm selection at a time" and "the product builds one of the firmwares graded" hold only for text that `blanked()` lexes the way GCC does, and the page states them without that bound.

**Required outcome:** Refuse an unterminated literal outside comments (C ends it at the newline), or bound the claim at the site and in the page and record a public Issue. Moving it to an Issue does not by itself clear the lens.

**Verification:** The `cases_r2` unterminated-quote case is REFUSED at the fixed head, or the bound is published with the Issue link.

## Rule-by-rule judgement against the retirement acceptance

"Base" means gate 1b at 759da623 on the same text, and "SDK" means the pinned RV32 SDK mapped onto the gate's selector.

The first two columns come from the page:
- **Page verdict:** retired, narrowed or kept.
- **Replacing instrument:** as named in the cost table.

Three columns are measured here:
- **Accepted case at base:** measured in `receipts/accepted/base-{sdk,absent}.*`. Every one is REFUSED on the retired rule's own sentence in both environments, and ACCEPTED at head in both (`receipts/accepted/head-*`).
- **Hostile controls, replacement disconnected:** measured in `receipts/disconnect/TABLE.txt`.
- **Reviewer judgement:** whether the retirement is accepted at this head.

| Rule (page row at 7fd04d45) | Page verdict | Replacing instrument | Accepted case at base | Hostile controls, replacement disconnected | Reviewer judgement |
|---|---|---|---|---|---|
| conditional reach (565) | retired | per-selection grading | both cases REFUSED on "a conditional group reaching" | selection off, SDK: all 14 selection-pinned controls fail their pin, 4 pass outright. Absent: all 5 that run there fail, 1 passes. The 16-selection bound control was not in this set | NOT ACCEPTED at this head: F1, F3, F4 |
| conditional carrying `#define`/`#include` (565) | narrowed | per-selection grading | REFUSED on "a conditional group carrying #define" | the verifier-group `#define` is RED here (was GREEN at base); `ADP_CTRL` moved by a plain-`#` product arm is refused in its selection | narrowing sound for plain `#`; F1 applies |
| token-joining splice (564) | retired | `-E` in six bodies + resolved census | REFUSED on the splice sentence | `-E` off: the 10 boot-body controls refused only off their pin (resolver). `-E`, census and resolver off: all splice and paste controls pass | NOT ACCEPTED at this head: F2 |
| `##` (585) | retired | same two | REFUSED on "firmware must not paste tokens" | as above | NOT ACCEPTED at this head: F2 |
| `%:`/`??` (585) | kept | none | n/a | digraph-pasted call name refused on its own sentence in both gate runs | honest reason; accepted |
| read-only `#define` accessor (584) | narrowed | fail-closed read rules | REFUSED on "hides milan_read() inside a macro body" | macro-hidden store, read-macro enable value and read-macro identity forgery all refused on their pins in both gate runs | accepted |
| directive set (566) | kept | none | n/a | existing controls | honest reason; accepted. Its reader shares F1's anchor (pre-existing) |
| directory listing pin (568) | retired | `-H` by the path opened and the file reached | README + notes.txt REFUSED on "the firmware's directory is pinned to" | `-H` off: `command.h`, `init.h` and the LINK controls all pass | accepted. The firmware reaches the build only through `make -f` of its Makefile, whose pattern rule names only `milan_baremetal.c`, so the quoted-include lookup is the directory's one channel (`sw/litex/milan_soc.py:3863-3865`, firmware `Makefile`) |
| `#include` name set (567) | kept | none | n/a | unchanged | accepted; the `-H` caveat is at the site (`:3415-3423`) and in the page |
| ordered cast set, store set, reorder (563, 583) | retired | resolved store census | fifth cast, fifth store and reorder each REFUSED on the cast- or store-set sentence | census and resolver off: every cast, store, asm, arm-store, redefinition and flipped-verifier control passes | NOT ACCEPTED at this head: F1 (the sets read every arm; the replacement sees only arms F1's reader finds) |
| inline-`asm` set (563) | retired | same, reading the template | fence REFUSED on "the firmware's inline asm is pinned" | as above; the `lui` template is refused by resolved address when connected | NOT ACCEPTED at this head: F1 (`lui` store in a form-feed arm) |

**#409 acceptance 4, the author's open point (the two helper-body mutants, refused first by a text rule still in force):**
- Judged SATISFIED in substance.
- The whole-gate entries are pinned on the surviving helper return-provenance rule. It answers first on every machine: P in every disconnect run, with or without a compiler.
- The resolver's own refusal of both mutants is a hard assertion on its own sentence (`RESOLVER_STORE_PIN`) on every live run, at `sw/builder/test_builder.py:11133-11157`.
- Disconnecting the resolver function fails the gate at that control: "the resolver accepted a store inside the exempted address helper" (`receipts/accepted/resolver-off-sdk.log`).
- The census's blindness is asserted beside it.
- Moving the table entry itself onto the resolver's sentence would require reordering the text rules or weakening one. The acceptance's intent (off the retired cast set, onto the value-resolving census) is met.

**Compiler absence and hosted requirement:**
- Absent mode is a registered `NOT RUN` naming the three instruments, with the verdict `TEXT RULES ONLY, AND WEAKER`.
- It counts 35 census and resolver entries plus 26 retired-rule entries as SKIPPED, never rejected (`receipts/head-gate1b-absent.log`).
- `--absent --require-rv32` fails: "--require-rv32: the hosted firmware instruments must run" (`receipts/12-absent-require.log`).
- Both hosted builder consumers still pass `--require-rv32`: `.github/workflows/docs.yml:190` and `.github/workflows/elaborate.yml:260`, unchanged by this diff.
- At the exact head, the `docs-check` job executed "Install and verify the pinned RV32 SDK", "Compiler-absent firmware controls" and "End-station builder gates", all successful.
- The `elaborate` job executed "Elaboration gates" after installing the SDK.
- "Physical gPTP (nightly and manual)" is a skipped context, not an executed job.

## Issue acceptance, as measured

**#408:**
- (1) met.
- (2) Rows are retired, narrowed or kept with reasons, and the three named accepted cases are GREEN here and RED at base. But the replacements for 564, 585 (`##`) and 565 do not carry what those rules refused: F1, F2. Costs are incomplete: F3.
- (3) met.
- (4) The count of 228 is reproduced, and every entry is re-pinned on its replacement (disconnect matrix). "No reduction" fails for unlisted hostile spellings: F1, F2.
- (5) `docs_check.py`, `check_baremetal_only.py --check`, `check_em_dash.py --base 759da623` and `git diff --check` pass (`receipts/20-static.log`). The claims in F1 to F4 are not accurate.

**#409:**
- (1) met: the struct-overlay and paged-base stores are refused on the resolver's message, and the helper-planted store is refused by the blindness control.
- (2) met.
- (3) met.
- (4) Entries are re-pinned and the helper point is judged satisfied, but "no reduction" fails through F1.
- (5) See F1.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3) | #408/#409 bodies and all comments; PR #535 body; `git diff 759da623..a13b6e2e`; gate 1b runs at head and base in both environments (`receipts/{head,base}-gate1b-*`); accepted cross-check (`receipts/accepted/`); probes r1-r4 (`receipts/probes/`) | R272-1 | a13b6e2e461695cdb8d978444ae499a5a6745429 |
| RTL | CLEAN | see the PASS line below | R272-1 | a13b6e2e461695cdb8d978444ae499a5a6745429 |
| Robustness | UNCLEAN (F1, F2, F4) | `sw/builder/test_builder.py` directive readers (`:2543`, `:2609`, `:3544`), `blanked()` (`:2408-2441`), `spliced()` (`:3554-3578`), `arm_selections()` (`:2700-2742`), the `-E` comparison (`:4208`, `:4301`); GCC directive-spelling receipt (`receipts/cpp/`); probes r1-r3 | R272-1 | a13b6e2e461695cdb8d978444ae499a5a6745429 |
| Tests | UNCLEAN (F1, F2) | the mutation table and accepted loop at head; disconnect matrix over all 33 retired-rule, selection and helper controls in 8 configurations (`receipts/disconnect/TABLE.txt`); the tuple reason-pin negative control; resolver-off run | R272-1 | a13b6e2e461695cdb8d978444ae499a5a6745429 |
| Docs | UNCLEAN (F1, F2, F3, F4) | `docs/integration/BAREMETAL_FIRMWARE.md` diff (sections at `:264-330`, `:1210-1260`, `:1270-1445`); `docs/testing/CI_WORKFLOWS.md:1129-1130`; gate print at `sw/builder/test_builder.py:13405-13735`; page counts reproduced (228/167 head, 217/182 base, 27+4 and 17+4) | R272-1 | a13b6e2e461695cdb8d978444ae499a5a6745429 |

[R272] PASS RTL - `git diff --stat 759da623..a13b6e2e` (three files, no HDL, no RTL source list), `sw/builder/test_builder.py:2375-2378` (the `milan_csr.sv`/`milan_datapath.sv` readers, outside the diff), and `receipts/head-gate1b-{sdk,absent}.log` - checked that no RTL, CSR decode or datapath contract the gate reads changed, and that 46/46 RTL mutation variants still elaborate as the real `milan_datapath`/`milan_csr` top under Verilator 5.050 in both environments at this head (46/46 at base too).

## Prior public findings on this PR

None to resolve or retain.
This was checked after this report's verdict and ledger were written.
At the round's start (2026-09-23T19:43:36Z) PR #535 carried only the review-start comment: no review, no inline comment and no finding.
The only later item is a second review round's start notice, which holds no findings.
No other reviewer's report was read.

## Reproduction

Every command runs in the foreground from any directory. `<packet>` is this directory, `<clone>` a checkout of the exact head with its three pinned submodules, `<base>` the same checkout at 759da623 and `<sdk>` the pinned SDK (`scripts/ci_rv32_sdk.py --verify-only` passes, `receipts/00-sdk-verify.log`). Verilator 5.050 is taken from `R272_VERILATOR_BIN`.

| Evidence | Command | Receipts |
|---|---|---|
| gate 1b, both environments | `scripts/run_gate1b.sh <clone> <sdk> <verilator-bin> <packet>/receipts head` (and `<base>` ... `base`) | `receipts/{head,base}-gate1b-{sdk,absent}.*` |
| absent with `--require-rv32` must fail | `sw/builder/test_firmware_compiler.py --absent --require-rv32 --audit ...` | `receipts/12-absent-require.*` |
| preprocessor spellings | `scripts/cpp_directive_check.sh <sdk> <packet>/receipts/cpp` | `receipts/cpp/` |
| probes r1 to r4, head and base | `scripts/run_probe_pair.sh <packet> <clone> <base> <mode> scripts/cases_rN.py rN`, where `<mode>` is `<sdk>` or `absent` | `receipts/probes/` |
| disconnect matrix | `scripts/run_disconnects.sh <packet> <clone> <sdk>`, then `scripts/tabulate_disconnect.py receipts/disconnect` | `receipts/disconnect/` |
| accepted cases at base, resolver off | `scripts/run_accepted_crosscheck.sh <packet> <clone> <base> <sdk>` | `receipts/accepted/` |
| static checks | `docs_check.py`, `check_em_dash.py --base 759da623`, `check_baremetal_only.py --check`, `git diff --check` | `receipts/20-static.log` |
| clone integrity after probes | `git ls-files -s`, `git write-tree`, `git status --ignored`, submodule status | `receipts/90-clone-integrity.txt` |

## Real limits

- Probes run the gate's own code in memory (`scripts/probe_gate1b.py`): one hook before the accepted loop or the mutation loop, and count-checked patches for disconnects. They never edit the clone.
- The base comparison uses a scratch copy of the clone checked out at 759da623. Only the three changed files differ.
- Only gate 1b was run, through `sw/builder/test_firmware_compiler.py` and the probe driver. The whole builder, parent, PP, gPTP and Yosys banks were not run, by instruction.
- The public evidence tree at 4644211f holds only the author's receipts. No separate manager bank receipt was found there or in the issue and PR comments. The manager's bank result is taken as stated in the round brief, not verified here.
- Hosted evidence was inspected, not reproduced; no `act` runs.
- LiteX's own `make` invocation for software packages was not re-read. The directory-pin judgement rests on the firmware `Makefile` pattern rule and `sw/litex/milan_soc.py:3863-3865`.
- `\f#undef` and `_Pragma("push_macro")`/`_Pragma("pop_macro")` were confirmed only at the preprocessor (`receipts/cpp/ff-undef.c`, `pragma-pop.c`): each changes which definition of a name the compiler uses, past a text reader. `\f#pragma` and `\f#include` were reasoned from the same anchor. None was graded through the whole gate, and all are pre-existing.
- No hardware. Physical calibration is NOT RUN, and skipped field contexts are not hardware proof.
- The candidate merge result on the live dev tip (26d855a9) was not built.
- Receipts have the reviewer host's home prefix replaced by `$HOME`: 577 substitutions, listed in `receipts/95-redaction.txt`, and nothing else changed.

## Pending manager duties

- Publish this report and the manifest-listed receipts.
- Route F1 to F4 to the author. The pre-existing exposures (identity via a plain macro, F4's blanking desync, the directive-closure `\f` gap, `_Pragma` macro stacking) need public Issues where the fix is not made in this lane. An Issue does not clear a lens.
- After fixes, re-review at the new head every lens whose scope changes, including RTL if any RTL-facing reader moves.
- Own the hosted and act acceptance, the external review, the candidate merge validation against live dev and the post-merge containment.

R272-1 FINISHED
