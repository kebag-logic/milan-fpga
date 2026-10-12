"""Apply one named mutant to a tree's ctrl_build.py by exact replacement (each anchor must occur exactly once).

usage: python3 -I mutate.py TREE NAME
"""
import sys
from pathlib import Path

GITLINK = '    superproject_configured(root)\n    entry = git(root, "ls-files", "--stage", "--", rel).stdout.split()\n'
MUTANTS = {
    "none": [],
    "no_superproject_check": [(GITLINK, GITLINK.split("\n", 1)[1])],
    "superproject_check_after_index_read": [(GITLINK, GITLINK.split("\n", 1)[1] + "    superproject_configured(root)\n")],
    "no_object_hash_check": [("    if held != oid:\n", "    if False:\n")],
    "no_stack_allowlist": [("    configured(stack)\n    head = ", "    head = ")],
    "stack_allowlist_after_object_reads": [("    configured(stack)\n    head = ", "    head = "),
                                           ("    want = pinned_tree(stack, pin, algorithm)\n",
                                            "    want = pinned_tree(stack, pin, algorithm)\n    configured(stack)\n")],
    "no_helper_core_fsmonitor_false": [('["git", "-c", HELPER_CONFIG, "-C", str(directory)', '["git", "-C", str(directory)')],
    "no_git_no_lazy_fetch": [(', "GIT_NO_LAZY_FETCH": "1"}', '}')],
    "superproject_uploadpack_not_refused": [('"remote.*.partialclonefilter",\n                        "remote.*.uploadpack", ',
                                             '"remote.*.partialclonefilter",\n                        ')],
    "superproject_worktree_scope_ignored": [("               if named in SUPERPROJECT_REFUSED and not",
                                             "               if scope != \"worktree\" and named in SUPERPROJECT_REFUSED and not")],
    "superproject_over_refuses_include_path": [('"core.sshcommand", "core.fsmonitor")',
                                                '"core.sshcommand", "core.fsmonitor", "include.path")')],
    "stack_over_refuses_branch_merge": [('"branch.*.remote", "branch.*.merge", ', '"branch.*.remote", ')],
    "tree_parse_ignores_subtrees": [('            if kind == "tree":\n                trees.append', '            if False:\n                trees.append')],
}
tree, name = Path(sys.argv[1]), sys.argv[2]
target = tree / "sw/firmware/ctrl/test/ctrl_build.py"
text = target.read_text(encoding="utf-8")
for old, new in MUTANTS[name]:
    if text.count(old) != 1:
        sys.exit(f"anchor not found exactly once for {name}: {old!r}")
    text = text.replace(old, new)
target.write_text(text, encoding="utf-8")
print(f"mutant {name} applied to {target}")
