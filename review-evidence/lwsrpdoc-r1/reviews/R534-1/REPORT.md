[R534] NEGATIVE - exact head 5f9b9d99e1d94485fc00a1b1539baf2ae861cb65

# R534-1 internal independent review: lwSRP PR #5 (Closes lwSRP #1), public-release documentation

- Repository: kebag-logic/lwSRP, PR #5, branch `docs-public`, base `main`.
- Exact head `5f9b9d99e1d94485fc00a1b1539baf2ae861cb65`, tree `e8bc64162172057dc185b67d0b4a19839819a78d`.
- Source base `19f5796`. Range reviewed: `19f5796..5f9b9d9` (commits `8962e2f`, merge `e64143a` of `e4f9995` / PR #3, `5f9b9d9`).
- Review start: https://github.com/kebag-logic/lwSRP/pull/5#issuecomment-6030838934
- Round: R534-1 (first review of this PR). Prior public findings on PR #5 at this head: none existed (the PR has no reviews or review comments, only the two start notices).

## Verdict summary

The pages are well built. All 16 published commands run (15 return rc 0). The only nonzero rc is the link check's 8 expected licence-file links. All 22 graphs render. Every graph has 2–11 nodes. Sentences are at most 24 words, and no unlinked clause, file or issue reference was found. The privacy scan is clean. The state-graph comparison with Tables 10-3 to 10-6 is accurate. All 23 next-state cells where the code differs from the tables are disclosed (receipt below).

The verdict is NEGATIVE for five MINOR findings:
- One wrong clause in the manager's clause matrix (35.2.3 is cited where 35.2.4 is meant).
- Two code deviations the status pages do not disclose: the MSRP group address, and the scope of a received LeaveAll.
- An understated scenario-test limit, confirmed by a planted wrong binding that still passes all three scenarios.
- One graph whose rendered layout draws an edge through an unrelated node.

## Reconstructed authority

1. Repository rules. There is no `AGENTS.md`. `CONTRIBUTING.md` at head carries the coding and documentation rules. the removed agent-instruction page is removed.
2. Issue #1 body. It sets the owner's four rules, the scope per page and the seven acceptance items.
3. Assignment comment and round-2 comment on issue #1:
   - SPDX first line on each page; exact README licence sentence.
   - Truth from `src/`, `tests/`, `CMakeLists.txt`, `build.sh` and `zephyr/`.
   - Mermaid only, with no SVGs in the tree.
   - State graphs follow Tables 10-3 to 10-6 and say whether they match or list differences.
   - Checks committed under `doc/tools/`.
   - lwSRP self-links checked with authenticated access.
   - Planned work labelled "planned", without links or content.
4. Interface authorities. IEEE 802.1Q-2018 clauses 10.7.4–10.7.11, Tables 10-1 to 10-6, 10.7.5.2, 10.7.5.20, 10.8.3, 35.2.2.1, 35.2.3 and 35.2.4. These were read locally and are only cited here, not quoted.
5. Code truth: `src/`, `tests/`, `CMakeLists.txt`, `build.sh`, `behave.ini`, `Kconfig.zephyr` and `zephyr/module.yml` at head.
6. Public evidence: `milan-fpga@3f31bba3` `review-evidence/lwsrpdoc-r1/` (author packet). All 11 files match the published SHA-256 values in its `MANIFEST.json` (`receipts/public-evidence-hashes.txt`). No manager-run receipt files were found in that tree. The manager comments on the issue and PR are the assignment, round-2 and start notices.

Scope integrity:
- Non-documentation paths at head are byte-identical to `main` `d96d9d4` (the PR #3 merge). The diff with documentation paths excluded is empty.
- The merge `e64143a` tree equals a clean `git merge-tree` of its parents (`56f64ba`).
- No source file was changed by the documentation commits.
- All commits use the repository's normal identity, with one-line subjects.

## Owner rules and acceptance items

| Item | Result | Evidence |
| --- | --- | --- |
| Rule 1, short sentences | Met. 708 units; 0 over 25 words; longest band 20–24 (1 unit). The PR body has 46 units, none over 14. | `receipts/page-commands/tools-1.log`, `receipts/sentence-lengths-pages.txt`, `receipts/sentence-lengths-prbody.txt` (independent splitter) |
| Rule 2, every reference a link | Met for clauses, files, functions, issues and tools named in the checker. Wording residue for plain "C11"/"SPDX" and one mis-targeted label (R534-1-06). | `tools-2.log`, `receipts/link-label-check.txt` |
| Rule 3, use per reader | Met. The README table routes developer, integrator, manager and tester to a page each. Each page states how to use lwSRP for that reader. | README.md:45-52 |
| Rule 4, graphs readable, clean, clear | 22 graphs; one layout defect (R534-1-05). | `receipts/graphs/`, `receipts/graph-render-summary.tsv` |
| A1 render + size | Met. 22/22 render rc 0 with the shipped tool and with the reviewer's own extraction. Node counts 2–11. Longest label 38 characters. | `tools-4.log`, `graph-render-summary.tsv` |
| A2 links | Met with the expected exception. 269 local links; failures are exactly the 8 `LICENSE`/`NOTICE` links (expected, separate licence PR). 12 external URLs: 9 anonymous HTTP 200, 3 lwSRP URLs pass with **authenticated** access (repository private). | `tools-3.log` |
| A3 sentence script with exceptions | Met; fenced blocks listed as syntax exceptions with a reason; no prose exemptions. | `tools-1.log` |
| A4 reference script | Met; rc 0. Heuristic gap noted (S1). | `tools-2.log`, `checker-mutation-probes.txt` |
| A5 every command runs with rc | Met. 16/16 executed; rc table below. | `receipts/page-commands/` |
| A6 conformance claims checked | **Not met.** R534-1-01, -02, -03, -04. | below |
| A7 nothing private | Met. No host paths, hostnames, account names or AI tool/model names in the tree, commit messages or PR body. The PR body uses the neutral label `[A561]`. | scan in this review |
| the removed agent-instruction page rules preserved in `CONTRIBUTING.md` | Met. Every rule is carried in CONTRIBUTING.md:10-26: braces on every conditional/loop body including one-statement bodies; no `typedef enum`; tagged enums; one element per line; `ENUM_NAME_` prefixes, with an example. | `git show 19f5796:the removed agent-instruction page vs CONTRIBUTING.md |
| SPDX first line, README licence sentence | Met. All 7 Markdown pages start with the SPDX comment. README.md:58 matches the required text exactly. | — |
| Planned work | Met. manager.md:60-63 and integrator.md:230-231 say "planned", with no links and no content. | — |

Published commands (each in a fresh export of the head; cgreen made discoverable through environment variables only, as doc/tester.md:11 instructs):

| Page | Command | rc |
| --- | --- | --- |
| README.md:35-38 | configure / build / ctest / behave | 0 / 0 / 0 / 0 (9 tests, 1690 passes; 3 scenarios, 10 steps) |
| doc/tester.md:15-20 | configure / build / ctest / `./build/unit_tests` / behave / behave --dry-run | 0 / 0 / 0 / 0 / 0 / 0 (dry run: 3 untested, 10 steps untested) |
| doc/tester.md:45-53 | isolated codec compile (heredoc) / run | 0 / 0 (1690 passes) |
| doc/tools/README.md:14-17 | sentences / references / links --github-auth / render | 0 / 0 / 1 (8 expected licence links only) / 0 |

## Findings

### R534-1-01 — MINOR — Conformance, Docs
- **Where:** doc/manager.md:32 (clause matrix row "IEEE 802.1Q-2018, clause 35.2.3").
- **Authority/evidence:** In IEEE 802.1Q-2018, 35.2.3 is "Provision and support of Stream registration service", which defines the REGISTER_STREAM / REGISTER_ATTACH service primitives. Talker and Listener attribute propagation, and the bandwidth calculations the row's limitation refers to, are in 35.2.4 "MSRP Attribute Propagation" (35.2.4.2, 35.2.4.3, 35.2.4.4). The row's content ("Talker flooding and Listener propagation toward registered Talkers"; src/modules/msrp.c:132-185) belongs to 35.2.4. The wrong number follows the code comments at src/modules/msrp.c:95,114,119.
- **Impact:** The clause-by-clause matrix (issue #1 scope, acceptance item 6) maps implemented behaviour to the wrong clause. A manager cannot use it to scope 35.2.3 work. The 35.2.3 service primitives are not implemented, and the page does not say so.
- **Required outcome:** Cite 35.2.4 for the propagation row. If 35.2.3 stays in the matrix, state that its service primitives are absent.
- **Verification:** Re-read the 35.2 contents list, then check the row text and link at the new head.

### R534-1-02 — MINOR — Conformance, Docs
- **Where:**
  - src/modules/msrp.c:352-353 sets the MSRP `group_addr` to 91-E0-F0-00-0E-80, citing "Table 10-1".
  - doc/manager.md:20 (clause 10.5 row) lists "Protocol identifiers and group addresses" as present, with no limitation.
  - doc/integrator.md:98 tells integrators that the application interface supplies the protocol identifiers.
- **Authority/evidence:**
  - IEEE 802.1Q-2018 35.2.2.1 requires MSRPDUs to use the Nearest Bridge group address from Table 8-1 (01-80-C2-00-00-0E).
  - Table 10-1 lists only the MMRP and MVRP addresses. Those two match the code at src/include/shish_lan/mrp.h:129-130.
  - The EtherTypes at mrp.h:124-126 match Table 10-2.
- **Impact:** The status pages describe a non-conforming constant as implemented. An integrator who builds the planned transmit path from `ops->group_addr`, as integrator.md:96-98 suggests, would send MSRPDUs to the wrong address. Acceptance item 6 requires the page to say where behaviour is not implemented as specified.
- **Required outcome:** State the MSRP address deviation in the manager matrix, either in the 10.5 row or in a new 35.2.2.1 row, with a link to src/modules/msrp.c#L352-L353. Warn integrators near integrator.md:98. The documentation PR may not change source.
- **Verification:** grep the pages for the new limitation and its link; re-run the link check.

### R534-1-03 — MINOR — Conformance, Docs
- **Where:**
  - src/core/mrp_mad.c:835-841. `rx_on_leaveall` discards `attr_type` and broadcasts rLA! to every attribute instance on the port.
  - src/core/mrp_pdu.c:154-155 invokes it once per VectorAttribute that carries LeaveAll.
  - The disclosure pages are silent on this: doc/developer.md:163-171 (Applicant recovery differences), doc/developer.md:202-207 (Registrar differences) and doc/manager.md:21-22.
- **Authority/evidence:** IEEE 802.1Q-2018 10.7.5.20 limits a received LeaveAll to the state machines of the Attribute Type in the Message. The note under that clause states that the LeaveAll message operates per Attribute Type.
- **Impact:**
  - For the stream application, a LeaveAll carried in a Listener message also moves Talker registrations IN→LV and Talker/Listener Applicants to their rLA! next state.
  - For the MAC application, a LeaveAll for one type affects the other type.
  - The pages present the listed tables as the implementation differences (developer.md:65-66, manager.md:13-14) but omit this one. The rLA labels in the Registrar and Applicant graphs therefore imply standard scope.
- **Required outcome:** Add the cross-type rLA! delivery as an implementation difference with a link to mrp_mad.c#L835-L841, in the Registrar comparison and the manager matrix (10.7.8 or a 10.7.5.20 row). Note it in the receive-path guidance (integrator.md:108-111).
- **Verification:** Read the new rows and links at the next head, then run the link check.

### R534-1-04 — MINOR — Tests, Docs
- **Where:**
  - doc/tester.md:87-88 says only "the current active-state assertion" repeats an operation instead of reading port state.
  - doc/tester.md:105 and doc/manager.md:52 report "three scenarios pass" without the limit.
  - Open issue #4, which records the defect, is not linked.
- **Authority/evidence:**
  - tests/features/steps/switch_steps.py:33-36 shows that the inactive-state assertion also only re-runs `port_disable` and checks rc.
  - Reviewer probe C (`receipts/suite-claim-probes.txt`) bound `shlan_test_port_disable` to the enable wrapper. Result: behave rc 0, 3 scenarios passed, 0 failed.
  - Probe D (connect and enable bindings turned into no-ops) was caught only by the out-of-range scenario: rc 1, 2 passed, 1 failed.
- **Impact:** A tester or manager reading the pages would believe the disable scenario verifies disabling. It does not detect a wrong disable dispatch. This understates a test-coverage limit, which acceptance item 6 and CONTRIBUTING.md:60 forbid.
- **Required outcome:** State that both the active-state and inactive-state assertions only repeat the operation. State that a wrong disable binding passes all three scenarios. Link [issue #4](https://github.com/kebag-logic/lwSRP/issues/4) from the tester coverage section, and preferably from the manager maturity section.
- **Verification:** Re-run probe C (`scripts/suite_claim_probes.sh`) and read the revised text.

### R534-1-05 — MINOR — Docs
- **Where:** doc/developer.md:28-39 ("Data structures" flowchart).
- **Authority/evidence:**
  - Owner rule 4 requires each graph to be readable, clean and clear.
  - Rendered with mermaid-cli 11.16.0, the edge "Attribute list → Value and identity" passes through the "LeaveAll and periodic timers" box. It reads as an edge from the timers to "Value and identity" (`receipts/graphs/DEFECT-doc-developer.md-28.png`).
  - The other 21 graphs were inspected and are clean.
- **Impact:** The graph suggests an ownership edge that does not exist. Per-port timers do not own attribute values.
- **Required outcome:** Re-lay out the graph so no edge crosses a node, then re-render and inspect it.
  - The reviewer's candidate: declare `Port --> List` before `Port --> Timers` and shorten the label to "Port timers".
  - It renders clean (`receipts/graphs/CANDIDATE-doc-developer.md-28.png`).
  - Any equivalent layout is acceptable.
- **Verification:** Render with the shipped renderer and view the image.

### R534-1-06 — RESIDUE — Docs (wording and link markup only; carried to the residue checklist)
Exact fixes:
- doc/integrator.md:17: `[CMAKE_BUILD_TYPE](../CMakeLists.txt)`. The target does not contain the variable. Link it to `https://cmake.org/cmake/help/latest/variable/CMAKE_BUILD_TYPE.html`.
- README.md:29, doc/integrator.md:16, doc/tester.md:10: plain "C11". Link it once per page, for example to `https://www.iso.org/standard/57853.html`.
- CONTRIBUTING.md:40 and doc/tools/README.md:44: plain "SPDX". Link it to `https://spdx.dev/`.
- doc/developer.md:180: `mrp_mad.c#L311-L407` overshoots the Registrar table, which ends at line 395. Use `#L311-L395`.
- doc/integrator.md:133: the 60-centisecond Leave value is armed at src/core/mrp_mad.c:561, outside the linked `#L639-L700`. Add a link such as `../src/core/mrp_mad.c#L560-L564`.

### Suggestions (do not affect the verdict)
- **S1:** `doc/tools/check_references.py:15` file pattern omits `.zephyr` (and other extensions). A planted plain "Kconfig.zephyr" was not detected (`checker-mutation-probes.txt`, probe `plain-kconfig-file`). Derive the file names from the tracked tree instead.
- **S2:** `Kconfig.zephyr:5-6` help text tells integrators to call both `shlan_timer_tick()` and `mrp_tick()`, which double-ticks. integrator.md:127-131 correctly says "Do not call both". Mention the conflicting help text there, or fix it in a source PR.
- **S3:** Add a tests row (runner, codec suite, scenario bindings, steps) to the developer code map (developer.md:10-19).
- **S4:** CONTRIBUTING.md could note that existing sources predate the brace rule (for example mrp_mad.c:435-437, :631-632, :765), so reviewers apply it to new and changed lines.
- **S5:** manager.md:30 cites 35.2.1 for the Talker/Listener values. 35.2.1.3 (Declaration Type) makes this defensible. The attribute type and FirstValue definitions are in 35.2.2.4 and 35.2.2.8; consider citing them.

### Carried item from PR #3
- **R536-1-01 — RESOLVED at this head.**
  - doc/architecture.md no longer contains a layout listing, so the deleted placeholder appears nowhere: `git grep -i placeholder` over the Markdown pages returns nothing.
  - The issue scope allowed rewriting or folding architecture.md. The new runner and bindings are documented with links at tester.md:26-27,34,39, manager.md:51-52 and integrator.md:19,186.
  - S3 suggests also adding them to the code map.

## Five lenses

### Conformance — UNCLEAN (R534-1-01, -02, -03)
- **Tables 10-3 and 10-4.** These were compared cell by cell with the code tables in `src/core/mrp_mad.c`. The reviewer's transcription stays local; only the differences are published, in `receipts/state-table-cell-diff.txt`. Results:
  - Applicant: 169/192 next-state cells match.
  - Registrar: 30/30 transcribed cells match.
  - Each of the 23 differing cells is disclosed in developer.md:99-104, 133-137, 159 and 163-171.
  - The disclosed differences also cover the transmit actions (tx! QA, txLA! VP/LA/QP), the periodic! Join actions, the Registrar extra Join indication in LV (mrp_mad.c:346, 352), the local New! registration (mrp_mad.c:318-323), the AN→QA/AA Registrar condition, and the note 4 and note 5 conditions. The "shared" wording at developer.md:129 correctly renders note 4.
- **Displayed graph transitions.** Every edge in the six state graphs (developer.md:76-250) matches its table:
  - Applicant declarations: 9 edges.
  - Observation: 6.
  - Withdrawal: 6.
  - Registrar: 8.
  - LeaveAll: 5. These match Table 10-5, including timer restarts and the request on entry to Active.
  - PeriodicTransmission: 4. These match Table 10-6.
- **Timers and events.** Flush! raising leavealltimer! (mrp_mad.c:867-868) is required by 10.7.5.2, so it is not a deviation. The periodic 1 s and LeaveAll randomization requirements in 10.7.4.3 and 10.7.4.4 are cited correctly.
- **Other matrix rows checked:** 10.2, 10.3, 10.5, 10.8.2, 10.8.3, 10.9–10.12, 11.2, 35.2.1 and 35.2.2.7.2. Each was checked against the code: parser at mrp_pdu.c:116-256, MVRP/MMRP/MSRP modules, the attribute-type comment conflict at mmrp.h:7-9 vs :25-26, and VID range at mvrp.c:64.
- **Defects found:** the 35.2.3 clause error and the two undisclosed deviations above.

### RTL — NOT APPLICABLE
lwSRP is a standalone C11 library. There is no RTL, HDL or FPGA artifact in the tree or the diff. The pinned simulator was not needed and was not used.

### Robustness — CLEAN
- **Checker fault injection.** Planted faults were tried against the doc checkers in disposable exports: 24 probe runs, one invalidated (its planted text was 24 words) and superseded (`receipts/checker-mutation-probes.txt`):
  - 26-word sentences (plain, wrapped and in a table cell) fail. The 25-word boundary passes.
  - Plain file, clause, table, issue, function and inline-code references fail.
  - A missing file, missing heading, line range past EOF, path outside the repository, or dead external URL fails.
  - A 16-node graph fails, as does a Mermaid syntax error.
  - An output directory inside the checkout is refused (rc 2).
  - An unclosed fence fails.
  - The one detection gap is S1.
- **Link checker.** The authenticated path only calls the GitHub API for links under the origin repository's path on `github.com`. Other URLs go anonymously, so credentials are never sent elsewhere (check_links.py:18-36).
- **Integrator robustness statements** were verified against the code:
  - Timer lifetime use-after-free: mrp_mad.c:763-778 frees timers still linked by timer.c:5-12.
  - `mrp_tick` ignores its arguments: mrp_mad.c:854-859.
  - Missing bounds checks: mrp_mad.c:780-882; only visit and status check.
  - Partial delivery before a parse error: mrp_pdu.c:178-218, 251.
  - Version and AttributeListLength are ignored: mrp_pdu.c:131-139, 239-240.
  - Register-queue hang contract: switch_ctrl.c:121-124.

### Tests — UNCLEAN (R534-1-04)
- **Counts and runs.** The test counts and rcs stated on the pages were re-derived by execution: 9 tests, 1690 passes, 3 scenarios, 10 steps; the dry run executes nothing.
- **"Rejects an empty suite"** (tester.md:31). Probe A: an empty cgreen suite makes ctest fail with rc 8 ("Error regular expression found ... No assertions").
- **"Unit dependency absent → host configuration fails"** (integrator.md:20). Probe B: configure rc 1, "Could not find CGREEN_LIB".
- **Codec-test coverage text** (tester.md:57-58). Checked against the nine `Ensure` blocks in tests/unit/mrp_pdu_test.c:23-150.
- **Defect.** Probe C exposes the scenario limit the pages understate (R534-1-04).
- **Hosted CI.** No hosted CI exists for this repository: there is no `.github/` and the head has 0 check runs and 0 statuses. No hosted evidence was available to inspect.

### Docs — UNCLEAN (R534-1-01 to -05; R534-1-06 residue)
- **Pages read in full:** README, CONTRIBUTING, architecture, developer, integrator, manager, tester and tools/README.
- **Graph readability.** All 22 graphs were rendered to SVG and PNG under the reviewer's own extraction and inspected visually (`receipts/graphs/`). Each has one idea and stays within the size limit. Directions suit the content. Labels are short.
- **Link labels.** All 59 identifier-bearing link labels were checked against their targets and line ranges. The only miss is the `CMAKE_BUILD_TYPE` residue; `CONFIG_LWSRP` → `Kconfig.zephyr` follows the Kconfig convention.
- **Scope items.** Every scope item in issue #1 is present. drawio is replaced by Mermaid graphs. the removed agent-instruction page is removed.
- **PR body.** The figures in the PR body match the reviewer's measurements: 708 units, 22 graphs, 2–11 nodes, 8 licence links, 3 authenticated + 9 anonymous URLs, and 16 commands. One statement is inaccurate: "Implementation differences ... appear in the status matrix" is incomplete per R534-1-02 and -03.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN (R534-1-01, -02, -03) | doc/developer.md:58-265, doc/manager.md:9-37, doc/integrator.md:96-140; src/core/mrp_mad.c (full), mrp_pdu.c, msrp.c, mmrp.c, mvrp.c, mrp.h; IEEE 802.1Q-2018 Tables 10-1 to 10-6, 10.7.4, 10.7.5.2, 10.7.5.20, 35.2.2.1, 35.2.3, 35.2.4; `receipts/state-table-cell-diff.txt` | R534-1 | 5f9b9d99e1d94485fc00a1b1539baf2ae861cb65 |
| RTL | NOT APPLICABLE | Tree listing (43 tracked files, no HDL); diff 19f5796..head | R534-1 | 5f9b9d99e1d94485fc00a1b1539baf2ae861cb65 |
| Robustness | CLEAN | doc/tools/*.py; 24 checker fault-probe runs; integrator lifetime, concurrency, parser and queue claims vs src/ | R534-1 | 5f9b9d99e1d94485fc00a1b1539baf2ae861cb65 |
| Tests | UNCLEAN (R534-1-04) | CMakeLists.txt, tests/unit/*, tests/features/*; 16 page commands; probes A–D; hosted check runs (none) | R534-1 | 5f9b9d99e1d94485fc00a1b1539baf2ae861cb65 |
| Docs | UNCLEAN (R534-1-01 to -05; -06 RESIDUE) | All 7 Markdown pages, 22 rendered graphs, PR body, commit messages, the removed agent-instruction page→CONTRIBUTING.md rule mapping, R536-1-01 | R534-1 | 5f9b9d99e1d94485fc00a1b1539baf2ae861cb65 |

## Real limits
- The standard tables were transcribed by hand from the local PDF for the cell comparison. Only differences are published, so a third party needs their own copy to reproduce the matching cells.
- Graph readability was judged on mermaid-cli 11.16.0 renders. GitHub's renderer version may lay graphs out differently.
- External links were checked from this host on 2026-10-07. lwSRP self-links were checked with authenticated access only, because the repository is private.
- cgreen was built from upstream source at 1.7.0-2-ga249b39 in a scratch prefix. Results with distribution packages were not tested.
- No embedded target, Zephyr build, hardware, network interoperability, or physical calibration was run. None is claimed. Field skips are not hardware proof.
- There is no hosted CI for this repository at this head.
- The manager's source static/builder and native banks were not re-run here, as required. No receipt files for them were found in the cited public evidence tree; only the author packet is there.
- The final current-dev candidate (merge turn) is distinct from this source validation and was not built here.

## Pending manager duties
- Carry R534-1-06 to the residue checklist.
- Route R534-1-01 to -05 to the author for a new head; re-review is required.
- Check the combined release tree once the separate Apache-2.0 PR supplies `LICENSE` and `NOTICE`. The 8 links must then resolve.
- Repeat the anonymous self-link check after the repository is published.
- Hosted/act acceptance and the final current-dev candidate build at the merge turn (live dev `910f338dbd050f4efd2d96991ddcf928a583d55f`) remain manager-owned.

## Integrity
- The reviewer clone was restored and verified at the exact head: HEAD and tree as above; `git status --porcelain --ignored` empty; index equal to the tree; 43/43 worktree blobs and modes equal to the tree; no gitlinks.
- No source edits, commits, pushes or GitHub writes were made.
- Probes ran only in disposable exports under the packet's scratch directory (`receipts/clone-integrity.txt`).

## Packet contents
- `scripts/`: portable scripts that take paths as arguments.
  - `run_page_commands.sh`
  - `render_graphs.py`
  - `check_link_labels.py`
  - `sentence_lengths.py`
  - `checker_mutation_probes.sh`
  - `suite_claim_probes.sh`
  - `compare_state_tables.py` (needs a local transcription)
- `receipts/`: raw logs and results. Host paths are replaced by `$PACKET`, `$CLONE`, `$HOME` and `$WORK`.
- All listed files are in `MANIFEST.sha256`.

R534-1 FINISHED
