[R678] POSITIVE - exact head cf1ca87529b4c1a9d6ba7acbf691b626e15bae9e

External independent review R678-6 of milan-fpga PR #770, issues #632 and #764. Tree: e4d84bf05d153298aeec0b15dc887aa16efef744.

All five lenses are CLEAN for this delta, with R678-5 coverage carried over for unchanged artifacts. R677-5-F1's clause and conformance-disclosure defects are resolved. Its requested clickable issue link is still missing and is retained below as navigation-only RESIDUE. There is no open BLOCKER, MAJOR or MINOR in this review. This verdict does not authorize merging or complete physical acceptance.

## Scope and independence

Reviewed the one commit from 24a292a0321df6f3516f25cb6e92e24fb1988e65. `delta.patch` and `checkout-final.json` prove that only `docs/reference/REGISTER_MAP.md` changed: eight added lines and three removed lines. Every other entry, including executable files, generated inputs, modes and gitlinks, is identical to round 5. No engine change was made.

Reconstructed AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue contracts and public scope decisions, requirements/interfaces, then diff/history and published evidence. The domain-reference, build-now listener, fixed queue depth, AAF-exact/CRF-rounded offsets and resource exceptions remain controlling. The full source-base comparison is e26f1816..cf1ca875; unchanged implementation is carried under the owner's later-round rule, not represented as freshly re-executed.

`independent-pass.txt` preserves the independent verdict and artifact-specific ledger written before opening previous reviewer reports. Prior public findings were then reconciled. No private author material, other checkout, management source bank or current-round peer report was read.

Public anchors: [review start](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6372703917), [manager fix](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6372658718), [R677-5](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6372618017), [R678-5](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6372621514).

## Direct clause check and R677-5-F1

I read the actual 2011 and 2020 texts, both 2011 corrigenda and Milan v1.2. `standard-identities.json` identifies the PDFs by SHA-256. `clause-check.txt` records paraphrased results; licensed text and extractions are not published.

| Authority | Direct result | Candidate paragraph |
|---|---|---|
| IEEE 802.1AS-2020 10.3.11.2.1 d), PDF page 116 | Without the TLV, the port's receivedPathTrace becomes empty | Correctly stated at REGISTER_MAP.md:1475 |
| IEEE 802.1AS-2020 10.3.13.2.4 f) 5), PDF page 121 | Copies the selected port's receivedPathTrace into pathTrace; appends thisClock only when nonempty | Correctly stated at :1476; together the two clauses explain count zero |
| IEEE 802.1AS-2011 10.3.10.2.1 d), PDF page 96 | A qualified TLV on the slave port supplies pathSequence plus thisClock; no no-TLV replacement is specified | :1477-1478 correctly says the previous path survives |
| IEEE 802.1AS-2011 10.3.12.1.1, PDF page 99; 10.3.12.1.4 i), with Cor1 | Initialization/own-GM selection establish the singleton thisClock path | The initialization citation supplies context, not a separate no-TLV procedure. Cor1 adds no no-TLV clear; Cor2 does not modify these clauses |
| Milan v1.2 4.2.6 and normative references; REQUIREMENTS.md:114 | The selected edition is 2011 with Cor1/Cor2 | :1479 explicitly calls the engine's empty publication a departure from the profiled edition |

The [engine issue #87](https://github.com/Mister-M-alt/FPGA-gPTP/issues/87) exists, is open, and records both alternatives for the engine owner. It has no decision comment. The PR body's open question names #87; its known limitation states both 2020 clauses and the 2011 departure. The historical round-8 table is less detailed but makes no contradictory claim. `public-context.json` preserves the relevant public text.

R677-5-F1 (MINOR, Conformance/Docs): the incomplete authority and implicit departure are resolved at their causes. The public decision artifact now exists. The literal hyperlink outcome remains as R678-6-R1 below, under the owner's RESIDUE rule. This does not declare the underlying engine-policy question resolved: #87 remains open, and no 2011-conformance or engine-fix claim is made.

## Findings and retained residue

**R678-6-R1 | RESIDUE | Docs**

- Artifact: `docs/reference/REGISTER_MAP.md:1480`.
- Authority/evidence: R677-5-F1 asks the paragraph to link the decision issue. The candidate says `in FPGA-gPTP #87.` without a URL or Markdown link. The issue exists at the link above.
- Impact: the reader must locate the cross-repository issue manually. The edition, behavior and clause claims are already explicit and correct; adding the link changes none of them.
- Exact required outcome: replace `in FPGA-gPTP #87.` with `in [FPGA-gPTP #87](https://github.com/Mister-M-alt/FPGA-gPTP/issues/87).`
- Verification: inspect the rendered link target and run the documentation gates. This navigation-only residue does not unclean a lens under the owner's rule.

**R677-5-R1 | RESIDUE | Docs | RETAINED**

- Artifact: `tb/verilator/milan_dp/dynmap_mutants.py:29` and `:35`, independently spot-checked unchanged.
- Authority/evidence: the source-comment rule forbids review-history labels; these predate this delta and are tracked by #746.
- Impact: wording residue only; no executable token changes.
- Exact required outcome: replace `The #637 round-2 controls follow (reviews R669-1 and R670-1): seven that` with `The #637 map-restore controls follow: seven that`; replace `and the round-1 ordering, which REMOVEs` with `and the former restore order, which REMOVEs`. Keep executable identifiers and mutation labels unchanged.
- Verification: inspect the docstring and confirm token/AST identity. Carry to the manager's residue checklist and #746. No new source-comment instance exists in this documentation-only delta.

## Earlier findings carried at their causes

These dispositions retain the public R678-5/R678-4 resolution chain. The complete tree-entry comparison proves the delta does not alter their implementation, tests or dependencies. They are not claimed as new simulation runs.

| Prior findings | Status at cf1ca875 and cause artifact |
|---|---|
| R677-4-F1 / R678-4-F1 | Resolved, retained: MILAN_COMPLIANCE_MATRIX.md:221 and AAF_LATENCY_TAPS.md:105 state per-event refusal and once-per-PDU counts, matching KL_render_queue and preserving physical limits |
| R677-4-F2 / R678-4-F2 | Resolved, retained: GM_LOSS_RECOVERY.md:321 has 21 controls plus two clean legs; milan_dp/README.md:90 describes the current no-rebase presentation behavior |
| R677-4-F3 | Resolved, retained: TESTING.md:647 describes NOTIFY passing at processor 93fb0b2d and the GSI-word mutant |
| R678-4-F3 | Assigned boot/reset/append citations remain corrected. The neighboring no-TLV clause defect subsequently named R677-5-F1 is resolved substantively above |
| R678-4-R1 | Five assigned dynmap comment fixes remain; the two other pre-existing docstring instances are retained separately as R677-5-R1 |
| R677-3-F1; R678-1-F1 | Listener implementation and partially late-event repair retained in KL_render_queue, derived interface leads and pin tests; campaign evidence supplied in earlier rounds. Physical proof remains pending by explicit scope |
| R677-3-F2 / R678-3-F2 | Corrected queue figures and counts retained in design/evidence-reader artifacts; later GM-step count correction retained |
| R677-3-F3 | T26 cause remains repaired by the two-stream closed-epoch map-write case and completed 31/31 campaign |
| R678-3-F1 | Retired render-law prose remains corrected in TIME_SYNC and recovery documents; later per-event documentation correction retained |
| R678-3-F3 | Source campaign gap remains resolved by full render, 18 pull-in phases plus history and full GM-step receipts; final merge-candidate execution remains pending |
| R678-3-R1 / R677-3-R1 | Assigned three review-history comments remain removed |
| R677-2-F1 | Adopted processor integration remains resolved at 93fb0b2d: prior 461/0 NOTIFY and 11-control evidence; no longer splice-only |
| R678-2-F1 | Full CRF carry and saturated readback retained in KL_mtt_round/KL_crf_tx and full-width offset tests |
| R677-2-F2; R678-1-F3/F4 | Hold-reference restart, circular fold and snapshot-edge hold repairs retained with det:afterhold, hold_keeps_ref and boundary/snapshot tests |
| R677-2-F3 | Corrected historical PR figures remain separated from current resource records |
| R678-1-F2 | Superseded by the public AAF-exact ruling: AAF rows remain as set; CRF alone rounds, with full-width carry |
| R677-1-F1/F2/F3 | Blend closing-interface/pop-edge fix, local PHC-step hold and settled/range checks retained in their unchanged source/tests |
| R677-1-F4/F5 | Corrected suite-budget basis and assigned CRF-divider comments retained |
| R678-1-R1 | Public internal/external reviewer roles remain explicit |
| R678-2-R1 / R677-2-R1; R677-2-R2 | Assigned reviewer-ID comments remain removed; offset comments retain AAF-as-set/CRF-as-applied distinction |
| R678-2-R2 / R677-2-R3/R4/R5 | Old listener deferral superseded by build-now; assigned scope prose remains corrected |

Optional items are retained, not silently marked fixed. Each remains SUGGESTION and does not condition this verdict:

| ID; attributable lenses | Artifact and evidence; impact | Optional outcome and verification |
|---|---|---|
| R678-5-S1 / R677-5-S1; Tests, Docs | dynmap_mutants.py listener setup and published first stopped attempt: generated inputs are prerequisites, so a fresh clone can fail setup | Document or prepare tdm8r_aemi.bin, ltn_rom.hex and ucode.hex through milan_dp_render; verify five clean legs and 63 controls from a fresh disposable checkout |
| R677-5-S2; Docs | GM_LOSS_RECOVERY.md:321 says plural steps under a single-step row; README:90 uses singular | Change `across the steps` to `across the step`; compare the row with the graded leg |
| R677-4-S1; Tests | sim_gmstep.cpp:986 boot/acquisition sequence: earlier review suggested a stronger observation before first talker | Add a direct pre-stream observation if desired, without changing the covered acquisition behavior; a planted premature-stop control should fail it |
| R677-4-S2; Docs | Earlier capture-coherence receipt directory lacks its own HEAD marker; sibling provenance supplied prior coverage | Add an explicit marker to future packets and verify it against the executed inputs |
| R677-3-S1 / R677-4-S3; RTL, Docs | Configured buffer declaration versus fixed queue depth remains optional policy work under the owner's fixed-shape decision | Align/document the accepted configuration policy; verify boundary configurations without expanding this PR |
| R677-3-S2 / R677-4-S3; Docs | CI-image command inventory retains a retired setpoint entry | Update the inventory against active suite targets and resolve every named command |
| R677-4-S4; Docs | MEDIA_CLOCK_FOLLOWING.md:1964 retains historical round wording in prose | Describe behavior directly if edited; preserve technical claims |
| R677-2-S2; RTL, Robustness | Carry-wrap defect fixed; extra factory-row policy guard remains optional | Define the accepted factory-offset domain before adding a guard; test its boundaries |
| R677-2-S3; RTL | KL_mmcm_drp_servo closing-cycle reference behavior remains unchanged/documented | Consider explicit reference timing if refactoring; preserve fold/snapshot tests |
| R677-2-S4 / R677-1-F6; RTL | Separate data-delay literals remain coupled to latency calculation | Derive from one parameter if refactoring; grade differing interface delays at pins |

R677-2-S1 is overtaken by AAF-exact offsets. R677-3-S3's refusal-tally enumeration and R677-3-S4's source campaign gap were addressed; the latter's candidate duty remains pending. R677-4-S5's assigned edition citations are addressed, with the explicit no-TLV follow-up above.

## Evidence and execution

The [public evidence packet](https://github.com/kebag-logic/milan-fpga/tree/2e4361bf22109bf9c158b2d3b5aba28401632a1e/review-evidence/632-r1) manifest has 11,160 entries. Its Git blob is c3c4ad2fcf3bfe24f8e3b3f9cb595bae10896e22. Independently verified that blob and **23 selected receipts** against their published SHA-256 values, with zero mismatches. This is a spot-check, not a claim to have downloaded all entries. See `receipt-verification.json` and `verify_receipts.py`.

The commit API reports **unsigned**, verified=false, signature=null. Consequently no signed-packet authentication is claimed; immutable public object identity and receipt hashes are the verified integrity evidence (`evidence-commit-verification.json`).

| Evidence | Result and limits |
|---|---|
| Own exact-head docs gates | All seven rc 0: docs_check, style, gPTP docs, paths, em-dash against 24a292a0, TOC check and anchors. Em-dash reports eight added lines, zero findings and 339/339 arms |
| Initial local renderer attempts | Three rc 2 setup refusals, retained as such. Installed only the repository's hash-locked dependencies in packet/scratch/mdvenv and reran successfully; no shared install |
| Public manager documentation-fix receipts | All seven gates rc 0; consistent with own execution. These are documentation gates, not a manager source bank |
| Author round-8 source receipts at 24a292a0 | gptp 185/185; ax1x1gptp 155 checks, zero failures; dynmap 68/68 (five clean plus 63 controls); all rc 0. Executable inputs are unchanged at cf1ca875 |
| Author docs-step receipts | 42 executed steps rc 0, two explicit skips. Skipping the host runner and destructive no-Git step is not execution evidence; separate archive checks are recorded in the public packet |
| Other inherited evidence | Prior full-bank, resource and mutation coverage carries from unchanged inputs. No fresh source or candidate bank is inferred |

Own checks used Python 3.14.8 directly, not a claimed reproduction of the author's full Make 4.3/Python 3.12.3 workflow. No simulation, synthesis, builder bank, hardware, Docker/act or host runner executed here. Additional heavy probes were unnecessary for this prose-only delta.

Hosted snapshot at this head: 45 jobs, eight successful, one physical-gPTP skip, twenty in progress and sixteen queued. Selectors/preparation successes are not long-bank completion. `hosted-snapshot.json` retains the observation; no hosted acceptance verdict is claimed.

## Reviewer-owned ledger

The full exact head below is the reviewed candidate. R678-6 covers the new paragraph and verifies carry-forward dependency identity; R678-5 at 24a292a0321df6f3516f25cb6e92e24fb1988e65 supplies unchanged coverage. It in turn retains implementation coverage from R678-4 at 417ec52864efc09f1e3ecd0f755cb0daa7604426. No covered executable artifact changed between those later rounds.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | REGISTER_MAP.md:1470; REQUIREMENTS.md:114; direct 2011/2020 clauses and Milan 4.2.6; PR question; FPGA-gPTP #87 | R678-6; unchanged R678-5 coverage carried | cf1ca87529b4c1a9d6ba7acbf691b626e15bae9e |
| RTL | CLEAN | delta.patch; checkout-final.json; engine KL_gptp_engine.sv:721 and :981; unchanged complete executable trees/pins | R678-6 carry-forward verification; R678-5 | cf1ca87529b4c1a9d6ba7acbf691b626e15bae9e |
| Robustness | CLEAN | REGISTER_MAP.md:1470; engine empty/nonempty/eight-entry branch; unchanged reset, bounds, malformed-input and timeout tests | R678-6 carry-forward verification; R678-5 | cf1ca87529b4c1a9d6ba7acbf691b626e15bae9e |
| Tests | CLEAN | receipt-verification.json; source logs and explicit skips; local-doc-gates-final.json; complete delta/executable identity | R678-6 delta; unchanged R678-5 coverage carried | cf1ca87529b4c1a9d6ba7acbf691b626e15bae9e |
| Docs | CLEAN | REGISTER_MAP.md:1470; clause-check.txt; public-context.json; prior-finding reconciliation; seven docs gates | R678-6 | cf1ca87529b4c1a9d6ba7acbf691b626e15bae9e |

## Integrity, limits and manager duties

`checkout-final.json` proves raw blob bytes, executable modes and complete stage-zero indexes for all 1,441 parent blobs and five initialized submodules: protocol processor 93fb0b2d, gPTP processor 55680bff, verilog-axis 48ff7a7e, tsn-c-stack 70936b77 and lwSRP 08ee86e8. All six gitlinks are unchanged; unrelated external efeb541a remains uninitialized. Git status is empty. Review-created bytecode was moved into unpublished scratch; no source restoration was needed.

No manager source bank exists at this head and none is claimed. The manager must build and validate the final current-dev merge candidate, publish builder/native-bank receipts, accept hosted/act results, reconcile both independent reviews and obtain merge authorization. Source base is e26f1816; designated live dev is e5b480a385841f19420570bbba7c46da101d1303. These source receipts do not discharge that merge-turn validation.

Physical calibration is NOT RUN. Field skips, simulation and timing/resource reports are not hardware proof. The manager retains the #764 ten-minute bench method and pending physical acceptance for #632/#764, as well as post-merge containment, issue closure and project completion. FPGA-gPTP #87 remains the public unresolved engine-owner decision; this review does not approve the departure as 2011 compliant. Carry both residue entries and the optional suggestions above.

No GitHub write, source fix, commit, push, author contact, merge, sub-agent or other-checkout edit occurred. Portable scripts are verify_checkout.py, verify_receipts.py and run_doc_gates.py. MANIFEST.sha256 lists publishable receipts and scripts relative to the packet root; scratch is excluded. REPORT.md is the final review artifact.

R678-6 FINISHED
