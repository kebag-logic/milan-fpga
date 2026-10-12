"""Lane B16, round 6: the spec r6_figures_build.py turns into check_b16_figures.py's ROWS_TSV and EXCLUDE.

Round 5's r5_figures_spec.py with round 6's changes: X marks the code literals (code=True), drops the page
marker (comments are no longer read) and names round 6's directory, commits and reviews; anchors moved with
the reworded text; the LOCKED row of lane B6's terms table reads each case's own receipt (R624-5-F1); the
idle channels' indices are rows bound to the text around them (a shown text starting with @); rows for the
packet's location (round 6) and round 6's figures.

Round 4's r4_figures_spec.py with round 5's changes: X holds the round 5 identifier categories, read over
blocks, each bound to its keyword or tested (a packet path, an anchor); anchors moved with the text; rows
for round 5's figures.

An authoring aid, not evidence: check_b16_figures.py holds every row explicitly and does not import this
file. Each A(anchor, rows...) names the one covered line that contains the anchor text (n picks among
several, off moves to a following line, doc="README.md" looks in the findings index). Each row is
(shown, receipt, key, precision); a shown text with a marked figure, `context «figure» context`, picks
that occurrence of the figure on the line. GEN and GEN2 derive the rows of the hash tables, the point
tables and the grade tables from the page itself, one row per figure. X is the EXCLUDE block verbatim.
"""
import re
L = []
def A(anchor, *rows, n=None, c=None, off=0, doc=None):
    L.append((anchor, n, rows, c, off, doc))

CS = "get(d, 'check=clock-sources.detail.sources')"
# round 4: census reads, the start record aside (R625-3-S1), recomputed from both census files
CR = lambda a, b, c, i: f"census_reads('restore/{a}.jsonl', 'restore/{b}.jsonl', 'restore/{c}.txt')[{i}]"
# ---------------- lane B16: heading, summary
A("## Dev 5603c353, 2026-10-12: lane B16",
  ("2026-10-12", "identity/lock-window.txt", "stamps('identity/lock-window.txt', 'LOCK')[0]", "date"), c="lane B16: heading and summary")
A("Refs #629. Operator [A603], 2026-10-12, under the",
  ("2026-10-12", "identity/lock-window.txt", "stamps('identity/lock-window.txt', 'LOCK')[0]", "date"))
A("| Tool controls | PASS | Lanes B6 and B9's byte-equal",
  ("decode «8» of 8", "controls/b16-tap-controls.json", "sum(c['result'] == 'PASS' for c in d['controls'])", "d"),
  ("8 of «8»", "controls/b16-tap-controls.json", "len(d['controls'])", "d"),
  ("alignment «6» of 6", "controls/b16-align-controls-synth.json", "sum(c['result'] == 'PASS' for c in d['controls'])", "d"),
  ("6 of «6»", "controls/b16-align-controls-synth.json", "len(d['controls'])", "d"))
A("| Step 2, the loopback as the positive reference |",
  ("Two", "runs/loop1/events.jsonl", "sum(1 for r in RUNS for b in ev(r, 'bind') if b['talker'] == 'peer-out-0' and b['listener'] == 'peer-in-0')", "W"))
A("| Where this setup and the working loopback differ |",
  ("twice", "summary/loop2/acmp-peer-tap.json", "sum(x['msg'] == 'CONNECT_TX_COMMAND' for x in d['acmp'])", "x"),
  ("200", "summary/loop2/acmp-peer-tap.json", "(lambda p: (p[1]['t'] - p[0]['t']) * 1000)([x for x in d['acmp'] if x['msg'] == 'CONNECT_TX_COMMAND'])", ".0f"))
# ---------------- B16: identity and setup
A("| Over ATDECC, the live ENTITY descriptor |",
  ("020000fffe000001", "identity/identity-verdict.txt", "get(d, 'check=atdecc-entity_id.detail.read')", "s"),
  ("2.96.0", "identity/identity-verdict.txt", "get(d, 'check=atdecc-firmware_version.detail.read')", "s"), c="B16: identity and setup")
A("| Console `milan_status` |",
  ("4d494c4e", "identity/identity-verdict.txt", "get(d, 'check=console-id.detail.read.0')", "s"),
  ("0x00020060", "identity/identity-verdict.txt", "'0x' + get(d, 'check=console-id.detail.read.1')", "s"))
A("| AEM image in QSPI, 7,512 bytes, its CRC32 |",
  ("7,512", "identity/console-identity.txt", "rx('identity/console-identity.txt', r\"cmd='crc 0x[0-9a-f]+ (\\d+)'\")", ",d"),
  ("5ba355eb", "identity/identity-verdict.txt", "get(d, 'check=console-aem-crc.detail.read')", "s"))
A("| Live ENTITY and CONFIGURATION |",
  ("312", "identity/identity-verdict.txt", "get(d, 'check=live-vs-qspi-ENTITY 0.detail.live_bytes')", "d"),
  ("106", "identity/identity-verdict.txt", "get(d, 'check=live-vs-qspi-CONFIGURATION 0.detail.live_bytes')", "d"))
A("| Clock sources of #629 |",
  ("CLOCK_SOURCE «0» INTERNAL", "identity/identity-verdict.txt", f"next(k for k, v in {CS}.items() if isinstance(v, dict) and v['type'] == 0)", "s"),
  ("; «1» INPUT_STREAM", "identity/identity-verdict.txt", f"next(k for k, v in {CS}.items() if isinstance(v, dict) and v['type'] == 2 and v['location_index'] == 1)", "s"),
  ("STREAM_INPUT «1»;", "identity/identity-verdict.txt", f"{CS}['1']['location_index']", "d"),
  ("; «2» INPUT_STREAM", "identity/identity-verdict.txt", f"next(k for k, v in {CS}.items() if isinstance(v, dict) and v['type'] == 2 and v['location_index'] == 0)", "s"),
  ("STREAM_INPUT «0»;", "identity/identity-verdict.txt", f"{CS}['2']['location_index']", "d"),
  ("CLOCK_SOURCE «3» answers", "identity/identity-verdict.txt", f"next(k for k, v in {CS}.items() if v == 'NO_SUCH_DESCRIPTOR')", "s"),
  ("lists «0», 1", "identity/identity-verdict.txt", "get(d, 'check=clock-sources.detail.clock_domain_list.0')", "d"),
  ("0, «1» and", "identity/identity-verdict.txt", "get(d, 'check=clock-sources.detail.clock_domain_list.1')", "d"),
  ("and «2» and reads", "identity/identity-verdict.txt", "get(d, 'check=clock-sources.detail.clock_domain_list.2')", "d"),
  ("reads «0» |", "identity/identity-verdict.txt", "get(d, 'check=clock-sources.detail.get_clock_source')", "d"))
A("| UART grader | 10 of 10 |",
  ("«10» of 10", "identity/grader-identity.txt", "rx('identity/grader-identity.txt', r'UART SMOKE: PASS \\((\\d+)/(\\d+)\\)')", "s"),
  ("10 of «10»", "identity/grader-identity.txt", "rx('identity/grader-identity.txt', r'UART SMOKE: PASS \\((\\d+)/(\\d+)\\)', group=2)", "s"))
A("| ADP | The DUT with entity model",
  ("001bc5c1935893e1", "identity/adp-discover.jsonl", "next(x['model_id'] for x in d if x.get('entity_id') == '020000fffe000001')", "s"))
A("| Identity gate | PASS, 05:45:06 to 05:45:12 CEST |",
  ("05:45:06", "identity/lock-window.txt", "stamps('identity/lock-window.txt', 'LOCK')[0]", "cest"),
  ("05:45:12", "identity/lock-window.txt", "stamps('identity/lock-window.txt', 'UNLOCK')[0]", "cest"))
A("As found, at 05:45 CEST, the bench was in lane B15's end state:",
  ("05:45", "restore/baseline-start-lock.txt", "stamps('restore/baseline-start-lock.txt', 'LOCK')[0]", "hm"))
A("`0205022001006000`; STREAM_PORT_INPUT 0, with four identity mappings, and",
  ("0205022001006000", "restore/census-start.jsonl", "cen('restore/census-start.jsonl', 'format-dut-5-0')['payload'][8:]", "s"),
  ("four", "restore/census-start.jsonl", "identity_maps(cen('restore/census-start.jsonl', 'map-dut-0x000e-0-0'))", "w"))
A("STREAM_PORT_OUTPUT 0, with eight. CLOCK_DOMAIN 0, on CLOCK_SOURCE 0. NVM image",
  ("eight", "restore/census-start.jsonl", "identity_maps(cen('restore/census-start.jsonl', 'map-dut-0x000f-0-0'))", "w"),
  ("CLOCK_SOURCE «0».", "restore/census-start.jsonl", "payload_word(cen('restore/census-start.jsonl', 'clock', 'dut'), 8)", "d"))
A("seq 276, 42 commits, `pend=0`. `SLIP_LB` 152 dups.",
  ("276", "restore/dut-start.txt", "nvm('restore/dut-start.txt')['seq']", "d"),
  ("42", "restore/dut-start.txt", "nvm('restore/dut-start.txt')['commits']", "d"),
  ("0", "restore/dut-start.txt", "nvm('restore/dut-start.txt')['pend']", "d"),
  ("152", "restore/dut-start.txt", "le32(mem('restore/dut-start.txt', '0x900008d4', 12)) & 0xffff", "d"))
A("`0205022002006000`, and its STREAM_INPUT 8, bound to the DUT's CRF talker. Its",
  ("0205022002006000", "restore/census-start.jsonl", "cen('restore/census-start.jsonl', 'format-peer-5-0')['payload'][8:]", "s"))
A("AAF talker, at `0205022001006000` with connection count 0.",
  ("0205022001006000", "restore/census-start.jsonl", "cen('restore/census-start.jsonl', 'format-peer-6-0')['payload'][8:]", "s"),
  ("count «0».", "restore/census-start.jsonl", "cen('restore/census-start.jsonl', 'tx-state-peer-0')['conn_count']", "d"))

X = r'''
X("commit", r"`(?P<t>5603c353|694d7da6|0d4ff919|e20fd282|35e332b6|c20c85bd|e8454e27|0782c55f|b84584e4|61ae8641|b83e5d76|36190193|a73ce5c4)`", code=True)
X("commit", r"\bDev (?P<t>5603c353)\b")
X("clause", r"\bIEEE (?P<t>1722\.1)\b")
X("clause", r"\bMilan v(?P<t>1\.2) Table (?P<t2>5\.4)\b")
X("descriptor index", r"\b(?:STREAM_INPUT|STREAM_OUTPUT|STREAM_PORT_INPUT|STREAM_PORT_OUTPUT|CLOCK_DOMAIN|ENTITY|CONFIGURATION)\s+(?P<t>\d+)\b")
X("channel index", r"\b[Cc]hannels?\s+(?P<t>\d+)(?:\s+(?:and|to)\s+(?P<t2>\d+))?\b")
X("step or round index", r"\b(?:[Ss]teps?|[Rr]ounds?)\s+(?P<t>[a-z]?\d+)(?:\s+and\s+(?P<t2>[a-z]?\d+))?\b")
X("list-item index", r"(?<!\S)(?P<t>\d+)\. ", list_item)
X("packet label", r"`(?P<t>629-b16-a603)`", code=True)
X("branch name", r"`(?P<t>629-b16-review-evidence)`", code=True)
X("link target", r"\]\((?P<t>[^()\s]+)\)", on_page, address=True)
X("issue number", r"(?<![\w&])#(?P<t>629|645)\b")
X("lane or case name", r"\b(?P<t>B(?:0|5|6|7|8|9|10|15|16[bc]?))\b")
X("review name", r"\b(?P<t>R62[45]-[1-6](?:-[FRS][1-9])?)\b")
X("operator", r"\[(?P<t>A603)\]")
X("serial port", r"\b(?P<t>McASP0)\b")
X("hash name", r"\b(?P<t>SHA-256|CRC32)\b")
X("entity name", r"\bentity name \"Milan FPGA (?P<t>1x1 TDM8)\"")
X("serial number", r"\bserial \"(?P<t>AX7101-0001)\"")
X("command", r"(?<![^\s`])(?P<t>python3)(?= -I )", lambda m, text: in_code(m, text, "python3"), code=True)
X("field name", r"`(?P<t>original_sha256|published_sha256)`", code=True)
X("packet directory", r"`(?P<t>author-r[1-6]/)`", code=True)
X("packet path", r"(?<![^\s`])(?P<t>[^\s`]*\d[^\s`]*)(?![^\s`])", in_code, code=True)
'''

ACMP = "summary/loop2/acmp-peer-tap.json"
def acmp_t(msg, i=0):
    return f"acmp('{msg}'" + (f", {i})" if i else ")")
T_UNBIND = acmp_t('DISCONNECT_RX_COMMAND')
POLL = "[x for r in ('loop1', 'loop2') for x in ev(r, 'listener-poll')]"
# ---------------- B16: method
A("**The tone.** Lane B15's: lane B9's loop (`b9_tone.py`, 997 Hz and 9,973 Hz",
  c="B16: method")
A("at -20 dBFS), SHA-256: `d9684a8f...`, played into the reference peer's talker",
  ("-20", "tools/b9_tone.py", "Decimal(rx('tools/b9_tone.py', r'^LEVEL_DBFS = (-?[\\d.]+)'))", "d"),
  ("d9684a8f...", "runs/tone-start.txt", "rx('runs/tone-start.txt', r'LOOP_SHA256 ([0-9a-f]{8})') + '...'", "s"))
A("inputs through the authorised tone source, from ",
  ("05:55:37", "runs/tone-start.txt", "stamps('runs/tone-start.txt', 'STATUS')[0] - Decimal(rx('runs/tone-start.txt', r'hw_ptr : (\\d+)')) / 48000", "cest"),
  ("06:01:59", "runs/tone-stop.txt", "stamps('runs/tone-stop.txt', 'LOCK')[0]", "cest"))
A("lane only started and stopped that playback, read the source's state twice and",
  ("twice", "r2/source-receipt.json", "sum(1 for k, r in d['reads'].items() if k.startswith('b16-') and r['kind'] == 'state')", "x"))
A("**The runs.** Each run is one locked action of `run_b16.py`:",
  ("one", "runs/loop1-lock.txt", "same(len(stamps(f'runs/{r}-lock.txt', 'LOCK')) for r in ('loop1', 'loop2'))", "w"))
A("- For 12 s after the bind, and again after the captures, the listener's",
  ("12", "runs/loop1/events.jsonl", f"same(round(max(x['dt'] for x in ev(r, 'listener-poll'))) for r in ('loop1', 'loop2'))", "d"))
A("GET_RX_STATE, its GET_COUNTERS and the talker's GET_TX_STATE are read every",
  ("2", "runs/loop1/events.jsonl", f"same(round(statistics.median(b['dt'] - a['dt'] for a, b in zip(ev(r, 'listener-poll'), ev(r, 'listener-poll')[1:]) if b['tag'] == a['tag'])) for r in ('loop1', 'loop2'))", "d"), off=1)
A("| `loop1` | 05:56:30 to 05:57:30 |",
  ("05:56:30", "runs/loop1-lock.txt", "stamps('runs/loop1-lock.txt', 'LOCK')[0]", "cest"),
  ("05:57:30", "runs/loop1-lock.txt", "stamps('runs/loop1-lock.txt', 'UNLOCK')[0]", "cest"),
  ("30.6", "runs/loop1/events.jsonl", "E('loop1', 'capture-done', what='tap')['seconds']", ".1f"),
  ("22", "runs/loop1/events.jsonl", "E('loop1', 'capture-done', what='extcap')['seconds']", ".0f"),
  ("05:56:45", "runs/loop1/events.jsonl", "E('loop1', 'captures-started')['started']['extcap']", "cest"))
A("| `loop2` | 05:59:18 to 06:00:28 |",
  ("05:59:18", "runs/loop2-lock.txt", "stamps('runs/loop2-lock.txt', 'LOCK')[0]", "cest"),
  ("06:00:28", "runs/loop2-lock.txt", "stamps('runs/loop2-lock.txt', 'UNLOCK')[0]", "cest"),
  ("52.5", "runs/loop2/events.jsonl", "E('loop2', 'capture-done', what='tap')['seconds']", ".1f"),
  ("05:59:19", "runs/loop2/events.jsonl", "E('loop2', 'captures-started')['started']['tap']", "cest"),
  ("16", "runs/loop2/events.jsonl", "E('loop2', 'capture-done', what='extcap')['seconds']", ".0f"),
  ("05:59:36", "runs/loop2/events.jsonl", "E('loop2', 'captures-started')['started']['extcap']", "cest"))
A("| Peer AAF to the peer's STREAM_INPUT 0, `loop1` and `loop2` |",
  ("0205022001006000", "runs/loop1/events.jsonl", "same(E(r, 'format-check', talker='peer-out-0')['talker_fmt'] for r in ('loop1', 'loop2'))", "s"),
  ("0205022002006000", "runs/loop1/events.jsonl", "same(E(r, 'format-check', talker='peer-out-0')['listener_fmt'] for r in ('loop1', 'loop2'))", "s"),
  ("0205022001006000", "runs/loop1/events.jsonl", "same(E(r, 'format-check', talker='peer-out-0')['set']['fmt'] for r in ('loop1', 'loop2'))", "s"),
  ("0205022001006000", "runs/loop1/events.jsonl", "same(E(r, 'format-check', talker='peer-out-0')['listener_after'] for r in ('loop1', 'loop2'))", "s"))
A("| DUT AAF to the peer's STREAM_INPUT 0, the as-found bind remade |",
  ("0205022002006000", "runs/loop1/events.jsonl", "same(E(r, 'format-check', listener='peer-in-0', set=None, talker='020000fffe000001-out-0')['talker_fmt'] for r in ('loop1', 'loop2'))", "s"),
  ("0205022002006000", "runs/loop1/events.jsonl", "same(E(r, 'format-check', listener='peer-in-0', set=None, talker='020000fffe000001-out-0')['listener_fmt'] for r in ('loop1', 'loop2'))", "s"))
A("(share of the channel's power within 5 Hz of a tone above 0.9) with one change.",
  ("5", "tools/tone_points_b16.py", "rx('tools/tone_points_b16.py', r'\\(fr > t - (\\d+)\\)')", "s"),
  ("0.9", "tools/tone_points_b16.py", "rx('tools/tone_points_b16.py', r'if share > ([\\d.]+) and lvl >= LEVEL_FLOOR_DBFS')", "s"),
  ("one", "tools/tone_points_b16.py", "b15_changes()", "w"))
A("The level floor is -100 dBFS instead of -40 dBFS",
  ("-100", "tools/tone_points_b16.py", "Decimal(rx('tools/tone_points_b16.py', r'^LEVEL_FLOOR_DBFS = (-?[\\d.]+)'))", "d"),
  ("-40", "tools/tone_points_b15.py", "rx('tools/tone_points_b15.py', r'and lvl > (-?\\d+)')", "s"))
A("source at about -38.5 dBFS and a converted tone could sit below -40 dBFS.",
  ("-38.5", "r2/source-receipt.json", "get(d, 'reads.b16-meters-1.meters.the documented pair of outputs.0.leaving_dbfs.0')", ".1f"),
  ("-40", "tools/tone_points_b16.py", "rx('tools/tone_points_b16.py', r'if lvl < (-?\\d+):')", "s"))
A("A channel present between -100 and -40 dBFS is flagged",
  ("-100", "tools/tone_points_b16.py", "Decimal(rx('tools/tone_points_b16.py', r'^LEVEL_FLOOR_DBFS = (-?[\\d.]+)'))", "d"),
  ("-40", "tools/tone_points_b16.py", "rx('tools/tone_points_b16.py', r'if lvl < (-?\\d+):')", "s"))
# ---------------- B16: the loopback
A("The peer's listener, polled every 2 s after the bind:",
  ("2", "runs/loop1/events.jsonl", f"same(round(statistics.median(b['dt'] - a['dt'] for a, b in zip(ev(r, 'listener-poll'), ev(r, 'listener-poll')[1:]) if b['tag'] == a['tag'])) for r in ('loop1', 'loop2'))", "d"), c="B16: the loopback")
A("| `loop1` | 14, over 12 s after the bind and 12 s after the captures |",
  ("14", "runs/loop1/events.jsonl", "len(ev('loop1', 'listener-poll'))", "d"),
  ("12", "runs/loop1/events.jsonl", "round(max(x['dt'] for x in ev('loop1', 'listener-poll', tag='after-loop-bind')))", "d"),
  ("12", "runs/loop1/events.jsonl", "round(max(x['dt'] for x in ev('loop1', 'listener-poll', tag='after-captures')))", "d"),
  ("0000000000000000", "runs/loop1/events.jsonl", "same(x['rx']['stream_id'] for x in ev('loop1', 'listener-poll'))", "s"),
  ("000000000000", "runs/loop1/events.jsonl", "same(x['rx']['dmac'] for x in ev('loop1', 'listener-poll'))", "s"),
  ("0x0002", "runs/loop1/events.jsonl", "same(x['rx']['flags'] for x in ev('loop1', 'listener-poll'))", "s"),
  ("| «0» at every read |", "runs/loop1/events.jsonl", "same(x['peer_tx0']['conn_count'] for x in ev('loop1', 'listener-poll'))", "d"),
  ("| «0», 0 at every", "runs/loop1/events.jsonl", "same([x['media_locked'] for x in ev('loop1', 'listener-poll')] + [ctrs(c)[0] for c in ev('loop1', 'counters', who='peer')])", "d"),
  ("0, «0» at every", "runs/loop1/events.jsonl", "same([x['frames_rx'] for x in ev('loop1', 'listener-poll')] + [ctrs(c)[11] for c in ev('loop1', 'counters', who='peer')])", "d"))
A("| `loop2` | 14, likewise |",
  ("14", "runs/loop2/events.jsonl", "len(ev('loop2', 'listener-poll'))", "d"))
A("The bind itself answered SUCCESS with connection count 1.",
  ("1", "runs/loop1/events.jsonl", "same(E(r, 'bind', talker='peer-out-0')['conn_count'] for r in ('loop1', 'loop2'))", "d"))
A("count stayed 0.",
  ("0", "runs/loop1/events.jsonl", f"same(x['peer_tx0']['conn_count'] for x in {POLL})", "d"))
A("| 0.0 | Controller to the peer | UNBIND_RX command |",
  ("0.0", ACMP, f"({T_UNBIND} - {T_UNBIND}) * 1000", ".1f"))
A("| 0.0 | The peer | UNBIND_RX response |",
  ("0.0", ACMP, f"({acmp_t('DISCONNECT_RX_RESPONSE')} - {T_UNBIND}) * 1000", ".1f"),
  ("count «0» |", ACMP, "get(d, 'acmp.msg=DISCONNECT_RX_RESPONSE')['conn_count']", "d"))
A("| 0.1 | Controller to the peer | BIND_RX command |",
  ("0.1", ACMP, f"({acmp_t('CONNECT_RX_COMMAND')} - {T_UNBIND}) * 1000", ".1f"))
A("| 99.6 | The peer | BIND_RX response |",
  ("99.6", ACMP, f"({acmp_t('CONNECT_RX_RESPONSE')} - {T_UNBIND}) * 1000", ".1f"),
  ("count «1»,", ACMP, "get(d, 'acmp.msg=CONNECT_RX_RESPONSE')['conn_count']", "d"),
  ("stream ID «0» |", ACMP, "int(get(d, 'acmp.msg=CONNECT_RX_RESPONSE')['stream_id'], 16)", "d"))
A("| 99.6 | The peer, to the network | PROBE_TX command |",
  ("99.6", ACMP, f"({acmp_t('CONNECT_TX_COMMAND')} - {T_UNBIND}) * 1000", ".1f"))
A("| 299.6 | The peer, to the network | PROBE_TX command, again |",
  ("299.6", ACMP, f"({acmp_t('CONNECT_TX_COMMAND', 1)} - {T_UNBIND}) * 1000", ".1f"))
A("further probe appear in the rest of the capture",
  ("49.6", ACMP, f"E('loop2', 'capture-done', what='tap')['seconds'] - {acmp_t('CONNECT_TX_COMMAND', 1)}", ".1f"))

FIND = "repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
SRC = "r2/source-receipt.json"
def srcv(reads, role, field, ch=(0, 1)):
    """One value over the named reads' meter rows of a role (every reading of both channels)."""
    return f"meter({reads!r}, {role!r}, {field!r})"
B16M = ("b16-meters-1", "b16-meters-2", "b16-state-2")
A("| `loop1` | The peer's link, its talker stream | 0 PDUs;",
  ("0", "summary/loop1/a-peer-tap.json", "d['info']['pdus']", "d"), c="B16: the four points of the loopback")
A("| `loop1` | The DUT's link, the peer's talker stream | 0 PDUs |",
  ("0", "summary/loop1/b-dut-tap.json", "d['info']['pdus']", "d"))
A("| `loop1` | The external capture, the peer's digital output |",
  ("two", "summary/loop1/d-extcap-pair.json", "sum(1 for r in d['rows'] if r['nonzero'] == 0)", "w"),
  ("1,056,000", "summary/loop1/d-extcap-pair.json", "same(r['frames'] for r in d['rows'])", ",d"))
A("| `loop2` | The peer's link, its talker stream | 0 PDUs;",
  ("0", "summary/loop2/a-peer-tap.json", "d['info']['pdus']", "d"))
A("| `loop2` | The DUT's link, the peer's talker stream | 0 PDUs |",
  ("0", "summary/loop2/b-dut-tap.json", "d['info']['pdus']", "d"))
A("| `loop2` | The external capture, the peer's digital output |",
  ("two", "summary/loop2/d-extcap-pair.json", "sum(1 for r in d['rows'] if r['nonzero'] == 0)", "w"),
  ("768,000", "summary/loop2/d-extcap-pair.json", "same(r['frames'] for r in d['rows'])", ",d"))
A("record shows the same: its counters stayed 0 and its output read exact zero. That lane",
  ("0", FIND, "rx(FIND_P, r'nothing\\. Its counters stayed (\\d+) and its digital output read exact zero')", "s"))
# ---------------- B16: the tone source, read only
A("at 05:47 and 06:01 CEST. The two reads are identical.",
  ("05:47", SRC, "Decimal(clock(get(d, 'reads.b16-state-1.at')))", "hm"),
  ("06:01", SRC, "Decimal(clock(get(d, 'reads.b16-state-2.at')))", "hm"), c="B16: the tone source, read only")
A("| The pair the documented wiring uses | -20.0 dBFS on each |",
  ("-20.0", SRC, srcv(B16M, "the documented pair of outputs", "before_setting_dbfs"), ".1f"),
  ("-18.5", SRC, "same(v for k in ('b16-state-1', 'b16-state-2') for v in get(d, 'reads.' + k + '.level_settings_db.the documented pair of outputs'))", ".1f"),
  ("-38.5", SRC, srcv(B16M, "the documented pair of outputs", "leaving_dbfs"), ".1f"))
A("| A second pair | -20.0 dBFS on each | +6.0 dB |",
  ("-20.0", SRC, srcv(B16M, "the second pair of outputs", "before_setting_dbfs"), ".1f"),
  ("+6.0", SRC, "same(v for k in ('b16-state-1', 'b16-state-2') for v in get(d, 'reads.' + k + '.level_settings_db.the second pair of outputs'))", "+.1f"),
  ("-14.0", SRC, srcv(B16M, "the second pair of outputs", "leaving_dbfs"), ".1f"))
A("| Every other output | Silent: no reading above -135.2 dBFS |",
  ("-135.2", SRC, "max(get(d, 'reads.' + k + '.meters.every other output.largest_before_setting_dbfs') for k in ('b16-state-1', 'b16-meters-1', 'b16-meters-2', 'b16-state-2'))", ".1f"),
  ("-147.6", SRC, "max(get(d, 'reads.' + k + '.meters.every other output.largest_leaving_dbfs') for k in ('b16-state-1', 'b16-meters-1', 'b16-meters-2', 'b16-state-2'))", ".1f"))
A("The playback reads -20.0 dBFS, so it reaches the documented pair at 0 dB, as",
  ("-20.0", SRC, srcv(B16M, "the tone's playback channels", "leaving_dbfs"), ".1f"),
  ("0", SRC, srcv(B16M, "the documented pair of outputs", "before_setting_dbfs") + " - " + srcv(B16M, "the tone's playback channels", "leaving_dbfs"), ".0f"))
A("The two state reads hold 2,262 entries each, all equal.",
  ("two", SRC, "sum(1 for k, r in d['reads'].items() if k.startswith('b16-') and r['kind'] == 'state')", "w"),
  ("2,262", SRC, "same(get(d, 'compare.0.entries') + [get(d, 'compare.0.both')])", ",d"))
A("This is the per-channel record the assignment asks for: the source's two",
  ("two", SRC, "len(get(d, 'reads.b16-meters-1.meters.the documented pair of outputs'))", "w"))
A("documented outputs carry the tone at -38.5 dBFS. The peer's output, its talker",
  ("-38.5", SRC, srcv(B16M, "the documented pair of outputs", "leaving_dbfs"), ".1f"))
# ---------------- B16: the controls
TAPC = "controls/b16-tap-controls.json"
ALC = "controls/b16-align-controls-synth.json"
A("| `b6_thdn.py controls` | Byte-equal to lane B15's `controls.json`,",
  ("7bbefc71...", "controls/controls.json", "sha('controls/controls.json')[:8] + '...'", "s"), c="B16: the controls")
A("| `b9_thdn.py controls` | Byte-equal to lane B15's `b9-controls.json`,",
  ("728a4f0e...", "controls/b9-controls.json", "sha('controls/b9-controls.json')[:8] + '...'", "s"))
A("| `tone_points_b16.py control`: lane B15's five controls | PASS, 5 of 5,",
  ("five", TAPC, "sum(1 for c in d['controls'] if 'lane B16' not in c['control'])", "w"),
  ("«5» of 5", TAPC, "sum(1 for c in d['controls'] if 'lane B16' not in c['control'] and c['result'] == 'PASS')", "d"),
  ("5 of «5»", TAPC, "sum(1 for c in d['controls'] if 'lane B16' not in c['control'])", "d"))
A("| The same, new: the tone pair at -60 dBFS on a one-LSB floor |",
  ("-60", TAPC, "same(get(d, 'controls.control=tone pair at -60 dBFS on the floor (lane B16)')['levels'])", "d"),
  ("-60.00", TAPC, "same(get(d, 'controls.control=tone pair at -60 dBFS on the floor (lane B16)')['levels'])", ".2f"))
A("| The same, new: a -130 dBFS tone alone |",
  ("-130", TAPC, "get(d, 'controls.control=-130 dBFS tone alone (lane B16)')['level']", "d"),
  ("1.0", TAPC, "same(get(d, 'controls.control=-130 dBFS tone alone (lane B16)')['share'])", ".1f"))
A("| The same, new: eight channels with the tone pair on channels 5 and 6 |",
  ("eight", "tools/tone_points_b16.py", "rx('tools/tone_points_b16.py', r'synth_pcap\\(p, sid, (\\d+), 2 \\* FS, \\(5, 6\\)\\)')", "w"),
  ("5", TAPC, "get(d, 'controls.control=eight channels, tone on 5/6 (lane B16)')['tone_channels']['997'][0]", "d"),
  ("6", TAPC, "get(d, 'controls.control=eight channels, tone on 5/6 (lane B16)')['tone_channels']['9973'][0]", "d"))
A("| `align_b16.py control synth`: lane B15's five planted cases",
  ("five", ALC, "sum(1 for c in d['controls'] if 'lane B16' not in c['control'])", "w"),
  ("«5» of 5", ALC, "sum(1 for c in d['controls'] if 'lane B16' not in c['control'] and c['result'] == 'PASS')", "d"),
  ("5 of «5»", ALC, "sum(1 for c in d['controls'] if 'lane B16' not in c['control'])", "d"))
A("| The same, new: one sample changed by +256 LSB, its low byte unchanged |",
  ("one", ALC, "re.search(r'^(\\w+) sample changed by \\+256', d['controls'][5]['control']).group(1) == 'one' and 1", "w"),
  ("+256", ALC, "re.search(r'by (\\+\\d+) LSB', d['controls'][5]['control']).group(1)", "s"),
  ("One", ALC, "d['controls'][5]['frames_differing']", "W"))

# ---------------- B16: bench as left
A("| DUT stream state | Unbound; STREAM_INPUT 0, at `0205022001006000`; both maps as found;",
  ("0205022001006000", "restore/census-end.jsonl", "cen('restore/census-end.jsonl', 'format-dut-5-0')['payload'][8:]", "s"),
  ("CLOCK_SOURCE «0»,", "restore/census-end.jsonl", "payload_word(cen('restore/census-end.jsonl', 'clock', 'dut'), 8)", "d"), c="B16: bench as left")
A("| Reference peer | Its STREAM_INPUT 0, bound to the DUT's AAF talker, at `0205022002006000`",
  ("0205022002006000", "restore/census-end.jsonl", "cen('restore/census-end.jsonl', 'format-peer-5-0')['payload'][8:]", "s"))
A("| Census, start against end | 44 of 45 reads equal, the census's start record aside; the other is the DUT's live propagation delay, 387 to 377 ns |",
  ("44", "", CR("census-start", "census-end", "census-compare", 0), "d"),
  ("45", "", CR("census-start", "census-end", "census-compare", 1), "d"),
  ("387", "restore/census-compare.txt", "int(rx('restore/census-compare.txt', r'<gm-id>([0-9a-f]{8})', 0), 16)", "d"),
  ("377", "restore/census-compare.txt", "int(rx('restore/census-compare.txt', r'<gm-id>([0-9a-f]{8})', 1), 16)", "d"))
A("| DUT saved state | NVM image seq 276, 42 commits, `pend=0`, `VD_OK`, unchanged: the DUT was not bound |",
  ("276", "restore/dut-end.txt", "nvm('restore/dut-end.txt')['seq']", "d"),
  ("42", "restore/dut-end.txt", "nvm('restore/dut-end.txt')['commits']", "d"),
  ("0", "restore/dut-end.txt", "nvm('restore/dut-end.txt')['pend']", "d"))
A("| The tone | Stopped by its process ID at 06:01:59 CEST; the playback closed |",
  ("06:01:59", "runs/tone-stop.txt", "stamps('runs/tone-stop.txt', 'LOCK')[0]", "cest"))
A("- **The DUT's AAF talker** counted two more stream stops and starts, one per",
  ("two", "restore/counters-end.jsonl", "same(counters('restore/counters-end.jsonl', 'dut', 6, 0)[i] - counters('restore/counters-start.jsonl', 'dut', 6, 0)[i] for i in (0, 1))", "w"),
  ("one", "restore/counters-end.jsonl", "same(counters('restore/counters-end.jsonl', 'dut', 6, 0)[i] - counters('restore/counters-start.jsonl', 'dut', 6, 0)[i] for i in (0, 1)) // sum(1 for r in RUNS for b in ev(r, 'bind') if b['listener'] == 'peer-in-0')", "w"))
A("- **`SLIP_LB`** read 152 dups at both ends, unchanged.",
  ("152", "restore/dut-end.txt", "same(le32(mem(f, '0x900008d4', 12)) & 0xffff for f in ('restore/dut-start.txt', 'restore/dut-end.txt'))", "d"))
# ---------------- B16: limits
A("- Two loopback runs, each about a minute, on this bench's reference peer only.",
  ("Two", "runs/loop1/events.jsonl", "sum(1 for r in RUNS for b in ev(r, 'bind') if b['talker'] == 'peer-out-0' and b['listener'] == 'peer-in-0')", "W"), c="B16: limits")


def GEN(doc, s, e):
    """Hash tables: one row per byte count and SHA-256."""
    out = []
    ev_row = re.compile(r"^\| `([^`]+)`[^|]*\| ([\d,]+) \| `([0-9a-f]{64})` \|$")
    raw_row = re.compile(r"^\| ((?:`[^`]+`(?:, )?)+)[^|]*\| `([^`]+)`[^|]*\| ([^|]+) \| `([0-9a-f]{64})` \|$")
    src_row = re.compile(r"^\| `(b16[a-z]?-(?:state|meters)-\d)\.json`[^|]*\| ([\d:]+) \| `([0-9a-f]{64})` \|$")
    for i in range(s, e):
        line = doc[i].strip()
        m = ev_row.match(line)
        if m:
            p = m.group(1)
            out.append((i + 1, [(m.group(2), p, "size(p)", ",d"), (m.group(3), p, "sha(p)", "s")]))
            continue
        m = raw_row.match(line)
        if m:
            runs = re.findall(r"`([^`]+)`", m.group(1)); f = m.group(2)
            rows = []
            if m.group(3).strip() != "Withheld":
                rows.append((m.group(3).strip(), "RAW-ARTIFACTS.json", f"same(raw(r + '/{f}')['bytes'] for r in {runs!r})", ",d"))
            rows.append((m.group(4), "RAW-ARTIFACTS.json", f"same(raw(r + '/{f}')['sha256'] for r in {runs!r})", "s"))
            out.append((i + 1, rows))
            continue
        m = src_row.match(line)
        if m:
            k = m.group(1)
            out.append((i + 1, [(m.group(2), "r2/source-receipt.json", f"get(d, 'reads.{k}.at')", "s"),
                                (m.group(3), "RAW-ARTIFACTS.json", f"same([raw('source/{k}.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.{k}.sha256')])", "s")]))
    return out


def prec(shown, signed=False, z=False):
    """The displayed precision of a figure: decimals, thousands separator, sign."""
    t = shown.lstrip("+-")
    n = len(t.split(".")[1]) if "." in t else 0
    return ("+" if shown.startswith("+") or signed else "") + ("z" if z else "") + ("," if "," in t else "") + (f".{n}f" if n else "d")


PFILE = {"(a)": "a-peer-tap", "(b)": "b-dut-tap", "(c)": "c-mcasp"}


def GEN2(doc, s, e):
    """The point tables (b16b-points, b16c-points) and the grade tables (b16b-b0, b16c-grade)."""
    out, mark = [], None
    for i in range(s, e):
        line = doc[i].strip()
        if line.startswith("<!-- "):
            mark = line; continue
        if not line.startswith("|") or line.startswith("|---") or line.startswith("| Run |") or line.startswith("| Tone |"):
            if not line:
                mark = None
            continue
        c = [x.strip() for x in line.strip("|").split("|")]
        rows = []
        if mark in ("<!-- b16b-points -->", "<!-- b16c-points -->"):
            run = re.match(r"`([^`]+)`", c[0]).group(1); p = c[1]; f = f"summary/{run}/{PFILE[p]}.json"
            fr = re.findall(r"\d{1,3}(?:,\d{3})*", c[2])
            rows.append((fr[0], f, "d['frames']", ",d"))
            if p != "(c)":
                rows.append((fr[1], f, "d['info']['pdus']", ",d"))
                rows.append((fr[2], f, "d['info']['seq_gaps']", "d"))
            rows.append((c[3], f, "T(d, 0, 'level_dbfs')", prec(c[3])))
            for (ch, tone), k in zip(((0, 997), (1, 9973)), (4, 7)):
                fz, ppm = re.match(r"([\d,.]+) Hz, ([-+\d.]+) ppm", c[k]).groups()
                th, wo = re.match(r"(-[\d.]+) \((-[\d.]+)\)", c[k + 1]).groups()
                rows += [(fz, f, f"T(d, {ch}, 'f_hz')", prec(fz)), (ppm, f, f"T(d, {ch}, 'ppm')", prec(ppm, z=True)),
                         (th, f, f"T(d, {ch}, 'thdn_db')", prec(th)), (wo, f, f"T(d, {ch}, 'worst')", prec(wo)),
                         (c[k + 2], f, f"T(d, {ch}, 'snr_db')", prec(c[k + 2]))]
        elif mark in ("<!-- b16b-b0 -->", "<!-- b16c-grade -->"):
            if mark == "<!-- b16b-b0 -->":
                run, c = "b0-2", c
            else:
                run, c = re.match(r"`([^`]+)`", c[0]).group(1), c[1:]
            f = f"summary/{run}/c-b9-grade.json"
            ch = "ch0" if c[0].startswith("997 Hz") else "ch1"
            fl, fw = re.match(r"(-[\d.]+) \((-[\d.]+)\)", c[4]).groups()
            al, aw = re.match(r"(-[\d.]+) \((-[\d.]+)\)", c[6]).groups()
            lv = re.match(r"(-[\d.]+) dBFS", c[7]).group(1)
            om, ox = re.match(r"([-\d.]+) \(([\d.]+)\)", c[8]).groups()
            rows += [(c[1], f, "d['summary']['blocks']", "d"), (f"| {c[1]} | «{c[2]}» | {c[3]} |", f, "d['summary']['events']", "d"),
                     (c[3], f, "d['summary']['blocks_at_floor']", "d"),
                     (fl, f, f"d['summary']['{ch}_floor']['thdn_db_median']", prec(fl)),
                     (fw, f, f"d['summary']['{ch}_floor']['thdn_db_worst']", prec(fw)),
                     (c[5], f, f"d['summary']['{ch}_floor']['snr_db_median']", prec(c[5])),
                     (al, f, f"d['summary']['{ch}_all']['thdn_db_median']", prec(al)),
                     (aw, f, f"d['summary']['{ch}_all']['thdn_db_worst']", prec(aw)),
                     (lv, f, f"d['summary']['{ch}_all']['level_dbfs_median']", prec(lv)),
                     (om, f, f"d['summary']['{ch}_all']['ppm_median']", prec(om, z=True)),
                     (ox, f, f"d['summary']['{ch}_all']['ppm_maxabs']", prec(ox))]
        if rows:
            out.append((i + 1, rows))
    return out

# ---------------- B16b: the resume
B16B = ("pts1", "pts2", "b0", "b0-2", "pts3")
LVL = "T(load(f'summary/{r}/a-peer-tap.json'), 0, 'level_dbfs')"
A("branch and head, `694d7da6`; the first bench action was at 06:22:23 CEST.",
  ("06:22:23", "soc/b16b-precheck-status.log", "stamps('soc/b16b-precheck-status.log', 'LOCK')[0]", "cest"), c="B16b: the resume")
A("| Identity gate, dev `5603c353`, again | PASS | 06:22:29 to 06:22:34 CEST,",
  ("06:22:29", "identity-b16b/lock-window.txt", "stamps('identity-b16b/lock-window.txt', 'LOCK')[0]", "cest"),
  ("06:22:34", "identity-b16b/lock-window.txt", "stamps('identity-b16b/lock-window.txt', 'UNLOCK')[0]", "cest"),
  ("44", "", CR("census-end", "census-startb", "census-compare-b16-to-b16b", 0), "d"),
  ("45", "", CR("census-end", "census-startb", "census-compare-b16-to-b16b", 1), "d"))
A("| (a) The peer's talker stream on the peer's link | TONE PRESENT |",
  ("-14.14", "summary/pts1/a-peer-tap.json", f"same({LVL} for r in ('pts1', 'pts2'))", ".2f"),
  ("06:28:50", "summary/pts2/a-peer-tap.json", "d['info']['last_t']", "cest"),
  ("-14.10", "summary/b0/a-peer-tap.json", f"same({LVL} for r in ('b0', 'b0-2', 'pts3'))", ".2f"),
  ("06:31:51", "summary/b0/a-peer-tap.json", "d['info']['first_t']", "cest"))
A("| (b) The same stream on the DUT's link | TONE PRESENT | Equal to (a), 0 sequence gaps on both taps |",
  ("0", "summary/pts1/a-peer-tap.json", "same(load(f'summary/{r}/{p}.json')['info']['seq_gaps'] for r in ('pts1', 'pts2', 'pts3', 'b0-2') for p in ('a-peer-tap', 'b-dut-tap'))", "d"))
A("| (c) The DUT's TDM output on McASP0 | TONE PRESENT |",
  ("«480,000» of", "summary/pts1/align-a-c.json", "same(align(r, p)['compared_equal'] for r in ('pts1', 'pts2', 'pts3') for p in 'ab')", ",d"),
  ("of «480,000»", "summary/pts1/align-a-c.json", "same(align(r, p)['mcasp_frames'] for r in ('pts1', 'pts2', 'pts3') for p in 'ab')", ",d"),
  ("three", "summary/pts1/align-a-c.json", "sum(1 for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') if (ROOT / f'summary/{r}/align-a-c.json').exists() and align(r, 'a')['mcasp_frames'] == 480000)", "w"),
  ("34.1", "r2/b0-2-receipt.json", "d['overlap']['seconds']", ".1f"),
  ("«0» slips", "summary/pts1/align-a-c.json", "same(len(align(r, p)['slips']) for r in ('pts1', 'pts2', 'pts3', 'b0-2') for p in 'ab')", "d"))
A("| (d) The positive control at the external capture | PRESENT |",
  ("-1.00", "summary/pts2/d-extcap-pair.json", "same(r['tone_' + t]['median']['level_dbfs'] for x in ('pts2', 'b0-2') for r, t in zip(load(f'summary/{x}/d-extcap-pair.json')['rows'], ('997', '9973')))", ".2f"),
  ("303.8", "summary/b0-2/d-loop-decode.json", "d['decoded'] / 48000", ".1f"),
  ("two", "summary/pts2/d-loop-decode.json", "load('summary/pts2/d-loop-decode.json')['repeats']", "w"),
  ("2", "summary/pts2/d-loop-decode.json", "same(e['frames'] for e in load('summary/pts2/d-loop-decode.json')['events'])", "d"))
A("| The tone source, read only | Changed during the lane, outside it | Its clock setting changed between 06:23 and 06:50 CEST",
  ("06:23", SRC, "Decimal(clock(get(d, 'reads.b16b-state-1.at')))", "hm"),
  ("06:50", SRC, "Decimal(clock(get(d, 'reads.b16b-state-2.at')))", "hm"))
G02 = "summary/b0-2/c-b9-grade.json"
A("| Step 4, B0: the DUT on INTERNAL | Graded |",
  ("-123.95", G02, "d['summary']['ch0_all']['thdn_db_median']", ".2f"),
  ("-122.80", G02, "d['summary']['ch1_all']['thdn_db_median']", ".2f"),
  ("300", G02, "d['summary']['blocks']", "d"),
  ("«0» discontinuities", G02, "d['summary']['events']", "d"),
  ("0.0000", G02, "d['summary']['effective_offset_ppm']", "z.4f"),
  ("34.1", "r2/b0-2-receipt.json", "d['overlap']['seconds']", ".1f"))
# ---------------- B16b: method
A("Each run is one locked action of `run_b16.py` through `run_locked_b16.sh`. The",
  ("one", "runs/pts1-lock.txt", f"same(len(stamps(f'runs/{{r}}-lock.txt', 'LOCK')) for r in {B16B!r})", "w"), c="B16b: method")
A("| `pts1` | `dirb` |",
  ("06:23:39", "runs/pts1-lock.txt", "stamps('runs/pts1-lock.txt', 'LOCK')[0]", "cest"),
  ("06:24:28", "runs/pts1-lock.txt", "stamps('runs/pts1-lock.txt', 'UNLOCK')[0]", "cest"),
  ("06:23:46", "runs/pts1/events.jsonl", "E('pts1', 'bind')['t']", "cest"),
  ("24.5", "runs/pts1/events.jsonl", "E('pts1', 'capture-done', what='tap')['seconds']", ".1f"),
  ("06:23:58", "runs/pts1/events.jsonl", "E('pts1', 'captures-started')['started']['tap']", "cest"),
  ("16", "runs/pts1/events.jsonl", "E('pts1', 'capture-done', what='extcap')['seconds']", ".0f"),
  ("10", "summary/pts1/c-mcasp.json", "d['seconds']", ".0f"),
  ("06:24:02", "runs/pts1/events.jsonl", "E('pts1', 'captures-started')['started']['mcasp']", "cest"))
A("| `pts2` | `dira` |",
  ("06:28:06", "runs/pts2-lock.txt", "stamps('runs/pts2-lock.txt', 'LOCK')[0]", "cest"),
  ("06:28:56", "runs/pts2-lock.txt", "stamps('runs/pts2-lock.txt', 'UNLOCK')[0]", "cest"),
  ("06:28:13", "runs/pts2/events.jsonl", "E('pts2', 'bind')['t']", "cest"),
  ("06:28:25", "runs/pts2/events.jsonl", "E('pts2', 'captures-started')['started']['tap']", "cest"),
  ("«2» s before", "tools/run_b16.py", "r2lead()", "d"),
  ("10", "summary/pts2/c-mcasp.json", "d['seconds']", ".0f"),
  ("06:28:31.5", "runs/pts2/events.jsonl", "E('pts2', 'captures-started')['started']['mcasp'] + r2lead()", "cest1"),
  ("«2» s after", "tools/run_b16.py", "r2lead()", "d"),
  ("06:28:29.5", "runs/pts2/events.jsonl", "E('pts2', 'captures-started')['started']['mcasp']", "cest1"))
A("| `b0` | `b0` |",
  ("06:31:28", "runs/b0-lock.txt", "stamps('runs/b0-lock.txt', 'LOCK')[0]", "cest"),
  ("06:37:05", "runs/b0-lock.txt", "stamps('runs/b0-lock.txt', 'UNLOCK')[0]", "cest"),
  ("06:31:30", "runs/b0/events.jsonl", "E('b0', 'bind', i=-1)['t']", "cest"),
  ("40", "summary/b0/a-peer-tap.json", "d['seconds']", ".0f"),
  ("06:31:50", "runs/b0/events.jsonl", "E('b0', 'captures-started')['started']['tap']", "cest"),
  ("306", "summary/b0/d-loop-decode.json", "d['frames'] / 48000", ".0f"))
A("| `b0-2` | `b0` |",
  ("06:37:31", "runs/b0-2-lock.txt", "stamps('runs/b0-2-lock.txt', 'LOCK')[0]", "cest"),
  ("06:43:17", "runs/b0-2-lock.txt", "stamps('runs/b0-2-lock.txt', 'UNLOCK')[0]", "cest"),
  ("06:37:39", "runs/b0-2/events.jsonl", "E('b0-2', 'bind', i=-1)['t']", "cest"),
  ("40", "summary/b0-2/a-peer-tap.json", "d['seconds']", ".0f"),
  ("06:37:59", "runs/b0-2/events.jsonl", "E('b0-2', 'captures-started')['started']['tap']", "cest"),
  ("306", "summary/b0-2/d-extcap-pair.json", "d['seconds']", ".0f"),
  ("300", "summary/b0-2/c-b9-grade.json", "d['seconds']", ".0f"),
  ("06:38:03.2", "runs/b0-2/events.jsonl", "E('b0-2', 'captures-started')['started']['mcasp']", "cest1"),
  ("2", "tools/run_b16.py", "r2lead()", "d"),
  ("06:38:05.2", "runs/b0-2/events.jsonl", "E('b0-2', 'captures-started')['started']['mcasp'] + r2lead()", "cest1"))
A("| `pts3` | `dirb` |",
  ("06:48:55", "runs/pts3-lock.txt", "stamps('runs/pts3-lock.txt', 'LOCK')[0]", "cest"),
  ("06:49:45", "runs/pts3-lock.txt", "stamps('runs/pts3-lock.txt', 'UNLOCK')[0]", "cest"),
  ("06:49:02", "runs/pts3/events.jsonl", "E('pts3', 'bind')['t']", "cest"),
  ("06:49:14", "runs/pts3/events.jsonl", "E('pts3', 'captures-started')['started']['tap']", "cest"))
A("as found. The DUT's eight identity mappings on STREAM_PORT_OUTPUT 0 and four on",
  ("eight", "restore/census-startb.jsonl", "identity_maps(cen('restore/census-startb.jsonl', 'map-dut-0x000f-0-0'))", "w"),
  ("four", "restore/census-startb.jsonl", "identity_maps(cen('restore/census-startb.jsonl', 'map-dut-0x000e-0-0'))", "w"))
A("SHA-256: `566d3dfa...`) was copied to the board, checked there and removed after",
  ("566d3dfa...", "runs/pts2/events.jsonl", "same(E(r, 'loop-staged')['sha256'] for r in ('pts2', 'b0', 'b0-2'))[:8] + '...'", "s"))
A("talker's, so none was set: `0205022001006000` on the DUT's STREAM_INPUT 0 and",
  ("0205022001006000", "runs/pts1/events.jsonl", f"same(x['listener_fmt'] for r in {B16B!r} for x in ev(r, 'format-check', listener='dut-in-0') if x['set'] is None and x['talker_fmt'] == x['listener_fmt'])", "s"))
A("`041060010000bb80` on its STREAM_INPUT 1. Every bind and unbind answered",
  ("041060010000bb80", "runs/b0/events.jsonl", "same(x['listener_fmt'] for r in ('b0', 'b0-2') for x in ev(r, 'format-check', listener='dut-in-1') if x['set'] is None and x['talker_fmt'] == x['listener_fmt'])", "s"), n=0)
A("0, INTERNAL, before and after each window of B0. Each run ended with every format, clock",
  ("0", "runs/b0/events.jsonl", "same(x['source'] for r in ('b0', 'b0-2') for x in ev(r, 'clock-read', who='dut'))", "d"))
A("path's own: an event-free block within 3 dB of the median. `dloop_b16.py`",
  ("3", "tools/b9_thdn.py", "Decimal(rx('tools/b9_thdn.py', r'^FLOOR_DB = ([\\d.]+)'))", "d"))
A("decodes lane B6's loop at (d) with lane B6's decoder. SNR equals minus THD+N",
  ("0.01", "summary/pts1/a-peer-tap.json", "bound(max(abs(t['median']['snr_db'] + t['median']['thdn_db']) for r in ('pts1', 'pts2', 'pts3', 'b0-2') for p in PFILE_ for c in (0, 1) for t in [pt(r, p, c, (997, 9973)[c])]), '0.01')", ".2f"), off=1)
A("**B0's window** is 300 s, not lane B7's 630 s, because one locked action",
  ("300", G02, "d['seconds']", ".0f"),
  ("630", FIND, "rx(FIND_P, r'^(\\d+) s, untouched, from (\\d+) s after the last bind or clock-source set')", "s"),
  ("one", "runs/b0-2-lock.txt", "len(stamps('runs/b0-2-lock.txt', 'LOCK'))", "w"))
A("must end within 10 minutes. The capture command ran 24.0 s after the last",
  ("24.0", "r2/b0-2-receipt.json", "d['timing']['command_after_binds_s']", ".1f"))
A("bind, and the board played the loop 2 s before it recorded (`run_b16.py`'s mode",
  ("2", "tools/run_b16.py", "r2lead()", "d"))
A("recording starts about 26 s after the last bind, past lane B7's 20 s.",
  ("26", "r2/b0-2-receipt.json", "d['timing']['recording_after_binds_s']", ".0f"),
  ("20", FIND, "rx(FIND_P, r'^(\\d+) s, untouched, from (\\d+) s after the last bind or clock-source set', group=2)", "s"))
A("**One incident.** In `b0` McASP0's recording failed immediately with",
  ("One", "RAW-ARTIFACTS.json", f"sum(1 for r in {B16B!r} if raw(r + '/mcasp-all.raw')['bytes'] == 0)", "W"))

# ---------------- B16b: the four points
PTS_B = ("pts1", "pts2", "pts3", "b0-2")
def idle(runs):
    return (f"[c for r in {runs!r} for p in ('a-peer-tap', 'b-dut-tap', 'c-mcasp') "
            f"for c in load(f'summary/{{r}}/{{p}}.json')['channels'] if c['channel'] in (2, 3)]")
def zero47(runs):
    return (f"same(c['nonzero'] for r in {runs!r} for c in load(f'summary/{{r}}/c-mcasp.json')['channels'] if c['channel'] >= 4)")
# round 6: the idle channels' indices, each bound to the text around it (the closed list refuses "carry")
IDLE_CH = lambda runs, i: (f"same(tuple(c['channel'] for c in load(f'summary/{{r}}/{{p}}.json')['channels'] if c['min'] == -1 "
                       f"and c['max'] == 0) for r in {runs!r} for p in ('a-peer-tap', 'b-dut-tap', 'c-mcasp'))[{i}]")
A("The tone in channels 0 and 1 of the peer's talker stream; channels 2 and 3",
  ("@channels «2» and", "", IDLE_CH(PTS_B, 0), "d", 0), ("@and «3» carry", "", IDLE_CH(PTS_B, 1), "d", 0))
A("carry -1 to 0 LSB at every point, and McASP0's channels 4 to 7, unmapped, are",
  ("-1", "summary/pts1/a-peer-tap.json", f"same(c['min'] for c in {idle(PTS_B)})", "d"),
  ("0", "summary/pts1/a-peer-tap.json", f"same(c['max'] for c in {idle(PTS_B)})", "d"), n=0, c="B16b: the four points")
A("| `pts1`, `pts3` | Its two channels at a constant -1 LSB:",
  ("two", "summary/pts1/d-extcap-pair.json", "same(len(load(f'summary/{r}/d-extcap-pair.json')['rows']) for r in ('pts1', 'pts3'))", "w"),
  ("-1", "summary/pts1/d-extcap-pair.json", "same(v for r in ('pts1', 'pts3') for x in load(f'summary/{r}/d-extcap-pair.json')['rows'] for v in (x['min'], x['max']))", "d"))
DP2 = "summary/pts2/d-extcap-pair.json"
T997, T9973 = "d['rows'][0]['tone_997']", "d['rows'][1]['tone_9973']"
A("| `pts2` | Lane B6's loop at -1.00 dBFS, 997.0000 Hz and 9,973.0000 Hz, 0.000 ppm;",
  ("-1.00", DP2, f"same([{T997}['median']['level_dbfs'], {T9973}['median']['level_dbfs']])", ".2f"),
  ("997.0000", DP2, f"{T997}['median']['f_hz']", ".4f"),
  ("9,973.0000", DP2, f"{T9973}['median']['f_hz']", ",.4f"),
  ("0.000", DP2, f"same(q(t['median']['ppm'], 3) for t in ({T997}, {T9973}))", "z.3f"),
  ("-146.06", DP2, f"{T997}['median']['thdn_db']", ".2f"),
  ("-145.99", DP2, f"{T9973}['median']['thdn_db']", ".2f"),
  ("11", DP2, f"same(len(floor_inside(t)) for t in ({T997}, {T9973}))", "d"),
  ("13", DP2, f"same(len(inside(t['per_block'])) for t in ({T997}, {T9973}))", "d"),
  ("16", DP2, f"same(len(t['per_block']) for t in ({T997}, {T9973}))", "d"),
  ("blocks, «0» and 1", DP2, f"same(silent(t['per_block'])[0] for t in ({T997}, {T9973}))", "d"),
  ("0 and «1» precede", DP2, f"same(silent(t['per_block'])[-1] for t in ({T997}, {T9973}))", "d"),
  ("block «2» holds", DP2, f"same(inside(t['per_block'])[0] - 1 for t in ({T997}, {T9973}))", "d"),
  ("Blocks «6» and", DP2, f"same([i for i in inside(t['per_block']) if i not in floor_inside(t)][0] for t in ({T997}, {T9973}))", "d"),
  ("and «12» each", DP2, f"same([i for i in inside(t['per_block']) if i not in floor_inside(t)][1] for t in ({T997}, {T9973}))", "d"),
  ("of «2» frames", "summary/pts2/d-loop-decode.json", "same(e['frames'] for e in load('summary/pts2/d-loop-decode.json')['events'])", "d"),
  ("6.131", "summary/pts2/d-loop-decode.json", "load('summary/pts2/d-loop-decode.json')['events'][0]['second']", ".3f"),
  ("12.113", "summary/pts2/d-loop-decode.json", "load('summary/pts2/d-loop-decode.json')['events'][1]['second']", ".3f"),
  ("-4", "summary/pts2/d-loop-decode.json", "load('summary/pts2/d-loop-decode.json')['net_step_frames']", "d"),
  ("665,599", "summary/pts2/d-loop-decode.json", "load('summary/pts2/d-loop-decode.json')['decoded']", ",d"),
  ("«0» torn", "summary/pts2/d-loop-decode.json", "load('summary/pts2/d-loop-decode.json')['torn']", "d"))
DB2 = "summary/b0-2/d-extcap-pair.json"
A("| `b0-2` | The loop as in `pts2`, at the floor in all 303 blocks wholly inside the playback;",
  ("303", DB2, f"same(n for t in ({T997}, {T9973}) for n in (len(floor_inside(t)), len(inside(t['per_block']))))", "d"),
  ("306", DB2, f"same(len(t['per_block']) for t in ({T997}, {T9973}))", "d"),
  ("blocks «0» and 1", DB2, f"same(silent(t['per_block'])[0] for t in ({T997}, {T9973}))", "d"),
  ("0 and «1» precede", DB2, f"same(silent(t['per_block'])[-1] for t in ({T997}, {T9973}))", "d"),
  ("block «2» holds", DB2, f"same(inside(t['per_block'])[0] - 1 for t in ({T997}, {T9973}))", "d"),
  ("«0» discontinuities", "summary/b0-2/d-loop-decode.json", "len(load('summary/b0-2/d-loop-decode.json')['events'])", "d"),
  ("«0» torn", "summary/b0-2/d-loop-decode.json", "load('summary/b0-2/d-loop-decode.json')['torn']", "d"),
  ("14,583,286", "summary/b0-2/d-loop-decode.json", "load('summary/b0-2/d-loop-decode.json')['decoded']", ",d"),
  ("14,583,189", "summary/b0/d-loop-decode.json", "load('summary/b0/d-loop-decode.json')['decoded']", ",d"))
TT = "taps2()"
A("In `pts2` both taps carry the DUT's AAF talker with the same loop at -1.00",
  ("-1.00", "summary/pts2/ctl-dut-talker-dut-tap.json", f"same(q(x['median']['level_dbfs'], 2) for x in {TT})", ".2f"))
A("dBFS, THD+N -146.06 dB and -145.99 dB, at the floor in all 15 blocks wholly",
  ("-146.06", "summary/pts2/ctl-dut-talker-dut-tap.json", f"same(q(x['median']['thdn_db'], 2) for x in {TT}[0::2])", ".2f"),
  ("-145.99", "summary/pts2/ctl-dut-talker-dut-tap.json", f"same(q(x['median']['thdn_db'], 2) for x in {TT}[1::2])", ".2f"),
  ("15", "summary/pts2/ctl-dut-talker-dut-tap.json", f"same(n for x in {TT} for n in (len(floor_inside(x)), len(inside(x['per_block']))))", "d"))
A("inside the playback. Of each tap's 23 blocks, 0 to 2 and 20 to 22 hold no",
  ("23", "summary/pts2/ctl-dut-talker-dut-tap.json", f"same(len(x['per_block']) for x in {TT})", "d"),
  ("blocks, «0» to 2 and", "summary/pts2/ctl-dut-talker-dut-tap.json", f"same(runs_of(silent(x['per_block']))[0][0] for x in {TT})", "d"),
  ("blocks, 0 to «2» and", "summary/pts2/ctl-dut-talker-dut-tap.json", f"same(runs_of(silent(x['per_block']))[0][1] for x in {TT})", "d"),
  ("«20» to", "summary/pts2/ctl-dut-talker-dut-tap.json", f"same(runs_of(silent(x['per_block']))[1][0] for x in {TT})", "d"),
  ("to «22»", "summary/pts2/ctl-dut-talker-dut-tap.json", f"same(runs_of(silent(x['per_block']))[1][1] for x in {TT})", "d"))
A("playback, and blocks 3 and 19 hold its start and end. So `pts2`'s two repeats",
  ("3", "summary/pts2/ctl-dut-talker-dut-tap.json", f"same(inside(x['per_block'])[0] - 1 for x in {TT})", "d"),
  ("19", "summary/pts2/ctl-dut-talker-dut-tap.json", f"same(inside(x['per_block'])[-1] + 1 for x in {TT})", "d"),
  ("two", "summary/pts2/d-loop-decode.json", "load('summary/pts2/d-loop-decode.json')['repeats']", "w"))
ALIGN3 = "[align(r, p) for r in ('pts1', 'pts2', 'pts3') for p in 'ab']"
A("| `pts1`, `pts2`, `pts3` | SAMPLE-EXACT in each: 480,000 of 480,000 frames, 0 slips |",
  ("480,000", "summary/pts1/align-b-c.json", f"same(x['compared_equal'] for x in {ALIGN3})", ",d"),
  ("480,000", "summary/pts1/align-b-c.json", f"same(x['mcasp_frames'] for x in {ALIGN3})", ",d"),
  ("0", "summary/pts1/align-b-c.json", f"same(len(x['slips']) for x in {ALIGN3})", "d"),
  ("480,000", "summary/pts1/align-a-c.json", f"same(x['compared_equal'] for x in {ALIGN3})", ",d"),
  ("480,000", "summary/pts1/align-a-c.json", f"same(x['mcasp_frames'] for x in {ALIGN3})", ",d"),
  ("0", "summary/pts1/align-a-c.json", f"same(len(x['slips']) for x in {ALIGN3})", "d"))
A("| `b0-2` | SAMPLE-EXACT over the 1,637,980 recorded frames the tap covers, 34.1 s,",
  ("1,637,980", "summary/b0-2/align-b-c.json", "d['compared_equal']", ",d"),
  ("34.1", "summary/b0-2/align-b-c.json", "d['compared_equal'] / 48000", ".1f"),
  ("«0» differing, 0 slips | SAMPLE-EXACT over 1,637,452", "summary/b0-2/align-b-c.json", "d['frames_differing']", "d"),
  ("0 differing, «0» slips | SAMPLE-EXACT over 1,637,452", "summary/b0-2/align-b-c.json", "len(d['slips'])", "d"),
  ("1,637,452", "summary/b0-2/align-a-c.json", "d['compared_equal']", ",d"),
  ("1,637,452 frames, «34.1» s", "summary/b0-2/align-a-c.json", "d['compared_equal'] / 48000", ".1f"),
  ("1,637,452 frames, 34.1 s, «0» differing", "summary/b0-2/align-a-c.json", "d['frames_differing']", "d"),
  ("1,637,452 frames, 34.1 s, 0 differing, «0» slips", "summary/b0-2/align-a-c.json", "len(d['slips'])", "d"))
B16BM = ("b16b-meters-1", "b16b-meters-2", "b16b-state-2")
A("level at (a), -14.14 dBFS, is the level at which the tone source's meters show",
  ("-14.14", "summary/pts1/a-peer-tap.json", f"same({LVL} for r in ('pts1', 'pts2'))", ".2f"))
A("it leaving the second pair of outputs, -14.0 dBFS. It is not the documented",
  ("-14.0", SRC, srcv(B16BM, "the second pair of outputs", "leaving_dbfs"), ".1f"))
A("pair's -38.5 dBFS. Lane B15's read found that second pair silent. Which input of the",
  ("-38.5", SRC, srcv(B16BM, "the documented pair of outputs", "leaving_dbfs"), ".1f"))
# ---------------- B16b: the tone source changed during the lane
CMP1 = "get(d, 'compare.1')"
A("The tone, lane B15's loop `d9684a8f...`, played from 06:23:26 to 06:52:19 CEST.",
  ("d9684a8f...", "runs/b16b-tone-start.txt", "rx('runs/b16b-tone-start.txt', r'LOOP_SHA256 ([0-9a-f]{8})') + '...'", "s"),
  ("06:23:26", "runs/b16b-tone-start.txt", "stamps('runs/b16b-tone-start.txt', 'STATUS')[0] - Decimal(rx('runs/b16b-tone-start.txt', r'hw_ptr : (\\d+)')) / 48000", "cest"),
  ("06:52:19", "runs/b16b-tone-stop.txt", "stamps('runs/b16b-tone-stop.txt', 'LOCK')[0]", "cest"), c="B16b: the tone source changed during the lane")
A("The source's state was read read-only at 06:23 and 06:50 CEST, and its meters",
  ("06:23", SRC, "Decimal(clock(get(d, 'reads.b16b-state-1.at')))", "hm"),
  ("06:50", SRC, "Decimal(clock(get(d, 'reads.b16b-state-2.at')))", "hm"))
A("-38.5 dBFS leaving the documented pair and -14.0 dBFS leaving the second pair.",
  ("-38.5", SRC, srcv(B16BM, "the documented pair of outputs", "leaving_dbfs"), ".1f"),
  ("-14.0", SRC, srcv(B16BM, "the second pair of outputs", "leaving_dbfs"), ".1f"), n=0)
A("The later state read caught 1,255 of the 2,262 entries the first held. Of the",
  ("1,255", SRC, f"{CMP1}['entries'][1]", ",d"),
  ("2,262", SRC, f"{CMP1}['entries'][0]", ",d"))
A("1,255 both hold, four differ, and this lane wrote none of them:",
  ("1,255", SRC, f"{CMP1}['both']", ",d"),
  ("four", SRC, f"{CMP1}['differ']", "w"))
A("- two inputs of a monitoring mix. These differ only in which messages the",
  ("two", SRC, f"sum(1 for x in {CMP1}['differing'] if x['cls'] == 'an input of a monitoring mix')", "w"))
A("reads caught: the first caught two messages for each address and the second",
  ("two", SRC, f"same(x['messages'][0] for x in {CMP1}['differing'] if x['cls'] == 'an input of a monitoring mix')", "w"))
A("one, which the first also caught. All of them are at minus infinity.",
  ("one", SRC, f"same(x['messages'][1] for x in {CMP1}['differing'] if x['cls'] == 'an input of a monitoring mix' and x['second_last_among_first'] and x['all_minus_infinity'])", "w"))
A("So, among the 1,255 entries both reads hold, two settings changed: the clock",
  ("1,255", SRC, f"{CMP1}['both']", ",d"),
  ("two", SRC, f"sum(1 for x in {CMP1}['differing'] if x['cls'] != 'an input of a monitoring mix')", "w"))
A("1,007. The reduced receipt `r2/source-receipt.json` carries these counts and",
  ("1,007", SRC, f"{CMP1}['entries'][0] - {CMP1}['both']", ",d"))
A("| `pts1`, `pts2`, to 06:28:50 | -14.1353 dBFS |",
  ("06:28:50", "summary/pts2/a-peer-tap.json", "d['info']['last_t']", "cest"),
  ("-14.1353", "summary/pts1/a-peer-tap.json", f"same({LVL} for r in ('pts1', 'pts2'))", ".4f"),
  ("+6.94", "summary/pts1/a-peer-tap.json", "min(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))", "+.2f"),
  ("+6.96", "summary/pts1/a-peer-tap.json", "max(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))", "+.2f"),
  ("-109.68", "summary/pts1/c-b9-grade.json", "load('summary/pts1/c-b9-grade.json')['summary']['ch0_floor']['thdn_db_median']", ".2f"),
  ("-111.26", "summary/pts2/c-b9-grade.json", "load('summary/pts2/c-b9-grade.json')['summary']['ch0_floor']['thdn_db_median']", ".2f"),
  ("-89.83", "summary/pts1/c-b9-grade.json", "load('summary/pts1/c-b9-grade.json')['summary']['ch1_floor']['thdn_db_median']", ".2f"),
  ("-91.51", "summary/pts2/c-b9-grade.json", "load('summary/pts2/c-b9-grade.json')['summary']['ch1_floor']['thdn_db_median']", ".2f"),
  ("+3.00", "summary/pts1/c-b9-grade.json", "load('summary/pts1/c-b9-grade.json')['phase_net_frames']", "+.2f"),
  ("+3.01", "summary/pts2/c-b9-grade.json", "load('summary/pts2/c-b9-grade.json')['phase_net_frames']", "+.2f"),
  ("10", "summary/pts1/c-b9-grade.json", "same(grade(r)['seconds'] for r in ('pts1', 'pts2'))", ".0f"),
  ("Two", "summary/pts2/d-loop-decode.json", "load('summary/pts2/d-loop-decode.json')['repeats']", "W"),
  ("2", "summary/pts2/d-loop-decode.json", "same(e['frames'] for e in load('summary/pts2/d-loop-decode.json')['events'])", "d"),
  ("13.9", "summary/pts2/d-loop-decode.json", "load('summary/pts2/d-loop-decode.json')['decoded'] / 48000", ".1f"))
A("| `b0`, `b0-2`, `pts3`, from 06:31:51 |",
  ("06:31:51", "summary/b0/a-peer-tap.json", "d['info']['first_t']", "cest"),
  ("-14.1035", "summary/b0/a-peer-tap.json", f"same({LVL} for r in ('b0', 'b0-2', 'pts3'))", ".4f"),
  ("0.000", "summary/b0/a-peer-tap.json", "same(q(pt(r, p, c, t)['median']['ppm'], 3) for r in ('b0-2', 'pts3') for p in 'abc' for c, t in ((0, 997), (1, 9973)))", "z.3f"),
  ("-123.98", "summary/pts3/c-b9-grade.json", "same(load('summary/pts3/c-b9-grade.json')['summary'][c + '_floor']['thdn_db_median'] for c in ('ch0', 'ch1'))", ".2f"),
  ("-123.98", "summary/b0-2/c-b9-grade.json", "load('summary/b0-2/c-b9-grade.json')['summary']['ch0_floor']['thdn_db_median']", ".2f"),
  ("-123.95", "summary/b0-2/c-b9-grade.json", "load('summary/b0-2/c-b9-grade.json')['summary']['ch1_floor']['thdn_db_median']", ".2f"),
  ("0.0000", "summary/pts3/c-b9-grade.json", "load('summary/pts3/c-b9-grade.json')['phase_net_frames']", "z.4f"),
  ("10", "summary/pts3/c-b9-grade.json", "load('summary/pts3/c-b9-grade.json')['seconds']", ".0f"),
  ("0.0005", "summary/b0-2/c-b9-grade.json", "load('summary/b0-2/c-b9-grade.json')['phase_net_frames']", ".4f"),
  ("300", "summary/b0-2/c-b9-grade.json", "load('summary/b0-2/c-b9-grade.json')['seconds']", ".0f"),
  ("303.8", "summary/b0-2/d-loop-decode.json", "same(q(dec(r)['decoded'] / 48000, 1) for r in ('b0', 'b0-2'))", ".1f"))
A("The change fell between `pts2`'s last tap frame at 06:28:50 and `b0`'s first",
  ("06:28:50", "summary/pts2/a-peer-tap.json", "d['info']['last_t']", "cest"))
A("at 06:31:51. `pts3`, without the CRF bind, reads as `b0-2`, so the CRF bind",
  ("06:31:51", "summary/b0/a-peer-tap.json", "d['info']['first_t']", "cest"))
A("any run. The tone at +6.94 to +6.96 ppm advanced smoothly against the stream,",
  ("+6.94", "summary/pts1/a-peer-tap.json", "min(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))", "+.2f"),
  ("+6.96", "summary/pts1/a-peer-tap.json", "max(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))", "+.2f"))
HB17 = "r'^\\| b17 \\|.*?the log holds (\\w+) underruns \\(([\\d:]+) to ([\\d:]+), during offline grading\\)'"
A("The operator's record of the tone's stop (step b17 of `HANDOFF.md`) notes five",
  ("five", "HANDOFF.md", f"rx('HANDOFF.md', {HB17})", "s"))
A("underruns in the playback's log, from 06:45:27 to 06:46:38 CEST, while this",
  ("06:45:27", "HANDOFF.md", f"rx('HANDOFF.md', {HB17}, group=2)", "s"),
  ("06:46:38", "HANDOFF.md", f"rx('HANDOFF.md', {HB17}, group=3)", "s"))
A("falls in that interval: `b0-2` ended at 06:43:09 and `pts3`'s taps started at",
  ("06:43:09", "runs/b0-2/events.jsonl", "E('b0-2', 'capture-done', what='mcasp')['t']", "cest"))
A("06:49:14. Lane B16's playback log, retained privately, holds no underrun",
  ("06:49:14", "runs/pts3/events.jsonl", "E('pts3', 'captures-started')['started']['tap']", "cest"))

# ---------------- B16b: B0
R2B = "r2/b0-2-receipt.json"
def slip(f, word=0):
    return f"slipb('{f}')"
A("DUT's CRF listener read MEDIA_LOCKED 1 12 s after its bind. The DUT's servo",
  ("1", "runs/b0-2/events.jsonl", "same(E(r, 'listener-read', listener='dut-in-1')['media_locked'] for r in ('b0', 'b0-2'))", "d"),
  ("12", "runs/b0-2/events.jsonl", "same(q(E(r, 'listener-read', listener='dut-in-1')['t'] - E(r, 'bind', listener='dut-in-1')['t'], 0) for r in ('b0', 'b0-2'))", "d"), c="B16b: B0")
A("read IDLE (`MCSRV_STAT` `0x00000020`) before the binds and after the window.",
  ("0x00000020", "runs/b0-2/dut-before-binds.txt", "same('0x%08x' % le32(mem(f'runs/{r}/dut-{w}.txt', '0x900008f8', 8)) for r in ('b0', 'b0-2') for w in ('before-binds', 'after-captures'))", "s"))
A("Its clock source read 0 at both marks.",
  ("0", "runs/b0-2/events.jsonl", "same(x['source'] for r in ('b0', 'b0-2') for x in ev(r, 'clock-read', who='dut'))", "d"))
A("`b0-2`, McASP0's 300 s at (c), graded by `b9_thdn.py`:",
  ("300", G02, "d['seconds']", ".0f"))
A("0.0005 frames over the window. The other 131 blocks at (c) hold no event",
  ("0.0005", G02, "d['phase_net_frames']", ".4f"),
  ("131", R2B, "d['degraded']", "d"))
A("either; they sit more than 3 dB above the floor in runs of blocks: 0 to 18,",
  ("3", "tools/b9_thdn.py", "Decimal(rx('tools/b9_thdn.py', r'^FLOOR_DB = ([\\d.]+)'))", "d"),
  ("0", R2B, "d['degraded_runs'][0][0]", "d"), ("18", R2B, "d['degraded_runs'][0][1]", "d"))
A("28 to 31, 43 to 44, 46 to 54 and later runs. Both taps' sample comparisons",
  ("28", R2B, "d['degraded_runs'][1][0]", "d"), ("31", R2B, "d['degraded_runs'][1][1]", "d"),
  ("43", R2B, "d['degraded_runs'][2][0]", "d"), ("44", R2B, "d['degraded_runs'][2][1]", "d"),
  ("46", R2B, "d['degraded_runs'][3][0]", "d"), ("54", R2B, "d['degraded_runs'][3][1]", "d"))
A("cover the recording's first 1,637,452 frames, 34.1 s, which hold whole blocks",
  ("1,637,452", R2B, "min(d['overlap']['frames_a'], d['overlap']['frames_b'])", ",d"),
  ("34.1", R2B, "d['overlap']['seconds']", ".1f"))
A("0 to 33. Of the 131, 23 lie there, blocks 0 to 18 and 28 to 31. There (c)",
  ("«0» to 33", R2B, "d['overlap']['whole_blocks'][0]", "d"), ("33", R2B, "d['overlap']['whole_blocks'][1]", "d"),
  ("131", R2B, "d['degraded']", "d"), ("23", R2B, "d['overlap']['degraded_inside']", "d"),
  ("blocks «0» to 18", R2B, "d['overlap']['degraded_inside_runs'][0][0]", "d"), ("18", R2B, "d['overlap']['degraded_inside_runs'][0][1]", "d"),
  ("28", R2B, "d['overlap']['degraded_inside_runs'][1][0]", "d"), ("31", R2B, "d['overlap']['degraded_inside_runs'][1][1]", "d"))
A("equals (a) sample for sample, so those 23 are in the peer's talker stream",
  ("23", R2B, "d['overlap']['degraded_inside']", "d"))
A("already: shown directly. The other 108 lie beyond the taps, blocks 43 to 251",
  ("108", R2B, "d['overlap']['degraded_beyond']", "d"),
  ("43", R2B, "d['overlap']['degraded_beyond_runs'][0][0]", "d"), ("251", R2B, "d['overlap']['degraded_beyond_runs'][-1][1]", "d"))
A("in thirteen runs, and include the worst block of each tone. No sample comparison",
  ("thirteen", R2B, "len(d['overlap']['degraded_beyond_runs'])", "w"))
A("Attribution, stage by stage. Inside the taps' 34.1 s each row is shown",
  ("34.1", R2B, "d['overlap']['seconds']", ".1f"))
FL = "[load('summary/' + r + '/c-b9-grade.json')['summary'][c + '_floor']['thdn_db_median'] for r in ('pts1', 'pts2') for c in ('ch0', 'ch1')]"
B0F = "[load('summary/b0-2/c-b9-grade.json')['summary'][c + '_floor']['thdn_db_median'] for c in ('ch0', 'ch1')]"
A("| Stage | Loss shown directly, inside the taps' 34.1 s | Beyond the taps, by inference only | Evidence |",
  ("34.1", R2B, "d['overlap']['seconds']", ".1f"))
A("| The tone source and the peer's path into its talker | The path's floor at -124 dB; 23 degraded blocks",
  ("-124", G02, "same(q(d['summary'][c + '_floor']['thdn_db_median'], 0) for c in ('ch0', 'ch1'))", "d"),
  ("23", R2B, "d['overlap']['degraded_inside']", "d"),
  ("-100.61", R2B, "d['tones']['997 Hz']['worst_inside']['thdn_db']", ".2f"),
  ("-80.63", R2B, "d['tones']['9,973 Hz']['worst_inside']['thdn_db']", ".2f"),
  ("7", R2B, "same(d['tones'][t]['worst_inside']['block'] for t in ('997 Hz', '9,973 Hz'))", "d"),
  ("06:28:50", "summary/pts2/a-peer-tap.json", "load('summary/pts2/a-peer-tap.json')['info']['last_t']", "cest"),
  ("+6.94", "summary/pts1/a-peer-tap.json", "min(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))", "+.2f"),
  ("+6.96", "summary/pts1/a-peer-tap.json", "max(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))", "+.2f"),
  ("13", G02, f"min(x - {B0F}[i % 2] for i, x in enumerate({FL}))", ".0f"),
  ("34", G02, f"max(x - {B0F}[i % 2] for i, x in enumerate({FL}))", ".0f"),
  ("10", "summary/pts1/c-mcasp.json", "same(load(f'summary/{r}/c-mcasp.json')['seconds'] for r in ('pts1', 'pts2'))", ".0f"),
  ("108", R2B, "d['overlap']['degraded_beyond']", "d"),
  ("-100.47", R2B, "d['tones']['997 Hz']['worst_beyond']['thdn_db']", ".2f"),
  ("-80.48", R2B, "d['tones']['9,973 Hz']['worst_beyond']['thdn_db']", ".2f"),
  ("224", R2B, "same(d['tones'][t]['worst_beyond']['block'] for t in ('997 Hz', '9,973 Hz'))", "d"),
  ("23", R2B, "d['overlap']['degraded_inside']", "d"),
  ("39", R2B, "same(d['tones'][t]['a_blocks'] for t in ('997 Hz', '9,973 Hz'))", "d"),
  ("-102.55", R2B, "d['tones']['997 Hz']['a_worst_db']", ".2f"),
  ("-82.58", R2B, "d['tones']['9,973 Hz']['a_worst_db']", ".2f"))
A("| The network, (a) to (b) | None | Not observed: the taps end |",
  ("0", "summary/b0-2/a-peer-tap.json", "same(load(f'summary/b0-2/{p}.json')['info']['seq_gaps'] for p in ('a-peer-tap', 'b-dut-tap'))", "d"),
  ("40", "summary/b0-2/a-peer-tap.json", "same(q(load(f'summary/b0-2/{p}.json')['seconds'], 0) for p in ('a-peer-tap', 'b-dut-tap'))", "d"))
A("| The DUT's listener, map and TDM render, (b) to (c) | None | That the DUT added none of the 108 is inference.",
  ("108", R2B, "d['overlap']['degraded_beyond']", "d"),
  ("300", G02, "d['seconds']", ".0f"),
  ("0.0005", G02, "d['phase_net_frames']", ".4f"),
  ("34.1", R2B, "d['overlap']['seconds']", ".1f"))
A("| The DUT's talker, the peer's listener and its output: the positive control | None in B0 |",
  ("14,583,286", "summary/b0-2/d-loop-decode.json", "load('summary/b0-2/d-loop-decode.json')['decoded']", ",d"),
  ("«0» net steps", "summary/b0-2/d-loop-decode.json", "load('summary/b0-2/d-loop-decode.json')['net_step_frames']", "d"),
  ("«0» discontinuities", "summary/b0-2/d-loop-decode.json", "len(load('summary/b0-2/d-loop-decode.json')['events'])", "d"),
  ("303", DB2, f"same(n for t in ({T997}, {T9973}) for n in (len(floor_inside(t)), len(inside(t['per_block']))))", "d"),
  ("two", "summary/pts2/d-loop-decode.json", "load('summary/pts2/d-loop-decode.json')['repeats']", "w"))
ALL4 = "[align(r, p) for r in ('pts1', 'pts2', 'pts3', 'b0-2')]"
A("compared: 3,077,452 against (a) and 3,077,980 against (b), over the four",
  ("3,077,452", "summary/b0-2/align-a-c.json", "sum(align(r, 'a')['compared_equal'] for r in ('pts1', 'pts2', 'pts3', 'b0-2'))", ",d"),
  ("3,077,980", "summary/b0-2/align-b-c.json", "sum(align(r, 'b')['compared_equal'] for r in ('pts1', 'pts2', 'pts3', 'b0-2'))", ",d"),
  ("four", "summary/b0-2/align-a-c.json", "sum(1 for r in RUNS if (ROOT / f'summary/{r}/align-a-c.json').exists() and r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3'))", "w"))
A("window: `SLIP_TDM` 0, static; `SLIP_LB` 158 to 160 dups, one slipped frame,",
  ("0", "runs/b0-2/dut-before-binds.txt", "same(le32(mem(f'runs/{r}/dut-{w}.txt', '0x900008d4', 12), 4) for r in ('b0', 'b0-2') for w in ('before-binds', 'after-captures'))", "d"),
  ("158", "runs/b0-2/dut-before-binds.txt", slip('runs/b0-2/dut-before-binds.txt'), "d"),
  ("160", "runs/b0-2/dut-after-captures.txt", slip('runs/b0-2/dut-after-captures.txt'), "d"),
  ("one", "runs/b0-2/dut-after-captures.txt", f"({slip('runs/b0-2/dut-after-captures.txt')} - {slip('runs/b0-2/dut-before-binds.txt')}) // 2", "w"))
A("and 156 to 158 in the incident run. The window at (c) holds no discontinuity,",
  ("156", "runs/b0/dut-before-binds.txt", slip('runs/b0/dut-before-binds.txt'), "d"),
  ("158", "runs/b0/dut-after-captures.txt", slip('runs/b0/dut-after-captures.txt'), "d"))
# ---------------- B16b: bench as left
A("| DUT stream state | Both STREAM_INPUTs unbound; STREAM_INPUT 0, at `0205022001006000`, and STREAM_INPUT 1, at `041060010000bb80`; both maps as found; CLOCK_SOURCE 0, INTERNAL; all read back |",
  ("0205022001006000", "restore/census-endb.jsonl", "cen('restore/census-endb.jsonl', 'format-dut-5-0')['payload'][8:]", "s"),
  ("041060010000bb80", "restore/census-endb.jsonl", "cen('restore/census-endb.jsonl', 'format-dut-5-1')['payload'][8:]", "s"),
  ("CLOCK_SOURCE «0»,", "restore/census-endb.jsonl", "payload_word(cen('restore/census-endb.jsonl', 'clock', 'dut'), 8)", "d"), n=0, c="B16b: bench as left")
A("| Reference peer | STREAM_INPUT 0, bound to the DUT's STREAM_OUTPUT 0, at `0205022002006000`,",
  ("0205022002006000", "restore/census-endb.jsonl", "cen('restore/census-endb.jsonl', 'format-peer-5-0')['payload'][8:]", "s"),
  ("CLOCK_SOURCE «1»,", "restore/census-endb.jsonl", "payload_word(cen('restore/census-endb.jsonl', 'clock', 'peer'), 8)", "d"))
A("| Census, B16b's start against its end | 44 of 45 reads equal, the census's start record aside;",
  ("44", "", CR("census-startb", "census-endb", "census-compare-b16b", 0), "d"),
  ("45", "", CR("census-startb", "census-endb", "census-compare-b16b", 1), "d"))
A("| DUT saved state | NVM image seq 276 to 286, commits 42 to 52, `pend=0`, `VD_OK` |",
  ("276", "restore/dut-startb.txt", "nvm('restore/dut-startb.txt')['seq']", "d"),
  ("286", "restore/dut-endb.txt", "nvm('restore/dut-endb.txt')['seq']", "d"),
  ("42", "restore/dut-startb.txt", "nvm('restore/dut-startb.txt')['commits']", "d"),
  ("52", "restore/dut-endb.txt", "nvm('restore/dut-endb.txt')['commits']", "d"),
  ("0", "restore/dut-endb.txt", "nvm('restore/dut-endb.txt')['pend']", "d"))
A("| The tone | Stopped by its process ID at 06:52:19 CEST; the playback closed |",
  ("06:52:19", "runs/b16b-tone-stop.txt", "stamps('runs/b16b-tone-stop.txt', 'LOCK')[0]", "cest"))
CB = lambda role, dt, idx, i: f"cdiff('restore/counters-endb.jsonl', 'restore/counters-startb.jsonl', '{role}', {dt}, {idx}, {i})"
BIND0 = "sum(1 for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') for b in ev(r, 'bind') if b['listener'] == 'dut-in-0')"
A("- **The peer's talkers** counted five more stream starts and stops on its AAF",
  ("five", "restore/counters-endb.jsonl", f"same([{CB('peer', 6, 0, 0)}, {CB('peer', 6, 0, 1)}])", "w"))
A("talker, one per run that bound the DUT, and two more on its CRF talker.",
  ("one", "restore/counters-endb.jsonl", f"same([{CB('peer', 6, 0, 0)}, {CB('peer', 6, 0, 1)}]) // {BIND0}", "w"),
  ("two", "restore/counters-endb.jsonl", f"same([{CB('peer', 6, 2, 0)}, {CB('peer', 6, 2, 1)}])", "w"))
A("- **`SLIP_LB`** read 152 dups at the start and 162 at the end: five slipped",
  ("152", "restore/dut-startb.txt", slip('restore/dut-startb.txt'), "d"),
  ("162", "restore/dut-endb.txt", slip('restore/dut-endb.txt'), "d"),
  ("five", "restore/dut-endb.txt", f"({slip('restore/dut-endb.txt')} - {slip('restore/dut-startb.txt')}) // 2", "w"))
A("frames over the five runs that bound the DUT's STREAM_INPUT 0. The console",
  ("five", "runs/pts1/events.jsonl", BIND0, "w"))
A("reads place one in each run of B0, between the read before its binds and the",
  ("one", "runs/b0-2/dut-after-captures.txt", "same(((le32(mem(f'runs/{r}/dut-after-captures.txt', '0x900008d4', 12)) & 0xffff) - (le32(mem(f'runs/{r}/dut-before-binds.txt', '0x900008d4', 12)) & 0xffff)) // 2 for r in ('b0', 'b0-2'))", "w"))

A("at 05:47 and 06:01 CEST. The two reads are identical.",
  ("two", SRC, "sum(1 for k, r in d['reads'].items() if k.startswith('b16-') and r['kind'] == 'state')", "w"))
A("| Runs | Tone at (a) | Offset against the stream | THD+N at (c), event-free blocks within 3 dB of the median |",
  ("3", "tools/b9_thdn.py", "Decimal(rx('tools/b9_thdn.py', r'^FLOOR_DB = ([\\d.]+)'))", "d"))
A("| Fabric, lock loss, protocol processor | As judged after lane B8, pending #645 | `SLIP_LB` counted five slipped frames over five binds of the DUT's AAF listener |",
  ("five", "restore/dut-endb.txt", f"({slip('restore/dut-endb.txt')} - {slip('restore/dut-startb.txt')}) // 2", "w"),
  ("five", "runs/pts1/events.jsonl", BIND0, "w"), c="B16b: #629 acceptance")
GR = "[r for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') if (ROOT / f'summary/{r}/c-b9-grade.json').exists()]"
A("- Four graded runs, on this bench's DUT and reference peer only. Three had",
  ("Four", "summary/b0-2/c-b9-grade.json", f"len({GR})", "W"),
  ("Three", "summary/pts1/c-b9-grade.json", f"sum(1 for r in {GR} if load(f'summary/{{r}}/c-b9-grade.json')['seconds'] == 10)", "W"), c="B16b: limits")
A("  10 s at McASP0 and about 24 s of each tap. B0's run had 300 s at McASP0, and 40 s",
  ("10", "summary/pts1/c-b9-grade.json", "same(grade(r)['seconds'] for r in ('pts1', 'pts2', 'pts3'))", ".0f"),
  ("24", "runs/pts1/events.jsonl", "same(q(E(r, 'capture-done', what='tap')['seconds'], 0) for r in ('pts1', 'pts2', 'pts3'))", "d"),
  ("300", G02, "d['seconds']", ".0f"),
  ("40", "summary/b0-2/a-peer-tap.json", "same(q(load(f'summary/b0-2/{p}.json')['seconds'], 0) for p in ('a-peer-tap', 'b-dut-tap'))", "d"))
A("- The path's floor and the 23 degraded blocks inside the taps' 34.1 s are",
  ("23", R2B, "d['overlap']['degraded_inside']", "d"),
  ("34.1", R2B, "d['overlap']['seconds']", ".1f"))
A("shown in the peer's talker stream; the other 108 degraded blocks are",
  ("108", R2B, "d['overlap']['degraded_beyond']", "d"))

# ---------------- B16c: the resume
C = ("bcrf", "baaf")
WIN = lambda r: f"win('{r}')"
TERMS = lambda r: f"terms('{r}')"
A("offline dry run below, the first bench action was at 07:48:07 CEST.",
  ("07:48:07", "soc/b16c-precheck-status.log", "stamps('soc/b16c-precheck-status.log', 'LOCK')[0]", "cest"), c="B16c: the resume")
A("| Identity gate, dev `5603c353`, again | PASS | 07:48:16 to 07:48:22 CEST,",
  ("07:48:16", "identity-b16c/lock-window.txt", "stamps('identity-b16c/lock-window.txt', 'LOCK')[0]", "cest"),
  ("07:48:22", "identity-b16c/lock-window.txt", "stamps('identity-b16c/lock-window.txt', 'UNLOCK')[0]", "cest"),
  ("44", "", CR("census-endb", "census-startc", "census-compare-b16b-to-b16c", 0), "d"),
  ("45", "", CR("census-endb", "census-startc", "census-compare-b16b-to-b16c", 1), "d"))
A("| Tool controls | PASS | The new run mode, dry-run offline against stand-ins in 8 of 8 scenarios,",
  ("«8» of 8", "controls/b16c-dryrun-summary.json", "sum(v == 'PASS' for v in d['scenarios'].values())", "d"),
  ("8 of «8»", "controls/b16c-dryrun-summary.json", "len(d['scenarios'])", "d"))
for r, lo, hi in (("bcrf", "2.585", "3.161"), ("baaf", "6.602", "7.180")):
    G_ = f"summary/{r}/c-b9-grade.json"
    A(f"Servo LOCKED {lo} to {hi} s after the set and at all 596 polls of the window.",
      (lo, f"r2/{r}-poll-trace.tsv", f"lock_bracket('{r}')[0]", ".3f"),
      (hi, f"r2/{r}-poll-receipt.json", f"lock_bracket('{r}')[1]", ".3f"),
      ("596", f"r2/{r}-poll-receipt.json", f"{WIN(r)}['servo']['LOCKED']", "d"),
      ("-123.98", G_, "d['summary']['ch0_all']['thdn_db_median']", ".2f"),
      ("-123.97", G_, "d['summary']['ch1_all']['thdn_db_median']", ".2f"),
      *((("300", G_, "d['summary']['blocks']", "d"), ("300", G_, "d['summary']['blocks_at_floor']", "d")) if r == "bcrf" else
        (("300", G_, "same([d['summary']['blocks'], d['summary']['blocks_at_floor']])", "d"),)),
      ("«0» discontinuities", G_, "d['summary']['events']", "d"),
      ("0.0000", G_, "d['summary']['effective_offset_ppm']", "z.4f"),
      ("three", G_, TERMS(r), "w"))
ALC4 = "[align(r, p)['compared_equal'] / 48000 for r in ('bcrf', 'baaf') for p in 'ab']"
A("| The four points | TONE PRESENT at (a), (b) and (c); (d) PRESENT |",
  ("34.2", "summary/bcrf/align-a-c.json", f"min({ALC4})", ".1f"),
  ("34.3", "summary/bcrf/align-a-c.json", f"max({ALC4})", ".1f"),
  ("«0» discontinuities", "summary/bcrf/d-loop-decode.json", "same(len(dec(r)['events']) for r in ('bcrf', 'baaf'))", "d"),
  ("«0» net steps", "summary/bcrf/d-loop-decode.json", "same(dec(r)['net_step_frames'] for r in ('bcrf', 'baaf'))", "d"))
# ---------------- B16c: method
A("Each case is one locked action of `run_b16c.py` through `run_locked_b16c.sh`.",
  ("one", "runs/bcrf-lock.txt", "same(len(stamps(f'runs/{r}-lock.txt', 'LOCK')) for r in ('bcrf', 'baaf'))", "w"), c="B16c: method")
A("closed, the DUT is on INTERNAL, and the peer is on CLOCK_SOURCE 1, its",
  ("1", "runs/bcrf/events.jsonl", "same(E(r, 'fol-check')['clk_peer'] for r in ('bcrf', 'baaf'))", "d"))
A("servo, slip, meter and CRF words every 0.5 s.",
  ("0.5", "runs/bcrf/events.jsonl", "same(E(r, 'poll-start')['period_s'] for r in ('bcrf', 'baaf'))", ".1f"))
A("3. Set the peer's CLOCK_DOMAIN to CLOCK_SOURCE 0, INTERNAL, read it back,",
  ("CLOCK_SOURCE «0»,", "runs/bcrf/events.jsonl", "same(E(r, 'set-clock', tag='peer-internal')['readback'] for r in ('bcrf', 'baaf'))", "d"))
A("and wait 5 s.",
  ("5", "runs/bcrf/events.jsonl", "same(q(E(r, 'mark', tag='after-peer-set')['t'] - E(r, 'set-clock', tag='peer-internal')['t'], 0) for r in ('bcrf', 'baaf'))", "d"))
A("5. Set the DUT's CLOCK_DOMAIN to CLOCK_SOURCE 1 for B-CRF or 2 for B-AAF,",
  ("CLOCK_SOURCE «1»", "runs/bcrf/events.jsonl", "E('bcrf', 'set-clock', tag='bcrf')['readback']", "d"),
  ("or «2» for", "runs/baaf/events.jsonl", "E('baaf', 'set-clock', tag='baaf')['readback']", "d"))
A("read it back, and wait up to 60 s for the servo to read LOCKED.",
  ("60", "tools/run_b16c.py", "Decimal(rx('tools/run_b16c.py', r'^LOCK_WAIT_S = ([\\d.]+)'))", "d"))
A("6. From 20 s after the set, capture as lane B16b's B0. At McASP0, the",
  ("20", "runs/bcrf/events.jsonl", "same(q(E(r, 'captures-started')['started']['tap'] - E(r, 'set-clock', who='dut', tag=r)['t'], 0) for r in ('bcrf', 'baaf'))", "d"))
A("DUT's TDM output is recorded for 300 s while lane B6's loop plays into the DUT's",
  ("300", "summary/bcrf/c-b9-grade.json", "same(grade(r)['seconds'] for r in ('bcrf', 'baaf'))", ".0f"))
A("TDM input. The external capture covers the window, and both taps its first",
  ("40", "summary/bcrf/a-peer-tap.json", "same(q(load(f'summary/{r}/{p}.json')['seconds'], 0) for r in ('bcrf', 'baaf') for p in ('a-peer-tap', 'b-dut-tap'))", "d"), off=1)
A("7. Read GET_COUNTERS and GET_CLOCK_SOURCE of both entities 20 s after the",
  ("20", "runs/bcrf/events.jsonl", "same(q(E(r, 'mark', tag='window-mark-0')['t'] - E(r, 'set-clock', who='dut', tag=r)['t'], 0) for r in ('bcrf', 'baaf'))", "d"))
A("DUT's set, about 6 s before the window, then at its middle and 15 s before",
  ("6", "runs/bcrf/events.jsonl", "same(q(E(r, 'captures-started')['started']['mcasp'] + r2lead() - E(r, 'mark', tag='window-mark-0')['t'], 0) for r in ('bcrf', 'baaf'))", "d"),
  ("15", "runs/bcrf/events.jsonl", "same(q(E(r, 'captures-started')['started']['mcasp'] + r2lead() + 300 - E(r, 'mark', tag='window-mark-2')['t'], 0) for r in ('bcrf', 'baaf'))", "d"))
A("peer back to CLOCK_SOURCE 1, read back.",
  ("1", "runs/bcrf/events.jsonl", "same(E(r, 'set-clock', who='peer', tag='restore')['readback'] for r in ('bcrf', 'baaf'))", "d"))
A("not playing at any of the eight checks. The SoC board's to-host bridge leg was",
  ("eight", "runs/bcrf/events.jsonl", "sum(len(ev(r, 'mcasp-playback-check')) for r in ('bcrf', 'baaf'))", "w"))
for r, src_, lead in (("bcrf", 1, "| `bcrf` | 07:50:00 to 07:56:15 |"), ("baaf", 2, "| `baaf` | 07:56:52 to 08:03:07 |")):
    lk = f"runs/{r}-lock.txt"; e_ = f"runs/{r}/events.jsonl"
    A(lead,
      ("«" + ("07:50:00" if r == "bcrf" else "07:56:52") + "» to", lk, f"stamps('{lk}', 'LOCK')[0]", "cest"),
      ("to «" + ("07:56:15" if r == "bcrf" else "08:03:07") + "» |", lk, f"stamps('{lk}', 'UNLOCK')[0]", "cest"),
      ("«" + ("07:50:12.3" if r == "bcrf" else "07:57:04.1") + "»", e_, f"E('{r}', 'set-clock', tag='peer-internal')['t']", "cest1"),
      ("«" + ("07:50:17.5" if r == "bcrf" else "07:57:09.3") + "»", e_, f"E('{r}', 'bind', i=-1)['t']", "cest1"),
      (f"CLOCK_SOURCE «{src_}»,", e_, f"E('{r}', 'set-clock', tag='{r}')['readback']", "d"),
      ("«" + ("07:50:29.7" if r == "bcrf" else "07:57:21.5") + "»", e_, f"E('{r}', 'set-clock', tag='{r}')['t']", "cest1"),
      ("«" + ("07:50:55" if r == "bcrf" else "07:57:47") + "» to", e_, f"E('{r}', 'captures-started')['started']['mcasp'] + r2lead()", "cest"),
      ("to «" + ("07:55:55" if r == "bcrf" else "08:02:47") + "», from", e_, f"E('{r}', 'captures-started')['started']['mcasp'] + r2lead() + load('summary/{r}/c-b9-grade.json')['seconds']", "cest"),
      ("from «26» s", e_, f"q(E('{r}', 'captures-started')['started']['mcasp'] + r2lead() - E('{r}', 'set-clock', tag='{r}')['t'], 0)", "d"),
      ("«" + ("07:56:00.0" if r == "bcrf" else "08:02:51.7") + "» to", e_, f"E('{r}', 'teardown')['t']", "cest1"),
      ("to «" + ("07:56:04.0" if r == "bcrf" else "08:02:55.7") + "» |", e_, f"E('{r}', 'mark', tag='after-restore')['t']", "cest1"))

A("| `summary/pts2/d-loop-decode.json` (the two repeats at (d)) |",
  ("two", "summary/pts2/d-loop-decode.json", "d['repeats']", "w"))

A("**Before any bench action** the two modes ran offline against stand-ins for",
  ("two", "controls/b16c-dryrun-summary.json", "sum(1 for k in d['scenarios'] if k in ('bcrf', 'baaf'))", "w"))
A("captures (`tools/dryrun_b16c/`). There were eight scenarios:",
  ("eight", "controls/b16c-dryrun-summary.json", "len(d['scenarios'])", "w"))
A("state; 8 of 8 pass. The wrapper's deadline path passes too: the action's",
  ("«8» of 8", "controls/b16c-dryrun-summary.json", "sum(v == 'PASS' for v in d['scenarios'].values())", "d"),
  ("8 of «8»", "controls/b16c-dryrun-summary.json", "len(d['scenarios'])", "d"))
A("the path's floor an event-free block within 3 dB of the median; and",
  ("3", "tools/b9_thdn.py", "Decimal(rx('tools/b9_thdn.py', r'^FLOOR_DB = ([\\d.]+)'))", "d"))
A("packet's files. SNR equals minus THD+N within 0.01 dB in every row.",
  ("0.01", "summary/bcrf/a-peer-tap.json", "bound(max(abs(t['median']['snr_db'] + t['median']['thdn_db']) for r in ('bcrf', 'baaf', 'b0-2') for p in PFILE_ for c in (0, 1) for t in [pt(r, p, c, (997, 9973)[c])]), '0.01')", ".2f"))
# ---------------- B16c: clock-source record
SC = lambda r, who, tag: f"E('{r}', 'set-clock', who='{who}', tag='{tag}')"
for r, src_, rows_ in (("bcrf", 1, ("| `bcrf` | The ruling's exception | The peer | 0, INTERNAL | SUCCESS | 0 |", "| `bcrf` | The case | The DUT, the listener | 1, its CRF input | SUCCESS | 1 |", "| `bcrf` | Restore | The DUT | 0, INTERNAL | SUCCESS | 0 |", "| `bcrf` | Restore, after the DUT's unbinds | The peer | 1, its CRF input, as found | SUCCESS | 1 |")),
                       ("baaf", 2, ("| `baaf` | The ruling's exception | The peer | 0 | SUCCESS | 0 |", "| `baaf` | The case | The DUT | 2, its AAF input | SUCCESS | 2 |", "| `baaf` | Restore | The DUT | 0 | SUCCESS | 0 |", "| `baaf` | Restore, after the DUT's unbinds | The peer | 1 | SUCCESS | 1 |"))):
    e_ = f"runs/{r}/events.jsonl"
    for anchor, (who, tag) in zip(rows_, (("peer", "peer-internal"), ("dut", r), ("dut", "restore"), ("peer", "restore"))):
        cells = anchor.split(" | ")
        val = cells[3].split(",")[0]
        A(anchor, (f"| {cells[2]} | «{val}»", e_, f"{SC(r, who, tag)}['src']", "d"),
          (f"SUCCESS | «{anchor.split(' | ')[5].split(' ')[0]}» |", e_, f"{SC(r, who, tag)}['readback']", "d"),
          **({"c": "B16c: clock-source record"} if r == "bcrf" and who == "peer" and tag == "peer-internal" else {}))
MK4 = "('window-mark-0', 'window-mark-1', 'window-mark-2', 'after-captures')"
A("At the four marks of step 7, GET_CLOCK_SOURCE read 1 or 2 on the DUT and 0 on",
  ("four", "runs/bcrf/events.jsonl", f"same(len([m for m in ev(r, 'mark') if m['tag'] in {MK4}]) for r in ('bcrf', 'baaf'))", "w"),
  ("1", "runs/bcrf/events.jsonl", f"same(m['clock']['dut'] for m in ev('bcrf', 'mark') if m['tag'] in {MK4})", "d"),
  ("2", "runs/baaf/events.jsonl", f"same(m['clock']['dut'] for m in ev('baaf', 'mark') if m['tag'] in {MK4})", "d"),
  ("0", "runs/bcrf/events.jsonl", f"same(m['clock']['peer'] for r in ('bcrf', 'baaf') for m in ev(r, 'mark') if m['tag'] in {MK4})", "d"))
A("the peer: 20 s after the DUT's set, about 6 s before the window; at its",
  ("20", "runs/bcrf/events.jsonl", "same(q(E(r, 'mark', tag='window-mark-0')['t'] - E(r, 'set-clock', who='dut', tag=r)['t'], 0) for r in ('bcrf', 'baaf'))", "d"),
  ("6", "runs/bcrf/events.jsonl", "same(q(E(r, 'captures-started')['started']['mcasp'] + r2lead() - E(r, 'mark', tag='window-mark-0')['t'], 0) for r in ('bcrf', 'baaf'))", "d"))
A("middle; 15 s before its end; and after it. After the restore it read 0 on the",
  ("15", "runs/bcrf/events.jsonl", "same(q(E(r, 'captures-started')['started']['mcasp'] + r2lead() + 300 - E(r, 'mark', tag='window-mark-2')['t'], 0) for r in ('bcrf', 'baaf'))", "d"),
  ("0", "runs/bcrf/events.jsonl", "same(E(r, 'mark', tag='after-restore')['clock']['dut'] for r in ('bcrf', 'baaf'))", "d"))
A("DUT and 1 on the peer.",
  ("1", "runs/bcrf/events.jsonl", "same(E(r, 'mark', tag='after-restore')['clock']['peer'] for r in ('bcrf', 'baaf'))", "d"))
A("so none was set: `0205022001006000` on the DUT's STREAM_INPUT 0 and",
  ("0205022001006000", "runs/bcrf/events.jsonl", "same(x['listener_fmt'] for r in ('bcrf', 'baaf') for x in ev(r, 'format-check', listener='dut-in-0') if x['set'] is None and x['talker_fmt'] == x['listener_fmt'])", "s"), n=1)
A("`041060010000bb80` on its STREAM_INPUT 1. Every bind and unbind answered",
  ("041060010000bb80", "runs/bcrf/events.jsonl", "same(x['listener_fmt'] for r in ('bcrf', 'baaf') for x in ev(r, 'format-check', listener='dut-in-1') if x['set'] is None and x['talker_fmt'] == x['listener_fmt'])", "s"), n=1)
# ---------------- B16c: B-CRF and B-AAF
A("The tone sits in channels 0 and 1 of the peer's talker stream. Channels 2 and",
  ("@Channels «2» and", "", IDLE_CH(("bcrf", "baaf"), 0), "d", 0), c="B16c: B-CRF and B-AAF")
A("3 carry -1 to 0 LSB at every point, and McASP0's channels 4 to 7, unmapped,",
  ("@and «3» carry", "", IDLE_CH(("bcrf", "baaf"), 1), "d", 0),
  ("-1", "summary/bcrf/a-peer-tap.json", f"same(c['min'] for c in {idle(('bcrf', 'baaf'))})", "d"),
  ("0", "summary/bcrf/a-peer-tap.json", f"same(c['max'] for c in {idle(('bcrf', 'baaf'))})", "d"))
A("an effective offset of 0 ppm. The 997 Hz tone's phase moved less than 0.000001",
  ("0", "summary/bcrf/c-b9-grade.json", "same(grade(r)['effective_offset_ppm'] for r in ('bcrf', 'baaf'))", "d"),
  ("0.000001", "summary/bcrf/c-b9-grade.json", "bound(max(abs(grade(r)['phase_net_frames']) for r in ('bcrf', 'baaf')), '0.000001')", ".6f"))
A("frames over the window, against 0.0005 in B0.",
  ("0.0005", G02, "d['phase_net_frames']", ".4f"))
for r, b_, a_ in (("bcrf", "1,646,473", "1,647,859"), ("baaf", "1,644,390", "1,641,156")):
    A(f"| `{r}` | SAMPLE-EXACT over {b_} recorded frames,",
      (b_, f"summary/{r}/align-b-c.json", "d['compared_equal']", ",d"),
      (f"{b_} recorded frames, «34.3» s", f"summary/{r}/align-b-c.json", "d['compared_equal'] / 48000", ".1f"),
      (f"{b_} recorded frames, 34.3 s, «0» differing", f"summary/{r}/align-b-c.json", "d['frames_differing']", "d"),
      (f"{b_} recorded frames, 34.3 s, 0 differing, «0» slips", f"summary/{r}/align-b-c.json", "len(d['slips'])", "d"),
      (a_, f"summary/{r}/align-a-c.json", "d['compared_equal']", ",d"),
      (f"{a_} frames, «{'34.3' if r == 'bcrf' else '34.2'}» s", f"summary/{r}/align-a-c.json", "d['compared_equal'] / 48000", ".1f"),
      (f"{a_} frames, {'34.3' if r == 'bcrf' else '34.2'} s, «0» differing", f"summary/{r}/align-a-c.json", "d['frames_differing']", "d"),
      (f"{a_} frames, {'34.3' if r == 'bcrf' else '34.2'} s, 0 differing, «0» slips", f"summary/{r}/align-a-c.json", "len(d['slips'])", "d"))
for r, dec in (("bcrf", "14,583,391"), ("baaf", "14,585,924")):
    DL, DP = f"summary/{r}/d-loop-decode.json", f"summary/{r}/d-extcap-pair.json"
    TA, TB = f"load('{DP}')['rows'][0]['tone_997']", f"load('{DP}')['rows'][1]['tone_9973']"
    A(f"| `{r}` | {dec} | 0 | 0 | 0 | 0 | -1.00 dBFS;",
      (dec, DL, "d['decoded']", ",d"),
      (f"| {dec} | «0» |", DL, "d['skips']", "d"),
      (f"| {dec} | 0 | «0» |", DL, "d['repeats']", "d"),
      (f"| {dec} | 0 | 0 | «0» |", DL, "d['net_step_frames']", "d"),
      (f"| {dec} | 0 | 0 | 0 | «0» |", DL, "d['torn']", "d"),
      ("-1.00", DP, f"same([q({TA}['median']['level_dbfs'], 2), q({TB}['median']['level_dbfs'], 2)])", ".2f"),
      ("-146.06", DP, f"{TA}['median']['thdn_db']", ".2f"),
      ("-145.99", DP, f"{TB}['median']['thdn_db']", ".2f"),
      ("«303» of the", DP, f"same(len(floor_inside(t)) for t in ({TA}, {TB}))", "d"),
      ("of the «303» wholly", DP, f"same(len(inside(t['per_block'])) for t in ({TA}, {TB}))", "d"),
      ("306", DP, f"same(len(t['per_block']) for t in ({TA}, {TB}))", "d"),
      ("blocks «0» and 1", DP, f"same(silent(t['per_block'])[0] for t in ({TA}, {TB}))", "d"),
      ("0 and «1» precede", DP, f"same(silent(t['per_block'])[-1] for t in ({TA}, {TB}))", "d"),
      ("block «2» holds", DP, f"same(inside(t['per_block'])[0] - 1 for t in ({TA}, {TB}))", "d"))
DEC2 = "[dec(r) for r in ('bcrf', 'baaf')]"
A("So there were 0 net steps between the DUT's TDM clock and the peer's output",
  ("0", "summary/bcrf/d-loop-decode.json", f"same(x['net_step_frames'] for x in {DEC2})", "d"))
A("over 303.8 s and 303.9 s. The decode counts a step as small as one frame, as",
  ("303.8", "summary/bcrf/d-loop-decode.json", "load('summary/bcrf/d-loop-decode.json')['decoded'] / 48000", ".1f"),
  ("303.9", "summary/baaf/d-loop-decode.json", "load('summary/baaf/d-loop-decode.json')['decoded'] / 48000", ".1f"),
  ("one", "controls/b16b-dloop-control.json", "step_frames()", "w"))
A("its planted control shows (`controls/b16b-dloop-control.json`); one frame in",
  ("one", "controls/b16b-dloop-control.json", "step_frames()", "w"))
A("14.58 million would be 0.07 ppm.",
  ("14.58", "summary/bcrf/d-loop-decode.json", f"step_frames() * min(x['decoded'] for x in {DEC2}) / Decimal(10 ** 6)", ".2f"),
  ("0.07", "summary/bcrf/d-loop-decode.json", f"step_frames() * Decimal(10 ** 6) / min(x['decoded'] for x in {DEC2})", ".2f"))

A("McASP0's 300 s at (c), graded by `b9_thdn.py`:",
  ("300", "summary/bcrf/c-b9-grade.json", "same(grade(r)['seconds'] for r in ('bcrf', 'baaf'))", ".0f"), n=1)

# ---------------- B16c: the following record
MKC = lambda r, tag, key, i: f"E('{r}', 'mark', tag='{tag}')['counters']['{key}'][{i}]"
A("From lane B9's console poll, 0.5 s per poll, and the GET_COUNTERS marks. The",
  ("0.5", "runs/bcrf/events.jsonl", "same(E(r, 'poll-start')['period_s'] for r in ('bcrf', 'baaf'))", ".1f"), c="B16c: the following record")
for r, lo, hi, row in (("bcrf", "2.585", "3.161", "| B-CRF | 2.585 to 3.161 s; ACQUIRE before it |"), ("baaf", "6.602", "7.180", "| B-AAF | 6.602 to 7.180 s; ACQUIRE before it |")):
    W_ = WIN(r); P_ = f"r2/{r}-poll-receipt.json"
    rows_ = [(lo, f"r2/{r}-poll-trace.tsv", f"lock_bracket('{r}')[0]", ".3f"),
             (hi, P_, f"lock_bracket('{r}')[1]", ".3f"),
             ("«596» of 596", P_, f"{W_}['servo']['LOCKED']", "d"),
             ("596 of «596»", P_, f"{W_}['polls']", "d"),
             ("-6.000", P_, f"{W_}['trim_ppm'][1]", ".3f"),
             ("-6.125", P_, f"{W_}['trim_ppm'][0]", ".3f")]
    if r == "bcrf":
        rows_ += [("+10.60", P_, f"{W_}['crf_rate_ppm'][0]", "+.2f"), ("+10.65", P_, f"{W_}['crf_rate_ppm'][1]", "+.2f"),
                  ("`AAFM_STAT` «0» |", P_, f"same(int(x, 16) for x in {W_}['aafm_stat'])", "d")]
    else:
        rows_ += [("+10.60", P_, f"{W_}['aafm_rate_ppm_valid'][0]", "+.2f"), ("+10.63", P_, f"{W_}['aafm_rate_ppm_valid'][1]", "+.2f"),
                  ("+10.59", P_, f"{W_}['crf_rate_ppm'][0]", "+.2f"), ("+10.65", P_, f"{W_}['crf_rate_ppm'][1]", "+.2f"),
                  ("0x001e0007", P_, f"'0x' + same({W_}['aafm_stat'])", "s"),
                  ("enabled, «0» history", P_, f"same((int(x, 16) >> 8) & 0xff for x in {W_}['aafm_stat'])", "d"),
                  ("30", P_, f"same(int(x, 16) >> 16 for x in {W_}['aafm_stat'])", "d")]
    rows_ += [("| «0», static |", P_, f"same({W_}['slip_tdm_dups'] + {W_}['slip_tdm_skips'])", "d")]
    for j, tag in enumerate(("window-mark-0", "window-mark-2")):
        lk, ul = ("23", "22") if r == "bcrf" else ("24", "23")
        rows_ += [((f"| «{lk}» / {ul} and" if j == 0 else f"and «{lk}» / {ul} |"), f"runs/{r}/events.jsonl", MKC(r, tag, 'dut-0x0024-0', 0), "d"),
                  ((f"| {lk} / «{ul}» and" if j == 0 else f"and {lk} / «{ul}» |"), f"runs/{r}/events.jsonl", MKC(r, tag, 'dut-0x0024-0', 1), "d")]
    A(row, *rows_)
A("its five console reads, falls between them. So each lock bracket runs from",
  ("five", "tools/console_poll_b8.py", "len(re.findall(r'\\(\"0x9000[0-9a-f]+\", \\d+\\)', rx('tools/console_poll_b8.py', r'^CMDS = \\((.*)\\)$')))", "w"))
A("LOCKED: polls 44 and 45 in B-CRF, 52 and 53 in B-AAF. The `SLIP_LB` brackets",
  ("44", "r2/bcrf-poll-receipt.json", "d['locked']['first_locked_poll'] - 1", "d"),
  ("45", "r2/bcrf-poll-receipt.json", "d['locked']['first_locked_poll']", "d"),
  ("52", "r2/baaf-poll-receipt.json", "d['locked']['first_locked_poll'] - 1", "d"),
  ("53", "r2/baaf-poll-receipt.json", "d['locked']['first_locked_poll']", "d"))
LO = lambda r: f"{WIN(r)}['mcsrv_stat_lo16']"
A("The servo word read `0x...0034` while LOCKED, as in lane B7's read, and",
  ("0x...0034", "r2/bcrf-poll-receipt.json", f"'0x...' + sorted(set({LO('bcrf')}) | set({LO('baaf')}))[0]", "s"))
A("`0x...0074` while the fine-PS actuator was busy: 580 and 16 of the window's",
  ("0x...0074", "r2/bcrf-poll-receipt.json", f"'0x...' + sorted(set({LO('bcrf')}) | set({LO('baaf')}))[1]", "s"),
  ("580", "r2/bcrf-poll-receipt.json", f"{LO('bcrf')}['0034']", "d"),
  ("16", "r2/bcrf-poll-receipt.json", f"{LO('bcrf')}['0074']", "d"))
A("polls in B-CRF, 584 and 12 in B-AAF. The design's",
  ("584", "r2/baaf-poll-receipt.json", f"{LO('baaf')}['0034']", "d"),
  ("12", "r2/baaf-poll-receipt.json", f"{LO('baaf')}['0074']", "d"))
DES = "repo:docs/design/MEDIA_CLOCK_FOLLOWING.md"
A("- LOCKED within 15 s of the set and never left during the capture: met;",
  ("15", DES, f"rx('{DES}', r'^\\| B AAF \\|.*Servo LOCKED within (\\d+) s of the set')", "s"))
A("- 0 net steps between the DUT's TDM clock and the peer's output: met, at (d);",
  ("0", DES, f"rx('{DES}', r'^\\| B AAF \\|.*?; (\\d+) net steps between')", "s"))
A("- its largest timestamp deviation recorded: 30 ns.",
  ("30", "r2/baaf-poll-receipt.json", f"same(int(x, 16) >> 16 for x in {WIN('baaf')}['aafm_stat'])", "d"))
B6R = r"r'^- B CRF passes when (.*)$'"
A("For B CRF the row says \"As B6\". Lane B6's pass rule has four terms (see",
  ("four", FIND, "len(re.split(r', and |, ', b6_rule()))", "w"))
DEC = lambda r: f"load('summary/{r}/d-loop-decode.json')"
A("| The DUT's servo reads LOCKED | Met | Met | LOCKED at 596 of 596 window polls;",
  # round 6 (R624-5-F1): each case's count from that case's own receipt; the rows output names both files
  ("«596» of 596", "", "each((r, win(r)['servo']['LOCKED']) for r in ('bcrf', 'baaf'))", "d"),
  ("596 of «596»", "", "each((r, win(r)['polls']) for r in ('bcrf', 'baaf'))", "d"),
  ("2.585", "r2/bcrf-poll-trace.tsv", "lock_bracket('bcrf')[0]", ".3f"), ("3.161", "r2/bcrf-poll-receipt.json", "lock_bracket('bcrf')[1]", ".3f"),
  ("6.602", "r2/baaf-poll-trace.tsv", "lock_bracket('baaf')[0]", ".3f"), ("7.180", "r2/baaf-poll-receipt.json", "lock_bracket('baaf')[1]", ".3f"))
A("| The counted frame-rate ratio within 0.5 ppm of zero | Met | Met |",
  ("0.5", FIND, "re.search(r'within ([\\d.]+) ppm', b6_rule()).group(1)", "s"),
  ("«0» net steps", "summary/bcrf/d-loop-decode.json", "same(dec(r)['net_step_frames'] for r in ('bcrf', 'baaf'))", "d"),
  ("14,583,391", "summary/bcrf/d-loop-decode.json", f"{DEC('bcrf')}['decoded']", ",d"),
  ("14,585,924", "summary/baaf/d-loop-decode.json", f"{DEC('baaf')}['decoded']", ",d"),
  ("14.58", "summary/bcrf/d-loop-decode.json", f"min({DEC('bcrf')}['decoded'], {DEC('baaf')}['decoded']) / Decimal(10 ** 6)", ".2f"),
  ("0.07", "summary/bcrf/d-loop-decode.json", f"Decimal(10 ** 6) / min({DEC('bcrf')}['decoded'], {DEC('baaf')}['decoded'])", ".2f"),
  ("0.0000", "summary/bcrf/c-b9-grade.json", "same(grade(r)['effective_offset_ppm'] for r in ('bcrf', 'baaf'))", "z.4f"))
A("| 0 listener discontinuities on the tone path | Met | Met | 0 at (c) over 300 s and 0 at (d) |",
  ("| «0» listener", FIND, "re.search(r'has (\\d+) listener discontinuities', b6_rule()).group(1)", "s"),
  ("| «0» at (c)", "summary/bcrf/c-b9-grade.json", "same(grade(r)['summary']['events'] for r in ('bcrf', 'baaf'))", "d"),
  ("300", "summary/bcrf/c-b9-grade.json", "same(grade(r)['seconds'] for r in ('bcrf', 'baaf'))", ".0f"),
  ("and «0» at (d)", "summary/bcrf/d-loop-decode.json", "same(len(dec(r)['events']) for r in ('bcrf', 'baaf'))", "d"))
A("[Method](#method)), and both cases are judged against all four here:",
  ("four", FIND, "len(re.split(r', and |, ', b6_rule()))", "w"))
A("So B-CRF and B-AAF meet three of lane B6's four terms; the timed ratio was not",
  ("three", "summary/bcrf/c-b9-grade.json", f"same([{TERMS('bcrf')}, {TERMS('baaf')}])", "w"),
  ("four", FIND, "len(re.split(r', and |, ', b6_rule()))", "w"))
STEPS = lambda r: f"load('r2/{r}-poll-receipt.json')['slip_lb_steps']"
ALLST = "[x for r in ('bcrf', 'baaf') for x in load(f'r2/{r}-poll-receipt.json')['slip_lb_steps']]"
PRE = lambda r: f"steps('{r}', 'binds..dut-set')"
ACQ = lambda r: f"steps('{r}', 'dut-set..first-locked-poll')"
A("**`SLIP_LB`**, the DUT's loopback ring, counted 162 dups at the start of B16c and",
  ("162", "restore/dut-startc.txt", slip('restore/dut-startc.txt'), "d"))
A("188 at its end, in steps of two. Each step is timed by the two polls between",
  ("188", "restore/dut-endc.txt", slip('restore/dut-endc.txt'), "d"),
  ("of «two».", "r2/bcrf-poll-receipt.json", f"same(x['dups'][1] - x['dups'][0] for x in {ALLST})", "w"),
  ("the «two» polls", "r2/bcrf-poll-receipt.json", f"same(len(x['polls']) for x in {ALLST})", "w"))
A("which it appears, against the DUT's set. In each case five steps fell in the",
  ("five", "r2/bcrf-poll-receipt.json", f"same([len({PRE('bcrf')}), len({PRE('baaf')})])", "w"))
A("12.2 s between the binds and the DUT's set, all with the servo IDLE: from 0.1",
  ("12.2", "r2/bcrf-poll-receipt.json", "same(q(-load(f'r2/{r}-poll-receipt.json')['marks_after_set_s']['binds'], 1) for r in ('bcrf', 'baaf'))", ".1f"),
  ("0.1", "r2/bcrf-poll-receipt.json", f"same([q({PRE('bcrf')}[0]['after_binds_s'][0], 1), q({PRE('baaf')}[0]['after_binds_s'][0], 1)])", ".1f"))
A("s after the binds to 1.4 s before the set. Then the DUT was on INTERNAL and",
  ("1.4", "r2/bcrf-poll-receipt.json", f"same([q(-{PRE('bcrf')}[-1]['after_set_s'][1], 1), q(-{PRE('baaf')}[-1]['after_set_s'][1], 1)])", ".1f"))
A("the clocks' difference and, for the first, with the one slip per bind",
  ("one", "runs/b0-2/dut-after-captures.txt", "same(((le32(mem(f'runs/{r}/dut-after-captures.txt', '0x900008d4', 12)) & 0xffff) - (le32(mem(f'runs/{r}/dut-before-binds.txt', '0x900008d4', 12)) & 0xffff)) // 2 for r in ('b0', 'b0-2'))", "w"))
A("- B-CRF: one step, between 2.08 and 2.66 s after the set;",
  ("one", "r2/bcrf-poll-receipt.json", f"len({ACQ('bcrf')})", "w"),
  ("2.08", "r2/bcrf-poll-receipt.json", f"{ACQ('bcrf')}[0]['after_set_s'][0]", ".2f"),
  ("2.66", "r2/bcrf-poll-receipt.json", f"{ACQ('bcrf')}[0]['after_set_s'][1]", ".2f"))
A("- B-AAF: two steps, between 2.08 and 2.65 s and between 5.10 and 5.68 s after",
  ("two", "r2/baaf-poll-receipt.json", f"len({ACQ('baaf')})", "w"),
  ("2.08", "r2/baaf-poll-receipt.json", f"{ACQ('baaf')}[0]['after_set_s'][0]", ".2f"),
  ("2.65", "r2/baaf-poll-receipt.json", f"{ACQ('baaf')}[0]['after_set_s'][1]", ".2f"),
  ("5.10", "r2/baaf-poll-receipt.json", f"{ACQ('baaf')}[1]['after_set_s'][0]", ".2f"),
  ("5.68", "r2/baaf-poll-receipt.json", f"{ACQ('baaf')}[1]['after_set_s'][1]", ".2f"))
A("the poll's last 12 polls. Lane B8's INTERNAL-to-AAF set slipped 2.0 to 3.0 s",
  ("12", "r2/bcrf-poll-receipt.json", "same(load(f'r2/{r}-poll-receipt.json')['spans']['restored..poll-end']['polls'] for r in ('bcrf', 'baaf'))", "d"),
  ("2.0", FIND, "rx(FIND_P, r'The listener ring slipped one frame ([\\d.]+) to ([\\d.]+) s after the servo first read LOCKED')", "s"),
  ("3.0", FIND, "rx(FIND_P, r'The listener ring slipped one frame ([\\d.]+) to ([\\d.]+) s after the servo first read LOCKED', group=2)", "s"))
MR = lambda f, i: f"counters('{f}', 'dut', 6, {i})[2]"
A("**MEDIA_RESET.** Both DUT talkers counted MEDIA_RESET 0 at the start of B16c and",
  ("0", "restore/counters-startc.jsonl", f"same([{MR('restore/counters-startc.jsonl', 0)}, {MR('restore/counters-startc.jsonl', 1)}])", "d"))
A("4 at its end, as many as the DUT's clock-source sets. The design declares one",
  ("4", "restore/counters-endc.jsonl", f"same([{MR('restore/counters-endc.jsonl', 0)}, {MR('restore/counters-endc.jsonl', 1)}, sum(len(ev(r, 'set-clock', who='dut')) for r in ('bcrf', 'baaf'))])", "d"),
  ("one", DES, f"rx('{DES}', r'\\| (One) MEDIA_RESET per switch on the DUT.s talker \\(Milan v1\\.2 Table 5\\.4\\)').lower()", "s"))
A("times them at the marks, in each case: one between the mark 5 s after the",
  ("one", "runs/bcrf/events.jsonl", "same(mdiff(r, 'window-mark-0', 'after-peer-set', 'peer-0x0005-0', 4) for r in ('bcrf', 'baaf'))", "w"),
  ("5", "runs/bcrf/events.jsonl", "same(q(E(r, 'mark', tag='after-peer-set')['t'] - E(r, 'set-clock', tag='peer-internal')['t'], 0) for r in ('bcrf', 'baaf'))", "d"))
A("peer's set and the first window mark, 20 s after the DUT's set; none from",
  ("20", "runs/bcrf/events.jsonl", "same(q(E(r, 'mark', tag='window-mark-0')['t'] - E(r, 'set-clock', who='dut', tag=r)['t'], 0) for r in ('bcrf', 'baaf'))", "d"))
A("there to the mark after the captures; and one at the restore.",
  ("one", "runs/bcrf/events.jsonl", "same(mdiff(r, 'after-restore', 'after-captures', 'peer-0x0005-0', 4) for r in ('bcrf', 'baaf'))", "w"))
A("**CLOCK_DOMAIN counters.** The DUT's LOCKED and UNLOCKED each moved once per",
  ("once", "runs/bcrf/events.jsonl", "same(mdiff(r, 'window-mark-0', 'after-peer-set', 'dut-0x0024-0', i) for r in ('bcrf', 'baaf') for i in (0, 1))", "x"))
A("from there to the restore. The peer's moved once each at each restore to its",
  ("once", "runs/bcrf/events.jsonl", "same(mdiff(r, 'after-restore', 'after-captures', 'peer-0x0024-0', i) for r in ('bcrf', 'baaf') for i in (0, 1))", "x"))

# ---------------- B16c: attribution
PM = lambda r, ch, t: f"fmt(pt('{r}', 'a', {ch}, {t})['median']['thdn_db'], '.2f')"
A("| The tone source and the peer's path into its talker | None beyond the path's floor |",
  ("-123.98/-123.97", "summary/bcrf/a-peer-tap.json", f"{PM('bcrf', 0, 997)} + '/' + {PM('bcrf', 1, 9973)}", "s"),
  ("-123.98/-123.98", "summary/baaf/a-peer-tap.json", f"{PM('baaf', 0, 997)} + '/' + {PM('baaf', 1, 9973)}", "s"),
  ("-123.93", "summary/bcrf/a-peer-tap.json", "same(q(pt(r, 'a', c, t)['worst_thdn_db'], 2) for r in ('bcrf', 'baaf') for c, t in ((0, 997), (1, 9973)))", ".2f"), c="B16c: attribution")
A("| The network, (a) to (b) | None | 0 sequence gaps on either tap; (a) and (b) both equal (c) over the same recorded frames |",
  ("0", "summary/bcrf/a-peer-tap.json", "same(load(f'summary/{r}/{p}.json')['info']['seq_gaps'] for r in ('bcrf', 'baaf') for p in ('a-peer-tap', 'b-dut-tap'))", "d"))
A("| The DUT's listener, its media-clock recovery, map and TDM render, (b) to (c) | None |",
  ("34.2", "summary/bcrf/align-a-c.json", f"min({ALC4})", ".1f"),
  ("34.3", "summary/bcrf/align-a-c.json", f"max({ALC4})", ".1f"),
  ("300", "summary/bcrf/c-b9-grade.json", "same(grade(r)['seconds'] for r in ('bcrf', 'baaf'))", ".0f"),
  ("0.000001", "summary/bcrf/c-b9-grade.json", "bound(max(abs(grade(r)['phase_net_frames']) for r in ('bcrf', 'baaf')), '0.000001')", ".6f"))
A("| The DUT's talker, the peer's listener and its output: the positive control | None | 0 discontinuities and 0 net steps in 14.58 million",
  ("«0» discontinuities", "summary/bcrf/d-loop-decode.json", "same(len(dec(r)['events']) for r in ('bcrf', 'baaf'))", "d"),
  ("«0» net steps", "summary/bcrf/d-loop-decode.json", "same(dec(r)['net_step_frames'] for r in ('bcrf', 'baaf'))", "d"),
  ("14.58", "summary/bcrf/d-loop-decode.json", f"min(x['decoded'] for x in {DEC2}) / Decimal(10 ** 6)", ".2f"),
  ("303", "summary/bcrf/d-extcap-pair.json", "same(n for r in ('bcrf', 'baaf') for t in (load(f'summary/{r}/d-extcap-pair.json')['rows'][0]['tone_997'], load(f'summary/{r}/d-extcap-pair.json')['rows'][1]['tone_9973']) for n in (len(floor_inside(t)), len(inside(t['per_block']))))", "d"))
A("3,289,015 against (a) and 3,290,863 against (b).",
  ("3,289,015", "summary/bcrf/align-a-c.json", "sum(align(r, 'a')['compared_equal'] for r in ('bcrf', 'baaf'))", ",d"),
  ("3,290,863", "summary/bcrf/align-b-c.json", "sum(align(r, 'b')['compared_equal'] for r in ('bcrf', 'baaf'))", ",d"))
A("Beyond the taps' 34 s, (c) is graded on its own. With every block at the",
  ("34", "summary/bcrf/align-a-c.json", f"same(q(x, 0) for x in {ALC4})", "d"))
A("There 131 of the 300 blocks at (c) sat off the floor. Inside the taps' 34.1 s,",
  ("131", R2B, "d['degraded']", "d"), ("300", R2B, "d['blocks']", "d"), ("34.1", R2B, "d['overlap']['seconds']", ".1f"))
A("23 of them lie, and (a) holds them sample for sample: shown directly. (a)'s",
  ("23", R2B, "d['overlap']['degraded_inside']", "d"))
A("own 39 blocks reach -102.6 dB and -82.6 dB. The other 108 lie beyond the taps",
  ("39", R2B, "same(d['tones'][t]['a_blocks'] for t in ('997 Hz', '9,973 Hz'))", "d"),
  ("-102.6", R2B, "d['tones']['997 Hz']['a_worst_db']", ".1f"),
  ("-82.6", R2B, "d['tones']['9,973 Hz']['a_worst_db']", ".1f"),
  ("108", R2B, "d['overlap']['degraded_beyond']", "d"))
A("floor. In the entries the reads around them both hold (618 between lane",
  ("618", SRC, "get(d, 'compare.2.both')", "d"))
A("B16b's last read and B16c's first, 668 within B16c), the tone source's state",
  ("668", SRC, "get(d, 'compare.3.both')", "d"))
GRADED1 = "same([sum(1 for r in ('b0', 'b0-2') if (ROOT / f'summary/{r}/c-b9-grade.json').exists()), sum(1 for r in RUNS if r == 'bcrf'), sum(1 for r in RUNS if r == 'baaf')])"
A("read the same for B0 and for both cases here. One run of each, at different",
  ("One", "summary/b0-2/c-b9-grade.json", GRADED1, "W"))
# ---------------- B16c: the tone source, read only
B16CM = ("b16c-meters-1", "b16c-meters-2", "b16c-state-2")
A("The tone, lane B15's loop `d9684a8f...`, played from 07:49:29 to 08:03:52",
  ("d9684a8f...", "runs/b16c-tone-start.txt", "rx('runs/b16c-tone-start.txt', r'LOOP_SHA256 ([0-9a-f]{8})') + '...'", "s"),
  ("07:49:29", "runs/b16c-tone-start.txt", "stamps('runs/b16c-tone-start.txt', 'STATUS')[0] - Decimal(rx('runs/b16c-tone-start.txt', r'hw_ptr : (\\d+)')) / 48000", "cest"),
  ("08:03:52", "runs/b16c-tone-stop.txt", "stamps('runs/b16c-tone-stop.txt', 'LOCK')[0]", "cest"), c="B16c: the tone source, read only")
A("CEST. The lane read the source's state at 07:48 and 08:03 CEST, and its meters",
  ("07:48", SRC, "Decimal(clock(get(d, 'reads.b16c-state-1.at')))", "hm"),
  ("08:03", SRC, "Decimal(clock(get(d, 'reads.b16c-state-2.at')))", "hm"))
A("passively at 07:49 and 08:03. The meters read as in lane B16b, at both",
  ("07:49", SRC, "Decimal(clock(get(d, 'reads.b16c-meters-1.at')))", "hm"),
  ("08:03", SRC, "Decimal(clock(get(d, 'reads.b16c-meters-2.at')))", "hm"))
A("times: -38.5 dBFS leaving the documented pair of outputs and -14.0 dBFS",
  ("-38.5", SRC, srcv(B16CM, "the documented pair of outputs", "leaving_dbfs"), ".1f"),
  ("-14.0", SRC, srcv(B16CM, "the second pair of outputs", "leaving_dbfs"), ".1f"))
A("The first state read equals lane B16b's last in all 618 entries both hold.",
  ("618", SRC, "get(d, 'compare.2.both') if get(d, 'compare.2.differ') == 0 else None", "d"))
CMP3 = "get(d, 'compare.3')"
A("Between B16c's two reads, two of the 668 entries both hold differ only in",
  ("B16c's «two» reads", SRC, "sum(1 for k, r in d['reads'].items() if k.startswith('b16c-') and r['kind'] == 'state')", "w"),
  ("reads, «two» of", SRC, f"{CMP3}['differ']", "w"),
  ("668", SRC, f"{CMP3}['both']", "d"))
A("two for each, the second one, which the first also caught. Both reads show",
  ("two", SRC, f"same(x['messages'][0] for x in {CMP3}['differing'])", "w"),
  ("one", SRC, f"same(x['messages'][1] for x in {CMP3}['differing'] if x['second_last_among_first'] and x['all_minus_infinity'])", "w"))
TS = lambda r: f"E('{r}', 'tone-summary')"
A("Lane B9's tone monitor read the playback RUNNING at every 0.2 s read of both",
  ("0.2", "runs/bcrf/events.jsonl", "same(q((E(r, 'tone-summary')['last_raw_ns'] - E(r, 'tone-summary')['first_raw_ns']) / Decimal(10 ** 9) / (E(r, 'tone-summary')['reads'] - 1), 1) for r in ('bcrf', 'baaf'))", ".1f"))
A("cases, 1,805 and 1,803 reads. It saw one trigger time and a monotonic hardware",
  ("1,805", "runs/bcrf/events.jsonl", "E('bcrf', 'tone-summary')['states']['RUNNING'] if E('bcrf', 'tone-summary')['states'] == {'RUNNING': E('bcrf', 'tone-summary')['reads']} else None", ",d"),
  ("1,803", "runs/baaf/events.jsonl", "E('baaf', 'tone-summary')['states']['RUNNING'] if E('baaf', 'tone-summary')['states'] == {'RUNNING': E('baaf', 'tone-summary')['reads']} else None", ",d"),
  ("one", "runs/bcrf/events.jsonl", "same(E(r, 'tone-summary')['trigger_times'] for r in ('bcrf', 'baaf'))", "w"))
# ---------------- B16c: bench as left
A("| DUT stream state | Both STREAM_INPUTs unbound; STREAM_INPUT 0, at `0205022001006000`, and STREAM_INPUT 1, at `041060010000bb80`; both maps as found; CLOCK_SOURCE 0, INTERNAL; all read back |",
  ("0205022001006000", "restore/census-endc.jsonl", "cen('restore/census-endc.jsonl', 'format-dut-5-0')['payload'][8:]", "s"),
  ("041060010000bb80", "restore/census-endc.jsonl", "cen('restore/census-endc.jsonl', 'format-dut-5-1')['payload'][8:]", "s"),
  ("CLOCK_SOURCE «0»,", "restore/census-endc.jsonl", "payload_word(cen('restore/census-endc.jsonl', 'clock', 'dut'), 8)", "d"), n=1, c="B16c: bench as left")
A("its CLOCK_DOMAIN on CLOCK_SOURCE 1, its CRF input, as found. It was set to 0 and back to 1 once per case, each read back |",
  ("CLOCK_SOURCE «1»,", "restore/census-endc.jsonl", "payload_word(cen('restore/census-endc.jsonl', 'clock', 'peer'), 8)", "d"),
  ("set to «0» and", "runs/bcrf/events.jsonl", "same(E(r, 'set-clock', tag='peer-internal')['readback'] for r in ('bcrf', 'baaf'))", "d"),
  ("back to «1» once", "runs/bcrf/events.jsonl", "same(E(r, 'set-clock', who='peer', tag='restore')['readback'] for r in ('bcrf', 'baaf'))", "d"),
  ("once", "runs/bcrf/events.jsonl", "same(len(ev(r, 'set-clock', tag='peer-internal')) for r in ('bcrf', 'baaf'))", "x"))
A("| Census, B16c's start against its end | 44 of 45 reads equal, the census's start record aside;",
  ("44", "", CR("census-startc", "census-endc", "census-compare-b16c", 0), "d"),
  ("45", "", CR("census-startc", "census-endc", "census-compare-b16c", 1), "d"))
A("| DUT saved state | NVM image seq 286 to 292, commits 52 to 58, `pend=0`, `VD_OK` |",
  ("286", "restore/dut-startc.txt", "nvm('restore/dut-startc.txt')['seq']", "d"),
  ("292", "restore/dut-endc.txt", "nvm('restore/dut-endc.txt')['seq']", "d"),
  ("52", "restore/dut-startc.txt", "nvm('restore/dut-startc.txt')['commits']", "d"),
  ("58", "restore/dut-endc.txt", "nvm('restore/dut-endc.txt')['commits']", "d"),
  ("0", "restore/dut-endc.txt", "nvm('restore/dut-endc.txt')['pend']", "d"))
A("| The tone | Stopped by its process ID at 08:03:52 CEST; the playback closed |",
  ("08:03:52", "runs/b16c-tone-stop.txt", "stamps('runs/b16c-tone-stop.txt', 'LOCK')[0]", "cest"))
CC = lambda role, dt, idx, i: f"cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', '{role}', {dt}, {idx}, {i})"
A("- **The peer's talkers** counted two more stream starts and stops each, one",
  ("two", "restore/counters-endc.jsonl", "same([" + ", ".join(CC('peer', 6, x, i) for x in (0, 2) for i in (0, 1)) + "])", "w"),
  ("one", "restore/counters-endc.jsonl", "same([" + ", ".join(CC('peer', 6, x, i) for x in (0, 2) for i in (0, 1)) + "]) // sum(1 for r in RUNS if r in ('bcrf', 'baaf'))", "w"))
A("per case. Its listeners of the DUT's talkers counted four MEDIA_RESETs each.",
  ("four", "restore/counters-endc.jsonl", "same([" + ", ".join(CC('peer', 5, x, 4) for x in (0, 8)) + "])", "w"))
A("- **The DUT's talkers** counted MEDIA_RESET 0 to 4 each; its listeners'",
  ("0", "restore/counters-startc.jsonl", f"same([{MR('restore/counters-startc.jsonl', 0)}, {MR('restore/counters-startc.jsonl', 1)}])", "d"),
  ("4", "restore/counters-endc.jsonl", f"same([{MR('restore/counters-endc.jsonl', 0)}, {MR('restore/counters-endc.jsonl', 1)}])", "d"))
A("- **The CLOCK_DOMAIN counters** read LOCKED / UNLOCKED 22 / 21 to 24 / 23 on",
  ("22", "restore/counters-startc.jsonl", "counters('restore/counters-startc.jsonl', 'dut', 36, 0)[0]", "d"),
  ("21", "restore/counters-startc.jsonl", "counters('restore/counters-startc.jsonl', 'dut', 36, 0)[1]", "d"),
  ("24", "restore/counters-endc.jsonl", "counters('restore/counters-endc.jsonl', 'dut', 36, 0)[0]", "d"),
  ("23", "restore/counters-endc.jsonl", "counters('restore/counters-endc.jsonl', 'dut', 36, 0)[1]", "d"))
A("the DUT and 6 / 5 to 8 / 7 on the peer.",
  ("6", "restore/counters-startc.jsonl", "counters('restore/counters-startc.jsonl', 'peer', 36, 0)[0]", "d"),
  ("5", "restore/counters-startc.jsonl", "counters('restore/counters-startc.jsonl', 'peer', 36, 0)[1]", "d"),
  ("8", "restore/counters-endc.jsonl", "counters('restore/counters-endc.jsonl', 'peer', 36, 0)[0]", "d"),
  ("7", "restore/counters-endc.jsonl", "counters('restore/counters-endc.jsonl', 'peer', 36, 0)[1]", "d"))
A("- **`SLIP_LB`** read 162 dups at the start and 188 at the end, every step",
  ("162", "restore/dut-startc.txt", slip('restore/dut-startc.txt'), "d"),
  ("188", "restore/dut-endc.txt", slip('restore/dut-endc.txt'), "d"))
# ---------------- B16c: #629 acceptance and limits
A("against lane B9's synthetic controls (PASS in lane B16). Against lane B6's four pass terms, three are met in each case",
  ("four", FIND, "len(re.split(r', and |, ', b6_rule()))", "w"),
  ("three", "summary/bcrf/c-b9-grade.json", f"same([{TERMS('bcrf')}, {TERMS('baaf')}])", "w"), c="B16c: #629 acceptance")
A("- One graded run per case, on this bench's DUT and reference peer only, each",
  ("One", "summary/bcrf/c-b9-grade.json", GRADED1, "W"), c="B16c: limits")
A("  with 300 s at McASP0, and 40 s of each tap. Lane B7's windows were 630 s;",
  ("300", "summary/bcrf/c-b9-grade.json", "same(grade(r)['seconds'] for r in ('bcrf', 'baaf'))", ".0f"),
  ("40", "summary/bcrf/a-peer-tap.json", "same(q(load(f'summary/{r}/{p}.json')['seconds'], 0) for r in ('bcrf', 'baaf') for p in ('a-peer-tap', 'b-dut-tap'))", "d"),
  ("630", FIND, "rx(FIND_P, r'^(\\d+) s, untouched, from (\\d+) s after the last bind or clock-source set')", "s"))
A("  one locked action must end within 10 minutes.",
  ("one", "runs/bcrf-lock.txt", "same(len(stamps(f'runs/{r}-lock.txt', 'LOCK')) for r in ('bcrf', 'baaf'))", "w"),
  ("10", "HANDOFF.md", "lock_limit()", "d"))
A("through the DUT's meters, +10.59 to +10.65 ppm against gPTP, not graded.",
  ("+10.59", "r2/bcrf-poll-receipt.json", "min(rates())", "+.2f"),
  ("+10.65", "r2/bcrf-poll-receipt.json", "max(rates())", "+.2f"))
A("- The servo's status carried bit 4, DRP config mismatch, at every ACQUIRE and",
  ("4", "r2/bcrf-poll-trace.tsv", "same(b for r in ('bcrf', 'baaf') for x in trace(r) if trace_state(x) in (3, 4) for b in [4 * ((int(x['0x8f8'], 16) >> 4) & 1)])", "d"))
A("In B0, 108 of the 131 lie beyond the taps and are assigned upstream by",
  ("108", R2B, "d['overlap']['degraded_beyond']", "d"), ("131", R2B, "d['degraded']", "d"))
A("- The degraded blocks of B0 and their absence here come from one run each.",
  ("one", "summary/b0-2/c-b9-grade.json", GRADED1, "w"))

# ---------------- B16, round 2: reduced receipts
WASP = "git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
OLD_RUNS = r"was(r'runs of blocks: (\d+) to (\d+), (\d+) to (\d+), (\d+) to (\d+) and later runs', {g})"
A("below, on 2026-10-12, documents only. Nothing on the bench was touched: no",
  ("2026-10-12", "git:35e332b6", "commit_time('35e332b6')", "date"), c="B16, round 2: reduced receipts")
A("| B0's floor at (c), `b0-2` | -123.98 dB on both tones |",
  ("-123.98", WASP, "was(r'\\| (-[\\d.]+) dB on both tones, `pts3` and `b0-2` \\|')", "s"),
  ("-123.98", R2B, "d['tones']['997 Hz']['floor_median_db']", ".2f"),
  ("-123.95", R2B, "d['tones']['9,973 Hz']['floor_median_db']", ".2f"),
  ("-123.98", "summary/pts3/c-b9-grade.json", "same(load('summary/pts3/c-b9-grade.json')['summary'][c + '_floor']['thdn_db_median'] for c in ('ch0', 'ch1'))", ".2f"))
A("| B0's degraded runs | 0 to 18, 28 to 31, 43 to 54 and later runs |",
  *[(v, WASP, OLD_RUNS.format(g=g), "s") for v, g in (("0", 1), ("18", 2), ("28", 3), ("31", 4), ("43", 5), ("54", 6))],
  *[(v, R2B, f"d['degraded_runs'][{i}][{j}]", "d") for v, (i, j) in (("0", (0, 0)), ("18", (0, 1)), ("28", (1, 0)), ("31", (1, 1)), ("43", (2, 0)), ("44", (2, 1)), ("46", (3, 0)), ("54", (3, 1)))],
  ("eleven", R2B, "len(d['degraded_runs']) - 4", "w"),
  ("45", R2B, "next(i for i in range(d['degraded_runs'][2][1] + 1, d['degraded_runs'][3][0]))", "d"))
A("| B0's recording start | From 06:38:03, 24 s after the last bind |",
  ("06:38:03", WASP, "was(r'McASP0 300 s from ([\\d:]+) while playing the loop')", "s"),
  ("24", WASP, "was(r'It starts (\\d+) s after the last bind')", "s"),
  ("06:38:05.2", "runs/b0-2/events.jsonl", "E('b0-2', 'captures-started')['started']['mcasp'] + r2lead()", "cest1"),
  ("26", R2B, "d['timing']['recording_after_binds_s']", ".0f"),
  ("06:38:03.2", "runs/b0-2/events.jsonl", "E('b0-2', 'captures-started')['started']['mcasp']", "cest1"),
  ("2", "tools/run_b16.py", "r2lead()", "d"))
A("| `pts2`'s start at McASP0, found by the operator's own check | As `pts1`, from 06:28:25 |",
  ("06:28:25", WASP, "was(r'\\| As `pts1`, from ([\\d:]+)\\. McASP0 also plays')", "s"),
  ("06:28:31.5", "runs/pts2/events.jsonl", "E('pts2', 'captures-started')['started']['mcasp'] + r2lead()", "cest1"),
  ("2", "tools/run_b16.py", "r2lead()", "d"))
A("| B-CRF and B-AAF against lane B6 | Three terms, all met |",
  ("Three", WASP, "was(r'the tone path\\. All (\\w+) are met here\\.').capitalize()", "s"),
  ("four", FIND, "len(re.split(r', and |, ', b6_rule()))", "w"),
  ("three", "summary/bcrf/c-b9-grade.json", f"same([{TERMS('bcrf')}, {TERMS('baaf')}])", "w"))
A("| B0's attribution | 131 degraded blocks in the peer's talker stream, reaching (c) unchanged |",
  ("131", WASP, "was(r'There its talker stream already held (\\d+) blocks off the floor')", "s"),
  ("131", R2B, "d['degraded']", "d"), ("23", R2B, "d['overlap']['degraded_inside']", "d"),
  ("34.1", R2B, "d['overlap']['seconds']", ".1f"), ("108", R2B, "d['overlap']['degraded_beyond']", "d"))
A("| B16c's first counter mark | At the window's start |",
  ("20", "runs/bcrf/events.jsonl", "same(q(E(r, 'mark', tag='window-mark-0')['t'] - E(r, 'set-clock', who='dut', tag=r)['t'], 0) for r in ('bcrf', 'baaf'))", "d"),
  ("6", "runs/bcrf/events.jsonl", "same(q(E(r, 'captures-started')['started']['mcasp'] + r2lead() - E(r, 'mark', tag='window-mark-0')['t'], 0) for r in ('bcrf', 'baaf'))", "d"))
A("| B16b's state comparison | Four entries differ |",
  ("Four", WASP, "was(r'1,255 both hold, (\\w+) differ').capitalize()", "s"),
  ("Two", SRC, f"sum(1 for x in {CMP1}['differing'] if x['cls'] != 'an input of a monitoring mix')", "W"),
  ("two", SRC, f"sum(1 for x in {CMP1}['differing'] if x['cls'] == 'an input of a monitoring mix')", "w"))
A("| B16's other source outputs | Silent | No reading above -135.2 dBFS |",
  ("-135.2", SRC, "max(get(d, 'reads.' + k + '.meters.every other output.largest_before_setting_dbfs') for k in ('b16-state-1', 'b16-meters-1', 'b16-meters-2', 'b16-state-2'))", ".1f"))
A("| B16c's `SLIP_LB` steps | 2.66 s, 2.65 s and 5.68 s after the set |",
  ("2.66", WASP, "was(r'- B-CRF: one step, ([\\d.]+) s after the set;')", "s"),
  ("2.65", WASP, "was(r'- B-AAF: two steps, ([\\d.]+) s and ([\\d.]+) s after the set\\.')", "s"),
  ("5.68", WASP, "was(r'- B-AAF: two steps, ([\\d.]+) s and ([\\d.]+) s after the set\\.', 2)", "s"),
  ("two", "r2/bcrf-poll-receipt.json", f"same(len(x['polls']) for x in {ALLST})", "w"),
  ("2.08", "r2/bcrf-poll-receipt.json", f"{ACQ('bcrf')}[0]['after_set_s'][0]", ".2f"),
  ("2.66", "r2/bcrf-poll-receipt.json", f"{ACQ('bcrf')}[0]['after_set_s'][1]", ".2f"),
  ("2.08", "r2/baaf-poll-receipt.json", f"{ACQ('baaf')}[0]['after_set_s'][0]", ".2f"),
  ("2.65", "r2/baaf-poll-receipt.json", f"{ACQ('baaf')}[0]['after_set_s'][1]", ".2f"),
  ("5.10", "r2/baaf-poll-receipt.json", f"{ACQ('baaf')}[1]['after_set_s'][0]", ".2f"),
  ("5.68", "r2/baaf-poll-receipt.json", f"{ACQ('baaf')}[1]['after_set_s'][1]", ".2f"))
A("  lists every `SLIP_LB` step with its two polls' times and servo states. The",
  ("two", "r2/bcrf-poll-receipt.json", f"same(len(x['polls']) for x in {ALLST})", "w"))
A("  trace beside each receipt holds every poll's eight raw words and its time",
  ("eight", "r2/bcrf-poll-trace.tsv", "same(len([k for k in trace(r)[0] if k.startswith('0x')]) for r in ('bcrf', 'baaf'))", "w"))
A("  It recomputes the run's own LOCKED brackets, 2.657 to 3.161 s and 6.68 to",
  ("2.657", "r2/bcrf-poll-receipt.json", "same([d['locked']['recomputed_s'][0], d['locked']['published'][0], E('bcrf', 'servo-state')['s_lo']])", ".3f"),
  ("3.161", "r2/bcrf-poll-receipt.json", "same([d['locked']['recomputed_s'][1], d['locked']['published'][1], E('bcrf', 'servo-state')['s_hi']])", ".3f"),
  ("6.68", "r2/baaf-poll-receipt.json", "same([load('r2/baaf-poll-receipt.json')['locked']['recomputed_s'][0], E('baaf', 'servo-state')['s_lo']])", ".2f"))
A("  7.18 s. Those open at the end of the last poll that read ACQUIRE. That poll",
  ("7.18", "r2/baaf-poll-receipt.json", "same([load('r2/baaf-poll-receipt.json')['locked']['recomputed_s'][1], E('baaf', 'servo-state')['s_hi']])", ".2f"))
A("  start instead, 2.585 s and 6.602 s; see",
  ("2.585", "r2/bcrf-poll-trace.tsv", "lock_bracket('bcrf')[0]", ".3f"),
  ("6.602", "r2/baaf-poll-trace.tsv", "lock_bracket('baaf')[0]", ".3f"))
A("- **The tone source's reads.** `r2_source_b16.py` reads the twelve retained",
  ("twelve", SRC, "len(d['reads'])", "w"))
A("  reads, four per lane, and a class map. The map says which of the source's",
  ("four", SRC, "same(sum(1 for k in d['reads'] if k.split('-')[0] == lane) for lane in ('b16', 'b16b', 'b16c'))", "w"))
A("(`controls/r2-controls.json`, 6 of 6 PASS): a changed byte in the raw poll is",
  ("«6» of 6", "controls/r2-controls.json", "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
  ("6 of «6»", "controls/r2-controls.json", "len(d['controls'])", "d"))
A("python3 -I tools/r2_source_b16.py <class map> <list of the twelve reads> r2/source-receipt.json",
  ("twelve", SRC, "len(d['reads'])", "w"))
A("The tone source's twelve reads, now also listed in the packet's",
  ("twelve", "RAW-ARTIFACTS.json", "sum(1 for x in d['files'] if x['path'].startswith('source/'))", "w"))
A("The two raw polls are those in [B16c: artifact hashes](#b16c-artifact-hashes):",
  ("two", "RAW-ARTIFACTS.json", "sum(1 for x in d['files'] if x['path'].endswith('/poll-run.jsonl'))", "w"))
A("`9cfc79bb...` (B-CRF) and `476a0077...` (B-AAF).",
  ("9cfc79bb...", "RAW-ARTIFACTS.json", "same([raw('bcrf/poll-run.jsonl')['sha256'], load('r2/bcrf-poll-receipt.json')['raw']['sha256']])[:8] + '...'", "s"),
  ("476a0077...", "RAW-ARTIFACTS.json", "same([raw('baaf/poll-run.jsonl')['sha256'], load('r2/baaf-poll-receipt.json')['raw']['sha256']])[:8] + '...'", "s"))
A("| `controls/r2-controls.json` (6 of 6 PASS) |",
  ("«6» of 6", "controls/r2-controls.json", "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
  ("6 of «6»", "controls/r2-controls.json", "len(d['controls'])", "d"))
A("| `controls/b16c-dryrun-summary.json` (8 of 8 scenarios) |",
  ("«8» of 8", "controls/b16c-dryrun-summary.json", "sum(v == 'PASS' for v in d['scenarios'].values())", "d"),
  ("8 of «8»", "controls/b16c-dryrun-summary.json", "len(d['scenarios'])", "d"))

# ---------------- bindings stated by descriptor index (the index is the state read back)
IDX = lambda s_: f"int({s_}.split('-')[-1])"
A("| `b0` | `b0` | 06:31:28 to 06:37:05 |",
  ("its STREAM_OUTPUT «2», to", "runs/b0/events.jsonl", IDX("E('b0', 'bind', listener='dut-in-1')['talker']"), "d"),
  ("to the DUT's STREAM_INPUT «1», then", "runs/b0/events.jsonl", IDX("E('b0', 'bind', talker='peer-out-2')['listener']"), "d"))
A("bound, its CRF to the DUT's STREAM_INPUT 1 and its AAF to STREAM_INPUT 0. The",
  ("STREAM_INPUT «1» and", "runs/b0-2/events.jsonl", "same(" + IDX("E(r, 'bind', talker='peer-out-2')['listener']") + " for r in ('b0', 'b0-2'))", "d"),
  ("to STREAM_INPUT «0».", "runs/b0-2/events.jsonl", "same(" + IDX("E(r, 'bind', talker='peer-out-0')['listener']") + " for r in ('b0', 'b0-2'))", "d"))
for anchor, cen_f in (("| Reference peer | STREAM_INPUT 0, bound to the DUT's STREAM_OUTPUT 0, at `0205022002006000`,", "restore/census-endb.jsonl"),
                      ("| Reference peer | STREAM_INPUT 0, bound to the DUT's STREAM_OUTPUT 0, STREAM_INPUT 8 to the DUT's STREAM_OUTPUT 1; its CLOCK_DOMAIN on CLOCK_SOURCE 1, its CRF input", "restore/census-endc.jsonl")):
    A(anchor,
      ("bound to the DUT's STREAM_OUTPUT «0»", cen_f, f"cen('{cen_f}', 'rx-state-peer-0')['talker_uid'] if cen('{cen_f}', 'rx-state-peer-0')['talker'] == '020000fffe000001' else None", "d"),
      ("STREAM_INPUT 8 to the DUT's STREAM_OUTPUT «1»;", cen_f, f"cen('{cen_f}', 'rx-state-peer-8')['talker_uid'] if cen('{cen_f}', 'rx-state-peer-8')['talker'] == '020000fffe000001' else None", "d"))
A("   STREAM_INPUT 8, bound to the DUT's STREAM_OUTPUT 1, as found.",
  ("STREAM_OUTPUT «1»,", "runs/bcrf/events.jsonl", "same(E(r, 'fol-check')['peer_in_8']['talker_uid'] for r in ('bcrf', 'baaf'))", "d"))
A("4. Bind the peer's CRF talker to the DUT's STREAM_INPUT 1 and its AAF talker",
  ("STREAM_INPUT «1» and", "runs/bcrf/events.jsonl", "same(" + IDX("E(r, 'bind', talker='peer-out-2')['listener']") + " for r in ('bcrf', 'baaf'))", "d"))
A("   to STREAM_INPUT 0, under the binding rule.",
  ("STREAM_INPUT «0»,", "runs/bcrf/events.jsonl", "same(" + IDX("E(r, 'bind', talker='peer-out-0')['listener']") + " for r in ('bcrf', 'baaf'))", "d"))

# ---------------- B16, round 3: figures check
W3 = lambda pat, g=1: f"was({pat!r}, {g}, at='35e332b6')"
A("stored as 122.475 dB, shows as 122.48. Clock times are cut to the last digit",
  ("122.475", "summary/pts3/a-peer-tap.json", "T(d, 1, 'snr_db')", "s"),
  ("122.48", "summary/pts3/a-peer-tap.json", "T(d, 1, 'snr_db')", ".2f"))
A("shown, as a clock shows them: lane B16b's identity gate ended at 06:22:34.993",
  ("06:22:34.993", "identity-b16b/lock-window.txt", "stamps(p, 'UNLOCK')[0]", "cest3"))
A("and shows as 06:22:34.",
  ("06:22:34", "identity-b16b/lock-window.txt", "stamps(p, 'UNLOCK')[0]", "cest"))
A("Its controls ran on altered copies (`controls/r3-controls.json`, 5 of 5 PASS,",
  ("«5» of 5", "controls/r3-controls.json", "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
  ("5 of «5»", "controls/r3-controls.json", "len(d['controls'])", "d"))
PL = "r3/playback-logs.json"
A("The playback's two retained logs are now listed in the packet's",
  ("two", "RAW-ARTIFACTS.json", "same([sum(1 for x in d['files'] if x['path'].startswith('playback/')), sum(1 for v in load('r3/playback-logs.json')['logs'].values() if 'sha256' in v)])", "w"))
for lane, f in (("b16", "b16-tone-play.log"), ("b16c", "b16c-tone-play.log")):
    A(f"| `{f}`, lane {lane.upper().replace('B16C', 'B16c')}'s |",
      (("06:02:00" if lane == "b16" else "08:03:53"), PL, f"d['logs']['{lane}']['modified']", "s"),
      ("| «0» |", PL, f"d['logs']['{lane}']['underrun_lines']", "d"),
      ("dab353b5ead02cb68b5ecebc757786c48b7672e6f93a37a152e37aedf9dfe43b", "RAW-ARTIFACTS.json", f"same([raw('playback/{f}')['sha256'], load('{PL}')['logs']['{lane}']['sha256']])", "s"))
A("The two logs are byte-equal: each holds the playback's setup, the stop",
  ("two", "RAW-ARTIFACTS.json", "len({x['sha256'] for x in d['files'] if x['path'].startswith('playback/')}) == 1 and sum(1 for x in d['files'] if x['path'].startswith('playback/'))", "w"))
F1 = r"\(a\) at (-[\d.]+) dB median, worst block (-[\d.]+) dB, on both tones in both cases"
A("| R625-2-F1: B16c's attribution at (a) |",
  ("-123.98", "", W3(F1), "s"), ("-123.93", "", W3(F1, 2), "s"),
  ("-123.98/-123.97", "summary/bcrf/a-peer-tap.json", f"{PM('bcrf', 0, 997)} + '/' + {PM('bcrf', 1, 9973)}", "s"),
  ("-123.98/-123.98", "summary/baaf/a-peer-tap.json", f"{PM('baaf', 0, 997)} + '/' + {PM('baaf', 1, 9973)}", "s"),
  ("-123.93", "summary/bcrf/a-peer-tap.json", "same(q(pt(r, 'a', c, t)['worst_thdn_db'], 2) for r in ('bcrf', 'baaf') for c, t in ((0, 997), (1, 9973)))", ".2f"))
PF = r"at the floor in (\d+) of (\d+) blocks; block 2"
P2 = r"the loop's floor, in (\d+) of (\d+) blocks\."
A("| R624-2-F1: the positive control's floor at (d) |",
  ("305", "", W3(PF), "s"), ("306", "", W3(PF, 2), "s"), ("13", "", W3(P2), "s"), ("16", "", W3(P2, 2), "s"),
  ("303", DB2, f"same(n for t in ({T997}, {T9973}) for n in (len(floor_inside(t)), len(inside(t['per_block']))))", "d"),
  ("11", DP2, f"same(len(floor_inside(t)) for t in ({T997}, {T9973}))", "d"),
  ("of «13»,", DP2, f"same(len(inside(t['per_block'])) for t in ({T997}, {T9973}))", "d"),
  ("blocks «6» and", DP2, f"same([i for i in inside(t['per_block']) if i not in floor_inside(t)][0] for t in ({T997}, {T9973}))", "d"),
  ("and «12» holding", DP2, f"same([i for i in inside(t['per_block']) if i not in floor_inside(t)][1] for t in ({T997}, {T9973}))", "d"),
  ("Blocks «0» and 1", DB2, f"same(silent(t['per_block'])[0] for t in ({T997}, {T9973}))", "d"),
  ("0 and «1» precede", DB2, f"same(silent(t['per_block'])[-1] for t in ({T997}, {T9973}))", "d"),
  ("block «2» holds", DB2, f"same(inside(t['per_block'])[0] - 1 for t in ({T997}, {T9973}))", "d"))
A("| R624-2-F1: the taps in `pts2` |",
  ("15", "summary/pts2/ctl-dut-talker-dut-tap.json", f"same(n for x in {TT} for n in (len(floor_inside(x)), len(inside(x['per_block']))))", "d"))
LB = lambda case: rf"\| {case} \| ([\d.]+) to ([\d.]+) s; ACQUIRE"
A("| R624-2-F2: B16c's LOCKED brackets |",
  ("2.66", "", W3(LB("B-CRF")), "s"), ("3.16", "", W3(LB("B-CRF"), 2), "s"),
  ("6.68", "", W3(LB("B-AAF")), "s"), ("7.18", "", W3(LB("B-AAF"), 2), "s"),
  ("2.585", "r2/bcrf-poll-trace.tsv", "lock_bracket('bcrf')[0]", ".3f"), ("3.161", "r2/bcrf-poll-receipt.json", "lock_bracket('bcrf')[1]", ".3f"),
  ("6.602", "r2/baaf-poll-trace.tsv", "lock_bracket('baaf')[0]", ".3f"), ("7.180", "r2/baaf-poll-receipt.json", "lock_bracket('baaf')[1]", ".3f"))
A("| R624-2-R1: the tone source's state |",
  ("Two", "", W3(r"So (\w+) settings changed: the clock setting") + ".capitalize()", "s"),
  ("1,255", SRC, f"{CMP1}['both']", ",d"),
  ("618", SRC, "get(d, 'compare.2.both')", "d"), ("668", SRC, "get(d, 'compare.3.both')", "d"))
A("| R624-2-R2: the five `SLIP_LB` steps before the set |",
  ("five", "r2/bcrf-poll-receipt.json", f"same([len({PRE('bcrf')}), len({PRE('baaf')})])", "w"),
  ("one", "runs/b0-2/dut-after-captures.txt", "same((slipb(f'runs/{r}/dut-after-captures.txt') - slipb(f'runs/{r}/dut-before-binds.txt')) // 2 for r in ('b0', 'b0-2'))", "w"))
A("| R624-2-S1: the servo status bit 4 |",
  ("4", "r2/bcrf-poll-trace.tsv", "same(b for r in ('bcrf', 'baaf') for x in trace(r) if trace_state(x) in (3, 4) for b in [4 * ((int(x['0x8f8'], 16) >> 4) & 1)])", "d"))
A("| B16: the identity gate | 05:45:07 to 05:45:13 |",
  ("05:45:07", "", W3(r"\| Identity gate \| PASS, ([\d:]+) to ([\d:]+) CEST \|"), "s"),
  ("05:45:13", "", W3(r"\| Identity gate \| PASS, ([\d:]+) to ([\d:]+) CEST \|", 2), "s"),
  ("05:45:06", "identity/lock-window.txt", "stamps(p, 'LOCK')[0]", "cest"),
  ("05:45:12", "identity/lock-window.txt", "stamps(p, 'UNLOCK')[0]", "cest"))
TONEW = r"inputs through the authorised tone source, from ([\d:]+) to ([\d:]+) CEST"
A("| B16: the tone | From 05:55:38 to 06:02:00 |",
  ("05:55:38", "", W3(TONEW), "s"), ("06:02:00", "", W3(TONEW, 2), "s"),
  ("05:55:37", "runs/tone-start.txt", "stamps(p, 'STATUS')[0] - Decimal(rx(p, r'hw_ptr : (\\d+)')) / 48000", "cest"),
  ("06:01:59", "runs/tone-stop.txt", "stamps(p, 'LOCK')[0]", "cest"))
A("| B16: `loop1` and `loop2` |",
  ("05:56:31", "", W3(r"\| `loop1` \| ([\d:]+) to ([\d:]+) \|"), "s"), ("05:57:31", "", W3(r"\| `loop1` \| ([\d:]+) to ([\d:]+) \|", 2), "s"),
  ("06:00:29", "", W3(r"\| `loop2` \| [\d:]+ to ([\d:]+) \|"), "s"),
  ("05:56:30", "runs/loop1-lock.txt", "stamps(p, 'LOCK')[0]", "cest"), ("05:57:30", "runs/loop1-lock.txt", "stamps(p, 'UNLOCK')[0]", "cest"),
  ("06:00:28", "runs/loop2-lock.txt", "stamps(p, 'UNLOCK')[0]", "cest"))
A("| B16: the tap after the probes |",
  ("49", "", W3(r"in the remaining (\d+) s of the capture"), "s"),
  ("49.6", ACMP, f"E('loop2', 'capture-done', what='tap')['seconds'] - {acmp_t('CONNECT_TX_COMMAND', 1)}", ".1f"))
A("| B16: lane B15's `pts1` |",
  ("0x0002", "", W3(r"same: rx state flags `(0x[0-9a-f]+)`, stream ID (\d+),"), "s"),
  ("ID «0»,", "", W3(r"same: rx state flags `(0x[0-9a-f]+)`, stream ID (\d+),", 2), "s"),
  ("counters «0»", FIND, "rx(FIND_P, r'nothing\\. Its counters stayed (\\d+) and its digital output read exact zero')", "s"))
A("| B16: the state reads |",
  ("05:48", "", W3(r"at ([\d:]+) and ([\d:]+) CEST\. The two reads are identical"), "s"),
  ("05:48 and «06:01» | At", "", W3(r"at ([\d:]+) and ([\d:]+) CEST\. The two reads are identical", 2), "s"),
  ("05:47", SRC, "Decimal(clock(get(d, 'reads.b16-state-1.at')))", "hm"),
  ("05:47 and «06:01» |", SRC, "Decimal(clock(get(d, 'reads.b16-state-2.at')))", "hm"))
A("| B16b: the resume |",
  ("06:20", "", W3(r"resumed at ([\d:]+) CEST on the same image, branch"), "s"),
  ("06:22:23", "soc/b16b-precheck-status.log", "stamps(p, 'LOCK')[0]", "cest"))
LV = r"at (-[\d.]+) dBFS before ([\d:]+) CEST and (-[\d.]+) dBFS after"
A("| B16b: the tone's level at (a) |",
  ("-14.14", "", W3(LV), "s"), ("06:29", "", W3(LV, 2), "s"), ("-14.10", "", W3(LV, 3), "s"),
  ("06:28:50", "summary/pts2/a-peer-tap.json", "d['info']['last_t']", "cest"),
  ("06:31:51", "summary/b0/a-peer-tap.json", "d['info']['first_t']", "cest"))
A("| B16b: phase drift before the change |",
  ("+3.00", "", W3(r"\| (\+[\d.]+) frames in 10 s, smooth"), "s"),
  ("10", "summary/pts1/c-b9-grade.json", "same(grade(r)['seconds'] for r in ('pts1', 'pts2'))", ".0f"),
  ("+3.00", "summary/pts1/c-b9-grade.json", "d['phase_net_frames']", "+.2f"),
  ("+3.01", "summary/pts2/c-b9-grade.json", "d['phase_net_frames']", "+.2f"))
A("| B16b: the offset before the change |",
  ("+6.95", "", W3(r"The (\+[\d.]+) ppm tone advanced"), "s"),
  ("+6.94", "summary/pts1/a-peer-tap.json", "min(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))", "+.2f"),
  ("+6.96", "summary/pts1/a-peer-tap.json", "max(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))", "+.2f"))
UR = r"records (\w+) underruns, ([\d.]+) to ([\d.]+) s each"
A("| B16b: the playback's underruns |",
  ("«Five», 0.43", "", W3(UR) + ".capitalize()", "s"), ("0.43", "", W3(UR, 2), "s"), ("1.63", "", W3(UR, 3), "s"),
  ("«Five», from", "HANDOFF.md", f"rx('HANDOFF.md', {HB17}).capitalize()", "s"),
  ("06:45:27", "HANDOFF.md", f"rx('HANDOFF.md', {HB17}, group=2)", "s"),
  ("06:46:38", "HANDOFF.md", f"rx('HANDOFF.md', {HB17}, group=3)", "s"))
A("| B16c: the resume |",
  ("07:32", "", W3(r"resumed at ([\d:]+) CEST on the same image and branch"), "s"),
  ("07:48:07", "soc/b16c-precheck-status.log", "stamps(p, 'LOCK')[0]", "cest"))
RT = r"\| `bcrf` \| [\d:]+ to [\d:]+ \| ([\d:.]+) \| ([\d:.]+) \| CLOCK_SOURCE 1, ([\d:.]+) \| ([\d:]+) to ([\d:]+), from 26 s after the set \| [\d:.]+ to ([\d:.]+) \|"
RA = r"\| `baaf` \| [\d:]+ to [\d:]+ \| [\d:.]+ \| [\d:.]+ \| CLOCK_SOURCE 2, [\d:.]+ \| [\d:]+ to [\d:]+, from 26 s after the set \| ([\d:.]+) to ([\d:.]+) \|"
A("| B16c: the run table |",
  *[(v, "", W3(RT, g), "s") for v, g in (("07:50:12.4", 1), ("07:50:17.6", 2), ("07:50:29.8", 3), ("07:50:56", 4), ("07:55:56", 5), ("07:56:04.1", 6))],
  ("08:02:51.8", "", W3(RA, 1), "s"), ("08:02:55.8", "", W3(RA, 2), "s"),
  ("07:50:12.3", "runs/bcrf/events.jsonl", "E('bcrf', 'set-clock', tag='peer-internal')['t']", "cest1"),
  ("07:50:17.5", "runs/bcrf/events.jsonl", "E('bcrf', 'bind', i=-1)['t']", "cest1"),
  ("07:50:29.7", "runs/bcrf/events.jsonl", "E('bcrf', 'set-clock', tag='bcrf')['t']", "cest1"),
  ("07:50:55", "runs/bcrf/events.jsonl", "E('bcrf', 'captures-started')['started']['mcasp'] + r2lead()", "cest"),
  ("07:55:55", "runs/bcrf/events.jsonl", "E('bcrf', 'captures-started')['started']['mcasp'] + r2lead() + grade('bcrf')['seconds']", "cest"),
  ("07:56:04.0", "runs/bcrf/events.jsonl", "E('bcrf', 'mark', tag='after-restore')['t']", "cest1"),
  ("08:02:51.7", "runs/baaf/events.jsonl", "E('baaf', 'teardown')['t']", "cest1"),
  ("08:02:55.7", "runs/baaf/events.jsonl", "E('baaf', 'mark', tag='after-restore')['t']", "cest1"))
A("| B16c: (d)'s decoded span |",
  ("«303.8» s in each", "", W3(r"over ([\d.]+) s in each case\. One frame"), "s"),
  ("«303.8» s and", "summary/bcrf/d-loop-decode.json", "d['decoded'] / 48000", ".1f"),
  ("303.9", "summary/baaf/d-loop-decode.json", "d['decoded'] / 48000", ".1f"))
A("| B16c: the peer's rate |",
  ("+10.6", "", W3(r"through the DUT's meters, (\+[\d.]+) ppm against gPTP"), "s"),
  ("+10.59", "r2/bcrf-poll-receipt.json", "min(rates())", "+.2f"),
  ("+10.65", "r2/bcrf-poll-receipt.json", "max(rates())", "+.2f"))
REW = ("plus one change", "one PDU", "one step earlier", "one request", "the two lanes", "one route")
NEWTXT = "re.sub(r'\"[^\"]*\"', '', ' '.join(t for t, _ in scope().values()))"
A("Six number words with no receipt were reworded: \"plus one change\", \"one PDU\",",
  ("Six", "", f"sum(1 for x in {REW!r} if x in load('git:35e332b6:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md') and x not in {NEWTXT})", "W"))

# ---------------- the page's Contents entry and the README row's lane B16 part
A("every block at the floor, no discontinuity, three of lane B6's four terms met and its timed ratio not run",
  ("three", "summary/bcrf/c-b9-grade.json", f"same([{TERMS('bcrf')}, {TERMS('baaf')}])", "w"),
  ("B6's «four» terms", FIND, "len(re.split(r', and |, ', b6_rule()))", "w"), c="the page's Contents entry for lane B16")
RM = "README.md"
A("the peer's listener probed it twice over the network with no answer",
  ("twice", ACMP, "sum(x['msg'] == 'CONNECT_TX_COMMAND' for x in d['acmp'])", "x"), doc=RM, c="the README row's lane B16 part")
A("(997 Hz and 9,973 Hz at -14.1 dBFS) and reaches the DUT's link and TDM output sample for sample in four runs",
  ("-14.1", "summary/pts1/a-peer-tap.json", f"same(q({LVL}, 1) for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3'))", ".1f"),
  ("four", "summary/pts1/align-a-c.json", "sum(1 for r in RUNS if (ROOT / f'summary/{r}/align-a-c.json').exists() and r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') and align(r, 'a')['frames_differing'] == 0)", "w"), doc=RM)
A("B0, the DUT on INTERNAL, is graded over 300 s: THD+N -123.95 dB and -122.80 dB median, no discontinuity; 131 of its 300 blocks",
  ("«300» s:", G02, "d['seconds']", ".0f"),
  ("-123.95", G02, "d['summary']['ch0_all']['thdn_db_median']", ".2f"),
  ("-122.80", G02, "d['summary']['ch1_all']['thdn_db_median']", ".2f"),
  ("131", R2B, "d['degraded']", "d"),
  ("its «300» blocks", R2B, "d['blocks']", "d"), doc=RM)
A("Inside the 34.1 s the taps cover, every impairment, 23 of those blocks among them,",
  ("34.1", R2B, "d['overlap']['seconds']", ".1f"), ("23", R2B, "d['overlap']['degraded_inside']", "d"), doc=RM)
A("the other 108 are assigned upstream by inference. No DUT change was made. The tone source",
  ("108", R2B, "d['overlap']['degraded_beyond']", "d"), doc=RM)
A("B-CRF and B-AAF are graded over 300 s at the DUT's TDM output.",
  ("300", "summary/bcrf/c-b9-grade.json", "same(grade(r)['seconds'] for r in ('bcrf', 'baaf'))", ".0f"), doc=RM)
A("The servo read LOCKED 2.585 to 3.161 s and 6.602 to 7.180 s after the set",
  ("2.585", "r2/bcrf-poll-trace.tsv", "lock_bracket('bcrf')[0]", ".3f"), ("3.161", "r2/bcrf-poll-receipt.json", "lock_bracket('bcrf')[1]", ".3f"),
  ("6.602", "r2/baaf-poll-trace.tsv", "lock_bracket('baaf')[0]", ".3f"), ("7.180", "r2/baaf-poll-receipt.json", "lock_bracket('baaf')[1]", ".3f"), doc=RM)
A("THD+N is -123.98 dB at 997 Hz and -123.97 dB at 9,973 Hz median, with all 300 blocks at the path's floor",
  ("-123.98", "summary/bcrf/c-b9-grade.json", "same(grade(r)['summary']['ch0_all']['thdn_db_median'] for r in ('bcrf', 'baaf'))", ".2f"),
  ("-123.97", "summary/bcrf/c-b9-grade.json", "same(grade(r)['summary']['ch1_all']['thdn_db_median'] for r in ('bcrf', 'baaf'))", ".2f"),
  ("300", "summary/bcrf/c-b9-grade.json", "same(n for r in ('bcrf', 'baaf') for n in (grade(r)['summary']['blocks'], grade(r)['summary']['blocks_at_floor']))", "d"), doc=RM)
A("the positive control shows 0 net steps between the DUT's TDM clock and the peer's output.",
  ("0", "summary/bcrf/d-loop-decode.json", "same(dec(r)['net_step_frames'] for r in ('bcrf', 'baaf'))", "d"), doc=RM)
A("Against lane B6's four pass terms, three are met in each case and the timed ratio was not run. No DUT change",
  ("four", FIND, "len(re.split(r', and |, ', b6_rule()))", "w"),
  ("three", "summary/bcrf/c-b9-grade.json", f"same([{TERMS('bcrf')}, {TERMS('baaf')}])", "w"), doc=RM)
A("| `controls/r3-controls.json` (5 of 5 PASS) |",
  ("«5» of 5", "controls/r3-controls.json", "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
  ("5 of «5»", "controls/r3-controls.json", "len(d['controls'])", "d"))

# ---------------- round 4: tokens a removed category covered, now each with a row
B16B_C = ("pts1", "pts2", "b0-2", "pts3")
A("[Dev 5603c353, 2026-10-12: lane B16](#dev-5603c353-2026-10-12-lane-b16).",
  ("2026-10-12", "identity/lock-window.txt", "stamps('identity/lock-window.txt', 'LOCK')[0]", "date"), c="round 4: link labels")
A("- **[Dev 5603c353, 2026-10-12: lane B16](#dev-5603c353-2026-10-12-lane-b16)**",
  ("2026-10-12", "identity/lock-window.txt", "stamps('identity/lock-window.txt', 'LOCK')[0]", "date"),
  ("at the «four» points", "summary/bcrf/c-b9-grade.json", "same(points(r) for r in ('bcrf', 'baaf'))", "w"))
A("Lane B15's four-point capture was to run with the DUT's",
  ("«four»-point", "summary/pts1/c-mcasp.json", f"same(points(r) for r in {B16B_C!r})", "w"), c="round 4: the four capture points")
A("See [B16b: the four points](#b16b-the-four-points) |",
  ("[B16b: the «four» points]", "summary/pts1/c-mcasp.json", f"same(points(r) for r in {B16B_C!r})", "w"))
A("### B16b: the four points",
  ("«four»", "summary/pts1/c-mcasp.json", f"same(points(r) for r in {B16B_C!r})", "w"))
A("| The four points | TONE PRESENT at (a), (b) and (c); (d) PRESENT |",
  ("The «four» points", "summary/bcrf/c-mcasp.json", "same(points(r) for r in ('bcrf', 'baaf'))", "w"))
A("| Step 4, B0: the DUT on INTERNAL | Graded |",
  ("«one»-second", "summary/b0-2/c-b9-grade.json", "blk_grade(('b0-2',))", "w"), c="round 4: block length, bit width, floor, frame step, limit")
A("| B-CRF: the DUT follows the peer's CRF talker | Graded |",
  ("«one»-second", "summary/bcrf/c-b9-grade.json", "blk_grade(('bcrf',))", "w"))
A("THD+N and SNR per one-second block. `align_b16.py` compares (c) with (a) and",
  ("«one»-second", "summary/pts1/c-mcasp.json", f"blk_points({B16B_C!r})", "w"))
A("zero. Each THD+N cell is the median over one-second blocks, with the worst",
  ("«one»-second", "summary/pts1/c-mcasp.json", f"blk_points({B16B_C!r})", "w"), n=0)
A("are zero. Each THD+N cell is the median over one-second blocks, with the worst",
  ("«one»-second", "summary/bcrf/c-mcasp.json", "blk_points(('bcrf', 'baaf'))", "w"))
A("with (b) on full 24-bit values. `b9_thdn.py grade` grades McASP0's recording",
  ("«24»-bit", "summary/pts1/align-a-c.json", f"cmp_bits({B16B_C!r})", "d"))
A("(c) against (a) and (b), on full 24-bit values:",
  ("«24»-bit", "summary/pts1/align-a-c.json", f"cmp_bits({B16B_C!r})", "d"), n=0)
A("(c) against (a) and (b), on full 24-bit values:",
  ("«24»-bit", "summary/bcrf/align-a-c.json", "cmp_bits(('bcrf', 'baaf'))", "d"), n=1)
A("(c); `align_b16.py` on full 24-bit values; `b9_thdn.py grade` at (c), with",
  ("«24»-bit", "summary/bcrf/align-a-c.json", "cmp_bits(('bcrf', 'baaf'))", "d"))
A("| The same, new: the tone pair at -60 dBFS on a one-LSB floor |",
  ("«one»-LSB", "tools/tone_points_b16.py", "rx('tools/tone_points_b16.py', r'the tone pair at -60 dBFS on the \\+-(\\d+) LSB floor')", "w"))
A("below one frame in 14.58 million, 0.07 ppm. At (c) 0.0000 ppm |",
  ("below «one» frame", "controls/b16b-dloop-control.json", "step_frames()", "w"))
A("must end within 10 minutes. The capture command ran 24.0 s after the last",
  ("10", "HANDOFF.md", "lock_limit()", "d"))

# ---------------- round 4: quoted number words of the rewordings, found on the page before them
WHOLE = {r"\b(one) route"}  # read in the whole page: it stood in the Contents entry, outside the section was() reads
QW = [  # (anchor, shown, regex with the word as group 1, the commit the phrase stood at)
    ('Six number words with no receipt were reworded: "plus one change", "one PDU",', '"plus «one» change"', r"plus (one) change", "35e332b6"),
    ('Six number words with no receipt were reworded: "plus one change", "one PDU",', '"«one» PDU"', r"\b(one) PDU", "35e332b6"),
    ('"one step earlier", "one request", "the two lanes" and "one route".', '"«one» step earlier"', r"\b(one) step earlier", "35e332b6"),
    ('"one step earlier", "one request", "the two lanes" and "one route".', '"«one» request"', r"\b(one) request", "35e332b6"),
    ('"one step earlier", "one request", "the two lanes" and "one route".', '"the «two» lanes"', r"the (two) lanes", "35e332b6"),
    ('"one step earlier", "one request", "the two lanes" and "one route".', '"«one» route"', r"\b(one) route", "35e332b6"),
    ("| R624-2-R2: the five `SLIP_LB` steps before the set |", "do not separate the «two» |", r"the receipts do not separate the (two)\.", "0782c55f"),
    ('and which state no figure, were reworded: "records each one",', '"records each «one»"', r"records each (one)\.", "0782c55f"),
    ('"the published one", "failed at once", "once the controller agent",', '"the published «one»"', r"the published (one) in both", "0782c55f"),
    ('"the published one", "failed at once", "once the controller agent",', '"failed at «once»"', r"failed at (once) with", "0782c55f"),
    ('"the published one", "failed at once", "once the controller agent",', '"«once» the controller agent"', r"\b(once) the controller agent", "0782c55f"),
    ('"these two cases", "the two cases run", "on one clock", "one state of it",', '"these «two» cases"', r"for these (two) cases", "0782c55f"),
    ('"these two cases", "the two cases run", "on one clock", "one state of it",', '"the «two» cases run"', r"the (two) cases run in the loop", "0782c55f"),
    ('"these two cases", "the two cases run", "on one clock", "one state of it",', '"on «one» clock"', r"run on (one) clock", "0782c55f"),
    ('"these two cases", "the two cases run", "on one clock", "one state of it",', '"«one» state of it"', r"graded (one) state of it", "0782c55f"),
    ('"two modes added", "the two clocks\' difference", "do not separate the two.",', '"«two» modes added"', r"with (two) modes added", "0782c55f"),
    ('"two modes added", "the two clocks\' difference", "do not separate the two.",', '"the «two» clocks\' difference"', r"the (two) clocks' difference", "0782c55f"),
    ('"two modes added", "the two clocks\' difference", "do not separate the two.",', '"do not separate the «two».', r"do not separate the (two)\.", "0782c55f"),
    ('"Two reviews of this section", "Two reviews of round 2",', '"«Two» reviews of this section"', r"(Two) reviews of this section", "0782c55f"),
    ('"Two reviews of this section", "Two reviews of round 2",', '"«Two» reviews of round 2"', r"(Two) reviews of round 2", "0782c55f"),
    ('"one row per quoted figure", "one line per row", "on one reference peer" and', '"«one» row per quoted figure"', r"holds (one) row per quoted figure", "0782c55f"),
    ('"one row per quoted figure", "one line per row", "on one reference peer" and', '"«one» line per row"', r"(one) line per row", "0782c55f"),
    ('"one row per quoted figure", "one line per row", "on one reference peer" and', '"on «one» reference peer"', r"each about a minute, on (one) reference peer", "0782c55f"),
    ('"on one DUT and one reference peer". The date after each ruling\'s link was', '"on «one» DUT', r"runs on (one) DUT and one reference peer", "0782c55f"),
    ('"on one DUT and one reference peer". The date after each ruling\'s link was', 'DUT and «one» reference peer"', r"runs on one DUT and (one) reference peer", "0782c55f"),
]
PAGE_AT = lambda at: f"load('git:{at}:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md')"
for i, (anchor, shown, pat, at) in enumerate(QW):
    key = f"was({pat!r}, 1, at={at!r})" if pat not in WHOLE else f"re.search({pat!r}, {PAGE_AT(at)}).group(1)"
    A(anchor, (shown, "", key, "s"), c="round 4: quoted number words, each found before its rewording" if i == 0 else None)
REW4 = ("records each one", "the published one", "failed at once", "once the controller agent", "these two cases",
        "the two cases run", "on one clock", "one state of it", "two modes added", "the two clocks' difference",
        "do not separate the two.", "Two reviews of this section", "Two reviews of round 2", "one row per quoted figure",
        "one line per row", "on one reference peer", "on one DUT and one reference peer")
A("**Rewording.** Seventeen phrases whose number words only a category covered,",
  ("Seventeen", "", f"sum(1 for x in {REW4!r} if x in was('(.*)', 1, at='0782c55f') and x not in {NEWTXT})", "W"))

# ---------------- round 4: where the packet is (R624-3-F1)
EV = "r4/evidence-receipt.json"
A("pinned at commit `b84584e4ccb069248909f0fdeb7f8b72a1c41ae4`. There the packet",
  ("b84584e4ccb069248909f0fdeb7f8b72a1c41ae4", EV, "d['evidence_commit']", "s"), c="round 4: where the packet is")
A("`e20fd282`; `author-r2/` for round 2, at `35e332b6`; and `author-r3/` for",
  ("e20fd282", EV, "d['archives']['author-r1']['page_commit']", "s"),
  ("35e332b6", EV, "d['archives']['author-r2']['page_commit']", "s"))
A("round 3, at `0782c55f`. So `runs/loop2/events.jsonl` is",
  ("0782c55f", EV, "d['archives']['author-r3']['page_commit']", "s"))
A("`review-evidence/629-b16-r1/MANIFEST.json` at `b84584e4` has 1,680 entries",
  ("b84584e4", EV, "d['evidence_commit'][:8]", "s"),
  ("1,680", EV, "d['manifest_entries']", ",d"))
A("and SHA-256: `8d417d54b13a264484bfcb0b69f8a643e5cd3bf2819294cea201242a2f67f034`.",
  ("8d417d54b13a264484bfcb0b69f8a643e5cd3bf2819294cea201242a2f67f034", EV, "d['manifest_sha256']", "s"))
A("paths in 27 author files, 1 in `author-r1/`, 9 in `author-r2/` and 17 in",
  ("27", EV, "d['path_redacted_author'] if d['hashes_differ_exactly_when_redacted'] else None", "d"),
  ("1", EV, "d['path_redacted_per_dir']['author-r1']", "d"),
  ("9", EV, "d['path_redacted_per_dir']['author-r2']", "d"),
  ("17", EV, "d['path_redacted_per_dir']['author-r3']", "d"))
A("No hash row in lane B16's section names any of them. Each of the 66",
  ("66", EV, "d['page_rows']['rows'] if d['page_rows']['rows'] == d['page_rows']['in_manifest'] == d['page_rows']['all_equal'] and d['page_rows']['path_redacted'] == 0 else None", "d"))
A("packet-file rows in its tables at `0782c55f`, here, in",
  ("0782c55f", EV, "d['page_commit'][:8]", "s"))

# ---------------- B16, round 4: packet and coverage
CRALL = lambda i: ("same([" + ", ".join(CR(a, b, c, i) for a, b, c in (
    ("census-start", "census-end", "census-compare"), ("census-end", "census-startb", "census-compare-b16-to-b16b"),
    ("census-startb", "census-endb", "census-compare-b16b"), ("census-endb", "census-startc", "census-compare-b16b-to-b16c"),
    ("census-startc", "census-endc", "census-compare-b16c"))) + "])")
A("| R625-3-S1, taken: the census | 45 of 46 entries equal |",
  ("45", "", "was(r'census (\\d+) of (\\d+) entries equal', 1, at='0782c55f')", "s"),
  ("46", "", "was(r'census (\\d+) of (\\d+) entries equal', 2, at='0782c55f')", "s"),
  ("44", "", CRALL(0), "d"),
  ("«45» reads", "", CRALL(1), "d"),
  c="B16, round 4: packet and coverage")
A("altered copy (`controls/r4-controls.json`, 8 of 8 PASS). The first five are",
  ("«8» of 8", "controls/r4-controls.json", "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
  ("8 of «8»", "controls/r4-controls.json", "len(d['controls'])", "d"),
  ("first «five»", "controls/r4-controls.json", "sum(1 for c in d['controls'] if c.get('from') == 'round 3')", "w"))
A("new check, passes 5 of 5 too (`controls/r4-rerun-r3-controls.json`).",
  ("«5» of 5", "controls/r4-rerun-r3-controls.json", "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
  ("5 of «5»", "controls/r4-rerun-r3-controls.json", "len(d['controls'])", "d"))
A("| `controls/r4-controls.json` (8 of 8 PASS) |",
  ("«8» of 8", "controls/r4-controls.json", "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
  ("8 of «8»", "controls/r4-controls.json", "len(d['controls'])", "d"))
A("| `controls/r4-rerun-r3-controls.json` (5 of 5 PASS) |",
  ("«5» of 5", "controls/r4-rerun-r3-controls.json", "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
  ("5 of «5»", "controls/r4-rerun-r3-controls.json", "len(d['controls'])", "d"))

# ---------------- B16, round 5: every digit
A("altered copy (`controls/r5-controls.json`, 22 of 22 PASS). Round 3's and",
  ("«22» of 22", "controls/r5-controls.json", "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
  ("22 of «22»", "controls/r5-controls.json", "len(d['controls'])", "d"), c="B16, round 5: every digit")
A("too: 5 of 5 and 8 of 8 (`controls/r5-rerun-r3-controls.json`,",
  ("«5» of 5", "controls/r5-rerun-r3-controls.json", "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
  ("5 of «5»", "controls/r5-rerun-r3-controls.json", "len(d['controls'])", "d"),
  ("«8» of 8", "controls/r5-rerun-r4-controls.json", "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
  ("8 of «8»", "controls/r5-rerun-r4-controls.json", "len(d['controls'])", "d"))
A("| `controls/r5-controls.json` (22 of 22 PASS) |",
  ("«22» of 22", "controls/r5-controls.json", "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
  ("22 of «22»", "controls/r5-controls.json", "len(d['controls'])", "d"))
A("| `controls/r5-rerun-r3-controls.json` (5 of 5 PASS) |",
  ("«5» of 5", "controls/r5-rerun-r3-controls.json", "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
  ("5 of «5»", "controls/r5-rerun-r3-controls.json", "len(d['controls'])", "d"))
A("| `controls/r5-rerun-r4-controls.json` (8 of 8 PASS) |",
  ("«8» of 8", "controls/r5-rerun-r4-controls.json", "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
  ("8 of «8»", "controls/r5-rerun-r4-controls.json", "len(d['controls'])", "d"))

# ---------------- round 6: where the packet is (R624-5-F3), read from the evidence branch at a73ce5c4
EV6 = "r6/evidence-receipt.json"
A("packet is in `author-r4/`, archived with this page at `61ae8641` and published by commit `b83e5d76`;",
  ("61ae8641", EV6, "d['archives']['author-r4']['page_commit']", "s"),
  ("b83e5d76", EV6, "d['archives']['author-r4']['commit'][:8]", "s"),
  ("36190193", EV6, "d['archives']['author-r5']['page_commit']", "s"),
  ("a73ce5c4", EV6, "same([d['archives']['author-r5']['commit'][:8], d['evidence_commit'][:8]])", "s"),
  c="round 6: where the packet is")

# ---------------- B16, round 6: the closed list
R6 = "controls/r6-controls.json"
A("altered copy (`controls/r6-controls.json`, 39 of 39 PASS). Round 5's 22 come",
  ("«39» of 39", R6, "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
  ("39 of «39»", R6, "len(d['controls'])", "d"),
  ("Round 5's «22» come", R6, "sum(1 for c in d['controls'] if c.get('from') in ('round 3', 'round 4', 'round 5'))", "d"),
  c="B16, round 6: the closed list")
A("against the new check: 5 of 5, 8 of 8 and 22 of 22",
  ("«5» of 5", "controls/r6-rerun-r3-controls.json", "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
  ("5 of «5»", "controls/r6-rerun-r3-controls.json", "len(d['controls'])", "d"),
  ("«8» of 8", "controls/r6-rerun-r4-controls.json", "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
  ("8 of «8»", "controls/r6-rerun-r4-controls.json", "len(d['controls'])", "d"),
  ("«22» of 22", "controls/r6-rerun-r5-controls.json", "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
  ("22 of «22»", "controls/r6-rerun-r5-controls.json", "len(d['controls'])", "d"))
for f_, n_ in (("r6-controls", 39), ("r6-rerun-r3-controls", 5), ("r6-rerun-r4-controls", 8), ("r6-rerun-r5-controls", 22)):
    A(f"| `controls/{f_}.json` ({n_} of {n_} PASS) |",
      (f"«{n_}» of {n_}", f"controls/{f_}.json", "sum(c['verdict'] == 'PASS' for c in d['controls'])", "d"),
      (f"{n_} of «{n_}»", f"controls/{f_}.json", "len(d['controls'])", "d"))


def GEN3(covered, tok):
    """Round 4: the tone frequencies, one row per 997, 9,973 or 997/9,973 followed by ' Hz' on any covered
    line, read from the tone tool and the analyser (tone_hz)."""
    keys = {"997": ("tone_hz(0)", ",d"), "9,973": ("tone_hz(1)", ",d"),
            "997/9,973": ("f'{tone_hz(0):,}/{tone_hz(1):,}'", "s")}
    out = []
    for where, text, at in covered:
        toks = [m for m in tok.finditer(text) if m.start() >= at]
        rows = []
        for j, m in enumerate(toks):
            t = m.group(0)
            if t in keys and re.match(r" Hz\b", text[m.end():]):
                k = sum(1 for x in toks[:j] if x.group(0) == t)
                rows.append((t, "tools/b6_tone.py", keys[t][0], keys[t][1], k))
        if rows:
            out.append((where, rows))
    return out
