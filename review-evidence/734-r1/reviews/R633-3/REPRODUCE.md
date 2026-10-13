The packet's scripts accept a full-history checkout at the report's exact head. Required processor and stream-primitive submodules must already be initialized at their recorded pins. Historical B16 objects must be present. The host needs an unprivileged namespace launcher and `/usr/bin/python3` with PyYAML. No candidate runner is imported or executed on the host.

Run from the packet directory, setting `candidate` to the isolated source checkout. Each boundary binds the candidate read-only at `/candidate`, the packet read-only at `/packet`, and one disposable directory below `scratch/` at `/work`. It removes ambient environment and unshares the network/process/filesystem boundary. Use a fresh `--work-name` when repeating a probe; old scratch trees are evidence of earlier attempts.

```sh
python3 run_boundary.py --work-name repeat-scope "$candidate" repeat-scope python3 scripts/ci_scope.py --selftest
python3 run_boundary.py --work-name repeat-events "$candidate" repeat-events bash -euc 'python3 scripts/ci_events.py --check; python3 scripts/ci_events.py --selftest'
python3 run_boundary.py --work-name repeat-runner "$candidate" repeat-runner bash -euc 'install -m 0555 /candidate/scripts/act_ci.py /work/install/act_ci.py; python3 -I /work/install/act_ci.py --selftest --worktree /candidate'
python3 run_boundary.py --work-name repeat-ordinary "$candidate" repeat-ordinary python3 scripts/act_ci.py --selftest
python3 run_boundary.py --work-name repeat-independent "$candidate" repeat-independent python3 /packet/independent_scope.py
python3 run_boundary.py --work-name repeat-round1 "$candidate" repeat-round1 python3 /packet/recheck_prior.py round1
python3 run_boundary.py --work-name repeat-round2 "$candidate" repeat-round2 python3 /packet/recheck_prior.py round2
python3 run_boundary.py --work-name repeat-rename "$candidate" repeat-rename python3 /packet/recheck_prior.py rename
python3 run_boundary.py --work-name repeat-external "$candidate" repeat-external python3 /packet/prior-probes/scope_audit.py /candidate /work/probe
python3 run_boundary.py --work-name repeat-environment "$candidate" repeat-environment python3 /packet/environment_probe.py
python3 integrity.py "$candidate"
```

The unchanged round-2 script intentionally has an obsolete identical-edit oracle. `recheck_prior.py` records its three mismatches before independently grading its unchanged functions under the round-3 equality contract. The unchanged rename demonstration likewise hardcodes the former formula. See REPORT.md for the exact interpretation; raw exit status alone is not the current-head verdict.

Each gate log begins with the exact executed command and ends with its status and elapsed time. `focused-docs.log` and `doc-format.log` record documentation commands. The latter used an isolated copy of a renderer environment satisfying `tools/markdown/requirements.txt`; install that hash-locked dependency set into scratch for reproduction. No shared environment is modified.

For image reproduction, put the pinned SDK archive under the chosen scratch work directory as `sdk.tar.xz`. Authenticate/install it with the command in `image-readonly-setup.log`; the digest and installer are in `scripts/ci_rv32_sdk.py`. Use the disposable clone and local pinned-submodule initialization command recorded in `images.log`, followed by its five-shape `ctrl_image.py --base a0f39ad4...` invocation. The scratch clone must be writable because the builder emits generated configuration files. Run the 33 audit controls using `image-controls.log`'s command and the same scratch workspace. Compare all linked files with:

```sh
python3 compare_images.py scratch/images/build
```

The report distinguishes this pinned-archive build from the author's different compiler build. Five base/head pairs must be byte-identical; reproduction of the author's absolute hashes is not asserted.

`MANIFEST.sha256` lists only publishable files, with paths relative to this directory. `scratch/` is never published. Verify the packet with `sha256sum -c MANIFEST.sha256`.
