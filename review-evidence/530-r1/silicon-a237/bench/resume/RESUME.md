# Bench resume after the network outage (A237, issue 530)

Found at 2026-09-24T05:48:17Z (07:48 CEST), under the bench lock, read-only (tools/run_resume.sh):

- Attempt 1 (bench/attempt1/, launched 05:15:15Z) had completed before the cut:
  crf_bind_window.py exited BIND_RC=0 at 05:29:34Z (720 s bound window, unbind at window end),
  both captures and the counter poll were stopped by the script at 05:29:54Z, the console poll
  ended by itself at 05:30:10Z and the lock was released at 05:30:10Z. The outage (about
  07:30-07:46 CEST = 05:30-05:46Z) cut the session only after that, before the remote files
  were fetched.
- No capture, bind-window, counter-poll or avdecc process was running on the controller host
  or the capture server (procs-*.txt).
- Leftover files: /tmp/a237/{bind.jsonl,counters.jsonl,pw1-run.pcap} on the controller host and
  /tmp/a237/tap-run.pcap on the capture server. Fetched into bench/attempt1/ (hashes in HANDOFF.md).
- Bind state: census-resume.jsonl vs census-start.jsonl -> ACMP states identical 18 of 18
  (no binding on either end: every peer STREAM_INPUT 0..9 and DUT STREAM_INPUT 0..1 unbound,
  every STREAM_OUTPUT conn_count 0), AEM settings reads identical 15 of 15 (census-compare.txt).
- DUT console: responsive; ID 4d494c4e, VERSION 00020060, SYNC=1 ASCAPABLE=1, GM 3cc0c6fffefe0210 (the grandmaster that also heads
  the reference peer's AS path), CRFT_CTRL 0x00000003, LWSRP_STATUS 0 (console-resume.txt).

No unbind was needed; the bench was already at the start state. The acceptance was then rerun
from the beginning (identity, gPTP, start census, bind window) as attempt 2.
