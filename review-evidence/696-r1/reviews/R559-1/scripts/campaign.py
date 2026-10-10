#!/usr/bin/env python3
"""R559-1 reviewer campaign for PR #706 (issue #696).

Usage: campaign.py <repo> <probe-tree> <receipts-dir> <scratch-dir>

Runs, concurrently, at the reviewed head:
  * the MAAP unit harness, coverage gate and real-datapath integration harness;
  * a parallel replay of tb/verilator/maap/mutants.py: the same MUTANTS table,
    the same run_case() acceptance rule (build ok, exit 1, named [FAIL] line),
    the clean controls and the four datapath rows of its main();
  * reviewer-authored plants (not in the author's table), unit and datapath;
  * the firmware differential self-test.
Every job writes <name>.log and <name>.rc into the receipts directory.
Datapath (milan_datapath) builds are limited to two at a time.
"""
import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO, PROBE, OUT, SCRATCH = (Path(a).resolve() for a in sys.argv[1:5])
OUT.mkdir(parents=True, exist_ok=True)
MAAP = REPO / "tb/verilator/maap"
DP_GATE = threading.Semaphore(2)
ENV = dict(os.environ, VERILATOR_JOBS="2", TMPDIR=str(SCRATCH / "tmp"))


def sh(name, argv, cwd, heavy=False, env=None):
    """Run one command; record its full output and exit status."""
    ctx = DP_GATE if heavy else contextlib.nullcontext()
    with ctx:
        r = subprocess.run(argv, cwd=cwd, env=env or ENV, capture_output=True, text=True)
    (OUT / f"{name}.log").write_text(f"$ {' '.join(map(str, argv))}\n(cwd {cwd})\n" + r.stdout + r.stderr)
    (OUT / f"{name}.rc").write_text(f"{r.returncode}\n")
    return r.returncode


_COUNTER = iter(range(10**6))


def load_mutants(maap_dir):
    """A private module instance, so its print() can be redirected per thread."""
    spec = importlib.util.spec_from_file_location(f"mutants_{next(_COUNTER)}", maap_dir / "mutants.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def case(work, name, source, failure, integration, maap_dir):
    """One campaign row through the module's own run_case(); output captured."""
    mod = load_mutants(maap_dir)
    buf = io.StringIO()
    mod.print = lambda *a, **k: print(*a, **{**k, "file": buf})
    ctx = DP_GATE if integration else contextlib.nullcontext()
    with ctx:
        ok = mod.run_case(work, name, source, failure, integration)
    return dict(name=name, expected=failure, integration=integration, passed=bool(ok), output=buf.getvalue())


def plant(work, name, source, failures):
    """Reviewer plant: same acceptance as run_case, any of the named checks may carry the kill."""
    rtl = work / f"{name}.sv"
    rtl.write_text(source)
    mdir = work / f"obj_{name}"
    b = subprocess.run(["make", "-s", "-C", str(MAAP), "build", f"MAAP_RTL={rtl}", f"MDIR={mdir}",
                        f"VERILATOR={ENV.get('VERILATOR', 'verilator')}", "VERILATOR_JOBS=2"],
                       env=ENV, capture_output=True, text=True)
    if b.returncode:
        return dict(name=name, expected=" | ".join(failures), integration=False, passed=False,
                    output="BUILD FAILED\n" + b.stdout[-3000:] + b.stderr[-3000:])
    r = subprocess.run([str(mdir / "VKL_maap_sim")], cwd=mdir, capture_output=True, text=True)
    out = r.stdout + r.stderr
    hit = [f for f in failures if f"[FAIL] {f}" in out]
    return dict(name=name, expected=" | ".join(failures), integration=False,
                passed=r.returncode == 1 and bool(hit), killed_by=hit,
                output=f"rc={r.returncode}\n" + "\n".join(l for l in out.splitlines() if "[FAIL]" in l or "checks" in l))


def author_rows(mod, source):
    """The rows mutants.main() runs, in its order (clean first)."""
    rows = [("clean", source, None, False)]
    for name, _, anchor, repl, failure in mod.MUTANTS:
        rows.append((name, source.replace(anchor, repl) if source.count(anchor) == 1 else None, failure, False))
    rows.append(("m4_datapath_clean", source, None, True))
    a = "      lfsr_r       <= 32'hACE1;\n      rng_seeded_r <= 1'b0;"
    rows.append(("m4_reset_time_sampling",
                 source.replace(a, "      lfsr_r       <= enable_seed_w;\n      rng_seeded_r <= 1'b1;")
                 if source.count(a) == 1 else None, "M4 datapath: programmed MAC changes probe intervals", True))
    a = "else if (restart_w || port_operational_p)"
    rows.append(("m5_datapath_ignores_link", source.replace(a, "else if (restart_w)")
                 if source.count(a) == 1 else None, "M5 datapath: link return starts four fresh PROBEs", True))
    a = "station_mac_i[31:0] + realtime_ns_i"
    rows.append(("m3_datapath_ignores_clock", source.replace(a, "station_mac_i[31:0]")
                 if source.count(a) == 1 else None, "M3 datapath: real-time clock changes probe intervals", True))
    return rows


#: reviewer plants inside KL_maap: (name, anchor, replacement, checks; one must fail)
PLANTS = (
    ("r_equal_mac_counts_as_lower", "octet_rev(station_mac_i) < octet_rev(rx_src_r)",
     "octet_rev(station_mac_i) <= octet_rev(rx_src_r)", ("M1 rProbe/PROBE higher or equal MAC yields", "M1 rDefend/DEFEND higher or equal MAC yields")),
    ("r_truncation_not_accumulated", "((rbeat_r == '0) || rx_bytes_valid_r)", "1'b1",
     ("M8 B.2 truncated PROBE-state input has no effect", "M8 B.2 truncated DEFEND-state input has no effect")),
    ("r_conflict_count_low_byte_only", "(rbeat_r == 3'd5) ? 8'h03", "(rbeat_r == 3'd5) ? 8'h01",
     ("M8 B.2 truncated PROBE-state input has no effect", "M8 B.2 truncated DEFEND-state input has no effect")),
    ("r_pending_not_cleared_on_send", "        if (defend_w) defend_pending_r <= 1'b0;\n", "",
     ("M6 pending response sent exactly once",)),
    ("r_seed_from_mac_high_bits", "station_mac_i[31:0] + realtime_ns_i",
     "station_mac_i[47:16] + realtime_ns_i", ("M3 B.3.6.1 first enable seeds MAC plus clock",)),
    ("r_count_echo_low_byte", "tx_cnt_r        <= rx_cnt_r;", "tx_cnt_r        <= {8'd0, rx_cnt_r[7:0]};",
     ("M2 B.3.6.6 requested count echoes all 16 bits",)),
    ("r_restart_on_link_loss", "port_operational_i && !port_operational_r",
     "!port_operational_i && port_operational_r",
     ("M5 B.3.5.9 link return restarts PROBE", "M5 B.3.5.9 link return revokes and reprobes")),
    ("r_seed_end_ignores_count", "wire [16:0] seed_end_w = {1'b0, seed_offset_i} + {9'd0, count_i};",
     "wire [16:0] seed_end_w = {1'b0, seed_offset_i};", ("M7 Table B.9 invalid supplied range refused",)),
)
#: reviewer plants in the datapath integration (probe tree only)
DP_PLANTS = (
    ("r_dp_link_tied_high", ".port_operational_i (eff_link_w),", ".port_operational_i (1'b1),",
     "M5 datapath: link return starts four fresh PROBEs"),
    ("r_dp_clock_tied_zero", ".realtime_ns_i     (ptp_now_w[31:0]),", ".realtime_ns_i     (32'd0),",
     "M3 datapath: real-time clock changes probe intervals"),
)


def dp_plant(name, anchor, repl, failure):
    """Copy the probe tree, edit milan_datapath.sv there, build and run the integration harness."""
    tree = SCRATCH / f"dp_{name}"
    if not tree.exists():
        subprocess.run(["cp", "-a", str(PROBE), str(tree)], check=True)
    dp = tree / "hdl/milan/milan_datapath.sv"
    text = dp.read_text()
    if text.count(anchor) != 1:
        return dict(name=name, expected=failure, integration=True, passed=False, output="anchor count != 1")
    dp.write_text(text.replace(anchor, repl))
    mdir = SCRATCH / f"obj_{name}"
    with DP_GATE:
        b = subprocess.run(["make", "-s", "-C", str(tree / "tb/verilator/maap"), "integration-build",
                            f"DP_MDIR={mdir}", f"VERILATOR={ENV.get('VERILATOR', 'verilator')}",
                            "VERILATOR_JOBS=4"], env=ENV, capture_output=True, text=True)
    if b.returncode:
        return dict(name=name, expected=failure, integration=True, passed=False,
                    output="BUILD FAILED\n" + b.stdout[-3000:] + b.stderr[-3000:])
    r = subprocess.run([str(mdir / "maap_integration")], cwd=mdir, capture_output=True, text=True)
    out = r.stdout + r.stderr
    return dict(name=name, expected=failure, integration=True,
                passed=r.returncode == 1 and f"[FAIL] {failure}" in out, output=f"rc={r.returncode}\n{out}")


def main():
    work = SCRATCH / "campaign"
    work.mkdir(parents=True, exist_ok=True)
    mod = load_mutants(MAAP)
    source = (REPO / "hdl/ieee1722/maap/KL_maap.sv").read_text()
    items = {i for _, i, _, _, _ in mod.MUTANTS if isinstance(i, int)} - {mod.SUPPORTING}
    rows = author_rows(mod, source)
    plants = [(n, source.replace(a, r) if source.count(a) == 1 else None, f) for n, a, r, f in PLANTS]
    with ThreadPoolExecutor(max_workers=12) as pool:
        jobs = {
            "unit": pool.submit(sh, "unit", ["make", "-s", "-C", str(MAAP), "run", f"MDIR={SCRATCH/'unit'}"], REPO),
            "coverage": pool.submit(sh, "coverage", ["make", "-s", "-C", str(MAAP), "coverage",
                                                     f"COV_MDIR={SCRATCH/'cov'}"], REPO),
            "integration": pool.submit(sh, "integration", ["bash", "-c",
                f"make -s -C {MAAP} integration-build DP_MDIR={SCRATCH/'integration'} VERILATOR_JOBS=4 "
                f"&& {SCRATCH/'integration'/'maap_integration'}"], REPO, True),
            "differential": pool.submit(sh, "differential", [sys.executable, "sw/firmware/ctrl/test/maap_differential.py",
                                                             "--self-test", "--keep", str(SCRATCH / "differential")], REPO),
        }
        clean = case(work, rows[0][0], rows[0][1], rows[0][2], rows[0][3], MAAP)
        futs = []
        for name, src, failure, integ in rows[1:]:
            if src is None:
                futs.append(pool.submit(lambda n=name, f=failure, i=integ: dict(
                    name=n, expected=f, integration=i, passed=False, output="anchor count != 1")))
            else:
                futs.append(pool.submit(case, work, name, src, failure, integ, MAAP))
        for name, src, failures in plants:
            if src is None:
                futs.append(pool.submit(lambda n=name, f=failures: dict(
                    name=n, expected=" | ".join(f), integration=False, passed=False, output="anchor count != 1")))
            else:
                futs.append(pool.submit(plant, work, name, src, failures))
        dpf = [pool.submit(dp_plant, *p) for p in DP_PLANTS]
        results = [clean] + [f.result() for f in futs]
        dres = [f.result() for f in dpf]
        rcs = {k: v.result() for k, v in jobs.items()}
    author = results[:len(rows)]
    mine = results[len(rows):] + dres
    lines = [f"#686 item guard: items {sorted(items)} == [1, 2, 3, 4]: {items == {1, 2, 3, 4}}"]
    for tag, group in (("AUTHOR", author), ("REVIEWER", mine)):
        for r in group:
            lines.append(f"[{tag}] [{'ok' if r['passed'] else 'ESCAPED'}] {r['name']}"
                         f"{'' if r['expected'] is None else ' -> ' + r['expected']}"
                         f"{' (datapath)' if r['integration'] else ''}")
    a_fail = sum(not r["passed"] for r in author)
    m_fail = sum(not r["passed"] for r in mine)
    lines.append(f"== author campaign replay: rows {len(author)} "
                 f"(controls {sum(r['expected'] is None for r in author)}, "
                 f"defects {sum(r['expected'] is not None for r in author)}), failures {a_fail} ==")
    lines.append(f"== reviewer plants: {len(mine)}, escaped {m_fail} ==")
    lines.append("job rcs: " + json.dumps(rcs, sort_keys=True))
    (OUT / "campaign-summary.txt").write_text("\n".join(lines) + "\n")
    (OUT / "campaign-rows.json").write_text(json.dumps(author + mine, indent=1) + "\n")
    print("\n".join(lines))
    ok = a_fail == 0 and m_fail == 0 and items == {1, 2, 3, 4} and all(v == 0 for v in rcs.values())
    (OUT / "campaign.rc").write_text(f"{0 if ok else 1}\n")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
