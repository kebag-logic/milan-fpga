The scripts take the reviewed checkout as their first positional argument. Run them from a Python environment with the repository dependencies available. They write disposable outputs only beneath this packet's `scratch/` directory. That directory is excluded from publication.

Commands used, with `CHECKOUT` denoting the isolated reviewed clone and `PACKET` this directory:

```sh
python3 -B "$PACKET/run_checks.py" "$CHECKOUT"
python3 -B "$PACKET/collect_native.py" "$CHECKOUT"
python3 -B "$PACKET/probe_tidy.py" "$CHECKOUT"
python3 -B "$PACKET/probe_verify.py" "$CHECKOUT"
python3 -B "$PACKET/audit_public.py" "$CHECKOUT"
python3 -B "$PACKET/check_integrity.py" "$CHECKOUT"
```

`run_checks.py` starts independent campaigns concurrently and waits for their completion in the foreground. It requests 12 build/mutation jobs for the store campaign. The other two campaigns are serial internally. Its per-campaign limit is 1,800 seconds. The individual commands are recorded at the start of their logs. No shell job was detached.

`collect_native.py` collects explicit main-suite results from the five already-built, unmodified binaries in that campaign's disposable tree, with two execution workers and no new build. It records each binary hash. This separates the main-suite verdicts from a potentially incomplete mutation campaign. The original campaign's 12 workers, the serial grader self-test and these two workers remain within the limit of 16.

The initial memory command used the default Python environment and failed because `migen` was unavailable there (`memory.log`, exit 1). It was rerun with the existing project Python environment, `PYTHONDONTWRITEBYTECODE=1` and `TMPDIR="$PACKET/scratch"`:

```sh
"$PROJECT_PYTHON" -B "$CHECKOUT/sw/litex/test_ctrl_memory.py"
```

That run passed (published as `memory-project-env.public.log`, exit 0). No package was installed. The raw `memory-project-env.log` remains local and is not in the publication manifest: its single home-directory prefix is replaced with `$WORKSPACE_HOME` in the public copy. `memory-project-env.raw.sha256` records the original bytes' hash. No test result is changed by that redaction.

`probe_tidy.py` builds three additional assertions through the existing store test rig at each of two shapes. The unchanged production source is compiled in disposable trees. At each shape, the four changed-work assertions fail and the two empty-maintenance controls pass. The test binary exits 1; the reproduction driver exits 0 after recording both shapes. `tidy-probe.rc=0` means the reproduction driver completed, not that the store satisfied those assertions.

`probe_verify.py` exits 0 only when its controls and the reviewed grader counterexample reproduce. It exercises both the frame helper and full reconstruction with valid CRCs. Its exit status is not a positive durability verdict.

`audit_public.py` verifies all published author packet hashes against the packet's own manifest and enumerates the test and mutation registries. It reads the public evidence commit from local Git objects; it does not modify the checkout.

`check_integrity.py` hashes actual tracked blob bytes with Git blob framing, checks executable/symlink modes, compares every index entry with the exact commit tree, and checks the four required registered submodules at their pinned commits. Both initial and final logs are retained. It does not rely solely on `git status`, which can miss altered bytes under index flags.

The `.rc` files record process exit status. See REPORT.md for which checks completed and their interpretation. Only files enumerated in MANIFEST.sha256 and REPORT.md are intended for publication.

The full optional campaigns did not complete within the driver limit. Their .rc files are absent because the driver raised TimeoutExpired before writing them. campaign-status.txt records this explicitly; neither partial log is a passing verdict. The main-suite collection completed independently with exit 0.
