[R252] POSITIVE - exact head e0c43b03f31d6c1220dd05a110e4bb30029233a0

R252-1 is the cleared-context internal Codex review of PP issue #102 / PR #103. All five lenses are CLEAN for this exact source head; this round found no open BLOCKER, MAJOR or MINOR. This is one independent source review. R253 external Opus remains pending and is not waived. Current-main candidate validation, merge authorization and post-merge evidence remain manager-owned obligations.

| Identity | Verified value |
|---|---|
| Checkout | `$VALIDATION_STORAGE/reviews/r252-pp102-r1`, detached HEAD |
| Head | `e0c43b03f31d6c1220dd05a110e4bb30029233a0` |
| Tree | `0547903adc17449dfb4f0c2610a23e6adb4ff6a2` |
| Source base and sole parent | `f70ba36ecb634467e4b1c3f0dbf1239d1e12af57` |
| Changed artifact | `tb/pp_top/Makefile:59`, mode 100644, one line |
| Preservation | Other 223 tracked entries unchanged; every entry mode preserved; no gitlinks |

The review follows the [public assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/103#issuecomment-5782563688), [issue #102](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/102), and its frozen takeover/acceptance, captured under [public/](public/). The exact [diff](raw/source.diff), [history](raw/history.txt), [source preservation audit](raw/evidence-audit.json), and [final tracked-file audit](raw/final-integrity.json) establish the reviewed population. No private transcript, implementation scratchpad or author contact was used.

The original [parent finding](https://github.com/kebag-logic/milan-fpga/issues/400#issuecomment-5781426819) concerned authorized donor `8452f564294300a82d56eed464276576f65f4d58`: the common group already enabled warnings, but the supplementary group violated the parent's per-group rule. The public original [command receipt](evidence/parent-original-idiom-cpp-final.json) records `python3 scripts/check_cpp_idiom.py` exiting 1 at parent candidate `17e2cf6928865bbf1cabcec4800483bef685900f`; its [raw output](evidence/parent-original-idiom-cpp-final.log) reports `build without warnings 1 > ratchet 0`. This review does not represent a new full parent-gate execution.

Parent policy was read at immutable `483a133ed08867ea0d300d2b4a027b5b48a4282f`. Trusted-clone Git object bytes were compared with exact public Git blobs before use; that clone was neither modified nor initialized. The preserved [AGENTS.md](parent/AGENTS.md), [CONTRIBUTING.md](parent/CONTRIBUTING.md) sections 2/3, and [CODE_QUALITY.md](parent/docs/development/CODE_QUALITY.md) Rule 11 supply the review, warning and verification contracts. AGENTS sections 6/7 require artifact-specific evidence, every attributable lens, a reviewer-owned lens/round/head ledger, and no open MINOR/MAJOR/BLOCKER under a CLEAN lens. Two independent positives, including the external system, are still required.

| Immutable parent input | Verified Git blob |
|---|---|
| AGENTS.md | `b9d500cc4a16d63103921c7aff1e7c5356eb3476` |
| CONTRIBUTING.md | `c8d4508401424b2049acee9826e95f6906fe93b2` |
| CODE_QUALITY.md | `3f4597dbf1225dac28b4ce52ac3f1e91d19a367d` |
| scripts/check_cpp_idiom.py | `1d9ccd7fa1fded549f8988149397ff10bc12b0d5` |
| scripts/code_quality_scope.py | `4603080a48d97e1e45f8b787273a2b459b1aebe6` |
| scripts/cpp_idiom.budget | `909800d2f6eb8e06540b7e7c593955a46d01e746` |

The donor's [README](source/README.md), [HDL consumption contract](source/hdl/README.md), [documentation map](source/docs/README.md), [engineer guide](source/docs/guides/hdl-engineer.md) and [hdl.yml](source/.github/workflows/hdl.yml) define its own gates. This donor has three hosted jobs and no repository-owned parent act runner. Parent workflow names and the parent's host orchestrator were not transplanted into this donor review. No Docker/act, host candidate orchestrator/selftest, hardware, shared installation or full donor/parent/Yosys bank was executed by R252.

| Frozen acceptance | Evidence and status |
|---|---|
| Both warning flags in every pp_top CFLAGS group; fixture unchanged | PASS: both groups, exact insertion and macro preservation in [parser results](raw/parser-results.json) |
| Real immutable parser accepts correction and detects each single-flag removal | PASS: independently executed; controls and raw log below |
| Complete pinned pp_top, fixture guards, preserved default/Domain behavior; mandatory donor gates | PASS: independent focused execution plus separately attributed public manager native executions and actual hosted jobs |
| Independent five-lens review, two positives including external, candidate and containment | R252-1 complete; R253 and manager completion obligations remain outstanding. No claim that issue #102 is fully complete or merge-ready |

The entire source change is the insertion of ` -Wall -Wextra` inside the supplementary quoted group. [parser_controls.py](scripts/parser_controls.py) verifies that replacing that one string in the base produces the entire new Makefile exactly. Thus recipe order, dependencies, source list, tally logic, all macro/fixture/default values and every other Makefile byte are preserved. All other tracked files, including scenarios, fixture guards, RTL, docs and workflow, have identical base/head blobs and modes.

Both CFLAGS groups are now:

```text
-CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"
-CFLAGS "-DPP_TOP_SRP_DOM_DEF_VID=0x$(SRP_VID_FIXTURE) -Wall -Wextra"
```

The original common group was already the first line above. The generated [default makefile](raw/obj_dir-Vpp_top_wrap.mk) and [fixture makefile](raw/obj_vid-Vpp_top_wrap.mk), together with actual C++ commands in the [build log](raw/pp-top-full.stdout.log), confirm additive groups. This change repairs the per-group policy incompatibility; it does not turn previously disabled effective warnings on. Rule 11 also explicitly retains Verilator's individual warning suppressions; no `-Werror`, new suppression, checker exemption or ratchet adjustment is introduced.

The reviewer imported the complete verified parent module and called its actual `cflags_missing`, without replacing or reimplementing the parser. [Raw command/output](raw/parser-controls.log.command.json), [raw log](raw/parser-controls.log), [results](raw/parser-results.json), and [disposable input copies](controls/) are retained.

| Input | Actual parser result |
|---|---|
| Original base | `['-Wall', '-Wextra']` |
| Exact reviewed file | `[]` |
| Only newly repeated `-Wall` removed | `['-Wall']` |
| Only newly repeated `-Wextra` removed | `['-Wextra']` |

The fixture contract was independently reconstructed from public [#95](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/95), [#97](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/97), [#98](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/98), their captured comments, and exact-head source. The shipping top parameter remains 16 bits with default 2 (`hdl/top/protocol_processor_top.sv:144`), directly bound to `KL_srp_top.DOM_DEF_VID_P` at line 2147. F01.5 (`docs/architecture/01_overview.md:166`) and the integrator guide require product VID 2. `5A3C` remains a verification fixture, whose 16-bit wire value differs from both 2 and its 12-bit observable value `A3C`. The HDL define remains `16'h5A3C`; the independent C++ expectation remains `0x5A3C`. The default wrapper has no override.

The preserved [DV implementation](source/tb/pp_top/sim_main.cpp) at lines 8242–8407 executes 20 checks on a fresh model: reset ports/snapshot/GET_DOMAIN and silence; LINK_UP byte-exact declaration and full 16-bit wire value; GET_TX_STATE's 12-bit VLAN; bridge adoption to VID 5 with one DOMAIN_CHANGE and Lv/New ordering; LINK_DOWN restoration with one DOMAIN_CHANGE and no declaration during the 500 ms down window; and LINK_UP re-declaration. The [Domain RTL](source/hdl/srp/KL_srp_domain.sv) at lines 155–171 and [F10.2](source/docs/architecture/10_srp_engine.md) at line 205 agree: restore on LINK_DOWN, declare on the subsequent LINK_UP. The byte-identical [pp_top README](source/tb/pp_top/README.md) records historical M25–M31 binding/default controls. Those historical mutation results are preserved evidence, not new R252 mutation runs.

R252 executed the complete `make ... run` target, including its guard prerequisites, with only the runtime `VFLAGS` job count changed from `-j 0` to `-j 8`. The exact [argv, times, exit and stream hashes](raw/pp-top-full.stdout.log.command.json), [expanded recipe](raw/pp-top-dry-run.log), [stdout](raw/pp-top-full.stdout.log), [stderr](raw/pp-top-full.stdout.log.stderr), [tallies](raw/build-tally.txt) and [executable hashes](raw/build-artifacts.json) are retained. Exit was 0.

The installed selector `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` was used without alteration. Its shell selector, Perl driver, Perl forwarder and final ELF were resolved and hashed in [tool-identity.json](raw/tool-identity.json). Both selector and real ELF report `Verilator 5.050 2026-07-01 rev v5.050`; ELF SHA-256 is `44898b22af4178b45214a0820a04eeac8632ae721ff005e69ef1cf69121bbfdd`, matching the public manager identity. Actual recipes retain the explicit eight-job cap.

| Independently executed case | Result |
|---|---|
| Default executable, no fixture macro | 1,391 checks, 0 failures; all sections including DV |
| Fixture executable, `0x5A3C` | 20 checks, 0 failures; DV alone |
| Canonical suite tally | **1,411 PASS, 0 FAIL** |
| Guard: no override / 5A3C | Both compile |
| Guard: 0002 | Refused with both 16-bit and 12-bit distinctness diagnostics |
| Guard: 1002 | Refused with only the 12-bit distinctness diagnostic |
| Compiler-locale regression | One unittest passes, testing absent and inherited LC_ALL |

`fixture_guards.py:45–60` requires the exact diagnostic set, refusal status and error count; unrelated compiler failures cannot satisfy it. `Makefile:54,67–73` makes guard enforcement part of the normal run. `sim_main.cpp:9054–9076` sends the default executable through `Suite(h).run()` and the fixture executable through DV only, increments actual CHECK calls and records each build's count. The final Makefile sum requires exactly two tally rows. The four guard cases and locale test are not added to 1,411. No omitted fixture-build sections receive checks. Existing wrapper diagnostics remain visible in stderr: 57 PINMISSING and 12 PINCONNECTEMPTY messages across generation passes, matching the public author log; this focused simulation is not described as warning-free.

The immutable [public manager packet](https://github.com/kebag-logic/milan-fpga/tree/ff273ff39b7bcb55f54e79ef4c423eb7244347b8/review-evidence/pp102-r1/source/manager) was downloaded by Git blob and verified. These are **manager executions inspected by R252**, not R252 reruns. [Full command receipts](evidence/source/manager/full-native.json), [exit records](evidence/source/manager/full-native/results.json), all nine [raw logs](evidence/source/manager/full-native/) and [reviewer audit](raw/evidence-audit.json) are included. Initial/final manager manifests independently agree with all 224 exact-head blobs, modes and SHA-256 values.

| Manager command, under its recorded scoped tool environment | Exit | Original measured result |
|---|---:|---|
| `verilator --version` | 0 | 5.050 |
| `git fetch --no-tags origin refs/pull/13/head` | 0 | Historical figure-reference fetch |
| `bash scripts/lint_hdl.sh` | 0 | 37 LINT OK modules; zero-tolerance gate |
| `bash scripts/run_suites.sh` | 0 | 30 suites, **14,943 checks, 0 failing**; pp_top 1,411 |
| `make -j1 check` | 0 | 41 Mermaid + 18 WaveDrom blocks, 807 links, 115 REQ rows/17 GAP findings; module matrix 86 rows/0 untested; staleness gate |
| `python3 scripts/gen_matrix.py --check` | 0 | 86 rows, 0 untested |
| `bash syn/yosys/run.sh` | 0 | All 32 listed elaboration tops, plus KL_aecp_engine Xilinx mapping assertions: six RAMB36, one staging RAM |
| `make -C tb/nvm_port figures` | 0 | 42 derived Verilator builds; baseline 122/0; measured arms, mutations, models and five historical matrix builds agree |
| `git diff --check <base> <head>` | 0 | No whitespace error |

The reviewer summed the 30 positive suite rows to 14,943 and matched their names against every actual `tb/*/Makefile`; no SKIP, FAIL or UNREADABLE row contributes. `run_suites.sh` prints the last canonical tally and removes individual temporary suite logs, so its retained stdout is the suite summary. The affected pp_top has separate full author and reviewer build logs. The Yosys result is the complete donor script's actual 32-top population and Xilinx check, not an invented 37-top count. Yosys's memory/port resize warnings are retained. The nvm figure gate's expected negative model/mutation outcomes are successful comparisons, not extra passing suite checks; its explicitly unmeasured prose patterns earn no checks.

Hosted evidence was inspected read-only, with job metadata and all six raw logs retained in [public/](public/) and checked by [hosted_audit.py](scripts/hosted_audit.py). Earlier observations of running suites were not counted as passes. Final observations show:

| Actual hosted run | Checkout and completed result |
|---|---|
| [Push 35772526304](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/35772526304) | Checkout `e0c43b03f31d6c1220dd05a110e4bb30029233a0`; docs-gates, suites, portability all completed success |
| [PR 35772531911](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/35772531911) | Run head is the reviewed head; actual checkout is synthetic merge `e66e6eb9271ff045d9061449423331d47472ab12` into base f70ba36; all three jobs completed success |

Both actual suites logs report 14,943/0, pp_top 1,411/0, matrix freshness and completed 42-build figures. Only the cached Verilator rebuild step was skipped; test steps actually executed. These observations do not substitute for the manager's current-main candidate decision or post-merge collection.

[R252] PASS Conformance — `tb/pp_top/Makefile:15,22,59`; `raw/parser-results.json`; issue #102 acceptance. Requirement/evidence: both real CFLAGS groups satisfy immutable policy, and the fixture/product distinction is unchanged. Impact: the specific integration-policy defect is removed with effective warning coverage preserved. Required outcome: met; retain both flags and existing macro. Verification: real parser positive and each separate negative control, exact one-line comparison, generated CFLAGS and complete execution.

[R252] PASS RTL — `raw/source.diff`; `raw/evidence-audit.json`; `hdl/top/protocol_processor_top.sv:144,2147`; `hdl/srp/KL_srp_domain.sv:155–171`. Requirement/evidence: all RTL blobs are unchanged; the 16-bit parameter/default/binding and Domain transition contract remain intact. The actual diff proves no new clock/reset, CDC, resource, width or state-machine change requires implementation review. Impact: no product behavior or interface change. Required outcome: preserved, with no source correction required. Verification: direct contract/source inspection, independent default/DV execution and inspected manager lint/portability results.

[R252] PASS Robustness — `controls/`; `tb/pp_top/fixture_guards.py:20–60`; `tb/pp_top/sim_main.cpp:78–88,8297–8405`; `raw/pp-top-full.stdout.log`. Requirement/evidence: each missing flag is detected independently; 0002 and 1002 cannot masquerade as distinct fixtures; errors outside the expected assertion set fail the guard. Default/configuration separation, bridge adoption, down-link silence and re-declaration remain exercised. Impact: no weakening of refusal or configuration-sensitive coverage. Required outcome: met. Verification: real parser controls, actual four-case compile guards, locale regression and complete unchanged scenarios; no skipped scenario is credited.

[R252] PASS Tests — `tb/pp_top/Makefile:54–73`; `tb/pp_top/sim_main.cpp:8425–8465,9047–9076`; `raw/build-tally.txt`; `raw/evidence-audit.json`. Requirement/evidence: normal entry executes guards and both binaries; 1,391 + 20 is derived from actual executed checks, and the mandatory bank's 30 original counts sum to 14,943. The fixture remains sensitive to missing binding as its unchanged contract records; no test expectations or check sites changed. Impact: source acceptance is supported by executable evidence. Required outcome: met. Verification: independent focused run, exact recipe/selector/ELF identity and attribution-preserving audit of manager/native/hosted evidence.

[R252] PASS Docs — `raw/source.diff`; `docs/architecture/01_overview.md:166`; `docs/architecture/10_srp_engine.md:205`; `tb/pp_top/README.md:493–566`; `public/donor-issue-102.json`; `public/pr103.json`. Requirement/evidence: authoritative docs already describe unchanged product/default/fixture/Domain behavior; the actual diff contains no documentation or product contract alteration. The issue and PR correctly identify a per-group policy fix and expose reproducible evidence and outstanding workflow stages. Impact: no undocumented interface or obsolete Domain timing is introduced. Required outcome: met; no doc patch required for repeated build flags. Verification: public contract/history reconstruction, exact doc blob preservation, manager make-check and actual hosted docs results.

The reviewer-owned [ledger](LEDGER.json) records this round and full head for each lens:

| Lens | Covering round | Exact head | State |
|---|---|---|---|
| Conformance | R252-1 | e0c43b03f31d6c1220dd05a110e4bb30029233a0 | CLEAN |
| RTL | R252-1 | e0c43b03f31d6c1220dd05a110e4bb30029233a0 | CLEAN |
| Robustness | R252-1 | e0c43b03f31d6c1220dd05a110e4bb30029233a0 | CLEAN |
| Tests | R252-1 | e0c43b03f31d6c1220dd05a110e4bb30029233a0 | CLEAN |
| Docs | R252-1 | e0c43b03f31d6c1220dd05a110e4bb30029233a0 | CLEAN |

Limitations remain explicit. The author's extra parent warning-flags self-test attempt **failed with exit 2** after seven parser fixtures because the read-only parent clone lacked initialized processor submodules. Its [original raw output](evidence/author/logs/focused-cflags.log) and [failure account](evidence/author/ORIGINAL-FAILURES.md) are preserved; the required focused controls passed separately. No full parent checker/self-test pass is inferred. R252's initial tool-resolution assertion stopped before build because an intermediate `verilator_bin` was a Perl forwarder; the resolved ELF identity and successful later run are separately recorded. An initial hosted-log retrieval was refused by gh's terminal-escape output guard; that receipt is retained, followed by successful raw-file capture with its explicit output option. Neither acquisition/setup attempt is called green.

Historical PR13/6 continuity remains **UNKNOWN** and the **PR13/9 negative-review baseline** remains explicit. Passing current historical-figure comparisons does not clear those review-history conditions. This one-line task neither adopts a parent pin nor satisfies restored-PTOF prerequisites under parent #400/#403/#70 (or donor #61/#83 with #93/#94 prerequisites). R253 remains a separately required pending external review. No finding was deferred to another issue to obtain this ledger's CLEAN states.

Final audit: all 224 tracked paths match HEAD in bytes, file kind, executable mode and stage-0 index identity. No hidden/sparse index flags, replacement refs, gitlinks, tracked changes or untracked source changes were found. Only ignored pp_top build products were generated in the assigned checkout. The final audit and ignored-file inventory are under `raw/final-*`; [MANIFEST.json](MANIFEST.json) and [MANIFEST.sha256](MANIFEST.sha256) cover the delivered evidence. [COMMANDS.md](COMMANDS.md) provides reproduction commands. No GitHub state, source commit/ref, other checkout, parent policy or installed tooling was changed. This reviewer-owned packet is ready for faithful manager publication after terminal completion.

R252-1 FINISHED
