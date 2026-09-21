[R213] POSITIVE - exact head 02c47cf0dbe7062ff762068875bf70b721dd6b37

Internal independent lane review, round four. Applied lenses: Conformance, Robustness, Tests, Docs, RTL. No BLOCKER, MAJOR or MINOR remains in the reviewed final scope. The four original R213 findings and the round-three publication-override finding are resolved at this candidate.

Scope was reconstructed from CONTRIBUTING.md, AGENTS.md, docs/README.md, REQUIREMENTS.md, issues [#465](https://github.com/kebag-logic/milan-fpga/issues/465), [#408](https://github.com/kebag-logic/milan-fpga/issues/408), [#409](https://github.com/kebag-logic/milan-fpga/issues/409), the authoritative firmware, architecture, register and saved-state documents, the complete candidate diff/history, both [original R213](https://github.com/kebag-logic/milan-fpga/pull/498#pullrequestreview-5263294055) and [original R214](https://github.com/kebag-logic/milan-fpga/pull/498#pullrequestreview-5263294169) negative reports, the [round-three response](https://github.com/kebag-logic/milan-fpga/pull/498#issuecomment-5755811193), both completed round-three reports, and the [round-four response](https://github.com/kebag-logic/milan-fpga/pull/498#issuecomment-5756245830). No private handoff or transcript was used.

The [manager's public scope decision](https://github.com/kebag-logic/milan-fpga/pull/498#issuecomment-5754191153) and current PR body agree: every existing text refusal remains active, the compiler instruments are additions, only #465 is proposed for closure, and #408/#409 retirement criteria remain open. This report judges that final scope. It does not infer resolution from another reviewer's verdict or from a test name.

[R213] PASS Conformance - sw/builder/test_builder.py:4797, sw/builder/test_builder.py:23312, REQUIREMENTS.md REQ-VER-03, issue #465 acceptance 1-4 - checked whole-firmware boot-word refusals, complete publication-loop pins, all five wait values and package capability ownership against the declared boot contract; no current text protection was lost.

[R213] PASS Robustness - sw/builder/test_builder.py:4231, sw/builder/test_builder.py:4265, sw/builder/test_builder.py:4337, review-evidence/probe-present.json, review-evidence/probe-absent.json, review-evidence/publication.json - challenged combined conditional/splice/paste shapes, selected arguments, equal-count reordered content, subsequent writes, loop else arms, duplicate loops and compiler absence; refusals and declared limits match the retained-rule contract.

[R213] PASS Tests - sw/builder/test_builder.py:11761, sw/builder/test_builder.py:23358, sw/builder/test_builder.py:23676, review-evidence/builder-present.log, review-evidence/builder-absent.log - ran complete gates 1b and 35 in both principal compiler environments, exercised independent negative and positive controls, and checked instrument acceptance separately from whole-contract refusal.

[R213] PASS Docs - docs/integration/BAREMETAL_FIRMWARE.md:206, docs/integration/BAREMETAL_FIRMWARE.md:1149, docs/integration/BAREMETAL_FIRMWARE.md:1234, review-evidence/focused-checks.json - checked the changed publication contract, retained text costs, instrument-only acceptance table, compiler limitations and current PR closure scope against implementation and executable observations; all listed documentation checks pass.

[R213] PASS RTL - hdl/common/csr/milan_csr.sv:794, hdl/common/csr/milan_csr.sv:2753, hdl/milan/milan_datapath.sv:2425, protocol-processor/hdl/adp/KL_adp_engine.sv:860, tb/verilator/pp_shadow/sim_main.cpp:1337 - traced CRFT_CTRL enable and the package-owned ADP capability bytes against REGISTER_MAP.md:875 and :938. The six-file candidate diff contains no RTL, constraint, firmware implementation or submodule-pin change; clock/reset/CDC and datapath behavior are unchanged by this PR.

The checkout was clean before testing. Local HEAD and live PR head match the exact candidate. Live dev was checked before and after testing and remained `07294a76e833f1831d9fcbceb8123b8380c4ae76`; `git merge-base --is-ancestor 07294a76e833f1831d9fcbceb8123b8380c4ae76 HEAD` exited 0. The candidate descends directly from that validation base. Only test_builder.py and BAREMETAL_FIRMWARE.md changed after the preceding reviewed head `f8b8c0fe17466ed4c64aaeee81ff21e0411fda59`.

| Required submodule | Verified gitlink and checkout |
|---|---|
| third_party/verilog-axis | 48ff7a7e2ef782cf778d47910cf85835c64b1bce |
| protocol-processor | 424c688fa2205b934a7689a58f2aa766420f2326 |
| gptp-processor | c1b617435824929a790739ea8585c3fe1a328cc0 |

The optional external submodule is uninitialized and was not a validation input. [Repository receipt](review-evidence/repository-state.json).

The findings were rechecked individually:

| Previous finding | Current evidence and disposition |
|---|---|
| Original 1: conditional-selected text combined with paste/splice escaped the preprocessor instrument | Resolved for the reported mechanisms. Independently built census-dropped and product-selected arms are refused by the instrument alone and by the retained reach rule. A splice inside a common comma-expression statement preserves statement count and is refused specifically by the second, closed-splice comparison. A pasted call in the same shape is refused by the conditional-arm bound. |
| Original 2: equal counts could hide changed content | Resolved. The comparator records ordered boot tokens and statement count. Exchanging configure_fabric/load_aem_image call tokens in actual preprocessor-output comparison data preserves their counts and the statement count, but is refused. This is explicitly a synthetic comparator control. A dropped external-CSR statement and a selected file-defined register argument are independently refused. |
| Original 3: no combined conditional/splice/paste controls | Resolved. Complete gate 1b executes the permanent whole-contract controls and seven instrument-only hostile controls. Independent variants include nested conditionals and common-expression splice/paste combinations, beyond the supplied totals. |
| Original 4: retirement claimed while the six refusals still graded firmware | Resolved by the public scope correction and matching implementation/docs. All six edits remain whole-contract refusals in both compiler environments. Instrument results are separately reported as five accepts and one refusal, without granting permission to make those edits. |
| Round three: a correct first add_constant could be followed by an overriding write | Resolved. Both original later-write forms are refused by the corrected predicate and complete gate 35 with each variant planted into milan_soc.py. Independent else-arm, conditional-write, duplicate-loop, early-continue, target-change and substituted-value variants also refuse. Pristine loops and comments/multiline-call variants pass the AST predicate. |

The original later-write reproductions retain the correct first call and append `soc.add_constant(_name, 3 if _name.endswith("CTRL_BOOT") else _value, check_duplicate=False)` in the fabric loop, or the corresponding heartbeat override to 300 in the firmware loop. Both now fail on `not the pinned complete loop`. The original file was restored in a finally block after each complete-gate test. [Publication evidence](review-evidence/publication.log).

The new predicate compares the complete For node, including target, iterator, body and else arm, and requires exactly one loop with each expected iterator. It pins these two publication loops. It does not prove arbitrary Python execution, name rebinding or surrounding control flow. Formatting positives above apply to the AST comparison; the separate mutation-site locators retain their textual anchors.

Preservation was checked against the live validation-base code, not only inferred from mutation totals. After removing docstrings, eleven relevant function bodies are AST-identical, including splice, primitive spelling, pointer-store parsing, ordered cast/store, asm, directive, preprocessing-reader and directory checks. The renamed directory checker preserves its exact equality; the factored conditional protection uses the same six anchors. The source diff retains their unconditional calls before the added compiler measurements. [AST comparison results](review-evidence/text-rule-ast.json).

Independent candidate/base observations, in both compiler environments, were:

| Edit | Whole contract, candidate and base, with and without RV32 | Candidate instrument alone, RV32 |
|---|---|---|
| Cast into a private static | Refused by cast set | Accepted by census/resolver |
| Helper pointer store into a private static | Refused by store set | Accepted by census/resolver |
| Exchange parse_u64/seconds_to_ns | Refused by ordered store set | Accepted by census/resolver |
| Token paste in a command handler | Refused by paste rule | Accepted by preprocessor comparison |
| README and notes beside firmware | Refused by directory pin | Accepted by include-resolution measurement |
| Conditional debug printf inside milan_init | Refused by reach rule | Refused by preprocessor comparison |
| Combined conditional/splice/paste variants | Refused by retained text rules | Refused; the rejecting instrument component is recorded |

A separately measured literal-only conditional argument remains accepted by the preprocessor instrument alone. The whole contract refuses it through the retained reach rule with and without RV32. This is a remaining instrument boundary, also identified publicly in round three, and is not a retirement claim. The instruments do not subsume every retained refusal. [Boundary evidence](review-evidence/residual-present.log).

Issue #465 was checked against its actual requirements:

| Acceptance | Evidence |
|---|---|
| Whole-firmware 0x750/0x614 | Extra writes in entity_advertise, and a computed-address 0x750 write in print_tod, are accepted by the base and refused by the candidate's resolved boot-word census with RV32. The instrument alone also refuses them. Without RV32, both heads accept those plants: the whole-firmware measurement is unavailable, not passed. |
| Publication values | Both original later-write cases now refuse through complete gate 35. Fourteen independent malformed-loop variants refuse at the predicate; pristine and two formatting/comment controls pass. |
| Five waits | Each value changed independently by one refuses the equality pin. Complete gate 35 passes five configurations plus CRF disabled, all five wait/publication controls and all four host-firmware controls. The NVM host self-test passes. |
| Package capability and docs | The harness uses PP_ADP_ENTITY_CAPS_C, derived by the Makefile from pp_adp_pkg; neither prior 0x614 provision nor its readback remains. Documentation, source-list and related checks pass. |

RTL was applied to concrete implementation artifacts. milan_csr decodes 0x750, resets its control to zero and drives the CRF enable from bit 0; milan_datapath connects that enable onward. Its 0x614 capability output is unconnected. The ADP engine inserts ADP_ENTITY_CAPS_C at wire bytes 34-37; KL_pp_shadow packs those bytes, and the datapath control merge carries them toward the MAC. The changed harness constructs its expected frame from the same package-owned contract rather than a CSR it provisioned.

The [completed external round-three report](https://github.com/kebag-logic/milan-fpga/pull/498#pullrequestreview-5263585652) supplies supporting evidence for these unchanged artifacts: 371 pp_shadow checks passed; a wrong expected capability failed; a changed package with a derived expectation passed; disconnecting the engine from that package failed. Those native experiments were not rerun in this round. Their supporting scope is the unchanged capability path, not approval of the corrected publication test.

Exact commands and results are retained in review-evidence. The executed scripts lived under `REVIEW_TMP=/data/milan/tmp/498-review-R213-r4`; copies are provided here. The launcher sets CPU affinity 64-79, MAKEFLAGS=-j8, TMPDIR beneath REVIEW_TMP, and disables bytecode. Commands ran synchronously. Temporary HOME and PATH environments excluded the installed RISC-V tools for absence testing; no installed compiler was moved or modified.

| Command | Result |
|---|---|
| `python3 -B "$REVIEW_TMP/runner.py" launch present python3 -B "$REVIEW_TMP/runner.py" test_baremetal_profile_contract test_boot_policy_follows_the_declaration` | Exit 0. Buildroot GCC 14.3.0; 208/208 mutations refused; 17/17 firmware and 4/4 Makefile edits accepted; 5/6 instrument candidates accepted, one refused; 7/7 instrument hostile controls refused. No focused skip. |
| Same command with `launch absent` | Exit 0. 182/182 mutations refused; same accepted-edit totals. One registered gate-1b compiler arm not run, including all three added instruments, resolver and instrument-only measurements. Gate 35 passes with the host compiler. |
| `python3 -B "$REVIEW_TMP/runner.py" launch elf python3 -B "$REVIEW_TMP/runner.py" test_baremetal_profile_contract` | Exit 1 on pristine candidate: unresolved __errno store versus declared __errno_location residual. |
| Same elf command with `--base` | Exit 1 with the identical refusal on validation-base code. Pre-existing conservative toolchain limitation, not a pass or skip. |
| Launcher modes present/absent, `python3 -B "$REVIEW_TMP/probe.py" <mode>`, each with and without `--base` | All four drivers exit 0; each individual expected acceptance/refusal is asserted and recorded in the four probe JSON files. |
| Launcher present, `python3 -B "$REVIEW_TMP/publication.py"` | Exit 0; predicate controls, both complete-gate later-write refusals and five independent wait changes verified. |
| Launcher present/absent, `python3 -B "$REVIEW_TMP/residual.py"` | Both exit 0; retained-rule refusal confirmed, instrument boundary recorded, absent instrument explicitly skipped. |
| Launcher present, `python3 -B "$REVIEW_TMP/checks.py"` | Exit 0; all fourteen commands below exit 0. |

The fourteen static/documentation/host commands, with exact arguments and logs in [focused-checks.json](review-evidence/focused-checks.json), are:

```text
python3 -B scripts/docs_check.py
python3 -B scripts/check_doc_style.py
python3 -B scripts/check_doc_paths.py
python3 -B scripts/gen_toc.py --check
python3 -B scripts/check_em_dash.py --base 07294a76e833f1831d9fcbceb8123b8380c4ae76
python3 -B scripts/check_feature_status.py
python3 -B scripts/check_solution_docs.py
python3 -B scripts/check_baremetal_only.py --check --selftest
python3 -B scripts/pp_srcs.py --check --selftest
python3 -B scripts/check_py_idiom.py
python3 -B scripts/check_cpp_idiom.py
python3 -B scripts/check_nvm_record_space.py
python3 -B docs/traceability/gen_module_matrix.py --check
python3 -B sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
```

The complete focused runs import the candidate without changing its checks and redirect builder output to scratch. Instrument probes expose its unchanged nested functions by returning locals before the baseline call in an in-process AST. Base probes use the validation-base test file with the unchanged implementation artifacts. No compiler callback, tracing hook or other-process instrumentation was used. Historical full-base totals 194/171 are public supporting evidence, not rerun totals from this round.

Exact-head hosted checks were queried twice using `gh api repos/kebag-logic/milan-fpga/commits/02c47cf0dbe7062ff762068875bf70b721dd6b37/check-runs`. Ten checks succeeded, including [rtl-fast](https://github.com/kebag-logic/milan-fpga/actions/runs/35568393144), [documentation checks](https://github.com/kebag-logic/milan-fpga/actions/runs/35568393304) and [elaborate](https://github.com/kebag-logic/milan-fpga/actions/runs/35568393220). Five were skipped in the [exhaustive workflow](https://github.com/kebag-logic/milan-fpga/actions/runs/35568393380): verilator-suites, yosys-portability, both shard entries and physical gPTP. A skipped long gate is not successful exhaustive evidence. [Exact-head check receipt](review-evidence/hosted-checks.json).

This reviewer-owned ledger records only lenses applied cleanly in this round:

| Lens | Covering round | Exact head |
|---|---|---|
| Conformance | R213 round four | 02c47cf0dbe7062ff762068875bf70b721dd6b37 |
| Robustness | R213 round four | 02c47cf0dbe7062ff762068875bf70b721dd6b37 |
| Tests | R213 round four | 02c47cf0dbe7062ff762068875bf70b721dd6b37 |
| Docs | R213 round four | 02c47cf0dbe7062ff762068875bf70b721dd6b37 |
| RTL | R213 round four | 02c47cf0dbe7062ff762068875bf70b721dd6b37 |

Coverage is not permission to merge. An independent external verdict and all mandatory exact-head gates remain required.

Limits: no full builder-main run, whole Verilator sweep, milan_dp, pp_shadow native rerun, full Yosys portability, processor-native sweep, full SoC elaboration, Vivado or hardware test was run here. Gate 1b did run its 46 RTL-mutant elaboration controls in both complete focused runs; that is not a full native sweep. Manager evidence is separate. No Docker, act, installs, privilege, subagents, commits, pushes or public writes were used.

Final git diff and diff --check are empty for tracked changes. Hashing all 1,388 tracked files across the main repository and the three required submodules found no byte mismatch against their commits. The publication file was restored byte-exact; only REVIEW.md and review-evidence/ were added. [Byte verification](review-evidence/tracked-byte-check.json).

R213 FINISHED
