# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Issue #582: enforce the clock contract and derive configured clock uses."""
import contextlib
import copy
import io
import os
from pathlib import Path
import re
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
            no_flash = copy.deepcopy(raw)
            no_flash["board"]["constraints"]["flashboot"] = "none"
            no_flash_path = directory / "no_flash.yaml"
            no_flash_path.write_text(yaml.safe_dump(no_flash))
            assert eb.load_config(no_flash_path)["constraints"]["flashboot"] == "none"
            # Issue #582 names both formerly accepted clock regressions.
            # Neighbours ensure equality is enforced, rather than a ceiling.
            for bad_hz in (100_000_000, 80_000_000, clock - 1, clock + 1, 0):
                bad = copy.deepcopy(raw)
                bad["board"]["constraints"].update(milan_clk_hz=bad_hz, sys_clk_hz=100_000_000)
                _refused(bad, directory, "baremetal clock: milan_clk_hz must be "
                         f"{clock} Hz (docs/integration/BAREMETAL_FIRMWARE.md build contract)")
                refusals += 1
                bad["board"]["constraints"]["flashboot"] = "none"
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


def test_gptp_rom_clock() -> None:
    """Compare builder ROM bytes with an independent configured-clock run."""
    generator = ROOT / "gptp-processor/hdl/ucode/gen_gptp_ucode.py"
    with tempfile.TemporaryDirectory(prefix="gptp-rom-clock-") as tmp:
        directory = Path(tmp)
        for path in CONFIGS:
            cfg = eb.load_config(path)
            result = eb.build(path, directory, write_fragment=False)
            actual = Path(result["paths"]["gptp_ucode"]).read_bytes()
            expected_path = directory / "expected.hex"
            command = [sys.executable, str(generator), "-o", str(expected_path),
                       "--mac", "0x" + cfg["platform"]["mac_address"].replace(":", ""),
                       "--p1", str(cfg["gptp"]["priority1"])]
            clocks = cfg["constraints"]
            subprocess.run(command + ["--clk-hz", str(clocks["milan_clk_hz"])],
                           check=True, capture_output=True, text=True, timeout=60)
            expected = expected_path.read_bytes()
            assert actual == expected, f"{path.stem}: gPTP ROM does not use configured Milan clock"
            # Controls must change bytes, not merely the argv.
            wrong_clocks = [[]]
            if clocks["sys_clk_hz"] == clocks["milan_clk_hz"]:
                print(f"[clock contract] {path.stem}: SKIP system-clock control: "
                      "sys_clk_hz == milan_clk_hz")
            else:
                wrong_clocks.append(["--clk-hz", str(clocks["sys_clk_hz"])])
            for wrong_args in wrong_clocks:
                subprocess.run(command + wrong_args, check=True, capture_output=True, text=True, timeout=60)
                assert expected_path.read_bytes() != expected, f"{path.stem}: ROM clock control is insensitive"
    print(f"[clock contract] {len(CONFIGS)} ROMs match configured Milan clocks; "
          "applicable default-clock and system-clock controls differ")


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
        argv = eb.emit_soc_argv(cfg) + ["--entity-gen-dir", str(ROOT / "configs/generated" / path.stem)]
        _soc_clock_case(milan_soc, argv, False)
        for bad in (eb.BAREMETAL_CLK_HZ - 1, eb.BAREMETAL_CLK_HZ + 1, 80_000_000, 100_000_000):
            bad_argv = list(argv)
            bad_argv[bad_argv.index("--milan-clk-freq") + 1] = str(bad)
            _soc_clock_case(milan_soc, bad_argv, True)
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
    _soc_clock_case(milan_soc, ["--no-milan", "--milan-clk-freq", str(clock)], False)
    _soc_clock_case(milan_soc, ["--no-milan", "--sys-clk-freq", str(clock)], False)
    for bad in (clock - 1, clock + 1, 80_000_000, 100_000_000):
        for option in ("--milan-clk-freq", "--sys-clk-freq"):
            _soc_clock_case(milan_soc, ["--no-milan", option, str(bad)], True)
    print("[clock contract] SoC configured clocks, neighbours, 80/100 MHz, "
          "nonfinite values, product argv, no-Milan, implicit system and disabled-domain paths pass")


def _sweep(board: str, config: Path | None = None, argv: list[str] | None = None) -> subprocess.CompletedProcess:
    """Run sweep_extra.sh under an empty HOME, where no Vivado or work tree can be reached."""
    env = dict(os.environ)
    env.pop("SWEEP_CFG", None)
    if config is not None:
        env["SWEEP_CFG"] = str(config)
    with tempfile.TemporaryDirectory(prefix="sweep-home-") as home:
        env["HOME"] = home
        result = subprocess.run(["bash", str(ROOT / "sw/litex/sweep_extra.sh"),
                                 *(argv or [board, "clock-test", "--dry-run"])],
                                cwd=ROOT, env=env, text=True, capture_output=True, timeout=60)
        assert not any(Path(home).iterdir()), f"sweep_extra.sh wrote under HOME: {result.stdout}"
    assert "LAUNCHED" not in result.stdout, result.stdout
    return result


def _assert_sweep_clocks(result: subprocess.CompletedProcess, config: Path) -> None:
    """Compare the preview with normalized clocks, including board defaults, and its entity inputs."""
    assert result.returncode == 0, result.stderr
    clocks = eb.load_config(config)["constraints"]
    argv = shlex.split(result.stdout)
    for option, key in (("--sys-clk-freq", "sys_clk_hz"), ("--milan-clk-freq", "milan_clk_hz")):
        assert argv.count(option) == 1, argv
        assert float(argv[argv.index(option) + 1]) == clocks[key], (option, argv)
    # The SoC finds the builder output by this directory's name and includes its gen/.
    assert argv.count("--entity-gen-dir") == 1, argv
    gen = Path(argv[argv.index("--entity-gen-dir") + 1])
    assert gen.name == config.stem, (gen, config)
    if config in CONFIGS:
        definition = gen / "gen/adp_shape_defaults.svh"
        assert config.name in definition.read_text(), f"{definition} does not name {config.name}"


def test_extra_sweep_clocks() -> None:
    """The real shell command follows defaults and changed configuration clocks."""
    for board, name in (("arty", "endstation_arty_4x4"), ("ax7101", "endstation_ax7101_1x1_tdm8")):
        _assert_sweep_clocks(_sweep(board), ROOT / "configs" / f"{name}.yaml")
    for path in CONFIGS:
        cfg = eb.load_config(path)
        _assert_sweep_clocks(_sweep(cfg["board_target"], path), path)
    with tempfile.TemporaryDirectory(prefix="sweep-clock-") as tmp:
        path = Path(tmp) / "clock variant.yaml"
        raw = yaml.safe_load(CONFIGS[0].read_text())
        raw["board"]["constraints"]["sys_clk_hz"] = 75_000_000
        path.write_text(yaml.safe_dump(raw))
        board = raw["board"]["target"]
        _assert_sweep_clocks(_sweep(board, path), path)
        del raw["board"]["constraints"]["sys_clk_hz"]
        path.write_text(yaml.safe_dump(raw))
        _assert_sweep_clocks(_sweep(board, path), path)
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
          "omitted system clock, board mismatch, invalid clock and missing configuration pass")


def test_extra_sweep_invocation() -> None:
    """--dry-run is honoured in any position; a bad argument list is refused before any launch."""
    config = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
    # The middle order was read as tag "--dry-run" and launched three builds.
    for argv in (["--dry-run", "ax7101", "order"], ["ax7101", "--dry-run", "order"],
                 ["ax7101", "order", "--dry-run"]):
        _assert_sweep_clocks(_sweep("ax7101", argv=argv), config)
    for argv, reason in ((["ax7101", "--dry-run"], "expected a board and a tag, got 1"),
                         (["ax7101", "order", "extra", "--dry-run"], "expected a board and a tag, got 3"),
                         (["ax7101", "order", "--dryrun"], "unknown option --dryrun"),
                         (["--dry-run", "ax7101", ""], "empty tag"),
                         (["--dry-run", "zynq", "order"], "unknown board zynq")):
        result = _sweep("ax7101", argv=argv)
        assert result.returncode == 2 and reason in result.stderr, (argv, result.stderr)
    # A launch builds first; a configuration outside configs/ gets no generated
    # entity directory, so the SoC would include the tracked shape instead.
    with tempfile.TemporaryDirectory(prefix="sweep-variant-") as tmp:
        variant = Path(tmp) / "sweep variant.yaml"
        variant.write_text(config.read_text())
        result = _sweep("ax7101", variant, ["ax7101", "order"])
        assert result.returncode != 0 and "wrote its entity definition to" in result.stderr, result.stderr
    # The build interpreter reads the configuration, as sweep.sh's setup_env arranges.
    script = ROOT / "sw/litex/sweep_extra.sh"
    venv = re.search(r'export PATH="\$HOME/([^"$:]+):\$PATH"', script.read_text())
    assert venv, "sweep_extra.sh exports no build interpreter"
    with tempfile.TemporaryDirectory(prefix="sweep-venv-") as home:
        marker = Path(home) / "interpreter-used"
        interpreter = Path(home) / venv[1] / "python3"
        interpreter.parent.mkdir(parents=True)
        interpreter.write_text(f'#!/bin/sh\ntouch "{marker}"\nexec "{sys.executable}" "$@"\n')
        interpreter.chmod(0o755)
        env = {key: value for key, value in os.environ.items() if key != "SWEEP_CFG"}
        result = subprocess.run(["bash", str(script), "--dry-run", "ax7101", "order"], cwd=ROOT,
                                env=dict(env, HOME=home), text=True, capture_output=True, timeout=60)
        assert result.returncode == 0 and marker.exists(), "configuration not read by the build interpreter"
    print("[clock contract] extra sweep: --dry-run in every position previews; missing, extra, "
          "unknown and empty arguments refuse before launching; an ungenerated entity refuses a launch; "
          "the build interpreter reads the configuration")


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


def _ax_gptp_dry_run(recipe: Path | None) -> subprocess.CompletedProcess:
    """The commands `make ax1x1gptp` would run, expanded by make itself."""
    command = ["make", "-s", "-n", "-B", "-C", str(ROOT / "tb/verilator/milan_dp"), "ax1x1gptp"]
    if recipe is not None:
        command.append(f"CLOCK_RECIPE={recipe}")
    return subprocess.run(command, text=True, capture_output=True, timeout=120)


def test_sim_clock() -> None:
    """The AX 1x1 physical-rate simulation takes every clock use from the contract."""
    with tempfile.TemporaryDirectory(prefix="sim-clock-") as tmp:
        planted = Path(tmp) / "recipe.py"
        planted_hz = eb.BAREMETAL_CLK_HZ + 1
        planted.write_text(f"CPU_HZ = {planted_hz}\n")
        # The planted recipe proves derivation: a literal would keep the contract value.
        for recipe, hz in ((None, eb.BAREMETAL_CLK_HZ), (planted, planted_hz)):
            result = _ax_gptp_dry_run(recipe)
            assert result.returncode == 0, result.stderr
            for use in (f"--clk-hz {hz} ", f"-GMILAN_CLK_FREQ_HZ={hz} ", f"-DMILAN_CLK_HZ_TB={hz} "):
                assert result.stdout.count(use) == 1, f"make ax1x1gptp does not pass {use.strip()}"
        absent = _ax_gptp_dry_run(Path(tmp) / "absent.py")
        assert absent.returncode != 0 and "did not yield CPU_HZ" in absent.stderr, absent.stderr
    source = (ROOT / "tb/verilator/milan_dp/sim_ax1x1gptp.cpp").read_text()
    assert "constexpr uint64_t kHz = MILAN_CLK_HZ_TB;" in source, "harness clock is not the Makefile's"
    for spelling in (str(eb.BAREMETAL_CLK_HZ), f"{eb.BAREMETAL_CLK_HZ / 1e6:g} MHz"):
        assert spelling not in source, f"sim_ax1x1gptp.cpp restates the contract clock as {spelling!r}"
    print("[clock contract] AX 1x1 gPTP simulation: ROM, elaboration and harness clocks follow "
          "the contract and a planted recipe; an unreadable recipe is refused; the harness "
          "restates no clock")


if __name__ == "__main__":
    test_baremetal_clock_contract()
    test_gptp_rom_clock()
    test_extra_sweep_clocks()
    test_extra_sweep_invocation()
    test_tap_clock_docs()
    test_sim_clock()
    if "--soc" in sys.argv:
        test_soc_clock_contract()
