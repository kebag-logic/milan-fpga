# [A273] REVIEW READY

Author handoff for PR #114 / issue #112, merge round.

- Assignment: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/112#issuecomment-5818554274
- Branch: `112-stale-grant`.
- New head: `f222f6b96328c8eb0f4d2c5c3470ebd365e51fdc`.
- First parent: `ae7f531bc97a7277116e0df78e70c84396c499d0`.
- Second parent: `7a47f5788ff504f099a47ad4407c340771bb6bdb`.
- Merge base: `939c143333d11e2378a514f1c7b6abd4c3259bfd`.
- Commit subject: `Merge main into 112-stale-grant preserving admission and stream info changes`. One line, no body or trailers.

`git fetch origin main` returned the specified main head. A single `git merge --no-ff --no-commit 7a47f5788ff504f099a47ad4407c340771bb6bdb` was resolved and committed. The first-parent history contains exactly one new commit. No rebase, push, PR edit, merge into main, parent commit, or hardware action was performed.

## Conflict resolution

| File and final line | Resolution |
|---|---|
| `syn/ooc/README.md:87` and `:133` | Retained the complete #112 SRP admission recipe and base/round-1/round-2 area table, including pending-round and register-accounting notes; appended main's complete #43/#49 GET_STREAM_INFO 8x8/1x1 area table and ownership explanation. Main's processor recipe notes at the beginning also survive. These are the original dated measurements; no combined area or hardware result is claimed. |
| `tb/srp_top/README.md:14`, `:88`, `:103`, `:121`, `:175` | Resolved the conflicting live tally to **1,531**, confirmed by the merged suite (1,527 branch checks plus main's four FailureInformation checks). Retained all H/I/J freshness, pending-capacity and optimistic-window notes and main's section-D FailureInformation/mutation notes. Historical mutation tallies remain tied to their original campaigns. |

[merge-resolution.diff](merge-resolution.diff) records the complete remerge diff: only those two README resolutions required manual changes.

## Clean-merged overlap and interaction review

The merge base is 939c1433 (full SHA in merge-metadata.json). Comparing both parents with that base finds eight shared changed files: two conflicted READMEs and the six clean merges below. Every shared file was checked against both parent diffs and its merged contents. branch-overlap.diff and main-overlap.diff preserve those comparisons. The eight branch-only files and eighteen main-only files match their respective parent byte for byte. The remerge diff contains only the two README conflict resolutions.

| Clean-merged overlap | Checks and result |
|---|---|
| `hdl/srp/KL_srp_top.sv:192`, `:214`, `:420`, `:622`, `:759`, `:785`, `:864` | The new sink FailureInformation strobe and raw bridge validity comment survive beside the source admission ports. Accepted talker gate operations still invalidate the current slope; only published admission rounds age the optimistic window. The listener instance forwards FailureInformation and its dedicated change strobe directly. Neither the listener path nor its notification depends on admission round completion. |
| `hdl/top/protocol_processor_top.sv:514`, `:2209`, `:2289`, `:3052`, `:3089`, `:3097`, `:3134` | The confirmed-admission contract and unchanged source grant wiring survive. GSI input selection still checks kind/type and the full descriptor index, substitutes only selectors 4/5/7, gates the raw bridge on the selected sink's FAILED state, and reads committed listener pbsta/acmpsta. The failure-change strobe feeds only the input notification OR. Source admission, optimistic ACTIVE, and source notifications retain their separate owners. |
| `tb/srp_top/sim_main.cpp:308`, `:333`, `:368`, `:515`, `:721`, `:1103` | Failure-change counters sample the low phase once; admission samples retain acceptance before the edge and resulting grants after the edge. Section D retains all four new checks for changed/unchanged FailureInformation and wire silence. Sections H/I/J remain invoked and retain the phase sweep, refusal/capacity/wire assertions, and held-verdict optimistic-window checks. Reset clears captured traffic between the admission scenarios. |
| `tb/srp_top/srp_top_wrap.sv:77`, `:104`, `:117`, `:221` | The GSI-related failure-change output is connected to the real listener output; all five admission probes remain read-only hierarchical observations of the real gate, round phase, optimistic window, and join tick. No test input drives those observed states. |
| `docs/architecture/10_srp_engine.md:276`, `:292`, `:334`, `:354`, `:378`, `:398` | Current-declaration validity, whole-round holds, latency, published-round window aging, and held aggregate snapshots remain documented. The separate listener section retains main's changed-FailureInformation self-loop, notification-only behavior, unchanged-refresh silence, and raw-bridge gating contract. The source admission hold does not become a sink registration or listener redeclaration event. |
| `docs/guides/integrator.md:254`, `:284`, `:300` | The service/admission notes and ACTIVE AND real-grant guidance coexist with the internal input GSI ownership notes. Input selectors 5/7 remain internal; selector 4 still takes the external destination MAC and substitutes the failure byte. Existing output words remain the integrator's responsibility. |

Interaction conclusion: #112 can delay publication of source admission verdicts and the resulting local talker declaration transition. #111 reads received talker registration/failure state for STREAM_INPUT and the committed ACMP listener record. Its readers do not sample source grants or pending-round state. The admission hold does not gate RX processing, GSI gathering, or the dedicated failure-change notification. GSI input field changes cannot invalidate source slopes or age the optimistic window. The merged full processor suite exercises both paths; the SRP service suite retains source/wire tests and the added sink failure-refresh tests. Both mutation campaigns provide their named negative checks. This is an author coherence check, not independent review approval.

## Gate execution

Every listed gate completed with its own rc 0. Commands ran in the foreground, directly to log files, with no output pipeline; gate timeouts were three hours each (the mutant runners also enforce their own per-build limits). The common environment prepended `$VALIDATION_TOOLS/verilator-v5.050/bin` to PATH and limited each process tree to eight available CPUs. [environment.json](environment.json) records exact versions. Toolchains and temporary build trees remained outside this output directory.

The sole processor workflow is `.github/workflows/hdl.yml`; all of its verification steps are represented below, including the history fetch required by the NVM figure gate. Diagram lint is additionally included. The suite-bank command covers both PRs' suites, including the full default/fixture processor runs and admission shapes 1, 2, 3, 5, and 8.

### Processor gates

| Command | rc | Evidence |
|---|---:|---|
| `python3 scripts/check-links.py` | 0 | [links.log](links.log) |
| `python3 scripts/check-matrix.py` | 0 | [matrix.log](matrix.log) |
| `python3 scripts/render-wavedrom.py --check` | 0 | [wavedrom.log](wavedrom.log) |
| `make stale` | 0 | [stale.log](stale.log) |
| `make lint` | 0 | [diagram-lint.log](diagram-lint.log) |
| `./scripts/lint_hdl.sh` | 0 | [hdl-lint.log](hdl-lint.log) |
| `./scripts/run_suites.sh` | 0 | [suite-bank.log](suite-bank.log) |
| `python3 scripts/gen_matrix.py --check` | 0 | [module-matrix.log](module-matrix.log) |
| `git fetch --no-tags origin refs/pull/13/head` | 0 | [figure-history-fetch.log](figure-history-fetch.log) |
| `make -C tb/nvm_port figures` | 0 | [nvm-figures.log](nvm-figures.log) |
| `./syn/yosys/run.sh` | 0 | [yosys.log](yosys.log) |

Documentation checks covered 855 links, 115 requirement rows (with 17 recorded GAP findings), 18 waveform diagrams, and 41 sequence/state diagrams; all gates returned rc 0. HDL lint passed all 40 module tops. The generated traceability matrix passed with 92 rows and zero untested modules. The NVM figure gate completed 46 builds (one baseline, 12 arms, 22 mutations, six historical models, five matrix cases), and every measured figure agrees. Portability passed 35 top elaborations and the complete AECP engine memory-mapping assertion: one staging RAMB36 and six RAMB36 blocks in total.

The full bank passed **33 suites / 1,008,919 canonical checks**, with zero failing or unreadable suites. Its aggregate counts the final admission shape as specified by the repository runner; the smaller shapes execute before it.

| Suite | Checks | Result |
|---|---:|---|
| `acmp_listener` | 2,544 | PASS |
| `acmp_nvm` | 349 | PASS |
| `acmp_talker` | 839 | PASS |
| `adp_engine` | 533 | PASS |
| `aecp_notify` | 10 | PASS |
| `ca_originator` | 16 | PASS |
| `desc_mem_guard` | 78 | PASS |
| `desc_store` | 584 | PASS |
| `dispatch` | 211 | PASS |
| `dyn_state` | 89 | PASS |
| `event_router` | 81 | PASS |
| `lsn_admit` | 18 | PASS |
| `maap` | 75 | PASS |
| `nvm_port` | 136 | PASS |
| `originator` | 104 | PASS |
| `pp_top` | 1,948 | PASS |
| `prng` | 76 | PASS |
| `release_merge` | 18 | PASS |
| `resp_buf` | 64 | PASS |
| `rx_slots` | 130 | PASS |
| `rx_validator` | 393 | PASS |
| `scoreboard` | 3,705 | PASS |
| `side_port` | 368 | PASS |
| `srp_admission` | 991,231 | PASS |
| `srp_decoder` | 190 | PASS |
| `srp_encoder` | 556 | PASS |
| `srp_stream_fsms` | 1,087 | PASS |
| `srp_top` | 1,531 | PASS |
| `timer_map` | 1,360 | PASS |
| `timer_service` | 48 | PASS |
| `tx_arbiter` | 66 | PASS |
| `tx_slots` | 95 | PASS |
| `ucpu` | 386 | PASS |

### Mutation gates

| Command | rc | Evidence |
|---|---:|---|
| `python3 tb/pp_top/gsi_mutants.py --output $MANAGEMENT/2026-09-23/pp112-a273/gsi-mutants` | 0 | [gsi-mutants.log](gsi-mutants.log) |
| `python3 tb/srp_admission/mutants.py --output $MANAGEMENT/2026-09-23/pp112-a273/admission-mutants` | 0 | [admission-mutants.log](admission-mutants.log) |

The GSI campaign detected all **13 mutants by their required named checks**. All 15 builds succeeded; golden and restored controls each completed 488 checks with rc 0. Each mutant simulation returned rc 1, as required, rather than failing to build. See [gsi-mutants/results.json](gsi-mutants/results.json).

| GSI variant | Build rc | Run rc | Expected verdict |
|---|---:|---:|---|
| `golden` | 0 | 0 | Control passes |
| `failure-code-zero` | 0 | 1 | Named check detects mutant |
| `failure-bridge-zero` | 0 | 1 | Named check detects mutant |
| `pbsta-zero` | 0 | 1 | Named check detects mutant |
| `acmpsta-zero` | 0 | 1 | Named check detects mutant |
| `wrong-sink` | 0 | 1 | Named check detects mutant |
| `integrator-path` | 0 | 1 | Named check detects mutant |
| `missing-descriptor-leak` | 0 | 1 | Named check detects mutant |
| `status-notification-zero` | 0 | 1 | Named check detects mutant |
| `rebind-started-trigger-removed` | 0 | 1 | Named check detects mutant |
| `failure-change-strobe-removed` | 0 | 1 | Named check detects mutant |
| `failure-change-redeclares` | 0 | 1 | Named check detects mutant |
| `index-guard-removed` | 0 | 1 | Named check detects mutant |
| `bridge-gate-removed` | 0 | 1 | Named check detects mutant |
| `restored` | 0 | 0 | Control passes |

The admission campaign passed **12/12 verdicts**: three clean controls and each of three mutants in the two-source, eight-source and real-service SRP suites. Controls passed 12,615 / 991,231 / 1,531 checks respectively. Mutant `make` invocations return rc 2 because their completed simulations report expected failed assertions; the enclosing campaign returns rc 0 only when the named check detects every mutant.

| Admission variant | 2 sources | 8 sources | SRP service suite |
|---|---|---|---|
| `control` | rc 0, PASS | rc 0, PASS | rc 0, PASS |
| `stale-evaluation` | Named check detects mutant | Named check detects mutant | Named check detects mutant |
| `pending-absent` | Named check detects mutant | Named check detects mutant | Named check detects mutant |
| `discarded-round-strobes` | Named check detects mutant | Named check detects mutant | Named check detects mutant |

Individual logs are in [admission-mutants](admission-mutants), with the full campaign verdict in [admission-mutants.log](admission-mutants.log).

### Parent consumer gates

Working directory: `$LANES/pp112-parent-consumer`. The local merge head was fetched, checked out detached in `protocol-processor`, and staged before the quality and integration gates. The required reset ran afterward.

| Command | rc | Evidence |
|---|---:|---|
| `git -C protocol-processor fetch $LANES/pp112-stale-grant HEAD` | 0 | [parent-fetch.log](parent-fetch.log) |
| `git -C protocol-processor checkout --detach FETCH_HEAD` | 0 | [parent-checkout.log](parent-checkout.log) |
| `git add protocol-processor` | 0 | [parent-add.log](parent-add.log) |
| `python3 scripts/check_cpp_idiom.py` | 0 | [parent-cpp.log](parent-cpp.log) |
| `python3 scripts/check_py_idiom.py` | 0 | [parent-py.log](parent-py.log) |
| `python3 scripts/check_rtl_source_lists.py` | 0 | [parent-source-lists.log](parent-source-lists.log) |
| `make -C tb/verilator/pp_shadow -j8` | 0 | [parent-pp-shadow.log](parent-pp-shadow.log) |
| `git reset -q protocol-processor` | 0 | [parent-reset.log](parent-reset.log) |

The integration suite passed **371 checks / 0 failures**. Parent HEAD remains `54112923417837dffc8722890e2beb733468f441`. Its index again contains the original processor pin `73a5478784bd861f8c8d33c0d1619594390b9529`; the submodule working checkout remains at the tested merge head as requested. The parent already had an unstaged submodule difference before this round. There are no staged changes and no parent commit.

## Final state

The processor working tree is clean, both expected parents and the one-line commit message are verified, and all required gates are green at the new head. The six clean overlaps required no manual code changes. No interaction defect was found between GSI input ownership and the source admission hold. Independent review remains the next step; this handoff makes no reviewer approval claim.
