# Independent pass, written before reading any prior review finding
Head 1c8b485f5eebfa8efaba6f5facbade7e5aa4caaa.
Measured: head 888/888; base encoder 888: 810 PASS, 78 FAIL; 57/57 campaign checks on the srp_encoder arms; every README arm count reproduced.
Survivors of both tb/srp_encoder and tb/srp_top: x-busy-not-in-alloc, x-start-collect-term-dropped, x-start-laprepare-term-dropped.
PV20 comment says the offer is held only until taken; the head path holds it through the drain, which masks x-busy-not-in-alloc. With a drop-on-accept producer the head stays 888/888 and that arm fails 4 named PV20 checks.
PV19 comment says never held; probe: an unknown type waits on a full table and beside its own drain.
Preliminary verdict: depends on whether the behaviours above are inside A10 item 5 (R780-1-F2), to be settled from the finding text. Conformance CLEAN, RTL CLEAN (hdl unchanged), Robustness CLEAN, Tests provisional UNCLEAN, Docs CLEAN apart from residue.
