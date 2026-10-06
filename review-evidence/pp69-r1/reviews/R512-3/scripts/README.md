These scripts reproduce the focused source review at the fixed processor head.
Use a fresh output directory and an unchanged detached clone at
`669ded57b1fabc2bbf274b8ad05493c7593e0a0a`.

```sh
rtk proxy python3 scripts/run_review.py \
  --repo /path/to/exact-head-clone \
  --packet /path/to/new-output \
  --compiler /path/to/pinned-5.050/verilator
```

The coordinator prepares exact-head extractions, runs the disjoint 30-control and
56-control notification campaigns concurrently, and joins every child. It also runs
ADP, notification-unit and interface-guard checks. Each campaign uses two jobs;
each native compilation uses two workers. Make receives `-j16`, directly or via
`MAKEFLAGS`. Documentation gates run in a disposable clone with history while the
longer campaign continues. All temporary builds and mutation copies are under the
output's `scratch/`; no tracked file in the supplied clone is changed.

`check_delta.py` verifies merge preservation, all 86 control definitions/anchors,
count-one source identity and the corrected stamp formula. `summarize_campaign.py`
requires exactly 86 unique killed controls with successful builds, completed
tallies, every named failure, and passing goldens. `check_integrity.py` checks raw
tracked blob bytes, executable/symlink modes, index entries and gitlink inventory.

The publication packet contains the actual run logs and return codes. The first
documentation attempt used an archive without Git metadata and failed; its
receipts and as-run companion script are retained. `run_docs.py` is the corrected,
successful setup. The reproduction coordinator uses that setup directly.

The wrapper prefix in the example can be omitted on hosts without that command
proxy. Standard Python, Git, make, a C++ compiler, the pinned simulator and the
repository's documentation dependencies are needed. No source-bank, physical,
container or hardware acceptance is invoked by these scripts.
