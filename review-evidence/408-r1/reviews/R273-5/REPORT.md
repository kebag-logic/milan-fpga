[R273] NEGATIVE - exact head 11b1b86c11378cac414ef58f6be40d8da00980da

External independent review, round R273-5, of PR #535 (issues #408 + #409),
correction round 3 (A248, commit 11b1b86c on 8e12d31f). Cleared context;
reconstructed from AGENTS.md / CONTRIBUTING.md, docs/README, the frozen #408 /
#409 acceptance and the manager decision on #408 (comment 5811522505), the
diff `759da623..11b1b86c` and `8e12d31f..11b1b86c`, and public executable
evidence. Prior public FINDINGS were read only after the independent pass
below; their disposition is in section D.

Scope of this round (manager direction, comment 5811522505): gate 1b now
checks a declared lexical subset **S** *before* any reader
(`assert_within_lexical_subset()`), enumerating the C11 6.4 token classes plus
gnu99 extensions as either modelled-exact or refused-by-name; the corpus is
restricted to S. Judge: is S closed, is every reader exact on S, does the
shipping firmware stay in S, is acceptance 4 met, do docs/gate print state S
honestly. Re-run every earlier probe unchanged in both modes.

Tool identities verified before use (receipts/verilator-identity.txt,
receipts/sdk-verify.log): Verilator 5.050 rev v5.050 sha256 905795b9…;
pinned RV32 SDK riscv32-ilp32d--glibc--stable-2025.08-1, gcc 14.3.0, archive
sha256 d42680e9… (matches ci_rv32_sdk ARCHIVE_SHA256). Clone byte-pristine
before and after all probes (receipts/clone-state-before.txt,
clone-state-after.txt): tree 0f40b320…, empty porcelain, four submodule
gitlinks unchanged. All probes ran in the foreground on copies / extracted
ASTs / in-memory hooks; nothing was written into the review clone.

================================================================================
VERDICT: NEGATIVE
================================================================================

One open MAJOR (F1) leaves the Conformance, Robustness, Tests and Docs lenses
UNCLEAN. RTL is CLEAN (no RTL artifact in this round's diff). Every prior
public finding this round targets is resolved at this head (section D), and
acceptance 4 (no reduction) is independently confirmed (271/271 SDK, 213/213
absent, exit 0, both above the 163 floor and round two's 264/206). The single
reason the verdict is NEGATIVE is F1: the round's central deliverable — a
*closed* grammar S on which "the readers read a directive exactly where GCC
does" — is not achieved for one C11 6.4.3 class, and the docs and gate print
assert that it is.

--------------------------------------------------------------------------------
F1  MAJOR  — Conformance, Robustness, Tests, Docs
    A raw extended identifier character in a directive name is inside S, and
    the readers disagree with GCC on it: S is not closed against C11 6.4.3.
--------------------------------------------------------------------------------
Artifacts:
  - sw/builder/test_builder.py:4893  assert_within_lexical_subset()  (S)
  - sw/builder/test_builder.py:4947  the UCN refusal (`view.find("\\")`)
  - sw/builder/test_builder.py:4988  subset_refusal_corpus (no non-ASCII case)
  - docs/integration/BAREMETAL_FIRMWARE.md:305 (the 6.4.3 row)
  - the gate print, test_builder.py:15184-15200 ("… a universal character
    name in an identifier … is refused by name before any reader") and
    :5137-5150 ("on S the readers … read a directive exactly where that GCC
    does")
  - receipts/subset-probe-identifiers.jsonl, receipts/nest.s,
    receipts/probes/md-head-{sdk,absent}.json, receipts/ident.c

Authority / evidence:
  - Manager decision on #408 (comment 5811522505), direction 1: S refuses "at
    minimum: `$` and universal character names in identifiers … Every other
    class the readers do not model exactly is refused too. A firmware
    containing anything outside S is refused … before any reader runs." Its
    acceptance 2: "Every reviewer probe from all rounds is either refused by
    the subset check or agrees with GCC."
  - C11 5.2.1.1 / 6.4.2.1 / 6.4.3 and Annex D: a source character outside the
    basic set that is a valid identifier character is, in an identifier,
    equivalent to a universal character name. GCC 14.3 at -std=gnu99 admits
    such a character directly (no backslash), in both an identifier and a
    directive name.
  - `assert_within_lexical_subset()` refuses the UCN *class* only by
    `view.find("\\")` (test_builder.py:4947): it catches the `\uXXXX`
    spelling and nothing else. A directive name carrying a raw U+00B7
    (UTF-8 0xC2 0xB7), U+0387 or U+203F is not refused.
  - Independent proof, three parts, all at this head:
    1. GCC accepts U+00B7 in a live identifier, clean at -std=gnu99 -Wall
       (receipts/ident.c compiles, exit 0).
    2. `receipts/nest.s`: a firmware fragment
         #ifdef MILAN_NEVER_DEFINED
         #if·x            (· = U+00B7)
         #endif
             *(volatile unsigned int *)0x90000600u = 1u;
         #ifdef MILAN_NEVER_DEFINED
         #endif·y
         #endif
       compiles under the pinned RV32 GCC to `li a5,-1879048192; li a4,1;
       sw a4,1536(a5)` — a live store to 0x90000000+0x600 = the ADP_CTRL
       window. GCC reads `#if·x` / `#endif·y` as unknown directives ignored
       inside the skipped `#ifdef MILAN_NEVER_DEFINED`, so the middle
       `#endif` closes the outer conditional and the store is live.
    3. receipts/subset-probe-identifiers.jsonl: for the same shape,
       `assert_within_lexical_subset()` returns without raising (S =
       ADMITTED) while the gate's directive reader and GCC disagree about the
       structure — eight within-S spellings (U+00B7, U+0387, U+203F, U+00A0,
       each in two shapes) where reader ≠ GCC. The `$` control on the same
       shape is refused by S; the extended characters are not.

Impact:
  - The property the round exists to establish — "exact on S; outside S
    refused", stated in the gate print and BAREMETAL_FIRMWARE.md:293-299,350 —
    is false: a within-S directive (`#if·x`) is read by the gate's reader as
    `#if` while GCC reads it as the unknown directive `if·x`. This is the same
    reader-vs-GCC defect class as R272-3 F1 (`$`) and R273-4 F1
    (`__has_include`), which this round was chartered to close by *closing the
    grammar* rather than by adding one more denylist entry. The implementation
    added denylist entries ($, backslash, __has_include, header-name, digraph,
    trigraph, raw, unterminated, _Pragma) but did not restrict the modelled
    character set, so a new spelling in the same class slips straight through
    to the readers.
  - Acceptance 2 is violated by letter: this reviewer probe is a within-S
    spelling that neither S refuses nor the readers read as GCC does.
  - No silent CSR-store / identity-forge / verdict-overwrite escape is
    demonstrated end to end. In SDK mode the compiled census is authoritative
    and catches every store regardless of the textual misnest (md-head-sdk:
    MD1–MD4 all REFUSED). In absent mode the census stands down, so the
    misnested cast store (MD1) is accepted exactly as its plain form (MD1p) is
    — the documented stand-down, not a new hole — and boot-path / ADP targets
    (MD2–MD4) are still refused because `arm_selections()` grades every arm of
    the unmodelled `#if` (16-selection cap → refuse, not fall through). The
    reader's conservatism is fail-safe on every shape I could build, which is
    why this is MAJOR and not BLOCKER. The manager may reasonably escalate to
    BLOCKER on strict non-compliance with direction 1, since the doc and gate
    print make a refusal + exactness claim that the code does not honour.

Required outcome (not prescribing the design):
  Either (a) S refuses a directive name / identifier carrying any character
  outside the modelled `[A-Za-z_0-9]` set (the honest reading of "every class
  the readers do not model exactly is refused", and of "6.4.3 UCN REFUSED"),
  with the message naming the construct before any reader; or (b) if such
  characters are to be admitted, the readers must be shown exact on them
  against GCC and the "6.4.3 UCN REFUSED" / "exact on S" claims in
  BAREMETAL_FIRMWARE.md:305,293-350 and the gate print corrected. Whichever is
  chosen, `subset_refusal_corpus` (or the corpus) must carry a raw
  extended-identifier-character case so the property is tested, and the
  mutation count must not drop.

Verification:
  - Re-run receipts/probes/subset_probe.py at the corrected head: every
    listed spelling is either S=REFUSED (naming the construct) or reader ==
    GCC (0 holes).
  - Re-run the md cases (receipts/probes/make_md_cases.py) in --absent: MD1 /
    MD1a / MD1b must be refused by S (like MD1c today) before any reader, so
    the closure — not the downstream census/arm-grading — is what stops them.
  - `docs_check.py`, `check_baremetal_only.py --check` still exit 0; the S
    table and gate print read true.

================================================================================
LENS LEDGER  (reviewer-owned)
================================================================================
| Lens        | State   | Examined artifacts (at head 11b1b86c)                                   | Covering round | Exact head |
|-------------|---------|-------------------------------------------------------------------------|----------------|------------|
| Conformance | UNCLEAN | manager decision 5811522505 (dir 1, acc 2); #408/#409 acceptance 1-5; C11 6.4.2.1/6.4.3, Annex D; assert_within_lexical_subset() tb.py:4893; gate1b-sdk.log (271/271), gate1b-absent.log (213/213); F1 | R273-5 | 11b1b86c |
| RTL         | CLEAN   | `git diff 8e12d31f..11b1b86c` touches only sw/builder/test_builder.py and docs/integration/BAREMETAL_FIRMWARE.md — no hdl/*.sv; the RTL-census/resolver behaviour (#409) is unchanged this round | R273-5 | 11b1b86c |
| Robustness  | UNCLEAN | assert_within_lexical_subset() tb.py:4893-4980, subset_refusal_corpus tb.py:4988; subset-probe-identifiers.jsonl (8 within-S reader≠GCC), md-head-{sdk,absent}.json; digraph/$/__has_include/BOM/raw/trigraph/_Pragma refusals confirmed (r2, hi, bom, unread receipts); F1 | R273-5 | 11b1b86c |
| Tests       | UNCLEAN | assert_subset_refuses() tb.py:5018, assert_lexer_matches_compiler() tb.py:5505; lexer-oracle.jsonl (fixed 78 + generated 1767, record_vs_gcc 0, gate_vs_record 0); corpus carries no raw extended-identifier case (F1); 271/271 & 213/213 re-pinned | R273-5 | 11b1b86c |
| Docs        | UNCLEAN | BAREMETAL_FIRMWARE.md:293-350 (S table, esp. line 305 6.4.3 row), :1319, :1565; the gate print tb.py:15184-15200 & :5137-5150; docs_check/doc_style/gen_toc/doc_paths/em_dash all exit 0 but the 6.4.3-REFUSED and exact-on-S claims are inaccurate (F1) | R273-5 | 11b1b86c |

================================================================================
D. PRIOR PUBLIC FINDINGS — disposition at this head
================================================================================
All confirmed by re-running the original probes unchanged in both compiler
modes (receipts/probes/, receipts/compare-vs-round4.txt):
  - R273-4 F1 BLOCKER (`__has_include(<...>)` header name hides a line):
    RESOLVED. HI1-HI5 flip ACCEPTED→REFUSED with "uses __has_include … outside
    S", in both sdk and absent (compare-vs-round4.txt). S refuses the class.
  - R272-3 F1 MAJOR (`$` after / in a directive name): RESOLVED. `$` refused
    by S in both modes (md-head-*: MD1c; subset_refusal_corpus entries 1-2).
  - R272-2 F1 BLOCKER (split digraph `%`\NL`:ifdef`): RETAINED refused. r2
    H1-H6, C4 all REFUSED in both modes.
  - R273-3 (byte-order-mark, paste-bound): unchanged. r2 B1 (BOM alone)
    ACCEPTED benign; B2 (BOM + 12th include) REFUSED; bom-head-* stable.
  - Acceptance 4 (no reduction): CONFIRMED. 271/271 (sdk) and 213/213
    (absent), exit 0; 1845/1845 directive spellings; 30/30 firmware edits.

================================================================================
REAL LIMITS OF THIS REVIEW
================================================================================
  - Source validation only. Physical calibration NOT RUN; hosted long-gate
    contexts and the current-dev candidate merge (source base 759da623, live
    dev eaf0e6c4) are the manager's and were not built here.
  - No full parent / PP / gPTP / Yosys / builder banks; no act / Docker / host
    orchestration; ≤8 parallel jobs, all foreground, inside the clone and the
    packet scratch only.
  - F1 is a demonstrated exactness / closure defect and a literal
    acceptance-2 violation; it is NOT a demonstrated silent-store escape. I
    could not weaponize it past the SDK census (authoritative) or the absent-
    mode stand-down + exhaustive arm grading. Absence of a demonstrated
    exploit is not proof none exists.
  - The RV32 SDK is the pinned disposable Bootlin toolchain mapped onto the
    census selector; this is local compatibility evidence, not proof of hosted
    selector adoption.

================================================================================
PENDING MANAGER DUTIES
================================================================================
  - Decide severity escalation of F1 (MAJOR vs BLOCKER) on the non-compliance
    reading of direction 1; either way it is blocking and un-covers four
    lenses.
  - Own the current-dev candidate-merge validation and the hosted / act
    acceptance; distinguish executed jobs from skipped contexts.
  - Physical calibration and any hardware proof remain outstanding and are not
    a source-review gate.

R273-5 FINISHED
