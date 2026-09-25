#!/usr/bin/env python3
"""Fault probes for scripts/check-integrator-params.py on disposable copies.

Usage: probe-checker.py <clone-dir> <scratch-dir>
Each probe mutates a copy of the top, guide or diagram, runs the checker with
--top/--guide/--diagram pointing at the copies, and compares the exit code and
required message fragments with the expectation. Prints one line per probe.
"""
import re, shutil, subprocess, sys
from pathlib import Path

clone, scratch = Path(sys.argv[1]), Path(sys.argv[2])
checker = clone / "scripts/check-integrator-params.py"
src = {"top": clone / "hdl/top/protocol_processor_top.sv",
       "guide": clone / "docs/guides/integrator.md",
       "diagram": clone / "docs/diagrams/21-integration-faces.svg"}
text = {k: p.read_text(encoding="utf-8") for k, p in src.items()}

def sub(s, old, new, count=1):
    assert old in s, f"anchor not found: {old!r}"
    return s.replace(old, new, count)

def guide_row(name):
    return re.search(r"^\| `%s` \|.*\n" % name, text["guide"], re.M)[0]

def svg_line(name):
    return re.search(r"^.*<text[^>]*>[^<]*\b%s\b[^<]*</text>\n" % name, text["diagram"], re.M)[0]

T, G, D = text["top"], text["guide"], text["diagram"]
REGTL = "    parameter int unsigned REG_TL_TIMEOUT_MS_P = 300_000,\n"
probes = [
  # id, target, mutated text, expected rc, required fragments
  ("baseline", None, None, 0, ["top 24, guide 24, diagram 24, OK"]),
  ("top-remove", "top", sub(T, REGTL, ""), 1,
   ["guide: extra REG_TL_TIMEOUT_MS_P", "diagram: extra REG_TL_TIMEOUT_MS_P"]),
  ("top-add", "top", sub(T, "    parameter logic [15:0] SRP_DOM_DEF_VID_P   = 16'd2,\n",
     "    parameter logic [15:0] SRP_DOM_DEF_VID_P   = 16'd2,\n    parameter int unsigned NEW_KNOB_P = 3,\n"), 1,
   ["guide: missing NEW_KNOB_P", "diagram: missing NEW_KNOB_P"]),
  ("top-add-after-localparams", "top", sub(T, "$clog2(TX_OVERSIZE_BYTES_P + 1)  // 11\n) (",
     "$clog2(TX_OVERSIZE_BYTES_P + 1),  // 11\n    parameter int unsigned LATE_P = 1\n) ("), 1,
   ["guide: missing LATE_P", "diagram: missing LATE_P"]),
  ("top-add-list-continuation", "top", sub(T, "    parameter int unsigned LOCK_TIMEOUT_MS_P   = 60_000,\n",
     "    parameter int unsigned LOCK_TIMEOUT_MS_P   = 60_000, CONT_P = 2,\n"), 1,
   ["guide: missing CONT_P", "diagram: missing CONT_P"]),
  ("top-rename", "top", sub(T, "LOCK_TIMEOUT_MS_P   = 60_000", "LOCK_TMO_MS_P   = 60_000"), 1,
   ["guide: missing LOCK_TMO_MS_P", "guide: extra LOCK_TIMEOUT_MS_P", "diagram: extra LOCK_TIMEOUT_MS_P"]),
  ("top-line-comment", "top", sub(T, REGTL, "    // " + REGTL.lstrip()), 1, ["guide: extra REG_TL_TIMEOUT_MS_P"]),
  ("top-block-comment-extra", "top", sub(T, REGTL, REGTL + "    /* parameter int unsigned GHOST_P = 1, */\n"), 0, ["OK"]),
  ("top-string-punct", "top", sub(T, '"ltn_rom.hex"', '"a,b)(c=/*d*/.hex"'), 0, ["OK"]),
  ("top-dup", "top", sub(T, REGTL, REGTL + REGTL), 1, ["top: duplicate REG_TL_TIMEOUT_MS_P"]),
  ("top-no-header", "top", sub(T, "  import pp_pkg::*;\n#(", "  import pp_pkg::*;\n//#(").replace(") (\n    input  wire         clk_i", "(\n    input  wire         clk_i", 1), 1, ["top:"]),
  ("top-unterminated", "top", T[:T.index("    localparam pp_timer_map_t TMR_MAP_C")], 1, ["top: unterminated parameter header"]),
  ("top-garbage-decl", "top", sub(T, REGTL, "    parameter int unsigned 300_000,\n"), 1, ["top: cannot parse declaration"]),
  ("top-empty-inventory", "top", re.sub(r"\bparameter\b(?=\s+(int|string|logic))", "localparam", T), 1,
   ["top: parsed no parameters"]),
  ("top-missing-file", "top", None, 1, ["top:"]),
  ("guide-missing-row", "guide", sub(G, guide_row("N_CONTROL_P"), ""), 1, ["guide: missing N_CONTROL_P"]),
  ("guide-extra-row", "guide", sub(G, guide_row("SRP_DOM_DEF_VID_P"), guide_row("SRP_DOM_DEF_VID_P") + "| `EXTRA_KNOB_P` | x | y |\n"), 1,
   ["guide: extra EXTRA_KNOB_P"]),
  ("guide-dup-row", "guide", sub(G, guide_row("CLK_HZ_P"), guide_row("CLK_HZ_P") * 2), 1, ["guide: duplicate CLK_HZ_P (2 occurrences)"]),
  ("guide-row-commented", "guide", sub(G, guide_row("N_CONTROL_P"), "<!--\n" + guide_row("N_CONTROL_P") + "-->\n"), 1,
   ["guide: missing N_CONTROL_P"]),
  ("guide-row-fenced", "guide", sub(G, guide_row("N_CONTROL_P"), "```\n" + guide_row("N_CONTROL_P") + "```\n"), 1,
   ["guide: missing N_CONTROL_P"]),
  ("guide-row-unticked", "guide", sub(G, "| `N_CONTROL_P` |", "| N_CONTROL_P |"), 1, ["guide: missing N_CONTROL_P"]),
  ("guide-name-in-later-column-only", "guide", sub(G, "| `N_CONTROL_P` |", "| (see) | `N_CONTROL_P` |"), 1,
   ["guide: missing N_CONTROL_P"]),
  ("guide-row-outside-section2", "guide", sub(G, guide_row("N_CONTROL_P"), "").replace(re.search(r"^## 3\..*\n", G, re.M)[0], re.search(r"^## 3\..*\n", G, re.M)[0] + "\n| `N_CONTROL_P` | x | y |\n", 1), 1,
   ["guide: missing N_CONTROL_P"]),
  ("guide-empty-inventory", "guide", re.sub(r"^\| `[A-Z_]+_P` \|.*\n", "", G, flags=re.M), 1,
   ["guide: parsed no parameters"]),
  ("guide-no-section", "guide", sub(G, "## 2. Parameters", "## 2. Knobs"), 1, ["guide: cannot find section 2"]),
  ("diagram-missing", "diagram", sub(D, "CLK_HZ_P · TIM_DIV_US_P", "TIM_DIV_US_P"), 1, ["diagram: missing CLK_HZ_P"]),
  ("diagram-extra", "diagram", sub(D, "<text x=\"464\" y=\"560\">SRP_DOM_DEF_VID_P</text>",
     "<text x=\"464\" y=\"560\">SRP_DOM_DEF_VID_P · EXTRA_KNOB_P</text>"), 1, ["diagram: extra EXTRA_KNOB_P"]),
  ("diagram-dup", "diagram", sub(D, "<text x=\"464\" y=\"560\">SRP_DOM_DEF_VID_P</text>",
     "<text x=\"464\" y=\"560\">SRP_DOM_DEF_VID_P · CLK_HZ_P</text>"), 1, ["diagram: duplicate CLK_HZ_P (2 occurrences)"]),
  ("diagram-outside-group", "diagram", sub(D, svg_line("NVM_RS_TMO_CYC_P"), "").replace("  </g>\n  <a href", "  </g>\n  <text x=\"1\" y=\"1\">NVM_RS_TMO_CYC_P</text>\n  <a href", 1), 1,
   ["diagram: missing NVM_RS_TMO_CYC_P"]),
  ("diagram-xml-comment", "diagram", sub(D, svg_line("NVM_RS_TMO_CYC_P"), "<!-- " + svg_line("NVM_RS_TMO_CYC_P").strip() + " -->\n"), 1,
   ["diagram: missing NVM_RS_TMO_CYC_P"]),
  ("diagram-no-group", "diagram", sub(D, 'id="integration-parameters"', 'id="other"'), 1, ["expected one integration-parameters inventory group"]),
  ("diagram-two-groups", "diagram", sub(D, "  <!-- ===== LEFT ===== -->", "  <g id=\"integration-parameters\"/>\n  <!-- ===== LEFT ===== -->"), 1,
   ["expected one integration-parameters inventory group"]),
  ("diagram-empty-inventory", "diagram", re.sub(r"(<g id=\"integration-parameters\"[^>]*>).*?(</g>)", r"\1\2", D, flags=re.S), 1,
   ["diagram: parsed no parameters"]),
  ("diagram-malformed", "diagram", D.replace("</svg>", ""), 1, ["diagram:"]),
  # Limits (informational): the checker's word "visible" is not enforced.
  ("LIMIT-diagram-hidden-text", "diagram", sub(D, svg_line("NVM_RS_TMO_CYC_P"), svg_line("NVM_RS_TMO_CYC_P").replace("<text ", "<text display=\"none\" ")), 0, ["OK"]),
]

work = scratch / "probe"; shutil.rmtree(work, ignore_errors=True); work.mkdir(parents=True)
fails = 0
for pid, target, mutated, rc_exp, frags in probes:
    paths = dict(src)
    if target:
        p = work / f"{pid}.{src[target].suffix.lstrip('.')}"
        if mutated is not None:
            p.write_text(mutated, encoding="utf-8")
        paths[target] = p
    r = subprocess.run([sys.executable, str(checker), "--top", str(paths["top"]),
                        "--guide", str(paths["guide"]), "--diagram", str(paths["diagram"])],
                       capture_output=True, text=True)
    out = r.stdout + r.stderr
    ok = r.returncode == rc_exp and all(f in out for f in frags) and "Traceback" not in out
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} {pid}: rc={r.returncode} expected={rc_exp} | " + " / ".join(out.strip().splitlines()))
print(f"probes: {len(probes)}, unexpected: {fails}")
sys.exit(1 if fails else 0)
