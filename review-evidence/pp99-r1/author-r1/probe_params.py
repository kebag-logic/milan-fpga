from pathlib import Path
import subprocess

out = Path(__file__).resolve().parent
repo = Path("$LANES/pp99-integrator-params")
guide = (repo / "docs/guides/integrator.md").read_text()
top = (repo / "hdl/top/protocol_processor_top.sv").read_text()
diagram = (repo / "docs/diagrams/21-integration-faces.svg").read_text()
row = next(line for line in guide.splitlines() if line.startswith("| `N_CONTROL_P` |"))
first = "    parameter int unsigned N_STREAM_IN_P       = 8,"

def probe(label, arg, body, expected, diagnostic=None):
    path = out / (label + {"--guide": ".md", "--top": ".sv", "--diagram": ".svg"}[arg])
    path.write_text(body)
    result = subprocess.run(["rtk", "proxy", "python3", "scripts/check-integrator-params.py", arg, str(path)],
                            cwd=repo, capture_output=True, text=True, timeout=120)
    print(f"{label}: rc {result.returncode}, expected {expected}")
    print(result.stdout.strip())
    assert result.returncode == expected, result.stderr
    if diagnostic:
        assert diagnostic in result.stdout

probe("missing-row-still-mentioned", "--guide", guide.replace(row, "") + "\n`N_CONTROL_P` remains mentioned outside the inventory.\n", 1, "guide: missing N_CONTROL_P")
probe("extra-guide-row", "--guide", guide.replace(row, row + "\n| `EXTRA_P` | test | test |"), 1, "guide: extra EXTRA_P")
probe("duplicate-guide-row", "--guide", guide.replace(row, row + "\n" + row), 1, "guide: duplicate N_CONTROL_P")
probe("new-top-param", "--top", top.replace(first, first + "\n    parameter int unsigned EXTRA_P = 1,"), 1, "guide: missing EXTRA_P")
probe("removed-top-param", "--top", top.replace(first, ""), 1, "guide: extra N_STREAM_IN_P")
probe("comments-localparams-grouped", "--top", top.replace(first, "    // parameter int GHOST_P = 1,\n    /* parameter int BLOCK_P = 1, */\n    localparam int DERIVED_P = fn(1, (2 + 3)),\n" + first).replace("parameter int unsigned N_CLK_DOMAIN_P", "N_CLK_DOMAIN_P").replace('"ltn_rom.hex"', '\"file,(x)//parameter_FAKE_P.hex\"'), 0)
probe("empty-guide-inventory", "--guide", "## 2. Parameters\n\n## 3. Other\n", 1, "guide: parsed no parameters")
probe("unparseable-top", "--top", "module unrelated; endmodule\n", 1, "cannot find protocol_processor_top")
probe("missing-diagram-param", "--diagram", diagram.replace("N_AUDIO_UNIT_P · ", ""), 1, "diagram: missing N_AUDIO_UNIT_P")
probe("extra-diagram-param", "--diagram", diagram.replace("N_AUDIO_UNIT_P · ", "EXTRA_P · N_AUDIO_UNIT_P · "), 1, "diagram: extra EXTRA_P")
probe("duplicate-diagram-param", "--diagram", diagram.replace("N_AUDIO_UNIT_P · ", "N_AUDIO_UNIT_P · N_AUDIO_UNIT_P · "), 1, "diagram: duplicate N_AUDIO_UNIT_P")
print("All parameter gate probes passed.")
