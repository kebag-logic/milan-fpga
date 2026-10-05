# Reproduce the focused review

Use a disposable clone detached at `7124bde172a523179a2788dca825587aa5a2a1e6`. Its tree must be `6009d72c1ee277ec12e287926b371000be555fba`. Keep all clones, temporary files, environments and generated output below the packet's `scratch/` directory. Never apply probes to the source checkout being reviewed.

Prerequisites: Python, Git, Make, a C++ compiler, the scoped 5.050 compiler, a working diagram CLI 11.16.0, its browser dependency, the two font families named by the receipts, and the Python waveform package `wavedrom==2.0.3.post3`. Create a virtual environment at `scratch/venv`; use that interpreter for the renderer probe. The raw setup commands are in `receipts/setup.log`. No shared installation is needed.

The scripts accept explicit source and scratch paths. `run_logged.py` takes `--packet`, `--cwd`, `--name`, then `--` and the foreground command. It records a log, return code and elapsed seconds and directs temporary output to scratch. Invoke independent runs in concurrent foreground sessions. All child processes must finish before the session ends.

- `integrity.py --source CLONE`: requested commit/tree, all 556 tracked blob bytes and modes, index tree, worktree status and gitlinks.
- `source_audit.py --source CLONE`: integration lineage, comment-only C11 changes, retained round-3 blobs, exact historical prose/waveform provenance, RX waveform signals.
- `make -j16 check` from the disposable clone: all nine documentation gates and both built-in self-tests.
- `id_probes.py --source CLONE --scratch SCRATCH`: 111 independent fixtures and three weakened-scanner controls.
- `render_probe.py --source RENDER_COPY`: margin geometry and malformed-margin controls. RENDER_COPY is a separate scratch copy of `docs/` and `scripts/`, because this probe temporarily removes source margins before restoring the original bytes. Do not overlap it with freshness checks in the same copy.
- `node text_fit.mjs CLONE SCRATCH OUTPUT_JSON CLI_PACKAGE_JSON`: current TX/host text bounds and older-export clipping controls. The final argument is the installed diagram CLI's absolute `package.json` path, used to locate its browser dependency. Append `fig-02-rxwave` for the supplemental RX measurements. Screenshots stay in scratch.
- `make -j16 VERILATOR=PATH_TO/limited_compiler.py` from `tb/side_port` and `tb/aecp_notify`: the two focused unit suites. The wrapper caps each compilation at four workers; `REVIEW_COMPILER` can select another verified installation of the identical compiler release. Run at most three such builds together.
- `python3 tb/pp_top/notify_mutants.py --output RECEIPT_DIR --verilator PATH_TO/limited_compiler.py --jobs 3 --only counter_spacing_from_selection_tw counter_stamp_at_send_only counter_stamp_first_job_only`: one unit-suite golden and three focused notification controls. It does not run the processor-top suite.
- `reconcile_probes.py --source CLONE --scratch SCRATCH`: exact prior ID reproducers through the checker and make target, figure self-test mutants, and optional parser-coverage observations. This temporarily creates one file in the disposable clone and removes it in a finally block. Run it after the independent pass has been sealed and do not overlap with an ID gate in that clone.
- Repeat `integrity.py` for both the original and disposable source clones after probes.

The original independent-verdict receipt is immutable. Its SHA-256 and the later review-comment intake timestamp are in `receipts/independence.json`. These establish review order; a rerun of the tests does not create a new independent review.

`MANIFEST.sha256` lists the publishable files using packet-relative paths. Validate it from the packet root with `sha256sum -c MANIFEST.sha256`. Scratch contents and unlisted imported source material are not published.
