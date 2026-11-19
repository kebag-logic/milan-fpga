[R870] NEGATIVE - exact head 0d1eb8e4c5821e9431097950882659f2083d96ba

Round R870-1, external independent review of PR #952 for #951/#665. All five lenses applied. Three MINOR findings remain open. The implementation matches the approved nominal hold-off; no functional defect was reproduced in the changed code. The findings concern a clause claim, unsupported timing-evidence carry, and an incorrect placement figure. They are not RESIDUE under the owner's definition.

Tree: `d1ec05dff82782f478eaddde89b396c0c070422c`. Comparison base: `0839453f6d7135063e904bcaf4ac1852ad6b522a`, the flip-train head. Three one-line commits change nine files. This reviews that range, not the train's earlier changes or a current-dev merge candidate.

Scope was reconstructed from [#951](https://github.com/kebag-logic/milan-fpga/issues/951), its public comments, [#665's ruling, item 2](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-7007273447), and #895's accepted minimum and transmit-term rulings. IEEE 802.1Q-2018 35.2.2.8 and 10.7.4.3 and Milan v1.2 Table 4.3 were read directly. Repository authorities include REQUIREMENTS.md, FR_NFR.md 3.4.1, MAILBOX_SPLIT.md's TALKER_DECL contract and the SRP README. The independent diff pass preceded any search for prior PR findings. Public author evidence came from [archive af4b3079](https://github.com/kebag-logic/milan-fpga/tree/af4b3079a6bc8444fb0052f5611d23e1477d2fa7/review-evidence/951-r1/author-r1/receipts). No private author material was used.

**R870-1-F1 - MINOR - Conformance, Docs**

Artifact: `sw/firmware/ctrl/srp/srp_mbx.c:35`, `sw/firmware/ctrl/srp/README.md:234`, `docs/design/SPLIT_CONTROL_MEMORY.md:3173`, `docs/design/MAILBOX_SPLIT.md:1290`.

Authority/evidence: 802.1Q 10.7.4.3 specifies the nominal random draw below 1.5 x LeaveAllTime. Milan Table 4.3 additionally permits leavealltimer up to 15.5 s. The new source comment extends its 15 s maximum to a peer; the durable documentation calls 30 s the longest two periods while citing Milan. The PR acknowledges the tolerance limitation, but the in-tree explanation omits it. Two permitted upper-edge intervals total 31 s. The JoinTime/transmit terms compensate local Leave departure, not the extra second of peer-timer tolerance.

Impact: the documented coverage of Milan-permitted timers is stronger than the implemented, approved nominal bound. This is an inaccurate clause/coverage claim. It is not evidence that the chosen value violates 35.2.2.8's minimum: the code follows the explicit approximately-30.2-second ruling.

Required outcome: qualify the selected maximum as the **nominal IEEE random-draw maximum**. Record in the durable SRP/design explanation that Milan's additional tolerance is excluded and two permitted upper-edge intervals may reach 31 s. Qualify the source's peer-maximum comment and linked contract summary consistently. Preserve the approved formula unless the scope authority explicitly chooses tolerance-inclusive coverage; do not silently alter the frozen acceptance.

Verification: compare corrected claims with Table 4.3 and the public ruling. For documentation/comment-only corrections, verify executable inputs remain equivalent. A changed hold-off requires updated boundary tests, old-value controls and image evidence.

**R870-1-F2 - MINOR - Tests, Docs**

Artifact: PR #952's **"The CPU rows carry"** assertion; author receipts `cpu/compare/*-probes.txt`, `cpu/control/srp-talker-and-loss-probes.txt`; `tb/verilator/ctrl_service_budget/README.md:261`.

Authority/evidence: NFR-SCOUT-03 and FR_NFR.md 3.4.1 require path bounds; the harness's formal pass requires complete arm/group coverage. The published comparison has 156 paired probes with unchanged verdicts, covering three valid-destinations groups and selected arm A groups. It omits the complete formal bank and answering-ports paths. Executable code changes placement. Measured timing changes despite unchanged control flow: approximately -7.066 ms for `srp.talker_loss`, and +0.171 ms for the cited arm A row. The old-value-plus-padding control follows the new placement. Graders reading unchanged tables do not measure omitted paths.

Impact: useful sampled regression evidence cannot transfer every previous measured row or cost statement to the new layout. No omitted-row regression is alleged; an unchanged verdict there is unproved.

Required outcome: replace unconditional all-row carry with the measured subset's actual scope and mark complete timing validation pending. Publish the already-planned full measurement at the final train/current-dev candidate, identifying image hashes, all required arms/groups, statement/load/share checks and existing-miss dispositions. That exact-image final bank can discharge this finding; a duplicate full source-head bank is not requested. Reuse requires equality of the relevant measured and final image bytes.

Verification: inspect the complete final bank's coverage and regrading, and confirm the PR no longer treats the sample as complete carry. Until then the timing-evidence portion of Tests remains unclean.

**R870-1-F3 - MINOR - Docs**

Artifact: `docs/design/SPLIT_CONTROL_MEMORY.md:3176`; PR #952's image-diff paragraph; `images/pairs/platform-1x1-if1.imgdiff.txt` and the other nineteen pair receipts.

Authority/evidence: the new text says `.rodata` moves eight bytes with alignment. In the platform 1x1/1if receipt, `.text` grows from 0x1b7fc to 0x1b800 while `.rodata` remains at 0x1b800. Across twenty receipts, `.rodata` moves zero bytes in thirteen pairs and eight bytes in seven. It stays fixed in all four platform pairs.

Impact: the numerical placement summary misstates the measured image comparison. The underlying evidence still supports the intended hold-off-only semantic change. Correcting a measured figure is excluded from RESIDUE by the owner rule.

Required outcome: say following code moves four bytes and `.rodata` moves **zero or eight bytes according to alignment**, with SRAM unchanged; apply the same qualification in the PR.

Verification: compare the corrected summary with all twenty `.rodata` address pairs. No rebuild is needed solely for this correction.

**R870-1-RS1 - RESIDUE - Docs**

Artifact: PR #952, Linked Issue / roles. Reviewer fields still contain `[R<n>]` despite public review-start assignments. Impact: stale administrative wording only. Exact fix: replace the placeholders with the assigned sessions R869 and R870 under their published roles. Verify against the start comments. This residue does not affect verdict or lens cleanliness.

**Independent executable evidence**

Portable reproduction from the exact-head checkout and pinned dependencies:

```sh
mkdir -p "$PACKET/scratch"
git -C "$CHECKOUT" fetch --no-tags origin af4b3079a6bc8444fb0052f5611d23e1477d2fa7
git -C "$CHECKOUT" archive af4b3079a6bc8444fb0052f5611d23e1477d2fa7 review-evidence/951-r1 | tar -x -C "$PACKET/scratch"
python3 -B "$PACKET/focused_checks.py" "$CHECKOUT" "$PACKET" --jobs 4
python3 -B "$PACKET/width_checks.py" "$CHECKOUT" "$PACKET"
python3 -B "$PACKET/audit_evidence.py" "$PACKET/scratch/review-evidence/951-r1"
python3 -B "$PACKET/verify_checkout.py" "$CHECKOUT"
```

- `focused-1x1.log`, `focused-8x8.log`: 16 Talker tests and 9 composed SrpGate tests at each point, all 50 passing. Independent processes ran concurrently with four compile jobs each, joined by a foreground driver.
- Twenty mutations caught their named defects, ten per point: old two-LeaveAllTime value directly and after a composed MAAP conflict, one-period/omitted-term/down-rounded-term/never-ending holds, and all three re-anchored LeaveTime mutations. Individual failure logs are retained. The old-value 1x1 test sees declaration at 20,630 ms against 30,570 ms required. Those failures are expected mutation results.
- `width.log`: 32 successful checks over four shapes and host/target compilers. Actual sources accept normal values and 65,535, reject 65,536, and reject the normal hold with `held_cs` narrowed to eight bits, naming the static assertion. It reads the element's actual size; current uint16_t storage on these 8-bit-byte targets gives the correct exclusive limit of 65,536.
- `evidence-audit.log`: published manifest hashes match; twenty image reports each identify only the SRP object changing, and three normalized listing lines. Forty relinks are reported load-byte-equal to their built originals. All twenty image hashes match between the first code commit and the width-check commit. The last commit changes only four Markdown files.
- `checkout-integrity.log`: physical tracked bytes, executable/symlink modes and full index equal the reviewed head. Five required submodules match their gitlinks and physical bytes/modes/index. Optional `external` is uninitialized and unused. Disposable mutated source copies and linked test builds stayed under packet `scratch/`; no tracked source was edited.

Published diagnostic logs retain test output and numbers; absolute checkout/packet prefixes are replaced by `<checkout>`/`<packet>`. One compiler-generated untracked stack-usage sidecar was moved into scratch and the portable compiler probe now sets its working directory there. The final checkout has no untracked residue.

**Lens results**

Conformance: checked `srp_mbx.c:32-46,526-527` against #951/#665 and both IEEE clauses. LeaveAllTime is named once, the maximum is derived, JoinTime stays 19 cs and transmit terms stay ceil(35/10), ceil(77/10), ceil(105/10). Values are 3,023, 3,027 and 3,030 cs. Nominal scope is met; F1 prevents clean coverage of the clause claim.

[R870] PASS RTL - `sw/firmware/ctrl/srp/srp_mbx.c:141,315,526`, `srp_mbx.h:167`, complete nine-file diff - traced loading, saturating countdown, expiry scheduling and unchanged declaration gate. The 16-bit count safely holds each value. Accepted withdrawal starts the hold; a refused Leave does not. Unchanged destinations can return immediately, moved ones wait. No RTL, clocks/resets, CDC, mailbox ABI or submodule pins change. Image object/map evidence supports a four-byte constant-load expansion. Timing evidence has F2's limit.

[R870] PASS Robustness - `sw/firmware/ctrl/test/srp_talker.cpp:294,340,463,583`, `srp_gate.hpp:319`, both focused logs and width.log - applied reset/reallocation, validity changes, unchanged destinations, admission changes, refused joins/Leaves, expiry and storage-boundary checks. Small/large source shapes and both interface counts pass. Existing malformed-input and LeaveTime behavior is unchanged; the three updated mutation anchors still detect their faults. This covers the selected nominal hold, not tolerance-inclusive peer aging.

Tests: inspected the independently stated horizon, decoded-wire assertions, latest-Leave scheduling, composed conflict fixture and mutation needles; reproduced positive/negative checks. These are adequate for the formula change. F2 leaves the broader timing carry claim unclean.

Docs: read all four changed Markdown files, PR/Issue evidence and source-comment delta. Historical 20-second references remain contextualized. No new prohibited source-comment session/bench label was found. F1-F3 remain open; RS1 is residue.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #951/#665; 35.2.2.8, 10.7.4.3, Milan Table 4.3; srp_mbx.c:32-46,526; SRP README:234 | R870-1 applied; no clean covering round | 0d1eb8e4c5821e9431097950882659f2083d96ba |
| RTL | CLEAN | srp_mbx.c:141,315,526; srp_mbx.h:167; width.log; 20 image-pair receipts; full diff | R870-1 | 0d1eb8e4c5821e9431097950882659f2083d96ba |
| Robustness | CLEAN | srp_talker.cpp; srp_gate.hpp:319; focused logs; width.log; 20 mutation logs | R870-1 | 0d1eb8e4c5821e9431097950882659f2083d96ba |
| Tests | UNCLEAN (F2) | srp_talker.cpp; srp_talker_mutants.py; srp_mutants.py; public gates and CPU receipts; harness README:261 | R870-1 applied; no clean covering round | 0d1eb8e4c5821e9431097950882659f2083d96ba |
| Docs | UNCLEAN (F1,F2,F3) | four changed Markdown files; source-comment delta; PR #952; #951 evidence; image maps | R870-1 applied; no clean covering round | 0d1eb8e4c5821e9431097950882659f2083d96ba |

**Gate evidence and real limits**

Author code-head receipts report 74 passing suite verdicts, control mutants 825/825, AECP 366 and SRP 513 `[ok]` lines, including 106 Talker-plant rows. Coverage passes for 40 files. Twin, twin-plants, twin-maps and twin-maps-plants each have rc 0. These are author executions at `4224df63`, carried through a docs-only final commit, not manager source-bank executions or newly repeated full banks by this review.

Final-head docs has 104/104 rc-zero steps. Both final builder legs report rc 0 **with one NOT RUN arm each**: the ineffective MAKEFLAGS mutation and the absent physical calibration report. The earlier shared-clone builder refusal is not counted as a pass; its isolated rerun is. Physical calibration is NOT RUN. These results and field skips are not hardware proof.

Release BIOS binary/ELF, ROM/RAM initialization and archive object-member hashes match. Raw generated gateware and archive-container hashes differ; gateware outside comments and the member match. Operational release-image identity has these generation/packaging qualifications. No release rebuild was performed here.

The CPU sample has 156 unchanged verdicts, with seven existing backlog-owed misses per point on both images, not zero total misses. Valid-destinations has none. The padding control supports placement as the timing cause; it proves neither omitted rows nor final-head coverage. Source-gate receipts are condensed; simulation traces are represented by hashes rather than published raw traces. This review audited published receipts and comparison/extraction scripts, not new full image builds or CPU simulations.

The one-time `hosted-snapshot.json` does not show complete successful hosted acceptance: `rtl-fast` cancelled; `elaborate` and `docs-check` failed; `wire-accountability` and `docs-check-no-git` succeeded. The full-workflow selector succeeded, but the queried job page does not establish successful exhaustive aggregates. Successful setup/manifest steps and skipped/cancelled test steps are not test passes. This snapshot does not assign a source root cause; the manager owns hosted acceptance.

**Prior public findings**

After writing this independent verdict and ledger, read-only inspection found two review-start comments, zero submitted reviews and zero inline review threads on PR #952. No prior public finding exists to resolve or retain at this head. `prior-findings.json` records that result. The other session's report was not read.

**Pending manager duties**

Resolve/re-review F1-F3 and carry RS1 on the residue checklist. Publish complete final-image measurements for F2. Obtain the second independent verdict and a reviewer-accepted clean ledger. The manager owns hosted/local-replica acceptance and full builder/native-bank validation of the final current-dev candidate, identifying candidate commit/tree and image hashes. No manager source-head bank exists or is inferred. Supplied live dev `e275d7950ef3385753e6a15d2e191ba855b171ed` is not this review's base; identify the eventual merge candidate afresh. This report authorizes no merge.

Reference-device conflict delay and physical qualification are NOT RUN here. No hardware access was attempted. Full parent/processor/synthesis/builder banks, container execution and host-side CI orchestration were outside this review's scope. No source fix, commit, push, GitHub write, author contact or delegated review occurred. Post-merge containment and Issue/Project completion remain manager duties after authorized merge.

R870-1 FINISHED
