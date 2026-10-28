[A680j] TAKEN
Branch: 665-s1-faces (PR #795), continuing on [A680i]'s head `27c54171` (nothing pushed)
Authoritative references: ruling issuecomment-6461910715 (option (c)) on [A680i]'s STOP issuecomment-6461886441; round-8 assignment issuecomment-6461128613, answering R701-7 (PR #795 issuecomment-6461122749); rulings 6412739248 item 1, 6425357821 and 6421238472 still in force
Interpreted scope:
- The CPU budget harness's SoC pulses `fw_ack_p_i` for each interface at the contract's bound: `ack_cycles` bus cycles (64, the generated constant, not a literal) after that interface's `fw_send_o` rises. Every other face input stays tied idle by name, so window requests time out as the fabric-less split SoC sees them.
- The README and the PR body state this one difference from `CtrlMailbox` and why: a CPU budget needs the slowest acknowledgement the contract allows.
- Everything done at `27c54171` (F1, F2, W1) is kept.
Validation plan:
- a self-test check with a planted mutant for the acknowledgement's bound;
- real harness builds at 1x1/1if and 8x8/2if, arm A and arm B, one group each, to the measurement, compared with S2's recorded figures and with [A680i]'s one-cycle probe, stating the differences S1's firmware explains;
- the round-8 gates: the harness self-test and mutants, R701-7's three probes unchanged, `test_ctrl_memory.py`, the firmware-boundary steps, the firmware self-test (four shards, separate units), `fw_coverage.py --check`, `test_builder.py`, the linked images at four points, `gen_mailbox.py --check`, the docs gates with the bare-metal scope gate, `behave`, and the four-shard Verilator sweep.
Blockers: none
