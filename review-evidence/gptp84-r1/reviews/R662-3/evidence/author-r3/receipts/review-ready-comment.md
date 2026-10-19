[A655] REVIEW READY at head 53ac2e9d75ceb381c2d2b04854e760304d9ae43f (branch 84-85-tu-pathtrace, two commits on main 43acfbcc: #84 4d6288e8, #85 53ac2e9d; not pushed). Same head as the STOP; no source change was needed.

- Parent companion per the ruling: `parent-adoption-gptp_shadow-85.patch` updates seven lines of milan-fpga `tb/verilator/gptp_shadow/sim_main.cpp`. It has one row per expectation (:891 count 3->4, :930 count 1->2 plus a new check that tail0 is thisClock, :943 3->4, :1003 3->4), each citing IEEE 802.1AS-2020 10.3.9.23 / 10.3.13.2.4 f) 5). It rides the next gptp-processor pin adoption.
- Full parent consumer list on a committed local snapshot of dev e9cbb676 (gitlink 53ac2e9d plus the patch, local commit 28e1085f, not pushed): **11/11 rc 0**. gptp_shadow passes 310/310 and its mutation arm passes; the builder union covers 103 gates once with the same verdict digest as base.
- The new parent check fails under two planted mutants (thisClock not appended; the announcing source appended instead). The control passes 310/310.
- Repository gates: unchanged from the STOP, all rc 0 at base and head; engine mutation arm 72/72.
