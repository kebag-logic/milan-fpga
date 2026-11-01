# HANDOFF - [A720f] issue #640 Mark II charter, round 6 (docs only)

Status: REVIEW READY at head 3f5fea241e8dacd976798ca817c67e55096cf1aa (2026-11-01). Every docs-workflow gate step rc 0 on a clean clone of that head; `git diff --check 1f29f189 HEAD` rc 0. Local only, nothing pushed.

- Lane: $LANES/640-mark2-charter, branch 640-mark2-charter. Round-5 head 270866ecb95155ef48428ec3a049c357f7eae946 (PR #828). Round-6 head 3f5fea241e8dacd976798ca817c67e55096cf1aa, tree e2600e7d503b92f793cd48cad8c9fd47fb645f7b.
- Base: live dev 1f29f189279f9fc0132f4918e47342b87d22f33a (re-fetched after the gates, unchanged); merge base 1f29f189. Round 6 adds 10 lines and removes 4 on one page (270866ec..HEAD); against 1f29f189 the PR adds 1,754 and removes 112 over 7 pages.
- Remote checked: https://github.com/kebag-logic/milan-fpga.git
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6556380588 (text: evidence/taken_posted.md)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6556877240 (text: evidence/review_ready_posted.md)
- Reviews answered: R757-5 (PR #828 issuecomment-6556322232) and R758-5 (issuecomment-6556353161), both read in full.
- Manager ruling applied: R758-5-F1's second outcome, no new mechanism, merge rule unchanged.
- Decisions: comments on #640, #665 and #823 since 08:30 UTC today are lane TAKEN and REVIEW READY posts, so round 5's reading stands.
- Scratch: $VALIDATION_STORAGE/640-a720f. Evidence (small files): ./evidence/.

## Commits (one-line subjects, no body, no trailers)

| # | SHA | Files | Group |
|---|---|---|---|
| 1 | 872ff20e458681f3990453170559b97bf93a0264 | SE | R758-5-F1 |
| 2 | 3f5fea241e8dacd976798ca817c67e55096cf1aa | SE | R757-5 RR8 and R758-5-R1; R757-5 RR9 |

`SE` = docs/design/MARK_II_STREAM_ENGINES.md. RR10 is PR-body text only. No rebase, no amend, nothing pushed.

## Changes (file:line at 3f5fea24)

| Change, file:line | Source |
|---|---|
| SE:624 "Under a valid head, conversion error never shifts a sample." | R758-5-F1 required outcome, as written |
| SE:627-628 new paragraph after the "A new anchor" line: "A margin under 125 µs lapses the head every packet." "Interleaved copies can then land one sample apart." | R758-5-F1, as written; SE:672 (a time the render point passed counts as invalid) and rule 2 SE:647 are why |
| SE:630 new pointer "[Open design item 3](#open-design-items) owns that case." Its own paragraph, because the paragraph above is at the two-sentence limit | Assignment: give the case its owner |
| SE:660 "Under a valid head, clean copies keep that external behaviour." | R758-5-F1: same condition on the Annex D.2 claim. Milan v1.2 Annex D.2, read this round in round 5's extract: "implementation can be different as long as the external behavior is the same", "it renders one or the other, depending what is available". Reworded from "The merge keeps ..." for the 10-word limit |
| SE:1173 new row, item 3 "Short margin on both networks": requirement (defines a margin; lapse; interleaving; the lane states the shift it allows; this page fixes no mechanism or figure) and verification, with the assigned setup word for word | Assignment; R758-5-F1. Legal margin: IEEE 802.1BA-2011 6.5 class A transit 2 ms against the 2 ms default offset, as R758-5 cites at SE:560 |
| SE:1173 links the probe and its output at commit f9cfe08c, tip of the public evidence branch, the same pinned link form as the item 2 pointer | Assignment: the reviewer's published probe as the starting case |
| SE:647 rule 2 "it anchors the head and restarts the map with only bit 0 set" | R757-5 RR9 exact fix |
| SE:1185 TU-4 "A stream that starts with tu, unpaired or on both networks, still renders." | R757-5 RR8 exact fix |
| PR body, Round 5 row R757-4-N7: "TU-4 requires that a stream starting with tu still renders, unpaired or on both networks, with the lane stating how." | R757-5 RR8 exact fix |
| PR body, commit row `07f8eb91` ends "The tu text left in round 5." | R757-5 RR10 exact fix |
| PR body, known limitations gains one line, "Short margin on both networks" | Assignment |
| PR body, Round 3 row R757-2-N2 gains "(round 6 conditions this on a valid head)" | Not in the assignment. Same reasoning as RR10: a history row must not read as a current unconditional claim |

Unchanged: the merge rules' conditions and actions, every register, every latency, save, area and Block RAM figure, every other page.

## Decisions taken inside the assignment

- **RR8 and R758-5-R1 differ in text.** The assignment calls them the same. RR8: "A stream that starts with tu, unpaired or on both networks, still renders." R1: "An unpaired stream or a pair that starts with tu still renders." They mean the same. RR8's is applied, because it also supplies the PR-body text.
- **A pointer sentence was added (SE:630).** The assignment names the item; without the pointer the page would state the limit without its owner.
- **"Margin" is defined in item 3, not at SE:627.** SE:627 is the reviewer's exact sentence, and the paragraph has no room under the limits.

## Derived numbers

| Number | Derivation |
|---|---|
| 125 µs | The page's class A packet interval. A first copy arriving less than this before its time leaves the next packet arriving after the head's time has passed |
| 766 shifts, 383 unwritten samples, in 2,000 packets (SE:1173) | Reviewer's probe result, section A of its output, at each of 48, 96 and 192 kHz. Stated as the probe's result, not a design figure. My re-run against the round-4 merge model is byte-identical to the published output (evidence/probe/) |

Probe digests: `probe_margin_r5.py` f8d451fa2b7aa92f3d5e1ef73b557b8b78c04b59babb26df56e04085d0755a50; `probe_margin_r5.out` cd30fc2c620089c6d2cc90d6cfa9866271ee04715da5ad0ae7c9549603a6ae3a.

## Finding closure

| Finding | Closed by | Verification |
|---|---|---|
| R758-5-F1 | SE:624, :627-628, :630, :660, :1173; PR known limitations | Read the lines against the finding's second outcome; the probe stays reproducible at the linked commit |
| R757-5 RR8, R758-5-R1 | SE:1185, PR Round 5 row | Read SE:1185 against case G at SE:1205 |
| R757-5 RR9 | SE:647 | Read against `LCTX_MERGE` WMAP's "bit k set when the packet k intervals before the head is written" |
| R757-5 RR10 | PR commit row | Read the row |

### Suggestions

R757-5 S8 to S13 and R758-5 S1 to S4 are not taken: the assignment says touch nothing else. All are optional.

## Gate table

Every step of `.github/workflows/docs.yml` was run as its jobs run it, sequentially (no parallel sweeps), on $VALIDATION_STORAGE/640-a720f/gates/wt at 3f5fea241e8dacd976798ca817c67e55096cf1aa (tree e2600e7d), a fresh clean clone of the lane with the four submodules the jobs fetch (gptp-processor 135afd04, protocol-processor a9e84b66, tsn-c-stack 70936b77, verilog-axis 48ff7a7e, their module directories copied from round 5's scratch clone, each origin its .gitmodules URL). Gate venv: round 5's, copied. The pinned RV32 SDK was installed fresh into this lane's scratch HOME ("SDK fresh installation: verified"); the shared SDK was not touched. TMPDIR pointed at scratch for this run. dev is unchanged since round 5's base (1f29f189), so the workflow is too. After the run the clone's status was empty and its gitlinks unchanged. All 50 rc files read 0. Logs and rc files: ./evidence/gates/.

| Job | Step (workflow id) | Command | rc | Result |
|---|---|---|---:|---|
| wire-accountability | Advertised-vs-emitted gate | `check_wire_accountability.py --self-test` | 0 | RESULT: PASS |
| docs-check-no-git | Strip git metadata, then run the docs gate | `docs_check.py`, `check_feature_status.py` on `git archive HEAD` without .git | 0 | 0 findings |
| docs-gates-0 | gate_1 HDL reference | `gen_hdl_reference.py --selftest`; `--output` | 0 | index.html written |
| docs-gates-0 | gate_7 link health | `docs_check.py` | 0 | 0 findings, 213 md + 1436 scrubbed files |
| docs-gates-0 | gate_8 em dash | `check_em_dash.py --base 1f29f189` (merge base with live dev) | 0 | 0 findings over 1754 added lines in 7 pages |
| docs-gates-0 | gate_9 concise docs | `check_doc_style.py` (+ `--selftest`), `check_gptp_docs.py` (+ `--selftest`) | 0 | OK; 30 controls |
| docs-gates-0 | gate_10 diagram no-drift | `DOC_MAP.gen.py --check/--selftest`, `timesync_chain.gen.py --check/--selftest` | 0 | OK |
| docs-gates-0 | gate_11 solution docs | `check_solution_docs.py` (+ `--selftest`) | 0 | 45 controls |
| docs-gates-0 | gate_12 submodule docs | `submodule_boundaries.gen.py --check/--selftest`, `check_submodule_docs.py` (+ `--selftest`) | 0 | OK |
| docs-gates-0 | gate_13 WaveDrom | `gen_wavedrom.py --selftest` and the three `--check` runs | 0 | current |
| docs-gates-0 | gate_14 PNGs | `check_diagram_pngs.py` (+ `--selftest`) | 0 | 6 rasters, 28 controls |
| docs-gates-0 | gate_15 feature status | `check_feature_status.py --self-test` | 0 | 0 findings |
| docs-gates-0 | gate_16 traceability | `gen_module_matrix.py --check` | 0 | up to date, 80 modules |
| docs-gates-0 | gate_18 imported gPTP docs | `check_gptp_docs.py --with-submodule`; `make -C gptp-processor docs` | 0 | PASS |
| docs-gates-0 | gate_19 measurement self-tests | `measure_control_flow.py --selftest`, `measure_cohesion.py --selftest` | 0 | 18 PASS |
| docs-gates-0 | gate_21 bare-metal scope | `check_baremetal_only.py --check` and `--selftest` | 0 | 0 findings over 1434 files; 867 arms |
| docs-gates-0 | ci_step_28 RV32 SDK | `ci_rv32_sdk_selftest.py`; `ci_rv32_sdk.py --destination $HOME/br-milan-rv32/host` | 0 | SDK fresh installation: verified |
| docs-gates-0 | gate_24 compiler-absent controls | `test_firmware_compiler.py --selftest`; `--absent --audit` | 0 | GATE 1b PASS; 1 NOT RUN by design; 0 compiler invocations (683 s) |
| docs-gates-0 | gate_26 NVM record space | `check_nvm_record_space.py` (+ `--self-test`) | 0 | 0 findings, 5 configs |
| docs-gates-0 | gate_27 capture census | `check_nvm_capture.py` | 0 | PASS |
| docs-gates-0 | gate_28 saved-state writer | `test_nvm_firmware.py --self-test` | 0 | OK, 5 shapes |
| docs-gates-0 | gate_29 SoC sources | `check_soc_sources.py` (+ `--selftest`), `iob_pack_selftest.py` | 0 | 22 arms |
| docs-gates-0 | gate_30 RTL source lists | `check_rtl_source_lists.py` (+ `--selftest`) | 0 | 50 PASS |
| docs-gates-0 | gate_31 naming | `measure_naming.py --check/--selftest` | 0 | 66 PASS |
| docs-gates-0 | gate_32 port contracts | `check_port_contracts.py` (+ `--selftest`) | 0 | 82 PASS |
| docs-gates-0 | gate_33 fail-fast | `measure_fail_fast.py --check/--selftest` | 0 | 106 PASS |
| docs-gates-0 | gate_34 TODO ownership | `check_todo_ownership.py` (+ `--selftest`) | 0 | 45 PASS |
| docs-gates-0 | gate_35 test evidence | `measure_test_evidence.py --check/--selftest` | 0 | 105 PASS |
| docs-gates-0 | gate_36 hygiene | `check_hygiene.py --check/--selftest` | 0 | 35 PASS |
| docs-gates-0 | gate_37 to 40 idioms | `check_sv_idiom.py`, `check_cpp_idiom.py`, `check_py_idiom.py`, `check_sh_idiom.py` (+ `--selftest` each) | 0 | 55, 75, 54, 48 PASS |
| docs-gates-0 | gate_43 cited paths | `check_doc_paths.py` | 0 | 1084 paths resolve |
| docs-gates-0 | gate_44 archive | `check_archive.py` (+ `--selftest`) | 0 | OK, 24 controls |
| docs-gates-0 | gate_45 contents | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | 152 pages; 580 cross-page links reproduced |
| docs-gates-0 | gate_46 to 49 | `gen_aem_store.py --self-test`, `check_sweep_shape.py`, `check_deploy_shape.py`, `check_entity_shape.py` (`--self-test`) | 0 | PASS |
| docs-gates-0 | gate_50 CI controls | `ci_gate_workflows.py --check` and the thirteen self-tests | 0 | PASS |
| docs-gates-1 | gate_25_0 builder leg 0 | `ci_builder_legs.py run 0 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS (1072 s) |
| docs-gates-2 | gate_25_1 builder leg 1 | `ci_builder_legs.py run 1 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS EXCEPT 16 NOT RUN |
| docs-gates-2 | gate_41 CI events | `ci_events.py --check/--selftest` | 0 | 2199 items, 5258 arms |
| docs-gates-2 | gate_42 act runner contract | `act_ci.py --selftest`; installed copy `--selftest --worktree` | 0 | PASS |
| (lane) | Markdown gates, pinned venv $VALIDATION_STORAGE/818-mdvenv | `docs_check.py`; `check_em_dash.py --base 1f29f189`; `check_doc_style.py`; `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | same results as above |
| (lane) | whitespace | `git diff --check 1f29f189 HEAD` | 0 | no output |
| (lane) | style on touched pages | `style_touched.py` (check_doc_style's analyze()) over every changed block of the 7 pages against 1f29f189 | 0 | 0 findings |

Notes:
- The 16 NOT RUN arms of leg 1 are the same as round 5's: 15 need an interpreter that imports migen, litex and litex_boards, which the docs workflow never installs, and gate 11 needs a local Arty build report. Each leg's rc is 0; the verdict is judged on the union of the legs.
- docs-check "Require every gate exactly once" verifies the uploaded CI receipts and runs only on GitHub; ci-manifest, ci-fail-fast and ci-cancel-tail are CI orchestration. None was run locally. act was not used: it needs a pushed head, and this lane pushes nothing.
- Setup: `git clone --no-local` of the lane, origin set to the public URL in the clone only; submodules checked out with `--no-fetch` at the pinned gitlinks. The lane's own origin was not touched.
- /tmp: TMPDIR pointed at scratch. `find /tmp -maxdepth 2 -user alex -newer run_all.start` lists other sessions' working-directory markers and one `tmpvncdzo15.py` with its `__pycache__`. No step of this lane writes that name, its origin is not established, and it was left alone.

## Evidence (./evidence)

| File | What |
|---|---|
| taken_posted.md, review_ready_posted.md | The TAKEN and REVIEW READY texts as posted |
| probe/ | The reviewer's probe and output as published, and my re-run |
| style_touched.py, style_touched.log | check_doc_style's analyze() over every changed block of the 7 touched pages against 1f29f189 |
| make_pr_body.py | Builds PR-BODY.md from round 5's by exact-text replacement |
| gates/ | Every gate step's log and rc at 3f5fea24, run_all.out, run_all.sh, run_gates.sh; LARGE_LOGS.txt holds the one log over 200 KB by digest and size |
| SHA256SUMS | Digests of every file above |

## Open points for the reviewers and the manager

- **R757-5 S9 stays open.** Item 3 names both networks, as assigned. S9's arm is one surviving network, a time 100 ns past a sample boundary, 160 ns of packet-to-packet jitter: its probe reports samples missing and misplaced, where R758-5's one-network control (no such jitter) shows 0 shifts. SE:665 "While the other stays clean, the pair loses no samples." is unchanged. R758-5 finds it holds; R757-5 reads it as too strong in that regime and asks the manager to carry S9 to lane 6. Item 3's verification does not cover that arm.
- The clean row (verification table, "Listener merge, clean copies") still names no margin arm. Item 3 is that case's only owner, as assigned.
- The requirement text still needs owner approval, as in round 5.

## Not done / not allowed

No push, PR edit, merge to dev, rebase, sub-agent, bench, flashing or Vivado. No RTL, firmware, generator, gate or configuration change. No existing comment edited. No finding argued; none reopened. The shared RV32 SDK in the home directory was not touched.
