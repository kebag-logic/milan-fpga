[A544] REVIEW READY (round 3)
Commit: `9412006bd58c002835bb06d46045c53098cc59a5` on local branch `665-f1-nvm` (not pushed). It is the round-2 head `7f8dc1b1` plus five one-line commits:
- `da35570a`: code and suite;
- `ce78be4a`: the FASTCONNECT section 7 tie edit;
- `716d3213`: the module page;
- `e2000ef9`: a `--no-ff` merge of dev `28f9666f` (PR #666, one findings page; no lane file or submodule touched);
- `9412006b`: the cumulative call bound corrected from 2,171 us to 2,213 us, with the case that shows why.

Changed: `sw/firmware/ctrl_nvm/`, the `docs/README.md` row and the FASTCONNECT section 7 tie line, 32 files against dev `28f9666f`. `milan_baremetal.c` is identical to dev, and nothing links the module into an image. Every item of 5997929153:
1. **Decision 2** (R501-2 F1, MAJOR).
   - A slot's verdict stands on at most 3 reads (`NVM_READ_TRIES`). OK stands on one read, because its CRC-32 covers the SEQ. Any other verdict, BLANK included, stands only when two reads agree. A read the port fails is a media fault.
   - A slot with no standing verdict, or one that never re-stages as judged (3 re-stages), is UNREAD. Its verdict is `VD_LEN`, a new status field `unread` gets its bit, and no SEQ is taken from it.
   - Any UNREAD slot puts the writer in a new phase, HELD, until reset. While HELD, changes are marked and reported in `dirty`, nothing is erased or written, and the console is refused. The restore still applies what was accepted.
   - New check `authority_unknown` (model port). It runs both orientations at SEQ 1, 5, 0x80000000 and 0xFFFFFFFF, under four faults:
     - 3 failed reads: the boot is BLANK and the writer HELD, with no erase and the console refused;
     - 2 failed reads: the slot is applied;
     - an unreported flipped bit: the slot is applied;
     - an aliased read in which the valid slot reads blank: the slot is applied.
   - Each case then runs a clean reboot, a change, a verified commit and another clean reboot. It compares the restored payload every time, and requires that nothing reported committed is lost.
   - `read_fail_boot` grades the bound:
     - two failed header reads, then a good one: the slot is applied;
     - three failed container reads (a new read-fail-at fault), or three failed re-stages: the writer is held;
     - one failed re-stage: the slot is read again and applied.
   - Planted: `unread_not_held`, the generation restart. Its first failure is "slot A at 0x1, read-fail:3:0: the writer is not held", with the store at SEQ 1 in slot B. Also `read_not_retried`, `refusal_unconfirmed`, `blank_unconfirmed` and `restage_not_retried`.
2. **Decision 1** (R501-2 F3). FASTCONNECT section 7 reads `newer = (int32_t)(A.seq - B.seq) >= 0 ? A : B` and cites 5997929153. `newer_wins` ties at 7 and at 0xFFFFFFFF with distinct payloads. Planted: `tie_picks_b` ("seq A 0x7 B 0x7: chose 1, want 0").
3. **Service bound** (R501-2 F2, R500-2 F2).
   - The LiteSPI port now has a per-call deadline: a call still waiting on the master after `LS_CALL_US` = 2,000 us of `timer0` time fails. The check runs every 64 not-ready status reads, counted over the whole call.
   - Runs with no stall armed are asserted under 250 us per call. The suite's real maximum over all such runs is 168 us on the model port and 210 us on LiteSPI, at every shape. The PR body now scopes its 210 us to runs with no stall armed, and gives the suite's maximum over all runs (below).
   - Every run is asserted under 2,213 us per call, the sum of four terms: the deadline (2,000 us), one check interval (3 us), the rest of a page program at the ready pace (42 us), and the window's link time (168 us).
   - New check `port_deadline`:
     - ten slowed waits complete in 1,859 us;
     - twelve slowed waits end just before the deadline, and the call finishes past it in 2,189 us (2,190 us at `endstation_arty_4x4`). This is the suite's real maximum over all runs;
     - every wait slowed by 4,000 reads, none reaching the 4,096-read limit: each program fails at the deadline (2,009 us), three attempts are spent, the authority is untouched, and a later change commits.
   - Planted: `call_deadline_ignored` ("max_call_us=41970 > 2213" in the round-2 port) and `deadline_per_wait`.
   - The README separates the measured nominal figures, the cumulative bound (with a table of eight master cases) and CPU time. On chip the port call's deadline is `timer0`, real time. The store's capture step is a derived floor, compared with nothing.
4. **R500-2**:
   - F1: the restore order is now slots, binding walk, model check, D3 walk (D3 8.1 steps 3 to 8). An unproven model ends CLOSED with the bindings kept. `model_unproven_closes` asserts the bindings applied, `bind_terminal` COMPLETE, CLOSED, nothing released, and blank with an unproven model CLOSED. Planted: `bindings_skipped_unproven`, `model_ready_ignored`.
   - F3: new check `fallback_restage`, in which both slots' re-stages flip every time: BLANK, nothing applied, both slots `VD_LEN` and UNREAD, writer HELD. `debounce` adds a change to the record the capture examines next. Planted: `fallback_restage_unchecked`, `taken_off_by_one` ("erase 1704 us after it").
   - F4: `stale` heals at a DR2b suppression too. `recovers_after_failure` adds a failed attempt, then the same value set again while the retry writes, then DR2b, ending `stale=0`. Planted: `dr2b_keeps_stale`.
   - S1: a failed fallback re-stage is marked `VD_LEN`.
5. Dev moved, so it was merged `--no-ff` (above).

Validation, all at `9412006b`, none piped, all rc 0:
- `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test`: "OK across 5 shape(s), 40 checks, and all 80 planted defects reddened", in 175 s.
  - Each shape runs 40 checks: 29 on both ports, 7 on the model port alone and 4 on LiteSPI alone.
  - Power cut: 3,126 cases, 0 bad, the same table as round 2.
  - RV32 bss is 4,048 B at 1x1 and 14,408 B at 8x8; text is about 11.8 KB.
- `nvm_hosttest/test_nvm_firmware.py --self-test`; `check_nvm_capture.py`; `check_nvm_record_space.py` and `--self-test`.
- `sw/builder/test_builder.py --require-rv32` (Verilator 5.050): "ALL GATES PASS EXCEPT 1 NOT RUN", in 1,339 s. Gate 11 needs a local Vivado report of the mf48 build tree that this host lacks; it is environmental, as in rounds 1 and 2.
- The C/C++, Python and shell idiom gates and their self-tests; hygiene, TODO ownership, test evidence and bare-metal scope, each with its self-test; fail-fast, control flow and cohesion.
- The docs gates:
  - `docs_check`;
  - `check_em_dash --base 28f9666f` (415 added lines in 3 pages, 0 findings) and `--selftest`;
  - doc style, gPTP docs, DOC_MAP, solution and submodule docs, feature status, module matrix, doc paths and archive;
  - `gen_toc --selftest/--verify-anchors/--check`;
  - `ci_events --check`;
  - `git diff --check 28f9666f HEAD`.
- Not run: `nvm_cosim`, lint, xvlog and Yosys, because the lane changes no HDL; `act_ci`, because there is no PR head.

Acceptance criteria: round-1 and round-2 items still met. Every round-3 item, 1 to 5, is addressed above, each with a check and a planted defect that fails it.

Open risks/questions:
- Readings, also in the module page and HANDOFF:
  - (a) Two reads of one slot that disagree are a media fault, and BLANK needs a second read like a refusal.
  - (b) The read retry is bounded at boot. A slot still UNREAD holds the writer until the next reset.
- Stated limit: a fault that corrupts a valid slot the same way on every boot read, unreported by the port, is read as content. The generation can then restart below that slot. No reading of the bytes can tell it apart, and decision 2 takes no generation from unvalidated bytes.
- Carried: the shipping writer's VD_REC/VD_LEN parity gap; its generation restart, which is #671; the lane gate is not in a hosted workflow (R500-1 S1).

HANDOFF.md, PR-BODY.md (beginning `[A544]`, "Relates to #665"), the check-to-defect table, the power-cut table and the gate logs are in the lane's packet.
