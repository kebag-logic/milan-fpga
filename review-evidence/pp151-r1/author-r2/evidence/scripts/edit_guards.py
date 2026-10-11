"""Turn every elaboration guard in <root>/hdl into a module-scope $fatal(1, ...).
Same-line edits only, so no line in any file moves."""
import pathlib, re, sys
root = pathlib.Path(sys.argv[1])
n = 0
for f in sorted((root / "hdl").rglob("*.sv")):
    text = f.read_text()
    lines = text.split("\n")
    changed = False
    for i, ln in enumerate(lines):
        m = re.match(r"^(\s*)\$error\(", ln)
        if m:
            lines[i] = ln.replace("$error(", "$fatal(1, ", 1)
            n += 1; changed = True
    if f.name == "KL_pp_acmp_listener.sv":
        old = ["  initial begin : parameter_checks",
               "    if (STRM_TIMEOUT_CYC_P == 0)",
               '      $fatal(1, "STRM_TIMEOUT_CYC_P must be greater than zero");',
               "  end"]
        new = ["  //! at module scope: Verilator lint and xelab never see a guard in an initial block",
               "  if (STRM_TIMEOUT_CYC_P == 0) begin : g_strm_tmo_check",
               '    $fatal(1, "STRM_TIMEOUT_CYC_P must be greater than zero");',
               "  end"]
        k = lines.index(old[0])
        assert lines[k:k + 4] == old, lines[k:k + 4]
        lines[k:k + 4] = new
        n += 1; changed = True
    if changed:
        f.write_text("\n".join(lines))
print(f"{n} guards edited")
