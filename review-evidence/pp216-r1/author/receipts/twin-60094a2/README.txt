The two-placement simulation of milan-fpga #665 (lane S6b, branch 665-s6b-cosim at a88772f1), run on a scratch copy with protocol-processor pinned at 60094a2 and its ROM digests re-recorded through syn/yosys/ooc.sh --record-rom-digests, committed locally (b3117fc249, d90ab7a5ff), never pushed:

make -C tb/verilator/milan_dp twin

rc 2 (make; twin_compare.py exits 1): its 3 findings are exactly the three owed rows of this defect, each reporting the defect has gone:
[DIFF] owed row fabric-mvrp-leave-all: the defect has gone, the all-fabric half's grade finds none of it; the lane that fixed it (#857 (a release-image defect)) deletes the row
[DIFF] owed row fabric-domain-one-new: the defect has gone, the all-fabric half's grade finds none of it; the lane that fixed it (#860 (a release-image defect)) deletes the row
[DIFF] owed row fabric-vid2-join-in: the defect has gone, the all-fabric half's grade finds none of it; the lane that fixed it (#860 (a release-image defect)) deletes the row
twin: 3 finding(s); counts {'all-fabric': {'ACMP': 7, 'ADP': 12, 'AECP': 53, 'MAAP': 8, 'MSRP': 88, 'MVRP': 24}, 'split': {'ACMP': 7, 'ADP': 13, 'AECP': 49, 'MAAP': 8, 'MSRP': 91, 'MVRP': 92}}

The owed row entity-available-index (milan-fpga #858, processor #217) still holds ([OWED]); it is not this issue's. The three rows live in the #665 lane (read only here); they are deleted on the parent side with the adoption of this head.
