[R288] NEGATIVE - exact head 663d50d65ff49c33b153107b2f79d6f3c5725799

# R288-1 independent internal review: processor issue #99 / PR #119

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head: `663d50d65ff49c33b153107b2f79d6f3c5725799`, tree `21e0fddbbe927569b7e16f282088ea4fc1b7b7f1` (verified in the isolated detached clone)
- Source base: `008edbbf486598ae237414273d75e385cf0e1a56`; merged main: `60152f3ff068b81333326b5081b5303253ba7fe7`
- Commits reviewed: `52659df` (round 1, executor A244), `9cfe2d3` (merge of main `60152f3f`), `663d50d` (checker docstrings, executor A300)
- Review start: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/119#issuecomment-5826909437

## Verdict

NEGATIVE. The core deliverable is correct. Section 2 of the integrator guide and diagram 21 each list exactly the 24 overridable top-level parameters. The checker derives that set from the RTL and fails closed on every control assigned to it. The workflow change is limited to the new check, and no RTL changed.

Two MINOR documentation defects remain open:

- **F1:** five of the new owner links point to anchors that do not exist on GitHub.
- **F2:** the verification document's list of `make check` targets does not include the new `params` target.

Both are small, bounded fixes. Under the review rules, an open MINOR finding makes the verdict NEGATIVE.

## Reconstructed scope (public)

- No `AGENTS.md` or `CONTRIBUTING.md` exists at this head. The project conventions come from `README.md` and `docs/README.md`:
  - §2 single-source rules: parameter values live only in F01.5 and timing values only in F08.1.
  - §6 editing workflow: `make check` must pass.
- Issue #99 body: audit the top-level parameter inventory; no RTL or default change; do not duplicate authoritative values (#70).
- Decision 5789750553 (2026-09-23): a complete inventory. Every `protocol_processor_top` parameter goes in guide §2 and in diagram 21.
- Assignment 5810655949: documentation-only work on base `008edbbf`. It covers the five missing names, reconciles diagram 21 and its master, and names each owner without copying values. Validation is the documentation gates as CI runs them, plus an enumeration check that parses the top.
- Assignment 5826543636: merge main `60152f3f`, re-run the checker, run every CI gate plus the parent consumer check on `508-pp-pin-adopt`, and make no RTL change.
- Prior public review findings on PR #119: none. At fetch time the PR had only the two review-start comments, no reviews and no review comments (`receipts/pr119-*.json`). Nothing had to be resolved or retained.

## Findings

### F1 — MINOR — Conformance, Docs: five new owner links point to anchors GitHub does not generate

- **Location:**
  - `docs/guides/integrator.md:80`, `:81`, `:82`, `:83` link to `../architecture/07_memory_maps.md#331-realization-the-image-lives-in-main-memory-not-on-chip`.
  - `docs/guides/integrator.md:88` links to `…#332-the-other-main-memory-region-the-aecp-response-buffer`.
- **Authority:**
  - Acceptance (issue #99 assignment 5810655949; PR body): section 2 must link each parameter to its authoritative owner.
  - `scripts/check-links.py:62`: "A missing anchor is reported as loudly as a missing file because it fails the same way for a reader".
- **Evidence:**
  - GitHub renders the target headings `docs/architecture/07_memory_maps.md:147` and `:215` at this exact head with the ids `331-realization--the-image-lives-in-main-memory-not-on-chip` and `332-the-other-main-memory-region--the-aecp-response-buffer`. The em dash leaves a double hyphen (`receipts/gh-rendered-07_memory_maps.html`).
  - `scripts/github_anchor_check.py` checks every fragment in the two changed markdown files against GitHub's rendered ids. It reports these 5 links DEAD and the other 33 OK (`receipts/github-anchors-head.txt`, rc=1).
  - The repository's link gate passes these links only because its slug function collapses runs of whitespace (`scripts/check-links.py:22-26`, `\s+` → `-`), and GitHub does not. The same gap affects 4 links already on main (`receipts/slug-gap-scan-main60152f3.txt`, `receipts/github-anchors-preexisting.txt`). Those 4 are outside this PR; see S1.
- **Impact:** on the published rendering, the owner links for `DESC_BASE_P`, `DESC_LINE_BYTES_P`, `DESC_IDX_ENTRIES_P`, `DESC_NAME_ENTRIES_P` and `RESP_BASE_P` open 07 at the top of the page instead of the §3.3.1 or §3.3.2 contract. That is 5 of the 24 rows this issue exists to link to their owners.
- **Required outcome:** point these rows at anchors that exist both on GitHub and in the repository's link gate.
  - For §3.3.1, use the existing explicit anchor `#sec-desc-memory` (`07_memory_maps.md:146`). The guide's §4.1 already uses it, and it resolves OK on GitHub.
  - For §3.3.2, add an explicit `<a id="…">` anchor before the heading and link to it.
  - Do not use the double-hyphen slug. The local slug function would then fail it.
- **Verification:** `python3 scripts/check-links.py` still OK. `scripts/github_anchor_check.py <root> <repo> <new-head> docs/guides/integrator.md docs/diagrams/README.md` reports `0 dead` once the head is pushed.

### F2 — MINOR — Docs, Tests: the normative list of `make check` targets omits the new `params` target

- **Location:**
  - `docs/architecture/09_verification.md:109-121` (§7 "Documentation-sync regression").
  - Against it: `Makefile:12-13` (`check: … modmatrix params stale`).
- **Authority:**
  - 09 §7 is the verification architecture's list of what "`make check` is the CI gate, and runs today". The `Makefile:12` comment defers to it: "everything CI should enforce (see docs/architecture/09_verification.md section 7)".
  - Precedent: commit `aaa8cb1` added the `modmatrix` target to `Makefile` and its §7 row in `09_verification.md` together.
- **Evidence:** at this head §7 lists `lint`, `links`, `wavedrom-check`, `matrix`, `modmatrix` and `stale`, but not `params`. The PR adds `params` to `check` (`git diff 60152f3..663d50d -- Makefile`). The only mention of the new gate is in the integrator guide (`docs/guides/integrator.md:103-105`).
- **Impact:** a reader of the verification plan cannot learn that the parameter inventory is enforced, or what it asserts. The document that the Makefile calls the list of CI-enforced gates is now incomplete.
- **Required outcome:** add a §7 row for `params` → `scripts/check-integrator-params.py`. It should say that the guide §2 table and the diagram 21 `integration-parameters` group each equal the top's overridable parameter set, with no missing, extra or duplicate names, and that the check fails on an empty or unparseable input. Optionally, also mention it in the `make check` row of `docs/guides/hdl-engineer.md:218`.
- **Verification:** read §7 against the `check:` prerequisites in `Makefile:13`; `make check` stays at rc 0.

### Suggestions (non-blocking)

- **S1 (Tests, Docs; pre-existing, follow-up):** make the `slug()` in `scripts/check-links.py:22-26` produce one hyphen per space, as GitHub does. That fixes the whole class of problem behind F1. It would also flag 4 links on main that are already dead on GitHub:
  - `02_interfaces.md` → `#6-class-d-level-status-dictionary`
  - `05_acmp_engine.md` → `#6bis-talker-side-stateless-responder`
  - two links from `05_acmp_engine.md` → `02_interfaces.md#42-maap-address-allocation`

  Evidence: `receipts/slug-gap-scan-head.txt`, `receipts/github-anchors-preexisting.txt`. This is outside the #99 scope, so it does not count against this PR.
- **S2 (Robustness):** the module docstring (`scripts/check-integrator-params.py:8`) says "only visible text in its inventory group counts". But `diagram_parameters` (`:80-88`) also counts `<text display="none">`. Probe `OBS-diagram-hidden-text-counts` hid a name the diagram was missing and the checker returned rc=0 (`receipts/checker-probes.txt`). Either skip `display="none"` and `visibility="hidden"` elements, or narrow the docstring. Separately, guide §2 says the table is "in declaration order" (`integrator.md:51`). That is true at this head (`receipts/json-top-params.txt`), but the checker compares sets and does not enforce order.
- **S3 (Docs):** the `DESC_NAME_ENTRIES_P` row (`integrator.md:83`) replaced the old "up to 1024" with "within the store's supported limits". That limit is enforced only in `hdl/aecp/KL_aecp_desc_store.sv:248-249` (`1..1024`), and the row does not link there. Linking the store would let an integrator find the bound without restating the value. An out-of-range value already stops elaboration with `$error`, so nothing can fail silently.
- **S4 (Docs):** the new diagram 21 paragraph (`docs/diagrams/README.md:60-70`) sits between the generic render command and the general "Check for overlapping text…" checklist (`:72`). That checklist now reads as if it applies only to diagram 21. Move the paragraph after the checklist.

## Lens evidence

### Conformance

- **Complete inventory:** there are 24 overridable parameters, confirmed three independent ways:
  - The checker's header parser.
  - An elaborated AST dump from the pinned simulator, listing the top's parameters that can be overridden (`GPARAM` vars, `receipts/json-top-params.txt`): the same 24, in the guide's row order.
  - A command-line override probe (`receipts/override-probe.txt`): all 24 names are accepted with rc=0 and no warnings. A bogus name and a derived localparam (`TMR_AW_C`) are both rejected with "not found in the design".
- **Guide §2:** the table lists exactly those 24 (`integrator.md:66-89`), including the five named in the issue plus `NVM_RS_TMO_CYC_P`. The pre-change guide from main `60152f3` fails the checker with exactly 6 missing names (`receipts/prechange-inputs.txt`).
- **Owners:**
  - Every F01.5 P-ID cited exists in `01_overview.md:146-178`.
  - Every F08.1 T-ID cited exists in `08_timing.md:28,29,43`.
  - The F08.2 and F10.2 anchors and all linked RTL and generator files exist.
  - The RTL binding descriptions match: `DESC_MEM_TMO_CYC_P` → the listener handshake (`protocol_processor_top.sv:1818`) and the AECP engine (`:3334`); `N_*` → the engine and dyn_state (`:3337-3339`); `REG_TL`/`LOCK` → notify (`:3513-3514`).
  - Open gap: the five §3.3.1/§3.3.2 anchors are dead on GitHub (F1).
- **No copied defaults:** there are no default values in guide §2 or in the diagram. A search of `integrator.md` for the old values finds none; they were only in the removed table. The diagram's "default 100 MHz" and "default 0x2…" texts were removed.
- **Diagram 21:** the master's `integration-parameters` group carries the same 24 names (`21-integration-faces.svg:32-45`).

### RTL

- The `hdl/`, `tb/` and `syn/` tree ids at head equal those of main `60152f3`. `52659df` equals base `008edbbf` for the same trees (`receipts/rtl-unchanged.txt`).
- The top's parameter header is byte-identical between `008edbbf` and head (same sha256).
- The merge `9cfe2d3` changes only the seven PR files against main, and main's own `integrator.md` edits (§4.1 guard text, SRP status rows, GSI note) are preserved.
- Lint of the full top with all 24 overrides is clean on the pinned simulator (Verilator 5.050 rev v5.050, identity checked) (`receipts/override-probe.txt`).

### Robustness

The checker was probed on scratch copies, 29 cases with the unmodified checker (`scripts/probe_param_checker.py`, `receipts/checker-probes.txt`): 28 assigned controls plus 1 observational case.

- **Baseline:** rc 0.
- **Top parameter controls, each rc 1 with the named diagnostic:**
  - removed top parameter
  - added top parameter
  - untyped and multi-name added parameters
  - rename
  - parameter demoted to localparam
  - empty top inventory
  - top missing the module header
  - unterminated header
  - unparseable declaration
  - missing file
- **Guide controls, each rc 1:** missing row, extra row, duplicate row, empty inventory, missing section, a row hidden in an HTML comment, a row hidden in a fenced block, and a name mentioned only outside §2.
- **Diagram controls, each rc 1:** missing entry, extra entry, duplicate entry, empty group, no group, two groups, malformed XML, and a name present only outside the group.
- **Also:**
  - A parameter-like name in a comment is correctly ignored (rc 0).
  - No probe produced a traceback.
  - The one observational gap is S2.

### Tests

- The checker is derived, not copied: `scripts/check-integrator-params.py` contains no list of parameter names. It parses the header with comments and strings masked and counts only `parameter` declarations.
- `663d50d` changes only function docstrings. The AST is identical to `52659df` apart from those, and all four public functions are annotated and documented (`receipts/checker-docstring-ast.txt`).
- The `.github/workflows/hdl.yml` diff against main is one renamed step and one added `python3 scripts/check-integrator-params.py` line. Nothing else changed.
- `Makefile` adds a `params` target and wires it into `check`.
- **Local gates at head** (`receipts/head-gates.txt`, `receipts/make-check.txt`), all rc 0:
  - `check-integrator-params`: top 24, guide 24, diagram 24
  - `check-links`: 916 links
  - `check-matrix`
  - `make params`
  - `make stale`
  - `gen_matrix --check`
  - `render-wavedrom --check`
  - full `make check`
- **Hosted runs at the exact head:**
  - docs-gates `success` on both the push context and the PR merge-ref context. Both logs show `parameters: top 24, guide 24, diagram 24, OK` (`receipts/hosted-docs-gates-log-excerpt.txt`).
  - portability `success` on both.
  - suites were still `in_progress` on both at 04:55 UTC (`receipts/hosted-check-runs-final.txt`).
- Open gap: 09 §7 does not document the new gate (F2).

### Docs

- Diagram 21: the committed PNG is byte-identical (sha256 `99b9de25…`) to a fresh render of the master with the documented command, `rsvg-convert -w 1905` (`receipts/png-rerender-diff.txt`). A visual inspection of the render found no overlap or clipping, and the inventory panel is legible.
- The `docs/diagrams/README.md` renderer note is accurate.
- The guide's banner and §2 prose follow the single-source rule and state the owner split: F01.5 for architectural values, F08.1 for timing, and the RTL for implementation-only settings.
- Open gaps: F1 and F2. Suggestions S3 and S4.

### Parent consumer (508 branch)

This review did not execute the parent consumer; its banks were not permitted. The public evidence records all 11 parent gates at rc 0 on local parent commit `ce65f96b8aee17dc589ca253188801da9db9ceef`, whose only changed path is the `protocol-processor` gitlink `663d50d6`. That includes 371 integration checks and a py-idiom ratchet of 0 undocumented public functions after the docstring commit, down from an initial refusal of 4. See `kebag-logic/milan-fpga@3f96319…/review-evidence/pp99-r1/author/{validation-summary,parent-audit}.json` and `logs/parent-*.log`.

`ce65f96` is committed locally only and cannot be fetched publicly. This review verified the evidence, not the execution.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue #99 body plus decision/assignment comments; `integrator.md` §2; `01_overview.md` F01.5; `08_timing.md` F08.1/F08.2; `07_memory_maps.md` §3.3.1/§3.3.2; `10_srp_engine.md` F10.2; top header `protocol_processor_top.sv:71-177` and its bindings; GitHub-rendered anchors; AST parameter list; override probe | R288-1 | 663d50d65ff49c33b153107b2f79d6f3c5725799 |
| RTL | CLEAN | `hdl`/`tb`/`syn` tree ids against main and base; parameter-header sha256 at base and head; merge `9cfe2d3` file set; pinned-simulator lint with 24 overrides | R288-1 | 663d50d65ff49c33b153107b2f79d6f3c5725799 |
| Robustness | CLEAN (S2 only) | `scripts/check-integrator-params.py` (all functions); 29 fault-injection probes; malformed, missing and ambiguous inputs | R288-1 | 663d50d65ff49c33b153107b2f79d6f3c5725799 |
| Tests | UNCLEAN (F2) | checker derivation; docstring-only AST proof; `hdl.yml` diff; `Makefile` diff; local gates and `make check`; hosted docs-gates/portability logs and status; `09_verification.md` §7 | R288-1 | 663d50d65ff49c33b153107b2f79d6f3c5725799 |
| Docs | UNCLEAN (F1, F2) | `integrator.md` (banner, §2, trailing note); `docs/diagrams/README.md`; `21-integration-faces.svg`/`.png` (rerender plus visual inspection); `09_verification.md` §7; `hdl-engineer.md` §8 | R288-1 | 663d50d65ff49c33b153107b2f79d6f3c5725799 |

## Real limits

- Not run by this review, because they were not permitted:
  - the full suite bank, `lint_hdl.sh` over all modules, Yosys/sv2v portability, and the nvm_port figure gate;
  - the parent consumer gates;
  - hosted re-runs.
- Their results come from public evidence and hosted status only.
- The GitHub anchor check reflects GitHub's rendering at review time, fetched read-only for the exact head.
- Probes ran on copies under the scratch directory. Two byproducts of the local gates in the clone were removed: the ignored `.venv-wavedrom/` bootstrap and a `scripts/__pycache__`. The final state of the clone: HEAD and tree exact, detached, `git status --ignored` empty, index tree equal to HEAD's tree, and all 247 tracked blobs and modes re-hashed with 0 mismatches (`receipts/restore-verification.txt`). This processor repository has no gitlinks and no `.gitmodules`, so there were no submodule pins to verify.
- The round-1 head announced earlier on the issue (`383a89a`) has the same tree as the published `52659df`; only the commit metadata differs.

## Pending manager duties

- Hosted `suites` jobs at the exact head (push run 36095706256 and PR run 36095709787) were still in progress when this review ended. Hosted and act acceptance stay with the manager.
- The final current-dev candidate build at the merge turn: source base `008edbbf…`, live dev `c533b4818df8b3f581df76aa0d1c6d5f55d20449`.
- Parent consumer adoption of the processor gitlink on `508-pp-pin-adopt`: `ce65f96` is local-only.
- Physical calibration NOT RUN. Field skips are not hardware proof.
- Re-review after F1 and F2 are addressed.

R288-1 FINISHED
