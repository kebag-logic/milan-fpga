[R272] NEGATIVE - exact head ef9034578f97ebc2951801d867b7c57f8196423d

Internal cleared-context independent review, round R272-2, of PR #535
(issues #408 and #409), correction round 1 (A219: three commits `75066c16`,
`d8abee3e`, `ef903457` on the round-1 head `a13b6e2e`, base dev `759da623`).
Exact head `ef9034578f97ebc2951801d867b7c57f8196423d`, tree
`1604179afc0b3af5e4590ecd5087e265c015f3dd`. Isolated clone
`$REVIEWS/r272-2-408` (verified clean vs head, index and worktree,
after all probes; submodule gitlinks intact, `external` deliberately
uninitialised).

## Verdict

NEGATIVE. One BLOCKER (F1). It is the same class the correction round was
assigned to close (R272-1 F1): a preprocessing-directive spelling the pinned
GCC honours while every gate 1b directive reader misses it, so a product-only
CSR store the retired cast/asm sets refused on dev is accepted here. The round
fixed the four spellings it was given (form feed, vertical tab, NUL, lone CR)
but the class is not closed: a `%:` digraph split by a backslash-newline
(`%\`<newline>`:ifdef`) is another member, and it defeats both the directive
readers and the KEPT `%:` ban. Acceptance 4 (no reduction) governs, and this is
a proven reduction versus dev. F1 leaves Conformance, Robustness, Tests and
Docs UNCLEAN.

The other findings the round addressed (R272-1 F2/F3/F4, R273-1 F1) are
genuinely fixed and their controls fire; the full gate reproduces the author's
tallies exactly (255/255 with the SDK, 198/198 absent, 29/29 + 4/4 accepted).
So the NEGATIVE rests on F1 alone.

## Reconstruction basis

AGENTS.md and CONTRIBUTING.md (§6 lenses, §7 completion, "no reduction");
docs/README authority order; issues #408/#409 frozen acceptance (acceptance 4
"No reduction" governs) and their post-#498 remaining-scope comments; the
manager's A219 correction assignment
(https://github.com/kebag-logic/milan-fpga/issues/408#issuecomment-5802875987);
`git diff 759da623..ef903457` (only `sw/builder/test_builder.py`,
`docs/integration/BAREMETAL_FIRMWARE.md`, `docs/testing/CI_WORKFLOWS.md`
changed); issue #544 (function-like-macro identity overwrite, explicitly
deferred, out of this round). Prior public FINDINGS (R272-1, R273-1) read only
after the independent pass below.

Tooling verified before use: pinned RV32 SDK installed offline from the pinned
archive (sha256 `d42680e9...`) and `--verify-only` clean (GCC 14.3.0,
riscv32-buildroot-linux-gnu); scoped Verilator `5.050` at the manager path.
Faithful-environment check: both authoritative gate runs reproduce the author's
numbers exactly (receipts `gate1b-sdk.txt` 255/255, `gate1b-absent.txt`
198/198), so F1 is a real gap, not a broken run.

---

## F1 — BLOCKER — Conformance, Robustness, Tests, Docs

**Artifact:** `sw/builder/test_builder.py` — the shared directive lexer /
readers: `spliced()` (~L3782), `cpp_directive_re` / `cpp_hash` (~L2691),
`c_lexed()` (~L2542), the KEPT `%:`/`??` ban in
`_assert_primitive_spelling_is_readable()` (~L2259), the fixed `lexer_corpus`
(~L4844); `docs/integration/BAREMETAL_FIRMWARE.md` (the `%:`/`??` row and the
"bound is measured" / corpus caveat, ~L1262-1470).

**Authority / evidence.** Issues #408/#409 acceptance 4 ("No reduction: every
mutation the retired rules pinned is re-pinned … the count is not below 163");
the A219 assignment: the F1 BLOCKER "is a real loss of protection … a directive
spelling hides a conditional from every gate 1b directive reader while GCC
honours it, so stores the retired cast and asm sets refused are accepted.
Acceptance 4 (no reduction) governs. Any retired rule whose replacement cannot
match it is restored."

Measured, pinned GCC 14.3 `-std=gnu99` (`receipts/gcc-spellings.json`,
`receipts/FINDING-F1-summary.txt`):
- `%\`<newline>`:ifdef FOO … %\`<newline>`:endif` is honoured as `#ifdef`: the
  FOO arm is conditionally dropped (keeps `("a","z")`), exactly as `#ifdef`
  and `%:ifdef` do. Digraphs are active at gnu99 (unlike trigraphs).
- On the exact hostile block (`scratch/hostile_block.c`): with no
  `CSR_UART_BASE` (the census stub tree) GCC drops the store; with
  `-DCSR_UART_BASE=1` (the shipping product, whose LiteX header defines it) GCC
  compiles `*(volatile unsigned int *)0x90000600u = 1u;` (emits `sw`).

Gate probe, full gate 1b, SDK mapped, Verilator 5.050
(`receipts/probe-split-digraph.txt`; harness
`scripts/probe_split_digraph.py`), a product-only cast store in a UART command
handler:
- `#ifdef CSR_UART_BASE` → REFUSED (SELECTION_PIN + CENSUS_PIN);
- `\f#ifdef` (form feed) → REFUSED (the round's fix works for the corpus);
- `%:ifdef` (plain digraph) → REFUSED (`%:`→`#` translation);
- `%\`<newline>`:ifdef` (split digraph) → **ACCEPTED**.

Dev gate (`759da623` `test_builder.py`, same byte-identical firmware/CSR/soc)
on the same store (`receipts/probe-dev-split-digraph.txt`;
`scripts/probe_dev2.py`): `#ifdef` REFUSED (ordered cast set), split digraph
REFUSED (file-wide token-joining splice ban). **Dev refused; head accepts.**

**Impact.** A firmware carrying `%\`<newline>`:ifdef CSR_UART_BASE` … CSR store
… `%\`<newline>`:endif` passes gate 1b, yet the pinned GCC compiles that store
into the shipping product (`CSR_UART_BASE` defined), enabling/writing the
entity CSR the boot gate exists to police, while the census stub tree
(`CSR_UART_BASE` undefined) drops the arm so the resolver never sees it. This is
the precise stub-tree/product asymmetry per-selection grading exists to close,
defeated because the readers never find the conditional. It is a reduction
versus dev (which refused the same store on every machine) and reproduces in
both compiler-present and compiler-absent modes.

Why it slips at head (read from the diff, confirmed by probe):
1. Readers run `spliced(code)`. `spliced()` translates `%:`→`#` on raw text
   **before** closing splices, so `%\`<newline>`:` (no `%:` substring) is not
   translated; it then blanks the splice to `%  :ifdef`, which
   `cpp_directive_re` (`^[ \t]*#(?!#)…`) does not match. No reader sees the
   conditional.
2. The KEPT `%:` ban is `assert "%:" not in code` over the length-preserving
   blanked view, where the code splice is retained (`%`,`\`,newline,`:`), so the
   substring `%:` is absent and the ban does not fire.
3. R272-1 F2's fix narrowed the token-joining splice ban to the six boot-path
   bodies; the UART handler is outside them, and outside them splice/paste are
   "retired onto the resolver, which reads the call or store a splice or paste
   builds." That premise fails here: the splice builds a **directive**, not a
   store, so there is nothing for the resolver to read — the census simply drops
   the arm.
4. The fixed 55-entry `lexer_corpus` tests `%:ifdef` and `??=ifdef` but not the
   splice-split digraph, so `assert_lexer_matches_compiler()` and the 43 round-2
   controls never exercise this spelling; no control fails for it.

The disclosed limitation ("a spelling outside the corpus that GCC reads
differently is outside the measurement") is a general caveat and does not
discharge acceptance 4 here: `%:` is a documented C digraph the gate explicitly
models and the page's `%:`/`??` row states is refused ("nothing but a digraph or
a trigraph spells either pair"), so this is an undisclosed, concrete reduction of
a spelling the gate claims to handle, not an unknowable one.

**Required outcome.** Restore protection for this class where the replacement
cannot match it (the manager's own remedy for F1), e.g. one of: keep the
token-joining splice ban file-wide (as dev had it) rather than only inside the
six bodies; recognise a `%:` (and `%:%:`) digraph even when a splice splits it,
in both `spliced()` and the KEPT `%:` ban (close splices before the digraph
translation); or add the splice-split digraph spellings to the lexer corpus so
the readers are measured against GCC on them. A control must be added that is
GREEN when the fix is present and RED when removed, and the row/caveat in
`BAREMETAL_FIRMWARE.md` corrected.

**Verification.** `scripts/probe_split_digraph.py <sdk> split_digraph` must exit
0 (REFUSED) after the fix; the four spellings above must all be refused; the
whole-suite tallies must not drop a legitimate accepted case.

---

## Round-1 findings: retained or resolved at this head

Read after the independent pass. All confirmed fixed; every listed control is
refused in the 255/255 SDK run (`receipts/gate1b-sdk.txt`) and no legitimate
edit is refused (29/29 + 4/4 accepted):

- **R272-1 F1 (form feed / VT / NUL / lone CR before `#`)** — the four given
  spellings are RESOLVED (probe: `\f#ifdef` store REFUSED; corpus 55/55 read as
  the pinned GCC records and re-measured on the compiler). The **class is not
  closed** — see F1 above (split `%:` digraph).
- **R272-1 F2 (`-E` compared only eight boot tokens)** — RESOLVED for the six
  boot-path bodies: the splice and `##` bans are KEPT there and refuse on every
  machine; `assert_boot_path_is_spelled()` refuses the spliced/pasted/nested
  identity-sample forgeries (controls in the SDK run). Note the narrowing to the
  six bodies is what leaves F1's class open outside them.
- **R272-1 F3 (every combination graded; correlated debug misnamed)** —
  RESOLVED: `condition_key()`/`arm_selections()` relate groups on one macro; the
  selection sentence reads "graded as a firmware of its own"; the two correlated
  debug edits are accepted, a store in the second related group refused.
- **R272-1 F4 (open literal desynchronised the reader)** — RESOLVED: an open
  literal ends at its line as in GCC; open literal, raw string and any trigraph
  are refused before any reader (`assert_lexes_as_compiled()`).
- **R273-1 F1 (absent-mode overstatement; second `#define`)** — RESOLVED:
  `assert_each_macro_defined_once()` refuses a second `#define` of a name on
  every machine (the hidden-read forgery H6/H7); the NOT RUN text, verdict first
  clause and page name what a compiler-absent runner loses (verified in
  `gate1b-absent.txt`).

Deferred and correctly out of scope: issue #544 (function-like-macro overwrites
the identity sample) and R273-S3; both stated as bounds in the page.

---

## Reviewer-owned coverage ledger

| Lens | Verdict | Examined artifacts (at head ef903457) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | GCC 14.3 directive semantics vs `spliced()`/`cpp_directive_re`/`c_lexed()`/KEPT `%:` ban and `lexer_corpus` in `sw/builder/test_builder.py`; `receipts/gcc-spellings.json`, `probe-split-digraph.txt`; acceptance 4 | R272-2 | ef9034578f97ebc2951801d867b7c57f8196423d |
| RTL | CLEAN | No HDL changed dev→head (`git diff --name-only`: only test_builder.py + 2 docs); gate's 46/46 RTL-mutant elaboration green under scoped Verilator 5.050 (`gate1b-sdk.txt`) | R272-2 | ef9034578f97ebc2951801d867b7c57f8196423d |
| Robustness | UNCLEAN (F1) | Hostile malformed directive spellings (form feed, VT, NUL, CR, plain and split `%:` digraph) through the full gate; `probe-split-digraph.txt`, `probe-dev-split-digraph.txt` | R272-2 | ef9034578f97ebc2951801d867b7c57f8196423d |
| Tests | UNCLEAN (F1) | `lexer_corpus` (55) + the 43 round-2 controls do not cover the split `%:` digraph and no control fails for it; otherwise sound — `gate1b-sdk.txt` 255/255, `gate1b-absent.txt` 198/198, 29/29 + 4/4 accepted, negative reason-pin control present | R272-2 | ef9034578f97ebc2951801d867b7c57f8196423d |
| Docs | UNCLEAN (F1) | `docs/integration/BAREMETAL_FIRMWARE.md` `%:`/`??` row overstates refusal of `%:`; corpus caveat understates a concrete reduction. Gates green: `docs_check.txt`, `em_dash.txt`, `baremetal_only.txt` all exit 0 | R272-2 | ef9034578f97ebc2951801d867b7c57f8196423d |

No lens is covered clean while F1 (BLOCKER, attributable to four of them) is
open. RTL is clean on its own artifacts and findings elsewhere do not un-cover
it.

## Real limits of this review

- Source validation only, at the reviewed head. The final current-dev candidate
  merge (source base `759da623`, live dev `50e78097…`) is the manager's to build
  and gate; not attempted here.
- Physical calibration NOT RUN; hardware-dependent fields not proven (no hardware
  in scope).
- I ran gate 1b (SDK + absent), the docs/em-dash/baremetal gates, and focused
  fault probes only. I did **not** run the full parent/PP/gPTP/Yosys/builder
  banks, `act`, or hosted contexts (out of scope). Hosted exact-head evidence and
  the full static/native banks are the manager's acceptance (public evidence
  cited in the assignment).
- The `%:` split-digraph is demonstrated at the gate-1b boot-contract level, the
  gate the finding concerns; I did not enumerate every other digraph/whitespace
  permutation. `??`-trigraphs are inert at gnu99 (measured) and are additionally
  refused, so they are not a parallel hole.

## Pending manager/lane duties (not this reviewer's)

- Fix F1 and re-review at the new head (a later commit un-covers the lenses F1
  touches; coverage banks against a commit, not a round).
- Build and gate the current-dev candidate merge per CONTRIBUTING §2.7; run
  hosted required contexts on the pushed head; post-merge containment.
- Two independent positive reviews (one external) remain the bar; this review is
  not positive.

R272-2 FINISHED
