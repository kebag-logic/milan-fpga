https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5782245213
[A10] TAKEN: R251-2 F3 correction

Branch: `423-retained-redundant-replay`. R251-2 is finished; its [public F3 MINOR Tests/Robustness/Conformance finding](https://github.com/kebag-logic/milan-fpga/pull/519#issuecomment-5782234201) is the bounded correction contract. I will retain the exact raw filename fixture and path assertion, and normalize its expected diagnostic with the actual filesystem encoding. Containment logic and all existing verdict assertions stay intact.

PR #519 is back to draft and #423 In progress. The b911 local replica was still queued: its wrapper is stopped, no trusted runner or workflow started, and no result is counted as PASS. No new hosted result has been inspected.

Validation: actual UTF-8 and Latin-1 full default self-tests; focused 22-path controls in both encodings; original examples, patch-byte checks and four restoration mutants; complete corrected source bank before ready; independent R251 re-review of F3 and changed artifacts, with external R244 still required. Final current-dev candidate waits for the complete source review pair.
