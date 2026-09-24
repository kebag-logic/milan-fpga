[R309] NEGATIVE - exact head e41703b2948ef53e5cb0dd01a1e13c5632637615

# R309-1: external independent review of issue #548 / PR #556

- Role: [R309], external independent reviewer, round R309-1, cleared context.
- Exact head: `e41703b2948ef53e5cb0dd01a1e13c5632637615`, tree `4dd0f8cb28230a5a8d2e51e5e19ce25a0a24af23`.
- Diff under review: `573f0052a0e4412e81f0845438fcec2086ce5d55..e41703b2948ef53e5cb0dd01a1e13c5632637615`, one commit (`e41703b29 Document and pin CTLR_DIAG as a structural zero`), 5 files, +33/-19.
- Reconstructed from: AGENTS.md, CONTRIBUTING.md (sections 1, 3, 5, 6), docs/README.md; issue #548 body (acceptance 1-3), the manager decision (issue comment 5821224656: STRUCTURAL ZERO, count not restored, scope items 1-6), the executor's TAKEN and REVIEW READY comments; the register map verdict legend (`docs/reference/REGISTER_MAP.md:92-103`); the processor sources at gitlink `09f9bf38`; the diff; the public evidence packet `review-evidence/548-r1` at `ae967643`; my own executed probes (receipts below).

## Verdict

**NEGATIVE.** The register map, the #117 evidence page, the two edited RTL comment sites and the new test are correct and well evidenced. But acceptance 2 ("Make the RTL, REGISTER_MAP and any page that reads it agree") is not met: `hdl/common/csr/milan_csr.sv` still carries two comment blocks, in the file this PR edited, that describe 0x6F4 as a **live** word with a probe/reply/eviction field layout. That is the same disagreement the issue exists to remove. It is filed as R309-F1 (MAJOR) under Conformance, RTL and Docs. Robustness and Tests are clean.

## Findings

### R309-F1 - MAJOR - Conformance, RTL, Docs - `hdl/common/csr/milan_csr.sv:761-766` and `hdl/common/csr/milan_csr.sv:2395-2400` - the CSR address table and read-mux comments still document CTLR_DIAG as a live count

```text
[R309] MAJOR Conformance, RTL, Docs - hdl/common/csr/milan_csr.sv:761-766, :2395-2400 - CSR address/mux comments still document 0x6F4 as a live probe/reply/eviction count
```

- **Authority/evidence.** Issue #548 acceptance 2: "Make the RTL, REGISTER_MAP and any page that reads it agree". The manager decision classifies 0x6F4 as STRUCTURAL ZERO. At the exact head:
  - `milan_csr.sv:761-763`: `//! gh #59 departing-controller detection (Milan v1.2 §5.4.5.3). RO live,` / `//! one word: {evictions[31:24], CONTROLLER_AVAILABLE replies seen[23:12],` / `//! CONTROLLER_AVAILABLE probes sent[11:0]}. All three wrap.`, attached to `A_CTLR_DIAG = 'h6F4` at `:766`.
  - `milan_csr.sv:2395-2399`: `//! gh #59: probes sent / replies seen / controllers shed. All three climb together on a healthy bench (each probe is answered); a climbing eviction count with a static reply count is a controller that died without deregistering ...`, attached to the read decode `A_CTLR_DIAG: live_mux = i_ctlr_diag;` at `:2400`.
  - The PR rewrote the port comment at `milan_csr.sv:309-312` in the same file to say STRUCTURAL ZERO. So after this PR the file contradicts itself, and the two stale blocks sit at the address constant and the read decode, where a firmware or tools author who wires a new reader actually looks.
  - A full-tree search at the head (`git grep -i -E 'CTLR_DIAG|0x6F4|ctlr_diag|evict|probes sent|replies seen|controllers shed'`, excluding `docs/history` and the submodules) finds no other stale live-count reader. Every other hit is the corrected text, the tie, the port wiring or the new check.
  - The manager's scope item 2 pointed at "`milan_csr.sv` (about line 309)". It does not narrow the frozen acceptance, which says "the RTL".
- **Impact.** No functional effect: the RTL is comment-only identical (see RTL evidence). The documentation defect the issue targets survives in the RTL. The `//!` comments are the in-code register specification under the house style ("the port list IS the spec", CONTRIBUTING.md section 1). A reader of the CSR block is told the word is live and given a field layout and a diagnostic signature, which invites exactly the inference that #548 removed from the #117 page.
- **Required outcome.** Both comment blocks carry the STRUCTURAL ZERO verdict, consistent with `milan_csr.sv:309-312` and `REGISTER_MAP.md:1244-1257`. They must not describe live fields, wrap behaviour or a healthy-bench signature. Keep the reserved-word note for 0x6F8/0x6FC. The change stays comment-only.
- **Verification.** (a) The same full-tree search shows no current text describing 0x6F4 as live or giving it probe/reply/eviction fields. (b) `scripts/rtl_comment_free_equiv.py <repo> 573f0052a0e4412e81f0845438fcec2086ce5d55 <new head> hdl/common/csr/milan_csr.sv hdl/milan/milan_datapath.sv` still reports IDENTICAL. (c) The timed notification leg still passes, with the new zero check `[ok]`.

### R309-S1 - SUGGESTION - Tests, Robustness - `tb/verilator/milan_dp/sim_nxn.cpp:612-626` (`axi_read`), used by the new check at `:1596-1597`

`axi_read` returns `0` when `rvalid` never asserts within the guard, and does not check `RRESP`. A zero-equality check is therefore also satisfied by a wedged read channel. In this build the path is shown live at that exact point: all four nonzero mutants read their planted value there (receipts). So this does not make the new check vacuous, and the helper predates this PR. Optional hardening, as a separate change: have the helper report a timeout or non-OKAY response. Leaves no lens unclean.

### R309-S2 - SUGGESTION - Docs - `docs/reference/REGISTER_MAP.md:1259-1260`

The pre-existing line "Timers per the reference: probe response 200 ms ×2, retry 4 s, no-talker 10 s, random pre-probe delay 0..1023 ms (LFSR)" (from `86cde3951`) gives the ACMP listener probe-ladder timers. It now directly follows the new CTLR_DIAG paragraph, which ends on the departing-controller leg. A reader can take these as the departing-controller monitor's timers, which are 30-60 s and a 250 ms retry (`docs/reference/MILAN_COMPLIANCE_MATRIX.md:144`). The line also describes a ladder the page says now runs inside the processor. Out of #548 scope; this is a candidate for a new Issue, not a change to this lane. Leaves no lens unclean.

## Per-lens results

```text
[R309] MAJOR Conformance - hdl/common/csr/milan_csr.sv:761-766, :2395-2400 - acceptance 2 not met for the RTL (R309-F1)
[R309] MAJOR RTL - hdl/common/csr/milan_csr.sv:761-766, :2395-2400 - RTL register-spec comments contradict the STRUCTURAL ZERO tie and the edited port comment (R309-F1)
[R309] MAJOR Docs - hdl/common/csr/milan_csr.sv:761-766, :2395-2400 - in-code register documentation still reads 0x6F4 as a live count (R309-F1)
[R309] PASS Robustness - hdl/milan/milan_datapath.sv:3206 (module scope, outside every generate; the last generate before it closes at :3189), hdl/common/csr/milan_csr.sv:2400 (unconditional read decode), receipts/notify/*.log - the zero is unconditional across shapes, parameters and reset; read after probe, one retry and eviction; LSB, MSB, mixed-field and CSR-mux nonzero mutants are all caught
[R309] PASS Tests - tb/verilator/milan_dp/sim_nxn.cpp:1594-1597, receipts/notify-probe-summary.txt - the new check reads 0x6F4 over the AXI-Lite port after the monitor probed, retried and evicted B; clean 147/0; four mutants each exit 1 with exactly this check as the only failure; it runs in the default make via ./obj_notify (Makefile:486-495)
```

What was checked for the lenses that are otherwise clean inside the diff:

- **Conformance (diff-scoped items, all satisfied).**
  - Acceptance 1: the decision is recorded publicly (issue comment 5821224656).
  - Scope item 1: the row `REGISTER_MAP.md:1244`, the paragraph `:1248-1257` and the group TOC gloss `:188` use the legend's own wording from `:101` ("STRUCTURAL ZERO", "the source ... is deleted and has no replacement", "reads 0 because there is nothing behind it, not because nothing happened", "Never read it as a measurement"). The row and paragraph use the page's 🔴 marker convention. All three name the processor as the monitor's home, and the paragraph names `KL_aecp_notify` and `KL_aecp_ca_originator`. Both files exist at gitlink `09f9bf38` (`protocol-processor/hdl/aecp/`).
  - The claim "the processor exports no probe, reply or eviction count" holds at that gitlink. No `protocol_processor_top.sv` output carries a controller-monitor count, and the notify/originator ports are internal handshakes only (`KL_aecp_notify.sv:217-223`, `KL_aecp_ca_originator.sv:24-50`).
  - Scope item 3: `docs/findings/117_GPTP_SILICON_EVIDENCE.md:468-474` drops the eviction inference and keeps the wire facts (registration 13:10:47.0, deregistration 13:11:26.5, both SUCCESS, and the 13:13 read). `:524` qualifies the second read. The anchor link resolves (`check_doc_paths` 0, `docs_check` 0).
  - Scope item 4: no other current page reads 0x6F4. `docs/history` is untouched by the diff.
  - Scope item 5: met (Tests).
  - Scope item 6: `sw/builder/test_builder.py` is untouched by the diff.
- **RTL (diff-scoped, clean).** The comment-free token streams of `milan_csr.sv` and `milan_datapath.sv` are byte-identical between `573f0052` and the head (sha256 `cb178d9b...` and `327d63f9...`; `receipts/rtl_comment_free_equiv.txt`). The detector is sensitive: on a known functional change (`8eca7031d`) it reports DIFFERENT (`receipts/rtl_comment_free_equiv_control.txt`). The tie `aecp_ctlr_diag = 32'd0` is unchanged, and the new comments at `milan_datapath.sv:1500-1502` and `:3204-3205` and at `milan_csr.sv:309-312` are accurate. Only F1 is open under RTL.
- **Docs (diff-scoped, clean).** Current-doc searches, wording and path gates (`receipts/static/`) pass. Two points:
  - The `milan_dp` README describes the notify section without enumerating checks, so no count went stale.
  - The em-dash scan of the 32 added lines finds no U+2014 (`receipts/static/added_lines.txt`), and `git diff --check` is clean.

  Only F1 is open under Docs.

## Reviewer-owned completion ledger (this round)

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R309-F1) | issue #548 acceptance + decision 5821224656; REGISTER_MAP.md:92-103, :188, :1244-1257; 117_GPTP_SILICON_EVIDENCE.md:468-474, :524; milan_csr.sv:309-312, :761-766, :2395-2400; protocol-processor@09f9bf38 hdl/aecp, hdl/top | R309-1 | e41703b2948ef53e5cb0dd01a1e13c5632637615 |
| RTL | UNCLEAN (R309-F1) | milan_csr.sv (whole file, comment-free equivalence + comments at :309, :761, :2395); milan_datapath.sv:1500-1503, :3187-3206, :2535 | R309-1 | e41703b2948ef53e5cb0dd01a1e13c5632637615 |
| Robustness | CLEAN | milan_datapath.sv:3206 scope; milan_csr.sv:2400 decode; mutants m1-m4 (LSB/MSB/mixed/CSR-mux); read after probe+retry+evict | R309-1 | e41703b2948ef53e5cb0dd01a1e13c5632637615 |
| Tests | CLEAN | sim_nxn.cpp:1529-1617, :612-626, :95-104; Makefile:486-495; own clean + 4 mutant builds/runs (receipts/notify/) | R309-1 | e41703b2948ef53e5cb0dd01a1e13c5632637615 |
| Docs | UNCLEAN (R309-F1) | REGISTER_MAP.md legend/row/paragraph/gloss; 117 page; full-tree search; docs_check, check_doc_style, check_doc_paths, check_cpp_idiom receipts; RTL `//!` register comments | R309-1 | e41703b2948ef53e5cb0dd01a1e13c5632637615 |

A fix for F1 touches `milan_csr.sv` (RTL and Docs scope), so RTL and Docs must be re-covered at the new head, and Conformance re-checked for acceptance 2. Tests and Robustness are un-covered only if the fix touches their artifacts (the tie, the decode, the harness or the Makefile).

## Prior public review findings on this PR

When this round started, the PR had no reviews, no inline comments and no reviewer findings. The internal round's report ([R308] NEGATIVE, PR comment 5821998048) was posted while this round was running. I read it only after the verdict, findings and ledger above were written. At this head, each of its items is handled as follows:

| prior item | status at e41703b2 | this round |
|---|---|---|
| R308-1-F1 MINOR (Conformance, RTL, Docs): `milan_csr.sv:761-763`, `:2395-2399` still document a live count | **RETAINED, open.** The code is unchanged at this head | Same defect as R309-F1, found independently. I rate it MAJOR because it leaves the frozen acceptance 2 unmet for "the RTL". The internal round rates it MINOR because the generated HDL reference does not render these lines. Under either severity the three lenses stay unclean, the verdict is NEGATIVE, and the required outcome is the same comment-only fix |
| R308-1-S1 SUGGESTION (Tests, Robustness): `axi_read` returns 0 on a timed-out read | Retained as a suggestion | Concur; same as R309-S1. Non-blocking. The mutants show the path delivers data at that point |
| R308-1-S2 SUGGESTION (Docs): the 0x6F4 row drops the old `[31:24]/[23:12]/[11:0]` layout that sibling rows keep as "Was: ..." | Retained as a suggestion | Concur, non-blocking. Worth folding into the F1 fix as a single "Was: ..." clause. The paragraph at `REGISTER_MAP.md:1248-1257` does not carry the old layout either |
| Out-of-scope note: `milan_csr.sv:758` labels `A_ACMPL_DBG` (0x6E8) "RO live" while `REGISTER_MAP.md:1241` calls it STRUCTURAL ZERO | Confirmed present at this head | Not a finding against #548 (scoped to 0x6F4). Agree it belongs in a new Issue, together with R309-S2 |

## Executed evidence (receipts)

- `receipts/notify-probe-summary.txt`, `receipts/notify/*.log`, `receipts/notify/results.json`: my own build of `obj_notify` from a plain copy of the exact head, using the recipe `make -n run` prints in the exact-head clone (`receipts/notify-make-n-run.txt`).
  - Clean: rc 0, 147 checks, 0 failures. The log shows probe at 35791 ms, retry at 36041 ms and DEREGISTER at 36292 ms after B's last command, then `[ok] ... CTLR_DIAG (0x6F4) is STRUCTURAL ZERO after controller traffic = 0x0`.
  - m1: the datapath tie is `32'h01001001` (the author's value). Result: rc 1, 147/1, got `0x1001001`.
  - m2: the tie is `32'h00000001`. Result: rc 1, 147/1, got `0x1`.
  - m3: the tie is `32'h80000000`. Result: rc 1, 147/1, got `0x80000000`.
  - m4: the CSR read decode is `i_ctlr_diag | 32'h100`. Result: rc 1, 147/1, got `0x100`.
  - In every mutant the single failure is the named check.
  - My build is independent of the author's packet. The author's `notify-clean-build` step took 0.068 s, which suggests it reused an existing `obj_notify`. My clean binary was built fresh into a new object directory.
  - Install paths in the build logs are redacted.
- `receipts/rtl_comment_free_equiv.txt`, `receipts/rtl_comment_free_equiv_control.txt`: comment-free RTL identity plus the detector-sensitivity control.
- `receipts/static/`:
  - Passing (rc 0): `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py` and `check_cpp_idiom.py`.
  - Not run to a verdict: `gen_toc.py --check` and `check_em_dash.py --base 573f0052` refused with rc 2 because the pinned Markdown renderer is not installed in this environment. I did not install it; package installation was not permitted here. The added-line em-dash scan and `git diff --check` are in `added_lines.txt` and the report above.
- `receipts/hosted-check-runs.txt`: exact-head hosted check runs, read-only, at the time of this review.
  - Completed success: 17, including `docs-check`, `docs-check-no-git` and `rtl-fast`.
  - Skipped (not executed): `Physical gPTP (nightly and manual)`.
  - In progress: `Verilator shard 1/5` and `Verilator shard 4/5`. Shard 4 is the milan_dp shard per `.github/workflows/rtl.yml:222`.
- `receipts/verilator-identity.txt`: the scoped tool reports `Verilator 5.050 2026-07-01 rev v5.050`, wrapper sha256 recorded.
- `receipts/restore-check.txt`: after the probes the clone's worktree and index are identical to HEAD, the index tree is `4dd0f8cb...`, and there are no untracked or ignored files. The gitlinks for `protocol-processor`, `gptp-processor` and `third_party/verilog-axis` are checked out at their recorded commits and clean. `external` was not initialised, as at the start.
- `scripts/notify_probe.py`, `scripts/rtl_comment_free_equiv.py`: portable reproducers.

## Real limits

- `gen_toc.py --check` and the committed em-dash gate were not run to a verdict here (missing pinned renderer). Hosted `docs-check` and `docs-check-no-git` report success at the exact head, and the executor's packet records rc 0 for both. I rely on those for these two gates.
- I did not run the full `make -C tb/verilator/milan_dp` sweep or any parent, PP, gPTP, Yosys or builder bank, by assignment. Only the timed notification leg and its mutants were executed.
- No physical calibration or hardware was run. The #117 page edit is judged as text against the manager decision; no silicon claim is re-measured.
- Mutants are constant nonzero values. No mutant makes 0x6F4 nonzero only after controller traffic. The check's placement after the eviction is established from source order and the clean log.

## Pending manager duties

- Hosted/act acceptance at the exact head, including the milan_dp Verilator shard (4/5) and shard 1/5, which were in progress at review time.
- The final current-dev candidate build and merge-result validation (source base and live dev both `573f0052` at review time).
- Re-review routing after F1 is fixed: RTL, Docs and Conformance re-covered at the new head.
- Post-merge containment and Issue closure per CONTRIBUTING.

R309-1 FINISHED
