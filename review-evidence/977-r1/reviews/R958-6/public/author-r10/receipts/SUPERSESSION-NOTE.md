# Supersession and publication note for author-r10/receipts/INDEX.md (2026-11-28)

This note is published beside the round-10 receipts index and does not change it. That index and its receipts keep their bytes. The authority for each published file's hash is the published manifest (`MANIFEST.json`, `published_sha256`).

**Superseded wording.** Round 11's packet (author-r11) and the current PR body supersede four pieces of round 10's text:

- **The 80 ms figure.** "Pending" or "behind the owner's answer" for THE TRANSMIT's 80 ms at 8x8/1if is superseded: [the owner approved it on 2026-11-27](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7217388999).
- **The reviewers.** The reviewer placeholders are superseded: the internal reviewer is `[R957]` and the external reviewer is `[R958]`.
- **The run counts.** "All exit 0" is superseded. Each point's 289 runs are 285 that exit 0, plus 4 single srp-kept and srp-bound runs that `kept_grade`'s pairing refuses alone and that pass as the 2 pairs.
- **The lwSRP restore arm.** "Which no image builds" (the PR body's Pins row) is superseded: the `LWSRP_LEAN_COPY` 0 restore arm is used by the default-option shapes, and the published ELF comparisons cover those images too.

**Compressed names and published paths.** The index lists these receipts as compressed files, but they were published uncompressed. Each is published under the same name without `.gz`, in the same directory. The sizes and hash prefixes in the index are those of the compressed files.

| Index row | Published path |
|---|---|
| `r10d/gates/fwgate-shard1-8765bfd5.txt.gz` | `r10d/gates/fwgate-shard1-8765bfd5.txt` |
| `r10d/gates/fwgate-shard2-8765bfd5.txt.gz` | `r10d/gates/fwgate-shard2-8765bfd5.txt` |
| `r10d/gates/fwgate-shard3-8765bfd5.txt.gz` | `r10d/gates/fwgate-shard3-8765bfd5.txt` |
| `r10d/gates/harness-run.py_--self-test-8765bfd5.txt.gz` | `r10d/gates/harness-run.py_--self-test-8765bfd5.txt` |
| `r10d/gates/final/fwgate-shard1-25ff0632.txt.gz` | `r10d/gates/final/fwgate-shard1-25ff0632.txt` |
| `r10d/gates/final/fwgate-shard2-25ff0632.txt.gz` | `r10d/gates/final/fwgate-shard2-25ff0632.txt` |
| `r10d/gates/final/fwgate-shard3-25ff0632.txt.gz` | `r10d/gates/final/fwgate-shard3-25ff0632.txt` |
| `r10d/gates/final/harness-run.py_--self-test-25ff0632.txt.gz` | `r10d/gates/final/harness-run.py_--self-test-25ff0632.txt` |
