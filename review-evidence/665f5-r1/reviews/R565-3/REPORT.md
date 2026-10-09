[R565] POSITIVE - exact head fb9c57d2ae3484804ff90f67feb57bf420c93dfa

R565-3 external independent delta review of issue #665 / PR #700.
Tree: `762bda168ec58bfdd05f1c9394fea28b0696b9a5`.

R564-2-F1 is **RESOLVED**. All nine round-1 findings remain resolved. All five lenses are CLEAN at this head. No BLOCKER, MAJOR or MINOR remains from this review. One publication-status wording residue remains. This verdict concerns the reviewed source head; it does not declare merge readiness.

## Scope and reconstruction

Read the operating contract, CONTRIBUTING, documentation index, frozen F5 acceptance and public manager decisions, requirements and interface authorities before the implementation delta. Inspected the full PR's changed-path inventory and history from `5603c353137e90c1fa95429f6d00ef7a2298d9ee`, then the complete round-3 diff from `0ded1f269a44d107498f177c8276665656e07d30`. The full PR changes 38 files; round 3 is two commits changing six test/documentation files. No production source, RTL, configuration, generated output or submodule pin changes in round 3. Prior public findings were read only after the independent delta pass. No other reviewer report file, private author material or lane scratchpad was read.

Public authorities and evidence:

- [F5 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081266905), [224 KB ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081705916), [round-2 correction scope](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6085423196), and [frozen round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6086491737).
- `REQUIREMENTS.md:23`, `docs/reference/FR_NFR.md:330`, `docs/ARCHITECTURE_HW_SW_SPLIT.md`, `docs/design/MAILBOX_SPLIT.md:115`, `aecp.h:78`, and issues #678, #653 and #637. Clause checks use IEEE 1722.1-2021 7.4.15.1 and Milan v1.2 5.4.2.9 as explicitly resolved by the public round-3 decision; no new standards interpretation is introduced.
- [Original published executable packet](https://github.com/kebag-logic/milan-fpga/tree/c7078141c09865a979913272774331198a209b2f/review-evidence/665f5-r1), followed by [published round-3 author receipts](https://github.com/kebag-logic/milan-fpga/tree/69f1bf91ca30964676749e131d5e3fb7383570b6/review-evidence/665f5-r1/author-r3). The older packet is historical evidence, not exact-head execution evidence.

## Round-3 finding disposition

**R564-2-F1 | MINOR | Conformance, Tests, Docs | RESOLVED**

Artifacts: `sw/firmware/ctrl/test/test_aecp.cpp:780`, `:810`; `aecp_wire.cpp:56`; `aecp_wire_oracle.py:91`, `:187`; `sw/firmware/ctrl/aecp/README.md:154`; unchanged `aecp_commands.c:276`.

Authority/evidence: XXX_VALID selects the sub-command. Without MSRP_ACC_LAT_VALID, no latency is applied and the response reports current latency. Milan's request echo is conditional on that flag. The native loop now requests 765432 against stored 123456. The added test covers flags 0/4/8/12 both before a saved override (observation 12345, untouched store) and after one (123456), checking the response, full store, override bit, change callback and peer-notification count. Repeated commands also preserve state.

The differential first stores 67890, then requests 765432 without the latency-valid flag. Its oracle uses current latency when the flag is clear and requested latency only on successful valid-latency SET. The seventh observation control substitutes the request value and requires the exact `SET requested or current latency` diagnostic. The README states the exception. Core code is byte-identical to round 2.

Impact addressed: an unrequested persistent latency change or request-echo response can no longer pass these checks by equality of stimulus values. Required outcome is satisfied without changing production behavior.

Verification: both unchanged reviewer plants were rerun against the complete 70-test, two-interface composed suite. Each returned 1 through completed assertion failures in **both** `Core.SetStreamInfoReportsCurrentFieldsOnSuccessAndRefusal` and `Core.SetStreamInfoWithoutSubcommandPreservesState`. Neither was a build failure or crash. The maintained table's diagnostic grader independently caught both plants and `nosub-notifies-change`. See `receipts/review-mutants/` and `receipts/named-plants/`.

## Earlier findings retained as resolved

All paths below are relative to `sw/firmware/ctrl/`. The unchanged public probes were rerun; standing tests also passed in both composed interface arms.

| Finding | Original severity / lenses | Current artifact and evidence | Disposition |
|---|---|---|---|
| R565-1-F1 | MAJOR / Conformance, Robustness, Tests | `aecp/aecp_commands.c:84`; `test/test_aecp.cpp:565`; root configurations 1/65535 normalize to zero; invalid indices and ordinary configuration checks remain | RESOLVED |
| R564-1-F1 | MINOR / Conformance, Robustness, Tests | Same root-descriptor implementation; unchanged P1 and Q3 probes pass | RESOLVED |
| R565-1-F2 | MAJOR / Conformance, Tests | `aecp/aecp_commands.c:300`; `test/test_aecp.cpp:780`; nonzero current format/ID/MAC/VLAN and refusal fields checked; unchanged current-fields probe passes | RESOLVED |
| R564-1-F2 | MINOR / Conformance, Robustness, Tests | `aecp/aecp_commands.c:329`; `test/test_aecp.cpp:794`; ignored flags succeed and unsupported valid sub-commands remain atomic; P2 passes | RESOLVED |
| R565-1-F3 | MAJOR / Conformance, RTL, Robustness, Tests | `aecp/aecp.c:459`; `test/test_aecp.cpp:1016`; unavailable events retained with timed retry while independent events progress | RESOLVED |
| R564-1-F5 | MINOR / Conformance, RTL, Robustness, Tests | Same retry path; P6 delivers both later counter notices; Q1 performs 1000 reads over 1000 ms despite five polls/ms, with zero busy polls | RESOLVED |
| R565-1-F4 | MINOR / Conformance, RTL, Robustness, Tests, Docs | `aecp/aecp.c:5`; `test/test_aecp.cpp:580`; real cross-instance inputs, initialization-before-clear protection and diagnostic guard pass; guard-order mutation fails | RESOLVED |
| R564-1-F3 | MINOR / Conformance, Robustness, Tests, Docs | `aecp/aecp.c:280`; `test/test_aecp.cpp:1298`; HDCP fixed header returns typed NOT_IMPLEMENTED with zero data; P3/Q4 pass; README message-type table records remaining differences | RESOLVED |
| R564-1-F4 | MINOR / Conformance, RTL, Tests | `aecp/aecp_commands.c:102`, `aecp/aecp_mbx.c:94`, `app/ctrl_app_aecp.c`; `test/test_aecp.cpp:388` reads the real ADP advertisement count, also `:1288` tests interface observation | RESOLVED |

R564-1-RES1 is resolved by `docs/design/MAILBOX_SPLIT.md:568`. The old P5 probe's printed “no ADP port exists” label is historical fixture wording and is not evidence for available_index; the composed advertisement-count test provides that evidence.

Prior SUGGESTIONs remain optional and unchanged: R564-1 S1 (known unsupported-command response sizing/common command model), S2 (future descriptor-name applicability), S3 (time-limited registration disposition); R564-2 S1 (retry backoff), S2 (adapter-level guard scope), S3 (output failure-valid flag consistency). Their original lenses and nonblocking disposition are retained; none is claimed implemented or used to conceal an open required fix.

## New residue

**R565-3-RES1 | RESIDUE | Docs | PR #700 body, Status paragraph**

Authority/evidence: `receipts/pr-status-snapshot.json` confirms the published head is `fb9c57d2ae3484804ff90f67feb57bf420c93dfa`, while the body says the two round-3 commits are unpushed and the PR remains at `0ded1f26`. This is the round-3 instance of R564-2-RES1's stale publication wording.

Impact: readers receive stale publication instructions. It changes no measurement, code, test, generated artifact, conformance claim or review verdict.

Required exact fix: replace the first two Status sentences with: “Implementation head `fb9c57d2ae3484804ff90f67feb57bf420c93dfa` is the published PR head on `665-f5-aecp` targeting `dev`.” Replace “After the authorized owner publishes the candidate:” with “To check out the published candidate:”. Preserve the gate and independent-review qualifications.

Verification: compare the revised publication wording with the current PR head. Manager carries this to the residue checklist. No GitHub write was made by this reviewer.

## Executed evidence at this head

| Check | Result | Receipt |
|---|---|---|
| Firmware bank, `--require-rv32 --jobs 4` | 59 arms, 65 tallies, 1408 checks, zero failures | `receipts/firmware-bank.log`, `firmware-tally.json` |
| Complete composed AECP suite, interfaces 1 and 2 | 70/70 tests on each | `receipts/aecp-suite.log`, `gates.json` |
| Unchanged earlier probes | R565-1 4/4; R564-1 8/8; R564-2 5/5 at each interface count | `receipts/prior-probes.log`, `probe-provenance.json` |
| Unchanged R564-2 five source plants | All caught by completed assertion failures; both latency plants fail both required tests | `receipts/review-mutants/` |
| Three maintained round-3 source plants | All required named diagnostics caught; includes no-subcommand notification defect | `receipts/named-plants/` |
| Fresh wire differential, pinned one-interface reference | 132 observations, 42 descriptors, command/notification census, seven controls | `receipts/wire-one/` |
| Fresh wire differential, merged #69 two-interface reference | 137 observations on each ingress, seven controls per ingress | `receipts/wire-two/` |
| Default mailbox target, `make -j16` | Both buses, both interface counts, firmware co-simulation, host checks; all five quick plants caught | `receipts/mailbox-bounded-runtime.log`, `mailbox-bounded.json` |
| `gen_mailbox.py --check` | PASS | `receipts/mailbox-generator.log`, `.rc` |
| Raw tracked bytes, modes, index and required gitlinks | PASS; 1264 parent files and four initialized pinned submodules; clean status | `receipts/integrity-final.json` |

The scoped simulator identified itself as 5.050, revision v5.050, before use. Reference inventories were content-checked by the differential driver. Every disposable tree and build stayed under `scratch/`; no candidate source bytes were edited. The mailbox runtime receipt contains verbatim test/tally lines; full compiler chatter remains in unpublished scratch.

The initial mailbox invocation overlooked the campaign's nested four-worker/four-compiler default, so configured concurrency could exceed sixteen while other gates ran. Actual peak compiler count was not sampled. Its evidence is superseded by a fresh complete run explicitly passing `--jobs 1`, with `VBUILD_JOBS=1` and `make -j16`; subsequent scheduling stayed within sixteen. Peak unit memory was 5,765,459,968 bytes, below 12,884,901,888. All commands were foreground children and were joined before completion. See `receipts/execution-limits.json`.

## Published source-head link and gate evidence

The author's exact-head receipt table contains 32 successful command records, including the source-head builder, coverage, sanitizer, source mutation and documentation families. These are author executions, not manager source banks and not executions claimed for this review.

The round-3 size table and final link log report:

| Shape / interfaces | text | rodata | data | bss | stack | RAM span |
|---|---:|---:|---:|---:|---:|---:|
| Shipping / 1 | 82932 | 11950 | 56 | 37252 | 8192 | 140400 |
| Shipping / 2 | 84220 | 11950 | 56 | 48620 | 8192 | 153056 |
| Largest / 1 | 82980 | 25158 | 448 | 77428 | 8192 | 194224 |
| Largest / 2 | 84356 | 25158 | 448 | 103556 | 8192 | 221728 |

Static pools are included in BSS. I compared the published round-2 and round-3 section and pool tables: all four match. The author reports byte-identical load images; no new independent link was performed in this delta review. The unchanged production/link inputs support retention of the 221728-byte source-head result, with 2272 bytes below the stricter decimal 224000 ceiling. Nominal 49 versus 32-bit-packed 55 memory tiles still require routed integration proof. Source receipts and provenance are under `receipts/published/` and `published-provenance.json`.

There is **no manager source bank at this head**, and none is inferred. Source base is `5603c353137e90c1fa95429f6d00ef7a2298d9ee`; live dev observed for this review is `7c1b52bee26b497080ee22b1c1986109f80a5ee7`. The current-dev merge candidate is a distinct tree that the manager builds and validates at the merge turn.

## Reviewer-owned lens ledger

Each lens was applied in this round to the delta and relevant unchanged contracts/fix paths, with fresh regression evidence. CLEAN is scoped to this source review and does not discharge pending merge gates.

| Lens | CLEAN/UNCLEAN | Examined artifacts and result | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `aecp_commands.c:276`, `test_aecp.cpp:780`, `aecp_wire_oracle.py:91`; conditional latency rule, ignored flags, current response fields, root reads and typed refusals agree with public clause decisions | R565-3 | fb9c57d2ae3484804ff90f67feb57bf420c93dfa |
| RTL | CLEAN | Full changed-path inventory has no RTL change; `aecp.h:78`, `aecp.c:5`, `:459`, `aecp_mbx.c:139`, application bridge and bounded mailbox gate preserve ownership, callback, retry and completion contracts | R565-3 | fb9c57d2ae3484804ff90f67feb57bf420c93dfa |
| Robustness | CLEAN | `test_aecp.cpp:810`, `:1016`, `:1213`, `:1298`; repeated no-ops, state/override retention, callback silence, unavailable providers, backpressure, timer pace, malformed/non-AEM inputs and both interfaces pass | R565-3 | fb9c57d2ae3484804ff90f67feb57bf420c93dfa |
| Tests | CLEAN | `aecp_mutants.py:35`, `aecp_wire_oracle.py:187`, full firmware/AECP logs, unchanged probes and source-plant diagnostics prove the targeted regressions fail named assertions | R565-3 | fb9c57d2ae3484804ff90f67feb57bf420c93dfa |
| Docs | CLEAN | `aecp/README.md:98`, `:154`, `:160`; frozen assignment, public source receipts and PR contract agree on behavior and evidence limits; only R565-3-RES1 wording residue remains | R565-3 | fb9c57d2ae3484804ff90f67feb57bf420c93dfa |

## Real limits and pending manager duties

- `gh pr checks` returned 8 because jobs remain pending. Exact-head records show successful executed lint, BDD, wire-accountability, docs-no-git, selector and four synthesis shard jobs. Five simulation shards, firmware-unit, yosys-elaboration, docs-check and elaborate were still in progress. The physical gPTP job was **skipped**. No successful exhaustive aggregate or final `rtl-fast` result is asserted. See `receipts/hosted-final.log` and `hosted-final-check-runs.json`. Hosted/local-replica acceptance belongs to the manager.
- No full parent, processor, gPTP, synthesis or builder bank was run by this reviewer. No hardware, physical calibration, routed fit, stack call-chain bound or shipping-image acceptance is claimed. The author's missing physical-calibration row is **NOT RUN**; field skips are not hardware proof. Protocol/reference simulation and mailbox acceptance are desk evidence.
- The manager must finish hosted and authorized local-replica acceptance, validate the latest current-dev merge candidate with builder and native banks, and publish its receipts on the PR. No source-head result substitutes for that candidate validation.
- Finish the independent internal review and confirm no review round remains in flight; apply the full CONTRIBUTING merge bar and require explicit maintainer authorization. After merge, perform the required containment and review-integrity checks and reconcile the issue/lane state. Issue #665 has wider integration obligations; this F5 source verdict does not close them.
- Carry the publication residue and the retained optional suggestions in public state. Physical observer wiring, timing/stack calibration, routed memory fit/reserve, the common command model and later default-flip acceptance remain separate integration duties.

Portable reproduction scripts and raw runtime receipts are listed in `MANIFEST.sha256`; only listed files and this report are publishable. `scratch/` is excluded.

R565-3 FINISHED
