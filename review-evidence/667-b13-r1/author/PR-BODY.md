[A549]

Refs #667.

Records B13 measurements on dev `28f9666f`, seed `asl`. The two-hour bidirectional AAF/CRF soak completed 145 checkpoints without an assigned error-class increase. Among 100 two-second talker starts, 14 recorded EARLY=1 and backward first-to-second timestamp steps of -544,469,385 to -279,759,747 ns; LATE remained zero. The other 86 steps were 124,999 to 125,020 ns.

The findings include every cycle, all 61 supported counter start/end/delta values, the ENTITY NOT_SUPPORTED result, B12 comparison, clause references and restoration evidence. All saved effective state and console readbacks match. Both sessions deregistered, all measurement processes exited, and the lock is free.

Validation at `afa4e687234b80e9474aa6dd0dc756de16a241bd`: docs_check.py, check_doc_style.py, gen_toc.py --check, check_em_dash.py --base 423ac5d9, check_doc_paths.py, check_baremetal_only.py --check, and git diff --check all returned zero. Offline decoder and restore controls: 22 passed.

Limits: absolute gPTP correlation was NOT RUN. Nine segment-local soak gaps were fully recovered in overlapping captures. One soak capture receipt omitted its drop statistic. NVM bookkeeping advanced by three successful commits with no failures.
