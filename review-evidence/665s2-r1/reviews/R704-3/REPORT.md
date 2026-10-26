[R704] POSITIVE - exact head f887663852d118e810ef690c3dd5cf9fe2292588

External independent delta review R704-3 of issue #665 / PR #792. All five lenses are CLEAN for this delta. No BLOCKER, MAJOR or MINOR remains from the reviewed changes or named prior findings. Four wording-residue items are recorded below. The expected T_svc miss is the measurement result, not a review finding or a timing-compliance approval.

Head tree: `cf2618f79f020ff486b2165ffd81f12e1146298d`. Source base: `e76a755afc0536453161e3cd33f6f4d2dcd7641f`; PR base branch: `dev-soft-core`. Reviewed delta: `cd3525c3ddcbdb5d78bf8fccdab354c468926997..f887663852d118e810ef690c3dd5cf9fe2292588`, seven files within `tb/verilator/ctrl_service_budget/`. The round-2 ledger stands outside this delta. Build code, testbench, SoC, firmware, shipping RTL, clocks, fixture trace, CI and workflows are unchanged (`scope-audit.json`).

Reconstruction followed AGENTS/CONTRIBUTING, docs/README, the issue's frozen public scope and decisions, requirements/interfaces, source-range inventory and independent delta/history inspection, then public executable evidence. Authorities include the [S2 acceptance](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6409745905), [original decisions](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6409738976), [round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6420330377), FR_NFR.md 3.4.1/3.4.2, MAILBOX_SPLIT.md service/backlog tables, mailbox.yaml and the firmware adapter contracts. The [later owner decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6421463860) puts instruction-cache evaluation before firmware-only tuning. These remain the no-cache baseline measurements.

My independent verdict and five-lens ledger were written before reading the other prior review report. Prior public findings were read only after the independent delta pass. No other current-round report, private author material or management scratchpad was read.

**Execution and evidence**

The [immutable public packet](https://github.com/kebag-logic/milan-fpga/tree/0b3e0e3ab108a6d66ed762da7c8766a15d250a97/review-evidence/665s2-r1) was exported by object identity. All 575 selected public files match their publication SHA-256 entries (`publication-check.json`). The publication commit has signature status `N`, and no detached signature file is present under its evidence prefix: this verifies immutable identity and digest consistency, not cryptographic signature authentication.

The head's self-test passes 81 checks and catches 52/52 mutants (`selftest.log`). Independently omitting SRP, MAAP or the four ACMP commands behind the owed input fails named population checks. Independently halving the composed maximum fails `fixture passes: worst pass and composed maximum` (`delta3-probes.json`). The source also tests a longest pass neither first nor last, the run's final pass, over-population, starvation, missing/wrong notification recipients, seven-response ordering, dropped commands, and duplicate control-path counting.

Both focused builds succeeded. Their linked ELF, ROM banks, firmware/configuration digests, cached CPU netlist and CPU/memory configuration match the published inputs (`delta3-probes.json`). Runtime archives and generated SoC text differ in raw digest across build directories; whole-build byte identity is not claimed. Cached CPU inputs were copied under scratch and generation disabled. The scoped simulator identified version 5.050 before use. Native compilation used `make -j16`, serialized between the two concurrent build drivers. Simulations ran concurrently with at most fifteen workers; observed unit memory peak was below 2 GB.

At each point I freshly ran `backlog`, `backlog-adp`, `backlog-adp-refill`, `backlog-owed`, `aecp`, and `aecp-fanout`. All twelve complete graded results equal the published results, and all twelve raw logs match the published hashes, including logs omitted from the public packet because of size (`native-audit.json`, `measurements/`). Both campaigns return zero with budget findings recorded and zero refusals. The selected 1x1 set has 50 misses among 83 instances, 17 among 49 paths; 8x8 has 63 among 101 instances, 29 among 67 paths. These are focused subsets, not full-campaign totals.

An independent raw decoder, which does not import the harness grader, checks receive-commit attribution, cumulative SRP release pointers, releasing-pass ends, composed maxima, ACMP response sequence order, and notification recipients/last commits (`audit_native.py`). Eight unchanged prior public stimulus/log pairs also regrade exactly at the current head (`unchanged-regrade.json`). Fourteen other available public raw traces regrade identically, and the full published counts and SHUTDOWN deduplication reproduce (`published-audit.json`).

| Fresh arm-A measurement | 1x1 | 8x8 |
|---|---:|---:|
| Composed maximum, completed load | 14.80520 ms | 27.84032 ms |
| SRP released in backlog-adp / refill | 0/32; 0/32 | 0/32; 0/32 |
| SRP first-record wait in those windows, lower bounds | 567.96826 / 628.31956 ms | 583.54194 / 658.79270 ms |
| SRP first / last under ordinary backlog | 84.10549 / 158.91864 ms | 131.24711 / 278.53608 ms |
| SRP first / last under owed backlog | 65.97072 / 182.68999 ms | 143.91252 / 340.84785 ms |
| SET_NAME to last required recipient | 11.33241 ms, 16 recipients | 20.68273 / 22.97921 ms, 32 recipients each |
| Owed response, full twelve-command ACMP load | 126.29163 ms | 161.10225 ms |
| Same response, measured from room return | 66.28867 ms | 101.09929 ms |

The owed windows independently decode responses `0x7380` through `0x7386`, in order, ahead of the measured `0x7387`. Each window commits ADP 8, ACMP 12, AECP 16, MAAP 7, SRP 32 and fifteen GM events. Other composed windows use the independently specified contract population; the refill row has ADP 11, and the event row adds LINK 1. The SRP-starved windows are explicitly excluded from the completed-load maximum and reported with unreleased counts and lower-bound waits. Their 31.32/44.19 ms passes remain visible. The commands dropped beyond ACMP's owed capacity are reported separately, not counted as successful responses.

Arm-B, SHUTDOWN and full-harness control evidence was assessed from source and verified published receipts, not rebuilt in this round. The public SHUTDOWN results are one path/two instances at 1x1 and two paths/three instances at 8x8. The three controls are reported caught. Published source-head gate receipts identify this head and report success, including 406/406 behavior scenarios; these remain the author's evidence. No manager source bank is claimed or inferred.

**Prior probes, unchanged**

`prior/probe_scenario_control.py`, `probe_delta.py`, `probe_native_delta.py` and `audit_receipts.py` are byte-identical to their public round-2 originals. The SRP-omission probe now fails two named checks. The endpoint, stale/missing input, absent-log and headline-mutation probes pass, and the admission-shortfall map is empty. The audit script's hard-coded `author-r2/receipts` input location was bound to the current public receipts in a separate scratch view; its code and expectations were unchanged.

The unchanged native driver reproduces the original owed-response figures above and the earlier two-recipient fan-out at 7.70397 ms (`prior-native-unmodified.log`). Its old augmentation adds four commands to a scenario that now already includes them. Consequently the new supplemental behind-input probes have `no start` in that disposable variant. This is recorded explicitly, not presented as a zero-refusal campaign or as proof of the new drop rows. The unmodified original probe's endpoint remains measured, and the corrected head's separate campaigns have zero refusals and verify the complete population. The old identity script's expected head was updated only in the separate current-head integrity script; no claim is made that the old head expectation passes.

**Prior-finding dispositions**

| Finding | Disposition at this head | Cause-level evidence |
|---|---|---|
| R704-2-F1; retained R704-1-F1 / R703-1-F1 load cause | Resolved | scenario.py:799 supplies twelve ACMP commands; grade.py:621 derives required counts independently of Group.load; selftest.py:51 restates them. Native populations and seven response identities match; omitted SRP, MAAP and trailing ACMP fail named checks. |
| R704-2-F2 | Resolved | scenario.py:922 canonicalizes the SHUTDOWN control to adp.shutdown; real-group count and differing-worst-instance checks pass; published totals deduplicate exactly. |
| R703-2-F1 | Resolved | grade.py:655, :695, :742 track releases, measured service and starvation. Raw SRP pointers and waits reproduce; README.md:362 reports per-window starvation. This resolves the missing measurement, not the firmware starvation itself. |
| R703-2-F2 | Resolved | scenario.py:529 registers sixteen controllers on every interface; grade.py:514 reports recipient cost. Fresh capacity endpoints and all measured fan-outs equal receipts; arm-B extensions are verified through public evidence. |
| R703-2-F3 | Resolved | selftest.py:368 checks an interior longest pass, final worst pass and over-population. Named first-pass/final-pass/over-load controls are caught; independent half-maximum plant fails the headline check. Published original N6/N8/N10 results also report caught. |
| R704-1-F2 / R703-1-F3 | Remains resolved | Complete causal recipient set and last-commit endpoint retained; unchanged late/missing-recipient traces and fresh capacity decode pass. |
| R703-1-F2 | Remains resolved | Clock ratio, pass origin and headline controls fail named checks; independent raw conversions match current rows. |
| R703-1-F4 | Remains resolved | run.py:66 retains worst-instance aggregation, now prioritizing starvation/drop rows; current published counts and path/interface deduplication reproduce. |
| R704-1-F3 / R703-1-F5 | Remains resolved | Unchanged build.py attestation; unchanged prior CLI probes reject changed/deleted ELF, ROM, SoC, CPU inputs and unresolved keys. |
| R704-1-F4 / R703-1-F6 | Remains resolved | Unchanged prior missing/partial-log probes refuse by name; explicit intact subset succeeds. |
| R704-1-F5 / R703-1-F7 | Remains resolved | Labelled SHUTDOWN entry and delay-control evidence retained; only path counting changed and is now corrected. |
| R704-1-R1 / R703-1-R-1 | Remains resolved | Previously named source-comment labels remain removed. No new prohibited lane/reviewer/round/comment-ID label found in added source comments. |
| R703-1-R-2/R-3 | Remains resolved | Module totals and completed versus unfinished composed-window figures are distinguished. |
| R703-1-R-4 / R704-2-R1 | Retained as R704-3-R1 | Suite-index sentence remains unchanged. |
| R703-2-R1 | Partially applied; source-docstring remainder retained as R704-3-R2 | README explains the own-channel exceptions; scenario.py:845 still says every input is last. |
| R703-2-R2/R3/R4/R5 | Resolved | Earlier-rule names, removed round clause, defined arm labels, per-interface path wording and full-event-ring explanation are present. |
| R703-1-S1/S2 | Remains applied | WIRE channel/interface ordering, timed-out waits and flash-cost range retained. |
| R703-2-S1/S2/S3 | Optional, retained | Refill phase sweep, checkout bytecode hygiene, and clarification of directory-dependent build digests. No clean lens depends on these suggestions. |

**Wording residue**

**R704-3-R1 - RESIDUE - Docs**

Artifact: `docs/testing/TESTING.md:518`. Authority/evidence: retained R703-1-R-4 / R704-2-R1; the suite index names only one manual Makefile exception. Impact: incomplete index wording; no executable or measurement change. Exact required outcome: replace the sentence with `The manual nvm_capture_cpu and ctrl_service_budget measurements are the Makefile exceptions.`, retaining code formatting and linking ctrl_service_budget to `../../tb/verilator/ctrl_service_budget/README.md`. Verification: inspect the sentence and relative link. This remains assigned to the manager's residue checklist because the file is outside this implementation scope.

**R704-3-R2 - RESIDUE - Docs**

Artifact: `tb/verilator/ctrl_service_budget/scenario.py:845`. Authority/evidence: retained source-docstring portion of R703-2-R1; the owed input is eighth of twelve, and the ADP refill population exceeds its initial burst. The code, assertions and result tables now represent this correctly. Impact: stale explanatory wording only. Exact required outcome: replace the opening three docstring lines with `Each composed window carries its row's defined load (#665; MAILBOX_SPLIT.md:753-758), including MAAP, SRP and fifteen grandmaster changes. The row's input is last on its channel except in the owed row, which places the remaining admitted ACMP commands behind it.` Keep the following refill explanation. Verification: compare with owed_group and defined_load; no generated script or result changes.

**R704-3-R3 - RESIDUE - Docs**

Artifact: `tb/verilator/ctrl_service_budget/README.md:352`. Authority/evidence: a new never-answered-command row now separates the owed-response row from `the same, from the moment the room returns`; the displayed numbers still correctly belong to the owed response (`native-audit.json`). Impact: ambiguous antecedent only; the measurement and figures are correct. Exact required outcome: replace that row label with `the owed response, from the moment the room returns`. Verification: figures remain 66.29 / 101.10 / 66.28 / 101.10 and no generated artifact changes.

**R704-3-R4 - RESIDUE - Docs**

Artifact: PR #792 body, Status and Known limitations. Authority/evidence: the later owner decision in issuecomment-6421463860 puts cache evaluation before firmware-only tuning; the body still presents the next step solely as S2b. Impact: stale sequencing prose, with no change to this measurement scope or verdict. Exact required outcome: replace `so owner decision D4's STOP into S2b stands` with `so the measurement STOP stands; the later owner decision puts instruction-cache evaluation before firmware-only tuning`, and make the corresponding Known limitations sentence point to that decision. Verification: follow the public decision link; retain every measurement and limitation.

These residue fixes change wording only. They do not change measurements, figures, test behavior, generated artifacts, conformance/clause claims or privacy rules, and do not make a lens unclean.

**Reviewer-owned delta ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen items 1-5; FR_NFR.md:337 and :407; MAILBOX_SPLIT.md:753; grade.py:435, :621, :695; scenario.py:529, :799, :909; twelve native groups and independent endpoint/population/count audits | R704-3 | f887663852d118e810ef690c3dd5cf9fe2292588 |
| RTL | CLEAN | mailbox.yaml admission/depths; KL_mbx_rx.sv receive commitment; ctrl_loop.c:121; srp_mbx.c:441; aecp.c:388; tsn-c-stack acmp.c:292; unchanged SoC/testbench and matched ELF/ROM/netlist; raw backpressure/release/response ordering | R704-3 | f887663852d118e810ef690c3dd5cf9fe2292588 |
| Robustness | CLEAN | grade.py:435, :655, :695, :742; starvation and dropped-command rows; full recipient capacity; three omission plants; seven-response ordering; prior stale/missing-input and absent-log probes | R704-3 | f887663852d118e810ef690c3dd5cf9fe2292588 |
| Tests | CLEAN | selftest.py:51, :368, :439, :480, :537; selftest_mutants.py; oracle.json against unchanged fixture.log; 81 checks/52 caught mutants; independent half-maximum and population plants; exact native/public comparisons | R704-3 | f887663852d118e810ef690c3dd5cf9fe2292588 |
| Docs | CLEAN | README result/limits tables; scenario/grade/run docstrings; public acceptance and PR body; hashed author gate receipts; prior-finding reconciliation and R1-R4 wording residue | R704-3 | f887663852d118e810ef690c3dd5cf9fe2292588 |

The RTL lens covers changed admitted-load/backpressure characterization and its dependency on firmware service, without reopening unchanged shipping architecture. This ledger approves the delta's measurement behavior, not product compliance or a merge candidate.

**Real limits and pending manager duties**

These are source-head simulation measurements at one phase per probe. Burst observations are not sustained-arrival bounds; pass bounds apply to the same passes. SRP service ends at the end of its releasing pass, not proof that retained lwSRP replay completed. A window left unfinished yields a measured lower bound. The linked fixture, placeholder devices, region-decode cover, unavailable observation ports in arm A, zero flash erase/program waits, polling loop, absent media/DDR and idle DMA remain limitations. START_STREAMING, lock-expiry notifications and counter pushes are not measured. Capacity testing covers the command-triggered fan-outs implemented in these scenarios; it does not certify those omitted asynchronous paths. Mailbox commits do not prove wire/network deadlines. Physical calibration was NOT RUN; field skips are not hardware proof.

The manager must publish this packet, carry the four residue items, reconcile the independent reviews, and disposition the measured SRP starvation, ACMP owed-capacity drops and fan-out cost in the follow-on work. Cache-first evaluation follows the latest owner decision, using this corrected baseline. Hosted/act acceptance remains the manager's; I did not inspect or claim executed hosted jobs. The manager must build and validate the final current-dev merge candidate, publish its builder/native receipts, obtain explicit merge authorization and perform post-merge containment. This review does not validate integration with live dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee`, authorize a merge, or close the broader issue.

No source fix, commit, push, GitHub write, author contact, sub-agent, prohibited bank, Docker/act, hardware access, shared installation or other-checkout edit was performed. Disposable inputs/builds are under this packet's scratch directory. `identity-final.json` verifies exact tracked blob bytes, file types/modes, index and all five required initialized submodule gitlinks and contents; the unrelated external submodule remains uninitialized. `MANIFEST.sha256` lists publishable receipts, excluding scratch. Driver metadata paths are normalized by role; numerical raw traces and the prior probe scripts are unchanged, with digests recorded in `receipt-index.json`.

R704-3 FINISHED
