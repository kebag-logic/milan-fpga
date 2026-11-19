# Receipts index (#943 round 2, head a16899b1)

Generated from the files present by make_index.py. Host paths are replaced by `<lane>`, `<scratch>`, `<home>`, `<tools>` and `<tmp>`. Each row: path, size, sha256 prefix, first line.

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `budget/arm-b-8x8-1if-share-round1.txt` | 407 | `82101ed06a015e66` | # arm B (answering-ports) at 8x8/1if on round 1's images: its aecp-largest-notice passes over the share, as th |
| `budget/brief-probe.txt` | 741 | `1dd8a9e1c288142d` | # tools/probe_brief_r2.py: the declaring-outputs arm's b_stream (declaring_outputs.FIXTURE_EDITS at a16899b1)  |
| `budget/declaring-outputs-1x1-console.txt` | 705 | `6f997fd7f437d5f5` | # run.py --point 1x1 --variant declaring-outputs (budget.sh adds --record-budget-findings --record-share-findi |
| `budget/declaring-outputs-1x1-rows.md` | 2780 | `f007956bd03c3560` | # the arm's aecp-outputs rows and aecp-fanout's SET_STREAM_INFO row at 1x1/1if (table.md at a16899b1) |
| `budget/declaring-outputs-8x8-1if-console.txt` | 849 | `9a84f26269f6f680` | # run.py --point 8x8-1if --variant declaring-outputs (budget.sh adds --record-budget-findings --record-share-f |
| `budget/declaring-outputs-8x8-1if-rows.md` | 3925 | `e76c21c50b30b715` | # the arm's aecp-outputs rows and aecp-fanout's SET_STREAM_INFO row at 8x8/1if (table.md at a16899b1) |
| `budget/flip-grade-1x1.txt` | 1875 | `bc03416864e6ce1b` | # flip_grade.py --check --point 1x1/1if at the round-2 code (statements unchanged) |
| `budget/flip-grade-8x8.txt` | 1452 | `20a25dad8ebfcce7` | # flip_grade.py --check --point 8x8/1if at the round-2 code (statements unchanged) |
| `budget/harness-selftest.txt` | 11526 | `8700890ad5b6d942` | # run.py --self-test on the lane tree carrying a16899b1's harness: the declaring checks' lines and the verdict |
| `budget/plant-brief-completed-1x1.txt` | 1424 | `477cdfc7ed14e556` | # run.py --point 1x1 --variant declaring-outputs --mutation brief-completed, on 502b041c with round 2's change |
| `budget/plant-brief-completed-8x8.txt` | 1435 | `5b770c3a8faceb7e` | # run.py --point 8x8-1if --variant declaring-outputs --mutation brief-completed, on 502b041c with round 2's ch |
| `budget/plant-completion-dearer-1x1.txt` | 1262 | `f7f2fda56759ba99` | # run.py --point 1x1 --variant declaring-outputs --mutation completion-dearer, on 502b041c with round 2's chan |
| `budget/plant-completion-dearer-8x8.txt` | 1274 | `44b51fe684eacb48` | # run.py --point 8x8-1if --variant declaring-outputs --mutation completion-dearer, on 502b041c with round 2's  |
| `budget/plant-completion-unexecuted-1x1.txt` | 5341 | `583e5499df528c53` | # run.py --point 1x1 --variant declaring-outputs --mutation completion-unexecuted, on 502b041c with round 2's  |
| `budget/plant-completion-unexecuted-8x8.txt` | 7129 | `2b12d3031c21a0f9` | # run.py --point 8x8-1if --variant declaring-outputs --mutation completion-unexecuted, on 502b041c with round  |
| `budget/record-classes-1x1-without-declaring.txt` | 1441 | `529b0a31e875e3e2` | # record_classes.py at the round-2 code over the same legs without the declaring-outputs leg: the coverage con |
| `budget/record-classes-1x1.txt` | 1641 | `5e5efe08191fae7c` | # record_classes.py at a16899b1 over 1x1/1if's arm A (all 99 groups, merged; round 1, the same firmware), answ |
| `budget/record-classes-8x8-1if.txt` | 1671 | `0edb085197fb5c8f` | # record_classes.py at a16899b1 over 8x8/1if's arm A (all 98 groups, merged; round 1, the same firmware), answ |
| `budget/record-classes-8x8-without-declaring.txt` | 1459 | `80d716c0df2ee040` | # record_classes.py at the round-2 code over the same legs without the declaring-outputs leg: the coverage con |
| `docs/docs-gate-steps-a16899b1.txt` | 9155 | `31ab7f58105af50b` | # docs.yml's gate jobs' run: steps on a fresh clean clone of a16899b1 (tools/docs_steps.py): each step's rc, a |
| `firmware/boundary-without-verilator-a16899b1.txt` | 1289 | `b2767a7ff25a3eff` | # ctrl_boundary.py --require-rv32 --selftest --without verilator (the LiteX venv's python3) on a clean clone o |
| `firmware/firmware-gate-a16899b1-shard0.txt` | 4420 | `6a2bea54cb8753e4` | # test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 4 on a clean clone of a16899b1; the verd |
| `firmware/firmware-gate-a16899b1-shard1.txt` | 56749 | `d938eb762bfd286c` | # test_ctrl_firmware.py --require-rv32 --self-test --shard 1/4 --jobs 4 on a clean clone of a16899b1; the verd |
| `firmware/firmware-gate-a16899b1-shard2.txt` | 35347 | `bff95253aba344a8` | # test_ctrl_firmware.py --require-rv32 --self-test --shard 2/4 --jobs 4 on a clean clone of a16899b1; the verd |
| `firmware/firmware-gate-a16899b1-shard3.txt` | 66590 | `97a1fa73311b1b20` | # test_ctrl_firmware.py --require-rv32 --self-test --shard 3/4 --jobs 4 on a clean clone of a16899b1; the verd |
| `firmware/fw-coverage-a16899b1.txt` | 9936 | `a9352921427f8863` | # fw_coverage.py --check --jobs 4 on a clean clone of a16899b1 |
| `firmware/plants-1x1-if1.txt` | 4819 | `3540a898506226fe` | # every row of aecp_output_mutants.ROWS planted alone at 1x1-if1, AppOutputs and Core.TheRunningCheckObservesE |
| `firmware/plants-1x1-if2-before-renaming.txt` | 5300 | `6882aab6772332c3` | # the same at 1x1-if2 before output-listener-on-interface-zero and output-listener-of-output-zero were named b |
| `firmware/plants-1x1-if2.txt` | 5252 | `28e52de88906825d` | # every row of aecp_output_mutants.ROWS planted alone at 1x1-if2, AppOutputs and Core.TheRunningCheckObservesE |
| `firmware/plants-8x8-if1.txt` | 4814 | `2f308cddc144dc55` | # every row of aecp_output_mutants.ROWS planted alone at 8x8-if1, AppOutputs and Core.TheRunningCheckObservesE |
| `tests/app-1x1-if2.txt` | 1779 | `beb22ed78ce6aaec` | # aecp_arms.py --app --interfaces 2 --filter 'AppOutputs.*:Core.TheRunningCheckObservesEveryStreamBriefly' on  |
| `tools/budget.sh.txt` | 790 | `b4ce78e65a15d984` | #!/usr/bin/env bash |
| `tools/docs_steps.py.txt` | 7423 | `04965eaba348c812` | #!/usr/bin/env python3 |
| `tools/env.sh.txt` | 595 | `f3afe5735d662dad` | # env.sh: the pinned tools for lane 943's harness and image runs (sourced) |
| `tools/launch_budget.sh.txt` | 1181 | `1d4c6657dd107381` | #!/usr/bin/env bash |
| `tools/launch_fw.sh.txt` | 1396 | `d3b61386207e6918` | #!/usr/bin/env bash |
| `tools/launch_wip.sh.txt` | 1250 | `9524c338610e5dcb` | #!/usr/bin/env bash |
| `tools/make_index.py.txt` | 1435 | `eafaeef960329f3f` | #!/usr/bin/env python3 |
| `tools/probe_brief_r2.py.txt` | 2991 | `f667ffb3739a9ddd` | #!/usr/bin/env python3 |
| `tools/probe_rows.py.txt` | 4700 | `d1b590a6425c3a78` | """probe_mutants.py <tree> <out> <config> <interfaces> <set> [shard/of] |
| `tools/queue2.sh.txt` | 426 | `813a65d96a93ad00` | #!/usr/bin/env bash |
| `tools/sanitize.py.txt` | 1086 | `23d9fc7993d7d6d0` | #!/usr/bin/env python3 |
| `tools/unit.sh.txt` | 764 | `957c8744e9b253dd` | #!/usr/bin/env bash |
| `tools/unit_venv.sh.txt` | 782 | `e4b23a7512931e50` | #!/usr/bin/env bash |
