[R225] POSITIVE - exact head 0d43ff25d38917e77bb5c3d2ddb6473013cea3ba

R225-1, cold independent internal review of kebag-logic/milan-fpga PR #507 / issue #440. Base: `b17580b91deb11f3441dfc5d7f9fafe539d929b8`. Candidate tree: `c0e67508d3b753c21a28a243d365c4c37ed86d43`.

All five lenses were applied. No BLOCKER, MAJOR or MINOR finding remains from this review. One optional test suggestion follows. This is a code-review verdict, not a declaration that execution or merge obligations are complete.

The public contract was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, REQUIREMENTS.md section 8 / REQ-VER-04, code-quality rule 12, [issue #440](https://github.com/kebag-logic/milan-fpga/issues/440), [decision 5771170243](https://github.com/kebag-logic/milan-fpga/issues/440#issuecomment-5771170243), the linked R86-9 report, and the PR's diff, single-commit history and public evidence. The decision explicitly selects space/tab fence suffixes and any of four literal type-1 closers, with ASCII case folding and no internal blank. It preserves global refusal and leaves container redesign to #437. These closing rules agree with the relevant [CommonMark 4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks) and [4.6](https://spec.commonmark.org/0.31.2/#html-blocks) boundaries and the GFM observations examined here. No conflicting normative requirement was found within this scope.

[R225] PASS Conformance - `scripts/gen_toc.py:473`, `scripts/gen_toc.py:484`, `scripts/gen_toc.py:503`, `corpus-base.json`, `corpus-head.json`, `e2e-head.json` - the settled closer rules and all four issue acceptance criteria hold. Fence matching retains delimiter identity, minimum length and indentation constraints while narrowing trailing characters to space/tab. Any literal `pre`, `script`, `style` or `textarea` closer ends a type-1 block, on its opening line or a later line, including inside longer text. ASCII capitals work; U+017F, U+0131 and U+0130 do not acquire ASCII meaning.

The identical 205 public synthetic fixtures were independently replayed against both exact source revisions. Their archived HTML responses were fetched and counted independently; they remain attributed renderer evidence. Twenty-five fresh `gh api markdown` GFM responses were also obtained, with exact requests and responses retained. All 25 agree with the normalized candidate helper.

| Population / reader | Agree | Escape | Withhold | Rows carrying refused characters |
|---|---:|---:|---:|---:|
| Base raw helper | 90 | 62 | 53 | 108 |
| Head raw helper | 200 | 0 | 5 | 108 |
| Base after actual Path.read_text | 93 | 60 | 52 | 100 |
| Head after actual Path.read_text | 205 | 0 | 0 | 100 |

These reproduce the published measurements. The 116 raw and 112 normalized heading-count changes occur in the closer/CR population. The 100 normalized refused rows are not claimed as accepted shipped pages. The reconstructed corpus explicitly includes the historical 25 non-CR fence characters, 27 non-CR type-1 character/blank cases, CR, both fence markers, both type-1 call sites, all opener/closer pairs, ASCII capitals and Unicode lookalikes. The original historical instrument was unavailable; this is a replay of its published population reconstruction, not a claim to have rerun its complete historical campaigns.

[R225] PASS RTL - `candidate.diff`, `summary.json:changed_paths` and `final-integrity.json` - the six-file change contains five documentation-tool Python files and docs/DOC_GENERATION.md. No HDL, hardware interface, clock/reset/CDC logic, constraint, workflow, build source list, version or gitlink changes. The software architecture preserves gen_toc as the parser/provenance owner; the new module supplies fixtures and expectations. No hardware or exhaustive RTL validation was performed by this reviewer.

[R225] PASS Robustness - `scripts/gen_toc.py:292`, `scripts/gen_toc.py:332`, `scripts/check_em_dash.py:210`, `scripts/check_em_dash.py:267`, `boundaries-head.json`, `reader-cli.json`, `e2e-head.json` - 3,614 independent boundary probes pass. They cover both fence markers, shorter/equal/longer runs, allowed and malformed suffixes, indentation, headings at EOF without a terminal LF, incomplete blocks, all four HTML names, both closer positions, embedded closers, invalid names, reset into a subsequent block and fence/comment/type-6 precedence. The same probes expose 368 mismatches at the base.

Seventeen independent real-Git page comparisons pass at the head. Hidden labels behind internal blanks, Unicode lookalikes and malformed longer fence suffixes are rejected; legitimate ASCII, cross-name, tab and longer-fence labels are exempt. FF/NBSP cases retain named base refusal and no exemption. The Git text reader normalizes CR/CRLF in every relevant case. CR-only fence and HTML pages exempt the valid copied label while still reporting the heading that Git's LF-based diff considers newly added; that separate boundary remains unchanged. Eight actual generator CLI probes additionally confirm CR/CRLF normalization, unchanged named refusal, and failure to close on internal blank/CR.

The five raw withholdings are exactly `F-backtick-U000D`, `F-tilde-U000D`, `B-fence-crlf`, `B-fence-cr`, and `B-type1-cr`. All carry raw CR and disappear after reader normalization. Internal CR in `</pre` followed by CR then `>` remains an invalid closer after normalization.

Production AST comparison, excluding docstrings, confirms unchanged refusal, paragraph/container, ownership, generated-block, heading/anchor and gate judgment functions. The only changed gen_toc functions are the closer helper, its two callers and selftest; check_em_dash changes only selftest. On each of the base and head Markdown populations, both engines produce identical blocks, line kinds, headings, refusal, ownership and provenance records for all 163 pages. All headings and generated blocks remain unchanged between revisions; 105 pages retain generated provenance. This supports the unchanged-scope claim without claiming that #437's existing container limitations are repaired.

[R225] PASS Tests - `scripts/gen_toc_closer_cases.py:33`, `scripts/gen_toc_closer_cases.py:102`, `scripts/gen_toc.py:834`, `scripts/check_em_dash.py:945`, `controls-base.json`, `controls-head.json`, `mutations.json` - the existing 279 TOC arms remain, with only the two directly affected family/site-kind expectations updated. The new 404 I440 arms produce 683/683. Existing em-dash control functions are unchanged; 17 real-Git arms raise its total from 34 to 51. Source ownership and the 25-site guard remain active.

Ten independently constructed mutations of the issue's closer properties fail behavioral I440 arms: Python strip restoration, tab rejection, internal blanks, Unicode folding, case sensitivity, omission at either type-1 call site, line-start-only matching, dropping a closing name and matching only the opening name. These were run in disposable copies, with exact patches and outputs retained. Python-strip restoration remains masked by the unchanged refusal in the shipped em-dash tests, but fails 52 raw I440 arms. The other nine also fail shipped em-dash controls. This verifies sensitivity at both changed decisions instead of relying solely on source guards or author mutation claims.

[R225] SUGGESTION Tests, Robustness - `scripts/gen_toc.py:497`, `scripts/gen_toc_closer_cases.py:36`, `mutations/exact-fence-length/change.patch` - add a permanent valid longer-closing-fence control.

Requirement/evidence: CommonMark 4.5 accepts a closing run at least as long as the opener. The current implementation satisfies this, and independent boundary and real-Git probes pass. However, changing `>=` to `==` survives both permanent selftests (683/683 and 51/51).

Impact: a future regression in this unchanged length condition could escape those suites. This is optional hardening of an adjacent, unchanged condition, not a stronger acceptance criterion for #440 or a current parser defect.

Optional change and verification: add a positive case such as a three-backtick opener followed by five backticks and space/tab; require that arm to fail under the recorded length mutation. No fix is required for this verdict.

[R225] PASS Docs - `docs/DOC_GENERATION.md:29`, `scripts/gen_toc.py:292`, `scripts/gen_toc.py:473`, `scripts/gen_toc_guards.py:57`, public `author/MEASUREMENT.md`, and [review-start record](https://github.com/kebag-logic/milan-fpga/pull/507#issuecomment-5772565104) - authoritative prose accurately states the closer rules, ASCII limitation, reconstructed measurement, five raw CR withholdings, normalization at both readers, unchanged refusal/provenance and separate container scope. The expanded public evidence is sufficient to reproduce this review. Compressed issue-comment payloads were not decoded or used. The PR body's older draft/in-progress wording is superseded by its linked public readiness record; the actual PR was ready at the requested head when read.

Reviewer-owned ledger, covering round R225-1:

| Lens | Covering round | Head | Result |
|---|---|---|---|
| Conformance | R225-1 | 0d43ff25d38917e77bb5c3d2ddb6473013cea3ba | CLEAN |
| RTL | R225-1 | 0d43ff25d38917e77bb5c3d2ddb6473013cea3ba | CLEAN |
| Robustness | R225-1 | 0d43ff25d38917e77bb5c3d2ddb6473013cea3ba | CLEAN; optional suggestion only |
| Tests | R225-1 | 0d43ff25d38917e77bb5c3d2ddb6473013cea3ba | CLEAN; optional suggestion only |
| Docs | R225-1 | 0d43ff25d38917e77bb5c3d2ddb6473013cea3ba | CLEAN |

Independent local gate receipts are in `gates.json`: TOC selftest 683/683; sites 25; TOC check 105 lists; anchors 144; em-dash against the exact base zero findings over 32 added lines with 51/51 controls; docs_check zero findings across 163 Markdown files and 827 scrubbed text files; diff whitespace check passes.

Evidence limits: the local Python idiom scan returned setup refusal (exit 2), because both processor submodules are uninitialized. No local idiom PASS is claimed. All four submodule paths are empty directories with `-` status, including external and verilog-axis. No installation, initialization, full parent sweep, Docker/act, hardware, privileged action, product edit, product commit, push, public write, merge, subagent or collaboration with the author/other reviewer occurred. Git commits were created only inside disposable fixture repositories to exercise the authorized real-Git controls. Archived full-native, 43-command manager/builder and draft-replica results at this head are attributed manager evidence, not independently rerun results; see `public-evidence/manager/` and the [public archive](https://github.com/kebag-logic/milan-fpga/tree/ada8bf7b1cb74cc89e5a451bb2dcd659722ffa28/review-evidence/440-r1).

Pending execution/merge obligations, separate from this verdict: the review-start record says the all-four ready local replica and exhaustive hosted checks are pending. This reviewer did not poll or certify them. Exact-head required contexts, the independent external review, current-dev candidate validation, merge authorization and post-merge containment still belong to the completion process. No physical acceptance is claimed.

Final integrity: detached HEAD and tree remain the exact objects above. Git status, working-tree diff and staged diff are empty. All 851 tracked non-gitlink files match their index blob bytes and modes; all index entries match the initial capture. The four gitlinks and uninitialized directories are unchanged. Receipts: `initial-integrity.json`, `final-integrity.json`, `tracked-sha256.json`. Product files were never mutated, so no restoration was necessary.

Reproduction commands and receipt descriptions are in `RECEIPTS.md`; all paths named above are relative to this report's directory. Deliverables contain factual conclusions and reproducible evidence only.

R225-1 FINISHED
