# Issue 529 silicon confirmation bench packet, A231, 2026-09-24 (private)

Raw artifacts behind the [A231] result comment on #529. HANDOFF.md is the
summary; MANIFEST.sha256 hashes every file here except itself.

| Path | What |
|---|---|
| identity/ | console identity transcript (milan_status, mem_list, CRC readback, ID/VERSION mem_read), grader log, reference CRC table over the three 50e78097 seeds and the #117 image, lock window, origin/dev tip |
| bench/clock-offset-start.txt | build box against controller host clock offset |
| bench/discover-start.jsonl | ADP discovery from the controller host |
| bench/gptp/ | 60 s console poll and controller GET_AVB_INFO/GET_AS_PATH watch |
| bench/census-start.jsonl, final/census-final.jsonl, final/census-compare.txt | binding and settings census before and after, and the comparison |
| bench/step2/ | #117 step 5 re-run: counters probe logs (DUT, peer), enumeration log and entity dumps, controller-host capture, decoded AECP |
| bench/step3/ | bind window: bind log, 5 s counters poll and its summary, console poll and summary, 300 s registered enumeration log and entity dumps, controller-host capture, decoded AECP (DUT, peer summary), unsolicited-notification analysis |
| bench/final/ | final enumeration, census, console read, grader, capture, decoded AECP |
| bench/pw1-tmp-before-cleanup.txt | hashes of every controller-host temporary file before removal |
| bench/*/remote-sha256.txt | controller-host hashes of each capture and dump before copying |
| tools/ | every script and the enumerator source and binary used; #117 tools unchanged; a231_* are new |
| public-comment-529.md, posted-comment-529.readback.md, posted-comment-url.txt | the posted #529 comment |

Bench-identifying strings (host aliases, interface names, the console by-id
name, the reference peer's entity ID and descriptor payloads) appear in raw
files here. The public comment names equipment by role only.
