# Attempt 1: aborted, not counted as a cycle

Run `PROOF=1 BIND=0 PRE=20 HOLD=20 POST=260 run_cycle.sh 1` at 13:51:17 UTC
(build-box clock). The directory was renamed from `cycle1` to
`attempt1-aborted` afterwards; the file names inside still say `c1`.

What went wrong: `tools/console_poll.py` had not yet been copied into the
packet, so the console poller exited at once with rc 2
(`console_poll.stdout`), and no `console.txt` was written. Twenty seconds
into the locked section the power-strip host switched OUT4 off
(T_OFF_CMD 1790171504.933 on its clock). Six seconds later the guard
(`console_alive.py`) found no transcript, printed PROOF_ABORT and switched
OUT4 back on at 1790171510.883, so the switch was off for 5.95 s. The
sequence's own "on" at 1790171525.223 found OUT4 already on. No other outlet
changed (`powerstrip.txt`, `lock.txt`).

What the partial artifacts show (controller-host clock, `pw1-watch.jsonl`):
the switch's port 8 lost carrier at 1790171506.072 and regained it at
1790171524.576; the first successful GET_AVB_INFO after that, at
1790171528.678, found the DUT naming itself (`020000fffe000001`) as
grandmaster with AS_CAPABLE clear, and the one at 1790171530.679 found the
switch (`3cc0c6fffefe0210`) with AS_CAPABLE set. The reference peer's ADP
available_index continued (5849 to 5855). `tap-c1.pcap` and `pw1-c1.pcap`
cover the same 60 s.

Fixes before cycle 1: `console_poll.py` copied unchanged from the previous
packet (SHA-256 `3a0de7d8...`, identical to its manifest entry); a pre-flight
check in `cycle_locked.sh` refuses any power action unless the console
transcript is growing; `console_alive.py` reports a missing transcript as not
alive. A 5 s poll check (`bench/poll-test/`) passed at 13:52:59 UTC with no
power action.
