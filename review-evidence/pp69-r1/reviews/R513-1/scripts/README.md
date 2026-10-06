Run from an exact detached checkout of cb730a2f9dd7e4f60a03a38d4b47b569e68da8df.
The scripts derive the packet location from their own path. Supply `--repo` and
`--verilator` as absolute paths. No shared installation is needed. The simulator
must identify as the required 5.050 version; a C++ compiler, Python, make, git,
the logic-statistics programs and the read-only public API client must already exist.

Run `run_focus.py --repo REPO --verilator SIMULATOR` first. It creates the exact-head
archive, scratch temporary directory and compiler-fanout wrapper needed by the other
execution scripts. Then run:

- `run_controls.py --verilator SIMULATOR`: only the 25 issue-69 mutation arms and five controls.
- `run_probes.py --repo REPO --verilator SIMULATOR`: reviewer-owned tuple model and top traffic probes; only disposable bench sources change.
- `run_base_suites.py --repo REPO --verilator SIMULATOR`: the two small shipping suites at the frozen base.
- `plant_audit.py --repo REPO`: static planting checks, no full campaign execution.
- `notify_stats.py --repo REPO`: only the touched notify module, count one, base/head.
- `check_checkout.py --repo REPO`: all tracked blobs, modes, index entries and gitlinks.
- `public_receipts.py`: verify the included public evidence hashes and refresh hosted job/step status using GET requests only. Hosted status is a point-in-time observation.

Each execution script waits for all of its child processes in the foreground.
The campaign driver has two concurrent campaigns, two workers per campaign, and
three compiler workers per build: at most 12 compiler workers. Do not overlap
separate execution scripts in a way that exceeds the 16-job or 12-GB review limit.
No physical build is part of reproduction.

Documentation check: from REPO, set TMPDIR to the packet's scratch/tmp and run
`make -j16 params ids figures links matrix modmatrix`, recording its log and exit code.
The Git metadata is required for IDs and figures; an archive alone is insufficient.
Diagram inspection used the committed docs/diagrams/21-integration-faces.svg rendered
to scratch/integration.png with the installed SVG renderer. The raster is disposable.

The packet includes raw logs and per-unit return-code files. A mutant's nonzero
simulation exit is expected; the campaign's verdict additionally requires its named
assertion failure and a completed tally. Static planting checks are not mutant kills.

`MANIFEST.sha256` lists publication paths relative to the packet root. Verify from
that root with `sha256sum -c MANIFEST.sha256`. The scratch directory is never published.
