The processor gates at the head 51f88c7e14e7e2527c09ff9a23b93dd6b857fd50 (branch 632-sinfo-notify-stored,
three commits on processor main 08023123), pinned Verilator 5.050, each run in a clean clone at that commit
(git status empty before and after), at most two builds at once.

Slot 1 (one clone), in order:
  make_check.log (rc 0)          `make check`: lint, wavedrom, links, matrix, req-tags (231 tags), modmatrix,
                                 params, aecpcmd (selftest 231 of 231; 31 commands), ids, figures, stale
  lint_hdl.log (rc 0)            ./scripts/lint_hdl.sh
  suites.txt (rc 0)              REQ_TAG_LOG=req-tags.txt ./scripts/run_suites.sh (the CI step): every suite
                                 PASS, 1,030,329 checks, 0 failing; pp_top 10,741 over its seven builds
  req-tags.txt                   the evidence lines that run wrote
  req_tags_executed.log (rc 0)   python3 scripts/check-req-tags.py --suites suites.txt --evidence req-tags.txt

campaigns/ (the second clone; one build at a time, beside slot 1's one):
  notify.*      python3 tb/pp_top/notify_mutants.py --jobs 1 --only <the 22 --notify-only controls>:
                goldens PASS, 22 of 22 KILLED by their named checks (the two new ones fail NS4+NS5 and
                NS1+NS2)
  d3.*          python3 tb/pp_top/d3_mutants.py --jobs 1 --only <the 12 controls graded by section S>:
                goldens PASS, 12 of 12 KILLED, each failing exactly the count tb/pp_top/README.md records
  aecp_cmds.*   python3 -B tb/aecp_cmds/mutants.py --jobs 1 (a CI gate): 17 of 17 detected by their named
                failures; golden and restored PASS
  aecp_dispatch.*  (cd tb/pp_top && python3 aecp_dispatch_mutants.py --jobs 1) (a CI gate), run in the
                first clone after slot 1 finished: four controls PASS, 69 of 69 KILLED, 73 checks
  aecp.*        (cd tb/pp_top && python3 aecp_mutants.py --jobs 1) (a CI gate), in the second clone: six
                controls PASS, 61 of 61 KILLED, 67 checks
  *.logs.manifest  size and sha256 of every per-mutant log of that campaign (the logs stay in scratch)

The milan-fpga consumer measurement for this head is ../notify_sinfo_pp_0b097464/ (hdl/ is identical at
0b097464 and 51f88c7e). The superseded run at 0b097464 is ../processor_0b097464_superseded/.
