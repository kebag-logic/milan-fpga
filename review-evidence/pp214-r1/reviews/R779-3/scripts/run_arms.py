#!/usr/bin/env python3
"""Disposable probe driver: build tb/srp_encoder on a private copy per arm.

usage: run_arms.py CLONE SCRATCH OUT.tsv JOBS [name-prefix ...]
Reads the clone, writes only under SCRATCH. Every arm is one or more exact text
edits that must match exactly once, so a drifted arm stops the run. The verdict
comes from the simulator's own tally and FAIL lines. VERILATOR names the tool.
"""
import collections, concurrent.futures as cf, os, re, shutil, subprocess, sys
from pathlib import Path

ENC = "hdl/srp/KL_srp_encoder.sv"
TB = "tb/srp_encoder/sim_main.cpp"
BUSY = "assign busy_app_w  = (st_r != E_IDLE) && (st_r != E_COLLECT)\n"
KEYM = "return {APP_MSRP_C, t, v[271:208]};"
KEYV = "return {APP_MVRP_C, ATTR_MVRP_VID_C, v[271:256], 48'd0};"
STATES = ["E_ALLOC", "E_HDR", "E_RD", "E_CAP", "E_BOUND", "E_MSGHDR", "E_VHDR", "E_VFV", "E_V3PK",
          "E_V4PK", "E_MSGCLOSE", "E_PATCH", "E_PDUEND", "E_COMMIT", "E_TXREQ"]
GUARD = "std::vector<uint8_t> got = std::vector<uint8_t>(kMaxFrameBytes);"
NOALLOC = ("st_r   <= preparing_r ? E_COLLECT : E_HDR;", "st_r   <= E_ALLOC;")


def arms():
    out = {"HEAD": [], "BASE-ENCODER": []}
    for s in STATES:
        out[f"busy-open-{s}"] = [(ENC, BUSY, BUSY.rstrip("\n") + f" && (st_r != {s})\n")]
    for n in range(64):
        out[f"key-streamid-bit{n:02d}"] = [(ENC, KEYM, f"return {{APP_MSRP_C, t, v[271:208] & ~(64'd1 << {n})}};")]
    for n in range(16):
        out[f"key-vid-bit{n:02d}"] = [(ENC, KEYV, f"return {{APP_MVRP_C, ATTR_MVRP_VID_C, v[271:256] & ~(16'd1 << {n}), 48'd0}};")]
    m = "if (push_msrp_w && !sr_hit_w) cnt_msrp_r <= cnt_msrp_r + CNT_W_C'(1);"
    v = "if (push_mvrp_w && !sr_hit_w) cnt_mvrp_r <= cnt_mvrp_r + CNT_W_C'(1);"
    out["hit-counts-msrp"] = [(ENC, m, m.replace(" && !sr_hit_w", ""))]
    out["hit-counts-mvrp"] = [(ENC, v, v.replace(" && !sr_hit_w", ""))]
    wm = "assign msrp_waddr_w = sr_hit_w ? sr_idx_r : cnt_msrp_r[IDX_W_C-1:0];"
    wv = "assign mvrp_waddr_w = sr_hit_w ? sr_idx_r : cnt_mvrp_r[IDX_W_C-1:0];"
    out["hit-appends-msrp"] = [(ENC, wm, "assign msrp_waddr_w = cnt_msrp_r[IDX_W_C-1:0];"), (ENC, m, m.replace(" && !sr_hit_w", ""))]
    out["hit-appends-mvrp"] = [(ENC, wv, "assign mvrp_waddr_w = cnt_mvrp_r[IDX_W_C-1:0];"), (ENC, v, v.replace(" && !sr_hit_w", ""))]
    out["start-laprepare-term-gone"] = [(ENC, "|| ((st_r == E_IDLE) && la_prepare_i)) : start1_w;", ") : start1_w;")]
    out["guard-removed"] = [(TB, GUARD, "std::vector<uint8_t> got;")]
    out["noframe-guard-on"] = [(ENC, *NOALLOC)]
    out["noframe-guard-off"] = [(ENC, *NOALLOC), (TB, GUARD, "std::vector<uint8_t> got;")]
    rdy = "assign ev_ready_o  = base_ok_w\n"
    for st in STATES[1:]:
        out[f"take-on-{st}"] = [(ENC, rdy, f"assign ev_ready_o  = ((st_r == {st}) && (cur_app_r == ev_app_i)) || base_ok_w\n")]
    for a, b in (("E_RD", "E_CAP"), ("E_CAP", "E_BOUND"), ("E_BOUND", "E_MSGHDR"), ("E_V3PK", "E_MSGCLOSE"), ("E_PDUEND", "E_COMMIT")):
        out[f"pair-open-{a}-{b}"] = [(ENC, BUSY, BUSY.rstrip("\n") + f" && (st_r != {a}) && (st_r != {b})\n")]
    for lab in ("push-on-prepared-start", "push-taken-in-alloc", "second-queueing"):
        out[f"OLD-{lab}"] = [("@patch", lab, "")]
    out["OLD-HEAD"] = []
    out["OLD-hit-counts-msrp"] = out["hit-counts-msrp"]
    out["OLD-hit-counts-mvrp"] = out["hit-counts-mvrp"]
    out["OLD-hit-appends-msrp"] = out["hit-appends-msrp"]
    out["OLD-hit-appends-mvrp"] = out["hit-appends-mvrp"]
    two = [(TB, 'CHECK(h.push_enc(pending), "%s: a value pending", row);\n  h.drop_on_accept = true;',
            'CHECK(h.push_enc(pending), "%s: a value pending", row);\n  Ev extra = pending;\n  extra.val[app ? 1 : 3] = 0x09;\n'
            '  CHECK(h.push_enc(extra), "%s: a second value pending", row);\n  h.drop_on_accept = true;'),
           (TB, "model_pdu({pending}, prepared, OWN_MAC));", "model_pdu({pending, extra}, prepared, OWN_MAC));")]
    out["two-entry-HEAD"] = list(two)
    for st in ("E_RD", "E_CAP", "E_BOUND", "E_V3PK", "E_COMMIT"):
        out[f"two-entry-busy-open-{st}"] = two + [(ENC, BUSY, BUSY.rstrip("\n") + f" && (st_r != {st})\n")]
    return out


def one(job):
    name, edits, clone, scratch, base = job
    tree = Path(scratch) / "arms" / name
    shutil.rmtree(tree, ignore_errors=True)
    tree.mkdir(parents=True)
    shutil.copytree(Path(clone) / "hdl", tree / "hdl")
    (tree / "tb").mkdir()
    shutil.copytree(Path(clone) / "tb/common", tree / "tb/common")
    shutil.copytree(Path(clone) / "tb/srp_encoder", tree / "tb/srp_encoder", ignore=shutil.ignore_patterns("obj_dir"))
    if name == "BASE-ENCODER":
        (tree / ENC).write_bytes(subprocess.run(["git", "-C", clone, "show", "a9e84b66:" + ENC],
                                                stdout=subprocess.PIPE, check=True).stdout)
    if name.startswith("OLD-"):
        (tree / TB).write_bytes(subprocess.run(["git", "-C", clone, "show", "1c8b485f:" + TB],
                                               stdout=subprocess.PIPE, check=True).stdout)
    for rel, old, new in edits:
        if rel == "@patch":
            subprocess.run(["patch", "-p1", "-s", "-i", str(Path(clone) / "tb/srp_top/mutations" / (old + ".patch"))],
                           cwd=tree, check=True)
            continue
        p = tree / rel
        s = p.read_text()
        if s.count(old) != 1:
            return name, "DRIFT", rel, "", ""
        p.write_text(s.replace(old, new))
    r = subprocess.run(["timeout", "420", "make", "-C", str(tree / "tb/srp_encoder"), "run",
                        "VERILATOR=" + os.environ["VERILATOR"]], stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True, errors="replace", check=False)
    (tree / "receipt.log").write_text(r.stdout)
    fails = [l for l in r.stdout.splitlines() if l.startswith("FAIL:")]
    tags = collections.Counter(re.split(r"[ :]", l[5:].strip(), maxsplit=1)[0] for l in fails)
    tally = next((l for l in reversed(r.stdout.splitlines()) if re.search(r"\d+ checks:", l)), "NO TALLY")
    shutil.rmtree(tree / "tb/srp_encoder/obj_dir", ignore_errors=True)
    shutil.rmtree(tree / "hdl", ignore_errors=True)
    return name, f"rc={r.returncode}", tally, " ".join(f"{k}({v})" for k, v in sorted(tags.items())), fails[0][:100] if fails else ""


def main():
    clone, scratch, out, jobs = sys.argv[1:5]
    prefixes = sys.argv[5:]
    table = arms()
    names = [n for n in table if not prefixes or any(n.startswith(p) for p in prefixes)]
    with cf.ThreadPoolExecutor(int(jobs)) as pool:
        rows = list(pool.map(one, [(n, table[n], clone, scratch, None) for n in names]))
    with open(out, "w") as f:
        for row in rows:
            f.write("\t".join(row) + "\n")
    print(len(rows), "arms")


if __name__ == "__main__":
    main()
