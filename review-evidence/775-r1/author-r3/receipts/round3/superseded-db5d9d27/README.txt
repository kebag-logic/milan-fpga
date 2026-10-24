Receipts at db5d9d27, the round-3 head before 220b51f2. Every gate there was rc 0, and the full
sweep was 64/64 suites, 0 failures. But its check total, 2,190,132, was 464 checks too high:
format_mutants.py printed each planted pair's lockstep tally line, and scripts/suite_tally.py
counted the first tally on each of those four lines (4 x 116). Commit 220b51f2 prints that result
as checks/failures pairs, which the tally does not read. All gates were rerun at 220b51f2; the
receipts outside this folder are the ones that count.
db5d9d27 sweep avtp_rxmon.log: checks 1041 failures 0
c2a080ae sweep avtp_rxmon.log: checks 551 failures 0
