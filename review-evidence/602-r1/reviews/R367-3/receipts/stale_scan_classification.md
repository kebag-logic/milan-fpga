# R367-3 stale-claim scan classification, exact head 6b2ebd1c

Scan: `python3 stale_scan_r367_2.py <clone>` (the round-2 scanner, unchanged; raw hits in `stale_scan_hits.txt`).
Scope: every tracked text file except `docs/history/**` and the submodules.
Total: 197 hits in 26 files (185 in 26 files at `471892a9`).

## Change against round 2

Per-file hit counts changed only in files the round-3 commit edits:

| File | R367-2 | R367-3 | Reason |
|---|---:|---:|---|
| `docs/integration/BAREMETAL_FIRMWARE.md` | 6 | 5 | `:1469` and `:1471` rewritten; `:1468` no longer matches, because its +-2 window (`:1466-1470`) no longer holds a restart term after the `:1469` rewrite (the `:1468` line itself is unchanged and true) |
| `tb/verilator/milan_dp/gmstep_mutants.py` | 22 | 30 | the two delayed-adjtime controls and the docstring line |
| `tb/verilator/milan_dp/Makefile` | 6 | 7 | the `:20-21` wording now names "#602 PHC-only mr exclusions" |
| `tb/verilator/milan_dp/README.md` | 30 | 33 | the coincident-scope note (`:661-663`), the two delayed-control rows, the adjtime-window sentence |
| `tb/verilator/milan_dp/sim_gmstep.cpp` | 20 | 21 | the pending-merge comment at `:1098-1099` |

Every other file's hits are byte-identical in content to round 2 (no other file is touched by `471892a9..6b2ebd1c`), so the round-2 classification carries over.

## STALE (a current document states the superseded #387 PHC-step restart coupling)

None.

The two round-2 STALE rows are now correct:

| Location | Text at head | Enforced by |
|---|---|---|
| `docs/integration/BAREMETAL_FIRMWARE.md:1469` | "`media_rebase_p_w` has exactly two references: Its initializer and sole reader, `render_recentre_p_w`, under the #602 ruling" | `sw/builder/test_builder.py:10719` (`"media_rebase_p_w": 2`); `hdl/milan/milan_datapath.sv:3132` and `:6054` are the only two references |
| `docs/integration/BAREMETAL_FIRMWARE.md:1471` | "`mcr_restart_p_w` is exactly `crf_clk_selected_r & ((tkd_crflk_q_r & ~crf_locked_w) \| crf_mr_toggle_p_w)`: The #602 ruling excludes the PHC-step term" | `test_builder.py:10774-10780` (initializer pin), `:10720` (census 2), `:10786` (direct `restart_p_i`); `milan_datapath.sv:3133-3134,3163` |

## Current and correct (new or changed hits this round)

- `BAREMETAL_FIRMWARE.md:1468,1470,1522,1524`: unchanged and still true (censuses 5 and 3; render initializer; control summary).
- `GM_LOSS_RECOVERY.md:236-243`: five option-off controls, two of them delayed adjtime causes; matches `gmstep_mutants.py` `CONTROLS` (5 with `leg="option-off"`).
- `GM_LOSS_RECOVERY.md:156`: "A simultaneous PHC step neither adds nor suppresses those restarts" states the ruling's design rule (5859297355, third bullet), not a check name.
- `TESTING.md:273`: fifteen gmstep plus five option-off controls = the 20 entries of `CONTROLS`; five default.
- `milan_dp/README.md:661-663,684-686,711-733,985,1001`; `gmstep_mutants.py:23,62,199-225`; `sim_gmstep.cpp:1098-1099,1143`; `sim_main.cpp:109-110,1062-1065`; `Makefile:20-22`.

## Targeted phrase grep (outside `docs/history/**`)

`git grep -iE 'neither adds nor suppresses|PHC step toggles|toggles mr once|three references|\| media_rebase_p_w`|#387 mr checks|later counts require re-measurement|eighteen controls|three option-off'` returns only `GM_LOSS_RECOVERY.md:156` (the ruling's rule, above) and the legitimate source-change check name "a real source change toggles mr once" (`README.md:698`, `gmstep_mutants.py:137`, `sim_gmstep.cpp:837`).
