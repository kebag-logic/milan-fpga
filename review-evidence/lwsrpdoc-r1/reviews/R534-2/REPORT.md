[R534] POSITIVE - exact head cd659eb5e93c4da5e97fcbd6282b1efba16e565d

# R534-2 internal independent review: lwSRP PR #5 (closes lwSRP #1), round 3 delta

- Reviewed head: `cd659eb5e93c4da5e97fcbd6282b1efba16e565d`, tree `e5bb35e6cd2efd707cbedaf5d799b8877a0aab30`.
- Delta under review: one commit, `5f9b9d9..cd659eb`. The full change `19f5796..cd659eb` was re-read for the owner's rules.
- Public review start: [PR #5 comment 6031210228](https://github.com/kebag-logic/lwSRP/pull/5#issuecomment-6031210228).
- Assignment: the "Round 3 for [A561]" comment on [issue #1](https://github.com/kebag-logic/lwSRP/issues/1#issuecomment-6031053742).

## Verdict summary

POSITIVE. There are no open BLOCKER, MAJOR or MINOR findings.

- All eight round-3 items are resolved at their root. Each was checked against the code, by running the published commands, or by a probe.
  - R534-1-01 to R534-1-06, R535-1-01 and R535-1-02.
  - The carried R536-1-01 residue is also resolved.
- One RESIDUE (R534-2-01) remains. The PR body's relative links do not resolve on the PR page. It is link markup in the PR body only, and it goes to the residue checklist.
- Two SUGGESTIONS do not affect the verdict.

## Reconstruction (order followed)

1. Repository guidance. There is no AGENTS.md at this head. I read CONTRIBUTING.md, README.md, every page under `doc/` and `doc/tools/README.md`.
2. Frozen scope.
   - The issue #1 body: the owner's four rules, the scope list and seven acceptance items.
   - The manager's comments: the assignment (6030336537), round 2 (6030706379) and round 3 (6031053742).
   - Issues [#4](https://github.com/kebag-logic/lwSRP/issues/4), [#6](https://github.com/kebag-logic/lwSRP/issues/6) and [#7](https://github.com/kebag-logic/lwSRP/issues/7) are the linked trackers.
3. Interface authorities: the code at this head.
   - `src/core/mrp_mad.c`, `src/core/mrp_pdu.c`, `src/modules/msrp.c`.
   - `src/include/shish_lan/{mrp,msrp,mrp_pdu}.h`, `Kconfig.zephyr`, `CMakeLists.txt`.
   - `tests/features/*`, `tests/unit/*`.
   - Clause numbers rest on the maintainer-filed issues #6 and #7 (see Limits).
4. Diff and history.
   - `git diff 19f5796..cd659eb` and the round-3 delta `5f9b9d9..cd659eb`.
   - The round-3 commit changes nine files: eight documentation pages and `doc/tools/check_references.py`.
   - The commit subject is one line, with no body or trailers. Author and committer are the repository identity.
   - `git diff --check 19f5796..HEAD` returns rc 0.
5. Public evidence.
   - The archive at `3f31bba` and the author round-3 packet `review-evidence/lwsrpdoc-r1/author-r3/` on the evidence branch at `21b72908`.
   - All 35 author-r3 files match the published SHA-256 values in that packet's `MANIFEST.json` (`receipts/author-r3-hash-check.txt`).
6. Prior public findings. I read R534-1 (6031046955) and R535-1 (6031016045) only after finishing my own pass over the diff. I did not read any concurrent review.

## Round-3 items verified at root

| Item | Required outcome | Evidence at this head | Status |
| --- | --- | --- | --- |
| R534-1-01 | Propagation row cites 35.2.4. If 35.2.3 stays, say its primitives are absent. | `doc/manager.md:35` gives the 35.2.4 row and links the propagation policy at `src/modules/msrp.c#L132-L185` (that is `msrp_map_join` and `msrp_map_leave`, read). `doc/manager.md:34` gives the 35.2.3 row: "Stream registration and attachment service primitives are absent". It links `msrp.h#L78-L89`, which holds only the declare and withdraw wrappers. | RESOLVED |
| R534-1-02 | State the MSRP address deviation in the matrix and near the transmit guidance, with links to #6 and the code. | `doc/manager.md:32` is a new row, "35.2.2.1 and Table 8-1", linking `msrp.c#L352-L353` and #6. `doc/integrator.md:101-104` warns integrators and links the code, the clause and #6. `src/modules/msrp.c:353` is `{0x91,0xE0,0xF0,0x00,0x0E,0x80}`, as the pages state. | RESOLVED |
| R534-1-03 | Cross-type rLA! difference in the Registrar comparison, the matrix and the receive-path guidance, with links to #7 and the code. | `doc/developer.md:208-213`, `doc/manager.md:21` and `doc/integrator.md:118-123` link `mrp_mad.c#L835-L841`, `mrp_pdu.c#L154-L155` and #7. In the code, `rx_on_leaveall` discards `attr_type` and calls `broadcast_event(...RLA)`. The Applicant rLA! row is at `mrp_mad.c:247-252` and the Registrar row at `:365-370`. The executable probe `receipts/probes/cross-type-rla.txt` sends a Listener message with LeaveAll. The registered Talker Advertise moves `appl AO->LO, reg IN->LV`. A Listener message without LeaveAll leaves it IN (control). | RESOLVED |
| R534-1-04 | State the scenario coverage limits as given and link #4 from the tester and manager pages. | `doc/tester.md:87-88,105,111-113` and `doc/manager.md:56-59` state that both assertions only repeat the operation and that a wrong disable binding passes all three scenarios. Both pages link #4. `tests/features/steps/switch_steps.py:26-36` matches. Probe P3 rebinds `shlan_test_port_disable` to enable: configure, build and scenarios all return rc 0, with three scenarios and ten steps passed (`receipts/probes/p3-wrong-disable.txt`). | RESOLVED |
| R534-1-05 / R535-1-01 | Re-lay out the "Data structures" graph so no edge crosses a node. Inspect it at native size and at page width. Check every graph. | `doc/developer.md:29-40` now declares `Port --> List` before `Port --> Timers[Port timers]`. I rendered it at native width (697 px), which is below the 830 px page width, so both views are identical. No edge crosses a node. A geometric SVG check reports 0 crossings on all 16 flowchart and state graphs. The same check flags the round-2 graph (`5f9b9d9`): edge `List->Value` crosses `Timers` (rc 1), which shows the check is sensitive. All 22 graphs were viewed (table below). | RESOLVED |
| R534-1-06 / R535-1-02 | Apply the exact fixes and link every C11. The reference checker flags bare C11 and has a self-test. | C11 is linked at `README.md:29`, `doc/integrator.md:16` and `doc/tester.md:10`. SPDX is linked at `CONTRIBUTING.md:41` and `doc/tools/README.md:45`. `CMAKE_BUILD_TYPE` links the build-system documentation (`doc/integrator.md:17`). The Registrar range is `#L311-L395`, which ends at the table's `};` (`doc/developer.md:182`). The Leave arming is linked at `#L560-L564` (`doc/integrator.md:147`). Checker probes follow this table. | RESOLVED |
| R536-1-01 (carried) | Architecture page test-layout table. | `doc/architecture.md:68-75` matches the exact fix. | RESOLVED |
| R534-1 S1 to S5 | Suggestions. | `.zephyr` is added to the file pattern. The `Kconfig.zephyr#L5-L6` conflict is stated (`doc/integrator.md:142`). The code map has a tests row (`doc/developer.md:20`). CONTRIBUTING has the brace-rule note. The 35.2.1.3, 35.2.2.4 and 35.2.2.8 citations are in. | ADOPTED |

Reference-checker probes:

- I planted bare `C11` in each of three forms: a sentence, inline code and a table cell. Each run returns rc 1 and reports `unlinked standard: C11` (`receipts/probes/p1-planted-references.txt`).
- The other planted names also fail with rc 1: C17/C2x, ISO/IEC, POSIX, C++17, IEEE 802.1Q, an unlinked clause, Table 8-1, `issue #7`, `#6`, `Kconfig.zephyr`, `mrp_rx` and SPDX. The restored tree returns rc 0.
- `--self-test` returns rc 0 with 79 cases.
- Removing `11` from the C-standard alternatives makes the self-test fail with rc 1 on two named cases. The page checker alone then still returns rc 0 (`receipts/probes/p2-selftest-mutation.txt`). The self-test is therefore a real guard.

ISO page:

- Anonymous clients get HTTP 403. This is the expected case and not a finding.
- A real browser session returned HTTP 200 with the title "ISO/IEC 9899:2011 - Information technology — Programming languages — C" (`receipts/probes/iso-page.txt` and `receipts/probes/iso-page-browser.png`).
- The page marks the 2011 edition as withdrawn. That is correct for a C11 reference, and `CMakeLists.txt:22-23` requires standard 11.

## Owner's rules and acceptance at this head (whole PR)

| Rule or item | Result | Evidence |
| --- | --- | --- |
| Rule 1 / A3: sentences of 25 words or fewer | Met | Sentence check rc 0: 760 units, 0 over the limit. A planted 26-word sentence fails with rc 1. PR body: 55 units, 0 over 25. |
| Rule 2 / A4: every reference is a link | Met for pages | Reference check rc 0. My own sweep of prose with links stripped found no bare file, function, identifier, clause, issue or standard-edition names. Remaining capitalised tokens are state and protocol abbreviations or generic terms (MAC, VLAN, HTTP, Markdown). The PR body's links are present but relative; see R534-2-01. |
| Rule 3: usage per reader | Met | The README reader table, plus developer, integrator, manager and tester guides, each with actions and sequences. |
| Rule 4 / A1: graphs render, about 15 nodes or fewer, readable | Met | 22 graphs render (rc 0), with 2–11 nodes. A planted 16-node graph fails with rc 1. No edge crosses a node. Labels are legible at native size and page width (see S1). |
| A2: links resolve and answer | Met except the agreed expectations | 290 local links. The eight failures are the LICENSE and NOTICE targets, pending the Apache-2.0 PR. Of 18 external URLs: 6 repository URLs pass authenticated, 11 pass anonymously, and the ISO page returns 403 to automated clients but exists (above). Anonymous repository checks return 404 while the repository is private. |
| A5: every published command runs with a recorded rc | Met | 17 occurrences. 16 return rc 0. The authenticated link check returns rc 1 for exactly the expected nine items. |
| A6: conformance claims checked against code | Met for the round-3 rows | Each new or changed row was read against its linked lines. The rLA! claim was executed. |
| A7: nothing private | Met | No host paths, private hostnames, or tool or model names in pages or check scripts. The former root style-instructions file and `doc/architecture.drawio` are removed, as scoped. |

## Findings

### R534-2-01 — RESIDUE — Docs (PR body only)

- **Where:** the PR #5 body, in the "Round 3" paragraphs, the validation table and the closing lines. The rendered body has 12 relative hrefs over 11 distinct targets: `doc/manager.md#implementation-status`, `doc/tester.md#coverage`, `doc/developer.md#data-structures`, `doc/architecture.md#test-layout`, `doc/tools/check_references.py` (twice), `doc/tools/check_sentences.py`, `doc/tools/check_links.py`, `doc/tools/render_mermaid.py`, `doc/tester.md#run-the-suites`, `LICENSE` and `NOTICE`.
- **Authority/evidence:**
  - Owner rule 2: every reference is a working link.
  - `receipts/pr-body-links.txt` lists every href from the API-rendered body.
  - Relative hrefs resolve against `https://github.com/kebag-logic/lwSRP/pull/5`, giving `.../lwSRP/pull/doc/manager.md` and so on.
  - The same URL shape on a public repository answers 404 or redirects to a new-pull-request sign-in page. It never reaches the file.
- **Impact:** a reader of the PR cannot follow these links. No page, measurement, figure, verdict, test, code, conformance or clause claim changes, and no privacy rule is touched.
- **Exact fix:** in the PR body, replace each relative target with an absolute blob URL. For example, use `https://github.com/kebag-logic/lwSRP/blob/docs-public/doc/manager.md#implementation-status`, or the merge-time commit in place of `docs-public`. Use the same form for the other targets. Keep LICENSE and NOTICE pointing at the post-merge `main` paths.
- **Verification:** render the PR body and confirm every href is absolute and reaches its file.

### Suggestions (no effect on the verdict)

- **S1:** two sequence graphs place self-message labels across a lifeline. They are `doc/integrator.md:81` ("Apply optional propagation") and `doc/integrator.md:127` ("Apply events and rearm"). This is the renderer's normal layout, and the text stays legible.
  - The widest sequence graphs are `doc/integrator.md:46` (1390 px native, scaled to 59% at page width) and `:81` (1140 px, 71%). At page width their message text is small but readable.
  - Shorter participant aliases would keep the text larger.
- **S2:** `doc/tools/render_mermaid.py` checks syntax and node count only. The no-crossing property now depends on manual inspection.
  - A geometric edge-versus-node test on the produced SVGs would keep the round-3 fix from regressing. One example is `scripts/edge-node-crossings.py` in this packet, which detects the round-2 defect.

## Five lenses

### Conformance — CLEAN

- Every round-3 row and sentence was read against its linked lines.
  - `mrp_mad.c:311-395` (Registrar table), `:550-582`, `:614-633`, `:639-700`, `:835-841` and `:871-882`.
  - `mrp_pdu.c:141-160`, `msrp.c:132-185` and `:352-353`, `msrp.h:78-89`, `mrp.h:117-119`, `Kconfig.zephyr:5-6`.
- The developer page says port timers drive LeaveAll and periodic events and each attribute owns its Leave timer (`doc/developer.md:44`). This matches `mrp_mad.c:70,81,83`.
- The cross-type rLA! difference was executed (`receipts/probes/cross-type-rla.txt`).
- The 35.2.3 / 35.2.4 split, the 35.2.2.1 and Table 8-1 address row, and the 10.7.5.20 row match the maintainer-filed authorities in #6 and #7 and the accepted R534-1 findings.

### RTL — CLEAN (no hardware description in scope)

- lwSRP contains no HDL. I applied this lens as source and build integrity.
- Compared with current `main` (`d96d9d4`), no source, build, test, `zephyr/` or `Kconfig.zephyr` file differs.
- `git merge-tree --write-tree d96d9d4 HEAD` gives exactly the reviewed tree `e5bb35e6…`, so this source validation covers the merge result.
- The scoped simulator identity was verified (5.050) but was not needed.

### Robustness — CLEAN

The check tools fail closed (`receipts/probes/tool-robustness.txt`):

- Render output inside the checkout is refused (rc 2, nothing written).
- `--github-auth` without a GitHub HTTPS origin is refused (rc 2).
- Mutually exclusive options are refused (rc 2).
- An unclosed fence is an error (rc 1).
- A missing target and an out-of-range line anchor each fail (rc 1).
- The self-test is independent of the working directory.
- The checkers write no bytecode into the checkout.

### Tests — CLEAN

All runs used an exported snapshot of HEAD, with the unit framework built from its public source into a scratch prefix (`receipts/suites/`).

- README sequence: configure, build, `ctest` and `behave` each return rc 0.
- Tester sequence: configure, build, `ctest`, `./build/unit_tests`, `behave` and `behave --dry-run` each return rc 0.
- The isolated heredoc compile and `./build/mrp_pdu_tests` return rc 0.
- Results: 9 tests and 1690 passes in both unit runs. Three scenarios and ten steps pass. The dry run reports 3 scenarios and 10 steps untested (matching only), as documented.
- The wrong-disable limitation was reproduced (P3).

### Docs — CLEAN (R534-2-01 is RESIDUE)

- Sentence check rc 0 (760 units). Reference check rc 0. Self-test rc 0 (79 cases). Render rc 0 (22 graphs).
- The authenticated link check returns rc 1 for exactly the eight licence-file targets and the ISO 403.
- All 22 graphs were inspected visually and geometrically.
- PR-body figures match my measurements: 760 units, 79 cases, 290 local links, 18 URLs (6+11+1), 22 graphs with 2–11 nodes, and 17 commands with 16 at rc 0.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | `doc/manager.md` matrix; `doc/developer.md` Registrar and data-structure text; `doc/integrator.md` transmit, receive and timer text; cited lines in `src/core/mrp_mad.c`, `src/core/mrp_pdu.c`, `src/modules/msrp.c`, `src/include/shish_lan/{mrp,msrp}.h`, `Kconfig.zephyr`; issues #6 and #7; executed rLA! probe | R534-2 | cd659eb5e93c4da5e97fcbd6282b1efba16e565d |
| RTL | CLEAN (no HDL; source and build integrity) | Non-doc diff against `main` d96d9d4 (empty); merge-tree result equals the reviewed tree; snapshot build | R534-2 | cd659eb5e93c4da5e97fcbd6282b1efba16e565d |
| Robustness | CLEAN | `doc/tools/*.py` failure paths; planted defects for each checker | R534-2 | cd659eb5e93c4da5e97fcbd6282b1efba16e565d |
| Tests | CLEAN | 12 suite commands from README.md and doc/tester.md; wrong-disable probe; checker self-test and its mutation | R534-2 | cd659eb5e93c4da5e97fcbd6282b1efba16e565d |
| Docs | CLEAN (R534-2-01 RESIDUE) | All 8 Markdown pages; 22 graphs at native size and 830 px page width; 5 published check commands; PR body; author-r3 packet hashes | R534-2 | cd659eb5e93c4da5e97fcbd6282b1efba16e565d |

## Per-graph inspection

| Graph | Type | Nodes | Native px | Page-width px | Edge crosses node | Readability |
| --- | --- | --- | --- | --- | --- | --- |
| CONTRIBUTING.md:48 | flowchart | 5 | 253 | 253 | no (0) | clear |
| README.md:14 | flowchart | 6 | 509 | 509 | no (0) | clear |
| doc/architecture.md:10 | flowchart | 11 | 800 | 800 | no (0) | clear |
| doc/architecture.md:34 | flowchart | 7 | 274 | 274 | no (0) | clear |
| doc/architecture.md:56 | flowchart | 4 | 1021 | 814 | no (0) | clear, slightly scaled |
| doc/developer.md:29 (Data structures) | flowchart | 10 | 697 | 697 | no (0) | clear |
| doc/developer.md:78 | state | 6 | 395 | 395 | no (0) | clear |
| doc/developer.md:116 | state | 6 | 403 | 403 | no (0) | clear |
| doc/developer.md:148 | state | 7 | 328 | 328 | no (0) | clear |
| doc/developer.md:184 | state | 3 | 396 | 396 | no (0) | clear |
| doc/developer.md:220 | state | 2 | 541 | 541 | no (0) | clear |
| doc/developer.md:249 | state | 2 | 454 | 454 | no (0) | clear |
| doc/developer.md:275 | flowchart | 6 | 230 | 230 | no (0) | clear |
| doc/integrator.md:46 | sequence | 4 | 1390 | 814 | n/a (lifelines) | readable; small at page width (S1) |
| doc/integrator.md:81 | sequence | 4 | 1140 | 814 | n/a | readable; self-label on lifeline (S1) |
| doc/integrator.md:127 | sequence | 3 | 806 | 806 | n/a | readable; self-label on lifeline (S1) |
| doc/integrator.md:158 | sequence | 3 | 875 | 814 | n/a | clear |
| doc/integrator.md:183 | sequence | 2 | 540 | 540 | n/a | clear |
| doc/integrator.md:215 | sequence | 4 | 920 | 814 | n/a | clear |
| doc/manager.md:44 | flowchart | 6 | 271 | 271 | no (0) | clear |
| doc/tester.md:62 | flowchart | 6 | 261 | 261 | no (0) | clear |
| doc/tester.md:92 | flowchart | 8 | 749 | 749 | no (0) | clear |

Node counts are from the shipped renderer. Pixel sizes are from the renderer's PNG output at a 3000 px page (native) and an 830 px page.

## Executed commands and exit codes

| Command (published location) | rc |
| --- | --- |
| README.md:35-38: configure, build, ctest, behave | 0, 0, 0, 0 |
| doc/tester.md:15-20: configure, build, ctest, `./build/unit_tests`, behave, `behave --dry-run` | 0, 0, 0, 0, 0, 0 |
| doc/tester.md:45-53: isolated compile (verbatim heredoc), `./build/mrp_pdu_tests` | 0, 0 |
| doc/tools/README.md:14-18: sentences, references, `--self-test`, links `--github-auth`, render | 0, 0, 0, 1 (expected 9), 0 |
| Anonymous link check (documented post-publication form) | 1: the expected 9 plus 6 private-repository 404s |

## Real limits

- I had no access to the IEEE 802.1Q-2018 text; the only local copy is in author scratch space, which is off-limits.
  - Clause numbers rest on the maintainer-filed issues #6 and #7, the accepted R534-1 findings and the code. Those are 35.2.2.1, Table 8-1, 10.7.5.20, 35.2.3 and 35.2.4.
  - I did not re-compare the state graphs with Tables 10-3 to 10-6 this round. Their content is unchanged since round 2, apart from the Registrar evidence range.
- I rendered the graphs with mermaid-cli 11.16.0. GitHub's renderer version and fonts may lay graphs out differently. The data-structures fix depends on edge declaration order.
- The repository is private. Repository links were checked with authenticated access, and anonymous checks must be repeated after publication.
- The PR-body link defect is established by URL resolution and by the same route shape on a public repository, not by an authenticated web view of PR #5.
- There is no hosted CI for lwSRP: the head has 0 check runs and 0 statuses. Hosted and act acceptance is the manager's.
- Hardware, embedded targets, timer runtime behavior and interoperability are unverified. Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Carry R534-2-01 to the residue checklist and fix the PR-body links.
- Merge the Apache-2.0 PR so that the eight LICENSE and NOTICE links resolve. Then re-run the link check.
- After publication, re-run anonymous link checks for the six repository URLs. Recheck the ISO page with a browser.
- Build the final current-dev candidate at the merge turn: source base 19f5796, live dev 09f1841bd2c6a9dea8eb1994d887f7386ca4f62d. This source validation does not replace that build.
- Decide whether the author packet's command logs need further redaction of a local command-wrapper prefix. This is outside the PR's pages.

## Receipts

- `scripts/`: `run-all.sh`, `run-doc-checks.sh`, `run-suites.sh`, `run-probes.sh`, `render-png.sh`, `edge-node-crossings.py`, `probe-cross-type-rla.c`, `run-probe-rla.sh`, `open-iso-page.cjs`.
- `receipts/doc-checks/`: logs and rc for each check.
- `receipts/suites/`: the 12 suite command logs and rc.
- `receipts/probes/`: planted references, self-test mutation, wrong disable, cross-type rLA!, ISO page, tool robustness.
- `receipts/graphs/`: sources, SVGs and native and page-width PNGs for all 22 graphs; the crossing check; the round-2 control graph.
- `receipts/pr-body-links.txt`, `receipts/clone-integrity.txt`, `receipts/author-r3-hash-check.txt`, `receipts/environment.txt`.
- The clone was never modified; all probes ran on exported snapshots under scratch.
  - At the end: HEAD `cd659eb5…` and tree `e5bb35e6…`.
  - `git status --porcelain --ignored` is empty, and the worktree and index diffs are rc 0.
  - The index hash equals the tree hash, and there are no gitlinks (none are required).

R534-2 FINISHED
