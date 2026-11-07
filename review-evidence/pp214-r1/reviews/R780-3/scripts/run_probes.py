#!/usr/bin/env python3
"""Disposable fault probes for tb/srp_encoder at a given clone.

usage: run_probes.py CLONE PACKET GROUP[,GROUP] [--jobs N]

Each probe exports hdl/ and tb/ from named commits into PACKET/scratch/p/<name>,
applies exact-string edits there, builds with $VERILATOR and keeps the raw log in
PACKET/receipts/probes/<name>.log. The clone is never written.
"""
import argparse
import collections
import concurrent.futures
import os
import re
import shutil
import subprocess
from pathlib import Path

HEAD = "7feeccea3a6c8210ece8d5d1d8929d67582163f9"
PREV = "1c8b485f"
BASE = "a9e84b66"
ENC = "hdl/srp/KL_srp_encoder.sv"
SIM = "tb/srp_encoder/sim_main.cpp"
WRAP = "tb/srp_encoder/srp_tb_wrap.sv"

MSRP_KEY = "return {APP_MSRP_C, t, v[271:208]};"
VID_KEY = "v[271:256], 48'd0}"
BUSY = "assign busy_app_w  = (st_r != E_IDLE) && (st_r != E_COLLECT)\n"
HIT_MSRP = "if (push_msrp_w && !sr_hit_w) cnt_msrp_r"
HIT_MVRP = "if (push_mvrp_w && !sr_hit_w) cnt_mvrp_r"
READY = "&& (!valid_type_w || (tgt_cnt_w == '0) || sr_hit_w || sr_last_w);"
GUARD = "std::vector<uint8_t> got = std::vector<uint8_t>(kMaxFrameBytes);"

STALL_ROW = r'''
void SrpSuite::probe_stall(bool tick_in_alloc) {
  bring_out_of_reset();
  d->enc_la_cancel_i = 1;
  d->enc_la_prepare_i = 1;
  h.tick();
  if (tick_in_alloc) d->enc_join_tick_i = 1;
  for (int i = 0; i < 50; ++i) {
    h.tick();
    d->enc_join_tick_i = 0;
    if (h.last_prepare_done) break;
  }
  d->enc_join_tick_i = 0;
  d->enc_la_prepare_i = 0;
  d->enc_la_cancel_i = 0;
  const Ev dom = mk_ev(0, 4, 1, 0, {0x06, 0x03, 0x00, 0x02});
  const Ev vid = mk_ev(1, 1, 1, 0, {0x00, 0x02});
  const bool msrp_taken = h.push_enc(dom, 200000);
  const bool mvrp_taken = h.push_enc(vid, 2000);
  d->enc_join_tick_i = 2;
  h.tick();
  d->enc_join_tick_i = 0;
  const bool mvrp_sent = h.wait_and_drain(got, 20000);
  printf("PROBE tick_in_alloc=%d msrp_push_taken=%d mvrp_push_taken=%d mvrp_frame_sent=%d\n",
         int(tick_in_alloc), int(msrp_taken), int(mvrp_taken), int(mvrp_sent));
  d->enc_la_prepare_i = 1;
  for (int i = 0; i < 50; ++i) { h.tick(); if (h.last_prepare_done) break; }
  d->enc_la_prepare_i = 0;
  const bool after = h.push_enc(dom, 2000);
  printf("PROBE tick_in_alloc=%d after_next_prepare_msrp_push_taken=%d\n",
         int(tick_in_alloc), int(after));
}
'''


def stall_edits():
    return [
        (WRAP, "input  wire          enc_la_prepare_i,",
         "input  wire          enc_la_prepare_i,\n    input  wire          enc_la_cancel_i,"),
        (WRAP, ".la_cancel_i (1'b0),", ".la_cancel_i (enc_la_cancel_i),"),
        (SIM, "  void keep_every_vid_bit_in_the_identity();",
         "  void keep_every_vid_bit_in_the_identity();\n  void probe_stall(bool tick_in_alloc);"),
        (SIM, "int SrpSuite::run() {\n", STALL_ROW + "\nint SrpSuite::run() {\n"),
        (SIM, "  hold_a_push_off_its_drain_start();\n",
         "  hold_a_push_off_its_drain_start();\n  probe_stall(false);\n  probe_stall(true);\n"),
    ]


def repo_patch(clone, label):
    return ("patch", str(Path(clone) / "tb/srp_top/mutations" / (label + ".patch")))


def probes(clone):
    out = collections.OrderedDict()
    out["control-head"] = dict(group="core", edits=[])
    # the bit walk: mask one identity bit at a time
    for bit in range(64):
        out[f"key-msrp-b{bit:02d}"] = dict(group="walk", edits=[
            (ENC, MSRP_KEY, f"return {{APP_MSRP_C, t, v[271:208] & ~(64'd1 << {bit})}};")])
    for bit in range(16):
        out[f"key-vid-b{bit:02d}"] = dict(group="walk", edits=[
            (ENC, VID_KEY, f"(v[271:256] & ~(16'd1 << {bit})), 48'd0}}")])
    # the merge-count arms that left PV20
    hit_m = [(ENC, HIT_MSRP, "if (push_msrp_w) cnt_msrp_r")]
    hit_v = [(ENC, HIT_MVRP, "if (push_mvrp_w) cnt_mvrp_r")]
    out["hit-counts-msrp"] = dict(group="core", edits=hit_m)
    out["hit-counts-mvrp"] = dict(group="core", edits=hit_v)
    # the sized frame
    empty = [(ENC, READY, "&& (!valid_type_w || sr_hit_w || sr_last_w);")]
    unsized = [(SIM, GUARD, "std::vector<uint8_t> got;")]
    out["empty-table-searches"] = dict(group="core", edits=empty)
    out["unsized-head"] = dict(group="core", edits=unsized)
    out["unsized-empty-table-searches"] = dict(group="core", edits=empty + unsized)
    # the same arms against the previously reviewed suite
    out["prev-control"] = dict(group="core", tb=PREV, edits=[])
    for label in ("push-on-prepared-start", "push-taken-in-alloc", "second-queueing"):
        out["prev-" + label] = dict(group="core", tb=PREV, edits=[repo_patch(clone, label)])
    out["prev-hit-counts-msrp"] = dict(group="core", tb=PREV, edits=hit_m)
    out["prev-hit-counts-mvrp"] = dict(group="core", tb=PREV, edits=hit_v)
    # the suite at this head against the base RTL
    out["base-rtl"] = dict(group="core", hdl=BASE, edits=[])
    # a push taken on each stretch of the drain
    states = ["E_HDR", "E_RD", "E_CAP", "E_BOUND", "E_MSGHDR", "E_VHDR", "E_VFV", "E_V3PK",
              "E_MSGCLOSE", "E_PATCH", "E_PDUEND", "E_COMMIT", "E_TXREQ"]
    for state in states:
        out["busy-off-" + state] = dict(group="drain", edits=[
            (ENC, BUSY, BUSY.rstrip("\n") + f" && (st_r != {state})\n")])
    out["busy-off-whole-drain"] = dict(group="drain", edits=[
        (ENC, BUSY, "assign busy_app_w  = 1'b0 && (st_r != E_IDLE) && (st_r != E_COLLECT)\n")])
    # the canceled empty round with a tick latched in E_ALLOC
    out["stall-head"] = dict(group="stall", edits=stall_edits())
    out["stall-base"] = dict(group="stall", hdl=BASE, edits=stall_edits())
    return out


def export(clone, ref, paths, dest):
    tar = subprocess.Popen(["git", "-C", clone, "archive", ref, *paths], stdout=subprocess.PIPE)
    subprocess.run(["tar", "-x", "-C", str(dest)], stdin=tar.stdout, check=True)
    if tar.wait() != 0:
        raise RuntimeError("git archive failed")


def tally(text):
    found = re.findall(r"^\d+ checks: \d+ PASS, \d+ FAIL$", text, re.M)
    return found[-1] if found else "NO TALLY"


def rows(text):
    count = collections.Counter()
    for line in text.splitlines():
        if line.startswith("FAIL: "):
            count[re.split(r"[ :]", line[6:], maxsplit=1)[0]] += 1
    return " ".join(f"{k}({v})" for k, v in sorted(count.items()))


def run(item):
    name, spec, clone, packet = item
    tree = packet / "scratch" / "p" / name
    shutil.rmtree(tree, ignore_errors=True)
    tree.mkdir(parents=True)
    export(clone, spec.get("hdl", HEAD), ["hdl"], tree)
    export(clone, spec.get("tb", HEAD), ["tb/srp_encoder", "tb/common"], tree)
    for edit in spec["edits"]:
        if edit[0] == "patch":
            subprocess.run(["patch", "-p1", "-s", "-i", edit[1]], cwd=tree, check=True)
            continue
        path, old, new = edit
        target = tree / path
        source = target.read_text()
        if source.count(old) != 1:
            raise RuntimeError(f"{name}: {old!r} matches {source.count(old)} times")
        target.write_text(source.replace(old, new))
    log = packet / "receipts" / "probes" / (name + ".log")
    with log.open("w") as stream:
        result = subprocess.run(["make", "-C", str(tree / "tb/srp_encoder")],
                                stdout=stream, stderr=subprocess.STDOUT, check=False)
    text = log.read_text(errors="replace")
    shutil.rmtree(tree, ignore_errors=True)
    return f"{name}\trc={result.returncode}\t{tally(text)}\t{rows(text)}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("clone")
    parser.add_argument("packet", type=Path)
    parser.add_argument("groups")
    parser.add_argument("--jobs", type=int, default=8)
    args = parser.parse_args()
    os.environ.setdefault("VERILATOR", "verilator")
    (args.packet / "receipts" / "probes").mkdir(parents=True, exist_ok=True)
    wanted = set(args.groups.split(","))
    items = [(n, s, args.clone, args.packet) for n, s in probes(args.clone).items()
             if s["group"] in wanted]
    with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
        lines = list(pool.map(run, items))
    table = args.packet / "receipts" / "probes" / ("summary-" + "-".join(sorted(wanted)) + ".tsv")
    table.write_text("\n".join(lines) + "\n")
    print("\n".join(line[:230] for line in lines))


if __name__ == "__main__":
    main()
