[R872] NEGATIVE - exact head 502b041cc0bd0e4ea230b8a3a65f553ab69df3ff

External independent review, R872-1, PR #953 / issues #943 and #665. All five lenses were applied. The functional fix passes the focused checks. Declaring-output timing lacks maintained budget coverage, and the exploratory timing evidence contains a reproducible fixture error. Neither finding establishes a measured production deadline violation; both prevent accepting the present proof.

Tree: `eef553476a70ca961390ab9dbdf44a808d4c0076`. Range: `0839453f6d7135063e904bcaf4ac1852ad6b522a..502b041cc0bd0e4ea230b8a3a65f553ab69df3ff`, 13 one-line commits, 17 files. The public base is `flip-train-1117`, consistent with the owner's assignment to train step 13. This is not validation of a merge into live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`.

Scope reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, [#943](https://github.com/kebag-logic/milan-fpga/issues/943) and its public scope comments, the [#665 ruling, item 1](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-7007273447), requirements/interfaces, diff/history, then executable receipts. Standards examined directly: Milan v1.2 5.4.2.10.2 and Tables 5.8/5.11/5.12; IEEE 1722.1-2021 7.4.16; IEEE 802.1Q-2018 35.2.2.7.2 and Table 35-3. Timing authority: REQUIREMENTS.md section 1; FR_NFR.md NFR-SCOUT-03 and sections 3.4.1/3.4.2, H-AECP/H-NOTIFY. MAILBOX_SPLIT.md remains unchanged.

**R872-1-F1 — MAJOR — Conformance, RTL, Robustness, Tests**

Artifact: `sw/firmware/ctrl/app/ctrl_app_aecp.c:54`, `:85`; `tb/verilator/ctrl_service_budget/build.py:122`, `:141`, `:203`; published `author-r1/receipts/budget/declaring-face-measurement.txt`; PR #953 “Known limitations”.

Authority/evidence: NFR-SCOUT-03 requires measured bounds for each moved control path. H-AECP includes state access; H-NOTIFY includes complete fan-out. The new completion executes only for whole observations with STREAM_DEST_MAC_VALID set. The maintained answering-ports stub zeroes the flags, answering-every-port supplies zeroed observations, and the unmodified face is unavailable. The author explicitly records that no formal arm executes the completion. The exploratory arm measures one SET_STREAM_INFO record at each point, is outside maintained coverage, does not establish the completed GET_STREAM_INFO/notification service paths, and mishandles brief reads (F2).

Impact: a cost regression in the new source lookup and registrar completion can escape maintained budget checks while class/model checks remain green. Existing tight margins make this material. Passing undeclared rows and host functional tests do not establish the new declaring path's CPU service envelope.

Required outcome: maintain and grade a declaring-output case at 1x1/1if and 8x8/1if that actually executes the completion for full observations and the relevant response/notice paths, preserves brief reads, and accounts for its work in applicable record, retry/fan-out and service rows. Preserve authorized bounds. Moving this proof to a follow-up does not resolve it. An alternative proof must establish the same bounds for the added work.

Verification: executed receipts must demonstrate completion execution and applicable successful, refused and backpressured paths; a negative control must detect omitted execution coverage or cost. Re-run class/model checks on the resulting image. Retain the existing 40/33 passing rows as evidence for what they execute, without extending their claim to declaring outputs.

**R872-1-F2 — MINOR — Tests, Docs**

Artifact: published `author-r1/receipts/budget/declaring-face.patch.txt`, added `b_stream` body; `declaring-face-measurement.txt`, opening explanation; PR #953 declaring-output measurement paragraph; [#943 review-ready comment](https://github.com/kebag-logic/milan-fpga/issues/943#issuecomment-7015365492), corresponding risk item.

Authority/evidence: `aecp.h` and `aecp_face.c:162` define brief observations. The experiment's replacement executes `memset(v, 0, sizeof *v)`, then sets STREAM_DEST_MAC_VALID without restoring `brief`. A brief map check therefore enters `output()` at `ctrl_app_aecp.c:85`. The independent `probe_brief.py` compiles the exact published replacement with the exact-head bridge and counts the source callback. `brief-probe.log` records:

```text
published:
answered=1 input_brief=1 returned_brief=0 source_calls=1 dest=91e0f0000100
brief-preserved-control:
answered=1 input_brief=1 returned_brief=1 source_calls=0 dest=000000000000
```

Impact: the experiment changes both code placement and executed work. Its assertion that paced and largest-command records never execute the completion is false. Their 325 us and 1,920 us costs are not isolated placement measurements. This does not invalidate the separate final-image 310 us/1,720 us receipts. It invalidates the exclusive causal explanation of the experimental excess, so it is not wording-only RESIDUE.

Required outcome: preserve `brief` in the declaring fixture, remeasure, and correct dependent PR/issue evidence. Separate measured placement variation from additional execution; do not assign the excess quantitatively to either using this experiment.

Verification: brief observations retain brief=1 and call the source owner zero times; whole declaring observations still invoke it and return the expected values. Publish corrected numerical receipts and grades at both points. F1 separately requires maintained coverage.

**R872-1-R1 — RESIDUE — Docs**

Artifact: PR #953 Status and Linked Issue / roles.

Authority/evidence: public metadata names `flip-train-1117` as base; public start comments assign both reviewers. The body still calls this the first PR after the flip train, points at dev-soft-core, and leaves reviewer placeholders.

Impact: stale scheduling/role prose only; correction changes no measurement, test, clause claim or verdict.

Exact fix: change the current destination to `943-out-status -> flip-train-1117`; replace the “first PR after” scheduling sentence with “This PR joins the flip train as step 13 under the owner's 2026-11-19 decision”; fill internal reviewer `[R871]` and external reviewer `[R872]`. Keep any future destination conditional. Verification: compare with public base metadata and start comments. Residue does not affect cleanliness.

**Artifact-specific lens results**

| Lens | Examination and conclusion |
|---|---|
| Conformance | `ctrl_app_aecp.c:54`, `aecp_commands.c:373`, `srp_mbx.c:181`, `:461`, `ctrl_plat.c:96`: destination comes from the same MAAP-backed owner as ACMP. Registrar copies match stream ID and use the output's configured interface. Tables 5.8/5.12 explicitly include Asking Failed in REGISTERING; both flags under Asking Failed are correct. REGISTERING_FAILED is flags bit 0x40. Withdrawal suppresses both; the unchanged face clears destination validity and supplies zero when undeclared. Timing remains open under F1. |
| RTL | No HDL, mailbox layout or submodule pin changes. `aecp_face.c:165` keeps the bounded selector-0 read and the same publication-licence source for running; `aecp_maps.c:129` uses only running. The brief map check preserves its functional admission condition. All `aecp_stream_read` callers initialize brief; full GET/SET_STREAM_INFO remain whole reads. Validated ACMP configuration bounds interface selection; source/SRP guards short-circuit safely. No new CDC/reset cone or hardware handshake. Resource/timing proof remains open under F1. |
| Robustness | `test_aecp.cpp:818`, `:871`, `:2207` and independent runs cover every output, isolation from other outputs/interfaces, Ready/Ready Failed/Asking Failed, Listener leave, Talker withdrawal/redeclaration, absent allocation/SRP, extra and out-of-range sources, and brief/whole reads. Full 1x1 suites retain refusal, backpressure, pending acknowledgement and map rejection checks. Declaring-state timing remains open under F1. |
| Tests | Full 176-test application suite passes at each 1x1 interface count. AppOutputs and both brief-read controls pass at 8x8/1if and 8x8/2if. Old production code fails the new controls. All 15 new plants plus retained stream-read-brief are independently caught by name. No existing oracle is weakened in the diff. F1/F2 remain open. |
| Docs | All changed Markdown, public scope, new source comments and receipt attribution examined. AECP README describes the actual completion and brief behavior; memory documentation records the cost restatement; twin README correctly describes the removed owed row. No new forbidden bench/review identity was found in source comments. F2 prevents clean timing-evidence documentation; R1 is residue. |

The public scope explicitly excludes Listener-registration-triggered notices, Talker Failed failure fields, and changing the DA-gate declaring predicate to TALKER_DECL. Those limitations remain; this review neither resolves nor silently expands into them. The separate GET_TX_STATE failure flag remains a manager follow-up.

**Executed checks and evidence**

Independent receipts: `validated-*.log`, `plants.json` and individual `plant-*.log`, `old-code-*.log`, `brief-probe.log`, `flip-grade-*.log`, `validation.log`. Portable scripts take the reviewed repository as argument. Builds/probe trees are under packet scratch/. Focused builds used at most 16 compilation jobs; controls at most 12.

An initial broad 8x8 filter also ran generic map fixtures: ten failed at both interface counts. Repeating against base versions of all four changed production files reproduced those same ten failures, plus the two expected new controls. The generic fixtures normally run at the shipping shape. Their raw exploratory logs are retained; no full-8x8 green regression claim is made. The scoped 8x8 output/brief checks pass.

The [public author archive](https://github.com/kebag-logic/milan-fpga/tree/2c500f737f8d59d6962457da458e31e68460e0a5/review-evidence/943-r1/author-r1) supplies the larger campaigns. All 63 manifest hashes verify. Most execution is at `211c1edeb5d38443422b32550eb8f4a092b1cb28`; later changes are two Markdown files and a Python comment. These are carried executable receipts, not newly executed exact-head banks and not manager source-bank results.

| Evidence | Assessment |
|---|---|
| Firmware/coverage | Published four shards report 1,804 invocations, 825/825 control plants, 381 AECP plants and no escapes; coverage reports 40 files. Changed controls independently replayed above. |
| Twin owed row | `twin_compare.py:399` removes the exact waived discrepancy; general notice comparison stays active. `twin_plants.py:105` zeros destination bytes 66..71, retaining validity. The dropped-notice plant removes the output notices. Published twin rc=0; both replacement plants are refused by general comparison under both comparison settings. The owed row is genuinely answered, without a broader waiver. No independent full twin build claimed. |
| CPU rows | Independently parsed all 40/33 published AECP rows: each measured value fits its printed bound. Published arm A covers 99/98 groups, separately identifying seven held-egress backlog rows. Answering/Talker-notice receipts do not prove completion execution. |
| CPU costs/model | Final-image published 1x1 paced: 29,422 cycles, 310/310 us; long: 965/975 us. 8x8 long: 163,520 cycles, 1,720 us, matching most-plus-5%-rounded-to-5-us. The restatement changes a cost, not a service bound. Independent model checks pass: 1x1 last notice 137.97/140 ms; 8x8 load 0.744/0.75, transmit 76.81/77 ms. The published 325-us trial yields 141.54/140 ms and was correctly not adopted. Actual-face brief optimization is behavior-preserving; F2 qualifies the exploratory placement explanation. |
| ROM/release | Published ROM increases exactly 280 B at all four points to 126264/127864/138904/140480 B; SRAM unchanged; RAMB36 remains 45/46/58/63. Published memory tests pass. Both shipping shapes' all-fabric bios.bin, disassembly and stripped ELF hashes match base. Full debug ELFs differ and are not claimed identical. No independent image rebuild or hardware-image proof claimed. |
| Boundary | Published non-simulation boundary receipts refuse sink_mutants.py and talker_notice.py on base and source. Independent blob comparison proves both and ctrl_configs.py unchanged. Pre-existing, not this PR's regression. Separate simulation-boundary success does not clear the refused job. |
| Documentation | Published docs gate steps target 502b041c and return zero; SDK verification refusal is disclosed separately. Docs gates do not clear F1/F2. |

Placement sensitivity remains relevant to subsequent candidate images. The specific declaring-face experiment also changes execution and cannot quantify placement alone.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Milan 5.4.2.10.2/Tables 5.8/5.11/5.12; FR_NFR.md:330, :496; ctrl_app_aecp.c:54; budget receipts | R872-1 applied; no clean covering round | 502b041cc0bd0e4ea230b8a3a65f553ab69df3ff |
| RTL | UNCLEAN (F1) | 17-file diff; aecp_face.c:165; aecp_maps.c:129; ctrl_app_aecp.c:85; build.py:122 | R872-1 applied; no clean covering round | 502b041cc0bd0e4ea230b8a3a65f553ab69df3ff |
| Robustness | UNCLEAN (F1) | test_aecp.cpp:871; shape/interface logs; registrar/source bounds; active-path timing omission | R872-1 applied; no clean covering round | 502b041cc0bd0e4ea230b8a3a65f553ab69df3ff |
| Tests | UNCLEAN (F1, F2) | aecp_output_mutants.py; plants.json; base controls; build.py:141; brief-probe.log | R872-1 applied; no clean covering round | 502b041cc0bd0e4ea230b8a3a65f553ab69df3ff |
| Docs | UNCLEAN (F2) | AECP README:115; SPLIT_CONTROL_MEMORY.md:2998; twin README:1447; PR and declaring-face measurement | R872-1 applied; no clean covering round | 502b041cc0bd0e4ea230b8a3a65f553ab69df3ff |

This verdict and ledger were written before consulting another review report or prior reviewer findings. The subsequent public check found two review-start comments, zero submitted reviews and zero inline review threads. No prior public findings were present to resolve or retain; the receipt is prior-findings.json.

Reproduction: fetch archive commit 2c500f737f8d59d6962457da458e31e68460e0a5 and extract its review-evidence/943-r1/author-r1 directory and review-evidence/943-r1/MANIFEST.json beneath this packet's scratch/. Run run_focused.py, run_controls.py, probe_brief.py and validate_packet.py in that order, each with the exact-head checkout path as its argument. The scripts build only disposable copies or separate build outputs. Published author receipts remain cited at their immutable archive; they are not regenerated by these focused scripts.

Limits and pending manager duties: no full parent/processor/synthesis/builder banks, hosted acceptance, workflow replication, merge-candidate validation or physical qualification are asserted. The pinned simulation executable's identity was verified, but no independent CPU simulation is claimed. Source execution receipts belong to the author. The manager must resolve F1/F2 through corrected-head review; carry R1 to the residue checklist; reconcile the boundary refusal and required hosted contexts, distinguishing executed jobs from skips; validate the current-dev merge candidate with builder/native banks and publish receipts; finish the independent review/merge bar; perform post-merge containment. Physical calibration is NOT RUN; field skips are not hardware proof.

Preservation verification: all 1,933 tracked parent blobs match index bytes/modes; index tree equals HEAD tree; checkout is clean. Five required initialized submodules match their gitlinks and are clean. The unrelated external gitlink remains uninitialized at its original pin. No source fix, commit, push, GitHub write, merge, hardware action or other-checkout edit occurred. Only REPORT.md and MANIFEST.sha256-listed files are publication inputs; scratch/ is excluded.

R872-1 FINISHED
