Run from the exact review checkout. Pass the packet directory explicitly.
The scripts make no tracked source edits.

```sh
rtk proxy python3 /path/to/packet/verify_figures.py .
rtk proxy python3 /path/to/packet/verify_tree.py .
rtk proxy python3 /path/to/packet/audit_prose.py .
```

For the documentation campaign, use a disposable environment under packet scratch.
Install the checkout's hash-locked `tools/markdown/requirements.txt` there.
The campaign also needs PyYAML, wavedrom 2.0.3.post3 and rsvg-convert.
Keep the three required public submodules initialized at their gitlinks.

```sh
rtk proxy /path/to/packet/scratch/venv/bin/python /path/to/packet/run_docs.py . /path/to/packet/docs-gates
```

The runner executes eight lightweight checks concurrently and waits for all.
Every command receives its own log and rc file.
Its JSON command inventory is `docs-gates/results.json`.
This is the focused reviewer campaign, not a full implementation bank.
The author receipt describes a separate 48-command campaign.

Verify the published packet from its root:

```sh
rtk proxy sha256sum -c MANIFEST.sha256
```

The manifest intentionally excludes scratch and unlisted acquisition intermediates.
Prose observations scan whole pages, including existing budget prose.
They are screening results, not individually adjudicated findings.
The report identifies the confirmed wording-only findings and exact fixes.
