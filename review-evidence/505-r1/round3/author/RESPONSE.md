[A163] RESPONSE TO R220-2 F3

Old head: `ad62493186576144f9fa1568babad012bc9ad8ca`.
Old tree: `6b279253aa7d3edd6d9b5e9adc1ed9caf6f13d75`.
New head: `5d45ecc0cf2dc572d538cbc534b5d9f95c8688e7`.
New tree: `2ec2d2e9931d250dacb945643cf3a444ec0e9a91`.
Actual merge base: `b17580b91deb11f3441dfc5d7f9fafe539d929b8`.
The original dev base, origin/dev and live remote dev matched that merge base at the final check.

Changed artifact: `docs/testing/CI_WORKFLOWS.md:768`, only the remaining-content-gap paragraph in item 12. The commit replaces two lines with four. It names the seven RTL jobs' scripts without specialized pins and the sibling full-ci-gate "Print the event and pin the one SHA this run validates" script as future #439 work. The four-carrier statements and all remaining document bytes are preserved.

Original finding: R220-2 MINOR Docs F3. The inaccurate current-tree prose is corrected; the executable gaps remain future #439 work. The finding is not relabeled or disposed of merely by linking #439. Independent reviewers determine its resolution.

The replacement text is:

> The seven RTL jobs still have scripts without specialized pins.
> The sibling `full-ci-gate` SHA-pin script also remains unpinned:
> "Print the event and pin the one SHA this run validates".
> Both remaining content gaps are future work under #439.

The #439 public decision supplies the tracker for both executable gaps. This commit corrects the inaccurate paragraph in PR505 itself. It implements no future pin.

Focused validation exited 0: ci_events --check (1505 items), --selftest (1144 arms and 1046 mutation arms), docs_check, gen_toc --check, check_doc_paths, check_em_dash --base at the actual merge base above, and working-tree/committed-range git diff --check. Exact commands and results are in HANDOFF.md and logs/04 through logs/14. Complete hash audits confirm only the paragraph changed, with all other tracked bytes and all gitlinks preserved.

Historical AC5 attribution: A10 measured act behavior at `6af65a151663e1301f1983a6c9d22650a0b35da9`; R220-2 independently read those receipts and retained them for the prior head `ad62493186576144f9fa1568babad012bc9ad8ca`. This author did not execute act or remeasure AC5. Those receipts are historical, not execution on the new head. Any retention decision for the corrected head belongs to the manager and independent reviewers.

Remaining manager work: publish the full review-ready evidence and corrected head; complete the required local/native gates, supported trusted act replicas and exact-head hosted gates; arrange targeted cold R219/R220 Docs and Conformance re-reviews. Only reviewers may accept any unchanged banked RTL/Robustness/Tests coverage. Candidate-merge validation and eventual post-merge containment remain required. No review verdict or completion ledger is supplied by this author.

The local commit is unpushed. PR505 remains draft at remote head `ad62493186576144f9fa1568babad012bc9ad8ca`. No PR metadata or project mutation, push, merge, other agent, Docker/act execution, privileged action, hardware access, dependency installation, unrelated gate or other worktree edit was performed. The optional malformed-pristine traceback suggestion was not adopted.

Public references:

- [Original R220-2 F3](https://github.com/kebag-logic/milan-fpga/pull/505#issuecomment-5772521129).
- [Accepted correction scope](https://github.com/kebag-logic/milan-fpga/pull/505#issuecomment-5772548304).
- [Settled #439 scope decision](https://github.com/kebag-logic/milan-fpga/issues/439#issuecomment-5772547851).
- [A163 TAKEN before edit](https://github.com/kebag-logic/milan-fpga/issues/407#issuecomment-5772948224).
- [A163 factual issue handoff](https://github.com/kebag-logic/milan-fpga/issues/407#issuecomment-5772987925).
