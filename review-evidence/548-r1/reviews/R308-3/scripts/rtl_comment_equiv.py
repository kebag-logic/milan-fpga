"""Prove every tracked HDL file (.sv/.svh/.v/.vh) is identical between two
revisions once comments are removed, and that a planted functional change is
detected. Usage: python rtl_comment_equiv.py <repo> <rev-a> <rev-b>"""
import subprocess
import sys

HDL = (".sv", ".svh", ".v", ".vh")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True,
                          capture_output=True).stdout


def strip(src: str) -> str:
    """Remove // and /* */ comments outside string literals, then drop
    blank lines and trailing whitespace so a comment-only line vanishes."""
    out, i, n = [], 0, len(src)
    in_str = False
    while i < n:
        c = src[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(src[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
        elif c == '"':
            in_str = True
            out.append(c)
            i += 1
        elif src.startswith("//", i):
            j = src.find("\n", i)
            i = n if j < 0 else j
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2)
            seg = src[i:n if j < 0 else j + 2]
            out.append("\n" * seg.count("\n"))
            i = n if j < 0 else j + 2
        else:
            out.append(c)
            i += 1
    lines = [ln.rstrip() for ln in "".join(out).split("\n")]
    return "\n".join(ln for ln in lines if ln.strip())


def files(repo, rev):
    out = git(repo, "ls-tree", "-r", "--name-only", rev).decode().split("\n")
    return {p for p in out if p.endswith(HDL)}


def main():
    repo, a, b = sys.argv[1:4]
    fa, fb = files(repo, a), files(repo, b)
    if fa != fb:
        print("HDL file set differs:", sorted(fa ^ fb))
        return 1
    diff = []
    for p in sorted(fa):
        sa = git(repo, "show", f"{a}:{p}").decode("utf-8", "replace")
        sb = git(repo, "show", f"{b}:{p}").decode("utf-8", "replace")
        if strip(sa) != strip(sb):
            diff.append(p)
    raw = [p for p in sorted(fa)
           if git(repo, "rev-parse", f"{a}:{p}") != git(repo, "rev-parse", f"{b}:{p}")]
    print(f"{len(fa)} tracked HDL files; byte-changed {len(raw)}: {raw}")
    print(f"comment-stripped differences: {len(diff)} {diff}")
    # control: a nonzero diagnostic tie must be detected by the same stripper
    p = "hdl/milan/milan_datapath.sv"
    sb = git(repo, "show", f"{b}:{p}").decode()
    tie = "assign aecp_ctlr_diag = 32'd0;"
    assert sb.count(tie) == 1, "tie line not unique"
    mut = sb.replace(tie, "assign aecp_ctlr_diag = 32'h01001001;")
    ctl = strip(mut) != strip(sb)
    print(f"control (nonzero aecp_ctlr_diag tie) detected: {ctl}")
    # control: a comment-only edit must NOT be detected
    cmt = sb.replace(tie, tie + " // probe comment")
    ctl2 = strip(cmt) == strip(sb)
    print(f"control (comment-only edit) ignored: {ctl2}")
    return 0 if (not diff and ctl and ctl2) else 1


sys.exit(main())
