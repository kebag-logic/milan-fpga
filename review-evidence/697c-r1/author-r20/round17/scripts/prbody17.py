"""Scratch (round 17): apply the round-17 edits to PR-BODY.md, each anchor required exactly once.
usage: prbody17.py <PR-BODY.md> <round-17 section file> <status file> <unit summary> <review-ready comment id>"""
import sys
from pathlib import Path

body_path = Path(sys.argv[1])
body = body_path.read_text(encoding="utf-8")
section = Path(sys.argv[2]).read_text(encoding="utf-8").replace("UNIT_SUMMARY", sys.argv[4])
status = Path(sys.argv[3]).read_text(encoding="utf-8").replace("UNIT_SUMMARY", sys.argv[4])
comment = sys.argv[5]
status = status.replace("REVIEW_READY_ID", comment)
section = section.replace("REVIEW_READY_ID", comment)
HEAD = "5b4ea55160c5ee34263e24140f960c4f03d923bc"
OLD = "516a69be9afba02670e37874294bd1f45ccb9316"


def once(old: str, new: str) -> None:
    global body
    count = body.count(old)
    assert count == 1, (count, old[:120])
    body = body.replace(old, new)


# Contents
once("- **[Round 16](#round-16)** — How the superproject's own configuration is held: a promisor remote, its transport "
     "and an fsmonitor refused by name before the gitlink is read.\n",
     "- **[Round 16](#round-16)** — How the superproject's own configuration is held: a promisor remote, its transport "
     "and an fsmonitor refused by name before the gitlink is read.\n"
     "- **[Round 17](#round-17)** — How one parser reads both repositories' keys, the superproject's refused by section "
     "and variable whatever the subsection, and how dev `c6bd08c6` merges.\n")

# Status: the round-16 block becomes a one-paragraph summary under the round-17 block.
start = body.index("## Status\n\n") + len("## Status\n\n")
end = body.index("Round 15: GREEN locally at ")
old_status = body[start:end]
assert old_status.startswith(f"GREEN locally at `{OLD}`"), old_status[:80]
round16 = (f"Round 16: GREEN locally at `{OLD}` (round 16, one commit on `44eef11f`): before the gitlink is read, the "
           "superproject's own configuration refused by name for a promisor remote, its transport and an fsmonitor "
           "named with a subsection (R584-14 found the subsection-less and empty-subsection spellings passed; round 17 "
           "judges them by section and variable); R585-14's two probes refused with `RAN=0` on Git 2.56.0 and upstream "
           "2.43.0; 102 pin controls, 4 of them new, 0 misbehaved; 35 of 35 RV32 images byte-identical to dev "
           "`c20c85bd`'s. In the runner's replica: `firmware-boundary` PASS in 696 s (105, 102 and 4 controls), "
           "`firmware-verilator` PASS in 495 s (6, 102 and 4), `firmware-unit`'s steps every one rc 0 in 2074 s "
           "(`mutants: 506 of 506 caught`) — REVIEW READY in #697 comment "
           "[6120798872](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6120798872).\n\n")
body = body[:start] + status + "\n" + round16 + body[end:]

# Round 15's open item (a)
once("round 16 refuses those keys by name);", "round 16 refuses those keys by name, and round 17 judges them by section "
     "and variable, whatever their subsection);")

# R585-15-RES-2
once("`firmware-unit`'s steps {every one rc 0 in 2074 s: `mutants: 506 of 506 caught`, the firmware gate's 915 verdict "
     "lines `[ok]` and equal to round 15's, coverage 100 % in 30 files with every row equal}.",
     "`firmware-unit`'s steps: every one rc 0 in 2074 s, `mutants: 506 of 506 caught`, the firmware gate's 915 verdict "
     "lines `[ok]` and equal to round 15's, coverage 100 % in 30 files with every row equal.")

# The Round 17 section, before the references.
once("## Authoritative references\n", section + "\n## Authoritative references\n")

# References
once("and the [round 16 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6119960001).",
     "the [round 16 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6119960001) and the "
     "[round 17 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6121496568).")
refs = body.index("- [Control firmware](")
line_end = body.index("\n", refs)
line = body[refs:line_end]
assert line.count(OLD) == 5, line.count(OLD)
body = body[:refs] + line.replace(OLD, HEAD) + body[line_end:]

# How to validate
once("python3 sw/firmware/ctrl/test/ctrl_image.py --base c20c85bddd4ec5a054be42b55fc291a3b4c7f7d8",
     "python3 sw/firmware/ctrl/test/ctrl_image.py --base c6bd08c6f52632c6d33d834ce842ac3cf63f29cc")
once("- `--base c20c85bd`: `+0` in every section at both shapes;", "- `--base c6bd08c6`: `+0` in every section at both shapes;")
once("0 finding(s), 105 boundary, 102 pin and 4 figure controls, 0 misbehaved`",
     "0 finding(s), 105 boundary, 106 pin and 4 figure controls, 0 misbehaved`")
once("`--only verilator`: 6 boundary, 102 pin and 4 figure controls", "`--only verilator`: 6 boundary, 106 pin and 4 figure controls")
once("the twenty-three object-store, attribute and configuration controls",
     "the twenty-seven object-store, attribute and configuration controls")
once("four states of a superproject's own configuration, its gitlink read,",
     "seven states of a superproject's own configuration, its gitlink read,")
once("and the same over ssh through `core.sshCommand`; an included file",
     "and the same over ssh through `core.sshCommand`; that sparse superproject beside a promisor remote declared by "
     "`remote.promisor` or `remote.partialCloneFilter` without a subsection, or by `remote \"\".promisor`, reached through "
     "a recorder by an `ext::` URL rewrite, each naming that one key; an included file")
once("and thirteen states of the stack's own configuration,",
     "and fourteen states of the stack's own configuration, `submodule \"\".active` (an empty subsection) among them,")

# Known limitations
old16 = body[body.index("- Round 16: the superproject's own configuration is held by the keys it may not hold"):]
old16 = old16[:old16.index("\n") + 1]
new16 = ("- Round 16: the superproject's own configuration is held by the keys it may not hold "
         "(`ctrl_build.SUPERPROJECT_REFUSED`: a promisor remote, its transport and `core.fsmonitor`), refused by name "
         "before the gitlink is read from its index; from round 17 each is judged by its section and variable, whatever "
         "its subsection, so the superproject declares no promisor remote in any key spelling Git reads. Its other keys "
         "are not judged (an allowlist would refuse `actions/checkout`'s `http.<url>.extraheader`); 28 of them that name "
         "a program, in a plain and a sparse superproject, start nothing while the gitlink is read, on Git 2.56.0 and "
         "upstream 2.43.0 (round 16's scratch probe). The stack's own configuration is held by its allowlist (round 15). "
         "`GIT_NO_LAZY_FETCH=1` and `core.fsmonitor=false` are defence in depth; where a Git does not honour "
         "`GIT_NO_LAZY_FETCH` (an upstream release before 2.45.0 other than the CVE-2024-32465 maintenance releases, such "
         "as 2.43.0 or 2.44.0), these two checks are what holds.\n"
         "- Round 17: one parser (`ctrl_build.parsed_key`) splits both repositories' keys into section, subsection and "
         "variable as Git's own `parse_config_key` does. The stack's allowlist lists no family with an empty subsection, "
         "so a key such as `submodule \"\".active` is refused by its name, failing closed; Git writes none.\n")
once(old16, new16)

assert "on any Git" not in body and "whatever a Git version" not in body and "whatever it makes of" not in body
body_path.write_text(body, encoding="utf-8")
print(f"PR-BODY.md: {len(body.encode())} bytes")
