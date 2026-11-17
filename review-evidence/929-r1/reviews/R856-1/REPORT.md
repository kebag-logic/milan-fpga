[R856] POSITIVE - exact head 372556835d03b70134b2e76567b63b25c4cca005

R856-1, external independent review of issue #929 / PR #935. Tree `34b71495c92a7dbee90c516354100ed61a51446e`; reviewed all five commits and all ten changed files in `70f4056f384e12520ccae254fe26f6286fd39db6..372556835d03b70134b2e76567b63b25c4cca005`.

All five lenses and supplemental local executions are complete.

No BLOCKER, MAJOR or MINOR finding. One wording residue follows. This is a source review verdict, not merge authorization or validation of the current-dev candidate.

The review followed AGENTS.md, CONTRIBUTING.md, docs/README.md, the [issue's public scope](https://github.com/kebag-logic/milan-fpga/issues/929), REQUIREMENTS.md, docs/design/MAILBOX_SPLIT.md, sw/firmware/ctrl/srp/README.md, and [#895's corrected declaration contract](https://github.com/kebag-logic/milan-fpga/issues/895). The applicable portions of IEEE 802.1Q-2018 35.2.2.8/35.2.2.8.7, Tables 35-6 and 10-3, and Milan v1.2 4.3.3.1/4.3.3.2/Table 4.4 were read from the standards. The diff was examined before executable evidence and prior-findings reconciliation. No private author material or other reviewer's report informed this verdict or ledger.

**Finding R856-1-D1: RESIDUE; Docs; `sw/firmware/ctrl/srp/README.md:320-321`.**

Authority/evidence: the final sentence groups all three new plants under the qualification that the two-source shape cannot catch them. The source comment at `sw/firmware/ctrl/test/srp_mutants.py:310` and the PR's table correctly distinguish the first two. Independent runs confirm those two are inert at 1x1; duplicate ownership is caught at both shapes. The third plant verifies that the repaired 8x8 fixture reaches the attachment assertion.

Impact: the prose obscures the distinct reason for the third plant. Test definitions, executed results, population, clause interpretation and verdict are unaffected. This is a prose qualification correction under the supplied residue rule.

Required outcome/exact fix: replace that final sentence with: "The two-interface campaign also plants these three defects at the 8x8 entity." The detailed distinction already appears in the source comment and PR table.

Verification: compare the replacement with `srp_mutants.py:310-323` and `srp-focused.log`. No test or measurement changes. Carry D1 to the manager's residue checklist.

**Five independently applied lenses**

[R856] PASS Conformance - `tb/verilator/milan_dp/twin_compare.py:257,466,610`; `sw/firmware/ctrl/test/srp_mbx.cpp:284`; `sw/firmware/ctrl/srp/srp_mbx.c:252-325` - The deleted row described pre-#895 behavior. Its removal also removes those Talkers from `owed_msrp`, exposing them to the ordinary LeaveAll comparison; Table 10-3 grading remains active. Local captures contain Advertise for stream `0200000000010000`, followed by withdrawal: split 5190/20190 ms, fabric 5200/20000 ms. The base comparator on identical captures reports exactly the stale row failure; the head reports zero (`twin-trace.log`). The nine-source unit fixture deliberately has no MAAP validity gate: source 0 is allocated; eight unallocated sources report code 2, consistent with the adapter contract and Table 35-6. Product validity remains governed by Milan 4.3.3.1.

[R856] PASS RTL - complete range diff; `tb/verilator/milan_dp/Makefile:956-990`; `dynmap_mutants.py:109-123,460-491`; `sw/firmware/ctrl/srp/srp_mbx.h` pool definitions - No RTL, production firmware, mailbox contract, budget bound or gitlink changes. Existing clock/reset/CDC and state-owner contracts retain their base implementations. The input recipes come from their owning suites. The dispatch fixture doubles each shape-derived pool class and arena; it preserves second initialization, attachment refusal, ownership transfer after destruction and zero-leak checks. Image receipts support the unchanged production scope.

[R856] PASS Robustness - `dynmap_mutants.py:460-473,641-667`; `srp_mbx.cpp:284-332,715-732`; `twin_plants.py:231-266` - Each selected leg prepares inputs before its control; a failed make or absent file invalidates the campaign, regardless of later catches. Independent simulated-success/no-input probes exercise all five named legs and require nonzero campaign exits. Actual listener/talker recipes populate absent files in a separate fresh clone. Startup retains Domain/VLAN checks, an exact aggregate Talker count, and each StreamID's type, events, timing, TSpec and failure code. Four complete mailbox arms retain reset, backpressure, ordering, link and cleanup coverage. The new wire plant preserves identities/events and adds the specified nine-byte failure information, updating both length fields.

[R856] PASS Tests - `srp_arms.py:98-102`; `test_ctrl_firmware.py:196,203-220`; `srp_mutants.py:310-323`; `twin_compare.py:67-125,660-672`; `twin_plants.py:231-266` - Independent full mailbox runs pass 74/74 at 1x1 and 8x8, each with one and two interfaces. All three new defects fail their named 8x8 assertions; the first two escape at 1x1 and duplicate ownership is caught at both shapes. The workflow's suites phase includes both new arms. Campaign dispatch excludes the shape-specific additions from its selected one-interface population. Restated plant words retain specific matching to the Advertise trace; the new failed-Talker plant exercises the ordinary comparison after removal of the exception. No check was weakened merely to pass.

[R856] PASS Docs - `tb/verilator/milan_dp/README.md:914,1385-1500`; `sw/firmware/ctrl/srp/README.md:316-321`; PR body, issue REVIEW READY, archived workflow and image receipts - Scope, input preparation, shape arms, stale-row cause, changed diagnostic words and remaining TSpec comparison limitation are publicly reconstructible. Added source comments contain behavior/reasons and issue or clause references, with no new prohibited lane/reviewer/round labels. D1 is residue. The explicitly excluded existing items remain limitations, not new findings.

**Reviewer-owned coverage ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #929/#895, cited standards; twin_compare.py:257/466/610, srp_mbx.cpp:284, srp_mbx.c:252; twin-trace.log | R856-1 | 372556835d03b70134b2e76567b63b25c4cca005 |
| RTL | CLEAN | Complete range diff; Makefile:956, dynmap_mutants.py:109/460, srp_mbx.h pool definitions; image receipts | R856-1 | 372556835d03b70134b2e76567b63b25c4cca005 |
| Robustness | CLEAN | dynmap_mutants.py:460/641, srp_mbx.cpp:284/715, twin_plants.py:231; dynmap-probes.log, four full mailbox logs | R856-1 | 372556835d03b70134b2e76567b63b25c4cca005 |
| Tests | CLEAN | srp_arms.py:98, test_ctrl_firmware.py:196/203, srp_mutants.py:310, twin_compare.py:660; srp-focused.log, twin/dynmap receipts | R856-1 | 372556835d03b70134b2e76567b63b25c4cca005 |
| Docs | CLEAN | Changed READMEs, public scope/PR, archived receipts and evidence-audit.log; D1 is residue | R856-1 | 372556835d03b70134b2e76567b63b25c4cca005 |

**Evidence provenance and limits**

Prior-findings reconciliation was performed after this independent verdict and ledger were written. PR #935 had two review-start comments (6932764210 and 6932772912), zero submitted reviews and zero inline review threads. No prior public finding on this PR required resolution or retention. Both public manager comments were examined; neither asserts a manager source bank.

Independent execution at the exact head:

| Check | Result | Local receipt |
|---|---|---|
| `make -j16 -C tb/verilator/milan_dp twin` with scoped simulator and four compile jobs per half | rc 0; zero findings | twin.log, twin.rc |
| Same recipe, `twin-plants` | rc 0; 21 plants, each refused both ways | twin-plants.log, twin-plants.rc |
| Four full `srp_mbx.cpp` arms, both entity shapes and interface counts | 74/74 each, all rc 0 | srp-control-*.log/.rc |
| Three new SRP plants at 8x8; paired 1x1 controls | three named catches; first two inert at 1x1; duplicate ownership caught at both | srp-focused.log and individual srp-*.log/.rc |
| Fresh-tree dynmap selected cases 36 and 37, `--jobs 4` | listener and talker controls pass; both named mutants caught; 4/4, rc 0 | dynmap-focused.log/.rc, dynmap-probes.log/.rc |
| All five legs with input make replaced by success without outputs | each leg named and campaign rc 1, as required; mutant execution stubbed for these refusal probes | dynmap-probes.log |
| Single absent input and failed-make guards | 11 individual missing-file refusals plus five failed-make refusals | input-guards.log |
| Base comparator replay on local head captures | exactly the stale owed-row failure; head comparator zero | twin-trace.log |
| Capture digests compared with published base/#932 digests | both captures byte-identical | capture-identity.log |

Reproduce with `prepare_clone.py SOURCE PACKET/scratch/tree`, then `run_focused.py PACKET/scratch/tree PACKET SCOPED_SIMULATOR`. Use a second fresh clone for `dynmap_probe.py FRESH_CHECKOUT PACKET SCOPED_SIMULATOR`; it prepares both affected legs and invokes cases 36/37 with `--jobs 4`. `input_guards.py CHECKOUT PACKET` exercises isolated input sentinels without RTL builds. `twin_trace.py CHECKOUT PACKET` replays the base comparator. These scripts, raw diagnostic content and return-code receipts are included in the manifest. Published logs replace host paths with placeholders only; untouched originals remain under unpublished `scratch/raw`. The capture JSONs are unchanged.

The [published author packet](https://github.com/kebag-logic/milan-fpga/tree/c836e7a857b6b4333b78910e5502a42a03697380/review-evidence/929-r1/author-r1/receipts) supplies source-head execution evidence. `audit_evidence.py` verifies all 267 extracted receipt hashes and reconciles:

- Twin: zero findings; 21 distinct plants refused twice each.
- Fresh-clone dynmap: five controls and 66 named catches, 71/71. Both one-off listener input-step plants retain diffs, named failures and rc=1. Their relevant source is unchanged by later documentation/wrapping commits.
- Workflow replay: 14 jobs, 88 zero-rc steps, 56 explicitly not-run steps. The unsuccessful first boundary attempt is retained separately; final receipts show rc=0. Full SRP-mutants and one documentation-gate log are omitted; hashes and rc receipts remain. The 424-catch total is the author's reported result, not an independent full rerun or a count recovered from an omitted log. Dispatch inspection finds 306 two-interface and 116 one-interface source mutants, plus two pin refusal controls.
- Release firmware: six matching binary/disassembly/stripped-ELF hashes across two configs. Whole ELFs differ; the published section audit identifies only debug-section differences.
- Split firmware: all 24 recorded ELF/stripped/loadable hashes match across four ledger points and the two configs' mapped/stand-in images. Both ledger receipts pass all four points.

Local scripts take checkout/packet paths as arguments. Builds and mutations remain in packet scratch trees; supplied worktree files were not edited. Simulator identity was verified as 5.050, revision v5.050, before use. Independent campaigns ran concurrently under foreground supervisors with bounded compilation concurrency. `tree-integrity.log` proves the supplied head/tree, actual tracked blob bytes/modes, index entries and all five required populated submodule pins/bytes. The unrelated unpopulated `external` gitlink is verified in the index only.

The known STREAM_OUTPUT notice omission, 73-versus-217 MaxFrameSize difference and pre-#895 SRP-transmit README section remain supplied scope exclusions. This review does not claim Talker TSpec equality, live audio or hardware operation. Physical calibration was NOT RUN; field skips are not hardware proof.

No manager source bank exists at this head and none is inferred. No full parent/processor/time-plane/synthesis/builder bank, hardware test, container workflow replay, source fix, commit, push or GitHub write was performed here. Hosted acceptance remains with the manager.

Pending manager duties: reconcile the internal review and open findings, carry D1 to the residue checklist, validate the exact current-dev candidate with the required builder/native banks and publish receipts, accept hosted/local workflow evidence, obtain merge authorization, then complete containment and issue/project closure. Source base `70f4056f` differs from the supplied live-dev reference `6b66f66d89cf25d2717687bcc2c3bf617685a99a`; source evidence does not validate their composed candidate.

R856-1 FINISHED
