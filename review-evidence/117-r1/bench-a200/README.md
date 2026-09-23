# Issue 117 bench packet, A200, 2026-09-23 (private)

Raw artifacts behind docs/findings/117_GPTP_SILICON_EVIDENCE.md at lane head
c3eb95fa9ac86a3f20b45f94057d6c011127db08. Every file is hashed in
MANIFEST.sha256.

| Path | What |
|---|---|
| identity/ | console CRC readback transcript, grader log, reference CRC table (tools/expected_crc.py over the three dev seeds and the replaced f6b31625 image), lock window |
| bench/probe-tap-0.pcap | first 12 s tap capture (topology probe) |
| bench/pw1-discover-1.jsonl, peer-aem-1.jsonl, peer-clock-sources.jsonl, peer-control-descriptor.jsonl | controller-host ADP discovery and read-only reference peer descriptor reads |
| bench/pw1-link-probe.pcap, pw1-link-all.pcap | controller-host link captures (switch port 8 identity, switch DHCP requests) |
| bench/census-start.jsonl, final/census-final.jsonl | binding and settings census before and after |
| bench/console-memread-test.* | mem_read check against known CSR words |
| bench/hosts-clock-and-daemons.txt, tool-revisions.txt | host clock offsets, daemon check, tool versions |
| bench/runA/ | steady state: tap capture, console poll, controller poll, analysis, Pdelay turnaround output |
| bench/runB/ | CRF bind window: tap capture, console poll, bind log, analysis, CRF details, MSRP decode, stream timeline |
| bench/runC/ | controller conformance: tap capture, counters probe logs (DUT and peer), enumeration log and entity dumps, raw stream counters, AECP tallies, unsolicited GET_AVB_INFO decode |
| bench/final/ | final tap capture, console read, grader log |
| bench/behave-offline.txt | offline behave run in the lane clone; NOT evidence: the clone has no initialized gptp-processor submodule, so 24 scenarios error at config load |
| bench/pw1-tmp-before-cleanup.txt | hashes of the controller-host temporary files before removal |
| gates-c3eb95fa.txt | docs gate transcripts at the committed head |
| tools/ | every script and the enumerator source and binary used, with run_a.sh, run_b.sh, run_c.sh orchestration |

The reference peer's firmware string is in bench/peer-aem-1.jsonl (ENTITY
descriptor payload); the public page carries only the SHA-256 of the 64-octet
field, as the 2026-09-14 survey did.
