Reviewer scripts for R801-1 (processor issue #216 / PR #218, exact head 60094a268c0df46703a3bee08c94118153634fd9).

run_gate.sh NAME WORKDIR CMD...   runs CMD in WORKDIR; writes receipts/NAME.{cmd,log,rc,start,end}.
                                  VERILATOR_DIR (optional) is prepended to PATH.
launch.sh                         the three gate sets as run (clones of the head under scratch/{hcamp,hsuite,hdocs}):
                                  1) python3 -B tb/srp_top/mutants.py --output <out> --jobs 5
                                  2) make -j4 in tb/srp_top, tb/srp_encoder, tb/srp_stream_fsms, tb/pp_top
                                  3) make check; python3 scripts/gen_matrix.py --check; bash scripts/lint_hdl.sh;
                                     git diff --check 044cb25f <head>
probes/run_probe.sh ARM GROUP     exports the head (git archive, SRC=<clone>) into scratch/, applies ARM, builds tb/srp_top
                                  and runs GROUP. Run as:
                                    run_gate.sh probe_probe216 <packet> probes/run_probe.sh probe216 probe216
                                    run_gate.sh probe_pN <packet> probes/run_probe.sh <arm> applicant
probes/mutate.py                  the five reviewer arms p1..p5 (one exact textual replacement each)
probes/probe_tb.py                adds the reviewer scenario group 'probe216' (peer JoinIn of VID 2 before the first user)
cmp_readme_216.py                 tb/srp_top README #216 arm table vs the campaign log
cmp_enc_readme.py                 tb/srp_encoder README "| `arm`: ... | row | N FAIL" rows vs the campaign log
cmp_top_readme.py                 crude: every tb/srp_top README row's first integer cell vs the campaign log
                                  (column meanings differ between tables; a DIFF there is a lead, not a finding)

Host paths in receipts are replaced by <packet>, <clone>, <toolchain>, <verilator-5.050>, <home>, <tmp>.
