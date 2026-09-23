# Receipts: [A197], #74 item 2

Head `6d1572d6caeb94cd3dd871b9df90e4c5298998b6`, base `ede8d48ecd7c7f589a14b957951f040d92c99c70`. The tool is the pinned Verilator 5.050 wrapper, `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`.

| File | What it proves |
|---|---|
| `head-6d1572d6caeb94cd3dd871b9df90e4c5298998b6/media_grid_align.log` | Branch suite at head: 45/45. `MGA_MUT_U_SIGN` fails [G2], `MGA_MUT_NO_KEEPOFF` fails [G7] (5203 dups over 8 windows), `MGA_MUT_COIN` fails [G9] (11 dups for one slip) |
| `head-6d1572d6caeb94cd3dd871b9df90e4c5298998b6/chmap_capture.log` | 204/204, including the three new [T0] coincidence checks; netlist leg 20/20 |
| `head-6d1572d6caeb94cd3dd871b9df90e4c5298998b6/milan_dp-aclk-run.log` | Root true-ratio leg at head: 139/139 |
| `head-6d1572d6caeb94cd3dd871b9df90e4c5298998b6/aclk-base-vs-head.diff` | Empty: the aclk output is byte-identical to `base-milan_dp-aclk-run.log`, the same leg built with the two base RTL files |
| `head-6d1572d6caeb94cd3dd871b9df90e4c5298998b6/g0-g6-head.txt`, `g0-g6-base.txt`, `g0-g6-base-newharness.txt` | Existing arms G0-G6 print identical results at base (old harness and new harness) and at head |
| `head-6d1572d6caeb94cd3dd871b9df90e4c5298998b6/*.log` (gates) | `lint_rtl` 90<=90; `sv_idiom`, naming, port contracts, `cpp_idiom`, test evidence, hygiene, fail-fast, TODO, RTL source lists, feature status, doc paths, gPTP docs, solution docs and TOC anchors all exit 0 |
| `gates/em_dash.log`, `gates/gen_toc_check.log`, `gates/docs_check.log`, `gates/doc_style.log`, `gates/diff_check.log` | Docs gates on the committed head: em-dash 0 findings over 35 added lines in 4 pages; the others exit 0 |
| `gates/xvlog_gate.log` | xvlog analysis PASS: 0 findings in `hdl/`, 4 == ratchet in the pinned processors |
| `run_base_receipts.sh`, `base-mga-newharness.log`, `base-cmc-newharness.log` | The committed harnesses built against base RTL (`base_rtl/`, from `git show ede8d48e`). `media_grid_align` fails 13/45 (G7 windows {0,0,771,2351,2431,1980,1694,1701} dups; G8 2278 dups at lock; G9 10 dups, and 0 skips with 9 dups). `chmap_capture` fails 3/204 (exactly the new checks) |
| `base-media_grid_align.log` | The base suite as it stood (25/25) before any edit, for timing and population |
| `branch-*.log` | Intermediate branch runs, superseded by `head-6d1572d6caeb94cd3dd871b9df90e4c5298998b6/` |
| `../scratch/explore/free12-base.log`, `free12-fix.log` | 12 s free-running A/B. Base: 74 dups / 0 skips, and 65 dups / 0 skips. With the coincidence fix: 7 dups, and 7 skips, one per 1.9582 s |
| `../scratch/mga/j-{base,fix,both}-run.log` | Jitter A/B used for the DECISION. Fix alone chatters 994/994 at a raced lock; both halves are clean. The later G8 engage failure in `j-both` was a harness jitter-leak bug, fixed in the committed harness |
