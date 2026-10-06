Use an exact detached clone of `4dab80ae4564ef8d6e1030564dcea4ba19235ee6`, with the three required submodules initialized at their gitlinks. Set `REPO` to the clone and `PACKET` to this packet.

Prepare a disposable documentation environment under `scratch/`, using the repository's locked Markdown dependencies and YAML support. This review used system packages for already available YAML support.

```sh
python3 -m venv --system-site-packages "$PACKET/scratch/doc-env"
"$PACKET/scratch/doc-env/bin/python" -m pip install --require-hashes -r "$REPO/tools/markdown/requirements.txt"
python3 "$PACKET/scripts/audit_scope.py" "$REPO" "$PACKET/receipts/pr-approval.json"
python3 "$PACKET/scripts/check_prior_preservation.py" "$REPO"
python3 "$PACKET/scripts/verify_integrity.py" "$REPO"
"$PACKET/scratch/doc-env/bin/python" "$PACKET/scripts/run_focused.py" "$REPO"
```

The focused runner is one foreground process, joins all checks, permits four concurrent checks, and retains a separate log and exit file per command. Temporary files stay under `scratch/`. Run it in a working copy of the packet to preserve original receipt hashes.

The scope script recomputes the exact two-parent merge, measures the requested diffs, checks preservation and compares all 19 public approval entries. It may write disposable merge objects in the clone's object store but changes no ref, index or working file. Its published input contains the exact examined approval section and the hash of the full public body.

The integrity script hashes raw bytes directly, then checks modes, complete index entries, registered submodule ownership and gitlinks. The prior-preservation script checks the previously corrected artifacts and retained wording residue.

Primary standard identities and examined clauses are in `receipts/clause-sources.json`; licensed files and extractions are not published. Public evidence and hosted snapshots represent the observed states only.

From the packet directory, run `sha256sum -c MANIFEST.sha256`. Only listed files and REPORT.md are publishable. Never publish `scratch/`.
