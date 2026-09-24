[R281] NEGATIVE - exact head 612db13c244335b0fa3467d02ebab1c350b01990

# R281-1: external cleared-context review of issue #536 / PR #543

- Exact head: `612db13c244335b0fa3467d02ebab1c350b01990`, tree `80a23ecd3630d054c0062d62ba138494efc44693` (verified in the detached review clone).
- Source base: `26d855a9176d63625e6635a029a0c44e3d57ce9a`. Diff: 5 files, +288/-29, no RTL, no gitlink change (`protocol-processor` 424c688, `gptp-processor` c1b6174 at both ends).
- Reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue body and its public comments (assignment, TAKEN, REVIEW READY), the #510 owner decision (issuecomment-5789766089), the PR body, the Milan v1.2 specification text, the pinned processor sources and benches, the diff and both commits, and the published evidence at `review-evidence/536-r1` (hashes match its MANIFEST.json).
- All five lenses applied: Conformance, RTL, Robustness, Tests, Docs.

## Result in one paragraph

The model change itself is correct. Driving 45 MVU-relevant frames through a build of the pinned processor (Verilator 5.050, `tb/pp_top` at 424c688, with the pinned suite's own 732 checks through its MilanInfoPhase passing, M1 to M9 included) shows the exact-head model answering every frame byte for byte as the RTL does. That covers every frame the contract feature sends, plus over-length, truncated, foreign-octet, non-VENDOR_UNIQUE, real Figure 5.5/5.6/5.7 and silent cases. The Milan clause numbers in the diff check out against the specification, except for one misattributed quotation. One IEEE citation is misapplied to MVU; that is a prior finding, verified and retained. The verdict is NEGATIVE on three MINOR findings of this round, plus one prior MINOR (R280-F3(a)) retained after verification. The new outline that claims to grade "each compared field" pins only 3 of the sub-decode's guards: six single-substitution mutants of the model survive the whole suite (326/326), and each of them demonstrably disagrees with the pinned RTL. Two RECOMMENDED rows send a command shape their cited clause does not define. One comment quotes Section 4.2.4 under a 5.4.4.1 heading.

## Findings

### F1 - MINOR - Tests, Robustness

`[R281] MINOR Tests, Robustness - tests/features/aecp_response_contract.feature:148-172 (Examples "each compared field, one at a time" at :163); tests/steps/aecp_engine_model.py:550,552 - the sub-decode outline pins 3 of the mirrored engine's guards; message type, upper length and 5 of 6 protocol_id octets are unguarded`

- Requirement/evidence:
  - `_mvu_command_type()` mirrors `mvu_get_milan_info_w` (`protocol-processor/hdl/aecp/KL_aecp_engine.sv:1291-1296`). That decode has six conjuncts: protocol MVU (message type 6), `pld_cmd_r >= 8`, @22..@23, @24..@25, @26 and @27 (`pid_lo_r`), and the @28 word.
  - The outline's negative rows vary only @27 (`C1-01`), the r bit, and one octet short.
  - Six one-line mutants remove an engine term. All six leave the contract feature at 42/42 and the whole suite at 326/326 green (`receipts/mutation_arms.txt`, `receipts/mutation_survivors_full_suite.txt`):
    - message type 6 conjunct dropped
    - length guard made exact (`!= 8`)
    - @22..@23 not compared
    - @24..@25 not compared
    - @26 not compared
    - only @27 compared, so 40 of the 48 bits are unguarded
  - None of the six is an equivalent mutant. `receipts/mvu_model_vs_rtl.txt` lists, for each one, the frames where it disagrees with the pinned RTL:
    - message types 0, 2, 4, 8 and 14 carrying the MVU bytes, which the RTL echoes NOT_IMPLEMENTED of their own type
    - GET_MILAN_INFO at cdl 24 and cdl 112, which the RTL serves: SUCCESS, cdl 32
    - one foreign octet at each of @22 to @26, which the RTL echoes
  - The exact-head model matches the RTL on all of these frames.
  - The pinned processor documents exactly this gap in its own bench (`protocol-processor/tb/pp_top/sim_main.cpp:2400-2413`, M8): "M3 ... exercises one comparison term out of four ... 40 of the 48 bits the design compares were guarded by nothing". The feature (:149) cites M3, M5, M5b and M6, but not M8.
  - This feature already sweeps non-AEM message types against the AEM arms (the #83 outline at :212-231). It has no MVU counterpart.
- Impact:
  - The offline model can drift in three of its four guard families while the conformance suite stays green. That is the silent-drift direction the steps header (`aecp_engine_steps.py:143-154`) says this suite exists to stop.
  - One of those drifts answers a non-VENDOR_UNIQUE message as GET_MILAN_INFO, which is the #83 defect class the model's own comments (`aecp_engine_model.py:363-369`) say a model must not reproduce.
  - The Examples title and the feature comment claim coverage the rows do not have.
- Required outcome: every conjunct the model mirrors has at least one row that fails when that conjunct is removed or weakened. At minimum:
  - one foreign octet per protocol_id position @22 to @27, the M8 granularity
  - one over-length GET_MILAN_INFO that is still served (SUCCESS, cdl 32)
  - one non-VENDOR_UNIQUE message type carrying the MVU bytes, echoed NOT_IMPLEMENTED
- Verification: `scripts/mutate_model.py` rerun at the fix head. All six arms above must turn the contract feature red, and the unmutated tree must stay green.

### F2 - MINOR - Conformance, Tests, Robustness

`[R281] MINOR Conformance, Tests, Robustness - tests/features/aecp_response_contract.feature:129,131 (fed by tests/steps/aecp_engine_steps.py:378-381 and build_mvu_command at tests/steps/aecp_engine_model.py:659-672) - the SET_SYSTEM_UNIQUE_ID and SET_MEDIA_CLOCK_REFERENCE_INFO rows send a Figure 5.3 frame and record cdl 20 under clauses whose commands are cdl 28 and cdl 92`

- Requirement/evidence:
  - Milan v1.2 5.4.4.2, Figure 5.5: SET_SYSTEM_UNIQUE_ID carries a 64-bit `system_unique_id` after the reserved field, so its payload is 16 octets and cdl is 28.
  - 5.4.4.4, Figure 5.6: SET_MEDIA_CLOCK_REFERENCE_INFO carries `clock_domain_index`, flags, the two priorities, a reserved quadlet and a 64-octet name, so its payload is 80 octets and cdl is 92.
  - Figure 5.3's caption names only GET_MILAN_INFO and GET_SYSTEM_UNIQUE_ID. Figure 5.7 (GET_MEDIA_CLOCK_REFERENCE_INFO) has the same 8-octet length, with `clock_domain_index` where Figure 5.3 has reserved.
  - Every row is built by `build_mvu_command()`, which always emits the Figure 5.3 8-octet payload. So rows 0x0001 and 0x0003 grade a truncated command while their clause cells name 5.4.4.2 and 5.4.4.4.
  - The pinned RTL answers the real Figure 5.5 and 5.6 commands with the NOT_IMPLEMENTED echo at cdl 28 and cdl 92 (a 118-octet frame). The exact-head model agrees byte for byte (`receipts/mvu_model_vs_rtl.txt`, cases `x_fig55_set_system_unique_id_cdl28` and `x_fig56_set_mcr_info_cdl92`). The model is right. The rows do not exercise the commands they name. Details are in `receipts/spec_citation_check.txt`.
- Impact:
  - The table records cdl 20 as this device's answer to SET_SYSTEM_UNIQUE_ID and SET_MEDIA_CLOCK_REFERENCE_INFO. Under the Milan figures those commands, and the engine's echo of them, are cdl 28 and cdl 92. These rows are the offline record of the #510 RECOMMENDED fallback, so a reader takes the wrong wire length from them.
  - No MVU row echoes more than 8 payload octets, so a length-dependent defect in the MVU echo stays green. This is the maximum-length side of the Robustness lens.
- Correction, made after the verdict and ledger were written: the first draft of this impact also leaned on IEEE 9.3.5.3.3's "correctly sized response". While verifying the prior finding R280-F3(a) against the IEEE text, this reviewer confirmed that sentence is scoped to AEM commands, so it is removed here. The finding rests on the Milan figures and the RTL receipts alone. Robustness was added to the lens list for the same reason the prior review gives, the untested maximum-length echo. Neither change moves the verdict or any ledger row.
- Required outcome: two acceptable fixes.
  - Preferred: each RECOMMENDED row sends its command in its own figure (5.5, 5.3, 5.6, 5.7) and asserts the echo at that length (cdl 28, 20, 92, 20).
  - Otherwise: the rows state that they send a Figure 5.3 frame, and they stop asserting a per-command length.
- Verification:
  - Each row's status-flip arm stays red.
  - A mutant that caps the MVU NOT_IMPLEMENTED echo at 8 payload octets turns rows 0x0001 and 0x0003 red.

### F3 - MINOR - Docs, Conformance

`[R281] MINOR Docs, Conformance - tests/steps/aecp_engine_model.py:81-83 - a Section 4.2.4 sentence is quoted under a Section 5.4.4.1 heading`

- Requirement/evidence:
  - The comment introduces "the three Figure 5.4 quadlets this device reports (Milan v1.2 5.4.4.1)" and then quotes: "A PAAD shall set the value of the protocol_version field in the GET_MILAN_INFO response to 1".
  - That sentence is Milan v1.2 Section 4.2.4, verbatim.
  - Section 5.4.4.1 words it differently: "The protocol_version field shall be set to the Milan protocol version supported by the PAAD-AE. The value of this field is 1."
  - The pinned processor cites both clauses (`protocol-processor/hdl/aecp/ucode/gen_ucode.py:101-102`, "§4.2.4 and §5.4.4.1"), and pp_top M2 cites §4.2.4.
  - The author asked, in the issue's REVIEW READY open risks, for a reviewer with the text to check this wording.
  - Every other Milan clause citation in the diff checks out (`receipts/spec_citation_check.txt`). The one exception is an IEEE citation, not a Milan one: `feature:105-106` applies IEEE 9.3.5.3.3 to MVU, and that is retained from the prior review below as R280-F3(a). The Milan citations that check out include 5.4.3.2.2 (r is zero in every MVU command and response) and 5.4.4.1: SHALL, Figures 5.3 and 5.4, reserved field zero on send and ignored on receive, protocol_version value 1, certification_version 0.
- Impact: anyone who checks the quotation in the cited clause will not find it there. CONTRIBUTING.md section 6 requires compliance references to cite the clause, and the steps header makes the recorded clauses govern this file.
- Required outcome: attribute the quotation to Section 4.2.4, optionally adding 5.4.4.1's own sentence, or quote 5.4.4.1 instead.
- Verification: compare the text against the specification.

### S1 - SUGGESTION - Docs (does not affect coverage)

`tests/features/aecp_response_contract.feature:32-36` ("NOTE ON THE DECODE") says the dispatch arms read @22..@23 "without consulting the protocol", and that a VENDOR_UNIQUE protocol_id starting 00-04 "would land on the READ_DESCRIPTOR microprogram". The #83 outline in the same file (:183-210) and the model (`aecp_engine_model.py:356-375`) contradict that note. The text predates this PR and the diff does not touch it. The fix is optional: in this lane under the cleanup rule, or in a separate issue.

## Clean lens evidence

`[R281] PASS RTL - protocol-processor@424c688 hdl/aecp/KL_aecp_engine.sv:697-719,1141-1168,1284-1296,2421-2433,2812-2825,3178-3214; hdl/aecp/ucode/gen_ucode.py:98-118,683-718; tb/pp_top/sim_main.cpp:2198-2437 - no RTL, processor pin or gitlink changes; the model's sub-decode, E_MVUINFO body, VENDOR_UNIQUE header echo, echo length and drop arc match the pinned RTL byte for byte on 45 frames (receipts/mvu_model_vs_rtl.txt), after the pinned suite's own 732 checks through MilanInfoPhase passed (receipts/pp_top_probe_run.log)`

The RTL reading behind that line:

- The MVU decode is gated on `cmd_r.protocol == PP_PROTO_MVU`. Responses are dropped at pop (`drop_w`, :1168).
- Every other re-dispatch flag at the A_PLD exit derives from `aem_w`, which requires message type 0 (:1141). So nothing overrides `UPC_MVUINFO_C` for an MVU command.
- The walk captures @22..@29 into `raw_ct_r`, `cfg_ix_r`, `pid_lo_r` and `desc_ty_r`. `ctrs_r` is clear for MVU, so the capture is not blocked.
- `pld_cmd_r = min(cdl - 12, PLD_MAX, slot)` is the same quantity as the model's `pld_cmd`.
- E_MVUINFO restates `C50A`, `C100`, `0000`, `0000`, `00000001`, `00000000`, `00000000`: 20 octets, cdl 32. That is the model's body.

## Reviewer-owned completion ledger (this round)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2, F3; retained R280-F3(a)) | Issue #536 acceptance 1-3; #510 decision; Milan v1.2 4.2.4, 4.2.5, 5.3.9, 5.4.3.2-5.4.3.3, 5.4.4.1-5.4.4.5, Tables 5.18-5.20, Figures 5.2-5.7; IEEE 1722.1-2021 9.3.5.3.3, 9.6.2.3 and 9.6.5.3.1 (9.6 checked after reading the prior review); `tests/steps/aecp_engine_model.py:74-90,281-554,659-672`; `tests/features/aecp_response_contract.feature:98-181`; model-vs-RTL receipt | R281-1 | 612db13c244335b0fa3467d02ebab1c350b01990 |
| RTL | CLEAN | Pinned engine, microcode and pp_top lines named in the PASS line above; `git diff --stat` base..head (no RTL, gitlinks unchanged); 45-frame RTL differential; pinned pp_top 732/732 through MilanInfoPhase | R281-1 | 612db13c244335b0fa3467d02ebab1c350b01990 |
| Robustness | UNCLEAN (F1) | Model and RTL on cdl 12/18/19 (truncated), cdl 24/112 (over-length), foreign octet at each of @22 to @27, r = 1, command_type 0x0005/0x7FFF/0xFFFF, message types 0/2/4/8/14 with MVU bytes, VENDOR_UNIQUE response as input, other target entity, junk reserved (all match RTL; only 3 classes pinned by rows) | R281-1 | 612db13c244335b0fa3467d02ebab1c350b01990 |
| Tests | UNCLEAN (F1, F2) | `tests/features/aecp_response_contract.feature:98-181`; `tests/steps/aecp_engine_steps.py:250-266,378-397,799-872`; exact-head behave (contract 42/299, full 14/326/1600); 9 reviewer mutation arms (3 killed, 6 survived); the author's published 21 arms (`review-evidence/536-r1/author/mutations.log`) | R281-1 | 612db13c244335b0fa3467d02ebab1c350b01990 |
| Docs | UNCLEAN (F3; retained R280-F3(a)) | `tests/README.md:90`; `docs/MILAN_V12_ROADMAP.md:539` (Section 6 row) with `:133-135` (served MVU fact block); `docs/reference/MILAN_COMPLIANCE_MATRIX.md:95-105,135`; `docs/reference/FR_NFR.md:143,187-189`; `docs/reference/milan_feature_status.json:37-39`; comments and headers in the three touched test files; PR body; 14 focused gates at the head (`receipts/focused_gates.txt`, all rc 0) | R281-1 | 612db13c244335b0fa3467d02ebab1c350b01990 |

The only lens this round covers clean is RTL, at `612db13c244335b0fa3467d02ebab1c350b01990`. A later commit that changes the model's mirror of the engine re-opens RTL coverage as well.

## Evidence and reproduction (packet-relative paths)

- `scripts/mutate_model.py --clone <exact-head clone> --scratch <dir> --out <log>`: nine single-substitution arms, each in a disposable copy of `tests/`. The rest of the clone is symlinked read-only into that copy. Receipts: `receipts/mutation_arms.txt` and `receipts/mutation_survivors_full_suite.txt`.
- `scripts/mvu_cases.py gen|diff`: builds the 45 frames with the candidate's own builders, addressed with the pp_top identities, and compares model and RTL answers. It also reports where each mutant diverges. Receipts: `receipts/mvu_cases.txt`, `receipts/mvu_rtl_answers.txt` and `receipts/mvu_model_vs_rtl.txt`.
- `scripts/pp_top_probe.py`: inserts the probe phase into a disposable copy of the pinned `tb/pp_top/sim_main.cpp`, right after `MilanInfoPhase`. The inserted text is in `receipts/pp_top_probe.diff`.
  - Every other source in the scratch copy was verified equal to the pinned blob.
  - It was built with the scoped Verilator 5.050, rev v5.050 (wrapper sha256 `905795b9...e92f`), at 8 jobs.
  - Run log: `receipts/pp_top_probe_run.log`.
- `receipts/behave_contract_head.log` and `receipts/behave_full_head.log`: exact-head suite, matching the author's tally.
- `receipts/focused_gates.txt`: docs_check, check_em_dash (base 26d855a9), check_feature_status, check_py_idiom, check_doc_style, gen_module_matrix --check, measure_test_evidence --check, check_hygiene --check, check_todo_ownership, measure_fail_fast --check, measure_naming --check, check_doc_paths, gen_toc --check, git diff --check. All rc 0.
- `receipts/hosted_check_runs.tsv`: exact-head hosted runs, inspected only.
  - The seven required contexts (rtl-fast, docs-check, wire-accountability, docs-check-no-git, elaborate, verilator-suites, yosys-portability) all completed success, and the Verilator and Yosys shards executed.
  - "Physical gPTP (nightly and manual)" was skipped, which is not hardware proof.
  - Hosted and act acceptance stays with the manager.
- `receipts/spec_citation_check.txt`: citation-by-citation result against the Milan v1.2 text (specification file sha256 `6bb902be...3bba8`), plus the IEEE 1722.1-2021 row added after the prior review.
- `scripts/verify_clone.sh` produced `receipts/clone_restore_verify.txt`, after all probes:
  - HEAD and tree are exact, and there is no modified, untracked or ignored path.
  - The index equals HEAD, and no skip-worktree or assume-unchanged flag is set.
  - All 872 tracked blobs re-hash to HEAD with their HEAD modes.
  - All four gitlinks are unchanged. `protocol-processor` (222 blobs) and `gptp-processor` (103 blobs) are at their pins and re-hash byte for byte.
  - This round's own behave runs had created six bytecode-cache directories after the clone was made. They were removed before this check.
  - No source in the clone was ever edited. Every probe ran in disposable copies under the packet's `scratch/`, which is not published.

## Prior public findings on this PR

This reviewer read the one prior public review on this PR only after the verdict, findings and ledger above were written: the internal round R280-1, NEGATIVE at this same head (PR comment 5806086835). Each of its items is either retained at `612db13c244335b0fa3467d02ebab1c350b01990` or resolved:

| Prior item | Severity, lenses | Disposition at this head | Basis |
|---|---|---|---|
| R280-F1: no row pins the protocol_id head and middle, or the message_type guard | MINOR; Tests, Robustness | RETAINED, same defect as R281-F1 | Independently reproduced. The arms `mt_guard_dropped`, `pid_head_22_23_dropped`, `pid_24_25_dropped`, `pid_26_dropped` and `pid_only_27` survive 326/326, and each disagrees with the pinned RTL. R281-F1 also covers the upper length bound (`len_exact_20`). R280 examined an over-length command without raising it. |
| R280-F2: the 0x0001 and 0x0003 rows send a truncated form of their own command | MINOR; Conformance, Tests, Robustness | RETAINED, same defect as R281-F2 | Same RTL result: Figure 5.5 echoed at cdl 28, Figure 5.6 at cdl 92, and the model agrees. This reviewer concurs with the Robustness attribution and has adopted it. |
| R280-F3(a): IEEE 9.3.5.3.3 is cited for the MVU echo at `feature:105-106` | MINOR; Conformance, Docs | RETAINED, verified | IEEE 1722.1-2021 (sha256 `ad7b8220...9c`): 9.3.5.3.3 is processCommand of the **AEM** entity state machine ("an AEM Command other than ACQUIRE_ENTITY and LOCK_ENTITY"), and its "correctly sized response" sentence sits there. Vendor Unique commands fall under 9.6: the status is Table 9-6, and 9.6.5.3.1 asks only for "an appropriate status code". The diff adds this citation once (`+  # 5.19 status 1, IEEE 9.3.5.3.3)`). This reviewer's independent pass checked only the Milan citations, and its own F2 draft repeated the misreading (corrected above). Conformance and Docs were already UNCLEAN, so the ledger does not change. |
| R280-F3(b): the 4.2.4 quote is placed under 5.4.4.1 | MINOR; Conformance, Docs | RETAINED, same defect as R281-F3 | Same specification text. |
| R280-S1: the MVU gate regex parses only `[15:0]` and `16'h` spellings | SUGGESTION; Tests | RETAINED as a suggestion | Checked. A `[14:0]` / `15'h` or a `16'd` declaration of a served constant does not parse, and the gate stays green while GET_MILAN_INFO still parses. Failing closed on any unparsed `MVU_(GET\|SET)_` localparam would remove this. It does not affect coverage. |
| R280-S2: `SERVED_MVU` is not tied to the ledger's `served_mvu_operations` | SUGGESTION; Tests, Docs | RETAINED as a suggestion | This is the author's own recorded limitation. Both lists hold only GET_MILAN_INFO today (`docs/reference/milan_feature_status.json:37-39`). |
| R280-O1: the stale "NOTE ON THE DECODE" | out of scope | Agreed; same as R281-S1 | Present at base. The diff does not touch it. |
| R280-O2: the dated behave total in `tests/README.md:80,128` (312 scenarios, 2026-08-30) | out of scope | Agreed, not a finding | The text is explicitly dated and says the run's own tally is authoritative. It is present at base. The per-feature row this PR edits (42) is correct. |
| R280-O3: the 5.4.4.1 NOTE about not replying from a non-compliant configuration | out of scope | Agreed | The PR's limitations state it. It is a processor/owner decision. |

With these retained, the open set at this head is R281-F1 to F3, the same three defects as R280-F1 to F3, plus R280-F3(a). All are MINOR. No BLOCKER or MAJOR is open. The two independent rounds agree that RTL is the only lens covered clean at this head.

## Real limits

- Offline model and simulation only. Nothing ran on hardware, physical calibration was NOT RUN, and field skips are not hardware proof.
- The RTL comparison is one pinned pp_top build at 424c688. It drives each frame alone, after the pinned prefix, into an idle engine. It says nothing about MVU under backpressure, concurrent traffic or reset during activity; the model does not claim those.
- pp_top ran only through MilanInfoPhase, and then the probe stopped the run. Later phases, the full processor bank, the parent bank, Yosys, the builder, act and the candidate merge were not run, as this round's rules require.
- One unintended execution, disclosed so it cannot be mistaken for evidence. While reading the scratch Makefile's source list, `make -p` in the scratch pp_top copy also ran that Makefile's default target once, with the host's default Verilator (5.052) and the Makefile's own `-j 0`. That exceeded this round's 8-job limit for one build. Its output was discarded and its `obj_dir` deleted before the pinned 5.050 build that produced every RTL receipt. It touched only the scratch copy.
- The specification was read through a text rendering, and figure layouts were read from that rendering. Offsets were cross-checked against the RTL answers.
- The #537 lane's documentation rows were deliberately not reviewed, to respect the scope split.

## Pending manager duties

- Publish this report and route R281-F1 to F3, and the retained R280-F3(a), to the author lane. Each needs a fix and a re-review at the new head. Moving any of them to another issue does not resolve it.
- Rebuild the final current-dev candidate at the merge turn. The source base and live dev were both `26d855a9176d63625e6635a029a0c44e3d57ce9a` when this round started.
- Own hosted and act acceptance at the final head, then run post-merge containment.
- Optional follow-up, not a finding: the author's open item of tying `SERVED_MVU` to the ledger's `served_mvu_operations` in `scripts/check_feature_status.py`.

R281-1 FINISHED
