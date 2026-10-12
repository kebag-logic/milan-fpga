"""Apply one named mutant to a disposable copy's sw/firmware/ctrl/test/ctrl_build.py (each edit must match once).

Usage: python3 -I mutants.py <copy> <mutant>      (python3 -I mutants.py --list)
"""
import sys
from pathlib import Path

MUTANTS = {
    # round 16's match: a superproject remote key refused only with a named subsection
    "named_only": [("if f\"{section}.{variable}\" in SUPERPROJECT_REFUSED and\n",
                    "if f\"{section}.{variable}\" in SUPERPROJECT_REFUSED and (section != \"remote\" or _) and\n")],
    # a remote key with a named or an empty subsection refused, none not
    "sub_present_only": [("if f\"{section}.{variable}\" in SUPERPROJECT_REFUSED and\n",
                          "if f\"{section}.{variable}\" in SUPERPROJECT_REFUSED and (section != \"remote\" or _ is not None) and\n")],
    # the parser reads an empty subsection as none
    "parser_empty_is_none": [("return section, subsection if dot else None, variable",
                              "return section, subsection if dot and subsection else None, variable")],
    # the stack's allowlist gives an empty subsection the named family `*`
    "family_empty_is_named": [("named = \"*\" if subsection else '\"\"'", "named = \"*\"")],
    # the superproject's keys not judged at all
    "no_superproject_check": [("    superproject_configured(root)\n    entry = git(",
                               "    entry = git(")],
    # the superproject's keys judged after the index is read
    "superproject_check_late": [("    superproject_configured(root)\n    entry = git(root, \"ls-files\", \"--stage\", \"--\", rel).stdout.split()\n",
                                 "    entry = git(root, \"ls-files\", \"--stage\", \"--\", rel).stdout.split()\n    superproject_configured(root)\n")],
    # the stack's allowlist not checked
    "no_stack_allowlist": [("    configured(stack)\n    head = git(", "    head = git(")],
    # no object hashed against its id
    "no_hash_check": [("    if held != oid:\n", "    if False:\n")],
    # the helper's core.fsmonitor=false dropped
    "no_helper_config": [("[\"git\", \"-c\", HELPER_CONFIG, \"-C\", str(directory), *args]",
                          "[\"git\", \"-C\", str(directory), *args]")],
    # GIT_NO_LAZY_FETCH dropped
    "no_lazy_env": [(", \"GIT_NO_LAZY_FETCH\": \"1\"}", "}")],
    # both defence-in-depth settings dropped
    "no_defence_in_depth": [("[\"git\", \"-c\", HELPER_CONFIG, \"-C\", str(directory), *args]",
                             "[\"git\", \"-C\", str(directory), *args]"),
                            (", \"GIT_NO_LAZY_FETCH\": \"1\"}", "}")],
    # the superproject's check reads only the local scope (work tree's and command's left out)
    "super_local_only": [("if f\"{section}.{variable}\" in SUPERPROJECT_REFUSED and\n",
                          "if f\"{section}.{variable}\" in SUPERPROJECT_REFUSED and scope == \"local\" and\n")],
}

if sys.argv[1] == "--list":
    print("\n".join(MUTANTS))
    sys.exit(0)
target = Path(sys.argv[1]) / "sw/firmware/ctrl/test/ctrl_build.py"
text = target.read_text(encoding="utf-8")
for old, new in MUTANTS[sys.argv[2]]:
    if text.count(old) != 1:
        sys.exit(f"mutant {sys.argv[2]}: {old!r} matches {text.count(old)} times")
    text = text.replace(old, new)
target.write_text(text, encoding="utf-8")
print(f"mutant {sys.argv[2]} applied to {target}")
