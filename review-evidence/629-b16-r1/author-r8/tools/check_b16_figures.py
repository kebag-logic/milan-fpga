#!/usr/bin/env python3
"""Lane B16, rounds 3 to 8: every quoted figure of lane B16's findings, recomputed from its receipt.

usage: <parser python> check_b16_figures.py <findings.md> <packet root> <out rows.tsv> <out coverage.tsv>
                                            [--repo <root>] [--show <n>]

<parser python> has tools/markdown/requirements.txt installed by hash. The text covered: the section "Dev
5603c353, 2026-10-12: lane B16" of docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md, the page's introduction
on lane B16 and its Contents entry, and the lane B16 part of the page's row in the README.md beside it. That
section states each rule, round by round.

ROWS_TSV: one row per quoted figure, its line, the figure as shown, the receipt (a packet file, repo:<path>
or git:<commit>:<path>; ^, the row above's), the displayed precision and the key. The figure must be the
whole number on its line and equal what the key recomputes, rounded half up on exact decimals (clock times,
CEST, cut to the last digit shown).

Round 8: both documents are parsed whole by the repository's pinned Markdown parser, verified as the
documentation gates verify it; only its visible inline text is judged (text, code spans, link text), and
a construct off ALLOWED is refused at its line as MARKUP. Coverage: every digit must lie in a figure a row
claims or in an identifier a category of EXCLUDE binds and the closed list follows (follows); a number
before a unit (MEASURE) is a measurement only a row may claim. Anything else is UNCOVERED.

--repo: the repository root (default: the one holding <findings.md>); --show caps the failures printed
(default 40). Exit 0 when every row matches, every digit is covered and nothing is refused; 1 otherwise, or
without the pinned parser. Outputs: each row with its recomputed value and status; each identifier that
covers a digit, then each UNCOVERED number, then each refused construct (MARKUP). No private file or raw
capture is read.
"""
import datetime
import hashlib
import importlib.metadata
import importlib.util
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
TENS = ["thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "thousand"]  # round 4: tokens too

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


def passed(d):
    return sum(c["verdict"] == "PASS" for c in d["controls"])


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


class Cases(Exception):
    """Round 6: cases one figure stands for, which do not share its value; the row is a MISMATCH naming each."""


def each(pairs):
    """Round 6: one figure for several cases, each (case, value) read from that case's own receipt: the value
    they share, or a MISMATCH that names every case's value."""
    vals = list(pairs)
    if not vals or any(v != vals[0][1] for _, v in vals):
        raise Cases(", ".join(f"{c} {v}" for c, v in vals))
    return vals[0][1]


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


# Round 4: receipts for figures round 3 left to a category.
def tone_hz(i):
    """The i-th tone's frequency in Hz: the tone tool's (b6_tone.py, whose tone b9_tone.py plays) and the
    analyser's (tone_points_b16.py), which must agree."""
    return same([int(rx("tools/b6_tone.py", r"^F0, F1 = (\d+), (\d+)$", group=i + 1)),
                 int(rx("tools/tone_points_b16.py", r"^TONES = \((\d+), (\d+)\)$", group=i + 1))])


def points(run):
    """The capture points a run's summaries hold, (a) to (d): the letters of its summary/<run>/<p>-*.json."""
    return len({p.name[0] for p in (ROOT / f"summary/{run}").glob("[a-d]-*.json")})


def cmp_bits(runs):
    """The bit width align_b16.py compared at, from each of the runs' alignment summaries."""
    return same(int(re.fullmatch(r"full (\d+)-bit values", align(r, p)["comparison"]).group(1))
                for r in runs for p in "ab" if (ROOT / f"summary/{r}/align-{p}-c.json").exists())


def blk_grade(runs):
    """Seconds per block of b9_thdn.py's grade at (c): the recording's seconds over its blocks."""
    return same(Decimal(grade(r)["seconds"]) / grade(r)["summary"]["blocks"] for r in runs)


def blk_points(runs):
    """Seconds per block of tone_points_b16.py at McASP0, both tones: the recording's seconds over its blocks."""
    return same(Decimal(load(f"summary/{r}/c-mcasp.json")["seconds"]) / T(load(f"summary/{r}/c-mcasp.json"), ch, "rec")["blocks"]
                for r in runs for ch in (0, 1))


def step_frames():
    """The step, in frames, of each event dloop_b16.py's planted control finds."""
    return same(e["frames"] for e in load("controls/b16b-dloop-control.json")["result"]["events"])


def lock_limit():
    """The lane's limit on one locked action, in minutes, as the operator's record states it."""
    return same(int(x) for x in re.findall(r"one locked action must end within (\d+) minutes", load("HANDOFF.md")))


CENSUS_VOLATILE = {"t", "seq", "rtt_ms", "sequence_id", "t_tx", "t_rx"}  # census_cmp.py's VOLATILE


def census_reads(a, b, cmp):
    """Two census files' reads after their start records, compared by census_cmp.py's rule: (equal,
    compared). Each file holds its start record once, and `cmp` counts exactly one more of each."""
    def strip(o):
        if isinstance(o, dict):
            return {k: strip(v) for k, v in o.items() if k not in CENSUS_VOLATILE}
        if isinstance(o, list):
            return [strip(v) for v in o]
        return o
    A, B = [strip(x) for x in load(a)], [strip(x) for x in load(b)]
    assert A[0].get("type") == "start" == B[0].get("type") and not any("type" in x for x in A[1:] + B[1:])
    assert len(A) == len(B) and A[0] == B[0]
    out = sum(x == y for x, y in zip(A[1:], B[1:])), len(A) - 1
    assert (out[0] + 1, out[1] + 1) == (int(rx(cmp, r'"same": (\d+)')), int(rx(cmp, r'"compared": (\d+)'))), cmp
    return out


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
# Tab-separated: line, shown, receipt (empty: the key names its files), precision (#k: the k-th occurrence on
# the line), key (d, the loaded receipt; p, its path). Precisions: a format spec (z drops a zero's sign), s, w
# or W (a number word), x (once, twice), date, cest (HH:MM:SS), cest1 (tenths), hm (HH:MM).
ROWS_TSV = r"""
# ROWS-BEGIN
# lane B16: heading and summary
2287	2026-10-12		date	stamps('identity/lock-window.txt', 'LOCK')[0]
2289	2026-10-12		date	stamps('identity/lock-window.txt', 'LOCK')[0]
2317	8	controls/b16-tap-controls.json	d#0	sum(c['result'] == 'PASS' for c in d['controls'])
2317	8	^	d#1	len(d['controls'])
2317	6	controls/b16-align-controls-synth.json	d#0	sum(c['result'] == 'PASS' for c in d['controls'])
2317	6	^	d#1	len(d['controls'])
2318	Two	runs/loop1/events.jsonl	W	sum(1 for r in RUNS for b in ev(r, 'bind') if b['talker'] == 'peer-out-0' and b['listener'] == 'peer-in-0')
2319	twice	summary/loop2/acmp-peer-tap.json	x	sum(x['msg'] == 'CONNECT_TX_COMMAND' for x in d['acmp'])
2319	200	^	.0f	(lambda p: (p[1]['t'] - p[0]['t']) * 1000)([x for x in d['acmp'] if x['msg'] == 'CONNECT_TX_COMMAND'])
# B16: identity and setup
2334	020000fffe000001	identity/identity-verdict.txt	s	get(d, 'check=atdecc-entity_id.detail.read')
2334	2.96.0	^	s	get(d, 'check=atdecc-firmware_version.detail.read')
2335	4d494c4e	^	s	get(d, 'check=console-id.detail.read.0')
2335	0x00020060	^	s	'0x' + get(d, 'check=console-id.detail.read.1')
2336	7,512		,d	rx('identity/console-identity.txt', r"cmd='crc 0x[0-9a-f]+ (\d+)'")
2336	5ba355eb	identity/identity-verdict.txt	s	get(d, 'check=console-aem-crc.detail.read')
2337	312	^	d	get(d, 'check=live-vs-qspi-ENTITY 0.detail.live_bytes')
2337	106	^	d	get(d, 'check=live-vs-qspi-CONFIGURATION 0.detail.live_bytes')
2338	0	^	s#0	next(k for k, v in get(d, 'check=clock-sources.detail.sources').items() if isinstance(v, dict) and v['type'] == 0)
2338	1	^	s#0	next(k for k, v in get(d, 'check=clock-sources.detail.sources').items() if isinstance(v, dict) and v['type'] == 2 and v['location_index'] == 1)
2338	1	^	d#1	get(d, 'check=clock-sources.detail.sources')['1']['location_index']
2338	2	^	s#0	next(k for k, v in get(d, 'check=clock-sources.detail.sources').items() if isinstance(v, dict) and v['type'] == 2 and v['location_index'] == 0)
2338	0	^	d#1	get(d, 'check=clock-sources.detail.sources')['2']['location_index']
2338	3	^	s#0	next(k for k, v in get(d, 'check=clock-sources.detail.sources').items() if v == 'NO_SUCH_DESCRIPTOR')
2338	0	^	d#3	get(d, 'check=clock-sources.detail.clock_domain_list.0')
2338	1	^	d#2	get(d, 'check=clock-sources.detail.clock_domain_list.1')
2338	2	^	d#1	get(d, 'check=clock-sources.detail.clock_domain_list.2')
2338	0	^	d#4	get(d, 'check=clock-sources.detail.get_clock_source')
2339	10		s#0	rx('identity/grader-identity.txt', r'UART SMOKE: PASS \((\d+)/(\d+)\)')
2339	10		s#1	rx('identity/grader-identity.txt', r'UART SMOKE: PASS \((\d+)/(\d+)\)', group=2)
2340	001bc5c1935893e1	identity/adp-discover.jsonl	s	next(x['model_id'] for x in d if x.get('entity_id') == '020000fffe000001')
2341	05:45:06		cest	stamps('identity/lock-window.txt', 'LOCK')[0]
2341	05:45:12		cest	stamps('identity/lock-window.txt', 'UNLOCK')[0]
2346	05:45		hm	stamps('restore/baseline-start-lock.txt', 'LOCK')[0]
2349	0205022001006000		s	cen('restore/census-start.jsonl', 'format-dut-5-0')['payload'][8:]
2349	four		w	identity_maps(cen('restore/census-start.jsonl', 'map-dut-0x000e-0-0'))
2350	eight		w	identity_maps(cen('restore/census-start.jsonl', 'map-dut-0x000f-0-0'))
2350	0		d#2	payload_word(cen('restore/census-start.jsonl', 'clock', 'dut'), 8)
2351	276		d	nvm('restore/dut-start.txt')['seq']
2351	42		d	nvm('restore/dut-start.txt')['commits']
2351	0		d	nvm('restore/dut-start.txt')['pend']
2351	152		d	le32(mem('restore/dut-start.txt', '0x900008d4', 12)) & 0xffff
2353	0205022002006000		s	cen('restore/census-start.jsonl', 'format-peer-5-0')['payload'][8:]
2355	0205022001006000		s	cen('restore/census-start.jsonl', 'format-peer-6-0')['payload'][8:]
2355	0		d#0	cen('restore/census-start.jsonl', 'tx-state-peer-0')['conn_count']
# B16: method
2365	-20		d	Decimal(rx('tools/b9_tone.py', r'^LEVEL_DBFS = (-?[\d.]+)'))
2365	d9684a8f...		s	rx('runs/tone-start.txt', r'LOOP_SHA256 ([0-9a-f]{8})') + '...'
2366	05:55:37		cest	stamps('runs/tone-start.txt', 'STATUS')[0] - Decimal(rx('runs/tone-start.txt', r'hw_ptr : (\d+)')) / 48000
2366	06:01:59		cest	stamps('runs/tone-stop.txt', 'LOCK')[0]
2367	twice	r2/source-receipt.json	x	sum(1 for k, r in d['reads'].items() if k.startswith('b16-') and r['kind'] == 'state')
2370	one	runs/loop1-lock.txt	w	same(len(stamps(f'runs/{r}-lock.txt', 'LOCK')) for r in ('loop1', 'loop2'))
2375	12	runs/loop1/events.jsonl	d	same(round(max(x['dt'] for x in ev(r, 'listener-poll'))) for r in ('loop1', 'loop2'))
2377	2	^	d	same(round(statistics.median(b['dt'] - a['dt'] for a, b in zip(ev(r, 'listener-poll'), ev(r, 'listener-poll')[1:]) if b['tag'] == a['tag'])) for r in ('loop1', 'loop2'))
2384	05:56:30		cest	stamps('runs/loop1-lock.txt', 'LOCK')[0]
2384	05:57:30		cest	stamps('runs/loop1-lock.txt', 'UNLOCK')[0]
2384	30.6	runs/loop1/events.jsonl	.1f	E('loop1', 'capture-done', what='tap')['seconds']
2384	22	^	.0f	E('loop1', 'capture-done', what='extcap')['seconds']
2384	05:56:45	^	cest	E('loop1', 'captures-started')['started']['extcap']
2385	05:59:18		cest	stamps('runs/loop2-lock.txt', 'LOCK')[0]
2385	06:00:28		cest	stamps('runs/loop2-lock.txt', 'UNLOCK')[0]
2385	52.5	runs/loop2/events.jsonl	.1f	E('loop2', 'capture-done', what='tap')['seconds']
2385	05:59:19	^	cest	E('loop2', 'captures-started')['started']['tap']
2385	16	^	.0f	E('loop2', 'capture-done', what='extcap')['seconds']
2385	05:59:36	^	cest	E('loop2', 'captures-started')['started']['extcap']
2394	0205022001006000	runs/loop1/events.jsonl	s	same(E(r, 'format-check', talker='peer-out-0')['talker_fmt'] for r in ('loop1', 'loop2'))
2394	0205022002006000	^	s	same(E(r, 'format-check', talker='peer-out-0')['listener_fmt'] for r in ('loop1', 'loop2'))
2394	0205022001006000	^	s	same(E(r, 'format-check', talker='peer-out-0')['set']['fmt'] for r in ('loop1', 'loop2'))
2394	0205022001006000	^	s	same(E(r, 'format-check', talker='peer-out-0')['listener_after'] for r in ('loop1', 'loop2'))
2395	0205022002006000	^	s	same(E(r, 'format-check', listener='peer-in-0', set=None, talker='020000fffe000001-out-0')['talker_fmt'] for r in ('loop1', 'loop2'))
2395	0205022002006000	^	s	same(E(r, 'format-check', listener='peer-in-0', set=None, talker='020000fffe000001-out-0')['listener_fmt'] for r in ('loop1', 'loop2'))
2402	5		s	rx('tools/tone_points_b16.py', r'\(fr > t - (\d+)\)')
2402	0.9		s	rx('tools/tone_points_b16.py', r'if share > ([\d.]+) and lvl >= LEVEL_FLOOR_DBFS')
2402	one	tools/tone_points_b16.py	w	b15_changes()
2403	-100		d	Decimal(rx('tools/tone_points_b16.py', r'^LEVEL_FLOOR_DBFS = (-?[\d.]+)'))
2403	-40		s	rx('tools/tone_points_b15.py', r'and lvl > (-?\d+)')
2404	-38.5	r2/source-receipt.json	.1f	get(d, 'reads.b16-meters-1.meters.the documented pair of outputs.0.leaving_dbfs.0')
2404	-40		s	rx('tools/tone_points_b16.py', r'if lvl < (-?\d+):')
2405	-100		d	Decimal(rx('tools/tone_points_b16.py', r'^LEVEL_FLOOR_DBFS = (-?[\d.]+)'))
2405	-40		s	rx('tools/tone_points_b16.py', r'if lvl < (-?\d+):')
# B16: the loopback
2411	2	runs/loop1/events.jsonl	d	same(round(statistics.median(b['dt'] - a['dt'] for a, b in zip(ev(r, 'listener-poll'), ev(r, 'listener-poll')[1:]) if b['tag'] == a['tag'])) for r in ('loop1', 'loop2'))
2415	14	^	d	len(ev('loop1', 'listener-poll'))
2415	12	^	d	round(max(x['dt'] for x in ev('loop1', 'listener-poll', tag='after-loop-bind')))
2415	12	^	d	round(max(x['dt'] for x in ev('loop1', 'listener-poll', tag='after-captures')))
2415	0000000000000000	^	s	same(x['rx']['stream_id'] for x in ev('loop1', 'listener-poll'))
2415	000000000000	^	s	same(x['rx']['dmac'] for x in ev('loop1', 'listener-poll'))
2415	0x0002	^	s	same(x['rx']['flags'] for x in ev('loop1', 'listener-poll'))
2415	0	^	d#0	same(x['peer_tx0']['conn_count'] for x in ev('loop1', 'listener-poll'))
2415	0	^	d#1	same([x['media_locked'] for x in ev('loop1', 'listener-poll')] + [ctrs(c)[0] for c in ev('loop1', 'counters', who='peer')])
2415	0	^	d#2	same([x['frames_rx'] for x in ev('loop1', 'listener-poll')] + [ctrs(c)[11] for c in ev('loop1', 'counters', who='peer')])
2416	14	runs/loop2/events.jsonl	d	len(ev('loop2', 'listener-poll'))
2418	1	runs/loop1/events.jsonl	d	same(E(r, 'bind', talker='peer-out-0')['conn_count'] for r in ('loop1', 'loop2'))
2420	0	^	d	same(x['peer_tx0']['conn_count'] for x in [x for r in ('loop1', 'loop2') for x in ev(r, 'listener-poll')])
2427	0.0	summary/loop2/acmp-peer-tap.json	.1f	(acmp('DISCONNECT_RX_COMMAND') - acmp('DISCONNECT_RX_COMMAND')) * 1000
2428	0.0	^	.1f	(acmp('DISCONNECT_RX_RESPONSE') - acmp('DISCONNECT_RX_COMMAND')) * 1000
2428	0	^	d#0	get(d, 'acmp.msg=DISCONNECT_RX_RESPONSE')['conn_count']
2429	0.1	^	.1f	(acmp('CONNECT_RX_COMMAND') - acmp('DISCONNECT_RX_COMMAND')) * 1000
2430	99.6	^	.1f	(acmp('CONNECT_RX_RESPONSE') - acmp('DISCONNECT_RX_COMMAND')) * 1000
2430	1	^	d#0	get(d, 'acmp.msg=CONNECT_RX_RESPONSE')['conn_count']
2430	0	^	d#0	int(get(d, 'acmp.msg=CONNECT_RX_RESPONSE')['stream_id'], 16)
2431	99.6	^	.1f	(acmp('CONNECT_TX_COMMAND') - acmp('DISCONNECT_RX_COMMAND')) * 1000
2432	299.6	^	.1f	(acmp('CONNECT_TX_COMMAND', 1) - acmp('DISCONNECT_RX_COMMAND')) * 1000
2435	49.6	^	.1f	E('loop2', 'capture-done', what='tap')['seconds'] - acmp('CONNECT_TX_COMMAND', 1)
# B16: the four points of the loopback
2447	0	summary/loop1/a-peer-tap.json	d	d['info']['pdus']
2448	0	summary/loop1/b-dut-tap.json	d	d['info']['pdus']
2449	two	summary/loop1/d-extcap-pair.json	w	sum(1 for r in d['rows'] if r['nonzero'] == 0)
2449	1,056,000	^	,d	same(r['frames'] for r in d['rows'])
2450	0	summary/loop2/a-peer-tap.json	d	d['info']['pdus']
2451	0	summary/loop2/b-dut-tap.json	d	d['info']['pdus']
2452	two	summary/loop2/d-extcap-pair.json	w	sum(1 for r in d['rows'] if r['nonzero'] == 0)
2452	768,000	^	,d	same(r['frames'] for r in d['rows'])
2458	0	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	rx(FIND_P, r'nothing\. Its counters stayed (\d+) and its digital output read exact zero')
# B16: the tone source, read only
2473	05:47	r2/source-receipt.json	hm	Decimal(clock(get(d, 'reads.b16-state-1.at')))
2473	06:01	^	hm	Decimal(clock(get(d, 'reads.b16-state-2.at')))
2484	-20.0	^	.1f	meter(('b16-meters-1', 'b16-meters-2', 'b16-state-2'), 'the documented pair of outputs', 'before_setting_dbfs')
2484	-18.5	^	.1f	same(v for k in ('b16-state-1', 'b16-state-2') for v in get(d, 'reads.' + k + '.level_settings_db.the documented pair of outputs'))
2484	-38.5	^	.1f	meter(('b16-meters-1', 'b16-meters-2', 'b16-state-2'), 'the documented pair of outputs', 'leaving_dbfs')
2485	-20.0	^	.1f	meter(('b16-meters-1', 'b16-meters-2', 'b16-state-2'), 'the second pair of outputs', 'before_setting_dbfs')
2485	+6.0	^	+.1f	same(v for k in ('b16-state-1', 'b16-state-2') for v in get(d, 'reads.' + k + '.level_settings_db.the second pair of outputs'))
2485	-14.0	^	.1f	meter(('b16-meters-1', 'b16-meters-2', 'b16-state-2'), 'the second pair of outputs', 'leaving_dbfs')
2486	-135.2	^	.1f	max(get(d, 'reads.' + k + '.meters.every other output.largest_before_setting_dbfs') for k in ('b16-state-1', 'b16-meters-1', 'b16-meters-2', 'b16-state-2'))
2486	-147.6	^	.1f	max(get(d, 'reads.' + k + '.meters.every other output.largest_leaving_dbfs') for k in ('b16-state-1', 'b16-meters-1', 'b16-meters-2', 'b16-state-2'))
2488	-20.0	^	.1f	meter(('b16-meters-1', 'b16-meters-2', 'b16-state-2'), "the tone's playback channels", 'leaving_dbfs')
2488	0	^	.0f	meter(('b16-meters-1', 'b16-meters-2', 'b16-state-2'), 'the documented pair of outputs', 'before_setting_dbfs') - meter(('b16-meters-1', 'b16-meters-2', 'b16-state-2'), "the tone's playback channels", 'leaving_dbfs')
2494	two	^	w	sum(1 for k, r in d['reads'].items() if k.startswith('b16-') and r['kind'] == 'state')
2494	2,262	^	,d	same(get(d, 'compare.0.entries') + [get(d, 'compare.0.both')])
2499	two	^	w	len(get(d, 'reads.b16-meters-1.meters.the documented pair of outputs'))
2500	-38.5	^	.1f	meter(('b16-meters-1', 'b16-meters-2', 'b16-state-2'), 'the documented pair of outputs', 'leaving_dbfs')
# B16: the controls
2509	7bbefc71...		s	sha('controls/controls.json')[:8] + '...'
2510	728a4f0e...		s	sha('controls/b9-controls.json')[:8] + '...'
2511	five	controls/b16-tap-controls.json	w	sum(1 for c in d['controls'] if 'lane B16' not in c['control'])
2511	5	^	d#0	sum(1 for c in d['controls'] if 'lane B16' not in c['control'] and c['result'] == 'PASS')
2511	5	^	d#1	sum(1 for c in d['controls'] if 'lane B16' not in c['control'])
2512	-60	^	d	same(get(d, 'controls.control=tone pair at -60 dBFS on the floor (lane B16)')['levels'])
2512	-60.00	^	.2f	same(get(d, 'controls.control=tone pair at -60 dBFS on the floor (lane B16)')['levels'])
2513	-130	^	d	get(d, 'controls.control=-130 dBFS tone alone (lane B16)')['level']
2513	1.0	^	.1f	same(get(d, 'controls.control=-130 dBFS tone alone (lane B16)')['share'])
2514	eight		w	rx('tools/tone_points_b16.py', r'synth_pcap\(p, sid, (\d+), 2 \* FS, \(5, 6\)\)')
2514	5	controls/b16-tap-controls.json	d	get(d, 'controls.control=eight channels, tone on 5/6 (lane B16)')['tone_channels']['997'][0]
2514	6	^	d	get(d, 'controls.control=eight channels, tone on 5/6 (lane B16)')['tone_channels']['9973'][0]
2515	five	controls/b16-align-controls-synth.json	w	sum(1 for c in d['controls'] if 'lane B16' not in c['control'])
2515	5	^	d#0	sum(1 for c in d['controls'] if 'lane B16' not in c['control'] and c['result'] == 'PASS')
2515	5	^	d#1	sum(1 for c in d['controls'] if 'lane B16' not in c['control'])
2516	one	^	w	re.search(r'^(\w+) sample changed by \+256', d['controls'][5]['control']).group(1) == 'one' and 1
2516	+256	^	s	re.search(r'by (\+\d+) LSB', d['controls'][5]['control']).group(1)
2516	One	^	W	d['controls'][5]['frames_differing']
# B16: bench as left
2529	0205022001006000		s	cen('restore/census-end.jsonl', 'format-dut-5-0')['payload'][8:]
2529	0		d#1	payload_word(cen('restore/census-end.jsonl', 'clock', 'dut'), 8)
2530	0205022002006000		s	cen('restore/census-end.jsonl', 'format-peer-5-0')['payload'][8:]
2531	44		d	census_reads('restore/census-start.jsonl', 'restore/census-end.jsonl', 'restore/census-compare.txt')[0]
2531	45		d	census_reads('restore/census-start.jsonl', 'restore/census-end.jsonl', 'restore/census-compare.txt')[1]
2531	387		d	int(rx('restore/census-compare.txt', r'<gm-id>([0-9a-f]{8})', 0), 16)
2531	377		d	int(rx('restore/census-compare.txt', r'<gm-id>([0-9a-f]{8})', 1), 16)
2532	276		d	nvm('restore/dut-end.txt')['seq']
2532	42		d	nvm('restore/dut-end.txt')['commits']
2532	0		d	nvm('restore/dut-end.txt')['pend']
2533	06:01:59		cest	stamps('runs/tone-stop.txt', 'LOCK')[0]
2541	two		w	same(counters('restore/counters-end.jsonl', 'dut', 6, 0)[i] - counters('restore/counters-start.jsonl', 'dut', 6, 0)[i] for i in (0, 1))
2541	one		w	same(counters('restore/counters-end.jsonl', 'dut', 6, 0)[i] - counters('restore/counters-start.jsonl', 'dut', 6, 0)[i] for i in (0, 1)) // sum(1 for r in RUNS for b in ev(r, 'bind') if b['listener'] == 'peer-in-0')
2545	152		d	same(le32(mem(f, '0x900008d4', 12)) & 0xffff for f in ('restore/dut-start.txt', 'restore/dut-end.txt'))
# B16: limits
2562	Two	runs/loop1/events.jsonl	W	sum(1 for r in RUNS for b in ev(r, 'bind') if b['talker'] == 'peer-out-0' and b['listener'] == 'peer-in-0')
# B16b: the resume
2642	06:22:23		cest	stamps('soc/b16b-precheck-status.log', 'LOCK')[0]
2646	06:22:29		cest	stamps('identity-b16b/lock-window.txt', 'LOCK')[0]
2646	06:22:34		cest	stamps('identity-b16b/lock-window.txt', 'UNLOCK')[0]
2646	44		d	census_reads('restore/census-end.jsonl', 'restore/census-startb.jsonl', 'restore/census-compare-b16-to-b16b.txt')[0]
2646	45		d	census_reads('restore/census-end.jsonl', 'restore/census-startb.jsonl', 'restore/census-compare-b16-to-b16b.txt')[1]
2647	-14.14	summary/pts1/a-peer-tap.json	.2f	same(T(load(f'summary/{r}/a-peer-tap.json'), 0, 'level_dbfs') for r in ('pts1', 'pts2'))
2647	06:28:50	summary/pts2/a-peer-tap.json	cest	d['info']['last_t']
2647	-14.10	summary/b0/a-peer-tap.json	.2f	same(T(load(f'summary/{r}/a-peer-tap.json'), 0, 'level_dbfs') for r in ('b0', 'b0-2', 'pts3'))
2647	06:31:51	^	cest	d['info']['first_t']
2648	0	summary/pts1/a-peer-tap.json	d	same(load(f'summary/{r}/{p}.json')['info']['seq_gaps'] for r in ('pts1', 'pts2', 'pts3', 'b0-2') for p in ('a-peer-tap', 'b-dut-tap'))
2649	480,000	summary/pts1/align-a-c.json	,d#0	same(align(r, p)['compared_equal'] for r in ('pts1', 'pts2', 'pts3') for p in 'ab')
2649	480,000	^	,d#1	same(align(r, p)['mcasp_frames'] for r in ('pts1', 'pts2', 'pts3') for p in 'ab')
2649	three	^	w	sum(1 for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') if (ROOT / f'summary/{r}/align-a-c.json').exists() and align(r, 'a')['mcasp_frames'] == 480000)
2649	34.1	r2/b0-2-receipt.json	.1f	d['overlap']['seconds']
2649	0	summary/pts1/align-a-c.json	d#0	same(len(align(r, p)['slips']) for r in ('pts1', 'pts2', 'pts3', 'b0-2') for p in 'ab')
2650	-1.00	summary/pts2/d-extcap-pair.json	.2f	same(r['tone_' + t]['median']['level_dbfs'] for x in ('pts2', 'b0-2') for r, t in zip(load(f'summary/{x}/d-extcap-pair.json')['rows'], ('997', '9973')))
2650	303.8	summary/b0-2/d-loop-decode.json	.1f	d['decoded'] / 48000
2650	two		w	load('summary/pts2/d-loop-decode.json')['repeats']
2650	2		d	same(e['frames'] for e in load('summary/pts2/d-loop-decode.json')['events'])
2651	06:23	r2/source-receipt.json	hm	Decimal(clock(get(d, 'reads.b16b-state-1.at')))
2651	06:50	^	hm	Decimal(clock(get(d, 'reads.b16b-state-2.at')))
2652	-123.95	summary/b0-2/c-b9-grade.json	.2f	d['summary']['ch0_all']['thdn_db_median']
2652	-122.80	^	.2f	d['summary']['ch1_all']['thdn_db_median']
2652	300	^	d	d['summary']['blocks']
2652	0	^	d#0	d['summary']['events']
2652	0.0000	^	z.4f	d['summary']['effective_offset_ppm']
2652	34.1	r2/b0-2-receipt.json	.1f	d['overlap']['seconds']
# B16b: method
2662	one	runs/pts1-lock.txt	w	same(len(stamps(f'runs/{r}-lock.txt', 'LOCK')) for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3'))
2670	06:23:39		cest	stamps('runs/pts1-lock.txt', 'LOCK')[0]
2670	06:24:28		cest	stamps('runs/pts1-lock.txt', 'UNLOCK')[0]
2670	06:23:46	runs/pts1/events.jsonl	cest	E('pts1', 'bind')['t']
2670	24.5	^	.1f	E('pts1', 'capture-done', what='tap')['seconds']
2670	06:23:58	^	cest	E('pts1', 'captures-started')['started']['tap']
2670	16	^	.0f	E('pts1', 'capture-done', what='extcap')['seconds']
2670	10	summary/pts1/c-mcasp.json	.0f	d['seconds']
2670	06:24:02	runs/pts1/events.jsonl	cest	E('pts1', 'captures-started')['started']['mcasp']
2671	06:28:06		cest	stamps('runs/pts2-lock.txt', 'LOCK')[0]
2671	06:28:56		cest	stamps('runs/pts2-lock.txt', 'UNLOCK')[0]
2671	06:28:13	runs/pts2/events.jsonl	cest	E('pts2', 'bind')['t']
2671	06:28:25	^	cest	E('pts2', 'captures-started')['started']['tap']
2671	2	tools/run_b16.py	d#0	r2lead()
2671	10	summary/pts2/c-mcasp.json	.0f	d['seconds']
2671	06:28:31.5	runs/pts2/events.jsonl	cest1	E('pts2', 'captures-started')['started']['mcasp'] + r2lead()
2671	2	tools/run_b16.py	d#1	r2lead()
2671	06:28:29.5	runs/pts2/events.jsonl	cest1	E('pts2', 'captures-started')['started']['mcasp']
2672	06:31:28		cest	stamps('runs/b0-lock.txt', 'LOCK')[0]
2672	06:37:05		cest	stamps('runs/b0-lock.txt', 'UNLOCK')[0]
2672	06:31:30	runs/b0/events.jsonl	cest	E('b0', 'bind', i=-1)['t']
2672	40	summary/b0/a-peer-tap.json	.0f	d['seconds']
2672	06:31:50	runs/b0/events.jsonl	cest	E('b0', 'captures-started')['started']['tap']
2672	306	summary/b0/d-loop-decode.json	.0f	d['frames'] / 48000
2673	06:37:31		cest	stamps('runs/b0-2-lock.txt', 'LOCK')[0]
2673	06:43:17		cest	stamps('runs/b0-2-lock.txt', 'UNLOCK')[0]
2673	06:37:39	runs/b0-2/events.jsonl	cest	E('b0-2', 'bind', i=-1)['t']
2673	40	summary/b0-2/a-peer-tap.json	.0f	d['seconds']
2673	06:37:59	runs/b0-2/events.jsonl	cest	E('b0-2', 'captures-started')['started']['tap']
2673	306	summary/b0-2/d-extcap-pair.json	.0f	d['seconds']
2673	300	summary/b0-2/c-b9-grade.json	.0f	d['seconds']
2673	06:38:03.2	runs/b0-2/events.jsonl	cest1	E('b0-2', 'captures-started')['started']['mcasp']
2673	2	tools/run_b16.py	d	r2lead()
2673	06:38:05.2	runs/b0-2/events.jsonl	cest1	E('b0-2', 'captures-started')['started']['mcasp'] + r2lead()
2674	06:48:55		cest	stamps('runs/pts3-lock.txt', 'LOCK')[0]
2674	06:49:45		cest	stamps('runs/pts3-lock.txt', 'UNLOCK')[0]
2674	06:49:02	runs/pts3/events.jsonl	cest	E('pts3', 'bind')['t']
2674	06:49:14	^	cest	E('pts3', 'captures-started')['started']['tap']
2677	eight		w	identity_maps(cen('restore/census-startb.jsonl', 'map-dut-0x000f-0-0'))
2677	four		w	identity_maps(cen('restore/census-startb.jsonl', 'map-dut-0x000e-0-0'))
2679	566d3dfa...	runs/pts2/events.jsonl	s	same(E(r, 'loop-staged')['sha256'] for r in ('pts2', 'b0', 'b0-2'))[:8] + '...'
2683	0205022001006000	runs/pts1/events.jsonl	s	same(x['listener_fmt'] for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') for x in ev(r, 'format-check', listener='dut-in-0') if x['set'] is None and x['talker_fmt'] == x['listener_fmt'])
2684	041060010000bb80	runs/b0/events.jsonl	s	same(x['listener_fmt'] for r in ('b0', 'b0-2') for x in ev(r, 'format-check', listener='dut-in-1') if x['set'] is None and x['talker_fmt'] == x['listener_fmt'])
2686	0	^	d	same(x['source'] for r in ('b0', 'b0-2') for x in ev(r, 'clock-read', who='dut'))
2694	3		d	Decimal(rx('tools/b9_thdn.py', r'^FLOOR_DB = ([\d.]+)'))
2696	0.01	summary/pts1/a-peer-tap.json	.2f	bound(max(abs(t['median']['snr_db'] + t['median']['thdn_db']) for r in ('pts1', 'pts2', 'pts3', 'b0-2') for p in PFILE_ for c in (0, 1) for t in [pt(r, p, c, (997, 9973)[c])]), '0.01')
2698	300	summary/b0-2/c-b9-grade.json	.0f	d['seconds']
2698	630	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	rx(FIND_P, r'^(\d+) s, untouched, from (\d+) s after the last bind or clock-source set')
2698	one		w	len(stamps('runs/b0-2-lock.txt', 'LOCK'))
2699	24.0	r2/b0-2-receipt.json	.1f	d['timing']['command_after_binds_s']
2700	2	tools/run_b16.py	d	r2lead()
2702	26	r2/b0-2-receipt.json	.0f	d['timing']['recording_after_binds_s']
2702	20	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	rx(FIND_P, r'^(\d+) s, untouched, from (\d+) s after the last bind or clock-source set', group=2)
2704	One	RAW-ARTIFACTS.json	W	sum(1 for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') if raw(r + '/mcasp-all.raw')['bytes'] == 0)
2714	channels «2» and		d#0	same(tuple(c['channel'] for c in load(f'summary/{r}/{p}.json')['channels'] if c['min'] == -1 and c['max'] == 0) for r in ('pts1', 'pts2', 'pts3', 'b0-2') for p in ('a-peer-tap', 'b-dut-tap', 'c-mcasp'))[0]
2714	and «3» carry		d#0	same(tuple(c['channel'] for c in load(f'summary/{r}/{p}.json')['channels'] if c['min'] == -1 and c['max'] == 0) for r in ('pts1', 'pts2', 'pts3', 'b0-2') for p in ('a-peer-tap', 'b-dut-tap', 'c-mcasp'))[1]
# B16b: the four points
2715	-1	summary/pts1/a-peer-tap.json	d	same(c['min'] for c in [c for r in ('pts1', 'pts2', 'pts3', 'b0-2') for p in ('a-peer-tap', 'b-dut-tap', 'c-mcasp') for c in load(f'summary/{r}/{p}.json')['channels'] if c['channel'] in (2, 3)])
2715	0	^	d	same(c['max'] for c in [c for r in ('pts1', 'pts2', 'pts3', 'b0-2') for p in ('a-peer-tap', 'b-dut-tap', 'c-mcasp') for c in load(f'summary/{r}/{p}.json')['channels'] if c['channel'] in (2, 3)])
2742	two	summary/pts1/d-extcap-pair.json	w	same(len(load(f'summary/{r}/d-extcap-pair.json')['rows']) for r in ('pts1', 'pts3'))
2742	-1	^	d	same(v for r in ('pts1', 'pts3') for x in load(f'summary/{r}/d-extcap-pair.json')['rows'] for v in (x['min'], x['max']))
2743	-1.00	summary/pts2/d-extcap-pair.json	.2f	same([d['rows'][0]['tone_997']['median']['level_dbfs'], d['rows'][1]['tone_9973']['median']['level_dbfs']])
2743	997.0000	^	.4f	d['rows'][0]['tone_997']['median']['f_hz']
2743	9,973.0000	^	,.4f	d['rows'][1]['tone_9973']['median']['f_hz']
2743	0.000	^	z.3f	same(q(t['median']['ppm'], 3) for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2743	-146.06	^	.2f	d['rows'][0]['tone_997']['median']['thdn_db']
2743	-145.99	^	.2f	d['rows'][1]['tone_9973']['median']['thdn_db']
2743	11	^	d	same(len(floor_inside(t)) for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2743	13	^	d	same(len(inside(t['per_block'])) for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2743	16	^	d	same(len(t['per_block']) for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2743	0	^	d#0	same(silent(t['per_block'])[0] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2743	1	^	d#0	same(silent(t['per_block'])[-1] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2743	2	^	d#0	same(inside(t['per_block'])[0] - 1 for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2743	6	^	d#0	same([i for i in inside(t['per_block']) if i not in floor_inside(t)][0] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2743	12	^	d#0	same([i for i in inside(t['per_block']) if i not in floor_inside(t)][1] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2743	2		d#1	same(e['frames'] for e in load('summary/pts2/d-loop-decode.json')['events'])
2743	6.131		.3f	load('summary/pts2/d-loop-decode.json')['events'][0]['second']
2743	12.113		.3f	load('summary/pts2/d-loop-decode.json')['events'][1]['second']
2743	-4		d	load('summary/pts2/d-loop-decode.json')['net_step_frames']
2743	665,599		,d	load('summary/pts2/d-loop-decode.json')['decoded']
2743	0		d#1	load('summary/pts2/d-loop-decode.json')['torn']
2744	303	summary/b0-2/d-extcap-pair.json	d	same(n for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']) for n in (len(floor_inside(t)), len(inside(t['per_block']))))
2744	306	^	d	same(len(t['per_block']) for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2744	0	^	d#0	same(silent(t['per_block'])[0] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2744	1	^	d#0	same(silent(t['per_block'])[-1] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2744	2	^	d#0	same(inside(t['per_block'])[0] - 1 for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
2744	0		d#1	len(load('summary/b0-2/d-loop-decode.json')['events'])
2744	0		d#2	load('summary/b0-2/d-loop-decode.json')['torn']
2744	14,583,286		,d	load('summary/b0-2/d-loop-decode.json')['decoded']
2744	14,583,189		,d	load('summary/b0/d-loop-decode.json')['decoded']
2746	-1.00	summary/pts2/ctl-dut-talker-dut-tap.json	.2f	same(q(x['median']['level_dbfs'], 2) for x in taps2())
2747	-146.06	^	.2f	same(q(x['median']['thdn_db'], 2) for x in taps2()[0::2])
2747	-145.99	^	.2f	same(q(x['median']['thdn_db'], 2) for x in taps2()[1::2])
2747	15	^	d	same(n for x in taps2() for n in (len(floor_inside(x)), len(inside(x['per_block']))))
2748	23	^	d	same(len(x['per_block']) for x in taps2())
2748	0	^	d#0	same(runs_of(silent(x['per_block']))[0][0] for x in taps2())
2748	2	^	d#0	same(runs_of(silent(x['per_block']))[0][1] for x in taps2())
2748	20	^	d#0	same(runs_of(silent(x['per_block']))[1][0] for x in taps2())
2748	22	^	d#0	same(runs_of(silent(x['per_block']))[1][1] for x in taps2())
2749	3	^	d	same(inside(x['per_block'])[0] - 1 for x in taps2())
2749	19	^	d	same(inside(x['per_block'])[-1] + 1 for x in taps2())
2749	two		w	load('summary/pts2/d-loop-decode.json')['repeats']
2759	480,000	summary/pts1/align-b-c.json	,d	same(x['compared_equal'] for x in [align(r, p) for r in ('pts1', 'pts2', 'pts3') for p in 'ab'])
2759	480,000	^	,d	same(x['mcasp_frames'] for x in [align(r, p) for r in ('pts1', 'pts2', 'pts3') for p in 'ab'])
2759	0	^	d	same(len(x['slips']) for x in [align(r, p) for r in ('pts1', 'pts2', 'pts3') for p in 'ab'])
2759	480,000	summary/pts1/align-a-c.json	,d	same(x['compared_equal'] for x in [align(r, p) for r in ('pts1', 'pts2', 'pts3') for p in 'ab'])
2759	480,000	^	,d	same(x['mcasp_frames'] for x in [align(r, p) for r in ('pts1', 'pts2', 'pts3') for p in 'ab'])
2759	0	^	d	same(len(x['slips']) for x in [align(r, p) for r in ('pts1', 'pts2', 'pts3') for p in 'ab'])
2760	1,637,980	summary/b0-2/align-b-c.json	,d	d['compared_equal']
2760	34.1	^	.1f	d['compared_equal'] / 48000
2760	0	^	d#0	d['frames_differing']
2760	0	^	d#1	len(d['slips'])
2760	1,637,452	summary/b0-2/align-a-c.json	,d	d['compared_equal']
2760	34.1	^	.1f#1	d['compared_equal'] / 48000
2760	0	^	d#2	d['frames_differing']
2760	0	^	d#3	len(d['slips'])
2764	-14.14	summary/pts1/a-peer-tap.json	.2f	same(T(load(f'summary/{r}/a-peer-tap.json'), 0, 'level_dbfs') for r in ('pts1', 'pts2'))
2765	-14.0	r2/source-receipt.json	.1f	meter(('b16b-meters-1', 'b16b-meters-2', 'b16b-state-2'), 'the second pair of outputs', 'leaving_dbfs')
2766	-38.5	^	.1f	meter(('b16b-meters-1', 'b16b-meters-2', 'b16b-state-2'), 'the documented pair of outputs', 'leaving_dbfs')
# B16b: the tone source changed during the lane
2771	d9684a8f...		s	rx('runs/b16b-tone-start.txt', r'LOOP_SHA256 ([0-9a-f]{8})') + '...'
2771	06:23:26		cest	stamps('runs/b16b-tone-start.txt', 'STATUS')[0] - Decimal(rx('runs/b16b-tone-start.txt', r'hw_ptr : (\d+)')) / 48000
2771	06:52:19		cest	stamps('runs/b16b-tone-stop.txt', 'LOCK')[0]
2772	06:23	r2/source-receipt.json	hm	Decimal(clock(get(d, 'reads.b16b-state-1.at')))
2772	06:50	^	hm	Decimal(clock(get(d, 'reads.b16b-state-2.at')))
2774	-38.5	^	.1f	meter(('b16b-meters-1', 'b16b-meters-2', 'b16b-state-2'), 'the documented pair of outputs', 'leaving_dbfs')
2774	-14.0	^	.1f	meter(('b16b-meters-1', 'b16b-meters-2', 'b16b-state-2'), 'the second pair of outputs', 'leaving_dbfs')
2775	1,255	^	,d	get(d, 'compare.1')['entries'][1]
2775	2,262	^	,d	get(d, 'compare.1')['entries'][0]
2776	1,255	^	,d	get(d, 'compare.1')['both']
2776	four	^	w	get(d, 'compare.1')['differ']
2780	two	^	w	sum(1 for x in get(d, 'compare.1')['differing'] if x['cls'] == 'an input of a monitoring mix')
2781	two	^	w	same(x['messages'][0] for x in get(d, 'compare.1')['differing'] if x['cls'] == 'an input of a monitoring mix')
2782	one	^	w	same(x['messages'][1] for x in get(d, 'compare.1')['differing'] if x['cls'] == 'an input of a monitoring mix' and x['second_last_among_first'] and x['all_minus_infinity'])
2784	1,255	^	,d	get(d, 'compare.1')['both']
2784	two	^	w	sum(1 for x in get(d, 'compare.1')['differing'] if x['cls'] != 'an input of a monitoring mix')
2786	1,007	^	,d	get(d, 'compare.1')['entries'][0] - get(d, 'compare.1')['both']
2792	06:28:50	summary/pts2/a-peer-tap.json	cest	d['info']['last_t']
2792	-14.1353	summary/pts1/a-peer-tap.json	.4f	same(T(load(f'summary/{r}/a-peer-tap.json'), 0, 'level_dbfs') for r in ('pts1', 'pts2'))
2792	+6.94	^	+.2f	min(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))
2792	+6.96	^	+.2f	max(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))
2792	-109.68		.2f	load('summary/pts1/c-b9-grade.json')['summary']['ch0_floor']['thdn_db_median']
2792	-111.26		.2f	load('summary/pts2/c-b9-grade.json')['summary']['ch0_floor']['thdn_db_median']
2792	-89.83		.2f	load('summary/pts1/c-b9-grade.json')['summary']['ch1_floor']['thdn_db_median']
2792	-91.51		.2f	load('summary/pts2/c-b9-grade.json')['summary']['ch1_floor']['thdn_db_median']
2792	+3.00		+.2f	load('summary/pts1/c-b9-grade.json')['phase_net_frames']
2792	+3.01		+.2f	load('summary/pts2/c-b9-grade.json')['phase_net_frames']
2792	10	summary/pts1/c-b9-grade.json	.0f	same(grade(r)['seconds'] for r in ('pts1', 'pts2'))
2792	Two		W	load('summary/pts2/d-loop-decode.json')['repeats']
2792	2		d	same(e['frames'] for e in load('summary/pts2/d-loop-decode.json')['events'])
2792	13.9		.1f	load('summary/pts2/d-loop-decode.json')['decoded'] / 48000
2793	06:31:51	summary/b0/a-peer-tap.json	cest	d['info']['first_t']
2793	-14.1035	^	.4f	same(T(load(f'summary/{r}/a-peer-tap.json'), 0, 'level_dbfs') for r in ('b0', 'b0-2', 'pts3'))
2793	0.000	^	z.3f	same(q(pt(r, p, c, t)['median']['ppm'], 3) for r in ('b0-2', 'pts3') for p in 'abc' for c, t in ((0, 997), (1, 9973)))
2793	-123.98		.2f	same(load('summary/pts3/c-b9-grade.json')['summary'][c + '_floor']['thdn_db_median'] for c in ('ch0', 'ch1'))
2793	-123.98		.2f	load('summary/b0-2/c-b9-grade.json')['summary']['ch0_floor']['thdn_db_median']
2793	-123.95		.2f	load('summary/b0-2/c-b9-grade.json')['summary']['ch1_floor']['thdn_db_median']
2793	0.0000		z.4f	load('summary/pts3/c-b9-grade.json')['phase_net_frames']
2793	10		.0f	load('summary/pts3/c-b9-grade.json')['seconds']
2793	0.0005		.4f	load('summary/b0-2/c-b9-grade.json')['phase_net_frames']
2793	300		.0f	load('summary/b0-2/c-b9-grade.json')['seconds']
2793	303.8	summary/b0-2/d-loop-decode.json	.1f	same(q(dec(r)['decoded'] / 48000, 1) for r in ('b0', 'b0-2'))
2795	06:28:50	summary/pts2/a-peer-tap.json	cest	d['info']['last_t']
2796	06:31:51	summary/b0/a-peer-tap.json	cest	d['info']['first_t']
2798	+6.94	summary/pts1/a-peer-tap.json	+.2f	min(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))
2798	+6.96	^	+.2f	max(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))
2801	five		s	rx('HANDOFF.md', r'^\| b17 \|.*?the log holds (\w+) underruns \(([\d:]+) to ([\d:]+), during offline grading\)')
2802	06:45:27		s	rx('HANDOFF.md', r'^\| b17 \|.*?the log holds (\w+) underruns \(([\d:]+) to ([\d:]+), during offline grading\)', group=2)
2802	06:46:38		s	rx('HANDOFF.md', r'^\| b17 \|.*?the log holds (\w+) underruns \(([\d:]+) to ([\d:]+), during offline grading\)', group=3)
2805	06:43:09	runs/b0-2/events.jsonl	cest	E('b0-2', 'capture-done', what='mcasp')['t']
2806	06:49:14	runs/pts3/events.jsonl	cest	E('pts3', 'captures-started')['started']['tap']
# B16b: B0
2813	1	runs/b0-2/events.jsonl	d	same(E(r, 'listener-read', listener='dut-in-1')['media_locked'] for r in ('b0', 'b0-2'))
2813	12	^	d	same(q(E(r, 'listener-read', listener='dut-in-1')['t'] - E(r, 'bind', listener='dut-in-1')['t'], 0) for r in ('b0', 'b0-2'))
2814	0x00000020	runs/b0-2/dut-before-binds.txt	s	same('0x%08x' % le32(mem(f'runs/{r}/dut-{w}.txt', '0x900008f8', 8)) for r in ('b0', 'b0-2') for w in ('before-binds', 'after-captures'))
2815	0	runs/b0-2/events.jsonl	d	same(x['source'] for r in ('b0', 'b0-2') for x in ev(r, 'clock-read', who='dut'))
2817	300	summary/b0-2/c-b9-grade.json	.0f	d['seconds']
2826	0.0005	^	.4f	d['phase_net_frames']
2826	131	r2/b0-2-receipt.json	d	d['degraded']
2827	3		d	Decimal(rx('tools/b9_thdn.py', r'^FLOOR_DB = ([\d.]+)'))
2827	0	r2/b0-2-receipt.json	d	d['degraded_runs'][0][0]
2827	18	^	d	d['degraded_runs'][0][1]
2828	28	^	d	d['degraded_runs'][1][0]
2828	31	^	d	d['degraded_runs'][1][1]
2828	43	^	d	d['degraded_runs'][2][0]
2828	44	^	d	d['degraded_runs'][2][1]
2828	46	^	d	d['degraded_runs'][3][0]
2828	54	^	d	d['degraded_runs'][3][1]
2829	1,637,452	^	,d	min(d['overlap']['frames_a'], d['overlap']['frames_b'])
2829	34.1	^	.1f	d['overlap']['seconds']
2830	0	^	d#0	d['overlap']['whole_blocks'][0]
2830	33	^	d	d['overlap']['whole_blocks'][1]
2830	131	^	d	d['degraded']
2830	23	^	d	d['overlap']['degraded_inside']
2830	0	^	d#1	d['overlap']['degraded_inside_runs'][0][0]
2830	18	^	d	d['overlap']['degraded_inside_runs'][0][1]
2830	28	^	d	d['overlap']['degraded_inside_runs'][1][0]
2830	31	^	d	d['overlap']['degraded_inside_runs'][1][1]
2831	23	^	d	d['overlap']['degraded_inside']
2832	108	^	d	d['overlap']['degraded_beyond']
2832	43	^	d	d['overlap']['degraded_beyond_runs'][0][0]
2832	251	^	d	d['overlap']['degraded_beyond_runs'][-1][1]
2833	thirteen	^	w	len(d['overlap']['degraded_beyond_runs'])
2836	34.1	^	.1f	d['overlap']['seconds']
2840	34.1	^	.1f	d['overlap']['seconds']
2842	-124	summary/b0-2/c-b9-grade.json	d	same(q(d['summary'][c + '_floor']['thdn_db_median'], 0) for c in ('ch0', 'ch1'))
2842	23	r2/b0-2-receipt.json	d	d['overlap']['degraded_inside']
2842	-100.61	^	.2f	d['tones']['997 Hz']['worst_inside']['thdn_db']
2842	-80.63	^	.2f	d['tones']['9,973 Hz']['worst_inside']['thdn_db']
2842	7	^	d	same(d['tones'][t]['worst_inside']['block'] for t in ('997 Hz', '9,973 Hz'))
2842	06:28:50		cest	load('summary/pts2/a-peer-tap.json')['info']['last_t']
2842	+6.94	summary/pts1/a-peer-tap.json	+.2f	min(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))
2842	+6.96	^	+.2f	max(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))
2842	13		.0f	min(x - [load('summary/b0-2/c-b9-grade.json')['summary'][c + '_floor']['thdn_db_median'] for c in ('ch0', 'ch1')][i % 2] for i, x in enumerate([load('summary/' + r + '/c-b9-grade.json')['summary'][c + '_floor']['thdn_db_median'] for r in ('pts1', 'pts2') for c in ('ch0', 'ch1')]))
2842	34		.0f	max(x - [load('summary/b0-2/c-b9-grade.json')['summary'][c + '_floor']['thdn_db_median'] for c in ('ch0', 'ch1')][i % 2] for i, x in enumerate([load('summary/' + r + '/c-b9-grade.json')['summary'][c + '_floor']['thdn_db_median'] for r in ('pts1', 'pts2') for c in ('ch0', 'ch1')]))
2842	10	summary/pts1/c-mcasp.json	.0f	same(load(f'summary/{r}/c-mcasp.json')['seconds'] for r in ('pts1', 'pts2'))
2842	108	r2/b0-2-receipt.json	d	d['overlap']['degraded_beyond']
2842	-100.47	^	.2f	d['tones']['997 Hz']['worst_beyond']['thdn_db']
2842	-80.48	^	.2f	d['tones']['9,973 Hz']['worst_beyond']['thdn_db']
2842	224	^	d	same(d['tones'][t]['worst_beyond']['block'] for t in ('997 Hz', '9,973 Hz'))
2842	23	^	d	d['overlap']['degraded_inside']
2842	39	^	d	same(d['tones'][t]['a_blocks'] for t in ('997 Hz', '9,973 Hz'))
2842	-102.55	^	.2f	d['tones']['997 Hz']['a_worst_db']
2842	-82.58	^	.2f	d['tones']['9,973 Hz']['a_worst_db']
2843	0	summary/b0-2/a-peer-tap.json	d	same(load(f'summary/b0-2/{p}.json')['info']['seq_gaps'] for p in ('a-peer-tap', 'b-dut-tap'))
2843	40	^	d	same(q(load(f'summary/b0-2/{p}.json')['seconds'], 0) for p in ('a-peer-tap', 'b-dut-tap'))
2844	108	r2/b0-2-receipt.json	d	d['overlap']['degraded_beyond']
2844	300	summary/b0-2/c-b9-grade.json	.0f	d['seconds']
2844	0.0005	^	.4f	d['phase_net_frames']
2844	34.1	r2/b0-2-receipt.json	.1f	d['overlap']['seconds']
2845	14,583,286		,d	load('summary/b0-2/d-loop-decode.json')['decoded']
2845	0		d#1	load('summary/b0-2/d-loop-decode.json')['net_step_frames']
2845	0		d#0	len(load('summary/b0-2/d-loop-decode.json')['events'])
2845	303	summary/b0-2/d-extcap-pair.json	d	same(n for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']) for n in (len(floor_inside(t)), len(inside(t['per_block']))))
2845	two		w	load('summary/pts2/d-loop-decode.json')['repeats']
2848	3,077,452	summary/b0-2/align-a-c.json	,d	sum(align(r, 'a')['compared_equal'] for r in ('pts1', 'pts2', 'pts3', 'b0-2'))
2848	3,077,980	summary/b0-2/align-b-c.json	,d	sum(align(r, 'b')['compared_equal'] for r in ('pts1', 'pts2', 'pts3', 'b0-2'))
2848	four	summary/b0-2/align-a-c.json	w	sum(1 for r in RUNS if (ROOT / f'summary/{r}/align-a-c.json').exists() and r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3'))
2852	0	runs/b0-2/dut-before-binds.txt	d	same(le32(mem(f'runs/{r}/dut-{w}.txt', '0x900008d4', 12), 4) for r in ('b0', 'b0-2') for w in ('before-binds', 'after-captures'))
2852	158		d	slipb('runs/b0-2/dut-before-binds.txt')
2852	160		d	slipb('runs/b0-2/dut-after-captures.txt')
2852	one		w	(slipb('runs/b0-2/dut-after-captures.txt') - slipb('runs/b0-2/dut-before-binds.txt')) // 2
2853	156		d	slipb('runs/b0/dut-before-binds.txt')
2853	158		d	slipb('runs/b0/dut-after-captures.txt')
# B16b: bench as left
2889	0205022001006000		s	cen('restore/census-endb.jsonl', 'format-dut-5-0')['payload'][8:]
2889	041060010000bb80		s	cen('restore/census-endb.jsonl', 'format-dut-5-1')['payload'][8:]
2889	0		d#1	payload_word(cen('restore/census-endb.jsonl', 'clock', 'dut'), 8)
2890	0205022002006000		s	cen('restore/census-endb.jsonl', 'format-peer-5-0')['payload'][8:]
2890	1		d#1	payload_word(cen('restore/census-endb.jsonl', 'clock', 'peer'), 8)
2891	44		d	census_reads('restore/census-startb.jsonl', 'restore/census-endb.jsonl', 'restore/census-compare-b16b.txt')[0]
2891	45		d	census_reads('restore/census-startb.jsonl', 'restore/census-endb.jsonl', 'restore/census-compare-b16b.txt')[1]
2892	276		d	nvm('restore/dut-startb.txt')['seq']
2892	286		d	nvm('restore/dut-endb.txt')['seq']
2892	42		d	nvm('restore/dut-startb.txt')['commits']
2892	52		d	nvm('restore/dut-endb.txt')['commits']
2892	0		d	nvm('restore/dut-endb.txt')['pend']
2893	06:52:19		cest	stamps('runs/b16b-tone-stop.txt', 'LOCK')[0]
2902	five		w	same([cdiff('restore/counters-endb.jsonl', 'restore/counters-startb.jsonl', 'peer', 6, 0, 0), cdiff('restore/counters-endb.jsonl', 'restore/counters-startb.jsonl', 'peer', 6, 0, 1)])
2903	one		w	same([cdiff('restore/counters-endb.jsonl', 'restore/counters-startb.jsonl', 'peer', 6, 0, 0), cdiff('restore/counters-endb.jsonl', 'restore/counters-startb.jsonl', 'peer', 6, 0, 1)]) // sum(1 for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') for b in ev(r, 'bind') if b['listener'] == 'dut-in-0')
2903	two		w	same([cdiff('restore/counters-endb.jsonl', 'restore/counters-startb.jsonl', 'peer', 6, 2, 0), cdiff('restore/counters-endb.jsonl', 'restore/counters-startb.jsonl', 'peer', 6, 2, 1)])
2906	152		d	slipb('restore/dut-startb.txt')
2906	162		d	slipb('restore/dut-endb.txt')
2906	five		w	(slipb('restore/dut-endb.txt') - slipb('restore/dut-startb.txt')) // 2
2907	five	runs/pts1/events.jsonl	w	sum(1 for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') for b in ev(r, 'bind') if b['listener'] == 'dut-in-0')
2908	one	runs/b0-2/dut-after-captures.txt	w	same(((le32(mem(f'runs/{r}/dut-after-captures.txt', '0x900008d4', 12)) & 0xffff) - (le32(mem(f'runs/{r}/dut-before-binds.txt', '0x900008d4', 12)) & 0xffff)) // 2 for r in ('b0', 'b0-2'))
2473	two	r2/source-receipt.json	w	sum(1 for k, r in d['reads'].items() if k.startswith('b16-') and r['kind'] == 'state')
2790	3		d	Decimal(rx('tools/b9_thdn.py', r'^FLOOR_DB = ([\d.]+)'))
# B16b: #629 acceptance
2917	five		w	(slipb('restore/dut-endb.txt') - slipb('restore/dut-startb.txt')) // 2
2917	five	runs/pts1/events.jsonl	w	sum(1 for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') for b in ev(r, 'bind') if b['listener'] == 'dut-in-0')
# B16b: limits
2924	Four	summary/b0-2/c-b9-grade.json	W	len([r for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') if (ROOT / f'summary/{r}/c-b9-grade.json').exists()])
2924	Three	summary/pts1/c-b9-grade.json	W	sum(1 for r in [r for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') if (ROOT / f'summary/{r}/c-b9-grade.json').exists()] if load(f'summary/{r}/c-b9-grade.json')['seconds'] == 10)
2925	10	^	.0f	same(grade(r)['seconds'] for r in ('pts1', 'pts2', 'pts3'))
2925	24	runs/pts1/events.jsonl	d	same(q(E(r, 'capture-done', what='tap')['seconds'], 0) for r in ('pts1', 'pts2', 'pts3'))
2925	300	summary/b0-2/c-b9-grade.json	.0f	d['seconds']
2925	40	summary/b0-2/a-peer-tap.json	d	same(q(load(f'summary/b0-2/{p}.json')['seconds'], 0) for p in ('a-peer-tap', 'b-dut-tap'))
2931	23	r2/b0-2-receipt.json	d	d['overlap']['degraded_inside']
2931	34.1	^	.1f	d['overlap']['seconds']
2932	108	^	d	d['overlap']['degraded_beyond']
# B16c: the resume
3001	07:48:07		cest	stamps('soc/b16c-precheck-status.log', 'LOCK')[0]
3005	07:48:16		cest	stamps('identity-b16c/lock-window.txt', 'LOCK')[0]
3005	07:48:22		cest	stamps('identity-b16c/lock-window.txt', 'UNLOCK')[0]
3005	44		d	census_reads('restore/census-endb.jsonl', 'restore/census-startc.jsonl', 'restore/census-compare-b16b-to-b16c.txt')[0]
3005	45		d	census_reads('restore/census-endb.jsonl', 'restore/census-startc.jsonl', 'restore/census-compare-b16b-to-b16c.txt')[1]
3006	8	controls/b16c-dryrun-summary.json	d#0	sum(v == 'PASS' for v in d['scenarios'].values())
3006	8	^	d#1	len(d['scenarios'])
3008	2.585	r2/bcrf-poll-trace.tsv	.3f	lock_bracket('bcrf')[0]
3008	3.161	r2/bcrf-poll-receipt.json	.3f	lock_bracket('bcrf')[1]
3008	596	^	d	win('bcrf')['servo']['LOCKED']
3008	-123.98	summary/bcrf/c-b9-grade.json	.2f	d['summary']['ch0_all']['thdn_db_median']
3008	-123.97	^	.2f	d['summary']['ch1_all']['thdn_db_median']
3008	300	^	d	d['summary']['blocks']
3008	300	^	d	d['summary']['blocks_at_floor']
3008	0	^	d#0	d['summary']['events']
3008	0.0000	^	z.4f	d['summary']['effective_offset_ppm']
3008	three	^	w	terms('bcrf')
3009	6.602	r2/baaf-poll-trace.tsv	.3f	lock_bracket('baaf')[0]
3009	7.180	r2/baaf-poll-receipt.json	.3f	lock_bracket('baaf')[1]
3009	596	^	d	win('baaf')['servo']['LOCKED']
3009	-123.98	summary/baaf/c-b9-grade.json	.2f	d['summary']['ch0_all']['thdn_db_median']
3009	-123.97	^	.2f	d['summary']['ch1_all']['thdn_db_median']
3009	300	^	d	same([d['summary']['blocks'], d['summary']['blocks_at_floor']])
3009	0	^	d#0	d['summary']['events']
3009	0.0000	^	z.4f	d['summary']['effective_offset_ppm']
3009	three	^	w	terms('baaf')
3010	34.2	summary/bcrf/align-a-c.json	.1f	min([align(r, p)['compared_equal'] / 48000 for r in ('bcrf', 'baaf') for p in 'ab'])
3010	34.3	^	.1f	max([align(r, p)['compared_equal'] / 48000 for r in ('bcrf', 'baaf') for p in 'ab'])
3010	0	summary/bcrf/d-loop-decode.json	d#0	same(len(dec(r)['events']) for r in ('bcrf', 'baaf'))
3010	0	^	d#1	same(dec(r)['net_step_frames'] for r in ('bcrf', 'baaf'))
# B16c: method
3020	one	runs/bcrf-lock.txt	w	same(len(stamps(f'runs/{r}-lock.txt', 'LOCK')) for r in ('bcrf', 'baaf'))
3026	1	runs/bcrf/events.jsonl	d	same(E(r, 'fol-check')['clk_peer'] for r in ('bcrf', 'baaf'))
3029	0.5	^	.1f	same(E(r, 'poll-start')['period_s'] for r in ('bcrf', 'baaf'))
3030	0	^	d#0	same(E(r, 'set-clock', tag='peer-internal')['readback'] for r in ('bcrf', 'baaf'))
3031	5	^	d	same(q(E(r, 'mark', tag='after-peer-set')['t'] - E(r, 'set-clock', tag='peer-internal')['t'], 0) for r in ('bcrf', 'baaf'))
3034	1	^	d#0	E('bcrf', 'set-clock', tag='bcrf')['readback']
3034	2	runs/baaf/events.jsonl	d#0	E('baaf', 'set-clock', tag='baaf')['readback']
3035	60		d	Decimal(rx('tools/run_b16c.py', r'^LOCK_WAIT_S = ([\d.]+)'))
3036	20	runs/bcrf/events.jsonl	d	same(q(E(r, 'captures-started')['started']['tap'] - E(r, 'set-clock', who='dut', tag=r)['t'], 0) for r in ('bcrf', 'baaf'))
3037	300	summary/bcrf/c-b9-grade.json	.0f	same(grade(r)['seconds'] for r in ('bcrf', 'baaf'))
3039	40	summary/bcrf/a-peer-tap.json	d	same(q(load(f'summary/{r}/{p}.json')['seconds'], 0) for r in ('bcrf', 'baaf') for p in ('a-peer-tap', 'b-dut-tap'))
3040	20	runs/bcrf/events.jsonl	d	same(q(E(r, 'mark', tag='window-mark-0')['t'] - E(r, 'set-clock', who='dut', tag=r)['t'], 0) for r in ('bcrf', 'baaf'))
3041	6	^	d	same(q(E(r, 'captures-started')['started']['mcasp'] + r2lead() - E(r, 'mark', tag='window-mark-0')['t'], 0) for r in ('bcrf', 'baaf'))
3041	15	^	d	same(q(E(r, 'captures-started')['started']['mcasp'] + r2lead() + 300 - E(r, 'mark', tag='window-mark-2')['t'], 0) for r in ('bcrf', 'baaf'))
3044	1	^	d	same(E(r, 'set-clock', who='peer', tag='restore')['readback'] for r in ('bcrf', 'baaf'))
3048	eight	^	w	sum(len(ev(r, 'mcasp-playback-check')) for r in ('bcrf', 'baaf'))
3053	07:50:00		cest#0	stamps('runs/bcrf-lock.txt', 'LOCK')[0]
3053	07:56:15		cest#0	stamps('runs/bcrf-lock.txt', 'UNLOCK')[0]
3053	07:50:12.3	runs/bcrf/events.jsonl	cest1#0	E('bcrf', 'set-clock', tag='peer-internal')['t']
3053	07:50:17.5	^	cest1#0	E('bcrf', 'bind', i=-1)['t']
3053	1	^	d#0	E('bcrf', 'set-clock', tag='bcrf')['readback']
3053	07:50:29.7	^	cest1#0	E('bcrf', 'set-clock', tag='bcrf')['t']
3053	07:50:55	^	cest#0	E('bcrf', 'captures-started')['started']['mcasp'] + r2lead()
3053	07:55:55	^	cest#0	E('bcrf', 'captures-started')['started']['mcasp'] + r2lead() + load('summary/bcrf/c-b9-grade.json')['seconds']
3053	26	^	d#0	q(E('bcrf', 'captures-started')['started']['mcasp'] + r2lead() - E('bcrf', 'set-clock', tag='bcrf')['t'], 0)
3053	07:56:00.0	^	cest1#0	E('bcrf', 'teardown')['t']
3053	07:56:04.0	^	cest1#0	E('bcrf', 'mark', tag='after-restore')['t']
3054	07:56:52		cest#0	stamps('runs/baaf-lock.txt', 'LOCK')[0]
3054	08:03:07		cest#0	stamps('runs/baaf-lock.txt', 'UNLOCK')[0]
3054	07:57:04.1	runs/baaf/events.jsonl	cest1#0	E('baaf', 'set-clock', tag='peer-internal')['t']
3054	07:57:09.3	^	cest1#0	E('baaf', 'bind', i=-1)['t']
3054	2	^	d#0	E('baaf', 'set-clock', tag='baaf')['readback']
3054	07:57:21.5	^	cest1#0	E('baaf', 'set-clock', tag='baaf')['t']
3054	07:57:47	^	cest#0	E('baaf', 'captures-started')['started']['mcasp'] + r2lead()
3054	08:02:47	^	cest#0	E('baaf', 'captures-started')['started']['mcasp'] + r2lead() + load('summary/baaf/c-b9-grade.json')['seconds']
3054	26	^	d#0	q(E('baaf', 'captures-started')['started']['mcasp'] + r2lead() - E('baaf', 'set-clock', tag='baaf')['t'], 0)
3054	08:02:51.7	^	cest1#0	E('baaf', 'teardown')['t']
3054	08:02:55.7	^	cest1#0	E('baaf', 'mark', tag='after-restore')['t']
2987	two	summary/pts2/d-loop-decode.json	w	d['repeats']
3056	two	controls/b16c-dryrun-summary.json	w	sum(1 for k in d['scenarios'] if k in ('bcrf', 'baaf'))
3058	eight	^	w	len(d['scenarios'])
3069	8	^	d#0	sum(v == 'PASS' for v in d['scenarios'].values())
3069	8	^	d#1	len(d['scenarios'])
3078	3		d	Decimal(rx('tools/b9_thdn.py', r'^FLOOR_DB = ([\d.]+)'))
3080	0.01	summary/bcrf/a-peer-tap.json	.2f	bound(max(abs(t['median']['snr_db'] + t['median']['thdn_db']) for r in ('bcrf', 'baaf', 'b0-2') for p in PFILE_ for c in (0, 1) for t in [pt(r, p, c, (997, 9973)[c])]), '0.01')
# B16c: clock-source record
3086	0	runs/bcrf/events.jsonl	d#0	E('bcrf', 'set-clock', who='peer', tag='peer-internal')['src']
3086	0	^	d#1	E('bcrf', 'set-clock', who='peer', tag='peer-internal')['readback']
3087	1	^	d#0	E('bcrf', 'set-clock', who='dut', tag='bcrf')['src']
3087	1	^	d#1	E('bcrf', 'set-clock', who='dut', tag='bcrf')['readback']
3088	0	^	d#0	E('bcrf', 'set-clock', who='dut', tag='restore')['src']
3088	0	^	d#1	E('bcrf', 'set-clock', who='dut', tag='restore')['readback']
3089	1	^	d#0	E('bcrf', 'set-clock', who='peer', tag='restore')['src']
3089	1	^	d#1	E('bcrf', 'set-clock', who='peer', tag='restore')['readback']
3090	0	runs/baaf/events.jsonl	d#0	E('baaf', 'set-clock', who='peer', tag='peer-internal')['src']
3090	0	^	d#1	E('baaf', 'set-clock', who='peer', tag='peer-internal')['readback']
3091	2	^	d#0	E('baaf', 'set-clock', who='dut', tag='baaf')['src']
3091	2	^	d#1	E('baaf', 'set-clock', who='dut', tag='baaf')['readback']
3092	0	^	d#0	E('baaf', 'set-clock', who='dut', tag='restore')['src']
3092	0	^	d#1	E('baaf', 'set-clock', who='dut', tag='restore')['readback']
3093	1	^	d#0	E('baaf', 'set-clock', who='peer', tag='restore')['src']
3093	1	^	d#1	E('baaf', 'set-clock', who='peer', tag='restore')['readback']
3095	four	runs/bcrf/events.jsonl	w	same(len([m for m in ev(r, 'mark') if m['tag'] in ('window-mark-0', 'window-mark-1', 'window-mark-2', 'after-captures')]) for r in ('bcrf', 'baaf'))
3095	1	^	d	same(m['clock']['dut'] for m in ev('bcrf', 'mark') if m['tag'] in ('window-mark-0', 'window-mark-1', 'window-mark-2', 'after-captures'))
3095	2	runs/baaf/events.jsonl	d	same(m['clock']['dut'] for m in ev('baaf', 'mark') if m['tag'] in ('window-mark-0', 'window-mark-1', 'window-mark-2', 'after-captures'))
3095	0	runs/bcrf/events.jsonl	d	same(m['clock']['peer'] for r in ('bcrf', 'baaf') for m in ev(r, 'mark') if m['tag'] in ('window-mark-0', 'window-mark-1', 'window-mark-2', 'after-captures'))
3096	20	^	d	same(q(E(r, 'mark', tag='window-mark-0')['t'] - E(r, 'set-clock', who='dut', tag=r)['t'], 0) for r in ('bcrf', 'baaf'))
3096	6	^	d	same(q(E(r, 'captures-started')['started']['mcasp'] + r2lead() - E(r, 'mark', tag='window-mark-0')['t'], 0) for r in ('bcrf', 'baaf'))
3097	15	^	d	same(q(E(r, 'captures-started')['started']['mcasp'] + r2lead() + 300 - E(r, 'mark', tag='window-mark-2')['t'], 0) for r in ('bcrf', 'baaf'))
3097	0	^	d	same(E(r, 'mark', tag='after-restore')['clock']['dut'] for r in ('bcrf', 'baaf'))
3098	1	^	d	same(E(r, 'mark', tag='after-restore')['clock']['peer'] for r in ('bcrf', 'baaf'))
3101	0205022001006000	^	s	same(x['listener_fmt'] for r in ('bcrf', 'baaf') for x in ev(r, 'format-check', listener='dut-in-0') if x['set'] is None and x['talker_fmt'] == x['listener_fmt'])
3102	041060010000bb80	^	s	same(x['listener_fmt'] for r in ('bcrf', 'baaf') for x in ev(r, 'format-check', listener='dut-in-1') if x['set'] is None and x['talker_fmt'] == x['listener_fmt'])
# B16c: B-CRF and B-AAF
3108	Channels «2» and		d#0	same(tuple(c['channel'] for c in load(f'summary/{r}/{p}.json')['channels'] if c['min'] == -1 and c['max'] == 0) for r in ('bcrf', 'baaf') for p in ('a-peer-tap', 'b-dut-tap', 'c-mcasp'))[0]
3109	and «3» carry		d#0	same(tuple(c['channel'] for c in load(f'summary/{r}/{p}.json')['channels'] if c['min'] == -1 and c['max'] == 0) for r in ('bcrf', 'baaf') for p in ('a-peer-tap', 'b-dut-tap', 'c-mcasp'))[1]
3109	-1	summary/bcrf/a-peer-tap.json	d	same(c['min'] for c in [c for r in ('bcrf', 'baaf') for p in ('a-peer-tap', 'b-dut-tap', 'c-mcasp') for c in load(f'summary/{r}/{p}.json')['channels'] if c['channel'] in (2, 3)])
3109	0	^	d	same(c['max'] for c in [c for r in ('bcrf', 'baaf') for p in ('a-peer-tap', 'b-dut-tap', 'c-mcasp') for c in load(f'summary/{r}/{p}.json')['channels'] if c['channel'] in (2, 3)])
3142	0	summary/bcrf/c-b9-grade.json	d	same(grade(r)['effective_offset_ppm'] for r in ('bcrf', 'baaf'))
3142	0.000001	^	.6f	bound(max(abs(grade(r)['phase_net_frames']) for r in ('bcrf', 'baaf')), '0.000001')
3143	0.0005	summary/b0-2/c-b9-grade.json	.4f	d['phase_net_frames']
3149	1,646,473	summary/bcrf/align-b-c.json	,d	d['compared_equal']
3149	34.3	^	.1f#0	d['compared_equal'] / 48000
3149	0	^	d#0	d['frames_differing']
3149	0	^	d#1	len(d['slips'])
3149	1,647,859	summary/bcrf/align-a-c.json	,d	d['compared_equal']
3149	34.3	^	.1f#1	d['compared_equal'] / 48000
3149	0	^	d#2	d['frames_differing']
3149	0	^	d#3	len(d['slips'])
3150	1,644,390	summary/baaf/align-b-c.json	,d	d['compared_equal']
3150	34.3	^	.1f#0	d['compared_equal'] / 48000
3150	0	^	d#0	d['frames_differing']
3150	0	^	d#1	len(d['slips'])
3150	1,641,156	summary/baaf/align-a-c.json	,d	d['compared_equal']
3150	34.2	^	.1f#0	d['compared_equal'] / 48000
3150	0	^	d#2	d['frames_differing']
3150	0	^	d#3	len(d['slips'])
3157	14,583,391	summary/bcrf/d-loop-decode.json	,d	d['decoded']
3157	0	^	d#0	d['skips']
3157	0	^	d#1	d['repeats']
3157	0	^	d#2	d['net_step_frames']
3157	0	^	d#3	d['torn']
3157	-1.00		.2f	same([q(load('summary/bcrf/d-extcap-pair.json')['rows'][0]['tone_997']['median']['level_dbfs'], 2), q(load('summary/bcrf/d-extcap-pair.json')['rows'][1]['tone_9973']['median']['level_dbfs'], 2)])
3157	-146.06		.2f	load('summary/bcrf/d-extcap-pair.json')['rows'][0]['tone_997']['median']['thdn_db']
3157	-145.99		.2f	load('summary/bcrf/d-extcap-pair.json')['rows'][1]['tone_9973']['median']['thdn_db']
3157	303		d#0	same(len(floor_inside(t)) for t in (load('summary/bcrf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/bcrf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3157	303		d#1	same(len(inside(t['per_block'])) for t in (load('summary/bcrf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/bcrf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3157	306		d	same(len(t['per_block']) for t in (load('summary/bcrf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/bcrf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3157	0		d#4	same(silent(t['per_block'])[0] for t in (load('summary/bcrf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/bcrf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3157	1		d#0	same(silent(t['per_block'])[-1] for t in (load('summary/bcrf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/bcrf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3157	2		d#0	same(inside(t['per_block'])[0] - 1 for t in (load('summary/bcrf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/bcrf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3158	14,585,924	summary/baaf/d-loop-decode.json	,d	d['decoded']
3158	0	^	d#0	d['skips']
3158	0	^	d#1	d['repeats']
3158	0	^	d#2	d['net_step_frames']
3158	0	^	d#3	d['torn']
3158	-1.00		.2f	same([q(load('summary/baaf/d-extcap-pair.json')['rows'][0]['tone_997']['median']['level_dbfs'], 2), q(load('summary/baaf/d-extcap-pair.json')['rows'][1]['tone_9973']['median']['level_dbfs'], 2)])
3158	-146.06		.2f	load('summary/baaf/d-extcap-pair.json')['rows'][0]['tone_997']['median']['thdn_db']
3158	-145.99		.2f	load('summary/baaf/d-extcap-pair.json')['rows'][1]['tone_9973']['median']['thdn_db']
3158	303		d#0	same(len(floor_inside(t)) for t in (load('summary/baaf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/baaf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3158	303		d#1	same(len(inside(t['per_block'])) for t in (load('summary/baaf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/baaf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3158	306		d	same(len(t['per_block']) for t in (load('summary/baaf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/baaf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3158	0		d#4	same(silent(t['per_block'])[0] for t in (load('summary/baaf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/baaf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3158	1		d#0	same(silent(t['per_block'])[-1] for t in (load('summary/baaf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/baaf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3158	2		d#0	same(inside(t['per_block'])[0] - 1 for t in (load('summary/baaf/d-extcap-pair.json')['rows'][0]['tone_997'], load('summary/baaf/d-extcap-pair.json')['rows'][1]['tone_9973']))
3160	0	summary/bcrf/d-loop-decode.json	d	same(x['net_step_frames'] for x in [dec(r) for r in ('bcrf', 'baaf')])
3161	303.8		.1f	load('summary/bcrf/d-loop-decode.json')['decoded'] / 48000
3161	303.9		.1f	load('summary/baaf/d-loop-decode.json')['decoded'] / 48000
3161	one	controls/b16b-dloop-control.json	w	step_frames()
3162	one	^	w	step_frames()
3163	14.58	summary/bcrf/d-loop-decode.json	.2f	step_frames() * min(x['decoded'] for x in [dec(r) for r in ('bcrf', 'baaf')]) / Decimal(10 ** 6)
3163	0.07	^	.2f	step_frames() * Decimal(10 ** 6) / min(x['decoded'] for x in [dec(r) for r in ('bcrf', 'baaf')])
3129	300	summary/bcrf/c-b9-grade.json	.0f	same(grade(r)['seconds'] for r in ('bcrf', 'baaf'))
# B16c: the following record
3167	0.5	runs/bcrf/events.jsonl	.1f	same(E(r, 'poll-start')['period_s'] for r in ('bcrf', 'baaf'))
3174	2.585	r2/bcrf-poll-trace.tsv	.3f	lock_bracket('bcrf')[0]
3174	3.161	r2/bcrf-poll-receipt.json	.3f	lock_bracket('bcrf')[1]
3174	596	^	d#0	win('bcrf')['servo']['LOCKED']
3174	596	^	d#1	win('bcrf')['polls']
3174	-6.000	^	.3f	win('bcrf')['trim_ppm'][1]
3174	-6.125	^	.3f	win('bcrf')['trim_ppm'][0]
3174	+10.60	^	+.2f	win('bcrf')['crf_rate_ppm'][0]
3174	+10.65	^	+.2f	win('bcrf')['crf_rate_ppm'][1]
3174	0	^	d#0	same(int(x, 16) for x in win('bcrf')['aafm_stat'])
3174	0	^	d#1	same(win('bcrf')['slip_tdm_dups'] + win('bcrf')['slip_tdm_skips'])
3174	23	runs/bcrf/events.jsonl	d#0	E('bcrf', 'mark', tag='window-mark-0')['counters']['dut-0x0024-0'][0]
3174	22	^	d#0	E('bcrf', 'mark', tag='window-mark-0')['counters']['dut-0x0024-0'][1]
3174	23	^	d#1	E('bcrf', 'mark', tag='window-mark-2')['counters']['dut-0x0024-0'][0]
3174	22	^	d#1	E('bcrf', 'mark', tag='window-mark-2')['counters']['dut-0x0024-0'][1]
3175	6.602	r2/baaf-poll-trace.tsv	.3f	lock_bracket('baaf')[0]
3175	7.180	r2/baaf-poll-receipt.json	.3f	lock_bracket('baaf')[1]
3175	596	^	d#0	win('baaf')['servo']['LOCKED']
3175	596	^	d#1	win('baaf')['polls']
3175	-6.000	^	.3f	win('baaf')['trim_ppm'][1]
3175	-6.125	^	.3f	win('baaf')['trim_ppm'][0]
3175	+10.60	^	+.2f	win('baaf')['aafm_rate_ppm_valid'][0]
3175	+10.63	^	+.2f	win('baaf')['aafm_rate_ppm_valid'][1]
3175	+10.59	^	+.2f	win('baaf')['crf_rate_ppm'][0]
3175	+10.65	^	+.2f	win('baaf')['crf_rate_ppm'][1]
3175	0x001e0007	^	s	'0x' + same(win('baaf')['aafm_stat'])
3175	0	^	d#0	same((int(x, 16) >> 8) & 0xff for x in win('baaf')['aafm_stat'])
3175	30	^	d	same(int(x, 16) >> 16 for x in win('baaf')['aafm_stat'])
3175	0	^	d#1	same(win('baaf')['slip_tdm_dups'] + win('baaf')['slip_tdm_skips'])
3175	24	runs/baaf/events.jsonl	d#0	E('baaf', 'mark', tag='window-mark-0')['counters']['dut-0x0024-0'][0]
3175	23	^	d#0	E('baaf', 'mark', tag='window-mark-0')['counters']['dut-0x0024-0'][1]
3175	24	^	d#1	E('baaf', 'mark', tag='window-mark-2')['counters']['dut-0x0024-0'][0]
3175	23	^	d#1	E('baaf', 'mark', tag='window-mark-2')['counters']['dut-0x0024-0'][1]
3178	five		w	len(re.findall(r'\("0x9000[0-9a-f]+", \d+\)', rx('tools/console_poll_b8.py', r'^CMDS = \((.*)\)$')))
3180	44	r2/bcrf-poll-receipt.json	d	d['locked']['first_locked_poll'] - 1
3180	45	^	d	d['locked']['first_locked_poll']
3180	52	r2/baaf-poll-receipt.json	d	d['locked']['first_locked_poll'] - 1
3180	53	^	d	d['locked']['first_locked_poll']
3183	0x...0034	r2/bcrf-poll-receipt.json	s	'0x...' + sorted(set(win('bcrf')['mcsrv_stat_lo16']) | set(win('baaf')['mcsrv_stat_lo16']))[0]
3184	0x...0074	^	s	'0x...' + sorted(set(win('bcrf')['mcsrv_stat_lo16']) | set(win('baaf')['mcsrv_stat_lo16']))[1]
3184	580	^	d	win('bcrf')['mcsrv_stat_lo16']['0034']
3184	16	^	d	win('bcrf')['mcsrv_stat_lo16']['0074']
3185	584	r2/baaf-poll-receipt.json	d	win('baaf')['mcsrv_stat_lo16']['0034']
3185	12	^	d	win('baaf')['mcsrv_stat_lo16']['0074']
3188	15		s	rx('repo:docs/design/MEDIA_CLOCK_FOLLOWING.md', r'^\| B AAF \|.*Servo LOCKED within (\d+) s of the set')
3189	0		s	rx('repo:docs/design/MEDIA_CLOCK_FOLLOWING.md', r'^\| B AAF \|.*?; (\d+) net steps between')
3193	30	r2/baaf-poll-receipt.json	d	same(int(x, 16) >> 16 for x in win('baaf')['aafm_stat'])
3195	four	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	w	len(re.split(r', and |, ', b6_rule()))
3200	596		d#0	each((r, win(r)['servo']['LOCKED']) for r in ('bcrf', 'baaf'))
3200	596		d#1	each((r, win(r)['polls']) for r in ('bcrf', 'baaf'))
3200	2.585	r2/bcrf-poll-trace.tsv	.3f	lock_bracket('bcrf')[0]
3200	3.161	r2/bcrf-poll-receipt.json	.3f	lock_bracket('bcrf')[1]
3200	6.602	r2/baaf-poll-trace.tsv	.3f	lock_bracket('baaf')[0]
3200	7.180	r2/baaf-poll-receipt.json	.3f	lock_bracket('baaf')[1]
3201	0.5	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	re.search(r'within ([\d.]+) ppm', b6_rule()).group(1)
3201	0	summary/bcrf/d-loop-decode.json	d#0	same(dec(r)['net_step_frames'] for r in ('bcrf', 'baaf'))
3201	14,583,391		,d	load('summary/bcrf/d-loop-decode.json')['decoded']
3201	14,585,924		,d	load('summary/baaf/d-loop-decode.json')['decoded']
3201	14.58		.2f	min(load('summary/bcrf/d-loop-decode.json')['decoded'], load('summary/baaf/d-loop-decode.json')['decoded']) / Decimal(10 ** 6)
3201	0.07		.2f	Decimal(10 ** 6) / min(load('summary/bcrf/d-loop-decode.json')['decoded'], load('summary/baaf/d-loop-decode.json')['decoded'])
3201	0.0000	summary/bcrf/c-b9-grade.json	z.4f	same(grade(r)['effective_offset_ppm'] for r in ('bcrf', 'baaf'))
3203	0	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s#0	re.search(r'has (\d+) listener discontinuities', b6_rule()).group(1)
3203	0	summary/bcrf/c-b9-grade.json	d#1	same(grade(r)['summary']['events'] for r in ('bcrf', 'baaf'))
3203	300	^	.0f	same(grade(r)['seconds'] for r in ('bcrf', 'baaf'))
3203	0	summary/bcrf/d-loop-decode.json	d#2	same(len(dec(r)['events']) for r in ('bcrf', 'baaf'))
3196	four	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	w	len(re.split(r', and |, ', b6_rule()))
3205	three	summary/bcrf/c-b9-grade.json	w	same([terms('bcrf'), terms('baaf')])
3205	four	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	w	len(re.split(r', and |, ', b6_rule()))
3209	162		d	slipb('restore/dut-startc.txt')
3210	188		d	slipb('restore/dut-endc.txt')
3210	two	r2/bcrf-poll-receipt.json	w#0	same(x['dups'][1] - x['dups'][0] for x in [x for r in ('bcrf', 'baaf') for x in load(f'r2/{r}-poll-receipt.json')['slip_lb_steps']])
3210	two	^	w#1	same(len(x['polls']) for x in [x for r in ('bcrf', 'baaf') for x in load(f'r2/{r}-poll-receipt.json')['slip_lb_steps']])
3211	five	^	w	same([len(steps('bcrf', 'binds..dut-set')), len(steps('baaf', 'binds..dut-set'))])
3212	12.2	^	.1f	same(q(-load(f'r2/{r}-poll-receipt.json')['marks_after_set_s']['binds'], 1) for r in ('bcrf', 'baaf'))
3212	0.1	^	.1f	same([q(steps('bcrf', 'binds..dut-set')[0]['after_binds_s'][0], 1), q(steps('baaf', 'binds..dut-set')[0]['after_binds_s'][0], 1)])
3213	1.4	^	.1f	same([q(-steps('bcrf', 'binds..dut-set')[-1]['after_set_s'][1], 1), q(-steps('baaf', 'binds..dut-set')[-1]['after_set_s'][1], 1)])
3215	one	runs/b0-2/dut-after-captures.txt	w	same(((le32(mem(f'runs/{r}/dut-after-captures.txt', '0x900008d4', 12)) & 0xffff) - (le32(mem(f'runs/{r}/dut-before-binds.txt', '0x900008d4', 12)) & 0xffff)) // 2 for r in ('b0', 'b0-2'))
3219	one	r2/bcrf-poll-receipt.json	w	len(steps('bcrf', 'dut-set..first-locked-poll'))
3219	2.08	^	.2f	steps('bcrf', 'dut-set..first-locked-poll')[0]['after_set_s'][0]
3219	2.66	^	.2f	steps('bcrf', 'dut-set..first-locked-poll')[0]['after_set_s'][1]
3220	two	r2/baaf-poll-receipt.json	w	len(steps('baaf', 'dut-set..first-locked-poll'))
3220	2.08	^	.2f	steps('baaf', 'dut-set..first-locked-poll')[0]['after_set_s'][0]
3220	2.65	^	.2f	steps('baaf', 'dut-set..first-locked-poll')[0]['after_set_s'][1]
3220	5.10	^	.2f	steps('baaf', 'dut-set..first-locked-poll')[1]['after_set_s'][0]
3220	5.68	^	.2f	steps('baaf', 'dut-set..first-locked-poll')[1]['after_set_s'][1]
3224	12	r2/bcrf-poll-receipt.json	d	same(load(f'r2/{r}-poll-receipt.json')['spans']['restored..poll-end']['polls'] for r in ('bcrf', 'baaf'))
3224	2.0	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	rx(FIND_P, r'The listener ring slipped one frame ([\d.]+) to ([\d.]+) s after the servo first read LOCKED')
3224	3.0	^	s	rx(FIND_P, r'The listener ring slipped one frame ([\d.]+) to ([\d.]+) s after the servo first read LOCKED', group=2)
3228	0		d	same([counters('restore/counters-startc.jsonl', 'dut', 6, 0)[2], counters('restore/counters-startc.jsonl', 'dut', 6, 1)[2]])
3229	4		d	same([counters('restore/counters-endc.jsonl', 'dut', 6, 0)[2], counters('restore/counters-endc.jsonl', 'dut', 6, 1)[2], sum(len(ev(r, 'set-clock', who='dut')) for r in ('bcrf', 'baaf'))])
3229	one		s	rx('repo:docs/design/MEDIA_CLOCK_FOLLOWING.md', r'\| (One) MEDIA_RESET per switch on the DUT.s talker \(Milan v1\.2 Table 5\.4\)').lower()
3231	one	runs/bcrf/events.jsonl	w	same(mdiff(r, 'window-mark-0', 'after-peer-set', 'peer-0x0005-0', 4) for r in ('bcrf', 'baaf'))
3231	5	^	d	same(q(E(r, 'mark', tag='after-peer-set')['t'] - E(r, 'set-clock', tag='peer-internal')['t'], 0) for r in ('bcrf', 'baaf'))
3232	20	^	d	same(q(E(r, 'mark', tag='window-mark-0')['t'] - E(r, 'set-clock', who='dut', tag=r)['t'], 0) for r in ('bcrf', 'baaf'))
3233	one	^	w	same(mdiff(r, 'after-restore', 'after-captures', 'peer-0x0005-0', 4) for r in ('bcrf', 'baaf'))
3235	once	^	x	same(mdiff(r, 'window-mark-0', 'after-peer-set', 'dut-0x0024-0', i) for r in ('bcrf', 'baaf') for i in (0, 1))
3237	once	^	x	same(mdiff(r, 'after-restore', 'after-captures', 'peer-0x0024-0', i) for r in ('bcrf', 'baaf') for i in (0, 1))
# B16c: attribution
3244	-123.98/-123.97	summary/bcrf/a-peer-tap.json	s	fmt(pt('bcrf', 'a', 0, 997)['median']['thdn_db'], '.2f') + '/' + fmt(pt('bcrf', 'a', 1, 9973)['median']['thdn_db'], '.2f')
3244	-123.98/-123.98	summary/baaf/a-peer-tap.json	s	fmt(pt('baaf', 'a', 0, 997)['median']['thdn_db'], '.2f') + '/' + fmt(pt('baaf', 'a', 1, 9973)['median']['thdn_db'], '.2f')
3244	-123.93	summary/bcrf/a-peer-tap.json	.2f	same(q(pt(r, 'a', c, t)['worst_thdn_db'], 2) for r in ('bcrf', 'baaf') for c, t in ((0, 997), (1, 9973)))
3245	0	^	d	same(load(f'summary/{r}/{p}.json')['info']['seq_gaps'] for r in ('bcrf', 'baaf') for p in ('a-peer-tap', 'b-dut-tap'))
3246	34.2	summary/bcrf/align-a-c.json	.1f	min([align(r, p)['compared_equal'] / 48000 for r in ('bcrf', 'baaf') for p in 'ab'])
3246	34.3	^	.1f	max([align(r, p)['compared_equal'] / 48000 for r in ('bcrf', 'baaf') for p in 'ab'])
3246	300	summary/bcrf/c-b9-grade.json	.0f	same(grade(r)['seconds'] for r in ('bcrf', 'baaf'))
3246	0.000001	^	.6f	bound(max(abs(grade(r)['phase_net_frames']) for r in ('bcrf', 'baaf')), '0.000001')
3247	0	summary/bcrf/d-loop-decode.json	d#0	same(len(dec(r)['events']) for r in ('bcrf', 'baaf'))
3247	0	^	d#1	same(dec(r)['net_step_frames'] for r in ('bcrf', 'baaf'))
3247	14.58	^	.2f	min(x['decoded'] for x in [dec(r) for r in ('bcrf', 'baaf')]) / Decimal(10 ** 6)
3247	303	summary/bcrf/d-extcap-pair.json	d	same(n for r in ('bcrf', 'baaf') for t in (load(f'summary/{r}/d-extcap-pair.json')['rows'][0]['tone_997'], load(f'summary/{r}/d-extcap-pair.json')['rows'][1]['tone_9973']) for n in (len(floor_inside(t)), len(inside(t['per_block']))))
3250	3,289,015	summary/bcrf/align-a-c.json	,d	sum(align(r, 'a')['compared_equal'] for r in ('bcrf', 'baaf'))
3250	3,290,863	summary/bcrf/align-b-c.json	,d	sum(align(r, 'b')['compared_equal'] for r in ('bcrf', 'baaf'))
3252	34	summary/bcrf/align-a-c.json	d	same(q(x, 0) for x in [align(r, p)['compared_equal'] / 48000 for r in ('bcrf', 'baaf') for p in 'ab'])
3256	131	r2/b0-2-receipt.json	d	d['degraded']
3256	300	^	d	d['blocks']
3256	34.1	^	.1f	d['overlap']['seconds']
3257	23	^	d	d['overlap']['degraded_inside']
3258	39	^	d	same(d['tones'][t]['a_blocks'] for t in ('997 Hz', '9,973 Hz'))
3258	-102.6	^	.1f	d['tones']['997 Hz']['a_worst_db']
3258	-82.6	^	.1f	d['tones']['9,973 Hz']['a_worst_db']
3258	108	^	d	d['overlap']['degraded_beyond']
3261	618	r2/source-receipt.json	d	get(d, 'compare.2.both')
3262	668	^	d	get(d, 'compare.3.both')
3263	One	summary/b0-2/c-b9-grade.json	W	same([sum(1 for r in ('b0', 'b0-2') if (ROOT / f'summary/{r}/c-b9-grade.json').exists()), sum(1 for r in RUNS if r == 'bcrf'), sum(1 for r in RUNS if r == 'baaf')])
# B16c: the tone source, read only
3269	d9684a8f...		s	rx('runs/b16c-tone-start.txt', r'LOOP_SHA256 ([0-9a-f]{8})') + '...'
3269	07:49:29		cest	stamps('runs/b16c-tone-start.txt', 'STATUS')[0] - Decimal(rx('runs/b16c-tone-start.txt', r'hw_ptr : (\d+)')) / 48000
3269	08:03:52		cest	stamps('runs/b16c-tone-stop.txt', 'LOCK')[0]
3270	07:48	r2/source-receipt.json	hm	Decimal(clock(get(d, 'reads.b16c-state-1.at')))
3270	08:03	^	hm	Decimal(clock(get(d, 'reads.b16c-state-2.at')))
3271	07:49	^	hm	Decimal(clock(get(d, 'reads.b16c-meters-1.at')))
3271	08:03	^	hm	Decimal(clock(get(d, 'reads.b16c-meters-2.at')))
3272	-38.5	^	.1f	meter(('b16c-meters-1', 'b16c-meters-2', 'b16c-state-2'), 'the documented pair of outputs', 'leaving_dbfs')
3272	-14.0	^	.1f	meter(('b16c-meters-1', 'b16c-meters-2', 'b16c-state-2'), 'the second pair of outputs', 'leaving_dbfs')
3275	618	^	d	get(d, 'compare.2.both') if get(d, 'compare.2.differ') == 0 else None
3276	two	^	w#0	sum(1 for k, r in d['reads'].items() if k.startswith('b16c-') and r['kind'] == 'state')
3276	two	^	w#1	get(d, 'compare.3')['differ']
3276	668	^	d	get(d, 'compare.3')['both']
3278	two	^	w	same(x['messages'][0] for x in get(d, 'compare.3')['differing'])
3278	one	^	w	same(x['messages'][1] for x in get(d, 'compare.3')['differing'] if x['second_last_among_first'] and x['all_minus_infinity'])
3284	0.2	runs/bcrf/events.jsonl	.1f	same(q((E(r, 'tone-summary')['last_raw_ns'] - E(r, 'tone-summary')['first_raw_ns']) / Decimal(10 ** 9) / (E(r, 'tone-summary')['reads'] - 1), 1) for r in ('bcrf', 'baaf'))
3285	1,805	^	,d	E('bcrf', 'tone-summary')['states']['RUNNING'] if E('bcrf', 'tone-summary')['states'] == {'RUNNING': E('bcrf', 'tone-summary')['reads']} else None
3285	1,803	runs/baaf/events.jsonl	,d	E('baaf', 'tone-summary')['states']['RUNNING'] if E('baaf', 'tone-summary')['states'] == {'RUNNING': E('baaf', 'tone-summary')['reads']} else None
3285	one	runs/bcrf/events.jsonl	w	same(E(r, 'tone-summary')['trigger_times'] for r in ('bcrf', 'baaf'))
# B16c: bench as left
3294	0205022001006000		s	cen('restore/census-endc.jsonl', 'format-dut-5-0')['payload'][8:]
3294	041060010000bb80		s	cen('restore/census-endc.jsonl', 'format-dut-5-1')['payload'][8:]
3294	0		d#1	payload_word(cen('restore/census-endc.jsonl', 'clock', 'dut'), 8)
3295	1		d#1	payload_word(cen('restore/census-endc.jsonl', 'clock', 'peer'), 8)
3295	0	runs/bcrf/events.jsonl	d#2	same(E(r, 'set-clock', tag='peer-internal')['readback'] for r in ('bcrf', 'baaf'))
3295	1	^	d#2	same(E(r, 'set-clock', who='peer', tag='restore')['readback'] for r in ('bcrf', 'baaf'))
3295	once	^	x	same(len(ev(r, 'set-clock', tag='peer-internal')) for r in ('bcrf', 'baaf'))
3296	44		d	census_reads('restore/census-startc.jsonl', 'restore/census-endc.jsonl', 'restore/census-compare-b16c.txt')[0]
3296	45		d	census_reads('restore/census-startc.jsonl', 'restore/census-endc.jsonl', 'restore/census-compare-b16c.txt')[1]
3298	286		d	nvm('restore/dut-startc.txt')['seq']
3298	292		d	nvm('restore/dut-endc.txt')['seq']
3298	52		d	nvm('restore/dut-startc.txt')['commits']
3298	58		d	nvm('restore/dut-endc.txt')['commits']
3298	0		d	nvm('restore/dut-endc.txt')['pend']
3299	08:03:52		cest	stamps('runs/b16c-tone-stop.txt', 'LOCK')[0]
3308	two		w	same([cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 6, 0, 0), cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 6, 0, 1), cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 6, 2, 0), cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 6, 2, 1)])
3308	one		w	same([cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 6, 0, 0), cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 6, 0, 1), cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 6, 2, 0), cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 6, 2, 1)]) // sum(1 for r in RUNS if r in ('bcrf', 'baaf'))
3309	four		w	same([cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 5, 0, 4), cdiff('restore/counters-endc.jsonl', 'restore/counters-startc.jsonl', 'peer', 5, 8, 4)])
3310	0		d	same([counters('restore/counters-startc.jsonl', 'dut', 6, 0)[2], counters('restore/counters-startc.jsonl', 'dut', 6, 1)[2]])
3310	4		d	same([counters('restore/counters-endc.jsonl', 'dut', 6, 0)[2], counters('restore/counters-endc.jsonl', 'dut', 6, 1)[2]])
3312	22		d	counters('restore/counters-startc.jsonl', 'dut', 36, 0)[0]
3312	21		d	counters('restore/counters-startc.jsonl', 'dut', 36, 0)[1]
3312	24		d	counters('restore/counters-endc.jsonl', 'dut', 36, 0)[0]
3312	23		d	counters('restore/counters-endc.jsonl', 'dut', 36, 0)[1]
3313	6		d	counters('restore/counters-startc.jsonl', 'peer', 36, 0)[0]
3313	5		d	counters('restore/counters-startc.jsonl', 'peer', 36, 0)[1]
3313	8		d	counters('restore/counters-endc.jsonl', 'peer', 36, 0)[0]
3313	7		d	counters('restore/counters-endc.jsonl', 'peer', 36, 0)[1]
3314	162		d	slipb('restore/dut-startc.txt')
3314	188		d	slipb('restore/dut-endc.txt')
# B16c: #629 acceptance
3321	four	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	w	len(re.split(r', and |, ', b6_rule()))
3321	three	summary/bcrf/c-b9-grade.json	w	same([terms('bcrf'), terms('baaf')])
# B16c: limits
3333	One	^	W	same([sum(1 for r in ('b0', 'b0-2') if (ROOT / f'summary/{r}/c-b9-grade.json').exists()), sum(1 for r in RUNS if r == 'bcrf'), sum(1 for r in RUNS if r == 'baaf')])
3334	300	^	.0f	same(grade(r)['seconds'] for r in ('bcrf', 'baaf'))
3334	40	summary/bcrf/a-peer-tap.json	d	same(q(load(f'summary/{r}/{p}.json')['seconds'], 0) for r in ('bcrf', 'baaf') for p in ('a-peer-tap', 'b-dut-tap'))
3334	630	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	rx(FIND_P, r'^(\d+) s, untouched, from (\d+) s after the last bind or clock-source set')
3335	one	runs/bcrf-lock.txt	w	same(len(stamps(f'runs/{r}-lock.txt', 'LOCK')) for r in ('bcrf', 'baaf'))
3335	10	HANDOFF.md	d	lock_limit()
3340	+10.59	r2/bcrf-poll-receipt.json	+.2f	min(rates())
3340	+10.65	^	+.2f	max(rates())
3341	4	r2/bcrf-poll-trace.tsv	d	same(b for r in ('bcrf', 'baaf') for x in trace(r) if trace_state(x) in (3, 4) for b in [4 * ((int(x['0x8f8'], 16) >> 4) & 1)])
3347	108	r2/b0-2-receipt.json	d	d['overlap']['degraded_beyond']
3347	131	^	d	d['degraded']
3346	one	summary/b0-2/c-b9-grade.json	w	same([sum(1 for r in ('b0', 'b0-2') if (ROOT / f'summary/{r}/c-b9-grade.json').exists()), sum(1 for r in RUNS if r == 'bcrf'), sum(1 for r in RUNS if r == 'baaf')])
# B16, round 2: reduced receipts
3409	2026-10-12	git:35e332b6	date	commit_time('35e332b6')
3415	-123.98	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'\| (-[\d.]+) dB on both tones, `pts3` and `b0-2` \|')
3415	-123.98	r2/b0-2-receipt.json	.2f	d['tones']['997 Hz']['floor_median_db']
3415	-123.95	^	.2f	d['tones']['9,973 Hz']['floor_median_db']
3415	-123.98		.2f	same(load('summary/pts3/c-b9-grade.json')['summary'][c + '_floor']['thdn_db_median'] for c in ('ch0', 'ch1'))
3416	0	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'runs of blocks: (\d+) to (\d+), (\d+) to (\d+), (\d+) to (\d+) and later runs', 1)
3416	18	^	s	was(r'runs of blocks: (\d+) to (\d+), (\d+) to (\d+), (\d+) to (\d+) and later runs', 2)
3416	28	^	s	was(r'runs of blocks: (\d+) to (\d+), (\d+) to (\d+), (\d+) to (\d+) and later runs', 3)
3416	31	^	s	was(r'runs of blocks: (\d+) to (\d+), (\d+) to (\d+), (\d+) to (\d+) and later runs', 4)
3416	43	^	s	was(r'runs of blocks: (\d+) to (\d+), (\d+) to (\d+), (\d+) to (\d+) and later runs', 5)
3416	54	^	s	was(r'runs of blocks: (\d+) to (\d+), (\d+) to (\d+), (\d+) to (\d+) and later runs', 6)
3416	0	r2/b0-2-receipt.json	d	d['degraded_runs'][0][0]
3416	18	^	d	d['degraded_runs'][0][1]
3416	28	^	d	d['degraded_runs'][1][0]
3416	31	^	d	d['degraded_runs'][1][1]
3416	43	^	d	d['degraded_runs'][2][0]
3416	44	^	d	d['degraded_runs'][2][1]
3416	46	^	d	d['degraded_runs'][3][0]
3416	54	^	d	d['degraded_runs'][3][1]
3416	eleven	^	w	len(d['degraded_runs']) - 4
3416	45	^	d	next(i for i in range(d['degraded_runs'][2][1] + 1, d['degraded_runs'][3][0]))
3417	06:38:03	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'McASP0 300 s from ([\d:]+) while playing the loop')
3417	24	^	s	was(r'It starts (\d+) s after the last bind')
3417	06:38:05.2	runs/b0-2/events.jsonl	cest1	E('b0-2', 'captures-started')['started']['mcasp'] + r2lead()
3417	26	r2/b0-2-receipt.json	.0f	d['timing']['recording_after_binds_s']
3417	06:38:03.2	runs/b0-2/events.jsonl	cest1	E('b0-2', 'captures-started')['started']['mcasp']
3417	2	tools/run_b16.py	d	r2lead()
3418	06:28:25	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'\| As `pts1`, from ([\d:]+)\. McASP0 also plays')
3418	06:28:31.5	runs/pts2/events.jsonl	cest1	E('pts2', 'captures-started')['started']['mcasp'] + r2lead()
3418	2	tools/run_b16.py	d	r2lead()
3419	Three	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'the tone path\. All (\w+) are met here\.').capitalize()
3419	four	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	w	len(re.split(r', and |, ', b6_rule()))
3419	three	summary/bcrf/c-b9-grade.json	w	same([terms('bcrf'), terms('baaf')])
3420	131	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'There its talker stream already held (\d+) blocks off the floor')
3420	131	r2/b0-2-receipt.json	d	d['degraded']
3420	23	^	d	d['overlap']['degraded_inside']
3420	34.1	^	.1f	d['overlap']['seconds']
3420	108	^	d	d['overlap']['degraded_beyond']
3421	20	runs/bcrf/events.jsonl	d	same(q(E(r, 'mark', tag='window-mark-0')['t'] - E(r, 'set-clock', who='dut', tag=r)['t'], 0) for r in ('bcrf', 'baaf'))
3421	6	^	d	same(q(E(r, 'captures-started')['started']['mcasp'] + r2lead() - E(r, 'mark', tag='window-mark-0')['t'], 0) for r in ('bcrf', 'baaf'))
3422	Four	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'1,255 both hold, (\w+) differ').capitalize()
3422	Two	r2/source-receipt.json	W	sum(1 for x in get(d, 'compare.1')['differing'] if x['cls'] != 'an input of a monitoring mix')
3422	two	^	w	sum(1 for x in get(d, 'compare.1')['differing'] if x['cls'] == 'an input of a monitoring mix')
3423	-135.2	^	.1f	max(get(d, 'reads.' + k + '.meters.every other output.largest_before_setting_dbfs') for k in ('b16-state-1', 'b16-meters-1', 'b16-meters-2', 'b16-state-2'))
3424	2.66	git:e20fd282:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s	was(r'- B-CRF: one step, ([\d.]+) s after the set;')
3424	2.65	^	s	was(r'- B-AAF: two steps, ([\d.]+) s and ([\d.]+) s after the set\.')
3424	5.68	^	s	was(r'- B-AAF: two steps, ([\d.]+) s and ([\d.]+) s after the set\.', 2)
3424	two	r2/bcrf-poll-receipt.json	w	same(len(x['polls']) for x in [x for r in ('bcrf', 'baaf') for x in load(f'r2/{r}-poll-receipt.json')['slip_lb_steps']])
3424	2.08	^	.2f	steps('bcrf', 'dut-set..first-locked-poll')[0]['after_set_s'][0]
3424	2.66	^	.2f	steps('bcrf', 'dut-set..first-locked-poll')[0]['after_set_s'][1]
3424	2.08	r2/baaf-poll-receipt.json	.2f	steps('baaf', 'dut-set..first-locked-poll')[0]['after_set_s'][0]
3424	2.65	^	.2f	steps('baaf', 'dut-set..first-locked-poll')[0]['after_set_s'][1]
3424	5.10	^	.2f	steps('baaf', 'dut-set..first-locked-poll')[1]['after_set_s'][0]
3424	5.68	^	.2f	steps('baaf', 'dut-set..first-locked-poll')[1]['after_set_s'][1]
3436	two	r2/bcrf-poll-receipt.json	w	same(len(x['polls']) for x in [x for r in ('bcrf', 'baaf') for x in load(f'r2/{r}-poll-receipt.json')['slip_lb_steps']])
3437	eight	r2/bcrf-poll-trace.tsv	w	same(len([k for k in trace(r)[0] if k.startswith('0x')]) for r in ('bcrf', 'baaf'))
3439	2.657	r2/bcrf-poll-receipt.json	.3f	same([d['locked']['recomputed_s'][0], d['locked']['published'][0], E('bcrf', 'servo-state')['s_lo']])
3439	3.161	^	.3f	same([d['locked']['recomputed_s'][1], d['locked']['published'][1], E('bcrf', 'servo-state')['s_hi']])
3439	6.68		.2f	same([load('r2/baaf-poll-receipt.json')['locked']['recomputed_s'][0], E('baaf', 'servo-state')['s_lo']])
3440	7.18		.2f	same([load('r2/baaf-poll-receipt.json')['locked']['recomputed_s'][1], E('baaf', 'servo-state')['s_hi']])
3442	2.585	r2/bcrf-poll-trace.tsv	.3f	lock_bracket('bcrf')[0]
3442	6.602	r2/baaf-poll-trace.tsv	.3f	lock_bracket('baaf')[0]
3444	twelve	r2/source-receipt.json	w	len(d['reads'])
3445	four	^	w	same(sum(1 for k in d['reads'] if k.split('-')[0] == lane) for lane in ('b16', 'b16b', 'b16c'))
3458	6	controls/r2-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3458	6	^	d#1	len(d['controls'])
3470	twelve	r2/source-receipt.json	w	len(d['reads'])
3474	twelve	RAW-ARTIFACTS.json	w	sum(1 for x in d['files'] if x['path'].startswith('source/'))
3493	two	^	w	sum(1 for x in d['files'] if x['path'].endswith('/poll-run.jsonl'))
3494	9cfc79bb...	^	s	same([raw('bcrf/poll-run.jsonl')['sha256'], load('r2/bcrf-poll-receipt.json')['raw']['sha256']])[:8] + '...'
3494	476a0077...	^	s	same([raw('baaf/poll-run.jsonl')['sha256'], load('r2/baaf-poll-receipt.json')['raw']['sha256']])[:8] + '...'
3510	6	controls/r2-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3510	6	^	d#1	len(d['controls'])
3384	8	controls/b16c-dryrun-summary.json	d#0	sum(v == 'PASS' for v in d['scenarios'].values())
3384	8	^	d#1	len(d['scenarios'])
2672	2	runs/b0/events.jsonl	d#0	int(E('b0', 'bind', listener='dut-in-1')['talker'].split('-')[-1])
2672	1	^	d#0	int(E('b0', 'bind', talker='peer-out-2')['listener'].split('-')[-1])
2812	1	runs/b0-2/events.jsonl	d#0	same(int(E(r, 'bind', talker='peer-out-2')['listener'].split('-')[-1]) for r in ('b0', 'b0-2'))
2812	0	^	d#0	same(int(E(r, 'bind', talker='peer-out-0')['listener'].split('-')[-1]) for r in ('b0', 'b0-2'))
2890	0		d#1	cen('restore/census-endb.jsonl', 'rx-state-peer-0')['talker_uid'] if cen('restore/census-endb.jsonl', 'rx-state-peer-0')['talker'] == '020000fffe000001' else None
2890	1		d#0	cen('restore/census-endb.jsonl', 'rx-state-peer-8')['talker_uid'] if cen('restore/census-endb.jsonl', 'rx-state-peer-8')['talker'] == '020000fffe000001' else None
3295	0		d#1	cen('restore/census-endc.jsonl', 'rx-state-peer-0')['talker_uid'] if cen('restore/census-endc.jsonl', 'rx-state-peer-0')['talker'] == '020000fffe000001' else None
3295	1		d#0	cen('restore/census-endc.jsonl', 'rx-state-peer-8')['talker_uid'] if cen('restore/census-endc.jsonl', 'rx-state-peer-8')['talker'] == '020000fffe000001' else None
3027	1	runs/bcrf/events.jsonl	d#0	same(E(r, 'fol-check')['peer_in_8']['talker_uid'] for r in ('bcrf', 'baaf'))
3032	1	^	d#0	same(int(E(r, 'bind', talker='peer-out-2')['listener'].split('-')[-1]) for r in ('bcrf', 'baaf'))
3033	0	^	d#0	same(int(E(r, 'bind', talker='peer-out-0')['listener'].split('-')[-1]) for r in ('bcrf', 'baaf'))
3532	122.475	summary/pts3/a-peer-tap.json	s	T(d, 1, 'snr_db')
3532	122.48	^	.2f	T(d, 1, 'snr_db')
3533	06:22:34.993	identity-b16b/lock-window.txt	cest3	stamps(p, 'UNLOCK')[0]
3534	06:22:34	^	cest	stamps(p, 'UNLOCK')[0]
3554	5	controls/r3-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3554	5	^	d#1	len(d['controls'])
3595	two	RAW-ARTIFACTS.json	w	same([sum(1 for x in d['files'] if x['path'].startswith('playback/')), sum(1 for v in load('r3/playback-logs.json')['logs'].values() if 'sha256' in v)])
3603	06:02:00	r3/playback-logs.json	s	d['logs']['b16']['modified']
3603	0	^	d#0	d['logs']['b16']['underrun_lines']
3603	dab353b5ead02cb68b5ecebc757786c48b7672e6f93a37a152e37aedf9dfe43b	RAW-ARTIFACTS.json	s	same([raw('playback/b16-tone-play.log')['sha256'], load('r3/playback-logs.json')['logs']['b16']['sha256']])
3604	08:03:53	r3/playback-logs.json	s	d['logs']['b16c']['modified']
3604	0	^	d#0	d['logs']['b16c']['underrun_lines']
3604	dab353b5ead02cb68b5ecebc757786c48b7672e6f93a37a152e37aedf9dfe43b	RAW-ARTIFACTS.json	s	same([raw('playback/b16c-tone-play.log')['sha256'], load('r3/playback-logs.json')['logs']['b16c']['sha256']])
3606	two	^	w	len({x['sha256'] for x in d['files'] if x['path'].startswith('playback/')}) == 1 and sum(1 for x in d['files'] if x['path'].startswith('playback/'))
3564	-123.98		s	was('\\(a\\) at (-[\\d.]+) dB median, worst block (-[\\d.]+) dB, on both tones in both cases', 1, at='35e332b6')
3564	-123.93		s	was('\\(a\\) at (-[\\d.]+) dB median, worst block (-[\\d.]+) dB, on both tones in both cases', 2, at='35e332b6')
3564	-123.98/-123.97	summary/bcrf/a-peer-tap.json	s	fmt(pt('bcrf', 'a', 0, 997)['median']['thdn_db'], '.2f') + '/' + fmt(pt('bcrf', 'a', 1, 9973)['median']['thdn_db'], '.2f')
3564	-123.98/-123.98	summary/baaf/a-peer-tap.json	s	fmt(pt('baaf', 'a', 0, 997)['median']['thdn_db'], '.2f') + '/' + fmt(pt('baaf', 'a', 1, 9973)['median']['thdn_db'], '.2f')
3564	-123.93	summary/bcrf/a-peer-tap.json	.2f	same(q(pt(r, 'a', c, t)['worst_thdn_db'], 2) for r in ('bcrf', 'baaf') for c, t in ((0, 997), (1, 9973)))
3565	305		s	was('at the floor in (\\d+) of (\\d+) blocks; block 2', 1, at='35e332b6')
3565	306		s	was('at the floor in (\\d+) of (\\d+) blocks; block 2', 2, at='35e332b6')
3565	13		s	was("the loop's floor, in (\\d+) of (\\d+) blocks\\.", 1, at='35e332b6')
3565	16		s	was("the loop's floor, in (\\d+) of (\\d+) blocks\\.", 2, at='35e332b6')
3565	303	summary/b0-2/d-extcap-pair.json	d	same(n for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']) for n in (len(floor_inside(t)), len(inside(t['per_block']))))
3565	11	summary/pts2/d-extcap-pair.json	d	same(len(floor_inside(t)) for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
3565	13	^	d#1	same(len(inside(t['per_block'])) for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
3565	6	^	d#0	same([i for i in inside(t['per_block']) if i not in floor_inside(t)][0] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
3565	12	^	d#0	same([i for i in inside(t['per_block']) if i not in floor_inside(t)][1] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
3565	0	summary/b0-2/d-extcap-pair.json	d#0	same(silent(t['per_block'])[0] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
3565	1	^	d#0	same(silent(t['per_block'])[-1] for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
3565	2	^	d#0	same(inside(t['per_block'])[0] - 1 for t in (d['rows'][0]['tone_997'], d['rows'][1]['tone_9973']))
3566	15	summary/pts2/ctl-dut-talker-dut-tap.json	d	same(n for x in taps2() for n in (len(floor_inside(x)), len(inside(x['per_block']))))
3567	2.66		s	was('\\| B-CRF \\| ([\\d.]+) to ([\\d.]+) s; ACQUIRE', 1, at='35e332b6')
3567	3.16		s	was('\\| B-CRF \\| ([\\d.]+) to ([\\d.]+) s; ACQUIRE', 2, at='35e332b6')
3567	6.68		s	was('\\| B-AAF \\| ([\\d.]+) to ([\\d.]+) s; ACQUIRE', 1, at='35e332b6')
3567	7.18		s	was('\\| B-AAF \\| ([\\d.]+) to ([\\d.]+) s; ACQUIRE', 2, at='35e332b6')
3567	2.585	r2/bcrf-poll-trace.tsv	.3f	lock_bracket('bcrf')[0]
3567	3.161	r2/bcrf-poll-receipt.json	.3f	lock_bracket('bcrf')[1]
3567	6.602	r2/baaf-poll-trace.tsv	.3f	lock_bracket('baaf')[0]
3567	7.180	r2/baaf-poll-receipt.json	.3f	lock_bracket('baaf')[1]
3568	Two		s	was('So (\\w+) settings changed: the clock setting', 1, at='35e332b6').capitalize()
3568	1,255	r2/source-receipt.json	,d	get(d, 'compare.1')['both']
3568	618	^	d	get(d, 'compare.2.both')
3568	668	^	d	get(d, 'compare.3.both')
3569	five	r2/bcrf-poll-receipt.json	w	same([len(steps('bcrf', 'binds..dut-set')), len(steps('baaf', 'binds..dut-set'))])
3569	one	runs/b0-2/dut-after-captures.txt	w	same((slipb(f'runs/{r}/dut-after-captures.txt') - slipb(f'runs/{r}/dut-before-binds.txt')) // 2 for r in ('b0', 'b0-2'))
3570	4	r2/bcrf-poll-trace.tsv	d	same(b for r in ('bcrf', 'baaf') for x in trace(r) if trace_state(x) in (3, 4) for b in [4 * ((int(x['0x8f8'], 16) >> 4) & 1)])
3576	05:45:07		s	was('\\| Identity gate \\| PASS, ([\\d:]+) to ([\\d:]+) CEST \\|', 1, at='35e332b6')
3576	05:45:13		s	was('\\| Identity gate \\| PASS, ([\\d:]+) to ([\\d:]+) CEST \\|', 2, at='35e332b6')
3576	05:45:06	identity/lock-window.txt	cest	stamps(p, 'LOCK')[0]
3576	05:45:12	^	cest	stamps(p, 'UNLOCK')[0]
3577	05:55:38		s	was('inputs through the authorised tone source, from ([\\d:]+) to ([\\d:]+) CEST', 1, at='35e332b6')
3577	06:02:00		s	was('inputs through the authorised tone source, from ([\\d:]+) to ([\\d:]+) CEST', 2, at='35e332b6')
3577	05:55:37	runs/tone-start.txt	cest	stamps(p, 'STATUS')[0] - Decimal(rx(p, r'hw_ptr : (\d+)')) / 48000
3577	06:01:59	runs/tone-stop.txt	cest	stamps(p, 'LOCK')[0]
3578	05:56:31		s	was('\\| `loop1` \\| ([\\d:]+) to ([\\d:]+) \\|', 1, at='35e332b6')
3578	05:57:31		s	was('\\| `loop1` \\| ([\\d:]+) to ([\\d:]+) \\|', 2, at='35e332b6')
3578	06:00:29		s	was('\\| `loop2` \\| [\\d:]+ to ([\\d:]+) \\|', 1, at='35e332b6')
3578	05:56:30	runs/loop1-lock.txt	cest	stamps(p, 'LOCK')[0]
3578	05:57:30	^	cest	stamps(p, 'UNLOCK')[0]
3578	06:00:28	runs/loop2-lock.txt	cest	stamps(p, 'UNLOCK')[0]
3579	49		s	was('in the remaining (\\d+) s of the capture', 1, at='35e332b6')
3579	49.6	summary/loop2/acmp-peer-tap.json	.1f	E('loop2', 'capture-done', what='tap')['seconds'] - acmp('CONNECT_TX_COMMAND', 1)
3580	0x0002		s	was('same: rx state flags `(0x[0-9a-f]+)`, stream ID (\\d+),', 1, at='35e332b6')
3580	0		s#0	was('same: rx state flags `(0x[0-9a-f]+)`, stream ID (\\d+),', 2, at='35e332b6')
3580	0	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	s#1	rx(FIND_P, r'nothing\. Its counters stayed (\d+) and its digital output read exact zero')
3581	05:48		s	was('at ([\\d:]+) and ([\\d:]+) CEST\\. The two reads are identical', 1, at='35e332b6')
3581	06:01		s#0	was('at ([\\d:]+) and ([\\d:]+) CEST\\. The two reads are identical', 2, at='35e332b6')
3581	05:47	r2/source-receipt.json	hm	Decimal(clock(get(d, 'reads.b16-state-1.at')))
3581	06:01	^	hm#1	Decimal(clock(get(d, 'reads.b16-state-2.at')))
3582	06:20		s	was('resumed at ([\\d:]+) CEST on the same image, branch', 1, at='35e332b6')
3582	06:22:23	soc/b16b-precheck-status.log	cest	stamps(p, 'LOCK')[0]
3583	-14.14		s	was('at (-[\\d.]+) dBFS before ([\\d:]+) CEST and (-[\\d.]+) dBFS after', 1, at='35e332b6')
3583	06:29		s	was('at (-[\\d.]+) dBFS before ([\\d:]+) CEST and (-[\\d.]+) dBFS after', 2, at='35e332b6')
3583	-14.10		s	was('at (-[\\d.]+) dBFS before ([\\d:]+) CEST and (-[\\d.]+) dBFS after', 3, at='35e332b6')
3583	06:28:50	summary/pts2/a-peer-tap.json	cest	d['info']['last_t']
3583	06:31:51	summary/b0/a-peer-tap.json	cest	d['info']['first_t']
3584	+3.00		s	was('\\| (\\+[\\d.]+) frames in 10 s, smooth', 1, at='35e332b6')
3584	10	summary/pts1/c-b9-grade.json	.0f	same(grade(r)['seconds'] for r in ('pts1', 'pts2'))
3584	+3.00	^	+.2f	d['phase_net_frames']
3584	+3.01	summary/pts2/c-b9-grade.json	+.2f	d['phase_net_frames']
3585	+6.95		s	was('The (\\+[\\d.]+) ppm tone advanced', 1, at='35e332b6')
3585	+6.94	summary/pts1/a-peer-tap.json	+.2f	min(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))
3585	+6.96	^	+.2f	max(pt(r, p, c, t)['median']['ppm'] for r in ('pts1', 'pts2') for p in 'abc' for c, t in ((0, 997), (1, 9973)))
3586	Five		s#0	was('records (\\w+) underruns, ([\\d.]+) to ([\\d.]+) s each', 1, at='35e332b6').capitalize()
3586	0.43		s	was('records (\\w+) underruns, ([\\d.]+) to ([\\d.]+) s each', 2, at='35e332b6')
3586	1.63		s	was('records (\\w+) underruns, ([\\d.]+) to ([\\d.]+) s each', 3, at='35e332b6')
3586	Five		s#1	rx('HANDOFF.md', r'^\| b17 \|.*?the log holds (\w+) underruns \(([\d:]+) to ([\d:]+), during offline grading\)').capitalize()
3586	06:45:27		s	rx('HANDOFF.md', r'^\| b17 \|.*?the log holds (\w+) underruns \(([\d:]+) to ([\d:]+), during offline grading\)', group=2)
3586	06:46:38		s	rx('HANDOFF.md', r'^\| b17 \|.*?the log holds (\w+) underruns \(([\d:]+) to ([\d:]+), during offline grading\)', group=3)
3587	07:32		s	was('resumed at ([\\d:]+) CEST on the same image and branch', 1, at='35e332b6')
3587	07:48:07	soc/b16c-precheck-status.log	cest	stamps(p, 'LOCK')[0]
3588	07:50:12.4		s	was('\\| `bcrf` \\| [\\d:]+ to [\\d:]+ \\| ([\\d:.]+) \\| ([\\d:.]+) \\| CLOCK_SOURCE 1, ([\\d:.]+) \\| ([\\d:]+) to ([\\d:]+), from 26 s after the set \\| [\\d:.]+ to ([\\d:.]+) \\|', 1, at='35e332b6')
3588	07:50:17.6		s	was('\\| `bcrf` \\| [\\d:]+ to [\\d:]+ \\| ([\\d:.]+) \\| ([\\d:.]+) \\| CLOCK_SOURCE 1, ([\\d:.]+) \\| ([\\d:]+) to ([\\d:]+), from 26 s after the set \\| [\\d:.]+ to ([\\d:.]+) \\|', 2, at='35e332b6')
3588	07:50:29.8		s	was('\\| `bcrf` \\| [\\d:]+ to [\\d:]+ \\| ([\\d:.]+) \\| ([\\d:.]+) \\| CLOCK_SOURCE 1, ([\\d:.]+) \\| ([\\d:]+) to ([\\d:]+), from 26 s after the set \\| [\\d:.]+ to ([\\d:.]+) \\|', 3, at='35e332b6')
3588	07:50:56		s	was('\\| `bcrf` \\| [\\d:]+ to [\\d:]+ \\| ([\\d:.]+) \\| ([\\d:.]+) \\| CLOCK_SOURCE 1, ([\\d:.]+) \\| ([\\d:]+) to ([\\d:]+), from 26 s after the set \\| [\\d:.]+ to ([\\d:.]+) \\|', 4, at='35e332b6')
3588	07:55:56		s	was('\\| `bcrf` \\| [\\d:]+ to [\\d:]+ \\| ([\\d:.]+) \\| ([\\d:.]+) \\| CLOCK_SOURCE 1, ([\\d:.]+) \\| ([\\d:]+) to ([\\d:]+), from 26 s after the set \\| [\\d:.]+ to ([\\d:.]+) \\|', 5, at='35e332b6')
3588	07:56:04.1		s	was('\\| `bcrf` \\| [\\d:]+ to [\\d:]+ \\| ([\\d:.]+) \\| ([\\d:.]+) \\| CLOCK_SOURCE 1, ([\\d:.]+) \\| ([\\d:]+) to ([\\d:]+), from 26 s after the set \\| [\\d:.]+ to ([\\d:.]+) \\|', 6, at='35e332b6')
3588	08:02:51.8		s	was('\\| `baaf` \\| [\\d:]+ to [\\d:]+ \\| [\\d:.]+ \\| [\\d:.]+ \\| CLOCK_SOURCE 2, [\\d:.]+ \\| [\\d:]+ to [\\d:]+, from 26 s after the set \\| ([\\d:.]+) to ([\\d:.]+) \\|', 1, at='35e332b6')
3588	08:02:55.8		s	was('\\| `baaf` \\| [\\d:]+ to [\\d:]+ \\| [\\d:.]+ \\| [\\d:.]+ \\| CLOCK_SOURCE 2, [\\d:.]+ \\| [\\d:]+ to [\\d:]+, from 26 s after the set \\| ([\\d:.]+) to ([\\d:.]+) \\|', 2, at='35e332b6')
3588	07:50:12.3	runs/bcrf/events.jsonl	cest1	E('bcrf', 'set-clock', tag='peer-internal')['t']
3588	07:50:17.5	^	cest1	E('bcrf', 'bind', i=-1)['t']
3588	07:50:29.7	^	cest1	E('bcrf', 'set-clock', tag='bcrf')['t']
3588	07:50:55	^	cest	E('bcrf', 'captures-started')['started']['mcasp'] + r2lead()
3588	07:55:55	^	cest	E('bcrf', 'captures-started')['started']['mcasp'] + r2lead() + grade('bcrf')['seconds']
3588	07:56:04.0	^	cest1	E('bcrf', 'mark', tag='after-restore')['t']
3588	08:02:51.7	runs/baaf/events.jsonl	cest1	E('baaf', 'teardown')['t']
3588	08:02:55.7	^	cest1	E('baaf', 'mark', tag='after-restore')['t']
3589	303.8		s#0	was('over ([\\d.]+) s in each case\\. One frame', 1, at='35e332b6')
3589	303.8	summary/bcrf/d-loop-decode.json	.1f#1	d['decoded'] / 48000
3589	303.9	summary/baaf/d-loop-decode.json	.1f	d['decoded'] / 48000
3590	+10.6		s	was("through the DUT's meters, (\\+[\\d.]+) ppm against gPTP", 1, at='35e332b6')
3590	+10.59	r2/bcrf-poll-receipt.json	+.2f	min(rates())
3590	+10.65	^	+.2f	max(rates())
3592	Six		W	sum(1 for x in ('plus one change', 'one PDU', 'one step earlier', 'one request', 'the two lanes', 'one route') if x in load('git:35e332b6:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md') and x not in re.sub(r'"[^"]*"', '', ' '.join(t for t, _ in scope().values())))
# the page's Contents entry for lane B16
84	three	summary/bcrf/c-b9-grade.json	w	same([terms('bcrf'), terms('baaf')])
84	four	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	w#1	len(re.split(r', and |, ', b6_rule()))
# the README row's lane B16 part
README.md:15	twice	summary/loop2/acmp-peer-tap.json	x	sum(x['msg'] == 'CONNECT_TX_COMMAND' for x in d['acmp'])
README.md:15	-14.1	summary/pts1/a-peer-tap.json	.1f	same(q(T(load(f'summary/{r}/a-peer-tap.json'), 0, 'level_dbfs'), 1) for r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3'))
README.md:15	four	summary/pts1/align-a-c.json	w	sum(1 for r in RUNS if (ROOT / f'summary/{r}/align-a-c.json').exists() and r in ('pts1', 'pts2', 'b0', 'b0-2', 'pts3') and align(r, 'a')['frames_differing'] == 0)
README.md:15	300	summary/b0-2/c-b9-grade.json	.0f#0	d['seconds']
README.md:15	-123.95	^	.2f	d['summary']['ch0_all']['thdn_db_median']
README.md:15	-122.80	^	.2f	d['summary']['ch1_all']['thdn_db_median']
README.md:15	131	r2/b0-2-receipt.json	d	d['degraded']
README.md:15	300	^	d#1	d['blocks']
README.md:15	34.1	^	.1f	d['overlap']['seconds']
README.md:15	23	^	d	d['overlap']['degraded_inside']
README.md:15	108	^	d	d['overlap']['degraded_beyond']
README.md:15	300	summary/bcrf/c-b9-grade.json	.0f	same(grade(r)['seconds'] for r in ('bcrf', 'baaf'))
README.md:15	2.585	r2/bcrf-poll-trace.tsv	.3f	lock_bracket('bcrf')[0]
README.md:15	3.161	r2/bcrf-poll-receipt.json	.3f	lock_bracket('bcrf')[1]
README.md:15	6.602	r2/baaf-poll-trace.tsv	.3f	lock_bracket('baaf')[0]
README.md:15	7.180	r2/baaf-poll-receipt.json	.3f	lock_bracket('baaf')[1]
README.md:15	-123.98	summary/bcrf/c-b9-grade.json	.2f	same(grade(r)['summary']['ch0_all']['thdn_db_median'] for r in ('bcrf', 'baaf'))
README.md:15	-123.97	^	.2f	same(grade(r)['summary']['ch1_all']['thdn_db_median'] for r in ('bcrf', 'baaf'))
README.md:15	300	^	d	same(n for r in ('bcrf', 'baaf') for n in (grade(r)['summary']['blocks'], grade(r)['summary']['blocks_at_floor']))
README.md:15	0	summary/bcrf/d-loop-decode.json	d	same(dec(r)['net_step_frames'] for r in ('bcrf', 'baaf'))
README.md:15	four	repo:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md	w	len(re.split(r', and |, ', b6_rule()))
README.md:15	three	summary/bcrf/c-b9-grade.json	w	same([terms('bcrf'), terms('baaf')])
3617	5	controls/r3-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3617	5	^	d#1	len(d['controls'])
# round 4: link labels
22	2026-10-12		date	stamps('identity/lock-window.txt', 'LOCK')[0]
84	2026-10-12		date	stamps('identity/lock-window.txt', 'LOCK')[0]
84	four	summary/bcrf/c-b9-grade.json	w#0	same(points(r) for r in ('bcrf', 'baaf'))
# round 4: the four capture points
2638	four	summary/pts1/c-mcasp.json	w#0	same(points(r) for r in ('pts1', 'pts2', 'b0-2', 'pts3'))
2647	four	^	w#0	same(points(r) for r in ('pts1', 'pts2', 'b0-2', 'pts3'))
2712	four	^	w#0	same(points(r) for r in ('pts1', 'pts2', 'b0-2', 'pts3'))
3010	four	summary/bcrf/c-mcasp.json	w#0	same(points(r) for r in ('bcrf', 'baaf'))
# round 4: block length, bit width, floor, frame step, limit
2652	one	summary/b0-2/c-b9-grade.json	w#0	blk_grade(('b0-2',))
3008	one	summary/bcrf/c-b9-grade.json	w#0	blk_grade(('bcrf',))
2691	one	summary/pts1/c-mcasp.json	w#0	blk_points(('pts1', 'pts2', 'b0-2', 'pts3'))
2716	one	^	w#0	blk_points(('pts1', 'pts2', 'b0-2', 'pts3'))
3110	one	summary/bcrf/c-mcasp.json	w#0	blk_points(('bcrf', 'baaf'))
2692	24	summary/pts1/align-a-c.json	d#0	cmp_bits(('pts1', 'pts2', 'b0-2', 'pts3'))
2755	24	^	d#0	cmp_bits(('pts1', 'pts2', 'b0-2', 'pts3'))
3145	24	summary/bcrf/align-a-c.json	d#0	cmp_bits(('bcrf', 'baaf'))
3077	24	^	d#0	cmp_bits(('bcrf', 'baaf'))
2512	one		w#0	rx('tools/tone_points_b16.py', r'the tone pair at -60 dBFS on the \+-(\d+) LSB floor')
3201	one	controls/b16b-dloop-control.json	w#0	step_frames()
2699	10	HANDOFF.md	d	lock_limit()
# round 4: quoted number words, each found before its rewording
3592	one		s#0	was('plus (one) change', 1, at='35e332b6')
3592	one		s#1	was('\\b(one) PDU', 1, at='35e332b6')
3593	one		s#0	was('\\b(one) step earlier', 1, at='35e332b6')
3593	one		s#1	was('\\b(one) request', 1, at='35e332b6')
3593	two		s#0	was('the (two) lanes', 1, at='35e332b6')
3593	one		s#2	re.search('\\b(one) route', load('git:35e332b6:docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md')).group(1)
3569	two		s#0	was('the receipts do not separate the (two)\\.', 1, at='0782c55f')
3686	one		s#0	was('records each (one)\\.', 1, at='0782c55f')
3687	one		s#0	was('the published (one) in both', 1, at='0782c55f')
3687	once		s#0	was('failed at (once) with', 1, at='0782c55f')
3687	once		s#1	was('\\b(once) the controller agent', 1, at='0782c55f')
3688	two		s#0	was('for these (two) cases', 1, at='0782c55f')
3688	two		s#1	was('the (two) cases run in the loop', 1, at='0782c55f')
3688	one		s#0	was('run on (one) clock', 1, at='0782c55f')
3688	one		s#1	was('graded (one) state of it', 1, at='0782c55f')
3689	two		s#0	was('with (two) modes added', 1, at='0782c55f')
3689	two		s#1	was("the (two) clocks' difference", 1, at='0782c55f')
3689	two		s#2	was('do not separate the (two)\\.', 1, at='0782c55f')
3690	Two		s#0	was('(Two) reviews of this section', 1, at='0782c55f')
3690	Two		s#1	was('(Two) reviews of round 2', 1, at='0782c55f')
3691	one		s#0	was('holds (one) row per quoted figure', 1, at='0782c55f')
3691	one		s#1	was('(one) line per row', 1, at='0782c55f')
3691	one		s#2	was('each about a minute, on (one) reference peer', 1, at='0782c55f')
3692	one		s#0	was('runs on (one) DUT and one reference peer', 1, at='0782c55f')
3692	one		s#1	was('runs on one DUT and (one) reference peer', 1, at='0782c55f')
3685	Seventeen		W	sum(1 for x in ('records each one', 'the published one', 'failed at once', 'once the controller agent', 'these two cases', 'the two cases run', 'on one clock', 'one state of it', 'two modes added', "the two clocks' difference", 'do not separate the two.', 'Two reviews of this section', 'Two reviews of round 2', 'one row per quoted figure', 'one line per row', 'on one reference peer', 'on one DUT and one reference peer') if x in was('(.*)', 1, at='0782c55f') and x not in re.sub(r'"[^"]*"', '', ' '.join(t for t, _ in scope().values())))
# round 4: where the packet is
2609	b84584e4ccb069248909f0fdeb7f8b72a1c41ae4	r4/evidence-receipt.json	s	d['evidence_commit']
2613	e20fd282	^	s	d['archives']['author-r1']['page_commit']
2613	35e332b6	^	s	d['archives']['author-r2']['page_commit']
2614	0782c55f	^	s	d['archives']['author-r3']['page_commit']
2618	b84584e4	^	s	d['evidence_commit'][:8]
2618	1,680	^	,d	d['manifest_entries']
2619	8d417d54b13a264484bfcb0b69f8a643e5cd3bf2819294cea201242a2f67f034	^	s	d['manifest_sha256']
2623	27	^	d	d['path_redacted_author'] if d['hashes_differ_exactly_when_redacted'] else None
2623	1	^	d	d['path_redacted_per_dir']['author-r1']
2623	9	^	d	d['path_redacted_per_dir']['author-r2']
2623	17	^	d	d['path_redacted_per_dir']['author-r3']
2625	66	^	d	d['page_rows']['rows'] if d['page_rows']['rows'] == d['page_rows']['in_manifest'] == d['page_rows']['all_equal'] and d['page_rows']['path_redacted'] == 0 else None
2626	0782c55f	^	s	d['page_commit'][:8]
# B16, round 4: packet and coverage
3634	45		s	was(r'census (\d+) of (\d+) entries equal', 1, at='0782c55f')
3634	46		s	was(r'census (\d+) of (\d+) entries equal', 2, at='0782c55f')
3634	44		d	same([census_reads('restore/census-start.jsonl', 'restore/census-end.jsonl', 'restore/census-compare.txt')[0], census_reads('restore/census-end.jsonl', 'restore/census-startb.jsonl', 'restore/census-compare-b16-to-b16b.txt')[0], census_reads('restore/census-startb.jsonl', 'restore/census-endb.jsonl', 'restore/census-compare-b16b.txt')[0], census_reads('restore/census-endb.jsonl', 'restore/census-startc.jsonl', 'restore/census-compare-b16b-to-b16c.txt')[0], census_reads('restore/census-startc.jsonl', 'restore/census-endc.jsonl', 'restore/census-compare-b16c.txt')[0]])
3634	45		d#1	same([census_reads('restore/census-start.jsonl', 'restore/census-end.jsonl', 'restore/census-compare.txt')[1], census_reads('restore/census-end.jsonl', 'restore/census-startb.jsonl', 'restore/census-compare-b16-to-b16b.txt')[1], census_reads('restore/census-startb.jsonl', 'restore/census-endb.jsonl', 'restore/census-compare-b16b.txt')[1], census_reads('restore/census-endb.jsonl', 'restore/census-startc.jsonl', 'restore/census-compare-b16b-to-b16c.txt')[1], census_reads('restore/census-startc.jsonl', 'restore/census-endc.jsonl', 'restore/census-compare-b16c.txt')[1]])
3666	8	controls/r4-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3666	8	^	d#1	len(d['controls'])
3666	five	^	w#0	sum(1 for c in d['controls'] if c.get('from') == 'round 3')
3677	5	controls/r4-rerun-r3-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3677	5	^	d#1	len(d['controls'])
3705	8	controls/r4-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3705	8	^	d#1	len(d['controls'])
3706	5	controls/r4-rerun-r3-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3706	5	^	d#1	len(d['controls'])
# B16, round 5: every digit
3778	22	controls/r5-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3778	22	^	d#1	len(d['controls'])
3798	5	controls/r5-rerun-r3-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3798	5	^	d#1	len(d['controls'])
3798	8	controls/r5-rerun-r4-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3798	8	^	d#1	len(d['controls'])
3830	22	controls/r5-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3830	22	^	d#1	len(d['controls'])
3831	5	controls/r5-rerun-r3-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3831	5	^	d#1	len(d['controls'])
3832	8	controls/r5-rerun-r4-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3832	8	^	d#1	len(d['controls'])
# round 6: where the packet is
2616	61ae8641	r6/evidence-receipt.json	s	d['archives']['author-r4']['page_commit']
2616	b83e5d76	^	s	d['archives']['author-r4']['commit'][:8]
2616	36190193	^	s	d['archives']['author-r5']['page_commit']
2616	a73ce5c4	^	s	same([d['archives']['author-r5']['commit'][:8], d['evidence_commit'][:8]])
# B16, round 6: the closed list
3929	39	controls/r6-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3929	39	^	d#1	len(d['controls'])
3929	22	^	d#0	sum(1 for c in d['controls'] if c.get('from') in ('round 3', 'round 4', 'round 5'))
3945	5	controls/r6-rerun-r3-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3945	5	^	d#1	len(d['controls'])
3945	8	controls/r6-rerun-r4-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3945	8	^	d#1	len(d['controls'])
3945	22	controls/r6-rerun-r5-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3945	22	^	d#1	len(d['controls'])
3984	39	controls/r6-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3984	39	^	d#1	len(d['controls'])
3985	5	controls/r6-rerun-r3-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3985	5	^	d#1	len(d['controls'])
3986	8	controls/r6-rerun-r4-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3986	8	^	d#1	len(d['controls'])
3987	22	controls/r6-rerun-r5-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
3987	22	^	d#1	len(d['controls'])
# round 7: where the packet is
2616	e91a62ee	r7/evidence-receipt.json	s	d['archives']['author-r6']['page_commit']
2616	b616e7ea	^	s	same([d['archives']['author-r6']['commit'][:8], d['evidence_commit'][:8]])
# B16, round 7: no markup
4050	50	controls/r7-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
4050	50	^	d#1	len(d['controls'])
4050	39	^	d#0	sum(1 for c in d['controls'] if c.get('from') != 'round 7')
4068	5	controls/r7-rerun-r3-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
4068	5	^	d#1	len(d['controls'])
4068	8	controls/r7-rerun-r4-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
4068	8	^	d#1	len(d['controls'])
4069	22	controls/r7-rerun-r5-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
4069	22	^	d#1	len(d['controls'])
4069	39	controls/r7-rerun-r6-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
4069	39	^	d#1	len(d['controls'])
4091	111	r7/self-probes.json	d	len(d['probes']) if d['met'] == len(d['probes']) else None
4091	92	^	d	d['detected']
4092	19	^	d	sum(1 for x in d['probes'] if x['expect'] == 'pass' and x['met'])
4108	50	controls/r7-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
4108	50	^	d#1	len(d['controls'])
4109	5	controls/r7-rerun-r3-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
4109	5	^	d#1	len(d['controls'])
4110	8	controls/r7-rerun-r4-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
4110	8	^	d#1	len(d['controls'])
4111	22	controls/r7-rerun-r5-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
4111	22	^	d#1	len(d['controls'])
4112	39	controls/r7-rerun-r6-controls.json	d#0	sum(c['verdict'] == 'PASS' for c in d['controls'])
4112	39	^	d#1	len(d['controls'])
# round 8: where the packet is
2616	295ba9d7	r8/evidence-receipt.json	s	d['archives']['author-r7']['page_commit']
2616	fa974c3f	^	s	same([d['archives']['author-r7']['commit'][:8], d['evidence_commit'][:8]])
# B16, round 8: the parser
4208	73	controls/r8-controls.json	d#0	passed(d)
4208	73	^	d#1	len(d['controls'])
4208	50	^	d#0	sum(1 for c in d['controls'] if c.get('from') != 'round 8')
4226	48	controls/r8-controls-on-r7-check.json	d	passed(d)
4227	25	^	d	sum(c['verdict'] == 'FAIL' for c in d['controls'])
4230	5	controls/r8-rerun-r3-controls.json	d	passed(d)
4231	5	^	d	len(d['controls'])
4231	7	controls/r8-rerun-r4-controls.json	d	passed(d)
4231	8	^	d	len(d['controls'])
4231	21	controls/r8-rerun-r5-controls.json	d	passed(d)
4231	22	^	d	len(d['controls'])
4231	38	controls/r8-rerun-r6-controls.json	d	passed(d)
4231	39	^	d	len(d['controls'])
4231	48	controls/r8-rerun-r7-controls.json	d	passed(d)
4231	50	^	d	len(d['controls'])
4249	138	r8/self-probes.json	d	len(d['probes']) if d['met'] == len(d['probes']) else None
4250	108	^	d	d['detected']
4250	30	^	d	sum(1 for x in d['probes'] if x['expect'] == 'pass' and x['met'])
4251	Five	^	W	sum(1 for x in d['probes'] if x['probe'] in d['ruled'] and x['met'])
4269	73	controls/r8-controls.json	d#0	passed(d)
4269	73	^	d#1	len(d['controls'])
# hash tables: one row per byte count and SHA-256
2582	1,567,518	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-peer.pcap')['bytes'] for r in ['loop1'])
2582	0f4c6b42f6792dc84d8ba89d93e9edb97add667bf236b2d06833256ba14f1b0b	^	s	same(raw(r + '/tap-peer.pcap')['sha256'] for r in ['loop1'])
2583	1,567,518	^	,d	same(raw(r + '/tap-dut.pcap')['bytes'] for r in ['loop1'])
2583	a879b24feec3f4cdd4d72522d152afce4a1f6b527ce6a8210213c9779a6d9036	^	s	same(raw(r + '/tap-dut.pcap')['sha256'] for r in ['loop1'])
2584	afff760831cd795283185c800d86460a1216511be9ebeb90a00baebc2ce8d0e2	^	s	same(raw(r + '/extcap.raw')['sha256'] for r in ['loop1'])
2585	8,752,338	^	,d	same(raw(r + '/tap-peer.pcap')['bytes'] for r in ['loop2'])
2585	6e0e1f4271d31495bd4d4c33ca4f5a55d791c9c3c8540a53b584abc505696776	^	s	same(raw(r + '/tap-peer.pcap')['sha256'] for r in ['loop2'])
2586	8,680,530	^	,d	same(raw(r + '/tap-dut.pcap')['bytes'] for r in ['loop2'])
2586	898242c513f4f30be70d0b3386f983e536f4bc4e5d63eaf341149b47aa6ac276	^	s	same(raw(r + '/tap-dut.pcap')['sha256'] for r in ['loop2'])
2587	265d9585facf0aa1d6766454a5a0c1a871ae1449e0850e7de7f684b32b03067c	^	s	same(raw(r + '/extcap.raw')['sha256'] for r in ['loop2'])
2594	18,087	tools/b16-asrun/run_b16.py	,d	size(p)
2594	d1a60cc2be9af3d8a3f81424ce468441ceeae88c960d817c127de5816f27a289	^	s	sha(p)
2595	19,842	tools/tone_points_b16.py	,d	size(p)
2595	975645309ecb92d124b28d488c74902a2aea9379470e3eec563f1d93ea20869c	^	s	sha(p)
2596	7,802	tools/align_b16.py	,d	size(p)
2596	71fd639b5db4c00f4048c6f2930330ee6880388613459a0d7411d577ab3eac86	^	s	sha(p)
2597	2,949	tools/acmp_tap_b16.py	,d	size(p)
2597	8c686a58e5c0288623c50cd7a40b273a6d0336b66af9765f0214a4dffaf57f65	^	s	sha(p)
2598	1,565	controls/b16-tap-controls.json	,d	size(p)
2598	77a5995f07b9e300b5d819477e70441ed7ba3a26848e881ec6841219867da8fe	^	s	sha(p)
2599	1,176	controls/b16-align-controls-synth.json	,d	size(p)
2599	20ca766eb693b2f2252f6de97efda18c94455ade5d661813a8e26fd604b1d276	^	s	sha(p)
2600	11,587	runs/loop1/events.jsonl	,d	size(p)
2600	0390182f646584223bceeaf240e47135be383e47ddd56b4d15950336a441f954	^	s	sha(p)
2601	11,656	runs/loop2/events.jsonl	,d	size(p)
2601	cb3a5ffada5c35cdbbbbacc866e3f15abeded2e706754e9b3958479f75a0e2c0	^	s	sha(p)
2602	8,739	summary/loop2/acmp-peer-tap.json	,d	size(p)
2602	ecd9b4589b9508322c587938417550fa7dcb3a6eaee2065261e3ad73dabf6688	^	s	sha(p)
2603	664	summary/loop1/d-extcap-pair.json	,d	size(p)
2603	496e6ad34ad164d1b8fea06c92d8ed099e3e831386c58d4b192d7881dfc64704	^	s	sha(p)
2604	661	summary/loop2/d-extcap-pair.json	,d	size(p)
2604	17f6c33f990654a1dd6dae8e5277ecd874955337cac66f0cfeb94eac33f549a5	^	s	sha(p)
2605	369	restore/census-compare.txt	,d	size(p)
2605	3a9a17cfc7ab6849571b9b2221c4981e8a19b7f460f1f66c30f9293a43f2de6f	^	s	sha(p)
2606	1,532	identity/identity-verdict.txt	,d	size(p)
2606	4634ee944266589d6be3a9a1f90c93cd58c003b4d9fc60a341d43e46d7ff2130	^	s	sha(p)
2945	90,602,048	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-peer.pcap')['bytes'] for r in ['pts1'])
2945	b235c4321fc2324cab2412692bd5d1b0642b73ea13549c028c1722ba9dfbc68a	^	s	same(raw(r + '/tap-peer.pcap')['sha256'] for r in ['pts1'])
2946	90,981,020	^	,d	same(raw(r + '/tap-dut.pcap')['bytes'] for r in ['pts1'])
2946	e0b086473164bf58ba304eb7b2d9e435eb412fcf11da8d246524abd18f4bb083	^	s	same(raw(r + '/tap-dut.pcap')['sha256'] for r in ['pts1'])
2947	15,360,000	^	,d	same(raw(r + '/mcasp-all.raw')['bytes'] for r in ['pts1'])
2947	ff408b45488948294ed1c7bc5ce2ca13725fd0c7613e311d16fbf880f3992dd5	^	s	same(raw(r + '/mcasp-all.raw')['sha256'] for r in ['pts1'])
2948	02345629d6828ebe193391209b4bda618ff95f1d83b24e164996d8fcefbf75d4	^	s	same(raw(r + '/extcap.raw')['sha256'] for r in ['pts1'])
2949	90,981,358	^	,d	same(raw(r + '/tap-peer.pcap')['bytes'] for r in ['pts2'])
2949	f06bfd1ed8f486f765bce404607e88b0fda7c3e33da6d936cfa9840bfebf8b1b	^	s	same(raw(r + '/tap-peer.pcap')['sha256'] for r in ['pts2'])
2950	90,980,890	^	,d	same(raw(r + '/tap-dut.pcap')['bytes'] for r in ['pts2'])
2950	9c6059d0b7ad9a23fe8176733d087d01b13613d96c0012244f1982a2acbaf75e	^	s	same(raw(r + '/tap-dut.pcap')['sha256'] for r in ['pts2'])
2951	15,360,000	^	,d	same(raw(r + '/mcasp-all.raw')['bytes'] for r in ['pts2'])
2951	f3447f30211ed37e548e9746bf2c9c9e4795797d1e551dc3afae2204f7f0eb6c	^	s	same(raw(r + '/mcasp-all.raw')['sha256'] for r in ['pts2'])
2952	08bf83e0eb4a50540517142c82ad0f386852384ae66f89fad1dd3824b9fd31e5	^	s	same(raw(r + '/extcap.raw')['sha256'] for r in ['pts2'])
2953	1,536,000	^	,d	same(raw(r + '/b6-loop.raw')['bytes'] for r in ['pts2', 'b0', 'b0-2'])
2953	566d3dfae6eb60a658b8cb0ddf5c833900ccbe4feb41c427a970a5854cc75588	^	s	same(raw(r + '/b6-loop.raw')['sha256'] for r in ['pts2', 'b0', 'b0-2'])
2954	153,665,476	^	,d	same(raw(r + '/tap-peer.pcap')['bytes'] for r in ['b0'])
2954	075ff41dfbe12b06673eac87f2b04b78519fbb914fd987e7d6b7af4d3ae42e23	^	s	same(raw(r + '/tap-peer.pcap')['sha256'] for r in ['b0'])
2955	154,049,176	^	,d	same(raw(r + '/tap-dut.pcap')['bytes'] for r in ['b0'])
2955	ce0f42c6753d8acd2c214d98c9162ffcd12b566ecfab8ba6f2b38bedb67a6737	^	s	same(raw(r + '/tap-dut.pcap')['sha256'] for r in ['b0'])
2956	0	^	,d	same(raw(r + '/mcasp-all.raw')['bytes'] for r in ['b0'])
2956	e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855	^	s	same(raw(r + '/mcasp-all.raw')['sha256'] for r in ['b0'])
2957	b0517ab7e64865159ba8aa319fd9084886812d8ddbf1dedbc95889740c9c41c1	^	s	same(raw(r + '/extcap.raw')['sha256'] for r in ['b0'])
2958	154,050,970	^	,d	same(raw(r + '/tap-peer.pcap')['bytes'] for r in ['b0-2'])
2958	c0efda0683566f3b1a5299fe1ffa97f970585ce51d6ca218c7d9d825c08bbf23	^	s	same(raw(r + '/tap-peer.pcap')['sha256'] for r in ['b0-2'])
2959	154,049,284	^	,d	same(raw(r + '/tap-dut.pcap')['bytes'] for r in ['b0-2'])
2959	59bcfef4cfe31f3326360aa3b861e5a5dc7f26f45f00f94afcbc65dce286209d	^	s	same(raw(r + '/tap-dut.pcap')['sha256'] for r in ['b0-2'])
2960	460,800,000	^	,d	same(raw(r + '/mcasp-all.raw')['bytes'] for r in ['b0-2'])
2960	9b7072a2ff202841d81ffb4846697a9ebb9240ed72b66610292b4071f83486c1	^	s	same(raw(r + '/mcasp-all.raw')['sha256'] for r in ['b0-2'])
2961	52da5d1febaebd5b03617b24f40c52ed381f57a3490ef20c4a2f6ad7a931dc7b	^	s	same(raw(r + '/extcap.raw')['sha256'] for r in ['b0-2'])
2962	90,981,956	^	,d	same(raw(r + '/tap-peer.pcap')['bytes'] for r in ['pts3'])
2962	6cdf04d06b9d92d11a9fd748e0a8d94b394f2a5337f8ce7a1da52d7f962c46c0	^	s	same(raw(r + '/tap-peer.pcap')['sha256'] for r in ['pts3'])
2963	90,980,912	^	,d	same(raw(r + '/tap-dut.pcap')['bytes'] for r in ['pts3'])
2963	f759569cdeab83ae2491346826a33cb1c8c015289ea80963400794ed52f5aed0	^	s	same(raw(r + '/tap-dut.pcap')['sha256'] for r in ['pts3'])
2964	15,360,000	^	,d	same(raw(r + '/mcasp-all.raw')['bytes'] for r in ['pts3'])
2964	c99d7fc661f7886da65aa8e7728527699b2ee78d30102baa851ea24163ae2558	^	s	same(raw(r + '/mcasp-all.raw')['sha256'] for r in ['pts3'])
2965	5260ce29b7d118595fa61d98435f3bab28a469448000856daa328b01c5565f2a	^	s	same(raw(r + '/extcap.raw')['sha256'] for r in ['pts3'])
2972	25,161	tools/run_b16.py	,d	size(p)
2972	424234725a2035ab9ce30512e2da1275495758283f1f483c86d982e008a43be2	^	s	sha(p)
2973	1,812	tools/run_locked_b16.sh	,d	size(p)
2973	8694f9b0e3c38814ab55896108abbde59f04e302b9de82f690c12f41646f90fa	^	s	sha(p)
2974	4,122	tools/dloop_b16.py	,d	size(p)
2974	d3bf1a0e81b2b01bd1c12713b5ab7dbca0903c596d3fb33b6ac194e725af1ecf	^	s	sha(p)
2975	705	controls/b16b-dloop-control.json	,d	size(p)
2975	fbce8878a37a47b76d67fed3e450eecf57b6b3083c7ec0edc12e789e5bd775fb	^	s	sha(p)
2976	8,437	runs/pts1/events.jsonl	,d	size(p)
2976	bcd8663a9cd40acd7c4cf7c933950751527d9088432d153a9306f40ae12031fd	^	s	sha(p)
2977	9,876	runs/pts2/events.jsonl	,d	size(p)
2977	d6a68179a3dc2aed3e36a15d2e080922068e476c9163657d4aeacfbe394ac45b	^	s	sha(p)
2978	11,877	runs/b0/events.jsonl	,d	size(p)
2978	6b9bb18043df40efeb2d93808cbca099d0988b25bfa04a91aefaaf9c3994053a	^	s	sha(p)
2979	11,883	runs/b0-2/events.jsonl	,d	size(p)
2979	d5e6d8dd6cc5b349a0aa37adad9394206fded1f221905b0e41f7d82f96dc82ab	^	s	sha(p)
2980	8,435	runs/pts3/events.jsonl	,d	size(p)
2980	a53e635e28ca361874eb2b9c5d842d45479ca69722f74ce10e27c31cd8997c40	^	s	sha(p)
2981	422	summary/pts1/align-a-c.json	,d	size(p)
2981	11bc737c7af2d4ef1cf77d234dfe275049102e65a801e5cf1ff0e8eb6548fcb3	^	s	sha(p)
2982	422	summary/pts2/align-a-c.json	,d	size(p)
2982	9cf3e2f3923e649dc20a34f9f711c4f62f0a772b41a7e7a51f28f0baaa7a8202	^	s	sha(p)
2983	422	summary/pts3/align-a-c.json	,d	size(p)
2983	dab152d9ae393ed2f20476b8e79b45d969bc3240c06a2235a49c58f2bc7f41cd	^	s	sha(p)
2984	426	summary/b0-2/align-a-c.json	,d	size(p)
2984	a24903924f8a43d07721c366966d7ee9a84a0b70f708612de079438bfb3e0da4	^	s	sha(p)
2985	426	summary/b0-2/align-b-c.json	,d	size(p)
2985	141619ca294c004ca02231eab1122a4a93ce6ddd732635c7d2e95bfbaf29bcd2	^	s	sha(p)
2986	135,813	summary/b0-2/c-b9-grade.json	,d	size(p)
2986	1d554ce3a70dfb4a5ef935d139980ff0bee6cf8eb505ec42fca2781a7ed54078	^	s	sha(p)
2987	563	summary/pts2/d-loop-decode.json	,d	size(p)
2987	49ce9f4c6487fcc15f41d68e5a25f36a0b83b7f994cee838e0c8204b455a21da	^	s	sha(p)
2988	316	summary/b0-2/d-loop-decode.json	,d	size(p)
2988	a58b5ebbe5a15cd3a3d216b18192b4157a5b762baa7b010be901428d9e56fd1b	^	s	sha(p)
2989	481	restore/census-compare-b16b.txt	,d	size(p)
2989	d14071dedb18e5cafc24421ede3cd450289d77e1af6f13f8a48c9d3c26f66648	^	s	sha(p)
2990	1,532	identity-b16b/identity-verdict.txt	,d	size(p)
2990	4634ee944266589d6be3a9a1f90c93cd58c003b4d9fc60a341d43e46d7ff2130	^	s	sha(p)
3359	154,049,992	RAW-ARTIFACTS.json	,d	same(raw(r + '/tap-peer.pcap')['bytes'] for r in ['bcrf'])
3359	edad46fe5de09dcace08a19eef8f5ecc5f0e9cab9bf5e506eb3e2f23a6bc97b3	^	s	same(raw(r + '/tap-peer.pcap')['sha256'] for r in ['bcrf'])
3360	154,048,228	^	,d	same(raw(r + '/tap-dut.pcap')['bytes'] for r in ['bcrf'])
3360	4e7013347ec9de4e29c61165f92acee4e22104bbf5e7aa1050225d38ba593d09	^	s	same(raw(r + '/tap-dut.pcap')['sha256'] for r in ['bcrf'])
3361	460,800,000	^	,d	same(raw(r + '/mcasp-all.raw')['bytes'] for r in ['bcrf'])
3361	b5e30bb576949c077f3ff611c6226d5bf094e7b65ff2e1f033541c3f9ba1c03f	^	s	same(raw(r + '/mcasp-all.raw')['sha256'] for r in ['bcrf'])
3362	b4f6a999500c5b1b0e1c058afeaf9788410f1b2f29e4a4e684ba19b1c2f50e4d	^	s	same(raw(r + '/extcap.raw')['sha256'] for r in ['bcrf'])
3363	218,420	^	,d	same(raw(r + '/poll-run.jsonl')['bytes'] for r in ['bcrf'])
3363	9cfc79bb2ae8ad6c6e8cca028d66af3b6695c0982ffe2a512ea756fb3dc06c03	^	s	same(raw(r + '/poll-run.jsonl')['sha256'] for r in ['bcrf'])
3364	199,498	^	,d	same(raw(r + '/tone-status.jsonl')['bytes'] for r in ['bcrf'])
3364	2a7974d5a6f6548e847844c326e52e59d6cc4b1f6dcfd0a730c673f85865a10c	^	s	same(raw(r + '/tone-status.jsonl')['sha256'] for r in ['bcrf'])
3365	154,049,168	^	,d	same(raw(r + '/tap-peer.pcap')['bytes'] for r in ['baaf'])
3365	234a2f0b414dcd0a07e9f2fb9047d417b9d14da77fddc0a0b708e315983ab36d	^	s	same(raw(r + '/tap-peer.pcap')['sha256'] for r in ['baaf'])
3366	154,048,154	^	,d	same(raw(r + '/tap-dut.pcap')['bytes'] for r in ['baaf'])
3366	5a8dbaad272ad1c6bbd18aa146486ed2a78c27d23270a8e9d243207b9269038b	^	s	same(raw(r + '/tap-dut.pcap')['sha256'] for r in ['baaf'])
3367	460,800,000	^	,d	same(raw(r + '/mcasp-all.raw')['bytes'] for r in ['baaf'])
3367	1351272cb679353885983762402caa13ef6e793831463dfc5a2ca242cca3a93e	^	s	same(raw(r + '/mcasp-all.raw')['sha256'] for r in ['baaf'])
3368	1eeaad6845cb2ad30de88ffe5eb211518f12acf14fa6fed9bd14a12cdd9c099c	^	s	same(raw(r + '/extcap.raw')['sha256'] for r in ['baaf'])
3369	218,401	^	,d	same(raw(r + '/poll-run.jsonl')['bytes'] for r in ['baaf'])
3369	476a007728d267931a7baf32095afd8342fde5e8c30984f469b857c3841bab73	^	s	same(raw(r + '/poll-run.jsonl')['sha256'] for r in ['baaf'])
3370	200,133	^	,d	same(raw(r + '/tone-status.jsonl')['bytes'] for r in ['baaf'])
3370	40962288e0fe5eca37964b068c2060c005bc39ccbbe470486c41003653ce3a99	^	s	same(raw(r + '/tone-status.jsonl')['sha256'] for r in ['baaf'])
3371	1,536,000	^	,d	same(raw(r + '/b6-loop.raw')['bytes'] for r in ['bcrf', 'baaf'])
3371	566d3dfae6eb60a658b8cb0ddf5c833900ccbe4feb41c427a970a5854cc75588	^	s	same(raw(r + '/b6-loop.raw')['sha256'] for r in ['bcrf', 'baaf'])
3379	41,693	tools/run_b16c.py	,d	size(p)
3379	8ed6b63f03598f595c6b2aedcfedcdd81f37d3d130cdc2368ba5010962948a3c	^	s	sha(p)
3380	2,564	tools/run_locked_b16c.sh	,d	size(p)
3380	6eed98dbba4f6fde2752e185c5406005ad5e0915910c8ca43026231b8aa0cd6f	^	s	sha(p)
3381	6,593	tools/tables_b16c.py	,d	size(p)
3381	95b33b4530062c48e17b0db09019ff18b0fa166938006693947ee3b31408d918	^	s	sha(p)
3382	1,903	tools/dryrun_b16c/dryrun_b16c.sh	,d	size(p)
3382	699955707f9847b5db9076782d0f4472978c27ea4d85cb45fcedcc8e95b60be7	^	s	sha(p)
3383	4,074	tools/dryrun_b16c/check_dryrun_b16c.py	,d	size(p)
3383	fdfffe23a65b2e07fd28270128e5832d8f0ce6eb801178bd0de671b216c4a204	^	s	sha(p)
3384	273	controls/b16c-dryrun-summary.json	,d	size(p)
3384	685737875fc4df85c27e5e37ac680f373cdc0e02e930da8189da8834a891e336	^	s	sha(p)
3385	617	controls/b16c-wrapper-deadline.txt	,d	size(p)
3385	090969eb04c94470e4589d465f960e72d938745fa1c61203570f0ef9fc439677	^	s	sha(p)
3386	20,973	runs/bcrf/events.jsonl	,d	size(p)
3386	9e6b07074af7d371cbca8df974a85e9a6d3f6bd73526bd6350c42344a7c88e55	^	s	sha(p)
3387	20,973	runs/baaf/events.jsonl	,d	size(p)
3387	2011eca5bb7b5802451342da06268acc88af4b2ac0c161c06edd9d7f7b24ab2f	^	s	sha(p)
3388	135,192	summary/bcrf/c-b9-grade.json	,d	size(p)
3388	a74f236bb68e333f5dbc8f1a47176badf318048573728e9cec603cc8de5a7e6b	^	s	sha(p)
3389	135,271	summary/baaf/c-b9-grade.json	,d	size(p)
3389	2b0ee83ea4d80978bc7239cba706e6c14881f77b4a503c89759021c0203efd84	^	s	sha(p)
3390	426	summary/bcrf/align-a-c.json	,d	size(p)
3390	80df5a0b1751a209f2b8055409e5399d3648618bd80ca036c913d9045e3721ec	^	s	sha(p)
3391	426	summary/bcrf/align-b-c.json	,d	size(p)
3391	e22934e3702eb234534b11342b3710bdee94001dd4ffbc1b446a9d52d7e51cf2	^	s	sha(p)
3392	426	summary/baaf/align-a-c.json	,d	size(p)
3392	1c88af889538788a8c7842e79aea5f2e3684802d5d2dbaa5dd293e8003dbfabd	^	s	sha(p)
3393	426	summary/baaf/align-b-c.json	,d	size(p)
3393	1a8d61828b3d882136014f6cd2b2eefc69a963b46a33d49c84e047702103c245	^	s	sha(p)
3394	316	summary/bcrf/d-loop-decode.json	,d	size(p)
3394	9b238160fb9fda206294b9df90bc52724c6d9d97d262681c8e7a6a011b74fae0	^	s	sha(p)
3395	316	summary/baaf/d-loop-decode.json	,d	size(p)
3395	342724e82b1877b12579f04102566a8ae7cba30dd0baea8a55a8cb88acf2e2b9	^	s	sha(p)
3396	12,847	summary/b16c-tables.md	,d	size(p)
3396	8df9a8ccda5f2bbc143bc2dbcaa8868e3dd5a1d1fab8eb427428c2a7d95a19f8	^	s	sha(p)
3397	481	restore/census-compare-b16c.txt	,d	size(p)
3397	5b0015fd2a63e3aa2a6676842da251196fcb1f1540c7532980f006b7c5f90dcc	^	s	sha(p)
3398	1,532	identity-b16c/identity-verdict.txt	,d	size(p)
3398	4634ee944266589d6be3a9a1f90c93cd58c003b4d9fc60a341d43e46d7ff2130	^	s	sha(p)
3480	05:47:56	r2/source-receipt.json	s	get(d, 'reads.b16-state-1.at')
3480	ce5574185d1c05f8ca0d1d669904eb4c4ea21229f8af7f33b624aa461e56dca0	RAW-ARTIFACTS.json	s	same([raw('source/b16-state-1.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16-state-1.sha256')])
3481	05:55:41	r2/source-receipt.json	s	get(d, 'reads.b16-meters-1.at')
3481	3a04b34f9fd83de714ba30523a4ed0ee4b09f4fae1e413d4adfc9891ebcfa6ca	RAW-ARTIFACTS.json	s	same([raw('source/b16-meters-1.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16-meters-1.sha256')])
3482	06:01:44	r2/source-receipt.json	s	get(d, 'reads.b16-meters-2.at')
3482	5e8e366bd950e2523b57735c4be8c3b672cda416b105b3ddc55ee3d6d18611b2	RAW-ARTIFACTS.json	s	same([raw('source/b16-meters-2.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16-meters-2.sha256')])
3483	06:01:48	r2/source-receipt.json	s	get(d, 'reads.b16-state-2.at')
3483	f4bcf327c815ec686ec7bb2573551e0ac78cbb6ba03d0862cff7480a65b6bd1e	RAW-ARTIFACTS.json	s	same([raw('source/b16-state-2.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16-state-2.sha256')])
3484	06:23:06	r2/source-receipt.json	s	get(d, 'reads.b16b-state-1.at')
3484	6b4cd4e6a325b389e4be65e43e5109ed903f7ca27b58864e9dbef531b4818c72	RAW-ARTIFACTS.json	s	same([raw('source/b16b-state-1.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16b-state-1.sha256')])
3485	06:23:30	r2/source-receipt.json	s	get(d, 'reads.b16b-meters-1.at')
3485	a7c844bddf786fb0eccfd15af94b5c0bc1b5ae55bbe49e5021dedce01a6c2c04	RAW-ARTIFACTS.json	s	same([raw('source/b16b-meters-1.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16b-meters-1.sha256')])
3486	06:50:05	r2/source-receipt.json	s	get(d, 'reads.b16b-meters-2.at')
3486	fb5c6e23143b1379948586545b66fc26a3419827c72eb929ad4b531fcbc273ed	RAW-ARTIFACTS.json	s	same([raw('source/b16b-meters-2.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16b-meters-2.sha256')])
3487	06:50:08	r2/source-receipt.json	s	get(d, 'reads.b16b-state-2.at')
3487	b8f0746478b7cd652f3a06234aa7358a4078614f0b0fc64344a9a476b1d25288	RAW-ARTIFACTS.json	s	same([raw('source/b16b-state-2.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16b-state-2.sha256')])
3488	07:48:56	r2/source-receipt.json	s	get(d, 'reads.b16c-state-1.at')
3488	195d59866d6ccd976e95d79f3833b6ff01c0ab5bac7d04e934b7338a97d54a3a	RAW-ARTIFACTS.json	s	same([raw('source/b16c-state-1.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16c-state-1.sha256')])
3489	07:49:34	r2/source-receipt.json	s	get(d, 'reads.b16c-meters-1.at')
3489	f694f3dfdbec41ec48e85fec9bc77019a4168855d2f01f921a88e677af19fbf7	RAW-ARTIFACTS.json	s	same([raw('source/b16c-meters-1.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16c-meters-1.sha256')])
3490	08:03:29	r2/source-receipt.json	s	get(d, 'reads.b16c-meters-2.at')
3490	794b67fe8ab03f3e61c2eaf9245d0988849b1ce73cd26167ab67f8690d5e01ab	RAW-ARTIFACTS.json	s	same([raw('source/b16c-meters-2.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16c-meters-2.sha256')])
3491	08:03:32	r2/source-receipt.json	s	get(d, 'reads.b16c-state-2.at')
3491	93cb9240f72ee45779008872da841cb3bec4bb7de527bb05381a91dfac781624	RAW-ARTIFACTS.json	s	same([raw('source/b16c-state-2.json')['sha256'], get(load('r2/source-receipt.json'), 'reads.b16c-state-2.sha256')])
3501	10,234	tools/r2_poll_b16c.py	,d	size(p)
3501	14ae199a556bca981cd9898d186efd983609325b93412beb6dd332a0f0276cb2	^	s	sha(p)
3502	6,604	tools/r2_source_b16.py	,d	size(p)
3502	903145f68d3ce8e4e2dc3813b67ac9acfad2b0361a58b146e73b839bec63fa3c	^	s	sha(p)
3503	4,874	tools/r2_b0_receipt.py	,d	size(p)
3503	cf650fa86179d611ddf63eed2151b5f1062847fd6797b277590e3a5e82cdfcad	^	s	sha(p)
3504	6,945	r2/bcrf-poll-receipt.json	,d	size(p)
3504	abb1f853804c23c364b49f2b4263bcae68b928881ccb501d187f78a64c00660f	^	s	sha(p)
3505	62,923	r2/bcrf-poll-trace.tsv	,d	size(p)
3505	050aeded3806ec9ec821b19da28b85313a9ae58921fc9d2c86a236d10078f1db	^	s	sha(p)
3506	7,446	r2/baaf-poll-receipt.json	,d	size(p)
3506	2f8cc0894cfb8918ff3b066721f8e0b0200c2241ee280375202cf6d6f641c931	^	s	sha(p)
3507	62,923	r2/baaf-poll-trace.tsv	,d	size(p)
3507	3e891d0faf7ba65997b8a487ad53f01e86dfc2713fa8b1721ff33c0d1bdfdeea	^	s	sha(p)
3508	21,276	r2/source-receipt.json	,d	size(p)
3508	1afbce9cdd27468394bf33265c45f1bb1d1e7a46091e15a715950a2ba4406912	^	s	sha(p)
3509	2,484	r2/b0-2-receipt.json	,d	size(p)
3509	8bcab8394d2f8d02890c76ce9bf5f864f53cf195ae4c58bec8bee055c3aba6f7	^	s	sha(p)
3510	1,984	controls/r2-controls.json	,d	size(p)
3510	dc6f67634197b22e7f30225758d4221f697833472997b0b05a8174d94956b437	^	s	sha(p)
3614	1,990	tools/r3_playback_logs.py	,d	size(p)
3614	27334c6d3106f9305187deef6196a7dcb7e14b10d6fbea08f721029766dcf595	^	s	sha(p)
3615	795	r3/playback-logs.json	,d	size(p)
3615	68e905288cf0c01c385a995bf66edc78e6323e041de99c1e0f1f3e4b360f64fe	^	s	sha(p)
3616	6,541	tools/r3_check_controls.py	,d	size(p)
3616	85fc57876334b823cd349a9752bf12581bbb22f9f5c5b2a4d6f68ab948a54157	^	s	sha(p)
3617	1,579	controls/r3-controls.json	,d	size(p)
3617	6b6f8bc7b99e5ec6843a7c385e681b4bcf4b89b1b56d84dcc10a88889ce6cc05	^	s	sha(p)
3702	5,191	tools/r4_evidence_receipt.py	,d	size(p)
3702	7dca8a53f24c1e7330ed2e154e41f4e30a47012171d68c2a80c138c2834c6164	^	s	sha(p)
3703	38,177	r4/evidence-receipt.json	,d	size(p)
3703	1a433cd27edb2632a92e7abbc1f4eebca9ad4d15fae55f23d98a48647ee9805a	^	s	sha(p)
3704	10,379	tools/r4_check_controls.py	,d	size(p)
3704	54d2e1df507cb1b8c8b77214942f49cfcbe3a524f4e52b882ae124384e6d4e0f	^	s	sha(p)
3705	3,116	controls/r4-controls.json	,d	size(p)
3705	d01b56caf89cf99604dc32ce2d69118618fae457074c7c723eb792ef890b68e5	^	s	sha(p)
3706	1,579	controls/r4-rerun-r3-controls.json	,d	size(p)
3706	a0c9a8ed6f768b70208c1c28e6d37c402444a57b2877b882f175c5db4586ce87	^	s	sha(p)
3829	16,186	tools/r5_check_controls.py	,d	size(p)
3829	bf84a387ebdaae6fee5dc93f9da5b9b06bcb827281ff1c51eac3b7da17a8aa2e	^	s	sha(p)
3830	8,154	controls/r5-controls.json	,d	size(p)
3830	c22a199aa34ed8fb4d01fe238bf601d45f519cec484fe3035aee833b179a0188	^	s	sha(p)
3831	1,579	controls/r5-rerun-r3-controls.json	,d	size(p)
3831	4871ef3e84d940d91cc7938ca2ebaf3f904e39b74e21678aa03c602dae7e3560	^	s	sha(p)
3832	3,116	controls/r5-rerun-r4-controls.json	,d	size(p)
3832	a79d24b9c9e272960eb1ffe528c5ada294571f5a5a63fbe217e8d2c344e4964d	^	s	sha(p)
3833	8,165	controls/r5-controls-on-r4-check.json	,d	size(p)
3833	2569e99d4283036b2bc38868812721621330b86b8dbfa735e5ad08fad544391b	^	s	sha(p)
3983	21,545	tools/r6_check_controls.py	,d	size(p)
3983	789a4f7ca25b8ef0d5b38bae9432d9f6be23434fe69ad20f0db9d7a80eb875de	^	s	sha(p)
3984	14,414	controls/r6-controls.json	,d	size(p)
3984	a9709363266aaa05cc1a04b2d90cbbb095a426650a9f802325cbf3fe0335f043	^	s	sha(p)
3985	1,579	controls/r6-rerun-r3-controls.json	,d	size(p)
3985	4871ef3e84d940d91cc7938ca2ebaf3f904e39b74e21678aa03c602dae7e3560	^	s	sha(p)
3986	3,115	controls/r6-rerun-r4-controls.json	,d	size(p)
3986	cde959a0d411c360f6a2159196d22bc0311006bea9025a863e192b75b3d0d02b	^	s	sha(p)
3987	8,153	controls/r6-rerun-r5-controls.json	,d	size(p)
3987	d3e0663e86195cf88e45353661cdd9464eb26d1f8622c378fc0abffaf667613f	^	s	sha(p)
3988	14,432	controls/r6-controls-on-r5-check.json	,d	size(p)
3988	8f03249c0ec24a6b018122b5be2d45780ab97d145d692d067abd43c2bb141943	^	s	sha(p)
3989	6,586	tools/r6_evidence_receipt.py	,d	size(p)
3989	71d32ba09f2ec1f4ab02bc9adf8085b66e96e5ca35c7243026b25ba10fe1f0bb	^	s	sha(p)
3990	46,562	r6/evidence-receipt.json	,d	size(p)
3990	bc3c0e91362f28ebcdc21d13c2e9d2ae875803da60e216b29e9227f79d35a58d	^	s	sha(p)
4107	28,060	tools/r7_check_controls.py	,d	size(p)
4107	6a53a284ef5e70910282c3551285d82161d77412804c27830b7c684adc80c8fb	^	s	sha(p)
4108	18,201	controls/r7-controls.json	,d	size(p)
4108	5b782cd6734c2a637df54b968693dfd230e9210677778f5039d08eb37f39e576	^	s	sha(p)
4109	1,579	controls/r7-rerun-r3-controls.json	,d	size(p)
4109	4871ef3e84d940d91cc7938ca2ebaf3f904e39b74e21678aa03c602dae7e3560	^	s	sha(p)
4110	3,115	controls/r7-rerun-r4-controls.json	,d	size(p)
4110	f635748893ab28b258768f74aeede60a58b2ffa3a41abecac5af8b11ce3d1b60	^	s	sha(p)
4111	8,153	controls/r7-rerun-r5-controls.json	,d	size(p)
4111	cfba195f4842f725385f6a7c7de1449c780050d94b05495bdff0289de32a00e7	^	s	sha(p)
4112	14,414	controls/r7-rerun-r6-controls.json	,d	size(p)
4112	79e4edf8360106c43474d4bc77807c8beb1296f62fb27d211217c0e89b648946	^	s	sha(p)
4113	18,212	controls/r7-controls-on-r6-check.json	,d	size(p)
4113	f288208a13bff378280fd5f9e4cbb1e4e17a137790730bc1d007319d398fa6e3	^	s	sha(p)
4114	6,919	tools/r7_evidence_receipt.py	,d	size(p)
4114	a46c4ad554c6a1448319f7d1e26fdf6e01407aedb0d4868d1fb96bf66d8b099e	^	s	sha(p)
4115	52,808	r7/evidence-receipt.json	,d	size(p)
4115	23322f43d94c68a2dcc6da0412007596828c33bcb60fdb522f1a0f4fbf4a128f	^	s	sha(p)
4268	36,524	tools/r8_check_controls.py	,d	size(p)
4268	68f85edf41723ad7e87aa7dd4353182666022bb7286cdfa81cccbbe86fb864d6	^	s	sha(p)
4269	26,053	controls/r8-controls.json	,d	size(p)
4269	83f791b3819086772ce214262e148c0b8e5e6241f1895cb31acc09cecb7ed64b	^	s	sha(p)
4270	26,077	controls/r8-controls-on-r7-check.json	,d	size(p)
4270	ddea3af5efc65645fcadde07c5e38f7d7d70149956d7437ae4d6fcc3949a4b40	^	s	sha(p)
4271	7,353	tools/r8_evidence_receipt.py	,d	size(p)
4271	95c3ca5ea4f5ebda66ea3d5bbeb2584cb7dda9773182ac40b3b9aea4c6a1ebee	^	s	sha(p)
4272	59,920	r8/evidence-receipt.json	,d	size(p)
4272	1377b5d575bd0adb974a5cfc5f002a8e3d12d222e8b89ff22cd7f6f14709b502	^	s	sha(p)
2722	1,145,034	summary/pts1/a-peer-tap.json	,d	d['frames']
2722	190,839	^	,d	d['info']['pdus']
2722	0	^	d	d['info']['seq_gaps']
2722	-14.1353	^	.4f	T(d, 0, 'level_dbfs')
2722	997.0069	^	.4f	T(d, 0, 'f_hz')
2722	+6.94	^	+z.2f	T(d, 0, 'ppm')
2722	-108.74	^	.2f	T(d, 0, 'thdn_db')
2722	-100.95	^	.2f	T(d, 0, 'worst')
2722	108.74	^	.2f	T(d, 0, 'snr_db')
2722	9,973.0692	^	,.4f	T(d, 1, 'f_hz')
2722	+6.94	^	+z.2f	T(d, 1, 'ppm')
2722	-88.87	^	.2f	T(d, 1, 'thdn_db')
2722	-80.97	^	.2f	T(d, 1, 'worst')
2722	88.87	^	.2f	T(d, 1, 'snr_db')
2723	1,149,822	summary/pts1/b-dut-tap.json	,d	d['frames']
2723	191,637	^	,d	d['info']['pdus']
2723	0	^	d	d['info']['seq_gaps']
2723	-14.1353	^	.4f	T(d, 0, 'level_dbfs')
2723	997.0069	^	.4f	T(d, 0, 'f_hz')
2723	+6.94	^	+z.2f	T(d, 0, 'ppm')
2723	-107.17	^	.2f	T(d, 0, 'thdn_db')
2723	-100.80	^	.2f	T(d, 0, 'worst')
2723	107.17	^	.2f	T(d, 0, 'snr_db')
2723	9,973.0692	^	,.4f	T(d, 1, 'f_hz')
2723	+6.94	^	+z.2f	T(d, 1, 'ppm')
2723	-87.26	^	.2f	T(d, 1, 'thdn_db')
2723	-80.81	^	.2f	T(d, 1, 'worst')
2723	87.26	^	.2f	T(d, 1, 'snr_db')
2724	480,000	summary/pts1/c-mcasp.json	,d	d['frames']
2724	-14.1353	^	.4f	T(d, 0, 'level_dbfs')
2724	997.0069	^	.4f	T(d, 0, 'f_hz')
2724	+6.95	^	+z.2f	T(d, 0, 'ppm')
2724	-105.27	^	.2f	T(d, 0, 'thdn_db')
2724	-98.66	^	.2f	T(d, 0, 'worst')
2724	105.27	^	.2f	T(d, 0, 'snr_db')
2724	9,973.0693	^	,.4f	T(d, 1, 'f_hz')
2724	+6.95	^	+z.2f	T(d, 1, 'ppm')
2724	-85.33	^	.2f	T(d, 1, 'thdn_db')
2724	-78.67	^	.2f	T(d, 1, 'worst')
2724	85.33	^	.2f	T(d, 1, 'snr_db')
2725	1,149,828	summary/pts2/a-peer-tap.json	,d	d['frames']
2725	191,638	^	,d	d['info']['pdus']
2725	0	^	d	d['info']['seq_gaps']
2725	-14.1353	^	.4f	T(d, 0, 'level_dbfs')
2725	997.0069	^	.4f	T(d, 0, 'f_hz')
2725	+6.96	^	+z.2f	T(d, 0, 'ppm')
2725	-107.72	^	.2f	T(d, 0, 'thdn_db')
2725	-101.02	^	.2f	T(d, 0, 'worst')
2725	107.72	^	.2f	T(d, 0, 'snr_db')
2725	9,973.0694	^	,.4f	T(d, 1, 'f_hz')
2725	+6.96	^	+z.2f	T(d, 1, 'ppm')
2725	-87.82	^	.2f	T(d, 1, 'thdn_db')
2725	-81.05	^	.2f	T(d, 1, 'worst')
2725	87.82	^	.2f	T(d, 1, 'snr_db')
2726	1,149,822	summary/pts2/b-dut-tap.json	,d	d['frames']
2726	191,637	^	,d	d['info']['pdus']
2726	0	^	d	d['info']['seq_gaps']
2726	-14.1353	^	.4f	T(d, 0, 'level_dbfs')
2726	997.0069	^	.4f	T(d, 0, 'f_hz')
2726	+6.96	^	+z.2f	T(d, 0, 'ppm')
2726	-108.33	^	.2f	T(d, 0, 'thdn_db')
2726	-100.62	^	.2f	T(d, 0, 'worst')
2726	108.33	^	.2f	T(d, 0, 'snr_db')
2726	9,973.0694	^	,.4f	T(d, 1, 'f_hz')
2726	+6.96	^	+z.2f	T(d, 1, 'ppm')
2726	-88.44	^	.2f	T(d, 1, 'thdn_db')
2726	-80.64	^	.2f	T(d, 1, 'worst')
2726	88.44	^	.2f	T(d, 1, 'snr_db')
2727	480,000	summary/pts2/c-mcasp.json	,d	d['frames']
2727	-14.1353	^	.4f	T(d, 0, 'level_dbfs')
2727	997.0069	^	.4f	T(d, 0, 'f_hz')
2727	+6.96	^	+z.2f	T(d, 0, 'ppm')
2727	-109.70	^	.2f	T(d, 0, 'thdn_db')
2727	-101.43	^	.2f	T(d, 0, 'worst')
2727	109.70	^	.2f	T(d, 0, 'snr_db')
2727	9,973.0694	^	,.4f	T(d, 1, 'f_hz')
2727	+6.96	^	+z.2f	T(d, 1, 'ppm')
2727	-89.87	^	.2f	T(d, 1, 'thdn_db')
2727	-81.46	^	.2f	T(d, 1, 'worst')
2727	89.87	^	.2f	T(d, 1, 'snr_db')
2728	1,149,834	summary/pts3/a-peer-tap.json	,d	d['frames']
2728	191,639	^	,d	d['info']['pdus']
2728	0	^	d	d['info']['seq_gaps']
2728	-14.1035	^	.4f	T(d, 0, 'level_dbfs')
2728	997.0000	^	.4f	T(d, 0, 'f_hz')
2728	0.000	^	z.3f	T(d, 0, 'ppm')
2728	-123.93	^	.2f	T(d, 0, 'thdn_db')
2728	-109.28	^	.2f	T(d, 0, 'worst')
2728	123.94	^	.2f	T(d, 0, 'snr_db')
2728	9,973.0000	^	,.4f	T(d, 1, 'f_hz')
2728	0.000	^	z.3f	T(d, 1, 'ppm')
2728	-122.47	^	.2f	T(d, 1, 'thdn_db')
2728	-89.43	^	.2f	T(d, 1, 'worst')
2728	122.48	^	.2f	T(d, 1, 'snr_db')
2729	1,149,822	summary/pts3/b-dut-tap.json	,d	d['frames']
2729	191,637	^	,d	d['info']['pdus']
2729	0	^	d	d['info']['seq_gaps']
2729	-14.1035	^	.4f	T(d, 0, 'level_dbfs')
2729	997.0000	^	.4f	T(d, 0, 'f_hz')
2729	0.000	^	z.3f	T(d, 0, 'ppm')
2729	-123.93	^	.2f	T(d, 0, 'thdn_db')
2729	-109.31	^	.2f	T(d, 0, 'worst')
2729	123.93	^	.2f	T(d, 0, 'snr_db')
2729	9,973.0000	^	,.4f	T(d, 1, 'f_hz')
2729	0.000	^	z.3f	T(d, 1, 'ppm')
2729	-122.47	^	.2f	T(d, 1, 'thdn_db')
2729	-89.46	^	.2f	T(d, 1, 'worst')
2729	122.47	^	.2f	T(d, 1, 'snr_db')
2730	480,000	summary/pts3/c-mcasp.json	,d	d['frames']
2730	-14.1035	^	.4f	T(d, 0, 'level_dbfs')
2730	997.0000	^	.4f	T(d, 0, 'f_hz')
2730	0.000	^	z.3f	T(d, 0, 'ppm')
2730	-123.97	^	.2f	T(d, 0, 'thdn_db')
2730	-110.32	^	.2f	T(d, 0, 'worst')
2730	123.98	^	.2f	T(d, 0, 'snr_db')
2730	9,973.0000	^	,.4f	T(d, 1, 'f_hz')
2730	0.000	^	z.3f	T(d, 1, 'ppm')
2730	-123.97	^	.2f	T(d, 1, 'thdn_db')
2730	-90.50	^	.2f	T(d, 1, 'worst')
2730	123.97	^	.2f	T(d, 1, 'snr_db')
2731	1,919,610	summary/b0-2/a-peer-tap.json	,d	d['frames']
2731	319,935	^	,d	d['info']['pdus']
2731	0	^	d	d['info']['seq_gaps']
2731	-14.1035	^	.4f	T(d, 0, 'level_dbfs')
2731	997.0000	^	.4f	T(d, 0, 'f_hz')
2731	0.000	^	z.3f	T(d, 0, 'ppm')
2731	-123.62	^	.2f	T(d, 0, 'thdn_db')
2731	-102.55	^	.2f	T(d, 0, 'worst')
2731	123.62	^	.2f	T(d, 0, 'snr_db')
2731	9,973.0000	^	,.4f	T(d, 1, 'f_hz')
2731	0.000	^	z.3f	T(d, 1, 'ppm')
2731	-114.29	^	.2f	T(d, 1, 'thdn_db')
2731	-82.58	^	.2f	T(d, 1, 'worst')
2731	114.29	^	.2f	T(d, 1, 'snr_db')
2732	1,919,592	summary/b0-2/b-dut-tap.json	,d	d['frames']
2732	319,932	^	,d	d['info']['pdus']
2732	0	^	d	d['info']['seq_gaps']
2732	-14.1035	^	.4f	T(d, 0, 'level_dbfs')
2732	997.0000	^	.4f	T(d, 0, 'f_hz')
2732	0.000	^	z.3f	T(d, 0, 'ppm')
2732	-123.62	^	.2f	T(d, 0, 'thdn_db')
2732	-102.15	^	.2f	T(d, 0, 'worst')
2732	123.62	^	.2f	T(d, 0, 'snr_db')
2732	9,973.0000	^	,.4f	T(d, 1, 'f_hz')
2732	0.000	^	z.3f	T(d, 1, 'ppm')
2732	-114.33	^	.2f	T(d, 1, 'thdn_db')
2732	-82.18	^	.2f	T(d, 1, 'worst')
2732	114.33	^	.2f	T(d, 1, 'snr_db')
2733	14,400,000	summary/b0-2/c-mcasp.json	,d	d['frames']
2733	-14.1035	^	.4f	T(d, 0, 'level_dbfs')
2733	997.0000	^	.4f	T(d, 0, 'f_hz')
2733	0.000	^	z.3f	T(d, 0, 'ppm')
2733	-123.95	^	.2f	T(d, 0, 'thdn_db')
2733	-100.47	^	.2f	T(d, 0, 'worst')
2733	123.95	^	.2f	T(d, 0, 'snr_db')
2733	9,973.0000	^	,.4f	T(d, 1, 'f_hz')
2733	0.000	^	z.3f	T(d, 1, 'ppm')
2733	-122.80	^	.2f	T(d, 1, 'thdn_db')
2733	-80.48	^	.2f	T(d, 1, 'worst')
2733	122.80	^	.2f	T(d, 1, 'snr_db')
2822	300	summary/b0-2/c-b9-grade.json	d	d['summary']['blocks']
2822	0	^	d#1	d['summary']['events']
2822	169	^	d	d['summary']['blocks_at_floor']
2822	-123.98	^	.2f	d['summary']['ch0_floor']['thdn_db_median']
2822	-123.91	^	.2f	d['summary']['ch0_floor']['thdn_db_worst']
2822	123.98	^	.2f	d['summary']['ch0_floor']['snr_db_median']
2822	-123.95	^	.2f	d['summary']['ch0_all']['thdn_db_median']
2822	-100.47	^	.2f	d['summary']['ch0_all']['thdn_db_worst']
2822	-14.10	^	.2f	d['summary']['ch0_all']['level_dbfs_median']
2822	0.0000	^	z.4f	d['summary']['ch0_all']['ppm_median']
2822	0.030	^	.3f	d['summary']['ch0_all']['ppm_maxabs']
2823	300	^	d	d['summary']['blocks']
2823	0	^	d#0	d['summary']['events']
2823	169	^	d	d['summary']['blocks_at_floor']
2823	-123.95	^	.2f	d['summary']['ch1_floor']['thdn_db_median']
2823	-120.18	^	.2f	d['summary']['ch1_floor']['thdn_db_worst']
2823	123.95	^	.2f	d['summary']['ch1_floor']['snr_db_median']
2823	-122.80	^	.2f	d['summary']['ch1_all']['thdn_db_median']
2823	-80.48	^	.2f	d['summary']['ch1_all']['thdn_db_worst']
2823	-14.10	^	.2f	d['summary']['ch1_all']['level_dbfs_median']
2823	0.0000	^	z.4f	d['summary']['ch1_all']['ppm_median']
2823	0.030	^	.3f	d['summary']['ch1_all']['ppm_maxabs']
3117	1,919,598	summary/bcrf/a-peer-tap.json	,d	d['frames']
3117	319,933	^	,d	d['info']['pdus']
3117	0	^	d	d['info']['seq_gaps']
3117	-14.1035	^	.4f	T(d, 0, 'level_dbfs')
3117	997.0000	^	.4f	T(d, 0, 'f_hz')
3117	0.000	^	z.3f	T(d, 0, 'ppm')
3117	-123.98	^	.2f	T(d, 0, 'thdn_db')
3117	-123.93	^	.2f	T(d, 0, 'worst')
3117	123.99	^	.2f	T(d, 0, 'snr_db')
3117	9,973.0000	^	,.4f	T(d, 1, 'f_hz')
3117	0.000	^	z.3f	T(d, 1, 'ppm')
3117	-123.97	^	.2f	T(d, 1, 'thdn_db')
3117	-123.93	^	.2f	T(d, 1, 'worst')
3117	123.97	^	.2f	T(d, 1, 'snr_db')
3118	1,919,574	summary/bcrf/b-dut-tap.json	,d	d['frames']
3118	319,929	^	,d	d['info']['pdus']
3118	0	^	d	d['info']['seq_gaps']
3118	-14.1035	^	.4f	T(d, 0, 'level_dbfs')
3118	997.0000	^	.4f	T(d, 0, 'f_hz')
3118	0.000	^	z.3f	T(d, 0, 'ppm')
3118	-123.99	^	.2f	T(d, 0, 'thdn_db')
3118	-123.93	^	.2f	T(d, 0, 'worst')
3118	123.99	^	.2f	T(d, 0, 'snr_db')
3118	9,973.0000	^	,.4f	T(d, 1, 'f_hz')
3118	0.000	^	z.3f	T(d, 1, 'ppm')
3118	-123.97	^	.2f	T(d, 1, 'thdn_db')
3118	-123.93	^	.2f	T(d, 1, 'worst')
3118	123.97	^	.2f	T(d, 1, 'snr_db')
3119	14,400,000	summary/bcrf/c-mcasp.json	,d	d['frames']
3119	-14.1035	^	.4f	T(d, 0, 'level_dbfs')
3119	997.0000	^	.4f	T(d, 0, 'f_hz')
3119	0.000	^	z.3f	T(d, 0, 'ppm')
3119	-123.98	^	.2f	T(d, 0, 'thdn_db')
3119	-123.93	^	.2f	T(d, 0, 'worst')
3119	123.99	^	.2f	T(d, 0, 'snr_db')
3119	9,973.0000	^	,.4f	T(d, 1, 'f_hz')
3119	0.000	^	z.3f	T(d, 1, 'ppm')
3119	-123.97	^	.2f	T(d, 1, 'thdn_db')
3119	-123.90	^	.2f	T(d, 1, 'worst')
3119	123.97	^	.2f	T(d, 1, 'snr_db')
3120	1,919,598	summary/baaf/a-peer-tap.json	,d	d['frames']
3120	319,933	^	,d	d['info']['pdus']
3120	0	^	d	d['info']['seq_gaps']
3120	-14.1035	^	.4f	T(d, 0, 'level_dbfs')
3120	997.0000	^	.4f	T(d, 0, 'f_hz')
3120	0.000	^	z.3f	T(d, 0, 'ppm')
3120	-123.98	^	.2f	T(d, 0, 'thdn_db')
3120	-123.93	^	.2f	T(d, 0, 'worst')
3120	123.98	^	.2f	T(d, 0, 'snr_db')
3120	9,973.0000	^	,.4f	T(d, 1, 'f_hz')
3120	0.000	^	z.3f	T(d, 1, 'ppm')
3120	-123.98	^	.2f	T(d, 1, 'thdn_db')
3120	-123.93	^	.2f	T(d, 1, 'worst')
3120	123.98	^	.2f	T(d, 1, 'snr_db')
3121	1,919,580	summary/baaf/b-dut-tap.json	,d	d['frames']
3121	319,930	^	,d	d['info']['pdus']
3121	0	^	d	d['info']['seq_gaps']
3121	-14.1035	^	.4f	T(d, 0, 'level_dbfs')
3121	997.0000	^	.4f	T(d, 0, 'f_hz')
3121	0.000	^	z.3f	T(d, 0, 'ppm')
3121	-123.98	^	.2f	T(d, 0, 'thdn_db')
3121	-123.92	^	.2f	T(d, 0, 'worst')
3121	123.98	^	.2f	T(d, 0, 'snr_db')
3121	9,973.0000	^	,.4f	T(d, 1, 'f_hz')
3121	0.000	^	z.3f	T(d, 1, 'ppm')
3121	-123.98	^	.2f	T(d, 1, 'thdn_db')
3121	-123.93	^	.2f	T(d, 1, 'worst')
3121	123.98	^	.2f	T(d, 1, 'snr_db')
3122	14,400,000	summary/baaf/c-mcasp.json	,d	d['frames']
3122	-14.1035	^	.4f	T(d, 0, 'level_dbfs')
3122	997.0000	^	.4f	T(d, 0, 'f_hz')
3122	0.000	^	z.3f	T(d, 0, 'ppm')
3122	-123.98	^	.2f	T(d, 0, 'thdn_db')
3122	-123.92	^	.2f	T(d, 0, 'worst')
3122	123.99	^	.2f	T(d, 0, 'snr_db')
3122	9,973.0000	^	,.4f	T(d, 1, 'f_hz')
3122	0.000	^	z.3f	T(d, 1, 'ppm')
3122	-123.97	^	.2f	T(d, 1, 'thdn_db')
3122	-123.91	^	.2f	T(d, 1, 'worst')
3122	123.97	^	.2f	T(d, 1, 'snr_db')
3123	1,919,610	summary/b0-2/a-peer-tap.json	,d	d['frames']
3123	319,935	^	,d	d['info']['pdus']
3123	0	^	d	d['info']['seq_gaps']
3123	-14.1035	^	.4f	T(d, 0, 'level_dbfs')
3123	997.0000	^	.4f	T(d, 0, 'f_hz')
3123	0.000	^	z.3f	T(d, 0, 'ppm')
3123	-123.62	^	.2f	T(d, 0, 'thdn_db')
3123	-102.55	^	.2f	T(d, 0, 'worst')
3123	123.62	^	.2f	T(d, 0, 'snr_db')
3123	9,973.0000	^	,.4f	T(d, 1, 'f_hz')
3123	0.000	^	z.3f	T(d, 1, 'ppm')
3123	-114.29	^	.2f	T(d, 1, 'thdn_db')
3123	-82.58	^	.2f	T(d, 1, 'worst')
3123	114.29	^	.2f	T(d, 1, 'snr_db')
3124	14,400,000	summary/b0-2/c-mcasp.json	,d	d['frames']
3124	-14.1035	^	.4f	T(d, 0, 'level_dbfs')
3124	997.0000	^	.4f	T(d, 0, 'f_hz')
3124	0.000	^	z.3f	T(d, 0, 'ppm')
3124	-123.95	^	.2f	T(d, 0, 'thdn_db')
3124	-100.47	^	.2f	T(d, 0, 'worst')
3124	123.95	^	.2f	T(d, 0, 'snr_db')
3124	9,973.0000	^	,.4f	T(d, 1, 'f_hz')
3124	0.000	^	z.3f	T(d, 1, 'ppm')
3124	-122.80	^	.2f	T(d, 1, 'thdn_db')
3124	-80.48	^	.2f	T(d, 1, 'worst')
3124	122.80	^	.2f	T(d, 1, 'snr_db')
3134	300	summary/bcrf/c-b9-grade.json	d	d['summary']['blocks']
3134	0	^	d#1	d['summary']['events']
3134	300	^	d	d['summary']['blocks_at_floor']
3134	-123.98	^	.2f	d['summary']['ch0_floor']['thdn_db_median']
3134	-123.93	^	.2f	d['summary']['ch0_floor']['thdn_db_worst']
3134	123.99	^	.2f	d['summary']['ch0_floor']['snr_db_median']
3134	-123.98	^	.2f	d['summary']['ch0_all']['thdn_db_median']
3134	-123.93	^	.2f	d['summary']['ch0_all']['thdn_db_worst']
3134	-14.10	^	.2f	d['summary']['ch0_all']['level_dbfs_median']
3134	0.0000	^	z.4f	d['summary']['ch0_all']['ppm_median']
3134	0.000	^	.3f	d['summary']['ch0_all']['ppm_maxabs']
3135	300	^	d	d['summary']['blocks']
3135	0	^	d#0	d['summary']['events']
3135	300	^	d	d['summary']['blocks_at_floor']
3135	-123.97	^	.2f	d['summary']['ch1_floor']['thdn_db_median']
3135	-123.90	^	.2f	d['summary']['ch1_floor']['thdn_db_worst']
3135	123.97	^	.2f	d['summary']['ch1_floor']['snr_db_median']
3135	-123.97	^	.2f	d['summary']['ch1_all']['thdn_db_median']
3135	-123.90	^	.2f	d['summary']['ch1_all']['thdn_db_worst']
3135	-14.10	^	.2f	d['summary']['ch1_all']['level_dbfs_median']
3135	0.0000	^	z.4f	d['summary']['ch1_all']['ppm_median']
3135	0.000	^	.3f	d['summary']['ch1_all']['ppm_maxabs']
3136	300	summary/baaf/c-b9-grade.json	d	d['summary']['blocks']
3136	0	^	d#1	d['summary']['events']
3136	300	^	d	d['summary']['blocks_at_floor']
3136	-123.98	^	.2f	d['summary']['ch0_floor']['thdn_db_median']
3136	-123.92	^	.2f	d['summary']['ch0_floor']['thdn_db_worst']
3136	123.99	^	.2f	d['summary']['ch0_floor']['snr_db_median']
3136	-123.98	^	.2f	d['summary']['ch0_all']['thdn_db_median']
3136	-123.92	^	.2f	d['summary']['ch0_all']['thdn_db_worst']
3136	-14.10	^	.2f	d['summary']['ch0_all']['level_dbfs_median']
3136	0.0000	^	z.4f	d['summary']['ch0_all']['ppm_median']
3136	0.000	^	.3f	d['summary']['ch0_all']['ppm_maxabs']
3137	300	^	d	d['summary']['blocks']
3137	0	^	d#0	d['summary']['events']
3137	300	^	d	d['summary']['blocks_at_floor']
3137	-123.97	^	.2f	d['summary']['ch1_floor']['thdn_db_median']
3137	-123.91	^	.2f	d['summary']['ch1_floor']['thdn_db_worst']
3137	123.97	^	.2f	d['summary']['ch1_floor']['snr_db_median']
3137	-123.97	^	.2f	d['summary']['ch1_all']['thdn_db_median']
3137	-123.91	^	.2f	d['summary']['ch1_all']['thdn_db_worst']
3137	-14.10	^	.2f	d['summary']['ch1_all']['level_dbfs_median']
3137	0.0000	^	z.4f	d['summary']['ch1_all']['ppm_median']
3137	0.000	^	.3f	d['summary']['ch1_all']['ppm_maxabs']
3138	300	summary/b0-2/c-b9-grade.json	d	d['summary']['blocks']
3138	0	^	d#1	d['summary']['events']
3138	169	^	d	d['summary']['blocks_at_floor']
3138	-123.98	^	.2f	d['summary']['ch0_floor']['thdn_db_median']
3138	-123.91	^	.2f	d['summary']['ch0_floor']['thdn_db_worst']
3138	123.98	^	.2f	d['summary']['ch0_floor']['snr_db_median']
3138	-123.95	^	.2f	d['summary']['ch0_all']['thdn_db_median']
3138	-100.47	^	.2f	d['summary']['ch0_all']['thdn_db_worst']
3138	-14.10	^	.2f	d['summary']['ch0_all']['level_dbfs_median']
3138	0.0000	^	z.4f	d['summary']['ch0_all']['ppm_median']
3138	0.030	^	.3f	d['summary']['ch0_all']['ppm_maxabs']
3139	300	^	d	d['summary']['blocks']
3139	0	^	d#0	d['summary']['events']
3139	169	^	d	d['summary']['blocks_at_floor']
3139	-123.95	^	.2f	d['summary']['ch1_floor']['thdn_db_median']
3139	-120.18	^	.2f	d['summary']['ch1_floor']['thdn_db_worst']
3139	123.95	^	.2f	d['summary']['ch1_floor']['snr_db_median']
3139	-122.80	^	.2f	d['summary']['ch1_all']['thdn_db_median']
3139	-80.48	^	.2f	d['summary']['ch1_all']['thdn_db_worst']
3139	-14.10	^	.2f	d['summary']['ch1_all']['level_dbfs_median']
3139	0.0000	^	z.4f	d['summary']['ch1_all']['ppm_median']
3139	0.030	^	.3f	d['summary']['ch1_all']['ppm_maxabs']
# round 4: rows GEN3 selects by token
2364	997	tools/b6_tone.py	,d#0	tone_hz(0)
2364	9,973	^	,d#0	tone_hz(1)
2647	997	^	,d#0	tone_hz(0)
2647	9,973	^	,d#0	tone_hz(1)
2652	997	^	,d#0	tone_hz(0)
2652	9,973	^	,d#0	tone_hz(1)
2720	997	^	,d#0	tone_hz(0)
2720	9,973	^	,d#0	tone_hz(1)
2792	997	^	,d#0	tone_hz(0)
2792	9,973	^	,d#0	tone_hz(1)
2793	997	^	,d#0	tone_hz(0)
2793	9,973	^	,d#0	tone_hz(1)
2822	997	^	,d#0	tone_hz(0)
2823	9,973	^	,d#0	tone_hz(1)
2825	997	^	,d#0	tone_hz(0)
3008	997	^	,d#0	tone_hz(0)
3008	9,973	^	,d#0	tone_hz(1)
3115	997	^	,d#0	tone_hz(0)
3115	9,973	^	,d#0	tone_hz(1)
3134	997	^	,d#0	tone_hz(0)
3135	9,973	^	,d#0	tone_hz(1)
3136	997	^	,d#0	tone_hz(0)
3137	9,973	^	,d#0	tone_hz(1)
3138	997	^	,d#0	tone_hz(0)
3139	9,973	^	,d#0	tone_hz(1)
3142	997	^	,d#0	tone_hz(0)
3244	997/9,973	^	s#0	f'{tone_hz(0):,}/{tone_hz(1):,}'
3415	997	^	,d#0	tone_hz(0)
3415	9,973	^	,d#0	tone_hz(1)
3564	997/9,973	^	s#0	f'{tone_hz(0):,}/{tone_hz(1):,}'
README.md:15	997	^	,d#0	tone_hz(0)
README.md:15	9,973	^	,d#0	tone_hz(1)
README.md:15	997	^	,d#1	tone_hz(0)
README.md:15	9,973	^	,d#1	tone_hz(1)
# ROWS-END
"""


def parse_rows():
    rows = []
    for x in ROWS_TSV.strip("\n").splitlines():
        if not x or x.startswith("#"):
            continue
        line, shown, src, spec, key = x.split("\t", 4)
        src = rows[-1][2] if src == "^" else src
        spec, _, k = spec.partition("#")
        rows.append((line, shown, src, key, spec, int(k) if k else None))
    return rows


ROWS = parse_rows()

# ---------------------------------------------------------------- coverage
# The figures a row may claim. Round 5: this finds row candidates only; what is covered is decided per digit.
TOKEN = re.compile(
    r"(?<![\w/#.+\-])(?:"
    r"(?P<sha>[0-9a-f]{64})|(?P<commit>[0-9a-f]{40})|(?P<abbr>[0-9a-f]{8}\.\.\.)|"
    r"(?P<hex>0x(?:\.\.\.)?[0-9a-fA-F]+)|"
    r"(?P<date>\d{4}-\d\d-\d\d)|(?P<time>\d\d:\d\d(?::\d\d(?:\.\d+)?)?)|(?P<ver>\d+\.\d+\.\d+)|"
    r"(?P<num>[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:/[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)*)"
    r")(?![\w])"
    r"|(?<=`)(?P<id>[0-9a-f]{6,16})(?=`)"
    r"|\b(?P<word>(?i:" + "|".join(WORDS[1:] + TENS) + r"|once|twice))\b")

# Round 5: a number however it is spelled: a sign (ASCII, Unicode or fullwidth), any Unicode digits with
# thousands commas or a leading point, a decimal part, an exponent.
SIGNS = "+\\-\u2212\u2010-\u2015\ufe63\uff0b\uff0d"
NUM = re.compile(rf"[{SIGNS}]?(?:\d+(?:,\d{{3}})*(?:\.\d+)?|\.\d+)(?:[eE][{SIGNS}]?\d+)?")

# A number followed by a unit is a measurement: only a row may claim it. Between the two may stand nothing,
# whitespace, invisible characters, any hyphen or dash, emphasis or code marks, a backslash, a double quote or
# an opening bracket (rounds 5 and 6). "zero" is read as a number before a unit too. Round 8: no entity,
# comment or tag is looked past: the parser decodes entities and refuses the rest, so the text holds none.
DASHES = "\\-\u2010-\u2015\u2212\ufe63\uff0d"
SEP = r"[\s\u00ad\u200b-\u200d\u2060\ufeff" + DASHES + r"*_~`\\\"\u201c\u201d(\[]*"
MEASURE = re.compile(
    SEP + r"(?i:%|\u2030|per\s*cent|percent(?:age)?|pct|dBFS|dBr|dBc|dBu|dBV|dB|decibels?|ppm|ppb|"
    r"parts?\s+per\s+(?:million|billion|trillion)|(?:pico|nano|micro|milli)?seconds?|[pnu\u00b5\u03bcm]?s|"
    r"[pnu\u00b5\u03bcm]?secs?|mins?|minutes?|h|hrs?|hours?|days?|(?:kilo|mega|giga)?hertz|[kMG]?Hz|[kMG]?bps|"
    r"[kMG]?bit/s|frames?|samples?|blocks?|bytes?|[kMGT]i?B|bits?|LSBs?|polls?|"
    r"PDUs?|packets?|messages?|steps?|slips?|dups?|repeats?|skips?|discontinuit(?:y|ies)|entries|entry|reads|"
    r"cycles?|ticks?|times)(?!\w)")
ZERO = re.compile(r"\b(?i:zero)\b")

# Round 6: what may follow an identifier, a closed list. Past spaces, hyphens and dashes, a slash or a
# backslash, emphasis and code marks, brackets and quotes (not a possessive 's) must stand the end of the text,
# a mark that ends a phrase (. , ; : ! ? |; not a point or comma before a digit; a dash set off by spaces), a
# possessive 's, or a word of AFTER that does not lead into a measurement ("7 to 9 ppm"). Anything else makes
# the identifier's digits a measurement. Round 8: no tag or link target is in the text, so none is looked past.
AFTER = ("and", "or", "to", "of")
ENDS = ".,;:!?|"
PAST = re.compile(r"(?:[\s" + DASHES
                  + r"/\\*_~`()\[\]{}\"\u201c\u201d\u2018\u00ab\u00bb]|['\u2019](?![sS](?![^\W\d_])))*")
POSSESSIVE = re.compile(r"['\u2019][sS](?![^\W\d_])")
SPACED_DASH = re.compile(r"(?:^|\s)(?:-{2,}|[\u2013\u2014\u2015])\s")
WORD_AT = re.compile(r"[^\W\d_]+(?!\w)")


def follows(text, e, code=False):
    """Whether the closed list holds what follows an identifier ending at text[e]: (True, '') or (False,
    what stands there). A code literal ends with its code word."""
    if code and (e == len(text) or text[e] == "`" or text[e].isspace()):
        return True, ""
    i = PAST.match(text, e).end()
    if i == len(text) or SPACED_DASH.search(text, e, i):
        return True, ""
    if text[i] in ENDS:
        return not (text[i] in ".," and text[i + 1:i + 2].isdigit()), text[i:i + 2]
    if POSSESSIVE.match(text, i):
        return True, ""
    w = WORD_AT.match(text, i)
    if w and w.group(0) in AFTER:
        x = NUM.match(text, PAST.match(text, w.end()).end())
        return not (x and measured(text, x.start(), x.end())), text[i:x.end()] if x else ""
    return False, w.group(0) if w else text[i]


def measured(text, a, b):
    """The number at text[a:b] stands before a unit. A number quoted on its own ("37") is a mention: its
    closing quote does not join it to a unit; it needs a row either way."""
    quoted = a and text[a - 1] in '"\u201c' and text[b:b + 1] in ('"', '\u201d')
    return not quoted and MEASURE.match(text, b) is not None

# (category, regex, test, code). Each regex reads a block and holds the keyword with the identifier: its groups
# named t, t2 (or, with none, the whole match). A match holding a bar or crossing a sentence's end counts for
# nothing; a test, when given, must pass; what follows the identifier must be on the closed list (follows). A
# code literal (code) must lie in one code span, as the parser read it (round 8), and ends with its code word.
EXCLUDE = []


def X(cat, rx, ok=None, code=False):
    EXCLUDE.append((cat, re.compile(rx), ok, code))


_names = {}


def packet_path(word):
    """A path cited in code that names a packet file or directory (a bare name: the base name of one), a
    raw file RAW-ARTIFACTS.json lists, or one of them in the published packet's directory."""
    if not _names:
        _names["rel"] = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*")}
        _names["raw"] = {x["path"] for x in load("RAW-ARTIFACTS.json")["files"]}
        _names["base"] = {p.rsplit("/", 1)[-1] for p in _names["rel"] | _names["raw"]}
    w = word.rstrip("/")
    m = re.fullmatch(r"review-evidence/629-b16-r1(?:/author-r[1-8])?(?:/(.+))?", w)
    if m:
        return not m.group(1) or m.group(1) == "MANIFEST.json" or packet_path(m.group(1))
    if "/" in w:
        return w in _names["rel"] or w in _names["raw"]
    return w in _names["base"]


CODE = []


def in_code(m, text, name=None):
    """The match lies inside one code span (CODE, as the parser read it) and names a packet path, or is
    `name`."""
    s = CODE[m.start()] if 0 < m.start() and m.end() < len(CODE) else -1
    return s >= 0 and all(CODE[i] == s for i in range(m.start() - 1, m.end() + 1)) \
        and (m.group("t") == name if name else packet_path(m.group("t")))


_slugs, HEADINGS = set(), []


def on_page(t):
    """A link target that resolves: an issue or pull request of the repository on GitHub, or the anchor of
    a heading of the findings page (HEADINGS, as the parser reads them)."""
    if re.fullmatch(r"https://github\.com/kebag-logic/milan-fpga/(?:issues|pull)/\d+(?:#issuecomment-\d+)?", t):
        return True
    if not _slugs:
        for x in HEADINGS:
            s = re.sub(r"[^\w\- ]", "", x.strip().lower()).replace(" ", "-")
            n, i = s, 1
            while n in _slugs:
                n, i = f"{s}-{i}", i + 1
            _slugs.add(n)
    page, _, anchor = t.partition("#")
    return page in ("", DOC_P.name) and anchor in _slugs


# EXCLUDE-BEGIN
X("commit", r"`(?P<t>5603c353|694d7da6|0d4ff919|e20fd282|35e332b6|c20c85bd|e8454e27|0782c55f|b84584e4|61ae8641|b83e5d76|36190193|a73ce5c4|e91a62ee|b616e7ea)`", code=True)
X("commit", r"\bDev (?P<t>5603c353)\b")
X("clause", r"\bIEEE (?P<t>1722\.1)\b")
X("clause", r"\bMilan v(?P<t>1\.2) Table (?P<t2>5\.4)\b")
X("descriptor index", r"\b(?:STREAM_INPUT|STREAM_OUTPUT|STREAM_PORT_INPUT|STREAM_PORT_OUTPUT|CLOCK_DOMAIN|ENTITY|CONFIGURATION)\s+(?P<t>\d+)\b")
X("channel index", r"\b[Cc]hannels?\s+(?P<t>\d+)(?:\s+(?:and|to)\s+(?P<t2>\d+))?\b")
X("step or round index", r"\b(?:[Ss]teps?|[Rr]ounds?)\s+(?P<t>[a-z]?\d+)(?:\s+and\s+(?P<t2>[a-z]?\d+))?\b")
X("packet label", r"`(?P<t>629-b16-a603)`", code=True)
X("branch name", r"`(?P<t>629-b16-review-evidence)`", code=True)
X("issue number", r"(?<![\w&])#(?P<t>629|645)\b")
X("lane or case name", r"\b(?P<t>B(?:0|5|6|7|8|9|10|15|16[bc]?))\b")
X("review name", r"\b(?P<t>R62[45]-[1-7](?:-[FRS][1-9])?)\b")
X("operator", r"\[(?P<t>A603)\]")
X("serial port", r"\b(?P<t>McASP0)\b")
X("hash name", r"\b(?P<t>SHA-256|CRC32)\b")
X("entity name", r"\bentity name \"Milan FPGA (?P<t>1x1 TDM8)\"")
X("serial number", r"\bserial \"(?P<t>AX7101-0001)\"")
X("command", r"(?<![^\s`])(?P<t>python3)(?= -I )", lambda m, text: in_code(m, text, "python3"), code=True)
X("field name", r"`(?P<t>original_sha256|published_sha256)`", code=True)
X("packet directory", r"`(?P<t>author-r[1-8]/)`", code=True)
X("packet path", r"(?<![^\s`])(?P<t>[^\s`]*\d[^\s`]*)(?![^\s`])", in_code, code=True)
# EXCLUDE-END


def scope():
    """Every covered line, (document, line) -> (text, the column its covered part starts at)."""
    f = DOC_P.read_text(encoding="utf-8").splitlines()
    r = README_P.read_text(encoding="utf-8").splitlines()
    out = {}
    s = next(i for i, x in enumerate(f) if x.startswith(SECTION))
    e = next((i for i in range(s + 1, len(f)) if f[i].startswith("## ")), len(f))
    for i in range(s, e):
        out[(DOC_P.name, i + 1)] = (f[i], 0)
    i = next(i for i, x in enumerate(f) if x.startswith("In lane B16, the operator tried the reference peer's own loopback"))
    while f[i].strip():
        out[(DOC_P.name, i + 1)] = (f[i], 0)
        i += 1
    i = next(i for i, x in enumerate(f) if x.startswith("- **[Dev 5603c353, 2026-10-12: lane B16]"))
    out[(DOC_P.name, i + 1)] = (f[i], 0)
    i = next(i for i, x in enumerate(r) if x.startswith("| [629_MEDIA_CLOCK_FOLLOWING_BENCH.md]"))
    out[(README_P.name, i + 1)] = (r[i], r[i].index("Lane B16, `5603c353`:"))
    return out


# Round 8: the reader. The repository's pinned Markdown parser, verified as the documentation gates verify it
# (scripts/gen_toc_renderer.py), with that renderer's extensions and options. Only ALLOWED constructs may stand
# in the covered text; any other is refused at its line, named MARKUP, and not read. GENERATED: the markers
# check_solution_docs.py writes, excepted as whole lines of raw HTML, byte for byte.
ALLOWED = ("document", "paragraph", "heading", "list", "item", "block_quote", "table", "table_header", "table_row",
           "table_cell", "text", "softbreak", "linebreak", "emph", "strong", "link", "code")
LEAVES = ("paragraph", "heading", "table_cell")
GENERATED = ("<!-- solution-cpu-contract:start -->", "<!-- solution-cpu-contract:end -->",
             "<!-- solution-interface-groups:start -->", "<!-- solution-interface-groups:end -->")
NODE_API = """typedef struct cmark_node cmark_node;
cmark_node *cmark_node_first_child(cmark_node *node);
cmark_node *cmark_node_next(cmark_node *node);
const char *cmark_node_get_type_string(cmark_node *node);
int cmark_node_get_type(cmark_node *node);
int cmark_node_get_start_line(cmark_node *node);
int cmark_node_get_start_column(cmark_node *node);
int cmark_node_get_end_line(cmark_node *node);
int cmark_node_get_end_column(cmark_node *node);
const char *cmark_node_get_literal(cmark_node *node);
const char *cmark_node_get_url(cmark_node *node);"""
_bound = {}


def bind():
    """The pinned parser and its node calls, loaded once; exit 1, naming what is missing or drifted, otherwise."""
    if not _bound:
        try:
            import cffi
            from cmarkgfm import _cmark
            spec = importlib.util.spec_from_file_location("gen_toc_renderer", REPO / "scripts/gen_toc_renderer.py")
            R = sys.modules["gen_toc_renderer"] = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(R)
        except (ImportError, OSError) as exc:
            sys.exit(f"check_b16_figures.py: the pinned Markdown parser cannot be loaded ({exc}); run it with an "
                     "interpreter that has tools/markdown/requirements.txt installed")
        versions = {}
        for n in R.PINNED:
            try:
                versions[n] = importlib.metadata.version(n)
            except importlib.metadata.PackageNotFoundError:
                versions[n] = None
        bad = R.verify(versions, _cmark.ffi.string(_cmark.lib.cmark_version_string()).decode())
        if bad:
            sys.exit("check_b16_figures.py: not the pinned Markdown parser: " + "; ".join(bad))
        ffi = cffi.FFI()
        ffi.cdef(NODE_API)
        _bound.update(lib=_cmark.lib, ffi=ffi, api=ffi.dlopen(_cmark.__file__), ext=R.EXTENSIONS)
    return _bound


def tree(path):
    """Every node of a document in document order: (kind, first line, column, last line, column, literal, link
    target, depth); columns count bytes from 1. A footnote, <unknown> to the parser, is named by its type."""
    b = bind()
    lib, ffi, api = b["lib"], b["ffi"], b["api"]
    lib.cmark_gfm_core_extensions_ensure_registered()
    parser = lib.cmark_parser_new(lib.CMARK_OPT_SOURCEPOS | lib.CMARK_OPT_UNSAFE | lib.CMARK_OPT_FOOTNOTES
                                  | lib.CMARK_OPT_GITHUB_PRE_LANG)
    for name in b["ext"]:
        lib.cmark_parser_attach_syntax_extension(parser, lib.cmark_find_syntax_extension(name.encode()))
    raw = path.read_bytes()
    lib.cmark_parser_feed(parser, raw, len(raw))
    root = lib.cmark_parser_finish(parser)

    def s(c):
        return "" if c == ffi.NULL else ffi.string(c).decode("utf-8", "replace")
    out, stack = [], [(ffi.cast("cmark_node *", root), 0)]
    while stack:
        n, d = stack.pop()
        if n == ffi.NULL:
            continue
        if d:
            stack.append((api.cmark_node_next(n), d))
        k, t = s(api.cmark_node_get_type_string(n)), api.cmark_node_get_type(n)
        k = {0x800b: "footnote_definition", 0xc00b: "footnote_reference"}.get(t, f"{k} {t:#x}") if k == "<unknown>" else k
        out.append((k, api.cmark_node_get_start_line(n),
                    api.cmark_node_get_start_column(n), api.cmark_node_get_end_line(n),
                    api.cmark_node_get_end_column(n), s(api.cmark_node_get_literal(n)), s(api.cmark_node_get_url(n)), d))
        stack.append((api.cmark_node_first_child(n), d + 1))
    return out


def normalise(raw, src, invisible="\u00ad\u200b\u200c\u200d\u2060\ufeff"):
    """One block's visible text (raw; src[i], the source of raw[i]), whitespace runs as one space, invisible
    characters dropped, ends trimmed. Round 8: escapes, entities and code are the parser's. Returns both."""
    out, pos = [], []
    for ch, p in zip(raw, src):
        if ch in invisible or ch.isspace() and (not out or out[-1] == " "):
            continue
        out.append(" " if ch.isspace() else ch)
        pos.append(p)
    while out and out[-1] == " ":
        out.pop()
        pos.pop()
    return out, pos


def place(lit, sl, sc, el, ec, src):
    """(line, byte column) of each character of a text or code node, aligned on the source; from a character
    the source does not show (an escape, an entity) on, the node's start; an autolink's text, the node's end."""
    if sc < 1:
        return [(sl, ec)] * len(lit)
    region = []
    for ln in range(sl, el + 1):
        b = src[ln - 1].encode() if ln <= len(src) else b""
        c, z = (sc - 1 if ln == sl else 0), (ec if ln == el else len(b))
        for ch in b[c:z].decode("utf-8", "replace"):
            region.append((ch, ln, c + 1))
            c += len(ch.encode())
        region.append(("\n", ln, c + 1))
    out, j = [], 0
    for ch in lit:
        while j < len(region) and region[j][0] != ch and region[j][0] in " \t\n" and not (ch == " " and region[j][0] == "\n"):
            j += 1
        if j < len(region) and (region[j][0] == ch or ch == " " and region[j][0] == "\n"):
            out.append(region[j][1:])
            j += 1
        else:
            j = len(region)
            out.append((sl, sc))
    return out


def blocks(lines):
    """Round 8: (blocks, refused). A block, (text, pos, code), is a paragraph, heading or table cell: its
    visible text; pos[i], the ((document, line), column) of text[i]; code[i], its code span or -1. A link's
    target that does not resolve (on_page) is a block of its own. refused: ((document, line), construct)."""
    out, refused, span = [], [], 0
    for doc, path in ((DOC_P.name, DOC_P), (README_P.name, README_P)):
        cov = {n: len(t[:at].encode()) + 1 for (d, n), (t, at) in lines.items() if d == doc}
        src = path.read_text(encoding="utf-8").split("\n")
        nodes = tree(path)
        if doc == DOC_P.name:
            HEADINGS.clear()
            for i, x in enumerate(nodes):
                if x[0] == "heading":
                    j = i + 1
                    while j < len(nodes) and nodes[j][7] > x[7]:
                        j += 1
                    HEADINGS.append("".join(y[5] for y in nodes[i + 1:j] if y[0] in ("text", "code")))
        skip, leaf, par = None, None, []
        for kind, sl, sc, el, ec, lit, url, d in nodes + [("", 0, 0, 0, 0, "", "", 0)]:
            del par[d:]
            if not sl:
                sl, sc, el, ec = par[-1] if par else (1, 1, 1, 1)
            if (el, ec) < (sl, sc):  # cmark-gfm ends a raw HTML block on the line before its first
                el, ec = sl, len(src[sl - 1].encode()) if sl <= len(src) else 0
            par.append((sl, sc, el, ec))
            if skip is not None and d > skip:
                continue
            skip = None
            if leaf and d <= leaf[2]:
                chars, ps = normalise(leaf[0], leaf[1])
                out.append(("".join(chars), [p[:2] for p in ps], [p[2] for p in ps]))
                leaf = None
            at = next((n for n in range(sl, el + 1) if n in cov and not (n == el and ec < cov[n])), None)
            if at is None or not kind:
                skip = d
                continue
            if kind not in ALLOWED:
                if not (kind == "html_block" and sl == el and src[sl - 1] in GENERATED and lit.rstrip("\n") == src[sl - 1]):
                    b = src[sl - 1].encode()[max(sc, 1) - 1:ec if el == sl else None].decode("utf-8", "replace")
                    refused.append(((doc, at), f"{kind} {b[:40].expandtabs(1).rstrip()}".rstrip()))
                skip = d
                continue
            if kind in LEAVES:
                leaf = [[], [], d]
            elif leaf is None:
                continue
            elif kind == "link" and not on_page(url):
                out.append((url, [((doc, sl), sc)] * len(url), [-1] * len(url)))
            elif kind in ("text", "code"):
                span += kind == "code"
                at_ = place(lit, sl, sc, el, ec, src)
                if kind == "code":
                    lit, at_ = "`" + lit + "`", [(at_ or [(sl, sc)])[0]] + at_ + [(at_ or [(sl, sc)])[-1]]
                for ch, (n, c) in zip(lit, at_):
                    if n in cov and c >= cov[n]:
                        leaf[0].append(ch)
                        leaf[1].append(((doc, n), c, span if kind == "code" else -1))
            elif kind in ("softbreak", "linebreak"):
                leaf[0].append(" ")
                leaf[1].append(((doc, sl), sc, -1))
    return out, refused


def where(line):
    """A row's line field: a findings-page line number, or README.md:<line>."""
    doc, _, n = line.rpartition(":")
    return (doc or DOC_P.name, int(n))


def main():
    global CODE
    lines = scope()
    blks, marks = blocks(lines)
    # Each token belongs to the source line of its first character: (block, start, end, text).
    toks, btok = {w: [] for w in lines}, [[] for _ in blks]
    for bi, (text, pos, _) in enumerate(blks):
        for m in TOKEN.finditer(text):
            toks[pos[m.start()][0]].append((bi, m.start(), m.end(), m.group(0)))
            btok[bi].append((m.start(), m.end(), m.group(0)))
    claimed = set()
    out, bad = [], 0
    for n, (line, shown, src, key, spec, k) in enumerate(ROWS, 1):
        status, val = "OK", ""
        _read.clear()
        try:
            w = where(line)
            assert w in toks, "line outside the covered text"
            # Round 6: a row may name the text around its figure, `before «figure» after`.
            pre, fig, post = shown.replace("\u00bb", "\u00ab").split("\u00ab") if "\u00ab" in shown else ("", shown, "")
            same_ = [t for t in toks[w] if t[3] == fig]
            hit = same_[k] if k is not None and k < len(same_) else (
                None if k is not None else next((t for t in same_ if t[:3] not in claimed), None))
            assert hit and hit[:3] not in claimed, "figure not on the line, or claimed twice"
            # Round 5: the figure is the whole number written there, not a part of a longer one.
            longer = next((x.group(0) for x in NUM.finditer(blks[hit[0]][0]) if x.start() < hit[2] and hit[1] < x.end()
                           and not (hit[1] <= x.start() and x.end() <= hit[2])), None)
            assert not longer, f"the figure is part of the longer number {longer}"
            text = blks[hit[0]][0]
            assert text[max(0, hit[1] - len(pre)):hit[1]] == pre and text[hit[2]:hit[2] + len(post)] == post, \
                "figure not in the text its row names around it"
            claimed.add(hit[:3])
            d = load(src) if src else None
            v = eval(key, dict(globals(), d=d, p=src))
            val = fmt(v, spec)
            if val != fig:
                status = "MISMATCH"
        except Cases as exc:
            status, val = "MISMATCH", str(exc)
        except Exception as exc:
            status = f"ERROR {type(exc).__name__}: {exc}"
        bad += status != "OK"
        out.append("\t".join([str(n), line, shown, src or "; ".join(_read) or "-", spec + ("" if k is None else f"#{k}"),
                              val, status]))
    # Round 5: every digit must lie in a figure a row claims, or in an identifier a category binds to its
    # keyword; a token (a number word too) the same. Anything else is UNCOVERED, named with its line.
    cov, uncovered, digits = [], [], dict(digits=0, digits_by_row=0, digits_by_category=0, digits_uncovered=0)
    refused = 0
    for bi, (text, pos, CODE) in enumerate(blks):

        def loc(i):
            return pos[i]

        tk = [(a, b, x, (bi, a, b) in claimed) for a, b, x in btok[bi]]
        nums = list(NUM.finditer(text))
        measure, in_num = [False] * len(text), [False] * len(text)
        for x in nums:
            in_num[x.start():x.end()] = [True] * (x.end() - x.start())
            if measured(text, x.start(), x.end()):
                measure[x.start():x.end()] = [True] * (x.end() - x.start())
        spans, why, no = [], {}, []
        for cat, rx, ok, code in EXCLUDE:
            for m in rx.finditer(text):
                if "|" in m.group(0) or re.search(r"[.!?]\s+\S", m.group(0)) or (ok and not ok(m, text)) or code and \
                        not (CODE[m.start()] >= 0 and all(CODE[i] == CODE[m.start()] for i in range(m.start(), m.end()))):
                    continue
                sp = [(m.start(g), m.end(g), cat) for g in rx.groupindex if g[0] == "t" and m.start(g) >= 0] or [
                    (m.start(), m.end(), cat)]
                # Round 6: what follows the identifier must be on the closed list, or it covers nothing.
                fine, after = follows(text, max(s[1] for s in sp), code)
                if not fine:
                    refused += 1
                    no += [(a, b, after) for a, b, _ in sp]
                    continue
                spans += sp
        # A digit that only refused identifiers hold is a measurement, which only a row may claim.
        for a, b, after in no:
            for i in range(a, b):
                if not any(s[0] <= i < s[1] for s in spans):
                    measure[i] = True
                    why[i] = after
        used, told = {}, set()
        in_tok = [False] * len(text)
        for a, b, x, row in tk:
            in_tok[a:b] = [True] * (b - a)
            nd = sum(1 for c in x if c.isnumeric())
            if row:
                digits["digits_by_row"] += nd
                continue
            meas = measured(text, a, b) or any(measure[a:b])
            sp = None if meas else next((s for s in spans if s[0] <= a and b <= s[1]), None)
            if sp:
                used[sp] = True
                digits["digits_by_category"] += nd
            else:
                digits["digits_uncovered"] += nd
                y = next((y for y in nums if y.start() < b and a < y.end() and not (a <= y.start() and y.end() <= b)), None)
                told.add(y.span() if y else None)
                uncovered.append((loc(y.start() if y else a), y.group(0) if y else x, meas, bool(y), text, a, b,
                                  why.get(a)))
        # every other digit: a number spelled in a way no token reads, or an identifier's digit
        for x in nums:
            free = [i for i in range(x.start(), x.end()) if text[i].isnumeric() and not in_tok[i]]
            ok_ = [i for i in free if not measure[i] and any(s[0] <= i < s[1] for s in spans)]
            for i in ok_:
                used[next(s for s in spans if s[0] <= i < s[1])] = True
            digits["digits_by_category"] += len(ok_)
            digits["digits_uncovered"] += len(free) - len(ok_)
            if len(ok_) < len(free) and x.span() not in told:
                uncovered.append((loc(x.start()), x.group(0), measure[x.start()], True, text, x.start(), x.end(),
                                  next((why[i] for i in free if i in why), None)))
        for i, c in enumerate(text):
            if c.isnumeric() and not in_tok[i] and not in_num[i]:
                digits["digits_uncovered"] += 1
                uncovered.append((loc(i), c, False, True, text, i, i + 1, None))
        for x in ZERO.finditer(text):
            if not in_tok[x.start()] and measured(text, x.start(), x.end()):
                uncovered.append((loc(x.start()), x.group(0), True, True, text, x.start(), x.end(), None))
        digits["digits"] += sum(1 for c in text if c.isnumeric())
        for a, b, cat in sorted(used):
            (doc, ln), _ = loc(a)
            cov.append("\t".join([f"{doc}:{ln}", " ".join(text[a:b].split()), cat]))
    marks.sort(key=lambda x: (x[0][0] != DOC_P.name, x[0][1]))
    with open(OUT_ROWS, "w") as f:
        f.write("# check_b16_figures.py rows, in ROWS_TSV's order: row, line, shown, receipt, precision, recomputed, status\n")
        f.write("\n".join(out) + "\n")
    with open(OUT_COV, "w") as f:
        f.write("# check_b16_figures.py coverage: line, identifier, category (every identifier that covers a digit "
                "or a token no row claims), then each UNCOVERED number, then each refused construct (MARKUP)\n")
        f.write("\n".join(cov) + "\n")
        for (w, _), text, *_ in uncovered:
            f.write(f"{w[0]}:{w[1]}\t{text}\tUNCOVERED\n")
        for w, t in marks:
            f.write(f"{w[0]}:{w[1]}\t{t}\tMARKUP\n")
    print(json.dumps(dict(lines=len(lines), tokens=sum(len(t) for t in toks.values()), rows=len(ROWS),
                          rows_ok=len(ROWS) - bad, rows_bad=bad, by_category=len(cov), **digits,
                          uncovered=len(uncovered), uncovered_measurements=sum(1 for x in uncovered if x[2]),
                          refused_identifiers=refused, markup=len(marks))))
    cap = int(OPTS.get("--show", 40))
    for x in [x for x in out if not x.endswith("\tOK")][:cap]:
        print("BAD", x)
    for (w, _), shown, meas, spelt, text, a, b, after in uncovered[:cap]:
        note = ("(a measurement: only a row can claim it)" if meas else "") + (
            " (no row can claim this spelling)" if spelt else "") + (
            f" (an identifier followed by {after!r}, not on the closed list)" if after is not None else "")
        print("UNCOVERED", f"{w[0]}:{w[1]}", shown, note.strip(), "|", " ".join(text[max(0, a - 60):b + 60].split()))
    for w, t in marks[:cap]:
        print("MARKUP", f"{w[0]}:{w[1]}", t, "(refused: a construct off the allowlist; write plain Markdown)")
    return 0 if not bad and not uncovered and not marks else 1


if __name__ == "__main__":
    sys.exit(main())
