# [A403] Evidence packet

Refs #451. Status: REVIEW READY at `6339479d`. Both directions decoded in all
eight slots; the first session's all-zero DIN came from the DUT talker's empty
output map, not the wiring. Read HANDOFF.md first. The repository findings page
is the public result.

| Artifact | Purpose |
|---|---|
| HANDOFF.md | Status, timelines of both sessions, restoration and residuals |
| TAKEN.md, STOP.md, REVIEW-READY.md | The three public comments, as posted |
| PR-BODY.md | Prepared pull-request text (no PR was created) |
| RAW-ARTIFACTS.json | Every raw file under the raw root, with bytes and SHA-256 |
| redaction.json | Each retained evidence file: raw source, original and retained hashes, labels used |
| evidence/identity-*.{txt,json} | UART CRC readback and AECP descriptor hashes against verified payloads |
| evidence/census-*.jsonl, maps-before.jsonl | AVDECC state before and after the first session |
| evidence/soc-*.log | First session SoC console: health, McASP0 configuration, clock sample, bridge stop and restore |
| evidence/dut-*.txt | First session DUT console reads: SRP/talker baseline, PHC rate, REBOOT-incident check, final state |
| evidence/dout-*/, evidence/din-*/ | First session actions: events, DUT samples, controller logs, SoC logs, decodes |
| evidence/ctl-*.{log,jsonl} | First session gPTP trial, probe debug and MRP debug |
| evidence/slip-rate.json | First session SLIP_TDM samples and the fitted rate |
| evidence/table-render.json | First session page table check |
| evidence/s2/soc/, evidence/s2/dut/ | Second session: SoC health, clock sample, period build test, bridge stop and restore; DUT reads before and after |
| evidence/s2/ctl/ | Second session census before and after, and the controller logs of each action |
| evidence/s2/din2-long/ | DIN exactly as the first session (all zero) |
| evidence/s2/din3-long/ | DIN with the output map routed: map edits, logs, `decode.json`, `pairs.json` |
| evidence/s2/dout2-sanity/ | DOUT 3 s: bind and map edits, DUT samples, capture and transfer logs, decode |
| gates/, gates-s2/ | The gate invocations at `361d1f47` and at `6339479d`, with output and return codes |
| tools/ | Every tool used, with bench identifiers moved to environment variables |

Tools in this packet take bench identifiers from environment variables:
`SOC_CONSOLE`, `DUT_CONSOLE`, `CTL_HOST`, `CTL_IFACE`, `PTP4L`, `GPTP_CFG`,
`ECM_HOST`, `PEER_EID`, `PEER_MAC`, `TALKER_EID` and `GM_ID`. The two shell
scripts take `IFACE`, `IFACE_MAC` and `TALKER_EID`. The second session's
tools also read `A403_TOOLS`, the directory holding `soccon.py` and
`console_read.py`. The first session's executed originals are under the raw
root in `tools-executed/`; the second session's tools ran as shipped here
and their raw copies are in `s2/tools/`. Both are indexed in
RAW-ARTIFACTS.json.

Second-session tools:

- `run_din2.py`: DIN exactly as the first session, with the pattern period
  built on the SoC board.
- `run_din3.py`: the same with eight identity mappings on STREAM_PORT_OUTPUT 0.
- `run_dout2.py`: DOUT with a console transfer. Its xz transfer failed
  because the board's xz only decompresses; `fetch_capture.py` then copied
  the capture with gzip.
- `decode_din_pairs.py`: per-channel continuity and per-pair frame
  coherence.
- `census_cmp.py`: census comparison ignoring per-exchange fields.

Reproduce the offline results while the raw root exists:

```sh
timeout 120 python3 tools/decode_capture.py <raw>/dout-long/dout-long.raw
timeout 120 python3 tools/attribute_dout.py <raw>/dout-long/dout-long.raw evidence/dout-long/talker.jsonl 8
timeout 300 python3 tools/decode_din_pcap.py <raw>/din-long/din-long.pcap 0200000000010000
timeout 300 python3 tools/decode_din_pcap.py <raw>/s2/din3-long/din3-long.pcap 0200000000010000
timeout 600 python3 tools/decode_din_pairs.py <raw>/s2/din3-long/din3-long.pcap 0200000000010000
timeout 120 python3 tools/decode_capture.py <raw>/s2/dout2-sanity/dout2-sanity.raw
timeout 60 <pinned-markdown-venv>/bin/python3 tools/table_render_check.py docs/findings/451_TDM8_FIRST_LIGHT.md
```

The attribution multiple 8 comes from the wall-clock start times of the
talker and of the capture. Of the neighbouring multiples, 8 is also the only
one under which any underrun lines up with a logged late PDU (7 and 9 give 0).

Bench actions need the bench lock and the environment above. The
controller-side tools must be staged under `/tmp/a403` on the controller.
Each action is bounded and restores its own bindings and mappings in a
`finally` block. The SoC bridge legs are stopped and restarted separately;
HANDOFF.md records the exact lines.
