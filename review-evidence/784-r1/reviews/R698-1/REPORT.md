[R698] POSITIVE - exact head 42dbe6bd42c950a7acedce56fcf29b82543123c6

Round R698-1, external independent review of issue #784 step 1 / PR #785. All five lenses were independently applied. No BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION finding was identified. This is a source-review verdict, not merge authorization or signed local CI acceptance.

Reviewed tree: `5fdfce709af95cf8bfe7efc1083cca5162b62d1f`. Source base: `d385b38e5282b395ca55d49d135e46a93f56a340`. The sole commit changes scripts/act_ci.py (+159/-7) and docs/testing/CI_WORKFLOWS.md (+10/-1). Workflows, templates, generators, RTL and gitlinks are unchanged.

Authority and reconstruction

Read AGENTS.md, CONTRIBUTING.md and docs/README.md, then the [issue and frozen assignment](https://github.com/kebag-logic/milan-fpga/issues/784#issuecomment-6400713781), its public scope decisions, REQUIREMENTS.md verification obligations, and the CI workflow trust and runner contracts before the diff/history. The independent pass preceded reading any other review findings. The [public review start](https://github.com/kebag-logic/milan-fpga/pull/785#issuecomment-6408072295) identifies this round.

The [temporary required-check decision](https://github.com/kebag-logic/milan-fpga/issues/784#issuecomment-6400810252) requires manager-signed local CI until step 2 restores the hosted image/checks. Step 1 must not close #784.

[R698] PASS Conformance - scripts/act_ci.py:92, :2061, :4828; issue #784 assignment; receipts/label-probes.log - RUNS_ON_LABELS is the single production source for sandbox membership and platform construction. Exactly ubuntu-latest and ubuntu-24.04 are accepted, with one platform entry each mapping to catthehacker/ubuntu:full-latest.

Independent probes drove run_validation, its real sandbox and command builder through the existing dry-run fixture. Ubuntu 22.04/26.04, a matrix expression, a list, an empty YAML value, an empty string, null, a mapping, a boolean, an integer, upper-case spelling and the ARM variant all refuse with the parsed value in the diagnostic, zero Docker boundaries and no platform command. Production run_validation:5994 performs the check before submodule initialization, runtime checks, Docker boundary creation or workflow execution. Git materialization/byte verification still precede it.

[R698] PASS RTL - scripts/act_ci.py:5975, :4828, :4862, :7651; .github/workflows/docs.yml:748; receipts/tree-integrity.log - orchestration trust and existing module interfaces are preserved. The two-file diff makes HDL, clock/reset and CDC changes inapplicable. Both labels retain the same 8g memory/equal-swap bound; hosted-memory commentary covers both labels.

Searching all label occurrences in act_ci.py found no other production acceptance path; remaining literal uses are fixtures. Other CI scripts naming ubuntu-latest are workflow generators, ci_events contracts/fixtures, a workflow-plan fixture and a historical Yosys comment. They consistently retain the step-1 label. Their appropriate contracts/generators are step-2 work. No ImageOS reader exists in scripts or .github.

The trusted dev runner sees unchanged ubuntu-latest workflows for this PR. Bootstrap policy, runtime pin, trusted-source selection, image and Docker authority are unchanged. A disposable copy relabeling all 46 shipping jobs ubuntu-24.04 passes this runner's real sandbox. This establishes step-2 label compatibility, not a completed live replay.

[R698] PASS Robustness - scripts/act_ci.py:2045, :6765, :6810; receipts/label-probes.log and mutation logs - exact membership rejects nonliteral/wrong-type YAML values and arbitrary Ubuntu labels. Every unsupported-value replay refuses before the mocked Docker boundary. Exact platform-list comparison detects missing/duplicate entries; image comparison detects wrong images. Existing container/service/action restrictions remain intact.

[R698] PASS Tests - scripts/act_ci.py:6720, :6742, :6810, :15257, :15464; receipts/runner-contract.log; receipts/ci-events.log and mutation logs - the 12 new arms are registered and call production functions. Materialization/external services are faked, while the validator and command builder remain real. The expected two-label list is independent of the production tuple.

Both complete runner invocations passed: ordinary --selftest, then a mode-0555 flat copy run with -I --selftest --worktree /repo. The receipt records direct_rc=0 and installed_rc=0. These reproduce the two invocation forms in docs.yml:748.

| Mutation | Child exit | Named checks that fail |
|---|---:|---|
| drop-2404-from-platform-map | 1 | 24.04 replay mapping; once-each platform list; accepted/mapped equality |
| map-2404-to-act-default-image | 1 | Same three checks, with 24.04 mapped to node:16-bullseye-slim |
| accept-any-ubuntu-prefix | 1 | 26.04 refusal; 22.04 refusal; ARM refusal; pre-Docker replay refusal; accepted/mapped equality |

The first two replacements reproduce the published mutants. The third was independently constructed from the reviewed membership condition. Each probe wrapper exits zero only after observing child exit 1 and the required named failure: wrapper zero means successful detection.

ci_events.py --check passed 2199 contract items; --selftest passed 5236 arms. No copied validator or command-construction oracle was substituted to obtain these results.

[R698] PASS Docs - docs/testing/CI_WORKFLOWS.md:2028; receipts/docs-gates-complete.log; public issue/PR evidence - the contract accurately names both temporary labels, shared image, named refusal, hosted 26.04 pip failure and step-2 pin. It explains the unsupported-platform false green. Added source comments describe behavior/reason, cite #784, and introduce no bench label, lane name, reviewer identity, round or issue-comment identifier.

Independent docs checks passed: docs_check, feature status, em-dash against d385b38e, documentation style, TOC self-test/anchors/check, document paths, bare-metal-only and documentation map. Workflow-generator and evidence-helper-pin checks also passed. The first docs attempt refused because the isolated environment lacked locked six; installing the complete hashed Markdown lock in the disposable environment resolved it. That failed setup receipt is retained. The map command emitted a font-configuration warning but passed its map/path/decoded-PNG check.

Public evidence examined

Read the [published author receipts](https://github.com/kebag-logic/milan-fpga/tree/1a5e9b86fb054bf2d33ad4c016ecb1e5e021d716/review-evidence/784-r1): complete runner-contract logs for both recorded Python environments, CI-event results, docs tables/receipts, mutation replacements/results and the no-daemon platform probe. The runner logs record rc 0 and no named self-test failures. Eight selected copied receipts match published SHA-256 values (receipts/public-hashes.log). These are author source-head receipts, not manager source banks.

The published platform probe distinguishes an unsupported-label skip with exit zero from a correctly mapped job reaching the intended image, then failing on a deliberately absent daemon. This supports the mapping contract; it is not successful job execution. Hosted-image excerpts concern PR #783 and the source-base push, not this exact head's hosted execution. No skipped context is counted as an executed test, and no exact-head hosted success is claimed.

Prior public finding reconciliation

After writing the independent verdict and ledger, re-read the PR discussion and queried submitted reviews and inline comments. The timeline contained only the two review-start notices; both review collections were empty. No prior public finding requires resolution or retention at this head. Receipt: receipts/prior-findings.json.

Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #784 assignment; act_ci.py:92,2061,4828; label-probes.log | R698-1 | 42dbe6bd42c950a7acedce56fcf29b82543123c6 |
| RTL | CLEAN | Two-file diff; act_ci.py:5975,4862,7651; docs.yml:748; tree-integrity.log | R698-1 | 42dbe6bd42c950a7acedce56fcf29b82543123c6 |
| Robustness | CLEAN | act_ci.py:2045,6765,6810; label-probes.log; mutation logs | R698-1 | 42dbe6bd42c950a7acedce56fcf29b82543123c6 |
| Tests | CLEAN | act_ci.py:6720,6742,6810,15257,15464; runner-contract.log; ci-events.log; mutation logs | R698-1 | 42dbe6bd42c950a7acedce56fcf29b82543123c6 |
| Docs | CLEAN | CI_WORKFLOWS.md:2028; docs-gates-complete.log; public source-head receipts | R698-1 | 42dbe6bd42c950a7acedce56fcf29b82543123c6 |

Limits and pending manager duties

Candidate-runner execution occurred only inside disposable unprivileged user/PID/network namespaces, with read-only source, private temporary storage, no host home/credentials/daemon socket and no capabilities. No Docker/act execution, privileged invocation, real-PR runner invocation, source edit, commit, push, GitHub write, author contact or sub-agent occurred. Local execution used Python 3.14/PyYAML 6.0.3; Python 3.12/PyYAML 6.0.2 evidence was read from published receipts. No full build banks or hardware measurements ran. Physical calibration is NOT RUN; field skips are not hardware proof.

Direct verification checked all 1442 tracked blob bytes/modes, all index entries, all six gitlinks and the three initialized submodule heads. The other three submodules remain uninitialized; their tree/index pins were verified. The clone remains clean at the requested exact head/tree. Mutants and relabeled workflow copies existed only under disposable scratch storage.

The manager must still publish/accept signed local CI with all-four-workflow trusted-runner replay and job coverage; validate the final current-dev candidate (assignment tip e76a755afc0536453161e3cd33f6f4d2dcd7641f); obtain the other independent positive review; ensure no review remains in flight; and perform authorized merge/containment. No manager source-bank run at this exact head is claimed or inferred. Step 2 and restoration of seven hosted required checks remain open under #784.

R698-1 FINISHED
