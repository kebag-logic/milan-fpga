[R289] NEGATIVE - exact head 663d50d65ff49c33b153107b2f79d6f3c5725799

# R289-1 external independent review: processor issue #99 / PR #119

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Head under review: `663d50d65ff49c33b153107b2f79d6f3c5725799`, tree `21e0fddbbe927569b7e16f282088ea4fc1b7b7f1` (verified, `receipts/verify-clone.txt`)
- Source base named for the round: `008edbbf486598ae237414273d75e385cf0e1a56`. Main merged in: `60152f3ff068b81333326b5081b5303253ba7fe7`. The PR's own delta is `60152f3..663d50d`: 7 files. The wider `008edbbf..663d50d` diff also carries PRs #109 to #118 through merge `9cfe2d3`.
- Round scope: [A244] round-1 commit `52659df`, plus [A300]'s merge `9cfe2d3` and checker docstrings `663d50d`. Assignments: issue #99 comments 5810655949 and 5826543636. Decision: 5789750553 (complete inventory).
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs. All five were applied independently, each with its own evidence below.

## Verdict

NEGATIVE, on one open MINOR (Docs lens). Everything the issue's acceptance asks for holds at this head:

- The guide's section 2 lists all 24 overridable parameters of `protocol_processor_top`, in declaration order.
- Each row links to an owner that exists, and no row copies a default.
- Diagram 21's SVG master and its committed PNG carry the same 24 names.
- The checker derives the set from the RTL and fails on every control named in the assignment.
- The workflow change only adds the check and renames the step.
- There is no RTL change.
- The parent consumer at `ce65f96` pins this head, and every static gate I could run on it passed.

The one defect: the PR adds a `params` target to `make check`, but did not update the document that lists what `make check` runs.

## Findings

### F1: MINOR, lenses: Docs

`[R289] MINOR Docs - docs/architecture/09_verification.md:111-120 - make-check gate table omits the new params target`

- **Requirement/evidence:**
  - `Makefile:12-13` defines `check: lint wavedrom-check links matrix modmatrix params stale`. Its comment names the authority: "everything CI should enforce (see docs/architecture/09_verification.md section 7)".
  - `09_verification.md:111` says "`make check` is the CI gate, and runs today:". The table under it lists `lint`, `links`, `wavedrom-check`, `matrix`, `modmatrix` and `stale`. It has no `params` row, even though this PR added `params` to the target (`Makefile:13`, `Makefile:39-40`).
  - AGENTS.md section 6, Docs lens: "Changed contracts are reflected in authoritative docs." The earlier `modmatrix` gate was added to the same table, so there is precedent.
  - Confirmed at this head with `grep -n` (see the receipts list below) and by reading `09_verification.md` section 7.
- **Impact:** The verification document's gate list is now incomplete. This is the same kind of inventory drift that issue #99 exists to remove. A reader using section 7 as the list of documentation gates would not know that the parameter-inventory gate exists, or what it asserts.
- **Required outcome:** Section 7 of `09_verification.md` gets a row for `params` / `scripts/check-integrator-params.py`, stating what it asserts. That is: the guide section 2 table and diagram 21's `integration-parameters` group equal the overridable parameters of the `protocol_processor_top` header, with no duplicates and no empty inventory. Optional, not required: two secondary lists were already incomplete before this PR and could be updated too: `docs/guides/hdl-engineer.md:218` and `docs/README.md:154`.
- **Verification:** Reading `09_verification.md` section 7 shows the row. `make check` and the docs-gates commands still return 0 (`run-doc-gates.sh`).

### Suggestions (non-blocking; they do not affect any lens verdict)

- **S1 (Robustness, Tests): hidden text counts as "visible".** `scripts/check-integrator-params.py:8,81-88` says only *visible* text counts. In fact any `<text>` inside the group counts, including `display="none"` text. Probe `LIMIT-diagram-hidden-text` returns rc=0 after moving an entry into hidden text. Either say "text" rather than "visible text", or reject hidden, zero-size or transparent text in the group. This is not an acceptance control; ordinary edits are caught.
- **S2 (Tests): no committed self-test.** The checker's failure controls are proven only by out-of-tree probes: the author's published `author-r1/parameter-probes.log` and this review's `probe-checker.py`, 34 of 34 controls. A committed `--selftest` with planted fixtures, like the parent's `pp_srcs.py --selftest` or `docs_check.py`'s scrub self-test, would keep them proven in CI.
- **S3 (Docs, Tests): nothing checks the PNG against the SVG.** `docs/diagrams/README.md:60-65` makes the diagram 21 PNG an export of the SVG master. Nothing gates that freshness: `make stale` covers only `.drawio` sources. At this head the PNG is pixel-identical to a fresh render (`receipts/png-compare.txt`), and no page embeds the PNG. So the risk is only future drift.
- **S4 (Docs): new paragraph splits the editing rule.** In `docs/diagrams/README.md:60-70`, the new diagram 21 paragraph sits between "Editing rule for these five" and its continuation at line 72 ("Check for overlapping text ..."). That continuation now reads as if it applies only to diagram 21.
- **S5 (Docs, outside this issue's scope): a default is restated in section 9.** `docs/guides/integrator.md:355-356` still restates a default: "`NVM_RS_TMO_CYC_P` (default 20 ms of `CLK_HZ_P`)". The text predates the round (commits `daab6a53`/`7297a642`, both ancestors of `008edbbf`) and sits outside section 2. Guides are outside the architecture single-source rule (`docs/README.md` section 2 scope). Per AGENTS.md section 4, it should become a separate issue if wanted, not a change here.

## Prior public review findings

- **Prior rounds on PR #119:** none. At the time of this review the PR had only the two review-start comments (R288-1, R289-1) and no review objects. Checked through the PR comments and reviews APIs, headers only; no other reviewer's report was read.
- **Origin observation X2** (R223 on PR #96), which created issue #99: **resolved at this head.**
  - `N_AUDIO_UNIT_P`, `N_CLK_DOMAIN_P`, `N_CONTROL_P`, `REG_TL_TIMEOUT_MS_P` and `LOCK_TIMEOUT_MS_P` are now in the guide's section 2, at `docs/guides/integrator.md:68-70,86-87`.
  - They are also in diagram 21's inventory group, at `docs/diagrams/21-integration-faces.svg:34,43 (group 32-45)`.
  - `NVM_RS_TMO_CYC_P`, which was also missing, is added too.
  - The pre-change guide, both at `008edbbf` and at `60152f3`, fails the new check with exactly these six missing (`receipts/probe-default-path.txt`).

## Lens evidence

### Conformance: clean

- **Issue acceptance vs. the RTL.** The pinned simulator 5.050 (identity in `receipts/tool-identity.txt`) independently elaborated `protocol_processor_top` to JSON. It finds 24 `GPARAM` names (`receipts/elab-params.txt`). That list is identical, in order, to the checker's parse and to the guide's rows (`receipts/order-and-owners.txt`). The diagram set equals the top set.
- **"Links each to its owner without copying defaults":**
  - Every `P-` ID cited in section 2 exists in F01.5, for example `01_overview.md:146-170`.
  - Every `T-` ID cited exists in F08.1 (`08_timing.md:28,29,43`).
  - The 07 §3.3.1 and §3.3.2, F08.2 and F10.2 anchors resolve (`check-links.py`: 916 links OK).
  - None of the 24 rows contains a default literal (`receipts/order-and-owners.txt`).
  - The row descriptions match the RTL bindings:
    - `DESC_MEM_TMO_CYC_P` → listener `STRM_TIMEOUT_CYC_P` (`protocol_processor_top.sv:1818`) and AECP `MEM_TIMEOUT_CYC_P` (`:3334`).
    - `REG_TL_TIMEOUT_MS_P` / `LOCK_TIMEOUT_MS_P` → `KL_aecp_notify` (`:3513-3514`).
    - `N_AUDIO_UNIT_P` / `N_CLK_DOMAIN_P` / `N_CONTROL_P` → `KL_aecp_engine` (`:3337-3339`).
- **Diagram 21:** its defaults were removed ("default 100 MHz", "0x20000000", "0x20100000"), and its inventory group lists all 24 names (`21-integration-faces.svg:32-45`).
- **Assigned validation** (the donor gates as CI runs them, plus the enumeration check): all returned 0 at this head (`receipts/gates.txt`).

### RTL: clean

- `git diff 60152f3..663d50d -- hdl tb syn` is empty. So is `008edbbf..52659df` for the same paths.
- The `protocol_processor_top.sv` blob at head equals merged main's (`cb81d642...`).
- The parameter header (`module` through `) (`) has sha256 `08aec13a...` at the base, at main and at head.
- Merge `9cfe2d3` equals a clean replay of its parents: tree `44a83554...`, empty diff (`receipts/probe-merge-rtl.txt`).
- `663d50d` differs from `9cfe2d3` only in 4 function docstrings; the AST is identical otherwise (`receipts/docstring-ast.txt`).
- The documented derived localparams (`protocol_processor_top.sv:154-176`) are correctly excluded, and they match the guide's "derived localparams are internal" statement.

### Robustness: clean (S1 recorded as a suggestion)

`probe-checker.py` ran 34 fault controls plus 1 recorded limit on disposable copies. All 34 behave as expected (`receipts/probe-checker.txt`):

- **Top:** removed, added, added after the localparams, added as a list continuation, renamed, commented out; a block-comment decoy and string punctuation are ignored; duplicate, missing header, unterminated header, garbage declaration, empty inventory, missing file.
- **Guide:** missing, extra and duplicate rows; a row that is commented out, fenced, unticked, only in a later column, or placed outside section 2; empty table; missing section.
- **Diagram:** missing, extra and duplicate entries; an entry outside the group or inside an XML comment; no group or two groups; empty group; malformed XML.

No control produced a traceback. The default CI/make invocation on a disposable export also fails closed: rc 1 for the script and rc 2 for `make params` / `make check` (`receipts/probe-default-path.txt`). The diagram's `_P`-suffix extraction matches the house naming rule, which requires `_C`/`_P` params.

### Tests: clean (S2, S3 recorded as suggestions)

- The new gate can fail for each defect it claims to catch. This is shown by the probes above and by both pre-change guides and diagrams failing.
- The hosted exact-head push run `36095706256` completed successfully. Its jobs:
  - `docs-gates` executed the new step and printed `parameters: top 24, guide 24, diagram 24, OK`.
  - `suites` passed its lint and suites, matrix and nvm figures steps; the Verilator build step was skipped because the cache hit.
  - `portability` passed.
- The pull_request run `36095709787` had docs-gates and portability passing, and suites still in progress when recorded at 2026-09-25T04:57:51Z (`receipts/hosted-runs.txt`).
- **Parent consumer:** I cloned local parent commit `ce65f96` (branch 508-pp-pin-adopt; only the processor gitlink changed, to `663d50d`) into scratch, with its submodules initialized from local sources at the pinned gitlinks (`receipts/parent-gitlinks.txt`). Eight static gates returned 0: py-idiom, cpp-idiom, rtl-source-lists, pp_srcs `--check --selftest`, port-contracts, naming, test-evidence, docs_check (`receipts/parent-static-gates.txt`). The public initial log shows py-idiom refused the pre-docstring checker ("undocumented public function 4 > ratchet 0"). The final log and my rerun show it passing.

### Docs: UNCLEAN (F1)

Examined, all at this head:

- `docs/guides/integrator.md` sections 1 and 2 (lines 12-17 and 46-105)
- `docs/diagrams/21-integration-faces.svg` and `.png`: the rendered PNG was inspected, and it is pixel-identical to a fresh render at `-w 1905`, with 0 of 2,438,400 pixels differing. The pre-change render differs, as a control.
- `docs/diagrams/README.md:57-72`
- `docs/README.md` section 2 single-source rules
- `09_verification.md` section 7
- `hdl-engineer.md:218`
- the PR body and the issue comments

F1 is open.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #99 body + 5789750553 / 5810655949 / 5826543636; `docs/guides/integrator.md:46-105`; `21-integration-faces.svg:32-45`; F01.5 `01_overview.md:144-179`; F08.1 `08_timing.md:11-43`; elaborator GPARAM list; `receipts/order-and-owners.txt`, `gates.txt`, `elab-params.txt` | R289-1 | 663d50d65ff49c33b153107b2f79d6f3c5725799 |
| RTL | CLEAN | `hdl/top/protocol_processor_top.sv:71-177,1808-1819,3326-3345,3508-3514`; PR-own diff `60152f3..663d50d`; merge replay; `receipts/probe-merge-rtl.txt`, `docstring-ast.txt` | R289-1 | 663d50d65ff49c33b153107b2f79d6f3c5725799 |
| Robustness | CLEAN | `scripts/check-integrator-params.py:23-128`; 34 fault controls + 1 limit; default-path probe; `receipts/probe-checker.txt`, `probe-default-path.txt` | R289-1 | 663d50d65ff49c33b153107b2f79d6f3c5725799 |
| Tests | CLEAN | `.github/workflows/hdl.yml:17-24`; `Makefile:13,39-40`; hosted run 36095706256 jobs; parent `ce65f96` static gates; public evidence `review-evidence/pp99-r1` at kebag-logic/milan-fpga@3f963195; `receipts/hosted-runs.txt`, `parent-static-gates.txt` | R289-1 | 663d50d65ff49c33b153107b2f79d6f3c5725799 |
| Docs | UNCLEAN (F1) | `docs/guides/integrator.md`; `docs/diagrams/21-integration-faces.{svg,png}`; `docs/diagrams/README.md:57-72`; `docs/architecture/09_verification.md:109-120`; `docs/guides/hdl-engineer.md:218`; `receipts/png-compare.txt` | R289-1 | 663d50d65ff49c33b153107b2f79d6f3c5725799 |

## Real limits

- I did not run the full processor suite bank, lint, yosys portability, the nvm figures, or the parent's xvlog / pp_shadow builds; the scope excluded them. For those I rely on the public author evidence and the hosted exact-head push run.
- The parent `gen_toc.py --verify-anchors` gate did not run: its pinned renderer lock is not installed here, and installing it would be a shared install. The published author log reports rc=0.
- The parent consumer commit `ce65f96` is local only (not pushed). I read it from the parent lane and did not modify the lane. That lane's HEAD has since moved to `e7474464`, which this review did not assess.
- The pull_request hosted run's `suites` job was still in progress when recorded. The hosted and act acceptance belongs to the manager.
- Physical calibration was NOT RUN. Nothing here is hardware proof, and field skips are not hardware proof.
- This is source-head validation. The final current-dev candidate (source base `008edbbf`, live dev `c533b481`) is built by the manager at the merge turn, and I did not assess it.
- The gate run bootstrapped an ignored `.venv-wavedrom/` and a `scripts/__pycache__/` in the clone. I removed both. The clone was then re-verified: HEAD, tree, index modes and blobs, and the rehashed bytes of all 247 tracked files match, with no untracked or ignored files. The processor repo has no gitlinks; the parent gitlinks are recorded (`receipts/parent-gitlinks.txt`).

## Pending manager duties

- Route F1 to the executor, then re-review the corrected head.
- Hosted/act acceptance at the final head, including the in-progress pull_request run `36095709787`.
- Build and validate the final current-dev candidate at the merge turn.
- Publish the parent consumer commit, or otherwise make it public.
- Decide whether S1 to S5 become follow-up issues.
- The second independent positive review, and merge authorization.

## Receipts and scripts (paths relative to the packet; listed in MANIFEST.sha256)

- Scripts:
  - `run-doc-gates.sh`
  - `elab-params.sh`
  - `probe-checker.py`
  - `probe-default-path.sh`
  - `probe-merge-rtl.sh`
  - `png-compare.py`
  - `docstring-ast.py`
  - `parent-static-gates.sh`
  - `verify-clone.sh`
- Receipts:
  - `receipts/gates.txt`
  - `receipts/elab-params.txt`
  - `receipts/probe-checker.txt`
  - `receipts/probe-default-path.txt`
  - `receipts/probe-merge-rtl.txt`
  - `receipts/png-compare.txt`
  - `receipts/docstring-ast.txt`
  - `receipts/order-and-owners.txt`
  - `receipts/hosted-runs.txt`
  - `receipts/parent-static-gates.txt`
  - `receipts/parent-gitlinks.txt`
  - `receipts/verify-clone.txt`
  - `receipts/tool-identity.txt`

Local absolute paths in receipts are redacted to `$PACKET`, `$CLONE`, `$LANES`, `$PINNED` and `$HOME`.

R289-1 FINISHED
