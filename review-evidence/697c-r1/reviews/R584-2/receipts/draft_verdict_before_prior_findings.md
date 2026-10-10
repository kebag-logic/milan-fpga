Draft written before reading R584-1 / R585-1 findings.
Verdict: NEGATIVE at 386b8e69e6f2fd0233e7a432e75c9d877c583a7b.
F1 MINOR (Conformance, Robustness, Tests, Docs): boundary judges image/shape-valued units only at IMAGE_SINKS=IMAGE_SOURCES=1u (ctrl_boundary.py:112), a value no builder compiles (2/2, 9/9); shape-value plant escapes (gate rc 0) while ctrl_image.py compiles it at both shapes. Docs claim every configuration (README:90, CI_WORKFLOWS:58).
F2 MINOR (Conformance, Robustness, Tests, Docs): tb/verilator/mbx/Makefile:112-118 run-if2 compiles host/mbx_model.c against the stack include/ without stack-pin; poisoned wire.h compiled with no refusal. Claims: Makefile:45, mbx README:17, ctrl README:103.
S1 SUGGESTION: two-token -D NAME not derived (no current builder).
Ledger draft: Conformance UNCLEAN (F1,F2); RTL CLEAN; Robustness UNCLEAN (F1,F2); Tests UNCLEAN (F1,F2); Docs UNCLEAN (F1,F2).
