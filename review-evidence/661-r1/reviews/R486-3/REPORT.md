[R486] POSITIVE - exact head 3048222541ea6be725417ba0cd957607f0b821cb

R486-3, internal independent source review of issue #661 / PR #663. Tree: `a640b146eb68632f2d9ca153639ba2683b172b0a`. All five lenses are CLEAN for the assigned scope. No BLOCKER, MAJOR or MINOR remains open. R487-2 F1 and R1 are resolved. Three wording residues and three optional suggestions remain below.

This is source approval. Final candidate validation, hosted/local-replica acceptance and physical release work remain manager duties.

**Scope and independence.** The review reconstructed the operating contract, documentation map, frozen acceptance and public decisions, linked authorities, source change inventory/history, the documentation delta and its consumers, then public executable evidence. The independent verdict and five-lens ledger were written before reading prior public reviewer reports. No private author material, private review packet or management storage was read.

The source base is `506d91dbeeba585d72d2e80d92fca799c719f8ee`. The previous reviewed head is `3880c1eb6e2f927a07f98150d5b05a228f8f4efd`; the supplied live-dev base is `fa450d301805881ad713b67521477bf042ddadfd`. The current head has exactly the previous head as its parent. Only `docs/reference/FR_NFR.md` and `docs/findings/README.md` differ. All other 1,013 tree entries retain their modes, types and object IDs. Earlier R486-2 coverage stands for that unchanged scope, as assigned. `receipts/delta.patch` and `receipts/delta-identity.json` record the comparison.

**Requirement correction.** [The public manager decision](https://github.com/kebag-logic/milan-fpga/pull/663#issuecomment-5994059536) explicitly resolves the conflict. I checked IEEE Std 1722.1-2021 Section 6.2.2.15 in the standards document itself, PDF page 54. `receipts/clause-comparison.json` records its identity and digest without redistributing the document.

FR-DISC-01 now preserves all three clause cases: increment after each transmitted ENTITY_AVAILABLE, reset to zero when transmitting ENTITY_DEPARTING, and reset after a power cycle. The separate advertisement and valid_time obligation remains. The former state-change wording was inconsistent with the standard; correcting it conforms the requirement to the clause and relaxes no standards obligation. The adopted processor's reset/increment logic at `protocol-processor/hdl/adp/KL_adp_engine.sv:703`, the register-map note at `docs/reference/REGISTER_MAP.md:1032`, and the corrected saved-state and compliance statements agree.

**Historical index correction.** `docs/findings/README.md:26` now contains R487-2 R1's exact requested sentence, verified byte-for-byte after the independent verdict was written. It dates the former builder acceptance to the measurement revision and identifies the later generation-time refusal. This agrees with `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:26` and `:600`, and the existing NAME-capacity refusal at `sw/builder/endstation_builder.py:2736`. No measured value or verdict is changed.

**Lens results.**

[R486] PASS Conformance - `docs/reference/FR_NFR.md:173`; IEEE 1722.1-2021 Section 6.2.2.15; public decision 5994059536 - The amended requirement preserves the standard's increment and both reset conditions. R487-2 F1 is resolved by the public decision and conforming wording.

[R486] PASS RTL - `receipts/delta-identity.json`; `protocol-processor/hdl/adp/KL_adp_engine.sv:703`; `receipts/checkout-after.json` - The delta changes no implementation, generated artifact, interface, clock/reset logic, timing input or gitlink. The index manager's reset and per-message updates agree with the amended requirement. The existing RTL coverage is retained against identical entries.

[R486] PASS Robustness - `tb/tools/avtp_wire_truth_checks.py:585`; `receipts/wire-probes.log` - Ordinary advertisements and departure/restart cycles pass; ordinary repeats, repeated zero after restart, and retained departing values fail. The zero-valued departure case and 32-bit wrap pass. All seven directed inputs yield the intended verdicts.

[R486] PASS Tests - `tb/tools/avtp_wire_truth_selftest.py:347`; `receipts/wire-truth.log`; mutation receipts - All 25 committed self-tests pass. Removing the reset exemption, exempting a nonzero value after departure, and exempting every zero each cause the committed reset test to fail. All three disposable defects are detected. No source mutation entered the checkout.

[R486] PASS Docs - `docs/findings/README.md:26`; `docs/reference/FR_NFR.md:173`; `receipts/prior-dispositions.json`; documentation gate receipts - The historical/current distinction is accurate, the normative conflict is resolved publicly, and the exact requested index text is present. The current PR body passes the repository privacy scrub. Only wording residues and optional suggestions remain.

**Executed validation.** The ten focused commands in `run_focused.py` all completed successfully after resolving two environment refusals. Independent commands ran concurrently through a foreground coordinator, at most four at once. There were no native builds or heavy campaigns.

| Check | Result |
|---|---|
| `scripts/docs_check.py` | rc 0; zero findings across 189 Markdown and 987 text files; scrub 23/23, routing 4/4 |
| `scripts/check_doc_style.py`, plus `--selftest` | Both rc 0 |
| `scripts/gen_toc.py --check` | rc 0; 131 annotated pages checked |
| `scripts/check_em_dash.py --base fa450d301805881ad713b67521477bf042ddadfd` | rc 0; zero findings, 339/339 controls |
| `scripts/check_doc_paths.py` | rc 0; 912 cited paths resolve, one allowlisted |
| `scripts/check_wire_accountability.py --self-test` | rc 0; 77 checks, zero findings, controls pass |
| `scripts/check_feature_status.py --self-test` | rc 0; 46/46 controls, zero findings |
| `tb/tools/avtp_wire_truth.py --self-test` | rc 0; 25 tests |
| Base-to-head whitespace check | rc 0 |
| `probe_wire_truth.py` | rc 0; seven directed inputs and three detected defects |

The initial contents and added-line checks returned rc 2 because the pinned Markdown dependencies were absent. Their original logs and return codes are retained as `toc-initial.*` and `em-dash-initial.*`. The hash-locked dependencies were installed only under packet scratch storage. Only the two refused checks were repeated; their final logs and `renderer-results.json` record success. `focused-results.json` deliberately retains the first attempt's statuses.

The wire-accountability script's FR_NFR reference is in its explanatory text; its executable checks concern advertised/emitted widths and fill behavior. Its successful run is a regression check, not a parser-based proof of the ADP clause. That proof comes from the direct clause comparison. The wire repeat check is likewise not presented as a complete ADP conformance oracle.

**Prior public findings, explicitly reconciled at this head.**

| Prior item | Disposition | Evidence |
|---|---|---|
| R487-2 F1, MINOR, Conformance/Docs | RESOLVED | Public decision 5994059536; FR-DISC-01; direct clause comparison |
| R487-2 R1, RESIDUE, Docs | RESOLVED | Exact requested sentence in findings index |
| R487-1 F1, MINOR, Conformance/Tests/Docs | RESOLVED | Corrected statements unchanged since R486-2; 25 tests, seven vectors and three detected defects |
| R486-1 F1 and R487-1 F2, MINOR, Docs | RESOLVED | Current body uses portable placeholders and passes the privacy scrub; manager correction 5991634080 remains applicable |
| R486-1 F2, MINOR, Docs | RESOLVED | Current body says 212 ports; implementation entries are identical to the prior reviewed census |
| R486-1 R1, RESIDUE, Docs | RESOLVED | Current body describes the published branch and detached checkout |
| R486-1 R2/R3 | RETAINED as RESIDUE | Exact fixes below; unchanged artifacts |
| R486-1 S1; R487-1 S1/S2 | RETAINED as SUGGESTION | Optional outcomes below; unchanged artifacts |

The [R486-2 verdict](https://github.com/kebag-logic/milan-fpga/pull/663#issuecomment-5994211606) and [R487-2 findings](https://github.com/kebag-logic/milan-fpga/pull/663#issuecomment-5994013182) were read only after this round's independent verdict and ledger. The older round-1 public findings were then checked for complete disposition. No prior MINOR is deferred to another Issue as a substitute for resolution.

**Retained and new non-blocking items.**

- **R486-1 R2 | RESIDUE | Docs | `docs/reference/SUBMODULES.md:148`.** Authority/evidence: the D3 header explicitly says the name-pending transfer is not yet adopted. Impact: the summary's present tense is ambiguous. Exact fix: "Not yet adopted: a later parent lane (D3 section 18.3, lane 3) moves name pending to `d3_unflushed_o`; until then the sticky term stays." Verification: compare with `SAVED_STATE_MATERIALIZATION.md:15`. The existing adoption status does not change.
- **R486-1 R3 | RESIDUE | Docs | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:333`.** Authority/evidence: the 8x8 configuration already declares the lint waiver, while the F5 explanation omits it. Impact: incomplete explanation of successful packing. Exact addition: "The 8x8 configuration's `model_lint_waivers` entry (L1 `port-cluster-minimum`, STREAM_PORT_INPUT 0 to 7, #584) lets the default lint pack it; the packer refuses the waiver once any of those ports passes. The waiver is not a conformance claim." Verification: retain the existing conformance debt and compare with the declared waiver. No clause claim changes.
- **R486-3 R1 | RESIDUE | Docs | PR #663 body, 'How to get into the same state', 'Expected head'.** Authority/evidence: the body fetches the published branch but still names the previous head as the expected checkout. `receipts/public-state.json` and `receipts/prior-dispositions.json` record the current head and body digest. Impact: stale reproduction wording following the manager's documentation commit. Exact fix: replace only "Expected head: `3880c1eb6e2f927a07f98150d5b05a228f8f4efd`" with "Expected head: `3048222541ea6be725417ba0cd957607f0b821cb`". Verification: the checkout expectation matches the published branch; historical validation rows remain attributed to their executed heads. This changes no measurement, figure, verdict, executable test, source, generated artifact, conformance/clause claim or privacy rule.
- **R486-1 S1 | SUGGESTION | Docs, RTL | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:38`.** Evidence: standalone 8x8 WNS changes from -1.947 to -4.095 ns, already distinguished from routed timing. Impact: a reader could overlook the limitation. Optional outcome: name the decline and the owner of an integrated 8x8 route. Verification: preserve the measured figures and the absence of an integrated fit claim.
- **R487-1 S1 | SUGGESTION | Tests | `tb/verilator/nvm_cosim/Makefile:50`.** Evidence: the producer list excludes the name writer; the D3 header leaves parent name persistence proof unclaimed. Impact: that integration remains statically checked only. Optional outcome: exercise the actual name writer/backend through write, restore and rollback in the assigned persistence lane. Verification: cleared-state readback and fault-sensitive controls.
- **R487-1 S2 | SUGGESTION | Robustness, Tests | `protocol-processor/hdl/aecp/desc/model_rules.py:115`; `protocol-processor/hdl/aecp/ucode/gen_ucode.py`.** Evidence: lint bounds 144/8 still agree with the consumer, but are separately declared. Impact: future edits could diverge. Optional outcome: tie the bounds through a consistency check. Verification: a planted consumer-bound change fails. No current mismatch is asserted.

**Reviewer-owned ledger.** CLEAN applies to the assigned source scope. R486-2 coverage is retained only for identical entries; the normative and documentation changes have been reviewed here.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | FR_NFR.md:173; IEEE 6.2.2.15; decision 5994059536; REGISTER_MAP.md:1032; clause-comparison.json | R486-3; unchanged R486-2 scope retained | 3048222541ea6be725417ba0cd957607f0b821cb |
| RTL | CLEAN | delta-identity.json; KL_adp_engine.sv:703; checkout-before/after.json; required gitlinks | R486-3; unchanged R486-2 scope retained | 3048222541ea6be725417ba0cd957607f0b821cb |
| Robustness | CLEAN | avtp_wire_truth_checks.py:585; wire-probes.log; reset, repeat and wrap cases | R486-3; unchanged R486-2 scope retained | 3048222541ea6be725417ba0cd957607f0b821cb |
| Tests | CLEAN | avtp_wire_truth_selftest.py:347; focused-results.json; renderer-results.json; three mutation logs | R486-3; unchanged R486-2 scope retained | 3048222541ea6be725417ba0cd957607f0b821cb |
| Docs | CLEAN | findings/README.md:26; FR_NFR.md:173; public-state.json; prior-dispositions.json; documentation logs | R486-3; unchanged R486-2 scope retained | 3048222541ea6be725417ba0cd957607f0b821cb |

**Real limits and manager duties.** All 20 objects in the specified [public evidence archive](https://github.com/kebag-logic/milan-fpga/tree/0010a410b0150c2c7043142fb64036a7d2655799/review-evidence/661-r1) match its published hashes. The archive's source validation and 49 successful documentation steps belong to `42f654478c11bd8f2b070969d83140587190f276`. The [round-2 public evidence](https://github.com/kebag-logic/milan-fpga/issues/661#issuecomment-5993741847) supplies later results. The assignment states that the manager's full source static/build and native banks passed at this head. These supplied results are distinct from this round's focused executions and from the final merge candidate; historical records are not relabelled as new executions.

No full parent, processor, time-synchronization, synthesis or builder bank was rerun. No route or original resource input-digest remeasurement was performed. Retained route timing and capture measurements remain historical source evidence. The supplied round-2 result retires #656's exception; #657 remains the authorized 28 PASS / 4 FAIL campaign exception. Physical calibration: NOT RUN. Four field/freshness skips and the two builder NOT RUN arms remain excluded from proof. Simulation, field skips and timing reports provide no hardware proof.

Hosted jobs were not inspected in this round. The manager owns exact-head hosted/local-replica acceptance and must distinguish executed checks from skipped contexts. Publish this packet, retain the external independent verdict, leave no review round in flight, and carry the three RESIDUE items to the residue checklist. Suggestions remain optional.

At merge, construct and validate the final candidate against then-current dev using the required complete gates. Source approval does not discharge that step. Merge requires explicit maintainer authorization. After merge, perform containment and the assigned flash/soak work, then complete Issue and project closure.

Final checkout verification matches the initial receipt exactly: 1,011 parent blobs, 558 processor blobs, 104 time-synchronization processor blobs and 214 stream-library blobs have exact bytes, modes and index entries. Required gitlinks remain `ead8036035affd53ef4b29979190f2f4f67084c0`, `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, and `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The unused external gitlink is unchanged and uninitialized. The checkout is clean. No source fix, commit, push, GitHub write, merge, author contact, hardware operation, shared install or other-checkout edit occurred.

Portable scripts and raw receipts are listed in `MANIFEST.sha256`, with paths relative to this packet. Run scripts from the reviewed checkout and pass its path as their first argument. Disposable dependencies and mutation copies live only under `scratch/`, which is excluded from publication.

R486-3 FINISHED
