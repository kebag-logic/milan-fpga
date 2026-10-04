#!/usr/bin/env python3
"""Lane B11 (#653, new): grade the disconnect order per cycle from the tap captures and the
probe's log. Offline; reads raw files, writes a JSON summary and Markdown tables.

usage: o653_grade.py <raw_dir> <out_dir> <session>[,<session>...]

Tap record (28 bytes before each Ethernet frame, read from the captures themselves): bytes 8..11
the port (2 = switch to DUT, 3 = DUT to switch), 12..19 a 64-bit nanosecond timestamp stored as
two little-endian 32-bit words, high word first, 20..23 the frame length. The provided
tap_order_decode.py reads bytes 12..19 as one little-endian 64-bit value (the two words swapped),
so its time column is not milliseconds, and it reads the ACMP listener, unique ID and connection
count at the wrong offsets; its line order is the file order. This grader orders by file
position and checks that the tap timestamp never decreases in file order across both ports.

Per cycle:
  * the UNBIND_RX command (switch to DUT) and response (DUT to switch) for the cycle's listener
    STREAM_INPUT;
  * the unsolicited GET_COUNTERS that reports the unlock: the first DUT-to-switch unsolicited
    GET_COUNTERS for that STREAM_INPUT whose MEDIA_UNLOCKED exceeds every value reported before
    the UNBIND_RX command in the same capture;
  * order = RESPONSE_FIRST if the response comes first in the capture, else COUNTERS_FIRST;
  * the stream frames (AVTP AAF or CRF, switch to DUT) still arriving after the command;
  * for the control cycle, the same order check against the probe's own solicited GET_COUNTERS
    response, which the probe waited for before sending the unbind: the check must read
    COUNTERS_FIRST there, so it is shown able to fail.
"""
import hashlib
import json
import struct
import subprocess
import sys
from pathlib import Path

RAW, OUT = Path(sys.argv[1]), Path(sys.argv[2])
SESSIONS = sys.argv[3].split(",")
DECODER = Path(__file__).resolve().parent.parent / "tap_order_decode.py"
DUT = "020000fffe000001"
ACMP = {6: "BIND_RX_CMD", 7: "BIND_RX_RESP", 8: "UNBIND_RX_CMD", 9: "UNBIND_RX_RESP"}
AEM = {0x29: "GET_COUNTERS", 0x0F: "GET_STREAM_INFO", 0x24: "REGISTER_UNSOL", 0x25: "DEREGISTER_UNSOL",
       0x09: "GET_STREAM_FORMAT", 0x08: "SET_STREAM_FORMAT", 0x4B: "GET_DYNAMIC_INFO"}


def records(path):
    d = path.read_bytes()
    off, i, out = 24, 0, []
    while off + 16 <= len(d):
        _, _, incl, _ = struct.unpack("<IIII", d[off:off + 16])
        p = d[off + 16:off + 16 + incl]
        off += 16 + incl
        if len(p) < 28 + 18:
            continue
        port, hi, lo = struct.unpack("<III", p[8:20])
        f = p[28:]
        et, b = f[12:14], 14
        if et == b"\x81\x00":
            et, b = f[16:18], 18
        if et != b"\x22\xf0":
            continue
        a = f[b:]
        out.append(dict(i=i, port=port, seq=i, tns=(hi << 32) | lo, a=a, src=f[6:12].hex()))
        i += 1
    return out


def classify(r):
    a = r["a"]
    sub, mt, st = a[0], a[1] & 0x0F, a[2] >> 3
    if sub == 0xFC and len(a) >= 54:
        return dict(kind="acmp", msg=ACMP.get(mt, f"ACMP_{mt}"), status=st, ctl=a[12:20].hex(), talker=a[20:28].hex(),
                    listener=a[28:36].hex(), tuid=struct.unpack(">H", a[36:38])[0],
                    luid=struct.unpack(">H", a[38:40])[0], cc=struct.unpack(">H", a[46:48])[0])
    if sub == 0xFB and len(a) >= 24:
        ct = struct.unpack(">H", a[22:24])[0]
        x = dict(kind="aecp", rsp=mt == 1, u=bool(ct >> 15), cmd=AEM.get(ct & 0x7FFF, hex(ct & 0x7FFF)), status=st,
                 target=a[4:12].hex(), ctl=a[12:20].hex(), seqid=struct.unpack(">H", a[20:22])[0])
        if ct & 0x7FFF == 0x29 and mt == 1 and len(a) >= 32 + 48:
            x["desc"] = struct.unpack(">HH", a[24:28])
            v = struct.unpack(">12I", a[32:80])
            x.update(ML=v[0], MU=v[1], SI=v[2])
        return x
    if sub in (0x02, 0x04):
        return dict(kind="stream", sub="AAF" if sub == 0x02 else "CRF")
    return dict(kind="other", sub=sub)


def grade_capture(path, listener, control_ctl=None):
    recs = records(path)
    tns_order_ok = all(b["tns"] >= a["tns"] for a, b in zip(recs, recs[1:]))
    for r in recs:
        r.update(classify(r))
    ctl = [r for r in recs if r["kind"] in ("acmp", "aecp")]
    cmd = next((r for r in ctl if r["kind"] == "acmp" and r["msg"] == "UNBIND_RX_CMD" and r["port"] == 2
                and r["listener"] == DUT and r["luid"] == listener), None)
    rsp = next((r for r in ctl if r["kind"] == "acmp" and r["msg"] == "UNBIND_RX_RESP" and r["port"] == 3
                and r["listener"] == DUT and r["luid"] == listener and (cmd is None or r["seq"] > cmd["seq"])), None)
    pushes = [r for r in ctl if r["kind"] == "aecp" and r["rsp"] and r["u"] and r["cmd"] == "GET_COUNTERS" and r["port"] == 3
              and r.get("desc") == (0x0005, listener)]
    g = dict(capture=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest(), bytes=path.stat().st_size,
             records_avtp=len(recs), control_frames=len(ctl), tap_time_monotonic_in_file_order=tns_order_ok, unbind_cmd=cmd is not None, unbind_rsp=rsp is not None)
    if not (cmd and rsp):
        g["order"] = "NO_UNBIND"
        return g
    g["unbind_status"] = rsp["status"]
    g["cmd_to_rsp_us"] = round((rsp["tns"] - cmd["tns"]) / 1e3, 1)
    mu_before = max([p["MU"] for p in pushes if p["seq"] < cmd["seq"]], default=0)
    unlock = next((p for p in pushes if p["MU"] > mu_before), None)
    g["pushes_before_cmd"] = [dict(ML=p["ML"], MU=p["MU"], SI=p["SI"]) for p in pushes if p["seq"] < cmd["seq"]]
    if unlock is None:
        g["order"] = "NO_UNLOCK_PUSH"
    else:
        g["order"] = "RESPONSE_FIRST" if rsp["seq"] < unlock["seq"] else "COUNTERS_FIRST"
        g["unlock_push"] = dict(ML=unlock["ML"], MU=unlock["MU"], SI=unlock["SI"], ctl=unlock["ctl"][-4:])
        g["rsp_to_push_us"] = round((unlock["tns"] - rsp["tns"]) / 1e3, 1)
        g["frames_between"] = [f'{"DUT->sw" if r["port"] == 3 else "sw->DUT"} {r.get("msg") or ("UNSOL " if r.get("u") else "") + r["cmd"] + (" RSP" if r.get("rsp") else " CMD")}'
                               for r in ctl if rsp["seq"] < r["seq"] < unlock["seq"]]
    stream = [r for r in recs if r["kind"] == "stream" and r["port"] == 2]
    after_cmd = [r for r in stream if r["seq"] > cmd["seq"]]
    after_rsp = [r for r in stream if r["seq"] > rsp["seq"]]
    before = [r for r in stream if r["seq"] < cmd["seq"]]
    g["stream_sub"] = stream[0]["sub"] if stream else None
    g["stream_frames_before_cmd"] = len(before)
    g["stream_frames_after_cmd"] = len(after_cmd)
    g["stream_frames_after_rsp"] = len(after_rsp)
    g["last_stream_frame_after_cmd_ms"] = round((after_cmd[-1]["tns"] - cmd["tns"]) / 1e6, 3) if after_cmd else None
    g["talker_streaming_at_cmd"] = bool(before) and bool(after_cmd)
    if control_ctl:
        own = next((r for r in ctl if r["kind"] == "aecp" and r["rsp"] and not r["u"] and r["cmd"] == "GET_COUNTERS"
                    and r["port"] == 3 and r["ctl"] == control_ctl and r.get("desc") == (0x0005, listener)), None)
        if own:
            g["control"] = dict(own_counters=dict(ML=own["ML"], MU=own["MU"], SI=own["SI"]),
                                order_vs_own="RESPONSE_FIRST" if rsp["seq"] < own["seq"] else "COUNTERS_FIRST",
                                own_rsp_to_cmd_us=round((cmd["tns"] - own["tns"]) / 1e3, 1))
        else:
            g["control"] = dict(order_vs_own="NO_OWN_GET_COUNTERS")
    # the provided decoder, unchanged, on the same capture: its line order
    dec = subprocess.run([sys.executable, "-B", str(DECODER), str(path)], capture_output=True, text=True, timeout=300)
    lines = dec.stdout.splitlines()
    (OUT / "decode").mkdir(parents=True, exist_ok=True)
    (OUT / "decode" / (path.stem + ".decode.txt")).write_text(dec.stdout)
    i_rsp = next((k for k, ln in enumerate(lines) if "ACMP UNBIND_RX_RESP" in ln), None)
    i_push = next((k for k, ln in enumerate(lines) if "UNSOL GET_COUNTERS" in ln and f"desc=0x5/{listener}" in ln
                   and "MUNLOCK=" in ln and
                   int(ln.split("MUNLOCK=")[1].split()[0]) > mu_before), None)
    g["decoder_rc"] = dec.returncode
    g["decoder_lines"] = len(lines)
    g["decoder_order"] = ("NO_LINES" if i_rsp is None or i_push is None else
                          "RESPONSE_FIRST" if i_rsp < i_push else "COUNTERS_FIRST")
    return g


def library_view(session):
    ev = [json.loads(ln) for ln in (RAW / f"{session}-probe.jsonl").read_text().splitlines() if ln.startswith("{")]
    cyc, cur = {}, None
    for e in ev:
        if e["ev"] == "cycle_begin":
            cur = e["tag"]
            cyc[cur] = dict(listener=e["listener_in"], control=e["control"], hold_ms=e["hold_ms"], updates=[])
        if cur is None:
            continue
        c = cyc[cur]
        if e["ev"] == "formats":
            c["formats"] = dict(talker=e["talker_format"], listener=e["listener_format"], equal=e["equal"])
        elif e["ev"] == "set_listener_format":
            c["set_listener_format"] = e["status"]
        elif e["ev"] == "bind":
            c["bind"], c["t_bind"] = e["status"], e["t_cmd"]
        elif e["ev"] == "lock_wait":
            c["locked"], c["lock_ms"] = e["locked"], e["ms"]
        elif e["ev"] == "unbind":
            c["unbind"], c["t_unbind"] = e["status"], e["t_cmd"]
        elif e["ev"] == "si_connection" and e["who"] == "dut" and e["state"] == "NotConnected":
            c["t_lib_notconnected"] = e["t"]
        elif e["ev"] == "si_counters" and e["who"] == "dut":
            c["updates"].append(dict(t=e["t"], **{k: e["counters"].get(k) for k in ("ML", "MU", "SI")},
                                     lib_conn=e["lib_conn"], compat=e["compat_names"], n_events=e["n_events"]))
        elif e["ev"] in ("compat_changed", "diagnostics", "query_error", "unsol_loss", "aecp_timeout", "aecp_unexpected",
                         "transport_error", "offline", "unsol_registration"):
            c.setdefault("library_flags", []).append(e)
        elif e["ev"] == "snapshot" and e["tag"].endswith("-post"):
            d = e["dut"]
            c["post"] = dict(counters={k: d["lib_counters"][k] for k in ("ML", "MU", "SI")}, conn=d["lib_conn"],
                             compat=d["compat_names"], events_new=d["events_new"], diag=d["diag"],
                             peer_compat=e["peer"]["compat_names"], peer_events_new=e["peer"]["events_new"])
        elif e["ev"] == "cycle_end":
            c["result"] = e["result"]
    for tag, c in cyc.items():
        tu = c.get("t_unbind")
        unl = next((u for u in c["updates"] if tu and u["t"] > tu and u["MU"] is not None and u["ML"] is not None
                    and u["MU"] >= 1 and u["ML"] == u["MU"]), None)
        c["lib_unlock_update"] = unl
        if unl and c.get("t_lib_notconnected"):
            c["lib_order"] = "RESPONSE_FIRST" if c["t_lib_notconnected"] < unl["t"] else "COUNTERS_FIRST"
            c["lib_unlock_after_unbind_ms"] = round((unl["t"] - tu) / 1e3, 3)
        held = [u for u in c["updates"] if tu and u["t"] < (unl["t"] if unl else 1e30) and u["ML"] == 1 and u["MU"] == 0]
        c["lib_held_1_0_after_unbind_ms"] = (round((unl["t"] - max(tu, c.get("t_lib_notconnected", tu))) / 1e3, 3)
                                             if unl and held else None)
        flags = c.get("library_flags", [])
        c["library_flagged"] = bool(flags) or bool(c.get("post", {}).get("events_new")) or bool(c.get("post", {}).get("peer_events_new"))
    tail = dict(session_events=[e for e in ev if e["ev"] in ("start", "entities", "online", "both_online", "deregister",
                                                              "dereg_entity", "exit", "session_destroyed")])
    return cyc, tail


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    allc, rows = {}, []
    for s in SESSIONS:
        lib, tail = library_view(s)
        aux = next((e for e in tail["session_events"] if e["ev"] == "entities"), {}).get("aux_eid")
        for tag, c in lib.items():
            cap = RAW / f"b11-a535-{s}-{tag}.pcap"
            g = grade_capture(cap, c["listener"], aux if c["control"] else None) if cap.exists() else dict(order="NO_CAPTURE")
            allc[f"{s}/{tag}"] = dict(session=s, tag=tag, library=c, wire=g)
        allc[f"{s}/_session"] = tail
    (OUT / "o653-grade.json").write_text(json.dumps(allc, indent=1, default=str) + "\n")
    hdr = ("| Cycle | Input | Bind | Lock (ms) | Hold (ms) | UNBIND_RX cmd to rsp (us) | Rsp to unlock push (us) | Wire order | "
           "Decoder order | Pushed ML/MU/SI | Stream frames after cmd | Library: conn at unlock update | Library flags | "
           "Library pair after |")
    lines = [hdr, "|" + "|".join(["---"] * (hdr.count("|") - 1)) + "|"]
    for k, v in allc.items():
        if k.endswith("/_session"):
            continue
        c, g = v["library"], v["wire"]
        up = g.get("unlock_push", {})
        lu = c.get("lib_unlock_update") or {}
        post = c.get("post", {}).get("counters", {})
        lines.append(f"| {k} | {c['listener']} | {c.get('bind')} | {c.get('lock_ms')} | {c['hold_ms']} | {g.get('cmd_to_rsp_us')} | "
                     f"{g.get('rsp_to_push_us')} | {g.get('order')} | {g.get('decoder_order')} | "
                     f"{up.get('ML')}/{up.get('MU')}/{up.get('SI')} | {g.get('stream_frames_after_cmd')} | "
                     f"{lu.get('lib_conn')} | {'yes' if c.get('library_flagged') else 'none'} | "
                     f"{post.get('ML')}/{post.get('MU')}/{post.get('SI')} |")
        if "control" in g:
            lines.append(f"| {k} control | {c['listener']} | own GET_COUNTERS {g['control'].get('own_counters')} | | | | | "
                         f"{g['control']['order_vs_own']} (vs own response) | | | | | | |")
    (OUT / "o653-table.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
