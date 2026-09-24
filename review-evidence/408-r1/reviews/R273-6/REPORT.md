[R273] NEGATIVE - exact head 4a56ef08ffb5c6e4dc3d1d31761949870c5bbe23

External independent review, round R273-6, of PR #535 (issues #408 + #409),
correction round 4 (A254, commit 4a56ef08 on 11b1b86c, tree cd80452d). This
was a cleared-context review. I reconstructed the task from AGENTS.md,
CONTRIBUTING.md, docs/README, the frozen #408/#409 acceptance, the manager
direction on #408 (comment 5813535416) and the manager decision on the
author's open points (comment 5815136430). I then read the diffs
`759da623..4a56ef08` and `11b1b86c..4a56ef08` and the public executable
evidence. My verdict and ledger were fixed in
`receipts/verdict-before-prior-findings.txt` before I read any prior public
finding. No other reviewer's report on this head was read. Section D gives
the disposition of prior findings.

Scope of this round: close S with a CHARACTER ALLOWLIST that is checked
first. Every C-reading regex runs in ASCII mode. A GENERATED closure table
holds 2520 cells. I was asked to judge five things:
- can any byte sequence reach a reader and be read differently from GCC;
- is acceptance 4 met;
- do the docs and the gate print state the allowlist honestly;
- the author's claims, by trying to break the table;
- the result of re-running every probe from my earlier rounds, unchanged, in
  both modes.

Tool identities were verified before use (`receipts/verilator-identity.txt`,
`receipts/sdk-verify.log`):
- Verilator 5.050 rev v5.050, sha256 905795b9...
- The pinned RV32 SDK riscv32-ilp32d--glibc--stable-2025.08-1, installed
  offline from the archive with sha256 d42680e9... (equal to ci_rv32_sdk
  ARCHIVE_SHA256), gcc 14.3.0.

The clone was byte-exact before and after every probe
(`receipts/clone-state-{before,after}.txt`): HEAD 4a56ef08, tree cd80452d,
the index tree equals HEAD, and porcelain and ignored are empty. The four
submodule gitlinks are unchanged (external efeb541a, gptp-processor c1b61743,
protocol-processor 424c688f, third_party/verilog-axis 48ff7a7e). verify_clone
checked 872 blobs by byte hash with 0 mismatches. Every probe ran in the
foreground, on in-memory copies of the gate or on extracted functions.
Nothing was written into the clone.

================================================================================
VERDICT: NEGATIVE
================================================================================

The round's central property holds, and I tried to break it. No byte
sequence I could build reaches a reader and is read differently from the
pinned GCC.

Part A re-measured all 2520 of the gate's own closure cells, one file per
GCC invocation:
- 0 differ from `_CLOSURE_KEPT`;
- 1470 are refused by the allowlist, 32 by another rule of S, and 1018 are
  read as GCC reads them;
- 43 are cells the allowlist closes, and the U+00B7 negative control is among
  them;
- 0 cells refused by the allowlist carry an `outside` flag the table
  contradicts.

On top of the table I added 8442 cells:
- 21 positions the table does not hold;
- every byte 0-255, the gate's 24 sequences and 17 more (noncharacters,
  bidirectional controls, soft hyphen, overlong NUL and others);
- every pair from a 22-byte ASCII and whitespace set, in 5 directive and
  identifier positions;
- 32 contested comment and literal boundary spellings.

The result of those 8442 cells:
- 0 cells where S admits the text and the readers and GCC both read names
  but differ;
- every admitted non-ASCII character sits in a comment or a literal;
- the allowlist runs first in `assert_boot_contract()`
  (test_builder.py:10064);
- with the allowlist disconnected in memory, all 12 of its pinned mutations
  fail, and 8 pass the whole gate when no compiler is present. This matches
  the author's claim exactly.

Acceptance 4 is met: 280/280 SDK and 222/222 absent, exit 0, both above 163;
29/29 + 4/4 edits accepted in both modes.

The single reason for NEGATIVE is F1, a documentation and honesty defect in
how the refusal of a byte that is not UTF-8 is justified. It is fixed with
text only. It leaves Docs and Conformance UNCLEAN. RTL, Robustness and Tests
are CLEAN.

--------------------------------------------------------------------------------
F1  MINOR  — Docs, Conformance
    The page and the gate's refusal message give GCC parity as the reason for
    refusing a byte that is not UTF-8 in a comment. The pinned GCC accepts
    that byte, and the page does not state the cost the manager decision
    requires it to state.
--------------------------------------------------------------------------------
Artifacts:
  - docs/integration/BAREMETAL_FIRMWARE.md:306 (the S row for "5.2.1 source
    characters, inside a comment or a literal"): "A byte that is not UTF-8 is
    refused wherever it sits, a comment included: GCC reads the file as UTF-8
    too, ..."
  - docs/integration/BAREMETAL_FIRMWARE.md:1346 (the allowlist cost row). It
    lists "a byte that is not UTF-8 anywhere, a comment included" as refused.
    Its "why" column never says that GCC accepts such a byte, and its
    **Remedy** ("keep any other character in a comment or a literal") does not
    apply to that half of the rule.
  - sw/builder/test_builder.py:5155-5160, the refusal message: "it is not
    UTF-8, which is how GCC reads the file as well, so S refuses it wherever
    it sits, a comment or a literal included". The same reasoning is in the
    S comment at :5116-5117 ("GCC reads its input as UTF-8 too").
  - receipts/gcc-invalid-utf8-comment.txt

Authority and evidence:
  - The manager decision on #408 (comment 5815136430), item 2: "Invalid UTF-8
    inside a comment is refused, although GCC accepts it there. The gate
    fails closed, and the page states the cost."
  - Direction 5 (comment 5813535416): the docs and the gate print state the
    allowlist as it runs.
  - Measured: `int a; /* \xb7 \xff */` preprocesses with rc 0 on the pinned
    riscv32-linux-gcc 14.3.0 at -std=gnu99 -E. Even with -Winvalid-utf8 it
    only warns and still exits 0 (receipts/gcc-invalid-utf8-comment.txt).
  - The author's REVIEW READY (#408 comment 5815097615) also says "GCC
    accepts it there. That cost is stated." No sentence on the page or in the
    gate print says GCC accepts it. The reason given ("GCC reads the file as
    UTF-8 too", "which is how GCC reads the file as well") tells a reader the
    refusal mirrors the compiler. It is a deliberate fail-closed refusal of
    an edit the compiler accepts.

Impact:
  - The behaviour is correct and fails closed. Nothing is admitted that
    should not be.
  - The authoritative page misstates why one of the new refusals exists, and
    it gives a remedy that does not work for it. A future editor or reviewer
    would take this refusal for GCC parity, not for a stated cost. They
    could then "fix" a supposed mismatch the wrong way, or miss that this is
    a known over-refusal.
  - This is the honesty point the round was asked to meet: "state the
    allowlist as it runs", and "the page states the cost".

Required outcome (not prescribing wording):
  - BAREMETAL_FIRMWARE.md:306 and :1346 and the refusal message at
    test_builder.py:5155-5160 state that the pinned GCC accepts a byte that
    is not UTF-8 inside a comment or a literal.
  - They state that S refuses it anyway, by decision, to fail closed, and
    that this is a cost.
  - The :1346 remedy covers that half of the rule (for example: re-encode
    the file as UTF-8).

Verification: re-read the three sites. `docs_check.py`, `check_doc_style.py`,
`gen_toc.py --check`, `check_doc_paths.py`, `check_em_dash.py --base
759da623` and `check_baremetal_only.py --check` still exit 0. If the message
text changes, the gate's own mutation "a byte that is not UTF-8, in a
comment" still refuses on SUBSET_CHARACTER_PIN in both modes.

--------------------------------------------------------------------------------
S1  SUGGESTION  — Docs, Tests  (optional; does not affect coverage)
    "Every byte in every position" overstates a nine-position table.
--------------------------------------------------------------------------------
Artifacts: BAREMETAL_FIRMWARE.md:1346 ("the closure table above is that
proof, every byte in every position"); test_builder.py:5108 (the same
phrase); `_CLOSURE_POSITIONS` (test_builder.py:2758) holds 9 positions.

Evidence: receipts/closure-extend.jsonl and closure-extend-summary.txt,
receipts/boundary-probe.log.
- For the REFUSAL half, position does not matter by construction. The
  allowlist scans the whole code text (`_C_S_OUTSIDE_RE` over
  `_c_phases(source).code`, test_builder.py:5162-5166). My extra positions
  confirm it: every non-ASCII cell in a code position was refused by the
  allowlist, 3526 of them.
- For the admitted ASCII bytes, exactness outside the nine positions rests on
  the 1845-spelling lexer corpora, not on the table. In my extra positions no
  admitted cell had the readers and GCC both read names and differ.
- There were two asymmetries, both harmless:
  - 32 cells are files GCC refuses to preprocess while `lexer_keeps` returns
    names. Examples: `#ifdef!FOO` in live code (29 bytes), `#a#ifdef` and
    `a\n#b`. No product can be built from such a file.
  - 4 cells are valid files the reader refuses: a null directive `#` followed
    by a line end or CR, then `#`. That is fail-closed.

Suggestion: say "every byte in each of the nine positions" (the paragraph at
BAREMETAL_FIRMWARE.md:322-337 already does), or add a directive-argument
position to the table. Neither is required.

================================================================================
LENS LEDGER  (reviewer-owned)
================================================================================
| Lens | State | Examined artifacts (at head 4a56ef08) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Manager direction 5813535416 items 1-5 and decision 5815136430 items 1-2 (F1: the page does not state that GCC accepts a byte that is not UTF-8 in a comment, as item 2 says it does). #408/#409 acceptance 1-5. Allowlist `_C_S_CHARACTERS`/`_C_S_OUTSIDE_RE`/`_C_S_UNDECODED_RE` tb.py:2726-2731, run first in `assert_within_lexical_subset()` tb.py:5144-5166, called first in `assert_boot_contract()` tb.py:10064. BOM refused (manager item 1): r2 B1/B2 and bom B1-B7 REFUSED in both modes. gate1b/head-{sdk,absent}.log: 280/280 and 222/222, 29/29 + 4/4, exit 0 | R273-6 | 4a56ef08 |
| RTL | CLEAN | `git diff 11b1b86c..4a56ef08 --stat`: only sw/builder/test_builder.py and docs/integration/BAREMETAL_FIRMWARE.md; no hdl/, syn/ or constraints/ file in `759da623..4a56ef08`. Gate 1b's RTL-reading checks (CSR decode, datapath, `blanked_sv`) are unchanged this round and pass in both modes (gate1b logs) | R273-6 | 4a56ef08 |
| Robustness | CLEAN | closure-extend: 10962 cells, 0 cells where S admits and the reader and GCC both read names but differ. Every non-ASCII character in a code position refused (table and 21 extra positions). Invalid UTF-8, overlong, surrogate and truncated sequences refused anywhere. boundary-probe: 32 contested comment/literal boundaries (splices in comment openers and closers, lone CR, apostrophe after a pp-number, prefixes, U+2028/U+0085/U+FEFF), 0 holes. Two BOMs, and a BOM at offset 1, refused. Unicode-aware str methods in the reader range read the blanked view (tb.py:10716) and fail closed. Disconnect: 8/12 allowlist entries pass the whole gate without the compiler; BOM alone with it | R273-6 | 4a56ef08 |
| Tests | CLEAN | `assert_character_closure()` tb.py:5864: Part A re-derived all 2520 cells one file per GCC call, 0 record mismatches, 43 closes including the U+00B7 negative control. `subset_refusal_corpus` tb.py:5236 (22 entries) plus 3 within-S controls. The 12 mutation entries pinned on SUBSET_CHARACTER_PIN all FAIL with the allowlist disconnected (disconnect/allowlist-off-{sdk,absent}.json), so each can fail for the defect it pins. Mutations 222/222 absent through the probe driver (disconnect/mutations-intact-absent.json). Lexer corpora 1845/1845 re-measured on the SDK. S1 is optional | R273-6 | 4a56ef08 |
| Docs | UNCLEAN | BAREMETAL_FIRMWARE.md:296-337 (S table 5.2.1 rows, closure paragraph), :1346 (cost row), :1564-1592 (fifth-round disconnect paragraph; its counts match my disconnect run), :1619-1637 (280/222, 29 + 4, nine new entries, three re-pinned: confirmed). Gate print tb.py:15649ff and :15832ff (matches gate1b logs). docs_check, check_doc_style, gen_toc --check, check_doc_paths, check_em_dash --base 759da623, check_baremetal_only --check, check_py_idiom, `git diff --check`: all rc 0 (static-checks.log). F1 open (rationale for the non-UTF-8 refusal, :306, :1346, tb.py:5155-5160) | R273-6 | 4a56ef08 |

================================================================================
A. WHAT WAS RUN (all receipts in this packet, listed in MANIFEST.sha256)
================================================================================
1. Gate 1b at the head (`sw/builder/test_firmware_compiler.py`), run twice:
   once with `--sdk-destination <sdk>` and once with `--absent`
   (receipts/gate1b/).
   - SDK: `GATE 1b PASS; 0 NOT RUN`, 406 compiles.
     - 280/280 mutations.
     - 1845/1845 spellings, re-measured on riscv32-linux-gcc.
     - 2520/2520 closure cells, split 1470/32/1018 with 43 closes,
       re-measured.
     - 22 subset refusals and 3 controls.
     - 29/29 + 4/4 edits accepted.
   - Absent: `GATE 1b PASS; 1 NOT RUN`, 0 compiles.
     - 222/222 mutations.
     - The same 2520 cells, recorded and not re-measured.
     - 29/29 + 4/4 edits accepted.
     - The stand-down names the allowlist in its print.
2. My earlier-round probes, UNCHANGED. The 49 probe and case files are
   byte-identical to the R273-5 manifest
   (receipts/probes-unchanged-vs-r273-5.txt). They were run in both modes:
   - receipts/probes/: r1, r2, bom, extra, hi, md, unread, published,
     grader and v272 at the head; md also at 11b1b86c and at dev; r1 also at
     dev;
   - receipts/round2/: the round-two whole-gate probe with its spellings;
   - subset-probe: 24 spellings, 0 holes. All 20 extended-character
     spellings and both `$` controls are REFUSED by S; the 2 within-S
     controls agree with GCC;
   - lexer-oracle (byte-identical to its R273-5 receipt:
     record_vs_gcc 0, gate_vs_record 0; the 2 "extra_lost" are
     `__has_include` spellings that S refuses).
   Against R273-5 every verdict change goes ACCEPTED to REFUSED
   (receipts/compare-vs-round5.txt):
   - r2 B1 (BOM alone), both modes;
   - bom B6 (BOM alone), both modes, and B5 (a cast-store macro behind a
     BOM), absent;
   - md MD1/MD1a/MD1b (U+00B7/U+0387/U+203F window stores), absent;
   - md MD5 (U+00B7 benign control), both modes.
   The only ACCEPTED cases left are:
   - controls: MD6 U+00B7 in a comment, HI3p, MD1p, B2c, U0;
   - the documented absent-mode stand-downs: extra X1/X2, a splice or paste
     outside the six bodies, and r2 C1/C2/C3/C5;
   - the documented #544 `__CONCAT` bound: X4.
   round3/lexer_probe.py fails with `NameError: _c_phases`
   (receipts/round3/). That is its round-one-layout extractor, which the
   head-layout lexer_oracle.py (above) supersedes. The failure is
   pre-existing and reproduces at 11b1b86c, as the author also reports.
3. New this round (probes/r6_extract.py, closure_extend.py,
   boundary_probe.py, regex_audit.py):
   - closure-extend.{log,jsonl,summary}. The raw log counts 36 "HOLE"
     because it treats a GCC refusal as a value. The summary splits those
     36 into 32 files GCC refuses to preprocess while the reader reads names
     and 4 reader refusals of valid files. There are 0 cells where both read
     names and differ.
   - boundary-probe: 32 spellings, 0 holes.
   - regex-audit: 197 `re.*` calls from tb.py:2342 to the end of the gate
     function.
     - Every call without ASCII mode that reads C text in the reader range
       is built on `cpp_hash` (`(?am)`, tb.py:3103), so it inherits ASCII
       mode.
     - The unflagged calls on C text at tb.py:11397-13439 build mutation-table
       inputs from the ASCII shipping firmware. They do not grade.
     - The rest read SystemVerilog, Makefile text, assembly, `-H` output,
       milan_soc.py or diagnostics.
     - Direction 2 is met for every reader.
   - firmware-bytes.txt: milan_baremetal.c holds only printable ASCII,
     1344 HT and 1640 LF. The Makefile holds printable ASCII, 3 HT and 21 LF.
   - disconnect/: the allowlist removed in memory, with 4 count-checked
     patches (cases/disconnect-allowlist.patch.json). Its 12 pinned
     mutations were graded in both modes. The author's published disconnect
     counts are reproduced.
   - static-checks.log: every doc and static check rc 0.

================================================================================
D. PRIOR PUBLIC FINDINGS — disposition at this head (read after the verdict)
================================================================================
  - R272-4 F1 MAJOR = R273-5 F1 MAJOR (a raw extended identifier character
    inside S; the readers disagree with GCC): RESOLVED.
    - S refuses every non-ASCII character in code by SUBSET_CHARACTER_PIN
      before any reader.
    - subset-probe: all 20 extended spellings REFUSED, 0 holes.
      md-head-absent MD1/MD1a/MD1b flip ACCEPTED to REFUSED, so the closure
      stops them, not the downstream grading.
    - The gate's `subset_refusal_corpus` carries U+00B7 and U+0301 after
      `#if` (R272-4's mid.c/comb.c shapes), U+0387, U+203F, U+00A0 and U+00B7
      in an identifier.
    - The Part A and extra closure tables show no admitted misread.
  - R273-4 F1 BLOCKER (`__has_include` header name): RESOLVED, retained. hi
    HI1-HI5 are REFUSED in both modes; lexer-oracle's two `__has_include`
    spellings are refused by S.
  - R272-3 F1 MAJOR (`$` in a directive name): RESOLVED, retained. S refuses
    `$` (subset-probe control; md MD1c).
  - R272-2 F1 BLOCKER (split `%:` digraph): RESOLVED, retained. round2 C4 and
    H1-H6 are REFUSED in both modes.
  - R273-3 F1 MINOR (BOM at offset 0) and F2 MINOR (`__CONCAT` bound):
    RESOLVED, retained.
    - The BOM is now refused outright, a stronger closure, per manager
      decision 5815136430 item 1. The accepted-edit count goes from 30 to 29,
      which the manager ruled a tightening, not a reduction.
    - X4 stays ACCEPTED as the documented #544 bound
      (BAREMETAL_FIRMWARE.md:407 and :1339).
  - R272-1 F1 BLOCKER, F2 MAJOR, F3/F4 MINOR, and R273-1 F1 MINOR: RESOLVED
    in earlier rounds, retained. The r1 cases show no verdict change against
    R273-5, and the 1845 lexer spellings were re-measured, 1845/1845.

================================================================================
REAL LIMITS OF THIS REVIEW
================================================================================
  - This is source validation only.
    - Physical calibration was NOT RUN, and field skips are not hardware
      proof.
    - I did not build the current-dev candidate merge (source base 759da623,
      live dev 59b81670). That is the manager's.
  - I ran no full parent, PP, gPTP, Yosys or builder bank (in particular not
    `test_builder.py --require-rv32`). The manager's public evidence covers
    them; I did not repeat it.
  - I ran no act, Docker or host orchestration. At most 8 parallel jobs ran,
    all in the foreground, in this clone and the packet scratch only.
  - Hosted contexts at the exact head, read only:
    - rtl-fast, verilator-suites, yosys-portability, docs-check,
      docs-check-no-git, full-ci-gate, bdd-conformance and the Verilator and
      Yosys shards completed with success;
    - "Physical gPTP (nightly and manual)" was SKIPPED, which is not a pass.
    - The manager owns hosted and act acceptance.
  - The RV32 SDK is the pinned disposable toolchain mapped onto the census
    selector. That is local compatibility evidence, not proof that the hosted
    selector adopts it.
  - The closure probes judge the readers through `lexer_keeps` and
    `lexer_names` (the gate's own corpus readers), loaded unmodified. They
    compare the `int` names each side keeps. A misread that leaves those
    names equal would not show. Absence of a demonstrated hole is not proof
    that none exists.

================================================================================
PENDING MANAGER DUTIES
================================================================================
  - Route F1 (MINOR, text-only) to a correction. Its lenses are Docs and
    Conformance; RTL, Robustness and Tests are covered CLEAN at 4a56ef08 and
    stay covered unless a later commit touches their scope.
  - Own the current-dev candidate-merge validation and hosted/act acceptance.
    Distinguish executed jobs from skipped contexts ("Physical gPTP" skipped).
  - Physical calibration and any hardware proof remain outstanding. They are
    not a source-review gate.

R273-6 FINISHED
