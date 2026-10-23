Superseded: the processor gates at 0b0974604f770412abea610c3ac819858c7dc708 (632-sinfo-notify-stored),
pinned Verilator 5.050, each in a clean clone at that commit. Kept because the suite sweep found D9.

make_check.log (rc 0)          `make check`: every docs gate, including the AECP command gate after
                               0b097464 re-recorded tb/aecp_cmds/decode.json (at 175a5a15 alone it refused:
                               "decode.json was swept from another ucode.hex").
aecp_cmds_record.log           `make -C tb/aecp_cmds record` in the processor clone (the re-record of
                               0b097464): 617,916 trials, 176 checks pass; the digest line alone moved.
lint_hdl.log (rc 0)            ./scripts/lint_hdl.sh
suites.txt (rc 1)              REQ_TAG_LOG=... ./scripts/run_suites.sh: every suite PASS but pp_top, whose first
                               build failed one check; `make run` then ran none of its six later builds.
pp_top_default_rerun_tallies.txt  the first build re-run by hand: the one failure is
                               "D3S5 premise: the change accepted at 315227, the WRITE's done at 315228".
                               D3S5 measured E_SINFO's latency to the store on a row never set (the
                               integrator's arm) and timed a SET on a set row (the stored arm), a cycle
                               apart. Fixed in 51f88c7e (the latency measured on a set row).
notify_mutants.*               every --notify-only control at 0b097464, one build at a time: goldens PASS,
                               22 of 22 KILLED by their named checks.
Host paths in aecp_cmds_record.log are replaced by <processor clone> and <toolchain path>.
