R931-1 receipts, exact head 166dfdc9fd2f22a9d2acd272bac4d1a5e3462f3e. $PACKET is this directory's parent; $REVIEWS its parent.
store-selftest.log/.rc        the store gate with --self-test --jobs 10 at five shapes, the cross-compiled size arm included
suite_probe-*.log             the same gate at the 1x1 and 8x8 shapes with two printing probes added (scripts/r931-store-probes.diff)
probe_store_tidy_and_inflight.txt, probe_rollback_then_forward.txt   those probes' output (F4, F2 context, F5)
mut-*.txt, mut8-*.txt         reviewer mutants, the unmodified suite at 1x1 and 8x8 (F3); kill-*.txt, kill_tests_on_head_1x1.txt the same with scripts/r931_kill_tests.py
r931-bind-flight-8x8-1if.txt  the save harness, BUDGET_FLASH_US=120000:500, scripts/r931-bind-flight.diff (F2)
split_target_commit_1x1.txt   the split-target commit case, base then head (F1)
boot_cost_8x8-1if.txt         boot with 0 and 16 frames in each slot (F9)
probe_bind_grade.txt          the bind grade over synthetic logs (F7)
window_backlog-adp_blank-0_8x8-1if.txt   one staged save window at this head (F6 context)
load_grade.txt, test_ctrl_memory.txt, clone_identity.txt
