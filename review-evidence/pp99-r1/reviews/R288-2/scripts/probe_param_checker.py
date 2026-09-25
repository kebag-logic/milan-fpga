#!/usr/bin/env python3
"""Fault-injection probes for scripts/check-integrator-params.py.

Usage: probe_param_checker.py <repo-root-at-exact-head> <scratch-dir>

Copies the checker's three inputs into <scratch-dir>/<probe>/, applies one
mutation per probe, runs the UNMODIFIED checker from <repo-root> with
--top/--guide/--diagram pointing at the mutated copies, and records rc and
output. A probe PASSES when the checker's rc and diagnostic match the
expectation. Also runs each probe once through a full tree copy using the
checker's default paths (`make params`-equivalent) for the first control.
Exits 1 if any expectation is not met.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
SCRATCH = Path(sys.argv[2]).resolve()
CHECKER = ROOT / "scripts/check-integrator-params.py"
TOP = "hdl/top/protocol_processor_top.sv"
GUIDE = "docs/guides/integrator.md"
DIAG = "docs/diagrams/21-integration-faces.svg"


def once(text, old, new):
    assert text.count(old) >= 1, old
    return text.replace(old, new, 1)


# (name, file, mutate(text)->text, expected rc, regex that must appear)
PROBES = [
    ("baseline", None, None, 0, r"top 24, guide 24, diagram 24, OK"),
    # --- top-level parameter set is derived from the RTL
    ("top-remove-param", TOP,
     lambda t: re.sub(r"\n\s*parameter int unsigned N_CONTROL_P\s*= 1,", "", t, count=1),
     1, r"guide: extra N_CONTROL_P.*\n.*diagram: extra N_CONTROL_P|diagram: extra N_CONTROL_P"),
    ("top-add-param", TOP,
     lambda t: once(t, "    parameter logic [15:0] SRP_DOM_DEF_VID_P   = 16'd2,",
                    "    parameter logic [15:0] SRP_DOM_DEF_VID_P   = 16'd2,\n"
                    "    parameter int unsigned NEW_PROBE_P = 3,"),
     1, r"guide: missing NEW_PROBE_P[\s\S]*diagram: missing NEW_PROBE_P"),
    ("top-add-param-no-type-multi", TOP,
     lambda t: once(t, "    parameter int unsigned N_CONTROL_P         = 1,",
                    "    parameter int unsigned N_CONTROL_P         = 1, EXTRA_A_P = 2,\n"
                    "    parameter EXTRA_B_P = 4,"),
     1, r"guide: missing EXTRA_A_P[\s\S]*guide: missing EXTRA_B_P"),
    ("top-rename-param", TOP,
     lambda t: t.replace("LOCK_TIMEOUT_MS_P   = 60_000", "LOCK_TMO_MS_P = 60_000", 1),
     1, r"guide: missing LOCK_TMO_MS_P[\s\S]*guide: extra LOCK_TIMEOUT_MS_P"),
    ("top-param-to-localparam", TOP,
     lambda t: once(t, "    parameter logic [15:0] SRP_DOM_DEF_VID_P   = 16'd2,",
                    "    localparam logic [15:0] SRP_DOM_DEF_VID_P   = 16'd2,"),
     1, r"guide: extra SRP_DOM_DEF_VID_P"),
    ("top-param-in-comment-only", TOP,
     lambda t: once(t, "    //! derived — do not override",
                    "    // parameter int unsigned GHOST_P = 1,\n    //! derived — do not override"),
     0, r"top 24, guide 24, diagram 24, OK"),
    ("top-empty-inventory", TOP,
     lambda t: re.sub(r"\n\s*parameter\s[^\n]*", "", t),
     1, r"top: (parsed no parameters|cannot parse)"),
    ("top-unparseable-no-module", TOP,
     lambda t: t.replace("module protocol_processor_top", "module renamed_top", 1),
     1, r"top: cannot find protocol_processor_top parameter header"),
    ("top-unparseable-unterminated", TOP,
     lambda t: t.split("#(", 1)[0] + "#(\n    parameter int unsigned A_P = (1,\n",
     1, r"top: unterminated parameter header"),
    ("top-unparseable-declaration", TOP,
     lambda t: once(t, "    parameter int unsigned N_CONTROL_P         = 1,",
                    "    parameter int unsigned N_CONTROL_P         = 1,\n    garbage here,"),
     1, r"top: cannot parse declaration"),
    ("top-missing-file", "TOP-DELETE", None, 1, r"top: .*No such file"),
    # --- guide section 2 table
    ("guide-missing-row", GUIDE,
     lambda t: re.sub(r"\n\| `N_CLK_DOMAIN_P` \|[^\n]*", "", t, count=1),
     1, r"guide: missing N_CLK_DOMAIN_P"),
    ("guide-extra-row", GUIDE,
     lambda t: once(t, "| `N_STREAM_IN_P` |", "| `BOGUS_P` | x | y |\n| `N_STREAM_IN_P` |"),
     1, r"guide: extra BOGUS_P"),
    ("guide-duplicate-row", GUIDE,
     lambda t: once(t, "| `N_STREAM_IN_P` |", "| `RESP_BASE_P` | x | y |\n| `N_STREAM_IN_P` |"),
     1, r"guide: duplicate RESP_BASE_P \(2 occurrences\)"),
    ("guide-empty-inventory", GUIDE,
     lambda t: re.sub(r"\n\| `[A-Z_]+_P` \|[^\n]*", "", t),
     1, r"guide: parsed no parameters"),
    ("guide-no-section", GUIDE,
     lambda t: t.replace("## 2. Parameters", "## 2. Knobs", 1),
     1, r"guide: cannot find section 2"),
    ("guide-row-only-in-comment", GUIDE,
     lambda t: re.sub(r"\n(\| `N_CLK_DOMAIN_P` \|[^\n]*)", r"\n<!--\1-->", t, count=1),
     1, r"guide: missing N_CLK_DOMAIN_P"),
    ("guide-row-only-in-fence", GUIDE,
     lambda t: re.sub(r"\n(\| `N_CLK_DOMAIN_P` \|[^\n]*)", r"\n```\n\1\n```", t, count=1),
     1, r"guide: missing N_CLK_DOMAIN_P"),
    ("guide-name-only-outside-section2", GUIDE,
     lambda t: re.sub(r"\n\| `N_CLK_DOMAIN_P` \|[^\n]*", "", t, count=1)
     + "\n| `N_CLK_DOMAIN_P` | elsewhere |\n",
     1, r"guide: missing N_CLK_DOMAIN_P"),
    # --- diagram 21 inventory group
    ("diagram-missing-entry", DIAG,
     lambda t: once(t, "N_AUDIO_UNIT_P · N_CLK_DOMAIN_P · N_CONTROL_P",
                    "N_AUDIO_UNIT_P · N_CONTROL_P"),
     1, r"diagram: missing N_CLK_DOMAIN_P"),
    ("diagram-extra-entry", DIAG,
     lambda t: once(t, "<text x=\"464\" y=\"560\">SRP_DOM_DEF_VID_P</text>",
                    "<text x=\"464\" y=\"560\">SRP_DOM_DEF_VID_P · BOGUS_P</text>"),
     1, r"diagram: extra BOGUS_P"),
    ("diagram-duplicate-entry", DIAG,
     lambda t: once(t, "<text x=\"464\" y=\"524\">NVM_RS_TMO_CYC_P</text>",
                    "<text x=\"464\" y=\"524\">NVM_RS_TMO_CYC_P · CLK_HZ_P</text>"),
     1, r"diagram: duplicate CLK_HZ_P \(2 occurrences\)"),
    ("diagram-empty-inventory", DIAG,
     lambda t: re.sub(r"(<g id=\"integration-parameters\"[^>]*>)[\s\S]*?(</g>)", r"\1\2", t, count=1),
     1, r"diagram: parsed no parameters"),
    ("diagram-no-group", DIAG,
     lambda t: t.replace('id="integration-parameters"', 'id="renamed"', 1),
     1, r"diagram: expected one integration-parameters inventory group"),
    ("diagram-two-groups", DIAG,
     lambda t: t.replace("</svg>", '<g id="integration-parameters"></g></svg>', 1),
     1, r"diagram: expected one integration-parameters inventory group"),
    ("diagram-malformed-xml", DIAG,
     lambda t: t.replace("</svg>", "", 1),
     1, r"diagram: "),
    ("diagram-name-outside-group-only", DIAG,
     lambda t: once(t, "N_AUDIO_UNIT_P · N_CLK_DOMAIN_P · N_CONTROL_P",
                    "N_AUDIO_UNIT_P · N_CONTROL_P").replace(
                        "described by CLK_HZ_P", "described by CLK_HZ_P, N_CLK_DOMAIN_P", 1),
     1, r"diagram: missing N_CLK_DOMAIN_P"),
    # --- robustness beyond the listed controls (observational)
    ("OBS-diagram-hidden-text-counts", DIAG,
     lambda t: once(t, "N_AUDIO_UNIT_P · N_CLK_DOMAIN_P · N_CONTROL_P",
                    "N_AUDIO_UNIT_P · N_CONTROL_P").replace(
                        "<text x=\"464\" y=\"560\">SRP_DOM_DEF_VID_P</text>",
                        "<text x=\"464\" y=\"560\">SRP_DOM_DEF_VID_P</text>"
                        "<text display=\"none\">N_CLK_DOMAIN_P</text>", 1),
     None, r""),
]


def main():
    shutil.rmtree(SCRATCH, ignore_errors=True)
    SCRATCH.mkdir(parents=True)
    bad = 0
    for name, rel, mutate, exp_rc, exp_re in PROBES:
        d = SCRATCH / name
        d.mkdir()
        paths = {}
        for key, r in (("top", TOP), ("guide", GUIDE), ("diagram", DIAG)):
            dst = d / Path(r).name
            shutil.copyfile(ROOT / r, dst)
            paths[key] = dst
        if rel == "TOP-DELETE":
            paths["top"].unlink()
        elif rel is not None:
            dst = d / Path(rel).name
            src = dst.read_text(encoding="utf-8")
            new = mutate(src)
            assert new != src, f"{name}: mutation did not apply"
            dst.write_text(new, encoding="utf-8")
        p = subprocess.run([sys.executable, str(CHECKER), "--top", str(paths["top"]),
                            "--guide", str(paths["guide"]), "--diagram", str(paths["diagram"])],
                           capture_output=True, text=True)
        out = (p.stdout + p.stderr).strip()
        if exp_rc is None:
            verdict = "OBSERVED"
        else:
            ok = p.returncode == exp_rc and re.search(exp_re, out) is not None \
                and "Traceback" not in out
            verdict = "PASS" if ok else "UNEXPECTED"
            bad += not ok
        print(f"=== {verdict} {name} rc={p.returncode} expected_rc={exp_rc}")
        print("\n".join("    " + line for line in out.splitlines()))
    print(f"probes: {len(PROBES)} run, {bad} unexpected")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
