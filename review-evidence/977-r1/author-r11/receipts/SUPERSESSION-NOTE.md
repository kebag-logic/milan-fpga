# Supersession and publication note for author-r11/receipts/INDEX.md (2026-11-28)

This note is published beside the round-11 receipts index and does not change it. That index and its receipts keep their bytes. The authority for each published file's hash is the published manifest (`MANIFEST.json`, `published_sha256`).

**Superseded wording.** The later packets (author-r12 and this round's) and the current PR body supersede round 11's text on two points:

- **The deliveries baseline.** It is now the ordinary passes after the delivery window, not the median ordinary pass before the record ([the manager's decision on #977's deferred deliveries](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7229657853)).
- **The 8x8/1if ceiling.** The ceiling asked of the owner is now 0.79, not 0.78.

**Compressed names and published paths.** The index lists these receipts as compressed files, but they were published uncompressed. Each is published under the same name without `.gz`, in the same directory. The sizes and hash prefixes in the index are those of the compressed files.

| Index row | Published path |
|---|---|
| `gates/fwgate-shard1-9976b94f.txt.gz` | `gates/fwgate-shard1-9976b94f.txt` |
| `gates/fwgate-shard2-9976b94f.txt.gz` | `gates/fwgate-shard2-9976b94f.txt` |
| `gates/fwgate-shard3-9976b94f.txt.gz` | `gates/fwgate-shard3-9976b94f.txt` |
| `gates/harness-run.py_--self-test-9976b94f.txt.gz` | `gates/harness-run.py_--self-test-9976b94f.txt` |
