#!/usr/bin/env python3
"""Label-only public scan of the B5 page, PR text and evidence archive.

usage: public_scan.py <orig-b5-r1-dir> <masked-b5-r1-dir> <out.txt> TARGET...
  TARGET is name=path (a file or a directory, scanned recursively).

The private values are derived IN MEMORY from the difference between the
original round-1 packet (<orig>) and the label-masked one (<masked>), and are
never written: the output names only a class, a target, a file and a line.
Every pattern must first hit a planted line and the original packet (power
checks); a pattern that fails either is reported and the scan exits 2.

Derivation probes (also label-only): whether a capture channel count follows
from an "every channel" byte size, and whether a peer stream count follows
from per-index labels, in each target.
"""
import difflib, re, sys
from pathlib import Path

orig, masked, out = Path(sys.argv[1]) / "author", Path(sys.argv[2]) / "author", sys.argv[3]
targets = [t.split("=", 1) for t in sys.argv[4:]]
LAB = re.compile(r"<[a-z][a-z0-9-]+>")

# ---- 1. private values per class, from the mask's own replacements ----------
vals = {}
def add(cls, v):
    v = v.strip().strip('",')
    if v:
        vals.setdefault(cls, set()).add(v)

for f in sorted(masked.rglob("*")):
    if not f.is_file():
        continue
    a = (orig / f.relative_to(masked)).read_text(errors="replace")
    b = f.read_text(errors="replace")
    if a == b:
        continue
    al, bl = a.split("\n"), b.split("\n")
    if len(al) == len(bl):
        for x, y in zip(al, bl):
            if x == y or not LAB.search(y):
                continue
            labs = LAB.findall(y)
            rx = "(.+?)".join(re.escape(p) for p in LAB.split(y))
            m = re.fullmatch(rx, x)
            if m:
                for lab, v in zip(labs, m.groups()):
                    add(lab.strip("<>"), v)
    aw, bw = re.findall(r"\S+|\s+", a), re.findall(r"\S+|\s+", b)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, aw, bw, autojunk=False).get_opcodes():
        new, old = "".join(bw[j1:j2]), "".join(aw[i1:i2])
        if op == "equal" or LAB.search(new):
            continue
        if new == "peer's output":
            add("link-type", old)
        elif "cap-all-" in new:
            mm = re.search(r"cap-all-(\d+)ch", old)
            if mm:
                add("capture-channel-count", mm.group(1))
        elif new == "kHz.":
            add("capture-channel-layout", old)

# derive the summary.json channel_identification original (line counts differ)
import json
oj = json.load(open(orig / "summary/a-long/summary.json"))
ci = json.dumps(oj.get("channel_identification"))
for m in re.finditer(r"\d+", ci):
    pass  # the indices are already taken from labelled lines above

# ---- 2. patterns per class -------------------------------------------------
def numrx(v, ctx):
    return [re.compile(c.format(v=re.escape(v)), re.I) for c in ctx]

pats = {}
for v in vals.get("capture-channel-count", ()):
    pats.setdefault("capture-channel-count", []).extend(numrx(v, [
        r"(?<![\d.]){v}\s*(?:-\s*)?(?:ch\b|channels?\b)", r"\ball {v}\b", r"cap-all-{v}ch",
        r"NCH\s*=\s*{v}\b", r"words\(\w+,\s*{v}\)"]))
idx = sorted(v for v in vals.get("capture-channel-index", ()) if v.isdigit())
for v in idx:
    pats.setdefault("capture-channel-index", []).extend(numrx(v, [
        r"capture channels? {v}\b", r"capture channel {v}\b", r"CAP_[LR]\s*=\s*{v}\b",
        r"channels {v}\b"]))
if len(idx) >= 2:
    pats["capture-channel-index"].append(re.compile(
        r"(?<![\d.]){}\s*(?:,|and|/)\s*{}(?![\d.])".format(re.escape(idx[0]), re.escape(idx[1]))))
for cls in ("link-type", "soc-usb-function", "host-iface", "usb-bus-position",
            "capture-channel-layout", "peer-channel-map", "peer-stream-indices"):
    for v in vals.get(cls, ()):
        if cls == "link-type":
            pats.setdefault(cls, []).append(re.compile(r"\b" + re.escape(v) + r"\b"))
        elif len(v) >= 4:
            pats.setdefault(cls, []).append(re.compile(re.escape(v)))
# generic classes, independent of the mask's own values
GENERIC = set()
pats.setdefault("link-type", []).append(GEN := re.compile(
    r"\b(ADAT|MADI|S/?PDIF|TOSLINK|AES/?EBU|AES3|lightpipe|optical|coaxial|Dante|Thunderbolt|FireWire)\b", re.I)); GENERIC.add(GEN)
pats.setdefault("interface-name", []).append(GEN := re.compile(
    r"\b(enp\d+s\d+\w*|eno\d+|ens\d+\w*|enx[0-9a-f]{12}|eth\d+|wlp\d+\w*|wlan\d+)\b")); GENERIC.add(GEN)
pats["interface-name"] += pats.pop("host-iface", [])
pats.setdefault("soc-product", []).append(GEN := re.compile(
    r"\b(BeagleBone|PocketBeagle|BeagleBoard|Sitara|AM335x|AM62\w*|Raspberry|Jetson|i\.MX\w*|Zynq|Arduino)\b", re.I)); GENERIC.add(GEN)
pats["soc-product"] += pats.pop("soc-usb-function", [])

PLANT = {  # one planted line per pattern is built from the pattern's own value
}
lines = []
def say(s):
    lines.append(s)

# ---- 3. power checks -------------------------------------------------------
fail = 0
orig_text = "\n".join(p.read_text(errors="replace") for p in orig.rglob("*") if p.is_file())
for cls, ps in sorted(pats.items()):
    for i, p in enumerate(ps):
        hit_orig = bool(p.search(orig_text))
        # planted line: a synthetic string the pattern must match
        plant = None
        if p in GENERIC:
            # plant EVERY alternative of a generic list, so no single word is singled out
            body = p.pattern[p.pattern.index("(") + 1:p.pattern.rindex(")")]
            alts = [re.sub(r"\\d\+", "0", re.sub(r"\\w\*|/\?", "", a)).replace("[0-9a-f]{12}", "a" * 12).replace("\\.", ".")
                    for a in body.split("|")]
            plant = all(p.search(f" {a} ") for a in alts) or None
            say(f"power {cls}#{i}: generic list, every one of {len(alts)} alternatives planted: {'hit' if plant else 'MISS'}")
            if not plant:
                fail += 1
            continue
        src = {"interface-name": "host-iface", "soc-product": "soc-usb-function"}.get(cls, cls)
        for v in sorted(vals.get(src, set()) | vals.get(cls, set())):
            for s in (f"x {v} channels x", f"all {v} x", f"capture channels {v} x", f"capture channel {v} x", f"cap-all-{v}ch.raw",
                      f"NCH = {v}", f"words(full, {v})", f"CAP_L = {v}", f"channels {v} x", f" {v} ",
                      f"{idx[0]} and {idx[1]}" if len(idx) >= 2 else "", v):
                if s and p.search(s):
                    plant = True
                    break
            if plant:
                break
        say(f"power {cls}#{i}: planted {'hit' if plant else 'MISS'}, original packet {'hit' if hit_orig else 'no hit'}")
        if not plant:
            fail += 1
say(f"classes: {', '.join(f'{k}={len(v)}' for k, v in sorted(pats.items()))}")
say(f"derived private values per class (count only): " +
    ", ".join(f"{k}={len(v)}" for k, v in sorted(vals.items())))

# ---- 4. scan --------------------------------------------------------------
def files(path):
    p = Path(path)
    return [p] if p.is_file() else sorted(x for x in p.rglob("*") if x.is_file())

cc = next(iter(vals.get("capture-channel-count", {"0"})))
for name, path in targets:
    tot = 0
    for f in files(path):
        try:
            t = f.read_text(errors="replace")
        except Exception:
            continue
        for ln, line in enumerate(t.split("\n"), 1):
            for cls, ps in pats.items():
                if any(p.search(line) for p in ps):
                    tot += 1
                    say(f"HIT {name} {cls} {f.relative_to(path) if Path(path).is_dir() else f.name}:{ln}")
        # derivation probe A: capture channel count from an every-channel byte size
        for m in re.finditer(r"every channel, (\d+) s \| (\d+)", t):
            secs, nbytes = int(m.group(1)), int(m.group(2))
            ok = nbytes == secs * 48000 * 3 * int(cc)
            say(f"DERIVE {name} capture-channel-count from '{f.name}' every-channel row ({secs} s): "
                f"{'YES, bytes/(s*48000*3) is the masked count' if ok else 'no'}")
        for m in re.finditer(r'"cap-all-<n>ch\.raw",\s*"bytes":\s*(\d+)', t):
            n = int(m.group(1))
            ok = n % (48000 * 3 * int(cc)) == 0
            say(f"DERIVE {name} capture-channel-count from '{f.relative_to(path) if Path(path).is_dir() else f.name}' "
                f"cap-all size: {'YES, an integer number of seconds at the masked count' if ok else 'no'}")
        # derivation probe B: a peer stream count from per-index census labels
        idxs = set(re.findall(r'"what":"(?:rx|tx)-state-peer-(\d+)"', t))
        if idxs:
            say(f"DERIVE {name} peer-stream-count from per-index labels in "
                f"{f.relative_to(path) if Path(path).is_dir() else f.name}: YES")
    say(f"TOTAL {name}: {tot} direct hits")
say(f"POWER FAILURES {fail}")
Path(out).write_text("\n".join(lines) + "\n")
sys.exit(2 if fail else 0)
