[A418] STOP

Head: `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`, branch `131-d3-core-scalars`, unchanged. No implementation commits. This is the assignment's fixed-contract conflict STOP, not a completed-prefix handoff.

[DR2c-carrier item 3](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5863247772) and D3 section 6.3 say a failed, never-ACKed slot leaves the producer record un-ACKed. D3 section 7.1 instead explicitly retires producer pending at the earlier successful whole-record window WRITE, transferring unsaved work to backend dirty. The binding producer clears dirty on port done (`hdl/acmp/KL_acmp_nvm_shadow.sv:568,612`); the parent backend's device done precedes slot ACK (`hdl/milan/KL_nvm_backend.sv:973,1023,1052` at parent `7a7582f0`). No slot-failure feedback reaches that producer.

At a synthetic 10 kHz clock, a standalone composition of the unchanged producer, arbiter, port and parent backend records window done at cycle 179 and producer retirement at 180. Three later attested transaction failures with no slot ACK retain backend dirty/stale while producer pending/alarm stay clear. The literal producer-retention assertion fails exactly once; withholding window completion keeps producer pending. This does not claim every firmware failure must raise an alarm. It identifies an owner/completion-domain conflict that requires clarification before implementing the fixed wording.

All six implementation groups remain: ownership/AECP hold; scalar records/triggers; both passes/combined restore; rollback/debt; DR2c for both producers; section 15.2 amendments/sweep reconciliation. No DR3a ratification or DR4 area result is claimed, and there is no parent-visible change or pin to adopt.

Baseline: all 33 processor suites pass (1,015,815 checks, zero failures), and all full processor entry points have final rc 0 results, including 56 rejected SRP mutations and the 46-build NVM figure check. Parent backend tests pass at both shapes. Parent xvlog/evidence/C++/Python gates return rc 2 because the supplied pinned gPTP population is uninitialized; these remain unmet gates. No gate was weakened.

The `pp131-a418` packet contains HANDOFF.md, PR-BODY.md, all 37 section 15.2 row statuses, the reproduction and controls, receipts, and artifact hashes. Required resolution: identify which owner retains failed-slot work and whether slot-to-producer retry feedback is intended.
