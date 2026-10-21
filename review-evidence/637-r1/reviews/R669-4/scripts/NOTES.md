# Probe recipe (R669-4)

All probes ran in disposable copies of the review clone at exact head
`4ff3642e8fe9a0bd48d28374350390cde553bc32`, never in the clone itself. The
Verilator used is the pinned 5.050 (`verilator --version`: "Verilator 5.050
2026-07-01 rev v5.050"), passed as `VERILATOR_PIN`.

| Run | Copy state | Command | Receipt |
|---|---|---|---|
| head | exact head | `probe.sh <copy> head <logdir> dynmap` | `receipts/probes/head.*` |
| headmp8, headmp4 | exact head | `probe.sh <copy> headmp8 <logdir> maprec8`, and `maprec4` | `receipts/probes/headmp8.*`, `headmp4.*` |
| dev78ca9bdf | `git checkout --detach 78ca9bdf` (the merge's dev parent) | `probe.sh <copy> dev78ca9bdf <logdir> dynmap` | `receipts/probes/dev78ca9bdf.*` |
| mut762wire | exact head, `receipts/probes/cC-mutant.diff` applied (the #762 `stopped_i` at `milan_datapath.sv:7300` tied to `'0`) | `probe.sh <copy> mut762wire <logdir> dynmap` | `receipts/probes/mut762wire.*` |
| mutrestore | exact head, `receipts/probes/cD-mutant.diff` applied (campaign row 15's plant: the restore refuses every framed record) | `probe.sh <copy> mutrestore <logdir> dynmap` | `receipts/probes/mutrestore.*` |
| testmerge59740e3c | `git read-tree -u --reset 803f7b24` over a head copy: the tree `git merge-tree --write-tree 4ff3642e8 59740e3c` writes (live dev) | `probe.sh <copy> testmerge59740e3c <logdir> dynmap` | `receipts/probes/testmerge59740e3c.*` (the identity's HEAD line is the copy's HEAD; see its NOTE) |

Each leg log is tallied by section with `python3 -I sections.py <log>`
(preamble, `[DYNMAP]`, the `[762-DP]` shipping-geometry case, `[MAPREC]`).
`table_vs_verdicts.py` compares the milan_dp README campaign table with the
published campaign verdicts. Host paths in the logs are replaced by
`<verilator-root>`, `<tools>`, `<scratch>`, `<packet>` and `<clone>`.
