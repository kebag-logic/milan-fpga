[R832] POSITIVE - exact head 3c58b143eac812d173b4326423c030b65ec63f9a

# R832-2: external delta review of PR #893 (issue #883), the seventh pin adoption

- **Head:** `3c58b143eac812d173b4326423c030b65ec63f9a`, tree `df75ea455a6bd742a4614b97e6dd5813d369991f`.
- **Delta:** `e18c8225..3c58b143`, two one-line commits (`8f3735d7`, `3c58b143`) under the round 3 ruling (#883 issuecomment-6809058443).
- **Source base:** `46c971fa`. Live dev is `fa6c094b`. Dev and the base hold the same bytes for both changed files, so dev's pattern is the base pattern.
- **Verdict basis:**
  - No BLOCKER, MAJOR or MINOR is open, so all five lenses are clean at this head.
  - F1 from the previous round is fixed. The PR-body and `TESTING.md` residue is fixed.
  - One prior RESIDUE stays open on #495, and this round adds one new PR-body RESIDUE. Three prior SUGGESTIONs are retained. None of these blocks the verdict.

## Context reconstructed

- **Contract read:** AGENTS.md sections 3 and 5 to 8, and the ruling.
- **What the ruling allows:** tooling and docs only, with no image, RTL, firmware or pin change. It names the F1 required outcome and residue items R1 and R2. The gates it names are `check_cpp_idiom.py --selftest`, the docs gates and `git diff --check`.
- **Author evidence:** the author's REVIEW READY at this head (#883 issuecomment-6810008166) and the PR body at `updatedAt 2026-11-11T23:52:05Z`, whose `headRefOid` equals this head.
- **Not used:** no private author material and no other reviewer's round-2 report. I read prior public findings only after my own pass over the delta.

## Delta scope (verified)

- **Changed files:** `git diff --name-status e18c8225 HEAD` lists only `M docs/testing/TESTING.md` and `M scripts/check_cpp_idiom.py`. The selftest lives inside `check_cpp_idiom.py`. The PR text is outside the tree. See `receipts/delta_scope.txt` and `receipts/delta.diff`.
- **No image, RTL, firmware, pin or gitlink change:**
  - `protocol-processor` is `801ef2283ec793e35a2590fc6593c90313a64041` and `gptp-processor` is `1616fc8f062fbf58c35ad31674b5b233207bbdb8`, the same at `e18c8225` and at this head.
  - No `hdl/`, `fw/`, `syn/` or `tb/` path is in the delta.
- **Commits:** both are one line with no trailers, each with one parent, in a linear chain on `e18c8225`.
- **`git diff --check`:** rc 0 against both `46c971fa` and `e18c8225`.

## Executed at this head (my own runs)

All runs used `python3 -I`, Python 3.14.9, on this clone or on scratch copies of it.

| What | Result | Receipt |
|---|---|---|
| Parent C++ idiom gate, tree scan | rc 0; `multi-declarator declaration: 0 <= 0`; every ratchet within budget; 2.49 s wall | `receipts/gate.txt`, `receipts/timing_base_vs_head.txt` |
| `check_cpp_idiom.py --selftest` | 83 checks: 83 PASS, 0 FAIL, rc 0 | `receipts/selftest.txt` |
| Planted mutants, each in its own mirror with only `_DECL_TEXT` replaced (`scripts/mutate_multidecl.py`) | All three KILLED; per-mutant detail below this table | `receipts/mutants.txt` |
| Prior-round probe `probe_cpp_multidecl.py` (unchanged, sha256 `25fba1ba...ab185ab`) | The head verdict equals `real>1` on all 9 rows | `receipts/probe_r832-1_at_head.txt` |
| Own edge probe (`scripts/probe_multidecl_edges.py`) | 0 wrong verdicts on 14 in-scope rows; detail below this table | `receipts/probe_edges.txt` |
| Python idiom gate at the 1000-line module bound, plus its selftest | rc 0, `over-long line: 0 <= 0`; selftest 54/54. The file is exactly 1000 lines, and its longest line is 113 columns against a limit of 120. | `receipts/py_idiom_gate.txt`, `receipts/gate_check_py_idiom_py_selftest.txt` |
| Docs gates that read `TESTING.md` | `docs_check.py` 0 findings over 215 md files; `check_doc_style.py` OK; `check_hygiene.py --check` PASS. `check_em_dash.py --base 46c971fa` did not run here (rc 2, missing renderer dependency); a manual scan of the delta's 16 added lines finds 0 em dashes. | `receipts/gate_*.txt` |
| Comment rule on added source lines | One new comment, `check_cpp_idiom.py:269`. It states the behaviour and `#495`, with no lane label, round, reviewer ID or comment ID. | `receipts/delta.diff` |
| Restore | HEAD, tree and index equal the exact head. The two blobs match by sha256. Gitlinks are unchanged. The bytecode caches this session created were removed, leaving 0 untracked or ignored entries. | `receipts/restore_check.txt` |

**Planted mutants, in detail:**
- The `e18c8225` flat-brace pattern fails the three nested two-declarator arms.
- A once-nested (two-deep) pattern fails the three-deep arm.
- The base/dev pattern fails the three "a brace initialiser's commas separate elements, not declarators (#495)" arms.

**Edge probe, in detail:**
- The 14 in-scope rows cover empty braces, a string literal holding a comma, a call inside braces, two initialisers both three deep, three declarators, `WData`, a `for` initialiser and a call.
- A row outside the documented scope behaves as the code comment says. `int d[1][1][1][2] = {{{{1, 2}}}}, e = 0;` is four deep and reads 0, the stated "up to three braces deep" limit. An unterminated one-line `{0,` reads 0.

**Hosted state at this head:** 1 check completed with success and 16 are queued, as read-only (`receipts/hosted_checkruns_head.tsv`). This is not acceptance evidence. The manager owns hosted and act acceptance.

## Findings

### N1 - RESIDUE - Docs - PR #893 body, validation table, row "C++ idiom gate"

- **The text:** "a one-level pattern the three-deep arm".
- **Why it is residue:** the same row calls `e18c8225`'s pattern "flat-brace", and a flat brace is also one level of braces. A reader can take "one-level" to mean that same pattern. The author's REVIEW READY says it unambiguously ("a one-nested-level pattern"), and `receipts/mutants.txt` confirms that the two-deep pattern fails only the three-deep arm. The defect is wording only.
- **Exact fix:** "a one-level pattern the three-deep arm" -> "a once-nested (two-deep) pattern the three-deep arm".

No BLOCKER, MAJOR or MINOR in this round.

### Checked and not a finding

- **F1 required outcome:**
  - Commas inside a balanced one-line brace initialiser are ignored to two nested levels, one more than the ruling's "at least one nested level". Commas between declarators still count (`check_cpp_idiom.py:269-271`). The separator `,` sits outside `_DECL_TEXT`'s brace groups, so a comma inside braces can never be taken as the declarator separator.
  - The arms are at `:705-712`. A nested single declarator gives 0 (`:705-708`), and nested two-declarator lines give 1 in both orders (`:709-712`).
  - The base pattern planted back still fails its arms.
- **Three reformatted arms** (`:700`, `:727`, `:738`): each joins a wrapped `scan(...)[...]` onto one line with identical semantics. They keep the module at exactly 1000 lines, the Python gate's bound, and every line stays at or under 120 columns.
- **Regex cost:**
  - The head pattern is quadratic on a pathological long line, as the base pattern was. On a 15 kB line it takes 1.06 s against the base's 0.24 s.
  - Real source lines are short, and the whole-tree gate runs in 2.49 s.
  - The alternation is disjoint on its first character (`[^{}\n]` against `\{`), so there is no exponential backtracking.
- **`TESTING.md:357` "the six gate mutants":** this equals `crflic_mutants.py` `MUTATIONS` entries 1 to 6 (`:91-113`, raw verdict and real grant, each everywhere, CRF alone and AAF source 0 alone). It also matches the Makefile comment at `:665`, "Six additional elaborations".
- **PR body #495 rows:**
  - Row 6758088112 cites `:269-271` and `:705-712`, which are correct at this head, and eight arms, which is 3 + 5, correct. Its planted-pattern claim matches `receipts/mutants.txt`.
  - Row 6731336971 now states all four items: items 2 and 3 are taken, and items 1 and 4 stay on #495.
- **Author's disclosed edge:** `int a = f(1, 2), b;` reads 0 at both the head and dev. Parentheses are excluded by design. The delta does not change this, and it is not F1.

## Prior public review findings (read after my own pass)

| Prior finding | Resolution at this head |
|---|---|
| F1 (R831-1 = R832-1), MINOR, Tests and Robustness, nested brace initialiser | **Resolved.** The required outcome is met as shown above. All three planted earlier patterns fail. The prior probe agrees on every row. The selftest passes 83/83 and the tree gate reads 0 <= 0. |
| R831-1 R1 = R832-1 R3, RESIDUE, PR body row 6731336971 | **Resolved.** The row now states its four items, and their status is accurate. |
| R831-1 R2 = R832-1 R1, RESIDUE, `TESTING.md:357` "three gate mutants" | **Resolved.** The line now says "the six gate mutants", which is correct. |
| R832-1 R2, RESIDUE, `syn/ooc/pp_resource_baseline.json:451` "+29 slices (80)" | **Retained as RESIDUE, open on #495.** The text is unchanged at `:451`, and the PR body says so (#495 row 6731336971 item 4). Exact fix as before: "+29 slices (80)" -> "+29 slices (+80)". |
| R831-1 S1, SUGGESTION, `sim_nxn.cpp` [AIDX] D label | **Retained as SUGGESTION.** It is outside the delta. |
| R831-1 S2, SUGGESTION, no planted arm for the [MVRPLA] bounds | **Retained as SUGGESTION.** It is outside the delta. |
| R831-1 S3, SUGGESTION, NFR-RES-01 stale figure | **Retained as SUGGESTION.** It is outside the delta. |

## Lens results at this head

```text
[R832] PASS Conformance - issue #883 ruling issuecomment-6809058443 against receipts/delta_scope.txt, scripts/check_cpp_idiom.py:269-271 and docs/testing/TESTING.md:357 - the delta is exactly the ruled scope (two files, no image/RTL/firmware/pin/gitlink change), meets F1's stated outcome and both residue items; acceptance items 1-5 depend on nothing the delta touches and keep R832-1's clean result at ancestor e18c8225
[R832] PASS RTL - receipts/delta_scope.txt (git diff --name-status e18c8225 HEAD; ls-tree gitlinks 801ef228 / 1616fc8f at both heads) - no hdl/, processor or gPTP path in the delta, so nothing within this lens's scope changed since R832-1 covered it clean at ancestor e18c8225
[R832] PASS Robustness - scripts/check_cpp_idiom.py:270-271; receipts/probe_edges.txt, receipts/probe_r832-1_at_head.txt, receipts/timing_base_vs_head.txt - boundary shapes (empty, flat, two- and three-deep, both declarator orders, strings/calls in braces, unterminated, four-deep documented limit) give the right verdict; no exponential backtracking; harness robustness untouched since e18c8225
[R832] PASS Tests - scripts/check_cpp_idiom.py:699-712 selftest arms; receipts/selftest.txt (83/83), receipts/mutants.txt (3/3 killed), receipts/gate.txt (0 <= 0) - each new arm fails for the defect it names; no test weakened; campaigns and legs untouched since e18c8225
[R832] PASS Docs - docs/testing/TESTING.md:357 against tb/verilator/milan_dp/crflic_mutants.py:90-113 and Makefile:665; check_cpp_idiom.py:269 comment against the pattern; PR #893 body #495 rows and validation table; receipts/gate_docs_check_py.txt, gate_check_doc_style_py.txt, gate_check_hygiene_py_check.txt - claims match the code and receipts; RESIDUE N1 and retained R832-1 R2 do not uncover the lens
```

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | the ruling; the delta's file list and gitlinks; F1 outcome at `check_cpp_idiom.py:269-271,705-712`; `TESTING.md:357` | R832-2 | `3c58b143eac812d173b4326423c030b65ec63f9a` |
| RTL | CLEAN | the delta's file list (no `hdl/`, processor or gPTP path); gitlinks `801ef228` and `1616fc8f` unchanged; the RTL itself last examined clean by R832-1 at ancestor `e18c8225`, and nothing in its scope has changed since | R832-2 (scope check); R832-1 (RTL content) | `3c58b143eac812d173b4326423c030b65ec63f9a` (R832-1: `e18c822536ebeaf1cb0f42abea74513501aa26c7`) |
| Robustness | CLEAN | `check_cpp_idiom.py:270-271`; the edge and prior probes; the timing check | R832-2 | `3c58b143eac812d173b4326423c030b65ec63f9a` |
| Tests | CLEAN | selftest arms `:699-712`; selftest 83/83; three planted mutants killed; tree gate; Python idiom gate | R832-2 | `3c58b143eac812d173b4326423c030b65ec63f9a` |
| Docs | CLEAN (N1 and R832-1 R2 to the residue checklist) | `TESTING.md:357` against `crflic_mutants.py` and the Makefile; the `:269` comment; the PR body #495 rows and validation table; the docs gates | R832-2 | `3c58b143eac812d173b4326423c030b65ec63f9a` |

## Real limits

- **No manager bank:** no manager source bank runs at this head, and I neither claim nor infer one. Source-head execution evidence beyond my focused runs is the author's published gate receipts.
- **Merge candidate not validated:** I did not validate the current-dev merge candidate (dev `fa6c094b`). That belongs to the manager at the merge turn. Dev's two changed files equal the base's, so dev and the delta do not diverge on these two files.
- **Em-dash gate not run:** `check_em_dash.py` could not run here because the pinned renderer dependency is not installed. I scanned the delta's added lines by hand instead. The authoritative run is the hosted or act docs job.
- **Gates not run:** I did not run the full docs workflow, any parent, PP, gPTP, Yosys or builder bank, or any Verilator build. The ruling and the delta need none of them.
- **Hosted evidence:** exact-head hosted contexts were mostly queued when I read them (1 success, 16 queued). That is not acceptance evidence.
- **Hardware:** physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- **Hosted and act:** run act at this head, and record hosted acceptance once the queued contexts finish (docs, wire-accountability, elaborate gates and full-ci-gate).
- **Merge candidate:** build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts on the PR.
- **Residue checklist:** carry N1 and R832-1 R2 (`pp_resource_baseline.json:451`, open on #495) to the residue checklist. Keep S1 to S3 as optional.
- **Merge approval:** pair this verdict with the internal delta reviewer's at this exact head. The merge still requires explicit maintainer authorization.

R832-2 FINISHED
