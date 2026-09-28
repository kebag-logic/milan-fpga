#!/usr/bin/env python3
"""Disposable controls on the F1 derivation, one fresh copy of <pristine> each.
Usage: controls.py <pristine-clone> <scratch-dir> [name...]
Each control edits one anchor that must match exactly once, then runs
`pp_srcs.py --check` and the declaration suite and records both rcs."""
import shutil, subprocess, sys
from pathlib import Path

TEST = "sw/builder/test_declarations.py"
NEW = '''    # Find the authority by its package declaration so source moves stay valid.
    sources = [(ROOT / path).read_text() for path in pp_sources()]
    packages = [source for source in sources
                if re.search(r"^\\s*package\\s+pp_adp_pkg\\s*;", source, re.M)]
    assert len(packages) == 1, "expected one pp_adp_pkg in derived processor sources"
    matches = re.findall(r"ADP_ENTITY_CAPS_C\\s*=\\s*32'h([0-9A-Fa-f_]+)", packages[0])
'''
OLD = '''    # The descriptor's authority supplies the only legal capabilities value.
    source = (ROOT / "protocol-processor/hdl/adp/pp_adp_pkg.sv").read_text()
    matches = re.findall(r"ADP_ENTITY_CAPS_C\\s*=\\s*32'h([0-9A-Fa-f_]+)", source)
'''
PKG = "protocol-processor/hdl/adp/pp_adp_pkg.sv"
CONTROLS = {
    # the assignment's removed-derivation control: the 44d3ae3b literal read
    "C1_revert_to_literal": [(TEST, NEW, OLD)],
    # the derived list loses the package: the suite must refuse, not skip
    "C2_package_dropped_from_derived_list": [(
        "scripts/pp_srcs.py", "EXCLUDE: dict[str, str] = {}",
        'EXCLUDE: dict[str, str] = {"pp_adp_pkg": "control"}')],
    # the package declaration renamed: the lookup must find none and refuse
    "C3_package_renamed": [(PKG, "package pp_adp_pkg;", "package pp_adp_pkg_x;")],
    # the constant changed in the authority: the independent read must follow
    # it (the suite stays consistent with the builder's own reader)
    "C4_authority_value_changed": [(PKG, "32'h0000_C588", "32'h0000_C580")],
    # the same with AEM_SUPPORTED kept: a legal alternative value
    "C4b_authority_value_changed_legal": [(PKG, "32'h0000_C588", "32'h0000_C589")],
    "C4c_authority_value_changed_legal": [(PKG, "32'h0000_C588", "32'h0000_C5C8")],
    # the constant duplicated in the found package: the one-match pin bites
    "C5_constant_duplicated": [(PKG, "  localparam logic [31:0] ADP_ENTITY_CAPS_C = 32'h0000_C588;",
        "  localparam logic [31:0] ADP_ENTITY_CAPS_C = 32'h0000_C588;\n"
        "  // ADP_ENTITY_CAPS_C = 32'h0000_C588;")],
    # contrast for C4b: the test stops reading the authority (value frozen);
    # the builder's own reader then diverges, so a live read is what C4b passed on
    "C6_frozen_value_with_C4b": [
        (TEST, "    caps = int(matches[0], 16)\n", "    caps = 0x0000C588\n"),
        (PKG, "32'h0000_C588", "32'h0000_C589")],
    # C7 (special-cased in main): the processor submodule is not checked out;
    # the suite must fail loudly, never pass on an empty derived list
}

def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=1800)
    lines = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    return r.returncode, lines

def main():
    pristine, scratch = Path(sys.argv[1]), Path(sys.argv[2])
    for name in sys.argv[3:] or list(CONTROLS) + ["C7_submodule_absent"]:
        tree = scratch / name
        if tree.exists():
            shutil.rmtree(tree)
        shutil.copytree(pristine, tree, symlinks=True)
        # the submodule gitfiles are relative, so the copy is self-contained
        if name == "C7_submodule_absent":
            shutil.rmtree(tree / "protocol-processor")
            (tree / "protocol-processor").mkdir()
        for rel, old, new in CONTROLS.get(name, []):
            f = tree / rel
            text = f.read_text()
            assert text.count(old) == 1, (name, rel, text.count(old))
            f.write_text(text.replace(old, new))
        rc1, out1 = run([sys.executable, "-B", "scripts/pp_srcs.py", "--check"], tree)
        rc2, out2 = run([sys.executable, "-B", "test_declarations.py"], tree / "sw/builder")
        bad = [l for l in out1 if "names submodule source" in l or l.startswith("FAIL") or "PROSE_OK" in l]
        err = [l for l in out2 if "Error" in l or l.startswith("assert")]
        print(f"{name}\tpp_srcs_check_rc={rc1}\t{(bad or out1[-1:] or [''])[0][:260]}", flush=True)
        print(f"{name}\ttest_declarations_rc={rc2}\t{(err[-1] if err else (out2[-1] if out2 else ''))[:260]}", flush=True)
        shutil.rmtree(tree)

if __name__ == "__main__":
    main()
