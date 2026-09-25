[A10] Residue of #162, filed on the maintainer decision of 2026-09-07 to close that ledger

## Objective and evidence

Let gate 1b ask the preprocessor instead of reading C text before it: run the census compiler with `-E` under the planned flags and apply the boot-path rules to the preprocessed translation unit, so the rules that exist only because the gate reads raw text are retired, each with an accepted case measured GREEN; and ask the preprocessor which files it opened (`-H`, or `-M`/`-MM`) so the include listing pins become one resolved-path measurement.

- #162's body lists the rows (the `#ifdef` ban, the multi-line `#define` ban, the eleven-name `#include` set and the firmware-directory listing) and records the review guidance: the `#define` and `#ifdef` bans are parsing artefacts that `gcc -E` retires outright, which also removes the blank-comments, preserve-offsets machinery; `gcc -H` or `-M` reports the files actually opened, turning the directory-listing pin and the `-I` pin into one positive measurement; `-H` proves resolution in the tree it is handed, so the caveat must be written at the site. The [A0] reopening comment of 2026-09-02 keeps both items as the ledger, and PR #322 (merged 2026-09-02, ec7f6862) names them in its Known limitations.
- `docs/integration/BAREMETAL_FIRMWARE.md` at dev 7fd04d45 states the surviving text rules and their cost: line 564 (a backslash-newline that joins two tokens), 565 (no `#ifdef`/`#if` reaching `milan_init()`, `configure_fabric()`, `entity_advertise()` or the three CSR accessors, none carrying a `#define`/`#undef`/`#include`), 566 (no `#pragma`, `#line`, `#error`, `#undef`, `#include_next`), 567 (the `#include` set is exactly the eleven headers), 568 (no new file in `sw/firmware/milan_baremetal/`), 584 (a read-only `#define` accessor wrapping `milan_read()`), 585 (`##`, `%:` or `??` anywhere in the file). Lines 594 to 598 show the pattern to follow: three rows left the table with #153, each with an accepted case measured GREEN.
- `sw/builder/test_builder.py`: `_assert_no_token_joining_splice` (line 1721), the `##`/`%:`/`??` assertion (1860), `firmware_listing` (1981), `blanked` (2006), `cpp_arms` (2142) and `assert_preprocessor_visible` (2178), `assert_include_resolution_is_pinned` (2991, called at 5420), `line_spliced` (3019) and `spliced` (3025), `assert_directive_set_is_closed` (3045), all inside `test_baremetal_profile_contract()` (1903). The gate print at lines 8778 to 8802 lists the same costs, a twelfth `#include` even of `<string.h>` and any new file in the firmware directory including a README among them.

## Authority and scope

- #162 (body rows and the 2026-09-02 comment); PR #322 (the restoration and the mutation table, 163 entries); PR #241 (the #153 retirement pattern); `docs/integration/BAREMETAL_FIRMWARE.md` lines 543 to 598.
- Context: `sw/builder/test_builder.py` `test_baremetal_profile_contract()`, `census_compiler()` (3327) and `census_take()` (3457) for the compiler and flags the `-E` run must share; `sw/firmware/milan_baremetal/`.
- In scope: the `-E` instrument and the retirement or narrowing of the rules at doc lines 564, 565, 566, 584 and 585 with the offset-preserving machinery they need; the include-resolution instrument replacing lines 567 and 568; the caveat that resolution is proven against the tree the census hands the compiler and that the pinned headers' contents stay trusted rather than read; every mutation those rules pinned re-pinned on the new instrument's own message; the doc table and the gate print updated.
- Out of scope: the `CFLAGS` token set and the Makefile `include` set (the #162 body keeps them: not parsing questions); the census's value resolution and the Makefile walker (the two sibling residue issues); the boot-path identifier anchors, which stay a stated locator cost (doc line 581).

## Acceptance and validation

1. Gate 1b compiles the firmware with `-E` under the planned flags with the same compiler the census adopts, and the boot-path text rules read that output; when the RV32 compiler is absent the instrument stands down with the census and the closing line names the arm.
2. Each rule at doc lines 564, 565, 566, 584 and 585 is retired, narrowed, or kept with its cost restated and a reason it cannot be measured; every retirement leaves with an accepted case measured GREEN and named in the doc table (at least: a `#ifdef` around a debug `printf` inside `milan_init()`, a read-only `#define` accessor over `milan_read()`, and a token-joining backslash-newline inside a macro body), and the accepted-case loop reports each.
3. The include instrument lists the files the preprocessor resolved; the pinned set is compared by resolved path; a shadowing file placed in `sw/firmware/milan_baremetal/` under a pinned header's name is refused by the path it resolved to; a README added to that directory is measured GREEN; the `-H` caveat is stated at the site and at the doc rows that replace lines 567 and 568.
4. No reduction: every mutation-table entry the retired rules pinned is re-pinned on the replacing instrument's message, the count is not below 163, and `python3 sw/builder/test_builder.py` exits 0 with the census live on a host carrying an RV32 gcc.
5. `docs/integration/BAREMETAL_FIRMWARE.md` and the gate print (lines 8774 to 8823) match what survives; `python3 -B scripts/docs_check.py` and `python3 scripts/check_baremetal_only.py --check` pass.

## Lane and review

Executor: unassigned. Independent reviewer: unassigned. Assigned by the manager when the lane opens.

Dependencies: none open. Lane conflicts: any branch editing `sw/builder/test_builder.py` gate 1b or `docs/integration/BAREMETAL_FIRMWARE.md`, and the two sibling #162 residue issues, which touch the same test and page; serialise the three.

