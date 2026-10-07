[R543] POSITIVE - exact head f800a2bb920c543934d6286a47fe20dde3efa2c5

Independent external review of [issue #13](https://github.com/kebag-logic/lwSRP/issues/13) and [PR #14](https://github.com/kebag-logic/lwSRP/pull/14), round R543-1. Tree: `f950b4f333aeb8b2cb267c7c2040645ff6f8050c`. Source base: `a4cbe41de1c80d43f26e0d348cbdb45075273a4f`.

The change satisfies the source acceptance criteria. One commit removes exactly 37 bytes: the SPDX line and its following blank line. LICENSE matches Apache's canonical file byte for byte. GitHub detects Apache-2.0 at this exact head. All other 59 tracked files retain their SPDX headers, complete bytes, and modes. No open BLOCKER, MAJOR, or MINOR remains. One optional documentation suggestion is retained below.

The review followed the [public assignment](https://github.com/kebag-logic/lwSRP/pull/14#issuecomment-6036960158). Reconstruction proceeded through repository rules and guides, frozen acceptance and public scope, linked authorities, the independent diff/history examination, and public executable evidence. No tracked AGENTS.md exists. [CONTRIBUTING.md](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/CONTRIBUTING.md), the root README, and the documentation guides govern contribution and validation. [Issue #8](https://github.com/kebag-logic/lwSRP/issues/8) supplies the earlier licensing requirements; issue #13 explicitly scopes the exception for LICENSE. Issue #13 had no comments or later scope decisions at the final capture.

The applicable external interface authority is the [canonical Apache text](https://www.apache.org/licenses/LICENSE-2.0.txt). Protocol standards and application interfaces are unchanged and introduce no new conformance obligation in this license-only diff. The Markdown header rule at [CONTRIBUTING.md:41](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/CONTRIBUTING.md#L41) does not apply to LICENSE. The shared parser scans Markdown pages, and the link check requires LICENSE to exist. Searches of all tracked content found no check or documentation requiring an SPDX line inside LICENSE. See [authority inventory](receipts/authority-inventory.txt), [reference search](receipts/license-references.txt), [diff](receipts/exact.diff), and [history](receipts/history.txt).

**Executed evidence**

All processes completed in the foreground. Each validation group has log and return-code receipts; the audit also records its nested comparison results. Independent documentation work and dependency preparation overlapped. Builds used `make -j16`, one compilation build at a time. Dependencies, builds, and probe copies stayed under packet scratch; no shared installation or source edit occurred.

| Check | Result | Receipts |
| --- | --- | --- |
| Canonical download and `cmp` | HTTP 200; cmp rc 0; 11,358 bytes; SHA-256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` | [Canonical bytes](receipts/apache-LICENSE-2.0.txt), [response](receipts/apache-response.txt), [audit](receipts/final-audit.log) |
| Entire tracked tree, index, bytes, and modes | 60 files; only LICENSE differs from base; 59 retained headers; 58 on line 1 and build.sh on line 2; clean worktree/index; zero gitlinks | [Initial audit](receipts/initial-audit.log), [final audit](receipts/final-audit.log) |
| Exact-head license API | Apache-2.0; blob `d645695673349e3947e8e5ae42332d0ac3164cd7`; decoded API bytes equal local LICENSE | [Head response](receipts/head-license.json) |
| Canonical negative controls | Old header, missing final newline, and CRLF copies each rejected by cmp, rc 1 as expected | [Audit](receipts/final-audit.log), [portable audit](scripts/audit.py) |
| Sentence check | rc 0; 975 sentences/fragments; zero over limit; zero prose exceptions | [Log](receipts/sentences.log) |
| Reference check and self-test | Both rc 0; zero unlinked references; 79 self-test cases, zero failures | [Check](receipts/references.log), [self-test](receipts/references-self-test.log) |
| Anonymous link check | rc 0; 354 local links, 20 external URLs, zero failures; all external responses HTTP 200 | [Log](receipts/links-anonymous.log) |
| Default Debug configure/build | Both rc 0; no compiler warnings or errors | [Configure](receipts/configure-off.log), [build](receipts/build-off.log) |
| Default ctest and direct unit execution | Both rc 0; ctest 1/1; 86 tests, 19,885 assertions | [ctest](receipts/ctest-off.log), [unit runner](receipts/unit-off.log) |
| Default scenarios | rc 0; one feature, three scenarios, ten steps passed; zero skips | [Log](receipts/behave-off.log) |
| Milan Debug configure/build | Both rc 0; no compiler warnings or errors | [Configure](receipts/configure-on.log), [build](receipts/build-on.log) |
| Milan ctest and direct unit execution | Both rc 0; ctest 1/1; 86 tests, 19,873 assertions | [ctest](receipts/ctest-on.log), [unit runner](receipts/unit-on.log) |
| Milan scenarios | rc 0; one feature, three scenarios, ten steps passed; zero skips | [Log](receipts/behave-on.log) |

The unit dependency was built from its public 1.7.0 release into scratch. Its provenance and archive checksum are in [dependency-provenance.json](receipts/dependency-provenance.json). This was a separate dependency build, not a parent builder bank. [Command metadata](receipts/build-commands.json) and [environment](receipts/environment.txt) identify the executed setup. Assertion counts match the existing documentation. Scenario passes do not establish independent port-state observation; the existing limitation remains documented and tracked by [issue #4](https://github.com/kebag-logic/lwSRP/issues/4).

**Public evidence and prior findings**

The [pinned public evidence](https://github.com/kebag-logic/milan-fpga/tree/f15a271b1211a566ff3b163b5a8195280e8bac9e/review-evidence/lwsrplicfix-r1) contains an author PR-body snapshot and anonymous link log. Both match their published manifest hashes: `3d2c35ed42511e9aa34daeb0face12c150a747367f1773ac5a04a052b76580f9` and `b9bfa14779575a64053ccbc8bfb3b3580d4b1c12c88c1f7d5bebd1bc0506eb67`. The link results are independently reproduced here. The body snapshot predates the subsequent PR-body corrections. See [manifest](receipts/public-evidence-manifest-content.json) and [public log](receipts/public-evidence/author/links.log).

My [independent verdict and five-lens ledger](receipts/independent-verdict.md) were written before reading another reviewer's report or findings on this PR. I then read the [public prior review](https://github.com/kebag-logic/lwSRP/pull/14#issuecomment-6037064383) and checked every finding. The final [PR-body snapshot](receipts/pr14-final.json) has update time `2026-10-07T11:35:55Z`, unchanged source head, and was verified again in the [final capture](receipts/reconcile-capture.json), completed `2026-10-07T11:37:58Z`.

- **R542-1/F1 — MINOR — RESOLVED.** Lenses: Conformance, Tests, Docs. Artifact: PR #14 validation table. Authority: CONTRIBUTING.md:59-60 requires test execution and recorded exit codes. The earlier body omitted required execution results, making the evidence record incomplete rather than merely awkward prose. Required outcome: record documentation checks, configure/build, ctest/unit execution, and scenario results at this head. Verification: the refreshed body records rc 0 for each required check, 975 sentence fragments with zero over limit, zero unlinked references, 79 self-tests, ctest 1/1 with 19,885 unit passes, and three scenarios/ten steps. The ctest entry explicitly records the unit runner's result. These values match this reviewer's receipts. This finding is closed without a source change.
- **R542-1/F2 — RESIDUE — RESOLVED.** Lens: Docs. Artifact: the two repository file links in PR #14. Authority/evidence: the old body used the moving `licence-canonical` branch, so deletion could break references. Required exact fix: replace `blob/licence-canonical/` with `blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/` in both links. Verification: both LICENSE and check_links.py URLs in the refreshed body use that exact immutable head. No measurement or claim changed; no residue remains open.
- **R542-1/F3 — SUGGESTION — RETAINED.** Lens: Docs. Artifact: [doc/tools/README.md:17](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tools/README.md#L17) and lines 34-40. Evidence: the example still includes authentication, while the repository is public. Impact: readers must apply the later instruction to omit authentication after publication. Optional outcome: make the anonymous command the primary example in a separate documentation change. Verification: the existing anonymous command passes 354 local and 20 external links here. The current page already explains public access correctly; this suggestion does not make a lens unclean.

At the final capture there were three PR issue comments: two review-start notices and the prior review. There were zero submitted PR reviews, zero inline review comments, and zero issue #13 comments. No additional findings or manager bank-evidence comments were present.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Issue #13 and #8 acceptance; canonical bytes and cmp; whole-tree audit; license API; CONTRIBUTING.md; corrected PR validation record; F1 closure | R543-1 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |
| RTL | CLEAN — not applicable | LICENSE-only diff; full 60-entry tree/index comparison; C build definition; no RTL or executable source change | R543-1 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |
| Robustness | CLEAN | Complete LICENSE byte comparison; unchanged NOTICE; 59 preserved headers and blobs; three canonical negative controls; header-dependency search; final index/mode audit | R543-1 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |
| Tests | CLEAN | Both Debug profiles; ctest and direct unit logs; executed scenarios; documentation checker logs; explicit hosted inventory; corrected PR results and F1 closure | R543-1 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |
| Docs | CLEAN | Contribution rules; README and documentation guides; Markdown parser/checkers; anonymous links; public scope and PR snapshots; F1/F2 closure and nonblocking F3 | R543-1 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |

**Limits and pending manager duties**

This verdict validates the source head only. The manager's assignment states that broader source static/builder and native banks passed. Their receipts were absent from the pinned packet and inspected comments, so this review does not independently attest those banks. Full parent, protocol, synthesis, and builder campaigns were not run. Unchanged graph rendering, embedded/freestanding checks, and broad reversal campaigns were not rerun. No wider protocol-conformance or interoperability claim follows from these focused checks.

The [hosted-run inventory](receipts/hosted-runs.json), [check runs](receipts/check-runs.json), and [commit status](receipts/commit-status.json) contain zero runs, zero checks, and zero individual statuses for this head. The aggregate status says pending. No hosted job executed or was skipped in those inventories; absence is not success. Hosted/act acceptance belongs to the manager.

The public repository and default-branch license endpoints still report NOASSERTION for the old LICENSE blob; the exact-head endpoint reports Apache-2.0. After merge, the manager must verify both default-branch detection endpoints and close issue #13 against that observation. This is a post-merge observation, not an unresolved defect in the reviewed blob.

The manager must build and validate the final current-dev candidate at merge time, using source base `a4cbe41de1c80d43f26e0d348cbdb45075273a4f` and live dev `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`, and handle any parent gitlink update. This clone has no submodule gitlinks or .gitmodules; every tracked blob, executable mode, and index entry was verified unchanged after probes. No source fixes, commits, pushes, external writes, or other-checkout edits were performed.

Physical calibration was NOT RUN. Field skips are not hardware proof. No hardware or target execution was attempted. The manager retains publication, the other independent review's clearance, hosted acceptance, and merge duties. The remaining documentation suggestion is optional.

Portable reproduction is described in [REPRODUCE.md](REPRODUCE.md). [MANIFEST.sha256](MANIFEST.sha256) lists publishable files. Published command logs replace local clone and packet path prefixes with neutral placeholders; original raw copies remain in unpublished scratch. [Path-redaction receipts](receipts/path-redaction.json) record original and published hashes. Scratch is excluded from publication.

R543-1 FINISHED
