The two-placement simulation of milan-fpga #665 (lane S6b, branch 665-s6b-cosim at a88772f1, read only: the lane was
not edited), run on a scratch copy of it with protocol-processor pinned at the head 84f6d6a and its ROM digests
re-recorded through syn/yosys/ooc.sh --record-rom-digests, committed locally (2492225f0d, 82622f3242; twin-pin-84f6d6a.txt),
never pushed (push URL disabled):

make -C tb/verilator/milan_dp twin

rc 2 (make; twin_compare.py exits 1): its 3 findings are exactly the three owed rows of this defect, each reporting
"the defect has gone" (twin-compare.txt): fabric-mvrp-leave-all (#857), fabric-domain-one-new and fabric-vid2-join-in
(#860). The other owed rows hold as [OWED] (stream-output-0-notices, split-talker-failed, entity-available-index for
#217), none of them this issue's. The record is identical to round 1's at 60094a2, frame counts included; the twin
does not bounce the link. twin.log is over 200 KB (RAW-RECORDS.txt: size and sha256); report.json is the compare's
own report.
