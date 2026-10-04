# #232 area lane, round 2: evidence packet

Processor PR #153, head `2ea3dee2cd92e5907a8942a8c32436ab2f46ff2d` (milan-fpga #232
comment 5976892215). Every file's sha256 is in `MANIFEST.sha256`; no file is over 200 KB,
and raw run directories stay in the lane's scratch area. Each extract names its raw
source's full sha256.

| Directory | Item | What it holds |
|---|---|---|
| `vivado/` | 2 (R453-1 F1) | report extracts and whole small reports of the eight Vivado runs behind the lane's area and timing figures, with `tools/rederive.py` re-deriving every figure (`vivado/README.md`) |
| `lockstep/` | 1, 2 (R453-1 F2, last bullet) | the author's lockstep bench of rounds 1 and 1b, its control diffs, every run's summary line, and the corrected control table |
| `probes/` | 1 | the reviewers' 22 controls planted and probed with their own scripts at the round-2 head: 22 of 22 fail a named committed check |
