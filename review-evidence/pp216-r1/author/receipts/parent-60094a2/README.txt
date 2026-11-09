The scratch parent's consumer gates with protocol-processor pinned at 60094a2.

Parent: a clone of milan-fpga dev ac0a01e3 with two local commits, never pushed (push URL disabled):
5541fb5c31 (the protocol-processor gitlink at 60094a2) and 6705f8c216 (syn/yosys/rom_digests.tsv re-recorded by
syn/yosys/ooc.sh --record-rom-digests; parent-rom-digests-60094a2.log). parent-pin-60094a2.txt is the parent's log
and submodule status.

Each gate is <name>.cmd / .log / .rc / .start / .end / .python (the interpreter seen before and after, CI's CPython
3.12.3 venv of ci/constraints-ci.txt). The commands are the rtl-fast workflow's run steps plus milan_dp, with CI's
pinned Verilator 5.050, Yosys 0.66, sv2v v0.0.12 and GoogleTest 1.14.0, jobs 4, and the docs workflow's gates that
read the processor tree (docs ratchets, idiom gates).

Timeline: milan_dp, the firmware SRP campaigns (fw_shard3_srp), fw_verilator, fw_boundary, changes, lint, bdd,
yosys-elaboration and publication-census ran 08:47 to 10:24. The firmware-unit job (fw_tally_selftest to
fw_coverage) was running at the host reboot (10:34) and was re-run whole from 10:56; fw_shard1 (control
campaign), fw_shard2 (AECP campaign), the docs ratchets and the idiom gates ran after it, to 12:01.

milan_dp.log and behave.log are over 200 KB: RAW-RECORDS.txt has their size and sha256, and milan_dp-summary.txt and
behave-summary.txt their result lines.

Every .rc is 0 (40 gates).
