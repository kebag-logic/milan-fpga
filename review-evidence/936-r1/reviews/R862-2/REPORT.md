[R862] POSITIVE - exact head d1aa4c44307edf4a9390c19cbb2c82fe5c5464d0

External independent review R862-2, issue #936 / PR #944. Tree `e8705c7ca87bb1d0f49be28e78bc54b93192ec1f`; source base `70f4056f`. This is a source-head verdict, not approval of a current-dev merge candidate.

All five lenses are CLEAN. No new BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION is raised. Both prior findings and the named wording residues are resolved at this head.

The six-commit delta from `7cfb8a0499941e56682f0c2f63326d120f5b7d9e` was examined: `343dfe43`, `bc921e68`, `33f24ca3`, `57a10c8d`, `83f1785f`, `d1aa4c44`. The earlier review stands for untouched artifacts and behavior; this round covers the changed artifacts and affected dependencies. Public reconstruction followed the operating contract, documentation index, [issue scope and decisions](https://github.com/kebag-logic/milan-fpga/issues/936), requirements/interfaces, base-to-head history and narrow diff, then [immutable author evidence](https://github.com/kebag-logic/milan-fpga/tree/b06d0f563f908f09907579d88b9688c565925dc8/review-evidence/936-r1/author-r2) and [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/936#issuecomment-6960339991). Prior public findings were reconciled after the independent delta pass. No other round-2 report was used. `public-contract.json` preserves the consulted public scope, ruling, handoff and PR text.

**Prior findings and residues**

| ID and original classification | Disposition | Artifact and verification |
|---|---|---|
| R862-1-F1, MAJOR; Conformance, Robustness, Tests, Docs | RESOLVED | `tb/verilator/ctrl_service_budget/talker_notice.py:106`, `:133`; `run.py:277`, `:604`; public `author-r2/receipts/budget/{r4-tn1,r4-tn8,r4-dr1,r4-de1}`. Real declaration/withdrawal now have loaded event-to-last-controller timing at both required shapes. Both loss and delay controls fail every named row for their intended reason. |
| R861-F1 (R861-1), MINOR; RTL, Robustness, Tests | RESOLVED | `sw/firmware/ctrl/app/ctrl_app_srp.c:66`, `:77`; `test_aecp.cpp:788`; `srp_gate.hpp:373`. A taken record contributes to owed work. Single-pass tests pass; independently restoring the old report is caught by each named test. |
| R862-1-R1 / R861-RES2, RESIDUE; Docs | RESOLVED | `sw/litex/ctrl_memory.py:247` names the cold-code and descriptor move to QSPI with #665 decision D3. The new comment no longer uses the lane label. The existing reason string is not a new comment violation. |
| R862-1-R2 / R861-RES1, RESIDUE; Docs | RESOLVED | `tb/verilator/milan_dp/README.md:1382`, `twin_compare.py:488`, and the PR limitation text name #943. The ownership label changed; owed-row predicates did not. |

These dispositions satisfy the required outcomes in [R862-1](https://github.com/kebag-logic/milan-fpga/pull/944#issuecomment-6953846656) and [R861-1](https://github.com/kebag-logic/milan-fpga/pull/944#issuecomment-6954572914). Neither finding is deferred to another issue.

**Independent lens results**

[R862] PASS Conformance - `tb/verilator/ctrl_service_budget/talker_notice.py:133`, `grade.py:343`, `:367`, `:570`, `docs/reference/FR_NFR.md:351` - checked against the frozen event-to-last-recipient contract, existing `notify` bound, Milan v1.2 5.4.5.1/5.4.5.2 Table 5.22 and IEEE 1722.1-2021 7.5.2. The declaration input is a real successful PROBE_TX; withdrawal uses a range-losing ANNOUNCE. Neither directly injects an AECP change. The fixture supplies an answering stream observation as requested by the prior finding. The tagged input selects its own RX commit, not a load frame. Every required controller/interface pair must receive a matching unsolicited STREAM_OUTPUT 0 GET_STREAM_INFO. Declaration ends at the later of the response and fan-out. No bound, origin or normative wait was relaxed.

[R862] PASS RTL - `sw/firmware/ctrl/app/ctrl_app_srp.c:63`, `ctrl_app_aecp.c:203`, `sw/firmware/ctrl/loop/ctrl_loop.c:325`, `:343`, `ctrl_loop.h:24`, `sw/litex/ctrl_memory.py:244` - checked the poll-order fix against the no-idle-while-owed contract. Delivery still consumes every interface mask, then reports whether it took a record. The next AECP poll transfers that work into existing event/retry machinery. Sink pending work remains ORed in; no mailbox access or reentry was added. The delta changes no RTL, clocks, CDC, mailbox ABI, gitlinks or product ROM banking. Bounded mask transfers retain their prior verdict; the published images account for the code-size change.

[R862] PASS Robustness - `talker_notice.py:83`, `:106`, `selftest_notice.py:158`, `sw/firmware/ctrl/test/test_aecp.cpp:788`, `srp_gate.hpp:373` - examined phase variation under channel burst/refill load and per-pass grandmaster changes, missing recipients, late notices, first/last source selection, interface transfer, declaration/expiry, and the idle boundary. The SRP load names another entity's stream, preventing Listener Ready from declaring source 0 before the timed event. Its own channel resumes load one refill period after the event. The App test begins from idle and stops at the first idle return; it cannot mask the original defect by blindly running extra passes. Untouched reset/type/VID/refusal behavior retains R862-1's result.

[R862] PASS Tests - `sw/firmware/ctrl/test/aecp_notice_mutants.py:31`, `srp_talker_mutants.py:281`, `srp_mutants.py:684`, `run.py:604`, `selftest_notice.py:158`, and this packet's `receipts/` - 10 independently run baseline cases passed; all five selected mutation runs were caught by the unchanged named assertions. They comprise the App idle-report plant at two interfaces, plus the SRP idle-report and mailbox-access plants at each interface count. The two-interface SRP gate mutation uses its campaign's 8x8 entity. Compilation failures or absent diagnoses do not count as kills. The re-anchored plant still adds `mbx_irq_status()` and is caught by `SrpBinding.BindIsDeferredAndKeepsEverySinkAndInterface` with “binding poll makes no mailbox access.”

The final refactor preserves all 304 AECP plant definitions, including paths, replacements and required diagnoses; all 14 build mutation definitions; and all six fixture variants. Full AECP table/diagnostic-reader controls pass. Extracted verdict and output helpers retain their logic. The Python idiom gate independently passes: long functions `9 <= 9`, long modules `10 <= 10`; no limit was raised.

[R862] PASS Docs - `sw/firmware/ctrl/{srp,aecp}/README.md`, `tb/verilator/ctrl_service_budget/README.md:271`, `docs/design/SPLIT_CONTROL_MEMORY.md:145`, `:553`, `sw/litex/ctrl_memory.py:269`, PR text and published image receipts - checked the documented handoff, owed report, load, probes, controls, memory and acceptance claims against code and receipts. New source comments describe behavior/reason with requirement or issue IDs, without new bench/reviewer/lane labels. The previously unsupported timing claim now has dedicated evidence. Known twin differences remain disclosed.

**Measurements and provenance**

`audit_packet.py` verified all 283 author-r2 files against the immutable archive's published SHA-256 manifest. It checked clean-head declarations in consoles, image/simulator identity consistency, all unplanted notice cycle arithmetic, recipients and bounds, control diagnoses, workflow completion receipts and the named mutation receipts. This verifies published-hash integrity. The archive commit has no cryptographic signature; none is claimed.

| Published exact-head run | Population | Result |
|---|---|---|
| `r4-tn1`, 1x1/1if | 16 rows, 16 recipients each | Maximum 6.88715 ms against 20 ms; no refusals or misses |
| `r4-tn8`, 8x8/1if | 16 rows, 16 recipients each | Maximum 7.55294 ms against 20 ms; no refusals or misses |
| `r4-dr1`, dropped notice | 16 rows | All 16 refused for missing notifications; named control caught |
| `r4-de1`, delayed notice | 16 rows | All 16 late, 26.641 to 30.568 ms; named control caught |
| `r4-lt1`, `r4-lt8` | Existing retried-notice rows | No refusals, budget misses or notice misses |
| `r4-ev1` | Existing queued notices, 1x1/1if | No refusals, budget misses or notice misses |

For example, the worst 1x1 declaration spans sys `300100141 -> 300788856`; the worst 8x8 withdrawal spans `360000955 -> 360756249`, at 100 MHz. The positive notice runs have no `STATED` line. Missing or late notices fail despite recording options. Controls require both rows of every selected group by name; partial catches, wrong reasons or unrelated refusals do not clear them.

`audit_images.py` compared published numeric and hash receipts. Five existing split images gain 8 B of ROM: the fixture's two two-interface points and the platform's two two-interface points plus 8x8/1if. SRAM and `ctrl_plat` are unchanged. Platform ROM is 117,688 / 119,304 / 130,392 / 131,976 B; the final `plat_ledger` reports PASS with zero findings. Fixture ROM is 112,624 / 114,216 / 125,280 / 126,832 B. At 8x8/2if the arm figures are 127,140 B (every-port), 126,992 B (valid-destinations), and 127,048 B (talker-notices), agreeing with the documents and authorized 59.5 entry. The timed talker arm uses 112,808 B at 1x1/1if and 125,464 B at 8x8/1if.

Nine fixture/arm and eight platform/full-fixture hashes match between `33f24ca3` and the final refactor. Six release comparison hashes match both base and final lists: two BIOS binaries, disassemblies and debug-stripped ELFs. Whole debug ELFs are not claimed byte-identical. These are the author's published builds, not fresh reviewer image builds.

**Reviewer-owned coverage ledger**

All paths are at the exact head below. Firmware filenames refer to the full paths expanded above; budget files are under `tb/verilator/ctrl_service_budget`.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `talker_notice.py:133`; `grade.py:343`; FR_NFR 3.4.1; `budget/r4-tn1`, `r4-tn8`, `r4-dr1`, `r4-de1` | R862-2 | d1aa4c44307edf4a9390c19cbb2c82fe5c5464d0 |
| RTL | CLEAN | `ctrl_app_srp.c:63`; `ctrl_app_aecp.c:203`; `ctrl_loop.c:325`; image/ledger receipts | R862-2 | d1aa4c44307edf4a9390c19cbb2c82fe5c5464d0 |
| Robustness | CLEAN | `talker_notice.py:83`, `:106`; `test_aecp.cpp:788`; `srp_gate.hpp:373`; control receipts | R862-2 | d1aa4c44307edf4a9390c19cbb2c82fe5c5464d0 |
| Tests | CLEAN | `aecp_notice_mutants.py`; `srp_mutants.py:684`; `selftest_notice.py:158`; `run.py:604`; focused logs and refactor checks | R862-2 | d1aa4c44307edf4a9390c19cbb2c82fe5c5464d0 |
| Docs | CLEAN | SRP/AECP/harness/twin READMEs; `SPLIT_CONTROL_MEMORY.md:553`; `ctrl_memory.py:247`; PR and public manifest | R862-2 | d1aa4c44307edf4a9390c19cbb2c82fe5c5464d0 |

**Reproduction, limits and pending duties**

`focused.py CHECKOUT PACKET all` runs three foreground-supervised workers, four compile jobs each. Planted copies and build trees stay under `PACKET/scratch`. `audit_packet.py ARCHIVE_ROOT` and `audit_images.py CHECKOUT ARCHIVE_ROOT` check the extracted public archive; `check_refactor.py CHECKOUT` compares moved definitions; `verify_tree.py CHECKOUT` checks tracked bytes and submodules. Raw test logs are included; expected mutation failures are successful defect detections. The Python gate command is `python3 -B scripts/check_py_idiom.py`.

The full local harness self-test completed with exit 0: `self-test: 0 failures`, all 246 diagnostic mutants caught. Its four new talker-notice checks pass. Raw output is `budget-selftest.log`; `budget-selftest.rc` is 0. This self-test exercises the harness and synthetic/fixture grading, not a fresh target simulation. Published command/test outputs replace workspace paths with neutral tokens; `receipt-provenance.json` records hashes before and after that normalization. `MANIFEST.sha256` enumerates every publishable file; `scratch/` is excluded.

Tracked-byte verification passes for all 1,634 superproject entries and 1,238 entries in the five required initialized submodules, including modes, symlinks, index entries and gitlink heads. `external` remains uninitialized as supplied. Candidate source was not edited. No source fix, commit, push, GitHub write, host replica, hardware access or change to another checkout was made.

The archive supplies consoles, per-row tables and summarized results. Complete original simulation traces and target binaries were not downloaded or re-executed. No target simulation, fresh full-standard audit, or full parent/processor/synthesis/builder bank was run by this reviewer. Source-head gate receipts are the author's executions. **No manager source bank ran at this head; none is inferred.** Hosted contexts were not used as execution evidence; skips are not test execution. Physical calibration is **NOT RUN**; simulations and field skips are not hardware proof.

The owner-ruled 1x1 held-egress growth and 8x8 STATED retries remain owed to #894. #943's STREAM_OUTPUT payload/face gaps and #935's stale `split-talker-failed` row/plant are known external work, not new findings here. This verdict does not claim the whole twin is green. Composition must resolve the stated #935, #932 and #914 conflicts and remeasure affected budgets, statements and ROM.

The manager must publish this report, obtain the other independent POSITIVE review, apply the owner's two-positive freeze rule, accept required hosted/local-replica evidence with executed/skipped jobs distinguished, and validate the actual current-dev merge candidate with builder/native banks and linked receipts. The supplied live-dev reference is `e275d7950ef3385753e6a15d2e191ba855b171ed`; it does not replace source base `70f4056f`. Merge authorization, completion of in-flight reviews, train validation and post-merge containment remain manager duties. Source approval alone does not close the issue.

R862-2 FINISHED
