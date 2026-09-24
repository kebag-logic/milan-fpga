"""Compare tracked RTL at two revisions, retaining strings and escaped names."""

import hashlib
import re
import subprocess
import sys


def git(*args):
    return subprocess.run(
        ["rtk", "proxy", "git", *args], capture_output=True,
        timeout=120, check=True,
    ).stdout


def rtl_paths(revision):
    paths = git("ls-tree", "-r", "--name-only", "-z", revision).split(b"\0")
    return sorted(p.decode() for p in paths if p.endswith((b".sv", b".svh", b".v", b".vh")))


LEXICAL = re.compile(rb'"(?:\\.|[^"\\])*"|\\[^\s]+|//[^\n]*|/\*.*?\*/', re.DOTALL)


def comment_free(source):
    def replace(match):
        value = match.group()
        if value.startswith((b"//", b"/*")):
            return re.sub(rb"[^\n]", b" ", value)
        return value

    cleaned = LEXICAL.sub(replace, source)
    return b"\n".join(line.rstrip() for line in cleaned.splitlines() if line.strip())


def main():
    base, head = sys.argv[1:]
    base_paths, head_paths = rtl_paths(base), rtl_paths(head)
    assert base_paths == head_paths, "RTL file inventory changed"
    changed = 0
    for path in base_paths:
        before = git("show", f"{base}:{path}")
        after = git("show", f"{head}:{path}")
        if before == after:
            continue
        changed += 1
        left, right = comment_free(before), comment_free(after)
        assert left == right, f"DIFFERENT: {path}"
        digest = hashlib.sha256(left).hexdigest()
        print(f"IDENTICAL {path}: base/head comment-free sha256 {digest}")

    # A changed diagnostic value must not disappear with its comment.
    tie_path = "hdl/milan/milan_datapath.sv"
    source = git("show", f"{base}:{tie_path}")
    original = b"assign aecp_ctlr_diag = 32'd0;"
    assert source.count(original) == 1
    mutant = source.replace(original, b"assign aecp_ctlr_diag = 32'd1;")
    assert comment_free(source) != comment_free(mutant)
    print("CONTROL: nonzero diagnostic tie is DIFFERENT (memory only)")

    # Independent diff check: every RTL line added or removed is //! prose.
    diff = git("diff", "--no-ext-diff", "--no-textconv", "--no-renames",
               "--unified=0", base, head, "--", *base_paths)
    for line in diff.splitlines():
        if line.startswith((b"+++", b"---")):
            continue
        if line.startswith((b"+", b"-")):
            assert line[1:].lstrip().startswith(b"//!"), line
    print("DIFF: every added/removed RTL line is a //! comment")
    print(f"IDENTICAL: {len(base_paths)} tracked RTL files; {changed} comment-only changes; "
          f"{len(base_paths) - changed} raw byte-identical files")
    print(f"Base: {base}")
    print(f"Head: {head}")


if __name__ == "__main__":
    main()
