# R491-2 receipt reproduction

Use an isolated checkout at the reviewed head, with the three required
submodules initialized at their recorded gitlinks. Set `SOURCE`, `PACKET`,
and `SIMULATOR` to that checkout, an empty output directory, and the pinned
5.050 executable. The scripts require Python 3, Git, make, a C++ compiler,
and the repository's existing Python dependencies. Public snapshots also
require authenticated read access through `gh`.

```sh
mkdir -p "$PACKET/scratch" "$PACKET/receipts"
python3 scripts/verify_tree.py "$SOURCE" > "$PACKET/receipts/tree-before.txt"
python3 scripts/focused_campaign.py "$SOURCE" "$PACKET" "$SIMULATOR" --jobs 2
python3 scripts/focused_checks.py "$SOURCE" "$PACKET"
python3 scripts/public_receipts.py "$PACKET"
python3 scripts/verify_tree.py "$SOURCE" > "$PACKET/receipts/tree-after.txt"
```

Run these from the published packet directory. All commands stay in the
foreground. The campaign supervisor waits for all children. It uses two
independent build/run workers; each recipe starts with `make -j16` and limits
its compilation to eight children. No source in the supplied checkout is
changed. A registered disposable clone, generated inputs, edited RTL copies,
build outputs and compiler transcripts stay under `scratch/`.

The campaign reads mutation definitions 5 through 11 directly from the
reviewed source. It requires nonzero harness exits with named failures, not
build failures or crashes. Two additional cases remove the capture and
render RAM hold terms separately and require the clean result. Their full
runtime transcripts match the clean transcript byte for byte at this head.

The first campaign run completed with exit 0. The checked-in summary records
every build exit, run exit, duration, expected failed assertion and result.
Each runtime log has an adjacent `.rc` receipt. Compiler logs are scratch
only because installation paths can identify a host.

Documentation and raw-diff checks each exited 0. The text receipt collapses
line wrapping only when comparing the requested sentences. During receipt
development, the review script initially miscounted the second CHANGELOG
sentence as ten words; it is nine. Correcting that review-script assertion
produced the passing receipt without changing any repository file.

Public check states are snapshots, so reproducing that read later can show
different job states. The immutable evidence index identifies five historical
executable receipts by both Git blob and SHA-256. It deliberately excludes
handoffs, private scratch material and other reviewers' packets. Those five
historical receipts do not prove the round-2 head by themselves.

`MANIFEST.sha256` covers the report, this guide, scripts and publishable
receipts. Validate from the packet directory with `sha256sum -c MANIFEST.sha256`.
Nothing under `scratch/` is publishable.
