[R273] NEGATIVE - exact head 8e12d31fefa7df0abb4d9474d0412ce123ac9644

Round R273-4 is an external cleared-context review of PR #535 (#408, #409) at
head `8e12d31fefa7df0abb4d9474d0412ce123ac9644`, tree
`73a2836b0fffdedb294675d75c61167eb446ceb8`. Source base is dev `759da623`.
This head is correction round 2, three commits on `ef903457`: `8fd74a99`,
`479a2175` and `8e12d31f`. I applied all five lenses.

One finding is open, a BLOCKER. Receipts are in this packet. Paths in them
read `<clone>`, `<sdk>`, `<packet>`, `<pinned-tool-bin>` and
`<shared-selector>`.

## Verdict in one paragraph

This round fixes what it was assigned, and I reproduced each fix:
- My unchanged round-two split-digraph cases (H1-H6) are refused in both
  modes.
- My round-three byte-order-mark cases (B1, B2, B4, B7) are refused.
- The paste-ban bound (`__CONCAT`, #544) is stated at the site and on the
  page.
- Gate 1b reproduces the author's figures in both modes.
- An independent GCC oracle agrees with the record and with the gate's
  readers on all 4985 corpus spellings.
- The disconnects I re-ran fail their controls.

The class the manager asked to be fixed is still open, through a member
neither corpus holds. Phase 3 in `_c_phases()` has no header-name state. GCC
lexes the operand of `__has_include` in an `#if` as one header-name token, so
in `#if !__has_include(<r273/*none>)` the `/*` opens no comment. The gate reads
it as a comment that runs to the next `*/`. The next line can end in `// */`,
which GCC reads as a line comment. That line is then compiled by the product
and blanked out of every text the gate reads.

This includes the arm selections it compiles. Per-selection grading builds
each selection from the gate's own reading, and the original file is never
compiled. So the compiled instruments cannot backstop the lexer here, as they
did on dev.

Results, dev against this head:

| Case | dev, pinned SDK | head, pinned SDK | dev, no compiler | head, no compiler |
|---|---|---|---|---|
| Identity sample forged in `milan_init()` | refused | **accepted** | refused | **accepted** |
| AEM verdict overwritten after the verifier | refused | **accepted** | refused | **accepted** |
| ADP enable in a UART command handler | refused | **accepted** | accepted | accepted |
| CSR-window store in a UART command handler | refused | **accepted** | accepted | accepted |

Acceptance 4 ("No reduction") governs, so this is F1.

## Finding raised by this round

### R273-4-F1 - BLOCKER - Conformance, Robustness, Tests, Docs

**Artifacts.** In `sw/builder/test_builder.py`:
- `:2342-2347`: `_C_PHASE12_RE`, `_C_LEX_STOP_RE`, `_C_PUNCTUATOR_RE`.
- `:2451-2525`, `_c_phases()`. The comment branch is at `:2473-2479`. There is
  no header-name state: `<` after `__has_include(` or `__has_include_next(` is
  not read as the start of one token.
- `:3067-3074`, `conditional_groups()`. The directive line runs to the next
  real line end in the view, so it swallows the hidden line.
- `:3191-3267`, `arm_selections()`. `blank_spans(source, group["lines"] + ...)`
  at `:3254` blanks that line from every compiled selection.
- `:4984-5256`: both lexer corpora, where no header-name spelling appears.

In `docs/integration/BAREMETAL_FIRMWARE.md`:
- `:293-309` describes phase 3 without header names.
- `:326-328` says "the readers are exact because they run GCC's phases in
  GCC's order".

**Authority.**
- #408/#409 acceptance 4 ("No reduction").
- The manager's round-2 direction
  (https://github.com/kebag-logic/milan-fpga/issues/408#issuecomment-5807562819):
  "Fix the class, not the spelling ... Show that no spelling in the corpus or
  the reviewers' probes can hide a directive. If a reader cannot be made
  phase-exact, restore the retired splice ban."
- C11 6.4.7 and 6.10.2 (header names), as GCC 14 applies them to
  `__has_include` at `-std=gnu99`.

**Evidence, lexer.** `receipts/hi-spellings/t1.c`-`t3.c`, compiled on the
pinned `riscv32-linux-gcc` 14.3.0 at `-std=gnu99 -E`:
- `int a;\n#if !__has_include(<x/*y>)\nint b; // */\n#endif\nint z;\n` keeps
  `a b z`.
- The gate's `_c_phases()` view is
  `int a;\n#if !__has_include(<x                       \n#endif\nint z;\n`.
  `int b;` is gone from it, and in the `#else` spelling the `#else` is gone too.
- `receipts/lexer-oracle.jsonl` (`probes/lexer_oracle.py`) loads the gate's
  phase code and readers unmodified (`probes/lexer_extract_head.py`):
  - 0 disagreements over the 78 fixed and 4907 generated spellings, with GCC
    run one file per invocation;
  - 2 of 4 extra spellings lose a line GCC keeps, both angled header names
    holding `/*`;
  - the quoted form and the angled `//` form are controls, and both agree.

**Evidence, whole gate.** The cases are `cases/hi.json`
(`probes/make_hi_cases.py`, generated from the tracked firmware). They are
graded through gate 1b's own `assert_boot_contract()` by my unchanged
round-three in-memory grader (`probes/probe.py`) at dev `759da623` and at this
head, in both modes. See `receipts/probes/hi-{dev,head}-{sdk,absent}.json` and
`hi-table.md`.

- HI1, identity sample forged in `milan_init()`:
  - dev: refused with the SDK and absent;
  - head: **accepted with the SDK and absent**.
- HI2, ADP enable in a UART command handler:
  - dev: refused with the SDK (compiled census), accepted absent;
  - head: **accepted with the SDK**, accepted absent.
- HI3, literal-address cast store into the CSR window, UART handler:
  - dev: refused with the SDK (compiled census), accepted absent;
  - head: **accepted with the SDK**, accepted absent.
- HI4, AEM verdict overwritten after the verifier:
  - dev: refused with the SDK and absent;
  - head: **accepted with the SDK and absent**.
- Controls, all as expected at head in both modes:
  - HI1q (a quoted header name) is refused.
  - HI1p (plain `#if 1`) is refused.
  - HI2p is refused.
  - HI3p is refused with the SDK. Absent it is accepted, which is the
    registered NOT RUN class.
  - HI5 (a benign `printf` behind the same header name) is accepted.

**Evidence, the product compiles it.** `receipts/probes/hi-head-direct-sdk.*`
(`probes/probe_direct.py`) hands the unselected file to the pinned compiler
over the census headers.

The `-E` output of each case holds the hidden line:
- HI1: `id = 0x4d494c4eu;`
- HI2: `milan_write(0x600u, milan_read(0x600u) | 1u);` in the handler
- HI3: `*(volatile unsigned int *)0x90000600u = 1u;`
- HI4: `aem_loaded = 1;`

`assert_compiled_census_is_clean()` over that unselected file refuses HI3.

**Impact.**
- With the pinned compiler, which is how both hosted builder consumers grade a
  merge, gate 1b accepts all four:
  - a forged identity sample;
  - an overwritten AEM verdict;
  - an entity enable outside the choke point;
  - a store into the Milan CSR window.
- dev refuses all four on that runner, and refuses the first two on every
  runner.
- This is the third member of the R272 F1 class: a directive reader that
  disagrees with GCC's phase 3.
- The page claims the readers are exact, and the run shows they are not.

**Required outcome.**
- No text GCC compiles may be absent from every text gate 1b grades. The
  candidate fixes below are examples, not a prescription:
  - read header names as GCC does, as one token after `#include` and inside
    `__has_include`/`__has_include_next`;
  - refuse `__has_include` and `__has_include_next` in the firmware; the
    firmware uses neither today;
  - refuse `/*` or `//` inside any `<...>` operand;
  - add a backstop that compiles or preprocesses the UNSELECTED file and
    compares it with the selection the product takes.
- If a reader cannot be made exact, restore a rule, as the manager's direction
  says.
- The corpora gain header-name spellings recorded from GCC.
- A whole-gate control (HI1 or equivalent) is refused on its own sentence in
  both modes and fails with the fix removed.
- The page states what phase 3 treats as a header name, or what is refused.

**Verification.**
- `probes/lexer_oracle.py <clone> <gcc> <out>` reports `extra_lost: 0`.
- `probes/run_probes.sh` over `cases/hi.json` shows HI1-HI4 refused at the
  fixed head in both modes, and HI5 accepted if the lexing route is taken.
- Gate 1b stays green in both modes.

## Prior public review findings on this PR, resolved or retained at this head

I read these after writing `receipts/verdict-before-reading-prior-findings.md`.

- **R272-2 F1 (BLOCKER, split `%:` digraph): RESOLVED.** Evidence:
  - My round-two cases (`cases/r2-cases.json`, unchanged) are refused at this
    head in both modes. That covers H1-H3 (product-only store behind
    `%\`-newline-`:ifdef`), H4 (`0 &&` in the verdict test), H5 and H6.
  - The generated corpus carries the spelling, and my oracle agrees on it.
  - Disconnect NOBAN (`receipts/disconnect/NOBAN-r2-*.json`): without the
    whole-file ban, C4 and H1-H4 pass absent and stay refused with the SDK.
    That matches the page's disconnect paragraph (`:1468-1490`).
  - Disconnect UNREAD: `<%:` (U1) passes absent without the unread-pair check
    and is refused connected (`receipts/disconnect/*unread*`).
  - The class R272-2 named is not closed. See F1 above.
- **R273-3 F1 (MINOR, BOM at offset 0): RESOLVED.**
  - B1, B2, B4 and B7 are refused at this head in both modes, where
    `ef903457` accepted them (`receipts/probes/prev-round-compare.txt`).
  - B6, a BOM alone, is accepted.
  - Disconnect BOMKEPT: the gate stops on its own BOM corpus entry in both
    modes (`receipts/disconnect/BOMKEPT-bom-*.log`).
- **R273-3 F2 (MINOR, `__CONCAT` claim): RESOLVED.**
  - The page (`:358-366` and rows `:1294-1295`), the site
    (`test_builder.py:4944-4953`) and the gate print (`:15104`) now say the
    paste ban reads this file's own `#define`s, with `__CONCAT` outside it,
    the #544 bound.
  - X4 is still accepted in both modes, as now stated.
- **R272-1 F1-F4 and R273-1 F1: remain RESOLVED.** Evidence:
  - All 74 published cases give the same verdicts as at `ef903457`, in both
    modes.
  - With the SDK, the only cases dev refused and this head accepts are exactly
    the 14 deliberate legitimate edits (ACC1-ACC11, E1, E4, E6;
    `receipts/probes/published-*.json`).
  - Absent, the extra cases are the registered NOT RUN class.
- **R273-1 S3 (SUGGESTION): RETAINED as a SUGGESTION**, under #544, unchanged.

## Lens results with evidence

- `[R273] PASS RTL - git diff --stat 759da623..8e12d31f (docs/integration/BAREMETAL_FIRMWARE.md, docs/testing/CI_WORKFLOWS.md, sw/builder/test_builder.py; no hdl/, no RTL source list, no gitlink change, receipts/clone-state.txt) and receipts/gate1b-{sdk,absent}.log - checked that no RTL, CSR decode or datapath contract changed and that 46/46 RTL mutation variants elaborate as the real milan_datapath/milan_csr top under Verilator 5.050 (receipts/verilator-identity.txt) in both modes.`
- **Conformance: UNCLEAN (F1).** Also checked, with no further finding:
  - Gate 1b with the pinned SDK: 264/264 mutations; 30/30 firmware and 4/4
    Makefile edits accepted; 4985/4985 spellings re-measured; 0 NOT RUN.
  - Absent: 206/206; 30/30 and 4/4; one registered NOT RUN naming the arm.
  - `--absent --require-rv32` exits 1 (`receipts/gate1b-*.log`).
  - #408 acceptance 1-3 and 5 and #409 acceptance 1-5 hold as in round three.
  - Counts: 264 and 206, both at least 163.
- **Robustness: UNCLEAN (F1).** Also checked, with no further finding:
  - Maximal munch for `%:`, `%:%:`, `<%:`, `%%:`, `#%:` and `%:#`
    (`test_builder.py:2504-2518`, all generated-corpus entries).
  - Splices after blanks, FF, VT, NUL, CRLF and lone CR.
  - The quoted and `//` header-name forms (oracle controls).
  - HI5, the benign case.
- **Tests: UNCLEAN (F1: no header-name spelling in either corpus and no
  control for it).** Also checked:
  - The generated corpus is rebuilt independently and agrees 3 ways (recorded,
    gate, GCC one file per invocation).
  - The corpus negative control is at `:5381-5392`.
  - Three disconnects fail their controls: BOMKEPT, UNREAD and NOBAN.
  - `test_firmware_compiler.py --selftest` exits 0.
- **Docs: UNCLEAN (F1: `:293-309`, `:326-328`).** Also checked, each exiting 0
  (`receipts/static-checks.log`):
  - `docs_check.py`;
  - `check_baremetal_only.py --check`;
  - `check_em_dash.py --base 759da623`;
  - `check_doc_style.py`;
  - `git diff --check`.

  The page's disconnect paragraph (`:1468-1490`) and count paragraph match
  what I measured.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #408/#409 acceptance 1-5; manager round-2 direction; `receipts/gate1b-*.log`, `receipts/probes/{hi,r2,bom,extra,published}-*.json`, `hi-head-direct-sdk.json` | R273-4 | 8e12d31fefa7df0abb4d9474d0412ce123ac9644 |
| RTL | CLEAN | `git diff --stat 759da623..8e12d31f`; `receipts/gate1b-{sdk,absent}.log` (46/46 RTL variants); `receipts/verilator-identity.txt` | R273-4 | 8e12d31fefa7df0abb4d9474d0412ce123ac9644 |
| Robustness | UNCLEAN (F1) | `test_builder.py:2312-2525, 2960-3300, 4808-4980`; `receipts/lexer-oracle.jsonl`; `receipts/hi-spellings/`; `receipts/probes/hi-*.json` | R273-4 | 8e12d31fefa7df0abb4d9474d0412ce123ac9644 |
| Tests | UNCLEAN (F1) | `test_builder.py:2528-2710, 4982-5408`; `receipts/lexer-oracle.jsonl`; `receipts/disconnect/*` | R273-4 | 8e12d31fefa7df0abb4d9474d0412ce123ac9644 |
| Docs | UNCLEAN (F1) | `docs/integration/BAREMETAL_FIRMWARE.md:285-370, 1290-1300, 1468-1490`; `receipts/static-checks.log` | R273-4 | 8e12d31fefa7df0abb4d9474d0412ce123ac9644 |

## Executable evidence (this packet)

- `receipts/sdk-verify.log`: the pinned SDK was installed from the pinned
  archive (sha256 `d42680e9...`) into a disposable tree and verified.
  `riscv32-linux-gcc` is 14.3.0.
- `receipts/verilator-identity.txt`: Verilator 5.050 and the wrapper sha256
  `905795b9...`.
- `receipts/gate1b-{sdk,absent,absent-require-rv32}.log`: gate 1b through
  `test_firmware_compiler.py`.
- `receipts/lexer-oracle.jsonl`: the independent corpus oracle and the extra
  spellings.
- `receipts/probes/`: the probe runs and their tables:
  - `hi-*` (F1) and `hi-head-direct-sdk.*`;
  - `r2-*`, my round-two cases, unchanged;
  - `bom-*`, `extra-*` and `published-*`, my round-three cases, unchanged;
  - `prev-round-compare.txt`, this head against my round-three receipts at
    `ef903457`.
- `receipts/disconnect/`: BOMKEPT, UNREAD, NOBAN and NONE, with the patches in
  `disconnect/*.json`. Each is count-checked and applied in memory.
- `receipts/static-checks.log`, `receipts/hosted-check-runs.tsv` and
  `receipts/clone-state.txt`.
- `receipts/verdict-before-reading-prior-findings.md`.

## Real limits

- Gate 1b ran in full in both modes. I did not run:
  - the whole builder;
  - the parent, PP and gPTP banks;
  - Yosys, act or hosted re-runs;
  - hardware.
- The author's disconnect receipts for this round are not in the public
  evidence tree (`470f959a` ends at round one). I derived three disconnects of
  my own, not the author's full 53-control matrix.
- The oracle covers the two corpora and four extra spellings, not every
  spelling.
- Physical calibration was NOT RUN, and field skips are not hardware proof.
- I only read the exact-head hosted check runs: 21 completed with success, and
  "Physical gPTP (nightly and manual)" was skipped. The manager owns hosted and
  act acceptance.

## Pending manager duties

- Route F1 to a correction round, and re-review at the new head.
- Build and validate the current-dev candidate merge (source base `759da623`,
  live dev `3d2f3e31`) at the merge turn.
- Decide whether R273-1 S3 stays under #544.

R273-4 FINISHED
