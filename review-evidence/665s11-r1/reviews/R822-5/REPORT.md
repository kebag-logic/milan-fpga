[R822] POSITIVE - exact head d3566d44dcae75069f56d97402a5f1b351743008

Independent round R822-5, issue #871 / PR #881. Tree `32693acb2b16ca8dc329fd20fcbc6b92f2b45db3`. Delta from accepted `049f0e4dd7b0b514d1ea9689822901750129c044`, including this lane's conflict resolution when importing `41ca9f87`. No BLOCKER, MAJOR or MINOR found. The residue below does not unclean a lens. This verdict and ledger were written before reading prior reviewers' findings; their reconciliation follows separately.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #871 acceptance/rulings; #665 ruling 6894152131 item 1; processor docs/architecture/06_aecp_engine.md 6.11; aecp_commands.c:596; aecp.c:280,594,917,969; timing survey | R822-5 | d3566d44dcae75069f56d97402a5f1b351743008 |
| RTL | CLEAN | Merge 6cfdf650 combined diff; sw/litex/milan_soc.py:3308; unchanged reset/crossing path; CSR exports; ctrl_loop.h:284; memory ledger and build input hashes | R822-5 | d3566d44dcae75069f56d97402a5f1b351743008 |
| Robustness | CLEAN | test_plat_boot.cpp:797,872,907,1089; test_aecp.cpp:3062; ctrl_reboot/run.py:672 and sim_main.cpp:105; twelve plant/control receipts; focused retry mutation | R822-5 | d3566d44dcae75069f56d97402a5f1b351743008 |
| Tests | CLEAN | aecp_reboot_mutants.py; aecp_owed_mutants.py:34; record_classes.py:142,195,274; sweep/campaign census; independent baseline, mutations and model controls | R822-5 | d3566d44dcae75069f56d97402a5f1b351743008 |
| Docs | CLEAN | REBOOT_RESET.md section 8; SPLIT_CONTROL_MEMORY.md sections 3,5,13; FR_NFR.md 3.4.1; AECP/platform/budget/REBOOT READMEs; REVIEW READY and archive inventory | R822-5 | d3566d44dcae75069f56d97402a5f1b351743008 |

Findings

**R822-5-R1 — RESIDUE — Docs — sw/firmware/ctrl/test/test_plat_boot.cpp:187 and sw/firmware/ctrl/test/plat_mutants.py:262.**

Authority/evidence: the owner's comment rule forbids new bench labels in source comments. Added/reflowed lines retain `ADP's TX_TAIL as the driver reads it (B18)` and `B23's AECP words)`.
Impact: wording only; no assertion, diagnostic, measurement or executable behavior changes.
Required outcome: remove `(B18)` from the first comment. In the second, replace `B20` with `NoOtherChannelTransmitsAfterTheDeparting`, `B19` with `NoFrameOfAnyChannelIsTakenFromTheSuccess`, and `B23` with `TheGateHoldsWhileTheResponseCannotBeHandedOver`. Leave test identifiers and required failure diagnostics unchanged. This also resolves retained R822-4 RES-A / R821-4 RS-A at lines 259–263.
Verification: inspect the added comment lines and run normal wording/style gates. Untouched legacy labels remain under #746.

**R822-5-R2 — RESIDUE — Docs — docs/design/REBOOT_RESET.md:316.** Retains R822-4 RES-B. Authority/evidence: the existing three-layer explanation has its colon and comma reversed: `SUCCESS: its three layers each carry one, the loop's stop`. Impact: punctuation alone obscures the list; the named layers and tests are correct. Exact fix: `SUCCESS. Its three layers each carry one: the loop's stop`. Verification: text inspection; preserve every layer and defect name.

**R822-5-R3 — RESIDUE — Docs — docs/design/REBOOT_RESET.md:297; sw/firmware/ctrl/plat/README.md:89; sw/firmware/ctrl/plat/ctrl_plat.h:37.** Retains R822-2 R2. Authority/evidence: `ctrl_plat.c` services the journal from the last loop pass, but ADP polling starts after the other rings drain and ADP shuts down. Impact: an imprecise prose join; the sequencing is already specified and implemented correctly. Exact fix in both prose passages: `From the loop's last pass the platform services the saved-state store on its own centisecond and its F_NVM, and, once every other ring has drained, ADP's poll until the port fires.` In the header, replace `and ADP until the port` with `and, from ADP's shutdown, ADP until the port`. Verification: compare those sentences with `depart()` and `quiet()`; no executable change.

Independent conclusions

- Merge readiness keeps both the owed-notice queue capacity condition and REBOOT hold. Completion tracking remains ahead of the new awaited-event walk. `round_waits` now includes `a->reboot != 0u`; both retry entry points use it. Existing command notices drain before REBOOT's final completion, while the guard prevents a new asynchronous retry round after acceptance. Refusal precedence, all-channel receive gate, reset-after-completion and terminal platform path remain intact.
- The CSR bank moves from `n_locs - 3` to `n_locs - 4`, leaving the record mover at -3. The published exports differ only by ctrl_reboot and ctrl_reboot_req at 0xf000e000, excluding timestamps. REBOOT datapath wiring and census files have no round-5 changes. #902 internals were not re-reviewed. Its merge trees 659d7687 and 07ed787e are equal; only SPLIT_CONTROL_MEMORY.md differs between 41ca9f87 and 07ed787e.
- The four platform test adaptations follow the loop's deferred saved-state pass and the driver's cached TX tail. Ring refusal starts at the first driver read; ADP refusal spans SHUTDOWN and its next poll. Assertions remain. Published control receipts catch the corresponding journal, reset and owed-DEPARTING defects.
- The flash model uses the generated KLJ3 journal span. The early-reset plant precedes the REBOOT handler, and the grader requires the SUCCESS-after-reset diagnostic. Published evidence catches all five plants and seven controls, including mixed replay. Clean order: SUCCESS 0.129 ms, notification 0.219 ms, DEPARTING 0.528 ms, port 0.543 ms; 54,327 CPU/bus cycles. Drain: 851.040 ms, REBOOT 62 bus cycles after erase, 14 subsequent page programs.
- The answering-ports fixture enables REBOOT and the new group exercises short/type/index/lock refusals before accepted ENTITY 0, with registered recipients. Record classes keep REBOOT ordinary and reject missing accepted/refused coverage and oversized records. At 1x1/1if, accepted 11,467 cycles gives 125 us and refusals 100–115 us, within 240 us. At 8x8/2if the reported values are 95–115 us within 265 us.
- The restatements follow ceil(measured_us × 1.05 / 5) × 5: SRP 26,865 cycles -> 285 us; ordinary AECP 22,531 -> 240; paced SET_CONFIGURATION 28,750 -> 305; idle events 3,627 -> 40. Both load columns remain conservative. Relative to the imported merge, ctrl/loop/ has one executable change, CTRL_LOOP_SRP_UNIT_US 280 -> 285 at one interface, plus a bound comment. The load check enforces its derivation.
- Independent checks reproduce load 0.520, every 1x1/1if row within bounds, slice 950 us and pace 8 ms. Tight rows: txL 48.75/49 ms, last queued notice 134.74/135 ms, ACMP 29.22/30 ms. The bound is derived under #894's amendment and stays below the 140 ms STOP threshold. Survey warnings for paced/long records are resolved by their explicit classes.
- Platform 8x8/2if is 60.5 RAMB36, formerly 60.0, identified by ctrl_plat 20,416 B. Owner ruling #665 comment 6892332745 permits the increase as S14 debt; device fit and timing remain required. Fixture points: 41.0/42.5/54.5/59.0; platform: 43.0/43.5/56.0/60.5.

Evidence and carry

Archive: [f2e8fa9f05d00f3963ee299277506a3a3eeeccce, author-r5](https://github.com/kebag-logic/milan-fpga/tree/f2e8fa9f05d00f3963ee299277506a3a3eeeccce/review-evidence/665s11-r1/author-r5). All 1,166 files match published_sha256, including 18 publisher-redacted files. The archive commit is unsigned (%G? = N): this establishes hash/provenance consistency, not an independent cryptographic signer. Large traces are indexed in RAW/LARGE tables but omitted; no full independent trace regrade is claimed. Public scope and evidence anchors: [assignment ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6894152131), [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/871#issuecomment-6899968849), [review start](https://github.com/kebag-logic/milan-fpga/pull/881#issuecomment-6900026049).

The review independently matched firmware-tree hashes and 42 checkout-input hashes across A/E1/B1F/B8R, substituting later campaign bytes with their measured revision. Arm A has 96 distinct indexed scripts, 94 included; its generators are unchanged. Source checks and focused mutations are this review's executions; full-bank evidence below is the author's published evidence.

| Gate evidence | Head | Result and carry |
|---|---|---|
| Full sweep | 57daf4ff | Independently recounted 65/65, 2,713,040 checks, zero failures/timeouts. Later changes do not touch these suite inputs. |
| Native workflow steps | 57daf4ff / 20e08ceb; AECP d3566d44 | 88 rc 0, 167 reasoned skips, zero bad; builder-running jobs use the later head. Not hosted execution or a manager source bank. |
| Control/SRP/unit/coverage | 57daf4ff receipts | Control 738/738; SRP, unit and coverage PASS. Later edits are separate AECP mutation and REBOOT simulation/comment files. |
| Full AECP | d3566d44 | Independently counted 314 successful mutation entries; both changed guards present; one site per anchor. |
| REBOOT/builder/saved-state | 20e08ceb | REBOOT 12/12, builder with explicit NOT RUN arms, saved-state 144/144. Later REBOOT changes are comments/README; the later AECP mutation row is not an input. |
| Docs/models | cb0fc679 | Docs 64 rc 0, 31 reasoned skips. Exact-head idiom/whitespace/docs-check receipts cover the later mutation-row edit. |
| Harness/hooks/behavior/split boots | 57daf4ff | 246/246; 28/28 and 96/96; 511 scenarios; split boots PASS. Relevant inputs unchanged afterward. |

Independent execution: selected baseline PASS; retry-after-success and owed-round-beside-queue mutations fail on their named assertions; record classes 14/14, load 26/26, flip 585/585, tier model 1,033/1,033 controls; load and flip checks PASS; grid selects 950 us. Portable scripts and raw receipts accompany the report.

Prior public findings: resolved or retained

Read only after the independent verdict and five-lens ledger above were written. Sources: PR #881 comments 6788965651, 6789318251, 6806677261, 6806678527, 6809438458, 6809453671, 6810823985 and 6811057292. Prior accepted coverage is carried only where its causal artifacts and dependencies remain unchanged; the merge and affected tests were examined above.

| Prior IDs and severity | Disposition at this head; causal evidence |
|---|---|
| R821-1 F1 MINOR / R822-1 F1 MAJOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED. `ctrl_plat.c` taking/depart gates all channels from accepted SUCCESS; `aecp.c` acceptance precedes handover. `test_plat_boot.cpp:944–1118` and per-channel gate/ring plants retain coverage; round-5 retry guard closes the new dependency. |
| R821-1 F2 / R822-1 F2 MINOR; Tests, Docs | RESOLVED. `ctrl_reboot/run.py:672` plants before the handler; the published 20e08ceb self-test fails on SUCCESS after reset, with exact words required. Later run.py changes are comments. |
| R821-1 F3 MINOR and R822-1 S4 SUGGESTION; Conformance, Docs | RESOLVED. `REBOOT_RESET.md:302–312` explicitly separates held-ring unboundedness from scenario measurement, restated after the merge. |
| R822-1 F3 MINOR; Tests | RESOLVED. `ctrl_reboot/run.py:827` pins PYTHONHASHSEED before exports. Not a claim about other simulation drivers. |
| R821-2 F1 / R822-2 F1 MINOR; Tests, Docs | RESOLVED. Five receive channels, individual ring holds, own-pass and full-response-ring cases remain at `test_plat_boot.cpp:944,1032,1060,1089`; acceptance-before-poll AECP assertion and individual planted defects remain. Published 738/738 control campaign covers the adapted tests. |
| R821-3 F1 / R822-3 F1 MINOR; Conformance, Tests, Docs | RESOLVED by the public option-(b) ruling, #871 comment 6809457669. Test header, `plat_mutants.py:259`, `REBOOT_RESET.md:316` and platform README explain the AECP exclusion and separately tested layers. The retry layer is now also named and tested. Current PR text refers to historical ruling rows without claiming a separate B20 AECP mutant. |
| R822-1 R1 RESIDUE | RESOLVED. `MAILBOX_SPLIT.md:1743` names mailbox, mover and REBOOT banks. |
| R822-2 R1; R821-3 RS1 / R822-3 RES1 RESIDUE | RESOLVED for their named lines: test header uses descriptive test names; `test_plat_boot.cpp:81,1026` spells TheResetWaitsForTheResponseToLeave. Other retained/new instances are R822-5-R1 above. |
| R821-3 RS2 RESIDUE / R822-3 S-a SUGGESTION; R821-3 RS3 RESIDUE | RESOLVED. Section 8 and platform README specify MAAP, SRP and a second AECP frame for the own-pass case. The current PR body no longer contains the stale three-channel row. |
| R821-4 RS-A / R822-4 RES-A; R822-4 RES-B; R822-2 R2 RESIDUE | RETAINED and consolidated into R822-5-R1, R2 and R3 above, with exact fixes. |
| R821-1 S1 SUGGESTION | RESOLVED. ENTITY 1 under another controller's lock is tested as NO_SUCH_DESCRIPTOR; `reboot-lock-before-the-index` remains in the AECP campaign. |
| R821-1 S3 / R822-1 S1 SUGGESTION | RESOLVED. `run.py` mixed-replay control and published 12/12 receipt require “a write half applied”. |
| R822-1 S2 SUGGESTION | RESOLVED historically by the published author-r2 S2-base tables/logs/compare, accepted in rounds 2–4. The round-5 timing conclusions use the new image receipts instead. |
| R822-1 S3 SUGGESTION | RESOLVED. `cdc_census.gen.py:123` describes the request level; its round-4 accepted artifact/dependencies are unchanged. |
| R822-2 S1 SUGGESTION | RESOLVED. Acceptance-before-poll, own-pass and full-ring cases plus their plants pin the gate start point. |
| R821-4 S-C SUGGESTION | RESOLVED/obsolete in current PR body: it no longer calls the older campaign's aggregate “88 failed checks” distinct checks. The new 88 count is workflow steps. |

Retained optional suggestions

These are the prior suggestions, consolidated without changing their severity or treating them as blocking. Each row supplies its artifact/evidence, practical limitation, optional outcome and verification. No new mandatory scope is inferred.

| ID / prior IDs | Severity; all lenses | Artifact and evidence; impact; optional outcome and verification |
|---|---|---|
| R822-5-S1 / R821-1 S2, R821-2 S3 | SUGGESTION; Tests | `ctrl_plat.c` quiet face poll and platform tests: the prior omission probe survives; a dedicated held-ack case would independently pin that service. Verify a face-poll omission fails its own assertion. |
| R822-5-S2 / R821-1 S4, R821-2 S4 | SUGGESTION; RTL | `milan_soc.py` all-fabric export: explicit zero tie conflicts with the ruling's byte-identical export requirement; CTRL_SPLIT=0 does not consume the input. Manager decision remains; if changed, compare exports and census. |
| R822-5-S3 / R821-2 S1, R822-2 S3 | SUGGESTION; Tests | `ctrl_reboot/run.py:563–570` requires BIND_RX arrival within the window, but only reports AEM arrival. Optionally require AEM in that window too; shift it outside in a control and require rejection. |
| R822-5-S4 / R821-2 S2 | SUGGESTION; Tests | `ctrl_reboot/run.py` CONTROLS: post-port quietness lacks its own injected-transmission control. Add one if desired; it should fail the post-port diagnostic specifically. |
| R822-5-S5 / R821-2 S5, R822-3 S-b | SUGGESTION; Tests | `test_plat_boot.cpp:982` holds the next ADP frame without decoding ENTITY_DEPARTING. Optionally assert its message type so the held object is explicit; substitute another ADP type and demonstrate failure. |
| R822-5-S6 / R821-2 S6 | SUGGESTION; RTL | `aecp.c:294` accepted accessor is a const state observation without the usual entry guard. Optional comment explaining its intentionally safe observation from the platform gate would document that distinction; inspect against call sites. |
| R822-5-S7 / R822-2 S2 | SUGGESTION; Docs | Historical packet INDEX had 15 post-publication mismatches. Retained historical caveat, not a current hash failure: all current published_sha256 entries verify. Regenerate historical index after redaction if repaired; verify each published byte. Unsigned archive remains a separate provenance limit. |
| R822-5-S8 / R822-2 S4 | SUGGESTION; Tests | `ctrl_plat.c` quiet and `ctrl_reboot/run.py` drain scenario: prior quiet-only-after-port probe survives because the current scenario does not distinguish the interval. Optional held-ring/NVM-deadline case should require service before the port and reject the omission. |
| R822-5-S9 / R821-3 S7 | SUGGESTION; Tests | `test_plat_boot.cpp:1072,1080` AECP own-pass assertions are not mandatory words in the relevant platform mutation entry. Optionally add the AECP words to that entry's required diagnostics; verify a missing-word control fails. |
| R822-5-S10 / R821-3 S8 | SUGGESTION; Docs | `test_plat_boot.cpp` header list mixes B-prefixed and descriptive test names. Optional uniform descriptive names; inspect comments without changing identifiers/diagnostics. |
| R822-5-S11 / R821-4 S-A, R822-4 S1 | SUGGESTION; Tests, Docs | `test_plat_boot.cpp:982` gives AECP no traffic to send in that scenario, even when two layers are lifted. This remains within accepted option (b). Optional comment: “This scenario gives AECP nothing to send, so its check also holds with two layers lifted.” Verify the explanation against fixture setup; do not claim an independent AECP B20 plant. |
| R822-5-S12 / R821-4 S-B, R822-4 S2 | SUGGESTION; Docs | `REBOOT_RESET.md:316`, platform README and mutation comment say AECP starts no frame after SUCCESS in the repository's sense of new traffic. Existing owed notices and REBOOT's own frames still drain. Optional wording: “AECP starts no new asynchronous traffic after acceptance; already owed notices and the REBOOT's frames drain before DEPARTING.” Check against `aecp_poll` and completion tests. |
| R822-5-S13 / R822-4 S3 | SUGGESTION; Docs | `plat/README.md:128` joins two list ends with “and”. Optionally separate the own-pass clause with semicolons. Text-only inspection suffices. |

Reproduction and receipt inventory

The accompanying scripts take two positional arguments, checkout and packet directory. To reproduce archive audits, fetch the immutable archive without submodule recursion and extract only `review-evidence/665s11-r1/MANIFEST.json` and `review-evidence/665s11-r1/author-r5` beneath `packet/scratch/`. Run `audit_packet.py TREE PACKET`, `check_receipts.py TREE PACKET`, `probe_mutants.py TREE PACKET` and `verify_checkout.py TREE PACKET` with Python 3. The mutation script uses eight build jobs and keeps all disposable build copies beneath scratch. `run_model_checks.py TREE PACKET` reproduces the model commands whose raw outputs accompany this report; no full bank is needed. The final byte/mode/index check covers the superproject and each initialized required submodule gitlink; external remains intentionally uninitialized at its recorded gitlink. No tracked source bytes or modes changed.

Only REPORT.md and entries in MANIFEST.sha256 are publication artifacts. Scratch trees and the locally cached public discussion are excluded.


Limits and manager duties

- Acceptance item 1 stays partial by public ruling: six items and binding restored; configuration/rate cannot leave defaults and are NOT RUN. The PR relates to #871, not closes it. Items 2–5 remain supported.
- CPU simulation observes the mailbox face, not physical wire delivery; only part of PHY hold is simulated and configuration loading is omitted. ADP calculation is 4,808.775/20,000 ms with configuration load unmeasured. Physical calibration and field skips are not hardware proof.
- Source base 1d6bf555 is distinct from the current-dev candidate. The manager must synchronize #898, rerun the affected image survey, validate builder/native banks on the current-dev candidate, and publish receipts. Supplied live dev: 6b66f66d89cf25d2717687bcc2c3bf617685a99a. Small timing margins matter on recomposition.
- Hosted/act acceptance, second independent review, merge authorization, final candidate gates, hardware qualification and post-merge containment remain manager duties. No manager source bank at this head is claimed. No GitHub writes, commits, source fixes, hardware operations or full-bank reruns were performed.

R822-5 FINISHED
