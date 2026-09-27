# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Issue #582: enforce the clock contract and derive configured clock uses."""
import contextlib
import copy
import io
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
from unittest.mock import patch

import yaml
import endstation_builder as eb

ROOT = Path(__file__).resolve().parents[2]
CONFIGS = sorted((ROOT / "configs").glob("endstation_*.yaml"))


def _refused(raw: dict, directory: Path, reason: str) -> None:
    """An invalid input must fail by name before producing any artifacts."""
    path = directory / "bad.yaml"
    path.write_text(yaml.safe_dump(raw))
    output = directory / "output"
    try:
        eb.build(path, output, write_fragment=False)
    except eb.ConfigError as exc:
        assert reason in str(exc), str(exc)
    else:
        raise AssertionError(f"accepted invalid input: {reason}")
    assert not output.exists(), "refused input wrote artifacts"


def test_baremetal_clock_contract() -> None:
    """Every tracked shape passes; faster, slower and adjacent clocks fail."""
    assert CONFIGS, "no end-station configurations found"
    refusals = 0
    with tempfile.TemporaryDirectory(prefix="baremetal-clock-") as tmp:
        directory = Path(tmp)
        for path in CONFIGS:
            raw = yaml.safe_load(path.read_text())
            cfg = eb.load_config(path)
            clock = raw["board"]["constraints"]["milan_clk_hz"]
            assert cfg["constraints"]["milan_clk_hz"] == eb.BAREMETAL_CLK_HZ == clock
            # Issue #582 names both formerly accepted clock regressions.
            # Neighbours ensure equality is enforced, rather than a ceiling.
            for bad_hz in (100_000_000, 80_000_000, clock - 1, clock + 1, 0):
                bad = copy.deepcopy(raw)
                bad["board"]["constraints"].update(milan_clk_hz=bad_hz, sys_clk_hz=100_000_000)
                _refused(bad, directory, "baremetal clock: milan_clk_hz must be "
                         f"{clock} Hz (docs/integration/BAREMETAL_FIRMWARE.md build contract)")
                refusals += 1
            bad = copy.deepcopy(raw)
            bad["board"]["constraints"]["sys_clk_hz"] = clock - 1
            _refused(bad, directory, "milan_clk_hz must not exceed sys_clk_hz")
            # The refusal covers every override, including a non-cache one.
            bad = copy.deepcopy(raw)
            bad.setdefault("soc", {})["scala_args"] = ["--unrelated-override"]
            _refused(bad, directory, "no scala_args overrides")
    print(f"[clock contract] {len(CONFIGS)} configured positives; {refusals} named clock refusals; "
          "system-clock ordering and non-cache Scala refusals; no output on failure")


def _soc_clock_case(soc, argv: list[str], refused: bool) -> None:
    class BeforePlatform(Exception):
        pass

    stderr = io.StringIO()
    with patch.object(sys, "argv", ["milan_soc.py", *argv]), contextlib.redirect_stderr(stderr), \
            patch.object(soc.board_audio_routing, "assert_front_end_routed", side_effect=BeforePlatform):
        try:
            soc.main()
        except BeforePlatform:
            assert not refused, f"clock accepted before platform: {argv}"
        except SystemExit as exc:
            assert refused and exc.code == 2, (argv, stderr.getvalue())
            assert "baremetal clock:" in stderr.getvalue(), stderr.getvalue()
            assert "BAREMETAL_FIRMWARE.md build contract" in stderr.getvalue(), stderr.getvalue()
        else:
            raise AssertionError("clock test did not reach the platform boundary")


def test_soc_clock_contract() -> None:
    """Execute the real CLI checks, stopping before any platform is built."""
    sys.path.insert(0, str(ROOT / "sw/litex"))
    import milan_soc

    for path in CONFIGS:
        cfg = eb.load_config(path)
        argv = eb.emit_soc_argv(cfg)
        _soc_clock_case(milan_soc, argv, False)
    clock = eb.BAREMETAL_CLK_HZ
    for bad in (clock - 1, clock + 1, 80_000_000, 100_000_000, -1, "nan", "inf"):
        _soc_clock_case(milan_soc, ["--milan-clk-freq", str(bad)], True)
    for bad in (80_000_000, 100_000_000):
        _soc_clock_case(milan_soc, ["--sys-clk-freq", str(bad)], True)
    _soc_clock_case(milan_soc, [], True)
    _soc_clock_case(milan_soc, ["--sys-clk-freq", str(clock)], False)
    # Zero disables the separate domain, just as in _CRG and the CPU binding.
    _soc_clock_case(milan_soc, ["--milan-clk-freq", "0"], True)
    _soc_clock_case(milan_soc, ["--sys-clk-freq", str(clock), "--milan-clk-freq", "0"], False)
    print("[clock contract] SoC configured clocks, neighbours, 80/100 MHz, "
          "nonfinite values, implicit system and disabled-domain paths pass")


def _sweep(board: str, config: Path | None = None) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.pop("SWEEP_CFG", None)
    if config is not None:
        env["SWEEP_CFG"] = str(config)
    return subprocess.run(["bash", str(ROOT / "sw/litex/sweep_extra.sh"), board, "clock-test", "--dry-run"],
                          cwd=ROOT, env=env, text=True, capture_output=True, timeout=60)


def _assert_sweep_clocks(result: subprocess.CompletedProcess, clocks: dict) -> None:
    assert result.returncode == 0, result.stderr
    argv = shlex.split(result.stdout)
    for option, key in (("--sys-clk-freq", "sys_clk_hz"), ("--milan-clk-freq", "milan_clk_hz")):
        assert argv.count(option) == 1, argv
        assert float(argv[argv.index(option) + 1]) == clocks[key], (option, argv)


def test_extra_sweep_clocks() -> None:
    """The real shell command follows defaults and changed configuration clocks."""
    for board, name in (("arty", "endstation_arty_4x4"), ("ax7101", "endstation_ax7101_1x1_tdm8")):
        raw = yaml.safe_load((ROOT / "configs" / f"{name}.yaml").read_text())
        _assert_sweep_clocks(_sweep(board), raw["board"]["constraints"])
    for path in CONFIGS:
        raw = yaml.safe_load(path.read_text())
        _assert_sweep_clocks(_sweep(raw["board"]["target"], path), raw["board"]["constraints"])
    with tempfile.TemporaryDirectory(prefix="sweep-clock-") as tmp:
        path = Path(tmp) / "clock variant.yaml"
        raw = yaml.safe_load(CONFIGS[0].read_text())
        raw["board"]["constraints"]["sys_clk_hz"] = 75_000_000
        path.write_text(yaml.safe_dump(raw))
        board = raw["board"]["target"]
        _assert_sweep_clocks(_sweep(board, path), raw["board"]["constraints"])
        mismatch = _sweep("ax7101" if board == "arty" else "arty", path)
        assert mismatch.returncode != 0 and "board does not match" in mismatch.stderr
        raw["board"]["constraints"]["milan_clk_hz"] = 80_000_000
        raw["board"]["constraints"]["sys_clk_hz"] = 100_000_000
        path.write_text(yaml.safe_dump(raw))
        bad = _sweep(board, path)
        assert bad.returncode != 0 and "baremetal clock:" in bad.stderr
        path.unlink()
        assert _sweep(board, path).returncode != 0, "missing configuration accepted"
    print("[clock contract] extra sweep: defaults, all configurations, changed system clock, "
          "board mismatch, invalid clock and missing configuration pass")


def test_tap_clock_docs() -> None:
    """The published cycle conversions follow each shape, including prunes."""
    text = (ROOT / "docs/AAF_LATENCY_TAPS.md").read_text()
    table = ["| Configuration | Milan clock (Hz) | ns/cycle | Latency taps |", "|---|---:|---:|---|"]
    for path in CONFIGS:
        raw = yaml.safe_load(path.read_text())
        hz = raw["board"]["constraints"]["milan_clk_hz"]
        present = raw["board"].get("features", {}).get("latency_taps", True)
        table.append(f"| `{path.stem}` | {hz} | {1e9 / hz:g} | {'present' if present else 'pruned'} |")
    actual = text.split("<!-- configured-tap-clocks:start -->\n", 1)[1].split(
        "\n<!-- configured-tap-clocks:end -->", 1)[0]
    assert actual == "\n".join(table), "tap clock table differs from the configurations"
    print(f"[clock contract] {len(CONFIGS)} tap conversions and presence declarations match configurations")


if __name__ == "__main__":
    test_baremetal_clock_contract()
    test_extra_sweep_clocks()
    test_tap_clock_docs()
    if "--soc" in sys.argv:
        test_soc_clock_contract()
