#!/usr/bin/env python3
"""Disposable reviewer arms on the encoder suite at the exact head.

Usage: probe_arms.py CLONE OUTDIR SCRATCH [--jobs N]
Each arm copies hdl/ and tb/ into SCRATCH, edits KL_srp_encoder.sv by exact
string replacement (refusing drift), runs tb/srp_encoder with line-buffered
stdout, and records rc, tally and the FAIL lines.
"""
import concurrent.futures as cf, os, pathlib, re, shutil, subprocess, sys, tempfile

ENC = "hdl/srp/KL_srp_encoder.sv"
KEY_MSRP = "return {APP_MSRP_C, t, v[271:208]};"
KEY_MVRP = "return {APP_MVRP_C, ATTR_MVRP_VID_C, v[271:256], 48'd0};"
ARMS = {
    "rv-search-ignores-start": [(
        "assign sr_engage_w = ev_valid_i && valid_type_w && base_ok_w && (tgt_cnt_w != '0);",
        "assign sr_engage_w = ev_valid_i && valid_type_w && !tgt_full_w && !busy_app_w && (tgt_cnt_w != '0);")],
    "rv-empty-table-searches": [(
        "&& (!valid_type_w || (tgt_cnt_w == '0) || sr_hit_w || sr_last_w);",
        "&& (!valid_type_w || sr_hit_w || sr_last_w);")],
    "start-term-collect-dropped": [(
        "? (start0_w || ((st_r == E_COLLECT) && go0_w)\n",
        "? (start0_w\n")],
    "start-term-prepare-dropped": [(
        "|| ((st_r == E_IDLE) && la_prepare_i)) : start1_w;",
        ") : start1_w;")],
}
for bit in range(64):
    ARMS[f"key-msrp-bit{bit:02d}"] = [(KEY_MSRP,
        f"return {{APP_MSRP_C, t, v[271:208] & ~(64'd1 << {bit})}};")]
for bit in range(16):
    ARMS[f"key-mvrp-bit{bit:02d}"] = [(KEY_MVRP,
        f"return {{APP_MVRP_C, ATTR_MVRP_VID_C, v[271:256] & ~(16'd1 << {bit}), 48'd0}};")]


def trial(args):
    name, clone, out, scratch = args
    with tempfile.TemporaryDirectory(prefix="arm-", dir=scratch) as tmp:
        tree = pathlib.Path(tmp)
        shutil.copytree(clone / "hdl", tree / "hdl")
        shutil.copytree(clone / "tb" / "common", tree / "tb" / "common")
        shutil.copytree(clone / "tb" / "srp_encoder", tree / "tb" / "srp_encoder",
                        ignore=shutil.ignore_patterns("obj_*"))
        path = tree / ENC
        text = path.read_text()
        for old, new in ARMS[name]:
            if text.count(old) != 1:
                return name, -1, "DRIFT", []
            text = text.replace(old, new)
        path.write_text(text)
        log = out / f"{name}.log"
        with log.open("w") as stream:
            rc = subprocess.run(["stdbuf", "-oL", "make", "-C", str(tree / "tb" / "srp_encoder")],
                                stdout=stream, stderr=subprocess.STDOUT, check=False).returncode
    body = log.read_text(errors="replace")
    tally = re.findall(r"^\d+ checks:.*$", body, re.M)
    fails = [l for l in body.splitlines() if l.startswith("FAIL:")]
    keep = fails + (tally or ["NO TALLY"]) + [l for l in body.splitlines()
                                              if "Segmentation" in l or "Error " in l]
    log.write_text("\n".join(keep) + "\n")
    return name, rc, tally[0] if tally else "NO TALLY", fails


def main():
    clone, out, scratch = (pathlib.Path(p).resolve() for p in sys.argv[1:4])
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
    out.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(jobs) as pool:
        rows = list(pool.map(trial, [(n, clone, out, scratch) for n in ARMS]))
    with (out / "SUMMARY.tsv").open("w") as table:
        for name, rc, tally, fails in rows:
            rowset = sorted({re.sub(r"^FAIL: (\S+).*", r"\1", l) for l in fails})
            table.write(f"{name}\trc={rc}\t{tally}\t{' '.join(rowset)}\n")


if __name__ == "__main__":
    main()
