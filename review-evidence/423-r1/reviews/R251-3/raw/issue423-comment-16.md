https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5780899288
[A10] TAKEN: bounded correction of R251 F1/F2

Branch: `423-retained-redundant-replay`, continuing PR #519 at `df53dfa116b34816db0193230ad9833e67bf46dd`. The root manager now also executes this correction in the existing isolated lane. No additional author agent is launched; #517 and #520 remain separate editors on their own branches, while R227 reviews #504. This supersedes the earlier single-author scheduling reservation only. All #423 review sessions are terminal and its old replica has completed cancellation/cleanup.

Authoritative references: REQ-VER-04, CONTRIBUTING section 2.1 step 7, the settled G1/H/T decision, and [R251's original findings](https://github.com/kebag-logic/milan-fpga/pull/519#issuecomment-5780883992). Preserve F1 BLOCKER Conformance/Robustness and F2 MAJOR Tests/Conformance exactly.

Interpreted scope: preserve raw filename bytes through both existing postimage/path checks and new retention checks, retain exact patch transport, and add bounded default-selftest subprocess regressions with verified filesystem encodings. Real byte-named fixtures cover missing and retained work, aliasing, undecodable bytes and non-Latin-1 Unicode. Locale unavailability must be explicit and cannot count as executed coverage. The G1/H/T policy, processor pins and acceptance criteria stay unchanged.

Validation plan: complete existing selftest, positive/negative locale matrix, targeted restoration mutations, public reproducer, required static/style gates and complete local native bar before updated publication. Then trusted act and exact-head hosted gates. R251 independently re-reviews its findings and changed scope; R244 supplies the required external review when available. A10 will not approve this implementation. Final current-dev candidate and post-merge bar remain mandatory.

Blockers: no unresolved design choice for this correction; external review is pending provider availability. PR remains draft and Project In progress.
