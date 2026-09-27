[A379] REVIEW READY
Commit: aafcae59732c0a12333b73d82d5cdcbcbf90c47f
Changed: consistent tap-page CI policy; no-Milan smoke-path help; configured entity directories in product refusal tests; reported equal-clock ROM-control skip.
Validation: all 48 committed-head commands rc 0, including both complete builder compiler modes, test_clock_contract.py --soc, declarations, capture, memory bridge, 38 documentation/policy commands and whitespace checks. The explicitly assigned self-tests all pass.
Reviewer evidence: S9 KILLED; equal-clock probe PASS with named SKIP; ROM mutants R1/R2 remain KILLED; controls pass; CLI defaults unchanged.
Acceptance: required item and all three taken suggestions met. All five configurations and all 61 generated artifact-role hashes match base 9e9954e9. No tracked configuration refused; STOP condition not triggered.
Open risks/questions: none newly introduced. Existing gate-11 physical calibration remains NOT RUN because its historical report is absent; compiler-absent stand-downs are expected and recorded. Independent delta review remains outstanding.
Handoff and updated PR body prepared. No push, PR edit or merge performed.
