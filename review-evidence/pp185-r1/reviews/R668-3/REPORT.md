[R668] POSITIVE - exact head 4865184c9ba88dd85aba3fc8036a6b74bcdb7073

R668-2-F1 is **RESOLVED**. The corrected comparison partitions planted mutants from golden/control baselines, and its published totals reconcile with the campaign records. All five lenses are CLEAN for this narrow evidence-only re-review. No new BLOCKER, MAJOR, MINOR or RESIDUE finding was found. Previously recorded, out-of-scope suggestions remain retained below.

Reviewed tree: `2f850bcae69e2361992a32e5f91ac97e4a81f979`. Source base: `b48312e13b8a3ed409dbe8a66d6311f2e37cd5f2`. The source head is identical to round 2. This is source/evidence review, not acceptance of a final parent merge candidate or hardware qualification.

**Scope, reconstruction and independence**

Read the supplied AGENTS instructions and referenced command policy first; the repository has no AGENTS.md or CONTRIBUTING.md. Reconstructed docs/README and README, issue #185/#186 bodies and manager decisions, requirement/interface authorities, the full-PR diff and history, then the immutable [public evidence packet](https://github.com/kebag-logic/milan-fpga/tree/c6574c479b48fadc7c33f0fb12df36ee77c44423/review-evidence/pp185-r1). The controlling [round-3 assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/196#issuecomment-6273649559) requires evidence correction only. The [timeout correction](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/186#issuecomment-6253571045) remains controlling: automatic unlock carries UNLOCK and locked_id zero.

Authorities examined: repository transcriptions of IEEE 1722.1-2021 §§7.2.22, 7.3.6.2/Table 7-122, Table 7-98, §7.4.2.1/Table 7-143 and §7.5.2; Milan v1.2 §5.3.12 and Table 5.22; REQ-AEM-003/006/014 and REQ-NOT-001/002; architecture 02 interfaces, 06 descriptor/lock contracts, 07 model rule L8, 08 timing and 09 verification. No licensed standards PDF was consulted.

The independent source pass preceded consultation of prior public findings. My round-2 report supplied the explicitly requested behavioural carry-forward and audit script. The [independent positive verdict and ledger](receipts/independent-verdict-ledger.md) were written before reading the other reviewer's findings. Those findings were then reconciled, without changing the independent verdict. No private author material, management checkout, or other private reviewer report was accessed. [Public scope receipt](receipts/public-scope.json).

**R668-2-F1 — MINOR, Tests and Docs — RESOLVED**

Cause and impact: the old comparison counted every top-level log as a mutant, inflating unchanged-mutant measurements with passing baselines and missing name_state's nested logs. This was a measurement defect, not wording residue.

Artifact: `author-r3/receipts/round3/scripts/r3_failsets.py:40–74`, with rendering at `:82–120`. Its roster comes exclusively from `results.json`. Notification/D3/ACMP baseline names must agree with empty `named_checks`; dispatch control names must agree with absence of a patch; name_state identifies its explicit golden record. Duplicate names are rejected. Dispatch reads only each roster entry's named log and checks the failure-line count against the record. Comparison uses verdict plus the failure-ID multiset, separately for mutants and baselines. No unfiltered log glob supplies the classifier. The shell wrapper's log enumeration collects hashes/extracts; it does not define mutant populations.

Required outcome and verification: baseline-only comparisons contribute zero mutants; all affected summaries state mutant and baseline populations separately; old receipts remain available; corrected prose and an explicit supersession map replace the inflated figures. All conditions are satisfied:

| Round-2 comparison | Mutants base / head | Unchanged | Changed | Added | Removed | Baselines base / head |
|---|---:|---:|---:|---:|---:|---:|
| notify, including exact-head rerun | 125 / 135 | 120 | 5 | 10 | 0 | 15 / 15 |
| aecp_dispatch | 63 / 69 | 60 | 3 | 6 | 0 | 4 / 4 |
| d3 | 110 / 110 | 110 | 0 | 0 | 0 | 6 / 6 |
| acmp | 54 / 54 | 54 | 0 | 0 | 0 | 7 / 7 |
| name_state | 16 / 16 | 16 | 0 | 0 | 0 | 1 / 1 |

The head-to-exact-head notification comparison gives 135 unchanged mutants and 15 separate baselines. Round-1c comparisons also reconcile: notify 107/2/16 with 13→15 baselines, dispatch 51/3/9 with four baselines, D3 110 with six, ACMP 51 with six, and name_state 16 with one. Against round-1b, notify has 114 unchanged and 11 added; dispatch 63, D3 110 and ACMP 51 are unchanged, with their baselines separate.

Reviewer execution and receipts:

- All **16 summaries** were independently reconciled. **13 comparisons** were replayed from published results and dispatch failure-line extracts, matching their JSON and detailed text after accounting for publication hash changes. The three ACMP comparisons were checked against the explicit JSON-line campaign rosters, verdicts, recorded input hashes and retained comparison rows. Their full result files exceed the public size cap; their complete failure-ID multisets were not independently replayed. [Comparative audit](receipts/comparisons-audit.json), [execution result](receipts/audit-round3.log).
- The unchanged `audit_evidence.py`, SHA-256 `2cf0bacc051e51a88cfc8f2b59da1d5b2957d98f47f8e58977f01611fb0bda0a`, ran against **author-r3**. Its output equals the previously published output byte-for-byte. It independently retains the 120/60/110 assertions, exact-head notification rerun check and parent gate-11 comparison. [Replay](receipts/prior-audit-replay.log), [output](receipts/evidence-audit-replayed.json), [reconciliation](receipts/reconcile.log).
- The four-case comparison self-test passes. Five additional reviewer baseline-only probes, one per campaign, each include an unlisted failing log and still report zero mutants. Four planted comparison defects each fail the self-test: counting baselines, ignoring changed failure IDs, accepting a dispatch-count mismatch, and accepting inconsistent baseline/plant metadata. [Self-test](receipts/comparison-selftest.log), [baseline example](receipts/baseline-only-notify.log), [original-defect control](receipts/mutant-baselines-counted.log).
- All 14 old detailed comparisons agree with the corrected rows. The only extra old rows are two notification goldens formerly listed as new mutants. `SUPERSEDES.md` regenerates byte-identically with all 16 mappings, including the two new exact-head comparisons. [Old-row check](receipts/old-rows.log), [map replay](receipts/supersedes-replay.log).

**Receipt preservation and documentation**

The original public `author-r2` directory remains byte-identical to its earlier publication: tree `e4bb0bd3fde416085f3f5a9aed27bd70a3e358d3` at both packet commits. [Tree preservation](receipts/old-public-tree-preserved.json).

All **1,475 retained original receipt digests** match the saved pre-publication round-2 index. The regenerated current index enumerates exactly **1,592 receipt files**. Public copies require an explicit qualification: 1,324 retained files are byte-identical across author-r2/author-r3; 151 differ solely by four path-placeholder substitutions. Every such difference was checked, with no unexplained content change. Thus the original public receipts are preserved, while the newly published copies use a different redaction vocabulary. [Index audit](receipts/preservation-index.json), [redaction reconciliation](receipts/publication-preservation.json).

Verified all 1,595 author-r3 files plus the three selected prior-review artifacts against the immutable manifest's published hashes. [Hash receipt](receipts/fetched-hashes.json). Both source and evidence commits are reported **unsigned**; this verifies published byte integrity and commit identity, not cryptographic signature authentication. [Signature observation](receipts/signature-observation.json).

Examined the HANDOFF and PR-BODY changes by section: both campaign tables, the 150-record exact-head sentence, the old 129-record common population, round-1c comparisons and the new reconciliation section now distinguish mutants from baselines. Old numbers occur as explicitly superseded history. Kept campaign-summary tables quote campaign closing lines rather than the inflated comparison totals. No tracked README quoted those erroneous aggregate totals. The live PR body matches the packet PR-BODY exactly after trimming boundary whitespace. [Prose audit](receipts/prose-audit.json), [PR identity](receipts/published-pr-identity.json).

**Prior public findings and suggestions at this head**

The [round-2 review](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/196#issuecomment-6273273700) resolved the assigned behavioural causes. Their implementation and dependencies have not changed:

| Prior ID / severity | Attributable lenses | Disposition and cause-level evidence retained |
|---|---|---|
| R668-1-F1 / MAJOR | Conformance, RTL, Robustness, Tests, Docs | RESOLVED: notify `:965–970`, `:1423`, `:1539` retain owed expiry and delay a colliding claim; LC1 and named claim/expiry/exclusion controls cover loss and incoherence. |
| R667-1-F1 / MINOR | Conformance, RTL, Tests, Docs | RESOLVED: notify `:1499`, `:1523` refresh active-round arguments/exclusion on take/release; LC4–LC6 and named controls cover mid-round changes. |
| R667-1-F2 / MINOR | Conformance, RTL, Tests, Docs | RESOLVED: `gen_ucode.py:1351–1379` compares all four IDENTIFY words and restores SUCCESS for image fallback; RDC7/RC3 and six controls cover refusal. |
| R667-1-F3 / MINOR | Tests, Docs | RESOLVED: `tb/pp_top/README.md:2866–2881` records 125 = 98 + 11 + 16, then ten more for 135; the roster agrees. |
| R667-1-R1 / RESIDUE | Docs | APPLIED: architecture 06 `:814` and compliance decision 16 use “on T-LOCK-UNLOCK expiry”. |
| R668-1-F2 / RESIDUE | Docs | APPLIED in round 2; the corrected source comments and exact source bytes remain unchanged. No new processor source comments occur in this round. |
| R668-2-F1 / MINOR | Tests, Docs | RESOLVED by this review's script, population, replay, preservation and prose checks above. |

Prior suggestions remain suggestions, not newly assigned acceptance work. Their impacts, suggested outcomes and checks remain applicable at the unchanged head:

| Prior suggestion | Lenses / artifact | Retained outcome and verification |
|---|---|---|
| R667-1-S1 | Tests, RTL; E_RDESCCT locate-miss arm | Add an absent-index regression or remove the redundant arm; verify NO_SUCH_DESCRIPTOR stub. |
| R667-1-S2 | Tests; processor CONTROL fixture | Use the conformant 113-byte fixture with a distinct tail byte; verify every RDC byte. |
| R667-1-S3 | Conformance, Docs; control_value_type guard | Check flagged value-type interpretation and document intent; retain the previous guard verdict in this evidence-only round. |
| R667-1-S4 | Docs; old “no shift” generator comments | Refresh stale wording beside existing shift operations; no behaviour change requested. |
| R667-1-S5 | Conformance, RTL; existing GET/SET_CONTROL index handling | Track non-IDENTIFY index behaviour separately; unchanged by this round. |
| R667-2-S1 | Robustness, RTL; notify `:1098–1100` | Retain the separate issue suggestion for an IDENTIFY press replacing a taken lock job; prior report records lost IDENTIFY/duplicate LOCK frames at older bases too. Its suggested verification is zero lost frames in the press-offset probe. No fresh reproduction is claimed here. |
| R667-2-S2 | Robustness, Docs; notify `:1540`, `:1749`; engine `:2679` | Document/assert the done-strobe margin for job re-presentation; verify the engine's real completion remains beyond that bound. |
| R667-2-S3 | Tests, Docs; microprogram RC3 and README | Record the last-word type-comparison control that fails RC3; no campaign coverage expansion assigned. |
| R667-2-S4 | Docs; suite README record prose | Retain the suggestion to replace review labels with neutral behavioural wording. These README records were not classified as source-comment violations. |

The other reviewer's round-2 report introduced no open blocking finding. Its suggestions were read only after the independent verdict and ledger were written.

**Reviewer-owned five-lens ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen scope and timeout correction; architecture 06/07/08; E_RDESCID/E_LOCKUNS; unchanged cause and IDENTIFY restrictions | R668-2 behaviour carried forward; R668-3 identity/scope check | 4865184c9ba88dd85aba3fc8036a6b74bcdb7073 |
| RTL | CLEAN | Notify expiry/claim/relatch FSM; engine job/gather capture; all tracked bytes/modes; top signature, queue/router and interface preservation | R668-2 behaviour carried forward; R668-3 integrity check | 4865184c9ba88dd85aba3fc8036a6b74bcdb7073 |
| Robustness | CLEAN | Retained LC0–LC7 and RDC guards; comparator duplicate/name/plant/count rejection; baseline-only stray-log probes | R668-2 behaviour; R668-3 evidence paths | 4865184c9ba88dd85aba3fc8036a6b74bcdb7073 |
| Tests | CLEAN | r3_failsets; all 16 summaries; unchanged audit replay; 13 detailed replays; ACMP rosters; four detected comparison mutants | R668-3 closes R668-2-F1; behavioural tests carried forward | 4865184c9ba88dd85aba3fc8036a6b74bcdb7073 |
| Docs | CLEAN | HANDOFF/PR-BODY, live PR, corrected tables, SUPERSEDES, current/saved indices, receipt preservation | R668-3 closes R668-2-F1; source documentation retained | 4865184c9ba88dd85aba3fc8036a6b74bcdb7073 |

**Execution limits and pending manager duties**

Only evidence audits and disposable comparison-script probes ran in this round. No behavioural suite, full processor/parent/builder/synthesis bank, container, shared install or hardware run was performed. All disposable files stayed under packet/scratch; execution was foreground, with at most 16 download workers. No source edit, commit, push, GitHub write, merge, author contact, delegation or other-checkout edit occurred.

The unchanged source-gate receipts identify exact head and retain eight zero return codes. The exact-head notification campaign records 135 kills and 15 passing goldens. The descriptor campaign remains an execution at `acc059a`, whose relevant implementation/tests were unchanged by the later commits; it is not relabelled as an exact-head execution. The earlier reviewer spot-checks of 131 notification checks and 447 microprogram checks are carried forward, not rerun.

Public dispatch failure-line extracts were checked against their result counts; complete dispatch logs were not published in those campaign directories. ACMP's omitted large result files prevent a full independent failure-ID replay. These limits do not prevent checking the corrected population accounting. No omitted log, skipped context or pending job is promoted to executed proof.

There is **no manager source bank at this head**, and none is inferred. The author scratch-parent receipts retain gate 11 rc 1 at base/head with byte-identical logs, the acknowledged #190 width dependency; the other sixteen return codes are zero. The exact-head parent processor gitlink is verified in the published receipts. [Source/parent identities](receipts/source-parent-identities.json).

The manager owns hosted/act acceptance and must validate the final current-dev merge candidate with builder and native banks, linking its receipts on the PR. The source base is `b48312e1`; the supplied live dev is `e26f1816e456dc8027924bc2e5d327a8aa6e46db`. The #190 parent adoption dependency remains part of that integration. This report does not establish current hosted completion or merge-candidate acceptance. Required independent positive reviews and the full completion bar still apply. Physical calibration is **NOT RUN**; field skips are not hardware proof.

[Final integrity](receipts/final-integrity.json) verifies all **663 tracked blob bytes and modes**, exact HEAD/tree, matching index tree and empty status. This processor checkout contains **zero submodule gitlinks**. Nothing required source restoration.

Replay from this packet: `python3 scripts/fetch_public.py`, `python3 scripts/audit_round3.py`, `python3 scripts/check_preservation.py`, and `python3 scripts/verify_checkout.py /path/to/exact-head-clone`. The wrapper places the unchanged prior audit beside the author-r3 round-2 records and executes it there. Only REPORT.md and files listed in MANIFEST.sha256 are publishable; scratch is excluded.

R668-3 FINISHED
