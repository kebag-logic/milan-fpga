Copied factual benchmark instrumentation from the interrupted A173 artifacts. No preliminary measurements are accepted as final evidence. Originals remain untouched.

fc2a142b7a98bebaf0604c132f3978e706011db8d84a4efbd3ccdeee6322f364  $WORKSPACE_HOME/milan-fpga-management/2026-09-22/517-author/bench/observe.py
74fb0da98f922e6f40db0ebefb4b0aa9f01bb4e9c8d2b9a1b7151235642fe062  $WORKSPACE_HOME/milan-fpga-management/2026-09-22/517-author/bench/analyze.py

A178 copied the A176 bench directory into 517-author-final. The A176 files remain unchanged. A178 extended run_suite.py to preserve all three tracked-header byte copies, check their committed identity, and hash the installed driver/binary on every run; compare.py checks those inputs and tool identities. failure_controls.py adds a planted removal of group exclusion. No old preliminary timing is used as an accepted measurement.

A178 also extended analyze.py to report sampled exclusive-group concurrency and samples where independent work overlaps the group. These observations remain telemetry, not added tests.
