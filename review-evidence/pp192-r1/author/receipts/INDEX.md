# Receipts index

Generated from the files present under `receipts/` (size in bytes, sha256), one index
file per top-level directory under `index/`.
Host paths in the logs are masked: `<scratch>` (the lane's scratch root), `<lane>` (the
lane tree), `<toolroot>` (the pinned tool image), `<management>`, `<home>`, `<data>`,
`<vivado-lock>` (the host-wide Vivado lock file).
A file over 200 KB after masking is not copied; `OVER-200KB.sha256` lists its sha256,
size and path, and `<file>.excerpt.txt` beside it keeps its FAIL, tally and verdict
lines. Campaign units' source-tree copies and build directories are not copied.
2462 files.

| Directory | Files | Bytes | Index |
|---|---|---|---|
| `./` | 1 | 2953 | `index/top.md` |
| `base/` | 991 | 13950430 | `index/base.md` |
| `compare/` | 79 | 538814 | `index/compare.md` |
| `cut-by-reset-1/` | 17 | 24794 | `index/cut-by-reset-1.md` |
| `cut-by-reset-2/` | 9 | 19216 | `index/cut-by-reset-2.md` |
| `dev/` | 19 | 32052 | `index/dev.md` |
| `head/` | 842 | 11323804 | `index/head.md` |
| `head-42c6a5e/` | 189 | 2743287 | `index/head-42c6a5e.md` |
| `head-6127c6b/` | 57 | 1210019 | `index/head-6127c6b.md` |
| `host-memory/` | 2 | 51574 | `index/host-memory.md` |
| `killed-restarted/` | 9 | 86501 | `index/killed-restarted.md` |
| `parent-base/` | 68 | 386270 | `index/parent-base.md` |
| `parent-chain/` | 1 | 2221 | `index/parent-chain.md` |
| `parent-head/` | 62 | 384456 | `index/parent-head.md` |
| `parent-head-adopt/` | 61 | 384081 | `index/parent-head-adopt.md` |
| `pre/` | 6 | 4024 | `index/pre.md` |
| `scripts/` | 25 | 26325 | `index/scripts.md` |
| `stopped-6127c6b/` | 24 | 71244 | `index/stopped-6127c6b.md` |
