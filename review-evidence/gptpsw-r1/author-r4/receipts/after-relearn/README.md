# Other validation after the relearn, at 631dc544

`python3 -B tb/verilator/ctrl_service_budget/run.py --self-test`: zero failures, rc=0.
`ctrl_split_boot`: 1x1/1if and 8x8/1if rebuilt and simulated with the new layout; both PASS, rc=0.
The boot log contains commands and deliberately non-evidentiary board-grader diagnostics; its own boot assertions pass.
Only prose changed between 631dc544 and the final head, as source-equivalence.txt records.
