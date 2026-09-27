"""Reproduce the bounded issue #582 mutations; restore each source in finally."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path.cwd().resolve()
PYTHON = sys.executable
TEST = "import sys; sys.path.insert(0, 'sw/builder'); import test_clock_contract as t; t.{}()"
PAIRS = "import sys; sys.path.insert(0, 'sw/litex'); import test_pp_mem_bridge as t; t.test_configured_clock_pairs()"
CASES = [
    ("builder guard removed", "sw/builder/endstation_builder.py",
     'if cons["milan_clk_hz"] != BAREMETAL_CLK_HZ:',
     'if False and cons["milan_clk_hz"] != BAREMETAL_CLK_HZ:',
     TEST.format("test_baremetal_clock_contract"), "accepted invalid input: baremetal clock"),
    ("builder equality becomes ceiling", "sw/builder/endstation_builder.py",
     'if cons["milan_clk_hz"] != BAREMETAL_CLK_HZ:',
     'if cons["milan_clk_hz"] > BAREMETAL_CLK_HZ:',
     TEST.format("test_baremetal_clock_contract"), "accepted invalid input: baremetal clock"),
    ("Scala message narrows to cache", "sw/builder/endstation_builder.py",
     "no scala_args overrides", "no cache/prefetch scala_args",
     TEST.format("test_baremetal_clock_contract"), "no cache/prefetch scala_args"),
    ("SoC guard removed", "sw/litex/milan_soc.py",
     "if (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:",
     "if False and (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:",
     TEST.format("test_soc_clock_contract"), "clock accepted before platform"),
    ("SoC equality becomes ceiling", "sw/litex/milan_soc.py",
     "if (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:",
     "if (args.milan_clk_freq or args.sys_clk_freq) > BAREMETAL_CLK_HZ:",
     TEST.format("test_soc_clock_contract"), "clock accepted before platform"),
    ("SoC system fallback bypassed", "sw/litex/milan_soc.py",
     "if (args.milan_clk_freq or args.sys_clk_freq) != BAREMETAL_CLK_HZ:",
     "if (args.milan_clk_freq or BAREMETAL_CLK_HZ) != BAREMETAL_CLK_HZ:",
     TEST.format("test_soc_clock_contract"), "clock accepted before platform"),
    ("sweep Milan clock copied", "sw/litex/sweep_extra.sh",
     "{c['milan_clk_hz']}", "100000000",
     TEST.format("test_extra_sweep_clocks"), "AssertionError"),
    ("sweep system clock copied", "sw/litex/sweep_extra.sh",
     "{c['sys_clk_hz']}", "100000000",
     TEST.format("test_extra_sweep_clocks"), "AssertionError"),
    ("watchdog domains swapped", "sw/litex/test_pp_mem_bridge.py",
     'pairs.append((path.stem, clocks["sys_clk_hz"], clocks["milan_clk_hz"]))',
     'pairs.append((path.stem, clocks["milan_clk_hz"], clocks["sys_clk_hz"]))',
     PAIRS, "configuration clock pairs not preserved"),
    ("watchdog clock copied", "sw/litex/test_pp_mem_bridge.py",
     'pairs.append((path.stem, clocks["sys_clk_hz"], clocks["milan_clk_hz"]))',
     'pairs.append((path.stem, clocks["sys_clk_hz"], 100_000_000))',
     PAIRS, "configuration clock pairs not preserved"),
    ("tap conversion retains old clock", "docs/AAF_LATENCY_TAPS.md",
     "| `endstation_ax7101_1x1_tdm8` | 50000000 | 20 | present |",
     "| `endstation_ax7101_1x1_tdm8` | 50000000 | 10 | present |",
     TEST.format("test_tap_clock_docs"), "tap clock table differs"),
]
results = []
with tempfile.TemporaryDirectory(prefix="clock-mutants-") as tmp:
    for index, (name, filename, old, new, test, diagnostic) in enumerate(CASES):
        path = ROOT / filename
        original = path.read_bytes()
        text = original.decode()
        assert text.count(old) == 1, (name, text.count(old))
        try:
            path.write_text(text.replace(old, new))
            result = subprocess.run([PYTHON, "-X", f"pycache_prefix={tmp}/{index}", "-c", test],
                                    cwd=ROOT, text=True, capture_output=True, timeout=180)
            output = result.stdout + result.stderr
            assert result.returncode != 0 and diagnostic in output, (name, result.returncode, output)
            results.append({"mutant": name, "test": test.split("; ")[-1],
                            "returncode": result.returncode, "diagnostic": diagnostic})
            print(f"KILLED {name}: rc {result.returncode}; {diagnostic}", flush=True)
        finally:
            path.write_bytes(original)
print(json.dumps(results, indent=2))
