# Issue #548 author handoff

Author: [A279]. Status: author work complete; ready for independent review.
Reviewers: [R308] internal, [R309] external.
Issue: https://github.com/kebag-logic/milan-fpga/issues/548
Assignment: https://github.com/kebag-logic/milan-fpga/issues/548#issuecomment-5821224656
Branch: `548-ctlr-diag-zero`
Base: `573f0052a0e4412e81f0845438fcec2086ce5d55`
Head: `e41703b2948ef53e5cb0dd01a1e13c5632637615`
Commit: `Document and pin CTLR_DIAG as a structural zero`
The commit has a one-line subject, no body and no trailers.
The worktree is clean. The head's sole parent is the assigned base.

## Decision and change list

**STRUCTURAL ZERO**: 0x6F4 reads zero because its former counter source is gone. The processor still owns departing-controller detection but exports no probe, reply or eviction count to this word. No functional RTL changed.

| Assignment item | File:line | Change |
| --- | --- | --- |
| 1 | `docs/reference/REGISTER_MAP.md:188` | Group gloss names STRUCTURAL ZERO and the processor monitor. |
| 1 | `docs/reference/REGISTER_MAP.md:1244` | CTLR_DIAG row states zero is not a measurement. |
| 1 | `docs/reference/REGISTER_MAP.md:1248` | Replaces live-count interpretation with the page's structural-zero meaning; names KL_aecp_notify and KL_aecp_ca_originator. |
| 2 | `hdl/common/csr/milan_csr.sv:309` | Corrects the diagnostic input comment. |
| 2 | `hdl/milan/milan_datapath.sv:1500` | Corrects the diagnostic signal comment. |
| 2 | `hdl/milan/milan_datapath.sv:3204` | Explains the unchanged zero tie and live processor monitor. |
| 3, 4 | `docs/findings/117_GPTP_SILICON_EVIDENCE.md:468` | Keeps registration/deregistration times and both SUCCESS responses; removes the inference from CTLR_DIAG. |
| 3, 4 | `docs/findings/117_GPTP_SILICON_EVIDENCE.md:524` | Labels the later zero reading as structural, not a measurement. |
| 5 | `tb/verilator/milan_dp/sim_nxn.cpp:1594` | One AXI-Lite assertion after the timed monitor proves probes, retry and eviction. |
| 6 | Gate table below | All assigned positive gates return 0. |

A search of current Markdown for CTLR_DIAG, aecp_ctlr_diag and 0x6F4 found no other current page interpreting the word as a live count. `docs/history/` and `sw/builder/test_builder.py` are untouched. `scope-verification.json` records the exact five-file scope and proves every added/removed RTL line is a comment.

## Test and mutant results

The timed `obj_notify` leg drives controller registration and real monitor traffic. The new check reads `0x6F4` through the AXI-Lite BFM after controller B has been probed, retried and evicted, while controller A remains active. It does not read an internal signal.

| Run | Exit | Checks / failures | Evidence |
| --- | --- | --- | --- |
| Focused normal notification leg | 0 | 147 / 0 | `notify-clean.log` |
| Nonzero diagnostic mutant | 1, expected | 147 / 1 | `notify-mutant.log` |
| Mutation campaign verdict | 0 | Clean control passed; exactly the intended failure caught | `notify-results.json`, `run-notify.py` |
| Notification leg inside default sweep | 0 through sweep | 147 / 0 | `milan-dp.log` |

The mutant replaces only `assign aecp_ctlr_diag = 32'd0;` with `assign aecp_ctlr_diag = 32'h01001001;` in a temporary source. This sets one bit in each former field. Its only failure is:

```text
[FAIL] [NOTIFY-T] CTLR_DIAG (0x6F4) is STRUCTURAL ZERO after controller traffic got=0x1001001 exp=0x0
```

This leg has no existing mutant runner. Run `python3 <packet-directory>/run-notify.py` from the candidate repository root to reproduce both cases. The helper selects the exact obj_notify command from `make -n run`, builds the clean leg, substitutes the temporary datapath source and object directory for the mutant, and requires exactly the named failure with exit 1. `notify-recipe.log` and `notify-results.json` preserve the recipe and actual command statuses. Temporary mutant source/build files were outside this packet and removed after the run.

## Gate table

Every gate ran in the foreground, without a pipeline. `VERILATOR_JOBS=8` bounded build parallelism. No host timeout shortened the default sweep. `final-results.json` collects final return codes; `milan-dp-summary.log` records every leg's tally. The default sweep includes both gPTP variants, all datapath shapes, the 139-check audio-clock leg, and the existing render campaign (two clean controls and four caught mutants).

| Exact command | Result | Evidence |
| --- | --- | --- |
| `python3 scripts/docs_check.py` | 0 | `docs-check.log` |
| `env GIT_DIR=/dev/null python3 scripts/docs_check.py` | 0 | `docs-check-no-git.log` |
| `python3 scripts/check_doc_style.py` | 0 | `doc-style.log` |
| `python3 scripts/gen_toc.py --check` | 0 after pinned dependency setup | `toc-retry.log` |
| `python3 scripts/check_doc_paths.py` | 0 | `doc-paths.log` |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `module-matrix.log` |
| `python3 scripts/xvlog_gate.py --check` | 0; 4 existing processor findings match ratchet, 0 first-party findings | `xvlog.log` |
| `python3 scripts/check_rtl_source_lists.py` | 0 | `rtl-source-lists.log` |
| `python3 scripts/check_cpp_idiom.py` | 0 | `cpp-idiom.log` |
| `python3 scripts/check_py_idiom.py` | 0 | `py-idiom.log` |
| `git diff --check` | 0 | `diff-check.log` |
| `python3 scripts/check_em_dash.py --base 573f0052a0e4412e81f0845438fcec2086ce5d55` | 0 | `em-dash.log` |
| `git diff --check 573f0052a0e4412e81f0845438fcec2086ce5d55 HEAD` | 0 | `diff-check-committed.log` |
| `make -C tb/verilator/milan_dp` | 0; 1307.54 s, all legs and existing render mutants pass | `milan-dp.log` |
| `python3 <packet-directory>/run-notify.py` | 0; clean 147/0, mutant 147/1 (expected simulator exit 1) | `notify-results.json` |

## Reproduction notes and limits

- Both documentation inventory modes passed. `GIT_DIR=/dev/null` makes the gate select its filesystem walk without removing worktree metadata or making another checkout. The log confirms that mode. Its Git-only inventory-parity arm is skipped as in CI; the normal mode passed that arm.
- The first TOC invocation refused missing html5lib. The system package installer refused the initial install as externally managed. The pinned `tools/markdown/requirements.txt` was then installed in `/tmp/548-a279-docs-venv` with system-site packages visible. With that environment's bin directory first on PATH, the TOC and committed em-dash gates pass. No dependency or lock file changed.
- The first evidence-helper aggregate expected `[PASS]`, while this harness prints `[ok]`. Both simulator results were already correct. Only the helper's log spelling was corrected; the rerun passed with the same 147/0 and 147/1 results. The committed test was unchanged.
- RTL analysis passed its existing ratchet: four known findings in pinned processor sources, zero findings in first-party RTL. This is analysis evidence, not hardware or timing evidence.
- No push, PR creation/edit, merge, hardware work, sub-agent or other checkout was used. No toolchains, SDK copies, virtual environments or tree exports are in this packet.

## Review handoff

`PR-BODY.md` is the prepared PR text. `REVIEW-READY.md` is the public issue-comment body; publishing it is the final author action. Independent review remains pending for [R308] and [R309]. There are no open technical questions from this change. The next lane owner handles publication and review under the repository workflow; no merge is authorized here.
