Round 12 attribution receipts (#894 issuecomment-6883864236 items 1 and 4).
- tree-b1-*.txt / tree-b8-*.txt: inclusive call trees (round12/scripts/calltree.py) of arm B's aecp-fanout
  SET_CONFIGURATION record (frame), the pass's AECP poll and the AECP bridge's delivery after it, and (8x8) the next
  centisecond dispatch, from committed-PC traces on round 11's final-pass arm B builds (images equal to 9606b3a9's).
  Traces: b1 sha256 714a0e328345569992a3f993286dd13abbcc34eb0cefd2604454944bf97887e1 (5,768,899 B),
  b8 4bd723f9b4e58157b20f0b9b91bcc802f75c04f0c372f9a571f9ee147a3db3de (5,849,400 B); not kept here (over 200 KB).
- budget-b1-frame.txt / budget-b8-frame.txt: commits / short / fetch / data stall split (round 11's budget.py).
- prof-b1-frame.txt: round 11's spanprof.py on the 1x1 record.
- tickwin-*.txt: each event the loop took in the SET_CONFIGURATION (and SET_STREAM_INFO) step's window, measured as
  event.TICK is (round 20's eventcost.py cut), and the AECP poll, delivery and record spans, by the rule
  (round12/scripts/tickwin.py); at 9606b3a9 (round 11's legs) and at the final firmware fe0cef5b (round 12's legs).
- tree-e1-timer-*.txt, budget-e1-timer.txt: the answering-every-port arm's dearest AECP timer slot event
  (notice-burst-5) at fe0cef5b (6,206 cycles) and 9606b3a9 (5,753): the same work, fetch stalls +479.
  Traces: e1-head-final sha256 f02cb48701f7002250568af6aa2ffb464f1d4a960fd7243e22f8b6ba91501566,
  e1-9606 f200709cffe2b4e5e71296bc2f723d6a61e4a36c66b3018482b72e245d7e8ee9 (not kept).
