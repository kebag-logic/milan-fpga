[A373] Enumeration evidence packet

Refs #117

The owner replaced Hive with headless la_avdecc enumeration on 2026-09-27. This packet records that replacement on the assigned `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5` image.

| Artifact | Purpose |
|---|---|
| expected-crc.txt | Assigned build artifact sizes, SHA-256 hashes and expected readback CRCs |
| identity-uart.txt | Read-only console VERSION and ROM/QSPI/AEM CRC readback |
| identity-aecp.jsonl | Raw ENTITY and CONFIGURATION responses; interface label substituted |
| identity-aecp-comparison.txt | Byte comparison against the assigned AEM templates |
| image-to-base-diff.txt | Product-image commit to lane-base diff, documentation/evidence only |
| link-selection.json | Live link/routing selection, interfaces represented by roles |
| run-N.log | Full library output from each independent 12 s process |
| run-N.entity.json | Entire DUT static/dynamic descriptor model, diagnostics and statistics |
| run-N.inventory.json | Every descriptor type and index derived from each model |
| enumeration-summary.txt | Per-run verdicts, counters, inventory and static-tree comparison |
| build-provenance.txt | Full compiler flags, library revision, linkage, hashes and sizes |
| final-uart.txt, cleanup.txt | Final status, transferred-file hashes, cleanup and free-lock check |
| redaction.json | Original and retained hashes for the interface-label substitution |
| gate-N.txt, gates.json | Exact final gate commands, physical working directory and return codes |
| VALIDATION-NOTES.md | Initial documentation/dependency and probe-build failures |
| tools/ | Small source files needed to reproduce the methods |

Recompute the inventory and stability result with `python3 tools/summarize.py`. Verify retained file hashes with `sha256sum -c MANIFEST.sha256` from this packet. Run the documentation gates with the pinned Markdown requirements installed outside this packet, using `python3 tools/run_gates.py`.

To repeat bench measurements, supply the current controller host and identify its live AVB interface from link/routing state, then confirm DUT AECP replies. Hold the bench lock for each action and use bounded foreground processes. Stage `enum_probe.cpp` and `avdecc_ro.py` in the temporary directory used by `tools/build_probe.py`. Execute that build recipe on the controller host, then `tools/enumerate_once.py <avb-interface> <1|2|3>` under the lock. Copy only the DUT JSON and logs after checking sizes and SHA-256, then remove the temporary directory. The recipe uses the existing library build and its own feature defines; binaries and dependency trees are intentionally absent from this packet.

Identity method: use `tools/expected_crc.py <assigned-build>` and compare the listed hashes to the public assignment. Under the lock, `tools/console_read.py <console> <transcript> milan_status mem_list 'crc 0x00000000 52216' 'crc 0x01000000 3825788' 'crc 0x01400000 7352'` performs read-only readback at 115200 baud. ENTITY and CONFIGURATION reads use `tools/avdecc_ro.py aem <avb-interface> 020000fffe000001 02:00:00:00:00:01 0x0004 0000000000000000 0x0004 0000000000010000`. Remove the four-byte configuration/reserved response prefix before comparing the 312 and 106 descriptor bytes to AEM image offsets 0x110 and 0x248. Both comparisons were exact.

No binds, CSR writes, flash, power, wiring or instrument operations were performed. The controller library performed its normal enumeration and unsolicited-registration lifecycle. The two library binaries, the probe binary and large build artifacts are represented by hashes and sizes, without retained copies.

Publication of this packet is for the coordinator. The documentation change has no push authorization.
