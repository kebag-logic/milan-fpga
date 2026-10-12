#!/usr/bin/env python3
"""Lane B16, round 3: every quoted figure of lane B16's findings, recomputed from its receipt.

usage: check_b16_figures.py <findings.md> <packet root> <out rows.tsv> <out coverage.tsv> [--repo <root>]
                            [--show <n>]

The text covered: the section "Dev 5603c353, 2026-10-12: lane B16" of
docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md, the page's introduction on lane B16 and its Contents
entry, and the lane B16 part of the page's row in docs/findings/README.md (beside <findings.md>).

ROWS_TSV holds one row per quoted figure in that text: the document line, the figure as shown, the
receipt, the displayed precision and the key into the receipt. A receipt is a file in the lane packet,
`repo:<path>` a file in the repository, or `git:<commit>:<path>` the page as it stood at an earlier
commit, for a figure a round superseded. For each row the check finds the figure on its line, recomputes
the value from the receipt and the key, rounds it to the displayed precision and compares the two.
Receipts are read as exact decimals (JSON numbers are parsed as Decimal) and rounded half up, so pts3's
SNR at (a), stored as 122.475, shows as 122.48. Clock times are CEST, the bench's local time, shown as a
clock shows them: cut to the last digit shown, so 06:22:34.993 shows as 06:22:34.

Coverage: every numeric token of that text (numbers, times, dates, hex words, hashes and the number words
one to twenty, once and twice) must be claimed by a row or by one of the named identifier categories in
EXCLUDE: descriptor and channel indices, ordinals, tone names, commit names, citations, links, units and
the like, none of them a measured or counted value. A token that is neither fails the check, so a figure
added without a row fails it too.

The repository root defaults to the one holding <findings.md>; --repo lets a control check an altered
copy of the page against the real repository. --show caps the failures printed (default 40).

Exit status 0 when every row matches and every token is covered; 1 otherwise. The two outputs are the
receipt: one line per row, in ROWS_TSV's order, with its recomputed value and status; and one line per
token that a category covers. Nothing here reads a private file or a raw capture.
"""
import datetime
import hashlib
import json
import re
import statistics
import subprocess
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

DOC_P, ROOT, OUT_ROWS, OUT_COV = (Path(a) for a in sys.argv[1:5])
OPTS = dict(zip(sys.argv[5::2], sys.argv[6::2]))
README_P = DOC_P.parent / "README.md"
REPO = Path(OPTS["--repo"]) if "--repo" in OPTS else DOC_P.resolve().parents[2]
SECTION = "## Dev 5603c353, 2026-10-12: lane B16"
CEST = datetime.timezone(datetime.timedelta(hours=2))
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
         "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]

RUNS = ["loop1", "loop2", "pts1", "pts2", "b0", "b0-2", "pts3", "bcrf", "baaf"]

# ---------------------------------------------------------------- receipts
_cache = {}
_read = []


def load(path):
    """A packet file (or repo:<path>): JSON as Decimal, JSONL as a list, anything else as text."""
    if path not in _read:
        _read.append(path)
    if path in _cache:
        return _cache[path]
    if re.fullmatch(r"git:[0-9a-f]+", path):
        return None
    if path.startswith("git:"):
        _, commit, rel = path.split(":", 2)
        raw = subprocess.run(["git", "-C", str(REPO), "show", f"{commit}:{rel}"], check=True, capture_output=True).stdout
        _cache[path] = " ".join(raw.decode().split())
        return _cache[path]
    p = REPO / path[5:] if path.startswith("repo:") else ROOT / path
    raw = p.read_bytes()
    if p.suffix == ".json":
        v = json.loads(raw, parse_float=Decimal)
    elif p.suffix == ".jsonl" or path.endswith("identity-verdict.txt"):
        v = [json.loads(x, parse_float=Decimal) for x in raw.decode().splitlines() if x.strip().startswith("{")]
    elif p.suffix == ".tsv":
        lines = raw.decode().splitlines()
        head = lines[0].split("\t")
        v = [dict(zip(head, x.split("\t"))) for x in lines[1:]]
    else:
        v = raw.decode(errors="replace")
    _cache[path] = v
    return v


def raw(path):
    """A raw file's entry in RAW-ARTIFACTS.json (the raw files stay outside the packet)."""
    return next(x for x in load("RAW-ARTIFACTS.json")["files"] if x["path"] == path)


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def size(path):
    return (ROOT / path).stat().st_size


def get(obj, dotted):
    """Walk a dotted key: names, list indices, or k=v selecting the first list element with that field."""
    for part in dotted.split("."):
        if isinstance(obj, list):
            if "=" in part:
                k, v = part.split("=", 1)
                obj = next(x for x in obj if str(x.get(k)) == v)
            else:
                obj = obj[int(part)]
        else:
            obj = obj[part]
    return obj


def ev(run, kind=None, **kw):
    """The run's events of a kind, optionally matching fields."""
    out = [e for e in load(f"runs/{run}/events.jsonl") if kind is None or e.get("kind") == kind]
    return [e for e in out if all(str(e.get(k)) == str(v) for k, v in kw.items())]


def E(run, kind, i=0, **kw):
    return ev(run, kind, **kw)[i]


def utc(s):
    """An ISO UTC stamp (2026-10-12T03:56:30.663Z) to epoch seconds."""
    d = datetime.datetime.strptime(s.rstrip("Z"), "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=datetime.timezone.utc)
    return Decimal(str(d.timestamp()))


def stamps(path, tag):
    """Every ISO stamp following `tag ` (as a whole word) in a text receipt, in order."""
    return [utc(m) for m in re.findall(rf"(?<![A-Z_]){tag} (\d{{4}}-\d\d-\d\dT[\d:.]+Z)", load(path))]


FIND_P = "repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"


def clock(hms):
    """A CEST clock reading HH:MM:SS on the lane's day to epoch seconds."""
    d = datetime.datetime.strptime("2026-10-12 " + hms, "%Y-%m-%d %H:%M:%S").replace(tzinfo=CEST)
    return int(d.timestamp())


PFILE_ = ("a", "b", "c")


def b6_rule():
    """Lane B6's pass rule for B CRF, from its Method section of the findings page."""
    m = re.search(r"^- B CRF passes when (.*?)\.\n", load(FIND_P), re.M | re.S)
    return " ".join(m.group(1).split())


def commit_time(commit):
    """A commit's committer time, epoch seconds (the date a documents-only round was recorded)."""
    out = subprocess.run(["git", "-C", str(REPO), "show", "-s", "--format=%ct", commit], check=True, capture_output=True)
    return Decimal(out.stdout.decode().strip())


def was(pattern, group=1, at="e20fd282"):
    """A figure lane B16's section showed at an earlier commit (lines joined, whitespace collapsed): e20fd282,
    before round 2, or 35e332b6, before round 3."""
    text = load(f"git:{at}:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md")
    text = text[text.index(" ".join(SECTION.split())):]
    return re.search(pattern, text).group(group)


def r2lead():
    """The board's playback lead before McASP0 records, in run_b16.py's modes dira and b0 (round 2's receipt)."""
    return load("r2/b0-2-receipt.json")["timing"]["playback_lead_s"]


# Short names for the receipts the rows read most often.
def T(d, ch, field):
    """Channel ch's tone record in a point summary (channel 0 carries 997 Hz, channel 1 9,973 Hz): a median
    field, or `worst` for the worst block's THD+N."""
    t = get(d, f"channels.channel={ch}.tone_{(997, 9973)[ch]}")
    return t if field == "rec" else t["worst_thdn_db"] if field == "worst" else t["median"][field]


def grade(r):
    return load(f"summary/{r}/c-b9-grade.json")


def dec(r):
    return load(f"summary/{r}/d-loop-decode.json")


def align(r, p):
    return load(f"summary/{r}/align-{p}-c.json")


def win(r):
    """The window span of a B16c case's poll receipt."""
    return load(f"r2/{r}-poll-receipt.json")["spans"]["window-start..window-end"]


def terms(r):
    """Lane B6's terms a B16c case meets: LOCKED at every window poll, 0 net steps at (d) (the counted
    ratio), and 0 discontinuities at (c) and (d). The fourth, the timed ratio, has no receipt: not run."""
    return sum([win(r)["servo"] == {"LOCKED": win(r)["polls"]}, dec(r)["net_step_frames"] == 0,
                grade(r)["summary"]["events"] == 0 and len(dec(r)["events"]) == 0])


def meter(reads, role, field):
    """One level over the named source reads' meter rows of a role, both channels, every reading."""
    src = load("r2/source-receipt.json")["reads"]
    return same(v for k in reads for c in (0, 1) for v in (src[k]["meters"][role][c][field] or []))


def cdiff(end, start, role, dt, idx, i):
    """A counter's change between two counters reads."""
    return counters(end, role, dt, idx)[i] - counters(start, role, dt, idx)[i]


def mdiff(r, later, earlier, key, i):
    """A counter's change between two of a B16c case's marks."""
    return E(r, "mark", tag=later)["counters"][key][i] - E(r, "mark", tag=earlier)["counters"][key][i]


def acmp(msg, i=0):
    """The time of the i-th ACMP message of a kind in loop2's decode of the peer's link, seconds."""
    return [x for x in load("summary/loop2/acmp-peer-tap.json")["acmp"] if x["msg"] == msg][i]["t"]


def taps2():
    """The four tone records of pts2's two tap captures of the DUT's talker (positive control)."""
    return [T(load(f"summary/pts2/ctl-dut-talker-{t}-tap.json"), ch, "rec") for t in ("dut", "peer") for ch in (0, 1)]


def steps(r, span):
    """A B16c case's SLIP_LB steps whose later poll lies in a span of its poll receipt."""
    return [x for x in load(f"r2/{r}-poll-receipt.json")["slip_lb_steps"] if x["span"] == span]


def rates():
    """Every window extreme of the followed stream's rate: B-CRF's CRF sink, B-AAF's AAF meter and CRF sink."""
    return win("bcrf")["crf_rate_ppm"] + win("baaf")["aafm_rate_ppm_valid"] + win("baaf")["crf_rate_ppm"]


def b15_changes():
    """Presence-rule constants that differ between lane B15's tone_points_b15.py and tone_points_b16.py."""
    b15, b16 = "tools/tone_points_b15.py", "tools/tone_points_b16.py"
    pairs = [(rx(b15, r"if share > ([\d.]+) and lvl"), rx(b16, r"if share > ([\d.]+) and lvl")),
             (rx(b15, r"\(fr > t - (\d+)\)"), rx(b16, r"\(fr > t - (\d+)\)")),
             (rx(b15, r"and lvl > (-?\d+)"), str(int(Decimal(rx(b16, r"^LEVEL_FLOOR_DBFS = (-?[\d.]+)")))))]
    return sum(1 for a, b in pairs if a != b)


def slipb(path):
    """SLIP_LB dups in a console read."""
    return le32(mem(path, "0x900008d4", 12)) & 0xFFFF


def bound(value, limit):
    """A bound shown as a figure ("within 0.01 dB"): the limit when the receipt's value is within it."""
    return limit if value <= Decimal(limit) else value


def same(values):
    """The one value all of them share; fails when they differ."""
    vals = list(values)
    assert vals and all(v == vals[0] for v in vals), f"not one value: {vals[:6]}"
    return vals[0]


def ctrs(e):
    """The 32 counters of a GET_COUNTERS payload (descriptor type, index, valid flags, then the counters)."""
    b = bytes.fromhex(e["payload"])
    return [int.from_bytes(b[i:i + 4], "big") for i in range(8, len(b), 4)]


def pt(run, point, ch, tone):
    """A point summary's tone record: point a, b or c; channel; tone 997 or 9973."""
    f = {"a": "a-peer-tap", "b": "b-dut-tap", "c": "c-mcasp"}[point]
    return get(load(f"summary/{run}/{f}.json"), f"channels.channel={ch}.tone_{tone}")


def inside(pb):
    """Blocks wholly inside the playback: after its first non-silent block, and before its last when silence
    follows (the tool's -400 dB THD+N sentinel and a level below -200 dBFS mark a silent block)."""
    loud = [i for i, b in enumerate(pb) if b["level_dbfs"] > -200]
    first, last = loud[0], loud[-1]
    end = last if last < len(pb) - 1 else last + 1
    return [i for i in range(first + 1, end)]


def floor_inside(t):
    """Blocks wholly inside the playback that sit within 3 dB of the median over those blocks."""
    pb = t["per_block"]
    ins = inside(pb)
    med = statistics.median(pb[i]["thdn_db"] for i in ins)
    return [i for i in ins if pb[i]["thdn_db"] <= med + 3]


def silent(pb):
    return [i for i, b in enumerate(pb) if b["level_dbfs"] <= -200]


def runs_of(idx):
    """Consecutive runs of block indices, as [first, last] pairs."""
    out = []
    for i in idx:
        if out and i == out[-1][1] + 1:
            out[-1][1] = i
        else:
            out.append([i, i])
    return out


def trace(run):
    return load(f"r2/{run}-poll-trace.tsv")


def trace_state(row):
    return int(row["0x8f8"], 16) & 7


def lock_bracket(run):
    """Start of the last poll that read ACQUIRE before the first LOCKED read, and the end of that LOCKED
    poll: the trace gives each poll's start; the receipt gives the LOCKED poll's end from the raw poll."""
    rec = load(f"r2/{run}-poll-receipt.json")
    k = int(rec["locked"]["first_locked_poll"])
    rows = trace(run)
    assert trace_state(rows[k]) == 4 and trace_state(rows[k - 1]) == 3
    return Decimal(rows[k - 1]["start_after_set_s"]), rec["locked"]["recomputed_s"][1]


def rx(path, pattern, i=0, group=1):
    """The i-th match of a regex in a text receipt, group 1 (or another group)."""
    return list(re.finditer(pattern, load(path), re.M))[i].group(group)


def cen(path, what, role=None):
    """A census entry by its `what` tag (and role, where the tag repeats)."""
    return next(x for x in load(path) if x.get("what") == what and role in (None, x.get("role")))


def payload_word(entry, hexpos, n=4):
    return int(entry["payload"][hexpos:hexpos + n], 16)


def audio_map(entry):
    """GET_AUDIO_MAP: (stream_index, stream_channel, cluster_offset, cluster_channel) per mapping."""
    p = entry["payload"]
    n = int(p[16:20], 16)
    return [tuple(int(p[24 + 16 * j + 4 * f:28 + 16 * j + 4 * f], 16) for f in range(4)) for j in range(n)]


def identity_maps(entry):
    """Mappings whose stream channel equals their cluster offset plus channel."""
    return sum(1 for si, sc, co, cc in audio_map(entry) if sc == co + cc)


def console(path, cmd):
    """The text of one console command's output in a console transcript."""
    blocks = re.split(r"^### .*$", load(path), flags=re.M)
    heads = re.findall(r"^### .*cmd='([^']*)'.*$", load(path), flags=re.M)
    return blocks[1 + heads.index(cmd)]


def mem(path, addr, n):
    """Bytes of a `mem_read <addr> <n>` in a console transcript."""
    line = re.search(rf"^{addr}\s+((?:[0-9a-f]{{2}} )+)", console(path, f"mem_read {addr} {n}"), re.M).group(1)
    return bytes(int(h, 16) for h in line.split())


def le32(b, off=0):
    return int.from_bytes(b[off:off + 4], "little")


def nvm(path):
    t = console(path, "milan_nvm")
    return dict(seq=int(re.search(r"image seq (\d+)", t).group(1)), commits=int(re.search(r"commits ok=(\d+)", t).group(1)),
                pend=int(re.search(r"pend=(\d+)", t).group(1)), verdict=re.search(r"verdict=(\w+)", t).group(1))


def counters(path, role, dtype, idx):
    """GET_COUNTERS values (32 counters, big-endian) from a counters JSONL read."""
    x = next(x for x in load(path) if x.get("cmd") == "GET_COUNTERS" and x.get("role") == role
             and int(x["payload"][:4], 16) == dtype and int(x["payload"][4:8], 16) == idx)
    b = bytes.fromhex(x["payload"])
    return [int.from_bytes(b[i:i + 4], "big") for i in range(8, len(b), 4)]


# ---------------------------------------------------------------- formats
def q(v, n):
    return Decimal(v).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP)


def fmt(v, spec):
    if spec == "s":
        return str(v)
    if spec == "date":
        return datetime.datetime.fromtimestamp(int(Decimal(v) // 1), CEST).strftime("%Y-%m-%d")
    if spec == "x":
        return {1: "once", 2: "twice"}[int(v)]
    if spec == "w":
        return WORDS[int(v)]
    if spec == "W":
        return WORDS[int(v)].capitalize()
    m = re.fullmatch(r"cest(\d?)|hm", spec)
    if m:
        n = int(m.group(1) or 0) if spec != "hm" else 0
        t = Decimal(v)
        if spec == "hm":
            t = t // 60 * 60
        else:
            t = (t * 10 ** n // 1) / Decimal(10 ** n)
        d = datetime.datetime.fromtimestamp(int(t // 1), CEST)
        out = d.strftime("%H:%M" if spec == "hm" else "%H:%M:%S")
        if n:
            out += "." + f"{t % 1:.{n}f}"[2:]
        return out
    m = re.fullmatch(r"([+z]*)(,?)(?:\.(\d+)f|d)", spec)
    assert m, spec
    flags, comma, n = m.group(1), m.group(2), m.group(3)
    if n is None:
        return format(int(v), ("+" if "+" in flags else "") + comma + "d")
    s = format(q(v, int(n)), ("+" if "+" in flags else "") + comma + f".{n}f")
    if "z" in flags and re.fullmatch(r"[-+]0\.?0*", s):
        s = s[1:]
    return s


# ---------------------------------------------------------------- rows
# One row per quoted figure, tab-separated: the document line, the figure as shown, the receipt, the
# displayed precision (with #k when the line repeats the shown text: its k-th occurrence, from 0), and the
# key, a Python expression over the helpers above with `d` bound to the loaded receipt and `p` to its path.
# An empty receipt means the key names its files itself; the output then lists every file the key read.
# Precisions: a format spec (.2f, +.2f, ,d, d; z drops the sign of a zero), s (the text as is), w or W (a
# number word), x (once, twice), date, cest (HH:MM:SS), cest1 (tenths), hm (HH:MM).
ROWS_TSV = r"""
# ROWS-BEGIN
# lane B16: heading and summary
2281	2026-10-12		date	stamps('identity/lock-window.txt', 'LOCK')[0]
2283	2026-10-12		date	stamps('identity/lock-window.txt', 'LOCK')[0]
2309	8	controls/b16-tap-controls.json	d#0	sum(c['result'] == 'PASS' for c in d['controls'])
2309	8	controls/b16-tap-controls.json	d#1	len(d['controls'])
2309	6	controls/b16-align-controls-synth.json	d#0	sum(c['result'] == 'PASS' for c in d['controls'])
2309	6	controls/b16-align-controls-synth.json	d#1	len(d['controls'])
2310	Two	runs/loop1/events.jsonl	W	sum(1 for r in RUNS for b in ev(r, 'bind') if b['talker'] == 'peer-out-0' and b['listener'] == 'peer-in-0')
2311	twice	summary/loop2/acmp-peer-tap.json	x	sum(x['msg'] == 'CONNECT_TX_COMMAND' for x in d['acmp'])
2311	200	summary/loop2/acmp-peer-tap.json	.0f	(lambda p: (p[1]['t'] - p[0]['t']) * 1000)([x for x in d['acmp'] if x['msg'] == 'CONNECT_TX_COMMAND'])
# B16: identity and setup
2326	020000fffe000001	identity/identity-verdict.txt	s	get(d, 'check=atdecc-entity_id.detail.read')
2326	2.96.0	identity/identity-verdict.txt	s	get(d, 'check=atdecc-firmware_version.detail.read')
2327	4d494c4e	identity/identity-verdict.txt	s	get(d, 'check=console-id.detail.read.0')
2327	0x00020060	identity/identity-verdict.txt	s	'0x' + get(d, 'check=console-id.detail.read.1')
2328	7,512		,d	rx('identity/console-identity.txt', r"cmd='crc 0x[0-9a-f]+ (\d+)'")
2328	5ba355eb	identity/identity-verdict.txt	s	get(d, 'check=console-aem-crc.detail.read')
2329	312	identity/identity-verdict.txt	d	get(d, 'check=live-vs-qspi-ENTITY 0.detail.live_bytes')
2329	106	identity/identity-verdict.txt	d	get(d, 'check=live-vs-qspi-CONFIGURATION 0.detail.live_bytes')
2330	0	identity/identity-verdict.txt	s#0	next(k for k, v in get(d, 'check=clock-sources.detail.sources').items() if isinstance(v, dict) and v['type'] == 0)
2330	1	identity/identity-verdict.txt	s#0	next(k for k, v in get(d, 'check=clock-sources.detail.sources').items() if isinstance(v, dict) and v['type'] == 2 and v['location_index'] == 1)
2330	1	identity/identity-verdict.txt	d#1	get(d, 'check=clock-sources.detail.sources')['1']['location_index']
2330	2	identity/identity-verdict.txt	s#0	next(k for k, v in get(d, 'check=clock-sources.detail.sources').items() if isinstance(v, dict) and v['type'] == 2 and v['location_index'] == 0)
2330	0	identity/identity-verdict.txt	d#1	get(d, 'check=clock-sources.detail.sources')['2']['location_index']
2330	3	identity/identity-verdict.txt	s#0	next(k for k, v in get(d, 'check=clock-sources.detail.sources').items() if v == 'NO_SUCH_DESCRIPTOR')
2330	0	identity/identity-verdict.txt	d#3	get(d, 'check=clock-sources.detail.clock_domain_list.0')
2330	1	identity/identity-verdict.txt	d#2	get(d, 'check=clock-sources.detail.clock_domain_list.1')
2330	2	identity/identity-verdict.txt	d#1	get(d, 'check=clock-sources.detail.clock_domain_list.2')
2330	0	identity/identity-verdict.txt	d#4	get(d, 'check=clock-sources.detail.get_clock_source')
2331	10		s#0	rx('identity/grader-identity.txt', r'UART SMOKE: PASS \((\d+)/(\d+)\)')
2331	10		s#1	rx('identity/grader-identity.txt', r'UART SMOKE: PASS \((\d+)/(\d+)\)', group=2)
2332	001bc5c1935893e1	identity/adp-discover.jsonl	s	next(x['model_id'] for x in d if x.get('entity_id') == '020000fffe000001')
2333	05:45:06		cest	stamps('identity/lock-window.txt', 'LOCK')[0]
2333	05:45:12		cest	stamps('identity/lock-window.txt', 'UNLOCK')[0]
2338	05:45		hm	stamps('restore/baseline-start-lock.txt', 'LOCK')[0]
2341	0205022001006000		s	cen('restore/census-start.jsonl', 'format-dut-5-0')['payload'][8:]
2341	four		w	identity_maps(cen('restore/census-start.jsonl', 'map-dut-0x000e-0-0'))
2342	eight		w	identity_maps(cen('restore/census-start.jsonl', 'map-dut-0x000f-0-0'))
2342	0		d#2	payload_word(cen('restore/census-start.jsonl', 'clock', 'dut'), 8)
2343	276		d	nvm('restore/dut-start.txt')['seq']
2343	42		d	nvm('restore/dut-start.txt')['commits']
2343	0		d	nvm('restore/dut-start.txt')['pend']
2343	152		d	le32(mem('restore/dut-start.txt', '0x900008d4', 12)) & 0xffff
2345	0205022002006000		s	cen('restore/census-start.jsonl', 'format-peer-5-0')['payload'][8:]
2347	0205022001006000		s	cen('restore/census-start.jsonl', 'format-peer-6-0')['payload'][8:]
2347	0		d#0	cen('restore/census-start.jsonl', 'tx-state-peer-0')['conn_count']
# B16: method
2357	-20		d	Decimal(rx('tools/b9_tone.py', r'^LEVEL_DBFS = (-?[\d.]+)'))
2357	d9684a8f...		s	rx('runs/tone-start.txt', r'LOOP_SHA256 ([0-9a-f]{8})') + '...'
2358	05:55:37		cest	stamps('runs/tone-start.txt', 'STATUS')[0] - Decimal(rx('runs/tone-start.txt', r'hw_ptr : (\d+)')) / 48000
2358	06:01:59		cest	stamps('runs/tone-stop.txt', 'LOCK')[0]
2359	twice	r2/source-receipt.json	x	sum(1 for k, r in d['reads'].items() if k.startswith('b16-') and r['kind'] == 'state')
2362	one	runs/loop1-lock.txt	w	same(len(stamps(f'runs/{r}-lock.txt', 'LOCK')) for r in ('loop1', 'loop2'))
2367	12	runs/loop1/events.jsonl	d	same(round(max(x['dt'] for x in ev(r, 'listener-poll'))) for r in ('loop1', 'loop2'))
2369	2	runs/loop1/events.jsonl	d	same(round(statistics.median(b['dt'] - a['dt'] for a, b in zip(ev(r, 'listener-poll'), ev(r, 'listener-poll')[1:]) if b['tag'] == a['tag'])) for r in ('loop1', 'loop2'))
2376	05:56:30		cest	stamps('runs/loop1-lock.txt', 'LOCK')[0]
2376	05:57:30		cest	stamps('runs/loop1-lock.txt', 'UNLOCK')[0]
2376	30.6	runs/loop1/events.jsonl	.1f	E('loop1', 'capture-done', what='tap')['seconds']
2376	22	runs/loop1/events.jsonl	.0f	E('loop1', 'capture-done', what='extcap')['seconds']
2376	05:56:45	runs/loop1/events.jsonl	cest	E('loop1', 'captures-started')['started']['extcap']
2377	05:59:18		cest	stamps('runs/loop2-lock.txt', 'LOCK')[0]
2377	06:00:28		cest	stamps('runs/loop2-lock.txt', 'UNLOCK')[0]
2377	52.5	runs/loop2/events.jsonl	.1f	E('loop2', 'capture-done', what='tap')['seconds']
2377	05:59:19	runs/loop2/events.jsonl	cest	E('loop2', 'captures-started')['started']['tap']
2377	16	runs/loop2/events.jsonl	.0f	E('loop2', 'capture-done', what='extcap')['seconds']
2377	05:59:36	runs/loop2/events.jsonl	cest	E('loop2', 'captures-started')['started']['extcap']
2386	0205022001006000	runs/loop1/events.jsonl	s	same(E(r, 'format-check', talker='peer-out-0')['talker_fmt'] for r in ('loop1', 'loop2'))
2386	0205022002006000	runs/loop1/events.jsonl	s	same(E(r, 'format-check', talker='peer-out-0')['listener_fmt'] for r in ('loop1', 'loop2'))
2386	0205022001006000	runs/loop1/events.jsonl	s	same(E(r, 'format-check', talker='peer-out-0')['set']['fmt'] for r in ('loop1', 'loop2'))
2386	0205022001006000	runs/loop1/events.jsonl	s	same(E(r, 'format-check', talker='peer-out-0')['listener_after'] for r in ('loop1', 'loop2'))
2387	0205022002006000	runs/loop1/events.jsonl	s	same(E(r, 'format-check', listener='peer-in-0', set=None, talker='020000fffe000001-out-0')['talker_fmt'] for r in ('loop1', 'loop2'))
2387	0205022002006000	runs/loop1/events.jsonl	s	same(E(r, 'format-check', listener='peer-in-0', set=None, talker='020000fffe000001-out-0')['listener_fmt'] for r in ('loop1', 'loop2'))
2394	5		s	rx('tools/tone_points_b16.py', r'\(fr > t - (\d+)\)')
2394	0.9		s	rx('tools/tone_points_b16.py', r'if share > ([\d.]+) and lvl >= LEVEL_FLOOR_DBFS')
2394	one	tools/tone_points_b16.py	w	b15_changes()
2395	-100		d	Decimal(rx('tools/tone_points_b16.py', r'^LEVEL_FLOOR_DBFS = (-?[\d.]+)'))
2395	-40		s	rx('tools/tone_points_b15.py', r'and lvl > (-?\d+)')
2396	-38.5	r2/source-receipt.json	.1f	get(d, 'reads.b16-meters-1.meters.the documented pair of outputs.0.leaving_dbfs.0')
2396	-40		s	rx('tools/tone_points_b16.py', r'if lvl < (-?\d+):')
2397	-100		d	Decimal(rx('tools/tone_points_b16.py', r'^LEVEL_FLOOR_DBFS = (-?[\d.]+)'))
2397	-40		s	rx('tools/tone_points_b16.py', r'if lvl < (-?\d+):')
# B16: the loopback
2403	2	runs/loop1/events.jsonl	d	same(round(statistics.median(b['dt'] - a['dt'] for a, b in zip(ev(r, 'listener-poll'), ev(r, 'listener-poll')[1:]) if b['tag'] == a['tag'])) for r in ('loop1', 'loop2'))
2407	14	runs/loop1/events.jsonl	d	len(ev('loop1', 'listener-poll'))
2407	12	runs/loop1/events.jsonl	d	round(max(x['dt'] for x in ev('loop1', 'listener-poll', tag='after-loop-bind')))
2407	12	runs/loop1/events.jsonl	d	round(max(x['dt'] for x in ev('loop1', 'listener-poll', tag='after-captures')))
2407	0000000000000000	runs/loop1/events.jsonl	s	same(x['rx']['stream_id'] for x in ev('loop1', 'listener-poll'))
2407	000000000000	runs/loop1/events.jsonl	s	same(x['rx']['dmac'] for x in ev('loop1', 'listener-poll'))
2407	0x0002	runs/loop1/events.jsonl	s	same(x['rx']['flags'] for x in ev('loop1', 'listener-poll'))
2407	0	runs/loop1/events.jsonl	d#0	same(x['peer_tx0']['conn_count'] for x in ev('loop1', 'listener-poll'))
2407	0	runs/loop1/events.jsonl	d#1	same([x['media_locked'] for x in ev('loop1', 'listener-poll')] + [ctrs(c)[0] for c in ev('loop1', 'counters', who='peer')])
2407	0	runs/loop1/events.jsonl	d#2	same([x['frames_rx'] for x in ev('loop1', 'listener-poll')] + [ctrs(c)[11] for c in ev('loop1', 'counters', who='peer')])
2408	14	runs/loop2/events.jsonl	d	len(ev('loop2', 'listener-poll'))
2410	1	runs/loop1/events.jsonl	d	same(E(r, 'bind', talker='peer-out-0')['conn_count'] for r in ('loop1', 'loop2'))
2412	0	runs/loop1/events.jsonl	d	same(x['peer_tx0']['conn_count'] for x in [x for r in ('loop1', 'loop2') for x in ev(r, 'listener-poll')])
2419	0.0	summary/loop2/acmp-peer-tap.json	.1f	(acmp('DISCONNECT_RX_COMMAND') - acmp('DISCONNECT_RX_COMMAND')) * 1000
2420	0.0	summary/loop2/acmp-peer-tap.json	.1f	(acmp('DISCONNECT_RX_RESPONSE') - acmp('DISCONNECT_RX_COMMAND')) * 1000
2420	0	summary/loop2/acmp-peer-tap.json	d#0	get(d, 'acmp.msg=DISCONNECT_RX_RESPONSE')['conn_count']
2421	0.1	summary/loop2/acmp-peer-tap.json	.1f	(acmp('CONNECT_RX_COMMAND') - acmp('DISCONNECT_RX_COMMAND')) * 1000
2422	99.6	summary/loop2/acmp-peer-tap.json	.1f	(acmp('CONNECT_RX_RESPONSE') - acmp('DISCONNECT_RX_COMMAND')) * 1000
2422	1	summary/loop2/acmp-peer-tap.json	d#0	get(d, 'acmp.msg=CONNECT_RX_RESPONSE')['conn_count']
2422	0	summary/loop2/acmp-peer-tap.json	d#0	int(get(d, 'acmp.msg=CONNECT_RX_RESPONSE')['stream_id'], 16)
2423	99.6	summary/loop2/acmp-peer-tap.json	.1f	(acmp('CONNECT_TX_COMMAND') - acmp('DISCONNECT_RX_COMMAND')) * 1000
2424	299.6	summary/loop2/acmp-peer-tap.json	.1f	(acmp('CONNECT_TX_COMMAND', 1) - acmp('DISCONNECT_RX_COMMAND')) * 1000
2427	49.6	summary/loop2/acmp-peer-tap.json	.1f	E('loop2', 'capture-done', what='tap')['seconds'] - acmp('CONNECT_TX_COMMAND', 1)
# B16: the four points of the loopback
2439	0	summary/loop1/a-peer-tap.json	d	d['info']['pdus']
2440	0	summary/loop1/b-dut-tap.json	d	d['info']['pdus']
2441	two	summary/loop1/d-extcap-pair.json	w	sum(1 for r in d['rows'] if r['nonzero'] == 0)
2441	1,056,000	summary/loop1/d-extcap-pair.json	,d	same(r['frames'] for r in d['rows'])
2442	0	summary/loop2/a-peer-tap.json	d	d['info']['pdus']
2443	0	summary/loop2/b-dut-tap.json	d	d['info']['pdus']
2444	two	summary/loop2/d-extcap-pair.json	w	sum(1 for r in d['rows'] if r['nonzero'] == 0)
2444	768,000	summary/loop2/d-extcap-pair.json	,d	same(r['frames'] for r in d['rows'])
2450	0	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	rx(FIND_P, r'nothing\. Its counters stayed (\d+) and its digital output read exact zero')
# B16: the tone source, read only
2465	05:47	r2/source-receipt.json	hm	Decimal(clock(get(d, 'reads.b16-state-1.at')))
2465	06:01	r2/source-receipt.json	hm	Decimal(clock(get(d, 'reads.b16-state-2.at')))
2476	-20.0	r2/source-receipt.json	.1f	meter(('b16-meters-1', 'b16-meters-2', 'b16-state-2'), 'the documented pair of outputs', 'before_setting_dbfs')
2476	-18.5	r2/source-receipt.json	.1f	same(v for k in ('b16-state-1', 'b16-state-2') for v in get(d, 'reads.' + k + '.level_settings_db.the documented pair of outputs'))
2476	-38.5	r2/source-receipt.json	.1f	meter(('b16-meters-1', 'b16-meters-2', 'b16-state-2'), 'the documented pair of outputs', 'leaving_dbfs')
2477	-20.0	r2/source-receipt.json	.1f	meter(('b16-meters-1', 'b16-meters-2', 'b16-state-2'), 'the second pair of outputs', 'before_setting_dbfs')
2477	+6.0	r2/source-receipt.json	+.1f	same(v for k in ('b16-state-1', 'b16-state-2') for v in get(d, 'reads.' + k + '.level_settings_db.the second pair of outputs'))
2477	-14.0	r2/source-receipt.json	.1f	meter(('b16-meters-1', 'b16-meters-2', 'b16-state-2'), 'the second pair of outputs', 'leaving_dbfs')
2478	-135.2	r2/source-receipt.json	.1f	max(get(d, 'reads.' + k + '.meters.every other output.largest_before_setting_dbfs') for k in ('b16-state-1', 'b16-meters-1', 'b16-meters-2', 'b16-state-2'))
2478	-147.6	r2/source-receipt.json	.1f	max(get(d, 'reads.' + k + '.meters.every other output.largest_leaving_dbfs') for k in ('b16-state-1', 'b16-meters-1', 'b16-meters-2', 'b16-state-2'))
2480	-20.0	r2/source-receipt.json	.1f	meter(('b16-meters-1', 'b16-meters-2', 'b16-state-2'), "the tone's playback channels", 'leaving_dbfs')
2480	0	r2/source-receipt.json	.0f	meter(('b16-meters-1', 'b16-meters-2', 'b16-state-2'), 'the documented pair of outputs', 'before_setting_dbfs') - meter(('b16-meters-1', 'b16-meters-2', 'b16-state-2'), "the tone's playback channels", 'leaving_dbfs')
2486	two	r2/source-receipt.json	w	sum(1 for k, r in d['reads'].items() if k.startswith('b16-') and r['kind'] == 'state')
2486	2,262	r2/source-receipt.json	,d	same(get(d, 'compare.0.entries') + [get(d, 'compare.0.both')])
2491	two	r2/source-receipt.json	w	len(get(d, 'reads.b16-meters-1.meters.the documented pair of outputs'))
2492	-38.5	r2/source-receipt.json	.1f	meter(('b16-meters-1', 'b16-meters-2', 'b16-state-2'), 'the documented pair of outputs', 'leaving_dbfs')
# B16: the controls
2501	7bbefc71...		s	sha('controls/controls.json')[:8] + '...'
2502	728a4f0e...		s	sha('controls/b9-controls.json')[:8] + '...'
2503	five	controls/b16-tap-controls.json	w	sum(1 for c in d['controls'] if 'lane B16' not in c['control'])
2503	5	controls/b16-tap-controls.json	d#0	sum(1 for c in d['controls'] if 'lane B16' not in c['control'] and c['result'] == 'PASS')
2503	5	controls/b16-tap-controls.json	d#1	sum(1 for c in d['controls'] if 'lane B16' not in c['control'])
2504	-60	controls/b16-tap-controls.json	d	same(get(d, 'controls.control=tone pair at -60 dBFS on the floor (lane B16)')['levels'])
2504	-60.00	controls/b16-tap-controls.json	.2f	same(get(d, 'controls.control=tone pair at -60 dBFS on the floor (lane B16)')['levels'])
2505	-130	controls/b16-tap-controls.json	d	get(d, 'controls.control=-130 dBFS tone alone (lane B16)')['level']
2505	1.0	controls/b16-tap-controls.json	.1f	same(get(d, 'controls.control=-130 dBFS tone alone (lane B16)')['share'])
2506	eight		w	rx('tools/tone_points_b16.py', r'synth_pcap\(p, sid, (\d+), 2 \* FS, \(5, 6\)\)')
2506	5	controls/b16-tap-controls.json	d	get(d, 'controls.control=eight channels, tone on 5/6 (lane B16)')['tone_channels']['997'][0]
2506	6	controls/b16-tap-controls.json	d	get(d, 'controls.control=eight channels, tone on 5/6 (lane B16)')['tone_channels']['9973'][0]
2507	five	controls/b16-align-controls-synth.json	w	sum(1 for c in d['controls'] if 'lane B16' not in c['control'])
2507	5	controls/b16-align-controls-synth.json	d#0	sum(1 for c in d['controls'] if 'lane B16' not in c['control'] and c['result'] == 'PASS')
2507	5	controls/b16-align-controls-synth.json	d#1	sum(1 for c in d['controls'] if 'lane B16' not in c['control'])
2508	one	controls/b16-align-controls-synth.json	w	re.search(r'^(\w+) sample changed by \+256', d['controls'][5]['control']).group(1) == 'one' and 1
2508	+256	controls/b16-align-controls-synth.json	s	re.search(r'by (\+\d+) LSB', d['controls'][5]['control']).group(1)
2508	One	controls/b16-align-controls-synth.json	W	d['controls'][5]['frames_differing']
# B16: bench as left
2521	0205022001006000		s	cen('restore/census-end.jsonl', 'format-dut-5-0')['payload'][8:]
2521	0		d#1	payload_word(cen('restore/census-end.jsonl', 'clock', 'dut'), 8)
2522	0205022002006000		s	cen('restore/census-end.jsonl', 'format-peer-5-0')['payload'][8:]
2523	45		s	rx('restore/census-compare.txt', r'"same": (\d+)')
2523	46		s	rx('restore/census-compare.txt', r'"compared": (\d+)')
2523	387		d	int(rx('restore/census-compare.txt', r'<gm-id>([0-9a-f]{8})', 0), 16)
2523	377		d	int(rx('restore/census-compare.txt', r'<gm-id>([0-9a-f]{8})', 1), 16)
2524	276		d	nvm('restore/dut-end.txt')['seq']
2524	42		d	nvm('restore/dut-end.txt')['commits']
2524	0		d	nvm('restore/dut-end.txt')['pend']
2525	06:01:59		cest	stamps('runs/tone-stop.txt', 'LOCK')[0]
2533	two		w	same(counters('restore/counters-end.jsonl', 'dut', 6, 0)[i] - counters('restore/counters-start.jsonl', 'dut', 6, 0)[i] for i in (0, 1))
2533	one		w	same(counters('restore/counters-end.jsonl', 'dut', 6, 0)[i] - counters('restore/counters-start.jsonl', 'dut', 6, 0)[i] for i in (0, 1)) // sum(1 for r in RUNS for b in ev(r, 'bind') if b['listener'] == 'peer-in-0')
2537	152		d	same(le32(mem(f, '0x900008d4', 12)) & 0xffff for f in ('restore/dut-start.txt', 'restore/dut-end.txt'))
# B16: limits
2554	Two	runs/loop1/events.jsonl	W	sum(1 for r in RUNS for b in ev(r, 'bind') if b['talker'] == 'peer-out-0' and b['listener'] == 'peer-in-0')
# B16b: the resume
2607	06:22:23		cest	stamps('soc/b16b-precheck-status.log', 'LOCK')[0]
2611	06:22:29		cest	stamps('identity-b16b/lock-window.txt', 'LOCK')[0]
2611	06:22:34		cest	stamps('identity-b16b/lock-window.txt', 'UNLOCK')[0]
2611	45		s	rx('restore/census-compare-b16-to-b16b.txt', r'"same": (\d+)')
2611	46		s	rx('restore/census-compare-b16-to-b16b.txt', r'"compared": (\d+)')
2612	-14.14	summary/pts1/a-peer-tap.json	.2f	same(T(load(f'summary/{r}/a-peer-tap.json'), 0, 'level_dbfs') for r in ('pts1', 'pts2'))
2612	06:28:50	summary/pts2/a-peer-tap.json	cest	d['info']['last_t']
2612	-14.10	summary/b0/a-peer-tap.json	.2f	same(T(load(f'summary/{r}/a-peer-tap.json'), 0, 'level_dbfs') for r in ('b0', 'b0-2', 'pts3'))
2612	06:31:51	summary/b0/a-peer-tap.json	cest	d['info']['first_t']
2613	0	summary/pts1/a-peer-tap.json	d	same(load(f'summary/{r}/{p}.json')['info']['seq_gaps'] for r in ('pts1', 'pts2', 'pts3', 'b0-2') for p in ('a-peer-tap', 'b-dut-tap'))
2614	480,000	summary/pts1/align-a-c.json	,d#0	same(align(r, p)['compared_equal'] for r in ('pts1', 'pts2', 'pts3') for p in 'ab')
2614	480,000	summary/pts1/align-a-c.json	,d#1	same(align(r, p)['mcasp_frames'] for r in ('pts1', 'pts2', 'pts3') for p in 'ab')
2614	three	summary/pts1/align-a-c.json	w	sum(1 for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') if (ROOT / f'summary/{r}/align-a-c.json').exists() and align(r, 'a')['mcasp_frames'] == 480000)
2614	34.1	r2/b0-2-receipt.json	.1f	d['overlap']['seconds']
2614	0	summary/pts1/align-a-c.json	d#0	same(len(align(r, p)['slips']) for r in ('pts1', 'pts2', 'pts3', 'b0-2') for p in 'ab')
2615	-1.00	summary/pts2/d-extcap-pair.json	.2f	same(r['tone_' + t]['median']['level_dbfs'] for x in ('pts2', 'b0-2') for r, t in zip(load(f'summary/{x}/d-extcap-pair.json')['rows'], ('997', '9973')))
2615	303.8	summary/b0-2/d-loop-decode.json	.1f	d['decoded'] / 48000
2615	two		w	load('summary/pts2/d-loop-decode.json')['repeats']
2615	2		d	same(e['frames'] for e in load('summary/pts2/d-loop-decode.json')['events'])
2616	06:23	r2/source-receipt.json	hm	Decimal(clock(get(d, 'reads.b16b-state-1.at')))
2616	06:50	r2/source-receipt.json	hm	Decimal(clock(get(d, 'reads.b16b-state-2.at')))
2617	-123.95	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch0_all']['thdn_db_median']
2617	-122.80	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch1_all']['thdn_db_median']
2617	300	summary/b0-2/c-b9-grade.json	d	d['summary']['blocks']
2617	0	summary/b0-2/c-b9-grade.json	d#0	d['summary']['events']
2617	0.0000	summary/b0-2/c-b9-grade.json	z.4f	d['summary']['effective_offset_ppm']
2617	34.1	r2/b0-2-receipt.json	.1f	d['overlap']['seconds']
# B16b: method
2627	one	runs/pts1-lock.txt	w	same(len(stamps(f'runs/{r}-lock.txt', 'LOCK')) for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3'))
2635	06:23:39		cest	stamps('runs/pts1-lock.txt', 'LOCK')[0]
2635	06:24:28		cest	stamps('runs/pts1-lock.txt', 'UNLOCK')[0]
2635	06:23:46	runs/pts1/events.jsonl	cest	E('pts1', 'bind')['t']
2635	24.5	runs/pts1/events.jsonl	.1f	E('pts1', 'capture-done', what='tap')['seconds']
2635	06:23:58	runs/pts1/events.jsonl	cest	E('pts1', 'captures-started')['started']['tap']
2635	16	runs/pts1/events.jsonl	.0f	E('pts1', 'capture-done', what='extcap')['seconds']
2635	10	summary/pts1/c-mcasp.json	.0f	d['seconds']
2635	06:24:02	runs/pts1/events.jsonl	cest	E('pts1', 'captures-started')['started']['mcasp']
2636	06:28:06		cest	stamps('runs/pts2-lock.txt', 'LOCK')[0]
2636	06:28:56		cest	stamps('runs/pts2-lock.txt', 'UNLOCK')[0]
2636	06:28:13	runs/pts2/events.jsonl	cest	E('pts2', 'bind')['t']
2636	06:28:25	runs/pts2/events.jsonl	cest	E('pts2', 'captures-started')['started']['tap']
2636	2	tools/run_b16.py	d#0	r2lead()
2636	10	summary/pts2/c-mcasp.json	.0f	d['seconds']
2636	06:28:31.5	runs/pts2/events.jsonl	cest1	E('pts2', 'captures-started')['started']['mcasp'] + r2lead()
2636	2	tools/run_b16.py	d#1	r2lead()
2636	06:28:29.5	runs/pts2/events.jsonl	cest1	E('pts2', 'captures-started')['started']['mcasp']
2637	06:31:28		cest	stamps('runs/b0-lock.txt', 'LOCK')[0]
2637	06:37:05		cest	stamps('runs/b0-lock.txt', 'UNLOCK')[0]
2637	06:31:30	runs/b0/events.jsonl	cest	E('b0', 'bind', i=-1)['t']
2637	40	summary/b0/a-peer-tap.json	.0f	d['seconds']
2637	06:31:50	runs/b0/events.jsonl	cest	E('b0', 'captures-started')['started']['tap']
2637	306	summary/b0/d-loop-decode.json	.0f	d['frames'] / 48000
2638	06:37:31		cest	stamps('runs/b0-2-lock.txt', 'LOCK')[0]
2638	06:43:17		cest	stamps('runs/b0-2-lock.txt', 'UNLOCK')[0]
2638	06:37:39	runs/b0-2/events.jsonl	cest	E('b0-2', 'bind', i=-1)['t']
2638	40	summary/b0-2/a-peer-tap.json	.0f	d['seconds']
2638	06:37:59	runs/b0-2/events.jsonl	cest	E('b0-2', 'captures-started')['started']['tap']
2638	306	summary/b0-2/d-extcap-pair.json	.0f	d['seconds']
2638	300	summary/b0-2/c-b9-grade.json	.0f	d['seconds']
2638	06:38:03.2	runs/b0-2/events.jsonl	cest1	E('b0-2', 'captures-started')['started']['mcasp']
2638	2	tools/run_b16.py	d	r2lead()
2638	06:38:05.2	runs/b0-2/events.jsonl	cest1	E('b0-2', 'captures-started')['started']['mcasp'] + r2lead()
2639	06:48:55		cest	stamps('runs/pts3-lock.txt', 'LOCK')[0]
2639	06:49:45		cest	stamps('runs/pts3-lock.txt', 'UNLOCK')[0]
2639	06:49:02	runs/pts3/events.jsonl	cest	E('pts3', 'bind')['t']
2639	06:49:14	runs/pts3/events.jsonl	cest	E('pts3', 'captures-started')['started']['tap']
2642	eight		w	identity_maps(cen('restore/census-startb.jsonl', 'map-dut-0x000f-0-0'))
2642	four		w	identity_maps(cen('restore/census-startb.jsonl', 'map-dut-0x000e-0-0'))
2644	566d3dfa...	runs/pts2/events.jsonl	s	same(E(r, 'loop-staged')['sha256'] for r in ('pts2', 'b0', 'b0-2'))[:8] + '...'
2648	0205022001006000	runs/pts1/events.jsonl	s	same(x['listener_fmt'] for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') for x in ev(r, 'format-check', listener='dut-in-0') if x['set'] is None and x['talker_fmt'] == x['listener_fmt'])
2649	041060010000bb80	runs/b0/events.jsonl	s	same(x['listener_fmt'] for r in ('b0', 'b0-2') for x in ev(r, 'format-check', listener='dut-in-1') if x['set'] is None and x['talker_fmt'] == x['listener_fmt'])
2651	0	runs/b0/events.jsonl	d	same(x['source'] for r in ('b0', 'b0-2') for x in ev(r, 'clock-read', who='dut'))
2659	3		d	Decimal(rx('tools/b9_thdn.py', r'^FLOOR_DB = ([\d.]+)'))
2661	0.01	summary/pts1/a-peer-tap.json	.2f	bound(max(abs(t['median']['snr_db'] + t['median']['thdn_db']) for r in ('pts1', 'pts2', 'pts3', 'b0-2') for p in PFILE_ for c in (0, 1) for t in [pt(r, p, c, (997, 9973)[c])]), '0.01')
2663	300	summary/b0-2/c-b9-grade.json	.0f	d['seconds']
2663	630	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	rx(FIND_P, r'^(\d+) s, untouched, from (\d+) s after the last bind or clock-source set')
2663	one		w	len(stamps('runs/b0-2-lock.txt', 'LOCK'))
2664	24.0	r2/b0-2-receipt.json	.1f	d['timing']['command_after_binds_s']
2665	2	tools/run_b16.py	d	r2lead()
2667	26	r2/b0-2-receipt.json	.0f	d['timing']['recording_after_binds_s']
2667	20	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	rx(FIND_P, r'^(\d+) s, untouched, from (\d+) s after the last bind or clock-source set', group=2)
2669	One	RAW-ARTIFACTS.json	W	sum(1 for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') if raw(r + '/mcasp-all.raw')['bytes'] == 0)
# B16b: the four points
2680	-1	summary/pts1/a-peer-tap.json	d	same(c['min'] for c in [c for r in ('pts1', 'pts2', 'pts3', 'b0-2') for p in ('a-peer-tap', 'b-dut-tap', 'c-mcasp') for c in load(f'summary/{r}/{p}.json')['channels'] if c['channel'] in (2, 3)])
2680	0	summary/pts1/a-peer-tap.json	d	same(c['max'] for c in [c for r in ('pts1', 'pts2', 'pts3', 'b0-2') for p in ('a-peer-tap', 'b-dut-tap', 'c-mcasp') for c in load(f'summary/{r}/{p}.json')['channels'] if c['channel'] in (2, 3)])
2707	two	summary/pts1/d-extcap-pair.json	w	same(len(load(f'summary/{r}/d-extcap-pair.json')['rows']) for r in ('pts1', 'pts3'))
2707	-1	summary/pts1/d-extcap-pair.json	d	same(v for r in ('pts1', 'pts3') for x in load(f'summary/{r}/d-extcap-pair.json')['rows'] for v in (x['min'], x['max']))
2708	-1.00	summary/pts2/d-extcap-pair.json	.2f	same([d['rows'][0]['tone_997']['median']['level_dbfs'], d['rows'][1]['tone_9973']['median']['level_dbfs']])
2708	997.0000	summary/pts2/d-extcap-pair.json	.4f	d['rows'][0]['tone_997']['median']['f_hz']
2708	9,973.0000	summary/pts2/d-extcap-pair.json	,.4f	d['rows'][1]['tone_9973']['median']['f_hz']
2708	0.000	summary/pts2/d-extcap-pair.json	z.3f	same(q(t['median']['ppm'], 3) for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2708	-146.06	summary/pts2/d-extcap-pair.json	.2f	d['rows'][0]['tone_997']['median']['thdn_db']
2708	-145.99	summary/pts2/d-extcap-pair.json	.2f	d['rows'][1]['tone_9973']['median']['thdn_db']
2708	11	summary/pts2/d-extcap-pair.json	d	same(len(floor_inside(t)) for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2708	13	summary/pts2/d-extcap-pair.json	d	same(len(inside(t['per_block'])) for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2708	16	summary/pts2/d-extcap-pair.json	d	same(len(t['per_block']) for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2708	0	summary/pts2/d-extcap-pair.json	d#0	same(silent(t['per_block'])[0] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2708	1	summary/pts2/d-extcap-pair.json	d#0	same(silent(t['per_block'])[-1] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2708	2	summary/pts2/d-extcap-pair.json	d#0	same(inside(t['per_block'])[0] - 1 for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2708	6	summary/pts2/d-extcap-pair.json	d#0	same([i for i in inside(t['per_block']) if i not in floor_inside(t)][0] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2708	12	summary/pts2/d-extcap-pair.json	d#0	same([i for i in inside(t['per_block']) if i not in floor_inside(t)][1] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2708	2		d#1	same(e['frames'] for e in load('summary/pts2/d-loop-decode.json')['events'])
2708	6.131		.3f	load('summary/pts2/d-loop-decode.json')['events'][0]['second']
2708	12.113		.3f	load('summary/pts2/d-loop-decode.json')['events'][1]['second']
2708	-4		d	load('summary/pts2/d-loop-decode.json')['net_step_frames']
2708	665,599		,d	load('summary/pts2/d-loop-decode.json')['decoded']
2708	0		d#1	load('summary/pts2/d-loop-decode.json')['torn']
2709	303	summary/b0-2/d-extcap-pair.json	d	same(n for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']) for n in (len(floor_inside(t)), len(inside(t['per_block']))))
2709	306	summary/b0-2/d-extcap-pair.json	d	same(len(t['per_block']) for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2709	0	summary/b0-2/d-extcap-pair.json	d#0	same(silent(t['per_block'])[0] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2709	1	summary/b0-2/d-extcap-pair.json	d#0	same(silent(t['per_block'])[-1] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2709	2	summary/b0-2/d-extcap-pair.json	d#0	same(inside(t['per_block'])[0] - 1 for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2709	0		d#1	len(load('summary/b0-2/d-loop-decode.json')['events'])
2709	0		d#2	load('summary/b0-2/d-loop-decode.json')['torn']
2709	14,583,286		,d	load('summary/b0-2/d-loop-decode.json')['decoded']
2709	14,583,189		,d	load('summary/b0/d-loop-decode.json')['decoded']
2711	-1.00	summary/pts2/ctl-dut-talker-dut-tap.json	.2f	same(q(x['median']['level_dbfs'], 2) for x in taps2())
2712	-146.06	summary/pts2/ctl-dut-talker-dut-tap.json	.2f	same(q(x['median']['thdn_db'], 2) for x in taps2()[0::2])
2712	-145.99	summary/pts2/ctl-dut-talker-dut-tap.json	.2f	same(q(x['median']['thdn_db'], 2) for x in taps2()[1::2])
2712	15	summary/pts2/ctl-dut-talker-dut-tap.json	d	same(n for x in taps2() for n in (len(floor_inside(x)), len(inside(x['per_block']))))
2713	23	summary/pts2/ctl-dut-talker-dut-tap.json	d	same(len(x['per_block']) for x in taps2())
2713	0	summary/pts2/ctl-dut-talker-dut-tap.json	d#0	same(runs_of(silent(x['per_block']))[0][0] for x in taps2())
2713	2	summary/pts2/ctl-dut-talker-dut-tap.json	d#0	same(runs_of(silent(x['per_block']))[0][1] for x in taps2())
2713	20	summary/pts2/ctl-dut-talker-dut-tap.json	d#0	same(runs_of(silent(x['per_block']))[1][0] for x in taps2())
2713	22	summary/pts2/ctl-dut-talker-dut-tap.json	d#0	same(runs_of(silent(x['per_block']))[1][1] for x in taps2())
2714	3	summary/pts2/ctl-dut-talker-dut-tap.json	d	same(inside(x['per_block'])[0] - 1 for x in taps2())
2714	19	summary/pts2/ctl-dut-talker-dut-tap.json	d	same(inside(x['per_block'])[-1] + 1 for x in taps2())
2714	two		w	load('summary/pts2/d-loop-decode.json')['repeats']
2724	480,000	summary/pts1/align-b-c.json	,d	same(x['compared_equal'] for x in [align(r, p) for r in ('pts1', 'pts2', 'pts3') for p in 'ab'])
2724	480,000	summary/pts1/align-b-c.json	,d	same(x['mcasp_frames'] for x in [align(r, p) for r in ('pts1', 'pts2', 'pts3') for p in 'ab'])
2724	0	summary/pts1/align-b-c.json	d	same(len(x['slips']) for x in [align(r, p) for r in ('pts1', 'pts2', 'pts3') for p in 'ab'])
2724	480,000	summary/pts1/align-a-c.json	,d	same(x['compared_equal'] for x in [align(r, p) for r in ('pts1', 'pts2', 'pts3') for p in 'ab'])
2724	480,000	summary/pts1/align-a-c.json	,d	same(x['mcasp_frames'] for x in [align(r, p) for r in ('pts1', 'pts2', 'pts3') for p in 'ab'])
2724	0	summary/pts1/align-a-c.json	d	same(len(x['slips']) for x in [align(r, p) for r in ('pts1', 'pts2', 'pts3') for p in 'ab'])
2725	1,637,980	summary/b0-2/align-b-c.json	,d	d['compared_equal']
2725	34.1	summary/b0-2/align-b-c.json	.1f	d['compared_equal'] / 48000
2725	0	summary/b0-2/align-b-c.json	d#0	d['frames_differing']
2725	0	summary/b0-2/align-b-c.json	d#1	len(d['slips'])
2725	1,637,452	summary/b0-2/align-a-c.json	,d	d['compared_equal']
2725	34.1	summary/b0-2/align-a-c.json	.1f#1	d['compared_equal'] / 48000
2725	0	summary/b0-2/align-a-c.json	d#2	d['frames_differing']
2725	0	summary/b0-2/align-a-c.json	d#3	len(d['slips'])
2729	-14.14	summary/pts1/a-peer-tap.json	.2f	same(T(load(f'summary/{r}/a-peer-tap.json'), 0, 'level_dbfs') for r in ('pts1', 'pts2'))
2730	-14.0	r2/source-receipt.json	.1f	meter(('b16b-meters-1', 'b16b-meters-2', 'b16b-state-2'), 'the second pair of outputs', 'leaving_dbfs')
2731	-38.5	r2/source-receipt.json	.1f	meter(('b16b-meters-1', 'b16b-meters-2', 'b16b-state-2'), 'the documented pair of outputs', 'leaving_dbfs')
# B16b: the tone source changed during the lane
2736	d9684a8f...		s	rx('runs/b16b-tone-start.txt', r'LOOP_SHA256 ([0-9a-f]{8})') + '...'
2736	06:23:26		cest	stamps('runs/b16b-tone-start.txt', 'STATUS')[0] - Decimal(rx('runs/b16b-tone-start.txt', r'hw_ptr : (\d+)')) / 48000
2736	06:52:19		cest	stamps('runs/b16b-tone-stop.txt', 'LOCK')[0]
2737	06:23	r2/source-receipt.json	hm	Decimal(clock(get(d, 'reads.b16b-state-1.at')))
2737	06:50	r2/source-receipt.json	hm	Decimal(clock(get(d, 'reads.b16b-state-2.at')))
2739	-38.5	r2/source-receipt.json	.1f	meter(('b16b-meters-1', 'b16b-meters-2', 'b16b-state-2'), 'the documented pair of outputs', 'leaving_dbfs')
2739	-14.0	r2/source-receipt.json	.1f	meter(('b16b-meters-1', 'b16b-meters-2', 'b16b-state-2'), 'the second pair of outputs', 'leaving_dbfs')
2740	1,255	r2/source-receipt.json	,d	get(d, 'compare.1')['entries'][1]
2740	2,262	r2/source-receipt.json	,d	get(d, 'compare.1')['entries'][0]
2741	1,255	r2/source-receipt.json	,d	get(d, 'compare.1')['both']
2741	four	r2/source-receipt.json	w	get(d, 'compare.1')['differ']
2745	two	r2/source-receipt.json	w	sum(1 for x in get(d, 'compare.1')['differing'] if x['cls'] == 'an input of a monitoring mix')
2746	two	r2/source-receipt.json	w	same(x['messages'][0] for x in get(d, 'compare.1')['differing'] if x['cls'] == 'an input of a monitoring mix')
2747	one	r2/source-receipt.json	w	same(x['messages'][1] for x in get(d, 'compare.1')['differing'] if x['cls'] == 'an input of a monitoring mix' and x['second_last_among_first'] and x['all_minus_infinity'])
2749	1,255	r2/source-receipt.json	,d	get(d, 'compare.1')['both']
2749	two	r2/source-receipt.json	w	sum(1 for x in get(d, 'compare.1')['differing'] if x['cls'] != 'an input of a monitoring mix')
2751	1,007	r2/source-receipt.json	,d	get(d, 'compare.1')['entries'][0] - get(d, 'compare.1')['both']
2757	06:28:50	summary/pts2/a-peer-tap.json	cest	d['info']['last_t']
2757	-14.1353	summary/pts1/a-peer-tap.json	.4f	same(T(load(f'summary/{r}/a-peer-tap.json'), 0, 'level_dbfs') for r in ('pts1', 'pts2'))
2757	+6.94	summary/pts1/a-peer-tap.json	+.2f	min(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))
2757	+6.96	summary/pts1/a-peer-tap.json	+.2f	max(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))
2757	-109.68		.2f	load('summary/pts1/c-b9-grade.json')['summary']['ch0_floor']['thdn_db_median']
2757	-111.26		.2f	load('summary/pts2/c-b9-grade.json')['summary']['ch0_floor']['thdn_db_median']
2757	-89.83		.2f	load('summary/pts1/c-b9-grade.json')['summary']['ch1_floor']['thdn_db_median']
2757	-91.51		.2f	load('summary/pts2/c-b9-grade.json')['summary']['ch1_floor']['thdn_db_median']
2757	+3.00		+.2f	load('summary/pts1/c-b9-grade.json')['phase_net_frames']
2757	+3.01		+.2f	load('summary/pts2/c-b9-grade.json')['phase_net_frames']
2757	10	summary/pts1/c-b9-grade.json	.0f	same(grade(r)['seconds'] for r in ('pts1', 'pts2'))
2757	Two		W	load('summary/pts2/d-loop-decode.json')['repeats']
2757	2		d	same(e['frames'] for e in load('summary/pts2/d-loop-decode.json')['events'])
2757	13.9		.1f	load('summary/pts2/d-loop-decode.json')['decoded'] / 48000
2758	06:31:51	summary/b0/a-peer-tap.json	cest	d['info']['first_t']
2758	-14.1035	summary/b0/a-peer-tap.json	.4f	same(T(load(f'summary/{r}/a-peer-tap.json'), 0, 'level_dbfs') for r in ('b0', 'b0-2', 'pts3'))
2758	0.000	summary/b0/a-peer-tap.json	z.3f	same(q(pt(r, p, c, t)['median']['ppm'], 3) for r in ('b0-2', 'pts3') for p in 'abc' for c, t in ((0, 997), (1, 9973)))
2758	-123.98		.2f	same(load('summary/pts3/c-b9-grade.json')['summary'][c + '_floor']['thdn_db_median'] for c in ('ch0', 'ch1'))
2758	-123.98		.2f	load('summary/b0-2/c-b9-grade.json')['summary']['ch0_floor']['thdn_db_median']
2758	-123.95		.2f	load('summary/b0-2/c-b9-grade.json')['summary']['ch1_floor']['thdn_db_median']
2758	0.0000		z.4f	load('summary/pts3/c-b9-grade.json')['phase_net_frames']
2758	10		.0f	load('summary/pts3/c-b9-grade.json')['seconds']
2758	0.0005		.4f	load('summary/b0-2/c-b9-grade.json')['phase_net_frames']
2758	300		.0f	load('summary/b0-2/c-b9-grade.json')['seconds']
2758	303.8	summary/b0-2/d-loop-decode.json	.1f	same(q(dec(r)['decoded'] / 48000, 1) for r in ('b0', 'b0-2'))
2760	06:28:50	summary/pts2/a-peer-tap.json	cest	d['info']['last_t']
2761	06:31:51	summary/b0/a-peer-tap.json	cest	d['info']['first_t']
2763	+6.94	summary/pts1/a-peer-tap.json	+.2f	min(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))
2763	+6.96	summary/pts1/a-peer-tap.json	+.2f	max(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))
2766	five		s	rx('HANDOFF.md', r'^\| b17 \|.*?the log holds (\w+) underruns \(([\d:]+) to ([\d:]+), during offline grading\)')
2767	06:45:27		s	rx('HANDOFF.md', r'^\| b17 \|.*?the log holds (\w+) underruns \(([\d:]+) to ([\d:]+), during offline grading\)', group=2)
2767	06:46:38		s	rx('HANDOFF.md', r'^\| b17 \|.*?the log holds (\w+) underruns \(([\d:]+) to ([\d:]+), during offline grading\)', group=3)
2770	06:43:09	runs/b0-2/events.jsonl	cest	E('b0-2', 'capture-done', what='mcasp')['t']
2771	06:49:14	runs/pts3/events.jsonl	cest	E('pts3', 'captures-started')['started']['tap']
# B16b: B0
2778	1	runs/b0-2/events.jsonl	d	same(E(r, 'listener-read', listener='dut-in-1')['media_locked'] for r in ('b0', 'b0-2'))
2778	12	runs/b0-2/events.jsonl	d	same(q(E(r, 'listener-read', listener='dut-in-1')['t'] - E(r, 'bind', listener='dut-in-1')['t'], 0) for r in ('b0', 'b0-2'))
2779	0x00000020	runs/b0-2/dut-before-binds.txt	s	same('0x%08x' % le32(mem(f'runs/{r}/dut-{w}.txt', '0x900008f8', 8)) for r in ('b0', 'b0-2') for w in ('before-binds', 'after-captures'))
2780	0	runs/b0-2/events.jsonl	d	same(x['source'] for r in ('b0', 'b0-2') for x in ev(r, 'clock-read', who='dut'))
2782	300	summary/b0-2/c-b9-grade.json	.0f	d['seconds']
2791	0.0005	summary/b0-2/c-b9-grade.json	.4f	d['phase_net_frames']
2791	131	r2/b0-2-receipt.json	d	d['degraded']
2792	3		d	Decimal(rx('tools/b9_thdn.py', r'^FLOOR_DB = ([\d.]+)'))
2792	0	r2/b0-2-receipt.json	d	d['degraded_runs'][0][0]
2792	18	r2/b0-2-receipt.json	d	d['degraded_runs'][0][1]
2793	28	r2/b0-2-receipt.json	d	d['degraded_runs'][1][0]
2793	31	r2/b0-2-receipt.json	d	d['degraded_runs'][1][1]
2793	43	r2/b0-2-receipt.json	d	d['degraded_runs'][2][0]
2793	44	r2/b0-2-receipt.json	d	d['degraded_runs'][2][1]
2793	46	r2/b0-2-receipt.json	d	d['degraded_runs'][3][0]
2793	54	r2/b0-2-receipt.json	d	d['degraded_runs'][3][1]
2794	1,637,452	r2/b0-2-receipt.json	,d	min(d['overlap']['frames_a'], d['overlap']['frames_b'])
2794	34.1	r2/b0-2-receipt.json	.1f	d['overlap']['seconds']
2795	0	r2/b0-2-receipt.json	d#0	d['overlap']['whole_blocks'][0]
2795	33	r2/b0-2-receipt.json	d	d['overlap']['whole_blocks'][1]
2795	131	r2/b0-2-receipt.json	d	d['degraded']
2795	23	r2/b0-2-receipt.json	d	d['overlap']['degraded_inside']
2795	0	r2/b0-2-receipt.json	d#1	d['overlap']['degraded_inside_runs'][0][0]
2795	18	r2/b0-2-receipt.json	d	d['overlap']['degraded_inside_runs'][0][1]
2795	28	r2/b0-2-receipt.json	d	d['overlap']['degraded_inside_runs'][1][0]
2795	31	r2/b0-2-receipt.json	d	d['overlap']['degraded_inside_runs'][1][1]
2796	23	r2/b0-2-receipt.json	d	d['overlap']['degraded_inside']
2797	108	r2/b0-2-receipt.json	d	d['overlap']['degraded_beyond']
2797	43	r2/b0-2-receipt.json	d	d['overlap']['degraded_beyond_runs'][0][0]
2797	251	r2/b0-2-receipt.json	d	d['overlap']['degraded_beyond_runs'][-1][1]
2798	thirteen	r2/b0-2-receipt.json	w	len(d['overlap']['degraded_beyond_runs'])
2801	34.1	r2/b0-2-receipt.json	.1f	d['overlap']['seconds']
2805	34.1	r2/b0-2-receipt.json	.1f	d['overlap']['seconds']
2807	-124	summary/b0-2/c-b9-grade.json	d	same(q(d['summary'][c + '_floor']['thdn_db_median'], 0) for c in ('ch0', 'ch1'))
2807	23	r2/b0-2-receipt.json	d	d['overlap']['degraded_inside']
2807	-100.61	r2/b0-2-receipt.json	.2f	d['tones']['997 Hz']['worst_inside']['thdn_db']
2807	-80.63	r2/b0-2-receipt.json	.2f	d['tones']['9,973 Hz']['worst_inside']['thdn_db']
2807	7	r2/b0-2-receipt.json	d	same(d['tones'][t]['worst_inside']['block'] for t in ('997 Hz', '9,973 Hz'))
2807	06:28:50		cest	load('summary/pts2/a-peer-tap.json')['info']['last_t']
2807	+6.94	summary/pts1/a-peer-tap.json	+.2f	min(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))
2807	+6.96	summary/pts1/a-peer-tap.json	+.2f	max(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))
2807	13		.0f	min(x - [load('summary/b0-2/c-b9-grade.json')['summary'][c + '_floor']['thdn_db_median'] for c in ('ch0', 'ch1')][i % 2] for i, x in enumerate([load('summary/' + r + '/c-b9-grade.json')['summary'][c + '_floor']['thdn_db_median'] for r in ('pts1', 'pts2') for c in ('ch0', 'ch1')]))
2807	34		.0f	max(x - [load('summary/b0-2/c-b9-grade.json')['summary'][c + '_floor']['thdn_db_median'] for c in ('ch0', 'ch1')][i % 2] for i, x in enumerate([load('summary/' + r + '/c-b9-grade.json')['summary'][c + '_floor']['thdn_db_median'] for r in ('pts1', 'pts2') for c in ('ch0', 'ch1')]))
2807	10	summary/pts1/c-mcasp.json	.0f	same(load(f'summary/{r}/c-mcasp.json')['seconds'] for r in ('pts1', 'pts2'))
2807	108	r2/b0-2-receipt.json	d	d['overlap']['degraded_beyond']
2807	-100.47	r2/b0-2-receipt.json	.2f	d['tones']['997 Hz']['worst_beyond']['thdn_db']
2807	-80.48	r2/b0-2-receipt.json	.2f	d['tones']['9,973 Hz']['worst_beyond']['thdn_db']
2807	224	r2/b0-2-receipt.json	d	same(d['tones'][t]['worst_beyond']['block'] for t in ('997 Hz', '9,973 Hz'))
2807	23	r2/b0-2-receipt.json	d	d['overlap']['degraded_inside']
2807	39	r2/b0-2-receipt.json	d	same(d['tones'][t]['a_blocks'] for t in ('997 Hz', '9,973 Hz'))
2807	-102.55	r2/b0-2-receipt.json	.2f	d['tones']['997 Hz']['a_worst_db']
2807	-82.58	r2/b0-2-receipt.json	.2f	d['tones']['9,973 Hz']['a_worst_db']
2808	0	summary/b0-2/a-peer-tap.json	d	same(load(f'summary/b0-2/{p}.json')['info']['seq_gaps'] for p in ('a-peer-tap', 'b-dut-tap'))
2808	40	summary/b0-2/a-peer-tap.json	d	same(q(load(f'summary/b0-2/{p}.json')['seconds'], 0) for p in ('a-peer-tap', 'b-dut-tap'))
2809	108	r2/b0-2-receipt.json	d	d['overlap']['degraded_beyond']
2809	300	summary/b0-2/c-b9-grade.json	.0f	d['seconds']
2809	0.0005	summary/b0-2/c-b9-grade.json	.4f	d['phase_net_frames']
2809	34.1	r2/b0-2-receipt.json	.1f	d['overlap']['seconds']
2810	14,583,286		,d	load('summary/b0-2/d-loop-decode.json')['decoded']
2810	0		d#1	load('summary/b0-2/d-loop-decode.json')['net_step_frames']
2810	0		d#0	len(load('summary/b0-2/d-loop-decode.json')['events'])
2810	303	summary/b0-2/d-extcap-pair.json	d	same(n for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']) for n in (len(floor_inside(t)), len(inside(t['per_block']))))
2810	two		w	load('summary/pts2/d-loop-decode.json')['repeats']
2813	3,077,452	summary/b0-2/align-a-c.json	,d	sum(align(r, 'a')['compared_equal'] for r in ('pts1', 'pts2', 'pts3', 'b0-2'))
2813	3,077,980	summary/b0-2/align-b-c.json	,d	sum(align(r, 'b')['compared_equal'] for r in ('pts1', 'pts2', 'pts3', 'b0-2'))
2813	four	summary/b0-2/align-a-c.json	w	sum(1 for r in RUNS if (ROOT / f'summary/{r}/align-a-c.json').exists() and r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3'))
2817	0	runs/b0-2/dut-before-binds.txt	d	same(le32(mem(f'runs/{r}/dut-{w}.txt', '0x900008d4', 12), 4) for r in ('b0', 'b0-2') for w in ('before-binds', 'after-captures'))
2817	158		d	slipb('runs/b0-2/dut-before-binds.txt')
2817	160		d	slipb('runs/b0-2/dut-after-captures.txt')
2817	one		w	(slipb('runs/b0-2/dut-after-captures.txt') - slipb('runs/b0-2/dut-before-binds.txt')) // 2
2818	156		d	slipb('runs/b0/dut-before-binds.txt')
2818	158		d	slipb('runs/b0/dut-after-captures.txt')
# B16b: bench as left
2854	0205022001006000		s	cen('restore/census-endb.jsonl', 'format-dut-5-0')['payload'][8:]
2854	041060010000bb80		s	cen('restore/census-endb.jsonl', 'format-dut-5-1')['payload'][8:]
2854	0		d#1	payload_word(cen('restore/census-endb.jsonl', 'clock', 'dut'), 8)
2855	0205022002006000		s	cen('restore/census-endb.jsonl', 'format-peer-5-0')['payload'][8:]
2855	1		d#1	payload_word(cen('restore/census-endb.jsonl', 'clock', 'peer'), 8)
2856	45		s	rx('restore/census-compare-b16b.txt', r'"same": (\d+)')
2856	46		s	rx('restore/census-compare-b16b.txt', r'"compared": (\d+)')
2857	276		d	nvm('restore/dut-startb.txt')['seq']
2857	286		d	nvm('restore/dut-endb.txt')['seq']
2857	42		d	nvm('restore/dut-startb.txt')['commits']
2857	52		d	nvm('restore/dut-endb.txt')['commits']
2857	0		d	nvm('restore/dut-endb.txt')['pend']
2858	06:52:19		cest	stamps('runs/b16b-tone-stop.txt', 'LOCK')[0]
2867	five		w	same([cdiff('restore/counters-endb.jsonl', 'restore/counters-startb.jsonl', 'peer', 6, 0, 0), cdiff('restore/counters-endb.jsonl', 'restore/counters-startb.jsonl', 'peer', 6, 0, 1)])
2868	one		w	same([cdiff('restore/counters-endb.jsonl', 'restore/counters-startb.jsonl', 'peer', 6, 0, 0), cdiff('restore/counters-endb.jsonl', 'restore/counters-startb.jsonl', 'peer', 6, 0, 1)]) // sum(1 for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') for b in ev(r, 'bind') if b['listener'] == 'dut-in-0')
2868	two		w	same([cdiff('restore/counters-endb.jsonl', 'restore/counters-startb.jsonl', 'peer', 6, 2, 0), cdiff('restore/counters-endb.jsonl', 'restore/counters-startb.jsonl', 'peer', 6, 2, 1)])
2871	152		d	slipb('restore/dut-startb.txt')
2871	162		d	slipb('restore/dut-endb.txt')
2871	five		w	(slipb('restore/dut-endb.txt') - slipb('restore/dut-startb.txt')) // 2
2872	five	runs/pts1/events.jsonl	w	sum(1 for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') for b in ev(r, 'bind') if b['listener'] == 'dut-in-0')
2873	one	runs/b0-2/dut-after-captures.txt	w	same(((le32(mem(f'runs/{r}/dut-after-captures.txt', '0x900008d4', 12)) & 0xffff) - (le32(mem(f'runs/{r}/dut-before-binds.txt', '0x900008d4', 12)) & 0xffff)) // 2 for r in ('b0', 'b0-2'))
2465	two	r2/source-receipt.json	w	sum(1 for k, r in d['reads'].items() if k.startswith('b16-') and r['kind'] == 'state')
2755	3		d	Decimal(rx('tools/b9_thdn.py', r'^FLOOR_DB = ([\d.]+)'))
# B16b: #629 acceptance
2882	five		w	(slipb('restore/dut-endb.txt') - slipb('restore/dut-startb.txt')) // 2
2882	five	runs/pts1/events.jsonl	w	sum(1 for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') for b in ev(r, 'bind') if b['listener'] == 'dut-in-0')
# B16b: limits
2889	Four	summary/b0-2/c-b9-grade.json	W	len([r for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') if (ROOT / f'summary/{r}/c-b9-grade.json').exists()])
2889	Three	summary/pts1/c-b9-grade.json	W	sum(1 for r in [r for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') if (ROOT / f'summary/{r}/c-b9-grade.json').exists()] if load(f'summary/{r}/c-b9-grade.json')['seconds'] == 10)
2889	10	summary/pts1/c-b9-grade.json	.0f	same(grade(r)['seconds'] for r in ('pts1', 'pts2', 'pts3'))
2890	24	runs/pts1/events.jsonl	d	same(q(E(r, 'capture-done', what='tap')['seconds'], 0) for r in ('pts1', 'pts2', 'pts3'))
2890	300	summary/b0-2/c-b9-grade.json	.0f	d['seconds']
2890	40	summary/b0-2/a-peer-tap.json	d	same(q(load(f'summary/b0-2/{p}.json')['seconds'], 0) for p in ('a-peer-tap', 'b-dut-tap'))
2895	23	r2/b0-2-receipt.json	d	d['overlap']['degraded_inside']
2895	34.1	r2/b0-2-receipt.json	.1f	d['overlap']['seconds']
2896	108	r2/b0-2-receipt.json	d	d['overlap']['degraded_beyond']
# B16c: the resume
2965	07:48:07		cest	stamps('soc/b16c-precheck-status.log', 'LOCK')[0]
2969	07:48:16		cest	stamps('identity-b16c/lock-window.txt', 'LOCK')[0]
2969	07:48:22		cest	stamps('identity-b16c/lock-window.txt', 'UNLOCK')[0]
2969	45		s	rx('restore/census-compare-b16b-to-b16c.txt', r'"same": (\d+)')
2969	46		s	rx('restore/census-compare-b16b-to-b16c.txt', r'"compared": (\d+)')
2970	8	controls/b16c-dryrun-summary.json	d#0	sum(v == 'PASS' for v in d['scenarios'].values())
2970	8	controls/b16c-dryrun-summary.json	d#1	len(d['scenarios'])
2972	2.585	r2/bcrf-poll-trace.tsv	.3f	lock_bracket('bcrf')[0]
2972	3.161	r2/bcrf-poll-receipt.json	.3f	lock_bracket('bcrf')[1]
2972	596	r2/bcrf-poll-receipt.json	d	win('bcrf')['servo']['LOCKED']
2972	-123.98	summary/bcrf/c-b9-grade.json	.2f	d['summary']['ch0_all']['thdn_db_median']
2972	-123.97	summary/bcrf/c-b9-grade.json	.2f	d['summary']['ch1_all']['thdn_db_median']
2972	300	summary/bcrf/c-b9-grade.json	d	d['summary']['blocks']
2972	300	summary/bcrf/c-b9-grade.json	d	d['summary']['blocks_at_floor']
2972	0	summary/bcrf/c-b9-grade.json	d#0	d['summary']['events']
2972	0.0000	summary/bcrf/c-b9-grade.json	z.4f	d['summary']['effective_offset_ppm']
2972	three	summary/bcrf/c-b9-grade.json	w	terms('bcrf')
2973	6.602	r2/baaf-poll-trace.tsv	.3f	lock_bracket('baaf')[0]
2973	7.180	r2/baaf-poll-receipt.json	.3f	lock_bracket('baaf')[1]
2973	596	r2/baaf-poll-receipt.json	d	win('baaf')['servo']['LOCKED']
2973	-123.98	summary/baaf/c-b9-grade.json	.2f	d['summary']['ch0_all']['thdn_db_median']
2973	-123.97	summary/baaf/c-b9-grade.json	.2f	d['summary']['ch1_all']['thdn_db_median']
2973	300	summary/baaf/c-b9-grade.json	d	same([d['summary']['blocks'], d['summary']['blocks_at_floor']])
2973	0	summary/baaf/c-b9-grade.json	d#0	d['summary']['events']
2973	0.0000	summary/baaf/c-b9-grade.json	z.4f	d['summary']['effective_offset_ppm']
2973	three	summary/baaf/c-b9-grade.json	w	terms('baaf')
2974	34.2	summary/bcrf/align-a-c.json	.1f	min([align(r, p)['compared_equal'] / 48000 for r in ('bcrf', 'baaf') for p in 'ab'])
2974	34.3	summary/bcrf/align-a-c.json	.1f	max([align(r, p)['compared_equal'] / 48000 for r in ('bcrf', 'baaf') for p in 'ab'])
2974	0	summary/bcrf/d-loop-decode.json	d#0	same(len(dec(r)['events']) for r in ('bcrf', 'baaf'))
2974	0	summary/bcrf/d-loop-decode.json	d#1	same(dec(r)['net_step_frames'] for r in ('bcrf', 'baaf'))
# B16c: method
2984	one	runs/bcrf-lock.txt	w	same(len(stamps(f'runs/{r}-lock.txt', 'LOCK')) for r in ('bcrf', 'baaf'))
2990	1	runs/bcrf/events.jsonl	d	same(E(r, 'fol-check')['clk_peer'] for r in ('bcrf', 'baaf'))
2993	0.5	runs/bcrf/events.jsonl	.1f	same(E(r, 'poll-start')['period_s'] for r in ('bcrf', 'baaf'))
2994	0	runs/bcrf/events.jsonl	d#0	same(E(r, 'set-clock', tag='peer-internal')['readback'] for r in ('bcrf', 'baaf'))
2995	5	runs/bcrf/events.jsonl	d	same(q(E(r, 'mark', tag='after-peer-set')['t'] - E(r, 'set-clock', tag='peer-internal')['t'], 0) for r in ('bcrf', 'baaf'))
2998	1	runs/bcrf/events.jsonl	d#0	E('bcrf', 'set-clock', tag='bcrf')['readback']
2998	2	runs/baaf/events.jsonl	d#0	E('baaf', 'set-clock', tag='baaf')['readback']
2999	60		d	Decimal(rx('tools/run_b16c.py', r'^LOCK_WAIT_S = ([\d.]+)'))
3000	20	runs/bcrf/events.jsonl	d	same(q(E(r, 'captures-started')['started']['tap'] - E(r, 'set-clock', who='dut', tag=r)['t'], 0) for r in ('bcrf', 'baaf'))
3001	300	summary/bcrf/c-b9-grade.json	.0f	same(grade(r)['seconds'] for r in ('bcrf', 'baaf'))
3003	40	summary/bcrf/a-peer-tap.json	d	same(q(load(f'summary/{r}/{p}.json')['seconds'], 0) for r in ('bcrf', 'baaf') for p in ('a-peer-tap', 'b-dut-tap'))
3004	20	runs/bcrf/events.jsonl	d	same(q(E(r, 'mark', tag='window-mark-0')['t'] - E(r, 'set-clock', who='dut', tag=r)['t'], 0) for r in ('bcrf', 'baaf'))
3005	6	runs/bcrf/events.jsonl	d	same(q(E(r, 'captures-started')['started']['mcasp'] + r2lead() - E(r, 'mark', tag='window-mark-0')['t'], 0) for r in ('bcrf', 'baaf'))
3005	15	runs/bcrf/events.jsonl	d	same(q(E(r, 'captures-started')['started']['mcasp'] + r2lead() + 300 - E(r, 'mark', tag='window-mark-2')['t'], 0) for r in ('bcrf', 'baaf'))
3008	1	runs/bcrf/events.jsonl	d	same(E(r, 'set-clock', who='peer', tag='restore')['readback'] for r in ('bcrf', 'baaf'))
3012	eight	runs/bcrf/events.jsonl	w	sum(len(ev(r, 'mcasp-playback-check')) for r in ('bcrf', 'baaf'))
3017	07:50:00		cest#0	stamps('runs/bcrf-lock.txt', 'LOCK')[0]
3017	07:56:15		cest#0	stamps('runs/bcrf-lock.txt', 'UNLOCK')[0]
3017	07:50:12.3	runs/bcrf/events.jsonl	cest1#0	E('bcrf', 'set-clock', tag='peer-internal')['t']
3017	07:50:17.5	runs/bcrf/events.jsonl	cest1#0	E('bcrf', 'bind', i=-1)['t']
3017	1	runs/bcrf/events.jsonl	d#0	E('bcrf', 'set-clock', tag='bcrf')['readback']
3017	07:50:29.7	runs/bcrf/events.jsonl	cest1#0	E('bcrf', 'set-clock', tag='bcrf')['t']
3017	07:50:55	runs/bcrf/events.jsonl	cest#0	E('bcrf', 'captures-started')['started']['mcasp'] + r2lead()
3017	07:55:55	runs/bcrf/events.jsonl	cest#0	E('bcrf', 'captures-started')['started']['mcasp'] + r2lead() + load('summary/bcrf/c-b9-grade.json')['seconds']
3017	26	runs/bcrf/events.jsonl	d#0	q(E('bcrf', 'captures-started')['started']['mcasp'] + r2lead() - E('bcrf', 'set-clock', tag='bcrf')['t'], 0)
3017	07:56:00.0	runs/bcrf/events.jsonl	cest1#0	E('bcrf', 'teardown')['t']
3017	07:56:04.0	runs/bcrf/events.jsonl	cest1#0	E('bcrf', 'mark', tag='after-restore')['t']
3018	07:56:52		cest#0	stamps('runs/baaf-lock.txt', 'LOCK')[0]
3018	08:03:07		cest#0	stamps('runs/baaf-lock.txt', 'UNLOCK')[0]
3018	07:57:04.1	runs/baaf/events.jsonl	cest1#0	E('baaf', 'set-clock', tag='peer-internal')['t']
3018	07:57:09.3	runs/baaf/events.jsonl	cest1#0	E('baaf', 'bind', i=-1)['t']
3018	2	runs/baaf/events.jsonl	d#0	E('baaf', 'set-clock', tag='baaf')['readback']
3018	07:57:21.5	runs/baaf/events.jsonl	cest1#0	E('baaf', 'set-clock', tag='baaf')['t']
3018	07:57:47	runs/baaf/events.jsonl	cest#0	E('baaf', 'captures-started')['started']['mcasp'] + r2lead()
3018	08:02:47	runs/baaf/events.jsonl	cest#0	E('baaf', 'captures-started')['started']['mcasp'] + r2lead() + load('summary/baaf/c-b9-grade.json')['seconds']
3018	26	runs/baaf/events.jsonl	d#0	q(E('baaf', 'captures-started')['started']['mcasp'] + r2lead() - E('baaf', 'set-clock', tag='baaf')['t'], 0)
3018	08:02:51.7	runs/baaf/events.jsonl	cest1#0	E('baaf', 'teardown')['t']
3018	08:02:55.7	runs/baaf/events.jsonl	cest1#0	E('baaf', 'mark', tag='after-restore')['t']
2951	two	summary/pts2/d-loop-decode.json	w	d['repeats']
3020	two	controls/b16c-dryrun-summary.json	w	sum(1 for k in d['scenarios'] if k in ('bcrf', 'baaf'))
3022	eight	controls/b16c-dryrun-summary.json	w	len(d['scenarios'])
3033	8	controls/b16c-dryrun-summary.json	d#0	sum(v == 'PASS' for v in d['scenarios'].values())
3033	8	controls/b16c-dryrun-summary.json	d#1	len(d['scenarios'])
3042	3		d	Decimal(rx('tools/b9_thdn.py', r'^FLOOR_DB = ([\d.]+)'))
3044	0.01	summary/bcrf/a-peer-tap.json	.2f	bound(max(abs(t['median']['snr_db'] + t['median']['thdn_db']) for r in ('bcrf', 'baaf', 'b0-2') for p in PFILE_ for c in (0, 1) for t in [pt(r, p, c, (997, 9973)[c])]), '0.01')
# B16c: clock-source record
3050	0	runs/bcrf/events.jsonl	d#0	E('bcrf', 'set-clock', who='peer', tag='peer-internal')['src']
3050	0	runs/bcrf/events.jsonl	d#1	E('bcrf', 'set-clock', who='peer', tag='peer-internal')['readback']
3051	1	runs/bcrf/events.jsonl	d#0	E('bcrf', 'set-clock', who='dut', tag='bcrf')['src']
3051	1	runs/bcrf/events.jsonl	d#1	E('bcrf', 'set-clock', who='dut', tag='bcrf')['readback']
3052	0	runs/bcrf/events.jsonl	d#0	E('bcrf', 'set-clock', who='dut', tag='restore')['src']
3052	0	runs/bcrf/events.jsonl	d#1	E('bcrf', 'set-clock', who='dut', tag='restore')['readback']
3053	1	runs/bcrf/events.jsonl	d#0	E('bcrf', 'set-clock', who='peer', tag='restore')['src']
3053	1	runs/bcrf/events.jsonl	d#1	E('bcrf', 'set-clock', who='peer', tag='restore')['readback']
3054	0	runs/baaf/events.jsonl	d#0	E('baaf', 'set-clock', who='peer', tag='peer-internal')['src']
3054	0	runs/baaf/events.jsonl	d#1	E('baaf', 'set-clock', who='peer', tag='peer-internal')['readback']
3055	2	runs/baaf/events.jsonl	d#0	E('baaf', 'set-clock', who='dut', tag='baaf')['src']
3055	2	runs/baaf/events.jsonl	d#1	E('baaf', 'set-clock', who='dut', tag='baaf')['readback']
3056	0	runs/baaf/events.jsonl	d#0	E('baaf', 'set-clock', who='dut', tag='restore')['src']
3056	0	runs/baaf/events.jsonl	d#1	E('baaf', 'set-clock', who='dut', tag='restore')['readback']
3057	1	runs/baaf/events.jsonl	d#0	E('baaf', 'set-clock', who='peer', tag='restore')['src']
3057	1	runs/baaf/events.jsonl	d#1	E('baaf', 'set-clock', who='peer', tag='restore')['readback']
3059	four	runs/bcrf/events.jsonl	w	same(len([m for m in ev(r, 'mark') if m['tag'] in ('window-mark-0', 'window-mark-1', 'window-mark-2', 'after-captures')]) for r in ('bcrf', 'baaf'))
3059	1	runs/bcrf/events.jsonl	d	same(m['clock']['dut'] for m in ev('bcrf', 'mark') if m['tag'] in ('window-mark-0', 'window-mark-1', 'window-mark-2', 'after-captures'))
3059	2	runs/baaf/events.jsonl	d	same(m['clock']['dut'] for m in ev('baaf', 'mark') if m['tag'] in ('window-mark-0', 'window-mark-1', 'window-mark-2', 'after-captures'))
3059	0	runs/bcrf/events.jsonl	d	same(m['clock']['peer'] for r in ('bcrf', 'baaf') for m in ev(r, 'mark') if m['tag'] in ('window-mark-0', 'window-mark-1', 'window-mark-2', 'after-captures'))
3060	20	runs/bcrf/events.jsonl	d	same(q(E(r, 'mark', tag='window-mark-0')['t'] - E(r, 'set-clock', who='dut', tag=r)['t'], 0) for r in ('bcrf', 'baaf'))
3060	6	runs/bcrf/events.jsonl	d	same(q(E(r, 'captures-started')['started']['mcasp'] + r2lead() - E(r, 'mark', tag='window-mark-0')['t'], 0) for r in ('bcrf', 'baaf'))
3061	15	runs/bcrf/events.jsonl	d	same(q(E(r, 'captures-started')['started']['mcasp'] + r2lead() + 300 - E(r, 'mark', tag='window-mark-2')['t'], 0) for r in ('bcrf', 'baaf'))
3061	0	runs/bcrf/events.jsonl	d	same(E(r, 'mark', tag='after-restore')['clock']['dut'] for r in ('bcrf', 'baaf'))
3062	1	runs/bcrf/events.jsonl	d	same(E(r, 'mark', tag='after-restore')['clock']['peer'] for r in ('bcrf', 'baaf'))
3065	0205022001006000	runs/bcrf/events.jsonl	s	same(x['listener_fmt'] for r in ('bcrf', 'baaf') for x in ev(r, 'format-check', listener='dut-in-0') if x['set'] is None and x['talker_fmt'] == x['listener_fmt'])
3066	041060010000bb80	runs/bcrf/events.jsonl	s	same(x['listener_fmt'] for r in ('bcrf', 'baaf') for x in ev(r, 'format-check', listener='dut-in-1') if x['set'] is None and x['talker_fmt'] == x['listener_fmt'])
# B16c: B-CRF and B-AAF
3073	-1	summary/bcrf/a-peer-tap.json	d	same(c['min'] for c in [c for r in ('bcrf', 'baaf') for p in ('a-peer-tap', 'b-dut-tap', 'c-mcasp') for c in load(f'summary/{r}/{p}.json')['channels'] if c['channel'] in (2, 3)])
3073	0	summary/bcrf/a-peer-tap.json	d	same(c['max'] for c in [c for r in ('bcrf', 'baaf') for p in ('a-peer-tap', 'b-dut-tap', 'c-mcasp') for c in load(f'summary/{r}/{p}.json')['channels'] if c['channel'] in (2, 3)])
3106	0	summary/bcrf/c-b9-grade.json	d	same(grade(r)['effective_offset_ppm'] for r in ('bcrf', 'baaf'))
3106	0.000001	summary/bcrf/c-b9-grade.json	.6f	bound(max(abs(grade(r)['phase_net_frames']) for r in ('bcrf', 'baaf')), '0.000001')
3107	0.0005	summary/b0-2/c-b9-grade.json	.4f	d['phase_net_frames']
3113	1,646,473	summary/bcrf/align-b-c.json	,d	d['compared_equal']
3113	34.3	summary/bcrf/align-b-c.json	.1f#0	d['compared_equal'] / 48000
3113	0	summary/bcrf/align-b-c.json	d#0	d['frames_differing']
3113	0	summary/bcrf/align-b-c.json	d#1	len(d['slips'])
3113	1,647,859	summary/bcrf/align-a-c.json	,d	d['compared_equal']
3113	34.3	summary/bcrf/align-a-c.json	.1f#1	d['compared_equal'] / 48000
3113	0	summary/bcrf/align-a-c.json	d#2	d['frames_differing']
3113	0	summary/bcrf/align-a-c.json	d#3	len(d['slips'])
3114	1,644,390	summary/baaf/align-b-c.json	,d	d['compared_equal']
3114	34.3	summary/baaf/align-b-c.json	.1f#0	d['compared_equal'] / 48000
3114	0	summary/baaf/align-b-c.json	d#0	d['frames_differing']
3114	0	summary/baaf/align-b-c.json	d#1	len(d['slips'])
3114	1,641,156	summary/baaf/align-a-c.json	,d	d['compared_equal']
3114	34.2	summary/baaf/align-a-c.json	.1f#0	d['compared_equal'] / 48000
3114	0	summary/baaf/align-a-c.json	d#2	d['frames_differing']
3114	0	summary/baaf/align-a-c.json	d#3	len(d['slips'])
3121	14,583,391	summary/bcrf/d-loop-decode.json	,d	d['decoded']
3121	0	summary/bcrf/d-loop-decode.json	d#0	d['skips']
3121	0	summary/bcrf/d-loop-decode.json	d#1	d['repeats']
3121	0	summary/bcrf/d-loop-decode.json	d#2	d['net_step_frames']
3121	0	summary/bcrf/d-loop-decode.json	d#3	d['torn']
3121	-1.00		.2f	same([q(load('summary/bcrf/d-extcap-pair.json')['rows'][0]['tone_997']['median']['level_dbfs'], 2), q(load('summary/bcrf/d-extcap-pair.json')['rows'][1]['tone_9973']['median']['level_dbfs'], 2)])
3121	-146.06		.2f	load('summary/bcrf/d-extcap-pair.json')['rows'][0]['tone_997']['median']['thdn_db']
3121	-145.99		.2f	load('summary/bcrf/d-extcap-pair.json')['rows'][1]['tone_9973']['median']['thdn_db']
3121	303		d#0	same(len(floor_inside(t)) for t in (load('summary/bcrf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/bcrf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3121	303		d#1	same(len(inside(t['per_block'])) for t in (load('summary/bcrf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/bcrf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3121	306		d	same(len(t['per_block']) for t in (load('summary/bcrf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/bcrf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3121	0		d#4	same(silent(t['per_block'])[0] for t in (load('summary/bcrf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/bcrf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3121	1		d#0	same(silent(t['per_block'])[-1] for t in (load('summary/bcrf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/bcrf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3121	2		d#0	same(inside(t['per_block'])[0] - 1 for t in (load('summary/bcrf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/bcrf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3122	14,585,924	summary/baaf/d-loop-decode.json	,d	d['decoded']
3122	0	summary/baaf/d-loop-decode.json	d#0	d['skips']
3122	0	summary/baaf/d-loop-decode.json	d#1	d['repeats']
3122	0	summary/baaf/d-loop-decode.json	d#2	d['net_step_frames']
3122	0	summary/baaf/d-loop-decode.json	d#3	d['torn']
3122	-1.00		.2f	same([q(load('summary/baaf/d-extcap-pair.json')['rows'][0]['tone_997']['median']['level_dbfs'], 2), q(load('summary/baaf/d-extcap-pair.json')['rows'][1]['tone_9973']['median']['level_dbfs'], 2)])
3122	-146.06		.2f	load('summary/baaf/d-extcap-pair.json')['rows'][0]['tone_997']['median']['thdn_db']
3122	-145.99		.2f	load('summary/baaf/d-extcap-pair.json')['rows'][1]['tone_9973']['median']['thdn_db']
3122	303		d#0	same(len(floor_inside(t)) for t in (load('summary/baaf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/baaf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3122	303		d#1	same(len(inside(t['per_block'])) for t in (load('summary/baaf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/baaf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3122	306		d	same(len(t['per_block']) for t in (load('summary/baaf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/baaf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3122	0		d#4	same(silent(t['per_block'])[0] for t in (load('summary/baaf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/baaf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3122	1		d#0	same(silent(t['per_block'])[-1] for t in (load('summary/baaf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/baaf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3122	2		d#0	same(inside(t['per_block'])[0] - 1 for t in (load('summary/baaf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/baaf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3124	0	summary/bcrf/d-loop-decode.json	d	same(x['net_step_frames'] for x in [dec(r) for r in ('bcrf', 'baaf')])
3125	303.8		.1f	load('summary/bcrf/d-loop-decode.json')['decoded'] / 48000
3125	303.9		.1f	load('summary/baaf/d-loop-decode.json')['decoded'] / 48000
3125	14.58	summary/bcrf/d-loop-decode.json	.2f	min(x['decoded'] for x in [dec(r) for r in ('bcrf', 'baaf')]) / Decimal(10 ** 6)
3125	0.07	summary/bcrf/d-loop-decode.json	.2f	Decimal(10 ** 6) / min(x['decoded'] for x in [dec(r) for r in ('bcrf', 'baaf')])
3093	300	summary/bcrf/c-b9-grade.json	.0f	same(grade(r)['seconds'] for r in ('bcrf', 'baaf'))
# B16c: the following record
3129	0.5	runs/bcrf/events.jsonl	.1f	same(E(r, 'poll-start')['period_s'] for r in ('bcrf', 'baaf'))
3136	2.585	r2/bcrf-poll-trace.tsv	.3f	lock_bracket('bcrf')[0]
3136	3.161	r2/bcrf-poll-receipt.json	.3f	lock_bracket('bcrf')[1]
3136	596	r2/bcrf-poll-receipt.json	d#0	win('bcrf')['servo']['LOCKED']
3136	596	r2/bcrf-poll-receipt.json	d#1	win('bcrf')['polls']
3136	-6.000	r2/bcrf-poll-receipt.json	.3f	win('bcrf')['trim_ppm'][1]
3136	-6.125	r2/bcrf-poll-receipt.json	.3f	win('bcrf')['trim_ppm'][0]
3136	+10.60	r2/bcrf-poll-receipt.json	+.2f	win('bcrf')['crf_rate_ppm'][0]
3136	+10.65	r2/bcrf-poll-receipt.json	+.2f	win('bcrf')['crf_rate_ppm'][1]
3136	0	r2/bcrf-poll-receipt.json	d#0	same(int(x, 16) for x in win('bcrf')['aafm_stat'])
3136	0	r2/bcrf-poll-receipt.json	d#1	same(win('bcrf')['slip_tdm_dups'] + win('bcrf')['slip_tdm_skips'])
3136	23	runs/bcrf/events.jsonl	d#0	E('bcrf', 'mark', tag='window-mark-0')['counters']['dut-0x0024-0'][0]
3136	22	runs/bcrf/events.jsonl	d#0	E('bcrf', 'mark', tag='window-mark-0')['counters']['dut-0x0024-0'][1]
3136	23	runs/bcrf/events.jsonl	d#1	E('bcrf', 'mark', tag='window-mark-2')['counters']['dut-0x0024-0'][0]
3136	22	runs/bcrf/events.jsonl	d#1	E('bcrf', 'mark', tag='window-mark-2')['counters']['dut-0x0024-0'][1]
3137	6.602	r2/baaf-poll-trace.tsv	.3f	lock_bracket('baaf')[0]
3137	7.180	r2/baaf-poll-receipt.json	.3f	lock_bracket('baaf')[1]
3137	596	r2/baaf-poll-receipt.json	d#0	win('baaf')['servo']['LOCKED']
3137	596	r2/baaf-poll-receipt.json	d#1	win('baaf')['polls']
3137	-6.000	r2/baaf-poll-receipt.json	.3f	win('baaf')['trim_ppm'][1]
3137	-6.125	r2/baaf-poll-receipt.json	.3f	win('baaf')['trim_ppm'][0]
3137	+10.60	r2/baaf-poll-receipt.json	+.2f	win('baaf')['aafm_rate_ppm_valid'][0]
3137	+10.63	r2/baaf-poll-receipt.json	+.2f	win('baaf')['aafm_rate_ppm_valid'][1]
3137	+10.59	r2/baaf-poll-receipt.json	+.2f	win('baaf')['crf_rate_ppm'][0]
3137	+10.65	r2/baaf-poll-receipt.json	+.2f	win('baaf')['crf_rate_ppm'][1]
3137	0x001e0007	r2/baaf-poll-receipt.json	s	'0x' + same(win('baaf')['aafm_stat'])
3137	0	r2/baaf-poll-receipt.json	d#0	same((int(x, 16) >> 8) & 0xff for x in win('baaf')['aafm_stat'])
3137	30	r2/baaf-poll-receipt.json	d	same(int(x, 16) >> 16 for x in win('baaf')['aafm_stat'])
3137	0	r2/baaf-poll-receipt.json	d#1	same(win('baaf')['slip_tdm_dups'] + win('baaf')['slip_tdm_skips'])
3137	24	runs/baaf/events.jsonl	d#0	E('baaf', 'mark', tag='window-mark-0')['counters']['dut-0x0024-0'][0]
3137	23	runs/baaf/events.jsonl	d#0	E('baaf', 'mark', tag='window-mark-0')['counters']['dut-0x0024-0'][1]
3137	24	runs/baaf/events.jsonl	d#1	E('baaf', 'mark', tag='window-mark-2')['counters']['dut-0x0024-0'][0]
3137	23	runs/baaf/events.jsonl	d#1	E('baaf', 'mark', tag='window-mark-2')['counters']['dut-0x0024-0'][1]
3140	five		w	len(re.findall(r'\("0x9000[0-9a-f]+", \d+\)', rx('tools/console_poll_b8.py', r'^CMDS = \((.*)\)$')))
3142	44	r2/bcrf-poll-receipt.json	d	d['locked']['first_locked_poll'] - 1
3142	45	r2/bcrf-poll-receipt.json	d	d['locked']['first_locked_poll']
3142	52	r2/baaf-poll-receipt.json	d	d['locked']['first_locked_poll'] - 1
3142	53	r2/baaf-poll-receipt.json	d	d['locked']['first_locked_poll']
3145	0x...0034	r2/bcrf-poll-receipt.json	s	'0x...' + sorted(set(win('bcrf')['mcsrv_stat_lo16']) | set(win('baaf')['mcsrv_stat_lo16']))[0]
3146	0x...0074	r2/bcrf-poll-receipt.json	s	'0x...' + sorted(set(win('bcrf')['mcsrv_stat_lo16']) | set(win('baaf')['mcsrv_stat_lo16']))[1]
3146	580	r2/bcrf-poll-receipt.json	d	win('bcrf')['mcsrv_stat_lo16']['0034']
3146	16	r2/bcrf-poll-receipt.json	d	win('bcrf')['mcsrv_stat_lo16']['0074']
3147	584	r2/baaf-poll-receipt.json	d	win('baaf')['mcsrv_stat_lo16']['0034']
3147	12	r2/baaf-poll-receipt.json	d	win('baaf')['mcsrv_stat_lo16']['0074']
3150	15		s	rx('repo:docs/design/MEDIA_CLOCK_FOLLOWING.md', r'^\| B AAF \|.*Servo LOCKED within (\d+) s of the set')
3151	0		s	rx('repo:docs/design/MEDIA_CLOCK_FOLLOWING.md', r'^\| B AAF \|.*?; (\d+) net steps between')
3155	30	r2/baaf-poll-receipt.json	d	same(int(x, 16) >> 16 for x in win('baaf')['aafm_stat'])
3157	four	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	w	len(re.split(r', and |, ', b6_rule()))
3162	596	r2/bcrf-poll-receipt.json	d#0	same(win('baaf')['servo']['LOCKED'] for r in ('bcrf', 'baaf'))
3162	596	r2/bcrf-poll-receipt.json	d#1	same(load(f'r2/{r}-poll-receipt.json')['spans']['window-start..window-end']['polls'] for r in ('bcrf', 'baaf'))
3162	2.585	r2/bcrf-poll-trace.tsv	.3f	lock_bracket('bcrf')[0]
3162	3.161	r2/bcrf-poll-receipt.json	.3f	lock_bracket('bcrf')[1]
3162	6.602	r2/baaf-poll-trace.tsv	.3f	lock_bracket('baaf')[0]
3162	7.180	r2/baaf-poll-receipt.json	.3f	lock_bracket('baaf')[1]
3163	0.5	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	re.search(r'within ([\d.]+) ppm', b6_rule()).group(1)
3163	0	summary/bcrf/d-loop-decode.json	d#0	same(dec(r)['net_step_frames'] for r in ('bcrf', 'baaf'))
3163	14,583,391		,d	load('summary/bcrf/d-loop-decode.json')['decoded']
3163	14,585,924		,d	load('summary/baaf/d-loop-decode.json')['decoded']
3163	14.58		.2f	min(load('summary/bcrf/d-loop-decode.json')['decoded'], load('summary/baaf/d-loop-decode.json')['decoded']) / Decimal(10 ** 6)
3163	0.07		.2f	Decimal(10 ** 6) / min(load('summary/bcrf/d-loop-decode.json')['decoded'], load('summary/baaf/d-loop-decode.json')['decoded'])
3163	0.0000	summary/bcrf/c-b9-grade.json	z.4f	same(grade(r)['effective_offset_ppm'] for r in ('bcrf', 'baaf'))
3165	0	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s#0	re.search(r'has (\d+) listener discontinuities', b6_rule()).group(1)
3165	0	summary/bcrf/c-b9-grade.json	d#1	same(grade(r)['summary']['events'] for r in ('bcrf', 'baaf'))
3165	300	summary/bcrf/c-b9-grade.json	.0f	same(grade(r)['seconds'] for r in ('bcrf', 'baaf'))
3165	0	summary/bcrf/d-loop-decode.json	d#2	same(len(dec(r)['events']) for r in ('bcrf', 'baaf'))
3158	four	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	w	len(re.split(r', and |, ', b6_rule()))
3167	three	summary/bcrf/c-b9-grade.json	w	same([terms('bcrf'), terms('baaf')])
3167	four	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	w	len(re.split(r', and |, ', b6_rule()))
3171	162		d	slipb('restore/dut-startc.txt')
3172	188		d	slipb('restore/dut-endc.txt')
3172	two	r2/bcrf-poll-receipt.json	w#0	same(x['dups'][1] - x['dups'][0] for x in [x for r in ('bcrf', 'baaf') for x in load(f'r2/{r}-poll-receipt.json')['slip_lb_steps']])
3172	two	r2/bcrf-poll-receipt.json	w#1	same(len(x['polls']) for x in [x for r in ('bcrf', 'baaf') for x in load(f'r2/{r}-poll-receipt.json')['slip_lb_steps']])
3173	five	r2/bcrf-poll-receipt.json	w	same([len(steps('bcrf', 'binds..dut-set')), len(steps('baaf', 'binds..dut-set'))])
3174	12.2	r2/bcrf-poll-receipt.json	.1f	same(q(-load(f'r2/{r}-poll-receipt.json')['marks_after_set_s']['binds'], 1) for r in ('bcrf', 'baaf'))
3174	0.1	r2/bcrf-poll-receipt.json	.1f	same([q(steps('bcrf', 'binds..dut-set')[0]['after_binds_s'][0], 1), q(steps('baaf', 'binds..dut-set')[0]['after_binds_s'][0], 1)])
3175	1.4	r2/bcrf-poll-receipt.json	.1f	same([q(-steps('bcrf', 'binds..dut-set')[-1]['after_set_s'][1], 1), q(-steps('baaf', 'binds..dut-set')[-1]['after_set_s'][1], 1)])
3177	one	runs/b0-2/dut-after-captures.txt	w	same(((le32(mem(f'runs/{r}/dut-after-captures.txt', '0x900008d4', 12)) & 0xffff) - (le32(mem(f'runs/{r}/dut-before-binds.txt', '0x900008d4', 12)) & 0xffff)) // 2 for r in ('b0', 'b0-2'))
3181	one	r2/bcrf-poll-receipt.json	w	len(steps('bcrf', 'dut-set..first-locked-poll'))
3181	2.08	r2/bcrf-poll-receipt.json	.2f	steps('bcrf', 'dut-set..first-locked-poll')[0]['after_set_s'][0]
3181	2.66	r2/bcrf-poll-receipt.json	.2f	steps('bcrf', 'dut-set..first-locked-poll')[0]['after_set_s'][1]
3182	two	r2/baaf-poll-receipt.json	w	len(steps('baaf', 'dut-set..first-locked-poll'))
3182	2.08	r2/baaf-poll-receipt.json	.2f	steps('baaf', 'dut-set..first-locked-poll')[0]['after_set_s'][0]
3182	2.65	r2/baaf-poll-receipt.json	.2f	steps('baaf', 'dut-set..first-locked-poll')[0]['after_set_s'][1]
3182	5.10	r2/baaf-poll-receipt.json	.2f	steps('baaf', 'dut-set..first-locked-poll')[1]['after_set_s'][0]
3182	5.68	r2/baaf-poll-receipt.json	.2f	steps('baaf', 'dut-set..first-locked-poll')[1]['after_set_s'][1]
3186	12	r2/bcrf-poll-receipt.json	d	same(load(f'r2/{r}-poll-receipt.json')['spans']['restored..poll-end']['polls'] for r in ('bcrf', 'baaf'))
3186	2.0	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	rx(FIND_P, r'The listener ring slipped one frame ([\d.]+) to ([\d.]+) s after the servo first read LOCKED')
3186	3.0	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	rx(FIND_P, r'The listener ring slipped one frame ([\d.]+) to ([\d.]+) s after the servo first read LOCKED', group=2)
3190	0		d	same([counters('restore/counters-startc.jsonl', 'dut', 6, 0)[2], counters('restore/counters-startc.jsonl', 'dut', 6, 1)[2]])
3191	4		d	same([counters('restore/counters-endc.jsonl', 'dut', 6, 0)[2], counters('restore/counters-endc.jsonl', 'dut', 6, 1)[2], sum(len(ev(r, 'set-clock', who='dut')) for r in ('bcrf', 'baaf'))])
3191	one		s	rx('repo:docs/design/MEDIA_CLOCK_FOLLOWING.md', r'\| (One) MEDIA_RESET per switch on the DUT.s talker \(Milan v1\.2 Table 5\.4\)').lower()
3193	one	runs/bcrf/events.jsonl	w	same(mdiff(r, 'window-mark-0', 'after-peer-set', 'peer-0x0005-0', 4) for r in ('bcrf', 'baaf'))
3193	5	runs/bcrf/events.jsonl	d	same(q(E(r, 'mark', tag='after-peer-set')['t'] - E(r, 'set-clock', tag='peer-internal')['t'], 0) for r in ('bcrf', 'baaf'))
3194	20	runs/bcrf/events.jsonl	d	same(q(E(r, 'mark', tag='window-mark-0')['t'] - E(r, 'set-clock', who='dut', tag=r)['t'], 0) for r in ('bcrf', 'baaf'))
3195	one	runs/bcrf/events.jsonl	w	same(mdiff(r, 'after-restore', 'after-captures', 'peer-0x0005-0', 4) for r in ('bcrf', 'baaf'))
3197	once	runs/bcrf/events.jsonl	x	same(mdiff(r, 'window-mark-0', 'after-peer-set', 'dut-0x0024-0', i) for r in ('bcrf', 'baaf') for i in (0, 1))
3199	once	runs/bcrf/events.jsonl	x	same(mdiff(r, 'after-restore', 'after-captures', 'peer-0x0024-0', i) for r in ('bcrf', 'baaf') for i in (0, 1))
# B16c: attribution
3206	-123.98/-123.97	summary/bcrf/a-peer-tap.json	s	fmt(pt('bcrf', 'a', 0, 997)['median']['thdn_db'], '.2f') + '/' + fmt(pt('bcrf', 'a', 1, 9973)['median']['thdn_db'], '.2f')
3206	-123.98/-123.98	summary/baaf/a-peer-tap.json	s	fmt(pt('baaf', 'a', 0, 997)['median']['thdn_db'], '.2f') + '/' + fmt(pt('baaf', 'a', 1, 9973)['median']['thdn_db'], '.2f')
3206	-123.93	summary/bcrf/a-peer-tap.json	.2f	same(q(pt(r, 'a', c, t)['worst_thdn_db'], 2) for r in ('bcrf', 'baaf') for c, t in ((0, 997), (1, 9973)))
3207	0	summary/bcrf/a-peer-tap.json	d	same(load(f'summary/{r}/{p}.json')['info']['seq_gaps'] for r in ('bcrf', 'baaf') for p in ('a-peer-tap', 'b-dut-tap'))
3208	34.2	summary/bcrf/align-a-c.json	.1f	min([align(r, p)['compared_equal'] / 48000 for r in ('bcrf', 'baaf') for p in 'ab'])
3208	34.3	summary/bcrf/align-a-c.json	.1f	max([align(r, p)['compared_equal'] / 48000 for r in ('bcrf', 'baaf') for p in 'ab'])
3208	300	summary/bcrf/c-b9-grade.json	.0f	same(grade(r)['seconds'] for r in ('bcrf', 'baaf'))
3208	0.000001	summary/bcrf/c-b9-grade.json	.6f	bound(max(abs(grade(r)['phase_net_frames']) for r in ('bcrf', 'baaf')), '0.000001')
3209	0	summary/bcrf/d-loop-decode.json	d#0	same(len(dec(r)['events']) for r in ('bcrf', 'baaf'))
3209	0	summary/bcrf/d-loop-decode.json	d#1	same(dec(r)['net_step_frames'] for r in ('bcrf', 'baaf'))
3209	14.58	summary/bcrf/d-loop-decode.json	.2f	min(x['decoded'] for x in [dec(r) for r in ('bcrf', 'baaf')]) / Decimal(10 ** 6)
3209	303	summary/bcrf/d-extcap-pair.json	d	same(n for r in ('bcrf', 'baaf') for t in (load(f'summary/{r}/d-extcap-pair.json')['rows'][0]['tone_997'], load(f'summary/{r}/d-extcap-pair.json')['rows'][1]['tone_9973']) for n in (len(floor_inside(t)), len(inside(t['per_block']))))
3212	3,289,015	summary/bcrf/align-a-c.json	,d	sum(align(r, 'a')['compared_equal'] for r in ('bcrf', 'baaf'))
3212	3,290,863	summary/bcrf/align-b-c.json	,d	sum(align(r, 'b')['compared_equal'] for r in ('bcrf', 'baaf'))
3214	34	summary/bcrf/align-a-c.json	d	same(q(x, 0) for x in [align(r, p)['compared_equal'] / 48000 for r in ('bcrf', 'baaf') for p in 'ab'])
3218	131	r2/b0-2-receipt.json	d	d['degraded']
3218	300	r2/b0-2-receipt.json	d	d['blocks']
3218	34.1	r2/b0-2-receipt.json	.1f	d['overlap']['seconds']
3219	23	r2/b0-2-receipt.json	d	d['overlap']['degraded_inside']
3220	39	r2/b0-2-receipt.json	d	same(d['tones'][t]['a_blocks'] for t in ('997 Hz', '9,973 Hz'))
3220	-102.6	r2/b0-2-receipt.json	.1f	d['tones']['997 Hz']['a_worst_db']
3220	-82.6	r2/b0-2-receipt.json	.1f	d['tones']['9,973 Hz']['a_worst_db']
3220	108	r2/b0-2-receipt.json	d	d['overlap']['degraded_beyond']
3223	618	r2/source-receipt.json	d	get(d, 'compare.2.both')
3224	668	r2/source-receipt.json	d	get(d, 'compare.3.both')
3225	One	summary/b0-2/c-b9-grade.json	W	same([sum(1 for r in ('b0', 'b0-2') if (ROOT / f'summary/{r}/c-b9-grade.json').exists()), sum(1 for r in RUNS if r == 'bcrf'), sum(1 for r in RUNS if r == 'baaf')])
# B16c: the tone source, read only
3231	d9684a8f...		s	rx('runs/b16c-tone-start.txt', r'LOOP_SHA256 ([0-9a-f]{8})') + '...'
3231	07:49:29		cest	stamps('runs/b16c-tone-start.txt', 'STATUS')[0] - Decimal(rx('runs/b16c-tone-start.txt', r'hw_ptr : (\d+)')) / 48000
3231	08:03:52		cest	stamps('runs/b16c-tone-stop.txt', 'LOCK')[0]
3232	07:48	r2/source-receipt.json	hm	Decimal(clock(get(d, 'reads.b16c-state-1.at')))
3232	08:03	r2/source-receipt.json	hm	Decimal(clock(get(d, 'reads.b16c-state-2.at')))
3233	07:49	r2/source-receipt.json	hm	Decimal(clock(get(d, 'reads.b16c-meters-1.at')))
3233	08:03	r2/source-receipt.json	hm	Decimal(clock(get(d, 'reads.b16c-meters-2.at')))
3234	-38.5	r2/source-receipt.json	.1f	meter(('b16c-meters-1', 'b16c-meters-2', 'b16c-state-2'), 'the documented pair of outputs', 'leaving_dbfs')
3234	-14.0	r2/source-receipt.json	.1f	meter(('b16c-meters-1', 'b16c-meters-2', 'b16c-state-2'), 'the second pair of outputs', 'leaving_dbfs')
3237	618	r2/source-receipt.json	d	get(d, 'compare.2.both') if get(d, 'compare.2.differ') == 0 else None
3238	two	r2/source-receipt.json	w#0	sum(1 for k, r in d['reads'].items() if k.startswith('b16c-') and r['kind'] == 'state')
3238	two	r2/source-receipt.json	w#1	get(d, 'compare.3')['differ']
3238	668	r2/source-receipt.json	d	get(d, 'compare.3')['both']
3240	two	r2/source-receipt.json	w	same(x['messages'][0] for x in get(d, 'compare.3')['differing'])
3240	one	r2/source-receipt.json	w	same(x['messages'][1] for x in get(d, 'compare.3')['differing'] if x['second_last_among_first'] and x['all_minus_infinity'])
3246	0.2	runs/bcrf/events.jsonl	.1f	same(q((E(r, 'tone-summary')['last_raw_ns'] - E(r, 'tone-summary')['first_raw_ns']) / Decimal(10 ** 9) / (E(r, 'tone-summary')['reads'] - 1), 1) for r in ('bcrf', 'baaf'))
3247	1,805	runs/bcrf/events.jsonl	,d	E('bcrf', 'tone-summary')['states']['RUNNING'] if E('bcrf', 'tone-summary')['states'] == {'RUNNING': E('bcrf', 'tone-summary')['reads']} else None
3247	1,803	runs/baaf/events.jsonl	,d	E('baaf', 'tone-summary')['states']['RUNNING'] if E('baaf', 'tone-summary')['states'] == {'RUNNING': E('baaf', 'tone-summary')['reads']} else None
3247	one	runs/bcrf/events.jsonl	w	same(E(r, 'tone-summary')['trigger_times'] for r in ('bcrf', 'baaf'))
# B16c: bench as left
3256	0205022001006000		s	cen('restore/census-endc.jsonl', 'format-dut-5-0')['payload'][8:]
3256	041060010000bb80		s	cen('restore/census-endc.jsonl', 'format-dut-5-1')['payload'][8:]
3256	0		d#1	payload_word(cen('restore/census-endc.jsonl', 'clock', 'dut'), 8)
3257	1		d#1	payload_word(cen('restore/census-endc.jsonl', 'clock', 'peer'), 8)
3257	0	runs/bcrf/events.jsonl	d#2	same(E(r, 'set-clock', tag='peer-internal')['readback'] for r in ('bcrf', 'baaf'))
3257	1	runs/bcrf/events.jsonl	d#2	same(E(r, 'set-clock', who='peer', tag='restore')['readback'] for r in ('bcrf', 'baaf'))
3257	once	runs/bcrf/events.jsonl	x	same(len(ev(r, 'set-clock', tag='peer-internal')) for r in ('bcrf', 'baaf'))
3258	45		s	rx('restore/census-compare-b16c.txt', r'"same": (\d+)')
3258	46		s	rx('restore/census-compare-b16c.txt', r'"compared": (\d+)')
3260	286		d	nvm('restore/dut-startc.txt')['seq']
3260	292		d	nvm('restore/dut-endc.txt')['seq']
3260	52		d	nvm('restore/dut-startc.txt')['commits']
3260	58		d	nvm('restore/dut-endc.txt')['commits']
3260	0		d	nvm('restore/dut-endc.txt')['pend']
3261	08:03:52		cest	stamps('runs/b16c-tone-stop.txt', 'LOCK')[0]
3270	two		w	same([cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 6, 0, 0), cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 6, 0, 1), cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 6, 2, 0), cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 6, 2, 1)])
3270	one		w	same([cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 6, 0, 0), cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 6, 0, 1), cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 6, 2, 0), cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 6, 2, 1)]) // sum(1 for r in RUNS if r in ('bcrf', 'baaf'))
3271	four		w	same([cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 5, 0, 4), cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 5, 8, 4)])
3272	0		d	same([counters('restore/counters-startc.jsonl', 'dut', 6, 0)[2], counters('restore/counters-startc.jsonl', 'dut', 6, 1)[2]])
3272	4		d	same([counters('restore/counters-endc.jsonl', 'dut', 6, 0)[2], counters('restore/counters-endc.jsonl', 'dut', 6, 1)[2]])
3274	22		d	counters('restore/counters-startc.jsonl', 'dut', 36, 0)[0]
3274	21		d	counters('restore/counters-startc.jsonl', 'dut', 36, 0)[1]
3274	24		d	counters('restore/counters-endc.jsonl', 'dut', 36, 0)[0]
3274	23		d	counters('restore/counters-endc.jsonl', 'dut', 36, 0)[1]
3275	6		d	counters('restore/counters-startc.jsonl', 'peer', 36, 0)[0]
3275	5		d	counters('restore/counters-startc.jsonl', 'peer', 36, 0)[1]
3275	8		d	counters('restore/counters-endc.jsonl', 'peer', 36, 0)[0]
3275	7		d	counters('restore/counters-endc.jsonl', 'peer', 36, 0)[1]
3276	162		d	slipb('restore/dut-startc.txt')
3276	188		d	slipb('restore/dut-endc.txt')
# B16c: #629 acceptance
3283	four	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	w	len(re.split(r', and |, ', b6_rule()))
3283	three	summary/bcrf/c-b9-grade.json	w	same([terms('bcrf'), terms('baaf')])
# B16c: limits
3295	One	summary/bcrf/c-b9-grade.json	W	same([sum(1 for r in ('b0', 'b0-2') if (ROOT / f'summary/{r}/c-b9-grade.json').exists()), sum(1 for r in RUNS if r == 'bcrf'), sum(1 for r in RUNS if r == 'baaf')])
3295	300	summary/bcrf/c-b9-grade.json	.0f	same(grade(r)['seconds'] for r in ('bcrf', 'baaf'))
3296	40	summary/bcrf/a-peer-tap.json	d	same(q(load(f'summary/{r}/{p}.json')['seconds'], 0) for r in ('bcrf', 'baaf') for p in ('a-peer-tap', 'b-dut-tap'))
3296	630	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	rx(FIND_P, r'^(\d+) s, untouched, from (\d+) s after the last bind or clock-source set')
3296	one	runs/bcrf-lock.txt	w	same(len(stamps(f'runs/{r}-lock.txt', 'LOCK')) for r in ('bcrf', 'baaf'))
3302	+10.59	r2/bcrf-poll-receipt.json	+.2f	min(rates())
3302	+10.65	r2/bcrf-poll-receipt.json	+.2f	max(rates())
3303	4	r2/bcrf-poll-trace.tsv	d	same(b for r in ('bcrf', 'baaf') for x in trace(r) if trace_state(x) in (3, 4) for b in [4 * ((int(x['0x8f8'], 16) >> 4) & 1)])
3309	108	r2/b0-2-receipt.json	d	d['overlap']['degraded_beyond']
3309	131	r2/b0-2-receipt.json	d	d['degraded']
3308	one	summary/b0-2/c-b9-grade.json	w	same([sum(1 for r in ('b0', 'b0-2') if (ROOT / f'summary/{r}/c-b9-grade.json').exists()), sum(1 for r in RUNS if r == 'bcrf'), sum(1 for r in RUNS if r == 'baaf')])
# B16, round 2: reduced receipts
3371	2026-10-12	git:35e332b6	date	commit_time('35e332b6')
3377	-123.98	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'\| (-[\d.]+) dB on both tones, `pts3` and `b0-2` \|')
3377	-123.98	r2/b0-2-receipt.json	.2f	d['tones']['997 Hz']['floor_median_db']
3377	-123.95	r2/b0-2-receipt.json	.2f	d['tones']['9,973 Hz']['floor_median_db']
3377	-123.98		.2f	same(load('summary/pts3/c-b9-grade.json')['summary'][c + '_floor']['thdn_db_median'] for c in ('ch0', 'ch1'))
3378	0	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'runs of blocks: (\d+) to (\d+), (\d+) to (\d+), (\d+) to (\d+) and later runs', 1)
3378	18	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'runs of blocks: (\d+) to (\d+), (\d+) to (\d+), (\d+) to (\d+) and later runs', 2)
3378	28	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'runs of blocks: (\d+) to (\d+), (\d+) to (\d+), (\d+) to (\d+) and later runs', 3)
3378	31	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'runs of blocks: (\d+) to (\d+), (\d+) to (\d+), (\d+) to (\d+) and later runs', 4)
3378	43	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'runs of blocks: (\d+) to (\d+), (\d+) to (\d+), (\d+) to (\d+) and later runs', 5)
3378	54	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'runs of blocks: (\d+) to (\d+), (\d+) to (\d+), (\d+) to (\d+) and later runs', 6)
3378	0	r2/b0-2-receipt.json	d	d['degraded_runs'][0][0]
3378	18	r2/b0-2-receipt.json	d	d['degraded_runs'][0][1]
3378	28	r2/b0-2-receipt.json	d	d['degraded_runs'][1][0]
3378	31	r2/b0-2-receipt.json	d	d['degraded_runs'][1][1]
3378	43	r2/b0-2-receipt.json	d	d['degraded_runs'][2][0]
3378	44	r2/b0-2-receipt.json	d	d['degraded_runs'][2][1]
3378	46	r2/b0-2-receipt.json	d	d['degraded_runs'][3][0]
3378	54	r2/b0-2-receipt.json	d	d['degraded_runs'][3][1]
3378	eleven	r2/b0-2-receipt.json	w	len(d['degraded_runs']) - 4
3378	45	r2/b0-2-receipt.json	d	next(i for i in range(d['degraded_runs'][2][1] + 1, d['degraded_runs'][3][0]))
3379	06:38:03	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'McASP0 300 s from ([\d:]+) while playing the loop')
3379	24	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'It starts (\d+) s after the last bind')
3379	06:38:05.2	runs/b0-2/events.jsonl	cest1	E('b0-2', 'captures-started')['started']['mcasp'] + r2lead()
3379	26	r2/b0-2-receipt.json	.0f	d['timing']['recording_after_binds_s']
3379	06:38:03.2	runs/b0-2/events.jsonl	cest1	E('b0-2', 'captures-started')['started']['mcasp']
3379	2	tools/run_b16.py	d	r2lead()
3380	06:28:25	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'\| As `pts1`, from ([\d:]+)\. McASP0 also plays')
3380	06:28:31.5	runs/pts2/events.jsonl	cest1	E('pts2', 'captures-started')['started']['mcasp'] + r2lead()
3380	2	tools/run_b16.py	d	r2lead()
3381	Three	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'the tone path\. All (\w+) are met here\.').capitalize()
3381	four	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	w	len(re.split(r', and |, ', b6_rule()))
3381	three	summary/bcrf/c-b9-grade.json	w	same([terms('bcrf'), terms('baaf')])
3382	131	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'There its talker stream already held (\d+) blocks off the floor')
3382	131	r2/b0-2-receipt.json	d	d['degraded']
3382	23	r2/b0-2-receipt.json	d	d['overlap']['degraded_inside']
3382	34.1	r2/b0-2-receipt.json	.1f	d['overlap']['seconds']
3382	108	r2/b0-2-receipt.json	d	d['overlap']['degraded_beyond']
3383	20	runs/bcrf/events.jsonl	d	same(q(E(r, 'mark', tag='window-mark-0')['t'] - E(r, 'set-clock', who='dut', tag=r)['t'], 0) for r in ('bcrf', 'baaf'))
3383	6	runs/bcrf/events.jsonl	d	same(q(E(r, 'captures-started')['started']['mcasp'] + r2lead() - E(r, 'mark', tag='window-mark-0')['t'], 0) for r in ('bcrf', 'baaf'))
3384	Four	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'1,255 both hold, (\w+) differ').capitalize()
3384	Two	r2/source-receipt.json	W	sum(1 for x in get(d, 'compare.1')['differing'] if x['cls'] != 'an input of a monitoring mix')
3384	two	r2/source-receipt.json	w	sum(1 for x in get(d, 'compare.1')['differing'] if x['cls'] == 'an input of a monitoring mix')
3385	-135.2	r2/source-receipt.json	.1f	max(get(d, 'reads.' + k + '.meters.every other output.largest_before_setting_dbfs') for k in ('b16-state-1', 'b16-meters-1', 'b16-meters-2', 'b16-state-2'))
3386	2.66	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'- B-CRF: one step, ([\d.]+) s after the set;')
3386	2.65	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'- B-AAF: two steps, ([\d.]+) s and ([\d.]+) s after the set\.')
3386	5.68	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'- B-AAF: two steps, ([\d.]+) s and ([\d.]+) s after the set\.', 2)
3386	two	r2/bcrf-poll-receipt.json	w	same(len(x['polls']) for x in [x for r in ('bcrf', 'baaf') for x in load(f'r2/{r}-poll-receipt.json')['slip_lb_steps']])
3386	2.08	r2/bcrf-poll-receipt.json	.2f	steps('bcrf', 'dut-set..first-locked-poll')[0]['after_set_s'][0]
3386	2.66	r2/bcrf-poll-receipt.json	.2f	steps('bcrf', 'dut-set..first-locked-poll')[0]['after_set_s'][1]
3386	2.08	r2/baaf-poll-receipt.json	.2f	steps('baaf', 'dut-set..first-locked-poll')[0]['after_set_s'][0]
3386	2.65	r2/baaf-poll-receipt.json	.2f	steps('baaf', 'dut-set..first-locked-poll')[0]['after_set_s'][1]
3386	5.10	r2/baaf-poll-receipt.json	.2f	steps('baaf', 'dut-set..first-locked-poll')[1]['after_set_s'][0]
3386	5.68	r2/baaf-poll-receipt.json	.2f	steps('baaf', 'dut-set..first-locked-poll')[1]['after_set_s'][1]
3398	two	r2/bcrf-poll-receipt.json	w	same(len(x['polls']) for x in [x for r in ('bcrf', 'baaf') for x in load(f'r2/{r}-poll-receipt.json')['slip_lb_steps']])
3399	eight	r2/bcrf-poll-trace.tsv	w	same(len([k for k in trace(r)[0] if k.startswith('0x')]) for r in ('bcrf', 'baaf'))
3401	2.657	r2/bcrf-poll-receipt.json	.3f	same([d['locked']['recomputed_s'][0], d['locked']['published'][0], E('bcrf', 'servo-state')['s_lo']])
3401	3.161	r2/bcrf-poll-receipt.json	.3f	same([d['locked']['recomputed_s'][1], d['locked']['published'][1], E('bcrf', 'servo-state')['s_hi']])
3401	6.68		.2f	same([load('r2/baaf-poll-receipt.json')['locked']['recomputed_s'][0], E('baaf', 'servo-state')['s_lo']])
3402	7.18		.2f	same([load('r2/baaf-poll-receipt.json')['locked']['recomputed_s'][1], E('baaf', 'servo-state')['s_hi']])
3404	2.585	r2/bcrf-poll-trace.tsv	.3f	lock_bracket('bcrf')[0]
3404	6.602	r2/baaf-poll-trace.tsv	.3f	lock_bracket('baaf')[0]
3406	twelve	r2/source-receipt.json	w	len(d['reads'])
3407	four	r2/source-receipt.json	w	same(sum(1 for k in d['reads'] if k.split('-')[0] == lane) for lane in ('b16', 'b16b', 'b16c'))
3420	6	controls/r2-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3420	6	controls/r2-controls.json	d#1	len(d['controls'])
3432	twelve	r2/source-receipt.json	w	len(d['reads'])
3436	twelve	RAW-ARTIFACTS.json	w	sum(1 for x in d['files'] if x['path'].startswith('source/'))
3455	two	RAW-ARTIFACTS.json	w	sum(1 for x in d['files'] if x['path'].endswith('/poll-run.jsonl'))
3456	9cfc79bb...	RAW-ARTIFACTS.json	s	same([raw('bcrf/poll-run.jsonl')['sha256'], load('r2/bcrf-poll-receipt.json')['raw']['sha256']])[:8] + '...'
3456	476a0077...	RAW-ARTIFACTS.json	s	same([raw('baaf/poll-run.jsonl')['sha256'], load('r2/baaf-poll-receipt.json')['raw']['sha256']])[:8] + '...'
3472	6	controls/r2-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3472	6	controls/r2-controls.json	d#1	len(d['controls'])
3346	8	controls/b16c-dryrun-summary.json	d#0	sum(v == 'PASS' for v in d['scenarios'].values())
3346	8	controls/b16c-dryrun-summary.json	d#1	len(d['scenarios'])
2637	2	runs/b0/events.jsonl	d#0	int(E('b0', 'bind', listener='dut-in-1')['talker'].split('-')[-1])
2637	1	runs/b0/events.jsonl	d#0	int(E('b0', 'bind', talker='peer-out-2')['listener'].split('-')[-1])
2777	1	runs/b0-2/events.jsonl	d#0	same(int(E(r, 'bind', talker='peer-out-2')['listener'].split('-')[-1]) for r in ('b0', 'b0-2'))
2777	0	runs/b0-2/events.jsonl	d#0	same(int(E(r, 'bind', talker='peer-out-0')['listener'].split('-')[-1]) for r in ('b0', 'b0-2'))
2855	0		d#1	cen('restore/census-endb.jsonl', 'rx-state-peer-0')['talker_uid'] if cen('restore/census-endb.jsonl', 'rx-state-peer-0')['talker'] == '020000fffe000001' else None
2855	1		d#0	cen('restore/census-endb.jsonl', 'rx-state-peer-8')['talker_uid'] if cen('restore/census-endb.jsonl', 'rx-state-peer-8')['talker'] == '020000fffe000001' else None
3257	0		d#1	cen('restore/census-endc.jsonl', 'rx-state-peer-0')['talker_uid'] if cen('restore/census-endc.jsonl', 'rx-state-peer-0')['talker'] == '020000fffe000001' else None
3257	1		d#0	cen('restore/census-endc.jsonl', 'rx-state-peer-8')['talker_uid'] if cen('restore/census-endc.jsonl', 'rx-state-peer-8')['talker'] == '020000fffe000001' else None
2991	1	runs/bcrf/events.jsonl	d#0	same(E(r, 'fol-check')['peer_in_8']['talker_uid'] for r in ('bcrf', 'baaf'))
2996	1	runs/bcrf/events.jsonl	d#0	same(int(E(r, 'bind', talker='peer-out-2')['listener'].split('-')[-1]) for r in ('bcrf', 'baaf'))
2997	0	runs/bcrf/events.jsonl	d#0	same(int(E(r, 'bind', talker='peer-out-0')['listener'].split('-')[-1]) for r in ('bcrf', 'baaf'))
3494	122.475	summary/pts3/a-peer-tap.json	s	T(d, 1, 'snr_db')
3494	122.48	summary/pts3/a-peer-tap.json	.2f	T(d, 1, 'snr_db')
3495	06:22:34.993	identity-b16b/lock-window.txt	cest3	stamps(p, 'UNLOCK')[0]
3496	06:22:34	identity-b16b/lock-window.txt	cest	stamps(p, 'UNLOCK')[0]
3511	5	controls/r3-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3511	5	controls/r3-controls.json	d#1	len(d['controls'])
3552	two	RAW-ARTIFACTS.json	w	same([sum(1 for x in d['files'] if x['path'].startswith('playback/')), sum(1 for v in load('r3/playback-logs.json')['logs'].values() if 'sha256' in v)])
3560	06:02:00	r3/playback-logs.json	s	d['logs']['b16']['modified']
3560	0	r3/playback-logs.json	d#0	d['logs']['b16']['underrun_lines']
3560	dab353b5ead02cb68b5ecebc757786c48b7672e6f93a37a152e37aedf9dfe43b	RAW-ARTIFACTS.json	s	same([raw('playback/b16-tone-play.log')['sha256'], load('r3/playback-logs.json')['logs']['b16']['sha256']])
3561	08:03:53	r3/playback-logs.json	s	d['logs']['b16c']['modified']
3561	0	r3/playback-logs.json	d#0	d['logs']['b16c']['underrun_lines']
3561	dab353b5ead02cb68b5ecebc757786c48b7672e6f93a37a152e37aedf9dfe43b	RAW-ARTIFACTS.json	s	same([raw('playback/b16c-tone-play.log')['sha256'], load('r3/playback-logs.json')['logs']['b16c']['sha256']])
3563	two	RAW-ARTIFACTS.json	w	len({x['sha256'] for x in d['files'] if x['path'].startswith('playback/')}) == 1 and sum(1 for x in d['files'] if x['path'].startswith('playback/'))
3521	-123.98		s	was('\\(a\\) at (-[\\d.]+) dB median, worst block (-[\\d.]+) dB, on both tones in both cases', 1, at='35e332b6')
3521	-123.93		s	was('\\(a\\) at (-[\\d.]+) dB median, worst block (-[\\d.]+) dB, on both tones in both cases', 2, at='35e332b6')
3521	-123.98/-123.97	summary/bcrf/a-peer-tap.json	s	fmt(pt('bcrf', 'a', 0, 997)['median']['thdn_db'], '.2f') + '/' + fmt(pt('bcrf', 'a', 1, 9973)['median']['thdn_db'], '.2f')
3521	-123.98/-123.98	summary/baaf/a-peer-tap.json	s	fmt(pt('baaf', 'a', 0, 997)['median']['thdn_db'], '.2f') + '/' + fmt(pt('baaf', 'a', 1, 9973)['median']['thdn_db'], '.2f')
3521	-123.93	summary/bcrf/a-peer-tap.json	.2f	same(q(pt(r, 'a', c, t)['worst_thdn_db'], 2) for r in ('bcrf', 'baaf') for c, t in ((0, 997), (1, 9973)))
3522	305		s	was('at the floor in (\\d+) of (\\d+) blocks; block 2', 1, at='35e332b6')
3522	306		s	was('at the floor in (\\d+) of (\\d+) blocks; block 2', 2, at='35e332b6')
3522	13		s	was("the loop's floor, in (\\d+) of (\\d+) blocks\\.", 1, at='35e332b6')
3522	16		s	was("the loop's floor, in (\\d+) of (\\d+) blocks\\.", 2, at='35e332b6')
3522	303	summary/b0-2/d-extcap-pair.json	d	same(n for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']) for n in (len(floor_inside(t)), len(inside(t['per_block']))))
3522	11	summary/pts2/d-extcap-pair.json	d	same(len(floor_inside(t)) for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
3522	13	summary/pts2/d-extcap-pair.json	d#1	same(len(inside(t['per_block'])) for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
3522	6	summary/pts2/d-extcap-pair.json	d#0	same([i for i in inside(t['per_block']) if i not in floor_inside(t)][0] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
3522	12	summary/pts2/d-extcap-pair.json	d#0	same([i for i in inside(t['per_block']) if i not in floor_inside(t)][1] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
3522	0	summary/b0-2/d-extcap-pair.json	d#0	same(silent(t['per_block'])[0] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
3522	1	summary/b0-2/d-extcap-pair.json	d#0	same(silent(t['per_block'])[-1] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
3522	2	summary/b0-2/d-extcap-pair.json	d#0	same(inside(t['per_block'])[0] - 1 for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
3523	15	summary/pts2/ctl-dut-talker-dut-tap.json	d	same(n for x in taps2() for n in (len(floor_inside(x)), len(inside(x['per_block']))))
3524	2.66		s	was('\\| B-CRF \\| ([\\d.]+) to ([\\d.]+) s; ACQUIRE', 1, at='35e332b6')
3524	3.16		s	was('\\| B-CRF \\| ([\\d.]+) to ([\\d.]+) s; ACQUIRE', 2, at='35e332b6')
3524	6.68		s	was('\\| B-AAF \\| ([\\d.]+) to ([\\d.]+) s; ACQUIRE', 1, at='35e332b6')
3524	7.18		s	was('\\| B-AAF \\| ([\\d.]+) to ([\\d.]+) s; ACQUIRE', 2, at='35e332b6')
3524	2.585	r2/bcrf-poll-trace.tsv	.3f	lock_bracket('bcrf')[0]
3524	3.161	r2/bcrf-poll-receipt.json	.3f	lock_bracket('bcrf')[1]
3524	6.602	r2/baaf-poll-trace.tsv	.3f	lock_bracket('baaf')[0]
3524	7.180	r2/baaf-poll-receipt.json	.3f	lock_bracket('baaf')[1]
3525	Two		s	was('So (\\w+) settings changed: the clock setting', 1, at='35e332b6').capitalize()
3525	1,255	r2/source-receipt.json	,d	get(d, 'compare.1')['both']
3525	618	r2/source-receipt.json	d	get(d, 'compare.2.both')
3525	668	r2/source-receipt.json	d	get(d, 'compare.3.both')
3526	five	r2/bcrf-poll-receipt.json	w	same([len(steps('bcrf', 'binds..dut-set')), len(steps('baaf', 'binds..dut-set'))])
3526	one	runs/b0-2/dut-after-captures.txt	w	same((slipb(f'runs/{r}/dut-after-captures.txt') - slipb(f'runs/{r}/dut-before-binds.txt')) // 2 for r in ('b0', 'b0-2'))
3526	two		s#0	was('the ring absorbed the difference between the (\\w+) clocks', 1, at='35e332b6')
3527	4	r2/bcrf-poll-trace.tsv	d	same(b for r in ('bcrf', 'baaf') for x in trace(r) if trace_state(x) in (3, 4) for b in [4 * ((int(x['0x8f8'], 16) >> 4) & 1)])
3533	05:45:07		s	was('\\| Identity gate \\| PASS, ([\\d:]+) to ([\\d:]+) CEST \\|', 1, at='35e332b6')
3533	05:45:13		s	was('\\| Identity gate \\| PASS, ([\\d:]+) to ([\\d:]+) CEST \\|', 2, at='35e332b6')
3533	05:45:06	identity/lock-window.txt	cest	stamps(p, 'LOCK')[0]
3533	05:45:12	identity/lock-window.txt	cest	stamps(p, 'UNLOCK')[0]
3534	05:55:38		s	was('inputs through the authorised tone source, from ([\\d:]+) to ([\\d:]+) CEST', 1, at='35e332b6')
3534	06:02:00		s	was('inputs through the authorised tone source, from ([\\d:]+) to ([\\d:]+) CEST', 2, at='35e332b6')
3534	05:55:37	runs/tone-start.txt	cest	stamps(p, 'STATUS')[0] - Decimal(rx(p, r'hw_ptr : (\d+)')) / 48000
3534	06:01:59	runs/tone-stop.txt	cest	stamps(p, 'LOCK')[0]
3535	05:56:31		s	was('\\| `loop1` \\| ([\\d:]+) to ([\\d:]+) \\|', 1, at='35e332b6')
3535	05:57:31		s	was('\\| `loop1` \\| ([\\d:]+) to ([\\d:]+) \\|', 2, at='35e332b6')
3535	06:00:29		s	was('\\| `loop2` \\| [\\d:]+ to ([\\d:]+) \\|', 1, at='35e332b6')
3535	05:56:30	runs/loop1-lock.txt	cest	stamps(p, 'LOCK')[0]
3535	05:57:30	runs/loop1-lock.txt	cest	stamps(p, 'UNLOCK')[0]
3535	06:00:28	runs/loop2-lock.txt	cest	stamps(p, 'UNLOCK')[0]
3536	49		s	was('in the remaining (\\d+) s of the capture', 1, at='35e332b6')
3536	49.6	summary/loop2/acmp-peer-tap.json	.1f	E('loop2', 'capture-done', what='tap')['seconds'] - acmp('CONNECT_TX_COMMAND', 1)
3537	0x0002		s	was('same: rx state flags `(0x[0-9a-f]+)`, stream ID (\\d+),', 1, at='35e332b6')
3537	0		s#0	was('same: rx state flags `(0x[0-9a-f]+)`, stream ID (\\d+),', 2, at='35e332b6')
3537	0	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s#1	rx(FIND_P, r'nothing\. Its counters stayed (\d+) and its digital output read exact zero')
3538	05:48		s	was('at ([\\d:]+) and ([\\d:]+) CEST\\. The two reads are identical', 1, at='35e332b6')
3538	06:01		s#0	was('at ([\\d:]+) and ([\\d:]+) CEST\\. The two reads are identical', 2, at='35e332b6')
3538	05:47	r2/source-receipt.json	hm	Decimal(clock(get(d, 'reads.b16-state-1.at')))
3538	06:01	r2/source-receipt.json	hm#1	Decimal(clock(get(d, 'reads.b16-state-2.at')))
3539	06:20		s	was('resumed at ([\\d:]+) CEST on the same image, branch', 1, at='35e332b6')
3539	06:22:23	soc/b16b-precheck-status.log	cest	stamps(p, 'LOCK')[0]
3540	-14.14		s	was('at (-[\\d.]+) dBFS before ([\\d:]+) CEST and (-[\\d.]+) dBFS after', 1, at='35e332b6')
3540	06:29		s	was('at (-[\\d.]+) dBFS before ([\\d:]+) CEST and (-[\\d.]+) dBFS after', 2, at='35e332b6')
3540	-14.10		s	was('at (-[\\d.]+) dBFS before ([\\d:]+) CEST and (-[\\d.]+) dBFS after', 3, at='35e332b6')
3540	06:28:50	summary/pts2/a-peer-tap.json	cest	d['info']['last_t']
3540	06:31:51	summary/b0/a-peer-tap.json	cest	d['info']['first_t']
3541	+3.00		s	was('\\| (\\+[\\d.]+) frames in 10 s, smooth', 1, at='35e332b6')
3541	10	summary/pts1/c-b9-grade.json	.0f	same(grade(r)['seconds'] for r in ('pts1', 'pts2'))
3541	+3.00	summary/pts1/c-b9-grade.json	+.2f	d['phase_net_frames']
3541	+3.01	summary/pts2/c-b9-grade.json	+.2f	d['phase_net_frames']
3542	+6.95		s	was('The (\\+[\\d.]+) ppm tone advanced', 1, at='35e332b6')
3542	+6.94	summary/pts1/a-peer-tap.json	+.2f	min(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))
3542	+6.96	summary/pts1/a-peer-tap.json	+.2f	max(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))
3543	Five		s#0	was('records (\\w+) underruns, ([\\d.]+) to ([\\d.]+) s each', 1, at='35e332b6').capitalize()
3543	0.43		s	was('records (\\w+) underruns, ([\\d.]+) to ([\\d.]+) s each', 2, at='35e332b6')
3543	1.63		s	was('records (\\w+) underruns, ([\\d.]+) to ([\\d.]+) s each', 3, at='35e332b6')
3543	Five		s#1	rx('HANDOFF.md', r'^\| b17 \|.*?the log holds (\w+) underruns \(([\d:]+) to ([\d:]+), during offline grading\)').capitalize()
3543	06:45:27		s	rx('HANDOFF.md', r'^\| b17 \|.*?the log holds (\w+) underruns \(([\d:]+) to ([\d:]+), during offline grading\)', group=2)
3543	06:46:38		s	rx('HANDOFF.md', r'^\| b17 \|.*?the log holds (\w+) underruns \(([\d:]+) to ([\d:]+), during offline grading\)', group=3)
3544	07:32		s	was('resumed at ([\\d:]+) CEST on the same image and branch', 1, at='35e332b6')
3544	07:48:07	soc/b16c-precheck-status.log	cest	stamps(p, 'LOCK')[0]
3545	07:50:12.4		s	was('\\| `bcrf` \\| [\\d:]+ to [\\d:]+ \\| ([\\d:.]+) \\| ([\\d:.]+) \\| CLOCK_SOURCE 1, ([\\d:.]+) \\| ([\\d:]+) to ([\\d:]+), from 26 s after the set \\| [\\d:.]+ to ([\\d:.]+) \\|', 1, at='35e332b6')
3545	07:50:17.6		s	was('\\| `bcrf` \\| [\\d:]+ to [\\d:]+ \\| ([\\d:.]+) \\| ([\\d:.]+) \\| CLOCK_SOURCE 1, ([\\d:.]+) \\| ([\\d:]+) to ([\\d:]+), from 26 s after the set \\| [\\d:.]+ to ([\\d:.]+) \\|', 2, at='35e332b6')
3545	07:50:29.8		s	was('\\| `bcrf` \\| [\\d:]+ to [\\d:]+ \\| ([\\d:.]+) \\| ([\\d:.]+) \\| CLOCK_SOURCE 1, ([\\d:.]+) \\| ([\\d:]+) to ([\\d:]+), from 26 s after the set \\| [\\d:.]+ to ([\\d:.]+) \\|', 3, at='35e332b6')
3545	07:50:56		s	was('\\| `bcrf` \\| [\\d:]+ to [\\d:]+ \\| ([\\d:.]+) \\| ([\\d:.]+) \\| CLOCK_SOURCE 1, ([\\d:.]+) \\| ([\\d:]+) to ([\\d:]+), from 26 s after the set \\| [\\d:.]+ to ([\\d:.]+) \\|', 4, at='35e332b6')
3545	07:55:56		s	was('\\| `bcrf` \\| [\\d:]+ to [\\d:]+ \\| ([\\d:.]+) \\| ([\\d:.]+) \\| CLOCK_SOURCE 1, ([\\d:.]+) \\| ([\\d:]+) to ([\\d:]+), from 26 s after the set \\| [\\d:.]+ to ([\\d:.]+) \\|', 5, at='35e332b6')
3545	07:56:04.1		s	was('\\| `bcrf` \\| [\\d:]+ to [\\d:]+ \\| ([\\d:.]+) \\| ([\\d:.]+) \\| CLOCK_SOURCE 1, ([\\d:.]+) \\| ([\\d:]+) to ([\\d:]+), from 26 s after the set \\| [\\d:.]+ to ([\\d:.]+) \\|', 6, at='35e332b6')
3545	08:02:51.8		s	was('\\| `baaf` \\| [\\d:]+ to [\\d:]+ \\| [\\d:.]+ \\| [\\d:.]+ \\| CLOCK_SOURCE 2, [\\d:.]+ \\| [\\d:]+ to [\\d:]+, from 26 s after the set \\| ([\\d:.]+) to ([\\d:.]+) \\|', 1, at='35e332b6')
3545	08:02:55.8		s	was('\\| `baaf` \\| [\\d:]+ to [\\d:]+ \\| [\\d:.]+ \\| [\\d:.]+ \\| CLOCK_SOURCE 2, [\\d:.]+ \\| [\\d:]+ to [\\d:]+, from 26 s after the set \\| ([\\d:.]+) to ([\\d:.]+) \\|', 2, at='35e332b6')
3545	07:50:12.3	runs/bcrf/events.jsonl	cest1	E('bcrf', 'set-clock', tag='peer-internal')['t']
3545	07:50:17.5	runs/bcrf/events.jsonl	cest1	E('bcrf', 'bind', i=-1)['t']
3545	07:50:29.7	runs/bcrf/events.jsonl	cest1	E('bcrf', 'set-clock', tag='bcrf')['t']
3545	07:50:55	runs/bcrf/events.jsonl	cest	E('bcrf', 'captures-started')['started']['mcasp'] + r2lead()
3545	07:55:55	runs/bcrf/events.jsonl	cest	E('bcrf', 'captures-started')['started']['mcasp'] + r2lead() + grade('bcrf')['seconds']
3545	07:56:04.0	runs/bcrf/events.jsonl	cest1	E('bcrf', 'mark', tag='after-restore')['t']
3545	08:02:51.7	runs/baaf/events.jsonl	cest1	E('baaf', 'teardown')['t']
3545	08:02:55.7	runs/baaf/events.jsonl	cest1	E('baaf', 'mark', tag='after-restore')['t']
3546	303.8		s#0	was('over ([\\d.]+) s in each case\\. One frame', 1, at='35e332b6')
3546	303.8	summary/bcrf/d-loop-decode.json	.1f#1	d['decoded'] / 48000
3546	303.9	summary/baaf/d-loop-decode.json	.1f	d['decoded'] / 48000
3547	+10.6		s	was("through the DUT's meters, (\\+[\\d.]+) ppm against gPTP", 1, at='35e332b6')
3547	+10.59	r2/bcrf-poll-receipt.json	+.2f	min(rates())
3547	+10.65	r2/bcrf-poll-receipt.json	+.2f	max(rates())
3549	Six		W	sum(1 for x in ('plus one change', 'one PDU', 'one step earlier', 'one request', 'the two lanes', 'one route') if x in load('git:35e332b6:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md') and x not in re.sub(r'"[^"]*"', '', ' '.join(t for t, _ in scope().values())))
# the page's Contents entry for lane B16
78	three	summary/bcrf/c-b9-grade.json	w	same([terms('bcrf'), terms('baaf')])
78	four	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	w#1	len(re.split(r', and |, ', b6_rule()))
# the README row's lane B16 part
README.md:15	twice	summary/loop2/acmp-peer-tap.json	x	sum(x['msg'] == 'CONNECT_TX_COMMAND' for x in d['acmp'])
README.md:15	-14.1	summary/pts1/a-peer-tap.json	.1f	same(q(T(load(f'summary/{r}/a-peer-tap.json'), 0, 'level_dbfs'), 1) for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3'))
README.md:15	four	summary/pts1/align-a-c.json	w	sum(1 for r in RUNS if (ROOT / f'summary/{r}/align-a-c.json').exists() and r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') and align(r, 'a')['frames_differing'] == 0)
README.md:15	300	summary/b0-2/c-b9-grade.json	.0f#0	d['seconds']
README.md:15	-123.95	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch0_all']['thdn_db_median']
README.md:15	-122.80	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch1_all']['thdn_db_median']
README.md:15	131	r2/b0-2-receipt.json	d	d['degraded']
README.md:15	300	r2/b0-2-receipt.json	d#1	d['blocks']
README.md:15	34.1	r2/b0-2-receipt.json	.1f	d['overlap']['seconds']
README.md:15	23	r2/b0-2-receipt.json	d	d['overlap']['degraded_inside']
README.md:15	108	r2/b0-2-receipt.json	d	d['overlap']['degraded_beyond']
README.md:15	300	summary/bcrf/c-b9-grade.json	.0f	same(grade(r)['seconds'] for r in ('bcrf', 'baaf'))
README.md:15	2.585	r2/bcrf-poll-trace.tsv	.3f	lock_bracket('bcrf')[0]
README.md:15	3.161	r2/bcrf-poll-receipt.json	.3f	lock_bracket('bcrf')[1]
README.md:15	6.602	r2/baaf-poll-trace.tsv	.3f	lock_bracket('baaf')[0]
README.md:15	7.180	r2/baaf-poll-receipt.json	.3f	lock_bracket('baaf')[1]
README.md:15	-123.98	summary/bcrf/c-b9-grade.json	.2f	same(grade(r)['summary']['ch0_all']['thdn_db_median'] for r in ('bcrf', 'baaf'))
README.md:15	-123.97	summary/bcrf/c-b9-grade.json	.2f	same(grade(r)['summary']['ch1_all']['thdn_db_median'] for r in ('bcrf', 'baaf'))
README.md:15	300	summary/bcrf/c-b9-grade.json	d	same(n for r in ('bcrf', 'baaf') for n in (grade(r)['summary']['blocks'], grade(r)['summary']['blocks_at_floor']))
README.md:15	0	summary/bcrf/d-loop-decode.json	d	same(dec(r)['net_step_frames'] for r in ('bcrf', 'baaf'))
README.md:15	four	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	w	len(re.split(r', and |, ', b6_rule()))
README.md:15	three	summary/bcrf/c-b9-grade.json	w	same([terms('bcrf'), terms('baaf')])
3574	5	controls/r3-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3574	5	controls/r3-controls.json	d#1	len(d['controls'])
# hash tables: one row per byte count and SHA-256
2574	1,567,518	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-peer.pcap')['bytes'] for r in ['loop1'])
2574	0f4c6b42f6792dc84d8ba89d93e9edb97add667bf236b2d06833256ba14f1b0b	RAW-ARTIFACTS.json	s	same(raw(r + '/tap-peer.pcap')['sha256'] for r in ['loop1'])
2575	1,567,518	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-dut.pcap')['bytes'] for r in ['loop1'])
2575	a879b24feec3f4cdd4d72522d152afce4a1f6b527ce6a8210213c9779a6d9036	RAW-ARTIFACTS.json	s	same(raw(r + '/tap-dut.pcap')['sha256'] for r in ['loop1'])
2576	afff760831cd795283185c800d86460a1216511be9ebeb90a00baebc2ce8d0e2	RAW-ARTIFACTS.json	s	same(raw(r + '/extcap.raw')['sha256'] for r in ['loop1'])
2577	8,752,338	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-peer.pcap')['bytes'] for r in ['loop2'])
2577	6e0e1f4271d31495bd4d4c33ca4f5a55d791c9c3c8540a53b584abc505696776	RAW-ARTIFACTS.json	s	same(raw(r + '/tap-peer.pcap')['sha256'] for r in ['loop2'])
2578	8,680,530	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-dut.pcap')['bytes'] for r in ['loop2'])
2578	898242c513f4f30be70d0b3386f983e536f4bc4e5d63eaf341149b47aa6ac276	RAW-ARTIFACTS.json	s	same(raw(r + '/tap-dut.pcap')['sha256'] for r in ['loop2'])
2579	265d9585facf0aa1d6766454a5a0c1a871ae1449e0850e7de7f684b32b03067c	RAW-ARTIFACTS.json	s	same(raw(r + '/extcap.raw')['sha256'] for r in ['loop2'])
2586	18,087	tools/b16-asrun/run_b16.py	,d	size(p)
2586	d1a60cc2be9af3d8a3f81424ce468441ceeae88c960d817c127de5816f27a289	tools/b16-asrun/run_b16.py	s	sha(p)
2587	19,842	tools/tone_points_b16.py	,d	size(p)
2587	975645309ecb92d124b28d488c74902a2aea9379470e3eec563f1d93ea20869c	tools/tone_points_b16.py	s	sha(p)
2588	7,802	tools/align_b16.py	,d	size(p)
2588	71fd639b5db4c00f4048c6f2930330ee6880388613459a0d7411d577ab3eac86	tools/align_b16.py	s	sha(p)
2589	2,949	tools/acmp_tap_b16.py	,d	size(p)
2589	8c686a58e5c0288623c50cd7a40b273a6d0336b66af9765f0214a4dffaf57f65	tools/acmp_tap_b16.py	s	sha(p)
2590	1,565	controls/b16-tap-controls.json	,d	size(p)
2590	77a5995f07b9e300b5d819477e70441ed7ba3a26848e881ec6841219867da8fe	controls/b16-tap-controls.json	s	sha(p)
2591	1,176	controls/b16-align-controls-synth.json	,d	size(p)
2591	20ca766eb693b2f2252f6de97efda18c94455ade5d661813a8e26fd604b1d276	controls/b16-align-controls-synth.json	s	sha(p)
2592	11,587	runs/loop1/events.jsonl	,d	size(p)
2592	0390182f646584223bceeaf240e47135be383e47ddd56b4d15950336a441f954	runs/loop1/events.jsonl	s	sha(p)
2593	11,656	runs/loop2/events.jsonl	,d	size(p)
2593	cb3a5ffada5c35cdbbbbacc866e3f15abeded2e706754e9b3958479f75a0e2c0	runs/loop2/events.jsonl	s	sha(p)
2594	8,739	summary/loop2/acmp-peer-tap.json	,d	size(p)
2594	ecd9b4589b9508322c587938417550fa7dcb3a6eaee2065261e3ad73dabf6688	summary/loop2/acmp-peer-tap.json	s	sha(p)
2595	664	summary/loop1/d-extcap-pair.json	,d	size(p)
2595	496e6ad34ad164d1b8fea06c92d8ed099e3e831386c58d4b192d7881dfc64704	summary/loop1/d-extcap-pair.json	s	sha(p)
2596	661	summary/loop2/d-extcap-pair.json	,d	size(p)
2596	17f6c33f990654a1dd6dae8e5277ecd874955337cac66f0cfeb94eac33f549a5	summary/loop2/d-extcap-pair.json	s	sha(p)
2597	369	restore/census-compare.txt	,d	size(p)
2597	3a9a17cfc7ab6849571b9b2221c4981e8a19b7f460f1f66c30f9293a43f2de6f	restore/census-compare.txt	s	sha(p)
2598	1,532	identity/identity-verdict.txt	,d	size(p)
2598	4634ee944266589d6be3a9a1f90c93cd58c003b4d9fc60a341d43e46d7ff2130	identity/identity-verdict.txt	s	sha(p)
2909	90,602,048	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-peer.pcap')['bytes'] for r in ['pts1'])
2909	b235c4321fc2324cab2412692bd5d1b0642b73ea13549c028c1722ba9dfbc68a	RAW-ARTIFACTS.json	s	same(raw(r + '/tap-peer.pcap')['sha256'] for r in ['pts1'])
2910	90,981,020	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-dut.pcap')['bytes'] for r in ['pts1'])
2910	e0b086473164bf58ba304eb7b2d9e435eb412fcf11da8d246524abd18f4bb083	RAW-ARTIFACTS.json	s	same(raw(r + '/tap-dut.pcap')['sha256'] for r in ['pts1'])
2911	15,360,000	RAW-ARTIFACTS.json	,d	same(raw(r + '/mcasp-all.raw')['bytes'] for r in ['pts1'])
2911	ff408b45488948294ed1c7bc5ce2ca13725fd0c7613e311d16fbf880f3992dd5	RAW-ARTIFACTS.json	s	same(raw(r + '/mcasp-all.raw')['sha256'] for r in ['pts1'])
2912	02345629d6828ebe193391209b4bda618ff95f1d83b24e164996d8fcefbf75d4	RAW-ARTIFACTS.json	s	same(raw(r + '/extcap.raw')['sha256'] for r in ['pts1'])
2913	90,981,358	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-peer.pcap')['bytes'] for r in ['pts2'])
2913	f06bfd1ed8f486f765bce404607e88b0fda7c3e33da6d936cfa9840bfebf8b1b	RAW-ARTIFACTS.json	s	same(raw(r + '/tap-peer.pcap')['sha256'] for r in ['pts2'])
2914	90,980,890	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-dut.pcap')['bytes'] for r in ['pts2'])
2914	9c6059d0b7ad9a23fe8176733d087d01b13613d96c0012244f1982a2acbaf75e	RAW-ARTIFACTS.json	s	same(raw(r + '/tap-dut.pcap')['sha256'] for r in ['pts2'])
2915	15,360,000	RAW-ARTIFACTS.json	,d	same(raw(r + '/mcasp-all.raw')['bytes'] for r in ['pts2'])
2915	f3447f30211ed37e548e9746bf2c9c9e4795797d1e551dc3afae2204f7f0eb6c	RAW-ARTIFACTS.json	s	same(raw(r + '/mcasp-all.raw')['sha256'] for r in ['pts2'])
2916	08bf83e0eb4a50540517142c82ad0f386852384ae66f89fad1dd3824b9fd31e5	RAW-ARTIFACTS.json	s	same(raw(r + '/extcap.raw')['sha256'] for r in ['pts2'])
2917	1,536,000	RAW-ARTIFACTS.json	,d	same(raw(r + '/b6-loop.raw')['bytes'] for r in ['pts2', 'b0', 'b0-2'])
2917	566d3dfae6eb60a658b8cb0ddf5c833900ccbe4feb41c427a970a5854cc75588	RAW-ARTIFACTS.json	s	same(raw(r + '/b6-loop.raw')['sha256'] for r in ['pts2', 'b0', 'b0-2'])
2918	153,665,476	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-peer.pcap')['bytes'] for r in ['b0'])
2918	075ff41dfbe12b06673eac87f2b04b78519fbb914fd987e7d6b7af4d3ae42e23	RAW-ARTIFACTS.json	s	same(raw(r + '/tap-peer.pcap')['sha256'] for r in ['b0'])
2919	154,049,176	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-dut.pcap')['bytes'] for r in ['b0'])
2919	ce0f42c6753d8acd2c214d98c9162ffcd12b566ecfab8ba6f2b38bedb67a6737	RAW-ARTIFACTS.json	s	same(raw(r + '/tap-dut.pcap')['sha256'] for r in ['b0'])
2920	0	RAW-ARTIFACTS.json	,d	same(raw(r + '/mcasp-all.raw')['bytes'] for r in ['b0'])
2920	e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855	RAW-ARTIFACTS.json	s	same(raw(r + '/mcasp-all.raw')['sha256'] for r in ['b0'])
2921	b0517ab7e64865159ba8aa319fd9084886812d8ddbf1dedbc95889740c9c41c1	RAW-ARTIFACTS.json	s	same(raw(r + '/extcap.raw')['sha256'] for r in ['b0'])
2922	154,050,970	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-peer.pcap')['bytes'] for r in ['b0-2'])
2922	c0efda0683566f3b1a5299fe1ffa97f970585ce51d6ca218c7d9d825c08bbf23	RAW-ARTIFACTS.json	s	same(raw(r + '/tap-peer.pcap')['sha256'] for r in ['b0-2'])
2923	154,049,284	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-dut.pcap')['bytes'] for r in ['b0-2'])
2923	59bcfef4cfe31f3326360aa3b861e5a5dc7f26f45f00f94afcbc65dce286209d	RAW-ARTIFACTS.json	s	same(raw(r + '/tap-dut.pcap')['sha256'] for r in ['b0-2'])
2924	460,800,000	RAW-ARTIFACTS.json	,d	same(raw(r + '/mcasp-all.raw')['bytes'] for r in ['b0-2'])
2924	9b7072a2ff202841d81ffb4846697a9ebb9240ed72b66610292b4071f83486c1	RAW-ARTIFACTS.json	s	same(raw(r + '/mcasp-all.raw')['sha256'] for r in ['b0-2'])
2925	52da5d1febaebd5b03617b24f40c52ed381f57a3490ef20c4a2f6ad7a931dc7b	RAW-ARTIFACTS.json	s	same(raw(r + '/extcap.raw')['sha256'] for r in ['b0-2'])
2926	90,981,956	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-peer.pcap')['bytes'] for r in ['pts3'])
2926	6cdf04d06b9d92d11a9fd748e0a8d94b394f2a5337f8ce7a1da52d7f962c46c0	RAW-ARTIFACTS.json	s	same(raw(r + '/tap-peer.pcap')['sha256'] for r in ['pts3'])
2927	90,980,912	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-dut.pcap')['bytes'] for r in ['pts3'])
2927	f759569cdeab83ae2491346826a33cb1c8c015289ea80963400794ed52f5aed0	RAW-ARTIFACTS.json	s	same(raw(r + '/tap-dut.pcap')['sha256'] for r in ['pts3'])
2928	15,360,000	RAW-ARTIFACTS.json	,d	same(raw(r + '/mcasp-all.raw')['bytes'] for r in ['pts3'])
2928	c99d7fc661f7886da65aa8e7728527699b2ee78d30102baa851ea24163ae2558	RAW-ARTIFACTS.json	s	same(raw(r + '/mcasp-all.raw')['sha256'] for r in ['pts3'])
2929	5260ce29b7d118595fa61d98435f3bab28a469448000856daa328b01c5565f2a	RAW-ARTIFACTS.json	s	same(raw(r + '/extcap.raw')['sha256'] for r in ['pts3'])
2936	25,161	tools/run_b16.py	,d	size(p)
2936	424234725a2035ab9ce30512e2da1275495758283f1f483c86d982e008a43be2	tools/run_b16.py	s	sha(p)
2937	1,812	tools/run_locked_b16.sh	,d	size(p)
2937	8694f9b0e3c38814ab55896108abbde59f04e302b9de82f690c12f41646f90fa	tools/run_locked_b16.sh	s	sha(p)
2938	4,122	tools/dloop_b16.py	,d	size(p)
2938	d3bf1a0e81b2b01bd1c12713b5ab7dbca0903c596d3fb33b6ac194e725af1ecf	tools/dloop_b16.py	s	sha(p)
2939	705	controls/b16b-dloop-control.json	,d	size(p)
2939	fbce8878a37a47b76d67fed3e450eecf57b6b3083c7ec0edc12e789e5bd775fb	controls/b16b-dloop-control.json	s	sha(p)
2940	8,437	runs/pts1/events.jsonl	,d	size(p)
2940	bcd8663a9cd40acd7c4cf7c933950751527d9088432d153a9306f40ae12031fd	runs/pts1/events.jsonl	s	sha(p)
2941	9,876	runs/pts2/events.jsonl	,d	size(p)
2941	d6a68179a3dc2aed3e36a15d2e080922068e476c9163657d4aeacfbe394ac45b	runs/pts2/events.jsonl	s	sha(p)
2942	11,877	runs/b0/events.jsonl	,d	size(p)
2942	6b9bb18043df40efeb2d93808cbca099d0988b25bfa04a91aefaaf9c3994053a	runs/b0/events.jsonl	s	sha(p)
2943	11,883	runs/b0-2/events.jsonl	,d	size(p)
2943	d5e6d8dd6cc5b349a0aa37adad9394206fded1f221905b0e41f7d82f96dc82ab	runs/b0-2/events.jsonl	s	sha(p)
2944	8,435	runs/pts3/events.jsonl	,d	size(p)
2944	a53e635e28ca361874eb2b9c5d842d45479ca69722f74ce10e27c31cd8997c40	runs/pts3/events.jsonl	s	sha(p)
2945	422	summary/pts1/align-a-c.json	,d	size(p)
2945	11bc737c7af2d4ef1cf77d234dfe275049102e65a801e5cf1ff0e8eb6548fcb3	summary/pts1/align-a-c.json	s	sha(p)
2946	422	summary/pts2/align-a-c.json	,d	size(p)
2946	9cf3e2f3923e649dc20a34f9f711c4f62f0a772b41a7e7a51f28f0baaa7a8202	summary/pts2/align-a-c.json	s	sha(p)
2947	422	summary/pts3/align-a-c.json	,d	size(p)
2947	dab152d9ae393ed2f20476b8e79b45d969bc3240c06a2235a49c58f2bc7f41cd	summary/pts3/align-a-c.json	s	sha(p)
2948	426	summary/b0-2/align-a-c.json	,d	size(p)
2948	a24903924f8a43d07721c366966d7ee9a84a0b70f708612de079438bfb3e0da4	summary/b0-2/align-a-c.json	s	sha(p)
2949	426	summary/b0-2/align-b-c.json	,d	size(p)
2949	141619ca294c004ca02231eab1122a4a93ce6ddd732635c7d2e95bfbaf29bcd2	summary/b0-2/align-b-c.json	s	sha(p)
2950	135,813	summary/b0-2/c-b9-grade.json	,d	size(p)
2950	1d554ce3a70dfb4a5ef935d139980ff0bee6cf8eb505ec42fca2781a7ed54078	summary/b0-2/c-b9-grade.json	s	sha(p)
2951	563	summary/pts2/d-loop-decode.json	,d	size(p)
2951	49ce9f4c6487fcc15f41d68e5a25f36a0b83b7f994cee838e0c8204b455a21da	summary/pts2/d-loop-decode.json	s	sha(p)
2952	316	summary/b0-2/d-loop-decode.json	,d	size(p)
2952	a58b5ebbe5a15cd3a3d216b18192b4157a5b762baa7b010be901428d9e56fd1b	summary/b0-2/d-loop-decode.json	s	sha(p)
2953	481	restore/census-compare-b16b.txt	,d	size(p)
2953	d14071dedb18e5cafc24421ede3cd450289d77e1af6f13f8a48c9d3c26f66648	restore/census-compare-b16b.txt	s	sha(p)
2954	1,532	identity-b16b/identity-verdict.txt	,d	size(p)
2954	4634ee944266589d6be3a9a1f90c93cd58c003b4d9fc60a341d43e46d7ff2130	identity-b16b/identity-verdict.txt	s	sha(p)
3321	154,049,992	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-peer.pcap')['bytes'] for r in ['bcrf'])
3321	edad46fe5de09dcace08a19eef8f5ecc5f0e9cab9bf5e506eb3e2f23a6bc97b3	RAW-ARTIFACTS.json	s	same(raw(r + '/tap-peer.pcap')['sha256'] for r in ['bcrf'])
3322	154,048,228	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-dut.pcap')['bytes'] for r in ['bcrf'])
3322	4e7013347ec9de4e29c61165f92acee4e22104bbf5e7aa1050225d38ba593d09	RAW-ARTIFACTS.json	s	same(raw(r + '/tap-dut.pcap')['sha256'] for r in ['bcrf'])
3323	460,800,000	RAW-ARTIFACTS.json	,d	same(raw(r + '/mcasp-all.raw')['bytes'] for r in ['bcrf'])
3323	b5e30bb576949c077f3ff611c6226d5bf094e7b65ff2e1f033541c3f9ba1c03f	RAW-ARTIFACTS.json	s	same(raw(r + '/mcasp-all.raw')['sha256'] for r in ['bcrf'])
3324	b4f6a999500c5b1b0e1c058afeaf9788410f1b2f29e4a4e684ba19b1c2f50e4d	RAW-ARTIFACTS.json	s	same(raw(r + '/extcap.raw')['sha256'] for r in ['bcrf'])
3325	218,420	RAW-ARTIFACTS.json	,d	same(raw(r + '/poll-run.jsonl')['bytes'] for r in ['bcrf'])
3325	9cfc79bb2ae8ad6c6e8cca028d66af3b6695c0982ffe2a512ea756fb3dc06c03	RAW-ARTIFACTS.json	s	same(raw(r + '/poll-run.jsonl')['sha256'] for r in ['bcrf'])
3326	199,498	RAW-ARTIFACTS.json	,d	same(raw(r + '/tone-status.jsonl')['bytes'] for r in ['bcrf'])
3326	2a7974d5a6f6548e847844c326e52e59d6cc4b1f6dcfd0a730c673f85865a10c	RAW-ARTIFACTS.json	s	same(raw(r + '/tone-status.jsonl')['sha256'] for r in ['bcrf'])
3327	154,049,168	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-peer.pcap')['bytes'] for r in ['baaf'])
3327	234a2f0b414dcd0a07e9f2fb9047d417b9d14da77fddc0a0b708e315983ab36d	RAW-ARTIFACTS.json	s	same(raw(r + '/tap-peer.pcap')['sha256'] for r in ['baaf'])
3328	154,048,154	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-dut.pcap')['bytes'] for r in ['baaf'])
3328	5a8dbaad272ad1c6bbd18aa146486ed2a78c27d23270a8e9d243207b9269038b	RAW-ARTIFACTS.json	s	same(raw(r + '/tap-dut.pcap')['sha256'] for r in ['baaf'])
3329	460,800,000	RAW-ARTIFACTS.json	,d	same(raw(r + '/mcasp-all.raw')['bytes'] for r in ['baaf'])
3329	1351272cb679353885983762402caa13ef6e793831463dfc5a2ca242cca3a93e	RAW-ARTIFACTS.json	s	same(raw(r + '/mcasp-all.raw')['sha256'] for r in ['baaf'])
3330	1eeaad6845cb2ad30de88ffe5eb211518f12acf14fa6fed9bd14a12cdd9c099c	RAW-ARTIFACTS.json	s	same(raw(r + '/extcap.raw')['sha256'] for r in ['baaf'])
3331	218,401	RAW-ARTIFACTS.json	,d	same(raw(r + '/poll-run.jsonl')['bytes'] for r in ['baaf'])
3331	476a007728d267931a7baf32095afd8342fde5e8c30984f469b857c3841bab73	RAW-ARTIFACTS.json	s	same(raw(r + '/poll-run.jsonl')['sha256'] for r in ['baaf'])
3332	200,133	RAW-ARTIFACTS.json	,d	same(raw(r + '/tone-status.jsonl')['bytes'] for r in ['baaf'])
3332	40962288e0fe5eca37964b068c2060c005bc39ccbbe470486c41003653ce3a99	RAW-ARTIFACTS.json	s	same(raw(r + '/tone-status.jsonl')['sha256'] for r in ['baaf'])
3333	1,536,000	RAW-ARTIFACTS.json	,d	same(raw(r + '/b6-loop.raw')['bytes'] for r in ['bcrf', 'baaf'])
3333	566d3dfae6eb60a658b8cb0ddf5c833900ccbe4feb41c427a970a5854cc75588	RAW-ARTIFACTS.json	s	same(raw(r + '/b6-loop.raw')['sha256'] for r in ['bcrf', 'baaf'])
3341	41,693	tools/run_b16c.py	,d	size(p)
3341	8ed6b63f03598f595c6b2aedcfedcdd81f37d3d130cdc2368ba5010962948a3c	tools/run_b16c.py	s	sha(p)
3342	2,564	tools/run_locked_b16c.sh	,d	size(p)
3342	6eed98dbba4f6fde2752e185c5406005ad5e0915910c8ca43026231b8aa0cd6f	tools/run_locked_b16c.sh	s	sha(p)
3343	6,593	tools/tables_b16c.py	,d	size(p)
3343	95b33b4530062c48e17b0db09019ff18b0fa166938006693947ee3b31408d918	tools/tables_b16c.py	s	sha(p)
3344	1,903	tools/dryrun_b16c/dryrun_b16c.sh	,d	size(p)
3344	699955707f9847b5db9076782d0f4472978c27ea4d85cb45fcedcc8e95b60be7	tools/dryrun_b16c/dryrun_b16c.sh	s	sha(p)
3345	4,074	tools/dryrun_b16c/check_dryrun_b16c.py	,d	size(p)
3345	fdfffe23a65b2e07fd28270128e5832d8f0ce6eb801178bd0de671b216c4a204	tools/dryrun_b16c/check_dryrun_b16c.py	s	sha(p)
3346	273	controls/b16c-dryrun-summary.json	,d	size(p)
3346	685737875fc4df85c27e5e37ac680f373cdc0e02e930da8189da8834a891e336	controls/b16c-dryrun-summary.json	s	sha(p)
3347	617	controls/b16c-wrapper-deadline.txt	,d	size(p)
3347	090969eb04c94470e4589d465f960e72d938745fa1c61203570f0ef9fc439677	controls/b16c-wrapper-deadline.txt	s	sha(p)
3348	20,973	runs/bcrf/events.jsonl	,d	size(p)
3348	9e6b07074af7d371cbca8df974a85e9a6d3f6bd73526bd6350c42344a7c88e55	runs/bcrf/events.jsonl	s	sha(p)
3349	20,973	runs/baaf/events.jsonl	,d	size(p)
3349	2011eca5bb7b5802451342da06268acc88af4b2ac0c161c06edd9d7f7b24ab2f	runs/baaf/events.jsonl	s	sha(p)
3350	135,192	summary/bcrf/c-b9-grade.json	,d	size(p)
3350	a74f236bb68e333f5dbc8f1a47176badf318048573728e9cec603cc8de5a7e6b	summary/bcrf/c-b9-grade.json	s	sha(p)
3351	135,271	summary/baaf/c-b9-grade.json	,d	size(p)
3351	2b0ee83ea4d80978bc7239cba706e6c14881f77b4a503c89759021c0203efd84	summary/baaf/c-b9-grade.json	s	sha(p)
3352	426	summary/bcrf/align-a-c.json	,d	size(p)
3352	80df5a0b1751a209f2b8055409e5399d3648618bd80ca036c913d9045e3721ec	summary/bcrf/align-a-c.json	s	sha(p)
3353	426	summary/bcrf/align-b-c.json	,d	size(p)
3353	e22934e3702eb234534b11342b3710bdee94001dd4ffbc1b446a9d52d7e51cf2	summary/bcrf/align-b-c.json	s	sha(p)
3354	426	summary/baaf/align-a-c.json	,d	size(p)
3354	1c88af889538788a8c7842e79aea5f2e3684802d5d2dbaa5dd293e8003dbfabd	summary/baaf/align-a-c.json	s	sha(p)
3355	426	summary/baaf/align-b-c.json	,d	size(p)
3355	1a8d61828b3d882136014f6cd2b2eefc69a963b46a33d49c84e047702103c245	summary/baaf/align-b-c.json	s	sha(p)
3356	316	summary/bcrf/d-loop-decode.json	,d	size(p)
3356	9b238160fb9fda206294b9df90bc52724c6d9d97d262681c8e7a6a011b74fae0	summary/bcrf/d-loop-decode.json	s	sha(p)
3357	316	summary/baaf/d-loop-decode.json	,d	size(p)
3357	342724e82b1877b12579f04102566a8ae7cba30dd0baea8a55a8cb88acf2e2b9	summary/baaf/d-loop-decode.json	s	sha(p)
3358	12,847	summary/b16c-tables.md	,d	size(p)
3358	8df9a8ccda5f2bbc143bc2dbcaa8868e3dd5a1d1fab8eb427428c2a7d95a19f8	summary/b16c-tables.md	s	sha(p)
3359	481	restore/census-compare-b16c.txt	,d	size(p)
3359	5b0015fd2a63e3aa2a6676842da251196fcb1f1540c7532980f006b7c5f90dcc	restore/census-compare-b16c.txt	s	sha(p)
3360	1,532	identity-b16c/identity-verdict.txt	,d	size(p)
3360	4634ee944266589d6be3a9a1f90c93cd58c003b4d9fc60a341d43e46d7ff2130	identity-b16c/identity-verdict.txt	s	sha(p)
3442	05:47:56	r2/source-receipt.json	s	get(d, 'reads.b16-state-1.at')
3442	ce5574185d1c05f8ca0d1d669904eb4c4ea21229f8af7f33b624aa461e56dca0	RAW-ARTIFACTS.json	s	same([raw('source/b16-state-1.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16-state-1.sha256')])
3443	05:55:41	r2/source-receipt.json	s	get(d, 'reads.b16-meters-1.at')
3443	3a04b34f9fd83de714ba30523a4ed0ee4b09f4fae1e413d4adfc9891ebcfa6ca	RAW-ARTIFACTS.json	s	same([raw('source/b16-meters-1.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16-meters-1.sha256')])
3444	06:01:44	r2/source-receipt.json	s	get(d, 'reads.b16-meters-2.at')
3444	5e8e366bd950e2523b57735c4be8c3b672cda416b105b3ddc55ee3d6d18611b2	RAW-ARTIFACTS.json	s	same([raw('source/b16-meters-2.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16-meters-2.sha256')])
3445	06:01:48	r2/source-receipt.json	s	get(d, 'reads.b16-state-2.at')
3445	f4bcf327c815ec686ec7bb2573551e0ac78cbb6ba03d0862cff7480a65b6bd1e	RAW-ARTIFACTS.json	s	same([raw('source/b16-state-2.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16-state-2.sha256')])
3446	06:23:06	r2/source-receipt.json	s	get(d, 'reads.b16b-state-1.at')
3446	6b4cd4e6a325b389e4be65e43e5109ed903f7ca27b58864e9dbef531b4818c72	RAW-ARTIFACTS.json	s	same([raw('source/b16b-state-1.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16b-state-1.sha256')])
3447	06:23:30	r2/source-receipt.json	s	get(d, 'reads.b16b-meters-1.at')
3447	a7c844bddf786fb0eccfd15af94b5c0bc1b5ae55bbe49e5021dedce01a6c2c04	RAW-ARTIFACTS.json	s	same([raw('source/b16b-meters-1.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16b-meters-1.sha256')])
3448	06:50:05	r2/source-receipt.json	s	get(d, 'reads.b16b-meters-2.at')
3448	fb5c6e23143b1379948586545b66fc26a3419827c72eb929ad4b531fcbc273ed	RAW-ARTIFACTS.json	s	same([raw('source/b16b-meters-2.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16b-meters-2.sha256')])
3449	06:50:08	r2/source-receipt.json	s	get(d, 'reads.b16b-state-2.at')
3449	b8f0746478b7cd652f3a06234aa7358a4078614f0b0fc64344a9a476b1d25288	RAW-ARTIFACTS.json	s	same([raw('source/b16b-state-2.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16b-state-2.sha256')])
3450	07:48:56	r2/source-receipt.json	s	get(d, 'reads.b16c-state-1.at')
3450	195d59866d6ccd976e95d79f3833b6ff01c0ab5bac7d04e934b7338a97d54a3a	RAW-ARTIFACTS.json	s	same([raw('source/b16c-state-1.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16c-state-1.sha256')])
3451	07:49:34	r2/source-receipt.json	s	get(d, 'reads.b16c-meters-1.at')
3451	f694f3dfdbec41ec48e85fec9bc77019a4168855d2f01f921a88e677af19fbf7	RAW-ARTIFACTS.json	s	same([raw('source/b16c-meters-1.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16c-meters-1.sha256')])
3452	08:03:29	r2/source-receipt.json	s	get(d, 'reads.b16c-meters-2.at')
3452	794b67fe8ab03f3e61c2eaf9245d0988849b1ce73cd26167ab67f8690d5e01ab	RAW-ARTIFACTS.json	s	same([raw('source/b16c-meters-2.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16c-meters-2.sha256')])
3453	08:03:32	r2/source-receipt.json	s	get(d, 'reads.b16c-state-2.at')
3453	93cb9240f72ee45779008872da841cb3bec4bb7de527bb05381a91dfac781624	RAW-ARTIFACTS.json	s	same([raw('source/b16c-state-2.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16c-state-2.sha256')])
3463	10,234	tools/r2_poll_b16c.py	,d	size(p)
3463	14ae199a556bca981cd9898d186efd983609325b93412beb6dd332a0f0276cb2	tools/r2_poll_b16c.py	s	sha(p)
3464	6,604	tools/r2_source_b16.py	,d	size(p)
3464	903145f68d3ce8e4e2dc3813b67ac9acfad2b0361a58b146e73b839bec63fa3c	tools/r2_source_b16.py	s	sha(p)
3465	4,874	tools/r2_b0_receipt.py	,d	size(p)
3465	cf650fa86179d611ddf63eed2151b5f1062847fd6797b277590e3a5e82cdfcad	tools/r2_b0_receipt.py	s	sha(p)
3466	6,945	r2/bcrf-poll-receipt.json	,d	size(p)
3466	abb1f853804c23c364b49f2b4263bcae68b928881ccb501d187f78a64c00660f	r2/bcrf-poll-receipt.json	s	sha(p)
3467	62,923	r2/bcrf-poll-trace.tsv	,d	size(p)
3467	050aeded3806ec9ec821b19da28b85313a9ae58921fc9d2c86a236d10078f1db	r2/bcrf-poll-trace.tsv	s	sha(p)
3468	7,446	r2/baaf-poll-receipt.json	,d	size(p)
3468	2f8cc0894cfb8918ff3b066721f8e0b0200c2241ee280375202cf6d6f641c931	r2/baaf-poll-receipt.json	s	sha(p)
3469	62,923	r2/baaf-poll-trace.tsv	,d	size(p)
3469	3e891d0faf7ba65997b8a487ad53f01e86dfc2713fa8b1721ff33c0d1bdfdeea	r2/baaf-poll-trace.tsv	s	sha(p)
3470	21,276	r2/source-receipt.json	,d	size(p)
3470	1afbce9cdd27468394bf33265c45f1bb1d1e7a46091e15a715950a2ba4406912	r2/source-receipt.json	s	sha(p)
3471	2,484	r2/b0-2-receipt.json	,d	size(p)
3471	8bcab8394d2f8d02890c76ce9bf5f864f53cf195ae4c58bec8bee055c3aba6f7	r2/b0-2-receipt.json	s	sha(p)
3472	1,984	controls/r2-controls.json	,d	size(p)
3472	dc6f67634197b22e7f30225758d4221f697833472997b0b05a8174d94956b437	controls/r2-controls.json	s	sha(p)
3571	1,990	tools/r3_playback_logs.py	,d	size(p)
3571	27334c6d3106f9305187deef6196a7dcb7e14b10d6fbea08f721029766dcf595	tools/r3_playback_logs.py	s	sha(p)
3572	795	r3/playback-logs.json	,d	size(p)
3572	68e905288cf0c01c385a995bf66edc78e6323e041de99c1e0f1f3e4b360f64fe	r3/playback-logs.json	s	sha(p)
3573	6,541	tools/r3_check_controls.py	,d	size(p)
3573	85fc57876334b823cd349a9752bf12581bbb22f9f5c5b2a4d6f68ab948a54157	tools/r3_check_controls.py	s	sha(p)
3574	1,579	controls/r3-controls.json	,d	size(p)
3574	6b6f8bc7b99e5ec6843a7c385e681b4bcf4b89b1b56d84dcc10a88889ce6cc05	controls/r3-controls.json	s	sha(p)
2687	1,145,034	summary/pts1/a-peer-tap.json	,d	d['frames']
2687	190,839	summary/pts1/a-peer-tap.json	,d	d['info']['pdus']
2687	0	summary/pts1/a-peer-tap.json	d	d['info']['seq_gaps']
2687	-14.1353	summary/pts1/a-peer-tap.json	.4f	T(d, 0, 'level_dbfs')
2687	997.0069	summary/pts1/a-peer-tap.json	.4f	T(d, 0, 'f_hz')
2687	+6.94	summary/pts1/a-peer-tap.json	+z.2f	T(d, 0, 'ppm')
2687	-108.74	summary/pts1/a-peer-tap.json	.2f	T(d, 0, 'thdn_db')
2687	-100.95	summary/pts1/a-peer-tap.json	.2f	T(d, 0, 'worst')
2687	108.74	summary/pts1/a-peer-tap.json	.2f	T(d, 0, 'snr_db')
2687	9,973.0692	summary/pts1/a-peer-tap.json	,.4f	T(d, 1, 'f_hz')
2687	+6.94	summary/pts1/a-peer-tap.json	+z.2f	T(d, 1, 'ppm')
2687	-88.87	summary/pts1/a-peer-tap.json	.2f	T(d, 1, 'thdn_db')
2687	-80.97	summary/pts1/a-peer-tap.json	.2f	T(d, 1, 'worst')
2687	88.87	summary/pts1/a-peer-tap.json	.2f	T(d, 1, 'snr_db')
2688	1,149,822	summary/pts1/b-dut-tap.json	,d	d['frames']
2688	191,637	summary/pts1/b-dut-tap.json	,d	d['info']['pdus']
2688	0	summary/pts1/b-dut-tap.json	d	d['info']['seq_gaps']
2688	-14.1353	summary/pts1/b-dut-tap.json	.4f	T(d, 0, 'level_dbfs')
2688	997.0069	summary/pts1/b-dut-tap.json	.4f	T(d, 0, 'f_hz')
2688	+6.94	summary/pts1/b-dut-tap.json	+z.2f	T(d, 0, 'ppm')
2688	-107.17	summary/pts1/b-dut-tap.json	.2f	T(d, 0, 'thdn_db')
2688	-100.80	summary/pts1/b-dut-tap.json	.2f	T(d, 0, 'worst')
2688	107.17	summary/pts1/b-dut-tap.json	.2f	T(d, 0, 'snr_db')
2688	9,973.0692	summary/pts1/b-dut-tap.json	,.4f	T(d, 1, 'f_hz')
2688	+6.94	summary/pts1/b-dut-tap.json	+z.2f	T(d, 1, 'ppm')
2688	-87.26	summary/pts1/b-dut-tap.json	.2f	T(d, 1, 'thdn_db')
2688	-80.81	summary/pts1/b-dut-tap.json	.2f	T(d, 1, 'worst')
2688	87.26	summary/pts1/b-dut-tap.json	.2f	T(d, 1, 'snr_db')
2689	480,000	summary/pts1/c-mcasp.json	,d	d['frames']
2689	-14.1353	summary/pts1/c-mcasp.json	.4f	T(d, 0, 'level_dbfs')
2689	997.0069	summary/pts1/c-mcasp.json	.4f	T(d, 0, 'f_hz')
2689	+6.95	summary/pts1/c-mcasp.json	+z.2f	T(d, 0, 'ppm')
2689	-105.27	summary/pts1/c-mcasp.json	.2f	T(d, 0, 'thdn_db')
2689	-98.66	summary/pts1/c-mcasp.json	.2f	T(d, 0, 'worst')
2689	105.27	summary/pts1/c-mcasp.json	.2f	T(d, 0, 'snr_db')
2689	9,973.0693	summary/pts1/c-mcasp.json	,.4f	T(d, 1, 'f_hz')
2689	+6.95	summary/pts1/c-mcasp.json	+z.2f	T(d, 1, 'ppm')
2689	-85.33	summary/pts1/c-mcasp.json	.2f	T(d, 1, 'thdn_db')
2689	-78.67	summary/pts1/c-mcasp.json	.2f	T(d, 1, 'worst')
2689	85.33	summary/pts1/c-mcasp.json	.2f	T(d, 1, 'snr_db')
2690	1,149,828	summary/pts2/a-peer-tap.json	,d	d['frames']
2690	191,638	summary/pts2/a-peer-tap.json	,d	d['info']['pdus']
2690	0	summary/pts2/a-peer-tap.json	d	d['info']['seq_gaps']
2690	-14.1353	summary/pts2/a-peer-tap.json	.4f	T(d, 0, 'level_dbfs')
2690	997.0069	summary/pts2/a-peer-tap.json	.4f	T(d, 0, 'f_hz')
2690	+6.96	summary/pts2/a-peer-tap.json	+z.2f	T(d, 0, 'ppm')
2690	-107.72	summary/pts2/a-peer-tap.json	.2f	T(d, 0, 'thdn_db')
2690	-101.02	summary/pts2/a-peer-tap.json	.2f	T(d, 0, 'worst')
2690	107.72	summary/pts2/a-peer-tap.json	.2f	T(d, 0, 'snr_db')
2690	9,973.0694	summary/pts2/a-peer-tap.json	,.4f	T(d, 1, 'f_hz')
2690	+6.96	summary/pts2/a-peer-tap.json	+z.2f	T(d, 1, 'ppm')
2690	-87.82	summary/pts2/a-peer-tap.json	.2f	T(d, 1, 'thdn_db')
2690	-81.05	summary/pts2/a-peer-tap.json	.2f	T(d, 1, 'worst')
2690	87.82	summary/pts2/a-peer-tap.json	.2f	T(d, 1, 'snr_db')
2691	1,149,822	summary/pts2/b-dut-tap.json	,d	d['frames']
2691	191,637	summary/pts2/b-dut-tap.json	,d	d['info']['pdus']
2691	0	summary/pts2/b-dut-tap.json	d	d['info']['seq_gaps']
2691	-14.1353	summary/pts2/b-dut-tap.json	.4f	T(d, 0, 'level_dbfs')
2691	997.0069	summary/pts2/b-dut-tap.json	.4f	T(d, 0, 'f_hz')
2691	+6.96	summary/pts2/b-dut-tap.json	+z.2f	T(d, 0, 'ppm')
2691	-108.33	summary/pts2/b-dut-tap.json	.2f	T(d, 0, 'thdn_db')
2691	-100.62	summary/pts2/b-dut-tap.json	.2f	T(d, 0, 'worst')
2691	108.33	summary/pts2/b-dut-tap.json	.2f	T(d, 0, 'snr_db')
2691	9,973.0694	summary/pts2/b-dut-tap.json	,.4f	T(d, 1, 'f_hz')
2691	+6.96	summary/pts2/b-dut-tap.json	+z.2f	T(d, 1, 'ppm')
2691	-88.44	summary/pts2/b-dut-tap.json	.2f	T(d, 1, 'thdn_db')
2691	-80.64	summary/pts2/b-dut-tap.json	.2f	T(d, 1, 'worst')
2691	88.44	summary/pts2/b-dut-tap.json	.2f	T(d, 1, 'snr_db')
2692	480,000	summary/pts2/c-mcasp.json	,d	d['frames']
2692	-14.1353	summary/pts2/c-mcasp.json	.4f	T(d, 0, 'level_dbfs')
2692	997.0069	summary/pts2/c-mcasp.json	.4f	T(d, 0, 'f_hz')
2692	+6.96	summary/pts2/c-mcasp.json	+z.2f	T(d, 0, 'ppm')
2692	-109.70	summary/pts2/c-mcasp.json	.2f	T(d, 0, 'thdn_db')
2692	-101.43	summary/pts2/c-mcasp.json	.2f	T(d, 0, 'worst')
2692	109.70	summary/pts2/c-mcasp.json	.2f	T(d, 0, 'snr_db')
2692	9,973.0694	summary/pts2/c-mcasp.json	,.4f	T(d, 1, 'f_hz')
2692	+6.96	summary/pts2/c-mcasp.json	+z.2f	T(d, 1, 'ppm')
2692	-89.87	summary/pts2/c-mcasp.json	.2f	T(d, 1, 'thdn_db')
2692	-81.46	summary/pts2/c-mcasp.json	.2f	T(d, 1, 'worst')
2692	89.87	summary/pts2/c-mcasp.json	.2f	T(d, 1, 'snr_db')
2693	1,149,834	summary/pts3/a-peer-tap.json	,d	d['frames']
2693	191,639	summary/pts3/a-peer-tap.json	,d	d['info']['pdus']
2693	0	summary/pts3/a-peer-tap.json	d	d['info']['seq_gaps']
2693	-14.1035	summary/pts3/a-peer-tap.json	.4f	T(d, 0, 'level_dbfs')
2693	997.0000	summary/pts3/a-peer-tap.json	.4f	T(d, 0, 'f_hz')
2693	0.000	summary/pts3/a-peer-tap.json	z.3f	T(d, 0, 'ppm')
2693	-123.93	summary/pts3/a-peer-tap.json	.2f	T(d, 0, 'thdn_db')
2693	-109.28	summary/pts3/a-peer-tap.json	.2f	T(d, 0, 'worst')
2693	123.94	summary/pts3/a-peer-tap.json	.2f	T(d, 0, 'snr_db')
2693	9,973.0000	summary/pts3/a-peer-tap.json	,.4f	T(d, 1, 'f_hz')
2693	0.000	summary/pts3/a-peer-tap.json	z.3f	T(d, 1, 'ppm')
2693	-122.47	summary/pts3/a-peer-tap.json	.2f	T(d, 1, 'thdn_db')
2693	-89.43	summary/pts3/a-peer-tap.json	.2f	T(d, 1, 'worst')
2693	122.48	summary/pts3/a-peer-tap.json	.2f	T(d, 1, 'snr_db')
2694	1,149,822	summary/pts3/b-dut-tap.json	,d	d['frames']
2694	191,637	summary/pts3/b-dut-tap.json	,d	d['info']['pdus']
2694	0	summary/pts3/b-dut-tap.json	d	d['info']['seq_gaps']
2694	-14.1035	summary/pts3/b-dut-tap.json	.4f	T(d, 0, 'level_dbfs')
2694	997.0000	summary/pts3/b-dut-tap.json	.4f	T(d, 0, 'f_hz')
2694	0.000	summary/pts3/b-dut-tap.json	z.3f	T(d, 0, 'ppm')
2694	-123.93	summary/pts3/b-dut-tap.json	.2f	T(d, 0, 'thdn_db')
2694	-109.31	summary/pts3/b-dut-tap.json	.2f	T(d, 0, 'worst')
2694	123.93	summary/pts3/b-dut-tap.json	.2f	T(d, 0, 'snr_db')
2694	9,973.0000	summary/pts3/b-dut-tap.json	,.4f	T(d, 1, 'f_hz')
2694	0.000	summary/pts3/b-dut-tap.json	z.3f	T(d, 1, 'ppm')
2694	-122.47	summary/pts3/b-dut-tap.json	.2f	T(d, 1, 'thdn_db')
2694	-89.46	summary/pts3/b-dut-tap.json	.2f	T(d, 1, 'worst')
2694	122.47	summary/pts3/b-dut-tap.json	.2f	T(d, 1, 'snr_db')
2695	480,000	summary/pts3/c-mcasp.json	,d	d['frames']
2695	-14.1035	summary/pts3/c-mcasp.json	.4f	T(d, 0, 'level_dbfs')
2695	997.0000	summary/pts3/c-mcasp.json	.4f	T(d, 0, 'f_hz')
2695	0.000	summary/pts3/c-mcasp.json	z.3f	T(d, 0, 'ppm')
2695	-123.97	summary/pts3/c-mcasp.json	.2f	T(d, 0, 'thdn_db')
2695	-110.32	summary/pts3/c-mcasp.json	.2f	T(d, 0, 'worst')
2695	123.98	summary/pts3/c-mcasp.json	.2f	T(d, 0, 'snr_db')
2695	9,973.0000	summary/pts3/c-mcasp.json	,.4f	T(d, 1, 'f_hz')
2695	0.000	summary/pts3/c-mcasp.json	z.3f	T(d, 1, 'ppm')
2695	-123.97	summary/pts3/c-mcasp.json	.2f	T(d, 1, 'thdn_db')
2695	-90.50	summary/pts3/c-mcasp.json	.2f	T(d, 1, 'worst')
2695	123.97	summary/pts3/c-mcasp.json	.2f	T(d, 1, 'snr_db')
2696	1,919,610	summary/b0-2/a-peer-tap.json	,d	d['frames']
2696	319,935	summary/b0-2/a-peer-tap.json	,d	d['info']['pdus']
2696	0	summary/b0-2/a-peer-tap.json	d	d['info']['seq_gaps']
2696	-14.1035	summary/b0-2/a-peer-tap.json	.4f	T(d, 0, 'level_dbfs')
2696	997.0000	summary/b0-2/a-peer-tap.json	.4f	T(d, 0, 'f_hz')
2696	0.000	summary/b0-2/a-peer-tap.json	z.3f	T(d, 0, 'ppm')
2696	-123.62	summary/b0-2/a-peer-tap.json	.2f	T(d, 0, 'thdn_db')
2696	-102.55	summary/b0-2/a-peer-tap.json	.2f	T(d, 0, 'worst')
2696	123.62	summary/b0-2/a-peer-tap.json	.2f	T(d, 0, 'snr_db')
2696	9,973.0000	summary/b0-2/a-peer-tap.json	,.4f	T(d, 1, 'f_hz')
2696	0.000	summary/b0-2/a-peer-tap.json	z.3f	T(d, 1, 'ppm')
2696	-114.29	summary/b0-2/a-peer-tap.json	.2f	T(d, 1, 'thdn_db')
2696	-82.58	summary/b0-2/a-peer-tap.json	.2f	T(d, 1, 'worst')
2696	114.29	summary/b0-2/a-peer-tap.json	.2f	T(d, 1, 'snr_db')
2697	1,919,592	summary/b0-2/b-dut-tap.json	,d	d['frames']
2697	319,932	summary/b0-2/b-dut-tap.json	,d	d['info']['pdus']
2697	0	summary/b0-2/b-dut-tap.json	d	d['info']['seq_gaps']
2697	-14.1035	summary/b0-2/b-dut-tap.json	.4f	T(d, 0, 'level_dbfs')
2697	997.0000	summary/b0-2/b-dut-tap.json	.4f	T(d, 0, 'f_hz')
2697	0.000	summary/b0-2/b-dut-tap.json	z.3f	T(d, 0, 'ppm')
2697	-123.62	summary/b0-2/b-dut-tap.json	.2f	T(d, 0, 'thdn_db')
2697	-102.15	summary/b0-2/b-dut-tap.json	.2f	T(d, 0, 'worst')
2697	123.62	summary/b0-2/b-dut-tap.json	.2f	T(d, 0, 'snr_db')
2697	9,973.0000	summary/b0-2/b-dut-tap.json	,.4f	T(d, 1, 'f_hz')
2697	0.000	summary/b0-2/b-dut-tap.json	z.3f	T(d, 1, 'ppm')
2697	-114.33	summary/b0-2/b-dut-tap.json	.2f	T(d, 1, 'thdn_db')
2697	-82.18	summary/b0-2/b-dut-tap.json	.2f	T(d, 1, 'worst')
2697	114.33	summary/b0-2/b-dut-tap.json	.2f	T(d, 1, 'snr_db')
2698	14,400,000	summary/b0-2/c-mcasp.json	,d	d['frames']
2698	-14.1035	summary/b0-2/c-mcasp.json	.4f	T(d, 0, 'level_dbfs')
2698	997.0000	summary/b0-2/c-mcasp.json	.4f	T(d, 0, 'f_hz')
2698	0.000	summary/b0-2/c-mcasp.json	z.3f	T(d, 0, 'ppm')
2698	-123.95	summary/b0-2/c-mcasp.json	.2f	T(d, 0, 'thdn_db')
2698	-100.47	summary/b0-2/c-mcasp.json	.2f	T(d, 0, 'worst')
2698	123.95	summary/b0-2/c-mcasp.json	.2f	T(d, 0, 'snr_db')
2698	9,973.0000	summary/b0-2/c-mcasp.json	,.4f	T(d, 1, 'f_hz')
2698	0.000	summary/b0-2/c-mcasp.json	z.3f	T(d, 1, 'ppm')
2698	-122.80	summary/b0-2/c-mcasp.json	.2f	T(d, 1, 'thdn_db')
2698	-80.48	summary/b0-2/c-mcasp.json	.2f	T(d, 1, 'worst')
2698	122.80	summary/b0-2/c-mcasp.json	.2f	T(d, 1, 'snr_db')
2787	300	summary/b0-2/c-b9-grade.json	d	d['summary']['blocks']
2787	0	summary/b0-2/c-b9-grade.json	d#1	d['summary']['events']
2787	169	summary/b0-2/c-b9-grade.json	d	d['summary']['blocks_at_floor']
2787	-123.98	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch0_floor']['thdn_db_median']
2787	-123.91	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch0_floor']['thdn_db_worst']
2787	123.98	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch0_floor']['snr_db_median']
2787	-123.95	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch0_all']['thdn_db_median']
2787	-100.47	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch0_all']['thdn_db_worst']
2787	-14.10	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch0_all']['level_dbfs_median']
2787	0.0000	summary/b0-2/c-b9-grade.json	z.4f	d['summary']['ch0_all']['ppm_median']
2787	0.030	summary/b0-2/c-b9-grade.json	.3f	d['summary']['ch0_all']['ppm_maxabs']
2788	300	summary/b0-2/c-b9-grade.json	d	d['summary']['blocks']
2788	0	summary/b0-2/c-b9-grade.json	d#0	d['summary']['events']
2788	169	summary/b0-2/c-b9-grade.json	d	d['summary']['blocks_at_floor']
2788	-123.95	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch1_floor']['thdn_db_median']
2788	-120.18	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch1_floor']['thdn_db_worst']
2788	123.95	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch1_floor']['snr_db_median']
2788	-122.80	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch1_all']['thdn_db_median']
2788	-80.48	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch1_all']['thdn_db_worst']
2788	-14.10	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch1_all']['level_dbfs_median']
2788	0.0000	summary/b0-2/c-b9-grade.json	z.4f	d['summary']['ch1_all']['ppm_median']
2788	0.030	summary/b0-2/c-b9-grade.json	.3f	d['summary']['ch1_all']['ppm_maxabs']
3081	1,919,598	summary/bcrf/a-peer-tap.json	,d	d['frames']
3081	319,933	summary/bcrf/a-peer-tap.json	,d	d['info']['pdus']
3081	0	summary/bcrf/a-peer-tap.json	d	d['info']['seq_gaps']
3081	-14.1035	summary/bcrf/a-peer-tap.json	.4f	T(d, 0, 'level_dbfs')
3081	997.0000	summary/bcrf/a-peer-tap.json	.4f	T(d, 0, 'f_hz')
3081	0.000	summary/bcrf/a-peer-tap.json	z.3f	T(d, 0, 'ppm')
3081	-123.98	summary/bcrf/a-peer-tap.json	.2f	T(d, 0, 'thdn_db')
3081	-123.93	summary/bcrf/a-peer-tap.json	.2f	T(d, 0, 'worst')
3081	123.99	summary/bcrf/a-peer-tap.json	.2f	T(d, 0, 'snr_db')
3081	9,973.0000	summary/bcrf/a-peer-tap.json	,.4f	T(d, 1, 'f_hz')
3081	0.000	summary/bcrf/a-peer-tap.json	z.3f	T(d, 1, 'ppm')
3081	-123.97	summary/bcrf/a-peer-tap.json	.2f	T(d, 1, 'thdn_db')
3081	-123.93	summary/bcrf/a-peer-tap.json	.2f	T(d, 1, 'worst')
3081	123.97	summary/bcrf/a-peer-tap.json	.2f	T(d, 1, 'snr_db')
3082	1,919,574	summary/bcrf/b-dut-tap.json	,d	d['frames']
3082	319,929	summary/bcrf/b-dut-tap.json	,d	d['info']['pdus']
3082	0	summary/bcrf/b-dut-tap.json	d	d['info']['seq_gaps']
3082	-14.1035	summary/bcrf/b-dut-tap.json	.4f	T(d, 0, 'level_dbfs')
3082	997.0000	summary/bcrf/b-dut-tap.json	.4f	T(d, 0, 'f_hz')
3082	0.000	summary/bcrf/b-dut-tap.json	z.3f	T(d, 0, 'ppm')
3082	-123.99	summary/bcrf/b-dut-tap.json	.2f	T(d, 0, 'thdn_db')
3082	-123.93	summary/bcrf/b-dut-tap.json	.2f	T(d, 0, 'worst')
3082	123.99	summary/bcrf/b-dut-tap.json	.2f	T(d, 0, 'snr_db')
3082	9,973.0000	summary/bcrf/b-dut-tap.json	,.4f	T(d, 1, 'f_hz')
3082	0.000	summary/bcrf/b-dut-tap.json	z.3f	T(d, 1, 'ppm')
3082	-123.97	summary/bcrf/b-dut-tap.json	.2f	T(d, 1, 'thdn_db')
3082	-123.93	summary/bcrf/b-dut-tap.json	.2f	T(d, 1, 'worst')
3082	123.97	summary/bcrf/b-dut-tap.json	.2f	T(d, 1, 'snr_db')
3083	14,400,000	summary/bcrf/c-mcasp.json	,d	d['frames']
3083	-14.1035	summary/bcrf/c-mcasp.json	.4f	T(d, 0, 'level_dbfs')
3083	997.0000	summary/bcrf/c-mcasp.json	.4f	T(d, 0, 'f_hz')
3083	0.000	summary/bcrf/c-mcasp.json	z.3f	T(d, 0, 'ppm')
3083	-123.98	summary/bcrf/c-mcasp.json	.2f	T(d, 0, 'thdn_db')
3083	-123.93	summary/bcrf/c-mcasp.json	.2f	T(d, 0, 'worst')
3083	123.99	summary/bcrf/c-mcasp.json	.2f	T(d, 0, 'snr_db')
3083	9,973.0000	summary/bcrf/c-mcasp.json	,.4f	T(d, 1, 'f_hz')
3083	0.000	summary/bcrf/c-mcasp.json	z.3f	T(d, 1, 'ppm')
3083	-123.97	summary/bcrf/c-mcasp.json	.2f	T(d, 1, 'thdn_db')
3083	-123.90	summary/bcrf/c-mcasp.json	.2f	T(d, 1, 'worst')
3083	123.97	summary/bcrf/c-mcasp.json	.2f	T(d, 1, 'snr_db')
3084	1,919,598	summary/baaf/a-peer-tap.json	,d	d['frames']
3084	319,933	summary/baaf/a-peer-tap.json	,d	d['info']['pdus']
3084	0	summary/baaf/a-peer-tap.json	d	d['info']['seq_gaps']
3084	-14.1035	summary/baaf/a-peer-tap.json	.4f	T(d, 0, 'level_dbfs')
3084	997.0000	summary/baaf/a-peer-tap.json	.4f	T(d, 0, 'f_hz')
3084	0.000	summary/baaf/a-peer-tap.json	z.3f	T(d, 0, 'ppm')
3084	-123.98	summary/baaf/a-peer-tap.json	.2f	T(d, 0, 'thdn_db')
3084	-123.93	summary/baaf/a-peer-tap.json	.2f	T(d, 0, 'worst')
3084	123.98	summary/baaf/a-peer-tap.json	.2f	T(d, 0, 'snr_db')
3084	9,973.0000	summary/baaf/a-peer-tap.json	,.4f	T(d, 1, 'f_hz')
3084	0.000	summary/baaf/a-peer-tap.json	z.3f	T(d, 1, 'ppm')
3084	-123.98	summary/baaf/a-peer-tap.json	.2f	T(d, 1, 'thdn_db')
3084	-123.93	summary/baaf/a-peer-tap.json	.2f	T(d, 1, 'worst')
3084	123.98	summary/baaf/a-peer-tap.json	.2f	T(d, 1, 'snr_db')
3085	1,919,580	summary/baaf/b-dut-tap.json	,d	d['frames']
3085	319,930	summary/baaf/b-dut-tap.json	,d	d['info']['pdus']
3085	0	summary/baaf/b-dut-tap.json	d	d['info']['seq_gaps']
3085	-14.1035	summary/baaf/b-dut-tap.json	.4f	T(d, 0, 'level_dbfs')
3085	997.0000	summary/baaf/b-dut-tap.json	.4f	T(d, 0, 'f_hz')
3085	0.000	summary/baaf/b-dut-tap.json	z.3f	T(d, 0, 'ppm')
3085	-123.98	summary/baaf/b-dut-tap.json	.2f	T(d, 0, 'thdn_db')
3085	-123.92	summary/baaf/b-dut-tap.json	.2f	T(d, 0, 'worst')
3085	123.98	summary/baaf/b-dut-tap.json	.2f	T(d, 0, 'snr_db')
3085	9,973.0000	summary/baaf/b-dut-tap.json	,.4f	T(d, 1, 'f_hz')
3085	0.000	summary/baaf/b-dut-tap.json	z.3f	T(d, 1, 'ppm')
3085	-123.98	summary/baaf/b-dut-tap.json	.2f	T(d, 1, 'thdn_db')
3085	-123.93	summary/baaf/b-dut-tap.json	.2f	T(d, 1, 'worst')
3085	123.98	summary/baaf/b-dut-tap.json	.2f	T(d, 1, 'snr_db')
3086	14,400,000	summary/baaf/c-mcasp.json	,d	d['frames']
3086	-14.1035	summary/baaf/c-mcasp.json	.4f	T(d, 0, 'level_dbfs')
3086	997.0000	summary/baaf/c-mcasp.json	.4f	T(d, 0, 'f_hz')
3086	0.000	summary/baaf/c-mcasp.json	z.3f	T(d, 0, 'ppm')
3086	-123.98	summary/baaf/c-mcasp.json	.2f	T(d, 0, 'thdn_db')
3086	-123.92	summary/baaf/c-mcasp.json	.2f	T(d, 0, 'worst')
3086	123.99	summary/baaf/c-mcasp.json	.2f	T(d, 0, 'snr_db')
3086	9,973.0000	summary/baaf/c-mcasp.json	,.4f	T(d, 1, 'f_hz')
3086	0.000	summary/baaf/c-mcasp.json	z.3f	T(d, 1, 'ppm')
3086	-123.97	summary/baaf/c-mcasp.json	.2f	T(d, 1, 'thdn_db')
3086	-123.91	summary/baaf/c-mcasp.json	.2f	T(d, 1, 'worst')
3086	123.97	summary/baaf/c-mcasp.json	.2f	T(d, 1, 'snr_db')
3087	1,919,610	summary/b0-2/a-peer-tap.json	,d	d['frames']
3087	319,935	summary/b0-2/a-peer-tap.json	,d	d['info']['pdus']
3087	0	summary/b0-2/a-peer-tap.json	d	d['info']['seq_gaps']
3087	-14.1035	summary/b0-2/a-peer-tap.json	.4f	T(d, 0, 'level_dbfs')
3087	997.0000	summary/b0-2/a-peer-tap.json	.4f	T(d, 0, 'f_hz')
3087	0.000	summary/b0-2/a-peer-tap.json	z.3f	T(d, 0, 'ppm')
3087	-123.62	summary/b0-2/a-peer-tap.json	.2f	T(d, 0, 'thdn_db')
3087	-102.55	summary/b0-2/a-peer-tap.json	.2f	T(d, 0, 'worst')
3087	123.62	summary/b0-2/a-peer-tap.json	.2f	T(d, 0, 'snr_db')
3087	9,973.0000	summary/b0-2/a-peer-tap.json	,.4f	T(d, 1, 'f_hz')
3087	0.000	summary/b0-2/a-peer-tap.json	z.3f	T(d, 1, 'ppm')
3087	-114.29	summary/b0-2/a-peer-tap.json	.2f	T(d, 1, 'thdn_db')
3087	-82.58	summary/b0-2/a-peer-tap.json	.2f	T(d, 1, 'worst')
3087	114.29	summary/b0-2/a-peer-tap.json	.2f	T(d, 1, 'snr_db')
3088	14,400,000	summary/b0-2/c-mcasp.json	,d	d['frames']
3088	-14.1035	summary/b0-2/c-mcasp.json	.4f	T(d, 0, 'level_dbfs')
3088	997.0000	summary/b0-2/c-mcasp.json	.4f	T(d, 0, 'f_hz')
3088	0.000	summary/b0-2/c-mcasp.json	z.3f	T(d, 0, 'ppm')
3088	-123.95	summary/b0-2/c-mcasp.json	.2f	T(d, 0, 'thdn_db')
3088	-100.47	summary/b0-2/c-mcasp.json	.2f	T(d, 0, 'worst')
3088	123.95	summary/b0-2/c-mcasp.json	.2f	T(d, 0, 'snr_db')
3088	9,973.0000	summary/b0-2/c-mcasp.json	,.4f	T(d, 1, 'f_hz')
3088	0.000	summary/b0-2/c-mcasp.json	z.3f	T(d, 1, 'ppm')
3088	-122.80	summary/b0-2/c-mcasp.json	.2f	T(d, 1, 'thdn_db')
3088	-80.48	summary/b0-2/c-mcasp.json	.2f	T(d, 1, 'worst')
3088	122.80	summary/b0-2/c-mcasp.json	.2f	T(d, 1, 'snr_db')
3098	300	summary/bcrf/c-b9-grade.json	d	d['summary']['blocks']
3098	0	summary/bcrf/c-b9-grade.json	d#1	d['summary']['events']
3098	300	summary/bcrf/c-b9-grade.json	d	d['summary']['blocks_at_floor']
3098	-123.98	summary/bcrf/c-b9-grade.json	.2f	d['summary']['ch0_floor']['thdn_db_median']
3098	-123.93	summary/bcrf/c-b9-grade.json	.2f	d['summary']['ch0_floor']['thdn_db_worst']
3098	123.99	summary/bcrf/c-b9-grade.json	.2f	d['summary']['ch0_floor']['snr_db_median']
3098	-123.98	summary/bcrf/c-b9-grade.json	.2f	d['summary']['ch0_all']['thdn_db_median']
3098	-123.93	summary/bcrf/c-b9-grade.json	.2f	d['summary']['ch0_all']['thdn_db_worst']
3098	-14.10	summary/bcrf/c-b9-grade.json	.2f	d['summary']['ch0_all']['level_dbfs_median']
3098	0.0000	summary/bcrf/c-b9-grade.json	z.4f	d['summary']['ch0_all']['ppm_median']
3098	0.000	summary/bcrf/c-b9-grade.json	.3f	d['summary']['ch0_all']['ppm_maxabs']
3099	300	summary/bcrf/c-b9-grade.json	d	d['summary']['blocks']
3099	0	summary/bcrf/c-b9-grade.json	d#0	d['summary']['events']
3099	300	summary/bcrf/c-b9-grade.json	d	d['summary']['blocks_at_floor']
3099	-123.97	summary/bcrf/c-b9-grade.json	.2f	d['summary']['ch1_floor']['thdn_db_median']
3099	-123.90	summary/bcrf/c-b9-grade.json	.2f	d['summary']['ch1_floor']['thdn_db_worst']
3099	123.97	summary/bcrf/c-b9-grade.json	.2f	d['summary']['ch1_floor']['snr_db_median']
3099	-123.97	summary/bcrf/c-b9-grade.json	.2f	d['summary']['ch1_all']['thdn_db_median']
3099	-123.90	summary/bcrf/c-b9-grade.json	.2f	d['summary']['ch1_all']['thdn_db_worst']
3099	-14.10	summary/bcrf/c-b9-grade.json	.2f	d['summary']['ch1_all']['level_dbfs_median']
3099	0.0000	summary/bcrf/c-b9-grade.json	z.4f	d['summary']['ch1_all']['ppm_median']
3099	0.000	summary/bcrf/c-b9-grade.json	.3f	d['summary']['ch1_all']['ppm_maxabs']
3100	300	summary/baaf/c-b9-grade.json	d	d['summary']['blocks']
3100	0	summary/baaf/c-b9-grade.json	d#1	d['summary']['events']
3100	300	summary/baaf/c-b9-grade.json	d	d['summary']['blocks_at_floor']
3100	-123.98	summary/baaf/c-b9-grade.json	.2f	d['summary']['ch0_floor']['thdn_db_median']
3100	-123.92	summary/baaf/c-b9-grade.json	.2f	d['summary']['ch0_floor']['thdn_db_worst']
3100	123.99	summary/baaf/c-b9-grade.json	.2f	d['summary']['ch0_floor']['snr_db_median']
3100	-123.98	summary/baaf/c-b9-grade.json	.2f	d['summary']['ch0_all']['thdn_db_median']
3100	-123.92	summary/baaf/c-b9-grade.json	.2f	d['summary']['ch0_all']['thdn_db_worst']
3100	-14.10	summary/baaf/c-b9-grade.json	.2f	d['summary']['ch0_all']['level_dbfs_median']
3100	0.0000	summary/baaf/c-b9-grade.json	z.4f	d['summary']['ch0_all']['ppm_median']
3100	0.000	summary/baaf/c-b9-grade.json	.3f	d['summary']['ch0_all']['ppm_maxabs']
3101	300	summary/baaf/c-b9-grade.json	d	d['summary']['blocks']
3101	0	summary/baaf/c-b9-grade.json	d#0	d['summary']['events']
3101	300	summary/baaf/c-b9-grade.json	d	d['summary']['blocks_at_floor']
3101	-123.97	summary/baaf/c-b9-grade.json	.2f	d['summary']['ch1_floor']['thdn_db_median']
3101	-123.91	summary/baaf/c-b9-grade.json	.2f	d['summary']['ch1_floor']['thdn_db_worst']
3101	123.97	summary/baaf/c-b9-grade.json	.2f	d['summary']['ch1_floor']['snr_db_median']
3101	-123.97	summary/baaf/c-b9-grade.json	.2f	d['summary']['ch1_all']['thdn_db_median']
3101	-123.91	summary/baaf/c-b9-grade.json	.2f	d['summary']['ch1_all']['thdn_db_worst']
3101	-14.10	summary/baaf/c-b9-grade.json	.2f	d['summary']['ch1_all']['level_dbfs_median']
3101	0.0000	summary/baaf/c-b9-grade.json	z.4f	d['summary']['ch1_all']['ppm_median']
3101	0.000	summary/baaf/c-b9-grade.json	.3f	d['summary']['ch1_all']['ppm_maxabs']
3102	300	summary/b0-2/c-b9-grade.json	d	d['summary']['blocks']
3102	0	summary/b0-2/c-b9-grade.json	d#1	d['summary']['events']
3102	169	summary/b0-2/c-b9-grade.json	d	d['summary']['blocks_at_floor']
3102	-123.98	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch0_floor']['thdn_db_median']
3102	-123.91	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch0_floor']['thdn_db_worst']
3102	123.98	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch0_floor']['snr_db_median']
3102	-123.95	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch0_all']['thdn_db_median']
3102	-100.47	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch0_all']['thdn_db_worst']
3102	-14.10	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch0_all']['level_dbfs_median']
3102	0.0000	summary/b0-2/c-b9-grade.json	z.4f	d['summary']['ch0_all']['ppm_median']
3102	0.030	summary/b0-2/c-b9-grade.json	.3f	d['summary']['ch0_all']['ppm_maxabs']
3103	300	summary/b0-2/c-b9-grade.json	d	d['summary']['blocks']
3103	0	summary/b0-2/c-b9-grade.json	d#0	d['summary']['events']
3103	169	summary/b0-2/c-b9-grade.json	d	d['summary']['blocks_at_floor']
3103	-123.95	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch1_floor']['thdn_db_median']
3103	-120.18	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch1_floor']['thdn_db_worst']
3103	123.95	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch1_floor']['snr_db_median']
3103	-122.80	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch1_all']['thdn_db_median']
3103	-80.48	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch1_all']['thdn_db_worst']
3103	-14.10	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch1_all']['level_dbfs_median']
3103	0.0000	summary/b0-2/c-b9-grade.json	z.4f	d['summary']['ch1_all']['ppm_median']
3103	0.030	summary/b0-2/c-b9-grade.json	.3f	d['summary']['ch1_all']['ppm_maxabs']
# ROWS-END
"""


def parse_rows():
    rows = []
    for x in ROWS_TSV.strip("\n").splitlines():
        if not x or x.startswith("#"):
            continue
        line, shown, src, spec, key = x.split("\t", 4)
        spec, _, k = spec.partition("#")
        rows.append((line, shown, src, key, spec, int(k) if k else None))
    return rows


ROWS = parse_rows()

# ---------------------------------------------------------------- coverage
TOKEN = re.compile(
    r"(?<![\w/#.+\-])(?:"
    r"(?P<sha>[0-9a-f]{64})|(?P<abbr>[0-9a-f]{8}\.\.\.)|"
    r"(?P<hex>0x(?:\.\.\.)?[0-9a-fA-F]+)|"
    r"(?P<date>\d{4}-\d\d-\d\d)|(?P<time>\d\d:\d\d(?::\d\d(?:\.\d+)?)?)|(?P<ver>\d+\.\d+\.\d+)|"
    r"(?P<num>[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:/[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)*)"
    r")(?![\w])"
    r"|(?<=`)(?P<id>[0-9a-f]{6,16})(?=`)"
    r"|\b(?P<word>(?i:" + "|".join(WORDS[1:]) + r"|once|twice))\b")

# (category, regex). A token is covered by a category when a match's group `t` spans exactly that token, or,
# for a regex with no group `t`, when the token lies inside a match (a link, its anchor or its URL).
EXCLUDE = []


def X(cat, rx):
    EXCLUDE.append((cat, re.compile(rx)))


# EXCLUDE-BEGIN
X("commit", r"`(?P<t>5603c353|694d7da6|0d4ff919|e20fd282|35e332b6|c20c85bd|e8454e27)`")
X("ordinal", r"\b(?:[Ss]teps?|[Rr]ounds?) (?P<t>\d+)\b")
X("ordinal", r"\b[Ss]teps \d+ and (?P<t>\d+)\b")
X("ordinal", r"^(?P<t>\d+)\. ")
X("citation", r"IEEE (?P<t>1722\.1)")
X("citation", r"Milan v1\.2 Table (?P<t>5\.4)")
X("descriptor index", r"\b(?:STREAM_INPUT|STREAM_OUTPUT|STREAM_PORT_INPUT|STREAM_PORT_OUTPUT|CLOCK_DOMAIN|ENTITY|CONFIGURATION) (?P<t>\d+)\b")
X("channel index", r"\b[Cc]hannels? (?P<t>\d+)\b")
X("channel index", r"\b[Cc]hannels \d+ (?:and|to) (?P<t>\d+)\b")
X("tone name", r"(?P<t>997|9,973|997/9,973) Hz\b")
X("register address", r"(?P<t>0x[0-9A-F]{3})\b")
X("bit index", r"\[(?P<t>\d+)(?::\d+)?\]")
X("bit index", r"\bbit (?P<t>\d+)\b")
X("packet name", r"`(?P<t>629)-b16-a603`")
X("link", r"\[[^\]]*\]\([^)]*\)")
X("link", r"\(#[a-z0-9-]+\)")
X("unit", r"\b(?P<t>one)-(?:LSB|second)\b")
X("unit", r"\b(?P<t>24)-bit\b")
X("pronoun", r"\beach (?P<t>one)\b")
X("bench", r"\bon (?P<t>one) (?:DUT and one )?reference peer\b")
X("bench", r"\bon one DUT and (?P<t>one) reference peer\b")
X("method name", r"\b(?P<t>four)-point\b")
X("idiom", r"\bat (?P<t>once)\b")
X("idiom", r"\b(?P<t>once) the\b")
X("linked ruling's date", r"^on (?P<t>2026-10-12)\. ")
X("bench rule", r"\bwithin (?P<t>10) minutes\b")
X("heading", r"^#+ .*$")
X("the two following cases, B-CRF and B-AAF", r"\b(?:these|the) (?P<t>two) cases\b")
X("phrase", r"\bon (?P<t>one) clock\b")
X("phrase", r"\b(?P<t>one) state of it\b")
X("the two following cases, B-CRF and B-AAF", r"\bthese (?P<t>two)$")
X("the four capture points, (a) to (d)", r"\b[Tt]he (?P<t>four) points\b")
X("the two modes it names", r"\b(?P<t>two) modes added, `bcrf` and$")
X("channel index", r"^(?P<t>3) carry -1 to 0 LSB")
X("phrase", r"\bthe (?P<t>two) clocks' difference\b")
X("phrase", r"\bdo not separate the (?P<t>two)\b")
X("pronoun", r"\bthe published (?P<t>one)\b")
X("the reviews it links", r"^(?P<t>Two) reviews of this section,$")
X("the reviews it links", r"^(?P<t>Two) reviews of round 2,$")
X("the figure check's rule", r"\b(?P<t>one) row per quoted figure\b")
X("the figure check's rule", r"\bevery (?P<t>one)\b")
X("unit", r"\"(?P<t>24)-bit\"")
X("the round it names", r"\bround (?P<t>2),$")
X("the figure check's rule", r"\b(?P<t>one) line per row\b")
X("a quoted phrase", r'"[^"]*"')
X("unit", r"\b(?P<t>One) frame in 14\.58 million\b")
X("unit", r"\bbelow (?P<t>one) frame in 14\.58 million\b")
# EXCLUDE-END


def scope():
    """Every line the check covers, as (document, line) -> (text, the column its covered part starts at): lane
    B16's section of the findings page, the page's introduction on lane B16 and its Contents entry, and the
    lane B16 part of the page's row in docs/findings/README.md."""
    f = DOC_P.read_text(encoding="utf-8").splitlines()
    r = README_P.read_text(encoding="utf-8").splitlines()
    out = {}
    s = next(i for i, x in enumerate(f) if x.startswith(SECTION))
    e = next((i for i in range(s + 1, len(f)) if f[i].startswith("## ")), len(f))
    for i in range(s, e):
        out[(DOC_P.name, i + 1)] = (f[i], 0)
    i = next(i for i, x in enumerate(f) if x.startswith("Lane B16 tried the reference peer's own loopback"))
    while f[i].strip():
        out[(DOC_P.name, i + 1)] = (f[i], 0)
        i += 1
    i = next(i for i, x in enumerate(f) if x.startswith("- **[Dev 5603c353, 2026-10-12: lane B16]"))
    out[(DOC_P.name, i + 1)] = (f[i], 0)
    i = next(i for i, x in enumerate(r) if x.startswith("| [629_MEDIA_CLOCK_FOLLOWING_BENCH.md]"))
    out[(README_P.name, i + 1)] = (r[i], r[i].index("Lane B16, `5603c353`:"))
    return out


def where(line):
    """A row's line field: a findings-page line number, or README.md:<line>."""
    doc, _, n = line.rpartition(":")
    return (doc or DOC_P.name, int(n))


def main():
    lines = scope()
    toks = {w: [(m.start(), m.end(), m.group(0)) for m in TOKEN.finditer(text) if m.start() >= at]
            for w, (text, at) in lines.items()}
    claimed = {w: set() for w in toks}
    out, bad = [], 0
    for n, (line, shown, src, key, spec, k) in enumerate(ROWS, 1):
        status, val = "OK", ""
        _read.clear()
        try:
            w = where(line)
            assert w in toks, "line outside the covered text"
            same_ = [t for t in toks[w] if t[2] == shown]
            hit = same_[k] if k is not None and k < len(same_) else (
                None if k is not None else next((t for t in same_ if t[:2] not in claimed[w]), None))
            assert hit and hit[:2] not in claimed[w], "figure not on the line, or claimed twice"
            claimed[w].add(hit[:2])
            d = load(src) if src else None
            v = eval(key, dict(globals(), d=d, p=src))
            val = fmt(v, spec)
            if val != shown:
                status = "MISMATCH"
        except Exception as exc:
            status = f"ERROR {type(exc).__name__}: {exc}"
        bad += status != "OK"
        out.append("\t".join([str(n), line, shown, src or "; ".join(_read) or "-", spec + ("" if k is None else f"#{k}"),
                              val, status]))
    cov, uncovered = [], []
    for w, ts in toks.items():
        for a, b, text in ts:
            if (a, b) in claimed[w]:
                continue
            cat = next((c for c, rx in EXCLUDE
                        if any((m.span("t") == (a, b)) if "t" in rx.groupindex else (m.start() <= a and b <= m.end())
                               for m in rx.finditer(lines[w][0]))), None)
            if cat:
                cov.append("\t".join([f"{w[0]}:{w[1]}", text, cat]))
            else:
                uncovered.append((w, text))
    with open(OUT_ROWS, "w") as f:
        f.write("# check_b16_figures.py rows, in ROWS_TSV's order: row, line, shown, receipt, precision, recomputed, status\n")
        f.write("\n".join(out) + "\n")
    with open(OUT_COV, "w") as f:
        f.write("# check_b16_figures.py coverage: line, token, identifier category (the tokens no row claims)\n")
        f.write("\n".join(cov) + "\n")
        for w, text in uncovered:
            f.write(f"{w[0]}:{w[1]}\t{text}\tUNCOVERED\n")
    print(json.dumps(dict(lines=len(lines), tokens=sum(len(t) for t in toks.values()), rows=len(ROWS),
                          rows_ok=len(ROWS) - bad, rows_bad=bad, by_category=len(cov), uncovered=len(uncovered))))
    cap = int(OPTS.get("--show", 40))
    for x in [x for x in out if not x.endswith("\tOK")][:cap]:
        print("BAD", x)
    for w, text in uncovered[:cap]:
        print("UNCOVERED", f"{w[0]}:{w[1]}", text, "|", lines[w][0][:160])
    return 0 if not bad and not uncovered else 1


if __name__ == "__main__":
    sys.exit(main())
