[A373] REVIEW READY

Refs #117. Head: `bcba79a50ecd2eca99db91c4f3802d888eaac7e4`; branch `117-la-avdecc-enum`, base `2a2a7bb655e528edc3087c88033cd3a47546feb4`. One local commit, not pushed.

Changed only the two Hive rows and blocker B4 in `docs/findings/117_GPTP_SILICON_EVIDENCE.md`, under the [2026-09-27 owner decision](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5858063707). Every other NOT RUN line is unchanged.

| Measurement | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| IEEE 1722.1 library compatibility | PASS | PASS | PASS |
| Milan library compatibility | PASS | PASS | PASS |
| Complaints / warnings / query errors | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| Descriptors / types | 41 / 14 | 41 / 14 | 41 / 14 |
| Enumeration time | 234 ms | 229 ms | 169 ms |
| Process return code | 0 | 0 | 0 |

**Identity: PASS before enumeration.** The assigned bitstream and AEM SHA-256 hashes match the local build artifacts. UART returned VERSION `00020060`, ROM CRC `9b6576a9`, QSPI payload CRC `3c18c276` and AEM CRC `93742dd2`. AECP ENTITY and CONFIGURATION are byte-identical to the assigned AEM templates. Entity `020000fffe000001`, model `001bc5c40236ba0e`, firmware `2.96.0`. CRC readback is a consistency check, not configuration SHA-256 readback. The diff from image `9e9954e9` to lane base `2a2a7bb6` contains four documentation/evidence files only.

**Stable result:** three separate 12 s processes, 17:29:27 through 17:30:35 UTC. Compatibility flags `IEEE17221` and `MILAN`, no compatibility-change events, and identical inventories/static trees. AECP retries, timeouts and unexpected responses are zero. The 41 descriptors comprise ENTITY 1, CONFIGURATION 1, AUDIO_UNIT 1, STREAM_INPUT 2, STREAM_OUTPUT 2, AVB_INTERFACE 1, CLOCK_SOURCE 2, LOCALE 1, STRINGS 1, STREAM_PORT_INPUT 1, STREAM_PORT_OUTPUT 1, AUDIO_CLUSTER 25, CONTROL 1 and CLOCK_DOMAIN 1.

**Provenance:** library `v4.3.1.1`, revision `6d61a92e7f264c69f23cdc38f50d31114e567aa0`, runtime `4.3.1-beta1`; probe source SHA-256 `ac552f67c8b769e0cfc46d0b80c4e9ece0c9da1811020d2c497e2f904749a623`. The build uses the library's own feature defines. Raw logs, full DUT entity dumps, flags, hashes and sizes are in packet `117-a373`, with `MANIFEST.sha256`, `HANDOFF.md` and `PR-BODY.md`. Publication is pending with the coordinator.

**Validation:** all rc 0 from the physical lane: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 2a2a7bb6` (116 added lines), `check_doc_paths.py`, `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check`, and `git diff --check`. The pinned Markdown dependencies were installed outside the packet. The committed diff also passes the whitespace check.

**Bench state:** each console or AVB action used its own lock. No binds, CSR writes, flash, power, wiring or instrument actions. Final UART still reports sync/asCapable and `tu=0`. No enumeration process or temporary remote files remain; bench lock free.

**Scope/limits:** the replacement row passes; this does not close acceptance box 4 or #117. The older dated enumeration result remains as historical evidence. Independent review and evidence publication remain with the coordinator.

