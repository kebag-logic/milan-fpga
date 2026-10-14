[A615] STOP - PR #738

Head: `18f2df92b13cb3f4036b073ed76940187bf10487` on `737-ci-image`.

Under PR #738 comment 6165220472, the unchanged `test_baremetal_profile_contract` was invoked with `--require-rv32` in final image `sha256:8cc05a5c51aa04a23063c5d0593065912845a4ba4ce5a5dfd3ff53b12ccd1d19` as a background job without a timeout. Completed process verdict: rc 1; wall time: 3,302 ms.

Failing assertion at `sw/builder/test_builder.py:5117`:
`AssertionError: --require-rv32: the hosted firmware instruments must run`

I omitted the prior scratch-home mapping from this invocation. The unchanged census selects its compiler through a home-relative path (`test_builder.py:4767`), so the run failed its compiler prerequisite before the long campaign. This setup failure does not establish an image defect; the required compiler-backed campaign verdict remains outstanding. No retry followed the failure, as the ruling requires STOP.

The two identical cold builds stand. No source changes, new commits, push or PR edits were made. HANDOFF.md, PR-BODY.md, builder-validation.json and the evidence manifest are updated; builder-background.receipt.json records the result, execution difference and raw-log/command hashes. The next validation needs the compiler location provisioned for the unchanged census and a completed passing campaign verdict.
