Round 3b: the milan_dp SET_STREAM_INFO notify leg and its planted control, with the
committed processor head's E_SINFO (option (b), as ruled) applied UNCOMMITTED to the
protocol-processor submodule at its pin, pinned Verilator 5.050, VERILATOR_JOBS=2.

milan-fpga lane head: 32fb8fc26acf7dedc507512d7a455898a26afd84 (lane_head.txt)
submodule pin:        2cbed0a987c1e68402658d69459ab7e5aa571adc (submodule_head.txt)
processor head:       0b0974604f770412abea610c3ac819858c7dc708 on 632-sinfo-notify-stored
                      (175a5a15 the E_SINFO change, its pp_top section NS and two planted
                      defects; 0b097464 tb/aecp_cmds' decode record against the new ROM)

How it was applied. The processor head is 50 commits past the pin, and a plain patch of
the head's gen_ucode.py does not apply at the pin with full context (a later comment
after the block differs); with one line of context its third hunk matches a different
`])` 33 lines away. So scripts/round3b/splice_sinfo.py replaced the pin's
`place(E_SINFO, [...])` block, which is otherwise identical, with the head's block and
its three asserts, each found exactly once. submodule_applied.diff is the resulting
submodule diff: exactly the committed E_SINFO hunk.

digests.sha256: the ROM the spliced generator emits is f9954a76..., byte-identical to
round 3's option (b) ROM (receipts/round3/notify_sinfo/ucode_variants.sha256), and
differs from the pin's ROM (518b900c...) in words 1859..1873 alone; those words equal
the processor head's own ROM at E_SINFO.

notify_leg_pp0b097464.log (rc 0)
    `make notify` in tb/verilator/milan_dp: 441 checks, 0 failures, RESULT: PASS.
    [NOTIFY] SET_STREAM_INFO steps 1..4 (2,000,000 held; 2,010,000; 2,010,000 again;
    2,020,834): pushes 0, 1, 0, 1; GET reads 2,000,000, 2,020,834, 2,020,834, 2,041,667.
gsi_mutant9_pp0b097464.log (rc 0)
    `python3 gsi_mutants.py 9`: the unmutated leg passes; the planted control (the stored
    read put back to GET_STREAM_INFO's applied word) is caught at "[NOTIFY]
    SET_STREAM_INFO step 3: 2,010,000 ns again modifies nothing" (3 failures of 441).
never_set_probe_pp0b097464.log (rc 0)
    the disposable never-set probe (scripts/round3b/sinfo_never_set_probe.py, round 3's
    probe with the call anchor of 28510858 and later), run in a scratch clone at
    32fb8fc2 with the same splice, never committed: P1 SET 0 ns on the CRF output's
    never-set row pushes once to B (2 ms in force before), P2 GET then reads 0, P3 SET
    2,000,000 back pushes once; 444 checks, 0 failures. The scratch clone's sim_nxn.cpp
    and submodule were restored afterwards.
submodule_restored.txt
    after the last measurement the lane's submodule is at its pin with an empty status,
    and milan_dp's (ignored) ucode.hex was regenerated from the pinned generator.

Host paths in the two make logs are replaced by <lane>, <scratch clone at 32fb8fc2> and
<toolchain path>.
