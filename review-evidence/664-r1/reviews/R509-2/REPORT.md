[R509] POSITIVE - exact head 8fb296e3e02985aee27ef04cb08278836b734a14

External independent review, R509-2, issue #664 / PR #674.
Tree: `ce846f8ab472d3c9bf605598224ae2521966d928`.
Source base: `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.

All five lenses are CLEAN. Both prior MINOR findings are resolved at this head, and the prior publication-wording residue is resolved. No BLOCKER, MAJOR or MINOR remains from this review. One additional wording-only residue is recorded below. This verdict does not supply owner approval or authorize merge.

Reconstruction followed the requested order: repository operating contract and documentation index; frozen issue and public scope decisions; linked requirements, standards and interfaces; full base-to-head diff and history; public executable evidence. The independent verdict and ledger were recorded in `independent-pass.md` before prior public findings were opened. No private author material, management checkout, lane scratchpad or unpublished reviewer report was read. Earlier unaffected conclusions stand.

**Prior findings, explicitly reconciled**

The prior public findings are [R509-1](https://github.com/kebag-logic/milan-fpga/pull/674#issuecomment-6010388957) and [R508-1](https://github.com/kebag-logic/milan-fpga/pull/674#issuecomment-6010426351). No submitted reviews or inline comments added further findings at observation.

| Finding | Original severity and attributable lenses | Disposition at this head |
|---|---|---|
| R508-1-F1 = R509-1-F1 | MINOR; Conformance, Docs | RESOLVED. `docs/reference/FR_NFR.md:367` and `:368` assign conflict/loss/retry to IEEE 1722-2016 B.3.2/Table B.7, constants to B.3.3/Table B.8, and the received event/DEFEND action to B.3.5.5/B.3.6.6. Both primary approval rows are byte-identical to the head. |
| R509-1-F2 | MINOR; Conformance, Robustness, Tests, Docs | RESOLVED. `FR_NFR.md:360`, `:403`, `:411` and `:576` cover received AVAILABLE/DEPARTING and original TMR_NO_ADP expiry through every matching sink's discovery and connection commitments and any resulting TX commit. `docs/design/MAILBOX_SPLIT.md:345` agrees. |
| R508-1-R1 = R509-1-R1 | RESIDUE; Docs | RESOLVED. The public PR body identifies the published candidate and makes the executor's earlier local-only activity explicitly historical. |

The listener checks cite IEEE 1722.1-2021 6.2.2.5 and Milan v1.2 5.6.4.1, Table 5.54 and 5.6.4.5.1-.4. They preserve received validity, restart ordering, interface and GM/domain guards, departing and expiry behavior. One shared allowance includes all matching sinks and subsequent connection/TX work; normative waits are recorded separately. Delayed event publication and state handoff cannot reset timing. Received validity 1, 10 and 31 and completion of ignored input handling are explicit checks. `standards-audit.md` records the independent clause comparison.

**Finding R509-2-R1: RESIDUE; Docs**

- Artifact: `sw/firmware/ctrl_nvm/README.md:464`.
- Authority/evidence: The unchanged limitations bullet still says F0's switch is unmerged. The same page's updated line 124 calls its HAL merged; `docs/design/MAILBOX_SPLIT.md:3` describes the implemented default-off foundation, and `sw/litex/milan_soc.py:3580` contains the switch.
- Impact: Obsolete publication-status wording only. The stated absence of an image linking the store remains unchanged. This corrects no measurement, figure, verdict, test, code, generated artifact, normative clause or privacy claim, and does not reopen a clean lens.
- Required outcome / exact fix: Replace the two-line bullet with: `- The #665 switch and its link: no image links this store yet.`
- Verification: Read the corrected bullet against the page's merged-HAL statement while retaining the unintegrated-store limitation. Carry it on the manager's residue checklist.

**Artifact-specific lens results**

[R509] PASS Conformance - `REQUIREMENTS.md:22`; `docs/reference/FR_NFR.md:321`, `:329`, `:360`, `:367`; public decisions 6009576644, 6009675758 and assignment 6010431422 - The documents follow the approved scope: all five control functions are selectable, including AECP notifications and counter serving; media, framing, filtering, timestamps and gPTP remain in fabric. All-fabric remains supported and shipping until F2-F5 acceptance. The new listener obligation and corrected MAAP authority match the primary clauses. The proposed 10 ms remains project policy requiring owner approval, with normative response limits, ordering and timer tolerances independently binding.

[R509] PASS RTL - `scope.json`; `docs/ARCHITECTURE_HW_SW_SPLIT.md:30`, `:67`, `:111`; `docs/reference/MAILBOX_CONTRACT.md:20`; `docs/design/MAILBOX_SPLIT.md:109` - The complete lane changes 21 Markdown files; round 2 changes two documents in four commits. No RTL, firmware source, test, default, VERSION, generator or gitlink changed. Single ownership, coherent fabric observations, 32-bit complete-record publication, cross-channel TX ordering, one interrupt, bus/HAL boundaries and F1 boot/apply terminals remain consistent. New CDC, reset or width behavior is not introduced. Listener admission and runtime integration remain explicitly future F3 work.

[R509] PASS Robustness - `docs/reference/FR_NFR.md:336`, `:403`, `:411`, `:428`; `docs/design/MAILBOX_SPLIT.md:341` - Applied the listener transitions to mismatch, restart, departure, expiry, ignored input and stale-event cases. Original deadlines, backlog, full TX rings, all matching sinks and delayed publication stay inside one service allowance. Global checks retain reset, wrap, CPU stalls, NVM work, maximum supported shapes and both adapters. Wire deadlines are measured separately; recovery does not erase late service.

[R509] PASS Tests - `docs/reference/FR_NFR.md:392`; `docs/ARCHITECTURE_HW_SW_SPLIT.md:191`, `:226`; `focused-results.json`; `archive-results.json`; `approval-check.log` - H-DISC now specifies an independently falsifiable late-listener/aging check even when advertiser checks pass. The contract requires state completion and subsequent TX completion, boundary validity values and every Table 5.54 cell. Existing model/access-count evidence is not promoted to implemented target-time instrumentation. All twelve focused checks passed. The five named VERSION assertions remain byte-identical and expect major 2; the later landing plan preserves the retired major-only assertion in a live suite.

[R509] PASS Docs - `docs/reference/FR_NFR.md:367`, `:368`, `:403`, `:576`; `docs/design/MAILBOX_SPLIT.md:345`; public PR approval section; `approval-check.log`; `checks/docs.log` - All 27 old/new entries and the complete timing/hook sections match the source. Only presentation links and table HTML encoding are normalized; both MAAP primary rows match without normalization. Generated traceability has no drift. Ownership searches found no surviving categorical ban on firmware service for the moved paths; shipping implementation descriptions remain scoped. The sole additional residue is publication wording, recorded above.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | REQUIREMENTS.md:22; FR_NFR.md:329,360,367; primary clauses in standards-audit.md; public scope decisions | R509-2 | 8fb296e3e02985aee27ef04cb08278836b734a14 |
| RTL | CLEAN | scope.json; split architecture sections 1-5; mailbox generated contract and F1 boot interface; integrity-final.log | R509-2 | 8fb296e3e02985aee27ef04cb08278836b734a14 |
| Robustness | CLEAN | FR_NFR.md:336,403,411,428; MAILBOX_SPLIT.md:341; Milan Table 5.54 guard comparison | R509-2 | 8fb296e3e02985aee27ef04cb08278836b734a14 |
| Tests | CLEAN | FR_NFR.md:392; split architecture sections 6-7; focused-results.json; archive-results.json; approval-check.log | R509-2 | 8fb296e3e02985aee27ef04cb08278836b734a14 |
| Docs | CLEAN; R509-2-R1 nonblocking | Full 21-file diff; round-2 two-file delta; public approval text; traceability and documentation receipts | R509-2 | 8fb296e3e02985aee27ef04cb08278836b734a14 |

**Validation and real limits**

Ten independent documentation/interface checks ran concurrently with at most four workers, with separate raw logs and exit receipts. Two additional checks ran concurrently in an exact-head source export without repository metadata. Every exit code was zero. Traceability passed 5/5 controls over 77 modules; wire accountability reported 77 checks and zero findings; added-line punctuation passed 339/339 controls over 594 added lines. The source-export documentation check explicitly skipped inventory parity because metadata was absent; the checkout check supplied that comparison. No runtime simulation or source mutation was needed for this documentation delta.

The fixed [first-round evidence packet](https://github.com/kebag-logic/milan-fpga/tree/b8faae80174f23ea928a49d0611a21884711c475/review-evidence/664-r1) hashes to its published manifest and describes the earlier head. It contains command results and artifact digests, not the full raw bank logs. Current-head [review-ready evidence](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6010818951) and the public PR body report 93 zero command exits with explicit exceptions. The assignment also reports successful manager source/static, builder and native banks. These are source-validation evidence, not reviewer execution or final current-dev candidate acceptance. Vendor analysis was skipped; historical placement calibration was NOT RUN. Field skips, compiler-absence controls and skipped physical jobs supply no hardware proof.

`public-state-summary.json` preserves one exact-head hosted observation: some digital jobs succeeded, others remained in progress, and physical testing was skipped. No eventual success is inferred. The public head and approval body were rechecked unchanged. Live dev was observed at the assigned source base; it must be checked again at the merge turn.

`integrity-final.log` proves the detached head and tree, all 1,105 root blobs and all 876 required-submodule blobs against committed bytes and executable modes, complete index entries and flags, and the required gitlinks. The unused external gitlink remains unchanged and uninitialized. The source checkout is clean; no tracked bytes required restoration. No source edits, commits, pushes, public writes, prohibited banks, container operations or hardware operations occurred.

**Pending manager duties**

- Obtain owner approval of the exact requirement text and proposed 10 ms budget; then update issue linkage as assigned.
- Obtain the other independent final verdict, accept the reviewer-owned coverage ledger, and ensure no review remains in flight. Carry R509-2-R1 to the residue checklist.
- Accept the required source evidence and its explicit limits; complete hosted/local-replica acceptance. Validate the final candidate against live dev at merge time and record head/base/tree identities.
- Obtain explicit maintainer merge authorization. After authorized merge, run the required containment and review-integrity checks, preserve their stated proof limits, and close/move the issue only when the full completion bar is met.
- Keep F2-F5 target-time measurements, all-stream/counter acceptance, audio soak and the VERSION-3 default flip as later implementation obligations. This review does not discharge them.

Portable reproduction scripts accept checkout paths. Use a packet-local environment with the repository's locked Markdown dependencies and YAML support. `run_focused_checks.py` and `check_archive.py` require `--python <packet-local-python>`. `verify_approval.py` takes the checkout and `pr-body.md`; `inspect_scope.py` and `verify_integrity.py` take the checkout. Disposable environments and licensed extracts remain under unpublished `scratch/`. `MANIFEST.sha256` is the publication allowlist; unlisted inputs are not packet artifacts for publication.

R509-2 FINISHED
