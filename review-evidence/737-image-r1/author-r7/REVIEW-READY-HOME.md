[A615] REVIEW READY - PR #738

Head: `18f2df92b13cb3f4036b073ed76940187bf10487` on `737-ci-image`.

Under PR #738 comment 6166238176, restored the exact round-2 HOME mapping, retained the SDK symlink, and preserved the environment, mounts and disabled network. The home-relative compiler preflight inside the final image passed, rc 0, GCC 14.3.0.

The unchanged `test_baremetal_profile_contract` with `--require-rv32` completed in the background without a timeout: **rc 0; wall time 1,014,708 ms (1014.708 seconds)**. The existing `MAKEFLAGS += -e` mutation arm was NOT RUN because this make does not re-read MAKEFLAGS mid-parse; the gate reports that no tool is missing. The compiler-backed census and identity checks ran. Final image manifest: `sha256:8cc05a5c51aa04a23063c5d0593065912845a4ba4ce5a5dfd3ff53b12ccd1d19`.

All 103 builder function invocations have now returned across nine groups, each command rc 0. The existing `mf48` resource-calibration arm remains NOT RUN because its Vivado build tree is absent, matching the hosted skip and public ruling. This is grouped evidence, not a monolithic builder invocation. The two identical cold builds stand.

HANDOFF.md, PR-BODY.md and the evidence ledger are updated. The new compiler preflight, environment comparison, completed-function report and campaign receipt record reproducible evidence, including timing and raw-log hashes. No source changes, new commits, push or PR edits were made. Independent review and workflow adoption remain outstanding.
