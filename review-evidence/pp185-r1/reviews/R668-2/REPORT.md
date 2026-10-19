[R668] NEGATIVE - exact head 4865184c9ba88dd85aba3fc8036a6b74bcdb7073

The assigned source fixes pass this review. Every named prior defect and both assigned wording residues are resolved. One new MINOR finding remains in the published executable-evidence comparison: passing baselines are counted as mutants in generated unchanged-failure totals. Tests and Docs are therefore UNCLEAN; Conformance, RTL and Robustness are CLEAN. No new functional defect was found.

Reviewed tree: `2f850bcae69e2361992a32e5f91ac97e4a81f979`. Full diff base: `b48312e13b8a3ed409dbe8a66d6311f2e37cd5f2`; delta base: `b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad`. This verdict concerns source validation and its published evidence, not acceptance of a final parent merge candidate or hardware qualification.

**Reconstruction and independence**

The supplied AGENTS instructions and referenced command policy were read first. There is no repository AGENTS.md or CONTRIBUTING.md. Reconstruction followed the documentation conventions, public issue bodies and decisions, linked requirement/interface authorities, full diff and history, five-commit delta, and then public executable evidence. The independent diff pass and initial five-lens verdict were written before reading either prior public findings comment; see [independent pass](independent-pass.txt) and [initial verdict/ledger](independent-verdict-ledger.txt). The later evidence audit identified F1 below and changed the final verdict. No other round-2 reviewer report was consulted.

The controlling [round-2 assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/196#issuecomment-6264668094) was read exactly. The [issue #186 correction](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/186#issuecomment-6253571045) supersedes the original timeout-flags instruction: automatic unlock carries UNLOCK with locked_id zero. The assignment rejects weakening either this rule or the IDENTIFY-only restriction. [Public scope receipt](public-scope.json).

Authorities examined: IEEE 1722.1-2021 7.2.22, 7.3.6.2/Table 7-122, Table 7-98, 7.4.2.1/Table 7-143 and 7.5.2 as transcribed in the public decisions and repository; Milan v1.2 5.3.12 and Table 5.22; REQ-AEM-003/006/014 and REQ-NOT-001/002; architecture 02 interfaces, 06 descriptor/lock contracts, 07 dynamic-state ownership and model rule L8, 08 F08.1, and 09 verification. No separate licensed standards PDF was consulted.

History examined includes the original CONTROL/flags changes, timeout correction, both main merges, and the five round-2 commits: `43a7987`, `4ba8c02`, `acc059a`, `7368215`, `4865184`. [Full diff](receipts/reviewed.diff), [round-2 diff](receipts/round2.diff).

**R668-2-F1 — MINOR — Generated comparison totals count passing baselines as mutants**

Attributable lenses: **Tests, Docs**.

Artifacts at the immutable [published packet](https://github.com/kebag-logic/milan-fpga/tree/992033a936efe4add5139167612f2b268be01134/review-evidence/pp185-r1): `author-r2/receipts/round2/scripts/r1c_failsets.py`, especially its unfiltered `glob("*.log")` and final `same` tally; `round2/compare/failsets-notify-base-vs-head.txt`, `failsets-aecp_dispatch-base-vs-head.txt`, and `failsets-d3-base-vs-head.txt`, final lines. Local copies: [comparison script](receipts/public-comparison-script.py), [notification comparison](receipts/public/compare/failsets-notify-base-vs-head.txt), [dispatch comparison](receipts/public/compare/failsets-aecp_dispatch-base-vs-head.txt), [D3 comparison](receipts/public/compare/failsets-d3-base-vs-head.txt).

The script treats every top-level log as a mutant. Successful golden/control logs have equal empty failure lists, so they increment the unchanged-mutant count. Independent reconstruction from the raw result records gives:

| Campaign | Published “mutants fail the same checks” | Unchanged mutants | Passing baselines incorrectly included | Other mutant changes |
|---|---:|---:|---:|---|
| Notification | 135 | 120 | 15 | 5 existing mutants gain failures; 10 new mutants |
| Descriptor dispatch | 64 | 60 | 4 | 3 existing mutants gain failures; 6 new mutants |
| D3 | 116 | 110 | 6 | none |

The notification base contains only 125 mutants; 135 cannot be the number of unchanged mutants across that base and head. The dispatch campaign's 73 PASS campaign checks are correctly 69 killed mutants plus four passing baselines; they are not 73 mutants. The ACMP comparison similarly reports 61 unchanged mutants while the campaign records 54 mutant kills; its comparison should also be regenerated with separate baseline accounting.

Authority/evidence: the assignment requires accurate executable receipts and preservation of previous failure coverage; the owner severity rule explicitly excludes measurements, figures and generated artifacts from wording-only RESIDUE. [Independent audit](evidence-audit.json), [portable audit](audit_evidence.py), and the hash-verified [notification](receipts/public/head-final2/campaigns/out/notify/results.json), [dispatch](receipts/public/head/campaigns/out/aecp_dispatch/results.json), and [D3](receipts/public/head/campaigns/out/d3/results.json) records establish the populations. The unchanged notification and D3 failure-ID multisets were recalculated; the dispatch record independently confirms the three changed failure counts and six added arms, agreeing with its detailed comparison rows.

Impact: the aggregate preservation measurement is overstated even though the detailed mutant verdicts remain valid. This does **not** invalidate the 135 notification kills or any of the sixteen new controls. It does make the generated comparison evidence inaccurate. This is a measurement/classification defect in the comparison script and its outputs, not a prose-only wording residue.

Required outcome: partition actual mutants and passing baselines explicitly, and regenerate the affected comparison receipts. State 120 unchanged notification mutants, five changed and ten added, separately from 15 passing baselines; 60 unchanged dispatch mutants, three changed and six added, separately from four baselines; 110 unchanged D3 mutants separately from six baselines. Apply the same classification to the other comparison outputs. Preserve the original execution receipts and link the corrected evidence; no RTL change or bank rerun is required for this finding.

Verification: run the corrected comparison against the existing base/head records and reconcile every population with `results.json` or the campaign's explicit mutant roster. A baseline-only comparison must contribute zero mutants. The reviewer audit can be replayed with `python3 audit_evidence.py`.

**Prior public findings: disposition at this head**

The [first prior findings](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/196#issuecomment-6264247031) and [second prior findings](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/196#issuecomment-6264653909) were read only after the independent diff pass and written initial verdict/ledger.

| Prior ID | Disposition | Cause-level verification |
|---|---|---|
| R668-1-F1, MAJOR | RESOLVED | `KL_aecp_notify.sv:965–970`, `:1423`, `:1539`: owed expiry is retained, a simultaneous claim waits, and the active round receives the automatic unlock's arguments and empty exclusion. LC1 covers before/on/after claim, both preceding LOCK words and the registered former owner. Claim, pending-expiry, relatch and exclusion controls are KILLED. |
| R667-1-F1, MINOR | RESOLVED | `KL_aecp_notify.sv:1499` and `:1523`: a taking LOCK or releasing UNLOCK refreshes an active lock round's arguments and exclusion and pends the final round. LC4–LC6 check coherent pairs and requester exclusion; each corresponding control is KILLED. |
| R667-1-F2, MINOR | RESOLVED | `gen_ucode.py:1351–1379`: E_RDESCID compares all four words at 82, 84, 86, 88 to IDENTIFY, restoring SUCCESS before whole-image fallback. RDC7 tests a vendor type and a mismatch in each word, then returns to IDENTIFY; RC3 checks the non-IDENTIFY microprogram path. Six new controls are KILLED; RDC0–RDC6 retain passing evidence. |
| R667-1-F3, MINOR | RESOLVED | `tb/pp_top/README.md:2856` onward now states 125 = 98 + 11 occupancy + 16 flags controls at the merge, then ten new controls for 135. These campaign totals match the rosters; F1 above concerns a different generated comparison measurement. |
| R667-1-R1, RESIDUE | APPLIED | Architecture 06 §6.8 now says “on `T-LOCK-UNLOCK` expiry”; compliance decision 16 uses the same wording. |
| R668-1-F2, RESIDUE | APPLIED | Every specifically listed comment change is present in the notification bench, processor bench, microprogram bench and notification mutation driver. Added source comments describe behavior/reasons; the reviewed full-PR comment additions contain none of the identified bench labels. No new comment-rule residue found. |

R667-1-S1 through S5 remain explicitly **unassigned suggestions**, as the round-2 assignment directs. They concern the redundant locate-miss arm/absent-index regression, a conformant 113-byte processor-level CONTROL fixture, flagged value-type interpretation, old “no shift” comments, and pre-existing GET/SET_CONTROL handling of other CONTROL indices. This delta does not change their causes; they are retained as prior suggestions without expanding round-2 acceptance. The short-descriptor and value-type guards keep their prior verdict.

**Five independent lens conclusions**

Conformance: each lock notification carries a single cause's pair. The timeout may wait across a presented job and its holder-read acceptance, after which the current round and pending final round carry UNLOCK/zero with no former-owner exclusion. A command changing the lock refreshes the remaining round jobs. Command-word echo remains in the unchanged engine/E_LOCKUNS path. The IDENTIFY type check preserves other controls' own image values and leaves the existing layout/configuration guards intact.

RTL: examined the notification FSM, last-assignment ordering, reset of `lk_exp_r`, `lk_on_w` arbitration, engine job operand capture and registered gather answer (`KL_aecp_engine.sv:2419–2442`), and the four 16-bit microprogram comparisons/status-restoring fallback. At the N_ANS answer edge, the engine captures the old coherent holder before expiry's sequential state update. No new top-level port, parameter or register-map change occurs. The full-PR top changes are internal flags wiring; its public signature matches the source base.

Robustness: examined expiry before/on/after claim, after load, on holder-read acceptance, lock takeover during UNLOCK, release during LOCK, requester exclusion, deferred-expiry retention and a holder re-lock when expiry is owed. LC2/LC3 directly cover the third path between job load and holder read. The final pending round reaches earlier recipients. Reset and non-IDENTIFY/fallback behavior remain covered. Queue count/occupancy lines match `b48312e1`; event-router files and the round-2 interface/map authorities are unchanged.

Tests: the oracles check expected destinations, sequence numbers and the serialized flags/holder bytes, with distinct control values and a registered former owner. This is a notification-block handshake model, not a fresh processor-wire capture of each collision. Existing processor-wire LN/L5b/L6d/TD/RN checks and engine/gather inspection connect it to emission. All ten new lock controls and six IDENTIFY controls have named kills. The exact-head notification rerun retains every old failure ID and adds only the documented failures; its fifteen goldens pass. F1 leaves this lens unclean only for the aggregate comparison measurement.

Docs: architecture 06 §§6.1/6.8 explains the IDENTIFY-only guard and chosen expiry/relatch mechanism; compliance decisions 15/16 and 09 match it. The PR's round-2 section records the design and boundary limits. Suite READMEs match the new checks, totals and affected mutant rows (`rd-tail-uncut` 17; `occupancy_reset_set` 32). The outstanding defect is the separate published comparison output, F1.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Public scope/authorities; E_RDESCCT/E_RDESCID/E_LOCKUNS; lock cause/exclusion paths | R668-2 delta; unaffected behavior retains prior coverage | 4865184c9ba88dd85aba3fc8036a6b74bcdb7073 |
| RTL | CLEAN | Notify FSM; engine job/gather pipeline; generated-program inputs; top signature/queue/router comparisons | R668-2 delta and named prior causes | 4865184c9ba88dd85aba3fc8036a6b74bcdb7073 |
| Robustness | CLEAN | LC0–LC7; owed expiry; reset; requester exclusion; non-IDENTIFY/short-layout fallback | R668-2 delta and retained prior guard coverage | 4865184c9ba88dd85aba3fc8036a6b74bcdb7073 |
| Tests | UNCLEAN — R668-2-F1 | Local focused suites; published gates, new controls, old failure preservation, generated comparison totals | R668-2 | 4865184c9ba88dd85aba3fc8036a6b74bcdb7073 |
| Docs | UNCLEAN — R668-2-F1 | 00/06/09, test READMEs, source comments, PR scope text, comparison receipts | R668-2 | 4865184c9ba88dd85aba3fc8036a6b74bcdb7073 |

**Execution and evidence identity**

| Evidence | Result and identity |
|---|---|
| Reviewer notification spot-check | Exact-head disposable export; all five runs, 131 checks PASS. [Log](aecp_notify-spotcheck.log), [rc](aecp_notify-spotcheck.rc). |
| Reviewer microprogram spot-check | Same export; 447 checks PASS. [Log](ucpu-spotcheck.log), [rc](ucpu-spotcheck.rc). |
| Author final source gates | `round2/head-final2/gates/HEAD.txt` is exact head; all eight rc files are zero, including 1,030,205 suite checks, event_router 81, pp_top 10,634, notify 131, ucpu 447. [Suite receipt](receipts/public/head-final2/gates/run_suites.log). |
| Author notification campaign | Exact-head `HEAD-notify.txt`; 135/135 KILLED, 15 goldens PASS; ten new lock controls included. [Results](receipts/public/head-final2/campaigns/out/notify/results.json). |
| Author descriptor campaign | Executed at `acc059ac35ef61d6e9bbe570353f26db3c39a40c`: 73 campaign checks PASS = 69 mutant kills + four baselines. Six new type controls included. Later commits change README records and split the notification bench; descriptor implementation/tests/driver remain identical. This is retained evidence, not a falsely claimed exact-head campaign execution. |
| Earlier probes repeated by author | Published claim/midround/vendor probes pass; these are author executions, not reviewer executions. [Claim](receipts/public/probes-head/probe-claim.log), [midround](receipts/public/probes-head/probe-midround.log), [vendor](receipts/public/probes-head/probe-vendor.log). |
| Parent consumer receipts | Author scratch parent over dev `e9cbb676`, with documented #180/#176 patches; processor pin exact head. Sixteen gates rc 0 at base/head. Gate 11 rc 1 has byte-identical logs. [Audit](evidence-audit.json), [head pin](receipts/public/parent-head/submodule-HEAD.txt), [parent history](receipts/public/parent-head/parent-log.txt). |

The reviewer spot-checks ran concurrently with eight compilation workers each, inside packet/scratch, and waited in the foreground. [Portable driver](run_focused.py), [identity](simulator-identity.txt), [results](focused-results.json). No full processor, parent, synthesis or builder bank was run by this reviewer.

241 selected public receipts were checked against the immutable packet's `published_sha256` values; the public comparison script was checked separately. [Hash verification](public-hash-verification.json), [script hash](comparison-script-hash.json), [fetch driver](fetch_evidence.py). The API reports both the source commit and evidence-packet commit as unsigned: [signature observation](signature-observation.json). Consequently this review verifies published byte integrity and commit identity, and makes no claim of cryptographic signature authentication. No private author material or omitted large-log bytes were accessed.

**Limits and pending manager duties**

- The full source-bank conclusion rests on the author's published execution receipts. There is no manager source bank at this exact head, and none is inferred.
- Parent gate 11 is the acknowledged #190 width mismatch (`cfg_tspec_max_frame_i`, 128 bits) against the older parent dev. Its base/head logs are byte-identical; it is not this delta. The #190 parent patch must accompany adoption.
- At the recorded [hosted observation](hosted-observation.json), exact-head runs 39293425859 and 39293418946 had successful portability/documentation jobs; both suites jobs were still in progress. No skipped job was promoted to executed proof. Hosted/act acceptance belongs to the manager.
- The manager must resolve F1's comparison receipts, obtain the required independent positive reviews, and build/validate the final current-dev merge candidate with builder and native banks, linking receipts on the PR. Source base is `b48312e1`; supplied live dev is `e26f1816e456dc8027924bc2e5d327a8aa6e46db`. Source validation does not replace that merge-turn validation.
- Physical calibration is NOT RUN; field skips are not hardware proof. No hardware was used. No timing/resource claim is inferred from these simulations.
- No source fix, commit, push, GitHub write, merge, author contact, delegation, container run, shared install, privileged operation or other-checkout edit was performed. Disposable exports/builds are confined to packet/scratch.

[Final integrity](final-integrity.json) verifies all 663 tracked blob bytes and modes, exact HEAD/tree, matching index tree and empty status. This processor repository has zero submodule gitlinks. The required parent processor gitlinks are checked in the published consumer receipts. [Portable integrity check](verify_checkout.py).

Only REPORT.md and files listed in MANIFEST.sha256 are publishable. Scratch is excluded.

R668-2 FINISHED
