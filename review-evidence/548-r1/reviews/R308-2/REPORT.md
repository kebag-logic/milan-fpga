[R308] POSITIVE - exact head 8544472a19a4b4d3853d64b15dea22f999372a32

# R308-2: internal independent delta review of issue #548 / PR #556

- Exact head: `8544472a19a4b4d3853d64b15dea22f999372a32`, tree `b7a11e8d2ac0d88826925877180806ee145208d8`.
- Parent: `e41703b2948ef53e5cb0dd01a1e13c5632637615`, the R308-1 head. Source base: `573f0052a0e4412e81f0845438fcec2086ce5d55`.
- Role: internal reviewer. I worked in a cleared context from my own detached clone. The round-2 executor is [A285].
- Scope authority:
  - Issue #548 body, frozen acceptance 1-3.
  - Manager decision issuecomment-5821224656: STRUCTURAL ZERO, the count is not restored, scope items 1-6.
  - Round-2 assignment issuecomment-5822084957, items 1-3: correct `milan_csr.sv:761-763` and about `:2395-2399`, re-run the tree-wide search, prove comment-free RTL identity with `573f0052`.
- Delta under review: one commit, `8544472a` "Correct CTLR_DIAG structural-zero comments". It touches only `hdl/common/csr/milan_csr.sv`, +10/-8, and every added or removed line is a `//!` comment. The full base-to-head range still touches exactly 5 files. No gitlink changed at any of `573f0052`, `e41703b2` or `8544472a`.

## Verdict summary

R308-1-F1 is closed. Both remaining comment blocks now carry the STRUCTURAL ZERO verdict:
- the address-table entry at `milan_csr.sv:761-765`;
- the read-mux arm at `milan_csr.sv:2397-2401`.

Each block says the word reads 0 because the local counter source was deleted. Each also says the processor owns the Milan 5.4.5.3 monitor but exports no replacement count, the address is kept for the ABI, and zero is no measurement. That matches the register-map legend at `docs/reference/REGISTER_MAP.md:101`: "The source of this word is deleted and has no replacement ... Never read it as a measurement". It also matches the port comment at `milan_csr.sv:309-312` and the row and paragraph at `REGISTER_MAP.md:1244` and `:1248-1257`. The 0x6F8/0x6FC reserved-word note is preserved at `:766-767`.

All 137 tracked RTL files are comment-free identical to `573f0052`, and to `e41703b2`. Two in-memory functional controls are detected. The tree-wide search outside `docs/history` finds no statement that 0x6F4 or `CTLR_DIAG` is live.

The pinned test still passes at this head, 147 checks with 0 failures. A nonzero mutant fails it alone. No MINOR, MAJOR or BLOCKER finding is open. Every lens is covered clean at this head.

## Prior public review findings: resolution at this head

| ID | Severity | Status at 8544472a | Evidence |
|---|---|---|---|
| R308-1-F1: CSR decode table and read mux still document `CTLR_DIAG` as a live count | MINOR (Conformance, RTL, Docs) | **RESOLVED** | See "F1 closure check" below; `receipts/search_ctlr_diag.txt`; `receipts/rtl_identity.txt` |
| R308-1-S1: a zero-expected `axi_read` cannot tell a zero from a timed-out read | SUGGESTION (Tests, Robustness) | **RETAINED** as SUGGESTION | `tb/verilator/milan_dp/sim_nxn.cpp:612-626` is unchanged. R308-1 mutant m2 showed the AXI path delivers `live_mux` data at that read point. SUGGESTION does not affect coverage |
| R308-1-S2: the 0x6F4 row drops the "Was: ..." field layout that sibling STRUCTURAL ZERO rows keep | SUGGESTION (Docs) | **RETAINED** as SUGGESTION | `docs/reference/REGISTER_MAP.md:1244` is unchanged |
| R309-1-F1 | MAJOR | The manager's assignment (issuecomment-5822084957) records it as the same finding as R308-1-F1. I did not read the other reviewer's report before writing this verdict. Its closure is established by the same evidence, but final disposition belongs to that reviewer | as for R308-1-F1 |

R308-1 also recorded an out-of-scope observation, which is still present and is not a finding against this PR. `hdl/common/csr/milan_csr.sv:758` still labels `A_ACMPL_DBG` (0x6E8) "RO live", while `REGISTER_MAP.md:1241` calls that word STRUCTURAL ZERO. A public Issue search for `ACMPL_DBG` returned no Issue. It is listed under pending manager duties.

## F1 closure check (against the R308-1 required outcome)

- **Both blocks state STRUCTURAL ZERO, and neither claims a live, wrapping or climbing count.**
  - `:761-765` now reads: "CTLR_DIAG (RO 0x6F4): STRUCTURAL ZERO (#548). Reads 0 because the local counter source was deleted. The processor owns the departing-controller monitor (Milan 5.4.5.3) but exports no replacement count. The address is kept for the ABI. Zero is no measurement."
  - `:2397-2401` carries the same five lines.
  - The removed lines "RO live ... All three wrap." and "All three climb together ... a climbing eviction count" are gone (`git diff e41703b2 8544472a`).
- **The reserved-word note is intact.** `:766-767`, "0x6F8 and 0x6FC are the LAST free words of this group — reserved ...", is byte-identical to base.
- **No functional RTL change.** See `receipts/rtl_identity.txt` and the RTL lens below.
- **The claims in the new text are true at gitlink `09f9bf38`.**
  - `protocol-processor/hdl/aecp/KL_aecp_notify.sv` and `KL_aecp_ca_originator.sv` exist.
  - `protocol-processor/hdl/top/protocol_processor_top.sv` has no output port carrying a controller probe, reply or eviction count; the only match for the search terms is `maap_state_o`.
  - The parent tie is `hdl/milan/milan_datapath.sv:3206` `assign aecp_ctlr_diag = 32'd0;`, and it reaches the arm through `.i_ctlr_diag (aecp_ctlr_diag)` at `:2535`.
- **The sweep is clean.** `receipts/search_ctlr_diag.txt` shows `git grep -n -i -I -E "ctlr_diag|0x6f4|h6f4|6F4\b" 8544472a -- . ":!docs/history"`. Every hit is one of:
  - STRUCTURAL ZERO text: `117_GPTP_SILICON_EVIDENCE.md:471-474,524`, `REGISTER_MAP.md:188,1244,1248-1257`, `milan_csr.sv:309,761,2397`, `milan_datapath.sv:1500`;
  - a declaration or wiring line with no claim: `milan_csr.sv:313,768,2402`, `milan_datapath.sv:1503,2535,3206`;
  - the pinning test: `sim_nxn.cpp:1596-1597`.
- **The broader sweep is also clean.** A second search looked outside `docs/history` for the deleted field vocabulary: "departing-controller", "probes sent", "replies seen", "eviction count", "controllers shed", "1780" (0x6F4 in decimal) and "6f4" without a word boundary. It hit README, roadmap, FR/NFR, compliance matrix, testing and `tb` README lines. Those describe the processor's monitor behaviour and never a CSR count. The other hits are unrelated hash substrings in `scripts/gen_toc_shapes.json` and `syn/yosys/rom_digests.tsv`.
- **The initialised submodules carry no `ctlr_diag`/`0x6f4` reference.** `docs/history` is untouched and still has one frozen mention, in `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md`.
- The author's published search (`review-evidence/548-r1/author-r2/tree-search.log` at `29dce329`) lists the same live hits as my own search.

## Findings

No new finding at this head. No MINOR, MAJOR or BLOCKER is open. The two retained items above are SUGGESTIONs.

## Lens results (artifact evidence at `8544472a`)

```text
[R308] PASS Conformance — hdl/common/csr/milan_csr.sv:309-313,761-768,2397-2402; docs/reference/REGISTER_MAP.md:101,188,1244,1248-1257; docs/findings/117_GPTP_SILICON_EVIDENCE.md:468-474,524; receipts/search_ctlr_diag.txt — acceptance 2 (RTL, REGISTER_MAP and every current page agree) and manager scope items 1-6, checked against the #548 decision and the page legend; R308-1-F1 closed
[R308] PASS RTL — receipts/rtl_identity.txt (137/137 tracked RTL files comment-free identical to 573f0052 and to e41703b2; nonzero-tie and retargeted-mux controls detected); hdl/milan/milan_datapath.sv:1500-1503,2535,3206; protocol-processor/hdl/top/protocol_processor_top.sv at 09f9bf38 — comment-only delta, the tie and read arm unchanged, the new comment text true against the processor's exports
[R308] PASS Robustness — receipts/rtl_identity.txt; hdl/milan/milan_datapath.sv:3206; hdl/common/csr/milan_csr.sv:2402 — the zero is an unconditional constant with no reset, configuration, backpressure or traffic dependence; the comment-only delta cannot change any such path (R308-1 Robustness evidence re-confirmed by identity at this head)
[R308] PASS Tests — tb/verilator/milan_dp/sim_nxn.cpp:1594-1597 (unchanged since e41703b2); receipts/notify_zero_probe.txt, notify_run_head.log (147 checks, 0 failures, CTLR_DIAG = 0x0 after probe 35791 ms, retry 36041 ms, DEREGISTER 36292 ms), notify_run_mutant.log (32'h01001001 tie: 147 checks, exactly 1 failure, this check, got=0x1001001) — the pin still fails for the defect it claims to detect at this head
[R308] PASS Docs — hdl/common/csr/milan_csr.sv:761-767,2397-2401 against REGISTER_MAP.md:101 legend; receipts/gates.txt (docs_check both inventory modes, check_doc_style, check_doc_paths, gen_toc --check, check_em_dash --base 573f0052, git diff --check range and worktree: all rc 0); PR #556 body — in-source documentation now agrees with the register map; PR body accurately describes round 2 and carries "Closes #548"
```

What was checked under each lens:

### Conformance

- Acceptance 1: the decision is recorded and followed. The count is not restored.
- Acceptance 2: the three `milan_csr.sv` comment sites, both `milan_datapath.sv` sites, the register-map row, paragraph and TOC gloss, and the #117 evidence page now say the same thing. The word is STRUCTURAL ZERO, the monitor lives in the processor, and zero is not a measurement.
- Round-2 assignment items:
  - Item 1 is met; see "F1 closure check" above.
  - Item 2: my own search agrees with the author's.
  - Item 3: my own identity script agrees with the author's.
- Acceptance 3 is split:
  - Local gates: see the Docs lens and `receipts/gates.txt`.
  - Hosted evidence: every check run at this exact head completed. All succeeded except `Physical gPTP (nightly and manual)`, which was skipped (`receipts/hosted_checks.tsv`, 22 runs, `head_sha` equal to the exact head).
  - Hosted acceptance itself is the manager's.
- Manager scope item 6 holds. `sw/builder/test_builder.py` and `docs/history/` are untouched over the full range (`git diff --stat 573f0052..8544472a` lists only 5 files).

### RTL

- `rtl_comment_free_identity.py` works as follows:
  - it strips `//` and `/* */` comments, string-aware, and collapses whitespace;
  - it compares every tracked `*.sv/*.svh/*.v/*.vh` blob at both commits;
  - the file sets are equal, and 137 of 137 are identical, both base to head and R308-1 head to head.
- Controls:
  - Changing the tie to `32'd1` is detected.
  - Retargeting the `A_CTLR_DIAG` arm to `i_i2spb_dbg` is detected.
- Static RTL gates at head: `check_sv_idiom.py` rc 0 and `check_rtl_source_lists.py` rc 0 (`receipts/gates.txt`).
- The gitlinks `external efeb541a`, `gptp-processor e5dcea6e`, `protocol-processor 09f9bf38` and `third_party/verilog-axis 48ff7a7e` are unchanged across all three commits.

### Robustness

- No functional path changed (RTL identity).
- The retained R308-1 Robustness evidence depends only on the functional RTL and the test source. Both are identical at this head, and the re-run leg reproduces it.

### Tests

- The test source is unchanged since `e41703b2`. I still rebuilt the timed notification leg (`obj_notify`) at this exact head with the pinned simulator. It is Verilator 5.050 (`--version` "Verilator 5.050 2026-07-01 rev v5.050"; wrapper sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`).
- The build used the Makefile's own recipe, extracted from `make -n` with continuation lines joined (`receipts/notify_recipe_line.txt`).
- Clean run: rc 0, 147 checks, 0 failures.
- Mutant run:
  - A scratch copy of `milan_datapath.sv` differs only at `:3206` (`receipts/notify_mutant_source.diff`).
  - Its build line differs from the head line only by that source path and the output directory (`receipts/notify_head_vs_mutant_recipe.diff`, empty after normalisation).
  - Result: rc 1, 147 checks, exactly 1 failure, which is the new CTLR_DIAG check.
- `check_cpp_idiom.py` rc 0.

### Docs

- The new in-source text uses the page's own verdict wording. Documentation gates were re-run at head (`receipts/gates.txt`):
  - `docs_check.py` in Git inventory mode (165 md files, 858 scrubbed text files, 0 findings) and in no-Git mode: rc 0.
  - `check_doc_style.py` and `check_doc_paths.py`: rc 0.
  - `gen_toc.py --check` and `check_em_dash.py --base 573f0052`: rc 2 on the host, which lacks the pinned renderer. Both return rc 0 in a disposable scratch environment installed with `--require-hashes` from `tools/markdown/requirements.txt`. The em-dash gate reports "0 finding(s) over 20 added line(s) in 2 changed Markdown page(s)".
  - `git diff --check`, for the range and the worktree: rc 0.
- The pre-existing em dash in the preserved reserved-word note at `milan_csr.sv:766` is unchanged context, not an added line.
- The PR body's round-2 section matches the commit.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #548 body, decision 5821224656, round-2 assignment 5822084957; milan_csr.sv:309-313,761-768,2397-2402; milan_datapath.sv:1500-1503,2535,3206; REGISTER_MAP.md:101,188,1244,1248-1257; 117_GPTP_SILICON_EVIDENCE.md:468-474,524; processor `KL_aecp_notify.sv`, `KL_aecp_ca_originator.sv`, `protocol_processor_top.sv` at 09f9bf38; receipts/search_ctlr_diag.txt; receipts/hosted_checks.tsv | R308-2 | 8544472a19a4b4d3853d64b15dea22f999372a32 |
| RTL | CLEAN | receipts/rtl_identity.txt (137 files, two controls); milan_csr.sv and milan_datapath.sv comment sites and tie/arm; gitlinks at 573f0052, e41703b2, 8544472a; receipts/gates.txt (sv idiom, source lists) | R308-2 | 8544472a19a4b4d3853d64b15dea22f999372a32 |
| Robustness | CLEAN | milan_datapath.sv:3206; milan_csr.sv:2402; receipts/rtl_identity.txt; receipts/notify_run_head.log:137-148 | R308-2 | 8544472a19a4b4d3853d64b15dea22f999372a32 |
| Tests | CLEAN | sim_nxn.cpp:612-626,1594-1597; receipts/notify_zero_probe.txt, notify_run_head.log, notify_run_mutant.log, notify_mutant_source.diff, notify_head_vs_mutant_recipe.diff | R308-2 | 8544472a19a4b4d3853d64b15dea22f999372a32 |
| Docs | CLEAN | milan_csr.sv in-source docs; REGISTER_MAP.md; 117_GPTP_SILICON_EVIDENCE.md; PR #556 body; receipts/gates.txt | R308-2 | 8544472a19a4b4d3853d64b15dea22f999372a32 |

This ledger covers the exact head `8544472a`. A later commit that touches any artifact in a lens's scope un-covers that lens. The current-dev candidate merge result is a different commit, and it needs its own validation by the manager.

## Real limits

- **No hardware proof.** Physical calibration and hardware were NOT RUN. The hosted physical gPTP context was skipped, and field skips are not hardware proof. The #117 page was judged as documentation only.
- **Only one focused leg was run.** I did not run the full parent, PP, gPTP, Yosys or builder banks, the default `make -C tb/verilator/milan_dp` sweep, `xvlog_gate.py --check`, `lint_rtl.py --check`, or the act/hosted replicas; the brief does not allow them. Only the `obj_notify` leg was built and run, at head and under one mutant. The other two R308-1 mutants (CSR read-mux MSB, tie = 1) were not re-run, because the functional RTL and the test are identical to the round where they ran.
- **No manager bank receipts were found.** The public evidence tree at `29dce329` (`review-evidence/548-r1`) holds the author packets and the round-1 review packets. I found no separate manager bank receipts there, and none in the issue or PR comments. This verdict does not rely on the manager's bank results.
- **Other reviewer's report not read.** I read neither the R309-1 report nor its comment body before writing this verdict. R309-1-F1 is known only through the manager's assignment text.
- **A first probe script failed on scratch-tree setup.** The first attempt to build from separate scratch clones was declined by the session's permission policy. The leg was therefore built from the review clone itself:
  - generated hex prerequisites were removed on exit;
  - the mutant used a scratch source copy substituted on the command line, so no tracked file was edited;
  - two early script attempts failed on recipe parsing before any model was built, and the final run is the one recorded.
- **Clone hygiene is verified** (`receipts/restore_verify.txt`):
  - HEAD and tree are exact;
  - `status --porcelain --ignored --untracked-files=all` is empty;
  - the index equals the HEAD tree (mode, blob and path);
  - the worktree blob hashes of all regular tracked files equal the HEAD tree;
  - the changed files' modes are `100644`;
  - the gitlinks match, and the three initialised submodules are clean at their gitlinks. `external` is uninitialised.
  - Interpreter caches and a generated `gen_divergent/` directory created by this session's runs were removed before that check.
- **Host paths redacted.** The pinned simulator path in `receipts/notify_recipe_line.txt` is redacted to `$PINNED_SIM`.

## Pending manager duties

- Exact-head hosted acceptance and the act replica.
- The final current-dev candidate: source base `573f0052`, live dev `ffcbd33d`. Build and validate the candidate merge result, then run post-merge containment.
- Obtain the external reviewer's delta verdict at this head. Merge requires two independent POSITIVE verdicts and a reviewer-accepted ledger at the merge head, plus explicit maintainer authorization.
- Decide whether to open a separate Issue for the stale `A_ACMPL_DBG` "RO live" comment at `hdl/common/csr/milan_csr.sv:758`. It is out of scope for #548, and no Issue was found.
- Optionally route the retained SUGGESTIONs R308-1-S1 and R308-1-S2.

R308-2 FINISHED
