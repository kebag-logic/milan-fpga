# Documentation handoff

Status: Round 2 review ready. Head: 5f9b9d99e1d94485fc00a1b1539baf2ae861cb65. Local and unpushed; worktree clean.
The Round 2 results supersede the historical Round 1 failures.

Branch: docs-public. Remote verified: https://github.com/kebag-logic/lwSRP.git.
Resumed head: 8962e2f1870b8981b4ed685c663e49a69b98f8ab; initial worktree clean.
The manager reset the Round 1 identity without changing the tree.
Merge commit: e64143aac912d1860625cbd8dccb7cb4f6af503c.
Its second parent is the required e4f9995b791489c53b8ccb8a8dc09ec508e32e6b.
The merge uses --no-ff and a one-line subject without body or trailers.

[Issue](https://github.com/kebag-logic/lwSRP/issues/1).
[Original assignment](https://github.com/kebag-logic/lwSRP/issues/1#issuecomment-6030336537).
[Round 2 assignment](https://github.com/kebag-logic/lwSRP/issues/1#issuecomment-6030706379).
All three bodies were read exactly.

## Round 2

The test fix was fetched and merged before documentation changes.
No source, build, or test file was manually edited.
The pages now describe the required host unit dependency and working scenario bindings.
All old empty-suite and scenario-setup failures were removed from the current guides.
The four planned work areas remain labelled planned, without invented PR links or descriptions.
The authenticated link option applies only to the origin repository.
Other external links remain anonymous; every authenticated result is labelled.
Local source line ranges are checked for valid bounds.

### Pages and audiences

| Page | Audience | Coverage |
| --- | --- | --- |
| README.md | All readers | Purpose, architecture, quick start, passing suites, reader links, exact required licence paragraph. |
| CONTRIBUTING.md | Contributors and reviewers | Style rules, documentation rules, contribution licence, review process. |
| doc/architecture.md | Developers and integrators | Layer boundaries, receive flow, missing transmit integration. |
| doc/developer.md | Developers | Code map, ownership, six table-checked state graphs, line-linked implementation differences, extension workflow. |
| doc/integrator.md | Integrators | Required host dependency, platform ports, API sequences, timing differences, lifetime limits, module use, planned freestanding headers. |
| doc/manager.md | Managers | Clause matrix with normative comparison results, maturity, passing evidence, role responsibilities, planned work and licence dependency. |
| doc/tester.md | Testers | Configured and isolated codec tests, passing scenarios, scenario authoring, coverage limits. |
| doc/tools/README.md | Authors, reviewers, testers | Checker commands, authentication boundary, source-line fragments, syntax exceptions, scratch rendering. |

### Standard comparison

The supplied PDF was read locally after text extraction into scratch only.
The normative tables are on printed pages 270–272; timer definitions are on printed page 265.
No PDF, extracted standard text, or long quotation was copied into the checkout or output directory.
Public citations use the IEEE standard catalogue with clause numbers in link text.

| Graph | Normative result | Implementation differences documented |
| --- | --- | --- |
| Applicant declarations | Matches Table 10-3 for displayed paths, with sufficient frame space and the Registrar condition. | AN transmit condition; New from AA/QA/LA; Join from QA/LA; QA transmit action; missing scheduling and frame-space checks. |
| Applicant observation | Matches Table 10-3 for displayed paths with the shared-link condition. | Missing point-to-point conditions; received JoinIn from LA; received In gating. |
| Applicant withdrawal | Matches Table 10-3 for displayed paths with frame space. | LA ordinary transmit destination; other transmit-with-LeaveAll, full-frame, recovery and periodic discrepancies are listed nearby. |
| Registrar | Matches Table 10-4 for displayed states; graph omits indication and timer actions. | Local New registers; received Join in LV emits an extra Join indication and invokes propagation. |
| LeaveAll | Matches Table 10-5 for displayed states. | Transmit additionally rearms; no emitted LeaveAll or public transmit caller; fixed timer lacks randomization. |
| PeriodicTransmission | Matches Table 10-6 for displayed states. | Disable additionally stops timer; interval is 20 centiseconds instead of one second; downstream Applicant periodic behavior differs. |

Each result is also stated beside the graph and summarized in the manager matrix.
These are selected paths, not a reproduced normative table or full implementation conformance claim.
State-machine runtime conformance was not tested.

### Graph inventory

All 22 renders returned rc 0. Each has 2–11 nodes.
All final layouts were visually inspected in four scratch preview sheets.
Labels are readable; no overlapping labels were found.
Rendered SVGs and previews remain in scratch only.

| Page and line | What it shows | Nodes | Render and visual result |
| --- | --- | --- | --- |
| CONTRIBUTING.md:47 | Pull requests | 5 | rc 0; readable; inspected |
| README.md:14 | Architecture | 6 | rc 0; readable; inspected |
| doc/architecture.md:10 | Ports and adapters | 11 | rc 0; readable; inspected |
| doc/architecture.md:34 | Receive path | 7 | rc 0; readable; inspected |
| doc/architecture.md:56 | Missing boundary | 4 | rc 0; readable; inspected |
| doc/developer.md:28 | Data structures | 10 | rc 0; readable; inspected |
| doc/developer.md:76 | Applicant declarations | 6 | rc 0; readable; inspected |
| doc/developer.md:114 | Applicant observation | 6 | rc 0; readable; inspected |
| doc/developer.md:146 | Applicant withdrawal | 7 | rc 0; readable; inspected |
| doc/developer.md:182 | Registrar | 3 | rc 0; readable; inspected |
| doc/developer.md:214 | LeaveAll | 2 | rc 0; readable; inspected |
| doc/developer.md:243 | PeriodicTransmission | 2 | rc 0; readable; inspected |
| doc/developer.md:269 | Add an application | 6 | rc 0; readable; inspected |
| doc/integrator.md:46 | Create and declare | 4 | rc 0; readable; inspected |
| doc/integrator.md:81 | Receive and observe | 4 | rc 0; readable; inspected |
| doc/integrator.md:115 | Drive time | 3 | rc 0; readable; inspected |
| doc/integrator.md:144 | Lifetime and concurrency | 3 | rc 0; readable; inspected |
| doc/integrator.md:169 | Switch adapter sequence | 2 | rc 0; readable; inspected |
| doc/integrator.md:201 | Register queue sequence | 4 | rc 0; readable; inspected |
| doc/manager.md:41 | Maturity and evidence | 6 | rc 0; readable; inspected |
| doc/tester.md:62 | Write a scenario | 6 | rc 0; readable; inspected |
| doc/tester.md:92 | Coverage | 8 | rc 0; readable; inspected |

### Check results and published commands

- Sentence checker: rc 0; 708 prose units; none exceed 25 words; no prose exemptions.
- Reference checker: rc 0; no detected unlinked references.
- Link checker: rc 1; 269 local link occurrences and 12 unique external URLs.
- Eight relative occurrences await LICENSE and NOTICE, which this lane must not add.
- Three repository URLs pass with authenticated API access. All nine other external URLs return anonymous HTTP 200.
- Graph renderer: rc 0; all 22 render commands return rc 0.
- Both documented configure/build sequences: rc 0.
- Both configured test invocations: rc 0.
- Direct configured suite: rc 0; nine tests and 1690 assertions.
- Isolated codec compile and execution: rc 0; nine tests and 1690 assertions.
- Both scenario runs: rc 0; three scenarios and ten steps pass.
- Scenario dry run: rc 0; all ten steps match; no behavior executed.
- All 16 shell command occurrences were executed in a scratch source snapshot, including duplicates.
- The source snapshot uses the merged source, build, and tests, plus the final documentation files.
- Existing scratch dependency discovery paths were supplied through the environment.
- Routing fixtures verify exact repository boundaries, foreign URLs, comment fragments, unsupported paths, and authentication failures.
- Negative link fixture: rc 1 as expected; two invalid line ranges, one absent file, and one missing heading fail. A valid range passes.
- Whitespace, scope, content, artifact size, and SPDX checks: rc 0.

[Round 2 published command results](ROUND2-PAGE-COMMANDS.md).
[Round 2 command ledger](ROUND2-COMMANDS.md).
[Historical Round 1 command ledger](COMMANDS.md).
[Historical Round 1 published command results](PAGE-COMMANDS.md).

Every command runs in the foreground with a timeout; no check is piped.
Every return code is preserved, including exploratory failures.
The first preview command returned rc 1 because its assumed package path was absent.
The corrected module resolution returned rc 0, and all four preview sheets were inspected.
The initial instruction read preceded knowledge of the command-prefix rule.
The recorder bootstrap completed with rc 0; a separate tool-state serialization attempt failed without affecting files or commands.

### Remaining limits and release dependencies

- The separate licence branch must provide LICENSE and NOTICE before release link acceptance can pass.
- Anonymous repository access remains unverified while the repository is private.
- No hardware, target firmware, or network interoperability run was available.
- No state-machine runtime suite or coverage percentage exists in the current tests.
- Static review found protocol differences; this lane documents them without changing implementation.
- The supplied standard tables were checked manually, not through exhaustive machine-generated transition tests.
- Existing missing transmit, parser, timer lifetime, and adapter capabilities remain as documented.
- Planned work has no published PR links in this review.

### Scope and repository hygiene

Only documentation and documentation tooling were manually changed in Round 2.
Source, build, tests, module configuration, and runner settings match the merged test-fix commit exactly.
The required README licence paragraph remains exact.
All rewritten Markdown pages retain the SPDX marker.
No private path or automated-author attribution was found in the tree.
The largest repository file is 36,387 bytes.
No generated assets, packages, virtual environments, or toolchains are in the tree or output directory.
No push, PR creation, rebase, amend, configuration change, sub-agent, or existing-comment mutation was performed.
The configured repository identity is used for both new local commits.
No second TAKEN marker was posted.

### Final status

Final head: 5f9b9d99e1d94485fc00a1b1539baf2ae861cb65.
Commit subject: docs: verify state tables and refresh harness guidance.
Both local commits have one-line subjects, no bodies or trailers, and the configured author and committer identity.
The executed documentation snapshot matches the final checkout byte for byte.
Final clean-tree and source-scope checks pass.
The review-ready issue marker is the final external action.

Posted `[A561] REVIEW READY 5f9b9d99e1d94485fc00a1b1539baf2ae861cb65` with rc 0.

[Round 2 final issue marker](https://github.com/kebag-logic/lwSRP/issues/1#issuecomment-6030826544).

## Complete Round 2 command ledger

# Round 2 command ledger

Commands run in the foreground. Each invocation has a 550-second timeout. No check is piped. Logs remain in scratch.

| Command | rc |
| --- | --- |
| `rtk proxy timeout 600 python3 -` (initial read-only inspection) | 0 |
| `git remote get-url origin` (initial inspection subprocess) | 0 |
| `git rev-parse HEAD` (initial inspection subprocess) | 0 |
| `git status --short --branch` (initial inspection subprocess) | 0 |
| `rg --files -g AGENTS.md -g '*.md' -g '*.py'` (initial inspection subprocess) | 0 |
| `rtk proxy timeout 600 python3 -` (create Round 2 handoff skeleton and recorder) | 0 |
| `rtk proxy timeout 550 python3 -` (cwd `$LANES/lwsrp-docs`; log `command-1791346090754723096.log`) | 0 |
| `rtk proxy timeout 550 gh api repos/kebag-logic/lwSRP/issues/1/comments --paginate --jq '.[] &#124; select(.body &#124; contains("Round 2 for [A561]")) &#124; {html_url,body}'` (cwd `$LANES/lwsrp-docs`; log `command-1791346090750951697.log`) | 0 |
| `rtk proxy timeout 550 gh api repos/kebag-logic/lwSRP/issues/1 --jq .body` (cwd `$LANES/lwsrp-docs`; log `command-1791346090738233742.log`) | 0 |
| `rtk proxy timeout 550 gh api repos/kebag-logic/lwSRP/issues/comments/6030336537 --jq .body` (cwd `$LANES/lwsrp-docs`; log `command-1791346090732978505.log`) | 0 |
| `rtk proxy timeout 550 cat doc/tools/check_links.py doc/tools/common.py doc/tools/render_mermaid.py doc/integrator.md doc/architecture.md` (cwd `$LANES/lwsrp-docs`; log `command-1791346099620741432.log`) | 0 |
| `rtk proxy timeout 550 git fetch origin tests-harness` (cwd `$LANES/lwsrp-docs`; log `command-1791346099609845882.log`) | 0 |
| `rtk proxy timeout 550 pdftotext -layout $WORKSPACE_HOME/standards/802.1Q-2018.pdf $VALIDATION_STORAGE/lwsrpdoc-a561/round2/802.1Q-2018.txt` (cwd `$LANES/lwsrp-docs`; log `command-1791346099627970370.log`) | 0 |
| `rtk proxy timeout 550 git merge --no-ff e4f9995b791489c53b8ccb8a8dc09ec508e32e6b -m 'Merge test harness fixes for documentation validation'` (cwd `$LANES/lwsrp-docs`; log `command-1791346113661154968.log`) | 0 |
| `rtk proxy timeout 550 rg -n 'Table 10-[3456]&#124;10\.7\.[789]&#124;10\.7\.10&#124;10\.7\.11' $VALIDATION_STORAGE/lwsrpdoc-a561/round2/802.1Q-2018.txt` (cwd `$LANES/lwsrp-docs`; log `command-1791346113793149845.log`) | 0 |
| `rtk proxy timeout 550 python3 -` (cwd `$LANES/lwsrp-docs`; log `command-1791346113797342957.log`) | 0 |
| `rtk proxy timeout 550 sed -n 16840,17160p $VALIDATION_STORAGE/lwsrpdoc-a561/round2/802.1Q-2018.txt` (cwd `$LANES/lwsrp-docs`; log `command-1791346123127085358.log`) | 0 |
| `rtk proxy timeout 550 python3 -` (cwd `$LANES/lwsrp-docs`; log `command-1791346123135354036.log`) | 0 |
| `rtk proxy timeout 550 sed -n 16500,16640p $VALIDATION_STORAGE/lwsrpdoc-a561/round2/802.1Q-2018.txt` (cwd `$LANES/lwsrp-docs`; log `command-1791346142122723846.log`) | 0 |
| `rtk proxy timeout 550 git show --no-patch --format=%H%n%P%n%B HEAD` (cwd `$LANES/lwsrp-docs`; log `command-1791346142126346202.log`) | 0 |
| `rtk proxy timeout 550 cat doc/tools/check_references.py tests/features/switch_bindings.c $VALIDATION_STORAGE/lwsrpdoc-a561/page_commands.py $VALIDATION_STORAGE/lwsrpdoc-a561/finalize.py` (cwd `$LANES/lwsrp-docs`; log `command-1791346142136371096.log`) | 0 |
| `rtk proxy timeout 550 rg -n 'zero assertions&#124;empty (test&#124;configured)&#124;placeholder&#124;optional unit&#124;blocked&#124;fails before&#124;currently fails&#124;not exported&#124;normative.*(open&#124;necessary)&#124;verification remains&#124;bare-metal port' README.md CONTRIBUTING.md doc` (cwd `$LANES/lwsrp-docs`; log `command-1791346344499509145.log`) | 0 |
| `rtk proxy timeout 550 python3 doc/tools/check_sentences.py` (cwd `$LANES/lwsrp-docs`; log `command-1791346344481841302.log`) | 0 |
| `rtk proxy timeout 550 python3 doc/tools/check_references.py` (cwd `$LANES/lwsrp-docs`; log `command-1791346344497054171.log`) | 0 |
| `rtk proxy timeout 550 python3 doc/tools/check_links.py --github-auth` (cwd `$LANES/lwsrp-docs`; log `command-1791346344480262292.log`) | 1 |
| `rtk proxy timeout 550 python3 -` (cwd `$LANES/lwsrp-docs`; log `command-1791346398771589778.log`) | 0 |
| `rtk proxy timeout 550 git diff --check` (cwd `$LANES/lwsrp-docs`; log `command-1791346416764678596.log`) | 0 |
| `rtk proxy git ls-files -z` (snapshot inventory) | 0 |
| `rtk proxy timeout 550 python3 -` (cwd `$LANES/lwsrp-docs`; log `command-1791346416765140438.log`) | 0 |
| `rtk proxy cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug` (README.md:35; scratch snapshot; log page-command-01.log) | 0 |
| `rtk proxy cmake --build build --parallel 2` (README.md:36; scratch snapshot; log page-command-02.log) | 0 |
| `rtk proxy ctest --test-dir build --output-on-failure` (README.md:37; scratch snapshot; log page-command-03.log) | 0 |
| `rtk proxy behave` (README.md:38; scratch snapshot; log page-command-04.log) | 0 |
| `rtk proxy cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug` (doc/tester.md:15; scratch snapshot; log page-command-05.log) | 0 |
| `rtk proxy cmake --build build --parallel 2` (doc/tester.md:16; scratch snapshot; log page-command-06.log) | 0 |
| `rtk proxy ctest --test-dir build --output-on-failure` (doc/tester.md:17; scratch snapshot; log page-command-07.log) | 0 |
| `rtk proxy ./build/unit_tests` (doc/tester.md:18; scratch snapshot; log page-command-08.log) | 0 |
| `rtk proxy behave` (doc/tester.md:19; scratch snapshot; log page-command-09.log) | 0 |
| `rtk proxy behave --dry-run` (doc/tester.md:20; scratch snapshot; log page-command-10.log) | 0 |
| `rtk proxy cc -std=c11 -Isrc/include tests/unit/mrp_pdu_test.c src/core/mrp_pdu.c -xc - -lcgreen -o build/mrp_pdu_tests <<'C'<br>#include <cgreen/cgreen.h><br>TestSuite *mrp_pdu_suite(void);<br>int main(void)<br>{<br>    return run_test_suite(mrp_pdu_suite(), create_text_reporter());<br>}<br>C` (doc/tester.md:45; scratch snapshot; log page-command-11.log) | 0 |
| `rtk proxy ./build/mrp_pdu_tests` (doc/tester.md:53; scratch snapshot; log page-command-12.log) | 0 |
| `rtk proxy python3 doc/tools/check_sentences.py` (doc/tools/README.md:14; scratch snapshot; log page-command-13.log) | 0 |
| `rtk proxy python3 doc/tools/check_references.py` (doc/tools/README.md:15; scratch snapshot; log page-command-14.log) | 0 |
| `rtk proxy python3 doc/tools/check_links.py --github-auth` (doc/tools/README.md:16; scratch snapshot; log page-command-15.log) | 1 |
| `rtk proxy python3 doc/tools/render_mermaid.py --output "$DOC_SCRATCH/graphs"` (doc/tools/README.md:17; scratch snapshot; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/CONTRIBUTING.md-47.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/CONTRIBUTING.md-47.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/README.md-14.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/README.md-14.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-architecture.md-10.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-architecture.md-10.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-architecture.md-34.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-architecture.md-34.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-architecture.md-56.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-architecture.md-56.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-developer.md-28.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-developer.md-28.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-developer.md-76.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-developer.md-76.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-developer.md-114.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-developer.md-114.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-developer.md-146.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-developer.md-146.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-developer.md-182.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-developer.md-182.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-developer.md-214.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-developer.md-214.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-developer.md-243.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-developer.md-243.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-developer.md-269.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-developer.md-269.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-integrator.md-46.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-integrator.md-46.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-integrator.md-81.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-integrator.md-81.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-integrator.md-115.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-integrator.md-115.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-integrator.md-144.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-integrator.md-144.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-integrator.md-169.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-integrator.md-169.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-integrator.md-201.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-integrator.md-201.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-manager.md-41.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-manager.md-41.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-tester.md-62.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-tester.md-62.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-tester.md-92.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round2/render/graphs/doc-tester.md-92.svg -b white` (render subprocess; log page-command-16.log) | 0 |
| `rtk proxy timeout 550 python3 $VALIDATION_STORAGE/lwsrpdoc-a561/round2/page_commands.py` (cwd `$LANES/lwsrp-docs`; log `command-1791346416765447078.log`) | 0 |
| `rtk proxy python3 $VALIDATION_STORAGE/lwsrpdoc-a561/round2/link-fixture/doc/tools/check_links.py --local-only` (negative link fixture) | 1 |
| `rtk proxy timeout 550 python3 -` (cwd `$LANES/lwsrp-docs`; log `command-1791346438865788804.log`) | 0 |
| `rtk proxy timeout 550 git diff --stat` (cwd `$LANES/lwsrp-docs`; log `command-1791346452845154749.log`) | 0 |
| `rtk proxy timeout 550 python3 -` (cwd `$LANES/lwsrp-docs`; log `command-1791346452839772172.log`) | 0 |
| `rtk proxy timeout 550 node --input-type=module -` (cwd `$LANES/lwsrp-docs`; log `command-1791346481450619535.log`) | 1 |
| `rtk proxy timeout 550 node --input-type=module -` (cwd `$LANES/lwsrp-docs`; log `command-1791346494213513888.log`) | 0 |
| `rtk proxy timeout 550 git diff --exit-code e4f9995b791489c53b8ccb8a8dc09ec508e32e6b -- src tests CMakeLists.txt build.sh zephyr Kconfig.zephyr behave.ini` (cwd `$LANES/lwsrp-docs`; log `command-1791346533734597842.log`) | 0 |
| `rtk proxy timeout 550 git diff -- doc/tools/check_links.py README.md doc/tester.md doc/integrator.md doc/manager.md` (cwd `$LANES/lwsrp-docs`; log `command-1791346533739591756.log`) | 0 |
| `rtk proxy timeout 550 python3 -` (cwd `$LANES/lwsrp-docs`; log `command-1791346533744733853.log`) | 0 |
| `git remote get-url origin` (checker child; initial checkout link check) | 0 |
| `gh api --hostname github.com repos/kebag-logic/lwSRP/issues --silent` (checker child; initial checkout link check) | 0 |
| `gh api --hostname github.com repos/kebag-logic/lwSRP/issues/1 --silent` (checker child; initial checkout link check) | 0 |
| `gh api --hostname github.com repos/kebag-logic/lwSRP/pulls --silent` (checker child; initial checkout link check) | 0 |
| `git remote get-url origin` (checker child; published command 15 in scratch snapshot) | 0 |
| `gh api --hostname github.com repos/kebag-logic/lwSRP/issues --silent` (checker child; published command 15 in scratch snapshot) | 0 |
| `gh api --hostname github.com repos/kebag-logic/lwSRP/issues/1 --silent` (checker child; published command 15 in scratch snapshot) | 0 |
| `gh api --hostname github.com repos/kebag-logic/lwSRP/pulls --silent` (checker child; published command 15 in scratch snapshot) | 0 |
| `rtk proxy timeout 550 python3 -` (cwd `$LANES/lwsrp-docs`; log `command-1791346622374435937.log`) | 0 |
| `rtk proxy timeout 550 git diff --check` (cwd `$LANES/lwsrp-docs`; log `command-1791346656024389940.log`) | 0 |
| `rtk proxy timeout 550 python3 -` (cwd `$LANES/lwsrp-docs`; log `command-1791346656028436292.log`) | 0 |
| `rtk proxy timeout 550 gh api --hostname github.com repos/kebag-logic/lwSRP/pulls/3 --silent` (cwd `$LANES/lwsrp-docs`; log `command-1791346656019590798.log`) | 0 |
| `rtk proxy timeout 550 git add README.md doc/developer.md doc/integrator.md doc/manager.md doc/tester.md doc/tools/README.md doc/tools/check_links.py` (cwd `$LANES/lwsrp-docs`; log `command-1791346657004753247.log`) | 0 |
| `rtk proxy timeout 550 git diff --cached --check` (cwd `$LANES/lwsrp-docs`; log `command-1791346657138278070.log`) | 0 |
| `rtk proxy timeout 550 git commit -m 'docs: verify state tables and refresh harness guidance'` (cwd `$LANES/lwsrp-docs`; log `command-1791346657260333853.log`) | 0 |
| `rtk proxy timeout 550 python3 -` (cwd `$LANES/lwsrp-docs`; log `command-1791346697843067346.log`) | 0 |
| `rtk proxy timeout 550 git rev-parse HEAD` | 0 |
| `rtk proxy timeout 550 git status --porcelain` | 0 |
| `rtk proxy timeout 550 git branch --show-current` | 0 |
| `rtk proxy timeout 550 git show -s --format=%B HEAD` | 0 |
| `rtk proxy timeout 550 git show -s --format=%B 'HEAD^'` | 0 |
| `rtk proxy timeout 550 git config --get user.name` | 0 |
| `rtk proxy timeout 550 git config --get user.email` | 0 |
| `rtk proxy timeout 550 git show -s --format=%an%x00%ae%x00%cn%x00%ce HEAD` | 0 |
| `rtk proxy timeout 550 git show -s --format=%an%x00%ae%x00%cn%x00%ce 'HEAD^'` | 0 |
| `rtk proxy timeout 550 git diff --exit-code e4f9995b791489c53b8ccb8a8dc09ec508e32e6b HEAD -- src tests CMakeLists.txt build.sh zephyr Kconfig.zephyr behave.ini` | 0 |
| `rtk proxy timeout 550 git diff --check 8962e2f1870b8981b4ed685c663e49a69b98f8ab HEAD` | 0 |
| `rtk proxy timeout 550 gh issue comment 1 --repo kebag-logic/lwSRP --body '[A561] REVIEW READY 5f9b9d99e1d94485fc00a1b1539baf2ae861cb65'` | 0 |
| `rtk proxy timeout 600 python3 $VALIDATION_STORAGE/lwsrpdoc-a561/round2/finish.py` (final verification, marker, and artifact finalization) | 0 |
