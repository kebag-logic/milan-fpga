Use a disposable exact-head checkout with its three required submodules initialized. Set REPO to that checkout and PACKET to this packet directory. No command below writes to GitHub.

```sh
(cd "$PACKET" && sha256sum -c MANIFEST.sha256)
python3 -m venv --system-site-packages "$PACKET/scratch/venv"
"$PACKET/scratch/venv/bin/python" -m pip install --no-cache-dir --require-hashes -r "$REPO/tools/markdown/requirements.txt"
python3 -B "$PACKET/scripts/verify_tree.py" "$REPO"
python3 -B "$PACKET/scripts/run_focused.py" "$REPO" "$PACKET" "$PACKET/scratch/venv/bin/python"
(cd "$REPO" && python3 -B tb/tools/avtp_wire_truth.py --self-test)
python3 -B "$PACKET/scripts/audit_public.py" "$REPO" "$PACKET"
python3 -B "$PACKET/scripts/verify_tree.py" "$REPO"
```

PyYAML 6.0.3 was available from the system environment. If absent, install it only into the packet environment with `"$PACKET/scratch/venv/bin/python" -m pip install PyYAML==6.0.3`.

The audit reads evidence commit `0010a410b0150c2c7043142fb64036a7d2655799` from Git and the captured public body in `receipts/pr-body.md`. Fetch that commit read-only if absent. The recorded final delta can be reproduced with `git diff --no-ext-diff --no-textconv 3880c1eb6e2f927a07f98150d5b05a228f8f4efd..3048222541ea6be725417ba0cd957607f0b821cb`.

The focused coordinator joins all children before returning, uses six concurrent slots, and bounds each command at 540 seconds. It records command, log and return code separately. It does not invoke any compiler, full bank, container or local workflow replica. Replay overwrites result receipts and durations; verify the publication manifest before replay, or use a separate output packet. The local standard is identified by hash in `receipts/standard-authority.json`; supply your authorized standards copy separately. No standards text or scratch directory is published.
