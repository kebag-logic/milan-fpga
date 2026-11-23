Run from an isolated checkout at `8267b8951616cfd570baf690835d4b0d38f14596`.
The packet directory is the directory containing these scripts. Requires the native C/C++ compilers, installed test libraries, Python and Git. No installation or broad bank run is performed.

All disposable files must remain under the packet's `scratch/` directory. The scripts derive that directory from their own location. Run these foreground commands, substituting the packet and checkout paths:

```sh
python3 -B <packet>/run_multi.py <checkout>
<packet>/scratch/multi
python3 -B <packet>/probe_delta.py <checkout>
python3 -B <packet>/probe_owner_gate.py <checkout>
python3 -B sw/firmware/ctrl/test/ctrl_hot.py --self-test
python3 -B <packet>/verify_checkout.py <checkout>
```

`probe_delta.py` runs three independent builds concurrently and waits for all of them. Each negative control must exit 1 with a test assertion; the driver itself succeeds only when all are rejected. It does not edit source files. `probe_owner_gate.py` substitutes reads of the SoC source in memory and runs gate 1c, not the builder bank.

For `audit_packet.py`, first fetch evidence commit `98bc6f22bc3c42bd78c1585b6e3bdca2018d25f1` from the public repository. Extract only `review-evidence/gptpsw-r1/author-r4` and `review-evidence/gptpsw-r1/MANIFEST.json` with `git archive` under `<packet>/scratch/`. Then run:

```sh
python3 -B <packet>/audit_packet.py <checkout>
```

This hashes the published author packet, checks source-input equivalence, reruns the egress checker against both published 8x8/1if result directories, and compares the hot-list order and memory identities. It does not rerun the original service campaigns. `published-spotchecks.txt` contains selected lines from the pinned publication; their full files remain accessible at the source link in REPORT.md. Standards are identified by hashes, with no standards text distributed.

The report's raw receipts are the `.log`, `.rc`, `.txt`, and hash files listed in MANIFEST.sha256. Scratch is excluded from publication.
