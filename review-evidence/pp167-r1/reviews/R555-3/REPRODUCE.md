This packet reviews processor head `bcbf382e5f4d17ccfd8ae75a80bbc45902c75b7d`.
Run from a disposable review clone at that head. Set `PACKET` to this packet's
absolute path and `REPO` to the clone's absolute path. Required executables are
Python, Git, Make, the diagram renderer used by `make check`, and the pinned
5.050 compiler. `REVIEW_VERILATOR` can select the compiler executable at another
installation. Public API snapshots also require an authenticated read-only
GitHub CLI session.

```sh
python3 "$PACKET/scripts/prepare.py"
python3 "$PACKET/scripts/integrity.py" "$REPO" "$PACKET/receipts/source-before.json"
python3 "$PACKET/scripts/scope_audit.py" "$REPO"
python3 "$PACKET/scripts/validate.py" "$REPO"
python3 "$PACKET/scripts/audit_published.py"
python3 "$PACKET/scripts/integrity.py" "$REPO" "$PACKET/receipts/source-after.json"
```

The foreground validation driver joins all three independent tasks. It invokes
`make -j16`, limits each compiler build to four workers, and passes `--jobs 2`
to the focused campaign. Maximum concurrent compiler workers are twelve.
Only the notification unit suite and the two SC controls are compiled. The
documentation gate runs in the original clone; compiler builds and mutation
trees live under `scratch/`. No synthesis or parent bank is run.

`prepare.py` installs dependencies only under `scratch/venv`. The first
recorded preparation installed the version pinned by this script. The
validation driver's safe replacement of its own `scratch/unit` directory was
added after the recorded first execution to permit repetition; it does not
change the executed commands or tested inputs.

`fetch_evidence.py` fetches selected immutable public blobs using the included
tree inventory and verifies their Git object IDs. `audit_published.py` also
checks the publication manifest and original author index. The area receipt
was path-redacted on publication; its two hashes are reconciled through that
manifest. `hosted_snapshot.py` can refresh the mutable hosted job/step snapshot;
do not confuse a later observation with the recorded one.

`MANIFEST.sha256` enumerates publishable files with paths relative to the packet.
Verify it from this directory with `sha256sum -c MANIFEST.sha256`. `scratch/`
is excluded from publication.
