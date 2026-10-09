The scripts take a clean exact-head checkout and a packet directory. Disposable trees stay beneath the packet's `scratch/` directory. They do not edit the reviewed checkout or write to remote services.

Prerequisites match the repository's Linux and RV32 validation dependencies. [Versions](receipts/versions.json) identify this run. The cross compiler must use a name accepted by the repository toolchain file. These scripts perform no installation.

Set `REVIEW_REPO` to the isolated checkout and `REVIEW_PACKET` to this directory. Run these foreground commands in order. Apply the environment's required command prefix when applicable.

```sh
python3 scripts/run_review.py "$REVIEW_REPO" "$REVIEW_PACKET"
python3 scripts/compare_comments.py "$REVIEW_REPO" "$REVIEW_PACKET"
python3 scripts/probe_comments.py "$REVIEW_REPO" "$REVIEW_PACKET"
python3 scripts/repeat_and_before.py "$REVIEW_REPO" "$REVIEW_PACKET"
python3 scripts/audit_receipts.py "$REVIEW_REPO" "$REVIEW_PACKET"
python3 scripts/read_hosted.py "$REVIEW_PACKET"
```

Foreground supervisors wait for every child. Concurrency stays within sixteen worker jobs; command limits are under ten minutes. The first script runs the validation checks with an explicit concurrency budget. Object comparison uses actual CI compile databases, stable paths and `-g0 -frandom-seed=0`. The supplemental script compares all hosted test outcomes before/after reduction and runs fresh/reused mutation campaigns.

The comment probe intentionally reproduces an open defect. Expected gate statuses at this head: baseline 0; ordinary prose 1; SPDX-block prose 0; spliced-SPDX prose 0. The block uses the required warning flags unchanged. Only the supplementary spliced-line compile disables the multiline-comment warning. The script exits zero after verifying these observations. That means successful reproduction, not defect acceptance.

The final audit independently checks named assertions in XML, local document targets, and checkout blobs/modes/index/gitlinks. The hosted reader uses existing authenticated read-only access to fixed published run IDs. It does not trigger workflows.

Original logs, XML, archives and binaries remain under scratch. Published local logs replace checkout, packet and home locations with neutral placeholders without changing results. [MANIFEST.sha256](MANIFEST.sha256) lists the publishable files. Unlisted API snapshots and downloaded prior reports are reconstruction inputs only.
