Local runs in a scratch copy of the lane while the change was developed (pinned Verilator 5.050,
default pp_top build). gsi1: the first GI step, whose coincidence case used a preceding STOP
on sink 1 to hold the notify block; it failed (two notifications per controller) because the
engine takes no command while a notification is pending. gsi2: the same with a frame-order
debug print. gsi3: the final GI step (GET_AVB_INFO hold), PASS. full1: every section of the
default build at the final code, PASS. acmp_listener and acmp_nvm: the two suites of the
changed listener and wrapper, PASS.
