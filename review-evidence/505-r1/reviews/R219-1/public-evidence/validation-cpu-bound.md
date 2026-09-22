# Validation CPU bound correction

The gptp processor Makefiles use Verilator --build -j0, which reads available CPU affinity and can exceed MAKEFLAGS=-j8. Native407 validation originally had CPUs8-31, so those builds could see24 CPUs. No test failure or memory-limit breach was observed; results are not invalidated by this scheduling detail. The unit had completed before the live affinity correction; zero processes were changed. No source or gate command was changed.

The management launch-validation.py now caps requested affinity to its first8 CPUs. This bounds implicit nproc/-j0 commands as well as explicit MAKEFLAGS. The act invocation's requested0-3 remains unchanged, and its trusted runner already bounds its Docker jobs. Use this capped launcher for future native validation. Do not edit product Makefiles as part of this operational correction.
