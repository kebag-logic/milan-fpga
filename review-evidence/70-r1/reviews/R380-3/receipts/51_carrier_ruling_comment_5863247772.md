[A10] Ruling on the DR2c carrier ([R381-2](https://github.com/kebag-logic/milan-fpga/pull/610#issuecomment-5863242490) F2). This clarifies [DR2c](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5862405632); the retry counts and spacing are unchanged.

**DR2c-carrier.**
1. "The alarm" in DR2c is the port's `nvm_alarm` from FASTCONNECT §9.2. It is the only reset-sticky alarm, and no new status bit is added.
2. Firmware transaction exhaustion (3 attempts, 1,000 ms apart) has no alarm of its own. It shows in two ways:
   - as the §9.2 `VD_*` verdict loss, so `nvm_stale` is 1;
   - as the failed slot never being ACKed.
3. A failed slot that is never ACKed leaves the producer record un-ACKed. If that exhausts the producer's record attempts (3, 500 ms apart), `nvm_alarm` rises and stays until reset.
4. A later successful commit clears `nvm_stale` exactly as §9.2 and the unchanged Recovery acceptance line require. It never clears `nvm_alarm`.
5. The lane-2 negative control targets `nvm_alarm`. The killed mutant clears `nvm_alarm` on a heartbeat or a later success. Clearing `nvm_stale` after a later successful commit is required behaviour, not a mutant.
6. SAVED_STATE_MATERIALIZATION, SNAPSHOT_OWNERSHIP and BAREMETAL_FIRMWARE state this with a §9.2 cross-reference. FASTCONNECT §9.2 names firmware exhaustion as a verdict loss.

Round 3 of PR #610 (R381-2 F1 and this ruling) will be assigned after the host restart, together with R380-2.
