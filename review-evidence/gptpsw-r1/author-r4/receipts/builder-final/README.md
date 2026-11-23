# Full builder suite at 8267b8951616cfd570baf690835d4b0d38f14596

The whole inventory ran with --require-rv32 and --require-elaboration, rc=0. The two reviewed failing assertions, gates 1c and 1d, pass.

Two arms remain explicitly NOT RUN: the MAKEFLAGS += -e plant has no effect with this make, and gate 11 needs a calibration build report absent from this host. They are not counted as passes. The same exceptions were recorded in the earlier complete run.
The driver receipt and full sanitized log are included.
