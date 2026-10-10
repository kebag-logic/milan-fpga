[A578] TAKEN
Branch: 608-b14-bench
Base: 5603c353137e90c1fa95429f6d00ef7a2298d9ee
Assignment: https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-6085135051
Reviewers: [R574] and [R575].
Scope: execute B14 items 1 through 8 in order, starting with identity. Record the switch repeats, disconnect cycles, starts, default maps, two-hour soak, Ethernet receive counters, MAAP observations and restore readbacks in the assigned findings page. Observe all STOP conditions.
Validation: docs_check.py, check_doc_style.py, gen_toc.py --check, check_em_dash.py --base 5603c353, check_doc_paths.py, check_baremetal_only.py, and git diff --check.
Blockers: none established; bench preconditions and identity pending.
