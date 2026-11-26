# what each receipt is (gptp113: FPGA-gPTP issue 113, branch 113-runner-ratchets, head af11b3ef631eb44cdc1730cfb31bedda95c33dc5)
# consumer probe: milan-fpga dev-soft-core c34e7d8b06 + local commit f791fdea1f moving the gptp-processor gitlink (never pushed)
idiom-base.log / evidence-base.log            consumer ratchets at dev-soft-core's own pin 1213ac5b (both rc 0)
idiom-3009.log / evidence-3009.log            consumer ratchets with the gitlink at 3009f9a2 (PR 112's merge): both rc 1, the issue's findings
idiom-af11b3e.log / evidence-af11b3e.log      the same with the gitlink staged at af11b3e (both rc 0)
consumer-ratchets-af11b3e.log                 the same at the committed probe f791fdea1f, clean tree, budgets diffed against dev-soft-core (unchanged)
*-selftest-af11b3e.log                        both ratchets' --selftest (54/54, 105/105)
clock-sites-3009.log                          passes_test.py lines that the consumer's wall-clock rule matches (its own regexes, tools/clock_sites.py)
ast-pass_run.log                              pass_run.py at 3009f9a2 and af11b3e: the same program once docstrings are removed (tools/ast_same.py)
donor-idiom-fix.patch.checked                 the pin lane's patch, as checked (applies to 3009f9a2; its stdout removal is behaviour-neutral; its closure renames were replaced by docstrings)
passes-test-r1.log / make-*-r1.log            first runs on the working tree that became af11b3e (before its commit); system Verilator 5.054 for lint
head-gates/                                   at the committed head af11b3e, clean tree, Verilator 5.050: make docs, contract, lint; passes-test twice (one under ulimit -c 0)
plants-r1.log                                 PR 112's 13 planted defects, each at the old layout (3009f9a2) and the new one (af11b3e), plus a control per layout (tools/plants.py, 3 at a time)
engine/                                       make -j4 -C tb/verilator/engine run: 3009f9a2 vs af11b3e, clean and with a scratch-only planted abort at pass 1's start (tools/engine_arm.sh); compare.txt, pass-records.txt
branch/                                       the two commits as patches
