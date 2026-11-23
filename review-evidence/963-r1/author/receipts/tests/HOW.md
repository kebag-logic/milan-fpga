# The cut's tests and plants

`failing-first-on-base.log`: the head's `test_aecp.cpp` built against the base's `aecp_maps.c`, `aecp_commands.c` and
`aecp_internal.h` (`dd163e41`), in the app arm and the work arm (`aecp_arms.core_arm`): both new or changed tests fail on
their own words. The `map-*` and `running-check-reads-whole` logs: each affected row of the AECP campaign's table planted
alone and graded by the campaign's own `caught()` rule (`some_plants.py` in `tools/`), all caught; the full campaign
is the firmware gate's shard 2/4 (`gates/firmware/fw-shard2.log`).
