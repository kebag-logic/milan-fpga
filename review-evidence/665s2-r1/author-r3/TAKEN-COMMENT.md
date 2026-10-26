[A681c] TAKEN
Branch: `665-s2-cpu-budget` (PR #792, round 3 on `cd3525c3`; base `dev-soft-core` `e76a755a`)
Authoritative references: round-3 assignment issuecomment-6420330377; R703-2 (PR #792 issuecomment-6420323457) and R704-2 (issuecomment-6419144949); `FR_NFR.md` 3.4.1 and H-NOTIFY; `MAILBOX_SPLIT.md:495-502`, `:645-657`, `:753-758`; `mailbox.yaml`; `KL_mbx_rx.sv`; `srp_mbx.c:441-451`; `aecp.c` (registrations, `transmit`).
Interpreted scope: changes stay under `tb/verilator/ctrl_service_budget/`, and the testbench and firmware are unchanged, so round 2's attested builds stay valid.
- (1) Every loaded channel's first and last record in a composed window is graded from its commit to the end of the pass that releases it. A record never released is a starved row carrying its lower-bound duration, and that window cannot set the composed maximum.
- (2) A new group registers 16 controllers on every interface. Every notifying command the image completes (SET_NAME, LOCK and unlock, sampling rate, clock source, identify, audio-map edits; plus SET_CONFIGURATION, SET_STREAM_INFO and BIND_RX's GET_STREAM_INFO notice where the answering-ports arm completes them) ends at its last recipient. The per-recipient cost is reported.
- (3) The owed row carries 12 ACMP commands, and the 7 responses ahead are checked by sequence. The required population of each window comes from the contract in the grader, never from the stimulus's declaration, and the self-test counts the actual stimulus.
- (4) The composition plants N6, N8 and N10 fail named checks.
- (5) The SHUTDOWN control is the same path as its functional instance.
Unchanged groups are regraded from their recorded logs on the attested builds. Changed and new groups are re-run.
Validation plan: `run.py --self-test`; both reviewers' probes rerun unmodified; both points, both arms, the SHUTDOWN arm and the three controls; docs gates; `cd tests && behave`.
Blockers: none
