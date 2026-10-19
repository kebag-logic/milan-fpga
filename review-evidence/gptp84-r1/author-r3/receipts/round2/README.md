# Round 2 receipts

Every file under this directory is listed, with its size and hash prefix, in
`../INDEX.md`, which is generated from the files present. Host paths are
replaced by placeholders (`<lane>`, `<lane-head>`, `<scratch>`,
`<parent-c-checkout>`, `<parent-head-snapshot>`, `<parent-base-snapshot>`,
`<parent-wt-NAME>` for the scratch parent worktrees, `<pinned-tools>`,
`<home>`, `<tmp>`, `<data>`, `<user>`, `<author>`).

| Directory | What ran | Revision |
|---|---|---|
| `lane-head-2022d363/` | every repository gate, engine mutation arm (24 slices) | head 2022d363 (final) |
| `lane-head-093b9c3b/` | the same, first run of the round | 093b9c3b (superseded; tallies identical) |
| `lane-images/` | the four ROM images regenerated and compared | 2022d363 |
| `lane-images-093b9c3b/` | the same | 093b9c3b |
| `d-vs-e.txt` | how gptp-processor 093b9c3b (snapshots B, D) differs from 2022d363 (E), and which parent files read gptp-processor tests | both |
| `snapshots.txt` | every local parent snapshot: subject, gitlink, diff from dev e9cbb676, submodules | parent |
| `parent-base-f3379118/` | milan_dp gptp, physical suite | parent base (gitlink 43acfbcc) |
| `parent-head-e347b8a0/` | milan_dp gptp, gptp-lat, physical suite, no companion | gitlink 093b9c3b |
| `parent-snapB-6814d01c/` | #85 mutants on the gptp leg; gptp_plane, gptp_tables, gptp_txts, tsn_fuzz | + shadow-85, milan_dp-85 |
| `parent-adoption-3f053cc1/` | snapshot D: all 11 consumer gates, builder legs and union, milan_dp gptp and gptp-lat, gm_steps, physical suite, gptp-leg mutants, physical-leg mutants | + all four companions, gitlink 093b9c3b |
| `parent-adoption-564466ea/` | snapshot E (the adoption): all 11 consumer gates, builder legs and union, milan_dp gptp and gptp-lat, gm_steps, physical suite | + all four companions, gitlink 2022d363 |
| `companions/apply-check.log` | the four patches applied in order to a clean dev e9cbb676 and compared with E's tests | dev e9cbb676 |
| `search/` | the whole-parent path-shape search and the suite inventory | dev e9cbb676 |
| `parent-consumer-template-copy.json` | verbatim copy of the manager's eleven consumer commands (the original file was removed from the host mid-round) | - |
| `../scripts/` | the scripts that drove these runs | - |

In each parent directory, `rc.txt` has one line per command with its return
code and seconds; `NN.log` is consumer gate NN of the template.
