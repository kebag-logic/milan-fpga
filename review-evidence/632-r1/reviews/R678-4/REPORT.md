[R678] NEGATIVE - exact head 417ec52864efc09f1e3ecd0f755cb0daa7604426

External independent review R678-4 of PR #770, issues #632 and #764. Tree: `aea3f763c8a6eea72a5f9bb8dec0bfe5af13b268`.

Three MINOR findings remain: whole-PDU rejection wording in the compliance matrix, an understated GM-step control inventory, and nine behavioral gPTP citations added by the dev merge that still name the wrong edition. One source-comment RESIDUE item is recorded. No new functional RTL defect was established. This is not merge approval.

## Authority and scope

Reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the public issue contracts and decisions, linked requirements/interfaces, the base-to-head diff and history, then published executable evidence. The independent diff pass and initial verdict/ledger preceded reading previous public review findings. No other round-4 review report was read.

Reviewed the delta from ee5ece607816a1bfc834bd51734b703a8aab8e46 to the exact head, within the requested e26f1816..HEAD comparison. Unchanged mechanisms retain their previous cause-specific dispositions unless the delta changes their dependencies. The dev merge was compared against both parents, d40e2ee8 and e5b480a3, including shared files that merged cleanly.

Applied the [round-6 assignment](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6341411985), [round-7 assignment](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6351804497), [area decision and round-7b assignment](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6357449062), [round-7c ruling](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6360257772), and its [edition correction](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6365323716). Earlier build-now, fixed-depth queue, block-RAM and AAF-exact/CRF-rounded decisions remain controlling. The grandmaster rule is IEEE 802.1AS-2011 9.6.2.1 and 10.2.3.13 under Milan v1.2 and its stated corrigenda. Historical hardware-assist cross-trace to 2020 does not change that product profile.

## Findings

### R678-4-F1 | MINOR | Conformance, Docs

**Artifact:** [docs/reference/MILAN_COMPLIANCE_MATRIX.md:221](https://github.com/kebag-logic/milan-fpga/blob/417ec52864efc09f1e3ecd0f755cb0daa7604426/docs/reference/MILAN_COMPLIANCE_MATRIX.md#L221), row 4.4.4.5/.9.

**Authority/evidence:** The row says “late and too-early PDUs are dropped and counted.” The round-6 ruling and IEEE 1722-2016 4.4.4.9/7.5 require the event-specific judgment now implemented by KL_render_queue. A PDU can contain refused events and events that remain presented. REGISTER_MAP.md:2085 correctly describes the once-per-PDU count without implying its other events are discarded. The corrected tests exercise this distinction.

**Impact:** An authoritative conformance row still claims the behavior R677-3-F1 required removing. This is a protocol-behavior claim, not wording-only residue. The code repair itself passes this review.

**Required outcome:** State that late/too-early events are refused, a PDU containing a refused event is counted once, and its other eligible events remain presented. Preserve the untimed-PDU rule and physical-evidence limits.

**Verification:** Compare the corrected row with the queue, REGISTER_MAP.md:2085 and mixed late/in-window/early tests. Documentation checks must remain green.

### R678-4-F2 | MINOR | Tests, Docs

**Artifact:** [docs/design/GM_LOSS_RECOVERY.md:321](https://github.com/kebag-logic/milan-fpga/blob/417ec52864efc09f1e3ecd0f755cb0daa7604426/docs/design/GM_LOSS_RECOVERY.md#L321).

**Authority/evidence:** The verification table says “20 in gmstep-mutants.” The same page at line 253 says 21 controls. The head's CONTROLS inventory contains 21, and the full published campaign passes 23 checks: 21 controls plus two clean legs. The new boot-grandmaster control is required by this round.

**Impact:** The documented executable inventory is understated. The campaign passes; the test-count claim is wrong and is not RESIDUE.

**Required outcome:** Replace “20 in gmstep-mutants” with “21 in gmstep-mutants”; preferably clarify “21 controls plus two clean legs, 23 checks.” Keep the separate five-control sweep description.

**Verification:** Reconcile the table with the AST inventory and gmstep_mutants_c2c996fa/gmstep-campaign.log. audit-receipts.json records all 21 named controls and their passing lines.

### R678-4-F3 | MINOR | Conformance, Tests, Docs

**Artifacts:** Nine behavioral references added by dc9cda7d still cite IEEE 802.1AS-2020:

| File | Lines | Behavior attributed to 2020 |
|---|---|---|
| docs/reference/REGISTER_MAP.md | 1051, 1476 | Own-grandmaster boot identity; appending thisClock to PathTrace |
| docs/reference/SUBMODULES.md | 242, 244 | Donor boot-grandmaster and PathTrace contracts |
| tb/verilator/milan_dp/sim_ax1x1gptp.cpp | 79, 1175, 1225 | PathTrace oracle; own-grandmaster boot and reset |
| tb/verilator/milan_dp/sim_gptp.cpp | 51, 818 | PathTrace oracle; own-grandmaster boot |

**Authority/evidence:** The review assignment requires gPTP behavior citations to name the 2011 edition. REQUIREMENTS.md and the compliance matrix distinguish that edition from hardware-assist cross-trace. Commit 417ec528 corrects the GM-step citations but leaves these merged behavioral citations unchanged. They are also present on dev; this finding identifies their introduction into this reviewed delta rather than attributing their original authorship to this implementation.

**Impact:** Register/interface contracts and test rationales still attach product behavior to an edition outside the adopted profile. These are clause claims, not RESIDUE. No incorrect boot or PathTrace execution is inferred from this citation defect.

**Required outcome:** Cite the applicable 2011 clauses and corrigenda for these boot/reset and PathTrace claims. Verify the clause mapping; do not simply change the year while retaining 2020 numbering. For gmIdentity/gmPresent use 9.6.2.1 and 10.2.3.13 as ruled. Review the neighboring pre-existing PathTrace citation at REGISTER_MAP.md:1471 while correcting that paragraph. Explicit historical/hardware-assist comparisons may retain properly scoped edition labels.

**Verification:** Scan changed source/comment and documentation lines and check each behavioral citation against the adopted edition. Current documentation gates pass despite these references; passing those gates alone does not close F3.

### R678-4-R1 | RESIDUE | Docs

**Artifact:** tb/verilator/milan_dp/dynmap_mutants.py:154,168,316,345,386, introduced into this delta by the dev merge.

**Authority/evidence:** The source-comment rule forbids review-round history in new source comments. Four comments say “#637 round 2”; line 168 says “round 1's order.” These are test-source comments, not a findings page. The three instances assigned in round 6 were removed; these five are separate imported instances.

**Impact:** Wording-only process history. No test, code, figure, clause or privacy claim changes. This does not make a lens unclean.

**Exact fix:** At lines 154, 316, 345 and 386 replace “#637 round 2:” with “#637:”. At line 168 replace “round 1's order:” with “The former restore order (#637):”. Preserve behavior/reason text and requirement IDs.

**Verification:** Inspect added source-comment lines; remove the five history labels without executable changes.

## Applied-lens evidence

**Conformance:** Read MEDIA_CLOCK_FOLLOWING.md:1817-1979, queue/root parameterization, refused-count ABI and public presentation/offset rulings. A negative timestamp no longer causes whole-PDU loss within the supported late reach. Presentation reference, per-interface lead and bind-wipe-only flush remain intact. Own-identity to GM A remains a real grandmaster change; the test repair does not exempt it. Stored-versus-applied notification behavior has integrated evidence at the adopted pin. F1 and F3 leave this lens unclean.

[R678] PASS RTL - hdl/ieee1722/aaf/KL_render_queue.sv:287-360,440-550,766-801,914-921; its hdl/milan/milan_datapath.sv instantiation; dc9cda7d against both parents - checked signed difference, positive division bias, quotient/frame widths, wrap interpretation, event walk, saturation and once-per-PDU accounting, root-derived maximum reach, unchanged bank/flush paths, and preservation of dev restart/adopted-pin behavior. No unresolved RTL finding in this delta.

The bounded mono payload behind the root's 2,048-byte receive FIFO yields a 504-event reach. Widened frame arithmetic accommodates that reach and the forward queue window. Events at/before the read frame are refused individually; later events can enter. Beyond the backward reach, whole refusal is safe because none of the bounded PDU's events can recover into the window. No new crossing primitive or clock/reset path was introduced by this repair.

[R678] PASS Robustness - tb/verilator/render_queue/sim_main.cpp; tb/verilator/milan_dp_render/sim_tdm8_render.cpp; tb/verilator/milan_dp/sim_gmstep.cpp:956-995; gmstep_mutants.py:202-217,263-271; named campaign receipts - checked negative/fractional timestamps, mixed late/in-window/early events, maximum payload, reach boundary and beyond, timestamp wrap, odd channels, two interface leads, reset/bind/closed-epoch remap, boot identity and event-qualified talker stopping. No unresolved Robustness finding in this delta.

**Tests:** Compared changed graders and mutation anchors with their claimed defects. T26 keeps stream 0 active while stream 1 closes the epoch, changes the map while commits remain observable, and grades nonempty decoded silence. The ungated-commit mutation is killed by name. The GM-stop control latches on gm_recentre_p_r AND the raw talker gate being open, after acquisition and stream provisioning. It uses no pulse ordinal, boot-cycle constant or fixed boot delay. gmstep_probes.vlt declares public_flat_rd only; the C++ observer reads the pulse and held identity without writing them. F2/F3 concern inventory/authority claims, not a failed campaign.

**Docs:** Compared timing, recovery, register, compliance, area and test authorities with source and receipts; inspected all conflict files, current resource notes, source comments and PR history. Old setpoint/re-base descriptions are retired at the previously named sites, and the area history preserves #771 facts. F1-F3 remain; R1 belongs on the residue checklist.

## Merge resolution

Checked twelve semantic resolution items across all seven conflicted files. The public conflicts.txt groups them as nine diff3 blocks; this table splits compound blocks by independently required facts. Display hunk count is not a substitute for semantic review.

| Item | Artifact | Result at the head |
|---|---|---|
| 1 | CHANGELOG contents | Both media-phase and #771 adoption entries |
| 2 | CHANGELOG sections | Both complete change sections |
| 3 | MEDIA_CLOCK_FOLLOWING switch row | #645 settle bound and retired #386 history |
| 4 | Same, loss/return row | Distinct AAF/CRF returns; #761 both CRF lock edges and controls |
| 5 | BAREMETAL_FIRMWARE census/flush rows | 4/2 PHC reference counts and bind-only flush; no restored re-base reader |
| 6 | Same, restart row | CRF lock XOR, received mr and both AAF terms |
| 7 | MILAN_COMPLIANCE_MATRIX AVTP rows | #761 mr and #632 no-re-base retained; presentation row has F1 |
| 8 | TESTING campaign rows | #637 map-record/63-control row plus this PR's GM-step/media-phase rows |
| 9 | Same, media-clock suite row | Dev's per-edge CRF restart controls |
| 10 | Same, TDM render suite row | Presentation law replaces setpoint law; pull-in/history coverage retained |
| 11 | Builder gate 1b | Printed facts, initializer and mutant messages retain bind-only flush and lock edges |
| 12 | milan_dp_mclk README leg B | Per-output request/mr, settle bound and 0.8 s gaps retained together |

Shared clean-merge dependencies examined include root restart/queue wiring, CRF format/timeout handling and acceptance-qualified timestamp pulse, test source lists, map-record integration, GM-step restart anchors, media-clock controls, evidence-reader counts and resource/submodule adoption records. No dev behavioral loss was established. The findings prevent claiming every merged documentation statement is clean.

## Execution evidence and provenance

Source evidence is at [0ca01426, author-r7](https://github.com/kebag-logic/milan-fpga/tree/0ca01426bbafc52fce122363488d535e4a131b0c/review-evidence/632-r1/author-r7). Verified 418 selected files, 5,137,426 bytes, against published_sha256: zero mismatches. The public Git commit API reports this commit as **unsigned**. This establishes manifest/content integrity at the immutable publication, not cryptographic signature authentication. See public-evidence-verification.json and evidence-commit-verification.json.

These are author executions, reconciled with logs and head markers, not a manager source bank. The final citation commit changes prose/comments. The GM-step repair after d835ba12 changes no file under hdl, syn or configs. Earlier receipts are carried only across changes outside the inputs they grade.

| Evidence | Verified result and boundary |
|---|---|
| TDM8 render, d835ba12 | 31/31: 20 source/shape mutations, 3 leg defects, 3 clean skew controls and 5 clean elaboration/mode checks. Every inventory entry has its named PASS line, including T26 |
| Pull-in, d835ba12 | All 18 boot phases plus history: 19 successful logs; 28 checks per boot phase, 272 in history; zero failures |
| GM-step, c2c996fa | 23/23: 21 controls and 2 clean legs; audited against current AST inventory |
| Stop planted alone | Repaired source and dev e5b480a3 with only the test patch: baseline and boot checks pass; the named four-interval pause check fails. Each run has 12 consequent failures, not a single-check failure |
| Boot clean/control | Clean leg 196/0. Own-identity exemption leaves baseline traffic intact and fails exactly the new boot check, at source and dev test-patch runs |
| SET_STREAM_INFO at processor 93fb0b2d | NOTIFY 461/0. Eleven GSI mutants caught plus one clean check. No splice needed; current design/README/change-log status says it passes |
| Full sweep, c2c996fa | 64 selected, 63 passed, one timeout; 2,190,061 checks and zero in-suite failures. Not a 64/64 successful single sweep |
| capture_coherence | Sweep's 2,400 s wall timeout recorded. Two separate successful receipts have the 447 and 20,832 check tallies, zero failures and complete control campaign. One publishes verdict lines plus the large-log hash; the other includes the full log |
| Firmware/boundary | Seven firmware gate rc files are zero; rerun boundary gate at c2c996fa is zero |
| Docs under make 4.3 | Command ledger: 42 executed steps pass; two non-executions recorded (host runner restriction; destructive no-Git command replaced by archive check). No claim prohibited host actions ran |
| Final docs gates | Five checks at 417ec528 exit zero; they do not detect F1-F3 |
| Lint/synthesis | Lint 89 against budget 89, current test-fix lint passes. Published Yosys bank 60 tops pass, zero fail; integrated datapath nonzero. Neither full bank rerun here |
| Builder | Published bank passes with physical/calibration skip; skip is not hardware proof |

The eleventh resource record matches the three published JSON records exactly. Out-of-context figures, identity, flow and scopes equal #771/dev; their input digests change. They are not byte-identical historical records.

| Endpoint | LUT | FF | Slices | RAMB36 / RAMB18 | WNS ns |
|---|---:|---:|---:|---:|---:|
| route-1x1 | 51,259 | 53,208 | 15,835 | 74 / 27 | +0.236 |
| ooc-1x1 | 23,828 | 20,000 | not recorded | 16 / 3 | +3.337 |
| ooc-8x8 | 32,467 | 28,220 | not recorded | 21 / 5 | +1.139 |

All three final resource-check receipts report success. Independently ran check-baseline: three endpoints pass. Notes cite both the [block-RAM exception](https://github.com/kebag-logic/milan-fpga/issues/632#issuecomment-6309313685) and area extension, retain 15 of 15,850 slices left, and identify Mark II #640 recovery. No tolerance was silently relaxed.

Own execution was focused: verified compiler identity 5.050; exact-head queue export passed 39 checks at two interfaces and 38 at odd channels, zero failures. Two builds ran concurrently with eight inner jobs each, within sixteen total. Portable scripts, raw logs with host paths redacted, and return codes are included; own-log-redactions.json records the hashes and redaction scope. No full parent/processor/gPTP/synthesis/builder bank or hardware run was performed here.

## Prior public findings

Read the six previous reports only after the independent pass and initial verdict/ledger: [R678-1](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6299647615), [R677-1](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6299997695), [R678-2](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6306376430), [R677-2](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6306520485), [R678-3](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6339307135), [R677-3](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6341403630).

| Prior item | Disposition and cause-specific evidence |
|---|---|
| R677-3-F1, partially late PDU | RTL/test cause resolved by biased division, per-event walk, boundary tests and controls. Compliance wording retained as R678-4-F1; that documentation claim is not banked clean |
| R677-3-F2 / R678-3-F2, figures/counts | Assigned figures corrected: current queue 531 LUT/236 FF and 883 LUT/402 FF; 553/228 and 890/387 explicitly historical; queue campaign 26, follow-ring 16; evidence-reader expectation updated; wrong two-frame description removed. New GM-step table count is F2 here |
| R677-3-F3, T26 | Resolved by two-stream closed-epoch map-write case and full 31/31 campaign |
| R678-3-F1, retired prose | Named TIME_SYNC/recovery/bind-wipe statements corrected. Current compliance contradiction retained as F1 here |
| R678-3-F3, full campaigns | Source gap resolved: full render, all pull-in phases/history and full GM-step published and inventory-audited. Current-dev candidate execution remains separate |
| R678-3-R1 / R677-3-R1 | Three assigned history comments removed by 0ffcd7f0; imported #637 instances are R1 here |
| R677-2-F1, notify gate | Real adopted-pin integration now resolves the dependency: 461/0 and 11 mutants. No longer based on splice-only evidence |
| R678-2-F1, CRF carry | Repair retained: carry reaches 64-bit stamps, readback saturates, reset/runtime boundaries and truncation controls retained; no delta reversion |
| R677-2-F2, reference after hold | Repair and det:afterhold/hold_keeps_ref retained; detector implementation unchanged |
| R677-2-F3, PR figures | Corrected historical figures remain separated from current records; no renewed original-cause defect |
| R678-1-F1, listener pins | Build-now implementation retained, campaigns supplied and partially late behavior fixed; physical proof still pending under explicit scope |
| R678-1-F2, offsets | Superseded by AAF-exact ruling; raw AAF, rounded CRF; full-width CRF fix retained |
| R678-1-F3/F4, fold/snapshot hold | Prior repairs and detector/hold checks retained; delta does not invalidate those causes |
| R677-1-F1/F2/F3 | Blend closing-interface/pop-edge repair, PHC-step hold, settled timing/range checks and named controls retained; current sweep exercises their suites |
| R677-1-F4/F5 | Corrected budget basis and three divider comments remain corrected |
| R678-1-R1 | Public reviewer roles explicit |
| R678-2-R1 / R677-2-R1 | Assigned reviewer-ID comments remain removed |
| R677-2-R2 | Comments retain as-set AAF/as-applied CRF distinction |
| R678-2-R2 / R677-2-R3-R5 | Deferral superseded by build-now; assigned scope prose updated. Current contradiction explicitly retained as F1 |
| R677-2-S1 | Overtaken by AAF-exact ruling; no monitor mismatch established |
| R677-2-S2 | Carry-wrap cause repaired; additional factory-row policy guard optional |
| R677-2-S3 | Closing-cycle fold-reference behavior unchanged/documented; optional suggestion retained |
| R677-2-S4 / R677-1-F6 | Separately literal data-delay coupling remains optional maintainability work |
| R677-3-S1 | Declared buffer versus fixed queue remains optional policy follow-up under the fixed-shape decision |
| R677-3-S2 | Stale CI image command inventory remains optional; no active workflow using retired setpoint target established |
| R677-3-S3 | Hard-coded refusal tallies replaced by declared PDU-refusal enumeration; addressed |
| R677-3-S4 | Source campaign gap addressed; final candidate publication pending |

## Reviewer-owned ledger

Every lens was applied. CLEAN means no open BLOCKER, MAJOR or MINOR under that lens in the reviewed scope, with unchanged-cause carry-forward described above. F1-F3 prevent completion.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1, F3 | Public rulings; presentation law; queue/root; REGISTER_MAP; compliance row; boot/PathTrace citations; notification receipts | R678-4, applied but not clean | 417ec52864efc09f1e3ecd0f755cb0daa7604426 |
| RTL | CLEAN | Queue arithmetic/banks/counters; root integration; CRF/restart merge dependencies; both-parent diffs; resource records; test-only repair boundary | R678-4 | 417ec52864efc09f1e3ecd0f755cb0daa7604426 |
| Robustness | CLEAN | Queue boundary/wrap/odd/two-interface tests; T26; stop/boot controls; full render/pull-in/GM-step receipts | R678-4 | 417ec52864efc09f1e3ecd0f755cb0daa7604426 |
| Tests | UNCLEAN: F2, F3 | sim_tdm8_render; sim_gmstep; read-only probes; AST inventories/logs; recovery table; gPTP test authority comments | R678-4, applied but not clean | 417ec52864efc09f1e3ecd0f755cb0daa7604426 |
| Docs | UNCLEAN: F1, F2, F3 | Timing/recovery/interface/compliance docs; seven conflict files; area/Mark II records; source comments; PR history/evidence | R678-4, applied but not clean | 417ec52864efc09f1e3ecd0f755cb0daa7604426 |

## Limits, pending duties and integrity

No manager source bank exists at this head, and none is inferred. Source receipts do not validate a future current-dev merge candidate. The manager must construct that candidate at live dev, run and publish required builder/native banks and hosted/local replication acceptance, reconcile independent reviews and lens coverage after fixes, obtain merge authorization, and complete post-merge containment and issue/project closure. No GitHub write, source fix, commit, push or merge was made here.

hosted-snapshot.json records exact-head contexts observed during review: some executed successfully, others were queued/in progress, and Physical gPTP was skipped. A successful scheduling/gate context does not replace uncompleted long jobs. No hosted acceptance verdict is claimed. Physical calibration was NOT RUN; field skips, simulations, resource timing and source evidence are not hardware proof of the #764 method.

checkout-verification.json confirms all 1,447 root tree entries, tracked blob bytes/modes and index match the exact head/tree. The five required submodule gitlinks, checked-out heads, bytes/modes and indexes match: processor 93fb0b2d, timing processor 55680bff, lwSRP 08ee86e8, stack 70936b77 and stream library 48ff7a7e. Unrelated external remains uninitialized. No restoration was needed: builds used a disposable exact-head export.

Portable reproduction: fetch_receipts.py; audit_receipts.py REPOSITORY; spotcheck.py REPOSITORY SCOPED_COMPILER for the focused shapes; verify_checkout.py REPOSITORY for final state. package_receipts.py copies the bounded raw evidence subset. Exports, downloads and builds under scratch/ are excluded from publication. MANIFEST.sha256 lists publishable scripts and receipts; REPORT.md is the review artifact. Included: 105 copied public raw receipts, independent reconciliation, own focused logs/return codes, authority snapshots and integrity results.

R678-4 FINISHED
