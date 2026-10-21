[R670] POSITIVE - exact head 4ff3642e8fe9a0bd48d28374350390cde553bc32

R670-4 external independent composition review of issue #637 / PR #768.

All five lenses are CLEAN for this source head. No open BLOCKER, MAJOR or MINOR was found in the assigned delta. The merge preserves both changes, their tests and their separate counts. Earlier resolved findings remain resolved. Retained suggestions and wording residue are collected below. Physical acceptance and final merge acceptance remain outstanding.

Tree: `62626aefcfd7c4ff0b53f3a5413f700477bb9611`. Prior reviewed head: `1e914414557874648ac5041aff88b96908e0e053`. Source base: `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`. Merge `d26fca65af68acae060480353200519c919ab55d` has parents `1e914414557874648ac5041aff88b96908e0e053` and `78ca9bdf104819265588726bce4322696c38b8c2`. The final commit changes only the milan_dp README.

Scope and reconstruction

The [composition assignment](https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6298729116) governs this round. The [issue](https://github.com/kebag-logic/milan-fpga/issues/637), its public assignments and the [one-pass ruling](https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6269988820) retain parent ownership, unchanged record format, map-only atomic restore, rollback and held faces. D3 sections 3, 8.3, 8.4, 8.7 and 18.4, FASTCONNECT 6.1, REQUIREMENTS REQ-VER-06 and pinned processor `docs/architecture/07_memory_maps.md:573` supply the applicable contracts. No processor interface or submodule pin changed.

AGENTS.md / CONTRIBUTING.md and docs/README.md were read first, then issue scope and authorities, the source-base diff/history with the later delta examined in detail, and immutable executable evidence. Existing R670-3 scope carries forward only where dependency checks establish preservation. Imported dev changes were examined for their interaction with map work; this is not a new standalone review of all of PR #767.

Read-order limitation: a request for the public PR body unexpectedly returned older public review bodies as well. This happened after the independent code/composition pass, but before the initial verdict/ledger file was written. Strict ledger-before-other-report ordering was therefore not achieved. `independent-initial.md` records that limitation. Prior findings were subsequently reconciled explicitly. No current round-4 report from another reviewer, private author material, private management checkout or lane scratchpad was read. No source edits, commits, pushes, GitHub writes, sub-agents, full banks, host orchestration or hardware operations were performed.

Composition and executable evidence

`verify_composition.py` proves the following from Git objects; `composition.txt` records its results:

- For `hdl/milan/milan_datapath.sv`, merge minus prior head has exactly the ordered added/removed lines of dev minus common base `e26f1816`; merge minus dev has exactly those of the map branch minus that base. Only diff headers and relocated hunk numbers are excluded, not source text. Both SHA256 values are recorded.
- The complete 61,270-character prior map helper block is retained byte-for-byte. Both imported counter functions are unchanged from dev. The 44 probe declarations are exactly the union of both parents.
- `sim_nxn.cpp:3123` runs the power-on map section, the counter section, then the map-record section before its terminal tally. The counter helper performs a fresh reset/boot. `maprec_first_boot` at `:4956` independently resets and loads an erased window.
- The final README-only commit leaves executable inputs of the merge-commit campaign and wiring controls unchanged.
- Supplied live dev `59740e3c9d0420e2e7fef185978954710448dc4a` merges cleanly with the reviewed head, producing tree `803f7b249409011a4e3701923dd5e09a68d0bff1`. This is structural mergeability, not candidate-bank execution.

All 844 `author-r3c/` files in the immutable [published packet](https://github.com/kebag-logic/milan-fpga/tree/1980192f9c93b1bcdeea1aa40daa64171f4ddaac/review-evidence/637-r1) match their manifest `published_sha256`, including six marked path-redacted. The evidence commit has no signature and no detached signature was supplied. This establishes published-byte integrity, not signer authentication or independent proof of execution.

| Published author evidence | Verified result and scope |
|---|---|
| All milan_dp legs at `4ff3642e` | 12,892 checks, zero failures. dynmap 686/0; maprec8 219/0; maprec4 137/0; nxn 1,981/0; nxndv 1,983/0; nxn8 3,765/0; nxn4c 1,981/0. Identity, individual tallies and suite tally agree. |
| Raw dynmap log | Independently counted: preamble 52, DYNMAP 110, counter section 37, MAPREC 487; total 686/0. Fifteen assertions carry the literal `[762-DP]` label; the 37 includes setup checks. |
| Full campaign at `d26fca65` | Render prerequisite rc 0, full campaign rc 0, 68/68: five clean legs and 63 caught controls. Every README failure/total pair matches the campaign verdict receipt. |
| Three wiring controls at `d26fca65` | Clean 686/0. Tied-zero and wrong-sink vector each fail exactly stopped gap and stopped silence. Bound-vector fails exactly started gap. All retain 686 checks and leave MAPREC clean. Raw logs were recounted. |
| Full sweep at `4ff3642e` | Four shards rc 0; 16+17+15+15 = 63 suites; 2,188,446 checks; zero failures/timeouts. Four declared field skips remain skips. |
| Docs and author builder at `4ff3642e` | 95 docs commands with zero exits; both builder legs rc 0. Calibration gate 11 remains NOT RUN. These are author receipts, not a manager source bank. |
| Route at `4ff3642e` | Published check PASS: LUT 49,937 (+324), FF 52,629 (+276), WNS +0.155 ns, WHS +0.036 ns, complete routing. The reported increase stays below the maps-stage 1x1 ceilings. Prior standalone measurements carry only over their unchanged input closure. |

`receipt-audit.txt` records independent arithmetic and raw-log checks. Its first parser incorrectly expected `[PASS]` instead of the harness's `[ok]`; `receipt-audit-initial.txt` preserves that failed audit. The corrected parser passes without changing source receipts or expectations. No simulation, campaign, synthesis, route or builder execution was rerun by this reviewer. Existing evidence sufficed for the narrow composition claims; no unresolved claim required a new fault probe.

Artifact-specific lens results

[R670] PASS Conformance - `milan_datapath.sv:4925`, `:5488`, `:5773`; `sim_nxn.cpp:4956`, `:5594`; D3 3/8.3/8.7/18.4 and processor memory-map 5.1 - parent write/restore ownership, framing, three-stage ordering, rollback, status and the map-only transaction remain intact. The stopped-input rule remains on the intended AAF vector. Empty/non-default persistence and malformed-record defaults retain their coverage. Board cold-cycle acceptance is excluded from this source PASS.

[R670] PASS RTL - `milan_datapath.sv:3304`, `:7300`; `KL_avtp_rx_monitor_ctx.sv:151`, `:903`, `:1022`, `:1072`; both-parent comparison - selected-CRF return requests and stopped-input wiring coexist with the unchanged map writer/restore. The AAF slice `[N_STREAMS-1:0]` excludes CRF sink `N_STREAMS`; the imported engine consumes it at the stated gap/silence boundaries. No map clock/reset, width, arbitration, hold or status path changed in the merge. `KL_pp_shadow.sv` and required pins retain earlier bytes.

[R670] PASS Robustness - `sim_nxn.cpp:4665`, `:4956`, `:5594`; `dynmap_mutants.py` rows 17-35 and 38-63; raw wiring receipts - the counter test starts from a fresh boot and persistence from an erased window. Retained cases cover rollback, late device answers, deadlines, taint, retries, malformed values, cross-port ownership and lone invalid records. Stop/start controls discriminate stopped gap, stopped silence and resumed gap, failing only their intended assertions.

[R670] PASS Tests - `sim_nxn.cpp:3123`; `dynmap_probes.vlt:1`; `README.md:84`, `:841`; `check_receipts.py` - no test arm is dropped; both parents' probes and the 59-page vacuity guard remain. Imported counter functions are unchanged from dev. Section counts total 686, all three wiring controls remain sensitive and the complete campaign catches 63/63 controls. The README-only delta establishes campaign input equivalence to the exact head.

[R670] PASS Docs - `tb/verilator/milan_dp/README.md:84`, `:782`, `:841`, `:1357`; issue readiness comment 6305925321; current PR composition account; receipt identities - run order, fresh boot, erased window, measured counts and campaign head are distinguished accurately. Added source comments contain no new prohibited reviewer/round/administrative-comment provenance. Retained residue and a historical command endpoint correction are recorded below.

Prior findings: resolved causes retained

Prior public findings examined: [R670-1](https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6269970193), [R669-1](https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6268811441), [R670-2](https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6295076402), [R669-2](https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6295588258), [R670-3](https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6298697660), [R669-3](https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6298948509). These are carried resolutions at their causes, not approval inferred from the author account.

| IDs; original severity; attributable lenses | Current disposition, cause and verification |
|---|---|
| R670-F1 / R669-F1; MAJOR; Conformance, RTL, Robustness, Tests, Docs; R669-S2 | RESOLVED. `pp_stat_*_w` at `milan_datapath.sv:5773` still composes busy/done/fail/blank. Public-register assertions and controls 38-44/56 remain caught. |
| R670-F2 MAJOR / R669-F5 MINOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED. AS_RNEXT/AS_RJDG/AS_EEND retain remove-all/apply/put-back. maprec8 covers both transfer orders and cyclic swap; control 54 still fails 12/219. |
| R670-F3 / R669-F2; MAJOR; Conformance, Robustness, Tests | RESOLVED. Retained real-path value/recovery helpers and controls 45-53/55/57/60 remain present and caught. |
| R670-F4 / R669-F3/F4; MAJOR; RTL, Tests, Docs | RESOLVED. `mrec_offset_i` at `:9158` retains the whole-record rationale; split helpers/test-evidence corrections remain; 95 current docs zero exits, no ratchet change. |
| R670-F5 / R669-F6; MINOR; Docs | RESOLVED. REGISTER_MAP PP_STAT[4] retains parent writer, three attempts 500 ms apart, reset-sticky alarm. |
| R670-F6; MINOR; Conformance, Docs | RESOLVED. Public ruling and D3 3/18.4 retain the accepted one-pass, map-only transaction, held faces and rollback obligation. |
| R669-2-F1; MINOR; Tests | RESOLVED. `sim_nxn.cpp:5563` and lone-record helpers retain four isolated invalid-record windows; controls 61/62/63 fail named blank assertions, 1/2/1 of 686. |
| R669-2-F2; MINOR; Docs | RESOLVED. REGISTER_MAP and D3 8.7 preserve binding cause while adding no map cause; applicable wiring unchanged. |
| R670-2-F1; MINOR; Tests, Docs | RESOLVED. Issue correction and PR round-2 table distinguish full campaign rc 2, listener retry rc 0, aggregate coverage and separate synthesis. Current full campaign has its own rc 0 receipt. |
| R670-R1/R2/R3 and R669-R1/R2/R3; RESIDUE; Docs | RESOLVED. Layout citation says check 15; assigned lane labels remain removed from shadow/shared-face comments. |
| R669-S1; SUGGESTION; Conformance, Docs | ADDRESSED. D3 18.4 retains the ungranted-request attempt and capture-hold rationale. |
| R670-2-R3; R670-3-R1 / R669-3-RES-1; RESIDUE; Docs | RESOLVED. Current PR roles record round-2 assignments and round-3 assignments/verdicts. This head correctly awaits completed review. |

Retained optional suggestions

All entries are SUGGESTION and leave their lenses CLEAN. Cited code and coverage are unchanged by this delta.

| ID; lenses | Artifact; authority/evidence and impact | Optional outcome; verification |
|---|---|---|
| R669-S3; Tests | `scripts/check_nvm_record_space.py`, check 15; guards layout literal, not every parent length formula. Formula drift has weaker static protection. | Compare formulas with census across shapes; formula mutation must fail. |
| R669-2-S1; Tests | `milan_datapath.sv:5384`, sweep wait; prior removed-wait probe survived. Specific wait sensitivity unproven. | Hold sweep across terminal and grade RAMs, or prove redundancy with server wait; test removed-wait control. |
| R669-2-S2; Tests, Docs | `milan_datapath.sv:5606`, refused stage-0 take-down; defensive failure arm unexercised. | Perturb store to exercise all-map rollback, or document reachability; verify public fail/default state. |
| R669-2-S3; Tests, Docs | `tb/verilator/milan_dp/Makefile:575`; fresh tree needs a separate render prerequisite, explicitly performed by current receipt. | Make campaign prepare its listener build; validate one fresh-tree command. |
| R669-3-S1; Tests, Robustness | `milan_datapath.sv:5426`, `sim_nxn.cpp:5586`; length-only predicate sensitivity not established by magic/length conjunction control. Assignment makes it optional. | Add correctly resealed wrong-length-only case/control; require its named default/blank assertion to fail. |

Wording residue and exact outcomes

Each item is RESIDUE, Docs-only, under the owner wording/comment rule. None changes a measurement, executable test, conformance interpretation or privacy rule. Preserve runtime identifiers, mutation anchors and generated results during prose cleanup. A runtime-description rename is separate work, not wording-only cleanup.

| ID | Artifact; evidence and impact | Exact required outcome | Verification |
|---|---|---|---|
| R670-2-R1 / R669-2-RES-1/RES-2 | `milan_datapath.sv:4925`; `sim_nxn.cpp:5628`; administrative issue-comment provenance in source. | RTL: `Milan v1.2 5.3.10.1; #637, D3 18.4`; C++: `D3 18.4; Milan v1.2 5.3.10.1; #637`. | Comment-only diff retaining behavior/reason. |
| R670-2-R2 / R669-2-RES-3 | `dynmap_mutants.py:29`, `:35`, `:154`, `:168`, `:316`, `:345`, `:386`; reviewer/round names in prose. | Use `Additional #637 controls follow`, `per-port ordering` and behavior-named sections; remove reviewer/round labels from comments/docstring. Keep row-54 runtime text/anchors stable in this cleanup. | Inspect comments and unchanged executable tokens/results. |
| R669-2-RES-4 | `dynmap_mutants.py:29`; prose omits some existing rows 38-60; executable inventory/table are correct. | State eight composition, fourteen value/recovery and one ordering row, or enumerate all 23. | Count unchanged rows. |
| R669-2-RES-5 | `milan_datapath.sv:5495`; stage 0 already emptied the port. | `refused before its saved set touches the port`. | Comment-only edit against stage sequence. |
| R670-3-R2 / R669-3-RES-2 | Published `author-r3c/HANDOFF.md:193`; historical `tb, hdl equal to the head` shorthand, with precise differences disclosed elsewhere. | `executable inputs equal to 1e914414; the README and a Makefile comment differ`. | Compare `600565b4..1e914414`; retain historical attribution. |
| R669-3-RES-3 | Published `author-r3c/HANDOFF.md:304`; nearby corrected account separates executions, summary omits qualifier. | `Across those two executions: 60 of 60 caught and all five clean legs pass; the full campaign command itself exited 2.` | Match historical receipts and corrected table. |
| R669-3-RES-4 | `public-pr-body.md:106`; historical round-3 validation rows lack direct receipt links. Navigation residue. | Link pinned `author-r3/receipts/round3/legs/`, campaign verdict/excerpt, docs `rc.tsv`, builder `rc.tsv`. | Open links and verify historical heads. |
| R670-4-R1 | `public-pr-body.md:91`; published `author-r3c/HANDOFF.md:125`, `:460`, `:613`; historical sections use moving `HEAD` in empty-diff statements. Current composition section separately records changed RTL/rerouting correctly. | Round 3: replace `git diff 8000520c HEAD` with `git diff 8000520c 1e914414`. Round 1: replace `git diff 90b15366 HEAD` with `git diff 90b15366 63a187e1`. | Explicit historical diffs are empty; current composition still identifies new RTL/route evidence. |

Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue/rulings; D3 3/8.3/8.7/18.4; FASTCONNECT 6.1; processor memory-map 5.1; preserved transaction/status and independent boots | R670-4 composition; R670-3 unchanged scope carried | 4ff3642e8fe9a0bd48d28374350390cde553bc32 |
| RTL | CLEAN | Both-parent RTL change equality; stopped_i slice/consumer; restart edge; preserved map/arbiter inputs and gitlinks | R670-4 composition; R670-3 unchanged scope carried | 4ff3642e8fe9a0bd48d28374350390cde553bc32 |
| Robustness | CLEAN | Reset/erased-window helpers; retained failure/deadline/multi-port tests; raw wiring controls/map campaign | R670-4 composition; R670-3 unchanged scope carried | 4ff3642e8fe9a0bd48d28374350390cde553bc32 |
| Tests | CLEAN | Complete map-block/imported-function equality; 44-probe union; raw 686 tally; 63 campaign rows; leg/sweep receipts | R670-4 | 4ff3642e8fe9a0bd48d28374350390cde553bc32 |
| Docs | CLEAN | README order/table; issue/PR account; comment delta; manifest/identities; residue ledger | R670-4 | 4ff3642e8fe9a0bd48d28374350390cde553bc32 |

Carried R670-3 head: `1e914414557874648ac5041aff88b96908e0e053`. Its prior R670-2 coverage remains within preserved scope only. Current executable composition and changed documentation are covered by this round.

Real limits and pending manager duties

- No manager source bank ran at this exact head; none is claimed or inferred. Source execution evidence belongs to the author packet. The clean current-dev test merge proves no candidate execution. The manager must gate the current-dev candidate with builder/native banks and publish exact head/tree receipts at merge time.
- Hosted snapshot: docs, elaborate and rtl-fast in progress; rtl-full queued. No successful completion was reported. No executed-success or skipped-success context is claimed. Hosted/local-replica acceptance belongs to the manager, distinguishing execution from skipped contexts.
- Physical calibration, field execution and on-board cold cycle are NOT RUN. Retained-window resets are not hardware proof. The 598-672-clock shipping hold uses zero-latency memory; board DDR latency remains unmeasured. Non-shipping 8x8 hold about 13,700 clocks against the 4,096-clock gather watchdog and post-place obligations remain open under D3 18.4.
- Obtain the other independent verdict, address the read-order limitation as appropriate, and ensure no review remains in flight. Carry residue and optional suggestions without treating them as physical acceptance.
- Obtain explicit maintainer merge authorization, prove post-merge containment, and complete issue/project accounting only for fulfilled acceptance. Keep #637's unfinished physical work visible; the PR correctly uses `Relates to`.

Final checkout audit: 1,422 parent blobs match exact bytes/modes; index equals assigned tree, with no hidden flags or untracked files. Every populated submodule's tracked bytes/modes/index and pin match: processor `2cbed0a9`, gPTP `e4869fd0`, axis `48ff7a7e`, stack `70936b77`, lwSRP `08ee86e8`. Optional `external` remains uninitialized at its recorded gitlink. No source restoration was needed.

Reproduction: `python3 verify_evidence.py <clone> <packet>/scratch`, `python3 verify_composition.py <clone>`, `python3 check_receipts.py <clone> <packet>/scratch`, `python3 audit_tree.py <clone>`. Immutable object IDs are in the scripts. `MANIFEST.sha256` lists publishable scripts/receipts with relative paths. Disposable extraction and prior-review working copies remain under `scratch/`, excluded from publication.

R670-4 FINISHED
