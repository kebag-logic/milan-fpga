# Offline reproduction

The scripts take paths as arguments and use only the standard library.
They perform no bench access and no GitHub writes.
Use the exact source head and pinned public archives below.
Place extracted archives and generated files under `scratch/`.

Source head: `18b98bbcecf478b903610a07667f232d944d6feb`.

Evidence archive: commit `2c4ca68a1d0b63651942ce2510f4fa5d19e944ab`, subtree `review-evidence/117-b19-r1`.

Image provenance archive: commit `bbc53aabb02a1654812ba2eaa1642f5e36e69ce0`, subtree `review-evidence/645-b18-r1/manager-provenance`.

Set `SOURCE_ROOT` to the exact source checkout, `PACKET_ROOT` to the extracted evidence subtree, `PROVENANCE_ROOT` to the extracted provenance subtree, and `OUTPUT_ROOT` to this report directory. Use quoted absolute paths.

```sh
python3 scripts/audit_packet.py "$PACKET_ROOT" "$SOURCE_ROOT"
python3 scripts/run_checks.py "$SOURCE_ROOT" "$PACKET_ROOT" "$OUTPUT_ROOT"
python3 scripts/check_support.py "$PACKET_ROOT" "$PROVENANCE_ROOT" "$OUTPUT_ROOT"
```

All three completed with exit status zero in this review. The first script intentionally reports the frozen packet's discrepancies: zero means the receipt audit completed, not that the PR passed review. It expects four mismatched first-assertion times at this evidence pin. The second reproduces the two summary artifacts in disposable scratch, runs four independent focused checks concurrently, and verifies source bytes, modes, index and gitlinks. It creates no source build. The third replays identity and census checks, rejects planted CRC mismatches, compares probe result lines, and checks image-provenance consistency.

Raw captures absent from the archive are not regenerated or claimed inspected. The public manifest's published hashes, rather than the original hashes of scrubbed files, authenticate downloaded bytes. Full capture replay requires a further public-safe raw-evidence provision.

`receipts/prior-findings.txt` records the read-only public reconciliation after the independent verdict and ledger were written. It records counts and notice links without copying another review.

Only files listed in `MANIFEST.sha256` and `REPORT.md` are publishable. The `scratch/` directory is excluded.
