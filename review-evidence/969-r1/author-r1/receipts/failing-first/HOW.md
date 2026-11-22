# Failing first

The head's tests (`bd08d206`) built against the base's SRP adapter (`sw/firmware/ctrl/srp/srp_mbx.c` and `srp_mbx.h` checked out
from `dd163e41`), every other file at the head: `srp_mbx.cpp` at 1x1 and 8x8, one and two interfaces, and
`test_plat_sinks.cpp` (platsinks) at 8x8/1if and 1x1/1if. Each log is one arm of the firmware harness (`srp_arms.arm_srp`,
`plat_arms.arm_platsinks`). Every new case fails; the control order (binding first) and the ended-registration case pass.
