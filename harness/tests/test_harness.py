#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! The harness's own gates. `python3 harness/tests/test_harness.py`
#!
#! House style of this repo's gate scripts: numbered gates, one line each,
#! `ALL GATES PASS` at the end, nonzero exit on any failure.
#!
#! **Never claim a script works because it looks right.** Every gate below runs
#! real code:
#!
#!   * THD+N is checked against a SYNTHESISED tone with a known answer, in both
#!     directions - a clean tone must read far below the acceptance threshold,
#!     and a tone with one injected harmonic at -80 dB must read -80 dB back.
#!     There is also a gate proving the windowing trap: applying a window to the
#!     same coherent tone inflates the residual.
#!   * The JSONL writer, the resume cursor, the STATUS transitions and the
#!     one-shot alert are exercised, not inspected.
#!   * The board `sh` scripts are syntax-checked with `sh -n`, and the batching
#!     rule (no per-register shell loop) is asserted structurally.
#!   * The full dry run drives every phase against the mock bench, then a second
#!     dry run injects a fault and asserts the FAILED path: STATUS, forensic
#!     bundle, exactly one alert, and BLOCKED never alerting.

from __future__ import annotations

import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HARNESS = Path(__file__).resolve().parent.parent
REPO = HARNESS.parent
sys.path.insert(0, str(HARNESS))

from milanharness import counters as cmod            # noqa: E402
from milanharness import csr as csrmod               # noqa: E402
from milanharness import latency as latmod           # noqa: E402
from milanharness import log as logmod               # noqa: E402
from milanharness import notify as notifymod         # noqa: E402
from milanharness import registry as regmod          # noqa: E402
from milanharness import report as reportmod         # noqa: E402
from milanharness.config import ConfigError, load    # noqa: E402
from milanharness.mock import MockBench, synth_tone  # noqa: E402
from milanharness.transport import Outage, Transport  # noqa: E402

FIX = HARNESS / "tests" / "fixtures"
FAILURES: list[str] = []
SKIPPED: list[str] = []
GATE = [0]


def gate(name: str):
    GATE[0] += 1
    return f"  [gate {GATE[0]}] {name}"


def ok(name: str, detail: str = "") -> None:
    print(gate(name) + (f": {detail}" if detail else ""))


def bad(name: str, detail: str) -> None:
    GATE[0] += 1
    msg = f"  [gate {GATE[0]}] FAIL {name}: {detail}"
    print(msg)
    FAILURES.append(msg)


def check(cond: bool, name: str, detail: str = "", why: str = "") -> None:
    if cond:
        ok(name, detail)
    else:
        bad(name, why or detail)


# ==========================================================================
def test_config():
    print("test_config:")
    cfg = load(allow_placeholders=True)
    check(len(cfg.boards) >= 2, "template config parses",
          f"{len(cfg.boards)} boards, schema {cfg.raw['schema_version']}")
    check(cfg.boards[0].csr_base == 0x90000000, "csr_base is configuration",
          f"0x{cfg.boards[0].csr_base:08X}")
    # Placeholders must REFUSE outside a dry run - the whole point of the config
    # file is that no bench identity is compiled into the scripts.
    try:
        load()
        bad("placeholder refusal", "the template loaded with placeholders intact")
    except ConfigError as exc:
        check("placeholder" in str(exc), "placeholder refusal", str(exc)[:70])
    # The coherent-tone precondition is enforced by the config, not by hope.
    raw = dict(cfg.raw)
    raw["audio"] = dict(raw["audio"], tone_hz=997)
    import tomllib  # noqa: F401  (proves the stdlib parser is what we rely on)
    from milanharness import config as cfgmod
    try:
        cfgmod._validate_ranges(cfg.path, raw)
        bad("non-exact-period tone refused", "997 Hz at 48 kHz was accepted")
    except ConfigError as exc:
        check("coherent" in str(exc), "non-exact-period tone refused",
              "config refuses a tone the un-windowed method cannot measure")
    check(cfg.items_path == "", "item registry defaults to unconfigured",
          "no compiled-in bench path; absence becomes BLOCKED, not a crash")


def test_registry():
    print("test_registry:")
    reg = regmod.load(FIX / "items.sample.toml")
    check(len(reg) == 5, "fixture registry loads", f"{len(reg)} rows")
    check(reg.validate() == [], "fixture registry is sound")
    check(len(reg.implemented()) == 3 and len(reg.stubs()) == 2,
          "implemented / not-implemented split",
          f"{len(reg.implemented())} implemented, {len(reg.stubs())} stubs")

    # A lost row must be a gate failure, not an invisible omission.
    body = (FIX / "items.sample.toml").read_text()
    trimmed = body.split('[[item]]\nid      = "es-4.1"')[0]
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "short.toml"
        p.write_text(trimmed)
        try:
            regmod.load(p)
            bad("lost row detected", "a registry missing a row validated clean")
        except regmod.RegistryError as exc:
            check("declares 5" in str(exc) or "es-4" in str(exc),
                  "lost row detected", "declared shape catches the omission")

    # Unconfigured registry is RegistryMissing -> BLOCKED, never a crash.
    try:
        regmod.load("")
        bad("missing registry raises RegistryMissing", "no exception")
    except regmod.RegistryMissing as exc:
        check("no item registry configured" in str(exc),
              "missing registry raises RegistryMissing", "-> BLOCKED path")
    try:
        regmod.load(str(FIX / "nope.toml"))
        bad("absent registry file raises RegistryMissing", "no exception")
    except regmod.RegistryMissing:
        ok("absent registry file raises RegistryMissing")

    # Overlay may refine, never add.
    with tempfile.TemporaryDirectory() as d:
        good = Path(d) / "ov.toml"
        good.write_text('[[item]]\nid = "es-2.1"\nrunner = "aecp_cmd"\n'
                        'status = "implemented"\n')
        r2 = regmod.load(FIX / "items.sample.toml", good)
        check(r2["es-2.1"].implemented, "overlay refines a row",
              "es-2.1 stub -> implemented via the private overlay")
        bad_ov = Path(d) / "bad.toml"
        bad_ov.write_text('[[item]]\nid = "es-99.1"\nrunner = "x"\n')
        try:
            regmod.load(FIX / "items.sample.toml", bad_ov)
            bad("overlay cannot add rows", "es-99.1 was accepted")
        except regmod.RegistryError as exc:
            check("never add" in str(exc), "overlay cannot add rows",
                  "an overlay can refine, not extend")


def test_thdn():
    print("test_thdn:")
    try:
        import numpy  # noqa: F401
    except ImportError:
        # Skipped, not failed: numpy is not installed system-wide on the dev
        # box and only the THD+N analysis needs it. Everything else in the
        # harness runs on a bare python3 >= 3.11.
        SKIPPED.append("THD+N gates: numpy not importable on this interpreter "
                       "- run under a venv that has it (harness/README.md)")
        print("  (skipped: numpy not importable)")
        return
    from milanharness import thdn

    rate, f0 = 48000, 1000
    # 1. A clean exact-period tone must read far below the acceptance threshold.
    clean = synth_tone(rate_hz=rate, f0_hz=f0, seconds=1.0, channels=2,
                       amplitude=0.5)
    res = thdn.analyse_capture(clean, rate_hz=rate, f0_hz=f0, channels=2)
    worst = max(r.thdn_dbfs for r in res)
    check(worst < -120.0, "clean tone reads below acceptance",
          f"worst {worst:.1f} dBFS (accept <= -120)",
          f"clean synthesised tone measured {worst:.1f} dBFS")

    # 2. A KNOWN harmonic must be recovered at its known level. This is the gate
    #    that makes the analysis a measurement rather than a smoke test.
    for want in (-80.0, -60.0, -40.0):
        dirty = synth_tone(rate_hz=rate, f0_hz=f0, seconds=1.0, channels=1,
                           amplitude=0.5, thd_at_db=want)
        got = thdn.analyse_capture(dirty, rate_hz=rate, f0_hz=f0,
                                   channels=1)[0].thdn_dbfs
        check(abs(got - want) < 0.5, f"known harmonic at {want:.0f} dB recovered",
              f"measured {got:.2f} dBFS",
              f"injected {want} dB, measured {got:.2f} dB")

    # 3. THE WINDOWING TRAP, demonstrated rather than asserted in a comment:
    #    windowing this coherent tone inflates the residual, i.e. manufactures
    #    distortion that is not there.
    import numpy as np
    x = np.frombuffer(clean, dtype=">i4").astype(np.float64)[0::2] / 2147483648.0
    n = (len(x) // 48) * 48
    x = x[:n]
    def _resid(sig):
        spec = np.abs(np.fft.rfft(sig))
        k0 = int(round(f0 * n / rate))
        keep = spec.copy()
        for k in (0, k0 - 1, k0, k0 + 1):
            keep[k] = 0.0
        return float(np.sqrt(np.sum(keep ** 2))) / max(spec[k0], 1e-30)
    flat = _resid(x)
    windowed = _resid(x * np.hanning(n))
    check(windowed > flat * 10, "windowing a coherent tone inflates the residual",
          f"no window {20 * math.log10(max(flat, 1e-30)):.1f} dB vs Hann "
          f"{20 * math.log10(max(windowed, 1e-30)):.1f} dB",
          "the window did not measurably inflate the residual, so the "
          "no-window rule would be unmotivated")

    # 4. A non-exact-period request must be refused, not approximated.
    try:
        thdn.analyse(np.zeros(4800), rate_hz=48000, f0_hz=997)
        bad("non-coherent request refused", "997 Hz was analysed anyway")
    except thdn.ThdnError as exc:
        check("coherently sampled" in str(exc), "non-coherent request refused",
              "the method refuses inputs it does not apply to")


def test_latency():
    print("test_latency:")
    from milanharness.config import Board
    board = Board(name="t", ssh="", via_jump=False, role="listener",
                  csr_base=0, datapath_clk_hz=100_000_000, version_expect=0,
                  n_listeners=1, n_talkers=1, pcm_ring_csr=0,
                  mac_loopback_csr=0, dma_ts_offset_csr=0,
                  alsa_capture_device="", alsa_capture_channels=2,
                  user_mtd_mount="", power_outlet=-1, netif="eth0")
    words = {
        "LTAP_RX_INFO": 4096, "LTAP_RX_EPOCH": 0,
        "LTAP_RX_D0": (52 << 16) | 50, "LTAP_RX_D0_MIN": 49,
        "LTAP_RX_D1": (33 << 16) | 30, "LTAP_RX_D1_MIN": 29,
        "LTAP_RX_D2": (12541 << 16) | 12500, "LTAP_RX_D2_MIN": 10378,
    }
    snap = csrmod.Snapshot(board="t", method="mock",
                           words={csrmod.REG[k]: v for k, v in words.items()})
    chain = latmod.decode(snap, "rx")
    ins = latmod.in_system(chain, board, 20.83)
    # 50 + 30 cycles at 100 MHz = 0.80 us last; 52 + 33 = 0.85 us max.
    check(abs(ins.last_us - 0.80) < 0.01 and abs(ins.max_us - 0.85) < 0.01,
          "in-system RX excludes the ring-fill stage",
          f"last {ins.last_us:.2f} us / max {ins.max_us:.2f} us "
          f"(excluded: {ins.excluded_stage})",
          f"got last={ins.last_us} max={ins.max_us}")
    check(ins.within_budget, "in-system RX inside one sample",
          f"{ins.max_us:.2f} us <= 20.83 us")
    # Including the excluded stage would blow the budget by ~6x - which is the
    # whole reason the split exists.
    total = board.cycles_to_us(sum(d.last_cyc for d in chain.deltas))
    check(total > 100.0, "the excluded stage is the pto, not pipeline latency",
          f"whole RX chain {total:.1f} us vs in-system {ins.last_us:.2f} us")

    # Saturated / timed-out chains must not pass as clean maxima.
    sat = csrmod.Snapshot(board="t", method="mock", words={
        **{csrmod.REG[k]: v for k, v in words.items()},
        csrmod.REG["LTAP_RX_INFO"]: (0xFFFF << 16) | 0,
    })
    c2 = latmod.decode(sat, "rx")
    check(not c2.trustworthy, "timed-out tap chain is flagged untrustworthy",
          f"samples={c2.samples} timeouts={c2.timeouts}")

    pts = [latmod.PtoPoint(500, 505, 25), latmod.PtoPoint(1000, 1002, 25)]
    okv, why = latmod.pto_sweep_verdict(pts)
    check(okv, "pto sweep passes when every point matches", why)
    pts.append(latmod.PtoPoint(2000, 1400, 25))
    okv, why = latmod.pto_sweep_verdict(pts)
    check(not okv, "pto sweep fails on ONE bad point, not on average", why)


def test_jsonl_and_resume():
    print("test_jsonl_and_resume:")
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        run = logmod.RunDir(root, "run-test", logmod.Limits(
            human_log_max_bytes=512, human_log_keep=3, max_item_output_bytes=64))
        run.set_phase("baseline")
        run.record(item="es-1.1", verdict=logmod.PASS, measured={"x": 1})
        run.set_phase("validation")
        run.record(item="es-1.2", verdict=logmod.FAIL, detail="y" * 500)
        recs = run.read_records()
        check(len(recs) == 2 and recs[0]["seq"] == 1 and recs[1]["seq"] == 2,
              "JSONL records are ordered and sequenced",
              f"{len(recs)} records")
        check({r["phase"] for r in recs} == {"baseline", "validation"},
              "JSONL rotates per phase",
              f"{sorted(p.name for p in run.jsonl_dir.iterdir())}")
        check("truncated" in recs[1]["detail"],
              "per-item output is capped",
              f"detail capped to {len(recs[1]['detail'])} chars")
        for k in ("ts", "run", "seq", "phase", "item", "kind", "verdict",
                  "measured", "detail"):
            if k not in recs[0]:
                bad("record schema", f"missing key {k!r}")
                break
        else:
            ok("record schema", "item/phase/verdict/measured/timestamp all present")

        # Human log rotation + gzip, bounded.
        for i in range(200):
            run.say("x" * 80)
        gz = sorted(run.dir.glob("harness.log.*.gz"))
        check(gz and len(gz) <= 3, "human log rotates and gzips, bounded",
              f"{len(gz)} rotated part(s), keep=3")

        # STATUS is the contract.
        run.set_status(logmod.STATUS_RUNNING, "starting")
        check(run.status() == ("RUNNING", "starting"), "STATUS RUNNING")
        run.set_status(logmod.STATUS_FAILED, "es-1.2: boom")
        check(run.status()[0] == "FAILED", "STATUS FAILED", run.status()[1])
        run.set_status(logmod.STATUS_DONE, "every item passed")
        check(run.status() == ("DONE", "every item passed"), "STATUS DONE")

        # Heartbeat answers "is it alive" without parsing a log.
        run.heartbeat(phase="soak", item="soak/interval-0007", iteration=7)
        hb = json.loads(run.heartbeat_path.read_text())
        check(all(k in hb for k in ("phase", "item", "iteration", "timestamp")),
              "heartbeat carries phase/item/iteration/timestamp",
              f"{hb['phase']} {hb['item']} #{hb['iteration']}")

        # Cursor: crash -> resume at the NEXT item, no arguments.
        run.mark_item_done("validation", "es-1.1")
        run.mark_phase_done("baseline")
        run2 = logmod.RunDir(root, "run-test")
        c = run2.load_cursor()
        check("validation/es-1.1" in c["done_items"]
              and "baseline" in c["done_phases"],
              "resume cursor persists items and phases", str(c["phase"]))
        check(run2._seq == 2, "record sequence continues across a resume",
              f"next seq {run2._seq + 1}")
        check(logmod.latest_run(root) == "run-test",
              "argument-free resume finds the newest run")

        # A torn last line must not make the run unreadable.
        p = run.jsonl_path("validation")
        with p.open("a") as fh:
            fh.write('{"ts": "broken", "seq"')
        check(len(run.read_records()) == 2,
              "a torn record does not lose the run",
              "truncated trailing line skipped")


def test_notify():
    print("test_notify:")
    calls = []

    def fake(argv, timeout):
        calls.append(argv)
        return (0, "")

    class C:
        def section(self, _n):
            return {"alert_webhook": "https://example.invalid/hook",
                    "alert_timeout_s": 7, "alert_command": []}

    n = notifymod.Notifier(C(), run_id="run-x", runner=fake)
    r1 = n.alert_failed("es-4.7", "GET_NAME returned NOT_IMPLEMENTED")
    r2 = n.alert_failed("es-4.8", "another failure")
    check(r1["sent"] and not r2["sent"], "alert fires exactly ONCE",
          "second failure recorded, not re-alerted")
    check(len(calls) == 1 and calls[0][0] == "curl", "webhook uses curl POST",
          " ".join(calls[0][:6]))
    check("--max-time" in calls[0] and "7" in calls[0],
          "webhook is timeout-bounded", "alert_timeout_s honoured")
    check(all("example.invalid" not in str(c) for c in
              r1["channels"]), "the endpoint URL is not copied into the record",
          "records say 'configured', not the URL")
    body = r1["body"]
    check(body.startswith("milan campaign FAILED: es-4.7 - ")
          and len(body) <= notifymod.MAX_BODY,
          "alert body matches the documented shape and length",
          f"{len(body)} chars: {body[:60]}...")

    # Undeliverable must not fail the campaign.
    def failing(argv, timeout):
        return (7, "curl: (7) Failed to connect")
    n2 = notifymod.Notifier(C(), run_id="run-y", runner=failing)
    r3 = n2.alert_failed("es-1.1", "boom")
    check(not r3["sent"] and "logging problem" in r3["why"],
          "an undeliverable alert is recorded, not raised", r3["why"][:60])

    # Unset = clean no-op.
    class C0:
        def section(self, _n):
            return {"alert_webhook": "", "alert_timeout_s": 10,
                    "alert_command": []}
    n3 = notifymod.Notifier(C0(), run_id="run-z", runner=fake)
    r4 = n3.alert_failed("es-1.1", "boom")
    check(not r4["sent"] and not n3.configured,
          "unset webhook is a clean no-op", r4["why"])


def test_counters_table():
    print("test_counters_table:")
    rows = cmod.load_rows(HARNESS / "config" / "counters.toml")
    check(len(rows) >= 25, "counter audit table loads", f"{len(rows)} rows")
    fams = {r.family for r in rows}
    check({"stream_input", "stream_output", "avb_interface", "clock_domain",
           "rmon"} <= fams, "all five counter families are represented",
          ", ".join(sorted(fams)))
    si = [r for r in rows if r.family == "stream_input"]
    check(len(si) == 10, "all ten STREAM_INPUT counters have a row",
          f"{len(si)} rows")
    check(all(r.read.startswith("win:") for r in si if r.read),
          "STREAM_INPUT is read full-width through the 0x800 window",
          "never from the saturating flat AVTPRX_* views")
    check(all(r.clears_on_bind for r in si),
          "STREAM_INPUT rows are marked clears_on_bind",
          "so the engine reads them BEFORE any re-bind")
    withhold = [r for r in rows if r.hold]
    check(len(withhold) >= 12, "most rows name neighbours that must not move",
          f"{len(withhold)} rows carry a hold list")

    # The engine itself.
    row = cmod.CounterRow("a", "f", "csr:0x660", "p", "==1", ("b",), False, "")
    res = cmod.audit_one(row, {"a": 10, "b": 5}, {"a": 11, "b": 5})
    check(res.verdict == "PASS", "counter that moves alone PASSes", res.detail)
    res = cmod.audit_one(row, {"a": 10, "b": 5}, {"a": 11, "b": 6})
    check(res.verdict == "FAIL" and res.moved_neighbours == ["b"],
          "a neighbour moving FAILs the row",
          "this is the only way a mis-wired counter shows up")
    res = cmod.audit_one(row, {"a": 10, "b": 5}, {"a": 10, "b": 5})
    check(res.verdict == "FAIL", "a counter that does not move FAILs", res.detail)
    res = cmod.audit_one(row, {"a": 10, "b": 5}, {"a": 3, "b": 5})
    check(res.verdict == "FAIL" and "BACKWARDS" in res.detail,
          "a counter going backwards FAILs", "wrap or a mid-window clear")
    res = cmod.audit_one(row, {"a": None}, {"a": None})
    check(res.verdict == "BLOCKED", "an unreadable counter is BLOCKED not FAIL",
          "the harness could not read it; the device did nothing wrong")

    # STATS_CAP: declared-unsupported is asserted on BOTH halves.
    snap = csrmod.Snapshot(board="t", method="mock", words={
        csrmod.REG["STATS_CAP"]: 0x1B8, csrmod.RMON_LANE0 + 4 * 0: 0})
    r = cmod.audit_capability(
        cmod.CounterRow("l0", "rmon", "rmon:0", "cap_declared_unsupported",
                        "==0", (), False, ""), snap)
    check(r.verdict == "PASS", "unsupported RMON lane declared and zero",
          r.detail)
    snap2 = csrmod.Snapshot(board="t", method="mock", words={
        csrmod.REG["STATS_CAP"]: 0x1B8, csrmod.RMON_LANE0 + 4 * 0: 42})
    r = cmod.audit_capability(
        cmod.CounterRow("l0", "rmon", "rmon:0", "cap_declared_unsupported",
                        "==0", (), False, ""), snap2)
    check(r.verdict == "FAIL" and "faked" in r.detail,
          "a lane declared unsupported that counts anyway FAILs", r.detail)


def test_csr_and_safety():
    print("test_csr_and_safety:")
    words = cmod  # noqa: F841 (keeps the import list honest)
    txt = "#METHOD=block\n0x000=0x4D494C4E\n0x004=0x00010013\nnoise\n0x654=bad\n"
    parsed = csrmod.parse_kv(txt)
    check(parsed == {0x000: 0x4D494C4E, 0x004: 0x00010013},
          "board key/value output parses tolerantly",
          "noise and malformed values skipped, good words kept")

    class FakeCsr:
        pass
    c = FakeCsr()
    c._arm_state = {"dir": 1, "idx": 2, "lwsrp_on": False, "sid_staged_for": 2}
    try:
        csrmod._guard_write(c, csrmod.REG["A_STRMW_CTRL"], 1)
        bad("t>0 arm with the engine OFF is refused", "the write was allowed")
    except csrmod.SafetyViolation as exc:
        check("unpaced" in str(exc), "t>0 arm with the engine OFF is refused",
              "the rail that keeps the peer board on the network")
    c._arm_state = {"dir": 0, "idx": 0, "lwsrp_on": True, "sid_staged_for": None}
    try:
        csrmod._guard_write(c, csrmod.REG["A_STRMW_CTRL"], 1)
        bad("unstaged CTRL commit is refused", "the write was allowed")
    except csrmod.SafetyViolation as exc:
        check("staged" in str(exc), "unstaged CTRL commit is refused",
              "an unstaged commit is what detached the entry-0 ACMP alias")
    c._arm_state = {"dir": 1, "idx": 3, "lwsrp_on": True, "sid_staged_for": 3}
    csrmod._guard_write(c, csrmod.REG["A_STRMW_CTRL"], 1)
    ok("a correctly staged t>0 arm with the engine ON is allowed")

    check(csrmod.NOT_BACKED == 0xDEADDEAD,
          "the not-backed poison value is distinguishable from zero",
          "0xDEADDEAD means 'not backed here', 0 means 'really zero'")


def test_board_scripts():
    print("test_board_scripts:")
    sh = shutil.which("sh")
    scripts = sorted((HARNESS / "board").glob("*.sh"))
    check(len(scripts) >= 5, "board scripts present",
          ", ".join(p.name for p in scripts))
    for p in scripts:
        r = subprocess.run([sh, "-n", str(p)], capture_output=True, text=True)
        check(r.returncode == 0, f"{p.name} is valid POSIX sh",
              "sh -n clean", r.stderr.strip()[:120])

    # No bench identity anywhere in the scripts. The patterns are ASSEMBLED
    # rather than written out, so this gate does not itself become the one file
    # in the tree carrying the literals it forbids.
    forbidden = ((r"/home/[a-z]+", "a home path"),
                 (r"192\.168\.\d+\.\d+", "an address literal"),
                 (r"\b" + "a" + "mx" + r"-", "a bench hostname prefix"),
                 (r"serial/by-" + "id/usb-", "a USB serial path"))
    for p in scripts + sorted((HARNESS / "milanharness").rglob("*.py")):
        text = p.read_text()
        for pat, why in forbidden:
            if re.search(pat, text):
                bad(f"{p.name} carries no bench identity", f"found {why}")
                break
        else:
            continue
        break
    else:
        ok("no script carries a bench identity",
           "hosts and addresses come from the config file")

    snap = (HARNESS / "board" / "csr_snapshot.sh").read_text()
    check("dd if=/dev/mem" in snap and "od -A n -t x4" in snap,
          "the snapshot fast path is ONE block read",
          "not a devmem loop - devmem costs ~0.75 s per invocation")
    check("4d494c4e" in snap.lower(),
          "the block path self-validates before it is trusted",
          "must reproduce the ID magic or it falls back to devmem")
    check("emit_slow" in snap, "a per-register fallback exists",
          "busybox dd/od option support varies; a wrong decode must not "
          "silently produce plausible garbage")

    win = (HARNESS / "board" / "csr_window.sh").read_text()
    check("0x804" in win and "while" in win and "break" in win,
          "the window script polls SNAP busy before reading",
          "skipping the poll is the 'not fresh' trap")

    rev = (HARNESS / "board" / "reverting_step.sh").read_text()
    check("trap" in rev and "setsid" in rev and "WATCHDOG" in rev,
          "destructive steps auto-revert two ways",
          "trap for ordinary death, a detached watchdog for everything else")
    check(rev.index("WATCHDOG=armed") < rev.index("APPLIED=loopback-on"),
          "the watchdog is armed BEFORE the destructive write",
          "otherwise a death between the two leaves the bench broken")

    kg = (HARNESS / "board" / "known_good.sh").read_text()
    check("APRB_PARSED" in kg and "media-plane" in kg,
          "known-good asserts a MOVEMENT check, not just liveness",
          "a bound-but-deaf board answers every static check")

    fl = (HARNESS / "board" / "flashlog.sh").read_text()
    check("/proc/mtd" in fl and "exit 0" in fl,
          "board flash logging degrades silently and records its falsifier",
          "no mtd node is deployed today; host-only logging is the record")


def test_dry_run():
    print("test_dry_run:")
    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, PYTHONPATH=str(HARNESS))
        cfg_path = Path(d) / "bench.toml"
        cfg_path.write_text(
            (HARNESS / "config" / "bench.example.toml").read_text()
            .replace('root = "./harness-runs"', f'root = "{d}/runs"')
            .replace("duration_s = 43200", "duration_s = 6")
            .replace("assert_every_s = 300", "assert_every_s = 2")
            .replace("rounds = 8", "rounds = 3"))

        def run_harness(*args):
            return subprocess.run(
                [sys.executable, "-m", "milanharness", "--config", str(cfg_path),
                 "--dry-run", *args],
                capture_output=True, text=True, env=env, cwd=str(HARNESS),
                timeout=600)

        r = run_harness("--seed", "12345", "--new")
        root = Path(d) / "runs"
        runs = sorted(p.name for p in root.iterdir()) if root.is_dir() else []
        check(bool(runs), "dry run creates a run directory", str(runs))
        if not runs:
            return
        run = logmod.RunDir(root, runs[-1])
        recs = run.read_records()
        phases = {r_["phase"] for r_ in recs}
        check({"baseline", "smoke", "validation", "counters", "matrix",
               "adversarial", "quality", "soak"} <= phases,
              "every phase's control flow ran against the mock",
              f"{len(phases)} phases, {len(recs)} records")
        check(run.status()[0] in ("DONE", "FAILED"),
              "STATUS reaches a terminal value", " ".join(run.status()))
        check((run.dir / "report.md").is_file(), "report written",
              str((run.dir / "report.md").stat().st_size) + " bytes")
        seeds = [r_["measured"].get("seed") for r_ in recs
                 if r_.get("item") == "harness" and r_.get("measured")]
        check(12345 in seeds, "the matrix seed is recorded for replay",
              f"seed {seeds[0] if seeds else '?'}")
        blocked = [r_ for r_ in recs if r_["verdict"] == "BLOCKED"]
        check(bool(blocked), "unrunnable items report BLOCKED, not FAIL",
              f"{len(blocked)} blocked (registry/controller absent)")
        alerts = [r_ for r_ in recs if r_.get("kind") == "alert"]
        check(not alerts or run.status()[0] == "FAILED",
              "no alert on a clean run", "silence on success")
        counters = [r_ for r_ in recs if r_["item"].startswith("counters/")]
        check(len(counters) >= 25, "every counter row produced a record",
              f"{len(counters)} counter records")

        # Resume: a run that stopped after `baseline` must skip it and carry on.
        run_harness("--new", "--phases", "baseline")
        partial = logmod.latest_run(root)
        before_n = len(logmod.RunDir(root, partial).read_records())
        r2 = run_harness("--run-id", partial, "--phases", "baseline,smoke")
        prun = logmod.RunDir(root, partial)
        recs2 = prun.read_records()
        resumed = [x for x in recs2 if x.get("kind") == "resume"]
        ran_smoke = [x for x in recs2 if x["phase"] == "smoke"
                     and x["kind"] == "check"]
        check(len(recs2) > before_n and bool(resumed) and bool(ran_smoke),
              "resume skips completed work and continues at the next item",
              f"{len(recs2) - before_n} new records, {len(resumed)} resume "
              f"marks, {len(ran_smoke)} smoke checks")
        cur = prun.load_cursor()
        check("baseline" in cur["done_phases"] and "smoke" in cur["done_phases"],
              "the cursor advances across a resume",
              f"done: {cur['done_phases']}")

        # --only narrows to one item.
        r3 = run_harness("--new", "--only", "baseline/dut-a/snapshot",
                         "--phases", "baseline")
        only_run = logmod.RunDir(root, logmod.latest_run(root))
        checks = [x for x in only_run.read_records()
                  if x["kind"] == "check" and x["verdict"] != "SKIP"]
        check(checks and all(x["item"] == "baseline/dut-a/snapshot"
                             for x in checks),
              "--only restricts the run to one item",
              f"{len(checks)} check(s), all `baseline/dut-a/snapshot`",
              f"items seen: {sorted({x['item'] for x in checks})}")
        check(r.returncode in (0, 1) and r2.returncode in (0, 1)
              and r3.returncode in (0, 1),
              "the harness never exits on an unhandled exception",
              f"rc {r.returncode}/{r2.returncode}/{r3.returncode}",
              (r.stderr or r2.stderr or r3.stderr)[-400:])

        # With a registry AND a controller configured, the implemented item
        # runners actually execute and the stubs are still visible as rows.
        cfg2 = Path(d) / "bench-items.toml"
        cfg2.write_text(
            cfg_path.read_text()
            .replace('path = ""', f'path = "{FIX / "items.sample.toml"}"', 1)
            .replace('controller_tool = ""',
                     'controller_tool = "/bin/true"', 1))
        subprocess.run(
            [sys.executable, "-m", "milanharness", "--config", str(cfg2),
             "--dry-run", "--new", "--phases", "validation"],
            capture_output=True, text=True, env=env, cwd=str(HARNESS),
            timeout=600)
        items = {x["item"]: x["verdict"] for x in
                 logmod.RunDir(root, logmod.latest_run(root)).read_records()
                 if x["item"].startswith("es-")}
        check(items.get("es-1.1") == "PASS" and items.get("es-4.1") == "PASS",
              "implemented items execute their runner",
              f"es-1.1={items.get('es-1.1')} es-4.1={items.get('es-4.1')}")
        check(items.get("es-2.1") == "BLOCKED"
              and items.get("es-3.1") == "BLOCKED",
              "stub items are VISIBLE as not-implemented rows",
              "an item with no row would be invisible - that is the failure "
              "mode the registry exists to prevent")
        check(len(items) == 5, "every registry row produced a record",
              f"{len(items)} of 5 fixture rows")


def test_dry_run_failure_path():
    print("test_dry_run_failure_path:")
    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, PYTHONPATH=str(HARNESS))
        cfg = Path(d) / "bench.toml"
        cfg.write_text(
            (HARNESS / "config" / "bench.example.toml").read_text()
            .replace('root = "./harness-runs"', f'root = "{d}/runs"')
            .replace('alert_command = []',
                     'alert_command = ["sh", "-c", '
                     f'"printf %s \\"$0\\" >> {d}/alerts.txt"]')
            .replace("duration_s = 43200", "duration_s = 4")
            .replace("assert_every_s = 300", "assert_every_s = 2")
            .replace("rounds = 8", "rounds = 2"))
        r = subprocess.run(
            [sys.executable, "-m", "milanharness", "--config", str(cfg),
             "--dry-run", "--dry-run-fault", "known_good:media-plane",
             "--new", "--phases", "baseline,smoke,counters"],
            capture_output=True, text=True, env=env, cwd=str(HARNESS),
            timeout=600)
        root = Path(d) / "runs"
        runs = sorted(p.name for p in root.iterdir())
        run = logmod.RunDir(root, runs[-1])
        state, reason = run.status()
        check(state == "FAILED", "injected fault drives STATUS to FAILED",
              reason[:80], f"STATUS was {state!r}")
        recs = run.read_records()
        fails = [x for x in recs if x["verdict"] == "FAIL"]
        alerts = [x for x in recs if x.get("kind") == "alert"]
        check(len(fails) >= 1, "the fault is recorded as FAIL",
              f"{len(fails)} FAIL record(s)")
        check(len(alerts) == 1, "exactly ONE alert for the whole run",
              "a single defect must not produce a hundred messages",
              f"{len(alerts)} alert records")
        bundles = list((run.dir / "forensics").iterdir())
        check(len(bundles) == 1, "one forensic bundle, on the first failure",
              f"{[b.name for b in bundles]}")
        if bundles:
            payload = json.loads((bundles[0] / "failure.json").read_text())
            for key in ("item", "reason", "seed", "phase", "boards"):
                if key not in payload:
                    bad("forensic bundle content", f"missing {key!r}")
                    break
            else:
                ok("forensic bundle carries item, reason, seed and both boards' CSRs",
                   f"{len(payload['boards'])} board snapshot(s)")
            check((bundles[0] / "harness.log.tail").is_file()
                  and (bundles[0] / "records.tail.jsonl").is_file(),
                  "forensic bundle stands alone",
                  "log tail + record tail captured with it")
        alert_file = Path(d) / "alerts.txt"
        if alert_file.is_file():
            body = alert_file.read_text().strip()
            check(body.startswith("milan campaign FAILED:"),
                  "the alert body reaches the channel in the documented shape",
                  body[:70])
        blocked = [x for x in recs if x["verdict"] == "BLOCKED"]
        check(bool(blocked) and len(alerts) == 1,
              "BLOCKED items never raise an alert",
              f"{len(blocked)} blocked, still exactly 1 alert")

        # The report must be reconstructable from the JSONL alone.
        model = reportmod.build(recs)
        md = reportmod.render(model, run_id=run.rid)
        check("FAILED" in md and "## Counter audit" in md,
              "report rebuilt from the records alone",
              f"{len(md.splitlines())} lines")
        check("Milan validated" not in md,
              "a failing run does not claim the verdict line",
              "the verdict line is reserved for an all-pass run")


def test_transport_outage():
    print("test_transport_outage:")
    class C:
        def __init__(self):
            self.d = {
                "exec": {"ssh": "ssh", "ssh_opts": [], "command_timeout_s": 5},
                "retry": {"attempts": 3, "backoff_initial_s": 0.001,
                          "backoff_max_s": 0.002, "outage_budget_s": 100},
                "jump": {"host": "jump"},
            }
        def section(self, n):
            return self.d[n]
        def get(self, s, k, default=None):
            return self.d[s].get(k, default)

    seen = []
    mock = MockBench(faults={"outage": 2})
    t = Transport(C(), on_outage=seen.append, runner=mock)
    r = t.run("board", "devmem 0x90000000 32")
    check(r.ok and len(seen) == 2,
          "a transient outage is survived, not aborted on",
          f"{len(seen)} retries recorded, then success")

    mock2 = MockBench(faults={"outage": 99})
    t2 = Transport(C(), on_outage=lambda *_: None, runner=mock2)
    try:
        t2.run("board", "devmem 0x90000000 32")
        bad("a persistent outage raises Outage", "no exception")
    except Outage as exc:
        check("unreachable" in str(exc), "a persistent outage raises Outage",
              "-> the runner marks the item BLOCKED, never FAILED")

    # Batching: a snapshot must cost ONE remote process, not one per register.
    mock3 = MockBench()
    t3 = Transport(C(), runner=mock3)
    from milanharness.config import Board
    b = Board(name="m", ssh="m", via_jump=False, role="listener",
              csr_base=0x90000000, datapath_clk_hz=100_000_000,
              version_expect=0x00010013, n_listeners=1, n_talkers=1,
              pcm_ring_csr=0, mac_loopback_csr=0, dma_ts_offset_csr=0,
              alsa_capture_device="", alsa_capture_channels=2,
              user_mtd_mount="", power_outlet=-1, netif="eth0")
    before = len(mock3.calls)
    snap = csrmod.Csr(t3, b).snapshot()
    check(len(mock3.calls) - before == 1 and len(snap.words) > 100,
          "a full snapshot is ONE remote call",
          f"{len(snap.words)} registers in {len(mock3.calls) - before} call(s)",
          "batching is the design, not an optimisation: ~0.75 s per devmem")


def main() -> int:
    for fn in (test_config, test_registry, test_thdn, test_latency,
               test_jsonl_and_resume, test_notify, test_counters_table,
               test_csr_and_safety, test_board_scripts, test_transport_outage,
               test_dry_run, test_dry_run_failure_path):
        try:
            fn()
        except Exception as exc:                       # noqa: BLE001
            import traceback
            bad(fn.__name__, f"gate crashed: {exc}\n{traceback.format_exc()}")
    print()
    if SKIPPED:
        print(f"SKIPPED ({len(SKIPPED)}): " + " | ".join(SKIPPED))
    if FAILURES:
        print(f"{len(FAILURES)} GATE(S) FAILED")
        return 1
    print("ALL GATES PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
