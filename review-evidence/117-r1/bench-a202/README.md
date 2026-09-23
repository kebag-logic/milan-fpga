# Issue 117 bench packet, A202, 2026-09-23 (private)

Raw artifacts behind step 3 (grandmaster loss and return) and the
grandmaster-change half of step 4 in docs/findings/117_GPTP_SILICON_EVIDENCE.md
at lane commit 0abf147f726721f4a323ee6a32095a02363fe2dc. Every file is hashed in
MANIFEST.sha256. Times in file names and logs are build-box UTC unless a
log says otherwise; the build box ran 1.080 to 1.085 s behind the NTP hosts
(clock-before/after.jsonl in every cycle directory).

| Path | What |
|---|---|
| identity/ | console CRC readback, grader log, reference CRC table recomputed from the four build directories, lock window |
| bench/powerstrip/ | power-strip status before (13:45) and after (14:12) step 3 |
| bench/census-start.jsonl, bench/final/census-end.jsonl, bench/final/census-compare.txt | binding and settings census from the controller host, and the comparison |
| bench/attempt1-aborted/ | the aborted first attempt (tool error, OUT4 off 5.95 s, no console record); NOTE.md explains |
| bench/poll-test/ | the 5 s console poll check with no power action, before cycle 1 |
| bench/cycle1 ... cycle6/ | per cycle: tap-cN.pcap (DUT link), pw1-cN.pcap (controller-host port on switch port 8), pw1-watch.jsonl (controller-host watcher), console.txt (0.1 s console poll), powerstrip.txt (power-strip host log, its own clock), lock.txt, timeline.txt, clock-before/after.jsonl, remote SHA-256 of both captures, analysis.txt and analysis.json |
| bench/summary.txt | the per-cycle table (tools/summarize.py) |
| bench/final/ | final console read, grader log, 22 s tap capture and its decode, host cleanup record |
| gates-0abf147f.txt | docs gate transcript at the committed head |
| tools/ | every script used; console_read.py, console_poll.py, avdecc_ro.py, wire_summary.py, expected_crc.py and pdelay_turnaround.py are byte-identical to the previous packet's |

Reproduce a cycle: `PRE=20 HOLD=20 POST=80 BIND=0|1 PROOF=0|1 tools/run_cycle.sh <n>`
(it expects avdecc_ro.py, a202_watch.py and census.sh in /tmp/a202 on the
controller host and powerstrip_cycle.sh at /tmp/a202-ps.sh on the power-strip
host; both were removed after the runs). Analysis:
`tools/analyze_cycle.py bench/cycle<n> --json bench/cycle<n>/analysis.json`,
then `tools/summarize.py bench 1 2 3 4 5 6`.
